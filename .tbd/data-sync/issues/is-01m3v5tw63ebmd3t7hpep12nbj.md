---
type: is
id: is-01m3v5tw63ebmd3t7hpep12nbj
title: frontier.html is within 92 KB of its 4,194,304-byte ceiling
kind: task
status: closed
priority: 3
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgh5vhwpb57pvzhtnd5ece
created_at: 2026-10-01T07:28:33.986Z
updated_at: 2026-10-03T14:38:02.922Z
closed_at: 2026-10-03T14:38:02.922Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
After the row popovers, frontier.html is 4,102,673 bytes. One more column or per-row detail breaks the ceiling. Move its row detail to fetched fragments as the result overviews are, or raise the ceiling on purpose.

## Notes

Committed c669d2f37 (every page drops data-col and data-col-index; frontier.html 4,070,117 bytes).
