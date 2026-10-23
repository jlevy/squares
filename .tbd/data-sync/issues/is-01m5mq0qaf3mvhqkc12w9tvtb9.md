---
type: is
id: is-01m5mq0qaf3mvhqkc12w9tvtb9
title: "PR #748 A1 (on #752): coverage source for [wand125 sqverify continuous 2026-10-12]"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: c-review-sqvc-1023
labels: []
dependencies: []
parent_id: is-01m5mpzs25g0r8zzepe0c8fmka
hold: null
hold_until: null
created_at: 2026-10-23T15:45:34.031Z
updated_at: 2026-10-23T15:45:47.994Z
started_at: 2026-10-23T15:45:47.993Z
---
Severity Medium, from #748's review A (https://github.com/jlevy/squares/pull/748#issuecomment-6368647934): #752 adds the recent key [wand125 sqverify continuous 2026-10-12] (dated 2026-10-12) and the evidence E-n040-wand125-sqverify-continuous-6715-report and -6718-report with no coverage source, so check_source_coverage's register_source_errors fails once #748 and #752 are both on main. Fix on #752: a packing/frontier/source-coverage.yaml entry for wand125/square-packing at f30cc2cf and d4a19815, tools/sqverify_continuous, local naming both packets, evidence the two report entries; the github.com/wand125/square-packing card already exists.
