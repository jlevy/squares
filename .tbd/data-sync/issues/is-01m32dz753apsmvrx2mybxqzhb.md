---
type: is
id: is-01m32dz753apsmvrx2mybxqzhb
title: Consolidate the full external n=17 source chain, not only the newest
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
created_at: 2026-09-21T16:49:44.099Z
updated_at: 2026-09-21T16:49:44.099Z
---
The announcement gives a chain: ojoshe 4.59 (Sep 4), Mira 4.613029 (Sep 8), Guzhou0806 4.613046 (Sep 19), Mira/Guzhou 4.614154 (Sep 20-21), Kleddamag + Codex 4.619791 (Sep 21).

As exact rationals the last three share a numerator with a falling denominator: 461300/99999, 461300/99951, 461300/99853. This repository retains only Mira and Guzhou0806 R012 (packing/resources/web/n17-weighted-certificates-2026-09-20/). It does NOT hold the 4.614154 intermediate at all, and has never seen ojoshe's 4.59.

Consolidate the chain as one account: what each source establishes, what it descends from (our own T-019 is the ancestor Mira and Guzhou both credit), which are independent and which are refinements of a shared construction, and what the shared-numerator structure means. Locate and retain the 4.614154 intermediate if it is publicly available; record its absence explicitly if not.

The point is a single coherent n=17 record rather than five disconnected intakes.
