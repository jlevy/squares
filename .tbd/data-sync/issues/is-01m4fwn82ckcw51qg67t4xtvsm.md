---
type: is
id: is-01m4fwn82ckcw51qg67t4xtvsm
title: W3 insight-iteration review of the n17 program after consolidation
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
child_order_hints:
  - is-01m4g7ns8nzs2jxvbhzspratsa
hold: null
hold_until: null
created_at: 2026-10-09T08:32:15.435Z
updated_at: 2026-10-09T11:44:47.380Z
started_at: 2026-10-09T09:29:40.803Z
---
Delegate to a Fable sub-agent at max effort once the merge set is stabilized: comprehensive review of everything done so far on n=17 and the most productive directions toward a foolproof proof or the greatest mathematical progress. Output: X-NNN report and candidate H-NNN items with mechanism, falsifier, expected information and limits, landed via PR from claude/modest-pascal-z3nisd.

## Notes

2026-10-09T09:29Z Launched Fable max sub-agent (W3) after stack 455 landed at main 533dd42. Worktree scratchpad/wt-w3, local branch w3/n17-program-review. Reserved identifiers: X-051, H-325..H-340. Output to be published via PR from claude/modest-pascal-z3nisd.



2026-10-09T10:11Z W3 done by Fable max agent (40.3 min, ~747k tokens, 154 tool calls). Published as PR https://github.com/jlevy/squares/pull/473 (branch claude/modest-pascal-z3nisd, head 0b4fa16d2): X-051 + H-325..H-340 + ideas/SYNOPSIS/ledger. Headline: sect 3.1 centre-only relaxations globally blind (20 unit-separated centres fit at U); sect 3.2 weighted-vertex screen cannot exclude any of 2,024 cell triples; top-3 = endpoint-state cap scan (H-325/H-330/H-326), capture via exact LP over feature-forced region (H-329/H-339/H-340, kill-test H-337), hard-tail throughput (H-331/H-327/H-332/H-338). W2 factual review A dispatched.



2026-10-09T10:55Z W2 factual review A https://github.com/jlevy/squares/pull/473#pullrequestreview-5469083247: sect 3.2 confirmed exactly and strengthened (each triple's product vertex is FEASIBLE: no SOS certificate for any cell triple at any order, ball or not). sect 3.1 premise wrong (B1: LP keeps assigned cells) but conclusion proved directly: all 8 first-eight states have exact unit-separated centres in their own cells accepted by build_model+check_primal (752-811 rows); all 95 distance-2 orbits admit unit-separated centres (min d^2 >= 1.00396). So first-eight LP outcome known: 8 relaxation survivors. Non-blocking numeric fixes listed. Corrections being applied on #473.
