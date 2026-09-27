import importlib.util
import os

import numpy as np

spec = importlib.util.spec_from_file_location(
    "e004", os.path.join(os.path.dirname(__file__), "..", "experiments", "E004_group_state", "run.py"))
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_rep_is_a_homomorphism():
    rng = np.random.default_rng(0)
    w = rng.integers(0, 2, (50, 12))
    rep = np.stack([e.perm_matrix(e.T), e.perm_matrix(e.C)])
    h = e.holonomies(w, rep).reshape(-1, 5, 5)
    y = e.labels(w)
    for hi, yi in zip(h, y):
        assert np.allclose(hi, e.perm_matrix(e.PERMS[yi]))


def test_sham_keeps_spectrum_relations():
    rng = np.random.default_rng(1)
    s = e.sham_of(e.perm_matrix(e.T), rng)
    assert np.linalg.norm(s @ s - np.eye(5)) < 1e-12


def test_centroid_readout_can_fail():
    rng = np.random.default_rng(2)
    f = rng.standard_normal((400, 4))
    y = rng.integers(0, 10, 400)
    assert e.centroid_accuracy(f[:200], y[:200], f[200:], y[200:]) < 0.3
