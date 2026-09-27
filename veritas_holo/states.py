"""Unit state vectors, the distance between them, trajectories, and the invariant checker."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np


def random_state(n: int, rng: np.random.Generator) -> np.ndarray:
    v = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    return v / np.linalg.norm(v)


def distance(x: np.ndarray, y: np.ndarray) -> float:
    """Phase-aligned Euclidean distance: || x - y * (<y,x>/|<y,x>|) ||.
    States are rays, so a global phase is ignored. Unlike arccos(|<x,y>|) this stays accurate near
    zero, which matters when the tolerances are 1e-12."""
    overlap = np.vdot(y, x)
    phase = overlap / abs(overlap) if abs(overlap) > 0 else 1.0
    return float(np.linalg.norm(x - y * phase))


@dataclass(frozen=True)
class Trajectory:
    states: tuple  # x_0 .. x_k, each a numpy array
    products: tuple  # U_1 .. U_k, the running operator products

    def digest(self) -> str:
        """sha256 over the raw bytes of every state, in order: the replay fingerprint."""
        h = hashlib.sha256()
        for s in self.states:
            h.update(np.ascontiguousarray(s, dtype=np.complex128).tobytes())
        return h.hexdigest()


def run_trajectory(x0: np.ndarray, operators: list) -> Trajectory:
    states, products = [x0], []
    u = np.eye(len(x0), dtype=complex)
    for op in operators:
        u = op @ u
        products.append(u)
        states.append(op @ states[-1])
    return Trajectory(tuple(states), tuple(products))


@dataclass(frozen=True)
class InvariantReport:
    name: str
    verdict: str  # PASS or FAIL
    worst: float
    tolerance: float


def check_norm_preserved(traj: Trajectory, tol: float = 1e-12) -> InvariantReport:
    """The invariant a unitary evolution must keep: every state stays a unit vector."""
    worst = max(abs(np.linalg.norm(s) - 1) for s in traj.states)
    return InvariantReport("norm_preserved", "PASS" if worst < tol else "FAIL", float(worst), tol)
