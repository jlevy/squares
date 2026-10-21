---
type: is
id: is-01m5fsnyqj85asc7tq4276kyk9
title: Widen profile directory table and keep account labels intact
kind: task
status: in_progress
priority: 2
version: 3
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:55:54.737Z
updated_at: 2026-10-21T17:57:38.942Z
started_at: 2026-10-21T17:56:05.132Z
---
Use the established wide-table bleed on larger screens; give the Links column enough space and keep each account icon/username together. On narrow screens preserve horizontal table scrolling rather than breaking handles awkwardly.

## Notes

Wide-table bleed and wider Links column; icons align with first line even when labels wrap. Latest user also removes parenthetical directory nicknames and reduces shared account icon size consistently in table/profile. Preserve profile Handles and visible account usernames.
