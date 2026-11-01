---
type: is
id: is-01m685x0n34btg2azt8bwd8d53
title: "Validate #836: Karimi v5 two-strip rows the walk above 1024 records, both routes, six controls per K (~9.2 CPU-h)"
kind: task
status: in_progress
priority: 2
version: 8
delegate: bold-ritchie-l9
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m685wqakx05engdrvf9s4789
hold: null
hold_until: null
created_at: 2026-10-31T05:11:15.363Z
updated_at: 2026-11-01T00:53:57.145Z
started_at: 2026-10-31T17:14:05.383Z
---
Stage 4 validation of #836's rows (import think-7yrs), the rows think-llit's walk above 1024 records from Mohsen Karimi's two-strip v5.0 deposit.

blocked_on: think-7yrs, think-llit

## Validation
- Claim: each recorded row's s(n) <= S at the exact side records.csv states, Zenodo 10.5281/zenodo.23664800 v5.0 (karimi_two_strip_records_v3_lite.zip, SHA-256 9c70c4d8...6325 as #836 states it), decided by devtools.two_strip_checker from the row's K, mH, tH, phH, mV, tV, phV; at most 3,918 rows (2,484 new counts and 1,434 lowered), as the walk decides.
- Run: from packing/, two_strip_checker decide over every v5 row with its seven controls (receipt beside W8's two-strip-decisions-v2.json); the write-out of every recorded row and both maintained exact routes on it; six controls on both routes at one count per K (66 values of K). First measure one count near 9944 on both routes with its six controls and re-price.
- Cost: about 9.2 CPU-h (checker 0.035; positives 8.3 at 7.6 CPU-s a row; controls 0.9). Basis: W8's receipts (67 CPU-s for 2,824 rows decided) and R5's extrapolation (5.95 CPU-h for 2,825 rows, past the 3775 sample). An estimate until the 9944 measurement.
- Budget status: gated on decision and dependencies (the deposit's retention, which needs zenodo.org; R1's walk); within the 40 CPU-h item cap.
- Possible subset under the cap: not needed; the whole item fits. Six controls at every recorded count would be about 75 CPU-h, over the cap.
- Depends on: think-7yrs stage 2 (zenodo.org reachable, or the owner fetches the zip); a column set per deposit in two_strip_checker's reader, since parse_records refuses v5's extra below_all_reported column (review A2 of #848; code time, seconds of compute); think-llit R1 (the walk above 1024); R5 (think-5dc3), with which these rows land.
- Done when: the decisions receipt and the replay receipts are committed in the packet, the rows are in source-coverage.yaml at the walk's verdicts, and check --replay passes for the release.
- Stage 3 items (review A10 of #863, 2026-11-01):
  - the recorded v5 rows cite karimi-records-2026-10-31/receipts/replay-v5.json (the full replay, PR #863) as their route evidence;
  - devtools.two_strip_checker is registered in frontier/verifiers.yaml at b0fe65eae, the commit the full replay ran from, beside couzo_678_replay (already V-couzo-678-replay).
  Both are R5's (think-5dc3) to carry out when it records the rows.
- Machine note: about 2 cores for 4.6 wall-hours, or 1 core for 9; it can share the host with a gate if held to 1 core. Written-out certificates (~1 GB raw) go to scratch and are not retained.

## Notes

2026-11-01 bold-ritchie-l9: THE FULL REPLAY IS DONE (PR https://github.com/jlevy/squares/pull/863; receipts f266dba91, head 4338e85f8 after merging main 737d8311e). All 5,308 v5 rows' certificates written out by two_strip_checker.write_out pass both maintained exact routes of devtools.couzo_678_replay (5,308 of 5,308 by sqpack.verify's predicates and by the independent checker's), each the certificate the decisions receipt names by SHA-256; at the 66 controlled counts (one per K, CONTROL_RULE) both routes refuse all six controls, 396 of 396 each. 31,499,439 squares and 71,808,283 candidate pairs decided (70,690,393 touching; least wall clearance and least pair gap 0, the closed contract). CPU: 47,031.4 s = 13.1 CPU-h (positives 12.1, controls 0.9), two workers at nice 5, 17:08:54Z to 23:54:32Z on 31 October; under the 40 CPU-h cap; above the 10.9 priced, since the positives cover all 5,308 rows rather than the at most 3,918 recordable. Receipts: karimi-records-2026-10-31/receipts/replay-v5/k035.json..k100.json (66, at most 169 lines each, plain JSON per the family's convention since think-rsqv has not landed) and receipts/replay-v5.json (summary); `two_strip_checker check` reads them back (0.34 CPU-s). Recorded as stage 4 evidence in the packet README (Decided Here) and #836's entry (summary, rows-v5 not_registered). NOT done, by the brief: no row in source-coverage.yaml, no frontier evidence entry (none exists above 1024; R1/R5 write them with the rows), no `check --replay` for the release. Remaining for this bead's Done-when: stage 3 (think-llit R1, the owner's D4; R5 think-5dc3) records the rows at the walk's verdicts and cites these receipts. The walk records at most 3,918 of these 5,308; this replay covers whichever it picks.

2026-10-31 bold-ritchie-l9 (lane L9 of think-3guf; PR https://github.com/jlevy/squares/pull/863, branch claude/bold-ritchie-xo28us-l9): the full replay of all 5,308 v5 rows is running, ahead of the walk (no row is recorded; stage 3 waits on think-llit's R1 and the owner's D4). Tool: `python -m devtools.two_strip_checker replay-all --version 5 --workers 2` (commit b0fe65eae), one job per row on both maintained exact routes of devtools.couzo_678_replay, with the routes' six controls at one count per K (CONTROL_RULE: the least fit slack, then the smallest count; 66 values of K). It writes karimi-records-2026-10-31/receipts/replay-v5/kNNN.json per K as each K completes and receipts/replay-v5.json (the coverage summary) once all 66 are in; `two_strip_checker check` reads them back. RESUMABLE: if the container restarts, rerun the same command from packing/ on the branch; it skips every K whose receipt names its rows. Receipts are committed and pushed as they land (K = 35 to 50 in b0fe65eae). Re-priced from the first 254 rows (cost ~ n^1.06): about 12 CPU-h for all 5,308 positives plus the 66 controlled counts, at two workers about 6 wall-hours. Log in the lane's scratch, out of Git (OR-18). think-rsqv (gzip receipts over 1,000 lines) has not landed; each per-K receipt is under 1,000 lines (at most 134 rows a K), so none is a retained_data candidate.

2026-10-31 bold-ritchie-l4: re-priced from measurement (karimi-records-2026-10-31/receipts/replay-sample-v5.json): near 9944 a count costs 14.7 CPU-s positive and 120 for six controls on both routes (1182: 1.2 + 10.2). Positives for the at most 3,918 recordable rows, scaled by n: about 9.7 CPU-h; six controls at one count per K (66 values): about 1.1; the checker over all 5,308 rows is done (212.9 CPU-s, receipts/two-strip-decisions-v5.json). Total about 10.9 CPU-h, under the 40 cap; six controls at every recordable count would be about 80, over it. The ingest dependency (a column set per deposit) is done on the branch. Still depends on R1 (think-llit) and R5 (think-5dc3).
