---
type: is
id: is-01m3rb0sr8p2xn3m96v3cs96cx
title: Decouple rectangle diagnostics and partition the PR review surface
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3rb0t4zqdze43drjkx9cqx2
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T05:01:27.687Z
updated_at: 2026-10-06T08:34:30.297Z
closed_at: 2026-10-06T08:34:30.297Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Admission extraction done by think-nxd8 (PR #250 MERGED, shared strict pending-inventory admission); the PR-split question is moot since PR #246 MERGED whole with preserved history (think-pd17)
resolution: null
duplicate_of: null
---
Extract strict frontier receipt admission so comparison and refinement do not import each other's CLI; preserve native rectangle acceptance as separate from n11 proof modules. Partition review into proof logic, evidence intake, rectangle tools, and CI/efficiency ownership. Decide actual PR split from dependency map with no force-push or history rewrite in planning; preserve existing reviewed checkpoints and comments. Do not gate morning proof on cleanup.
