---
type: is
id: is-01m0ypc53y37erfds2crrtsbqt
title: "W7: canonical differential for degenerate chunk cells"
kind: task
status: open
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-26-overnight-constructive-enumeration.md
labels: []
dependencies: []
hold: blocked
hold_until: null
created_at: 2026-08-26T09:28:15.229Z
updated_at: 2026-08-27T09:28:03.575Z
---
BC-016. Replay aligned and glued chunk strata across declared toolchains and pool widths. Retain endpoint values, canonical active-cell labels, tie behavior, and typed instability. This is deterministic measurement validation, not search; instability blocks the enumerator.

## Notes

Ranked for constructive prerequisite work after the midpoint rotation. BC-016 remains deterministic and target-free. The frozen peer routes are .github/workflows/packing-validation.yml#validate on ubuntu-latest and #macos-portability on macos-latest, both Python 3.14.7 with the frozen lock; receipts must retain actual runner, architecture, Python, NumPy, SciPy, and HiGHS fingerprints. Pool widths are 1 and 10; intended row ids are n005-seed007-known-answer, n010-seed014-known-answer, and n016-grid-not-below; endpoint floor is LP_FEASIBLE_EPS and ties require a complete symbolic label. Implementation is blocked because golden rows drop input poses, n16 has only a value guard, terminal tie provenance is absent, and glued rows are not executable. Next: retain the three poses and a glued row, implement the symbolic tie label and independent checker, then emit every route x width x row receipt. No n11 run or result.
