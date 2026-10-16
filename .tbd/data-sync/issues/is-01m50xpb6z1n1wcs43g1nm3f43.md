---
type: is
id: is-01m50xpb6z1n1wcs43g1nm3f43
title: Preserve Markdown destinations and literals when abbreviating News names
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m50wb1kss9b0h32m4fg0kv1f
hold: null
hold_until: null
created_at: 2026-10-15T23:17:25.342Z
updated_at: 2026-10-16T01:06:56.679Z
started_at: 2026-10-16T01:06:56.679Z
---
Independent surname review A1 found that abbreviation before Markdown parsing can rewrite a valid link destination containing a person name and can alter code spans. Apply an optional name transform only to ordinary text tokens in the existing inline_html renderer. Preserve URL/title attributes, inline code and math; still shorten normal name link labels. Add focused boundary controls and obtain independent final-delta review. No current selected claim triggers the defect; fix before publishing the surname release.
