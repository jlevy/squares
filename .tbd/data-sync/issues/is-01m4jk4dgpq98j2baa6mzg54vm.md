---
type: is
id: is-01m4jk4dgpq98j2baa6mzg54vm
title: "Intake 2026-10-10 watch reads: evand 799be37, franciscouzo 9bf90e7, itsnaka d45669b, wand125 22a23c8, jlevy/squares 657cc48 (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:30.070Z
updated_at: 2026-10-10T10:15:24.245Z
started_at: 2026-10-10T09:49:25.370Z
---
Five watched repositories have commits past their last read: evand/square-packing (19 commits, 2026-10-08 to 10-09), franciscouzo/square-packing (2 commits, removes 102, 103, 272), itsnaka/squish-certs (d45669b, the #481 submission), wand125/square-packing (22a23c8, the #446 s(29) certificate), and jlevy/squares itself (no packet pins it). Read each: an import bead and packet for a new result, else a read in packing/campaign/intake-watch.yaml with a note saying what changed.

## Notes

2026-10-10 (sub-agent lane, commit a8fe9fa11 on worktree-agent-a16342d415747a15f). intake-watch.yaml reads written: franciscouzo/square-packing through 9bf90e7 twice, bead think-m8ck (02f9690 is #476's pin: 65 certificates, in-horizon claims) and bead think-1545 (02f9690's 20 beyond-horizon certificates; n375 drops to 9953490883645300797660281830293/(5*10^29), n378 to 9973230520053043026984980967643/(5*10^29), 4.0e-4 below the tracked 19.946861170999796); 9bf90e7 only deletes the superseded 102, 103, 272 files. itsnaka/squish-certs through d45669b, bead think-ac4h (#481's pin). wand125/square-packing through 22a23c8, bead think-r333 (mixed_n29_L582).
Not written, reported to the coordinator instead:
- evand/square-packing ed01e0d..799be37 (19 commits, all read). Two hold results the record lacks: 268af52 search/trio126/n126_xu.cert, s(126) <= 11742640687119285146522492579501/10^30 = 11.742640687119285..., exact local minimum 15/2 + 3 sqrt 2, a reconstruction of Ryan Xu's packing 9.25e-11 below the register's 14678300859014678300859/1250000000000000000000 (the author says "No claim here"; think-ilwc owns reading 268af52); and 41fc9ec search/packer/candidates/big1_n375.cert, s(375) <= 9953490883645300797660281830293/(5*10^29), beyond the horizon, the same exact side as Couzo's 02f9690 n375 certificate. 41fc9ec's hunt2_n270.cert equals the exact s(270) already registered from Couzo's 2d32a6e. The rest is packer tooling, the s(110) census of local minima above the record (493 to 683), an exactsolve slack-pair fix (Lean local-minimum proofs unaffected per the author), and a site page.
- jlevy/squares: watched only because register source squish-n153-2026-10-07 has url https://github.com/jlevy/squares/issues/401#issuecomment-6043191866 and intake_sweep.repository() maps any github.com/<owner>/<repo>/... address, issue comments included, to a repository. The fix is in devtools/intake_sweep.py, not a read.
