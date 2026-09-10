---
type: is
id: is-01m1zzssc6t2mn96vsjt7cn7xz
title: Exercise math rendering guards when checker files change
kind: bug
status: closed
priority: 2
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:55.397Z
updated_at: 2026-09-08T10:26:58.083Z
closed_at: 2026-09-08T10:26:58.083Z
close_reason: "Merged in Squares #128 with KPress #59/#60. Final pre-merge browser/PDF gates and post-merge Pages run 34214731528 passed. The live v0.2.4-33cd4760 page passes delayed-font checks in Chromium, Firefox, and WebKit and actual-font/metric checks on screen and in print; caption and PDF visuals reviewed. Failure paths and negative controls are covered by retained regressions. Detailed evidence is in think-z7ab; full numerical post-merge CI remains tracked by think-h31m."
resolution: null
duplicate_of: null
---
PR128 adds check_math_faces to pages build but omits its own path from push and PR triggers. Extend filter contract so changing browser gates invokes them. Expand first-visible-math guard beyond Main/Math families, and cover print plus dynamic rerendering.

## Notes

Browser gates now pass hosted Chromium, Firefox and WebKit with positive/negative loading controls. Final read-only host review found no further rendering defect, but actual-face checker converted URL arguments to local paths. Add minimal shared URL-or-path normalization and a focused parser regression so deployed Pages verification can use the same CDP face/metric guard directly. Root will verify both live loading and actual fonts after deployment.
