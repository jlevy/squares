---
type: is
id: is-01m5k6ez8h4y01f6pf35ceqfsj
title: Migrate stale tests to one canonical All Results table
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-all-results-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:37:00.687Z
updated_at: 2026-10-23T01:45:57.328Z
started_at: 2026-10-23T01:37:16.833Z
closed_at: 2026-10-23T01:45:57.327Z
close_reason: Assigned canonical All Results test migration validated, staged and pushed by root64ab5603; global review/CI stays under integration beads.
resolution: null
duplicate_of: null
---
Own test_site_navigation.py, test_overview.py, test_overview_sections.py, test_site_urls.py and obsolete Recent-only test module/fixtures. Preserve complete canonical filters, replace removed producer assertions with compatibility-forwarder coverage; root alone commits/pushes.

## Notes

Completed canonical All Results test migration pushed by root64ab5603cc3b4fe02541019f7322b6b62ff62d3e. Three files: test_overview.py40focused passes116.64s; shared selection71passes with one old same-page fixture failure, repaired exact legacy fragment/query regression1pass4.18s. Scoped Ruff/format/diff clean and basedpyright0errors0warnings. Removed obsolete Recent disclosure UI tests; compatibility forwarder and complete All Results row/metadata coverage remain. overview_sections/site_urls passed unchanged. Root owns alias-controller initialization fix and current-head hosted acceptance, new topic-style request separately tracked.
