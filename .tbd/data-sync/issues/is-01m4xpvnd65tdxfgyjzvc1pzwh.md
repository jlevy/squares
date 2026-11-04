---
type: is
id: is-01m4xpvnd65tdxfgyjzvc1pzwh
title: "Validate: wand125 s(145) >= 306/25 (mixed_n145_L1224), linear replay of all 201 angles and linear-control (~37 CPU-h, range 24-64; stop at 40)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: bold-ritchie-l32
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
hold: null
hold_until: null
created_at: 2026-10-14T17:20:16.293Z
updated_at: 2026-11-04T06:00:34.655Z
started_at: 2026-11-02T19:05:32.040Z
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

## Notes

2026-11-02 bold-ritchie-l32 (intake lane L32, epic think-3guf; branch claude/bold-ritchie-xo28us-l32, draft PR #889): the preparation slice is done (commit 1e13a0571). fine_net_followup retain held certificates__mixed_n145_L1224.tar.gz (38,598,220 B, 6a937dc7...2a49, equal to the pin) and copied candidate.json (516,199 B, 3cd54c43...) and certificate.json (39,867 B, e3c58aa2...92ca) to the packet's release/ as deterministic gzip; the proof bundle n145-L12.24-proof-bundle.tar.gz (47,407,937 B, 4dc4f673...0a0b) is pinned by digest in acquisition/release-assets.json (PINNED_MEMBERS now names linear proof bundles); check-retained 0 problems. audit_wand125_linear registers it as n145 (root square-packing, directory problems/square-lower-bounds/certificates/mixed_n145_L1224): linear_tree adds the release members to the pinned tree, retained_path reads release-held files, tarball_pin falls back to the release record, and release_bundle takes the asset (supplied or fetched from the release), holds it to its pin and copies out the bundle. linear-audit for the packet: exact premises hold from the retained bytes (124,435,707 nodes; receipts/linear-audit.json). linear-fetch n145: BUNDLE_READY, 810 bundle files bound, 202 checker copies, all 201 inputs enclose the candidate (receipts/n145/fetch.json, 19:24-19:25Z, about 1 CPU-minute). Tests: test_wand125_linear_certificates.py and test_fine_net_followup.py 112 passed. The replay (linear-replay n145 --range 0-200 --workers 2 --stop-after-hours 17.8, nice -n 19) is queued after T-176's census in a detached queue, with linear-merge and linear-control after it only if the range completes; the stop keeps the lane under its 40 CPU-hour cap.

2026-11-04 bold-ritchie-l32: the first replay run (from 2026-11-02T20:51Z, two workers) replayed 50 of 201 angles, each LINEAR_ANGLE_REPLAYED with the certificate's own record (73,124 CPU-s in rows), before the container restarted at about 2026-11-03T07:51Z with two angles 30 s in flight (at most 59 CPU-s lost). Receipts committed at b61832a10 (16 angles) and 3308870e0 (50 angles and the second run's header). Lane ledger under the 40 CPU-hour cap, upper bounds: T-176 capture 11,404.3 + control <= 922; preparation (two linear-fetch, linear-audit, capture-agreement, retain) <= 160; T-179 run 1 preparation 72 + rows 73,124 + lost 59: 85,741 CPU-s spent, 58,259 left. Resumed 2026-11-04T04:58:17Z (run 2026-11-04T04:59:38Z-4304, 151 angles to do, bundle re-pinned and re-bound, all inputs enclosing the candidate) with --stop-after-hours 7.78 at two workers, which keeps the replay, a worst-case in-flight overrun and the linear-control under the cap. Measured ratio to the source's CPU: 1.189 over the first 50 angles (1.10 over the last 20); the 151 left are 47,820 source-seconds, about 52,600 to 56,900 CPU-s here.

2026-11-04T06:00Z bold-ritchie-l32, progress (live; claim held): lane CPU against the 40 CPU-hour cap, upper bounds: 24.9 CPU-h recorded (T-176 census 3.17 + control <= 0.26; preparation <= 0.04; T-179 replay 21.38 in receipt rows, run preparations 0.04, 59 s lost at the 3 November container restart) plus about 0.5 in flight. T-179 (think-v511): 56 of 201 angles replayed, every one the certificate's own record; resumed 2026-11-04T04:59Z at two workers; 145 angles left, about 14.2 CPU-h at the measured 1.17 of the source's CPU, then the route's control (minutes), about 39.2 of 40 in all. Expected replay finish about 14:00 to 16:00Z today on this shared host (load near 10), then merge, control and records in PR #889; if the cap arrives first the replay stops there and is recorded as partial. T-132 (think-r333): not run in this lane, as recorded on 2 November: the cap goes to T-179, and its census evidence waits on the stage 4 review think-1lri; its inputs are retained (219bc1268) and its record corrected (df08c632b).
