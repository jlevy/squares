---
type: is
id: is-01m3txd2djptfw3f89d3bsr7pq
title: "Result filters: a maximum age in days replaces the date range; the Results page starts with significance and age off"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T05:01:13.007Z
updated_at: 2026-10-01T07:14:55.890Z
closed_at: 2026-10-01T07:14:55.889Z
close_reason: Done in f226bfe92 on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. One Max age control in days replaces the date range; the homepage starts at S4 and 180 days (15 of 61 shown), all-results.html at All and no limit (61 shown); the as-rendered default uses the newest registered date, the live page the visitor's date; the 1 August cut is dropped.
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: (1) drop the date range filtering (from and to); have one maximum age in days instead, defaulting to 180. (2) On the standalone Results page, filtering by significance is off and filtering by date is off by default; otherwise its filters are the same as Recent Results on the homepage. So: one filter bar on both tables (think-3pi5) with an Age control (days; empty means no limit); the homepage's Recent Results starts at significance S4 and up and age 180 days; all-results.html starts at significance All and no age limit. Rows hidden by a default stay in the HTML. The no-script and build-time default needs a deterministic reference date (the render's revision date), with the live page measuring age from today.
