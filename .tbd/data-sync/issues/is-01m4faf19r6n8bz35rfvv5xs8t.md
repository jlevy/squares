---
type: is
id: is-01m4faf19r6n8bz35rfvv5xs8t
title: Place the full Frontier Survey after the Atlas graphics
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
created_at: 2026-10-09T03:14:17.527Z
updated_at: 2026-10-09T03:14:17.527Z
---
Move the entire Frontier Survey onto atlas.html after the graphical Atlas and remove separate Frontier navigation tab. Preserve all survey prose, controls, table, record popovers and math. Keep frontier.html legacy addresses working via forwarding with query/fragment preservation. Give Atlas graphical case targets and survey-row targets distinct stable fragments, so graphical targets fully expand before revealing their tile while survey targets reveal the correct row. Update case-popover buttons, hero references, canonical/deployment route declarations and affected checks without changing scientific records.
