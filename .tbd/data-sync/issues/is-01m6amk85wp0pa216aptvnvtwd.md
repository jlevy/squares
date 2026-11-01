---
type: is
id: is-01m6amk85wp0pa216aptvnvtwd
title: "Intake 2026-10-31 L11: read #842's cert-mode answer (moh63-dev, 2026-11-01T03:46Z) and post its follow-up; read TheSnakeFang/squarepack-certs f6b9499 (strip-n6)"
kind: task
status: in_progress
priority: 2
version: 2
delegate: bold-ritchie-l11
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-01T04:06:32.892Z
updated_at: 2026-11-01T04:06:37.898Z
started_at: 2026-11-01T04:06:37.898Z
---
Two items from the 2026-11-01 03:53 intake sweep (epic think-3guf, lane L11, bold-ritchie-l11).

1. #842 (closed): moh63-dev's comment of 2026-11-01T03:46:21Z (https://github.com/jlevy/squares/issues/842#issuecomment-6553028920) answers the closing reply's informational question. The zm_mixed.py runs without --cert-mode were not deliberate, and cannot change this cover's outcome: line_points is empty and there are 0 polygons, and all 62 recorded runs report "closed by Lemma T with line points: 0". The authors offer a cert-mode pass, accept review F1's interval-certified correction for zmx2, and will fix their README and paper wording in their next release. Work: move #842's read_through, record the answer in its notes, review F4 / F1 / section 11, and E-khalili-842-cover-report; this bead becomes #842's answer bead (think-1v4b is closed); stage 7 owes the follow-up (check_requests marks a reply due for a comment read in on a later day than the last reply); draft it from main with check_requests --draft 842, post it, and record it under replies.

2. TheSnakeFang/squarepack-certs, head f6b9499c3142 (2026-10-31, "strip-n6: raw O2 provenance for six squares in a strip, 1.87 <= H < 2"), one commit past the d56c9a0 read: read it and record the read in intake-watch.yaml.

Done when the PR carrying both is merged and #842's follow-up is posted and recorded. Do not close before the PR merges.
