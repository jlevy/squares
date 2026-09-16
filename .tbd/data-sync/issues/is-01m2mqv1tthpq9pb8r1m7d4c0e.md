---
type: is
id: is-01m2mqv1tthpq9pb8r1m7d4c0e
title: "Fix PR #180 browser-floor coverage test exceeding quick-lane wall"
kind: bug
status: closed
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m2m6y4gw224dgrwf37bgqnhd
created_at: 2026-09-16T09:12:51.289Z
updated_at: 2026-09-16T09:20:07.919Z
closed_at: 2026-09-16T09:20:07.916Z
close_reason: null
resolution: null
duplicate_of: null
---
Fresh exact-head hosted run 35077692137 at d7c07bf7 passed frontend and the visual/page matrix, but suite-a failed because test_the_package_program_is_required_for_package_typescript spent 12.74s in its call against the 12s quick-test backstop. Diagnose and fix the test so it retains the negative proof that package TypeScript is not covered by root-only programs without repeating TypeScript program discovery unnecessarily. Require focused local timing, exact-head hosted suite-a, and no weakening of the wall ceiling.

## Notes

Fixed at f4cfa5be26cc73f552537963b8689040d2ca1694. Fresh exact-head hosted packing run 35078515837 passed suite-a in 2m49s with no 12s per-test wall violation; frontend also passed in 2m46s. The 12s guard remains unchanged. Local isolated test 1.68-1.93s, full 55-test contract passes, official browser floor passes 552 files plus 146 Node tests, Ruff clean, BasedPyright 0/0/0.
