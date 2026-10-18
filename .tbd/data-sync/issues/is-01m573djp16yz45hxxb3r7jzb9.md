---
type: is
id: is-01m573djp16yz45hxxb3r7jzb9
title: "PR #661 D1: show the exact side underlying the adoption margin"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573danqmx1gv9fe3vh2xsbe
hold: null
hold_until: null
created_at: 2026-10-18T08:52:56.128Z
updated_at: 2026-10-18T09:00:59.569Z
started_at: 2026-10-18T08:53:32.339Z
closed_at: 2026-10-18T09:00:59.568Z
close_reason: "PR #661 review D fixed in 9783a53a22d753c3997d2f2c0f435b9176c3925f and pushed. All 59 adoption tests, 53-case adoption contract, request checker, Ruff and commit hook pass. Formal dispositions: https://github.com/jlevy/squares/pull/661#pullrequestreview-5562216085. CI and fresh followup review remain coordinator-owned; local broader gates incomplete on sparse inputs and bounded timeouts."
resolution: null
duplicate_of: null
---
High finding D1, https://github.com/jlevy/squares/pull/661#pullrequestreview-5562181788. packing/devtools/adopt_houses.py:1406 labels a retained display as the baseline for an improvement measured from verified_upper_bound.exact_form; regenerate packing/frontier/n-029.md and strengthen tests/test_house_adoption.py:1358 using exact arithmetic. Related broader retained-print issue think-gzrw is coordinator-owned.
