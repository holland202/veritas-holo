"""E009 pilot: do E005's learned operators hold up at 10^3-10^4 steps, and does snapping the running state to the
readout's own class centroids help? Also: a blind closure check (does the operators' orbit close up?)."""
import json, sys, time, numpy as np
import os; _R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'); sys.path.insert(0, _R); sys.path.insert(0, os.path.join(_R, 'experiments', 'E004_group_state'))
import importlib.util
sp = importlib.util.spec_from_file_location('e5r', os.path.join(_R, 'experiments', 'E005_learned_state', 'run.py'))
e5 = importlib.util.module_from_spec(sp); sys.modules['e5r'] = e5; sp.loader.exec_module(e5)
e4 = e5.e004
from veritas_holo.learn import all_words, train_operators
from concurrent.futures import ProcessPoolExecutor
WORDS = all_words(2, 8); Y = np.array([int(e4.labels(w[None])[0]) for w in WORDS])


def run_words(words, ops, cent=None, every=0):
    n = len(words); h = np.broadcast_to(np.eye(ops.shape[1], dtype=complex), (n,) + ops.shape[1:]).copy()
    for k in range(words.shape[1]):
        h = ops[words[:, k]] @ h
        if every and (k + 1) % every == 0:
            f = h.reshape(n, -1)
            idx = np.argmin((abs(f[:, None, :] - cent[None]) ** 2).sum(2), 1)
            h = cent[idx].reshape(h.shape).copy()
    return h.reshape(n, -1)


def closure_size(ops, tol=0.3, cap=600):
    elems = [np.eye(ops.shape[1], dtype=complex)]; frontier = [elems[0]]
    while frontier and len(elems) < cap:
        new = []
        for e in frontier:
            for o in ops:
                m = o @ e
                if min(np.linalg.norm(m - x) for x in elems) > tol:
                    elems.append(m); new.append(m)
                    if len(elems) >= cap:
                        return cap
        frontier = new
    return len(elems)


def one(seed):
    t0 = time.time()
    ops = train_operators(WORDS, Y, 8, np.random.default_rng(seed))
    rng = np.random.default_rng(5000 + seed)
    w = rng.integers(0, 2, (6000, 160)); y = e4.labels(w)
    ftr = run_words(w, ops)
    classes = np.unique(y); cent = np.stack([ftr[y == k].mean(0) for k in classes])
    res = {"seed": seed, "closure": closure_size(ops)}
    for L in (160, 1000, 5000):
        wt = rng.integers(0, 2, (500, L)); yt = e4.labels(wt)
        for tag, ev in (("raw", 0), ("snap8", 8)):
            f = run_words(wt, ops, cent, ev)
            res[f"{tag}{L}"] = float(np.mean(classes[np.argmin((abs(f[:, None, :] - cent[None]) ** 2).sum(2), 1)] == yt))
    res["s"] = round(time.time() - t0)
    return res


if __name__ == "__main__":
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(one, range(int(sys.argv[1]), int(sys.argv[2]))):
            print(json.dumps(r), flush=True)
