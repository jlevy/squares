---
type: is
id: is-01m5jexp6zbhzpmhy67a9tnp8e
title: "Import Evan Daniel: s(303) <= 17.909772217275, 1.86e-4 below Ostashev's (#728)"
kind: task
status: open
priority: 1
version: 2
labels:
  - result-import
dependencies: []
created_at: 2026-10-22T18:45:37.119Z
updated_at: 2026-10-22T19:45:36.316Z
---
Issue #728 (https://github.com/jlevy/squares/issues/728), opened 2026-10-22T17:17:20Z by evand (Evan Daniel): s(303) <= 447744305431858194305431410441/25000000000000000000000000000 = 17.909772217274327772..., claimed 1.86e-4 below the register's 17.909958291070 (Daniil Ostashev, #501/#562). Certificate evand/square-packing@f06521f search/packer/candidates/s303_r303w0.cert (SHA-256 929c2acf...8080), a dilation certificate (f64 packing scaled by 1+1e-12, rational half-angle tangents). The author calls it a new packing (matching distance 0.266 under the best of 8 symmetries; 91 tilted vs 92). Local optimality unresolved: a first-order descent of ~4.8e-7 probably exists.
Plan (efficiency rule of 22 October): stage 1 triage read-only (c-triage-1022c), then ONE records PR that registers, carries the independent stage 4 review, adopts at 303 and regularizes (House Rule), with no site edition (think-wdqo).
blocked_on: none

## Notes

2026-10-22 c-lane-728-import (records lane, for coord-intake-1021b): stages 2-3 pushed on branch claude/intake-728-daniel-s303, draft PR #731 (https://github.com/jlevy/squares/pull/731), head 52d89bf04, labels intake + S3. Registered as T-230 (main cacdafc1f after #722 merged; T-229 is #722's). Packet packing/resources/web/evand-n303-2026-10-22/ pins f06521f (8 files retained, 107,752 B; checkers + dilate_cert.py pinned against the n229 packet's identical copies, exactsolve.py against n183's; candidate/explore/dgen/bandflip/pk/crossing by digest); acquire_source --check PACKET_MATCHES_ITS_CONTRACT. check-claims --write at cacdafc1f: below T-186 by 1.8607379558e-4 and below all 13 other reports at 303. Replay of record (certify --workers 2): positive passes both routes, both controls refused on both; least wall 6.048e-13, least gap 1.2045e-12; 274,518 pair decisions, 33.54 route CPU-s, 44 s wall; check --replay passes (61 s). measure/identity.py (retained) repeats the triage measurement: 64 beyond 0.1 of T-186 under the identity, 91 tilted one sign vs 46/46, 45 same-sign / 44 flipped, no tilt shared. T-230 at V0/C0, draft S3, pending adoption; bibliography [Daniel n303 2026-10-22], credit "Daniel after Ostashev, Levy" (source README lists jlevy/Squares Project among the work it builds on, as for n155). Requests: #728 -> T-230; #522 read_through 17:00:22Z; #526 read_through 17:10:58Z + k0-knowledge-refresh + 15 Oct reply outdated (correction due). intake-watch: evand 7982d7a (think-7l2j), wand125 e48de24, Esummins 0b0a072. Next: map the stage 4 review (c-review-728-math), adopt at 303, regularize, then the release step after #725/#729.
