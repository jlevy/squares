---
type: is
id: is-01m45189mq6av7xe334we2vtyr
title: "Import wand125: valid7 checker fix of D-1 to D-3 at da469ec, an evidence update to T-064 (no issue)"
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T03:20:55.191Z
updated_at: 2026-10-05T07:19:54.069Z
started_at: 2026-10-05T04:23:01.955Z
closed_at: 2026-10-05T07:19:54.068Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Found by the intake sweep of 2026-10-05 (think-nkzt). wand125/valid7-independent-check moved from 38dd31b369991b0d96c917a4af0c7139b44a038d, which the wand125-valid7-independent-check-2026-10-02 packet pins, to da469ecff5da0c71882e894b65d680ce57a0c87e (2026-10-03T23:14:42Z, Hiroaki Hosono): "Fix the three points raised in evand/square-packing#1 (no change to any certified result)". It changes src/check_record.py, src/cover.py, src/rf.py and src/tier_b2.py (60 lines added, 20 removed). Nothing on jlevy/squares asked for it. It answers evand/square-packing#1, closed 2026-10-03, whose points are this record's review findings.

## Claim map (stage 1)

1. tier_b2.nonneg_open now tests the sign at an interior point that is not a root of p, and requires p(s) > 0. The unused rf.nonneg_on uses the same test. -(x - 1/2)^2 on (0, 1) and -x^2 (x - 1)^2 on [0, 1] are now refused. This fixes D-1 and D-2 of docs/project/reviews/review-2026-10-02-valid7-independent-checker.md. Register action: an evidence update, no new entry.
2. Line de-duplication and the edge-value cache in tier_b2 are keyed by the exact canonical text of the rational functions, not by Python's hash. This fixes D-3. Register action: an evidence update.
3. check_record.py --seed S chooses the --recheck and --recheck-b leaves. The default is a fresh random seed, printed. This follows Daniel's note on evand/square-packing#1. Register action: an evidence update.
4. With the fixed code, the published records-v1 still give RECORD OK (156,800 roots; 2,000 + 300 leaves re-certified with seed 6107336003611786136), and the three mutants are still refused. The records were not regenerated: they are still the runs of the pre-fix V1 and V2 code. Register action: an evidence update; no rung moves.

Who else holds it: T-064 is V3/C3 on two routes. One is the qx2_zm.py replay (E-k2m3-evand-valid7-qx2-replay). The other is this repository's full replay of the pre-fix V2 code with D-1 guarded (E-k2m3-wand125-valid7-independent, 2 and 3 October), which matched the published records and refused nothing. Nothing here changes T-064's claim or rung.

## Stages 2 and 3, and the price

- Retain the repository at da469ec as a new packet, wand125-valid7-independent-check-2026-10-04, with devtools.acquire_source. Its release records are the same records-v1 assets, pinned by digest.
- Add da469ec to V-wand125-valid7-checker's versions.
- In E-k2m3-wand125-valid7-independent's limitations, and at D-1 to D-3 of the 2 October review, say that the author fixed them upstream at da469ec and that the guarded replay of 2 and 3 October stands.
- No T-NNN.
- Replaying verify.sh at da469ec on the retained records costs minutes. The 2 October run took 623 s of wall time and 451 CPU-s on 4 cores.
- When the packet pins da469ec, remove its read in packing/campaign/intake-watch.yaml.

## Notes

2026-10-05 lane stage4, branch claude/ecstatic-pascal-pothtx-stage4 (not pushed), commit 70764a031: packet wand125-valid7-independent-check-2026-10-03 (named for the pin's UTC date 2026-10-03T23:14:42Z, not 10-04) at da469ec by acquire_source (--check PACKET_MATCHES_ITS_CONTRACT); release records-v1 re-downloaded 04:23Z, digests OK, records.sha256 identical. verify.sh replay on retained bytes (CPython 3.14.7, flint 0.9.0): RECORD OK, seed 2431791605250748986, mutants refused, exit 0, 427 s wall / 408 CPU-s (receipts/valid7_verify.log). New devtools.probe_valid7_fixes (V-probe-valid7-fixes, premises): D-1/D-2 examples accepted at 38dd31b, refused at da469ec; hash( gone; controls accepted (receipts/valid7_fix_probe.json, tests/test_probe_valid7_fixes.py). Records: bibliography [wand125 valid7 independent check 2026-10-03] + coverage entry; V-wand125-valid7-checker versions += da469ec; evidence update on E-k2m3-wand125-valid7-independent; dated updates at D-1..D-3 in the 2 Oct review; T-064 notes/artifacts/controls; intake-watch read removed. No rung change. Note: da469ec also adds check_record.py --claim tilt (ValidTilt9 domain), not in the claim map.
