---
type: is
id: is-01m5dz0nzsgm7vbzwbf7q2x9bh
title: "Import Evan Daniel: s(343) <= 18.977682482405 (#702)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-lane-702-import
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T00:50:40.249Z
updated_at: 2026-10-21T07:35:33.773Z
started_at: 2026-10-21T05:27:59.180Z
---
Stage 1 triage of jlevy/squares#702 (Evan Daniel, opened 2026-10-20T22:09:31Z), read-only, 21 October 2026, lane c-lane-records-1021. Nothing retained, imported or replayed.

## Source pin
- evand/square-packing at 88385abc95ab25d520302282d1946cbb07bc9cf3 (committed 2026-10-20T21:47:03Z, parent a435c970774403bf5c6f94815997b1cfd77dcf44), the repository's head when read on 21 October 2026. The issue links it as 88385ab.
- search/packer/candidates/s343_sw.cert SHA-256 18415455772cb1b9cdfd3b7384695ea202fb6a02291e2ede2db777e93d207dfa and s343_sw_regularized.cert SHA-256 f9a147750b51bfb3d24fa5469e93aeab903bad472f8d294b15250f2c3473e2b8, fetched at the pin into scratch: both equal the issue's digests.
- Header side 18977682482404124568634475670459/10^30 = 18.977682482404124568634475670459; rounded up at 12 places it is 18.977682482405, the issue's print.

## Claims the release makes
The commit adds 17 files: nine s343_sw* files and eight s270_sw* files.
1. s(343) <= 18.977682482405 (this issue): certificate, 80-digit KKT point, binary64 input, solver report, pre-descent point, regularized view at the same side, prior-record file and comparison.
2. s(270) <= 16.928162252197: the same commit, reported separately as jlevy/squares#703 (not in the record yet; its own import, not this bead's).
3. Numerical KKT, local-minimum (strict modulo 82 flat motions) and MILP statements at 80 digits: source evidence, not registered.
4. Credit: Evan Daniel as finder; Kevin Fang's two-wedge family (#484) credited as the construction, as in #489; called a different local minimum from Couzo's #678, found by a population search over stored near-record 343 packings from the 10 October Hunt 3. s343_sw_regularized.json says "by": ["Evan Daniel"]; s343_sw_prior.json names "pending:#678 (Francisco Couzo)" and the watched franciscouzo/square-packing@7b6c87e.

