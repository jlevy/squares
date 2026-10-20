---
type: is
id: is-01m5c0fxm92eqjcj2cnapa6hms
title: "check_requests --draft: C1 wording says no replay has passed for results whose replay is recorded"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5c0ftybryt8q817fj95axz8
created_at: 2026-10-20T06:37:59.305Z
updated_at: 2026-10-20T06:37:59.305Z
---
The --draft text for C1 results ('no replay here has passed yet') contradicts V3 for T-184 and T-191, whose reproduction is recorded as evidence. Found by c-lane-replies 2026-10-20; drafts for #594/#610 were rewritten by hand. Fix the template to distinguish 'replayed, controls owed' from 'not replayed'.
