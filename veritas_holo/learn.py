"""Learning operators from labelled words (E005). Plain NumPy: exact chain-rule gradients through the
matrix product, and Riemannian steps on U(n) that keep the operators unitary to rounding."""
from __future__ import annotations

import itertools

import numpy as np

from .algebra import expi


def haar_unitary(n, rng):
    q, r = np.linalg.qr(rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n)))
    return q * (np.diag(r) / abs(np.diag(r)))


def prefix_products(word, ops):
    pre = [np.eye(ops.shape[1], dtype=complex)]
    for a in word:
        pre.append(ops[a] @ pre[-1])
    return pre


def holonomy(word, ops):
    return prefix_products(word, ops)[-1]


def chain_grad(word, ops, G):
    """Euclidean gradient of Re tr(G^H H(word)) with respect to each generator."""
    pre, out = prefix_products(word, ops), np.zeros_like(ops)
    left = np.eye(ops.shape[1], dtype=complex)
    for k in range(len(word) - 1, -1, -1):
        out[word[k]] += left.conj().T @ G @ pre[k].conj().T
        left = left @ ops[word[k]]
    return out


def all_words(n_letters, max_len):
    return [np.array(w) for L in range(1, max_len + 1) for w in itertools.product(range(n_letters), repeat=L)]


def train_operators(words, y, dim, rng, n_letters=2, steps=3000, lr=0.05, npos=64, nneg=64, margin=4.0, beta=0.9,
                    diagonal=False):
    """Pull holonomies of equal-label words together and push different-label ones at least `margin` apart
    (squared Frobenius). Only (word, label) pairs are used: no relation of the group is given.
    diagonal=True restricts the operators to diagonal unitaries (the commuting class)."""
    by_label = {}
    for i, lab in enumerate(y):
        by_label.setdefault(int(lab), []).append(i)
    groups = [g for g in by_label.values() if len(g) >= 2]
    if diagonal:
        theta = rng.uniform(0, 2 * np.pi, (n_letters, dim))
        mom = np.zeros_like(theta)
    else:
        ops = np.stack([haar_unitary(dim, rng) for _ in range(n_letters)])
        mom = np.zeros_like(ops)
    for step in range(steps):
        if diagonal:
            ops = np.stack([np.diag(np.exp(1j * t)) for t in theta])
        cache = {}

        def hol(i):
            if i not in cache:
                cache[i] = holonomy(words[i], ops)
            return cache[i]

        pairs = []
        for _ in range(npos):
            g = groups[rng.integers(len(groups))]
            i, j = rng.choice(g, 2, replace=False)
            pairs.append((i, j, True))
        for _ in range(nneg):
            i, j = rng.integers(len(words), size=2)
            if y[i] != y[j]:
                pairs.append((i, j, False))
        grad = np.zeros_like(ops)
        for i, j, same in pairs:
            D = hol(i) - hol(j)
            d2 = float(np.sum(abs(D) ** 2))
            if same:
                G = 2 * D / npos
            elif d2 < margin:
                G = -2 * D / nneg
            else:
                continue
            grad += chain_grad(words[i], ops, G) - chain_grad(words[j], ops, G)
        step_lr = lr * (1 - step / steps)
        if diagonal:
            gth = np.real(np.conj(np.stack([np.diag(g) for g in grad])) * 1j * np.exp(1j * theta))
            mom = beta * mom + gth
            theta = theta - step_lr * mom
        else:
            for k in range(n_letters):
                omega = grad[k] @ ops[k].conj().T - ops[k] @ grad[k].conj().T
                mom[k] = beta * mom[k] + omega
                ops[k] = expi((1j * step_lr / 2) * mom[k]) @ ops[k]
    if diagonal:
        ops = np.stack([np.diag(np.exp(1j * t)) for t in theta])
    return ops
