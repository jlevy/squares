---
type: is
id: is-01m3v75h9swbdk0y0tna2vwrcm
title: "Papers page: the paper cards navigate directly, with no popover"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:51:51.863Z
updated_at: 2026-10-01T08:15:25.195Z
closed_at: 2026-10-01T08:15:25.193Z
close_reason: "Done in 547778a78 and 7ccd61696 on claude/site-polish-2: the three paper cards are plain same-tab links (is_site_page in overview_sections), the Papers intro links the optimality paper and T-060, and the math-face control uses a result row popover. In the local preview: papers.html has no popovertarget."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the papers.html page should also directly nav, as the targets are full pages, not records. The three paper cards (optimality paper, explainer, tutorial) become plain same-tab links like the homepage's page cards (think-bc5d, link_card new_tab=False); their popovers and framed previews go. The explainer card's quiet links (the optimality paper, T-060) move into the Papers intro or the card's own text, since a link cannot nest in a link. Settles item (b) of think-h896. On claude/site-polish-2.
