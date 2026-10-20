---
type: is
id: is-01m54ahn4m3hkpas6fz13bjhpd
title: "Import Evan Daniel: s(236) <= 15.861934390608, a new local minimum 2.02e-3 below T-146 (#659)"
kind: task
status: in_progress
priority: 1
version: 12
delegate: c-lane-692
labels:
  - result-import
dependencies: []
parent_id: is-01m549eweq3c13b32tjzbf0ats
child_order_hints:
  - is-01m5b11wcmc6cxqp03q00w348p
hold: null
hold_until: null
created_at: 2026-10-17T06:59:46.452Z
updated_at: 2026-10-20T02:06:42.689Z
started_at: 2026-10-18T08:47:56.022Z
---
Evan Daniel (@evand) reports s(236) <= 15.861934390608 on jlevy/squares#659 (filed 2026-10-16T14:05:14Z): the exact rational side 7930967195303679308621899285697/(5*10^29) = 15.861934390607358617243798571394 of evand/square-packing 5ad00693899ef50ccf6502f0346187cc422cc914 (committed 2026-10-16T14:03:49Z), search/packer/candidates/s236_bm3c.cert, rounded up at 12 places. Found by the 17 October intake pass (think-e2sz), lane W (user-eb-sweep-1017). Stage 1 triage below; stages 2 to 4 are this bead's, in an import lane the coordinator assigns.

## Triage (stage 1, 2026-10-17, read-only)

**Pin.** evand/square-packing 5ad00693899ef50ccf6502f0346187cc422cc914, the commit the issue names. It adds search/packer/candidates/s236_bm3c{.cert,.exact.txt,.input.txt,.json,_prior.json,_regularized.cert,_regularized.json,_vs_prior.json}. The head 757b40b (2026-10-17) carries the same .cert bytes. The source checkers are search/exact/verify_cert.py and verify_cert2.py, last changed at dbcb4c4, so the packet retains them at the pin as well. SHA-256 measured here: s236_bm3c.cert 21dbf6792bec64b06ab5fc1d6ac56a17432f971431100fdbe63e92d23bc091c9 and s236_bm3c_regularized.cert abae0c5240f986373a4c49f860004ba3b187495579b4f88d41bfec0d9015a546, both matching the issue. The certificate's header line reads `236 7930967195303679308621899285697/500000000000000000000000000000`.

