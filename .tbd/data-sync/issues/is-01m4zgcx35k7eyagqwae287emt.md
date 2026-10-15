---
type: is
id: is-01m4zgcx35k7eyagqwae287emt
title: Integrate the concurrent adoption release into News delivery
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
child_order_hints:
  - is-01m4zggamwhwqncs7k51rzys8q
hold: null
hold_until: null
created_at: 2026-10-15T10:05:50.052Z
updated_at: 2026-10-15T10:07:42.235Z
started_at: 2026-10-15T10:06:02.240Z
---
PR614 landed asd33de8b10 after PR617/e5e freeze. Mergeability run38716754101 detects conflicts in5generatedclaimdocs and release.py; main publishedv0.7.4/DATA6133c487. Preserve allmainadoptions/source/data/releasehistory, discard ourunpublishedv0.7.4 identity, merge then cut reviewedsitepatchv0.7.5 usingmaintainedtool. Regenerateclaimlinks, re-evaluatefreshpaperdispositionpaths againstnewbase; targetnewdata layout+releasechecks andfreshhostedCI/followupreview without repeatingunchanged11kchecks. Existingold-data pooldeep run may finish before mutation; reuse validupstreamscientificcheckpoint only when matchingrecord/source evidence.
