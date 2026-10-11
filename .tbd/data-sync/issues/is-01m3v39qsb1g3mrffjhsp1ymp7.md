---
type: is
id: is-01m3v39qsb1g3mrffjhsp1ymp7
title: Cards whose target is a full site page navigate directly, with no popover
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T06:44:15.260Z
updated_at: 2026-10-01T07:14:59.735Z
closed_at: 2026-10-01T07:14:59.704Z
close_reason: Done in 4df75b3db on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. The homepage's four page cards are plain same-tab links (link_card new_tab=False); no pop-page popovers remain. The Papers page's cards keep their popovers, per the owner's 'on the main overview page'.
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the main boxes with the explainer, tutorial, workbench and frontier atlas should navigate directly, since the targets are full pages on the site. The homepage's page cards (and the Papers page's paper cards, whose targets are full pages too) become plain links that go to the page in the same tab; no popover preview frames a page the site already serves. Popovers stay for cards whose target is not a site page of its own (a result, a case, an external repository or document). Supersedes think-x5z0 and think-1wa2 for these cards.
