---
type: is
id: is-01m0sk6tjfj4p5zdmrctkbx1mj
title: Do not attribute an unreported n=4 f-vector to Alpert et al.
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0shsv9v0pnbvnjwz4qgq16n
created_at: 2026-08-24T09:56:42.703Z
updated_at: 2026-08-24T10:13:55.899Z
closed_at: 2026-08-24T10:13:55.899Z
close_reason: "Fixed before the retained H-032 run in 257cb0d: labelled and unlabelled source comparisons are separate and fail closed; n=4 records no unreported f-vector; the orientation identity is derived independently on both sides. Exact generation/replay and focused controls pass."
resolution: null
duplicate_of: null
---
The first uncommitted small-n checker draft populated reported_f_vector=[24] for n=4 and cited Alpert et al. Table 2, but that table does not include an n=4 row. Retain the independently derived 24 isolated states, compare only the published Table 1 Betti vector [24,0], and state explicitly that the n=4 f-vector was not tabulated.
