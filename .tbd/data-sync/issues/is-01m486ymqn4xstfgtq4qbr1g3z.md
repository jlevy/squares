---
type: is
id: is-01m486ymqn4xstfgtq4qbr1g3z
title: "Optional: source-checker replays of T-068's four unreplayed rectangle certificates (n = 66, 86, 87, 90)"
kind: task
status: open
priority: 4
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-06T08:58:13.621Z
updated_at: 2026-10-06T08:58:13.621Z
---
Optional, beside the rung: complete replays with the source's own checker (Tokoharu's verify.cpp via run_verify.py) of the four T-068 certificates no source-checker replay here has run on: rect_n66_L8385, rect_n86_L9365, rect_n87_L941 and rect_n90_L95775 (wand125 rectangle packet 2026-10-01). Upstream per-angle CPU: 3.15, 2.51, 2.63 and 2.45 hours, 10.7 in all; about 16 CPU-hours here at the 2 October ratio, so 8 to 16 hours of wall at 1 to 2 threads.

T-068 is already V3/C3 at all 34 counts on the sqverify-fast census route (lane R5, 6 October). These replays would add a reproduction with the producer's code for these four counts, as T-074 has for 29 others; they move no rung and no verified bound (later mixed certificates hold n = 66, 86, 87 and 90).

Commands, from packing/: `.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-01 --replay --n N --workers W --out DIR`, then `--merge DIR...` into resources/web/wand125-rectangle-certificates-2026-10-01/receipts/replay and `--check`.
