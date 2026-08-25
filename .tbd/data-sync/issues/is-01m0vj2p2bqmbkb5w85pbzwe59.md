---
type: is
id: is-01m0vj2p2bqmbkb5w85pbzwe59
title: "PR #23 review R15: Respect CPU affinity and cgroup quotas in default jobs"
kind: bug
status: closed
priority: 3
version: 3
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
updated_at: 2026-08-25T04:44:40.086Z
started_at: 2026-08-25T04:16:15.537Z
closed_at: 2026-08-25T04:44:40.085Z
close_reason: "Completed in 69e65eb: validation and shared worker defaults use Python 3.14's process_cpu_count so container and affinity limits are respected."
resolution: null
duplicate_of: null
---
PR 23 review R15. File: explorations/packing/src/sqpack/cli/validate.py around line 847. Use Python 3.14 process_cpu_count for the default outer worker count.
