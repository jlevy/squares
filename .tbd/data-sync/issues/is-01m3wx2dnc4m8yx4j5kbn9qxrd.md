---
type: is
id: is-01m3wx2dnc4m8yx4j5kbn9qxrd
title: "check_source_coverage: fail when a source key cited by a register entry or its evidence has no coverage entry; backfill the two missing"
kind: task
status: closed
priority: 2
version: 5
delegate: c-gates-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-10-01T23:33:52.939Z
updated_at: 2026-10-23T09:08:17.118Z
started_at: 2026-10-23T06:19:03.682Z
closed_at: 2026-10-23T09:08:17.117Z
close_reason: "Delivered: check_source_coverage.register_source_errors refuses an uncovered recent source cited by the register or its evidence; seven coverage sources backfilled (eab870f8c) with site cards for four (8c26340d9). PR #748 head 417ba331b, CI green (Packing validation run 39927824318, Certificate page 39927824335)."
resolution: null
duplicate_of: null
---
W7. Found by the result import process review (docs/project/reviews/review-2026-10-01-result-import-process.md). check_source_coverage never reads the register or bibliography, so [wand125 rectangle bounds 2026-09-28] (T-046) and [wand125 tools 2026] (T-058, T-059) have no coverage entry and the gate passes. Add the check with a negative control, and add the two entries.

## Notes

2026-10-01: the import of issues 279 to 282 added coverage entries for its three new keys. The two missing entries the audit found ([wand125 rectangle bounds 2026-09-28], [wand125 tools 2026]) are still missing, and the check is still unbuilt.

2026-10-23 c-gates-1023 (PR #748): check_source_coverage.register_source_errors refuses a source dated from 22 August 2026 that a register entry (attribution, builds_on, corrects) or an evidence entry it cites names and no coverage source holds, by source_key or by citing evidence that carries the key. Seven keys failed on main; each now has a coverage source: wand125-rectangles-2026-09-28, wand125-tools-2026-09-29, n17-weighted-certificates-2026-09-20, esummins-packing-2026-10-12, karakus-2026, chelokot-nagamochi-counterexample-2026-09-05, evand-regularizer-2026-10-11. Commit eab870f8c; four tests in test_source_coverage.py (live pass, removal of a source, kingbird-current's evidence-held key, the 22 August boundary).
