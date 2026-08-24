---
type: is
id: is-01m0thvax1hetdk00p1g1hbkrp
title: Reject duplicate experiment rows in the synopsis cost table
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T18:52:12.063Z
updated_at: 2026-08-24T18:52:12.063Z
---
D-184. SYNOPSIS.md lists exp-024 twice in the cost-and-provenance table, overstating the visible row count even though generated totals remain correct. Remove the duplicate and extend tools/check_synopsis.py plus a focused negative control so each registered experiment appears exactly once in both the roll-up and cost tables. Acceptance: the positive synopsis check passes; a duplicated exp row fails; defects and generated views reconcile.
