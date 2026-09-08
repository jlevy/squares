---
type: is
id: is-01m1yex3gzj2xpc74rfrghd7bg
title: Verify the math text face in Safari, Firefox and CI's headless shell PDF
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - kpress
dependencies: []
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T17:33:23.870Z
updated_at: 2026-09-08T10:26:58.090Z
closed_at: 2026-09-08T10:26:58.090Z
close_reason: "Merged in Squares #128 with KPress #59/#60. Final pre-merge browser/PDF gates and post-merge Pages run 34214731528 passed. The live v0.2.4-33cd4760 page passes delayed-font checks in Chromium, Firefox, and WebKit and actual-font/metric checks on screen and in print; caption and PDF visuals reviewed. Failure paths and negative controls are covered by retained regressions. Detailed evidence is in think-z7ab; full numerical post-merge CI remains tracked by think-h31m."
resolution: null
duplicate_of: null
---
Playwright WebKit and Firefox (needs a browser download) or manual checks of the composite family, the metrics hook and print; confirm render_explainer_pdf --check on the pinned headless shell in the Pages job.

## Notes

The September 8 font review ran pinned Playwright Chromium, Firefox, and WebKit delayed-font checks and inspected caption screenshots. All three engines pass locally. PDF 17 pages with 26 embedded faces, no owned Type3; awaiting final integrated Pages CI and deployed-site checks. Continued under think-z7ab.
