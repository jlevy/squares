---
type: is
id: is-01m4zr45pxh7wjwcrkf88txx2k
title: Repair poster legend acceptance tests for the current admitted atlas export and numeric-only accents
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels:
  - pr-619
dependencies: []
parent_id: is-01m4me9gfnc1denbcj8v7veqnp
hold: null
hold_until: null
created_at: 2026-10-15T12:20:52.571Z
updated_at: 2026-10-15T13:17:34.424Z
started_at: 2026-10-15T12:21:11.707Z
closed_at: 2026-10-15T13:17:34.424Z
close_reason: Delivered in PR619, merged 31eaf6333c5d5b6b3d111241768cdd3d30982588. All 43 executed PR checks and selected Deep38735581202 passed. Main Pages38739226771 published site v0.7.7, shared infographics v0.6.1 and lower-bounds paper v0.4.7; actual deployment audit job116439283652 passed 4460/4460 checks. Main full Packing remains independently in progress; no three-minute performance claim. Focused CI safety and performance work continues under think-3d1m and think-kxmq.
resolution: null
duplicate_of: null
---
Final closure pre-push at4dd found two stale assertions in test_known_best_atlas.py: descriptor still requires optimality proof as a red role, and retained poster expected307 exact/17 numeric despite admitted current export308/16. Preserve independent geometry/badge/count assertions; update description controls for gray case labels, numeric-only accents and unmodified badge styling. Record10,930 normalpasses/49skips/1xfail/twofailures and RuffRUF001 rather than calling broadrun green. Incremental final validation must not repeat unchanged corpus without need.

## Notes

Fixed in9b4a7abfb, reviewed at finalPR619head3a00b00438e0b7ae4276eb2b38a6e45dd94b3701. Two targetedtests red2failed1.74s then green2passed1.86s. Existingdescription/layout/badge/rigidityassertionsretained; revisedtest independentlyreadsall324frontierrecords, pins308exact/16numericandcomparesentiredepictedbadgesets. Ruff/format/diffchecks clean. Broad4ddrun remainsfailed; no repeatedunchangednormalcorpus afterscratch77MiB. FinalhostedPacking/selectedDeep running; closeafterpublication.
