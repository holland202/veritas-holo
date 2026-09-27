# E006 (E005-U1): can the learned operators say whether training worked, before any test is opened? Registration

Status: **Registered** (2026-09-27), after the pilot on seeds 21-40 (`results/exploratory/E006_pilot.md`)
and before any run on the registered seeds 41-80.

## Question

E005's training succeeds on some seeds and fails on others. Can a check computed from the trained
operators alone, using no test words and no test labels, tell the two apart well enough to pick a
restart? The check uses prior knowledge: five words that are the identity in S5. It is therefore a
**mechanistic diagnostic that knows the group's relations**, not a self-assessment by a model that
knows nothing about the task. A blind version is E006-U1 below.

## Frozen setup

- Training exactly as E005 (`veritas_holo/learn.py`; 8 × 8 unitary; 510 words of length ≤ 8; 3000
  steps). Test exactly as E005 (nearest-centroid readout; fresh words of length 160; accuracy ≥ 0.99
  counts as success).
- **Relator score** = min over E005's five relators of #{eigenvalues within 1e-2 of 1}, out of 8.
- **Sealing:** for each seed, the runner computes the score and writes the accept/reject decision to
  the output **before** it generates or reads any test word for that seed. The order is fixed in code.
- **Acceptance rule:** ACCEPT if score ≥ 5, otherwise REJECT (restart).
- **Seeds 41-80** (40 runs). For the restart policy, the seeds form 10 jobs in order: (41-44),
  (45-48), …, (77-80). A job takes the first seed of its group that is ACCEPTED, or none if no seed is.

## Registered predictions

- **D1 (precision)** Of the ACCEPTED runs, at least 95% succeed at L = 160.
- **D2 (rejects are mostly failures)** Of the runs with score ≤ 3, at most 10% succeed.
- **D3 (the base rate is neither trivial nor hopeless)** The overall success rate lies in [0.5, 0.9].
  If every run succeeded, or none did, no diagnostic would be needed or possible.
- **D4 (the policy works)** At least 9 of the 10 jobs end with a successful run. The comparison is
  "take the first seed of each group without looking", reported alongside; at the pilot's base rate
  that should succeed about 7 times in 10.
- **D5 (cost)** The mean number of trainings per job is reported. No threshold is registered.

Score 4, the ambiguous band in the pilot, carries no prediction of its own. Its runs are reported.

## Limits

- The diagnostic uses the known relations of S5. It says nothing about tasks whose structure is
  unknown.
- One group, one width, one training setup.

## Unrun

- **E006-U1 (blind)** A diagnostic that knows nothing about the group. For example: do the learned
  operators have finite order, and do short words that the training data says are equal map to the
  same matrix? The relations would be read from the training data, not supplied.
