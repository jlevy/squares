---
type: is
id: is-01m44m1c47h22mb1g0kzppc54q
title: "Enforce OR-18: ceiling on added blob size and a scan for Git-history reads and blob-id gates in tools"
kind: task
status: open
priority: 2
version: 6
delegate: null
labels: []
dependencies: []
child_order_hints:
  - is-01m4aj1fjtr7gaa8x3p76rr12r
hold: null
hold_until: null
created_at: 2026-10-04T23:29:56.870Z
updated_at: 2026-10-07T06:50:29.849Z
started_at: 2026-10-05T07:21:15.313Z
---
OR-18 (jlevy/squares#345) states the rule but nothing fails a PR that breaks it. Add (1) a branch check that refuses added blobs over a few MB unless listed with a reason, and (2) a scan of packing/devtools and packing/src for git show/rev-parse REV:path reads and Git blob-id or commit gates on results. Existing frozen evidence is exempt per OR-16.

## Notes

Known violation on main: packing/devtools/check_n17_core_stress.py _frozen_bytes compares inputs via git show REV:path (found during the #347 rebuild).

2026-10-05 (PR 347 Review B, B5). The check_n17_core_stress.py site is lines 1554-1556 (_frozen_bytes on FROZEN_ROOT_REF, FROZEN_ENDPOINT_REF and FROZEN_FEATURE_REF, imported at line 47); it is main's code, carried unchanged into PR 347, whose body defers it to this bead.

2026-10-05 07:23 UTC (bead bookkeeper). Review B on jlevy/squares#347 (https://github.com/jlevy/squares/pull/347#pullrequestreview-5411026138), B5 (Low): the violation is at packing/devtools/check_n17_core_stress.py:1554-1556, which reads its three inputs through main's _frozen_bytes (git show REV:path); #347 carries it unchanged as main's code. Removing that read belongs to this bead (the review suggested think-vre9 or a new bead; this one already recorded it). Naming this bead in #347's Deferred list is think-916u. Not merge-blocking for stack 357.
