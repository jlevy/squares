---
type: is
id: is-01m0rmz8mp3e2zgfmkd9vqnmyz
title: Price unresolved runner cells against 8h and 24h launch horizons
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - unattended
  - focus-process
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-24T01:08:17.681Z
updated_at: 2026-08-24T01:08:17.681Z
---
D-081. runner.py preflight currently passes whenever any recipe is runnable, so one nominal timebox can present as overnight-ready even when target-host execution is much shorter and the queue empties. Add machine-readable per-cell planning cost, target-host calibration provenance, and a generated readiness view over unresolved cells. Acceptance: status and preflight distinguish operationally runnable from scientifically admissible; one cell is one queued round; p50/p95 costs come from at least three representative host measurements; 8h launch requires >=10h and 24h launch >=30h at p95; empty/underfilled queues fail the requested horizon without blocking ordinary status; and positive/negative fixtures cover horizon, resolved-cell, prereq, and multi-cell semantics.
