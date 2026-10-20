---
type: is
id: is-01m4qbx9sdrvphr9crfaxmrc4a
title: "PR #512 C4: n40 integrity-ceremony entry contradicts itself; crate_input docstring stale"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4qbwvsj8cz41qmdkx6gxykx
hold: null
hold_until: null
created_at: 2026-10-12T06:13:29.004Z
updated_at: 2026-10-12T06:28:19.583Z
started_at: 2026-10-12T06:13:38.075Z
closed_at: 2026-10-12T06:28:19.582Z
close_reason: "fixed in ef244c575: ceremony entry and crate_input docstring"
resolution: null
duplicate_of: null
---
Low. packing/devtools/integrity-ceremony.yaml:320-327 says no run is refused on a digest; the crate decision now is. Record the cost; fix crate_input docstring's '480 rows' (audit_continuous_pose.py:432-434). PR #512, https://github.com/jlevy/squares/pull/512#pullrequestreview-5487045374
