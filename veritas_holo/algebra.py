"""SU(n) operators, commutators and holonomy loops. Pure NumPy.

Everything here is a finite-dimensional matrix computation. "SU(n)" names the set of n x n unitary
matrices with determinant 1; nothing more is claimed by the name.
"""
from __future__ import annotations

import numpy as np


def random_hermitian(n: int, rng: np.random.Generator, *, traceless: bool = True, norm: float = 1.0) -> np.ndarray:
    """A random Hermitian matrix (complex Gaussian entries, Hermitised), optionally traceless,
    scaled to Frobenius norm `norm`."""
    a = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    h = (a + a.conj().T) / 2
    if traceless:
        h -= np.trace(h) / n * np.eye(n)
    return h * (norm / np.linalg.norm(h))


def random_diagonal_hermitian(n: int, rng: np.random.Generator, *, norm: float = 1.0) -> np.ndarray:
    """A random traceless real diagonal matrix of Frobenius norm `norm`: diagonal matrices commute."""
    d = rng.standard_normal(n)
    d -= d.mean()
    return np.diag(d * (norm / np.linalg.norm(d))).astype(complex)


def expi(h: np.ndarray) -> np.ndarray:
    """exp(i h) for Hermitian h, from its eigendecomposition: V diag(e^{i lambda}) V^dagger."""
    w, v = np.linalg.eigh(h)
    return (v * np.exp(1j * w)) @ v.conj().T


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def group_commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a b a^-1 b^-1 for unitary a, b (inverse = conjugate transpose)."""
    return a @ b @ a.conj().T @ b.conj().T


def unitarity_error(u: np.ndarray) -> float:
    return float(np.linalg.norm(u.conj().T @ u - np.eye(u.shape[0])))


def det_error(u: np.ndarray) -> float:
    """|det u - 1|: zero for an element of SU(n)."""
    return float(abs(np.linalg.det(u) - 1))


def holonomy_loop(x: np.ndarray, y: np.ndarray, eps: float) -> np.ndarray:
    """H(eps) = e^{i eps x} e^{i eps y} e^{-i eps x} e^{-i eps y}: transport around a small closed loop.
    By Baker-Campbell-Hausdorff, H(eps) = exp(-eps^2 [x, y] + O(eps^3)), so ||H - I|| ~ eps^2 ||[x, y]||."""
    return group_commutator(expi(eps * x), expi(eps * y))
