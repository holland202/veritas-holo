"""Unit and sabotage tests for the reference implementation. A check that cannot fail is not a check,
so every property test here has a case built to make it fail."""
import os
import subprocess
import sys

import numpy as np
import pytest

from veritas_holo import (check_norm_preserved, commutator, det_error, distance, expi, holonomy_loop,
                          random_diagonal_hermitian, random_hermitian, random_state, run_trajectory,
                          unitarity_error)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rng():
    return np.random.default_rng(7)


def test_expi_is_special_unitary_and_matches_a_series():
    h = random_hermitian(6, rng(), norm=0.3)
    u = expi(h)
    assert unitarity_error(u) < 1e-13 and det_error(u) < 1e-13
    series, term = np.eye(6, dtype=complex), np.eye(6, dtype=complex)
    for k in range(1, 30):
        term = term @ (1j * h) / k
        series = series + term
    assert np.linalg.norm(u - series) < 1e-13


def test_unitarity_and_det_errors_can_fail():
    g = rng().standard_normal((4, 4)).astype(complex)
    assert unitarity_error(g) > 1e-3
    assert det_error(expi(random_hermitian(4, rng(), traceless=False, norm=2.0))) > 1e-3  # U(n), not SU(n)


def test_distance_ignores_global_phase_but_not_a_real_difference():
    r = rng()
    x, y = random_state(5, r), random_state(5, r)
    assert distance(x, np.exp(1j * 0.7) * x) < 1e-15
    assert distance(x, y) > 1e-2


def test_commutator_zero_only_for_commuting_matrices():
    r = rng()
    assert np.linalg.norm(commutator(expi(random_diagonal_hermitian(8, r)), expi(random_diagonal_hermitian(8, r)))) < 1e-14
    assert np.linalg.norm(commutator(expi(random_hermitian(8, r)), expi(random_hermitian(8, r)))) > 1e-3


def test_holonomy_of_a_small_loop_is_the_commutator_to_second_order():
    r = rng()
    x, y = random_hermitian(8, r), random_hermitian(8, r)
    eps = 1e-3
    lead = np.eye(8) - eps ** 2 * commutator(x, y)  # BCH: exp(-eps^2 [x, y]) to first order
    assert np.linalg.norm(holonomy_loop(x, y, eps) - lead) < 10 * eps ** 3


def test_norm_checker_passes_unitary_and_fails_a_sham():
    r = rng()
    x = random_state(8, r)
    ops = [expi(random_hermitian(8, r)) for _ in range(4)]
    assert check_norm_preserved(run_trajectory(x, ops)).verdict == "PASS"
    m = r.standard_normal((8, 8)) + 1j * r.standard_normal((8, 8))
    sham = m * (np.sqrt(8) / np.linalg.norm(m))
    assert check_norm_preserved(run_trajectory(x, [ops[0], sham, ops[1]])).verdict == "FAIL"


def test_replay_digest_changes_when_any_state_changes():
    r = rng()
    x = random_state(8, r)
    ops = [expi(random_hermitian(8, r)) for _ in range(3)]
    a, b = run_trajectory(x, ops), run_trajectory(x, ops)
    assert a.digest() == b.digest()
    x2 = x.copy()
    x2[0] += 1e-15
    assert run_trajectory(x2, ops).digest() != a.digest()


def test_e001_runs_and_every_registered_prediction_holds():
    p = subprocess.run([sys.executable, os.path.join(ROOT, "experiments", "E001_operator_algebra", "run.py")],
                       capture_output=True, text=True, timeout=300)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "VERDICT  10 of 10 registered predictions and nulls held" in p.stdout


@pytest.mark.parametrize("name", ["P3", "N3", "P5", "N5"])
def test_e001_verdicts_depend_on_the_data(name, monkeypatch):
    """Sabotage: swap the operator factory for one that makes every operator diagonal. P3 and the
    non-diagonal checks must then fail, which shows their HELD is not hard-wired."""
    sys.path.insert(0, os.path.join(ROOT, "experiments", "E001_operator_algebra"))
    import importlib
    run = importlib.import_module("run")
    monkeypatch.setattr(run, "random_hermitian", lambda n, r, **k: random_diagonal_hermitian(n, r))
    out, _ = run.run(1)
    if name == "P3":
        assert out["P3"][0] is False  # diagonal operators commute: noncommutativity must fail
    else:
        assert out[name][0] is True  # the nulls and the invariant are unaffected
