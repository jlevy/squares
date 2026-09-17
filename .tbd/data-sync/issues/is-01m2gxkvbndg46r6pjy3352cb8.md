---
type: is
id: is-01m2gxkvbndg46r6pjy3352cb8
title: "The strategy evaluation loop: documents x n x disjoint seed blocks, with controls"
kind: feature
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gxkxbhyqesd394p4ezr66c
  - type: blocks
    target: is-01m2p0xq9nac6ftmr19978krh3
  - type: blocks
    target: is-01m2pkfjhe627n9qa4761eb6zm
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:36:49.012Z
updated_at: 2026-09-17T02:35:09.732Z
---
Benchmark cells keyed by (n, rung, use), where use is start, welds, forces, shake or phases, measured on the package instrument with retained final poses, repaired-then-validated scoring and disjoint seed blocks at equal work.

- Every structural rung runs beside a **rewired** hint (same size, edges on pairs that do not touch) and a **thinned** one (a random subset), which is the pattern `sweep_structure_hints.py` already uses. Without them a gain says constraints help, not that the structure did.
- **Test set**: n = 29 and 37, the only records below 40 with near-flush corner contacts, where merge-then-release should matter; n = 11 and 17 (tilted classes, no near-flush contacts); n = 5, 10, 26 (45-degree families); one partial grid as a control.
- **Outcome**: valid success rate within tolerance, and the smallest rung at which each n succeeds; **information axis**: remaining degrees of freedom; **cost**: steps and CPU, not wall clock.
- Held-out n for any parameter chosen from the results.

Blocked on the extraction, the kernel mechanics, and the shared validity contract (think-nals).

## Notes

2026-09-14, owner reframed this bead: the comparison is between STRATEGIES, each a PackingStrategy document with its guidance declared. The loop is a set of strategy documents by a set of n by a disjoint seed-block plan at equal work. Each document runs on an implementation that supports every phase, and each run passes the shared validity contract before it is scored. Trial rows carry the document content hash, derived guidance summary, catalogue ref and provenance. The report gives, per n, the valid success rate at tolerance, best-of-k over disjoint blocks, and cost; across n, which strategy and guidance succeeds where. Rewired and thinned controls are strategy documents in their own right, and any parameter chosen from results is checked on held-out n. The Search mode is this loop interface (think-czav).

2026-09-16 guidance addition from duplicate think-t0g7: the headless runner and CLI must accept the same GuidanceTarget/v1 and application config as the browser, emit raw trajectories and target-recovery metrics, and produce deterministic replay provenance for every round.
