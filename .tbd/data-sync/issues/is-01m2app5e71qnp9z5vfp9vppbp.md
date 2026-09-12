---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 18
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
updated_at: 2026-09-12T16:09:15.506Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

Integrated target-free provenance remains 2179b327 from 1a5a8565 and 8d21f58a from ecce6dba. The first calibration and follow-up preflight repair is d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014, with prior contract notes at d924a4bfff54fad8a039ae0cde2103a0e4817848. A source-distinct correction review accepted CAL-1 and CAL-7 and reproduced five residual defects. Correction commit 229b3fc2d3e5056c67b7dbe0224a399e524537c3 addresses CAL-2 through CAL-6 with a real generic small-net dilation comparison, end-to-end dilation labels, real SIGINT launch cleanup and handler restoration, staged terminal admission with late validation, serialization, and promotion controls, and two positive RSS observations. Combined target-free suites: 177 passed in 17.79s; repository-wide Ruff and BasedPyright clean; edit tier passed in 61.84s. CAL-2 through CAL-6 remain open for source-distinct re-review; CAL-1 and CAL-7 were already closed by the distinct review. No positive full-shape profile or BC329 target ran.
