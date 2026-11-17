---
type: is
id: is-01m7khyh9zn4ssnwrqk014gn8r
title: "Import #1009: Polkovskyi's 13 exact certificates (lowered: 210, 260, 262, 268, 272, 292, 295; 12-place refinements: 147, 156, 180, 270, 299, 307) at Mishapolk/square-packing-records b637e6c (T-314 to T-326), adopt and regularize; merges after think-qag8's PR"
kind: task
status: in_progress
priority: 1
version: 7
delegate: w3-pass-1117r
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T01:29:08.671Z
updated_at: 2026-11-17T22:07:18.555Z
started_at: 2026-11-17T01:29:10.698Z
---

## Notes

2026-11-17 02:00Z c-import-1009-1117 (progress): packet mishapolk-issue1009-2026-11-16 written at b637e6c (b9b7fa7 pushed 23:27:18Z with the same certificate bytes, force-pushed over at 23:32:03Z); all 13 .cert and Witness/v2 digests match the issue and both SHA256SUMS; every exact side rounds up to the issue's print. Algebraic-house reader for 295 committed alone as 9d02ee33e (for I1 to cherry-pick). certify: 39 jobs, 7m34s wall, 10.4 CPU-min, all accepted/refused as expected; least wall clearance 1e-28 at every count. Sharp controls plan written and hashed before any sharp control ran: scratchpad i2/controls-plan-1009.md, SHA-256 49270cac7d988a8d46078935256fc8bd9bffe9ef5d1eb6f6ea10f70dc8f97142, 2026-11-17T01:59:51Z.

2026-11-17T21:55Z coord-intake-1117r: reclaimed from silent c-*-1117 lanes; delegated to w3-pass-1117r (worktree /home/user/wt/w3): map review-1005 (82fb63e88) into #1011, adopt and regularize 262/292/295, merge; then #1009 (import-1009 83232579c, review-1009 6a4f56b3d).

2026-11-17T22:10Z w3-pass-1117r (coordinator approved): #1011 maps R1's review (T-310..T-313 confirmed V3/C3) and STAGES de Winter's adoptions in select_houses.PENDING_ADOPTION under THIS bead, why 'next pull request': 262 -> T-312, 292 -> T-311 (replacing T-193's no-writer staging there; 292 taken off CORRECTIONS_OWED), 295 -> T-313. Reason: both PRs land on 18 Nov, one day's prior-state archive holds one state per count (268, 25-26 Oct), and #1009 is lower at all three (262 and 295 by 1.58e-3; 292 by 3.62e-9 = 72x #1006's own contraction margin 5.0288e-11, a new result under option D). THIS BEAD NOW OWNS THE HOUSE MOVES AT 262, 292 AND 295: if import-1009 stalls or a #1009 certificate fails validation, de Winter's adoption (T-312/T-311/T-313) must still be done, with both strong generators' regularization, in the next PR this bead lands; it must not be lost. The six citation deferrals of #1005-#1007's evidence now name think-i38n.

2026-11-17T22:20Z w3-pass-1117r (coordinator decision, supersedes the 22:10Z staging note): staging dropped. #1011 lands the registration only (T-310..T-313 at V3/C3 on the replay); R1's review (#1013) is NOT mapped there. THIS BEAD OWNS (1) mapping R1's review (docs/project/reviews/review-2026-11-17-ozden-de-winter-1005-1007.md) into T-310..T-313 together with #1014's review of #1009, and adopting the smallest validated packing at each count in the import-1009 PR (Polkovskyi's at 262, 292, 295 where it is smaller: 262/295 by 1.58e-3, 292 by 3.62e-9 = 72 x #1006's own contraction margin 5.0288e-11, a new result under option D); and (2) IF #1009 STALLS OR FAILS REVIEW, adopting de Winter's packings (T-312 at 262, T-311 at 292, T-313 at 295) with both strong generators' regularization in its own PR, so they are not lost. Mapping draft kept at scratchpad w3/r1-mapping-and-staging.diff and w3/map_r1.py (staging and check_standing parts to be dropped).
