---
type: is
id: is-01m24paqcx5d26wd5zjjn8k7rc
title: Reproduce the measured results as plans
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-strategy-plans-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T03:38:36.818Z
updated_at: 2026-09-10T03:38:36.818Z
---
A plan that cannot restate a result already measured is not yet a description of it. Port these four into plan documents and check each reproduces its number:

1. Plain projection ratchet from the grid at n=11: reaches 3.9640625, and every failure uses exactly 48 solver calls.
2. Cold fixed-side solve at n=11, +4 per cent: 12/12 unconstrained, 5/12 with faces declared.
3. Built assembly handed to the same solver: 5/8 at +10 per cent against 1/8 random, 8 of 8 face contacts kept.
4. Contacts declared as equalities from Trump's own n=11 packing: drift 0.0000 at 200 steps, 0.2839 at 4000 -- the record is a repelling fixed point unless the constraint is a band.

Each plan carries its rung so the comparison is honest, and the rewired and thinned controls sit beside every structured plan.
