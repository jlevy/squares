---
type: is
id: is-01m26c1jahzgfckegz7fp9wcq7
title: "N11 BC329: build and admit a bounded fixed-core packet runner"
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol implementation lane
labels:
  - n11
  - tooling
dependencies: []
parent_id: is-01m260z2959dmcmn61pn2z7jsk
created_at: 2026-09-10T19:17:19.821Z
updated_at: 2026-09-10T22:41:10.716Z
---
Implement a maintained entry point for exactly one frozen core side and direction net. It must preserve the original T025 relative-weight scale, report the exact raw minimum m, compare m strictly with M/11, derive normalized bytes by the fixed rule alpha=1/m only after acceptance, enforce a hard process deadline, retain durable partial output, and support the complete exact route, reflected interval route, and dilation replay. Add focused adversarial tests and obtain independent target-free admission before prospectively registering or running BC329. Do not run the scientific target in this bead.

## Notes

Active on stacked branch codex/n11-bc329-fixed-core-runner at c0d357e5. This bead is target-free instrument admission only; no BC329 hypothesis, experiment, or scientific target may be registered or run until implementation and independent admission pass. T025 source is blob 684a6b7adf4524691a4fb996fa3625d909d171ac, SHA-256 3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c; T026 comparison is blob e12789cd8312797254f756446d5ec49c04046a7d, SHA-256 fe786efff724de4cd819928bb04b7337f9f643360f07048fce8c94efb4a646ea. Astra Max confirms the packet mathematics subject to runner admission. A partial observed minimum is only an upper bound on the global m and cannot set alpha; a replayed rational witness at or below M/11 rejects the fixed packet, including equality. Acceptance requires a complete m above M/11, alpha=1/m, explicit least_cell_charge 1, one byte-bound candidate through 2881 exact and 5761 reflected interval directions with exact minimum/enclosure 1, then dilation replay and exact comparison above T026. Execution-level source or method disagreement is invalid evidence while the scientific question remains unresolved. The old rescaling helper omits the real source's minimum declaration, uses a packing-relative provenance path, and has a colliding net-only ID. Admission must also bind the source/revision/import closure, persist atomic partials, supervise and reap the whole process tree, bound dense-route memory, avoid per-direction certificate serialization, and calibrate the full positive-path allowance before registration.
