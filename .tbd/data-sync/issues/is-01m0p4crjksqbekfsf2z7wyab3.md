---
type: is
id: is-01m0p4crjksqbekfsf2z7wyab3
title: Codify the rest of the hypothesis register as artifacts
kind: task
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:05.330Z
updated_at: 2026-08-23T01:41:10.449Z
---
H-003..H-010 and H-013..H-015 are still prose in the standing review; ids are reserved in campaign/ideas.md and the checker enforces the reservation. Convert each to a soft-schema artifact under campaign/hypotheses/ with registered: retroactive, criterion, instrument, instrument_ready, budget tier and kill criterion, derived_from: [X-001]. Retire the reservation as each lands - the checker flags a fulfilled reservation as stale. H-001, H-002, H-011, H-012 are already done as the pattern to follow.
