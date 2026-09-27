"""Holonomy fingerprints for concurrent histories (E003).

A log is a sequence of actions; each action touches a set of resources. Actions on disjoint
resources are independent and may be reordered. The fingerprint is a holonomy in SL(2, F_p)^R:
one exact 2x2 matrix product per resource, so independent actions land in different blocks and
commute, dependent ones share a block and (almost surely) do not. It composes: F(u.v) = F(v)F(u).
Not a security primitive: SL(2) Cayley hashes have published collision attacks.
"""
from __future__ import annotations

import hashlib

P = 2 ** 61 - 1
IDENT = (1, 0, 0, 1)


def mul(x, y):
    """2x2 product x @ y over F_p; matrices are tuples (a, b, c, d) for [[a, b], [c, d]]."""
    a, b, c, d = x
    e, f, g, h = y
    return ((a * e + b * g) % P, (a * f + b * h) % P, (c * e + d * g) % P, (c * f + d * h) % P)


def det(x):
    return (x[0] * x[3] - x[1] * x[2]) % P


def random_sl2(rng):
    a, b, c = (int(rng.integers(1, P)) for _ in range(3))
    return (a, b, c, (1 + b * c) * pow(a, -1, P) % P)


def random_diag_sl2(rng):
    a = int(rng.integers(2, P))
    return (a, 0, 0, pow(a, -1, P))


class Alphabet:
    """Actions 0..n-1, each touching a set of resources 0..R-1."""

    def __init__(self, touches):
        self.touches = [frozenset(t) for t in touches]
        self.n = len(self.touches)
        self.R = 1 + max(max(t) for t in self.touches)

    def independent(self, a, b):
        return a != b and not (self.touches[a] & self.touches[b])

    @classmethod
    def random(cls, n, R, rng):
        return cls([sorted(rng.choice(R, size=int(rng.integers(1, 3)), replace=False).tolist()) for _ in range(n)])


class Fingerprinter:
    """HF: matrices[a][r] for r in touches(a). `blocks` maps a resource to the block it multiplies into
    (identity for HF; all-zero for the one-block null N2)."""

    def __init__(self, alphabet, rng, commuting=False, one_block=False):
        self.al = alphabet
        draw = random_diag_sl2 if commuting else random_sl2
        self.blocks = 1 if one_block else alphabet.R
        self.mats = [{(0 if one_block else r): draw(rng) for r in (sorted(alphabet.touches[a])[:1] if one_block
                                                                    else sorted(alphabet.touches[a]))}
                     for a in range(alphabet.n)]

    def identity(self):
        return tuple(IDENT for _ in range(self.blocks))

    def extend(self, fp, word):
        fp = list(fp)
        for a in word:
            for r, m in self.mats[a].items():
                fp[r] = mul(m, fp[r])
        return tuple(fp)

    def of(self, word):
        return self.extend(self.identity(), word)

    @staticmethod
    def merge(fu, fv):
        """F(u.v) from F(u) and F(v) alone: one product per block, independent of the log lengths."""
        return tuple(mul(y, x) for x, y in zip(fu, fv))


def normal_form(word, alphabet):
    """Ground truth independent of fingerprints: lexicographic normal form of the trace. Repeatedly
    emit the smallest action with no dependent action before it among those remaining."""
    rest, out, allr = list(word), [], set(range(alphabet.R))
    while rest:
        seen, best, best_i = set(), None, None
        for i, a in enumerate(rest):
            t = alphabet.touches[a]
            if not (t & seen) and (best is None or a < best):
                best, best_i = a, i
            seen |= t
            if seen >= allr:
                break
        out.append(rest.pop(best_i))
    return tuple(out)


def base_digest(word, alphabet):
    """Baseline: per-resource SHA-256 over each resource's projection of the log."""
    hs = [hashlib.sha256() for _ in range(alphabet.R)]
    for a in word:
        for r in alphabet.touches[a]:
            hs[r].update(bytes((a,)))
    return hs


def base_extend(hs, word, alphabet):
    """The baseline's merge: it needs the second segment's raw events."""
    hs = [h.copy() for h in hs]
    for r in range(alphabet.R):
        hs[r].update(bytes(a for a in word if r in alphabet.touches[a]))
    return hs
