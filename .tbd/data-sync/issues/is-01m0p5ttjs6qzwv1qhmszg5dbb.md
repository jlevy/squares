---
type: is
id: is-01m0p5ttjs6qzwv1qhmszg5dbb
title: Add a cdylib seam only if quench-in-loop needs it
kind: task
status: open
priority: 4
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-23T02:05:14.712Z
updated_at: 2026-08-23T02:05:14.712Z
---
Conditional. If a strategy needs the quench inside its move loop rather than between candidates, add a cdylib crate-type to the existing sqsearch crate and call it with ctypes - measured at 0.52us for 33 f64 into numpy, so a per-iteration call is viable. No maturin, no wheels, no PyO3 dependency. Do NOT do this speculatively: the seam between proposer and quench is currently free at 1.4% of a quench.
