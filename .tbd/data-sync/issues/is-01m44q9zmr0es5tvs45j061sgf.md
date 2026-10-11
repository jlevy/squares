---
type: is
id: is-01m44q9zmr0es5tvs45j061sgf
title: "PR #333 A6 (Low): PowerShell-only replay commands."
kind: task
status: closed
priority: 2
version: 3
delegate: graph_gate
labels: []
dependencies: []
parent_id: is-01m44q9st2e0jh0h0cztp6hnv8
hold: null
hold_until: null
created_at: 2026-10-05T00:27:04.727Z
updated_at: 2026-10-05T02:29:01.002Z
started_at: 2026-10-05T00:54:30.340Z
closed_at: 2026-10-05T02:29:01.001Z
close_reason: Review A delivered in PR333/351/352; focused controls and source/pages gates pass; inherited parent merge conflict explicitly tracked by open think-q0z7, no active executor or reserved follow-up.
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/333#pullrequestreview-5408660716

**A6 (Low): PowerShell-only replay commands.**
- The replays in the 172 and 179 READMEs use `.venv/Scripts/python.exe` only.
- They don't say the committed cold receipt is required.

Authorized maintenance only. Disposition requires evidence and exact-head CI; no research follow-up reserved.
