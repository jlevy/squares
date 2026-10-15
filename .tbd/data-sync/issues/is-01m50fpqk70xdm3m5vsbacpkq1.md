---
type: is
id: is-01m50fpqk70xdm3m5vsbacpkq1
title: Increase shared H1 spacing across the site
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50ey9mm24zk1872jxfyn3a7
hold: null
hold_until: null
created_at: 2026-10-15T19:12:57.958Z
updated_at: 2026-10-15T19:36:22.956Z
started_at: 2026-10-15T19:20:12.338Z
---
Add a little space above all H1 titles and slightly more below, consistently including the homepage. Use shared design tokens and rules across normal reader pages, tutorials, About, News, Explanations and explainer heroes; preserve responsive layout and existing H2/H3 spacing. Inspect desktop and phone preview, document shared values and run the relevant typography/browser controls.

## Notes

Implemented shared site/reader H1 spacing including homepage, News, About, Explanations and tutorial pages. Standalone explainer paper heroes intentionally keep their publication layouts: their shells do not load site.css, so changing them would broaden this small site release into independent paper/PDF editions. Existing title contract updated and passed; desktop/narrow preview checked. Owner PR checklist includes live spacing review. Close only after deployment.
