---
type: is
id: is-01m6pmy1yjah0yzxy31g6sr734
title: "Import Evan Daniel: s(175), s(204), s(260), s(268), s(293), s(303), s(304) upper bounds, seven new packings (#914)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: bold-ritchie-l51
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-05T20:03:20.145Z
updated_at: 2026-11-05T20:03:23.960Z
started_at: 2026-11-05T20:03:23.959Z
---
Import of jlevy/squares#914 (opened 2026-11-05T19:07:50Z by evand, Evan Daniel): seven upper bounds, each the certificate's exact rational side rounded up at 12 places: s(175) <= 13.764050051544, s(204) <= 14.804361383652, s(260) <= 16.633520950889, s(268) <= 16.872499518136, s(293) <= 17.623065212061, s(303) <= 17.901832750855 and s(304) <= 17.920944093341. Global optimality is not claimed.

## Claim map
- Source: evand/square-packing@bb4cc78e5b35103c1f177db55e9cf08974e66563 (committed 2026-11-05T18:29:13Z, 38 min 37 s before the issue; the repository's head when read on 5 November), search/packer/candidates/. The commit adds the seven sets (56 files, 1,349,357 bytes): certificate, f64 input, pre-descent input, 80-digit point, run summary, prior facts, comparison with the store's prior, and at six counts a regularized view and its JSON. Licence MIT, copyright (c) 2026 Evan Daniel (LICENSE unchanged); CREDITS.md and the commit's Co-Authored-By trailer disclose Claude.
- The 13 SHA-256 digests the issue prints are the files' (checked on the checkout: all OK).
- Claims: (1) seven new upper bounds, one register entry per count [new upper-bound entries T-267 to T-273 at V0/C0]; (2) six exact KKT certificates (175, 204, 268, 293, 303, 304), each with a regularized view at the same side, and at 260 a dilation certificate of the f64 packing (the exact solver did not converge); (3) the source's two checkers verify_cert.py and verify_cert2.py report VALID on all 13 files, with a shared author and format (source statement only); (4) local optimality at 80 digits, not interval proofs (KKT at six counts; strict local minimum modulo flat motions at 204, 293, 304; inconclusive at 268; a first-order MILP descent at 303 not realised; not established at 260); (5) relationship: all seven new packings, not refinements, with matched-move and contact-pair numbers at 175, 204, 268 and 303; (6) credit: built by Daniel's fault-line composer, his implementation of Chris Deotte's multi-gadget fault DP (credit Deotte for the method); 175 from gadgets of the register's s(175) (Mishapolk's, after Daniil Ostashev et al.) and an earlier composer build; 204 from Daniel's own s(233) and s(370); 260 the same tilted island as #845's 260, same credit as #845's 260 (Kirill Tymchishin's Kaggle s(260) as the start); 268, 293, 303 and 304 gadget donors not recorded; (7) Kaggle per-puzzle side-only values at all seven counts, no coordinates: no report.
- Who holds each count (main 249bb82e7): 175 T-186 (Ostashev, improved by PingYou Ltd and Mishapolk); 204 T-264 (Daniel, improved by Özden); 260 T-265 (Daniel, improved by Yim); 268 T-242 (Lavrentev, improved by Daniel); 293 T-257 (Daniel); 303 T-240 (Couzo, after Lavrentev); 304 T-242 (Tymchishin, improved by Daniel). No register bound pending adoption below them; no other open report at these counts.

## Validation plan (priced)
- Replay in this lane: both maintained exact routes (upper_bound_reports certify) with the duplicate-square and outside-container controls and the sharp controls, for the seven certificates (packet evand-issue914-2026-11-05) and the six regularized views (packet evand-issue914-views-2026-11-05, pinned identical_to the first packet's copies); identity against each house by measure_identity. About 0.2 to 0.5 CPU-hours by #845's receipt (90 route CPU-s for four counts) and #895's sharp controls (157 CPU-s at 260).
- Review: a separately prompted tbd-strong-max stage 4 review of all seven (brief on its own bead), then adoption at each count under the house rule with both strong generators' regularization.

Answer bead: this bead.
