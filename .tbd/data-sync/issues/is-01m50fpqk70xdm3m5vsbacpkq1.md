---
type: is
id: is-01m50fpqk70xdm3m5vsbacpkq1
title: Increase shared H1 spacing across the site
kind: task
status: closed
priority: 2
version: 4
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m50ey9mm24zk1872jxfyn3a7
hold: null
hold_until: null
created_at: 2026-10-15T19:12:57.958Z
updated_at: 2026-10-15T20:08:46.544Z
started_at: 2026-10-15T19:20:12.338Z
closed_at: 2026-10-15T20:08:46.544Z
close_reason: "Delivered in PR623, merge6e73ef1c: independent senior/security reviews clear; matching-head PR CI passed; production Pages38797565374 deployed and exact-commit4480/4480liveauditpassed. Actual livev0.7.10 desktop/mobile reader pages checked. Owner8-itemvisualchecklist is inPRbody. Broader CIperformance/main-deep monitoring remains separate under existing open work."
resolution: null
duplicate_of: null
---
Add a little space above all H1 titles and slightly more below, consistently including the homepage. Use shared design tokens and rules across normal reader pages, tutorials, About, News, Explanations and explainer heroes; preserve responsive layout and existing H2/H3 spacing. Inspect desktop and phone preview, document shared values and run the relevant typography/browser controls.

## Notes

Implemented shared site/reader H1 spacing including homepage, News, About, Explanations and tutorial pages. Standalone explainer paper heroes intentionally keep their publication layouts: their shells do not load site.css, so changing them would broaden this small site release into independent paper/PDF editions. Existing title contract updated and passed; desktop/narrow preview checked. Owner PR checklist includes live spacing review. Close only after deployment.
