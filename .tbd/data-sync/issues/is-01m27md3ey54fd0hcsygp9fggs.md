---
type: is
id: is-01m27md3ey54fd0hcsygp9fggs
title: State the tolerance the gap bar decides 'met' against
kind: bug
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T07:02:40.861Z
updated_at: 2026-10-06T08:50:39.626Z
closed_at: 2026-10-06T08:50:39.626Z
close_reason: "Done: the gap bar's 'met' compares against a stated tolerance, GAP_MET = { centre: 0.02, angle: 0.5, side: 0.002 } in packages/workbench/src/application.js on origin/main, after the validity check (notes: c0d9db2b)."
resolution: null
duplicate_of: null
---
Three steps in 290..324 report a drawn side about 1e-6 above the record -- n = 300 gives 17.824124 against a record of 17.824123, n = 303 and 306 differ only past the sixth decimal. That is the rounding of the printed value, not a real excess, but 'met' is currently decided against it with an implicit tolerance. State the tolerance and compare against it.

## Notes

2026-09-14, lane D-page (PR #160 review D11, c0d9db2b): the gap bar's `valid` is now the PACKING_VALIDITY contract (1e-9), or the declared CATALOGUE_PRECISION (4e-6) where the frame draws a retained record as stored, and `met` requires `valid`. `met`'s side comparison is the stated relative GAP_MET.side (0.2%), which absorbs the 1e-6 rounding this bead describes; whether that relative tolerance is the one to keep is left open here.
