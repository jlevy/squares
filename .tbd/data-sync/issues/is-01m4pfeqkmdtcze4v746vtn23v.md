---
type: is
id: is-01m4pfeqkmdtcze4v746vtn23v
title: "Import wand125: register #446's s(19) >= 1931/400, s(20) >= 393/80, s(26) >= 1111/200, s(27) >= 1131/200 as reported (#446)"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-lower-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:56:11.508Z
updated_at: 2026-10-23T06:46:33.066Z
started_at: 2026-10-23T06:18:58.822Z
---
Found by the 2026-10-11 wand125/evand survey (think-1jnr). wand125/square-packing INDEX.json at 04fbef0 (2026-10-11) lists, as its best certificate at four counts, the #446 fine-net bundles mixed_n19_L48275 (1931/400 = 4.8275), mixed_n20_L49125 (393/80 = 4.9125), mixed_n26_L5555 (1111/200 = 5.555) and mixed_n27_L5655 (1131/200 = 5.655, the bf85d6b follow-up), all on the 2,073-direction net, data in release square-lower-bounds-v1. The record holds them only as evidence (E-wand125-fine-net-lower-bounds-446-report, E-wand125-fine-net-n27-5655-followup-report), #446's result-requests entry and case-record blockers; no register entry states them, unlike the same release's n = 28, 29, 30 values (T-142, T-132, T-143). Each is above its case's reported and verified lower bound (by 1/400, 3/400, 1/100 and 23/2000) and above every register claim at its count (T-103, T-104, T-105, T-106). Runbook row: bounds of one kind at several counts in one release, one entry whose scope covers them, registered as reported (V0/C0, pending adoption) with unfinished_confirmations naming think-ndvg's replay. Price: registration minutes (records lane); replay about 3.3 to 4.5 CPU-hours per certificate on the T-142/T-143 measurements, so about 13 to 18 CPU-hours for the four, under think-ndvg's owner budget.

## Notes

Overlap: think-dc0p (in_progress since 2026-10-06, unlabelled, no notes) names the n = 19 value with three superseded ones from square-packing-bounds f8e0178; #446's import (PR #450, think-ndvg) superseded it. Owner of the replay: think-ndvg. This bead owns only the registration (one entry, scope n = 19, 20, 26, 27), for the records lane.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/446; its 2026-10-12 reply (https://github.com/jlevy/squares/issues/446#issuecomment-6116243055) does not yet mention this registration. Listed on the tracker https://github.com/jlevy/squares/issues/544.
2026-10-23 c-lower-1023 (records lane of coord-intake-1023), branch claude/intake-2026-10-23-lower-bounds: registered as T-233 (V0/C0, recorded, pending adoption at n = 19, 20, 26, 27) in 7b90d47d2, over E-wand125-fine-net-lower-bounds-446-report and E-wand125-fine-net-n27-5655-followup-report, published 2026-10-08 (n19 and n26 first in 7400660 on 2026-10-07, n20 at 61e37d5, n27 at bf85d6b 2026-10-08T16:53Z; all four directories unchanged through head e48de24). Gains over T-103 to T-106: 1/400, 3/400, 1/100, 23/2000. #446's requests entry maps fine-net-n19, -n20, -n26 and -n27-5655-followup to T-233; the issue's n27 2261/400 is superseded in the same release and stays unregistered. #446 has no new author comment after read_through 2026-10-16T09:00:31Z (later comments are the project's replies of 19 and 20 October).
- Price (unfinished_confirmations, think-ndvg): the four assets downloaded (digests equal the #446 packet's) and their check2 receipts read: direction CPU 3,584 / 8,353 / 8,158 / 12,676 s (n19 at 6 threads, the rest at 12), 32,770 in all; twice over each net at this host's 0.689 ratio (think-wop1's n31 sample) is 12.54 CPU-h, 18.21 at the source's CPU. Per certificate: n19 1.37-1.99, n20 3.20-4.64, n26 3.12-4.53, n27 4.85-7.04 CPU-h. No replay runs in this lane; a census needs each candidate retained where it reads it first (fine_net_followup retain into a packet, as wand125-fine-net-n31-2026-10-11 does).

## Stage 7 draft for #446, after this branch merges (not posted)

@wand125, thank you. Four more of your fine-net lower bounds are now registered on `main`, as reported results:

- **T-233, V0/C0, recorded:** s(19) ≥ 1931/400 (`mixed_n19_L48275`), s(20) ≥ 393/80 (`mixed_n20_L49125`) and s(26) ≥ 1111/200 (`mixed_n26_L5555`) from this issue, with your 8 October follow-up s(27) ≥ 1131/200 (`mixed_n27_L5655`), which replaces the issue's 2261/400. Each is above its case's lower bound on `main` (T-103 to T-106) by 1/400, 3/400, 1/100 and 23/2000.

Until now the record held these four only as evidence entries. The case records do not change yet: n = 19, 20, 26 and 27 keep 193/40, 981/200, 1109/200 and 11287/2000 in both lower lanes until each certificate has a complete replay here.

Separately, your repository's `mixed_n31_L59775` (23e3186, 11 October), s(31) ≥ 2391/400, is registered as **T-232, V0/C0**. It goes above this issue's 597/100 by 3/400 and above the case's 2381/400 by 1/40. Its retained candidate and receipts are in `packing/resources/web/wand125-fine-net-n31-2026-10-11/`.

**What remains.** For each of the four in T-233: a complete `sqverify-fast` census at all 2,073 directions from a candidate retained where the census reads it, with the whole-net control (the 99/100 mutant at every direction), and a review that reads the certificate. From your check2 receipts we estimate about 12.5 to 18 CPU-hours for the four (`think-ndvg`). For T-232 the same census and review are under way. As with T-205 to T-207, a `sqverify-fast` replay here is a re-implementation that shares components with your checker, since `sqverify-proof-net` adapts this repository's crate.

This issue stays open while that work is queued, and a reply follows each change in the record.

(Before posting: confirm the ids are on `main`, update T-232's line to its state at merge (census, controls and review), and link the result pages.)
