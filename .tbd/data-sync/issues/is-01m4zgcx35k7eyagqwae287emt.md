---
type: is
id: is-01m4zgcx35k7eyagqwae287emt
title: Integrate the concurrent adoption release into News delivery
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
child_order_hints:
  - is-01m4zggamwhwqncs7k51rzys8q
hold: null
hold_until: null
created_at: 2026-10-15T10:05:50.052Z
updated_at: 2026-10-15T11:15:51.126Z
started_at: 2026-10-15T10:06:02.240Z
closed_at: 2026-10-15T11:15:51.126Z
close_reason: Delivered and reviewed in PR617, merge f97bc0b199e2493b0d84ba51f512e2b406b73021. Pages run38722914631 and full main Packing38722914629 succeeded; hosted verify-deployment succeeded10:59:54UTC. Live index/news/papers HTTP200 v0.7.5 smoke retained in news-live-v075-smoke.json. Includes shared article headers/original dates, compact filters/topics/meters, site fonts, concurrent adoption news and bookmark oracle.
resolution: null
duplicate_of: null
---
PR614 landed asd33de8b10 after PR617/e5e freeze. Mergeability run38716754101 detects conflicts in5generatedclaimdocs and release.py; main publishedv0.7.4/DATA6133c487. Preserve allmainadoptions/source/data/releasehistory, discard ourunpublishedv0.7.4 identity, merge then cut reviewedsitepatchv0.7.5 usingmaintainedtool. Regenerateclaimlinks, re-evaluatefreshpaperdispositionpaths againstnewbase; targetnewdata layout+releasechecks andfreshhostedCI/followupreview without repeatingunchanged11kchecks. Existingold-data pooldeep run may finish before mutation; reuse validupstreamscientificcheckpoint only when matchingrecord/source evidence.

## Notes

Integrated origin/main d33de8b105f5b7a43646ad5fc2aa890894dbb50c as merge 312dab523, preserving its v0.7.4 adoption history, DATA_REVISION 6133c487 and all three upstream paper exemptions. Cut v0.7.5 with maintained release API, regenerated the five claim documents and refreshed README in e0633e233. Release-impact check against d33 has no errors. Focused release/date/claim checks: 103 passed, 13 exhaustive cases deliberately deselected, 14.82s. An earlier accidentally broad invocation was interrupted after 109 passes/175.93s and retained; no full-gate success claim. Combined News/original-date/native-layout checks: 146 passed in 47.20s. Pushed current head to PR617; senior/correctness follow-up and current-head hosted CI remain pending. The prior old-data pool complement also finished 3 passed in 838.09s; it does not establish the new adoption data.
