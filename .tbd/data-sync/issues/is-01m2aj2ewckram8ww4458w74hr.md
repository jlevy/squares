---
type: is
id: is-01m2aj2ewckram8ww4458w74hr
title: Calibrate the BC329 complete positive path before target registration
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T10:19:38.251Z
updated_at: 2026-09-12T10:22:41.539Z
---
After correctness repairs, run a target-free byte-bound positive fixture through raw sweep, normalized exact route, reflected interval route, dilation replay, publication, and independent per-direction readback. Retain wall/CPU clocks, direction counts, peak RSS, output bytes/files, worker count, source and implementation manifests, and deadline headroom on the intended host. Set the prospective scientific/external allowances from this measurement. The synthetic fixture must exercise the same serialization and route shapes without asking the BC329 scientific question; no target registration until an independent reader accepts the receipt.
