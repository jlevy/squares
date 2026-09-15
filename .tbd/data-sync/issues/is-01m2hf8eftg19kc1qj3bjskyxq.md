---
type: is
id: is-01m2hf8eftg19kc1qj3bjskyxq
title: "PR #155 review D29: 1e-5 tolerance recorded as measured from the snapped control; 'two orders of magnitude'"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40g8vbnq8914rkt7p87c
created_at: 2026-09-15T02:45:09.754Z
updated_at: 2026-09-15T03:09:09.849Z
closed_at: 2026-09-15T03:09:09.848Z
close_reason: "Fixed in 7200aa5b on #155: tolerance recorded as chosen in exp-207/208/210 and H-210; control reads none retained; ratios replace 'two orders of magnitude'. The 1.3e-5 harness comment goes with bench_annealing.py on #160 (D10); retained control stays with think-2ngs."
resolution: null
duplicate_of: null
---
Review: attic/reviews/pr155/review-pr155-d46b86a5.md (PR #155 review at d46b86a5). Parent: think-xqc3.

Source: #155 R5 (record items). Harness half (comments, gate documentation, sweeps stored) is D10 on #160; think-2ngs owns the retained snap control.

Files: exp-207 :21, exp-208 :21, exp-210 :22-23, :39, :118; H-210 :25-26, :39-40; X-034 :111-112, :120-121.

Fix: tolerance fields say chosen with the unretained observation named; ratios stated from the table.
