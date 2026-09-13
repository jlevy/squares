---
type: is
id: is-01m2b884n0ms50xp93q6aaps1g
title: Revise and admit the BC329 three-profile run sheet
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol high documentation and operational review
labels:
  - n11
  - calibration
  - plan
dependencies:
  - type: blocks
    target: is-01m2appdgg1p32xwgxptcqqb2x
parent_id: is-01m2appdgg1p32xwgxptcqqb2x
created_at: 2026-09-12T16:47:13.055Z
updated_at: 2026-09-13T08:20:29.692Z
---
Apply the independent run-sheet review after the implementation gates land. Freeze and review the exact 4/5400/7200/2 tuple; invoke the maintained run-set coordinator and source-distinct reader; enforce uv>=0.12; retain argument-free host process labels; clarify which profile directories/logs are immutable and where later sidecars live; remove stale head hashes while keeping exact PR-head equality; name the durable retention destination; and include every refusal condition. Re-run shell/Python parsing and source-distinct operational review on the exact integrated PR156 head. The sheet remains target-free and may not execute profiles or BC329 during this bead.

## Notes

A durable target-free run-sheet draft is now tracked in the PR156 worktree and document map. It freezes 4/5400/7200/2, verifies uv>=0.12, exact clean local/remote identity and fixture bytes, uses the maintained coordinator, gives three literal source-distinct reader commands with retained stdout/stderr/status, keeps RUN_ROOT immutable, and names a Git retention directory with exact copy/archive/digest commands. The reader-revision placeholder remains deliberately ineligible until think-n4gh is committed and independently accepted. Exact shell parsing, practical-prose review, integrated-head operational review, push, and CI remain. No profile or BC329 ran.
