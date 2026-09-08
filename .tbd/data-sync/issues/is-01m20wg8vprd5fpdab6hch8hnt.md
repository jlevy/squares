---
type: is
id: is-01m20wg8vprd5fpdab6hch8hnt
title: Preserve bold math faces under the saved sans prose preference
kind: bug
status: in_progress
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-08T16:09:32.275Z
updated_at: 2026-09-08T16:58:06.171Z
closed_at: 2026-09-08T16:46:38.896Z
close_reason: "Implemented and independently reviewed in ce3b1ab5 / PR #131. Focused tests, browser controls, both font preferences, PDF reproducibility, and the committed atlas guard pass."
resolution: null
duplicate_of: null
---
Review of PR 128 found that kpress.proseFont=sans switches all prose math to the sans composite, including bold D4 expressions, while render_explainer prunes all 650-weight sans slots. Preserve required font faces and exercise the supported preference in actual browser/font validation.

## Notes

Linux CI rounds body-size glyph advances to whole pixels. Replacing that measurement with the pinned kpress enlarged-font probe, retaining the wrong-weight and rounding controls; PR #131 awaits Linux confirmation. The font-slot restoration itself passes the actual-face checks.
