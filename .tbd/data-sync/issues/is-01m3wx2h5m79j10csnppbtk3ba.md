---
type: is
id: is-01m3wx2h5m79j10csnppbtk3ba
title: "Repair register fields the import review found wrong: three truncated significance.by values, and three entries whose claim and activity disagree"
kind: bug
status: in_progress
priority: 2
version: 3
delegate: c-gates-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-10-01T23:33:56.531Z
updated_at: 2026-10-23T07:51:13.014Z
started_at: 2026-10-23T06:19:02.462Z
---
W9. results.yaml lines for T-056, T-057, T-061 read by: issue #227 intake ..., which YAML parses as the string issue because # starts a comment; quote them and add a check that refuses a by of one word. T-046, T-048 and T-055 say in claim or notes that the replay is unfinished while activity says it passed on 2026-09-29; rewrite them together when the stranded receipts land (think-20mv, think-nnlg, think-ifsv, think-0rrj).

## Notes

2026-10-23 c-gates-1023 (PR #748, branch claude/intake-2026-10-23-gates): check_results refuses a one-word significance.by (significance_by_problems), commit c584afff1, test test_a_significance_by_of_one_word_is_refused. The repairs this bead names were already on main: T-056, T-057 and T-061 rescored with full `by` values in e1a9ea9df (think-qh3s); T-048 and T-055 rewritten together and their activity removed in c03c6d4fb, T-046 in 928c30a1f (through T-045 and T-070), when the stranded receipts landed. The new check found T-115's bare review path (a79457130), now named as the repository's import triage. Related and not done here: think-mh6b's general guard against values a ' #' cuts short (results.yaml line 8040).
