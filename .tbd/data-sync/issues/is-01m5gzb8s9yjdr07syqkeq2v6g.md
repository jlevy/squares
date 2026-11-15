---
type: is
id: is-01m5gzb8s9yjdr07syqkeq2v6g
title: "result/t-180.html page budget runway: 402,418 of 450,000 bytes at 138 register results on its 264 counts (~32 more)"
kind: task
status: open
priority: 3
version: 2
assignee: c-lane-pr-b
labels:
  - records
dependencies: []
parent_id: is-01m5gxvxvdf0hbxwdvb8p87g68
created_at: 2026-10-22T04:54:10.473Z
updated_at: 2026-11-15T05:45:38.007Z
---
Review B7 of #718. result/t-180.html (the closed form T-180, scope 264 counts) lists every register result on its counts; it measured 402,418 bytes on 22 October 2026 at 138 results, against the 450,000 exception in packing/devtools/site_urls.py (PAGE_BUDGET_EXCEPTIONS). At about 1.5 KB a listed result (the growth from 341,524 bytes measured before), the room is about 32 more results on those counts. Done when: the page is re-measured before it passes about 440,000 bytes (or about 165 listed results), with its timing, and either the list is lightened or the ceiling moves as a measured choice under OR-17. Owner of the runway sentence in site_urls.py's reason. blocked_on: none

## Notes

2026-11-15 bold-ritchie-l172 (senior review L171 of PR #991, note N11, no change asked): result/t-174.html is the tightest result page against its budget, 348,784 of 350,000 bytes (1,216 to spare), as lane L170 measured it on #991's tree with T-303 registered, adopted and stamped; result/t-180.html measured 502,787 of 525,000 on the same tree. T-174's 68 counts do not include 90, so #991 does not grow the t-174 page, and no budget or ceiling moved. At about 1.1 to 1.5 KB a listed result, t-174 has room for about one more result on its counts; its timing is owed with t-180's under this bead.
