---
type: is
id: is-01m573djp16yz45hxxb3r7jzb9
title: "PR #661 D1: show the exact side underlying the adoption margin"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573danqmx1gv9fe3vh2xsbe
hold: null
hold_until: null
created_at: 2026-10-18T08:52:56.128Z
updated_at: 2026-10-18T08:53:32.339Z
started_at: 2026-10-18T08:53:32.339Z
---
High finding D1, https://github.com/jlevy/squares/pull/661#pullrequestreview-5562181788. packing/devtools/adopt_houses.py:1406 labels a retained display as the baseline for an improvement measured from verified_upper_bound.exact_form; regenerate packing/frontier/n-029.md and strengthen tests/test_house_adoption.py:1358 using exact arithmetic. Related broader retained-print issue think-gzrw is coordinator-owned.
