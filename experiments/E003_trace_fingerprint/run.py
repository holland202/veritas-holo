#!/usr/bin/env python3
"""E003 - a holonomy fingerprint for concurrent histories. Registered in PREREG.md (T1-T8) before this code.

  python experiments/E003_trace_fingerprint/run.py [--json OUT.json]
Exit: 0 every registered prediction held | 1 at least one did not
"""
import argparse
import json
import os
import platform
import statistics
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from veritas_holo.trace import Alphabet, Fingerprinter, base_digest, base_extend, det, normal_form  # noqa: E402

N_ACTIONS, N_RES, LEN, LOGS, SEEDS, SWAPS, SEGS = 12, 5, 200, 200, range(1, 6), 50, 16


def legal_shuffle(word, al, rng, k=SWAPS):
    w = list(word)
    for _ in range(k):
        ok = [i for i in range(len(w) - 1) if al.independent(w[i], w[i + 1])]
        i = ok[int(rng.integers(len(ok)))]
        w[i], w[i + 1] = w[i + 1], w[i]
    return w


def illegal_swap(word, al, rng):
    w = list(word)
    ok = [i for i in range(len(w) - 1) if w[i] != w[i + 1] and not al.independent(w[i], w[i + 1])]
    i = ok[int(rng.integers(len(ok)))]
    w[i], w[i + 1] = w[i + 1], w[i]
    return w


def hexes(hs):
    return tuple(h.hexdigest() for h in hs)


def tree_merge(fps, merge):
    while len(fps) > 1:
        fps = [merge(fps[i], fps[i + 1]) if i + 1 < len(fps) else fps[i] for i in range(0, len(fps), 2)]
    return fps[0]


