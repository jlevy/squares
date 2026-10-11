---
type: is
id: is-01m41d7k4fe8tbgjcqxejavg5k
title: "Site colours: every colour a named token, enforced by a test"
kind: task
status: closed
priority: 2
version: 10
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:33:17.327Z
updated_at: 2026-10-04T02:55:16.608Z
closed_at: 2026-10-04T02:55:16.608Z
close_reason: null
resolution: null
duplicate_of: null
---
Owner, 2026-10-03: all colours like the significance teal are logical CSS variables, so they can be changed in one place, and the design system enforces it. Tokenize the literal colours in the site stylesheets (shadows, the popover scrim, color-mix tints, the star's red) and add a check that no rule outside a custom property declaration names a colour of its own.

## Notes

Merged to main in jlevy/squares#330 at cecfb1c09 on 2026-10-04 02:36 UTC; deployed by Pages run 37171559780 (publish, deploy and verify-deployment passed).
