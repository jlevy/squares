---
type: is
id: is-01m2app5e71qnp9z5vfp9vppbp
title: Build the separate fixed-core packet calibration command
kind: feature
status: in_progress
priority: 1
version: 15
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
updated_at: 2026-09-12T14:52:14.272Z
---
Add a maintained calibrate_fixed_core_packet command with strict fixed-core-packet-calibration/v1 receipt semantics. It must remain outside the BC329 scientific state machine, use a frozen analytically solved positive fixture, call the real raw, normalized-exact, reflected-interval, dilation, publication, and strict per-direction readback kernels, and never emit packet-accepted or scientific evidence. Freeze and independently verify the fixture argument and exact answers; preserve truthful fixture provenance rather than T025 ancestry. Add cross-schema refusal, known-answer, row/witness mutation, source-separation, byte-binding, lifecycle, and metrics controls. Do not run the BC329 source or target.

## Notes

Calibration implementation commit 4ceaa248d6430eec7e6a3e4d97632a86646b57a7
adds a separate fixed-core-packet-calibration/v1 command and an analytically solved n=2
fixture on base c516a592. The fixture uses L=3/4, B=1/2, one point atom of weight
1/2, and horizontal and vertical two-of-three atoms of weight 3/4. Astra Max
independently proved that every admissible core has raw charge 2, normalized charge 1,
and normalized budget 1; its exact net and dilation constants also agree. The delta has
41 calibration tests and 127 combined focused tests passing; focused Ruff,
BasedPyright, Flowmark, link, KaTeX, and source-manifest checks pass. No BC329 target or
positive full-shape profile ran.

Source-distinct review at /private/tmp/bc329-calibration-source-distinct-review.md
refuses admission despite the correct fixture mathematics. Seven reproduced blockers
are now distinct child beads and dependencies of this bead: think-pk84 requires complete
terminal routes and known-answer readback; think-bi3f closes and exactly checks dilation;
think-1kgu binds partial interval/dilation sets and depends on think-yiay; think-lidy
handles SIGTERM/SIGHUP and launch-window cleanup and depends on think-5fdx; think-4wuj
makes bounded terminal readback precede success and depends on think-42zc; think-1e9p
requires interpretable CPU/RSS evidence; think-th5z binds actual worker and allowance
settings to the seed and reader. The review retained adversarial scripts and logs in
/private/tmp and found no scientific target or positive profile.

Integration must include the separately reviewed preflight repair and partial-direction
repair, close all seven calibration findings with maintained controls, and receive a
fresh source-distinct combined-head review before think-vy5i profiles may run.
