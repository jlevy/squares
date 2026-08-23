---
type: is
id: is-01m0rbwtd2mvxhcet6feb55wne
title: "D070: hold exclusion across complete repository critical sections"
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:40.385Z
updated_at: 2026-08-23T22:29:40.385Z
---
One-time marker checks leave check-to-read and check-to-format-or-stage races. Make each gate or runner CLI operation own or narrowly borrow an activity lease for its entire critical section; isolation removes the commit-hook mutation race.
