"""E011: a finite certificate for snapped decoding. For codebook {c_s}, noisy ops O_g and start h0:
margin = min over states s and letters g of  (second-nearest distance - distance to c_{g s}) of O_g c_s,
plus the same for O_g h0 -> c_g. If margin > 0, then by induction the snapped state equals c_{true state}
after every step, for every word of every length. If margin < 0 at a reachable (s, g), every word that
passes through s and then reads g is decoded wrong from that step on (snapping is deterministic)."""
import numpy as np, core
def margin(book, ops, h0=None):
    h0 = np.eye(5, dtype=complex) if h0 is None else h0
    worst = np.inf
    pairs = [(h0, g, core.NEXT[core.E, g]) for g in (0, 1)] + [(book[s], g, core.NEXT[s, g]) for s in range(120) for g in (0, 1)]
    for c, g, t in pairs:
        x = ops[g] @ c
        d = np.sqrt((abs(x[None] - book) ** 2).sum((1, 2)))
        other = np.min(np.delete(d, t))
        worst = min(worst, other - d[t])
    return float(worst)
def snapped_acc(book, ops, rng, L, n=32):
    words = rng.integers(0, 2, (n, L)); h = np.broadcast_to(np.eye(5, dtype=complex), (n, 5, 5)).copy(); s = np.full(n, core.E)
    for k in range(L):
        h = ops[words[:, k]] @ h; s = core.NEXT[s, words[:, k]]
        d = (abs(h[:, None] - book[None]) ** 2).sum((2, 3)); h = book[np.argmin(d, 1)].copy()
    return float(np.mean(np.argmin((abs(h[:, None] - book[None]) ** 2).sum((2, 3)), 1) == s))
def one(seed, delta, arm, L):
    rng, ops, exact = core.setup(seed, delta)
    if arm == "EXACT":
        book = exact
    else:
        book, have = core.data_book(rng, ops, 4000, 20)
        if not have.all():
            return dict(seed=seed, delta=delta, arm=arm, L=L, coverage=int(have.sum()), margin=None, acc=None)
    m = margin(book, ops)
    return dict(seed=seed, delta=delta, arm=arm, L=L, coverage=120, margin=round(m, 4), acc=snapped_acc(book, ops, rng, L))
if __name__ == "__main__":
    import sys, json
    a, b = int(sys.argv[1]), int(sys.argv[2]); L = int(sys.argv[3]); out = sys.argv[4]
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(s, d, arm, L) for s in range(a, b) for d in (0.05, 0.1, 0.15, 0.2, 0.3) for arm in ("DATA", "EXACT")]
    with ProcessPoolExecutor() as ex, open(out, "a") as fh:
        for r in ex.map(one, *zip(*jobs)):
            fh.write(json.dumps(r) + "\n"); fh.flush(); print(r, flush=True)
