# E011: a finite certificate for snapped decoding. Registration

Status: **Registered** (2026-09-27), after the pilot on seeds 701-710
(`results/exploratory/E011_pilot.md`), and before any run on the registered seeds 711-740.

## Claim

Snapping a running state to a finite codebook {c_s} (E008) is either exact for every length or not.
Which one holds is decided by a certificate computed from 242 operator applications: the margin
defined in `cert.py`. For operators with real error, a codebook built from labelled data (per-state
mean holonomy) earns the certificate at small error, and loses it before the exact codebook does.

## Frozen setup

- S5 with t = (0 1) and c = (0 1 2 3 4), in a Haar-random 5-dimensional basis. Each operator is
  multiplied by exp(iδH), where H is a random Hermitian matrix (as in E008).
- DATA codebook: the per-state mean holonomy of 4000 random labelled words of length 1-20. EXACT
  codebook: the 120 class matrices in the same basis.
- A run is certified when margin > 0. Its accuracy is the fraction of 32 random words of length 10⁴,
  decoded with snapping after every step, whose final state is right.
- Grid: seeds 711-740 × δ ∈ {0.05, 0.1, 0.15, 0.2, 0.3} × {DATA, EXACT}, 300 runs.
  Command: `python experiments/E011_snap_certificate/cert.py 711 741 10000 OUT.jsonl`.

## Registered predictions

- **P1 (soundness; a theorem, so this checks the implementation)** Every certified run has accuracy 1.0.
- **P2 (the certificate is not loose)** Every uncertified run has accuracy < 1.0.
- **P3 (anti-vacuity: the certificate can say no)** At least 30 of the 300 runs are uncertified.
- **P4 (data codebook range)** DATA is certified in at least 27 of 30 seeds at δ = 0.05, and in at most
  3 of 30 at δ = 0.2.
- **P5 (exact codebook range)** EXACT is certified in 30 of 30 seeds at every δ ≤ 0.2, and in at least
  27 of 30 at δ = 0.3.

## Unrun, left open

- **P6** A codebook chosen to maximise the margin, rather than by averaging, extends DATA's certified
  range beyond δ = 0.1. Nothing is built for it yet.
- P2 is only about length 10⁴ and 32 words. A negative margin at a rarely visited (s, g) could let a
  short run pass; the pilot never showed it.

## Limits

- Only S5, one presentation, dimension 5, one noise model.
- The certificate needs the state labels of the transitions (that is, the group's multiplication
  table). A system without labelled transitions cannot compute it.