## Map to the record
- 343 is beyond the n <= 324 case corpus: a dated beyond-horizon row in source-coverage.yaml from a new packet, not a register entry.
- main (4851d8193) holds the current row at 343: evand-record-hunt3-2026-10-10, 18.978232523635611279730512106023, verified (Daniel, #489). #702 is below it by 5.500412e-4, exactly.
- PR #701 (merged 2026-10-21 at e7de85ff6) superseded that row with couzo-issue678-2026-10-18 at 18.978232204823, reported. #702 is below that print by 5.497224e-4, decided below whatever the print rounds.
- Report order: #678 (Couzo) before #702, each below the last, so the owner's rule of 2026-10-14 records both; the import runs the ledger (stage 1, Several Reports at One Count); #701 has merged, so nothing blocks it.

## Validation price
- Retain at the pin with devtools.acquire_source (stage 2), then replay on the maintained two-route kernel (devtools.evand_arrangement_reports: sqpack.verify and devtools.check_rational_witness_independent), a positive, a duplicate-square control and an outside-container control, as #489's 343 row was (15 native jobs over five counts). Estimate from #689's receipt at 308 (3 jobs, 35.66 route CPU seconds, 283,668 pair decisions) scaled by (343/308)^2: about 45 route CPU seconds. Minutes, so it runs in the import without a cap.
- No mathematical review is owed for a beyond-horizon row by itself; the import says so if it registers anything in corpus.
- The source's verify_cert.py and verify_cert2.py are not needed for the row.


## Draft acknowledgement (posts after the PR carrying this triage merges)
@evand, thank you for the report. We have read `s343_sw.cert` and its regularized view at `88385ab` (full id 88385abc95ab25d520302282d1946cbb07bc9cf3); both digests match the ones your issue prints, and the certificate's header side, 18977682482404124568634475670459/10^30, rounds up at 12 places to your 18.977682482405. 343 is beyond this record's n <= 324 case corpus, so the result will be recorded as a dated beyond-horizon row, as your #489 343 was, once the packet is retained and the certificate replayed on this repository's two exact routes with its controls. It is 5.50e-4 below #489's row on main and below Couzo's #678 print, which an open pull request records; both are recorded in report order. The same commit's s(270) certificate is #703's, and is answered there.

## Notes

## Import progress, 21 October 2026 (lane c-lane-702-import)

Stages 2 and 3 are on draft PR #712 (https://github.com/jlevy/squares/pull/712), branch claude/intake-2026-10-21-evand-343, from main d640ad8fb, merged with main 9dda92240 (#710); head f46c0b7f3.

- Custody: packet packing/resources/web/evand-n343-sweep-2026-10-20 at 88385ab via devtools.acquire_source (22 files pinned, 15 retained, 382,667 bytes; s343_sw_vs_prior.json stored gzip). Both certificate digests equal the issue's and this bead's (18415455..., f9a14775...). The s270_sw files are not retained here (#703's packet). Checkers, exactsolve.py and explore.py pinned identical to the n183 packet; PACKER.md, dgen.py, descend.py by digest only. acquire_source --check passes.
- Replay: upper_bound_reports certify --workers 2: positive accepted, duplicate-square and outside-container controls refused on both routes (sqpack.verify, check_rational_witness_independent); 3 jobs, 351,918 pair decisions, 51.74 route CPU s (estimate 45), 37 s wall; walls >= 5.00e-21, pairs >= 9.99e-21. check --replay decides it again (53 s). Receipt: receipts/exact-certification.json.xz.
- Record: source evand-n343-sweep-2026-10-20 and its beyond-horizon row at 343, 18.977682482405, assurance reported, after couzo-issue678-2026-10-18's row, now superseded by it (5.497224e-4 below its print, 5.500412e-4 below #489's exact side, 1.722105e-2 below #484's). Evidence E-evand-702-n343-report (register-plan). Bibliography [Daniel n343 sweep 2026-10-20], Daniel after Fang, Arslanov, Mustafin, Shangitbayev, Levy (finder Daniel, construction Fang #484). No corpus result registered; KKT/local-min/MILP not recorded. result-requests #702: not_registered (the row), queued false, credit ask done.
- Release: after merging main 9dda92240 (#710's v0.8.11), re-pinned (DATA_REVISION 58f12aaa), survey no-public-change record re-rendered (42 files byte-identical against main 9dda9224), explainer claim-document record, site re-cut as v0.8.12 (PUBLICATION_REVISION 107e1ca4). #711 also cuts v0.8.12 and lands first, so #712 merges main and re-cuts after it. stamp_landed: nothing to stamp.
- Snapshot: head f46c0b7f3 232,773,217 vs cap 232,783,872 (10,655 under); delta +17,031 over main 9dda92240 (232,756,186). #711 reportedly leaves 4,318 under, so #712 would be about 12,713 over: it waits on the owner's cap decision (no cap value proposed).
- Validation: --records 52/52 at f46c0b7f3. --push 66/67 at f46c0b7f3; reachable tests (326 files) hit the 900 s ceiling on the shared host. Run alone at 341eb16e7: 11,696 passed, 3 failed (stale DATA_REVISION, fixed by the re-pin; two fixed_core_packet process-group tests, which also fail from main's checkout on this host). Hosted at f46c0b7f3: 31 pass, 28 skipped, 0 fail.
- Stage 7: final reply drafted at the coordinator's scratchpad replies-new/702.draft.md (DATE to fill at merge); nothing posted.
