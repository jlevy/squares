---
type: is
id: is-01m16r2y7ejdft38tsp8ck6m22
title: Extend the n=29 integer-relation sweep to the margin rule's own reach
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T12:32:05.870Z
updated_at: 2026-10-12T23:39:20.374Z
closed_at: 2026-10-12T23:39:20.373Z
close_reason: "Completed in session-044 (agenda-006 BC-073 complete): reach derived as degree 35, degrees 21-29 swept with no relation, cost of 30-35 measured; D-364 found and recorded on the way."
resolution: null
duplicate_of: null
---
agenda-006 BC-073, following BC-060 and BC-070. BC-060 swept degrees 2-20 at a coefficient bound of 1e22 on 1000 digits and refused at every degree. The margin rule's own reach formula, (d+1)*log10(C) < P - M, admits substantially more than degree 20 at that precision, so the sweep stopped well short of what the data supports. BC-070 now bounds the degree at 15,744, so the search has a ceiling for the first time. Extend the sweep to the reach the digits actually allow and report where it stops and why -- a refusal at a higher degree is a stronger statement about s(29) than a refusal at twenty.
