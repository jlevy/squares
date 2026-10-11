---
type: is
id: is-01m474970jceyrnd6gfejksmp5
title: "Import evand (no issue ask): exact certificates as verified ceilings at the 78 counts whose ceiling trails its report (13ee36e)"
kind: task
status: closed
priority: 2
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-05T22:52:19.858Z
updated_at: 2026-10-06T18:50:20.790Z
started_at: 2026-10-06T15:32:07.196Z
closed_at: 2026-10-06T18:50:20.789Z
close_reason: "T-101 merged in #389 (4148483da); #375 note posted (issuecomment-6023190825)"
resolution: null
duplicate_of: null
---
evand/square-packing 13ee36e (s12/search/exact/batch/certs) certifies 321 of the 324 register records exactly. Issue #375 asks only for the 48 that improve the register (T-098, think-t6ok); the author offers the rest as an independent exact replay of existing upper bounds and asks for nothing. But at all 78 counts where the record's verified upper bound now trails its reported side (after T-098), the source holds a certificate 1e-20 to 1e-14 above the printed side: rounded up at the printed precision it would carry the verified lane to the report, off the integer grid at most of them (by up to 0.464 at n = 101, 122, 145, 170, 197, 226, 257, 290, 291), including 16 counts n <= 100 (28, 29, 37, 39, 41, 50, 51, 53, 54, 55, 69, 70, 71, 83, 87, 88). The packet evand-square-packing-2026-10-05 pins those certificates by digest (only the 48 are retained) and receipts/first-party-check.json and source-replay.json already decide all 320 (n = 17 held, think-x4v4). An import would retain the 78 (about 1.5 MB), register them (one upper-bound entry or an evidence update per the runbook's table), and move the verified lanes through a layer like devtools.apply_exact_optima. Owner decision: whether the record acts on certificates the author did not ask to register.

## Notes

2026-10-06: merged onto main's branch and renumbered from the provisional T-118 to T-101 (8ffb6164f); PR opened.
