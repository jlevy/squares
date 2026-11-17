---
type: is
id: is-01m16hf4vq08hynk8gcc0hh8a5
title: Bound and count the n=29 solutions by homotopy continuation, without a Groebner basis
kind: task
status: closed
priority: 0
version: 3
delegate: w-beads29-1025
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-08-29T10:36:25.847Z
updated_at: 2026-10-25T17:16:51.955Z
started_at: 2026-10-25T17:16:38.058Z
closed_at: 2026-10-25T17:16:51.955Z
close_reason: "Superseded by T-246 (Evan Daniel's degree-7213 s(29) minimal polynomial, obtained by homotopy) and its validation under think-10m1 (#817/#816): the projection degree this bead sought is 7213."
resolution: canceled
duplicate_of: null
---
agenda-006 BC-070, following BC-066's measured wall. BC-066 established that Groebner elimination does not reach an eliminant for the n=29 system on this hardware, and that the obstruction is the size of the ideal rather than coefficient swell. Homotopy continuation answers the degree question without computing any basis: the mixed volume bounds the isolated solutions with every coordinate nonzero, and the packing's own solution lies in that torus because no angle in it is zero. Counting the solutions and taking the distinct s values gives the degree of the projection to the s-axis, which is what would turn BC-060's blind integer-relation sweep into a targeted search.
