---
type: is
id: is-01m1xd6e7k0vtcjygy4aehkwe9
title: "Phase 1: machine-reparse catalogue exact forms and degree locks against the frontier (closes think-k5z2)"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6ffzyzddb7by875t49z4
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:18.162Z
updated_at: 2026-09-07T07:45:03.297Z
---
Extend devtools/check_source_coverage.py (or a sibling) to reparse every Kingbird exact form, degree lock, and minimal polynomial, including the multi-line aligned form that hid n = 54, and fail on divergence from frontier/n-NNN.md. Must report zero divergences at n = 1..100 before any n > 100 transcription is trusted. Playbook names this the hard prerequisite.
