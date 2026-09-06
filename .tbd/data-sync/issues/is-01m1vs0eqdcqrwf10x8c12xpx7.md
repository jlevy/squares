---
type: is
id: is-01m1vs0eqdcqrwf10x8c12xpx7
title: "W5: reduce repeated slow-test work and audit negative-control cost"
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T16:32:16.108Z
updated_at: 2026-09-06T17:12:04.980Z
---

## Notes

Both preregistered component comparisons completed all3interleavedpairs with unchanged selected tests and passing outputs. Generated report: float control median275.50s range261.05-282.51 versus candidate17.45 range17.20-17.98; bridge module84.30 range81.13-86.28 versus31.72 range30.99-36.51. Adopted after affected-source and correctness/complexity review. Candidate whole-tree diff hashes varied with permitted unrelated edits, so raw receipts plus retained source reconstruction support a component-only exploratory conclusion. Full checkpoint started with --jobs2 --inner-jobs2 and artifacts /tmp/squares-validation-efficiency-full.
