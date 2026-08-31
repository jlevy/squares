---
type: is
id: is-01m1aqjm2qrvv2w0pvp2yzn1db
title: "Robust-rational sweep: promote the decimal known-best witnesses and retain the certificates"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-31T01:40:08.918Z
updated_at: 2026-08-31T01:40:08.918Z
---
packing-witness promote --strategy robust-rational promotes 34 of 36 decimal known-best witnesses in ~33s total (n=68,69 refuse: corners-form input), each independently checkable via devtools.check_rational_witness_independent, each within ~1e-9..1e-30 of its reported side. Nine of the ten annealed sizes still carry the trivial grid as verified ceiling. Sweep, retain certificates as evidence with novelty basis 'exact replay of a published packing'; each verified_upper_bound move remains a reviewed change per the evidence contract. Sequenced inside BC-089 by X-009.
