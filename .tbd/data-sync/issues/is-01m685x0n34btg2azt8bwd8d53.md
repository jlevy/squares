---
type: is
id: is-01m685x0n34btg2azt8bwd8d53
title: "Validate #836: Karimi v5 two-strip rows the walk above 1024 records, both routes, six controls per K (~9.2 CPU-h)"
kind: task
status: in_progress
priority: 2
version: 5
delegate: bold-ritchie-l9
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m685wqakx05engdrvf9s4789
hold: null
hold_until: null
created_at: 2026-10-31T05:11:15.363Z
updated_at: 2026-10-31T17:14:05.384Z
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
- Machine note: about 2 cores for 4.6 wall-hours, or 1 core for 9; it can share the host with a gate if held to 1 core. Written-out certificates (~1 GB raw) go to scratch and are not retained.

## Notes

2026-10-31 bold-ritchie-l4: re-priced from measurement (karimi-records-2026-10-31/receipts/replay-sample-v5.json): near 9944 a count costs 14.7 CPU-s positive and 120 for six controls on both routes (1182: 1.2 + 10.2). Positives for the at most 3,918 recordable rows, scaled by n: about 9.7 CPU-h; six controls at one count per K (66 values): about 1.1; the checker over all 5,308 rows is done (212.9 CPU-s, receipts/two-strip-decisions-v5.json). Total about 10.9 CPU-h, under the 40 cap; six controls at every recordable count would be about 80, over it. The ingest dependency (a column set per deposit) is done on the branch. Still depends on R1 (think-llit) and R5 (think-5dc3).
