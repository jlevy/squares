---
type: is
id: is-01m4pfeqkmdtcze4v746vtn23v
title: "Import wand125: register #446's s(19) >= 1931/400, s(20) >= 393/80, s(26) >= 1111/200, s(27) >= 1131/200 as reported (#446)"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-11T21:56:11.508Z
updated_at: 2026-10-12T07:57:27.372Z
---
Found by the 2026-10-11 wand125/evand survey (think-1jnr). wand125/square-packing INDEX.json at 04fbef0 (2026-10-11) lists, as its best certificate at four counts, the #446 fine-net bundles mixed_n19_L48275 (1931/400 = 4.8275), mixed_n20_L49125 (393/80 = 4.9125), mixed_n26_L5555 (1111/200 = 5.555) and mixed_n27_L5655 (1131/200 = 5.655, the bf85d6b follow-up), all on the 2,073-direction net, data in release square-lower-bounds-v1. The record holds them only as evidence (E-wand125-fine-net-lower-bounds-446-report, E-wand125-fine-net-n27-5655-followup-report), #446's result-requests entry and case-record blockers; no register entry states them, unlike the same release's n = 28, 29, 30 values (T-142, T-132, T-143). Each is above its case's reported and verified lower bound (by 1/400, 3/400, 1/100 and 23/2000) and above every register claim at its count (T-103, T-104, T-105, T-106). Runbook row: bounds of one kind at several counts in one release, one entry whose scope covers them, registered as reported (V0/C0, pending adoption) with unfinished_confirmations naming think-ndvg's replay. Price: registration minutes (records lane); replay about 3.3 to 4.5 CPU-hours per certificate on the T-142/T-143 measurements, so about 13 to 18 CPU-hours for the four, under think-ndvg's owner budget.

## Notes

Overlap: think-dc0p (in_progress since 2026-10-06, unlabelled, no notes) names the n = 19 value with three superseded ones from square-packing-bounds f8e0178; #446's import (PR #450, think-ndvg) superseded it. Owner of the replay: think-ndvg. This bead owns only the registration (one entry, scope n = 19, 20, 26, 27), for the records lane.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/446; its 2026-10-12 reply (https://github.com/jlevy/squares/issues/446#issuecomment-6116243055) does not yet mention this registration. Listed on the tracker https://github.com/jlevy/squares/issues/544.
