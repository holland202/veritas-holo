"""E012: recover a snapping codebook from noisy operators by projecting them onto the group's relator orders.

Given noisy operators O_t, O_c (E008/E011 noise model) and three orders read from the labelled transitions
(t has order 2, c order 5, the product tc order 4; these are relators of S5's presentation), alternate:
  R_t, R_c <- nearest unitary with eigenvalues rounded to the k-th roots of unity of their order,
  P       <- R_c R_t with eigenvalues rounded to 4th roots,
  R_c     <- round(average of R_c and P R_t^dagger), R_t <- round(average of R_t and R_c^dagger P).
The codebook is the breadth-first closure of R_t, R_c from the identity. E011's margin certifies it.
"""
import os, sys
from collections import deque
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "E011_snap_certificate"))
import core  # noqa: E402  (E011's setup, data_book and group tables)
import cert  # noqa: E402  (E011's margin and snapped_acc)


def order_of(word):
    s, k = core.E, 0
    while True:
        for g in word:
            s = core.NEXT[s, g]
        k += 1
        if s == core.E:
            return k


def round_spectrum(O, k):
    w, V = np.linalg.eig(O)
    roots = np.exp(2j * np.pi * np.arange(k) / k)
    R = V @ np.diag(roots[np.argmin(abs(w[:, None] - roots[None]), 1)]) @ np.linalg.inv(V)
    u, _, vh = np.linalg.svd(R)
    return u @ vh


def project(ops, rounds, orders):
    kt, kc, ktc = orders
    Rt, Rc = round_spectrum(ops[0], kt), round_spectrum(ops[1], kc)
    for _ in range(rounds):
        P = round_spectrum(Rc @ Rt, ktc)
        Rc = round_spectrum(0.5 * (P @ Rt.conj().T + Rc), kc)
        Rt = round_spectrum(0.5 * (Rc.conj().T @ P + Rt), kt)
    return np.stack([Rt, Rc])


def bfs_book(R):
    book = np.zeros((120, 5, 5), complex)
    book[core.E] = np.eye(5)
    seen, q = {core.E}, deque([core.E])
    while q:
        s = q.popleft()
        for g in (0, 1):
            t = core.NEXT[s, g]
            if t not in seen:
                seen.add(t); book[t] = R[g] @ book[s]; q.append(t)
    return book


TRUE_ORDERS = (order_of([0]), order_of([1]), order_of([1, 0]))  # (2, 5, 4)


def one(seed, delta, L=10000):
    rng, ops, exact = core.setup(seed, delta)
    data, have = core.data_book(rng, ops, 4000, 20)
    alt = bfs_book(project(ops, 20, TRUE_ORDERS))
    spectral = bfs_book(project(ops, 0, TRUE_ORDERS))
    wrong = bfs_book(project(ops, 20, (TRUE_ORDERS[0], TRUE_ORDERS[1], 3)))
    out = dict(seed=seed, delta=delta, coverage=int(have.sum()),
               m_data=round(cert.margin(data, ops), 4), m_spectral=round(cert.margin(spectral, ops), 4),
               m_alt=round(cert.margin(alt, ops), 4), m_wrong=round(cert.margin(wrong, ops), 4),
               m_exact=round(cert.margin(exact, ops), 4))
    out["acc_alt"] = cert.snapped_acc(alt, ops, np.random.default_rng(seed + 10**6), L)
    return out


if __name__ == "__main__":
    import json
    from concurrent.futures import ProcessPoolExecutor
    a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    done = set()
    if os.path.exists(out):
        done = {(r["seed"], r["delta"]) for r in map(json.loads, open(out))}
    jobs = [(s, d) for s in range(a, b) for d in (0.1, 0.15, 0.2, 0.3) if (s, d) not in done]
    with ProcessPoolExecutor(2) as ex, open(out, "a") as fh:
        for r in ex.map(one, *zip(*jobs)):
            fh.write(json.dumps(r, sort_keys=True) + "\n"); fh.flush(); print(r, flush=True)
