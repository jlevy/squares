---
type: is
id: is-01m4qjdm5hbj0m43ymvkcjr2jm
title: "Import Rio Calle: s(102) <= 10.605828696455852 (#529)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:07:15.376Z
updated_at: 2026-10-12T08:30:13.576Z
started_at: 2026-10-12T08:07:43.538Z
---
https://github.com/jlevy/squares/issues/529 (2026-10-12T04:32:54Z). riocalle/my-repo at 831368623f2d4dcef2e9434fd85c3e154083c97d: n102_s10.605828696455852.txt (decimal centres and radian angles), JSON and SVG copies, verify_exact.py (60-digit decimal, not exact). The author's exact certificate comes from a private engine; the record's exact certificate must be built here from the layout. Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports.

## Notes

Issue: https://github.com/jlevy/squares/issues/529 (opened 2026-10-12T04:32:54Z by riocalle, label intake). New contributor.

## Stage 1 triage, 2026-10-12 lane U (branch intake-528-529 from l4 dead83f0e; not pushed)

Pin: riocalle/my-repo 831368623f2d4dcef2e9434fd85c3e154083c97d (tree 4895d7e9), its only commit, committed 2026-10-12T04:23:19Z (authored 04:18:55Z), the head when cloned at 2026-10-12T08:03Z and the commit the issue names. No licence file and no reuse terms: derived-only custody. The JSON and SVG copies state the same 102 binary64 triples as the .txt, in the same order (measured in scratch).

Claims the release makes, and their register map:
1. s(102) <= 10.605828696455852 from n102_s10.605828696455852.txt (centres in [0, s]^2, rotations in radians, 18 significant digits). A bound the record already beats: T-146 (Evan Daniel's regularization of ry-xu's packing, 10.6058286964315784) is 2.43e-11 below it, registered on main since 10 October (V3/C3), the case's house on layer 4 (#518) and pending adoption on main. Below T-125 (main's house, 10.6058286965106059) by 5.48e-11, as the issue says. Whether to register a certificate of a distinct arrangement that moves no case is a records-lane/owner decision; the register plan is prepared either way.
2. "Solved to the bottom of its valley ... s = 10.605828696431638" (README): an author report with no layout at that side; not certified here and not registerable. It is 6.0e-14 above T-146's side.
3. earlier/n102_s10.605828708.*: the previous layout (Davidebyzero/packing_squares_in_squares__tools#6, opened 2026-10-08T17:34:14Z, confirmed by the API). Above every ceiling; stays in the packet.
4. Lineage: same design as ry-xu's T-125; 40 of 102 squares coincide with ry-xu's turned 180 degrees, 62 moved, 7 by up to half a square; found independently ~10 h after ry-xu's 2026-10-08 00:03 UTC publication. Priority is ry-xu's, as the author says. To be measured with the third route's arrangement_gap/patch_lineage.
5. A private engine's exact rational-interval certificate: not public, cannot be replayed.
6. AI assistance: Claude wrote and ran the search, finishing, refinement and both checkers, under the author's direction.
7. T-120 (#419) is Evan Daniel's degree-8 algebraic side, 10.607174680176051125342523..., of Francisco Couzo's 26 September configuration, a different design (T-098 holds its rational ceiling 10.60717468017605112545...). #529 is 1.346e-3 below it; it says nothing about #529's arrangement, whose exact algebraic side nobody has computed.

Credit name: "Rio Calle", as asked. GitHub profile riocalle: name Rio Calle, bio names the University of New Hampshire; twitter_username is null and the listed social accounts are LinkedIn and Instagram only, so no Twitter/X handle found.

Validation plan (priced): the author's checker verify_exact.py was read (json, sys, decimal only; reads its argument, writes nothing) and run once from scratch on the .txt and once on the JSON: both print min wall clearance 2.002e-12, min pair gap 1.932e-12 over 931 close pairs, LEGAL. It rounds at 60 digits, so it is a diagnostic. The record's certificate is derived here by a new calle-txt adapter (every decimal exact as printed, side as printed, tan(theta/2) rounded down at 40 places by a decided interval enclosure) and decided on both maintained exact routes with controls, --workers 1: 3 jobs, priced by a scratch prototype at 35 s for the positive. Third route: needs an upstream reader for calle-txt (proposed to the records layer). W2 review.

## Draft acknowledgement (not posted)

Thank you, Rio, and welcome. We received the layout at riocalle/my-repo 8313686 (n102_s10.605828696455852.txt, with its JSON and SVG copies). Since your engine's exact certificate is not public, we will build an exact certificate from the layout itself, every number exactly as printed and each square's half-angle tangent rounded to 40 places, and decide it on our exact routes with controls; we ran your verify_exact.py too, which reproduces your two gaps. We will also measure the packing against ry-xu's for the credit, which we will give as Rio Calle with ry-xu credited for the design and width, as you ask. One thing you should know first: since 10 October the record also holds Evan Daniel's exact regularization of ry-xu's packing at 10.6058286964315784, about 2.4e-11 below your side, so the comparison will name it.
