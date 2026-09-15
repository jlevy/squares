---
type: is
id: is-01m2hf8hw6jhs15rbqj5yh0cg9
title: "PR #155 review D79: ledger's lost-timing exemption hard-coded; SYNOPSIS says a budget is retained"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb40g8vbnq8914rkt7p87c
created_at: 2026-09-15T02:45:13.221Z
updated_at: 2026-09-15T02:45:13.221Z
---
Review: attic/reviews/pr155/review-pr155-d46b86a5.md (PR #155 review at d46b86a5). Parent: think-xqc3.

Source: #155 R20.

Files: packing/src/sqpack/campaign/ledger.py:880-891; packing/tests/test_campaign_tools.py:623-663; SYNOPSIS.md cost table rows exp-207..exp-210 (hand-maintained, no generator).

Fix: rounds declare known_defects D-067 and a migration dated after the round; the id list and fixed date are gone; SYNOPSIS rows state the recorded budgets.
