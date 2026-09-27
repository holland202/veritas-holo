import numpy as np

from veritas_holo.trace import Alphabet, Fingerprinter, det, mul, normal_form, random_sl2

AL = Alphabet([[0], [1], [0, 1], [2]])  # 0 and 1 independent; 2 depends on both; 3 independent of all


def test_sl2_and_mul():
    rng = np.random.default_rng(1)
    x, y = random_sl2(rng), random_sl2(rng)
    assert det(x) == 1 and det(mul(x, y)) == 1


def test_normal_form_ground_truth():
    assert normal_form([1, 0], AL) == normal_form([0, 1], AL)  # independent: same history
    assert normal_form([0, 2], AL) != normal_form([2, 0], AL)  # dependent: different history
    assert normal_form([3, 2, 0], AL) == normal_form([2, 0, 3], AL)


def test_fingerprint_follows_independence():
    f = Fingerprinter(AL, np.random.default_rng(2))
    assert f.of([0, 1, 3]) == f.of([3, 1, 0])
    assert f.of([0, 2]) != f.of([2, 0])


def test_merge_is_composition():
    f = Fingerprinter(AL, np.random.default_rng(3))
    u, v = [0, 2, 1, 3, 2], [1, 1, 2, 0]
    assert f.merge(f.of(u), f.of(v)) == f.of(u + v)


def test_nulls_can_fail_each_way():
    commuting = Fingerprinter(AL, np.random.default_rng(4), commuting=True)
    assert commuting.of([0, 2]) == commuting.of([2, 0])  # blind to order: accepts a dependent swap
    one = Fingerprinter(AL, np.random.default_rng(5), one_block=True)
    assert one.of([0, 1]) != one.of([1, 0])  # rejects an independent swap
