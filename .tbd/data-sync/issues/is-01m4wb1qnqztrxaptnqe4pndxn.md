---
type: is
id: is-01m4wb1qnqztrxaptnqe4pndxn
title: "PR592 C3: correct retained parser replay evidence"
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
hold: null
hold_until: null
created_at: 2026-10-14T04:34:37.878Z
updated_at: 2026-10-14T08:44:52.611Z
started_at: 2026-10-14T04:36:48.935Z
closed_at: 2026-10-14T08:44:52.611Z
close_reason: Fixed, independently confirmed in PR592 reviews D/E/F/G, green fast+Pages+full checkpoint38530454327 at final7a184720, and merged as f73e9de13d8ccc40b91d844b164f9c2ad9c032c1. Full mathematical proof replays remain tracked separately; no new verified n17 bound claimed.
resolution: null
duplicate_of: null
---
Retained literal parser changed but evidence still marks replay passed without running that version. Rerun the safe retained checker against its pinned producer and retain output, or report replay not-attempted. Preserve exact whitelist parsing and record limits truthfully.
