"""E011 (see PREREG.md): snapping to a codebook built from labelled data, for operators with real error.
E008 snapped to the EXACT 120 class matrices, which needs the group representation. Here the codebook
is the per-label mean holonomy of short labelled words under the same noisy operators."""
import os, sys, time, numpy as np
sys.path.insert(0, os.environ.get('HOLO_ROOT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from veritas_holo import expi
import itertools
T, C = (1, 0, 2, 3, 4), (1, 2, 3, 4, 0)
PERMS = list(itertools.permutations(range(5))); IDX = {p: i for i, p in enumerate(PERMS)}
def pm(g):
    m = np.zeros((5, 5))
    for i in range(5): m[g[i], i] = 1
    return m
P = np.stack([pm(p) for p in PERMS])
NEXT = np.array([[IDX[tuple(g[p[i]] for i in range(5))] for g in (T, C)] for p in PERMS])
E = IDX[tuple(range(5))]
def haar(n, rng):
    q, r = np.linalg.qr(rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))); return q * (np.diag(r) / abs(np.diag(r)))
def setup(seed, delta):
    rng = np.random.default_rng(seed)
    V = haar(5, rng)
    ops = np.stack([V @ pm(g) @ V.conj().T for g in (T, C)])
    herm = lambda m: (m + m.conj().T) / 2  # noqa: E731
    ops = np.stack([expi(delta * herm(rng.standard_normal((5, 5)) + 1j * rng.standard_normal((5, 5)))) @ o for o in ops])
    exact = np.einsum('ij,kjl,ml->kim', V, P, V.conj())
    return rng, ops, exact
def data_book(rng, ops, n_words, max_len):
    """Per-label mean holonomy of n_words random labelled words of length 1..max_len."""
    acc, cnt = np.zeros((120, 5, 5), complex), np.zeros(120)
    for _ in range(n_words):
        L = int(rng.integers(1, max_len + 1)); w = rng.integers(0, 2, L)
        h, s = np.eye(5, dtype=complex), E
        for a in w: h = ops[a] @ h; s = NEXT[s, a]
        acc[s] += h; cnt[s] += 1
    book = acc / np.maximum(cnt, 1)[:, None, None]
    return book, cnt > 0
def run(seed, L, delta, arm, n=32, n_words=4000, max_len=12):
    rng, ops, exact = setup(seed, delta)
    if arm == "DATA":
        book, have = data_book(rng, ops, n_words, max_len)
    else:
        book, have = exact, np.ones(120, bool)
    idx = np.flatnonzero(have); B = book[idx]
    words = rng.integers(0, 2, (n, L))
    h = np.broadcast_to(np.eye(5, dtype=complex), (n, 5, 5)).copy(); s = np.full(n, E)
    for k in range(L):
        h = ops[words[:, k]] @ h; s = NEXT[s, words[:, k]]
        if arm != "NONE":
            d = (abs(h[:, None] - B[None]) ** 2).sum((2, 3)); h = B[np.argmin(d, 1)].copy()
    d = (abs(h[:, None] - B[None]) ** 2).sum((2, 3)); pred = idx[np.argmin(d, 1)]
    return float(np.mean(pred == s)), int(have.sum())
if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1].split(",")]
    for delta in (1e-2, 3e-2, 1e-1, 2e-1):
        for L in (10**3, 10**4):
            for arm in ("NONE", "EXACT", "DATA"):
                t = time.time(); r = [run(sd, L, delta, arm) for sd in seeds]
                print(f"delta {delta:<5} L {L:<6} {arm:<5} acc {[a for a, _ in r]} coverage {[c for _, c in r]} {time.time()-t:.0f}s", flush=True)
