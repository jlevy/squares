---
type: is
id: is-01m0vwd9a6sb0a92f46srt46q7
title: Port PR 25 visualization toolkit onto the current packing architecture
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - pipeline-improvement
dependencies: []
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-25T07:16:00.450Z
updated_at: 2026-08-25T07:16:00.450Z
---
Retarget/rebase PR 25 from the merged workflow branch onto current main. Resolve content and location conflicts by placing reusable code under src/sqpack, case adapters under cases, tools under devtools, controls under tests, and validation under packing-validate. Also correct the stale dark-red n=11 caption. Do not partially land generated figures without replayable implementation.
