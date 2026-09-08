---
type: is
id: is-01m1yex3gzj2xpc74rfrghd7bg
title: Verify the math text face in Safari, Firefox and CI's headless shell PDF
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - kpress
dependencies: []
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T17:33:23.870Z
updated_at: 2026-09-07T19:10:33.417Z
---
Playwright WebKit and Firefox (needs a browser download) or manual checks of the composite family, the metrics hook and print; confirm render_explainer_pdf --check on the pinned headless shell in the Pages job.

## Notes

Chromium verified through Playwright (kpress browser test) and the explainer PDF export; Safari and Firefox by hand still open. CI on the pinned headless shell: jlevy/squares#114.
