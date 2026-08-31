---
type: is
id: is-01m0ye7mq2rqjtpka7hqa0m9r2
title: "W7: coarse class-angle sweep driver with LP-solve accounting"
kind: feature
status: open
priority: 1
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m1b2ac6fw0dw674sd1tz5q7q
created_at: 2026-08-26T07:05:58.754Z
updated_at: 2026-08-31T04:47:53.039Z
---
Per-stratum coarse theta-grid scan (default 1-degree over [0,90) per tilted chunk) feeding bracket refinement, pricing work in counted LP solves per the D-126 retained-work-unit rule. Enforces the X-003 ranking rule: no stratum triage on aligned stage-1 side values; every surviving stratum gets its sweep.
