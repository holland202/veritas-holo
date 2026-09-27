![veritas-holo](figures/banner.png)

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
| [E002](experiments/E002_holonomy_area/) | what does holonomy carry, and does it beat a cheap exact computation? | **6 of 6 held** on x86_64 and on the S25: it carries signed area for any noncommuting operators (P8's sham included); the shoelace formula gets it exactly for far less. **No advantage.** |
| [E003](experiments/E003_trace_fingerprint/) | can a holonomy fingerprint concurrent histories, forgiving legal reorderings and merging from fingerprints alone? | **8 of 8 held** on x86_64 and on the S25: exact on 3000 of 3000 pairs; merge time flat from 100 to 100,000 events. The advantage is composition, not information or speed. |
| [E004](experiments/E004_group_state/) | which kinds of recurrent state can track S5, the group behind the state-space-model limits? | **4 of 6 held, 2 FAILED (kept)**: relation-respecting operators exact at L=40, 160; commuting ones capped by letter counts; relation-free ones at chance. G1 failed on a readout flaw; G5's sham kept a fading signal. |
| [E005](experiments/E005_learned_state/) | can training discover a group's state from short examples, with no relations given? | **6 of 6 held**: learned from words of length ≤ 8, exact at length 160 (20× the training horizon) on 3 of 5 seeds; 2 failed; the relations appear in the learned operators; commuting training stays at the count ceiling. |
| [E006](experiments/E006_restart_diagnostic/) | can the trained operators show, before any test, whether training worked? | **4 of 4 held**: all 17 accepted runs worked and all 17 low-score runs failed; picking by the score gave a working model in 9 of 10 groups against 2 of 10 blind. The score knows S5's relations. |
| [E007](experiments/E007_heldout_composition/) | do learned operators handle transitions never seen in training, where a transition memoriser cannot? | **3 of 3 held**: all 12 runs that learned the seen words scored 1.0 on words full of unseen transitions; the memorising null (13 runs that learned the seen words) stayed at chance on them |
| E7 | a task whose holonomy information no equal-cost classical recurrence computes | not found yet |
| language models | only after a task with an advantage exists | not started |

**v0.1 is a pure mathematical reference implementation.** No language model, no GPU, no NPU. Every
property E001 checks is a known property of unitary matrices; passing it shows the instrument
works, not that geometry helps reasoning.

## The architectural law

No semantic assertion becomes a fact directly:

    observation → proposal → formalisation → execution → invariant test → evidence

A language model, when one is added, may only *propose* transitions. The engine applies them, the
invariants check them, and the result is recorded. The model proposes; the mathematics disposes.

## What works so far

<p>
<img src="figures/E004_state_tracking.png" width="49%" alt="E004 accuracy by arm">
<img src="figures/E005_learned_extrapolation.png" width="49%" alt="E005 accuracy at length 160 by seed">
</p>
<p>
<img src="figures/E002_area_readout.png" width="49%" alt="E002 R-squared by arm">
<img src="figures/E006_restart_diagnostic.png" width="49%" alt="E006 relator score against success">
</p>
<p><img src="figures/E006_restart_policy.png" width="49%" alt="E006 restart policy against blind choice">
<img src="figures/E007_heldout_composition.png" width="49%" alt="E007 accuracy with and without held-out transitions"></p>

Every figure is drawn by `scripts/make_figures.py` from the committed result files, not from typed
numbers. 

- A fingerprint for concurrent logs that ignores harmless reordering and merges from fingerprints
  alone (E003).
- Relation-respecting operators track the S5 state exactly at every tested length (up to 160), while
  a commuting diagonal recurrence is limited to letter-count information (E004). The diagonal arm is
  a mathematical control, not an implementation of any particular state-space model.
- A registered rule-count check, read from the trained operators before any test, predicted which S5
  training runs would extrapolate to length 160 (17 of 17 each way; score 4 ambiguous). The check
  uses the known S5 relations. Restarting on it gave a working model in 9 of 10 groups (E006).
- Operators trained without two transitions handle them exactly once training succeeds (12 of 12),
  while a model that memorises transitions stays at chance on them (E007).
- Training on labelled words of length ≤ 8 can find S5-tracking operators: on 3 of 5 registered seeds
  they were exact at length 160, 20× the longest training word. The readout was fitted on labelled
  long words; the operators never saw one. On 2 of 5 seeds training failed (E005).

Each line links to registered predictions, controls and a replayable run. What did not work is
kept too, in [`claims/`](claims/).

## Method

New and conceptual ideas are welcome here, including ones outside the usual toolkit. An idea stays
only if it is registered, run, and verified; otherwise it is recorded as refuted.


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
