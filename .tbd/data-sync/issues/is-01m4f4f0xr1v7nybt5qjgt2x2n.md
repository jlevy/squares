---
type: is
id: is-01m4f4f0xr1v7nybt5qjgt2x2n
title: PR448 diagnostic transport control must pass zero-warning typecheck
kind: bug
status: closed
priority: 1
version: 3
assignee: intake_remaining_fixes
delegate: claude-code@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m4ey826ykymayr66y0fz3f55
hold: null
hold_until: null
created_at: 2026-10-09T01:29:25.685Z
updated_at: 2026-10-23T06:12:17.985Z
started_at: 2026-10-09T01:30:25.653Z
closed_at: 2026-10-23T06:12:17.985Z
close_reason: "Tracker audit 2026-10-23 (c-audit-a-1023, think-s4ld), checked by coord-intake-1023: DONE; STALE-CLAIM. fix c4749f877 is an ancestor of origin/main; tests/test_negative_controls.py no longer references _profile_child"
resolution: null
duplicate_of: null
---
Actual hosted full run37867363555 job113617180041 fails tests/test_negative_controls.py:335:43 reportPrivateUsage: controls._profile_child is accessed outside its module (0errors/1warning, gate requires0/0/0). Source fix c4749f877527ff8a07a314af892aad252c970a0d replaces private-source introspection and synthetic stats with real tiny-child execution through the public main/runner interface, preserving all success/failure/timeout outcome assertions and custody. Independent Sol accepted treef450fff0f428ea271931e36f7ee7d95a382105f0;19profiling controls PASS10.50s, RuffPASS, actual fullfile BasedPyright0errors0warnings0notes. Normalhooks completed71.92s after external inventory-I/O delay; no bypass. Current upper normalmerge cascade and hosted exacthead qualification remain pending; no native12s credit. Source/evidence receipt Gitblob54b795457628113f8bf6ed85aba6416768bd6b1e; Notes/pr448-profile-public-transport-f450-independent-sol-peer.json.
