#!/usr/bin/env python3
"""E004 - S5 state tracking: commuting vs relation-respecting vs relation-violating holonomy.
Registered in PREREG.md (G1-G6) before this code.

  python experiments/E004_group_state/run.py [--json OUT.json]
Exit: 0 every registered prediction held | 1 at least one did not
"""
import argparse
import itertools
import json
import os
import platform
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from veritas_holo import expi  # noqa: E402

PERMS = list(itertools.permutations(range(5)))
INDEX = {p: i for i, p in enumerate(PERMS)}
T, C = (1, 0, 2, 3, 4), (1, 2, 3, 4, 0)  # t = (0 1), c = (0 1 2 3 4) as images of 0..4
LENGTHS, SEEDS, N_TRAIN, N_TEST = (10, 40, 160), (1, 2, 3), 6000, 2000
NEXT = np.array([[INDEX[tuple(g[p[i]] for i in range(5))] for g in (T, C)] for p in PERMS])  # the TABLE arm


def perm_matrix(g):
    m = np.zeros((5, 5), dtype=complex)
    for i in range(5):
        m[g[i], i] = 1
    return m


def haar_unitary(n, rng):
    q, r = np.linalg.qr(rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n)))
    return q * (np.diag(r) / abs(np.diag(r)))


def sham_of(m, rng):
    """Same eigenvalues as m, randomised eigenvectors (P8's sham)."""
    w = np.linalg.eigvals(m)
    v = haar_unitary(m.shape[0], rng)
    return (v * w) @ v.conj().T


def labels(words):
    s = np.full(len(words), INDEX[tuple(range(5))])
    for k in range(words.shape[1]):
        s = NEXT[s, words[:, k]]
    return s


def holonomies(words, mats):
    h = np.broadcast_to(np.eye(mats.shape[1], dtype=complex), (len(words),) + mats.shape[1:]).copy()
    for k in range(words.shape[1]):
        h = mats[words[:, k]] @ h
    return h.reshape(len(words), -1)


def diag_holonomies(words, diags):
    h = np.ones((len(words), diags.shape[1]), dtype=complex)
    for k in range(words.shape[1]):
        h = diags[words[:, k]] * h
    return h


def centroid_accuracy(f_tr, y_tr, f_te, y_te):
    classes = np.unique(y_tr)
    cent = np.stack([f_tr[y_tr == k].mean(axis=0) for k in classes])
    d = (abs(f_te[:, None, :] - cent[None, :, :]) ** 2).sum(axis=2)
    return float(np.mean(classes[np.argmin(d, axis=1)] == y_te))


def count_ceiling(w_tr, y_tr, w_te, y_te):
    n_tr, n_te = w_tr.sum(axis=1), w_te.sum(axis=1)
    overall = np.bincount(y_tr, minlength=120).argmax()
    best = {n: np.bincount(y_tr[n_tr == n], minlength=120).argmax() for n in np.unique(n_tr)}
    return float(np.mean(np.array([best.get(n, overall) for n in n_te]) == y_te))


