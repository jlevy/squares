---
type: is
id: is-01m5mn0bde1tg8dr676kbbns6t
title: "PR #748 (merge): senior review, address, gate"
kind: task
status: in_progress
priority: 1
version: 4
delegate: c-rev-748-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5mpx469084wmghw63k1vasv
hold: null
hold_until: null
created_at: 2026-10-23T15:10:24.686Z
updated_at: 2026-10-23T15:43:36.136Z
started_at: 2026-10-23T15:10:25.857Z
---

## Notes

Review A (senior, round 1) of PR #748 posted by c-rev-748-1023 as a PR comment:
https://github.com/jlevy/squares/pull/748#issuecomment-6368647934
Marker: <!-- tbd:review v=1 id=A kind=senior pr=748 round=1 head=417ba331bc249a3381253551b9bdf76a4715e182 base=c1115c0956104e40571d26de439c91917911d554 -->
Verdict: approve. Nothing in this branch blocks merge, but A1 must be settled by whichever of #748/#752 lands second.
Findings: A1 Medium; A2-A6 Low; A7-A9 suggestions. No Blocker or High.
A1: #752 at ad0d4ea1f adds [wand125 sqverify continuous 2026-10-12] (cited by T-145, T-157) with no coverage source.
Merged with #748, register_source_errors refuses it. The other six open intake heads (#745, #747, #750, #751, #753, #754) trip nothing.
Fix: add a coverage source for the key. The wand125/square-packing card already exists.
No dedicated review is warranted.
