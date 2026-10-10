---
type: is
id: is-01m4jk49cwm1b2prnhb3yrnztn
title: "Import Guzhou0806: s(40) > 335427/50000 from wand125's rect_n40_L67 density with a clipped-corner estimate (#485)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:25.852Z
updated_at: 2026-10-10T10:20:22.968Z
started_at: 2026-10-10T09:49:28.112Z
---
Issue https://github.com/jlevy/squares/issues/485 (opened 2026-10-10). Claim: s(40) > 335427/50000 = 6.70854, unrestricted rotations, above the case's reported and verified 67/10 from wand125's rect_n40_L67 (#281). Also a weaker full-core bound s(40) > 67000 sqrt(6400006889)/798988091 > 6.70848908. Source Guzhou0806/n40-square-packing at e5abeb4d078a5c5b35df6204dd9b93378e5a7880, release n40-670854-20261010, n40-670854.zip SHA-256 dbefee8658dc8f7d2e4a6ed21b0c3cd29f36ae393405a218f6bbfdce54465bc5. Rust nodal verifier, 401 directions, 32,970,910 nodes; wand125 commented a review on 2026-10-10 reporting a clean replay. Stages 1-3 on this pass; mathematical review of the clipped-corner estimate and strictness argument by Fable at max.

## Notes

## Stage 1 triage (mathematical lane, 2026-10-10)

Pin: Guzhou0806/n40-square-packing at e5abeb4d078a5c5b35df6204dd9b93378e5a7880 (commit 2026-10-10T06:47:01Z; tag n40-670854-20261010 -> that commit; release published 06:50:59Z). ZIP n40-670854.zip 203,095 bytes SHA-256 dbefee8658dc8f7d2e4a6ed21b0c3cd29f36ae393405a218f6bbfdce54465bc5 (checked). ZIP == tree except results/verification.json and results/nodes.jsonl (ZIP holds the CI receipt, source_commit e5abeb4d; tree holds the local one, source_commit null; the 401 rows identical apart from timing). CI run 38032128403: success on e5abeb4d.

Claims the release makes: (1) s(40) > 335427/50000 = 6.70854, unrestricted rotations, strict; (2) s(40) > 67000 sqrt(6400006889)/798988091 > 6.70848908 (full-core, no density peak); (3) the nodal statement: every side-9977/10000 square at each of 401 directions theta_j = 2 atan(j 83/80000) in K captures >= 10001/10000 of wand125's rect_n40_L67 density (its SHA 71011d03... is the retained 2026-10-01 packet's byte for byte); (4) g <= H = 2818711359413/10^9 a.e.; (5) chi >= 99979/100000, 40 chi - M = 1/625. No packing, optimality or priority claim; producer label CODE_DISTINCT_FULL is not a rung.

Register mapping (result-import.md table): a bound the record does not hold at n = 40 -> one new lower-bound entry (T-NNN to be assigned) on wand125's rect_n40_L67 density, claim naming both bounds, the full-core one as the weaker corollary with fewer hypotheses. Nobody else holds either value: the register's best at n = 40 is 67/10 (T-068); no later wand125 packet retained here has an n = 40 certificate; Kingbird lists packings only. wand125's issue comment (a third run of the entry point and an independent exact check of the transfer) is third-party evidence on the issue, not retained.

Priced validation plan: (a) nodal: sqverify-fast (first-party; the release vendors the crate at ef79288a4 byte for byte = HEAD, source d97758bb..., reviewed 6 Oct) on the regenerated 401-node input (SHA 49f696a4..., reproduced here from the retained candidate): 401 directions, 32,970,910 boxes, source reports 60 s wall at 4 threads / 235 CPU-s; expect 2-3 min at 2 threads -> minutes, same-branch stage 4. (b) finite: first-party exact script, 5 s (the review's exact_checks.py is the measurement; a devtools tool is the deliverable, OR-1). (c) controls priced at seconds (eight listed in the review). (d) a second method for the nodal step: Tokoharu's verify.cpp at 401 angles, ~2x its 201-angle cost (6,521 s wall upstream) plus an input generator for a finer net (W7) -> owner budget. Decides without the source's code: yes, (a)+(b) use no code of the release (finite.py is the source's; sqverify-fast is ours). Census-route caveat: net_directions/net_step/rectangle_control do not read a format T metadata net (GN-5) -> direct binary run plus a first-party control evaluation until a small driver change lands.

