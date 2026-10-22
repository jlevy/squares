---
type: is
id: is-01m5gzb8s9yjdr07syqkeq2v6g
title: "result/t-180.html page budget runway: 402,418 of 450,000 bytes at 138 register results on its 264 counts (~32 more)"
kind: task
status: open
priority: 3
version: 1
assignee: c-lane-pr-b
labels:
  - records
dependencies: []
parent_id: is-01m5gxvxvdf0hbxwdvb8p87g68
created_at: 2026-10-22T04:54:10.473Z
updated_at: 2026-10-22T04:54:10.473Z
---
Review B7 of #718. result/t-180.html (the closed form T-180, scope 264 counts) lists every register result on its counts; it measured 402,418 bytes on 22 October 2026 at 138 results, against the 450,000 exception in packing/devtools/site_urls.py (PAGE_BUDGET_EXCEPTIONS). At about 1.5 KB a listed result (the growth from 341,524 bytes measured before), the room is about 32 more results on those counts. Done when: the page is re-measured before it passes about 440,000 bytes (or about 165 listed results), with its timing, and either the list is lightened or the ceiling moves as a measured choice under OR-17. Owner of the runway sentence in site_urls.py's reason. blocked_on: none
