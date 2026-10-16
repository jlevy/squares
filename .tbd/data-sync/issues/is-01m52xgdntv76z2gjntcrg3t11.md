---
type: is
id: is-01m52xgdntv76z2gjntcrg3t11
title: "PR #644 D2: run the deferred checkpoint at the re-cut head (label on; blocked by the conflict with main)"
kind: task
status: closed
priority: 1
version: 3
delegate: user-eb-addr-644
labels:
  - regularization
dependencies: []
parent_id: is-01m51k8s0y2dbwnmvtwjv30zrx
hold: null
hold_until: null
created_at: 2026-10-16T17:52:40.122Z
updated_at: 2026-10-16T22:36:04.973Z
started_at: 2026-10-16T17:52:46.944Z
closed_at: 2026-10-16T22:36:04.972Z
close_reason: "The deferred checkpoint passed at #644's merged head 5419ccaa9 (run 38974269991: regularized-views, exhaustive-1..3, every deferred group green), recorded in #644's Validation; #644 merged at b35a6289f."
resolution: null
duplicate_of: null
---
Review D2 (High) of jlevy/squares#644: the deferred checkpoint (deep-gate.yml, "Deferred checkpoint") has never run on the branch. Review: https://github.com/jlevy/squares/pull/644#pullrequestreview-5550660772

State at the addressing pass (user-eb-addr-644, 16 October 2026, head ebe506910): the `deep-gate` label was added at 17:50:58Z, but no run started, because #651 merged into main at 17:49:19Z (26d8bb335) with site v0.7.15 and the PR has conflicted with main since (release.py and the five claim documents; mergeable_state dirty), and GitHub runs no pull_request workflow on a conflicted PR. A workflow dispatch of deep-gate.yml at the PR branch was refused: HTTP 403 "Resource not accessible by integration". The local substitute, `regularize_axis_components --verify-atlas --workers 2` over the whole layer, is recorded in the PR's Validation.

Done when: the coordinator's re-cut over main (which resolves the conflict) is pushed with the label on, the `synchronize` run of "Deferred checkpoint" finishes, and regularized-views, exhaustive-1 to exhaustive-3 and deep-gate-required are inspected and recorded under the PR's Validation. Waits on: the coordinator's re-cut of #644 in merge order.
