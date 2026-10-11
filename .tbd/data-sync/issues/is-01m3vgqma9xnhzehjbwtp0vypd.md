---
type: is
id: is-01m3vgqma9xnhzehjbwtp0vypd
title: Reject unsupported coordinate semantics in independent rational checker
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-01-post-optimality-w3-session.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3vgmc6hkrq861aymmpgdm9q
hold: null
hold_until: null
created_at: 2026-10-01T10:39:01.957Z
updated_at: 2026-10-01T10:54:29.162Z
started_at: 2026-10-01T10:40:53.983Z
closed_at: 2026-10-01T10:54:29.159Z
close_reason: Session165 retained W3/W10 decision and accepted exp235/H253 after exact controlled replay and independent Astra max output review. D510 metadata contract fixed; 230 retained rational-corner witnesses unaffected. Frontier admission separately think-vdmf; next math think-j516.
resolution: null
duplicate_of: null
---
W2 Session165: independent parse ignores coordinates.origin and square_size. A container-center unit witness with side2 and local corners(1,0),(2,0),(2,1),(1,1) can pass [0,2] geometry while main shifts it and rejects. Require supported rational-corner lower-left/right-up/unit semantics, meaningful differential regressions, retain existing controls. Source half-angle adapter emits canonical semantics; no n17 target was run before discovery.
