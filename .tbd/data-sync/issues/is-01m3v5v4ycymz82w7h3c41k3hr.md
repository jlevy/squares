---
type: is
id: is-01m3v5v4ycymz82w7h3c41k3hr
title: "preview_site: --press on a row hidden by the default filter times out; --shots has no dark mode"
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:28:42.949Z
updated_at: 2026-10-01T07:28:42.949Z
---
preview_site --press \"#t-056\" (a row the S4 default hides) times out in Playwright click and exits with a traceback; press should un-hide or report. --shots renders light only, so dark-theme checks needed a scratch script (design-chips-tmp/shoot.py).
