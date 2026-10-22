---
type: is
id: is-01m5jexp6zbhzpmhy67a9tnp8e
title: "Import Evan Daniel: s(303) <= 17.909772217275, 1.86e-4 below Ostashev's (#728)"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
created_at: 2026-10-22T18:45:37.119Z
updated_at: 2026-10-22T18:45:37.119Z
---
Issue #728 (https://github.com/jlevy/squares/issues/728), opened 2026-10-22T17:17:20Z by evand (Evan Daniel): s(303) <= 447744305431858194305431410441/25000000000000000000000000000 = 17.909772217274327772..., claimed 1.86e-4 below the register's 17.909958291070 (Daniil Ostashev, #501/#562). Certificate evand/square-packing@f06521f search/packer/candidates/s303_r303w0.cert (SHA-256 929c2acf...8080), a dilation certificate (f64 packing scaled by 1+1e-12, rational half-angle tangents). The author calls it a new packing (matching distance 0.266 under the best of 8 symmetries; 91 tilted vs 92). Local optimality unresolved: a first-order descent of ~4.8e-7 probably exists.
Plan (efficiency rule of 22 October): stage 1 triage read-only (c-triage-1022c), then ONE records PR that registers, carries the independent stage 4 review, adopts at 303 and regularizes (House Rule), with no site edition (think-wdqo).
blocked_on: none