Draft acknowledgement (no T-NNN, no rung): "Received, thank you. We have pinned Guzhou0806/n40-square-packing at e5abeb4d (release n40-670854-20261010; n40-670854.zip, SHA-256 dbefee86...) and read the issue and wand125's review. The claim s(40) > 335427/50000, with the weaker full-core bound s(40) > 67000 sqrt(6400006889)/798988091, is mapped as a new lower-bound result at n = 40 on wand125's rect_n40_L67 density, whose retained copy here has the SHA-256 you give. What will be checked: the 401-direction nodal statement with this repository's sqverify-fast (the crate you vendored, byte for byte), the density's expansion, mass and essential supremum, and the transfer's scalar chain in exact rationals, each with mutation controls; the transfer argument, the reference-square legality, the clipping bound and the strict endpoint have been read in a mathematical review, which found no blocking defect. The replay is priced at minutes. The register entry and its ratings follow the replay."

## Stage 4 mathematical review (summary)

Record: docs/project/reviews/review-2026-10-10-guzhou-n40-clipped-corner-bound.md (mapped). Verdict: no blocking defect in the mathematics. Re-derived: the D4 fold per parent; the case split (upper node within delta0 = 2 atan h -> reference inside the parent; else lower node with error < beta = 2 atan((D-h)/(1+Dh)), legal because B <= q and cos+sin increases on [0, pi/4]); the clipped-corner bound e^2/(2cs) by the vertex cone and subadditivity (PROOF.md's "four disjoint triangles" holds here but is not needed, GN-1); monotonicity 2(z-a)(az-1)/(z^2-1)^2 >= 0; g <= H a.e.; counting 40 chi > M; strictness by compactness and attainment; the full-core bound's closed form.

Checked by computation here (exact rationals, own code): 480 rows, M = 3999/100, 3840 terms / 3792 distinct, D4 invariance; ess sup g = 2818.71135941178... <= H, H - ess sup = 1.215e-9, rounded-up method returns H exactly; q >= B; B(cos d0 + sin d0) <= q with slack 1.63e-15 (h is 8.2e-16 below its limit, GN-2); b, A = 1.09967e-7, HA = 3.0996e-4, chi = 0.99979003557 >= 99979/100000; 40 chi - M = 1.6014e-3; (L/gamma)^2 = 28729630924721000000/638381969559824281 = (67000/798988091)^2 6400006889; derived input SHA 49f696a4... reproduced; receipts consistent (401 rows verified, least bound 1.000100000471634 at r = 73); even-index rows identical to the retained 3 October census rows at all 201 indices; adversarial scan of 600,401 orientations and 200,001 corner placements found no failure of the case split or legality; built the reviewed binary 567a0fd5... and reproduced directions 0, 1, 73, 220, 383, 400 field for field; controls: weights x 99/100 refused at 73 and 220, near-threshold mutant refused at 220, metadata removed -> standard net (another claim), angle_count 201 with D 83/80000 -> admission refuses; sqpack.rectangle_density agrees with the crate's probe at the control centre (least exact capture 1.0013165658 at r = 220). Same transfer on the 201 net: chi < 0 (refused); at X' = 335428/50000: 40 chi - M = -0.00998 at the best h (refused).

Not checked here: the complete 401-direction run (source, CI and wand125 report it); the crate's lemmas beyond the admission path (3 and 6 Oct reviews); the toolchain.

Findings: GN-1 proof text (triangles unconditional), GN-2 h at the limit (exact arithmetic only), GN-3 ZIP != tree in results/ (retain both receipts), GN-4 classification (nodal replay = reproduced with the producer's code, which is ours; finite = independently re-implemented), GN-5 census tooling ignores format T metadata nets (blocks the census route only; W7), GN-6 the format T metadata-net path has no retained review of its own (admission read here; lemma N0 covers it), GN-7 n-040.md body still says 6.695. Significance suggested S3 by T-099's precedent (technique new to the record). Replay contract with commands, expected outputs and eight controls is in the review.
