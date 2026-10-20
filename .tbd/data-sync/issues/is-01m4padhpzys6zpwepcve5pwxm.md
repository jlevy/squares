---
type: is
id: is-01m4padhpzys6zpwepcve5pwxm
title: "Import itsnaka (SQUISH): nine Mondrian packings at n = 176-305, smaller packings of 238, 239, 270, 305 (#500)"
kind: task
status: closed
priority: 1
version: 13
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:28:09.823Z
updated_at: 2026-10-14T18:51:37.117Z
started_at: 2026-10-11T20:28:23.635Z
closed_at: 2026-10-14T18:51:37.116Z
close_reason: "itsnaka 56fa71f read landed on main with #601 (merge 2319afaa5); the read's commit is 1364b0f1b after the message rewrite (was 31a817e8e)."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/issues/500 (2026-10-11T05:30Z). itsnaka/squish-certs aeacc6c124df339074f7370e1e010bb6e8c1b5ca squish-submission-2026-10-11, nNNN.cert.json exact rational (SQUISH format). Counts 176, 181, 238, 239, 270, 271, 272, 304, 305. 304 and 305 superseded by #506 (Couzo, built on these). Stages 1-4 replay through devtools.upper_bound_reports.

## Notes

2026-10-11 stage 1, 2 and 4-replay lane (intake W1 under think-mq0k; worktree branch worktree-agent-aa7e2838e10dafaa4, not pushed).

PIN: itsnaka/squish-certs aeacc6c124df339074f7370e1e010bb6e8c1b5ca (tree e67d0004e65363d58e8090560f92544093507104; authored and committed 2026-10-11T05:30:10Z; parent bd0c72e278b8f62f5b22169594daea1f171a49c4). First commit containing squish-submission-2026-10-11. Head when read: 56fa71f949234b63534772b3f3b4f1320fbf2afd (2026-10-11T05:30:50Z), which changes only the root README.md, to link #500 in its roster: no certificate or claim depends on it, so the pin stays aeacc6c. Commits past the intake-watch read (e63e4e5): d45669b (pinned by the #481 packet), bd0c72e (README links #481), aeacc6c (this pin), 56fa71f (README links #500). Retrieved 2026-10-11T20:34Z. No licence file: derived-only custody.
PACKET: packing/resources/web/squish-500-fourth-request-2026-10-11 (acquire_source declaration; scope README.md + squish-submission-2026-10-11, 67 files, 5,866,372 bytes, all pinned only; acquire_source --check: PACKET_MATCHES_ITS_CONTRACT). Nine derived exact facts (facts/n-NNN.yaml.gz), derive --check matches the checkout. Source key proposed: [SQUISH fourth request 2026-10-11].

CLAIMS THE RELEASE MAKES:
- Nine filed certificates nNNN.cert.json (s_exact, [x, y, t] rationals, box [0, S]^2), each s_exact equal to summary.csv's exact fraction. Issue's 15-digit S_n are truncations (each below the exact side by < 1e-15, at all nine); s_decimal is not a rounding (differs by -1.6e-15 to +6.9e-16). Safe display: s_exact rounded up.
- Five sources/ certificates, not offered as records: s154-a 12.9292934240939391 and s154-b 12.9305839972855079 (above case 154 by 2.73e-3 and 4.02e-3, and above T-136's 154), s240-b 15.9739500348208213 (above case by 4.26e-3), s272 16.9655871623998319 (below case 272 by 2.52e-3 but above the filed 272 by 6.876e-7: the filed 272 before its squeeze), s305 17.9508590931679247 (below case 305 by 2.10e-3, T-136 by 3.37e-4, T-140 by 2.81e-4, but above the filed 305 by 3.142e-4 and #506's print). Each is dominated by a filed certificate or above its case: no register action; stays in the packet.
- Author reports: SQUISH exact Fraction checker and Ellsworth check_packing.py at 1e-50 accept all nine and the sources; 60-digit contact solve, clearance 1e-32; an hour of nearby search and a squeeze moved none by more than 7e-07. No KKT, interval, local optimality, closed forms or optimality.

