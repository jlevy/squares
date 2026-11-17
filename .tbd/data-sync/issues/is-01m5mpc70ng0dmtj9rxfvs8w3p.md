---
type: is
id: is-01m5mpc70ng0dmtj9rxfvs8w3p
title: "PR #753 (merge on 24 October UTC): T-231, T-229 lineage, reply records"
kind: task
status: closed
priority: 1
version: 7
delegate: c-land-753-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T15:34:21.973Z
updated_at: 2026-10-24T08:25:44.864Z
started_at: 2026-10-23T15:34:24.630Z
closed_at: 2026-10-24T08:25:44.863Z
close_reason: "PR #753 merged 2026-10-24T01:03:07Z (5f5294d82); deferral think-mboh stays open."
resolution: null
duplicate_of: null
---

## Notes

Review A of PR #753, a PR comment: https://github.com/jlevy/squares/pull/753#issuecomment-6369144929 (posted 16:02:33Z against 3685cb964; edited 16:04:54Z to re-pin to 028d53e5e, which the lane pushed at about 16:02:31Z).
Marker: <!-- tbd:review v=1 id=A kind=senior pr=753 round=1 head=028d53e5e85884586dc602cf7df85bc54be436ee base=c1115c0956104e40571d26de439c91917911d554 -->
Verdict at 028d53e5e: approve. Nothing blocks merge but the day: merge only on 24 October UTC (A4). At 3685cb964 the verdict was request changes, for A1 alone.
Findings:
- A1 High, fixed in 028d53e5e: docs/project/site-urls.md was not re-rendered after ba0cb64e2. site_urls --check failed at 3685cb964 and the validate job failed. It passes at 028d53e5e (1160 rows, 0 failures). Needs a disposition.
- A2 Medium: T-231's claim says T-229 was the house when it was claimed; at that time the house was T-225.
- A3 Medium: stale V0/C0 or T-229-house text at resources/README.md:587-588, source-coverage.yaml:7945-7955 and :7763-7764, and the #719 packet README:13.
- A4 Medium: only the draft state guards the merge day. The re-dating list misses validate.py:179, test_known_best_atlas.py:2188, test_translation_escape_screen.py:116 and release.py:2462.
- A5 to A9 Low: credit notes overstate what the author said of this file; the handle in the new card and the packet title; the 204 ceiling leaves room for about one more adoption; the ledger re-gather is undated; the S2 label and the #734 statement.
- Suggestions A10 to A12.
Tests: 132 targeted pytest passed. The record and release tools pass. My own exact checker and its controls agree with the receipts.
Dedicated reviews: none recommended.

2026-10-24 c-land-753-1023 (landing lane): merged main 64b316b6c (#751, #748, #746, #747, #761, #762) into #753 at 264990965, no rebase (release.py RELEASE_IMPACTS keeps the explainer's v0.4.22 above infographics v0.7.0; the document map keeps both new rows; INVENTORY/VERIFIERS re-rendered). 695a07431 records the stage 7 replies and closes of 23 October: #533's status reply (issuecomment-6370778184, follow-up), #470 closed with its final reply (issuecomment-6376106671; think-5ip2's patch applied cleanly), and the #557/#565/#570/#574 hold notes (the owner stated no preference on 23 October, so the holds stand; basis recorded-reservation). dde44d903 re-measured the papers' no-change record against 64b316b6c (three papers byte-identical; the explainer differs only in 231 and v0.4.22); e3e2513ca re-pinned. At 00:00Z on 24 October: every place in the re-dating list already names 24 October, so nothing re-dated; 527ba8761 stamp_landed --apply (T-231 landed 2026-10-23 -> 2026-10-24; landings.yaml is not on main); 29ad81911 re-pinned (527ba87617c4); check_release_impact passes. Records tier 53/53 at e3e2513ca and at 29ad81911. Hosted CI at 29ad81911: Packing validation 40042862448, Certificate page 40042862455, Branch mergeability 40042856551, all success. Not merged and still draft (the coordinator's). Deferral: think-mboh (check_requests' hold_text still prints "pending the owner's confirmation" for a recorded-reservation hold).
