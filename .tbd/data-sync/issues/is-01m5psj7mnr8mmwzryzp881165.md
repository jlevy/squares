---
type: is
id: is-01m5psj7mnr8mmwzryzp881165
title: "PR #791 (merge): senior review of the plan for rows above 1024"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-791-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T11:08:33.813Z
updated_at: 2026-10-24T11:27:30.426Z
started_at: 2026-10-24T11:08:40.258Z
closed_at: 2026-10-24T11:27:30.426Z
close_reason: "Review A posted https://github.com/jlevy/squares/pull/791#issuecomment-6383635522: approve after six Medium plan-text fixes (A1-A6), seven Low; Göbel recommendation verified independently; addressed by c-plan-1024-llit."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-791-1024: Review A (senior, round 1) of PR #791 published as a PR comment at head f64478c87 (base b2ea7b09c): https://github.com/jlevy/squares/pull/791#issuecomment-6383635522. Verdict: approve after the Medium findings are fixed in the plan text; no Blocker or High. Findings: 6 Medium (A1 W7 lifts #666/#719 windows that only a records slice can lift; A2 recipe parents not rows, e.g. 964ee2b's 850, which #789 does not replay; A3 #789's fifth walk, 20 releases and claim_map_walk_sources LIMIT site; A4 D4 missing; A5 no negative controls for the ceiling/frozen receipts and the walk above 1024; A6 gate target covers one test), 7 Low (A7-A13), 4 suggestions (A14-A17). Göbel recommendation holds: recomputed independently (104/1073; 186/6256, no strip above 1617, 1,573 wrong counts 1682-6116; 343 members, 0 disagreements 325-1073, final to 10,000; Daniel +0.1334 and +0.1696). Owner questions: D3/N4/N6 correctly rule-decided; D5, think-kzme, N1, N5 open and labelled as the coordinator's. Not synced (brief).
