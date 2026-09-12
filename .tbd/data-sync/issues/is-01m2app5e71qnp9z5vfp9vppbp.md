---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 16
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
created_at: 2026-09-12T11:40:18.235Z
updated_at: 2026-09-12T15:25:36.231Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

Integrated the target-free repairs 1a5a8565eb7d8a4ed5c8dfc1979a2d3af5c034fe and ecce6dba0084d80e08d9eece2a37b19c1fe5e9ed as 2179b327 and 8d21f58a. Calibration blockers CAL-1 through CAL-7 and follow-up preflight findings think-fmju/think-g7vg/think-pvmv are repaired in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014; contract notes are committed in d924a4bfff54fad8a039ae0cde2103a0e4817848. Combined target-free tests: 170 passed in 18.44 seconds; Ruff passed; BasedPyright reported zero; packing-validate --edit passed 44/73 in 48.86 seconds (49.35 seconds command wall). The exact n=2 fixture and 14,404-row shape are unchanged. Leave all blockers open for source-distinct closure review; no positive full-shape profile or BC329 target ran.
