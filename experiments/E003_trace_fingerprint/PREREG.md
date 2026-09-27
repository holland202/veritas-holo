# E003: a holonomy fingerprint for concurrent histories. Registration

Status: **Registered** (2026-09-27), before any E003 code was written. Results go in `RESULTS.md`.

## Where this comes from

E002 showed that the signal in a holonomy comes from which operators do not commute. Commuting
operators carried nothing, and nothing about the information was beyond a cheap recurrence. E003
does not look for hidden information. It uses the commutation pattern **on purpose**, as a design
parameter, and asks about the one property a holonomy has that a sequential hash does not:
**it composes**. The holonomy of A then B is the product of the two holonomies, so it can be computed
from the two fingerprints alone.

This is not an answer to E002's E7 (information beyond an equal-cost recurrence). E7 stays open.

## The problem

A log is a sequence of actions. Each action touches a set of resources (a file, a motor, an
account). Two actions that touch no common resource are **independent**: running them in either
order gives the same outcome. Two logs describe **the same history** when one can be turned into the
other by swapping adjacent independent actions. (This is Mazurkiewicz trace equivalence, the
standard model of concurrent histories.) Logs recorded by different processes or devices interleave
independent actions in arbitrary order, so a byte hash of the log calls equal histories different.

**Wanted:** a fixed-size fingerprint F such that

1. F(u) = F(v) when u and v are the same history, however the independent actions interleave;
2. F(u) ≠ F(v) when they are not (for non-adversarial logs);
3. F(u·v) can be computed from F(u) and F(v) alone, without either raw log, at a cost that does not
   grow with the log lengths. Segments recorded on different devices can then be merged, or
   aggregated in a tree, from their fingerprints.

## Construction (the holonomy fingerprint, HF)

- Work in SL(2, F_p), p = 2^61 − 1, with exact integer arithmetic. There is no floating point, so
  the E001 replay issue cannot arise.
- For each (action a, resource r) with r ∈ touches(a), draw a random matrix M[a, r] ∈ SL(2, F_p)
  from a seeded generator.
- The fingerprint is one 2×2 matrix per resource: HF(w)[r] = the product of M[a, r] over the actions
  a of w that touch r, in order (later actions on the left).
- Merge: HF(u·v)[r] = HF(v)[r] · HF(u)[r]. That is R matrix products, independent of the log lengths.

Why it should work: two independent actions touch disjoint resources, so they multiply into different
blocks and commute. A dependent pair shares a block, and two random SL(2, F_p) matrices almost never
commute. The fingerprint is a holonomy in the product group SL(2, F_p)^R, and the independence
relation is built into which blocks commute. (Equivalently, HF hashes each resource's projection of
the log. The projection lemma for traces says those projections determine the history. This is known
mathematics; what is being tested is the implementation and the composition property.)

## Setup (fixed before running)

- 5 resources, 12 actions. Each action touches 1 or 2 resources, drawn from seed 0; the run prints
  the table. Logs are 200 uniformly random actions long. Seeds 1-5, 200 logs per seed (1000 logs).
- **Ground truth** does not use HF or projections: the lexicographic normal form of the trace
  (repeatedly emit the smallest action that has no dependent action before it). Two logs are the
  same history if and only if their normal forms are equal.
- **Legal shuffle:** 50 random swaps of adjacent, independent actions.
- **Illegal swap:** one swap of adjacent, distinct actions that share a resource.
- **Baseline (BASE):** per-resource SHA-256 chains over each resource's projection of the log. BASE
  decides equality exactly as HF should, and more cheaply per event. It cannot merge two digests,
  though: extending a chain needs the second segment's raw events.

## Registered predictions

- **T1 (invariance).** For each of the 1000 logs, the ground truth confirms that the legal shuffle
  is the same history, and HF is unchanged: 1000 of 1000.
- **T2 (sensitivity).** For each of the 1000 logs, the ground truth confirms that the illegal swap
  is a different history, and HF changes: 1000 of 1000.
- **T3 (agreement).** On 1000 pairs of independent random logs plus the 2000 pairs from T1 and T2,
  HF equality equals ground-truth equality on every pair.
- **T4 (composition).** For 1000 random splits u·v, merge(HF(u), HF(v)) = HF(u·v): 1000 of 1000.
  A 16-segment balanced-tree merge equals the fingerprint of the whole log: 1000 of 1000.
- **T5 (null N1, commuting).** The same construction with diagonal (commuting) matrices. It must
  **accept** illegal swaps as the same history. Acceptance ≥ 0.99. This is the E002 ABELIAN lesson
  used as a control: without noncommutativity the fingerprint cannot see order.
- **T6 (null N2, one block).** Every action multiplies into one shared block, so every pair is
  treated as dependent. It must **reject** legal shuffles. Rejection ≥ 0.99. This shows that
  invariance comes from the independence structure, not from the fingerprint being blind.
- **T7 (merge cost).** The median time to merge two fingerprints when the second segment has 100,000
  events, divided by the median when it has 100 events, is < 3 for HF. For BASE, the matching
  "extend the chain with the second segment" ratio is > 100.
- **T8 (the honest cost).** HF's per-event build time is higher than BASE's. The advantage
  registered here is composition, not speed.

## Stated limits (before running)

- **Not a security primitive.** Cayley hashes built on SL(2) products have published collision
  attacks (the Tillich–Zémor and LPS hash families). HF is claimed only against non-adversarial
  errors. Adversarial resistance is left unrun below.
- **BASE gets the same equality answers.** On equality alone HF has no advantage; the registered
  difference is T4 and T7.
- One alphabet, one log length, one prime.

## Unrun, the questions E003 hands on

- **E003-U1.** A version that holds up against an adversary who chooses the log, for example by
  mixing HF with a keyed hash. Not attempted.
- **E003-U2.** Use HF in sovereign-veritas: the witness logs of two devices would merge from
  fingerprints alone, with independent gate decisions allowed to interleave. Not built. This would
  be a change to sv.package and needs its own registration there.
- **E7** (from E002) stays open.

## Prior art (as far as a short search shows; not a novelty claim)

Trace monoids and the projection lemma (Cartier–Foata; Cori–Perrin); Cayley and monoidal hashing
(Zémor; Tillich–Zémor); "hashing modulo theories". The combination here is an associative
fingerprint that is exactly invariant under reordering of independent actions and mergeable from
digests alone, aimed at governance evidence logs. It was not found in that search. That is a
statement about the search, not about the literature.
