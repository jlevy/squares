---
type: is
id: is-01m16hf4vq08hynk8gcc0hh8a5
title: Bound and count the n=29 solutions by homotopy continuation, without a Groebner basis
kind: task
status: open
priority: 0
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T10:36:25.847Z
updated_at: 2026-08-29T10:36:25.847Z
---
agenda-006 BC-070, following BC-066's measured wall. BC-066 established that Groebner elimination does not reach an eliminant for the n=29 system on this hardware, and that the obstruction is the size of the ideal rather than coefficient swell. Homotopy continuation answers the degree question without computing any basis: the mixed volume bounds the isolated solutions with every coordinate nonzero, and the packing's own solution lies in that torus because no angle in it is zero. Counting the solutions and taking the distinct s values gives the degree of the projection to the s-axis, which is what would turn BC-060's blind integer-relation sweep into a targeted search.
