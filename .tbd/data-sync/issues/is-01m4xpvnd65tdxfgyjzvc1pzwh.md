---
type: is
id: is-01m4xpvnd65tdxfgyjzvc1pzwh
title: "Validate: wand125 s(145) >= 306/25 (mixed_n145_L1224), linear replay of all 201 angles and linear-control (~37 CPU-h, range 24-64; stop at 40)"
kind: task
status: open
priority: 1
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
created_at: 2026-10-14T17:20:16.293Z
updated_at: 2026-10-14T17:20:16.293Z
---
Validation part of think-u0av for n = 145 (T-179 in the 14 October records PR #602, s(145) to s(149), V0/C1). Record-changing at 145-149.

## Validation
- Claim: s(N) >= 306/25 = 12.24 for every N >= 145 (raising 145 to 149) by the linear certificate mixed_n145_L1224 (594 point, 1,541 segment and 9 rectangle orbits under D4, mass 14499999/100000, candidate digest 31788dc7...ca69; net core 9977/10000, 201 half-angles of step 83/40000) at wand125/square-packing 22f06b31a9295c8185be5d30a1a7b19982b16847; release asset certificates__mixed_n145_L1224.tar.gz, 38,598,220 B, SHA-256 6a937dc7...2a49 (asset 636102989); checker code/unified_linear_verify.cpp 0249726a...a06d (V-wand125-unified-linear-verify-cpp).
- Run: first a preparation slice (code and retention, no compute): register mixed_n145_L1224 in devtools.audit_wand125_linear and retain candidate.json (516,199 B) and certificate.json (39,867 B, e3c58aa2...92ca) beside README.md, manifest.json and completion-audit.json in packing/resources/web/wand125-linear-n145-2026-10-13/ (MIT permits). Then, from packing/, `python -m devtools.audit_wand125_linear linear-fetch mixed_n145_L1224 --work DIR`, `linear-replay mixed_n145_L1224 --work DIR --range 0-200 --workers 2 --stop-after-hours H` (resumable receipts), `linear-merge mixed_n145_L1224`, and `linear-control mixed_n145_L1224 --work DIR` (the original and two mutations at angle 35).
- Cost: about 37 CPU-h: the source's 109,342 s summed over the net x 1.213, this host's ratio on angles 35 and 111 (546.1 vs 450.3 CPU s, 2026-10-14, receipts/linear-sample-diagnostic.json) = about 132,600 CPU s, plus about 500 s of control. About 24 CPU-h at the 0.776 idle-host ratio of the n = 122 sample; at most about 64 CPU-h by the author's own replay (2 h 8 min at 30 workers). No job is shorter than the axis angle, about 3,400 s here.
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h) on the 37 CPU-h estimate. The high estimate (64) crosses the cap, so run with --stop-after-hours so the total stops at 40 CPU-h, and ask the owner before resuming past it.
- Possible <= 40 CPU-h subset: n/a (runnable on its estimate; the stop above is the guard).
- Depends on: the preparation slice above. No owner decision.
- Done when: linear-merge reports all 201 angles replayed and matching the certificate's records, linear-control refuses both mutations, and the replay evidence is registered on T-179 with the 14 October review as the mapped review; noted on think-u0av.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 18.5 wall-h at two workers; run it in --stop-after-hours chunks outside gates.
