---
type: is
id: is-01m45jb72n7v806gq5a9gza6fk
title: "Session 182 lane A: H-264 per-state price on the seed-182 draw (BC-419)"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-05-n17-overnight.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-05T08:19:36.661Z
updated_at: 2026-10-06T08:03:58.933Z
started_at: 2026-10-05T08:20:02.127Z
closed_at: 2026-10-06T08:03:58.932Z
close_reason: "H-264 accepted (exp-252, W2 confirmed with corrections) and BC-428/H-275 accepted (exp-257); exp-257's W2 corrections applied in 782655c6c on #379. exp-257 stopped on its clock and resumes at u31, tracked separately."
resolution: null
duplicate_of: null
---
W6 round under H-264 as rewritten in the session-182 registration (BC-419). Float pre-screen (survey_n17_residue --flag-set arity8 --sample 12 --seed 182), kernel control on the endpoint's own state (must not close), then the 12 draws in index order two at a time at 32 bins and 7,000 s; closures re-proved by the standing kernel verifier in full from the clean run worktree. Continues think-e17c. Write set: $SCRATCH/s182/A/ and the run worktree's ignored certificates folders s182-m* only; admissions and exp-252 are the coordinator's.

## Notes

2026-10-05 09:15 UTC. Registration cebb5d15a pushed, draft PR #365. Queue: $SCRATCH/s182/logs/queue-A.sh, receipts $SCRATCH/s182/A/. Survey (seed 182) running since 08:46; its positive control placed. Draws run in the survey's own seeded random order (run-order.txt, indices 2 4 1 5 8 10 3 12 11 6 7 9): the receipt's index field is the stratified draw position, not the random order. Closures go to certificates/s182-m<MASK>/.
