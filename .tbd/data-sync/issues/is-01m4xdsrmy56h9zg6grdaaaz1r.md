---
type: is
id: is-01m4xdsrmy56h9zg6grdaaaz1r
title: Preserve physical workbench module and JUnit identity in enforced receipts
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xatk8zfjpdxv9kq2gv4yn1
hold: null
hold_until: null
created_at: 2026-10-14T14:41:56.881Z
updated_at: 2026-10-14T14:42:11.450Z
started_at: 2026-10-14T14:42:11.449Z
---
Review H1 at1c5: collecting a workbench module alone changes pytest roots and names, while receipt parser guesses path-based classnames. Fix canonical two-root collection with physical item.path and pytest own JUnit address mapping; retain class and parameter text containing ::; refuse omitted changed workbench cases. Reviewer reproduction and regression required.
