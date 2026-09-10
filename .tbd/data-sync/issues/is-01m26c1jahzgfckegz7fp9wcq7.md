---
type: is
id: is-01m26c1jahzgfckegz7fp9wcq7
title: "N11 BC329: build and admit a bounded fixed-core packet runner"
kind: task
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol implementation lane
labels:
  - n11
  - tooling
dependencies: []
parent_id: is-01m260z2959dmcmn61pn2z7jsk
created_at: 2026-09-10T19:17:19.821Z
updated_at: 2026-09-10T22:31:35.075Z
---
Implement a maintained entry point for exactly one frozen core side and direction net. It must preserve the original T025 relative-weight scale, report the exact raw minimum m, compare m strictly with M/11, derive normalized bytes by the fixed rule alpha=1/m only after acceptance, enforce a hard process deadline, retain durable partial output, and support the complete exact route, reflected interval route, and dilation replay. Add focused adversarial tests and obtain independent target-free admission before prospectively registering or running BC329. Do not run the scientific target in this bead.

## Notes

Active on stacked branch codex/n11-bc329-fixed-core-runner at c0d357e5. Workflow is target-free instrument admission only. One Sol lane implements; one Sol lane inventories reuse and adversarial tests; one Astra Max lane audits the mathematical contract. No BC329 hypothesis, experiment, or scientific target may be registered or run until implementation and independent admission pass.
