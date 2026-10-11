---
type: is
id: is-01m3tx2zd309mf9e05jhxymgm4
title: "Homepage: the coverage and recent-progress paragraphs open Recent Results, not the introduction"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T04:55:42.235Z
updated_at: 2026-10-01T07:14:55.343Z
closed_at: 2026-10-01T07:14:55.337Z
close_reason: Done in 6f34ad316 on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. README carries two shared blocks, project-intro and recent-progress; the homepage renders the second at the head of Recent Results. The section is titled Recent Results (id recent-results).
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: on the homepage, the two paragraphs 'The project covers the problem at every n … n = 21, 32 and 45.' and 'A recent major result settles eleven squares … four stale cached-audit digests.' should be part of the New Results (Recent Results) section, not part of the introduction. They stay in README's intro and remain single-sourced: README marks them as a second shared block, and the overview renders that block at the head of Recent Results, above the lead line and the table; the introduction keeps the first paragraph and the owner's site statement.
