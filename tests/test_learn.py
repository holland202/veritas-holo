import numpy as np

from veritas_holo import expi
from veritas_holo.learn import all_words, chain_grad, haar_unitary, holonomy, train_operators


def test_chain_grad_matches_finite_difference():
    rng = np.random.default_rng(0)
    ops = np.stack([haar_unitary(5, rng) for _ in range(2)])
    w1, w2 = np.array([0, 1, 1, 0, 1]), np.array([1, 0, 1])

    def f(o):
        return float(np.sum(abs(holonomy(w1, o) - holonomy(w2, o)) ** 2))

    D = holonomy(w1, ops) - holonomy(w2, ops)
    g = chain_grad(w1, ops, 2 * D) - chain_grad(w2, ops, 2 * D)
    K = (lambda m: (m + m.conj().T) / 2)(rng.standard_normal((5, 5)) + 1j * rng.standard_normal((5, 5)))
    t, moved = 1e-6, ops.copy()
    moved[0] = expi(t * K) @ ops[0]
    num = (f(moved) - f(ops)) / t
    ana = float(np.real(np.trace(g[0].conj().T @ (1j * K @ ops[0]))))
    assert abs(num - ana) < 1e-4 * max(1, abs(ana))


def test_training_keeps_unitarity_and_can_fail():
    words = all_words(2, 4)
    y = np.array([len(w) % 2 for w in words])  # parity of length: a commuting task
    ops = train_operators(words, y, 3, np.random.default_rng(1), steps=50)
    assert max(np.linalg.norm(o.conj().T @ o - np.eye(3)) for o in ops) < 1e-10
    rng = np.random.default_rng(2)
    words = all_words(2, 4)
    y = rng.integers(0, 10, len(words))  # labels with no structure: nothing to learn
    ops = train_operators(words, y, 3, rng, steps=50)
    same = [(i, j) for i in range(len(words)) for j in range(i) if y[i] == y[j]]
    d = np.mean([np.linalg.norm(holonomy(words[i], ops) - holonomy(words[j], ops)) for i, j in same])
    assert d > 0.1  # random labels cannot all be pulled together
