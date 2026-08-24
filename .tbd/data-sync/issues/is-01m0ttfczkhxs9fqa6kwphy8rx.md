---
type: is
id: is-01m0ttfczkhxs9fqa6kwphy8rx
title: Establish the fast Python refactor-safety test harness
kind: task
status: open
priority: 0
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - testing
dependencies:
  - type: blocks
    target: is-01m0ttfnkek9mx0kv3rgqjth3r
  - type: blocks
    target: is-01m0ttfx53tjv841cn2v2anyf2
  - type: blocks
    target: is-01m0ttg3v5303w5k65gc8th28m
  - type: blocks
    target: is-01m0ttgbpts9xfvqz0wck4781q
  - type: blocks
    target: is-01m0ttgkhcyks8na3prg20kk8c
  - type: blocks
    target: is-01m0ttgtaj1j5rp28wxw84v4wr
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:22:58.150Z
updated_at: 2026-08-24T21:23:44.593Z
---
Add an explicit, fast Python test surface for E2 and E3 behavior before structural cleanup. Use the locked pytest dependency with an unambiguous tests directory, focused selection, deterministic fixtures, behavior and contract assertions, error-path coverage, and integration into the full validation gate. Negative-control the harness itself so empty or missing collection cannot report green, and do not migrate exact or proof scripts merely to increase the pytest count. Acceptance: a focused command protects the first reusable boundaries, named harness failures are watched red, and the existing script-level mathematical, replay, differential, golden, and mutation layers remain distinct.
