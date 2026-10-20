---
type: is
id: is-01m4x4c8rf9czxj1kybjqrg7xp
title: "#597 review A2: no test covers several moved replies through _moved"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-10-14T11:57:17.454Z
updated_at: 2026-10-14T11:57:25.786Z
closed_at: 2026-10-14T11:57:25.786Z
close_reason: "fixed in ee9c4703c: test_each_reply_whose_statement_has_moved_is_its_own_reason_oldest_first asserts two reasons in record order in replies_due and corrections; the reversed-order and first-only mutants of _moved both fail it (#597 head 8db1905d5)"
resolution: null
duplicate_of: null
---
Review A of #597 (review 5517404240), finding A2 (Medium): no test had more than one stale reply for an entry, so reversing the order of _moved's reasons or keeping only the first survived all 57 tests.
