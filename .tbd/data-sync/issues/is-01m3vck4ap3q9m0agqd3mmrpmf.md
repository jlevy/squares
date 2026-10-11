---
type: is
id: is-01m3vck4ap3q9m0agqd3mmrpmf
title: The 'superseded' chip is the same size as the other standing chips
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T09:26:40.213Z
updated_at: 2026-10-01T10:42:43.280Z
closed_at: 2026-10-01T10:42:43.279Z
close_reason: "c1442ae5d, merged into claude/site-polish-3. Cause: a CSS exception let standing chips wrap inside a 6.5rem box, so 'superseded' fit on one line where 'current best' broke to two; the exception is removed and test_every_standing_chip_is_one_size pins it."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the size of the chip for 'superseded' is also wrong for some reason. Find why the superseded chip differs (a different class or element, a font-size or padding from another rule, an inherited muted style, or a link inside it) and make every standing chip one component with one size; pin with a browser test that all standing chips share font size, line height and block size.
