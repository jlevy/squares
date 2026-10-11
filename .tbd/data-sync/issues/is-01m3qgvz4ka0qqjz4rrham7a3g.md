---
type: is
id: is-01m3qgvz4ka0qqjz4rrham7a3g
title: Fan out post-merge deferred validation jobs
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:24:26.375Z
updated_at: 2026-10-06T08:34:37.850Z
closed_at: 2026-10-06T08:34:37.850Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Post-merge fanout on origin/main: packing-validation.yml push path runs the deferred bins and exhaustive shards and post-merge-required binds them; main push runs pass (e.g. c4f008327). Its hosted wall measurement is pending under think-0atx in gate-budgets.yaml
resolution: null
duplicate_of: null
---
Reuse the reviewed deep-gate whole-Step bins in .github/workflows/packing-validation.yml so push/daily validation does not retain the predecessor serial deferred critical path. Preserve an exact disjoint union with the complete integration job, immutable push SHA binding, unique receipts, and existing aggregate semantics. Measure hosted critical-path wall and runner-minutes before replacing the current topology budgets.

## Notes

Isolated validation-parity branch codex/validation-parity at da69cf3ef ports reviewed deferred whole-Step bins and three exhaustive whole-file shards to main/daily/dispatch CI. Complete validate skips all 11 delegated Steps; separate post-merge-required aggregate binds every non-PR worker while packing-required remains the seven PR jobs. New/updated contract tests prove logical exact Step partition, shard flags, immutable github.sha checkout and HEAD receipt ordering, and unique uploads. Five focused tests passed (159 deselected), Ruff/format and BasedPyright clean; independent review clean. Hosted wall and runner-minute measurement, full gate, and integration/push remain pending; no speedup claimed.
