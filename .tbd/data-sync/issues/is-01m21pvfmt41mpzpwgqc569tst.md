---
type: is
id: is-01m21pvfmt41mpzpwgqc569tst
title: Keep list bullets square in Elements of the project and other contexts
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-08T23:50:02.649Z
updated_at: 2026-09-09T07:52:46.466Z
closed_at: 2026-09-09T07:52:46.465Z
close_reason: Verified square at 1x/2x, desktop/narrow, and print; no geometry defect remains and the final PDF review is optically square.
resolution: null
duplicate_of: null
---
Owner reports bullets under Elements of the project appear rectangular while others are square. Compare actual rendered marker width/height, layout and optical placement across serif/sans, screen/print and narrow views. Reuse the typography inspector; fix shared marker behavior upstream in KPress when applicable and verify no flex shrinking or line-height distortion. Preserve the already requested slight downward optical adjustment.

## Notes

Current verification covers all 29 visible unordered-list markers across desktop and narrow widths, device scales 1 and 2, and print. The Elements parent and nested markers remain square in computed geometry (3.65625 by 3.65625 CSS px on screen; 3.25 by 3.25 in print), preserve the requested 0.04em downward optical adjustment, and appear square in the final high-resolution PDF review. A 73px scroll shift produced identical crops, so there is no reproducible geometry or flex-shrink defect to fix. Disposable review crops belong under the repository's gitignored attic/.
