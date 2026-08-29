---
type: is
id: is-01m16r2y7ejdft38tsp8ck6m22
title: Extend the n=29 integer-relation sweep to the margin rule's own reach
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T12:32:05.870Z
updated_at: 2026-08-29T12:32:05.870Z
---
agenda-006 BC-073, following BC-060 and BC-070. BC-060 swept degrees 2-20 at a coefficient bound of 1e22 on 1000 digits and refused at every degree. The margin rule's own reach formula, (d+1)*log10(C) < P - M, admits substantially more than degree 20 at that precision, so the sweep stopped well short of what the data supports. BC-070 now bounds the degree at 15,744, so the search has a ceiling for the first time. Extend the sweep to the reach the digits actually allow and report where it stops and why -- a refusal at a higher degree is a stronger statement about s(29) than a refusal at twenty.
