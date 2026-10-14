---
type: is
id: is-01m4yd28hxb6m3ns2fbzws27ns
title: "Import Francisco Couzo: franciscouzo/square-packing 487b058 (no issue): s(211) 9.29e-6 below #586, and 296 certificates beyond 324"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-14T23:48:21.180Z
updated_at: 2026-10-14T23:48:21.180Z
---
Found by the #607 lane (think-qik6) on 2026-10-14. franciscouzo/square-packing 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d (2026-10-14T17:45:39Z, 'Land verified bounds through n=1024'), the parent of #607's pin 43ac7d2, is a watched-repository publication that no issue reports and no packet retains. Against b85dee2 (the issue-586 packet's pin) it adds 290 certificates under certificates/ (370 and 403 to 991), changes 7 (211, 339, 378, 379, 380, 381, 382) and deletes 22, and writes upper_bounds.json, the index #607 compares against.

Inside the corpus: certificates/n211.cert at 487b058 states s(211) <= 7496774813149710519467765230441/5*10^29 = 14.99354962629942..., 9.29e-6 below #586's 14.993558913975 (the ledger's best now at 211). Under the per-count rule it is a report at its first commit (17:45:39Z) and would be recorded.

Beyond the corpus: at 16 counts (339, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804, 812, 930) #607 (43ac7d2, 19:15:09Z) reports a smaller side, so 487b058's row there is recorded and then followed by #607's; the header of each of those 17 files (with 342, unchanged since 02f9690) states exactly the index's bound (read by the #607 lane, not retained). The other counts are unread.

Next: triage the whole commit (stage 1), retain a packet at 487b058 (stage 2), compare in report order, price the replay; add a franciscouzo read to intake-watch.yaml in the records PR.
