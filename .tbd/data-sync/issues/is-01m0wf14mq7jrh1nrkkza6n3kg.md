---
type: is
id: is-01m0wf14mq7jrh1nrkkza6n3kg
title: Correct mutated-state negative-control expectations
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
labels:
  - packing
  - bookkeeping
  - testing
dependencies: []
parent_id: is-01m0wer5tgw6h4kv8cvwa3wqpk
created_at: 2026-08-25T12:41:25.387Z
updated_at: 2026-08-25T12:50:48.697Z
closed_at: 2026-08-25T12:50:48.696Z
close_reason: Corrected both expected diagnostics to the mutated-state counts; all 62 controls fire. D-308 records the first expectation error.
resolution: null
duplicate_of: null
---
After synchronizing canonical mutation anchors, two expected diagnostics were set to canonical counts rather than the deliberately mutated counts: hypothesis control expected 41 instead of 42, while unprotected-fix mutation expected 106 instead of the resulting 105. Correct both and rerun all controls.
