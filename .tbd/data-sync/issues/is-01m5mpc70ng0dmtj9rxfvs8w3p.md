---
type: is
id: is-01m5mpc70ng0dmtj9rxfvs8w3p
title: "PR #753 (merge on 24 October UTC): T-231, T-229 lineage, reply records"
kind: task
status: in_progress
priority: 1
version: 4
delegate: c-rev-753-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T15:34:21.973Z
updated_at: 2026-10-23T16:05:11.087Z
started_at: 2026-10-23T15:34:24.630Z
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
