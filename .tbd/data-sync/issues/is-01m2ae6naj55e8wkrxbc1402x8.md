---
type: is
id: is-01m2ae6naj55e8wkrxbc1402x8
title: Keep D-490 conclusions within the retained two-length evidence
kind: bug
status: closed
priority: 2
version: 3
delegate: root integration lane
labels: []
dependencies: []
parent_id: is-01m26rygs7f0s76v147x0px4cd
created_at: 2026-09-12T09:12:01.606Z
updated_at: 2026-09-12T09:22:59.260Z
closed_at: 2026-09-12T09:22:59.259Z
close_reason: Corrected in 237c4023 and covered by focused regression, static, generated-view, and clean exact-commit browser checks; final publication gates continue in think-o96l.
resolution: null
duplicate_of: null
---
D-490 still calls the smaller second render deficient and says two bytes left the PDF objects. The retained CI log contains only the two normalized lengths; the render pair was not retained, and fixed-width cross-reference entries do not exclude changes elsewhere. Rewrite the record to state the observed order and size difference, treat object-body and readiness explanations as hypotheses, regenerate the defect view if needed, and preserve the unknown-cause disposition.

## Notes

Corrected at 237c4023. D-490 now records only that the second reported length was two bytes smaller and that 786119 matched other CI draws; it explicitly says the lost pair cannot identify which output was complete or locate the changed bytes. Object-body and readiness explanations remain hypotheses. The generated defect view and synopsis agree.
