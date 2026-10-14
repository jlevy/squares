---
type: is
id: is-01m4x6qhq3wkhbacrtv94d0x45
title: "Results overview: link each credit to the contributor's profile once #490 lands"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T12:38:24.227Z
updated_at: 2026-10-14T12:38:24.227Z
---
Deferred from #514 (think-2z22), review A finding A7. The seven days' entries and the weekly lines link a finder to the listed project holding the result (credit_link in overview_sections). When draft PR #490 lands contributor profiles and Result.credit_html, link the person's profile instead; a one-function change in credit_link, with the rollup tests' credit assertions updated.
