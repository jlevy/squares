---
type: is
id: is-01m7nx9kh2jdcesj1b3z9qyh1k
title: "Import #1018: Joost de Winter's raised lower bound for n = 108 and n = 109 (side 10.630037940829): triage the claim's kind and certificate, then stages 1-3"
kind: task
status: in_progress
priority: 1
version: 4
delegate: w6-dewinter-1118
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T23:25:54.594Z
updated_at: 2026-11-18T01:50:11.067Z
started_at: 2026-11-18T01:19:03.018Z
---

## Notes

### R-108 (blind review)

2026-11-18T01:50Z, lane r108-1118 (blind stage 4 review of #1018, branch claude/intake-2026-11-18-review-1018 in /home/user/wt/r108). Started: issue body read (REST, 01:34:16Z), source cloned at cc20a268 (lower_n108 only, blobless). Writing the checker and controls plan; nothing frozen yet and no program of this lane has read a certificate.

2026-11-18T01:50Z w6-dewinter-1118: triage of #1018 (read-only): a LOWER bound, s(109) >= s(108) >= 1700799526134255846599/159999384348528500000 = 10.6300379408297..., the 109 by monotonicity. Certificate retrievable at cc20a26 lower_n108/: evidence/n108_measure.json.gz, format M on a declared net (step 83/80000, last 400, B = 12487/12500), Hosono's mixed_n108_L1062 (T-216) with every rectangle times 1063/1062 and masses kept (L = 1063/100); 12 archived sqverify-fast partial runs (266,337,510 nodes), built from this repository's crate, source d97758bb (reviewed for declared nets); the bundled crate is file-for-file this repository's packing/sqverify_fast. Evidence kind: measure-capture certificate (computational), plus a one-page rational enlargement from 10.63 to the claimed side (scale by u = 2Bw(D/2), shift by h(1-u), h = 707107/1e6), which goes beyond SOUNDNESS.md's claim and needs the review. Stage 4 path: lower bound, not the house rule; the census replay at 401 directions (priced about 1.2 CPU-h from T-216's 136M nodes in 2087 CPU-s) plus whole-net controls (about 1 CPU-h), well under the 40 CPU-h cap, in the pass; the verified lanes at 108 and 109 move only with an accepted stage 4 review (R-108). Branch claude/intake-2026-11-18-import-1018, worktree /home/user/wt/w6-import-1018. Controls plan written before any program decided the certificate: packing/resources/web/de-winter-s108-lower-bound-2026-11-17/receipts/controls-plan-108.txt, SHA-256 52296592615bbedfa2742900123b994812c1ae4f406d74d1caf8e2e58f9ed37a, hashed 2026-11-18T01:49:49Z.
