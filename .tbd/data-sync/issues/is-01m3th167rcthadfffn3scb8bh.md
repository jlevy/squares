---
type: is
id: is-01m3th167rcthadfffn3scb8bh
title: "Final integration of the website PR: merge the five design branches, then current origin/main, and incorporate what landed"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T01:25:00.789Z
updated_at: 2026-10-01T05:04:33.116Z
closed_at: 2026-10-01T05:04:33.114Z
close_reason: "Done on claude/overview-page-impl, pushed at d078a2020 (jlevy/squares#255): the five design branches merged (752caec19, 02be55bd4, 913534347, c00e00a6e), the row popover wired to the result overview (090309910), origin/main 306ae9fab merged (8ef9107c5: jlevy/squares#259's optimality paper and #249's results import; T-061 registered 2026-09-30), the optimality paper added to Papers (e5047cfef), rationale wording (c266798d9), spec (28e4b07b2), shared test renders (13b822391), re-pin (91bc54323). Hosted CI at d078a2020: 27 checks pass, 0 fail. Later owner requests continue as their own beads."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: monitor origin/main; when the work is done, merge it into claude/overview-page-impl, resolve the remaining issues, and make sure newly landed results are properly incorporated. Steps: (1) merge the helper branches (cards and math faces; Papers tab and explainer retitle; table rows, popovers and facet filters; result overview; README and homepage intro) and wire the row popover to the result overview; (2) merge origin/main, at least cbd01be8c (jlevy/squares#259, the n = 11 optimality paper with its own renderer and Pages job: conflicts expected in pages.yml, pages_scope.py, README, SYNOPSIS, gate-budgets.yaml and the Pages tests), and whatever lands later (jlevy/squares#249 and #258, the results import, would add registered results that need the registered field, the site's generated surfaces, the reader prose and a re-pin); (3) add the n = 11 optimality paper to the Papers tab and link it from the explainer card; (4) share site-page renders across test modules (think-lfnl); (5) full gates, push, refresh jlevy/squares#255's description and the local preview.
