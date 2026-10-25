---
type: is
id: is-01m5rqxg0k8jtafadgszs35wjg
title: "PR #808 (merge): senior review A of W8 (two-strip checker, #799 packet)"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-808-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5qvfqtde25k8jmdn7skvkpc
hold: null
hold_until: null
created_at: 2026-10-25T05:18:14.547Z
updated_at: 2026-10-25T05:37:11.101Z
started_at: 2026-10-25T05:18:18.896Z
closed_at: 2026-10-25T05:37:11.100Z
close_reason: "Review A of #808 posted (issuecomment-6393980469): approve once A1 (ingest hardening) and A2 (triage: done) are addressed; addressed by c-w8-two-strip-1025."
resolution: null
duplicate_of: null
---

## Notes

2026-10-25 c-rev-808-1025: Review A (senior, round 1) posted as a PR comment at head ff752564b, base bb756e193: https://github.com/jlevy/squares/pull/808#issuecomment-6393980469. Verdict: approve once A1 and A2 are addressed; no Blocker or High. Findings: A1 Medium (records.csv ingest checks literals but not the header, row shape or sizes: a duplicated column wins silently; K=10^12 with n=1 is decided and write_out materializes every square), A2 Medium (requests entry triage: pending contradicts its mapped claim; check_requests --draft 799 says 'claims are not yet mapped'), A3 Low (the mH+1 control depends on the data; replace with K+1, mH+1, mV+1, refused 683/683), A4 Low (summary wording: 'Each square has an exact side'; 'least earlier statement' should be 'numeric'), A5 Low (plan R5 scope and price ignore V2). Suggestions A6 to A8. Lemmas proved; independent exact cross-check at 3555, 1729, 3762, 1410 agrees; near-misses at real fits genuinely overlap; Zenodo bytes re-verified. Scratch: /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/rev-808/.
