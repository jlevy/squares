---
type: is
id: is-01m0nym0vyhgqmzz7rfv5st5f4
title: f64 and Filtered scalars, with per-stage filter-rate counters
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:11.742Z
updated_at: 2026-08-23T05:26:44.772Z
---
Filtered = f64 plus an error bound, escalating only when the sign is in doubt. Instrument the filter rate per stage from the start: for n=11 only 14 of 55 pairs need the exact path, and that ratio at larger n is an open question the spec flags.
