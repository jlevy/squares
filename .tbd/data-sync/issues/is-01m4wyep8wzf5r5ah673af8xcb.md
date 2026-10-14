---
type: is
id: is-01m4wyep8wzf5r5ah673af8xcb
title: "render_announcement: Review A of PR 598, findings A1, A2, A5, A10, A11, A14, A15 (layer 5's tool, #563)"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T10:13:45.372Z
updated_at: 2026-10-14T10:13:45.372Z
---
Review A on https://github.com/jlevy/squares/pull/598#pullrequestreview-5516346807 found, in packing/devtools/render_announcement.py (layer 5, #563): A1 counts() treats the case lane's regularization of the entry's own packing as a rival (T-136 drops six counts, T-138 two); A2 a SUPERSEDED standing drops T-009 for its own regularization T-155; A5 shown() prints up to 40 decimals where the bound cannot beat previous (--all); A11 the header date defaults to UTC; A14 MONTHS repeats adopt_houses.words; A15 serial gh api users calls. A10: bibliography credited_names has no Rio Calle entry, so --all credits T-159 to Calle. Fix on #563 or after it merges.
