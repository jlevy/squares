---
type: is
id: is-01m4cf1wk0d2f2438dac0ckz2e
title: Fix exact-form identity and retained isolator defects found by Astra
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies:
  - type: blocks
    target: is-01m4cf1w4xst7bfypgq1at86z1
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T00:36:46.302Z
updated_at: 2026-10-08T04:03:19.859Z
started_at: 2026-10-08T00:37:45.020Z
closed_at: 2026-10-08T04:03:19.858Z
close_reason: "Completed and independently re-reviewed by GPT-6 Astra: symbolic exact-form identity, full-precision saved isolators, zero-M2 linear handling, conservative interval evaluation, replayed finite-field certificates, and counterexample/refusal regressions. Independent historical audit verifies all182 source pairs and222 prime replays; the complete n83 degree672 certificate was independently replayed. Final-head Packing37724241509 and Pages37724241497 pass at1d094ccb114a46d9836581c7ac8157593939817e. No geometry or optimality promotion."
resolution: null
duplicate_of: null
---
Astra max review reproduced: builder accepts an in-cell rational approximation as exact_form for catalogue provenance because it proves only enclosure; extractor serialized centre at 60 digits while radius was 1e-109 or 1e-308, making saved interval false; extractor linear polynomial triggers log10(0). Fix all, run counterexample regressions, and have Astra re-read the resulting mathematical contracts. Feeds review think-xe25.
