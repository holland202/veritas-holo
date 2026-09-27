# Label-free group discovery (exploratory pilot, seeds 701-710, not registered)

`experiments/E012_relator_projection/labelfree.py`. No labels are used. For each triple of candidate
orders (t, c, tc) ∈ {2..6}³, project the noisy operators (E012) and keep the triple with the smallest
fit residual whose closure is a finite group (at most 1500 elements). The closure is the codebook, and
its own multiplication table gives the certificate. Only afterwards are the true labels used, to score
long runs.

| δ | right orders (2,5,4) | closure of 120 | certified | exact at L = 10⁴ |
|---|---|---|---|---|
| 0.1 | 9/10 | 8/10 | 9/10 | 9/10 |
| 0.15 | 8/10 | 8/10 | 10/10 | 8/10 |
| 0.2 | 8/10 | 8/10 | 10/10 | 8/10 |
| 0.3 | 7/10 | 5/10 | 9/10 | 7/10 |

**The important failure.** 38 cases were certified but only 30 were exact against the truth. When the
wrong group is discovered (closures of 1152, 72, 768 or 48 elements), the certificate still holds: the
snapped state tracks the *discovered* group perfectly. A certificate computed without labels proves
self-consistency, not correctness. Before registering, the discovered group needs a check against a
few labelled words.
