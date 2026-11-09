---
type: is
id: is-01m6zhjx4dwahg13jmpa4c49j7
title: "Import #927-#931: Doğa Özden's five upper bounds, s(232), s(268), s(299), s(303), s(307) (kenaznia-doga, 9 November)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l63
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T06:57:58.922Z
updated_at: 2026-11-09T07:49:02.309Z
started_at: 2026-11-09T06:58:03.414Z
---
Five registration requests opened 2026-11-09T06:03Z by kenaznia-doga for Doğa Özden: #927 s(232) <= 15.761409644882 (repo kenaznia-doga/s232-upper-bound @ 09e324f4, sha256 22b3809e...), #928 s(268) <= 16.872469897837 (s268-upper-bound @ a40a15d9, 74c0e5d4...), #929 s(299) <= 17.801004434256 (s299-upper-bound-17801004 @ a042eab0, dfb0ccf7...), #930 s(303) <= 17.901789273157 (s303-upper-bound @ b43ca090, 9cbeb7a8...), #931 s(307) <= 17.979230960388 (s307-upper-bound @ dbe8838a, cb78adf8...). Witness/v2 files promoted with this repo's packing-witness promote --strategy robust-rational @ 19b354a5; LICENSE.md CC BY 4.0 / MIT. Precedent: #893/#894 (think-8b8m, packets ozden-s204/s299-upper-bound-2026-11-03, review-2026-11-04-ozden-893-894-299-204.md), #914 (seven at once). Stages 0-7 per packing/campaign/result-import.md.

## Notes

L63 (bold-ritchie-l63), 2026-11-09, branch claude/bold-ritchie-xo28us-l63 from main 19b354a5c.

Stage 1-2. All five repositories cloned at their pins; each holds one commit, 35 to 64 s before its issue. Every stated digest holds (YAML from the issues, JSON from the READMEs). Packets ozden-s{232,268,299,303,307}-upper-bound-2026-11-09 written by acquire_source: README, LICENSE.md, candidate YAML, JSON, both outputs retained; diff PNG pinned by digest; verifier/README.md pinned identical_to the 3 November s299 packet's copy; the new sqcheck.py (17,654 bytes, changed since 3 November) retained in the s232 packet and pinned identical_to it in the other four. JSON declared same_packing; the reader holds it equal to the YAML.

Claims (check-claims at main 19b354a5c): each issue's 12-place print is the exact side rounded up (admitted). Exact sides vs houses: 232 15.7614096448817244 below T-256 by 2.52e-4; 268 16.8724698978362125 below T-270 by 2.96e-5; 299 17.8010044342552937 below T-263 by 2.34e-4; 303 17.9017892731564904 below T-272 by 4.35e-5; 307 17.9792309603873628 below T-256 by 2.03e-5. Stated improvements all hold to 4 significant figures.

Replay: certify on both maintained routes, 15 jobs, 1,199,094 pair decisions, 479.4 route CPU-s; all positives accepted, all gross controls refused; walls touch exactly, least pair gap 2.01e-13 to 2.04e-13. Sharp controls: 55 of 55 as expected (232 239 s, 268 355 s, 299 324 s, 307 ~470 s, 303 ~420 s wall, one core each). acquire_source --check, retained_data check, check-claims, sharp-controls --check and check --replay pass per packet.

Identity (measure_identity vs house packet, regularized view, house witness): 232, 268, 303, 307 one to one with the house under the identity (6, 4, 5, 5 squares beyond 0.1); 299 not one to one by nearest centres against T-263 (12 beyond 0.1 under the identity assignment, one tilt reversed, largest 0.642). At 307 the regularized view is a corner witness the witness-corners adapter refuses for its schema path (../../../witnesses/witness.schema.yaml), so 307 is measured against T-256 and the house witness only.

Ledger upper-bounds-927-931-20261109: records all five, starts frozen at 19b354a5c.

Stage 3. T-275 (232), T-276 (268), T-277 (299), T-278 (303), T-279 (307), each with E-ozden-NNN-certificate-report and E-ozden-NNN-exact-feasibility (replayed-here, exact-algebraic, same-implementation as precedent F6), so check_results derives V3/C3 on the replay (as T-274 stood before its review was mapped). Draft S2 each (further arrangements). Bibliography keys [Özden sNNN upper bound 2026-11-09], lineage builds-on-project (the source starts from this repository's regularized atlas and makes its coordinates with this repository's promote), credits Ozden after <base holders>, Daniel (local optimizer), Levy. Requests entries #927-#931 (answer_bead think-463r, validation think-rd0p). Contributor census reconciled.

Adoption NOT done: the house rule's candidate needs an accepted review in the entry's reviews (select_houses.eligible), and check_results refuses a verified lane on a recent result by others without a mapped review. Adoption and both strong generators wait for think-rd0p's review to be mapped.

CPU so far: about 0.8 CPU-hours (certify ~8 min, sharp controls ~31 min, checks rerun ~35 min, identities ~3 min, tests ~5 min).
