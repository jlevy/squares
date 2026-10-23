---
type: is
id: is-01m5k0t5bchr0e2n7cyczxwtjg
title: Consolidate Recent Results into one chronological result table
kind: feature
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-tracker-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T23:58:15.914Z
updated_at: 2026-10-23T01:36:52.799Z
started_at: 2026-10-22T23:59:59.380Z
closed_at: 2026-10-23T01:36:52.799Z
close_reason: Superseded by explicit latest user serif-introduction and All Results consolidation requests; replacement behavior/evidence and active owner references recorded in notes.
resolution: null
duplicate_of: null
---
Recent Results renderer/data: one semantic table with all 229 registered results exactly once, sorted by arrival date (landed, registered fallback) descending and ID ascending as tie-breaker. The newest arrival date and six preceding calendar dates are initially expanded; all earlier rows share a second tbody behind Earlier results, with no server-hidden data so no-JavaScript readers see every result. Reuse all eight shared metadata cells and canonical full-result links/popovers. Preserve the three legacy recent fragment IDs at the table and older boundary. H1 and ancestry breadcrumb are the only content above the table. Measured 1,295,301 bytes; evidence-based 1,400,000-byte exception matching Results Archive is the required budget follow-up. Coordinate JS/CSS with components and Verification extraction under think-7r1w.

## Notes

Claimed by navigation-landings; four semantic table tests passed in 8.56s. No broad/full build invoked. Core renderer ready; budget/registry and final preview/browser checks are the remaining validation work.

SUPERSEDED by latest explicit user All Results consolidation, tracked by active think-6ts0: canonical results.html retains complete sortable/filterable table, recent-results.html is a compatibility forwarder, Recent menu/page/producer removed. Earlier chronological Recent table work had4semantic passes8.56s plus interaction checks and was built; its removed UI is not an unfinished delivery. Preserve shared filtering utilities and compatibility aliases; obsolete helper cleanup remains deferred think-31fw. Global CI stays kmpp/z3lz.
