---
type: is
id: is-01m1q7tdv63h6rejzsfzefgr96
title: Larger base type on the certificate page via kpress CSS variables
kind: task
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T22:14:55.077Z
updated_at: 2026-09-04T22:40:11.571Z
closed_at: 2026-09-04T22:40:11.571Z
close_reason: "Commit f05a7ccb: --kpress-host-font-size-base: 18px on :root; kpress derives the whole scale from it."
resolution: null
duplicate_of: null
---
Review feedback on PR #79: the page's type is too small across the board. Raise it by overriding kpress's base font-size / measure custom properties in the page's own CSS rather than restyling elements, so the whole scale (headings, body, captions, code, figures) moves together.
