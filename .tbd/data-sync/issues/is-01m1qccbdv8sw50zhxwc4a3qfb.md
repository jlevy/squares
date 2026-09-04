---
type: is
id: is-01m1qccbdv8sw50zhxwc4a3qfb
title: "F11: the reported minimum-mass witness must lie in the feasible part of its event cell, on both routes"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:36.731Z
updated_at: 2026-09-04T23:41:11.972Z
---
F11, larger than PR 80 says: on this branch's head 158 of 181 directions at n = 11 and 159 of 181 at n = 17 report a witness centre outside the admissible domain -- the midpoint of an event cell the domain polygon only partly covers. The verdict is unaffected; the point is not a witness (D-449 on this branch, outstanding until this lands). PR 80's _cell_witness fixes it, but merged onto this branch sweep.py auto-merges with the fix in the Fraction reference path only, while the integer route that runs keeps the midpoint and the value-and-witness equality test breaks on 5 of 6 directions. Port into one helper both minimum_covered_mass_integer and minimum_covered_mass_fraction call; keep the equality test; exhaust all 181 directions of all four retained certificates on the integer route (cheap now), because the strict-inside check is a new hard-error path the lane could only sample.
