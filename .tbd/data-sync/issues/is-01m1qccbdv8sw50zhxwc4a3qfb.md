---
type: is
id: is-01m1qccbdv8sw50zhxwc4a3qfb
title: "F11: the reported minimum-mass witness must lie in the feasible part of its event cell, on both routes"
kind: task
status: in_progress
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:36.731Z
updated_at: 2026-09-05T00:43:25.267Z
---
F11, larger than PR 80 says: on this branch's head 158 of 181 directions at n = 11 and 159 of 181 at n = 17 report a witness centre outside the admissible domain -- the midpoint of an event cell the domain polygon only partly covers. The verdict is unaffected; the point is not a witness (D-449 on this branch, outstanding until this lands). PR 80's _cell_witness fixes it. Its 28990b00 head merged onto this branch left the fix in the Fraction reference path only (the equality test failed on 5 of 6 directions); its 04127189 head applies the helper on both minimum_covered_mass_integer and minimum_covered_mass_fraction, checks the integer route's preconditions in the function itself, and re-implements reduce_to_cells independently of reduce_to_spans so the reference shares no geometry with the optimised route -- port that code as it stands. Keep the value-and-witness equality test; exhaust all 181 directions of all four retained certificates on the integer route (cheap now), because the strict-inside check is a new hard-error path the lane could only sample.
