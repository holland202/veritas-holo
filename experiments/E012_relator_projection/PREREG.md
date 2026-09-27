# E012: relator projection recovers a certified codebook from noisy operators. Registration

Status: **Registered** (2026-09-27), after the pilot on seeds 701-710 (`results/exploratory/E012_pilot.md`),
before any run on the registered seeds 741-770.

## Claim

Given noisy operators and the orders of three relators, read from labelled transitions, alternating
spectral projection (`relproj.py`, 20 rounds) gives a codebook that E011's certificate accepts far
beyond where E011's data codebook stops. The third relation (the order of tc) is necessary, and a wrong
relator destroys it.

## Frozen setup

- E011's noise model and group (S5, t = (0 1), c = (0 1 2 3 4), dimension 5), seeds 741-770 × δ ∈ {0.1,
  0.15, 0.2, 0.3}: 120 cases.
- Arms, all certified by E011's margin (> 0):
  - DATA: E011's per-state mean;
  - SPECTRAL: t and c rounded only;
  - ALT: all three orders, 20 rounds;
  - WRONG: ALT with order 3 for tc;
  - EXACT: reference.
- ALT is also run for 32 words of length 10⁴ with snapping.
- Command: `python experiments/E012_relator_projection/relproj.py 741 771 OUT.jsonl` (resumable).

## Registered predictions

- **R1** ALT is certified in at least 28 of 30 seeds at each δ ∈ {0.1, 0.15, 0.2}.
- **R2** ALT is certified in at least 20 of 30 seeds at δ = 0.3.
- **R3** At δ = 0.15 and at δ = 0.2, ALT is certified in at least 15 more seeds than DATA.
- **R4 (the third relation matters)** At δ = 0.2, ALT is certified in at least 10 more seeds than SPECTRAL.
- **R5 (null)** WRONG is certified in 0 of 120.
- **R6 (the certificate, again)** Every certified ALT case decodes 32/32 at L = 10⁴, and every uncertified one
  fewer.

## Unrun, left open

- **R7** Relator orders found without labels: the smallest k for which O^k is close to I. That would make
  the method work from the operators alone.
- The same method for learned operators (E005) whose training failed. Can projection repair a failed run?

## Limits

S5 only, one presentation, three relators chosen by hand from it, one noise model. The orders come from
labelled transitions, as the certificate itself needs.
