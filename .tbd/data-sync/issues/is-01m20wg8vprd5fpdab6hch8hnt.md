---
type: is
id: is-01m20wg8vprd5fpdab6hch8hnt
title: Preserve bold math faces under the saved sans prose preference
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-08T16:09:32.275Z
updated_at: 2026-09-08T16:10:28.848Z
---
Review of PR 128 found that kpress.proseFont=sans switches all prose math to the sans composite, including bold D4 expressions, while render_explainer prunes all 650-weight sans slots. Preserve required font faces and exercise the supported preference in actual browser/font validation.
