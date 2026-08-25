---
type: is
id: is-01m0vjxas2pfd1qn71sqhrgscf
title: Reconcile packing bead state with landed main after stacked PRs
kind: bug
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - bookkeeping
  - focus-process
dependencies:
  - type: blocks
    target: is-01m0vr7g27g67p699aepcdksxd
parent_id: is-01m0r7tk07nw6nb8wyzv4v776z
created_at: 2026-08-25T04:30:00.482Z
updated_at: 2026-08-25T06:02:56.442Z
---
The live tbd graph is not a reliable landed-main resumption queue after PR 22. A merged checkpoint bead (think-l1us) remained in progress and blocked think-nm35; stopped session-009 still has think-05hr in progress; and think-cns0 is closed for a D-129 fix that exists on open PR 23 but not main, where D-129 remains outstanding. Reconcile active session claims, preserve branch-ahead completion with explicit PR/commit provenance, define how onboarding distinguishes completed-on-branch from landed-on-main, and add the resulting bookkeeping defect to defects.yaml/rendered logbook with a regression or reconciliation check.
