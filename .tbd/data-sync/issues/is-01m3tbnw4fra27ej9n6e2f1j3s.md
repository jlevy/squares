---
type: is
id: is-01m3tbnw4fra27ej9n6e2f1j3s
title: Card headlines in the sans at medium weight, like the site's other large sans headings
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:27.118Z
updated_at: 2026-10-01T04:50:45.403Z
closed_at: 2026-10-01T04:50:45.402Z
close_reason: Done in 85fb33cba on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. Card headlines compute to Source Sans 3 Variable at weight 550, the page-title tokens.
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: headline text on the cards should be sans, medium weight, matching the other large headings that are sans (page titles, section heads in the sans). Set the card headline class to the shared sans heading token and weight, in site.css and paper-design.md, on every page's cards (overview, rung cards, document and project cards).
