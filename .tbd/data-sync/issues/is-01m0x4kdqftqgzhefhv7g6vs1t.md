---
type: is
id: is-01m0x4kdqftqgzhefhv7g6vs1t
title: "PR37-F4: add a focused regression for all-occurrence aggregate checking"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0x4c75pqtywfdr4cfnzzvhp
created_at: 2026-08-25T18:58:24.622Z
updated_at: 2026-08-25T19:11:21.323Z
closed_at: 2026-08-25T19:11:21.322Z
close_reason: "Fixed in b450072: extracted the all-occurrence behavior and added a focused one-current-plus-one-stale regression independent of document totals and line numbers."
resolution: null
duplicate_of: null
---
The check_synopsis change validates every matching unprotected-fix statement, but the existing mutation only changes the derived count and would also fail under the old single-match implementation. Add a small behavior-level test that presents one correct and one stale statement; avoid coupling to whole-document line numbers or totals.
