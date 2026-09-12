---
type: is
id: is-01m26c1jahzgfckegz7fp9wcq7
title: "N11 BC329: build and admit a bounded fixed-core packet runner"
kind: task
status: in_progress
priority: 1
version: 15
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: root integration with Sol admission review
labels:
  - n11
  - tooling
dependencies: []
parent_id: is-01m260z2959dmcmn61pn2z7jsk
child_order_hints:
  - is-01m2ag6b030mv58gf58yyka1as
  - is-01m2aj2d1mccqf56hnxqqcwt1b
  - is-01m2aj2deytqhx7j4f1pnte7sp
  - is-01m2aj2dszhq8h9e6sftwqjp0g
  - is-01m2aj2e56r62h83avk7kexvhb
  - is-01m2aj2egf99fwpwh005y9er6n
  - is-01m2aj2ewckram8ww4458w74hr
  - is-01m2aj7paytrdj85x26njv0jrr
  - is-01m2aj7psxqgwsrew721qhsfzj
  - is-01m2aj7q4y8raaw35s0jq3ty2y
created_at: 2026-09-10T19:17:19.821Z
updated_at: 2026-09-12T10:22:52.052Z
---
Implement a maintained entry point for exactly one frozen core side and direction net. It must preserve the original T025 relative-weight scale, report the exact raw minimum m, compare m strictly with M/11, derive normalized bytes by the fixed rule alpha=1/m only after acceptance, enforce a hard process deadline, retain durable partial output, and support the complete exact route, reflected interval route, and dilation replay. Add focused adversarial tests and obtain independent target-free admission before prospectively registering or running BC329. Do not run the scientific target in this bead.

## Notes

Fresh clean continuation branch codex/n11-bc329-runner-publication-stack starts at exact PR149 head 237c4023. The old WIP at c0d357e5 was independently audited by Sol high: 23 runner tests, 16 interval tests, Ruff, BasedPyright, and diff-check pass, but it is not admissible. The recovered draft and interval-progress seam are now copied to the clean branch; stale WIP plan/preflight prose was not copied. Published T026 source constants are rebased, still subject to mutation review under think-ak5v. Admission repairs are explicitly split: per-direction reconstructing readback think-p6nf; bounded out-of-order interval/dilation execution and progress think-cf2z; absolute deadlines, parent attestation and real process-group cleanup think-cm33; immediate exact-disagreement classification think-9p77; defined fsync/crash durability think-gxeg; runtime/strict schema/provenance think-95hs; unexpected failure preservation think-snw7; full target-free calibration think-122i; final-stack documentation think-zd1b. No BC329 hypothesis, experiment, or scientific target may be registered or run until every required repair, calibration, independent reader, and parent admission passes.
