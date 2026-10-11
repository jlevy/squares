---
type: is
id: is-01m3qrq45v5j2nn4p9rw9tg3pj
title: "Atlas: embed the full n = 1..324 ascent film with native controls, preload none, its poster frame and no autoplay, from the site copy"
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T23:41:36.315Z
updated_at: 2026-09-30T19:53:06.878Z
closed_at: 2026-09-30T05:16:47.104Z
close_reason: Overview page and design system (lane B), verified in f4346c9a1 on top of checkpoint cb8222602, with the data (8c24872ae), media (764a5ac90) and reader documents (14cb1c051) it renders.
resolution: null
duplicate_of: null
---

## Notes

Owner decision 2026-09-30: no autoplay; the overview shows the two atlas PDF previews and one embedded player for the full n = 1..324 film.

Audit 2026-09-30: on claude/overview-page-impl the homepage player (a45b835ca, made click-to-play with preload none and a poster in c5bb93279) was replaced by three atlas cards in e20203936, with the film on visualize.html (d73244ff4). It plays the release download; the site copy is think-9xvt, not in that PR. The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
