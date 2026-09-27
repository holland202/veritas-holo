#!/usr/bin/env python3
"""E009 - registered in PREREG.md. python experiments/E009_blind_check_lowprecision/run.py [--partial F] [--json OUT]"""
import argparse, json, os, platform, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
import core  # noqa: E402

SEEDS, THRESH = list(range(501, 541)), 0.32


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    done = {}
    if a.partial and os.path.exists(a.partial):
        for ln in open(a.partial, encoding="utf-8"):
            r = json.loads(ln); done[r["seed"]] = r
    todo = [s for s in SEEDS if s not in done]
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(core.one, todo):
            done[r["seed"]] = r
            if a.partial:
                open(a.partial, "a").write(json.dumps(r, sort_keys=True) + "\n")
    runs = [done[s] for s in SEEDS]
    ok = lambda r: r["f64_160"] >= 0.99  # noqa: E731
    acc = [r for r in runs if r["train_residual"] < THRESH]
    rej = [r for r in runs if r["train_residual"] >= THRESH]
    wins = [r for r in runs if ok(r)]
    print(f"VERITAS-HOLO E009 | seeds {SEEDS[0]}-{SEEDS[-1]} | {platform.machine()} | Python {platform.python_version()}")
    print(f"{'seed':>4} {'residual':>10} {'decision':>8} {'f64 L160':>9} {'f16 L1e4':>9}")
    for r in runs:
        print(f"{r['seed']:>4} {r['train_residual']:10.3g} {'ACCEPT' if r['train_residual'] < THRESH else 'REJECT':>8} "
              f"{r['f64_160']:9.4f} {r['f16raw10000']:9.4f}")
    pa = sum(ok(r) for r in acc) / len(acc) if acc else float("nan")
    pr = sum(ok(r) for r in rej) / len(rej) if rej else float("nan")
    v = {
        "B1": (bool(acc) and pa >= 0.95, f"accepted {len(acc)}, succeeded {sum(ok(r) for r in acc)} ({pa:.4f} >= 0.95)"),
        "B2": (not rej or pr <= 0.10, f"rejected {len(rej)}, succeeded {sum(ok(r) for r in rej)} ({pr:.4f} <= 0.10)"),
        "B3": (len(acc) >= 5 and len(rej) >= 5, f"{len(acc)} accepted, {len(rej)} rejected (each >= 5)"),
        "B4": (bool(wins) and all(r["f16raw10000"] >= 0.99 for r in wins),
               f"float16 at L=10000 on the {len(wins)} successful runs: min {min((r['f16raw10000'] for r in wins), default=float('nan')):.4f} (>= 0.99)"),
    }
    for k, (g, d) in v.items():
        print(f"{'HELD  ' if g else 'FAILED'} {k}  {d}")
    held = sum(g for g, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held")
    if a.json:
        json.dump({"experiment": "E009", "threshold": THRESH, "runs": runs,
                   "verdicts": {k: {"held": bool(g), "detail": d} for k, (g, d) in v.items()}}, open(a.json, "w"), indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
