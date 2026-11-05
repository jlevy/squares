---
type: is
id: is-01m6pmy1yjah0yzxy31g6sr734
title: "Import Evan Daniel: s(175), s(204), s(260), s(268), s(293), s(303), s(304) upper bounds, seven new packings (#914)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l51
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m6pn9e3bd7729mpbdkgf64gv
hold: null
hold_until: null
created_at: 2026-11-05T20:03:20.145Z
updated_at: 2026-11-05T21:18:51.000Z
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

## Notes

2026-11-05 (bold-ritchie-l51): retained, certified and registered on branch claude/bold-ritchie-xo28us-l51 (draft PR, lane L51 of epic think-3guf). Packet packing/resources/web/evand-issue914-2026-11-05 pins evand/square-packing at bb4cc78e5b35103c1f177db55e9cf08974e66563 (the head when read, and the first commit holding the seven sets; 38 min 37 s before the issue) and retains all 56 files of the seven sets plus LICENSE (MIT, Evan Daniel) and CREDITS.md; verify_cert*.py pinned identical_to the n183 packet. Packet packing/resources/web/evand-issue914-views-2026-11-05 pins the six regularized views identical_to packet A's copies, so both routes decide them too. All 13 digests the issue prints match. Both maintained exact routes accept all seven certificates (21 jobs, 1,439,796 pair decisions, 200.09 route CPU-s) and all six views (18 jobs, 1,237,776 pairs, 160.32 CPU-s), refuse every gross control, and the sharp controls came out as expected in both packets; check --replay admitted both receipts again. Each exact side rounds up at 12 places to the issue's print. Identity (packet A measure/): no certificate one to one with its house under any symmetry (moves beyond 0.1: 60, 66, 42, 80, 193, 124, 66; at 260 also 33 against T-257). Ledger campaign/issue-intake/upper-bounds-914-20261105 records all seven. Draft PR https://github.com/jlevy/squares/pull/916 (labels intake, S3); main b099992a9 (#912, T-266) merged in 4090aa586, head f848f1d4c. #914 labelled intake (stage 0). Registered T-267 (175), T-268 (204), T-269 (260), T-270 (268), T-271 (293), T-272 (303), T-273 (304) at V0/C0, draft S3 each, credit naming Chris Deotte for the method. result-requests.yaml #914 entry, answer bead this one. Stage 4 brief: think-lrj4 (tbd-strong-max, not run by this lane). The other 51 commits past the 0e76d9f read hold no other result (intake-watch.yaml read through bb4cc78).

Stage 7: no reply is owed before the records PR merges (result-import.md, stage 7: a reply follows the merge and links only to main; nothing here waits on the author). The import reply below is the acknowledgement. Post it after the PR merges and the deploy is verified: render from main with `check_requests --draft 914` (it refuses off main), reconcile with this draft, check that main and the site say what this says, post, and record it under #914's replies in the next change. It names T-267 to T-273, which are true only once on main.

DRAFT of #914's import reply (not posted):

@evand, thank you, Evan, for the seven certificates and for committing every input beside them.

- **Retained.** We read evand/square-packing at `bb4cc78`, the commit the issue names and the repository's head when read. All 56 files it adds under `search/packer/candidates/` are retained under your MIT licence, with `LICENSE` and `CREDITS.md`. The thirteen SHA-256 digests in the issue are the files'.
- **Checked here.** Each certificate holds its n squares, and its header side is the exact side the issue states; each rounds up at 12 places to the issue's print. Two maintained exact routes, the `sqpack` exact witness verifier and the independent rational corner checker, accept all seven over every wall and every pair in rational arithmetic, and the six regularized views as well, each at its certificate's side. Duplicate-square and outside-container controls, and sharp controls at exact contact and 1e-30 past it, came out as stated in advance. Your two checkers were not run here, and the routes share this repository's reader of your format.
- **Registered.** One entry per count, each at V0/C0 until the review: T-267 at 175, T-268 at 204, T-269 at 260, T-270 at 268, T-271 at 293, T-272 at 303 and T-273 at 304 ([results](https://squaremath.org/results.html#t-267)). Each is the first report below the record at its count, so the report-order rule records all seven.
- **Against the houses.** Measured here, none pairs one to one with the house's packing under any of the box's eight symmetries. The optimal assignment moves 60 squares beyond 0.1 at 175, 66 at 204, 42 at 260, 80 at 268, 193 at 293, 124 at 303 and 66 at 304. At 260, against your #845 packing, whose tilted island you say it recomposes, it moves 33. So the record reads all seven as new arrangements, as you say.
- **Credit.** Each entry credits you, with Chris Deotte credited for the method, as you asked. At 175 the register's packing (Daniil Ostashev's, as PingYou Ltd and Mishapolk refined it) is named as the start, and at 260 Kirill Tymchishin's Kaggle packing through your #845 island. At 204 the gadgets are your own s(233) and s(370), and at 268, 293, 303 and 304 the record says the donors were not recorded. The Kaggle side-only values state no packing, so they are not reports.
- **Next.** A separately run stage 4 review will decide all seven again with clean-room code and read the lineages. After that, each count adopts its certificate under the house rule, replacing T-186, T-264, T-265, T-242, T-257 and T-240, with both regularizers run on each new house; your six regularized views are offered as candidate drawings. We will reply again when that lands.
