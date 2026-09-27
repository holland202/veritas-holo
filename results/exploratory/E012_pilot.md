# E012 pilot (exploratory, seeds 701-710: the E011 pilot's seeds, disjoint from the registered 741-770)

**Question (E011's open P6).** Can a better codebook than E011's per-state mean be built from noisy
operators?

**Tried and dropped** (δ = 0.1 / 0.15 / 0.2 / 0.3, certified out of 10):

| codebook | 0.1 | 0.15 | 0.2 | 0.3 |
|---|---|---|---|---|
| DATA, per-state mean (E011) | 8 | 2 | 0 | 0 |
| least-squares consistent codebook (c_E = I, O_g c_s ≈ c_gs) | 7 | 0 | 0 | 0 |
| DATA projected to unitary | 9 | 2 | 0 | 0 |
| unitary fixed point from DATA | 5 | 4 | 2 | 0 |

The least-squares codebook shrank toward zero (entry norms about 0.06 at δ = 0.2), so its margins shrank too.

**What worked: projecting the operators onto the group's relator orders.** The labelled transitions give
the order of t (2), of c (5) and of the product tc (4). Round each operator's spectrum to roots of unity
of its order, then alternate with the same rounding of the product. The codebook is the closure of the
projected operators from the identity (`relproj.py`).

| codebook | 0.1 | 0.15 | 0.2 | 0.3 |
|---|---|---|---|---|
| SPECTRAL: t and c rounded, no product relation | 9 | 7 | 3 | 0 |
| ALT: alternating projection with all three orders, 20 rounds | 10 | 10 | 10 | 8 |
| WRONG: ALT told tc has order 3 | 0 | 0 | 0 | 0 |
| EXACT: the true representation (reference) | 10 | 10 | 10 | 10 |

The margins agreed with 10⁴-step snapped runs for ALT in 40 of 40 cases (38 certified and exact, 2
uncertified and wrong). Median ALT margins at δ = 0.1-0.2 were close to, or above, the exact
codebook's: 1.608 against 1.503 at δ = 0.1. The projected operators fit the noisy ones better than the
true representation does. When the relator is wrong, the method fails completely, so the relation
information is what does the work.
