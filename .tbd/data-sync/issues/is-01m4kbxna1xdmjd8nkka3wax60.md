---
type: is
id: is-01m4kbxna1xdmjd8nkka3wax60
title: "Import wand125: s(122) >= 563/50 by the mixed_n122_L1126 linear certificate, raising n = 122 to 126 (no issue)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:56:43.073Z
updated_at: 2026-10-10T17:45:34.765Z
---
Found by the 2026-10-10 evening reads (think-0nkn): wand125/square-packing a9f76c3 adds problems/square-lower-bounds/certificates/mixed_n122_L1126/, a linear certificate (502 points, 1,268 segments, 3 rectangles, mass 12199999/100000) on mixed_n101_L1028's 201-direction net (core 9977/10000, step 83/40000), checked by unified_linear_verify.cpp (SHA-256 0249726a..., V-wand125-unified-linear-verify-cpp, the T-080 route). Reports s(122) >= 563/50 = 11.26, hence s(N) >= 11.26 for N >= 122: above Green's reported 11.22928087555 at 122-125 and Nagamochi's 11.24695076595 at 126, and the verified Karakus strip bounds at 122-126; 127's 11.29563 stands. Data: square-lower-bounds-v1 asset certificates__mixed_n122_L1126.tar.gz (31,784,537 B, SHA-256 6443eae03c56dc99051965246dbf97f5f3540feb9c011eac96e6d094521f5deb). The author's full replay took 7 h 41 min at 3 workers (about 23 CPU-hours): stages 1-3 only; the replay waits for an owner budget. No issue reports it.

## Notes

2026-10-10 stages 1-2 (intake sub-agent, branch worktree-agent-afd0e09abab917b31 from claude/determined-rubin-yjfy2a 1e642dc88): tool commit a7bf259c8, packet commit 00dc1a204 (packing/resources/web/wand125-linear-n122-2026-10-10/).

Pin: mixed_n122_L1126 at a9f76c382d023b4095899c4eb7ea7483b8b87ecf (committed 2026-10-10T10:41:36Z), unchanged with its MIT LICENSE through head 27ed16885a3ac64c2a22c992f5375574ccf3ff16. Asset certificates__mixed_n122_L1126.tar.gz (31,784,537 B, 6443eae0...5deb, asset 627696187) equals the API digest and ASSET.json; the release's SHA256SUMS (440 lines, updated 14:12Z) does not list it. 18 documents equal their commit blobs; all 13 code/ files are byte-identical to retained copies (7 in wand125-linear-certificates-2026-10-02, 6 in wand125-point-and-mixed-2026-09-28). The asset holds candidate.json, certificate.json and n122-L11.26-proof-bundle.tar.gz (38,912,523 B, 3986d902...55d0, the digest README and completion-audit.json state). Kept outside Git; the scratch copy was deleted.

Claim: s(122) >= 563/50 = 11.26 from 502 point, 1,268 segment and 3 rectangle orbits, mass 12199999/100000, core 9977/10000, 201 angles of step 83/40000 (T-080's net and checker 0249726a). By mass, s(N) >= 11.26 for N >= 122: raises the reported lane at 122-125 (Green 11.22928087555) and 126 (Nagamochi 11.24695076595) and the verified Karakus strip lane at 122-126; 127 (Nagamochi 11.29563, Karakus 11.28192) already holds more.

Premises (fine_net_followup linear-premises, the T-080 route's readers given files and digests): linear_certificate holds every exact premise (D4 invariance of 14,184 images, digest c91a7509..., positive centre domains, checker and code identity, 201 records with 73,694,735 nodes, source audit digests; side exceeds Green and Nagamochi at 122) in 1.7 s; bundle_bindings binds 810 files and 202 checker copies; check_inputs binds all 201 inputs to the exact candidate in 53.5 s. EXACT_PREMISES_HOLD; no source program ran.

Sample (fine_net_followup linear-sample: replay_angle and the shipped checker from the retained copies, compile_verifier binary 31351e22, two workers): angles 37 and 108 returned the certificate's records, 57.4 and 117.9 CPU-s against the source's 73.6 and 152.0 (ratio 0.776). Priced complete replay 40,278 CPU-s (by nodes 40,005), control at angle 37 172 CPU-s, total 11.24 CPU-hours, about 5.6 h wall at two workers; the author's own replay took 7 h 41 min at three workers (up to about 23 CPU-hours). A first-party complete replay needs n = 122 registered in devtools.audit_wand125_linear.LINEAR with a packet retaining the five small files (MIT permits it), then linear-replay over 201 angles, linear-control and a review. Waits for an owner budget.

Register: one entry at V0/C0 (T-NN placeholder) with scope n_values [122, 123, 124, 125, 126], as T-080 carries 101-105; pending adoption at all five, case lanes unchanged. Proposed results, evidence, coverage, bibliography, resources README and n-122..n-126 open items handed to the coordinator. No issue asked, so no reply is owed.
