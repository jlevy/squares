---
type: is
id: is-01m2nf9a0cvj36jvzep9mx7wta
title: Make post-merge tree reuse classification fail closed
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-16T16:02:35.659Z
updated_at: 2026-09-17T20:39:20.308Z
---
PR #185 review: Step.reads_beyond_tree defaults False, so a newly added clock/network/git-dependent fast step is silently classified reusable and omitted after merge. Replace it with an explicit safe-default tree_reusable classification, and add a contract that every fast step is deliberately classified before exact-tree reuse may omit it.

## Notes

2026-09-16 evidence audit at da2259fb: SATISFIED. Positive allowlist TREE_REUSABLE_FAST_STEPS (validate.py:4443-4512); _after_verified_pull_request repeats everything else and fails on stale names (4627-4637); wired at packing-validation.yml:318-331; test_a_verified_merge_repeats_everything_not_positively_tree_reusable (test_validation_cli.py:2622). Close after green exact-head hosted CI. Follow-up on one allowlisted step that reads git/tbd: think-9oxz.
