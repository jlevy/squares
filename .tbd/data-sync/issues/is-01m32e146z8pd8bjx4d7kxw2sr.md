---
type: is
id: is-01m32e146z8pd8bjx4d7kxw2sr
title: PR 211's prose that R012 is the strongest public n=17 value is already stale
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
created_at: 2026-09-21T16:50:46.623Z
updated_at: 2026-09-21T16:50:46.623Z
---
Independent of how Kleddamag is adjudicated. The public chain advanced past PR 211 twice before it landed, and this repository holds neither step.

Exact ladder, all computed:
  T-019    459/100                      4.590000000000  (ours, on main)
  Mira     4613/1000                    4.613000000000  (retained)
  R012     461300/99999                 4.613046130461  (PR 211 registers this)
  R038     461300000000/99974999999     4.614153538431  (NOT held)
  prev     461300/99951                 4.615261478124  (NOT held)
  Kleddamag 461300/99853                4.619791092907  (attic only)

The 4.614154 is Guzhou0806 R038, pinned in the Kleddamag artifact's ATTRIBUTION.md at commit 32edfd3da78bf80a309398f552b3b602b9c45d6c. The 4.615261 is what the Kleddamag bounds.json calls previous_strict_lower. Note these are two DISTINCT values -- an earlier reading of the announcement chain conflated them.

Affects README.md:193-207, the packet README chronology table, and n-017.md's reported_lower_bound. Worth fixing in PR 211 before it lands, since it is a factual claim about the outside world rather than about our own evidence.
