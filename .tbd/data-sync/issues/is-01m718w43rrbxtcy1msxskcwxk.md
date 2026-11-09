---
type: is
id: is-01m718w43rrbxtcy1msxskcwxk
title: "synopsis/the-program-at-a-glance.html page budget runway: 600,604 bytes on 9 November 2026 (hosted run 42715322236), ceiling raised to 650,000; every intake adds document-table rows"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-09T23:04:12.664Z
updated_at: 2026-11-09T23:04:12.664Z
---
Hosted CI on #940 (c1010b323, run 42715322236, overview job) measured synopsis/the-program-at-a-glance.html at 600,604 bytes against the default page budget of 600,000 once lane L76 added three document-table rows to SYNOPSIS.md (the #938 ledger README, the #938 review, the think-1goz regularization README). Lane L76 gave the page an exception of 650,000 in devtools/site_urls.py PAGE_BUDGET_EXCEPTIONS as a measured choice, room for roughly 200 more rows at about 200 bytes each, as L71 did for result/t-180.html (think-v4me). Decide how the page should scale: split the document table, page it, or keep raising the ceiling on measurement. Timing of the page was not re-measured.
