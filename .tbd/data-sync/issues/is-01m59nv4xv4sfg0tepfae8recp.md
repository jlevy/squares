---
type: is
id: is-01m59nv4xv4sfg0tepfae8recp
title: "PR #665 M2: refresh n132 writer-owned prior-house provenance"
kind: bug
status: closed
priority: 2
version: 4
delegate: codex-665-adoption-reconcile
labels: []
dependencies: []
parent_id: is-01m59jbf3zmjznc12k8g2b5cwk
hold: null
hold_until: null
created_at: 2026-10-19T08:53:24.026Z
updated_at: 2026-10-19T09:24:32.058Z
started_at: 2026-10-19T08:53:36.182Z
closed_at: 2026-10-19T09:24:32.058Z
close_reason: Fixed at 708a372dcead45623cbda47a3a1e96ddddd7771a; authoritative retained-prior writer and exact-margin/source-custody checks confirm repair. M1 cap tracked separately in think-2921.
resolution: null
duplicate_of: null
---
Astra local review .codex/intake-resume-20261019/665-prospective-final-review.md M2, medium: frozen7d47153 n132 priority_notes does not match generalized history_note because reported/verified displays differ. Refresh only current writer-owned provenance from retained prior record; preserve numerical/geometry evidence and source archive.

## Notes

Fixed in34903e and708a372d:132current writer-owned note/opening/certificate refreshed from exact raw prior; all numerical fields unchanged. Full valid-input test_the_writer_rebuilds_every_adopted_record_from_its_prior_state now passes acrossall66. All37span audit additionally found308same issue and refreshed current spans while preserving history. Exact static upper/lower/result invariants pass.
