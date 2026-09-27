#!/usr/bin/env python3
"""E002 - does holonomy carry a path's signed area, for which operators, and does it beat the exact cheap
computation? Registered in PREREG.md (E1-E6) before this code was written.

  python experiments/E002_holonomy_area/run.py [--seeds 20] [--json OUT.json]
Exit: 0 every registered prediction held | 1 at least one did not
"""
import argparse
import json
import os
import platform
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from veritas_holo import commutator, expi, random_diagonal_hermitian, random_hermitian  # noqa: E402

L_EACH, N_TRAIN, N_TEST = 10, 200, 200
SX = np.array([[0, 1], [1, 0]], dtype=complex) / 2
SY = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2
STEP = {0: (1, 0), 1: (-1, 0), 2: (0, 1), 3: (0, -1)}  # x+, x-, y+, y-


def balanced_word(rng):
    return rng.permutation(np.repeat(np.arange(4), L_EACH))


def signed_area(word):
    """Shoelace over the closed lattice path the word traces: about 2 multiplications per step."""
    x = y = 0
    twice = 0
    for s in word:
        dx, dy = STEP[int(s)]
        nx, ny = x + dx, y + dy
        twice += x * ny - nx * y
        x, y = nx, ny
    assert x == 0 and y == 0, "a balanced word closes"
    return twice / 2


def random_unitary(n, rng):
    q, r = np.linalg.qr(rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n)))
    return q * (np.diag(r) / abs(np.diag(r)))


def holonomy(word, X, Y, eps):
    us = {0: expi(eps * X), 1: expi(-eps * X), 2: expi(eps * Y), 3: expi(-eps * Y)}
    h = np.eye(X.shape[0], dtype=complex)
    for s in word:
        h = us[int(s)] @ h
    return h


def readout(h, C):
    """Re tr(C^dagger (H - I)) / ||C||^2: the component of H - I along the arm's own commutator; 0 if C = 0."""
    nc = np.linalg.norm(C) ** 2
    return 0.0 if nc < 1e-24 else float(np.real(np.trace(C.conj().T @ (h - np.eye(h.shape[0])))) / nc)


def r2(y, pred):
    ss = float(np.sum((y - y.mean()) ** 2))
    return 1 - float(np.sum((y - pred) ** 2)) / ss


def fit_score(f_tr, a_tr, f_te, a_te):
    if np.var(f_tr) < 1e-24:  # a constant feature carries nothing: predict the training mean
        return r2(a_te, np.full_like(a_te, a_tr.mean()))
    a, b = np.polyfit(f_tr, a_tr, 1)
    return r2(a_te, a * f_te + b)


def seed_run(seed):
    rng = np.random.default_rng(seed)
    X32, Y32 = random_hermitian(32, rng), random_hermitian(32, rng)
    w, v = np.linalg.eigh(Y32)
    V = random_unitary(32, rng)
    Ysham = (V * w) @ V.conj().T  # same eigenvalues as Y32, randomised eigenvectors
    Xd, Yd = random_diagonal_hermitian(32, rng), random_diagonal_hermitian(32, rng)
    words = [balanced_word(rng) for _ in range(N_TRAIN + N_TEST)]
    area = np.array([signed_area(wd) for wd in words])
    arms = {"SU2": (SX, SY, 0.05), "SU32-RANDOM": (X32, Y32, 0.05), "SPECTRUM-SHAM": (X32, Ysham, 0.05),
            "ABELIAN": (Xd, Yd, 0.05), "SU2-LARGE": (SX, SY, 1.0)}
    out, abelian_dev = {}, 0.0
    for name, (X, Y, eps) in arms.items():
        C = commutator(X, Y)
        hs = [holonomy(wd, X, Y, eps) for wd in words]
        if name == "ABELIAN":
            abelian_dev = max(float(np.linalg.norm(h - np.eye(32))) for h in hs)
        f = np.array([readout(h, C) for h in hs])
        out[name] = fit_score(f[:N_TRAIN], area[:N_TRAIN], f[N_TRAIN:], area[N_TRAIN:])
    out["SHOELACE"] = r2(area[N_TRAIN:], area[N_TRAIN:])  # the exact computation predicts itself
    spec_gap = float(np.max(abs(np.linalg.eigvalsh(Ysham) - w)))
    return out, abelian_dev, spec_gap, float(np.std(area))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    per = {k: [] for k in ("SU2", "SU32-RANDOM", "SPECTRUM-SHAM", "ABELIAN", "SU2-LARGE", "SHOELACE")}
    abelian_dev = spec_gap = 0.0
    area_sd = []
    for s in range(1, a.seeds + 1):
        o, dev, gap, sd = seed_run(s)
        for k, v in o.items():
            per[k].append(v)
        abelian_dev, spec_gap = max(abelian_dev, dev), max(spec_gap, gap)
        area_sd.append(sd)
    mean = {k: float(np.mean(v)) for k, v in per.items()}
    low = {k: float(np.min(v)) for k, v in per.items()}
    print(f"VERITAS-HOLO E002 | seeds 1-{a.seeds} | {platform.machine()} | Python {platform.python_version()} | "
          f"NumPy {np.__version__}")
    print(f"paths: balanced words of length {4 * L_EACH}, {N_TRAIN} train + {N_TEST} held-out per seed; "
          f"signed-area sd {np.mean(area_sd):.2f}")
    print(f"sham check: max |eig(Y_sham) - eig(Y)| {spec_gap:.2e}")
    print(f"{'arm':15} {'mean R2':>10} {'min R2':>10}")
    for k in per:
        print(f"{k:15} {mean[k]:10.4f} {low[k]:10.4f}")
    verdicts = {
        "E1": (mean["SU2"] > 0.99, f"SU2 mean R2 {mean['SU2']:.4f} > 0.99"),
        "E2": (mean["SU32-RANDOM"] > 0.99, f"SU32-RANDOM mean R2 {mean['SU32-RANDOM']:.4f} > 0.99"),
        "E3": (mean["SPECTRUM-SHAM"] > 0.99, f"SPECTRUM-SHAM mean R2 {mean['SPECTRUM-SHAM']:.4f} > 0.99"),
        "E4": (mean["ABELIAN"] < 0.05 and abelian_dev < 1e-12,
               f"ABELIAN mean R2 {mean['ABELIAN']:.4f} < 0.05, max ||H-I|| {abelian_dev:.2e} < 1e-12"),
        "E5": (mean["SU2-LARGE"] < 0.5, f"SU2-LARGE mean R2 {mean['SU2-LARGE']:.4f} < 0.5"),
        "E6": (low["SHOELACE"] == 1.0, f"SHOELACE min R2 {low['SHOELACE']:.4f} == 1 at ~2 mult/step "
                                        f"(SU2 >= 8 complex mult/step, SU32 ~ {32 ** 3})"),
    }
    for k, (ok, d) in verdicts.items():
        print(f"{'HELD  ' if ok else 'FAILED'} {k}  {d}")
    held = sum(ok for ok, _ in verdicts.values())
    print(f"VERDICT  {held} of {len(verdicts)} registered predictions held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E002", "seeds": a.seeds, "machine": platform.machine(),
                       "python": platform.python_version(), "numpy": np.__version__,
                       "per_seed_r2": per, "mean_r2": mean, "min_r2": low, "abelian_max_dev": abelian_dev,
                       "sham_spectrum_gap": spec_gap,
                       "verdicts": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in verdicts.items()}},
                      fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(verdicts) else 1)


if __name__ == "__main__":
    main()
