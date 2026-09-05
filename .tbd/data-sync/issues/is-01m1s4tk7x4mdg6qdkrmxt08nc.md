---
type: is
id: is-01m1s4tk7x4mdg6qdkrmxt08nc
title: Case-level evidence lists omit the first-party certificates on the seven cases they support
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T16:01:03.740Z
updated_at: 2026-09-05T16:01:03.740Z
---
Survey 2026-09-05: on n=11,12,17,18,19,20,21 the case-level evidence array omits E-nNNN-fractional-certificate and E-fractional-interval-decision, which verified_lower_bound.evidence does cite (n-011.md:82, n-012.md:73, n-017.md:76, n-018.md:78, n-019.md:74, n-020.md:73, n-021.md:73). Same gap on three upper bounds: n-040.md:78, n-065.md:73, n-089.md:73. Nothing checks that the case-level list is a superset of the field-level lists, so a reader looking for what supports the record misses the strongest result on the case.
