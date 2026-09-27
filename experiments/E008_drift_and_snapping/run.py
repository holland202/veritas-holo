#!/usr/bin/env python3
"""E008 - registered in PREREG.md. python experiments/E008_drift_and_snapping/run.py [--json OUT]"""
import argparse, json, os, platform, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import core  # noqa: E402

SEEDS = (21, 22, 23)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rows = {}
    for s in SEEDS:
        r = {}
        r["F1_acc_1e6"], r["F1_dev_1e6"] = core.run(s, 10**6, 0, 0, n=8)
        r["F1_dev_1e3"] = core.run(s, 10**3, 0, 0, n=8)[1]
        r["F1_dev_1e5"] = core.run(s, 10**5, 0, 0, n=8)[1]
        r["F2_acc"] = core.run(s, 10**4, 1e-2, 0)[0]
        r["F3_acc"], r["F3_dev"] = core.run(s, 10**5, 1e-2, 1)
        r["F4_sparse_acc"] = core.run(s, 10**4, 0.1, 10)[0]
        r["F4_every_acc"] = core.run(s, 10**4, 0.1, 1)[0]
        rows[s] = r
        print(f"seed {s}: " + ", ".join(f"{k} {v:.4g}" for k, v in r.items()), flush=True)
    R = rows.values()
    v = {
        "F1": (all(r["F1_dev_1e6"] < 1e-8 and r["F1_acc_1e6"] == 1.0 and 10 <= r["F1_dev_1e5"] / r["F1_dev_1e3"] <= 1000
                   for r in R), "max dev at 1e6 " + ", ".join(f"{r['F1_dev_1e6']:.3g}" for r in R)
               + "; growth 1e3->1e5 " + ", ".join(f"{r['F1_dev_1e5'] / r['F1_dev_1e3']:.1f}x" for r in R)),
        "F2": (all(r["F2_acc"] <= 0.2 for r in R), "no snapping, delta 1e-2, L 1e4: " + ", ".join(f"{r['F2_acc']:.4f}" for r in R)),
        "F3": (all(r["F3_acc"] == 1.0 and r["F3_dev"] == 0 for r in R),
               "snap every step, delta 1e-2, L 1e5: " + ", ".join(f"{r['F3_acc']:.4f} (dev {r['F3_dev']:.1g})" for r in R)),
        "F4": (all(r["F4_sparse_acc"] <= 0.2 and r["F4_every_acc"] == 1.0 for r in R),
               "delta 0.1: snap every 10 " + ", ".join(f"{r['F4_sparse_acc']:.4f}" for r in R)
               + "; snap every step " + ", ".join(f"{r['F4_every_acc']:.4f}" for r in R)),
    }
    print(f"VERITAS-HOLO E008 | seeds {SEEDS} | {platform.machine()} | Python {platform.python_version()} | NumPy {np.__version__}")
    for k, (ok, d) in v.items():
        print(f"{'HELD  ' if ok else 'FAILED'} {k}  {d}")
    held = sum(ok for ok, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held")
    if a.json:
        json.dump({"experiment": "E008", "rows": {str(k): x for k, x in rows.items()},
                   "verdicts": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in v.items()}},
                  open(a.json, "w"), indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
