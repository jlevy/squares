---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Astra Max design; Sol implementation after admission
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2appdgg1p32xwgxptcqqb2x
  - type: blocks
    target: is-01m2appm2nx1m700ky98ytzv4z
parent_id: is-01m2aj2ewckram8ww4458w74hr
created_at: 2026-09-12T11:40:18.235Z
updated_at: 2026-09-12T13:47:55.545Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

Astra Max completed the target-free design at /private/tmp/bc329-calibration-design-review.md. It proves an n=2 cross fixture with L=3/4, B=1/2, a center point of weight 1/2, and horizontal/vertical 2-of-3 triples at offsets +/-3/16 of weight 3/4. Expected raw minimum/budget are 2, scale alpha=1/2, normalized minimum/budget 1, interval rows [8,8] on scale 8, dilation side squared 298598409/132756484, and full profile 14,404 direction rows. It flags the nested generic-positive record boundary and requires repeated same-regime timings. Sol xhigh implementation is now running from the admitted-preflight candidate; no calibration or BC329 target has run.
