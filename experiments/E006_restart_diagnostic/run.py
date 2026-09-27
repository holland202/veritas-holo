#!/usr/bin/env python3
"""E006 (E005-U1) - does a relator score computed from the trained operators alone pick successful runs?
Registered in PREREG.md (D1-D5) before this code.

  python experiments/E006_restart_diagnostic/run.py [--jobs 2] [--json OUT.json]
Each seed: train, compute the score, record ACCEPT/REJECT, and only then build and read test words.
"""
import argparse
import importlib.util
import json
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "experiments", "E004_group_state"))
_spec = importlib.util.spec_from_file_location("e005run", os.path.join(ROOT, "experiments", "E005_learned_state", "run.py"))
e005 = importlib.util.module_from_spec(_spec)
sys.modules["e005run"] = e005
_spec.loader.exec_module(e005)
from veritas_holo.learn import all_words, train_operators  # noqa: E402

SEEDS, THRESHOLD, GROUP = list(range(41, 81)), 5, 4
WORDS = all_words(2, 8)
Y = np.array([int(e005.e004.labels(w[None])[0]) for w in WORDS])


def relator_score(ops):
    counts = []
    for name in e005.RELATORS:
        m = np.eye(ops.shape[1], dtype=complex)
        for a in e005.relator_letters(name):
            m = ops[a] @ m
        counts.append(int(np.sum(abs(np.linalg.eigvals(m) - 1) < 1e-2)))
    return min(counts), counts


def one(seed):
    t0 = time.time()
    ops = train_operators(WORDS, Y, e005.DIM, np.random.default_rng(seed))
    score, counts = relator_score(ops)
    decision = "ACCEPT" if score >= THRESHOLD else "REJECT"
    sealed = {"seed": seed, "score": score, "counts": counts, "decision": decision, "decided_at": time.time()}
    # --- the test is built and read only after the decision is fixed ---
    acc = e005.score(ops, seed)
    return {**sealed, "acc40": acc[40][0], "acc160": acc[160][0], "tested_at": time.time(),
            "seconds": time.time() - t0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    if a.jobs > 1:
        with ProcessPoolExecutor(a.jobs) as ex:
            runs = list(ex.map(one, SEEDS))
    else:
        runs = [one(s) for s in SEEDS]
    assert all(r["decided_at"] < r["tested_at"] for r in runs), "a decision was recorded after its test"
    ok = lambda r: r["acc160"] >= 0.99  # noqa: E731
    print(f"VERITAS-HOLO E006 | seeds {SEEDS[0]}-{SEEDS[-1]} | {platform.machine()} | Python {platform.python_version()} "
          f"| NumPy {np.__version__}")
    print(f"acceptance rule: relator score >= {THRESHOLD} (of 8); decisions sealed before each test "
          f"(checked: all {len(runs)} decided before tested)")
    print(f"{'seed':>4} {'score':>5} {'decision':>8} {'acc 40':>8} {'acc 160':>8}")
    for r in runs:
        print(f"{r['seed']:>4} {r['score']:>5} {r['decision']:>8} {r['acc40']:8.4f} {r['acc160']:8.4f}")
    acc_runs = [r for r in runs if r["decision"] == "ACCEPT"]
    low = [r for r in runs if r["score"] <= 3]
    band4 = [r for r in runs if r["score"] == 4]
    base = sum(ok(r) for r in runs) / len(runs)
    jobs, blind = [], []
    for g in range(0, len(runs), GROUP):
        grp = runs[g:g + GROUP]
        pick = next((i for i, r in enumerate(grp) if r["decision"] == "ACCEPT"), None)
        jobs.append((pick is not None and ok(grp[pick]), (pick + 1) if pick is not None else len(grp)))
        blind.append(ok(grp[0]))
    prec = sum(ok(r) for r in acc_runs) / len(acc_runs) if acc_runs else float("nan")
    low_rate = sum(ok(r) for r in low) / len(low) if low else float("nan")
    print(f"accepted {len(acc_runs)}: {sum(ok(r) for r in acc_runs)} succeeded; score <= 3: {len(low)}, "
          f"{sum(ok(r) for r in low)} succeeded; score 4 (no prediction): {len(band4)}, {sum(ok(r) for r in band4)} succeeded")
    print(f"base success rate {base:.4f}; policy jobs succeeded {sum(j[0] for j in jobs)}/{len(jobs)}, "
          f"blind first-seed {sum(blind)}/{len(blind)}; mean trainings per job {np.mean([j[1] for j in jobs]):.2f}")
    v = {
        "D1": (acc_runs != [] and prec >= 0.95, f"precision of ACCEPT {prec:.4f} >= 0.95"),
        "D2": (low == [] or low_rate <= 0.10, f"success among score <= 3: {low_rate:.4f} <= 0.10 ({len(low)} runs)"),
        "D3": (0.5 <= base <= 0.9, f"base success rate {base:.4f} in [0.5, 0.9]"),
        "D4": (sum(j[0] for j in jobs) >= 9, f"policy delivered a successful run in {sum(j[0] for j in jobs)} of "
                                             f"{len(jobs)} jobs (>= 9)"),
    }
    for k, (good, d) in v.items():
        print(f"{'HELD  ' if good else 'FAILED'} {k}  {d}")
    held = sum(g for g, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held (D5 reported, not scored)")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E006", "machine": platform.machine(), "python": platform.python_version(),
                       "numpy": np.__version__, "threshold": THRESHOLD, "runs": runs,
                       "jobs": [{"success": s, "trainings": n} for s, n in jobs], "blind_first_seed": blind,
                       "verdicts": {k: {"held": bool(g), "detail": d} for k, (g, d) in v.items()}},
                      fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
