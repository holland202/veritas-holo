# E009 on the phone: float16 replication (registered 2026-09-27, before any phone run)

**Command (Termux, S25 Ultra, in `~/veritas-holo` after `git pull`):**

    python experiments/E009_blind_check_lowprecision/run.py --seeds 501-510 --partial $HOME/e009_phone.jsonl

It can be resumed: rerun the same command and finished seeds are skipped. Paste the full output.

Container reference (`results/verified/E009_x86_64.json`, seeds 501-510): training succeeded
(float64 accuracy ≥ 0.99 at L = 160) on seeds 502, 503, 506, 508, 510. All five scored 1.0 in float16 at
L = 10000.

**Predictions**

- **R1 (B4 on real hardware)** Every seed that succeeds on the phone scores ≥ 0.99 in float16 at
  L = 10000.
- **R2 (cross-platform determinism)** The phone's successful seeds are exactly {502, 503, 506, 508,
  510}. This could fail even if R1 holds: aarch64 and x86_64 BLAS round differently, and 3000 training
  steps can amplify that into a different outcome. If R2 fails, the note records which seeds changed.

**What this does not test.** float16 *arithmetic*. The float16 path stores the state in float16 after
each step and computes in float64, as in the container. Native half-precision matmul on the Adreno
GPU is a separate, unrun question.
