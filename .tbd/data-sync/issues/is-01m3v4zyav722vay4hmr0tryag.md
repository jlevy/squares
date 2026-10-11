---
type: is
id: is-01m3v4zyav722vay4hmr0tryag
title: "Results table: a wider Credit column and a narrower Result column"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:13:51.450Z
updated_at: 2026-10-01T10:42:38.847Z
closed_at: 2026-10-01T10:42:38.843Z
close_reason: "c1442ae5d, merged into claude/site-polish-3: six columns on both tables (ID, n, Result, Credit, Rungs, Date); Credit has a floor of 11.5rem and is shown in full; records are a quiet line under each result's summary on the Results page; measured by measure_site_pages columns and pinned by test_site_result_columns."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: on the results table, the Credit column should not be so narrow while the Result column is so wide. Rebalance the column widths on Recent Results and all-results.html so credits such as 'Queuingtheorydotcom after Levy, Kleddamag' do not wrap one word to a line; measure at 1280, 1024 and 768.
