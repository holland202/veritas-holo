"""E007 (registered in PREREG.md): held-out transition pairs. Usage:
  python experiments/E007_heldout_composition/run.py [--partial F.jsonl] [--json OUT.json]

Originally the exploratory pilot: S5 by its 4 adjacent transpositions; ordered pairs (s1,s2) and (s3,s4) never occur in
training. Readout is fitted on long words WITHOUT those pairs and tested on long words WITH them."""
import itertools, json, sys, time
import numpy as np
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from veritas_holo.learn import train_operators
from concurrent.futures import ProcessPoolExecutor

GENS = [tuple(j + 1 if k == j else j if k == j + 1 else k for k in range(5)) for j in range(4)]  # s_{j}=(j j+1)
PERMS = list(itertools.permutations(range(5))); IDX = {p: i for i, p in enumerate(PERMS)}
NEXT = np.array([[IDX[tuple(g[p[i]] for i in range(5))] for g in GENS] for p in PERMS])
HELD = {(0, 1), (2, 3)}


def labels(words):
    out = []
    for w in words:
        s = IDX[tuple(range(5))]
        for a in w:
            s = NEXT[s, a]
        out.append(s)
    return np.array(out)


def clean(w):
    return all((w[i], w[i + 1]) not in HELD for i in range(len(w) - 1))


def sample(rng, n, L, avoid):
    ws = []
    while len(ws) < n:
        w = [int(rng.integers(4))]
        while len(w) < L:
            a = int(rng.integers(4))
            if avoid and (w[-1], a) in HELD:
                continue
            w.append(a)
        if avoid or not clean(w):
            ws.append(w)
    return np.array(ws)


def hol(words, ops):
    h = np.broadcast_to(np.eye(ops.shape[1], dtype=complex), (len(words),) + ops.shape[1:]).copy()
    for k in range(words.shape[1]):
        h = ops[words[:, k]] @ h
    return h.reshape(len(words), -1)


def centroid_acc(ftr, ytr, fte, yte):
    cl = np.unique(ytr); cent = np.stack([ftr[ytr == k].mean(0) for k in cl])
    d = (abs(fte[:, None, :] - cent[None]) ** 2).sum(2)
    return float(np.mean(cl[np.argmin(d, 1)] == yte))


def score(ops):
    rel = [[i, i] for i in range(4)] + [[i, i + 1] * 3 for i in range(3)] + [[i, j] * 2 for i in range(4) for j in range(i + 2, 4)]
    c = []
    for r in rel:
        m = np.eye(ops.shape[1], dtype=complex)
        for a in r:
            m = ops[a] @ m
        c.append(int(np.sum(abs(np.linalg.eigvals(m) - 1) < 1e-2)))
    return min(c)


def to_pairs(w):
    """Second-order tokens: the first letter alone, then (previous, current) pairs. A model built on these can only
    use transitions it has seen: the memorisation alternative made concrete."""
    w = list(w)
    return np.array([w[0]] + [4 + 4 * w[k - 1] + w[k] for k in range(1, len(w))])


def one(args):
    seed, arm = args
    t0 = time.time()
    words = [np.array(w) for L in range(1, 6) for w in itertools.product(range(4), repeat=L)]
    if arm in ("HELDOUT", "PAIR"):
        words = [w for w in words if clean(list(w))]
    y = labels(words)
    if arm == "PAIR":
        ops = train_operators([to_pairs(w) for w in words], y, 8, np.random.default_rng(seed), n_letters=20)
        sc = -1
    else:
        ops = train_operators(words, y, 8, np.random.default_rng(seed), n_letters=4)
        sc = score(ops)
    enc = (lambda ws: np.stack([to_pairs(w) for w in ws])) if arm == "PAIR" else (lambda ws: ws)
    rng = np.random.default_rng(1000 + seed)
    res = {"seed": seed, "arm": arm, "n_train": len(words), "labels_covered": int(len(set(y.tolist()))), "score": sc}
    for L in (40, 160):
        cw = sample(rng, 6000, L, True); hw = sample(rng, 2000, L, False); cte = sample(rng, 2000, L, True)
        ycw, yhw, ycte = labels(cw), labels(hw), labels(cte)
        fc = hol(enc(cw), ops)
        res[f"clean{L}"] = centroid_acc(fc, ycw, hol(enc(cte), ops), ycte)
        res[f"held{L}"] = centroid_acc(fc, ycw, hol(enc(hw), ops), yhw)
    res["s"] = round(time.time() - t0)
    return res


SEEDS = list(range(301, 341))


def verdicts(runs):
    ok = lambda r, k: r[k] >= 0.99  # noqa: E731
    held = [r for r in runs if r["arm"] == "HELDOUT"]
    pair = [r for r in runs if r["arm"] == "PAIR"]
    hs = [r for r in held if ok(r, "clean160")]
    ps = [r for r in pair if ok(r, "clean160")]
    v = {
        "H1": (len(hs) >= 5 and all(ok(r, "held160") for r in hs),
               f"{len(hs)} HELDOUT runs learned CLEAN words (need >= 5); HELD accuracy at L=160 on them: "
               + ", ".join(f"{r['held160']:.4f}" for r in hs) + " (all >= 0.99)"),
        "H2": (all(r["held160"] < 0.05 for r in pair),
               f"PAIR HELD accuracy at L=160, max over {len(pair)} seeds: {max(r['held160'] for r in pair):.4f} (< 0.05)"),
        "H3": (len(ps) >= 1, f"{len(ps)} PAIR runs learned CLEAN words (>= 1), so the null is not just a weak learner"),
    }
    return v, hs, ps


def main():
    import argparse
    import platform
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    done = {}
    if a.partial and os.path.exists(a.partial):
        for ln in open(a.partial, encoding="utf-8"):
            r = json.loads(ln)
            done[(r["seed"], r["arm"])] = r
    todo = [(s, arm) for s in SEEDS for arm in ("HELDOUT", "PAIR") if (s, arm) not in done]
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(one, todo):
            done[(r["seed"], r["arm"])] = r
            if a.partial:
                with open(a.partial, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(r, sort_keys=True) + "\n")
    runs = [done[(s, arm)] for s in SEEDS for arm in ("HELDOUT", "PAIR")]
    print(f"VERITAS-HOLO E007 | seeds {SEEDS[0]}-{SEEDS[-1]} | {platform.machine()} | Python {platform.python_version()} "
          f"| NumPy {np.__version__}")
    print("held-out ordered pairs (s1,s2) and (s3,s4); readout fitted on CLEAN long words; scored on CLEAN and HELD")
    print(f"{'seed':>4} {'arm':>7} {'clean40':>8} {'held40':>8} {'clean160':>9} {'held160':>8}")
    for r in runs:
        print(f"{r['seed']:>4} {r['arm']:>7} {r['clean40']:8.4f} {r['held40']:8.4f} {r['clean160']:9.4f} {r['held160']:8.4f}")
    v, hs, ps = verdicts(runs)
    for k, (good, d) in v.items():
        print(f"{'HELD  ' if good else 'FAILED'} {k}  {d}")
    held_n = sum(g for g, _ in v.values())
    print(f"VERDICT  {held_n} of {len(v)} registered predictions held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E007", "machine": platform.machine(), "runs": runs,
                       "verdicts": {k: {"held": bool(g), "detail": d} for k, (g, d) in v.items()}}, fh, indent=1, sort_keys=True)
    sys.exit(0 if held_n == len(v) else 1)


if __name__ == "__main__":
    main()
