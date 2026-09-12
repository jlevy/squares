---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 23
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
  - type: blocks
    target: is-01m2b884n0ms50xp93q6aaps1g
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
  - is-01m2b883mnsa3g9ap94gy5aj0q
created_at: 2026-09-12T11:40:18.235Z
updated_at: 2026-09-12T16:47:29.356Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

Calibration implementation follow-up is at 967f7cd46e94a9fddbad653295b146de5740110c. Six CAL findings have source-distinct acceptance; the remaining CAL-5 mkstemp signal window is repaired for both staging passes with real SIGINT, descriptor/file cleanup, provenance/redelivery, and retained partial readback controls. Focused suites: 180 passed in 23.31s; Ruff/BasedPyright clean. Edit tier otherwise passed but reports an unrelated current bead-tree inconsistency. think-4wuj and think-1arg remain open for source-distinct readback before any profile. No positive full-shape profile or BC329 target ran.
