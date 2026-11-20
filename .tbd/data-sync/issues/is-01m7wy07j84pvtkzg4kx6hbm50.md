---
type: is
id: is-01m7wy07j84pvtkzg4kx6hbm50
title: "Import #1039, #1041, #1042: Joost de Winter's raised lower bounds (56 + 34 + 48 counts, 19-218), Hosono-style rectangle measures with coverage proofs; triage, retain, replay within the compute cap"
kind: task
status: in_progress
priority: 1
version: 5
delegate: c15-lower
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T16:52:57.032Z
updated_at: 2026-11-20T17:40:01.789Z
started_at: 2026-11-20T16:53:54.029Z
---

## Notes

## Lane c15-lower (2026-11-20)

Stage 1 done: draft PR #1051 (branch claude/intake-2026-11-20-lower-1039, head 133014bf78). Packet de-winter-lower-bounds-2026-11-19 at JoostdeWinter/square-packing 21d944c (text retained, measures/receipts/zip pinned by digest; both attachment URLs refused by the proxy; the 1039 zip is byte-identical in the folder, digest 9641ca15...). Report-order receipt campaign/issue-intake/lower-bounds-de-winter-20261120/ (devtools.lower_bound_claims): 139 claims all above the record; current 73 (1039: 23 + 7 consequences; 1041: 105, 111; 1042: 47; 161 comment), superseded 59. The 155-count comment on 1042 is think-4iec.

Control plan (17:39:53Z, before any replay it names): packing/resources/web/de-winter-lower-bounds-2026-11-19/receipts/controls-plan.txt, SHA-256 cc6a1bf43e33182bbdc448876ed5e730787e17262c0be6ad854de0ce76589f8e. Compute plan: about 17 CPU-hours central (34 at the upper estimate): 1041 ~2.4, 1042 ~6.6 (+ envelope arithmetic), 1039 ~8 (integer directions ~6.6, heterogeneous ~1, mixed ~0.5); each item under the 40 CPU-hour cap. The 1039 "existing source coverage" rows (sqverify-format receipts, 14.2G nodes, ~67 CPU-h if re-run) are not replayed: compared with the record's census receipts instead.