**Claims (every claim the issue makes).**
1. s(236) <= 15.861934390608, the certificate side rounded up at 12 places. The issue gives the "best public before it" as 15.863955747159 (itsnaka's SQUISH #481, also #593), an improvement of 2.02e-3, and compares against the register at main e2e018f3, the issues through #643, Ellsworth's catalogue, the monotone envelope and Friedman's L-step, checked on 16 October.
2. Both source checkers (verify_cert.py, separating axes; verify_cert2.py, polygon intersection; exact rational, standard library) accept both files. They share an author and the format.
3. s236_bm3c_regularized.cert is the same packing at the same side, regularized for display with 6 angle groups. It is a display view, not a second claim.
4. It is a different local minimum from #481 (numerical evidence at 80 digits, not interval proofs). Its KKT point is strict modulo 92 flat motions (#481's: 111), with no corner-to-corner MILP descent. It has 102 + 1057 contact equations (#481: 103 + 1231), 114 corner-to-corner contacts (#481: 153), 18 rattlers (#481: 10) and 40 tilted squares, 29 of them load-bearing (#481: 35). The load-bearing tilt angles are 37.7379 deg x26, 43.8654 deg x2 and 44.0334 deg x1. Under the optimal assignment over the eight symmetries, 209 load-bearing squares move by more than 1e-4 and 20 by more than 1e-2 (max 0.747), and no tilt angle is shared. The comparison data is s236_bm3c_vs_prior.json.
5. How it was found: in a replication test of #481, the author rebuilt #481's s(236) Mondrian composition from Kingbird's s(152)_r2 corner piece and the register's s(88) (itsnaka, #422) at side s(88) + 6. The basin explorer (fixed-side perturbation and re-polish, 45 minutes on one core) then descended below #481. The run was on 15 October, and the value was noticed below the register on 16 October (PACKER.md, 5ccdc6c). Credit request: "Please credit itsnaka's SQUISH 'Mondrian composition' (#481) for the construction."
6. AI assistance: the issue speaks for "us", and the pinned commit carries a Co-Authored-By Claude Opus 5.5 trailer ("Commit and post approved by Evan in chat"). This matches Daniel's earlier submissions (#606: "done with Claude (Claude Code). Evan Daniel directed and reviewed the work").
7. Not claimed: a closed form, an interval proof of local optimality, optimality.

**Map to the register.** A bound the record does not hold, so one new entry, s(236) <= 7930967195303679308621899285697/500000000000000000000000000000. Who else holds 236: the case lanes are T-146 (Evan Daniel's regularized list of itsnaka's #481 packing) at 3172791149431853484523540541259/(2*10^29) = 15.8639557471592675; T-174 (PingYou PR #574, a refinement 1.59e-19 below T-146) is pending adoption, staged in select_houses.PENDING_ADOPTION for think-3mry; #573 and #593 were not recorded (the 14 October ledger). Exact difference from both case lanes: 0.0020213565519088; from T-174's printed 15.863955747160 rounded up: at least 0.0020213565516. No other open report states a bound at 236.

**Report order (the owner's per-count rule, devtools.intake_ledger).** At 236 the 14 October ledger took #573, then PR #574 (recorded), then #593 (not recorded), and PR #574's T-174 stands. #659 (2026-10-16T14:05:14Z; certificate first committed 14:03:49Z) is the latest report. It is below every member of the standing side by 2.02e-3, which the 12-place prints decide: **recorded**, and classed as `new_packing` with `continues` itsnaka's #481 arrangement (T-136), per the source's words "a different local minimum from #481". Stage 3 transcribes it into a ledger directory (sources.yaml, then gather, render, check) before it registers.

**Validation price (stage 4).**
- Replay: this repository's two maintained exact routes via devtools.upper_bound_reports <packet> certify --workers 1 and check --replay, as T-187's #606 replay ran them. These are sqpack's witness verifier and the independent rational corner checker, each run on the certificate with a duplicate-square and an outside-container control. Estimate: about 55 route CPU-seconds. That is T-187's 21.14 route CPU-s at 146 squares (10,585 pairs) scaled by the pair count, 27,730 at 236.
- Source checkers: verify_cert.py and verify_cert2.py from the retained copy, read before they run. Standard library only, so minutes, unmeasured.
- Total: well under 0.1 CPU-h, so it runs in the import lane under any cap. No W7 slice is needed.
- Review: stage 4's review of the replay, as the 16 October review accepted T-187.

**House rule.** Yes. Once V3/C3 with an accepted review, it is below the house (T-146) and T-174's staged house by 2.02e-3, so select_houses moves 236 to it. The adopting PR regularizes 236: Evan Daniel's driver and grid-slack at 0.5, 1 and 5 degrees, about 0.2 CPU-h, then regularize_select. The author also ships a 6-group regularized view at the same side.
- Interaction: 236 is one of T-174's 50 staged counts (think-3mry). If this result is validated before think-3mry's adoption PR lands, select_houses takes 236 to this certificate instead, and think-3mry drops 236, which saves one regularization of a house that would lapse.
- Today's drawing at 236: decided-no-better, the house drawn, 1 light / 2 uneven / 0 near-axis, 6 classes / 6 hues.

**Draft significance:** S2. It is another arrangement of itsnaka's composition at 236, a new packing 2.02e-3 below the case ceiling, as T-187 is at 146. No lower bound and no optimum.

**Credit:** Evan Daniel, after Nate Chaoweeraprasit (itsnaka)'s #481 construction, as asked. The pieces named are Kingbird's s(152)_r2 and itsnaka's #422 s(88).

**Draft acknowledgement (not posted).** It is posted after the PR that carries this triage merges (stage 7), with no T-NNN until registered.

> @evand, thank you. We have your s(236) certificate at `5ad0069` (`search/packer/candidates/s236_bm3c.cert`, SHA-256 `21dbf679…`, matching the issue). Its exact side is 7930967195303679308621899285697/(5·10^29), which rounds up to your 15.861934390608: 2.02e-3 below the case's standing side at 236 (Nate Chaoweeraprasit's #481 packing in your own regularized list, 15.8639557471592675) and below PingYou Ltd's refinement of it (PR #574). Under the owner's report-order rule it is the latest report at 236 and will be recorded, crediting itsnaka's #481 composition as you ask. Next: we retain the certificate with your two checkers, replay it on this repository's two exact routes, and register it in a records pull request. We will reply with its id and rungs then. Once validated it becomes the house at 236 under the house rule, and the case's drawing is regularized in the same change.

## Notes

2026-10-17 user-eb-sweep-1017: triage recorded in the description (stage 1, read-only). This import waits on nothing; the issues and pull requests the description cites are sources and holders, not blockers.
blocked_on: none

2026-10-18 W1 intake (think-xmxb): PR667 A8 corrected: other open reports state236 (#593 and #470), so compare their registered/pending claims in stage3 ledger. Triage reading says the new certificate is smaller; it becomes an intake_ledger verdict only when the ledger renders. Replacement sweep carries this open owner; no packet/replay/house change yet.

2026-10-19 20:53Z lane-new: taken over from the 19 October handoff (issue #684) by the coordinator's lane brief; delegate changed from the spud10.local agent. Working in worktree scratchpad lnew/wt, branch claude/intake-2026-10-19-evand-singles (first PR: #659, #664, #669, #673).

2026-10-19 21:40Z lane-new: stage 2 and 3 committed and pushed, d7413ccdb on claude/intake-2026-10-19-evand-singles: packet (evand-n236-2026-10-16 / evand-n271-2026-10-17) retained by acquire_source at the issue pin, import declaration, certify receipt on both maintained routes (positive + 2 controls), check --replay passed, registered at V0/C0 as T-218 (236) / T-219 (271) [ids provisional: lane-680 also holds T-218; whichever PR merges second renumbers]. Stage 4 review requested from the coordinator (review branch claude/review-2026-10-19-evand-659-664-669-674). Adoption at the count written locally, strong regularizer runs under think-ip1p in progress.

2026-10-19 22:23Z lane-new: V3/C3 after the 19 October review (0466eb5aa); house adopted at the count (be6aa80aa, claude/intake-2026-10-19-evand-singles); regularization runs under think-ip1p finishing.

2026-10-20 lane-new: PR #692 opened (head f76d57a40, base 028bc72ec) with records, adoption at 155/229/236/271, regularization (think-ip1p), explainer v0.4.9 and site v0.7.36. packing-validate --records passes 52 steps at the head; --push is running. Senior review requested via the coordinator. Stage 7 reply waits for the merge and check_published_site.

2026-10-20 lane-new: PR #692 head e877e19ad. The first CI run at f76d57a40 found adoption follow-ups: sweeps checkout, censuses, translation screen, PR 574 claims, n-155 closed form, bibliography Levy suffix, test golden counts. They are fixed in 9b0c82d82 and a8222aad4. main b16ddeb0a (#691) is merged and the worker snapshot pruned of the 229 review SVG. v0.7.36 is re-cut last. --records passes 52/52.
