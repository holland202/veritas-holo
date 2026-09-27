# veritas-holo

**A falsifiable geometric reasoning substrate: finite-state manifolds, operator dynamics and
invariant constraints, built to be measured before it is believed.**

> Research question: can a compact, explicitly structured geometric state-transition system give
> measurable reasoning advantages over an equivalent unconstrained computation, at the same compute
> budget, against a sham with the structure destroyed?

Nothing in this repository answers that yet. What exists is the first instrument.

## Status

| experiment | what it asks | status |
|---|---|---|
| [E001](experiments/E001_operator_algebra/) | does the reference implementation obey the algebra (closure, inverse, commutators, holonomy, invariants, replay)? | **10 of 10 held** on x86_64 and on the S25; byte replay across platforms refuted (P9), replay to 10 decimals replicated (P10) |
| [E002](experiments/E002_holonomy_area/) | what does holonomy carry, and does it beat a cheap exact computation? | **6 of 6 held**: it carries signed area for any noncommuting operators (P8's sham included); the shoelace formula gets it exactly for far less. **No advantage.** |
| E003 | a task whose holonomy information no equal-cost classical recurrence computes (E7) | not found yet |
| language models | only after a task with an advantage exists | not started |

**v0.1 is a pure mathematical reference implementation.** No language model, no GPU, no NPU. Every
property E001 checks is a known property of unitary matrices; passing it shows the instrument
works, not that geometry helps reasoning.

## The architectural law

No semantic assertion becomes a fact directly:

    observation → proposal → formalisation → execution → invariant test → evidence

A language model, when one is added, may only *propose* transitions. The engine applies them, the
invariants check them, and the result is recorded. The model proposes; the mathematics disposes.

## Method

Every claim has a registered prediction written before the code that tests it, a null control that
must come out the other way (so a checker that always passes is caught), and a status:

`PROPOSED → IMPLEMENTED → TESTED → REPLICATED`, or `REFUTED` (kept, never deleted), or `UNKNOWN`.

Claims live in [`claims/`](claims/). Results are sorted into `results/exploratory`, `registered`,
`verified` and `refuted`. Numbers in prose are pasted from program output.

## What this is not

- Not a reproduction or a clone of any other system, and not compatible with anything it has not
  been tested against.
- Not "physics-based AI". Group names such as SU(n) describe the matrices used, nothing more. Any
  physics correspondence would need its own registered claims, and none exist.
- Not a smooth manifold where the states are discrete. When a discrete analogue is used, the code
  says so.

## Run it

    pip install numpy pytest
    python experiments/E001_operator_algebra/run.py
    python -m pytest -q

Pure Python and NumPy; runs on a phone in Termux.

## Related

The evidence and gating ideas come from
[sovereign-veritas](https://github.com/holland202/sovereign-veritas), a fail-closed permission gate
whose packages anyone can re-check. Coupling the two is a later step, not a present feature.

*Vincit Omnia Veritas.*
