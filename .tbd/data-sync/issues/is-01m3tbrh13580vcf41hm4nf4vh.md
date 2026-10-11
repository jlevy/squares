---
type: is
id: is-01m3tbrh13580vcf41hm4nf4vh
title: "Site: a Papers tab holding the explainer and the tutorial, each as a large card"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:52:54.038Z
updated_at: 2026-10-01T04:50:48.583Z
closed_at: 2026-10-01T04:50:48.580Z
close_reason: "Done in 57c13da5b and e5047cfef on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. Nav: Overview, Frontier, Results, Papers, Visualize, GitHub. papers.html holds three large cards: the n = 11 optimality paper (from jlevy/squares#259), the explainer, the tutorial; Papers is current on all of their pages."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: move Explainer and Tutorial under a single nav tab, Papers. A papers.html page carries one large card for each (think-ialw's large size), each explaining what the paper is. The nav's Explainer and Tutorial entries become one Papers entry, marked current on papers.html, explainer.html and tutorial.html; the pages keep their URLs. Update the nav partial, SITE_PAGES, the design doc's nav list, the published-site and Pages checks, and the tests that pin the entries.
