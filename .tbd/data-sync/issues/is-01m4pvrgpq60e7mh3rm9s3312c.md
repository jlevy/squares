---
type: is
id: is-01m4pvrgpq60e7mh3rm9s3312c
title: "check_requests: mark a reply due when a result is adopted on its case, superseded, or its issue gains a comment the record read"
kind: task
status: open
priority: 2
version: 2
labels:
  - packing
  - result-import
dependencies: []
created_at: 2026-10-12T01:31:15.030Z
updated_at: 2026-10-12T07:55:13.760Z
---
The owner's rule of 2026-10-11 (packing/campaign/result-import.md, Stage 7; codified under think-58lu): every issue a pass touches gets a comment, and every later change of its state a follow-up (imported, registered, confirmed or a defect found, adopted on its case, superseded, closed). devtools.check_requests --report (and the sweep's '#N owes a reply' items, which call it) derives replies due from ids, rungs, the four statuses recorded/reviewed/confirmed/incomplete, refuted, and 'outdated' statements (replies_due, _moved, _current). It does not see: a case record adopting a result (pending adoption to current), a supersession (render_recent_results.supersessions / result_status's position), or an issue whose new comments a pass read into its entry (read_through moved) with no reply since. The runbook now says the pass that makes such a change follows it up by hand. Done: replies_due reports each of the three, with tests in packing/tests/ for check_requests, and the reply schema's reported items can state the position (pending adoption / current / superseded) so a later move is detectable; result-import.md's After the Merge step 2 drops the by-hand sentence.

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/540 (label enhancement). Tracker https://github.com/jlevy/squares/issues/544.
