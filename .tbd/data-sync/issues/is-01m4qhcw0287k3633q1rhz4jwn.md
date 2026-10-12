---
type: is
id: is-01m4qhcw0287k3633q1rhz4jwn
title: "Workbench trajectory cost check: compare the best of three timings with the 400 ms ceiling (flaked on #512)"
kind: bug
status: open
priority: 3
version: 1
labels:
  - testing
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-12T07:49:22.050Z
updated_at: 2026-10-12T07:49:22.050Z
---
packages/workbench/tools/workbench_tools/animate_view_contract.py (about lines 1036-1043, run by workbench_tools.check_frontend as the "workbench browser behavior in Chromium" step) times six trajectory builds (n = 11, 100, 324; styles physics and bodies) once each and requires each under 400 ms and 4 MB. On PR #512, run 38182457550 attempt 1 (frontend job 114597711232, head 604699ee1) failed with "a trajectory costs over 400 ms or 4 MB: [(324, 'physics', 454, 1807280)]"; attempt 3 at the same commit passed. Proposed fix (not implemented): time each build three times and compare the fastest with 400 ms; keep the 4 MB limit on one measurement and both ceilings unchanged. Done when the check uses the best of three, the ceilings are unchanged, and check_frontend passes.
