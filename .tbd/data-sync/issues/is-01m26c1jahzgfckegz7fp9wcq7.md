---
type: is
id: is-01m26c1jahzgfckegz7fp9wcq7
title: "N11 BC329: build and admit a bounded fixed-core packet runner"
kind: task
status: in_progress
priority: 1
version: 19
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
  - is-01m2anz8ybfp4qym3sts3xf9vr
  - is-01m2anzgc2aqn6vzx29ps3rpn2
created_at: 2026-09-10T19:17:19.821Z
updated_at: 2026-09-12T11:41:18.401Z
---
Implement a maintained entry point for exactly one frozen core side and direction net. It must preserve the original T025 relative-weight scale, report the exact raw minimum m, compare m strictly with M/11, derive normalized bytes by the fixed rule alpha=1/m only after acceptance, enforce a hard process deadline, retain atomic process-level partial output without claiming host-crash or power-loss durability, and support the complete exact route, reflected interval route, and dilation replay. Add focused adversarial tests and obtain independent target-free admission before prospectively registering or running BC329. Do not run the scientific target in this bead.

## Notes

Astra Max independently checked the actual BC329 eleven-core theorem chain and exact constants target-free: M, M/11, B, D, S_c and the exact improvement over T026 agree; no theorem gap was found conditional on complete packet acceptance. Critical scope correction: BC329 is not the four-corner/seven-mark lane; that is BC330. No scientific target was run.
