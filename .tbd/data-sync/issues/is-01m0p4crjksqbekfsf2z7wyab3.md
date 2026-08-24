---
type: is
id: is-01m0p4crjksqbekfsf2z7wyab3
title: Codify the rest of the hypothesis register as artifacts
kind: task
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:05.330Z
updated_at: 2026-08-24T01:14:27.912Z
closed_at: 2026-08-24T01:14:27.891Z
close_reason: "Completed: H-003 through H-010 and H-013 through H-015 are enforced registry artifacts with criteria, readiness, budgets and kill rules; reservations are removed; ideas, X-001, ledger and synopsis reconcile. H-001 was split from new H-024, and H-021 through H-023 carry newly formalized measurement/local-geometry gaps."
resolution: null
duplicate_of: null
---
H-003..H-010 and H-013..H-015 are still prose in the standing review; ids are reserved in campaign/ideas.md and the checker enforces the reservation. Convert each to a soft-schema artifact under campaign/hypotheses/ with registered: retroactive, criterion, instrument, instrument_ready, budget tier and kill criterion, derived_from: [X-001]. Retire the reservation as each lands - the checker flags a fulfilled reservation as stale. H-001, H-002, H-011, H-012 are already done as the pattern to follow.
