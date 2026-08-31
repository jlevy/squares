---
type: is
id: is-01m0vcbwntnexj584c7kwfs0kn
title: Keep delegated audits inside declared command and time budgets
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
  - delegation
dependencies: []
parent_id: is-01m0r7tkdt35ged6b10gaf9wa0
created_at: 2026-08-25T02:35:37.529Z
updated_at: 2026-08-25T07:04:34.266Z
closed_at: 2026-08-25T07:04:34.266Z
close_reason: "Published in PR #28 at 1ebc13b: W7 and the frozen mixed portfolio are documented; session, phase, finalization, and delegation clock/receipt guards are executable; D-240 through D-248 are synchronized; ordinary validation passed 31/31 locally in 103.91s with 51 pytest contracts and 62 mutation controls; focused session contracts passed 20/20; Linux validate and macOS portability CI both passed. No research run started, and think-3cbq remains blocked on think-jqkv and the unreconciled launch prerequisites."
resolution: null
duplicate_of: null
---
During PR 22 merge-readiness review, a delegated read-only audit launched the explicitly excluded ./test.sh --strict deep gate in an isolated temp tree. Root detected process group 95566 after about two minutes, terminated the exact group, verified cleanup, and discarded the partial result. Record this in the defect log. Use the smallest correction: delegated task contracts must state wall/command exclusions when read-only work could still launch expensive diagnostics, and the coordinator must retain ownership of long-gate authorization and receipts. Do not build leases, permissions, worktrees, or adversarial isolation.
