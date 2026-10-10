---
type: is
id: is-01m4jk4a6jsy0cvkmbrwfcbk0n
title: "Import ebdeleeuw: s(70) <= 888096037156625096037155737/10^26, an exact refinement of Ryan Xu's packing (#483)"
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
created_at: 2026-10-10T09:43:26.674Z
updated_at: 2026-10-10T10:44:54.090Z
started_at: 2026-10-10T09:49:27.373Z
---
Issue https://github.com/jlevy/squares/issues/483 (opened 2026-10-10). Refinement 1.4263e-10 below Ryan Xu's exact certificate side 88809603717088809603717/10^22. Source ebdeleeuw/square-packing-n70 at 24221d5e51244ca5290d5b1c43f1fbe36f9749e0; certificate.json SHA-256 eeebf55cf3c1614a96f51339695f28443e35f33b0195bfc24ef0549b50550cb1, centres in [-S/2,S/2]^2, half-angle tangents. Stages 1-3 and a maintained exact replay (seconds).

## Notes

2026-10-10 stage 1-2 lane (intake W1, branch worktree-agent-af22382952a5d839e, packet commit 17deb32be).

PIN: ebdeleeuw/square-packing-n70 24221d5e51244ca5290d5b1c43f1fbe36f9749e0 (tree 60b3fba53a2b752e13370c2c096e2851859122e6, committed 2026-10-10T02:04:48Z, the repository's only commit). Retrieved 2026-10-10T09:54Z. certificate.json SHA-256 eeebf55cf3c1614a96f51339695f28443e35f33b0195bfc24ef0549b50550cb1 = the issue's; verification.json's recorded digests match the certificate, export, log and checker. No licence file: derived-only custody.
PACKET: packing/resources/web/ebdeleeuw-n70-refinement-2026-10-10 (6 files pinned only; acquire_source --check: PACKET_MATCHES_ITS_CONTRACT).

CLAIM MAP: the release makes one claim. s(70) <= 888096037156625096037155737/10^26 = 8.880960371566251 (15 places, up). Case n-070 reported and verified ceiling: Ryan Xu 88809603717088809603717/10^22 = 8.880960371708881 (T-125, E-ryxu-432-rational-feasibility). Below by exactly 14263000000014263/10^26 = 1.4263e-10, as the issue states. No other pending report at 70 (#465, #470, #476, #481, #484 checked). Smallest: #483.
Register action proposed: a new upper-bound entry at n = 70, published 2026-10-10, crediting Ryan Xu's arrangement and ebdeleeuw's refinement.

FORMAT (for the importer's centred-JSON adapter): JSON {schema: "sqpack-rational-v1" (the source's own label, not a repository format), n: 70, coordinate_system: "centered", side "p/q", squares: [{x, y, t}, ...]} rational strings, box [-S/2, S/2]^2, cos=(1-t^2)/(1+t^2), sin=2t/(1+t^2).

PRICE: a timing probe of sqpack.verify.verify_packing found the certificate valid, 2,415 pairs in 0.18 s. A two-route replay with two controls: seconds. Not a recorded replay.
