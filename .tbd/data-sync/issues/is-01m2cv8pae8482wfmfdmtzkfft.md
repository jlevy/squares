---
type: is
id: is-01m2cv8pae8482wfmfdmtzkfft
title: "PR #157 review DOC-02: reader-refusal and completion claims are too broad"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:48.526Z
updated_at: 2026-09-13T07:38:48.526Z
---
session-127 lines 241-251, SYNOPSIS.md:744-757 and the PR body conflate unsupported admission readers with the interval route's size guard. The interval implementation supports weighted counts below the cap; it does not categorically refuse weighted input. The implementation findings also contradict the blanket claim that all consumers were audited successfully. Fix: distinguish admission refusal from allocation limits; reconcile completion claims with the repaired code and regression evidence; preserve dated history with an explicit correction.
