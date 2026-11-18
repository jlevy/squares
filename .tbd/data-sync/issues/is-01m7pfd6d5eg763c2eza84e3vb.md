---
type: is
id: is-01m7pfd6d5eg763c2eza84e3vb
title: "PR #1028 A5 (Low): the packet README does not say how to run six programs"
kind: bug
status: closed
priority: 2
version: 3
delegate: r127b2-1118
labels: []
dependencies: []
parent_id: is-01m7pfcktsy9bnc43psx211dgs
hold: null
hold_until: null
created_at: 2026-11-18T04:42:26.597Z
updated_at: 2026-11-18T05:23:45.910Z
started_at: 2026-11-18T04:42:39.710Z
closed_at: 2026-11-18T05:23:45.910Z
close_reason: "fixed in c932385e65: README gives command and printed result for every program; the six commands rerun into scratch reproduce their receipts byte for byte (trial.json apart from times). Reply https://github.com/jlevy/squares/pull/1028#issuecomment-6969920966"
resolution: null
duplicate_of: null
---
Severity Low. packing/resources/web/de-winter-1015-1017-1020-review-r127b-2026-11-18/README.md:84-126. How to Run Them omits rb127_custody, rb127_trial, rb127_routes, rb127_e1p, rb127_describe and rb127_constant; What They Printed omits custody and describe. Stage 4 'Its code is kept'. Fix: one command and one result line each (the README is not frozen). PR #1028, review A: https://github.com/jlevy/squares/pull/1028#issuecomment-6969042368
