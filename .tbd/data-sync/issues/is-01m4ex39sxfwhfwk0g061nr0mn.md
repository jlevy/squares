---
type: is
id: is-01m4ex39sxfwhfwk0g061nr0mn
title: Publish the complete atlas on a dedicated page
kind: feature
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10.local
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3c459d9jrd6mds18ftqg
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-08T23:20:41.532Z
updated_at: 2026-10-09T04:59:36.812Z
started_at: 2026-10-09T00:25:38.385Z
---
Add atlas.html for the full 324-case atlas, reusing drawing assets, views, controls and canonical case pages/popovers. Expose it through shared navigation while retaining the Frontier survey. Register its URL, crawl metadata, builder assets, preview coverage and Pages scope. Forward existing homepage atlas fragments and query view state to the full atlas. Preserve published case/result addresses. See L4 in the spec.

## Notes

Newestownerrequest: Triangle is default selection on dedicatedatlas.html; Grid remains explicit selectable/shareable/reloadable. Keep existing?atlas=triangle links, otherqueryparameters,size,hash and case targets valid. Bootstrapandinitialtabselection agree without alteringhomepage scopedcollapsedGrid. Preserveusable noJS layout. Responsiveapproximate100whole-rowpreview is separatelytracked think-b2o9; expanded324strict.
