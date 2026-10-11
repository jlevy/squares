---
type: is
id: is-01m4h9p76mkqae3r2pvz2x3jsb
title: Read evand/square-packing past ed01e0d (e059b1e, 268af52, 1718a58)
kind: task
status: in_progress
priority: 3
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T21:39:13.236Z
updated_at: 2026-10-10T14:51:11.741Z
started_at: 2026-10-10T10:18:42.198Z
---
e059b1e exactsolve slack-pair fix; 268af52 certificates of the Ryan Xu and SQUISH ph14/ph10 n = 126 packings reconstructed from a picture; 1718a58 site. Advance the evand intake-watch row with a dated note.

## Notes

2026-10-10 (intake pass think-ff6c, branch claude/determined-rubin-yjfy2a): the evand/square-packing row is read through 799be37ac5d8 (19 commits past ed01e0d), naming this bead. Two certificates the record lacks are held here: 268af52 search/trio126/n126_xu.cert, s(126) <= 11742640687119285146522492579501/10^30 = 11.742640687119285..., the exact local minimum 15/2 + 3 sqrt 2 of Ryan Xu's packing reconstructed from a picture, 9.25e-11 below the register's 14678300859014678300859/1250000000000000000000; its README says "No claim here", so nothing on GitHub asked. 41fc9ec big1_n375.cert has the same exact side as Couzo's 02f9690 n375 certificate (think-1545's beyond-horizon row); hunt2_n270.cert equals the n270 side registered from Couzo's 2d32a6e (T-130). e059b1e's exactsolve slack-pair fix touched only n150 in the register batch (still a local minimum; the author reports the Lean proofs unaffected); an evidence note may belong under think-63vx / think-8sm2. Next: an import of the s(126) certificate as a no-issue precision refinement (result-import.md, "(no issue)"), via the declaration-driven importer (think-md2i), or a decision to leave it in the packet.

2026-10-10 (sub-agent lane, branch worktree-agent-ae20dced27ea45031 off claude/determined-rubin-yjfy2a 3884e9669, commit fc453e386f0af15379bfdc12e2d0e7a196859a05): stages 1 and 2 and the replay are done. Packet packing/resources/web/evand-trio126-2026-10-09 pins 268af529546176a25224ea3b2c7d29cef8d9e911 (tree 2679e86744bae0c4a6f1096b0c9413d63896c02d, committed 2026-10-09T05:43:37Z, MIT, retrieved 2026-10-10T13:50Z; upstream head 799be37, and no later commit touches search/trio126/). It retains all 11 trio126 files with LICENSE, CREDITS.md, search/exact/README.md and search/packer/img2packing.py; verify_cert*.py are pinned by digest, identical to the issue-399 packet's copies.
Claims of the commit: (1) n126_xu.cert, s(126) <= 11742640687119285146522492579501/10^30, exactly 92457494164707420499/10^30 (9.25e-11) below T-125's 14678300859014678300859/1250000000000000000000 and below T-098, T-113 and T-115 (all superseded at 126). It is the smallest side at 126 and maps to a new entry ("a bound the record does not hold"), registered under "(no issue)". (2) n126_ph14.cert, 11763736443985669176333330330349/10^30, 2.11e-2 above T-125; no SQUISH release states it. (3) n126_ph10.cert, 11773303606603240442283309232987/10^30, 3.07e-2 above T-125 and 4.00e-12 below T-115's superseded side. (2) and (3) are below the standing bound and ask for no work, so they stay in the packet.
15/2 + 3 sqrt 2: the record holds no closed form at 126 (the case's exact form is Xu's rational, degree 1; Xu's records file prints 11.7426406872). It is the side of a local minimum of one packing, not a value of s(126), and no certificate decides a packing at it: the rational side is 1.17e-19 above it. So there is no exact-value entry, and the closed form appears only as the source's statement.
Replay (n126_xu only): certify with 2 workers took 17.4 s wall; 3 jobs, 47,250 pair decisions, 11.48 route CPU s, longest job 10.76 s, at load 9 to 12. check --replay took 17.3 s, and 11.9 s on a recheck. Wall clearance is exactly 5e-21 and the least pair gap 9.99999999999999e-21. check-claims and check pass. register-plan printed T-NNN, E-evand-trio126-certificate-report, coverage evand-trio126-2026-10-09 and bibliography [Daniel trio126 2026-10-09] (independent; "Daniel after Xu, Chaoweeraprasit").
Validation: --records passed 49 of 49 (rerun after the 14:10Z disk-full window). --edit: 64 of 64 steps passed. Its basedpyright step was OOM-killed twice by the memory cgroup while other lanes ran basedpyright, then run directly single-threaded: 0 errors, 0 warnings, 0 notes in 181 s. tests/test_acquire_source.py and tests/test_upper_bound_reports.py: 126 passed.
The importer reads one certificate per count, so ph14 and ph10 are compared in the packet README, not in claims.json. A W7 slice keying rows by (n, path) would freeze them there.
Next: the coordinator registers T-NNN from the plan in the shared records, adds the packet to test_upper_bound_reports.py's PACKETS, and drops this bead from the evand intake-watch read once the packet pins 268af52 on the branch. Stage 4 (review of the replay, then adoption at n126) follows. This bead closes when the result is integrated, as no author asked.
