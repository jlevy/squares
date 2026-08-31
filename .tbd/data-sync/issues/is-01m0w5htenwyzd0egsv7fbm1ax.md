---
type: is
id: is-01m0w5htenwyzd0egsv7fbm1ax
title: Record and repair Python-format drift that broke both PR 29 CI jobs
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - gate
  - hygiene
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T09:55:46.260Z
updated_at: 2026-08-25T10:17:42.917Z
closed_at: 2026-08-25T10:17:42.916Z
close_reason: "D-268 is recorded and fixed: both replacement CI platforms passed the Python format floor, the complete local gate passes, and the remaining macOS failure was the separately owned obsolete D-272 expected-failure guard."
resolution: null
duplicate_of: null
---
Commit 0fcc4bf added fallback controls that passed focused pytest, Ruff lint, and BasedPyright locally but were not run through ruff format --check. Both Linux validate and macOS portability failed solely on tests/test_research_contracts.py formatting. Delegate the mechanical format fix, record the process defect in the logbook, require the complete local validation surface before the next push, and close only after green CI.
