#!/usr/bin/env python3
"""E005 - learn S5 state tracking from words of length <= 8, test at 40 and 160. Registered in PREREG.md (L1-L6).

  python experiments/E005_learned_state/run.py [--seeds 1 2 3 4 5] [--jobs 1] [--json OUT.json]
Exit: 0 every registered prediction held | 1 at least one did not
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "E004_group_state"))
import run as e004  # noqa: E402
from veritas_holo.learn import all_words, haar_unitary, train_operators  # noqa: E402

DIM, MAX_LEN, LENGTHS = 8, 8, (40, 160)
RELATORS = {"t^2": [0, 0], "c^5": [1] * 5, "(tc)^4": [1, 0] * 4, "(t c^-1 t c)^3": [1, 0, 1, 1, 1, 1, 0] * 3,
            "(t c^-2 t c^2)^2": [1, 1, 0, 1, 1, 1, 0] * 2}
# words act right to left in the product: holonomy(w) = U_{w_L} ... U_{w_1}; relator strings above are read as
# products of matrices left to right (t c = U_t U_c), so they are stored reversed into letter order below, and
# c^-1 = c^4, c^-2 = c^3


def relator_letters(name):
    return list(reversed(RELATORS[name]))


def score(ops, seed):
    out = {}
    for L in LENGTHS:
        rng = np.random.default_rng(100 * seed + L)
        w = rng.integers(0, 2, (8000, L))
        y = e004.labels(w)
        f = e004.holonomies(w, ops)
        out[L] = (e004.centroid_accuracy(f[:6000], y[:6000], f[6000:], y[6000:]),
                  e004.count_ceiling(w[:6000], y[:6000], w[6000:], y[6000:]))
    return out


def one_seed(seed):
    words = all_words(2, MAX_LEN)
    y = np.array([int(e004.labels(w[None])[0]) for w in words])
    t0 = time.time()
    init_rng = np.random.default_rng(seed)
    init = np.stack([haar_unitary(DIM, init_rng) for _ in range(2)])
    full = train_operators(words, y, DIM, np.random.default_rng(seed))
    t_full = time.time() - t0
    diag = train_operators(words, y, DIM, np.random.default_rng(seed), diagonal=True)
    eig = {}
    for name in RELATORS:
        m = np.eye(DIM, dtype=complex)
        for a in relator_letters(name):
            m = full[a] @ m
        eig[name] = int(np.sum(abs(np.linalg.eigvals(m) - 1) < 1e-2))
    return {"seed": seed, "full": score(full, seed), "diag": score(diag, seed), "init": score(init, seed),
            "unitarity": float(max(np.linalg.norm(o.conj().T @ o - np.eye(DIM)) for o in full)),
            "relator_eig_near_1": eig, "train_seconds": t_full, "n_words": len(words)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rep = np.stack([e004.perm_matrix(e004.T), e004.perm_matrix(e004.C)])
    rel_ok = {}
    for name in RELATORS:
        m = np.eye(5, dtype=complex)
        for x in relator_letters(name):
            m = rep[x] @ m
        rel_ok[name] = bool(np.allclose(m, np.eye(5)))
    if a.jobs > 1:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(a.jobs) as ex:
            runs = list(ex.map(one_seed, a.seeds))
    else:
        runs = [one_seed(s) for s in a.seeds]

    print(f"VERITAS-HOLO E005 | seeds {' '.join(map(str, a.seeds))} | {platform.machine()} | "
          f"Python {platform.python_version()} | NumPy {np.__version__}")
    print(f"training: all {runs[0]['n_words']} words of length 1-{MAX_LEN}; operators {DIM}x{DIM} unitary; "
          f"test at L = {LENGTHS[0]} and {LENGTHS[1]}")
    print("relators are the identity under the exact S5 representation: "
          + ", ".join(f"{k} {'yes' if v else 'NO'}" for k, v in rel_ok.items()))
    print(f"{'seed':>4} {'learned 40':>11} {'learned 160':>12} {'diag 40':>8} {'diag 160':>9} {'ceil 40':>8} "
          f"{'ceil 160':>9} {'init 40':>8} {'init 160':>9} {'min eig~1':>10} {'train s':>8}")
    for r in runs:
        print(f"{r['seed']:>4} {r['full'][40][0]:11.4f} {r['full'][160][0]:12.4f} {r['diag'][40][0]:8.4f} "
              f"{r['diag'][160][0]:9.4f} {r['diag'][40][1]:8.4f} {r['diag'][160][1]:9.4f} {r['init'][40][0]:8.4f} "
              f"{r['init'][160][0]:9.4f} {min(r['relator_eig_near_1'].values()):>7}/{DIM} {r['train_seconds']:8.0f}")
    win = [r for r in runs if r["full"][160][0] >= 0.99]
    v = {
        "L1": (len(win) >= 3, f"{len(win)} of {len(runs)} seeds reach >= 0.99 at L=160 (need >= 3)"),
        "L2": (all(r["full"][40][0] >= 0.99 for r in win),
               "those seeds at L=40: " + (", ".join(f"{r['full'][40][0]:.4f}" for r in win) or "none") + " (all >= 0.99)"),
        "L3": (all(r["diag"][L][0] <= r["diag"][L][1] + 0.02 for r in runs for L in LENGTHS),
               f"learned diagonal max excess over count ceiling "
               f"{max(r['diag'][L][0] - r['diag'][L][1] for r in runs for L in LENGTHS):+.4f} (<= +0.02)"),
        "L4": (all(r["init"][L][0] < 0.05 for r in runs for L in LENGTHS),
               f"untrained max {max(r['init'][L][0] for r in runs for L in LENGTHS):.4f} (< 0.05)"),
        "L5": (all(r["unitarity"] < 1e-10 for r in runs),
               f"max ||U'U - I|| {max(r['unitarity'] for r in runs):.2e} (< 1e-10)"),
        "L6": (all(rel_ok.values()) and all(min(r["relator_eig_near_1"].values()) >= 4 for r in win),
               f"successful seeds' min relator eigenvalues near 1: "
               f"{', '.join(str(min(r['relator_eig_near_1'].values())) for r in win) or 'none'} (each >= 4 of {DIM})"),
    }
    for k, (ok, d) in v.items():
        print(f"{'HELD  ' if ok else 'FAILED'} {k}  {d}")
    held = sum(ok for ok, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E005", "machine": platform.machine(), "python": platform.python_version(),
                       "numpy": np.__version__, "relators_exact": rel_ok,
                       "runs": [{**r, "full": {str(k): x for k, x in r["full"].items()},
                                 "diag": {str(k): x for k, x in r["diag"].items()},
                                 "init": {str(k): x for k, x in r["init"].items()}} for r in runs],
                       "verdicts": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in v.items()}},
                      fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
