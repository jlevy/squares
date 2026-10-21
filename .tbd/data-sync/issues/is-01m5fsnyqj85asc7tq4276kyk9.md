---
type: is
id: is-01m5fsnyqj85asc7tq4276kyk9
title: Widen profile directory table and keep account labels intact
kind: task
status: in_progress
priority: 2
version: 6
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:55:54.737Z
updated_at: 2026-10-21T19:47:23.211Z
started_at: 2026-10-21T17:56:05.132Z
---
Use the established wide-table bleed on larger screens; give the Links column enough space and keep each account icon/username together. On narrow screens preserve horizontal table scrolling rather than breaking handles awkwardly.

## Notes

User final layout follow-up: widen Name column so most full names stay on one line; allow long resource URLs to wrap at meaningful URL boundaries instead of forcing other columns narrow. Preserve wide-table bleed, full names only, blank zero/unknown cells, separate Results/Records/Credits, Accounts username icons. Review resource wrapping and name width together and rebuild live preview.
