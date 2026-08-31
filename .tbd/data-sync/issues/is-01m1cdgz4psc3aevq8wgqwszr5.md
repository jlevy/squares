---
type: is
id: is-01m1cdgz4psc3aevq8wgqwszr5
title: Certify the green17 set at its exact ceiling 753/250 + sqrt 2 over Q(sqrt 2)
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-31T17:22:57.814Z
updated_at: 2026-08-31T17:22:57.814Z
---
Follow-on from the 2026-08-31 verification review (session-060, BC-106). The sixteen-point green17 set is certified at side 4426213/1000000 by two independent methods; its exact ceiling is t* = 753/250 + sqrt(2) (top-strip Lemma 4 a+2b <= 2 sqrt 2 with equality), bracketed by certification at 4.426213 and interval-audit refutation at 4427/1000. Certifying at t* exactly needs the shared cell certifier (cases/bentz13/verify_cover.py) generalized to a Q(sqrt 2) scalar satisfying the cover scalar contract, a rational upper-bound reduction for the Lemma 5 threshold comparison, and the green17 plan rebuilt over that scalar. Also worth typing: an exact escape-family argument for every side above t*, which would pin the set's ceiling as exactly t* rather than bracketing it.
