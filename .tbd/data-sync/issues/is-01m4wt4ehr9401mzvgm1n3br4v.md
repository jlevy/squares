---
type: is
id: is-01m4wt4ehr9401mzvgm1n3br4v
title: "Import Kevin Fang: s(380), s(381), s(382) and any other new certificates at TheSnakeFang/squarepack-certs 078789a (no issue)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
child_order_hints:
  - is-01m4xpvghtj03w0tph56f9yk0s
hold: null
hold_until: null
created_at: 2026-10-14T08:58:15.479Z
updated_at: 2026-10-14T20:04:43.738Z
started_at: 2026-10-14T08:58:19.610Z
---
Watched repository TheSnakeFang/squarepack-certs, head 078789a4cfd3, 11 commits (2026-10-12) past the fang-two-wedge-certificates-2026-10-10 pin. The couzo lane's claims list n0380, n0381, n0382 (printed 19.976775433975, 19.976969740406, 19.989479729400) as pending; think-k8z2 dates n0381 to e646c47, 2026-10-12T19:06Z. Under the owner's report-order rule (think-abi1), a watched-repository publication is reported at its first commit, so Fang's certificates are recorded before Couzo's #583/#586 where they were below the record then. Stages 1-2 and the stage 4 replay on claude/serene-hopper-xxh80m (squares-43); the claims.json and register plan go to session 01UXZs37jGv5vqVGADH7Gkn8's records lane (agreed 2026-10-14T08:57Z), which registers in report order.

## Notes

2026-10-14, lane fang-certs (worktree squares-wt/fang-certs, branch lane/fang-certs; stages 1, 2 and 4-replay; nothing registered).

STAGE 1 TRIAGE
Pin: TheSnakeFang/squarepack-certs 078789a4cfd36f915f1bfbe76d742413d79b2965 (tree 89b612b7, committed 2026-10-13T06:57:58Z), head at 2026-10-14T09:20Z, 11 commits past c75bebd. No issue asked.

