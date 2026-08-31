---
type: is
id: is-01m0wer5tgw6h4kv8cvwa3wqpk
title: Resynchronize aggregate negative-control anchors
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
labels:
  - packing
  - validity
  - ci
dependencies: []
parent_id: is-01m0rvm4r4s2kf1d81dcscwm2c
child_order_hints:
  - is-01m0wf14mq7jrh1nrkkza6n3kg
created_at: 2026-08-25T12:36:31.695Z
updated_at: 2026-08-25T12:50:48.483Z
closed_at: 2026-08-25T12:50:48.482Z
close_reason: Synchronized four exact aggregate mutation anchors without weakening their nearby wrong-value mutations; all 62 controls fire. D-306 records the stale fixtures.
resolution: null
duplicate_of: null
---
The complete gate found four mutation controls whose exact anchors had drifted from current defect, hypothesis, soundness-direction, and gate aggregates; a fifth control exposed the real synopsis error. Update only the stale exact anchors to current canonical values without weakening expected diagnostics, then rerun the control harness.
