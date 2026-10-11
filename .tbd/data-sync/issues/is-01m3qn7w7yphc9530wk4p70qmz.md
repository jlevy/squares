---
type: is
id: is-01m3qn7w7yphc9530wk4p70qmz
title: Investigate reachable normal-lane tail balancing
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T22:40:50.941Z
updated_at: 2026-09-29T23:00:19.908Z
---
After publication of the pool-heavy split, diagnose and measure normal-lane scheduling on an identical retained selection and source. Frozen primary a2b8e696c receipt run 6085bce8a0eb46a287d2cd1a1b52cccb completed 7750 passed, 9 skipped in 416.24s at 10 xdist workers and PACK_JOBS=1. Per-worker progress shows at most four busy during the final ~121s and at most two during the final ~62s; one indivisible 141.16s node also limits gains. Current wrapper passes -n 10 without a distribution override, and installed xdist maps -n to load. Investigate bounded work-stealing or long-first scheduling with the same exact nodes, markers, fixtures, and failure semantics. Record comparable phase walls and worker utilization before accepting any change or claiming speedup; do not tune the frozen candidate.

## Notes

Read-only scheduler diagnosis on frozen a2b8e696cc2dce562abedcecb9456229d57a9168, retained normal-child receipt run 6085bce8a0eb46a287d2cd1a1b52cccb: pytest-xdist 3.8.0 ran 7750 passed and 9 skipped in 416.24s with -n 10 and PACK_JOBS=1. Its pinned plugin maps -n to --dist=load. LoadScheduling sends consecutive collection chunks, refills at a low watermark, and when global pending becomes empty shuts idle workers down without reclaiming tests already assigned to another worker. First worker finishes were 22:36:02-11 UTC; eight of ten had finished by 22:37:01.57; gw5 finished 22:37:48.64 and gw2 last at 22:38:03.84. After 22:37:01, gw2 and gw5 still started 43 and 96 tests respectively. This is a substantial queued-item tail, although progress receipts do not contain scheduler queue state or prove a counterfactual wall.

The largest observed individual normal node, test_promote_exact_phase1, occupied gw5 for 141.16s from 22:34:25.13 to 22:36:46.29, ending about 77.5s before the normal phase. It is an indivisible lower bound while active but does not explain the final 77.5s by itself. Pinned WorkStealingScheduling can request half a busy worker queue for an idle worker while keeping at least two items on the source, and moves only not-yet-running tests. It is a smaller first comparison than historical-duration ordering, which would require a new collection-order mechanism and could change fixture locality. A load maxschedchunk cap still leaves local queues because repeated low-watermark refills can accumulate assigned items; it is not a direct test of reclaiming the observed tail.

Predeclared next-slice hypothesis: on one clean identical source tree and exact normal marker/target manifest, use only the installed --dist=worksteal option for the normal child, holding -n 10, PACK_JOBS=1, pool child, and all assertions fixed. Run a quiet A/B/A block (default load, worksteal, default load) with retained per-worker progress and JUnit. Advance the option only if B passes the identical node-ID multiset and outcomes (7750 passes, 9 skips on this source), has normal wall at least 10% below the faster A control, and reduces the final at-most-two-worker tail from roughly 62s to at most 30s. Any failure, collection difference, or smaller improvement rejects this first hypothesis. One block is screening evidence, not a speedup or merge claim; repeat and integrated CI remain required before changing the published scheduler. No benchmark or source edit was made during the frozen publication gate.
