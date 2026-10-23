---
type: is
id: is-01m4pcbmdj7qjggrjemdjsct5v
title: "Import wand125: s(31) >= 2391/400 = 5.9775 by the mixed_n31_L59775 fine-net certificate (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-lower-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:02:04.210Z
updated_at: 2026-10-23T06:18:58.211Z
started_at: 2026-10-23T06:18:58.210Z
---
Found in the 2026-10-11 intake read of wand125/square-packing (think-q655); nothing on GitHub asked. Commit 23e3186 (2026-10-11T00:51:18Z, before the head 04fbef0) adds problems/square-lower-bounds/certificates/mixed_n31_L59775/: a fine-net measure certificate reporting s(31) >= 2391/400 = 5.9775 (31 unit squares do not fit in the closed square of side 2391/400), mass 3099999/100000 < 31, core B = 4999/5000, declared net proof_net {step 1/5002, last 2072}, 2,073 directions; candidate digest 2d8d9d59...; the candidate and check2 receipts sit in the repository's data release, not the commit. The author's pre-publication check ran sqverify_fast (jlevy/squares crate with proof_net support, wand125 branch fe12e036c, source digest ab6e33e164db) from the bundle's check2/src on a fresh Ubuntu 24.04 machine: 2073/2073 directions VERIFIED in 7,277 s, mass x 0.985 control refused in 32 directions.

Against the record: n = 31's reported and verified lower bound is 2381/400 = 5.9525 (wand125 rect, 2026-10-01); #446 reported 597/100 = 5.97 (mixed_n31_L597, E-wand125-fine-net-lower-bounds-446-report, not adopted). 2391/400 is above both, by 1/40 and 3/400. The same route as T-142/T-143 (think-i85v) and T-132 (think-r333): stage 1 triage, a packet at 23e3186 (or the head, with the release assets), stage 3 registration, and a stage 4 replay with sqverify-fast from reviewed source for declared nets over all 2,073 directions with whole-net controls; priced from the author's 7,277 s (threads not stated) and the T-142/T-143 receipts.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/534. Tracker https://github.com/jlevy/squares/issues/544.
