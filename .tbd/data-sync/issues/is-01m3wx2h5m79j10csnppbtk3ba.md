---
type: is
id: is-01m3wx2h5m79j10csnppbtk3ba
title: "Repair register fields the import review found wrong: three truncated significance.by values, and three entries whose claim and activity disagree"
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:56.531Z
updated_at: 2026-10-01T23:33:56.531Z
---
W9. results.yaml lines for T-056, T-057, T-061 read by: issue #227 intake ..., which YAML parses as the string issue because # starts a comment; quote them and add a check that refuses a by of one word. T-046, T-048 and T-055 say in claim or notes that the replay is unfinished while activity says it passed on 2026-09-29; rewrite them together when the stranded receipts land (think-20mv, think-nnlg, think-ifsv, think-0rrj).
