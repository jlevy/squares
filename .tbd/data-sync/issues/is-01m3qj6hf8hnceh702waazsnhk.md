---
type: is
id: is-01m3qj6hf8hnceh702waazsnhk
title: Give pool-heavy reachable tests an exclusive inner-worker phase
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3qn7w7yphc9530wk4p70qmz
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:47:41.413Z
updated_at: 2026-10-06T08:34:47.253Z
closed_at: 2026-10-06T08:34:47.252Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): devtools/reachable_tests.py on origin/main splits 'not pool_heavy' (bounded xdist, PACK_JOBS=1) from 'pool_heavy' (serial, PACK_JOBS=N); integrated at a2b8e696c, merged in PR #246 after hosted checks. No speedup was claimed
resolution: null
duplicate_of: null
---
Exclusive pytest workers with PACK_JOBS=1 still serialize the whole-corpus atlas test, which already uses a deterministic per-case process pool. Retained timings show a 1327.87-second single-node atlas call; current quiet run does not prove its live identity. Preserve all nodes and assertions: identify pool-heavy tests explicitly, run the remainder with bounded xdist and PACK_JOBS=1, then pool-heavy tests without xdist and with the reserved host allocation. Keep explicit resource overrides authoritative. Prove collection union/disjointness and failures/empty-lane behavior; measure the integrated candidate before claiming improvement.

## Notes

Full-gate candidate 91bb57cb2 exposed two integration defects after 7703 passes: the pool marker changed frozen packing/pyproject.toml and inherited reachable receipt variables entered runner unit-test code paths. Repairs 38e82612e and 156d65e80 are exact ports of independently reviewed fc97298d8 and 783e99e91. The restored pyproject blob 29a17dad3 matches proof commit c183cc9a; independent native receipt checks passed 28/28, strict marker collection selected exactly 1/40 atlas nodes, and reachable runner/progress tests passed 51/51 under hostile outer receipt variables. Workflow Step partition and mathematical acceptance code are unchanged. Keep in progress until integrated full push and published CI pass.

Frozen primary push a2b8e696cc2dce562abedcecb9456229d57a9168, receipt run 6085bce8a0eb46a287d2cd1a1b52cccb, has completed the normal reachable child: 7750 passed, 9 skipped in 416.24s pytest wall with 10 xdist workers and PACK_JOBS=1. Per-worker progress on 2026-09-29 UTC shows starts at 22:31:10, first workers ending 22:36:02-11, four still active after 22:36:11, only gw2/gw5 after 22:37:01, and last gw2 ending 22:38:03. The final roughly 62s therefore used at most two of ten workers; the final roughly 121s used at most four. gw5's longest indivisible node was test_promote_exact_phase1 at 141.16s; gw2 had test_receipt_scalar_substitutions_refuse[path9-True] at 53.29s and a sequence of 2-13s calibration cases. This is measured tail imbalance, not yet proof that another scheduler is faster. The reachable wrapper passes -n 10 without a --dist override; its installed pytest-xdist describes -n as --dist=load. Pool child began 22:38:07 with one canonical atlas node, PACK_JOBS=10 and xdist_workers=1; full pool and gate walls remain pending.

Completed pool split on the same frozen a2b8e696c push: normal child 7750 passed and 9 skipped in 416.24s at -n 10/PACK_JOBS=1; pool child ran exactly the canonical whole-atlas composite node, 1 passed with 7819 deselected in 140.99s at serial pytest/PACK_JOBS=10 (132.83s call). Both progress receipts have session_finish and source/run identity; parent reachable Step took 559.41s and the full named push passed 51/82 steps in 623.04s. The older 1327.87s atlas reading and the earlier 968.77s broad pytest were on different sources/selections, so the measured reduction is not a controlled speedup claim. Post-publication CI and a same-selection comparison remain the limits; do not close before CI.
