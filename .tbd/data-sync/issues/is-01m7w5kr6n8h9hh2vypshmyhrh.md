---
type: is
id: is-01m7w5kr6n8h9hh2vypshmyhrh
title: "Import JoostdeWinter: GeiserX's public 259-square packing below the register, pointer (#1040)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: c7-pointers
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T09:46:42.260Z
updated_at: 2026-11-20T09:46:48.225Z
started_at: 2026-11-20T09:46:48.225Z
---
jlevy/squares#1040 (JoostdeWinter, 2026-11-19T04:54:13Z, no comments): Sergio Fernández Rubio (GeiserX) published a packing of 259 unit squares with side 16.590016439573 in GeiserX/squares-in-squares data/submission-best.csv.gz at f822b34 (CC BY 4.0), joining tilted bands from his 292- and 445-square packings; 0.00136 below T-193's 16.591378145498. Nevska reached the same side on Kaggle on 8 November 2026 without published coordinates (side-only, context). The issue attaches packing-259.zip, an exact rational Witness/v2 of the packing with a verifier, and asks that the packing be credited to GeiserX.

Stage 1 (c7-pointers, 2026-11-20): the source is retained at f822b34 as packet geiserx-squares-in-squares-2026-11-18 (attribution files, data/README.md, results/round33-best-2026-11-17.tsv; the 7.4 MB submission pinned by digest only). It carries binary64 rows only, no certificate and no exact coordinates, so nothing is imported from it. The attachment (user-attachments/files/35066502) is refused by this session's proxy with HTTP 403 and was not read. The result stays queued on this bead until a session that can read the attachment retains it (or the author commits it to a watched repository); then: replay on both maintained routes with sharp controls, measure against T-193's packing, walk the ledger at 259, register with credit to GeiserX as the issue asks (the results table credits his own k123 join of his held 292 and 445 packings).
blocked_on: jlevy/squares#1040