def median_time(fn, reps=21):
    ts = []
    for _ in range(reps):
        t = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t)
    return statistics.median(ts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    al = Alphabet.random(N_ACTIONS, N_RES, np.random.default_rng(0))
    c = {k: 0 for k in ("t1_truth", "t1_hf", "t2_truth", "t2_hf", "t3_agree", "t3_pairs", "t4_split",
                        "t4_tree", "n1_accept", "n2_reject", "base_agree", "sl2_ok")}
    t_hf = t_base = 0.0
    n = 0
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        hf = Fingerprinter(al, rng)
        n1 = Fingerprinter(al, rng, commuting=True)
        n2 = Fingerprinter(al, rng, one_block=True)
        c["sl2_ok"] += all(det(m) == 1 for f in (hf, n1, n2) for d in f.mats for m in d.values())
        logs = [rng.integers(0, N_ACTIONS, LEN).tolist() for _ in range(LOGS)]
        for w in logs:
            n += 1
            nf = normal_form(w, al)
            s, x = legal_shuffle(w, al, rng), illegal_swap(w, al, rng)
            t = time.perf_counter()
            fw = hf.of(w)
            t_hf += time.perf_counter() - t
            t = time.perf_counter()
            bw = hexes(base_digest(w, al))
            t_base += time.perf_counter() - t
            fs, fx = hf.of(s), hf.of(x)
            same_s, same_x = normal_form(s, al) == nf, normal_form(x, al) == nf
            c["t1_truth"] += same_s
            c["t1_hf"] += same_s and fs == fw
            c["t2_truth"] += not same_x
            c["t2_hf"] += (not same_x) and fx != fw
            other = rng.integers(0, N_ACTIONS, LEN).tolist()
            pairs = [(w, s, fw, fs, same_s), (w, x, fw, fx, same_x),
                     (w, other, fw, hf.of(other), normal_form(other, al) == nf)]
            for u, v, fu, fv, truth in pairs:
                c["t3_pairs"] += 1
                c["t3_agree"] += (fu == fv) == truth
                c["base_agree"] += (bw == hexes(base_digest(v, al))) == truth
            k = int(rng.integers(1, LEN))
            c["t4_split"] += hf.merge(hf.of(w[:k]), hf.of(w[k:])) == fw
            cuts = np.linspace(0, LEN, SEGS + 1).astype(int)
            c["t4_tree"] += tree_merge([hf.of(w[cuts[i]:cuts[i + 1]]) for i in range(SEGS)], hf.merge) == fw
            c["n1_accept"] += n1.of(x) == n1.of(w)
            c["n2_reject"] += n2.of(s) != n2.of(w)
    # T7 merge cost
    rng = np.random.default_rng(99)
    hf = Fingerprinter(al, rng)
    head = rng.integers(0, N_ACTIONS, LEN).tolist()
    fu, bu = hf.of(head), base_digest(head, al)
    cost = {}
    for m in (100, 100_000):
        seg = rng.integers(0, N_ACTIONS, m).tolist()
        fv = hf.of(seg)
        cost[m] = (median_time(lambda: hf.merge(fu, fv)), median_time(lambda: base_extend(bu, seg, al), reps=7))
    hf_ratio, base_ratio = cost[100_000][0] / cost[100][0], cost[100_000][1] / cost[100][1]

    print(f"VERITAS-HOLO E003 | seeds {SEEDS.start}-{SEEDS.stop - 1} | {platform.machine()} | "
          f"Python {platform.python_version()} | NumPy {np.__version__}")
    print(f"alphabet: {N_ACTIONS} actions over {N_RES} resources: "
          + " ".join(f"{i}:{''.join(map(str, sorted(t)))}" for i, t in enumerate(al.touches)))
    print(f"logs: {n} of length {LEN}; legal shuffle = {SWAPS} independent swaps; SL(2, F_p) check "
          f"{c['sl2_ok']} of {len(SEEDS)} seeds")
    print(f"BASE (per-resource SHA-256) equality agrees with ground truth on {c['base_agree']} of "
          f"{c['t3_pairs']} pairs")
    print(f"merge time HF: {cost[100][0] * 1e6:.1f} us (|v|=100), {cost[100_000][0] * 1e6:.1f} us (|v|=100000)")
    print(f"extend time BASE: {cost[100][1] * 1e6:.1f} us (|v|=100), {cost[100_000][1] * 1e6:.1f} us (|v|=100000)")
    print(f"build time per event: HF {t_hf / (n * LEN) * 1e6:.2f} us, BASE {t_base / (n * LEN) * 1e6:.2f} us")
    v = {
        "T1": (c["t1_truth"] == n and c["t1_hf"] == n, f"legal shuffles same history {c['t1_truth']}/{n}, "
                                                        f"HF unchanged {c['t1_hf']}/{n}"),
        "T2": (c["t2_truth"] == n and c["t2_hf"] == n, f"illegal swaps different history {c['t2_truth']}/{n}, "
                                                        f"HF changed {c['t2_hf']}/{n}"),
        "T3": (c["t3_agree"] == c["t3_pairs"], f"HF equality = ground truth on {c['t3_agree']}/{c['t3_pairs']} pairs"),
        "T4": (c["t4_split"] == n and c["t4_tree"] == n, f"merge(F(u),F(v)) = F(uv) {c['t4_split']}/{n}; "
                                                          f"{SEGS}-segment tree {c['t4_tree']}/{n}"),
        "T5": (c["n1_accept"] / n >= 0.99, f"N1 commuting accepts illegal swaps {c['n1_accept']}/{n} "
                                           f"= {c['n1_accept'] / n:.4f} >= 0.99"),
        "T6": (c["n2_reject"] / n >= 0.99, f"N2 one-block rejects legal shuffles {c['n2_reject']}/{n} "
                                           f"= {c['n2_reject'] / n:.4f} >= 0.99"),
        "T7": (hf_ratio < 3 and base_ratio > 100, f"merge-time ratio 100000/100: HF {hf_ratio:.2f} < 3, "
                                                  f"BASE {base_ratio:.1f} > 100"),
        "T8": (t_hf > t_base, f"per-event build: HF {t_hf / t_base:.1f}x BASE (HF slower, as registered)"),
    }
    for k, (ok, d) in v.items():
        print(f"{'HELD  ' if ok else 'FAILED'} {k}  {d}")
    held = sum(ok for ok, _ in v.values())
    print(f"VERDICT  {held} of {len(v)} registered predictions held")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"experiment": "E003", "machine": platform.machine(), "python": platform.python_version(),
                       "numpy": np.__version__, "counts": c, "logs": n,
                       "alphabet": [sorted(t) for t in al.touches],
                       "merge_cost_s": {str(k): list(x) for k, x in cost.items()},
                       "verdicts": {k: {"held": bool(ok), "detail": d} for k, (ok, d) in v.items()}},
                      fh, indent=1, sort_keys=True)
    sys.exit(0 if held == len(v) else 1)


if __name__ == "__main__":
    main()
