---
type: is
id: is-01m4z41fnn0pf6c5wgngeg94gx
title: "Import wand125: s(28) > 1149/200 by a continuous-pose certificate (no issue)"
kind: task
status: in_progress
priority: 2
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
child_order_hints:
  - is-01m4z41wj3bh2kf9n411y2a40z
  - is-01m4z41xj0y1apyem4s5k2s9y6
hold: null
hold_until: null
created_at: 2026-10-15T06:29:52.948Z
updated_at: 2026-10-15T09:15:50.790Z
started_at: 2026-10-15T06:30:32.385Z
---
Found by the 05:30Z intake sweep of 2026-10-15 (epic think-mq0k): wand125/square-packing moved from afdcaac4e to b57e66712b5f722b39fcb703692006062c7d9eb7, three commits, all authored by Hiroaki Hosono and co-authored by Claude Opus 5.5. No issue reports any of them.

## Pins and every claim

- **8530bafb03d48444f30f241fbc1f29f01cd7c96c** (2026-10-15T04:13:10Z), "Continuous-pose certificate: s(28) > 1149/200 = 5.745". Adds `problems/square-lower-bounds/certificates/continuous_n28_L5745/` (19 files) and its INDEX.json and README entries. Claims: (1) no packing of 28 closed unit squares with disjoint interiors fits in the closed square of side 1149/200, so s(28) > 1149/200 = 5.745, a lower bound and not optimality; (2) it is checked by two verifiers "that share no code", both VERIFIED, both controls (every mass x 985/1000) REFUSED; (3) the first system was rerun before publication on a fresh Ubuntu 24.04.5 machine, VERIFIED; (4) it supersedes the source's mixed_n28_L57425 (5.7425) by 1/400. Data: release square-lower-bounds-v1 asset `certificates__continuous_n28_L5745.tar.gz`, asset id 642628950, 912,977 bytes, SHA-256 d7249d0df91a385d7747b9380303108087552a625962d529855550d8462b9ab8 (equal to the API digest, SHA256SUMS line 446 and ASSET.json). The certificate directory is the same tree at the head b57e667.
- **a070143f597e09611762f67f08c258619e1bd56b** (2026-10-15T03:22:54Z): `problems/right-isosceles/checker2/README.md` only, a tool-version note for the second checker of the right-isosceles n = 15 run (the first 98 root boxes logged before a speed fix of `simplest_between`, which returns the same integer for every b > 0). A container outside this record (squares in a square): nothing to import.
- **b57e66712b5f722b39fcb703692006062c7d9eb7** (2026-10-15T04:18:18Z): site only (`docs/data/methods.json`, `site/src/lib/results.ts`). Adds a "continuous-pose" method entry: n = 28 at 1149/200 "replaces the mixed certificate 5.7425"; "The first verifier is sqverify_fast (Joshua Levy, jlevy/squares) with a continuous-angle mode added by us. The second reuses the continuous-pose kernel of Guzhou0806/n40-square-packing (MIT)". No new claim: an evidence note for the 8530baf import.

The certificate: 884 rectangle rows (all positive) in D4 orbits, no points, total mass 2799999/100000 on K = [0, 573351/100000]^2 (L = 5.73351 = 5.745 x 0.998); core B = 499/500, threshold tau = 1, X = L/B = 1149/200 exactly. Every closed square of side B in K, at every centre and every angle (t = tan(theta/2) over [0, sqrt2 - 1], covered continuously, not on a net), is reported to capture mass >= 1; 28 x 1 > M then gives the claim. The candidate's search core 0.9977 and 201-direction search net are not inputs to the checks. Search: LP plus net rounds and repair LPs, about 42 CPU-hours (provenance/search-notes.md).

## Against the record and earlier reports at n = 28

