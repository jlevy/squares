---
type: is
id: is-01m44qz48kr4zse36ykc4v9hfb
title: "Homepage: link evand's Square Packing Atlas site and its open-problems page"
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:37.587Z
updated_at: 2026-10-05T07:19:51.808Z
started_at: 2026-10-05T00:41:16.239Z
closed_at: 2026-10-05T07:19:51.808Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Owner request: the evand site and https://evand.github.io/square-packing/problems.html are linked from the project homepage (packing/devtools/overview_sections.py OTHER_PROJECTS / templates/overview-article.md), re-rendered.

## Notes

Homepage: packing/devtools/templates/overview-article.md, Other Square Packing Projects intro now links https://evand.github.io/square-packing/ and https://evand.github.io/square-packing/problems.html (cards are links themselves, so the links are prose). evand card note in overview_sections.OTHER_PROJECTS updated: n = 21, 32, 45, 60, s(k^2-3)=k k>=6, s(k^2-4)=k awaiting replay. Commit 6d48ab842 on claude/ecstatic-pascal-pothtx-evand; render_overview ran clean; tests/test_overview.py, test_site_project_tallies.py pass (291).
