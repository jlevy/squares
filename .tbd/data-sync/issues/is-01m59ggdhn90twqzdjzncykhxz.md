---
type: is
id: is-01m59ggdhn90twqzdjzncykhxz
title: "Validate #680 n183: both source certificates, exact replay and sensitive controls"
kind: task
status: in_progress
priority: 2
version: 2
delegate: codex-680-replay-20261019
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m59few7wa6j6yrnw49hjap7r
hold: null
hold_until: null
created_at: 2026-10-19T07:20:09.521Z
updated_at: 2026-10-19T07:45:06.038Z
started_at: 2026-10-19T07:45:06.037Z
---
Stage 4 replay for #680, separate from Stage 1–3 source registration.

## Validation

- Claim: s(183) <= 13999580178736252502081470897571/10^30, at evand/square-packing 3a9948c781be668b1547cc2bf64a0d1e614f9bca, from both s183_h183b.cert and s183_h183b_regularized.cert retained in packing/resources/web/evand-n183-subgrid-2026-10-19/.
- Run: read the two retained standalone source checkers before execution; run each against each certificate with the project Python 3.14.7, then require duplicate-square and outside-wall mutants refused by each. Use the maintained devtools.upper_bound_reports/evand_arrangement_reports exact routes for the original certificate with their geometric controls; bind any additional regularized-view run explicitly. Retain commands, exact inputs, exit codes, wall/CPU and outputs. Register the deciding programs and their actual relationship to the generator. No dependency installation or numerical search is needed.
- Cost: engineering estimate 0.01–0.10 CPU-hours, not a measured checker timing. The certificates each hold 183 rational poses (16,653 possible pairs); both source programs import only sys and fractions and use an exact disc filter. Source solver JSON's 12 seconds is producer runtime, not a replay benchmark. Apply a 360-second ceiling to the first complete batch and reprice if exceeded.
- Budget status: runnable as a separate W2 slice after source-execution review; the estimate is minutes, below the standing 40 CPU-hour item cap. No replay was run by W1 custody.
- Possible subset under the cap: the full two-certificate batch fits this estimate; no sample is a confirmation.
- Depends on: retained source custody under think-xp0o; an independently prompted mathematical review; result IDs bound only after registration merges. Geometry can be checked without reconstructing the unlogged crossover mate.
- Done when: complete positive and two sensitive invalid controls per accepting route are retained and rechecked, verifier metadata and accepted mathematical review bind the exact claim, and Stage 4 integrates any earned rungs in a reviewed change. Adoption and strong-generator regularization require a separate owned disposition.
- Machine note: one or two CPU workers, existing primary Python environment, no Rust build or new environment. Use external task scratch and pause on I/O failure; no cache fallback on internal disk.
