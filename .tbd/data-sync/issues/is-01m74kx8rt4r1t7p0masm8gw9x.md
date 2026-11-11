---
type: is
id: is-01m74kx8rt4r1t7p0masm8gw9x
title: "Stage 4 blind review of #939, #946 (de Winter's re-solved s(199) and s(172); PR #948)"
kind: task
status: closed
priority: 1
version: 8
delegate: bold-ritchie-l82-review
labels:
  - intake
  - review
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T06:14:47.834Z
updated_at: 2026-11-11T06:45:59.723Z
started_at: 2026-11-11T06:14:54.559Z
closed_at: 2026-11-11T06:45:59.723Z
close_reason: "Blind stage-4 review of #939/#946 done: both accepted (F1/F2/F10/F11 minor, rest notes); clean-room l82_check ACCEPT; contraction receipts equal L78's; branch claude/bold-ritchie-xo28us-l82-review head 4f82c716a, to be folded into PR #948 (think-2h88)."
resolution: null
duplicate_of: null
---

## Notes

L82 review notes (bold-ritchie-l82-review)

- 06:22Z checker frozen: l82_check.py 03d58e60…, l82_selftest.py 18bcc73e…; self-test 1700 cases pass; 4 mutants all caught. Read so far: issues #939/#946 (no comments), author READMEs and data headers, schema basis text, the two method reviews. Not read: producer code, repo witness/verifier code, L78 PR #948.
- 06:22Z controls plan frozen (controls-plan.json 6e5fce1d…), 21 controls incl. T1/T2 calibration, K1/K2 contraction, A1-A4 algebra.
- #939 decided: ACCEPT by both methods, 19,701 pairs; 25 grid contacts; least positive margin 5.0e-101 (152,177); every control as stated. T-282 ACCEPT least 2.00833939294e-13 (36,38) = T1; T-284 ACCEPT 25 touching, least 1.4955e-16 (161,199) = T2.
- Algebra: both quintics irreducible (sympy factor_list; irreducible mod 17), 3 real roots each, p939(x)=p946(x-1); exactly one root in each stated interval (own Sturm + sympy); side-root = 1.36146e-99 (939), 1.56146e-319 (946). Root agrees with Daniel's held KKT S_exact.
- Disclosure: read think-ruu2 notes (coordinator's 1.0107e-13 figure) before my contraction run finished.
- #946 decided: ACCEPT by both methods, 14,706 pairs; no contacts; tight pairs at 1e-320, walls 1.5e-320. Controls as stated except S1 (mis-stated by me: no wall contacts); S1' (-1e-319) added after, refused.
- Measured: T-282 margin 2.53345785621e-12 (binding 36,38); gain 2.63452919980e-12 (both); share 1.0398946; certificates 1.0107e-13 below contracted T-282 (+L at 199); 12-place prints all ...284 (cert, contracted house, root). K1, K2 as stated. Daniel's held solve = same point (63 places, same 16 free squares).
- 06:38:01Z FINDINGS FROZEN: review-2026-11-11-de-winter-939-946.md sha256 51a61287179681303fdb198efd1befe39b975b8b1b526caebe69190f15a74e5b (490 lines, 30,063 bytes). Verdicts: both accepted; F1, F2 minor; none blocking. L78 not yet read.
- Frozen text committed and pushed as 5ef8151fb (branch claude/bold-ritchie-xo28us-l82-review).
- Reconciled with L78's PR #948 @ ded2c8df8: contraction receipts equal mine exactly (T-282 margin, T-284 base and whole, #946 own). T-285/T-286 held V0/C0, correct; mapping lifts to C1. Added F10 (minor: "84 moved off their contacts" wrong - 16 free, 68 keep tight contacts, 66 keep all), F11 (minor: significance rationale calls a 1.0399 share "padding" like T-280's sub-margin shares, leans on RV-3 option D), F12 (note: float fields underflow to subnormals, e.g. 1.561445e-319 vs exact 1.561468985e-319). Verdicts unchanged.
- Reconciliation, programs and receipts committed 4f82c716a and pushed. Programs/receipts under review/review-2026-11-11/ in de-winter-s199-upper-bound-2026-11-09 (programs) and de-winter-s172-upper-bound-2026-11-10.
