---
type: is
id: is-01m4846sy9cn7qh1qbpgfwn96w
title: "Sessions 171-172 records: call same-implementation replays fresh, not independent (#355 Review B B4 residual)"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-06T08:10:15.368Z
updated_at: 2026-10-07T06:23:10.673Z
closed_at: 2026-10-06T17:34:00.145Z
close_reason: "Merged in jlevy/squares#384 (stack #386) on 2026-10-06."
resolution: null
duplicate_of: null
---
Residual of Review B finding B4 on jlevy/squares#355 (https://github.com/jlevy/squares/pull/355#pullrequestreview-5411026555), which merged in stack 357 (main a6279886b).

Addressed on main: commit 1d02a11e2 fixed the cited sites (X048-session-172-capacity-support/README.md:3 now reads "freshly replayed (same implementation, no search)"; the Session 170-172 READMEs and D1/D2 reports define "fresh replay" and explain the receipt names).

Outstanding: the AgentSession records were not touched and still call the same-implementation replays independent. At origin/main eb43ffe9a:
- packing/campaign/agent-sessions/session-171-raw-row-support.md: lines 18, 42, 48, 64, 80, 118, 136, 141, 152, 186, 188, 196, 203, 254 (for example "57 complete selections independently replayed", "Independent fresh replay passed 735 pair checks", "B 55/96 rows independently replayed").
- packing/campaign/agent-sessions/session-172-capacity-support.md: lines 17, 51, 120, 155 (for example goal "Complete independently replayed support for all 96 rows", stop_reason "All 96 rows independently supported").

Rule: in this repository's evidential vocabulary (conventions.md, the independence section around lines 324-344) "independent" means a separate implementation. A fresh, search-free re-run of the same predicate code in a separate process is a "fresh replay (same implementation, no search)". Keep "independent" where it names a separate reviewer or role ("root independent review", "independent reviewer"); change it only where it describes the replay, support, check or acceptance evidence. Receipt file names (*-independent-replay.json) keep their historical spelling, as the READMEs already say. After editing, re-render the generated records (close_session --render, packing-ledger render) and run `packing-validate --records` from packing/. Low severity, wording only; no verdict changes.

Done when: grep -n -i independ over the two files returns only reviewer or role uses, and the records tier passes.

## Notes

2026-10-06: addressed on jlevy/squares#384 (claude/n17-session-certification, 7c4f758f5 and 6f635886d); closes when #384 merges.
