---
type: is
id: is-01m4zkm8r9pm5mkwhscg35vmfj
title: "J1: preserve checkpoint evidence across supported CI reruns"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m4zhkc4z66ywdsxw20sjcmg7
created_at: 2026-10-15T11:02:17.046Z
updated_at: 2026-10-15T11:02:17.046Z
---
Senior review J1: attempt-equal artifact consumption conflicts with rerun-starved.yml gh run rerun --failed. A producer that succeeded in attempt1 is not rerun when another prerequisite or aggregate reruns in attempt2, so the new aggregate seeks an artifact that cannot exist. Resolve the recovery protocol explicitly: either purposefully rerun the complete required run or verify exact successful producer-attempt provenance within the same run/source/base/tree without accepting failed/stale evidence. Weigh repeated runner cost against implementation cost; no silent stale-receipt fallback.
