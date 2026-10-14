---
type: is
id: is-01m4wb1qnqztrxaptnqe4pndxn
title: "PR592 C3: correct retained parser replay evidence"
kind: bug
status: open
priority: 2
version: 1
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wajcx0q76t3ppdzfbjxq4d
created_at: 2026-10-14T04:34:37.878Z
updated_at: 2026-10-14T04:34:37.878Z
---
Retained literal parser changed but evidence still marks replay passed without running that version. Rerun the safe retained checker against its pinned producer and retain output, or report replay not-attempted. Preserve exact whitelist parsing and record limits truthfully.
