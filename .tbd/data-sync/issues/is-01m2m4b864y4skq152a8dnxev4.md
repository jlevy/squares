---
type: is
id: is-01m2m4b864y4skq152a8dnxev4
title: "PR #175 review R2: the allowlist ratchets counts but not membership"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:10.562Z
updated_at: 2026-09-16T03:32:10.562Z
---
check_no_embedded_js.py:206 (BEAD.match) and :547 (ratchet). A bead: entry naming a nonexistent bead loads. Fix: resolve every bead through LIVE_BEAD_STATES as test_every_relaxed_flag_names_an_open_tracker does; plus a base comparison on --since. (PR #175, review 5218208204)
