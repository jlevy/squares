---
type: is
id: is-01m5qvfqtde25k8jmdn7skvkpc
title: "W8: a maintained checker for the two-strip L-packing family (#799), with #799's packet and requests entry"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-w8-two-strip-1025
labels:
  - result-import
dependencies: []
parent_id: is-01m5qsa2jj6mf8cgemykzyy109
hold: null
hold_until: null
created_at: 2026-10-24T21:01:23.661Z
updated_at: 2026-10-25T05:02:04.690Z
started_at: 2026-10-25T04:16:26.129Z
---
Code slice from c-triage-799-1024's triage (scratch triage-799/: import-plan-799.md, scripts/, work/two-strip-decide.json). Decide a two-strip L-packing (Ryu's Theorem 1.3 shape: tilted rows on the bottom wall, tilted columns on the right wall, axis grid elsewhere, rational tan(a/2)) exactly from its parameters: strip lemma, region separation, capacity count; controls capacity+1, a side 1e-15 below the binding fit inequality, mH+1, tH=0 (W7's one-unit-below control does not carry over: slack >= 1.13e-8). Also stage 2: retain Zenodo 10.5281/zenodo.23624433 V1.0's 58,338 bytes (records.csv, README, regenerate.py as text) and the issue text as packet karimi-two-strip-2026-10-24, and add #799's result-requests entry (triage: pending). Rows wait for R1's walk above 1024 (think-llit). Price: checker < 0.1 CPU-h; exact replay of all positives on both routes plus six controls at one count per K about 0.8 CPU-h, run when the rows land.

## Notes

2026-10-25 c-w8-two-strip-1025 (W8): draft PR https://github.com/jlevy/squares/pull/808 (labels intake, S2), branch claude/w8-2026-10-25-two-strip-checker, head ff752564b (main bb756e193 merged at 52c7b2ce3). Checker packing/devtools/two_strip_checker.py: strip lemma (lattice (s,c),(1/c,0); along the axes (N, dj + N s/c)), the two fit inequalities, capacity sum floor((W - e - x0_j) c) + 1 + (K - mV)(K - mH), all Fractions; 7 controls (capacity+1; side 1e-15 below the binding fit; mH+1 at capacity; tH=0; tV=1; K+1; unknown kind); write_out builder; custody by file names only (OR-16), written-out certificate digests allowlisted as generated-artifact in integrity-ceremony.yaml. Decides all 683 rows (receipts/two-strip-decisions.json, 6.8 CPU-s): surplus 0 at 403, max 19; least slacks 1.132e-8 (H), 1.358e-8 (V); 4,781/4,781 controls refused. Replay sample 1184/1193/1813/2363/3775 (receipts/replay-sample.json): both couzo_678_replay routes accept, 6/6 controls refused by both at each (30/30), 2,850-8,688 pairs; 49 s wall at 2 workers. Ryu Theorem 1.3 at equal bands: capacity >= N(k,b) for all 2 <= b < k <= 40 (equal at 15, larger at 726). Packet packing/resources/web/karimi-two-strip-2026-10-24 (capture_web_source zenodo 23624433; README.md, records.csv, regenerate.py as text, issue_text-1.md; acquisition/issue-799.json; 683 written-out certificates, 56,229,853 bytes, pinned by SHA-256 only). result-requests #799 added, triage pending, queued on think-5dc3, blocked_on think-llit, read_through 20:08:23Z. Methods-survey no-change record for result-requests.yaml + frontier README (43 files identical three ways). NEW SINCE TRIAGE, not retained or triaged: #799 comments 22:09:22Z (theorem preprint 10.5281/zenodo.23627827) and 22:34:47Z (Zenodo V2, record 23628190, 2,824 rows at 1184-9944, created 22:32:58Z). Read-only: V2 regenerate.py byte-identical to V1's; checker decides all 2,824 with every control refused; at V1's counts V2 is identical at 682 and lowers 2459 by 4e-8 (same parameters). Acknowledgement draft updated in think-5dc3's notes.
