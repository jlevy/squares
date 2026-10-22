---
type: is
id: is-01m5jxenmw8vmz2699ggvzfvqd
title: Make Results a container and name its content pages
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T22:59:33.658Z
updated_at: 2026-10-22T23:05:14.249Z
started_at: 2026-10-22T23:00:02.356Z
closed_at: 2026-10-22T23:05:14.247Z
close_reason: "Completed Results as a URL-less container with Recent Results, Results Archive, Visual Atlas, and Verification and Ratings destinations. Shared visible/structured trails use a plain Results container and clickable Archive/Visual Atlas detail parents. Added query-preserving direct-load and same-document redirects for all three moved Results section fragments. Updated removed-switcher headroom fixtures, paper Learn/Papers/current metadata, navigation formatting, and mobile font-arrival selectors without changing physical-font, geometry or CLS budgets. Evidence: navigation plus paper metadata 18 passed in 18.22s; corrected four headroom viewport cases 4 passed in 8.87s, other 15 headroom cases passed; real sans-arrival regression 1 passed in 37.86s; BasedPyright zero findings, overview tsc, Ruff, Biome and diff checks passed. Design contract formatted with pinned Flowmark."
resolution: null
duplicate_of: null
---
Make Results a URL-less navigation container; expose Recent Results, Results Archive, and Visual Atlas; update affected headroom and paper breadcrumb contracts.
