#!/usr/bin/env python3
"""E001 - operator algebra on SU(32). Registered in PREREG.md (P1-P7, nulls N3-N5) before this code.

  python experiments/E001_operator_algebra/run.py [--seed 1] [--json OUT.json]
Exit: 0 every registered prediction and null held | 1 at least one did not
"""
import argparse
import json
import os
import platform
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from veritas_holo import (check_norm_preserved, commutator, det_error, distance, expi, group_commutator,  # noqa: E402
                          holonomy_loop, random_diagonal_hermitian, random_hermitian, random_state,
                          run_trajectory, unitarity_error)

N, N_OPS, STEPS = 32, 8, 12
EPSILONS = (0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001)


def trajectory_for(seed):
    """The seeded objects every prediction uses, always drawn in the same order."""
    rng = np.random.default_rng(seed)
    x = random_state(N, rng)
    ops = [expi(random_hermitian(N, rng)) for _ in range(N_OPS)]
    path = [ops[i % N_OPS] for i in range(STEPS)]
    return rng, x, ops, path, run_trajectory(x, path)


def run(seed):
    rng, x, ops, path, traj = trajectory_for(seed)
    out = {}

    # P1 closure
    u_err = max(unitarity_error(u) for u in traj.products)
    d_err = max(det_error(u) for u in traj.products)
    out["P1"] = (u_err < 1e-10 and d_err < 1e-10, f"max ||U'U-I|| {u_err:.2e}, max |det U-1| {d_err:.2e}")

    # P2 inverse
    inv = max(distance(a.conj().T @ (a @ x), x) for a in ops)
    out["P2"] = (inv < 1e-12, f"max d(A'Ax, x) {inv:.2e}")

    # P3 noncommutativity, with the diagonal null N3
    pairs = [(i, j) for i in range(N_OPS) for j in range(i + 1, N_OPS)]
    comm = min(np.linalg.norm(commutator(ops[i], ops[j])) for i, j in pairs)
    out["P3"] = (comm > 1e-3, f"min ||[Ai,Aj]|| over {len(pairs)} pairs {comm:.4f}")
    diag = [expi(random_diagonal_hermitian(N, rng)) for _ in range(N_OPS)]
    dcomm = max(np.linalg.norm(commutator(diag[i], diag[j])) for i, j in pairs)
    out["N3"] = (dcomm < 1e-12, f"max ||[Di,Dj]|| over {len(pairs)} diagonal pairs {dcomm:.2e}")

    # P4 holonomy scaling, with the diagonal null N4, and the state holonomy (reported only)
    X, Y = random_hermitian(N, rng), random_hermitian(N, rng)
    h = [np.linalg.norm(holonomy_loop(X, Y, e) - np.eye(N)) for e in EPSILONS]
    slope = float(np.polyfit(np.log(EPSILONS), np.log(h), 1)[0])
    cxy = float(np.linalg.norm(commutator(X, Y)))
    ratio = h[-1] / EPSILONS[-1] ** 2 / cxy
    out["P4"] = (1.95 <= slope <= 2.05 and abs(ratio - 1) < 0.01,
                 f"slope {slope:.4f}, h(0.001)/0.001^2 / ||[X,Y]|| = {ratio:.6f}")
    Xd, Yd = random_diagonal_hermitian(N, rng), random_diagonal_hermitian(N, rng)
    hd = max(np.linalg.norm(holonomy_loop(Xd, Yd, e) - np.eye(N)) for e in EPSILONS)
    out["N4"] = (hd < 1e-12, f"max h(eps) for diagonal X, Y {hd:.2e}")
    state_holonomy = distance(group_commutator(ops[0], ops[1]) @ x, x)

    # P5 invariant preservation, with the non-unitary sham N5
    rep = check_norm_preserved(traj)
    out["P5"] = (rep.verdict == "PASS", f"checker {rep.verdict}, worst | ||x_k|| - 1 | {rep.worst:.2e}")
    m = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    sham = m * (np.sqrt(N) / np.linalg.norm(m))
    sham_path = [sham if p is ops[2] else p for p in path]
    srep = check_norm_preserved(run_trajectory(x, sham_path))
    out["N5"] = (srep.verdict == "FAIL" and srep.worst > 1e-3,
                 f"checker {srep.verdict}, worst | ||x_k|| - 1 | {srep.worst:.4f}")

    # P6 isometry
    delta = random_state(N, rng)
    x2 = x + 1e-6 * delta
    x2 /= np.linalg.norm(x2)
    u = traj.products[-1]
    iso = abs(distance(u @ x, u @ x2) - distance(x, x2))
    out["P6"] = (iso < 1e-12, f"|d(Ux,Ux') - d(x,x')| {iso:.2e} (d(x,x') = {distance(x, x2):.3e})")

    # P7 replay
    d1, d1b, d2 = traj.digest(), trajectory_for(seed)[4].digest(), trajectory_for(seed + 1)[4].digest()
    out["P7"] = (d1 == d1b and d1 != d2, f"seed {seed} twice: {d1[:16]} {d1b[:16]}; seed {seed + 1}: {d2[:16]}")
    return out, {"state_holonomy": state_holonomy, "slope": slope, "replay_digest": d1,
                 "rounded_digest_10dp": traj.digest(decimals=10),
                 "holonomy_curve": dict(zip(map(str, EPSILONS), map(float, h)))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out, extra = run(a.seed)
    print(f"VERITAS-HOLO E001 | seed {a.seed} | {platform.machine()} | Python {platform.python_version()} | "
          f"NumPy {np.__version__}")
    print(f"state dimension {N}, operators {N_OPS}, trajectory length {STEPS}")
    for k in ("P1", "P2", "P3", "N3", "P4", "N4", "P5", "N5", "P6", "P7"):
        ok, detail = out[k]
        print(f"{'HELD  ' if ok else 'FAILED'} {k:3} {detail}")
    print(f"state holonomy d(A1 A2 A1' A2' x, x) = {extra['state_holonomy']:.4f}  (reported, not predicted)")
    print(f"replay digest {extra['replay_digest']}")
    print(f"rounded digest (10 dp, P10) {extra['rounded_digest_10dp']}")
    held = sum(ok for ok, _ in out.values())
    print(f"VERDICT  {held} of {len(out)} registered predictions and nulls held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E001", "seed": a.seed, "machine": platform.machine(),
                       "python": platform.python_version(), "numpy": np.__version__,
                       "results": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in out.items()},
                       **extra}, fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(out) else 1)


if __name__ == "__main__":
    main()
