---
type: is
id: is-01m3v8nsb2pc6hz0b4ynz6jcvg
title: "Result filters: a 'Current best only' checkbox, on by default on the homepage and off on the Results page"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:18:12.953Z
updated_at: 2026-10-01T10:42:49.087Z
closed_at: 2026-10-01T09:52:38.146Z
close_reason: "9036d7c04 on claude/site-polish-2-filter, merged into the follow-up branch claude/site-polish-3 (b25702459): a Current best only checkbox in the shared filter bar, checked on the homepage (6 of 61 shown) and clear on the Results page; composes with Standing; 268 tests pass."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: add a filter for 'current best only' as a checkbox, checked on the homepage overview but not on the all results page. In the shared filter bar (result_filters, table.js, FilterDefaults): one checkbox that shows only rows whose standing is current best; composes with the other filters; default on in RECENT_DEFAULTS and off in RESULTS_DEFAULTS; rows hidden by it stay in the HTML; the count follows; a query preset; whether the Standing select stays beside it or the checkbox replaces it is decided from how the bar reads.

## Notes

Superseded by think-nr0y's wording: the checkbox reads 'Hide superseded' and hides exactly the superseded rows (ca137cfde); checked by default on the homepage, clear on the Results page.
