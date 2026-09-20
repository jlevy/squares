---
type: is
id: is-01m2y6d8gz95gssfd0m4asq5d4
title: Keep allowlist existence check within the fast-test budget
kind: bug
status: closed
priority: 2
version: 2
labels:
  - defect-class:performance
  - session-142
dependencies: []
parent_id: is-01m2y0xxta8s7t422xk5vyx0jc
created_at: 2026-09-20T01:20:37.918Z
updated_at: 2026-09-20T01:51:15.484Z
closed_at: 2026-09-20T01:51:15.484Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
Session 142 correction follow-up. Already fixed at 4c202aeb in packing/tests/test_check_declared_bounds.py: the allowlist-existence test now reads declared bound keys directly instead of generating the full reference-matching report it never consumes. The measured test wall fell from 12.38 s to 0.44 s while the separate positive and negative controls retain full reference matching coverage. Keep open until the correction branch's final CI passes, then close.
