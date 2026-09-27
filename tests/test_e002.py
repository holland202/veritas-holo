"""E002's pieces, checked before E002 was run: the area, the sham, and a readout that can say zero."""
import importlib.util
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("e002", os.path.join(ROOT, "experiments", "E002_holonomy_area", "run.py"))
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_signed_area_of_unit_squares_and_a_retraced_path():
    assert e.signed_area([0, 2, 1, 3]) == 1.0      # x+ y+ x- y-: counter-clockwise unit square
    assert e.signed_area([2, 0, 3, 1]) == -1.0     # clockwise
    assert e.signed_area([0, 1, 2, 3]) == 0.0      # out and back twice: no area


def test_sham_keeps_the_spectrum_and_changes_the_eigenvectors():
    rng = np.random.default_rng(3)
    y = e.random_hermitian(8, rng)
    w, _ = np.linalg.eigh(y)
    v = e.random_unitary(8, rng)
    ys = (v * w) @ v.conj().T
    assert np.max(abs(np.linalg.eigvalsh(ys) - w)) < 1e-12 and np.linalg.norm(ys - y) > 0.1


def test_readout_tracks_area_for_su2_and_is_zero_when_operators_commute():
    sq = [0, 2, 1, 3]
    f = e.readout(e.holonomy(sq, e.SX, e.SY, 0.01), e.commutator(e.SX, e.SY))
    assert abs(abs(f) - 0.01 ** 2) < 1e-6              # |f| = eps^2 * |area| for a unit square
    rng = np.random.default_rng(4)
    xd, yd = e.random_diagonal_hermitian(4, rng), e.random_diagonal_hermitian(4, rng)
    assert e.readout(e.holonomy(sq, xd, yd, 0.5), e.commutator(xd, yd)) == 0.0
