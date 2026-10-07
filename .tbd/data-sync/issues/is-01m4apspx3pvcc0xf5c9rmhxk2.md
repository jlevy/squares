---
type: is
id: is-01m4apspx3pvcc0xf5c9rmhxk2
title: n17 apex certificate large-integer roundtrip refusal
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-n17-ten-hour-session.md
labels: []
dependencies: []
parent_id: is-01m4agrtpeqyjz4bsfsn4dyjmc
created_at: 2026-10-07T08:13:38.071Z
updated_at: 2026-10-07T08:45:21.710Z
closed_at: 2026-10-07T08:45:21.704Z
close_reason: Same-claim exp264 fresh CLI replay accepted after canonical-string serialization repair; failed exp262 preserved. Source76e2830b4, production+replay5.67s.
resolution: null
duplicate_of: null
---
Session184 exp262 arithmetic passes at513adb1bf but required fresh CLI replay refuses oversized bare JSON integer from selected retained dual cell. Preserve original failed round; encode exact large numerators safely without relaxing generic reader guard; add realistic roundtrip and tamper controls; require separate preregistered sameclaim exp264 before target retry. Astra owns mathematical review; Sol owns serialization engineering.
