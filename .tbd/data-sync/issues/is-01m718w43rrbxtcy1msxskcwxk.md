---
type: is
id: is-01m718w43rrbxtcy1msxskcwxk
title: "synopsis/the-program-at-a-glance.html page budget runway: 600,604 bytes on 9 November 2026 (hosted run 42715322236), ceiling raised to 650,000; every intake adds document-table rows"
kind: task
status: open
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-09T23:04:12.664Z
updated_at: 2026-11-20T19:55:12.029Z
---
Hosted CI on #940 (c1010b323, run 42715322236, overview job) measured synopsis/the-program-at-a-glance.html at 600,604 bytes against the default page budget of 600,000 once lane L76 added three document-table rows to SYNOPSIS.md (the #938 ledger README, the #938 review, the think-1goz regularization README). Lane L76 gave the page an exception of 650,000 in devtools/site_urls.py PAGE_BUDGET_EXCEPTIONS as a measured choice, room for roughly 200 more rows at about 200 bytes each, as L71 did for result/t-180.html (think-v4me). Decide how the page should scale: split the document table, page it, or keep raising the ceiling on measurement. Timing of the page was not re-measured.

## Notes

Baseline, from the senior review of #940 (L79, finding 8): main 200f2ebc1 measures the page at 599,314 bytes (hosted run 42692448089, overview job 129415798553), 686 under the 600,000 budget; #940's c1010b323 and ca33dcdbb measure 600,604 (runs 42715322236 and 42718843600). The delta is 1,290 bytes in four rows: the results table's T-284 row and the document table's three rows, about 320 bytes a row, not 200. So 650,000 leaves room for about 150 more such rows, or about 38 single-result intakes, not the 200 rows the first reason said. The results table counts as well as the document table. The reason in devtools/site_urls.py PAGE_BUDGET_EXCEPTIONS now states this (commit 442d5a019 on claude/bold-ritchie-xo28us-l76).

20 Nov 2026: main ee3a7fc7d measures 649,931 bytes (hosted run 44800220668), 69 under 650,000. PR 1054 (the s(18) review, one SYNOPSIS and one document-map row) measures 652,743 (run 44802841166) and fails the overview job: about 2.8 KB for one review. Branch claude/intake-2026-11-20-synopsis-budget raises the ceiling to 750,000 with this measurement in the reason. The page's growth rate is the open question this bead tracks.