def order(m):
    p, k = m.copy(), 1
    while np.linalg.norm(p - np.eye(len(m))) > 1e-9:
        p, k = m @ p, k + 1
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    rep = np.stack([perm_matrix(T), perm_matrix(C)])
    k_tc = order(rep[0] @ rep[1])
    acc = {arm: {L: [] for L in LENGTHS} for arm in ("REP", "DIAG", "COUNT-CEILING", "RANDOM-U", "SHAM", "TABLE")}
    diag_dev, sham_rel = 0.0, []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        diags = np.exp(1j * rng.uniform(0, 2 * np.pi, (2, 32)))
        rand = np.stack([expi((lambda m: (m + m.conj().T) / 2)(rng.standard_normal((5, 5)) + 1j * rng.standard_normal((5, 5))))
                         for _ in range(2)])
        sham = np.stack([sham_of(rep[0], rng), sham_of(rep[1], rng)])
        st, sc = sham
        sham_rel.append((float(np.linalg.norm(st @ st - np.eye(5))),
                         float(np.linalg.norm(np.linalg.matrix_power(sc, 5) - np.eye(5))),
                         float(np.linalg.norm(np.linalg.matrix_power(st @ sc, k_tc) - np.eye(5)))))
        for L in LENGTHS:
            w = rng.integers(0, 2, (N_TRAIN + N_TEST, L))
            y = labels(w)
            tr, te = slice(0, N_TRAIN), slice(N_TRAIN, None)
            for arm, f in (("REP", holonomies(w, rep)), ("RANDOM-U", holonomies(w, rand)),
                           ("SHAM", holonomies(w, sham)), ("DIAG", diag_holonomies(w, diags))):
                acc[arm][L].append(centroid_accuracy(f[tr], y[tr], f[te], y[te]))
                if arm == "DIAG":
                    counts = w.sum(axis=1)
                    for n in np.unique(counts):
                        g = f[counts == n]
                        diag_dev = max(diag_dev, float(abs(g - g[0]).max()))
            acc["COUNT-CEILING"][L].append(count_ceiling(w[tr], y[tr], w[te], y[te]))
            acc["TABLE"][L].append(float(np.mean(labels(w[te]) == y[te])))
    mean = {arm: {L: float(np.mean(v)) for L, v in d.items()} for arm, d in acc.items()}
    lo = {arm: {L: float(np.min(v)) for L, v in d.items()} for arm, d in acc.items()}
    st2 = max(r[0] for r in sham_rel)
    sc5 = max(r[1] for r in sham_rel)
    stck = min(r[2] for r in sham_rel)

    print(f"VERITAS-HOLO E004 | seeds {SEEDS[0]}-{SEEDS[-1]} | {platform.machine()} | Python {platform.python_version()} | "
          f"NumPy {np.__version__}")
    print(f"S5 by t=(0 1), c=(0 1 2 3 4); order of tc = {k_tc}; {N_TRAIN} train + {N_TEST} test words per length; "
          f"chance 1/120 = {1 / 120:.4f}")
    print(f"{'arm':14}" + "".join(f"{'L=' + str(L):>10}" for L in LENGTHS) + "   (mean test accuracy over seeds)")
    for arm in acc:
        print(f"{arm:14}" + "".join(f"{mean[arm][L]:10.4f}" for L in LENGTHS))
    print(f"SHAM relations: max ||t^2-I|| {st2:.2e}, max ||c^5-I|| {sc5:.2e}, min ||(tc)^{k_tc}-I|| {stck:.4f}")
    long = (40, 160)
    v = {
        "G1": (all(lo["REP"][L] == 1.0 for L in LENGTHS), "REP min accuracy " + ", ".join(f"L={L} {lo['REP'][L]:.4f}" for L in LENGTHS)),
        "G2": (diag_dev < 1e-12 and all(mean["DIAG"][L] <= mean["COUNT-CEILING"][L] + 0.02 for L in long),
               f"DIAG equal-count deviation {diag_dev:.2e}; " + ", ".join(
                   f"L={L} {mean['DIAG'][L]:.4f} <= ceiling {mean['COUNT-CEILING'][L]:.4f} + 0.02" for L in long)),
        "G3": (all(mean["COUNT-CEILING"][L] < 0.05 for L in long),
               "COUNT-CEILING " + ", ".join(f"L={L} {mean['COUNT-CEILING'][L]:.4f}" for L in long) + " < 0.05"),
        "G4": (all(mean["RANDOM-U"][L] < 0.05 for L in long),
               "RANDOM-U " + ", ".join(f"L={L} {mean['RANDOM-U'][L]:.4f}" for L in long) + " < 0.05"),
        "G5": (st2 < 1e-12 and sc5 < 1e-12 and stck > 1e-3 and all(mean["SHAM"][L] < 0.05 for L in long),
               f"SHAM t^2 {st2:.2e}, c^5 {sc5:.2e} < 1e-12; (tc)^{k_tc} {stck:.4f} > 1e-3; " + ", ".join(
                   f"L={L} {mean['SHAM'][L]:.4f}" for L in long) + " < 0.05"),
        "G6": (all(lo["TABLE"][L] == 1.0 for L in LENGTHS), "TABLE min accuracy 1.0000 at every L (no advantage over classical)"
               if all(lo["TABLE"][L] == 1.0 for L in LENGTHS) else "TABLE below 1.0"),
    }
    for k, (ok, d) in v.items():
        print(f"{'HELD  ' if ok else 'FAILED'} {k}  {d}")
    held = sum(ok for ok, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E004", "machine": platform.machine(), "python": platform.python_version(),
                       "numpy": np.__version__, "order_tc": k_tc, "accuracy": {k: {str(L): x for L, x in d.items()} for k, d in acc.items()},
                       "diag_equal_count_dev": diag_dev, "sham_relations": sham_rel,
                       "verdicts": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in v.items()}},
                      fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
