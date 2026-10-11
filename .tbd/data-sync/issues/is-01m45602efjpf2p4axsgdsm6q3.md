---
type: is
id: is-01m45602efjpf2p4axsgdsm6q3
title: Stage 4 review of T-093 (Guzhou0806 R071, s(17) > 18641771/4000000), and its replay if Boost can be installed
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T04:43:48.559Z
updated_at: 2026-10-05T08:22:37.052Z
started_at: 2026-10-05T04:45:51.255Z
closed_at: 2026-10-05T08:22:37.052Z
close_reason: "T-093 at V3/C3: R071 C027 paired replay passed, separate review clean, packet trimmed to digest pins; merged into #362 at ed80b1637"
resolution: null
duplicate_of: null
---

## Notes

Stage 4 exit for T-093 done on branch claude/ecstatic-pascal-pothtx-rev-guzhou (worktree /home/user/squares-lanes/rev-guzhou), not pushed. Replay of R071 C027 via run_public.js bound passed 2026-10-05 04:53:42Z-05:51:40Z (3,478 s wall, 3,238 CPU-s, 2 cores): PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION, 0 of 4x5,114 rows differ, all rows at 1000026844, surplus 7404; executable cf761bb5 (= R068's local build). Controls over-claim and drop-rule refused by both checkers. Review docs/project/reviews/review-2026-10-05-guzhou-r071.md (separate lane, blind): no defect, none blocking, S2 confirmed; its 227-row sample equals the fresh ledgers. Commits: 8b6870856 (packet trim 163 files/146,029 lines -> 55/6,920; replay driver), bc6fd6c4a (finding F: ledgers exit on theorem disagreement), 4afd672d6 (replay receipts, controls, tests, verifiers), 904a29f58 (exit: verified lower bound 18641771/4000000, T-093 V3/C3, T-043 superseded), e1d97da55 (release pin); merges of claude/ecstatic-pascal-pothtx at b0e6fbd83 and e38dd4014.
