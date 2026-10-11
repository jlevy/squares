---
type: is
id: is-01m3tbnv0cq36g0pt6rsp4k9z2
title: "Card rows always centre: a row that does not fill the line centres on it"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:25.963Z
updated_at: 2026-10-01T04:50:44.352Z
closed_at: 2026-10-01T04:50:44.350Z
close_reason: Done in d51af5d5d on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. Cards are a centred wrapping flex row; a 19-width sweep found no off-centre row; the Papers page's three large cards centre.
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: card views should always be centred, so if only three or four cards are present they centre on the line. Today site.css centres a section of three or fewer (d0b20f37a); four cards on a wide screen still left-align. Centre any row that does not fill the line, at every width, including the last partial row of a longer section, without changing card widths.