Claim map (direct certificates, nNNNN/nNNNN.cert in Evan Daniel's format, same packing as nNNNN.cert.json; each folder written once, never changed):
- e646c47, 2026-10-12T19:06:24Z: 380 19.976775433974195, 381 19.976969740405508, 421 20.986150316947159, 463 21.986880406196935, 507 22.997807183348823, 553 23.998811020144984, 601 24.998914572427130, 651 25.991547815274380.
- c284cd0, 2026-10-13T00:05:31Z: 382 19.989479729399675, 422 20.988436524095744, 464 21.991709536768996, 508 22.994733849702143, 758 27.996346242823117, 814 28.999873603982716.
(README table and NOTES.md, rounded up at 15 places; every exact side rounds up to its print.) All beyond n <= 324: register action is one beyond-horizon row per count, no register entry. 507: the 508 side is 3.07e-3 below the 507 side, so s(507) <= 22.994733849702143 too; a consequence settling no case, no entry of its own (triage table); the 507 row keeps its own side.
Out of scope: theorem/, composites/, rectangles/, third_party/, tools/glue.py (think-0esw); n0308/n0343/n0344 unchanged since c75bebd (fang-two-wedge-certificates-2026-10-10).

Who else holds each value (record at main f73e9de13; issues read 2026-10-14):
- 380: row couzo-certificates-2026-10-11 19.987440766556 (verified); Fang below by 1.07e-2. Later: #583 19.973553606628, #586 19.961611078672 (Couzo, rounded up 12 places), below Fang by 3.22e-3 and 1.52e-2. Smallest: #586.
- 381: row couzo-certificates-2026-10-11 19.992663288464; Fang below by 1.57e-2. Later: #582 (Miles Gray) 19.985624661051481 exact, 8.66e-3 ABOVE Fang; #583 19.974977397657, below Fang by 1.99e-3. #589 = copy of #582, closed after 20 s. Smallest: #583.
- 382: no row. Later: #583 19.988600568289, #586 19.987713157610, below Fang by 8.79e-4 and 1.77e-3. Smallest: #586.
- 421, 422, 463, 464, 507, 508, 553, 601, 651, 758, 814: no row, no other report (issues #494-#596 bodies and comments searched; Kingbird captures and Mishapolk's README at dd3da5c hold none). Fang smallest; below the grid by 1.38e-2, 1.16e-2, 1.31e-2, 8.29e-3, 2.19e-3, 5.27e-3, 1.19e-3, 1.09e-3, 8.45e-3, 3.65e-3, 1.26e-4.
Report order (think-abi1, first commit): Fang 380/381 (10-12T19:06Z) precede #582/#583/#586 and are below the standing rows -> recorded; Fang 382 (10-13T00:05Z) is first -> recorded; #582 then not recorded at 381 (above Fang); #583/#586 recorded after Fang (couzo lane). #583/#586 credit Fang's arrangements as their seeds.

Priced plan: the source's checkers (verify.py, tools/rectcheck.py, Daniel's verify_cert.py) are retained or pinned and not run. The record decides the certificates without them, on the two maintained exact routes (devtools.upper_bound_reports certify, then check --replay). Measured 2026-10-14 on 380-382: 5.0e-4 route CPU s a pair decision; every job decides all n(n-1)/2 pairs on both routes.

Acknowledgement: no issue asked, so no reply is owed and none is drafted for posting. A courtesy note, if the owner wants one on Fang's earlier issue #484 after the merge: "Thank you for the fourteen direct certificates at 078789a (n = 380 to 814). We have retained them at that commit and replayed 380, 381 and 382 on both of this repository's exact checkers; the record will carry them as beyond-horizon rows in the order they were published, and the other eleven are retained and wait for a replay budget." (No T-NNN, no rung.)

STAGES 2 AND 4 (branch lane/fang-certs, commit 4275f846f, on the ostashev lane's cherry-picked 04de64adb and da4a68307; not pushed)
Packet packing/resources/web/fang-direct-certificates-2026-10-13: 93 files retained, 29 pinned (14 svg, 14 decimal .txt, verify_cert_daniel.py identical to the issue-399 copy). Key [Fang direct certificates 2026-10-13] in resources/bibliography.yaml and resources/README.md. Tests: packing/tests/test_upper_bound_reports_fang_direct.py.
Replay: replayed = [380, 381, 382] (coordinator's instruction; the one-worker certify over all 14, begun 09:29:38Z, was stopped at 09:44:12Z as its first 421 job started, and certify --finished assembled the receipt from the nine 380-382 outputs). 9 jobs, 1,303,026 pair decisions, 652.11 route CPU s, 863.27 job wall s, longest 138.29 s; all positives pass both routes, all 6 controls refused; least wall clearance 2^-65, least pair gaps 2.33e-20, 1.79e-20, 1.58e-20. check --replay (serial, one process): equal to the retained rows, 15m35s wall, 10m57s CPU, load 3-14, exit 0.

REPLAY OF THE OTHER ELEVEN, DONE 2026-10-14 under the owner's budget (replays under 4 CPU-h), branch lane/fang-certs-replay; the 3.02 CPU-h unfinished confirmation is removed. replayed = all 14. certify --workers 1 over 421-814: 33 jobs, 16:32:40Z-18:20:44Z, 108m04s wall, 92m49s CPU, exit 0, no timeout; 10,865,736 pair decisions, 5,554.48 route CPU s, 6,446.79 job wall s; longest job 496.24 s (758 outside-container); 814 jobs 386, 352, 374 s wall (under the 600 s JOB_TIMEOUT). certify --finished assembled all 42 jobs (the nine 380-382 outputs reused, equal to the earlier receipt's rows) into 14 per-count receipt shards. Every positive passes both routes, all 28 controls refused; least wall clearance 2^-65 everywhere; least pair gaps equal the source's verify_output.txt. check --replay over all 42: equal to the retained rows, 102m47s wall, 98m01s CPU, load 1-8, exit 0.

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): the 14 beyond-horizon rows, verified at 380, 381 and 382 by E-fang-direct-exact-feasibility; the other eleven's replay priced at 3.02 CPU-hours.

## Validation backlog (2026-10-14, owner's cap: hold anything > 40 CPU-h)

The replay of the other eleven (421 to 814) is its own bead, think-9zd2: 3.02 CPU-h, runnable, running now in squares-wt/fang-certs. The whole backlog is think-lh7d.