CLAIM MAP (exact side rounded up at 16 places; margin = other less this, cut at 10 significant digits; exact fractions in the packet's acquisition/claims.json; case = verified ceiling at main 3a5a91a90):
176 13.8128562532770564 | case T-101 (Kingbird print 13.82287565553229, Evan Daniel's exact ceiling 13.82287565553230) below by 1.001940225e-2 | no pending report | smallest: this.
181 13.9508195310229241 | case T-098 (Couzo, improved by Daniel) below by 2.929290931e-3 | #476's unrequested 181 below by the same | smallest: this.
238 15.9241067853214947 | case T-127 (SQUISH #401 refined by Gupta) below by 2.040071689e-3 | #470 (unregistered at 238) 2.040071689e-3 | smallest: this. Replaces SQUISH's own #401 packing (T-113/T-115 lineage).
239 15.9484433273005000 | case T-127 below by 8.698424271e-4 | #470 8.698424275e-4 | smallest: this. Replaces SQUISH's #401 packing (T-115 lineage).
270 16.9281969933290166 | case T-119 (Daniel) below by 9.610235117e-3 | T-130 8.526029547e-3, T-134 8.523037791e-3, T-136 (#481, SQUISH's own) 1.583132912e-3, T-138 8.526161708e-3, T-140 (#488) 1.578360212e-3 | smallest: this.
271 16.9491166878150100 | case T-098 below by 1.704104809e-3 | #476's 271 the same | smallest: this.
272 16.9655864748376712 | case T-119 (Daniel) below by 2.523670931e-3 | #476's 272 2.579393014e-3 (T-092's older 16.968165867864400 is above the case) | smallest: this.
304 17.9296570421708801 | case T-098 below by 4.992976219e-3 | #476's 304 the same; #506 (Couzo, 337078c, built from this packing) prints 17.929565946849 rounded up: ABOVE it by at least 9.109532188e-5 | smallest: #506.
305 17.9505448539256365 | case T-098 below by 2.414605089e-3 | T-136 (#481, SQUISH's own) 6.512902217e-4, T-140 (#488) 5.949182813e-4, #489's unregistered 305 (ties T-140) the same, #476's 305 2.414605089e-3; #506 prints 17.950466482138 rounded up: ABOVE it by at least 7.837178763e-5 | smallest: #506.
T-146 has no row at any of the nine counts. #501, #503, #504, #505 name none of them.
Register action proposed: one new upper-bound entry (bounds of one kind at several counts in one release), scope all nine in-horizon counts, published 2026-10-11 (aeacc6c's commit date). At 304 and 305 the entry is superseded at registration if #506 registers first, and it stays because #506 credits these packings as its starting points. 238, 239, 270 and 305 replace SQUISH's own earlier packings; the earlier entries keep their claims.

PRICE (measured, not estimated): see the replay receipts below. Pair decisions: 3 n (n-1) summed = 1,743,036.

## Draft acknowledgement (2026-10-11, not posted; the owner posts it)

Thank you, Nate. We received the nine exact certificates in `squish-submission-2026-10-11` and pinned itsnaka/squish-certs at aeacc6c124df339074f7370e1e010bb6e8c1b5ca, the commit that adds them; the later README commit 56fa71f changes no certificate. The five certificates in `sources/` (two of 154, and 240, 272 and 305) are recorded with them as provenance, and each is above its case's bound or above the filed certificate at its count. Each of the nine sides is below the bound the record holds at its count today, and below every other report pending there, including your own #481 packings and Francisco Couzo's #488 refinements of them at 270 and 305, except at 304 and 305, where Francisco Couzo's #506 reports smaller sides built from these packings; yours are recorded as his starting packings. The tree has no licence, so as before we keep digests and exact facts derived from the pinned certificates rather than the files. Next we replay every certificate exactly from `s_exact`, the rational centres and the half-angle tangents, by two maintained exact routes with duplicate-square and outside-container controls, and review the replay. One note: the 15-digit values in the issue are truncations of `s_exact`, and each certificate's `s_decimal` is not a rounding of it, so the record displays each side rounded up from the exact fraction.

## Stage 2 and stage 4 replay (2026-10-11, commit 56bdfb51b on worktree-agent-aa7e2838e10dafaa4, not pushed)

Packet packing/resources/web/squish-500-fourth-request-2026-10-11: declaration, acquisition record, manifest (67 files, 5,866,372 bytes, all pinned only), report.json, claims.json (frozen at main 3a5a91a90), nine facts, one whole receipt (2,412,308 bytes uncompressed, receipts/exact-certification.json.xz). HOUSES gains [SQUISH fourth request 2026-10-11]; tests/test_upper_bound_reports_500.py (5 tests) and EVERY in tests/test_upper_bound_reports.py cover it.
certify --workers 1: 27 jobs (9 positives, 18 controls), 2026-10-11T20:39:56Z to 21:20:06Z (40 min 10 s wall, load 2 to 14 on 4 cores); 1,743,036 pair decisions, 1,253.51 route CPU s, 2,322.21 job wall s summed, longest job 202.56 s (304 duplicate-square control). All 9 positives pass both routes (sqpack exact verify, independent rational corner checker); both routes refuse all 18 controls (overlap of squares 0 and 1; square 0 outside the wall). Least wall clearance exactly 0 at all nine (closed-box contact); least pair gap 1e-32 (+5.6e-49) at all nine.
check --replay: all 27 jobs decided again, equal to their rows; 21:20:20Z to 22:14:01Z (53 min 41 s, serial, load 12 to 19). "9 certificates and 27 jobs admitted".
Checks: acquire_source --check PACKET_MATCHES_ITS_CONTRACT; derive --check matches the checkout; check-claims rebuilds; pytest test_upper_bound_reports.py + _488_489 + _regularized: 168 passed; test_upper_bound_reports_500.py: 5 passed; packing-validate --records: 49 steps passed, exit 0.
Not run: the source's own checkers (SQUISH's Fraction checker, Ellsworth's check_packing.py); the third exact route (check_half_angle_area, a separate review lane); no review. No shared record edited; register-plan output handed to the records lane.

Reopened: Reopened by the 2026-10-12 reconciliation (think-va12): packing/campaign/intake-watch.yaml still names this bead as the owner of its repository's read-through, and check_bead_tree requires a record that declares a deferral to name an open bead. The import itself is complete; close this bead in the change where the next intake pass updates that intake-watch entry.


2026-10-14 09:25Z: reopened. intake-watch.yaml on main still names think-ga3m as the open owner of the itsnaka read through 56fa71f, so closing it failed check_bead_tree on every branch (D-025). Close it when think-5pn5's watch read re-points that entry.

2026-10-14T09:30Z (squares-43, think-5pn5): claude/serene-hopper-xxh80m commit 31a817e8e re-points the itsnaka/squish-certs read through 56fa71f with no bead (aeacc6c pinned by squish-500-fourth-request-2026-10-11, T-151). Close this bead in the session that sees 31a817e8e reach main, not before: main's intake-watch.yaml names it until then.
