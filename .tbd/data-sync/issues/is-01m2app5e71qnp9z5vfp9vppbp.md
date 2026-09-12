---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 20
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
child_order_hints:
  - is-01m2b1h78j7zhnz1kb62cnmfyg
  - is-01m2b1h7mj4f4wesbj8fwm0fbe
  - is-01m2b1h805emc13mx1cykp5s5x
  - is-01m2b1h8cawhz8q1y1tg2d3c5d
  - is-01m2b1h8ra857ksmj3dd8peqy8
  - is-01m2b1h94a1pkcxm1mhahqads1
  - is-01m2b1h9g2yqdvzd6h3rpr9x72
  - is-01m2b1nkj1qfxr53zgc5wkv8kq
  - is-01m2b4yfx3th5wcdaw9apr0vn5
created_at: 2026-09-12T11:40:18.235Z
updated_at: 2026-09-12T16:31:21.088Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

The calibration command is implemented on b6260970. Astra Max source-distinct correction review accepts CAL-2, CAL-3, CAL-4, and CAL-6; CAL-1 and CAL-7 were already accepted. Admission remains refused only on CAL-5: SIGINT during either staging-file acquisition can leak an unowned temporary file and descriptor, making partial readback fail. Sol is repairing that exact window; think-1arg will rereview before any profile. No positive full-shape profile or BC329 target ran.
