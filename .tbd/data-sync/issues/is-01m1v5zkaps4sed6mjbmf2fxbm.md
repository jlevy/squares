---
type: is
id: is-01m1v5zkaps4sed6mjbmf2fxbm
title: Quantify a strict improvement past T-022 by shrinking the certified core
kind: feature
status: in_progress
priority: 1
version: 5
labels:
  - mathematics
  - fractional
  - follow-up
dependencies: []
parent_id: is-01m1sn5t0dm6rjj200pw5p1b7a
child_order_hints:
  - is-01m1v75q8q7vgpswqag5fy7s8x
created_at: 2026-09-06T10:59:45.109Z
updated_at: 2026-09-06T11:20:34.326Z
---
Nonblocking explicit-epsilon route from the frozen T-018 atomic measure. For fixed atoms and weights of total M=434547/40000, search rational B'<9977/10000 and exactly replay the minimum net-core mass m(B'). Rescaling weights by 1/m(B') remains a contradiction whenever m(B')>M/11=434547/440000, so the old 1 threshold is unnecessarily strong. Acceptance: preregister a bounded rational shrink sweep or exact critical-event enumeration; implement the reusable finite arrangement check rather than a one-off calculation; retain exact event formulas, monotonicity and mutation controls; either certify one rational B' and an explicit algebraic or rational lower bound strictly above T-022, with source-distinct review, or retain a falsifying obstruction and price the next route. Keep it outside T-022 and the current release gate until independently reviewed.

## Notes

Coordinator allocation corrected 2026-09-06T11:05Z after checking X-016 ownership: H-080/exp-090 remain reserved to the closure-manager namespace and are NOT allocated here. Use fresh coordinator-satellite identities H-090 and exp-110, confirmed absent on the integrated branch, origin/main, and the live PR94 ref. Fixed preregistration target: B'=99769/100000, q=100001/100000, accept iff exact minimum m(B')>434547/440000; positive target bound 38100381/10000000=3.8100381 and exact comparison to T-022. No BC ID allocated. This is nonblocking and outside both manager ranges.