- Verified and reported lanes on main: s(28) >= 1147/200 = 5.735, **T-107** (V3/C3, wand125's check2 certificate on a declared 416-direction net). The brief's T-068/T-074 are the older 2289/400 = 5.7225 rows, superseded in both lanes on 2026-10-06.
- **T-142**: s(28) >= 2297/400 = 5.7425, mixed_n28_L57425 at 36b85b9 (committed 2026-10-10T11:47:30Z), registered 2026-10-10 at V0/C0, pending adoption; its replay is queued in think-i85v (#532) with its whole-net control held on the AXIS_ROUNDING question (#543). So 5.7425 did reach the record, as a reported entry, and it is the earlier report in this order.
- jlevy/squares#446's 287/50 = 5.74 (8 October), never adopted, inside E-wand125-fine-net-lower-bounds-446-report.
- The new claim is above T-142 by 1/400, above #446's 287/50 by 1/200, and above T-107 by 1/100 (strict). Upper bound 5.82444461667406 (T-101/T-155): gap about 0.0794.
- Order: T-142 was reported first (10 October) and the new claim is stronger, so by the owner's rule of 2026-10-14 both are recorded, the new one as a new entry after T-142; T-142 keeps its claim. The source's "supersedes" is the source's own index; the case record decides which is current.

## The source's verifiers, and what this repository has

- **check1: sqverify_continuous v4**, source_sha256 619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5, wand125's continuous-angle mode on this repository's sqverify_fast crate. The asset's `check1/src/sqverify_continuous_v4.tgz` (113,578 B, 72086975...) is byte for byte `tools/sqverify_continuous` at d4a1981 (all 28 files by Git blob), the v4 the 12 October read recorded (think-xzob). VERIFIED 86/86 roots, 1,265,052,068 nodes, least certified bound 1.0000000000047078 (root 72, t in [69/200, 7/20]), axis patch at A = 4989999/5000000 with least bound 1.00101; 4,183 s at 10 threads, 38,949 CPU-s summed over roots. Pre-publication run: same node count, 3,714 s at 30 threads. Control: REFUSED at all 86 roots and the axis patch (5,478 nodes, 1.4 s).
- **check2: contpose_check3 v1.2**, source_sha256 f3629c29..., a driver (check.py, generator.py; written by Codex to SPEC.md, per its spec and PROVENANCE.md) around Guzhou0806's T-145 kernels. Diffed here against the retained, reviewed upstream (da06206b, f5bc3f60): the changes are exactly CHANGES.md's, rectangle and side caps, the axis grid cap 15M -> 90M vertices, tau_den <= 2e6, and an input-digest and argument echo; no arithmetic changed. VERIFIED 43/43 slabs (default T-145 endpoints), 1,912,948,689 nodes, least slab bound 1.0000000000024087 (slab 5, t in [0.04, 0.05]), axis PROVED with exact minimum 100100837034268819262383728/10^26 on a 5789 x 5789 grid; 8,506 s at 16 workers, 109,538 CPU-s summed over slabs. Control REFUSED at the axis (minimum 0.98599...).
- **This repository** has no first-party decider of a continuous cover (GC-4; think-gpe0). It has: the reviewed, retained upstream pose kernel (V-guzhou-n40-continuous-pose, CI binary 69bc9e64, replayed in full for T-145 and T-157) and axis kernel (V-guzhou-n40-axis-integer-grid, whose 15M-vertex cap refuses this 33.5M-vertex grid); the first-party finite-step audit (V-audit-continuous-pose, devtools.audit_continuous_pose, whose input builders this import reuses); sqverify-fast's exact axis sweep (V-sqverify-fast), which decided T-145's near-axis statement a second way; and the review of sqverify_continuous itself, open as think-xzob (#533).
- Independence as this record reads it: check1 shares interval.rs, exact.rs, axis.rs, oracle.rs and rotated.rs with this repository's sqverify-fast and was written by its author after reading Guzhou0806's kernel; check2 is Guzhou0806's kernel with caps raised. "Share no code" holds between the two, but neither is independent of code this record already relies on, and both follow T-145's method.

## Done here (receipts in packing/resources/web/wand125-continuous-n28-2026-10-15/receipts/)

- **Retained**: packet `wand125-continuous-n28-2026-10-15` by `devtools.acquire_source` at 8530baf (tree 95e5de88), retrieved 2026-10-15T05:33Z: 21 files in scope, 19 retained (85,844 B; the directory's documents, both check1 summaries, check2's manifest and source), 2 pinned by identical copies (the square-lower-bounds MIT LICENSE = FN-1 packet's; check2/src/kernel/LICENSE = the T-145 packet's Guzhou0806 MIT notice). `--check`: PACKET_MATCHES_ITS_CONTRACT. The release asset stays outside Git, pinned by size and digest, as the fine-net precedents do.
- **Custody and exact premises** (`devtools.continuous_pose_followup premises`, a new maintained tool; EXACT_PREMISES_HOLD, 1.3 s; no source program run): asset digest = API = SHA256SUMS = ASSET.json; sealed bundle 30 files, all 29 listed digests match; every bundled document but the README equals the pinned one; check1 archive = d4a1981 blob for blob and its build.rs digest = 619b3c00; check2's source digest by VERSION.json's rule = f3629c29. Candidate: 884 positive rows inside K, mass 2799999/100000, X = L/B = 1149/200, 28 - M = 1/100000, L^2 - 2B^2 = 308811289201/10000000000 > 0, T^2 + 2T - 1 = 89/40000 > 0, control = every mass x 985/1000 row by row. check1: stated premises = recomputed (A = 4989999/5000000, margin B - A W(1e-7) = 200029979999/500000000000005000000 > 0); 86 roots = its default cuts, all verified, nodes = 2 leaves - 1, least bound >= 1, sums = summary; control log all refused. check2: both kernel inputs regenerated here from the candidate (audit_continuous_pose's pose builder; the dominated axis measure at density scale 10^8, which the source's guards force) have exactly the manifest's, the receipt's and the shipped inputs' digests (214b2731..., cc075cb9...), and the control's (c9f35ef6..., 9d5ff35d...); every slab argument, input digest, binary cover and bound; axis minimum exact >= 1; near-axis margin 1496999501/250000000000250000000 > 0.
- **The author's check2 control, run here** from a scratch copy under `python -I` as REPRODUCE.md says: built both kernels to exactly the binaries the receipt names (c028f0e3..., 3d144a45..., g++ 13.3.0), REFUSED at the axis, every output equal to the source's control receipt but timing (`receipts/check2-control-here.json`).
- **Diagnostic sample** (`continuous_pose_followup sample`, DIAGNOSTIC_SAMPLE, one program at a time at one thread, 06:03 to 06:27Z, host load 3.3 to 6.8 on 4 cores, about 20 CPU-minutes): check1 (built here, rustc 1.98.0, binary 31936c4d...) roots 0, 1, 2 equal the source's log in nodes, leaves, splits, depth and least bound (87.0 CPU-s vs 70.8); its control REFUSED as the source's (5,478 nodes); slabs 0 and 14 on the **reviewed T-145 pose kernel** (da06206b built from the T-145 packet into its CI binary 69bc9e64) on the input regenerated here equal check2's receipt (567.6 CPU-s vs 1,613.8); check2's axis kernel PROVED (main) and REFUSED (control) with outputs equal to its receipts.
- **Two findings from the sample.** (1) The printed least bounds (1 + 4.7e-12, 1 + 2.4e-12) are search stops, not slack: masses x 9999/10000 still verify root 7 (axis 1.00091), and x 999/1000 stops root 7 on its 2e8-node budget at a pose whose exact capture is 1.0000089, so the slack there is about 1e-3. (2) Neither the source's 985/1000 control nor the 999/1000 mutant is a refusal a control can count at an oblique root: the first is refused at the axis patch alone (minimum 0.98599), the second by budget, not by an exact capture below 1. A counted oblique control is still to be designed.
- Disclosure: this lane read sqverify_continuous v4's build.rs, main.rs and parts of slab.rs (its head, premises and run function) before running it, so it is not clean-room with respect to that code and should not write think-gpe0's first-party continuous decider.

## Credit and AI assistance, as the source gives them

- README.md (root), Credits: "Hiroaki Hosono (GitHub: wand125). Code and formats from other authors are credited in the folders that use them, in particular Evan Daniel (evand/square-packing), tokoharu, and jlevy/squares."
- problems/square-lower-bounds/README.md: "Parts of this work were produced with AI assistance under human direction."
- All three commits carry "Co-Authored-By: Claude Opus 5.5". check2/src/SPEC.md is headed "spec for Codex"; PROVENANCE.md says the driver, generator and tests are new orchestration around Guzhou0806's MIT kernel (commit 71c97d0), kernel/LICENSE is Guzhou0806's MIT notice.
- methods.json (b57e667) credits the first verifier's base to "sqverify_fast (Joshua Levy, jlevy/squares)". problems/square-lower-bounds/LICENSE is MIT, Copyright (c) 2026 wand125.
- Draft credit line: "Hiroaki Hosono (wand125) after Guzhou0806, Tokoharu and Levy", as T-145 and T-176 to T-178 credit.

## Priced validation plan

Owner cap: 40 CPU-hours per item; this lane ran only items under 30 minutes.

| Item | What | Price | Status | Bead |
| --- | --- | --- | --- | --- |
| Stage 3 register | one T-NN after T-142, evidence, coverage, three verifiers, the bibliography key and resources README row, from the packet's register-plan.yaml | minutes | runnable on the records lane (records PRs #612 and #614 are open) | this bead |
| Route B replay | the reviewed T-145 pose kernel (CI binary 69bc9e64) on the regenerated input, all 43 slabs; the near-axis patch by sqverify-fast's exact sweep at A = 249499501/250000000 (the reviewed axis kernel's 15M cap refuses this 33.5M grid) and by check2's axis kernel | 12.7 CPU-hours (high 30.4, the source's own CPU); about 6.5 h wall at two workers | runnable under the cap after a preparation slice (a `replay` subcommand with two workers and a judged receipt, as audit_continuous_pose run/check-replay do for T-145) and an owner budget | think-8eo1 |
| Route A replay | the source's sqverify_continuous v4, all 86 roots, `--threads 2` | 13.3 CPU-hours (high about 16) | gated on think-xzob's soundness review (#533) and an owner budget | think-0arj |
| Counted controls | a mutant that keeps the axis patch and is refused at a tight root or slab by an exact capture below 1 (x 999/1000 is not: it stops on budget at root 7), on each route; the published 985/1000 control (seconds) | unknown until the mutant scale is found; a first probe at root 72 or slab 5 costs 15 to 25 CPU-minutes | part of each validation bead | think-0arj, think-8eo1 |
| Review | a mapped mathematical review of this certificate at tbd-strong-max: the argument from the certificate to the claim, both programs' trust boundaries, the near-axis patch at both sides A, the thin printed margins against binary64 outward rounding, the control design, the draft S3 | one review lane, a few agent-hours | due now that the source is retained, in parallel with stage 3; not started by this lane, whose brief starts no sub-agent | to open |

Totals: about 26 CPU-hours for both routes at the sampled ratios (up to about 46 at the high ends); either route alone suffices for C3 with the review. Nothing here is held above the cap.

## Acknowledgement

No author reply is owed: nothing on GitHub asked, and the draft significance is S3, below the S4 at which the project opens an issue for an unasked result (result-import.md, stage 1, step 5), as for T-142 and T-176 to T-179. The precedent issue for this certificate's first program is the project's own #533 (think-xzob), and the replay lane for T-142 is #532. A tracking comment for #533, drafted here and not posted, for after the pull request that registers this merges (it names no T-NNN until then):

> wand125/square-packing [8530baf](https://github.com/wand125/square-packing/commit/8530bafb03d48444f30f241fbc1f29f01cd7c96c) (15 October) reports s(28) > 1149/200 = 5.745 from a rectangle measure checked at every angle, decided at the source by `sqverify_continuous` v4 (d4a1981, the version this issue's review would read) and by a second driver, `contpose_check3`, around Guzhou0806's T-145 kernels with only their caps raised. The intake retained its documents at 8530baf in `packing/resources/web/wand125-continuous-n28-2026-10-15/`, held its exact premises and both kernel inputs to the candidate, and ran a diagnostic sample that matched the source's logs at three of `sqverify_continuous`'s roots and at two slabs on the reviewed T-145 kernel, which is not a replay. This issue's soundness review of the continuous mode now bears on a third claim; the n = 28 replay is priced in the import's bead and waits for an owner budget with the n = 40 ones.

Branch: claude/wizardly-meitner-wqn4x3-intake-n28.

## Notes

2026-10-15, stages 1-2 (intake lane, branch claude/wizardly-meitner-wqn4x3-intake-n28 from origin/main c4c690a3e, pushed at c9ccaf6bf59b7a4ca828e5eeacab0c3f9dab8331; no PR opened):

- b0ebe86f2 devtools: continuous_pose_followup (premises, sample) with 28 tests; fine_net_followup.sealed_bundle takes a suffix; integrity-ceremony allowlist entry.
- 8f04ccb6b resources: packet packing/resources/web/wand125-continuous-n28-2026-10-15/ (acquire_source at 8530baf, --check PACKET_MATCHES_ITS_CONTRACT), receipts premises-n28.json (EXACT_PREMISES_HOLD), check2-control-here.json (source's control, refused at the axis), sample-diagnostic-n28.json (DIAGNOSTIC_SAMPLE), README.md, register-plan.yaml.
- c9ccaf6bf suite costs: admit-local of tests/test_continuous_pose_followup.py (report kept in devtools/suite-file-cost-admissions/continuous-pose-followup-2026-10-15.json); suite_files check: every shard under 10%.

Checks: `packing-validate --records` 51/51 steps of the tier passed (1m49s) on the rebased branch; focused tests (test_continuous_pose_followup, test_fine_net_followup, test_audit_continuous_pose, test_integrity_ceremony_contract, test_acquire_source) 146 passed in 14 s. `--push`: every step passed but "reachable behavioral tests", which escalated to the whole suite because the packet retains the source's Python (check2/src/check.py is "Python outside the mapped roots") and timed out at 1800 s on a host at load about 10, at 20% with no failure; CI's --fast covers it when a PR opens.

Register plan: one T-NN after T-142, V0/C0, draft S3, pending adoption beside T-142 while T-107 holds both lanes; evidence E-wand125-continuous-n28-5745-report; coverage wand125-continuous-n28-5745-2026-10-15; verifiers V-wand125-sqverify-continuous, V-wand125-contpose-check3, V-continuous-pose-followup; bibliography key [wand125 continuous n28 2026-10-15]. Registers, case records, intake-watch, result-requests, the bibliography and the resources README were not edited (records PRs #612 merged during this lane, #614 open). The intake-watch read through b57e667 is owed with the records change.

Scratch cleaned at the end; the asset and the built binaries are gone, re-derivable from the pinned digests.

## 2026-10-15 records-1016 lane (think-mq0k), branch claude/wizardly-meitner-wqn4x3-records-1016, https://github.com/jlevy/squares/pull/616

Registered as T-192 (V0/C0, draft S3) after T-142; T-142 and T-107 keep their claims; notes list every lower bound the register holds at 28. Verifiers V-wand125-sqverify-continuous, V-wand125-contpose-check3 and V-continuous-pose-followup registered; receipts kept off the artifacts. intake-watch reads wand125 through b57e667 (no bead: the packet pins 8530baf). wand125 has since pushed 5e6c603 (07:26:47Z, "Rectangles v2: new piece 7.N1"), unread. Stays open as the parent of think-8eo1 and think-0arj; the #533 tracking comment is still a draft here.
