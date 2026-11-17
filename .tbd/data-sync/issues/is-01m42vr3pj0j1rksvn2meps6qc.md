---
type: is
id: is-01m42vr3pj0j1rksvn2meps6qc
title: Regularize the 89 refused Kingbird-derived records in an algebraic field
kind: task
status: open
priority: 3
version: 4
delegate: null
labels: []
dependencies: []
parent_id: is-01m42vqz7v80k9cjt16sbe4qv1
hold: null
hold_until: null
created_at: 2026-10-04T07:06:13.074Z
updated_at: 2026-10-31T05:55:14.994Z
started_at: 2026-10-31T05:00:32.419Z
---
The 89 Kingbird records' 36-digit poses overlap at dilation 1; smallest verifying dilations 1+1e-31..1+1e-27 would make 75 views exact packings below the register's verified upper bound (a tier promotion) and 14 enlarge the container. Prototype the regularization in Q(alpha) from the constructions' exact algebraic coordinates (Kingbird pages, Gobel families) so no dilation is needed; gain is 2 squares across all 89 under the current rule, so measure value before building.

## Notes

2026-10-31 bold-ritchie-l5 (intake pass of 31 October, epic think-3guf, lane L5): the four exemptions this bead owned in default_drawings.SETTLED (39, 55, 290, 291; UNRATIFIED until 2026-11-09) are settled by both strong generators, run on 31 October: grid-slack v2 at 0.5, 1 and 5 degrees (grid-slack-yk2h-2026-10-31-n39-291-grid-deg05/-deg1/-deg5, 70 CPU-s) drew an exact view at every count that changes nothing visible (row 10, no change); Evan Daniel's driver (evand-regularize-yk2h-2026-10-31-n39-291-evand, 1,600 s of wall) drew at 39 a solved view at U that the selection admits (an exactly verified view at most U replacing the numerically checked witness), at 55 no visible change, and at 290 and 291 a same-side view with no visible change and a solved view held at row 4 (1.75e-19 above U). So 39 is regularized and 55, 290 and 291 are decided no better on the same witnesses; UNRATIFIED is empty, 0 counts exempt (67 regularized, 228 regular as published, 29 decided, 0 pending); --check-state --base-ref origin/main and flip_regularization --check pass. Evidence: packing/cases/regularized_drawings/think-yk2h-2026-10-31/. Branch claude/bold-ritchie-xo28us-regularize, draft PR #849 (data 390954982, re-pin 214c18a63). For the owner (in the PR): at 55, 290 and 291 an exact view at U exists that row 10 leaves undrawn for no visible change. The bead's wider aim, the 89 refused records in Q(alpha), is unchanged and stays open.
