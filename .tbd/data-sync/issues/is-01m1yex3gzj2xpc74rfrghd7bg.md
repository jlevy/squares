---
type: is
id: is-01m1yex3gzj2xpc74rfrghd7bg
title: Verify the math text face in Safari, Firefox and CI's headless shell PDF
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - kpress
dependencies: []
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T17:33:23.870Z
updated_at: 2026-09-08T08:24:35.373Z
---
Playwright WebKit and Firefox (needs a browser download) or manual checks of the composite family, the metrics hook and print; confirm render_explainer_pdf --check on the pinned headless shell in the Pages job.

## Notes

The September 8 font review ran pinned Playwright Chromium, Firefox, and WebKit delayed-font checks and inspected caption screenshots. All three engines pass locally. PDF 17 pages with 26 embedded faces, no owned Type3; awaiting final integrated Pages CI and deployed-site checks. Continued under think-z7ab.
