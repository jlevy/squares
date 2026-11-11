---
type: is
id: is-01m74fep2rzsgrq8ry7tty1bga
title: "Import #941, #942: Joost de Winter's 31 lowered upper bounds for n between 413 and 989"
kind: task
status: in_progress
priority: 2
version: 6
delegate: bold-ritchie-l90
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T04:56:55.639Z
updated_at: 2026-11-11T10:14:40.741Z
started_at: 2026-11-11T09:58:23.522Z
---
#941 (2026-11-10T13:30Z) fifteen lowered upper bounds n 413-910; #942 (14:41Z) sixteen n 632-989; JoostdeWinter. Beyond the atlas's 324, below the 1024 horizon: beyond-horizon rows. Precedent: Yim's 553-700 rows (PR #934). Starts after the Özden lane to stay within usage limits.

## Notes

2026-11-11 coordinator: JoostdeWinter/square-packing commits d3a020e, 71da0d5, a9486ed and a0c4fc8 (between the #939 pin 702c7af and the #946 pin c4e65d0, 9-10 November) add certificates at 37 new counts above 324 under above324/ and above324_refined/, with no issue of their own. Under the 14 October rule these are reports from their first commits. Triage them with #941/#942 (likely overlapping counts; compare report times and sides, keep each first report).

2026-11-11 L90 (bold-ritchie-l90), triage start. Branch claude/bold-ritchie-xo28us-l90 from main 8afdabe8f.
- Commits (UTC; push not read: the events API and the activity page both refuse this session, as for #934): d3a020e 2026-11-09T23:59:23Z adds above324/ with 9 certificates (413, 494, 539, 543, 547, 590, 809, 810, 867); 71da0d5 2026-11-10T06:15:17Z adds 6 more (738, 739, 753, 794, 851, 910) and touches no earlier certificate, so #941's 15 files at 71da0d5 are the blobs first committed there; a9486ed 14:39:52Z adds above324_refined/ with #942's 16 (1m26s before #942); a0c4fc8 15:37:44Z adds 597, 754, 864, 865, 869, 991.
- Surprise: a0c4fc8's six DO have a report: #942's addendum comment issuecomment-6772308414 at 2026-11-10T16:02:47Z claims all six at a0c4fc8. Following #763's practice (an issue's claims carry first_committed for certificates committed earlier), the comment is the report and a0c4fc8 its first commit; same verdicts either way unless something else reached those counts in 15:37-16:02Z (nothing found: no other issue in #939-#947 above 324).
- d3a020e's role: first publication of 9 of #941's certificates, 13.5 h before #941; no other report reached those counts in between (issues #943-#947 are below 324). Ledger: #941 claims carry first_committed d3a020e / 71da0d5.
- All 37 counts lie in 413..991: no count above 1024, nothing held for think-f2io.

2026-11-11 L90 retain + price (10:40Z).
- Packets written by devtools.acquire_source and PACKET_MATCHES_ITS_CONTRACT: de-winter-issue941-2026-11-10 at 71da0d5 (above324/, 15 certificates; 19 retained, 7 pinned), de-winter-issue942-2026-11-10 at a9486ed (above324_refined/, 16; 19 retained, 2 pinned), de-winter-a0c4fc8-2026-11-10 at a0c4fc8 (the six; 9 retained, 18 pinned, the 16 earlier certificates against the #942 packet's copies). The author's SHA256SUMS pass 16/16, 17/17 and 23/23. check-claims --write: all 37 exact sides round up to the 10-place prints; every one is below its standing row (smallest gain 7.08e-5 at 539, largest 3.26e-2 at 991) and below Göbel's construction; 655 has no row (grid 26).
- Price, measured: one positive job at 989 took 190 CPU s on both routes (all 488,566 pairs, O(n^2)). Scaled by (n/989)^2 over the 37 counts: certify (positive + 2 gross controls) <= 3.6 CPU-h, sharp controls (11 decisions a count) ~13.2 CPU-h, contraction margins --no-routes ~4 CPU s a count. About 17 CPU-h in all, under the 40 CPU-h cap; 2 workers at nice -n 19, so about 9 h wall.

Controls stated in advance (before any run):
- certify, each count on both routes: the certificate accepted; duplicate-square (square 2 a copy of square 1) refused; outside-container (a square moved the side and 2 outside) refused.
- sharp-controls, each count on both routes (devtools.upper_bound_sharp_controls): side lowered to the extent accepted at contact with margin exactly 0 and refused 1e-30 past it; the tightest pair closed to contact accepted (margin 0), 1e-30 past refused; every square moved toward the near wall by the least near-wall clearance accepted at contact, refused 1e-30 past; one square of the tightest pair enlarged to contact refused for its shape alone with margin 0, past contact also for the overlap; the square nearest a wall enlarged to its wall likewise; the duplicated square refused. 11 controls a count, 407 in all, each as the module predicts.
- contraction_margin, each count whose row holds a retained certificate (or the base of a recipe row): the margin of the row's certificate, uniform contraction to first contact, and this certificate's gain over it; --no-routes, since the margin is exact without them and the routes would only prove the contracted packing as a bound of its own (OR-14 economy; ~2.4 CPU-h saved).
