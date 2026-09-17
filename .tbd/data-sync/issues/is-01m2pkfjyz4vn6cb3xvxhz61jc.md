---
type: is
id: is-01m2pkfjyz4vn6cb3xvxhz61jc
title: Freeze guided-search calibration and held-out cells headlessly
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m2pkfk9z36garp9891702grd
  - type: blocks
    target: is-01m229c25xgrtk9hh5nd1brnxn
  - type: blocks
    target: is-01m2p0xq9nac6ftmr19978krh3
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-17T02:35:10.174Z
updated_at: 2026-09-17T02:35:22.020Z
---
From think-rey9's per-record component counts, feature coverage and remaining degrees of freedom, and think-gdkd's registered eligibility rules, fix the calibration and held-out cells per guidance tier in the campaign manifest before any tuning, without waiting on the browser Search mode (review finding S6). Single-component cells are excluded from the partition contrast; oriented-face coverage today is n=11 and n=29 only. think-3yma's Search presets read this partition rather than define it.
