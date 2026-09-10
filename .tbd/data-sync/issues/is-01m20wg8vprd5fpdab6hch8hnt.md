---
type: is
id: is-01m20wg8vprd5fpdab6hch8hnt
title: Preserve bold math faces under the saved sans prose preference
kind: bug
status: closed
priority: 2
version: 5
labels: []
dependencies: []
created_at: 2026-09-08T16:09:32.275Z
updated_at: 2026-09-08T17:15:49.591Z
closed_at: 2026-09-08T17:15:49.586Z
close_reason: "Portable 4096px font-advance probe passed Linux CI on d719f1e7; PR #131 merged as 38ca2892. Correct 650 and actual missing-face controls pass/fail as intended."
resolution: null
duplicate_of: null
---
Review of PR 128 found that kpress.proseFont=sans switches all prose math to the sans composite, including bold D4 expressions, while render_explainer prunes all 650-weight sans slots. Preserve required font faces and exercise the supported preference in actual browser/font validation.

## Notes

Linux CI rounds body-size glyph advances to whole pixels. Replacing that measurement with the pinned kpress enlarged-font probe, retaining the wrong-weight and rounding controls; PR #131 awaits Linux confirmation. The font-slot restoration itself passes the actual-face checks.
