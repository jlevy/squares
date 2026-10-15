---
type: is
id: is-01m4yd28hxb6m3ns2fbzws27ns
title: "Import Francisco Couzo: franciscouzo/square-packing 487b058 (no issue): s(211) 9.29e-6 below #586, and 296 certificates beyond 324"
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
child_order_hints:
  - is-01m4yst7ny3g52xgq8yr82r2az
hold: null
hold_until: null
created_at: 2026-10-14T23:48:21.180Z
updated_at: 2026-10-15T03:31:09.628Z
started_at: 2026-10-15T03:18:40.485Z
---
Found by the #607 lane (think-qik6) on 2026-10-14. franciscouzo/square-packing 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d (2026-10-14T17:45:39Z, 'Land verified bounds through n=1024'), the parent of #607's pin 43ac7d2, is a watched-repository publication that no issue reports and no packet retains. Against b85dee2 (the issue-586 packet's pin) it adds 290 certificates under certificates/ (370 and 403 to 991), changes 7 (211, 339, 378, 379, 380, 381, 382) and deletes 22, and writes upper_bounds.json, the index #607 compares against.

Inside the corpus: certificates/n211.cert at 487b058 states s(211) <= 7496774813149710519467765230441/5*10^29 = 14.99354962629942..., 9.29e-6 below #586's 14.993558913975 (the ledger's best now at 211). Under the per-count rule it is a report at its first commit (17:45:39Z) and would be recorded.

Beyond the corpus: at 16 counts (339, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804, 812, 930) #607 (43ac7d2, 19:15:09Z) reports a smaller side, so 487b058's row there is recorded and then followed by #607's; the header of each of those 17 files (with 342, unchanged since 02f9690) states exactly the index's bound (read by the #607 lane, not retained). The other counts are unread.

Next: triage the whole commit (stage 1), retain a packet at 487b058 (stage 2), compare in report order, price the replay; add a franciscouzo read to intake-watch.yaml in the records PR.

## Notes

## 2026-10-15 reads lane (think-mq0k): mapping at the head 58a7833

franciscouzo/square-packing is at 58a783368d4b7e70bb800f0009ea9ca03e578739 (2026-10-15T01:25:11Z): 487b058 (this bead), 43ac7d2 (#607, think-qik6), 4e4c8ce (00:31:53Z, the index for n < 1024) and 58a7833 (Göbel bounds). This bead's in-corpus claim is unchanged: certificates/n211.cert has the same blob c079cb6b at 487b058 and the head, and the head's certificates/best/n211.cert is the same bytes; side 7496774813149710519467765230441/5e29 = 14.99354962629942, 9.29e-6 below #586's dostashev-merged-bands pending side (the smallest earlier exact side here), 2.79e-3 below PR #574/T-149. First committed 2026-10-14T17:45:39Z. No packet retains it yet; a packet at 487b058 or at the head pins the same bytes.

4e4c8ce supersedes much of 487b058's beyond-horizon set: at 341 counts (325 to 1023) its index side is smaller than 487b058's verified lane and #607's, equal at 358 (333 grid). Triaged read-only as think-yfoo; deciding with this bead whether one beyond-horizon import at the head replaces a 487b058 packet is the next step (report order still dates each certificate by its first commit).

The eight commits 337078c..b85dee2 the sweep flags (a7067d7, eee88d3, 0fa0e0d, e9eb44b, 93570ef, 4596670, 06d8db2, b85dee2): every certificate they change is retained by the packets at 0fa0e0d (couzo-certificates-2026-10-12, #561), 4596670 (couzo-issue583-2026-10-13) or b85dee2 (couzo-certificates-2026-10-13, #586), or superseded within the day by those pins; the unretained paths are prose (README, reviews REVIEW_20261012*.md, SEARCH_TO_400.md), the #561 publication drafts e9eb44b added and 06d8db2 removed, search code (accept_candidates.py, Cargo, search_forever.py, notify.py), found/ logs, known_best.json and the decimal poses and drawings. Nothing to import; a read through b85dee2 records it.
