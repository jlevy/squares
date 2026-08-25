---
type: is
id: is-01m0vj2p2bqmbkb5w85pbzwe59
title: "PR #23 review R15: Respect CPU affinity and cgroup quotas in default jobs"
kind: bug
status: in_progress
priority: 3
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:27.306Z
updated_at: 2026-08-25T04:16:15.537Z
started_at: 2026-08-25T04:16:15.537Z
---
PR 23 review R15. File: explorations/packing/src/sqpack/cli/validate.py around line 847. Use Python 3.14 process_cpu_count for the default outer worker count.
