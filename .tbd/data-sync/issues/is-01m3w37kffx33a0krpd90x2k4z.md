---
type: is
id: is-01m3w37kffx33a0krpd90x2k4z
title: "Homepage: 'Reported, awaiting replay' is not a separate ad hoc block; those results sit with the main results, each with its current status"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:02:19.756Z
updated_at: 2026-10-01T22:18:25.168Z
closed_at: 2026-10-01T22:18:25.167Z
close_reason: "jlevy/squares#277 merged (main 3cbbfd1c2): the 'Reported, awaiting replay' block is gone; its 48 rows were T-046 and T-048 written out case by case; unconfirmed results are rows of the one table with their status, and a derived sentence above the homepage table links them."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'I have previously asked about the block "Reported, awaiting replay" on the main page. It doesn't make sense for this to be separated the way it is. Can you assign an agent specifically to this and be sure we understand where it's coming from and why it's not just integrated in a sensible way, systematically with our main results? Reflect the current status of each of these results. It should not appear in this ad hoc way on the main page.' Trace where the block comes from (which code, which data, which commit and bead introduced it, what the earlier request was), what each listed item is today (registered result or only a case-record report; its rungs, standing, evidence, whether a replay has since happened), and why it is outside the results table. Then integrate: every such item is a row of the one results table with its real status (V0/C0 or 'reported' standing, a filter value), or is dropped from the homepage if it is not a result; no separate block.

## Notes

2026-10-01, branch claude/awaiting-replay, draft PR 277. Found: the block's 48 rows were two register entries, T-046 (47 cases) and T-048 (n = 50), both already rows of the results table; the block was a port of README's per-case table (8b4488561 think-ti71 -> 886d4b583 think-yy2c) under a table that lists results, and both entries are S3 so the homepage's S4 default hid them. Done: block, popovers, styles and .site-group-row removed; every result shows a derived status (recorded/reviewed/confirmed/incomplete) under its kind, superseded as its own mark; Status filter replaces Standing; a derived sentence above the homepage table counts the unconfirmed results and links them. Finding: complete replays of T-048, T-055 and 21 of T-046's 45 certificates passed on 2026-09-29 and sit on unmerged transfer branches (claude/replay-wand125-*); the three entries now carry activity: in-analysis. The n = 17 certified upper bound is registered as T-065 (credit and significance entered as drafts). Plan: docs/project/specs/active/plan-2026-10-01-result-status.md. Not done: integrating those replays (think-20mv, think-nnlg, think-ifsv, think-0rrj), think-wcex, the three catalogue intakes.
