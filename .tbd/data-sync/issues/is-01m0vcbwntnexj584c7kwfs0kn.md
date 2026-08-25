---
type: is
id: is-01m0vcbwntnexj584c7kwfs0kn
title: Keep delegated audits inside declared command and time budgets
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
  - delegation
dependencies: []
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-25T02:35:37.529Z
updated_at: 2026-08-25T02:35:37.529Z
---
During PR 22 merge-readiness review, a delegated read-only audit launched the explicitly excluded ./test.sh --strict deep gate in an isolated temp tree. Root detected process group 95566 after about two minutes, terminated the exact group, verified cleanup, and discarded the partial result. Record this in the defect log. Use the smallest correction: delegated task contracts must state wall/command exclusions when read-only work could still launch expensive diagnostics, and the coordinator must retain ownership of long-gate authorization and receipts. Do not build leases, permissions, worktrees, or adversarial isolation.
