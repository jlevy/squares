---
type: is
id: is-01m4zp3krgs81t3yssprxyks8e
title: Fix the lower-bounds paper release command missing its required PDF update mode
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zh3apr6q86jmjggvd08bhr
hold: null
hold_until: null
created_at: 2026-10-15T11:45:37.028Z
updated_at: 2026-10-15T11:46:10.736Z
started_at: 2026-10-15T11:46:10.735Z
---
The real maintained paper v0.4.7 cut exposed an existing generation-command defect: cut_release steps invokes devtools.render_n11_lower_bounds_explainer_pdf without --update, but its real parser requires a mode. HTML/Markdown and release.py are prepared; PDF step correctly refused before publication. Add the required mode and a meaningful contract through the actual renderer parser, keep v0.4.7 fixed, then resume its remaining PDF/test commands. Preserve failed cut receipt; this defect predates PR618 and must be fixed on tutorial-closure rather than restarting its unchanged selected deep gate.
