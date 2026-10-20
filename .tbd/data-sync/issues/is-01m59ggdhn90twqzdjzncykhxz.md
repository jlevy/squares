---
type: is
id: is-01m59ggdhn90twqzdjzncykhxz
title: "Validate #680 n183: both source certificates, exact replay and sensitive controls"
kind: task
status: in_progress
priority: 2
version: 4
delegate: lane-680
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m59few7wa6j6yrnw49hjap7r
hold: null
hold_until: null
created_at: 2026-10-19T07:20:09.521Z
updated_at: 2026-10-19T20:39:59.159Z
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

## Notes

The coordinator authorized one bounded primary-certificate replay after the W1 custody checkpoint, using only the maintained devtools.upper_bound_reports evand-cert route. This completed and is committed at e72a3b6f0b7174ccc2312649d2d3e7af54c648b3, after f57ede12ce64cd1c74336d380b607478361c34c3, in .worktrees/confirm-422 on codex/intake-followup-20261019. Normal hooks passed in 3.14 seconds. The tree is clean; no push or PR.

Exact source pin 3a9948c781be668b1547cc2bf64a0d1e614f9bca. Primary-only acquisition/report.json at packing/resources/web/evand-n183-subgrid-2026-10-19/ declares expected n=183, exact side 13999580178736252502081470897571/1000000000000000000000000000000, and only search/packer/candidates/s183_h183b.cert. No same_packing field or regularized-view assertion. Custody passed; the maintained parser rejects missing/extra rows and mismatched count; exact side admission is equality to the fraction.

Command from packing with the existing Python 3.14.7 and W1 external environment: python -m devtools.upper_bound_reports evand-n183-subgrid-2026-10-19 certify --jobs-dir /Volumes/spud-ext1/agent-scratch/squares-intake-followup-20261019/n183-primary-jobs-01 --workers 1 --timeout 100. Exit 0; process real 34.87 seconds, user 32.38, system 0.48. This was the single batch, within its 360-second ceiling; each of three children had 100 seconds. No timeout or retry. Both repository routes accepted the positive and rejected duplicate-square and outside-container controls, all 16,653 pairs per route/job, 99,918 pair decisions. Native receipt: packet receipts/exact-certification.json.xz. Summed route CPU 30.55 seconds, summed job wall 31.27 seconds, longest job 10.79 seconds. Both positives have wall clearance 1/200000000000000000000 and exact positive pair gap about 1e-20.

Maintained command python -m devtools.upper_bound_reports evand-n183-subgrid-2026-10-19 check --n 183 exited 0: one certificate and three jobs admitted, without geometry reexecution. acquire_source --check passed, documentation check covered 2,073 documents with links and footers resolving, retained JSON layout had zero failures, git diff --check passed. Full records gate was not repeated: the preceding checkpoint records run still has the disclosed unpublished site/paper release disposition pending; its stale VERIFIERS failure was repaired and focused inventory passed.

Batch declaration, exact commands, timings, route outcomes, limitations and deciding-program relationship are retained in packing/campaign/issue-intake/intake-followup-20261019/n183-primary-replay.json. Unique native job inputs, controls, outputs, stdout/stderr and process log are preserved outside disposable scratch at /Volumes/spud-ext1/agent-source/squares-intake-followup-20261019/n183-primary-replay-01/. The independent reviewer has the exact paths and admission command for a read-only replay addendum under think-glg8.

Keep this bead open. This is unintegrated validation evidence only: no source checker executed; the regularized view, source-execution obligations, independent review/deciding-program mapping to the actual result, assurance decision, adoption and strong-generator regularization remain. No T number, rating, case bound, house, public issue reply or release changed. No source generator reran; no same-packing identity or no-expansion path was established. Result-ID/release order remains held for the coordinator after #671 integration.
