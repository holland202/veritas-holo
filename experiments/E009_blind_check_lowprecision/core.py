import json, sys, time, numpy as np
from pilot_common import e4, WORDS, Y, train_operators, ProcessPoolExecutor
from veritas_holo.learn import holonomy


def q16(h):
    return (h.real.astype(np.float16).astype(np.float64) + 1j * h.imag.astype(np.float16).astype(np.float64))


def run_words(words, ops, cent=None, every=0, lowp=False):
    n = len(words); h = np.broadcast_to(np.eye(ops.shape[1], dtype=complex), (n,) + ops.shape[1:]).copy()
    o = q16(ops) if lowp else ops
    for k in range(words.shape[1]):
        h = o[words[:, k]] @ h
        if lowp:
            h = q16(h)
        if every and (k + 1) % every == 0:
            f = h.reshape(n, -1)
            idx = np.argmin((abs(f[:, None, :] - cent[None]) ** 2).sum(2), 1)
            h = cent[idx].reshape(h.shape).copy()
    return h.reshape(n, -1)


def train_residual(ops):
    """Blind: mean distance between holonomies of training words that share a label. Uses training data only."""
    H = np.stack([holonomy(w, ops) for w in WORDS]).reshape(len(WORDS), -1)
    d = []
    for k in np.unique(Y):
        g = H[Y == k]
        if len(g) > 1:
            d.append(np.mean(np.linalg.norm(g - g.mean(0), axis=1)))
    return float(np.mean(d))


def one(seed):
    t0 = time.time()
    ops = train_operators(WORDS, Y, 8, np.random.default_rng(seed))
    rng = np.random.default_rng(5000 + seed)
    w = rng.integers(0, 2, (6000, 160)); y = e4.labels(w)
    ftr = run_words(w, ops); classes = np.unique(y); cent = np.stack([ftr[y == k].mean(0) for k in classes])
    res = {"seed": seed, "train_residual": train_residual(ops)}
    def acc(f, yt):
        return float(np.mean(classes[np.argmin((abs(f[:, None, :] - cent[None]) ** 2).sum(2), 1)] == yt))
    wt = rng.integers(0, 2, (400, 160)); res["f64_160"] = acc(run_words(wt, ops), e4.labels(wt))
    for L in (1000, 10000):
        wt = rng.integers(0, 2, (400, L)); yt = e4.labels(wt)
        res[f"f16raw{L}"] = acc(run_words(wt, ops, lowp=True), yt)
        res[f"f16snap{L}"] = acc(run_words(wt, ops, cent, 8, lowp=True), yt)
    res["s"] = round(time.time() - t0)
    return res


if __name__ == "__main__":
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(one, range(int(sys.argv[1]), int(sys.argv[2]))):
            print(json.dumps(r), flush=True)
