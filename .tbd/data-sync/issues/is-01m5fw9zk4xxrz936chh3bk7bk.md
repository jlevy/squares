---
type: is
id: is-01m5fw9zk4xxrz936chh3bk7bk
title: Review accessible profile links in generated atlas and PDF credit text
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
labels: []
dependencies: []
parent_id: is-01m4kg8rnz0f3k2t115v9ewvwn
created_at: 2026-10-21T18:41:48.130Z
updated_at: 2026-10-21T18:41:48.130Z
---
Generated atlas credit paragraphs currently use SVG text only and tests assert no href in information block. Reviewed figure identity spans do not imply SVG/PDF link annotations. Design native accessible SVG name anchors with print/PDF link validation and correct profile resolution, preserving text/layout. Separate follow-up during PR stabilization; do not claim current diagram text contains profile links.
