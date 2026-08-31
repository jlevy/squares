---
type: is
id: is-01m0sb7s0qq73bynbcywdvanbk
title: Generalize determination outcomes beyond search-only basin labels
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0rmz90gpps8wregvc64ykz9
created_at: 2026-08-24T07:37:25.270Z
updated_at: 2026-08-24T07:53:18.576Z
closed_at: 2026-08-24T07:53:18.575Z
close_reason: "D-133 fixed: the experiment schema and runbook now distinguish generic criterion_met/criterion_missed from search-specific basin labels; exp-012 records criterion_missed, and the new negative control proves an unknown generic outcome is refused."
resolution: null
duplicate_of: null
---
The experiment schema restricts every determination outcome to beat_record/reached_basin/near_miss/no_progress/invalid. H-024 and H-026 were validly preregistered with determination criteria but cannot record confirmed/refuted outcomes without mislabeling a corpus or rigidity result as basin progress. Extend the enum with criterion_met and criterion_missed (or an equally generic typed pair), update the runbook/runner placeholder semantics if needed, add a schema negative control, record the defect, and validate existing artifacts unchanged.
