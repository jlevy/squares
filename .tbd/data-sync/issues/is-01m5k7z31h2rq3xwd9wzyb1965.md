---
type: is
id: is-01m5k7z31h2rq3xwd9wzyb1965
title: Repair stale frontend contracts after Atlas, Results and case typography changes
kind: task
status: closed
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: root-navigation-final
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T02:03:17.424Z
updated_at: 2026-10-23T02:31:24.513Z
started_at: 2026-10-23T02:03:48.970Z
closed_at: 2026-10-23T02:31:24.511Z
close_reason: FinalCI twoE501lines shortened; Ruffcheckandformat bothpass. Earlierfivefocusedbrowsercasespassed; noassertionbehaviorchange.
resolution: null
duplicate_of: null
---
Repair assigned current-head CI failures in test_site_atlas_views.py, test_site_case_records.py, test_site_homepage.py, test_site_math_faces.py, test_site_rendering.py and test_site_result_popover.py. Migrate Frontier table URLs; preserve all324 Atlas coverage/current All Results labels; update serif case-pager classification/homepage order. Investigate mobile result-title font-arrival geometry as potential real bug without weakening stability checks. Preserve others work; focused reruns; stage for root sole committer.

## Notes

Browser stabilization complete in 70102e8ea: News/Results probe now checks category ink on shared neutral fill; case math-face allowlist includes asserted serif pager; legacy cases.html#n-17 follows frontier.html#n-17. Focused verification: News/math 4 passed in 83.29s; legacy redirect 1 passed in 53.98s. Root owns final current-head CI.
