---
type: is
id: is-01m3wx2dnc4m8yx4j5kbn9qxrd
title: "check_source_coverage: fail when a source key cited by a register entry or its evidence has no coverage entry; backfill the two missing"
kind: task
status: open
priority: 2
version: 2
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:52.939Z
updated_at: 2026-10-02T00:50:54.336Z
---
W7. Found by the result import process review (docs/project/reviews/review-2026-10-01-result-import-process.md). check_source_coverage never reads the register or bibliography, so [wand125 rectangle bounds 2026-09-28] (T-046) and [wand125 tools 2026] (T-058, T-059) have no coverage entry and the gate passes. Add the check with a negative control, and add the two entries.

## Notes

2026-10-01: the import of issues 279 to 282 added coverage entries for its three new keys. The two missing entries the audit found ([wand125 rectangle bounds 2026-09-28], [wand125 tools 2026]) are still missing, and the check is still unbuilt.
