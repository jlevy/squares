---
type: is
id: is-01m51hy2vfa71y9mv1bc8be41q
title: Review verification and confirmation levels for formal proof reports
kind: task
status: in_progress
priority: 1
version: 16
spec_path: docs/project/specs/active/plan-2026-10-15-formal-proof-verification-rubric.md
delegate: lane-645
labels: []
dependencies: []
child_order_hints:
  - is-01m52za96e6a69hxeez9kemwfg
  - is-01m59qvebg9yq3w0thdxr5mcq2
  - is-01m5abdtn9k5n7wm1s6q2n6p5t
hold: null
hold_until: null
created_at: 2026-10-16T05:11:10.447Z
updated_at: 2026-10-19T22:39:59.436Z
started_at: 2026-10-16T05:12:02.749Z
---
User explicitly requests a separate Astra-led PR auditing V0 and higher verification levels for credible formal proof reports. Distinguish inspected complete formalizations and successful proof-assistant runs from independent open reproduction and confirmation. Compare current rubric, evidence validators and actual formal reports; propose evidence-based consistent criteria and update implementation/docs/records only where justified, with per-result evidence and no automatic rung inflation from credibility alone. Preserve independent confirmation requirements and existing held assurance experiments. Keep this separate from News UI fixes and coordinate release metadata.

## Notes

Draft PR https://github.com/jlevy/squares/pull/645 contains source cd06fe728. Separate source-build evidence supports T154 V3/C1 while preserving the original reported entry and higher human-review requirements. Independent High A1 conditional closure and B1 actor/origin laundering are implemented with25 focused regressions passing. Post-commit integration13 passed across192 live results/604 evidence entries and generated views. Final publication/DATA pin/release-impact decisions, complete CI/checkpoint and final independent reviews remain. S3/project; incoming n19 remains unrated and unmerged in this audit.

2026-10-16 user-eb-addr-645 (addressing #645 reviews C and D): pushed D1 (eadbcce40, 97bb45a3b), D4 5fb32299e, D3 70ddd1818, C7 262c65678, D8 0f4d03afe, D7 8ff9b20b2 on codex/formal-proof-verification-rubric. Next: D2 consumers, D5 tests, C13, C2, C4, D6/C10 review record, C9 docs, C1 regen, C3 budget, C5 costs, C6 release, PR body, replies.

2026-10-16 user-eb-addr-645: main moved to 26d8bb335 (#642, #651 landed, site v0.7.15 on main); merged it at 006661d4b. Also pushed D2 ebe1e6ff3, D5 5addc0661, C13 4de743723, C2 6fdeb5754, C4 15089dd1e, D6 11537bec3, C10 7852f8dcd, C9 97e36f4d1, C1 565e3a145. Next: C3 n17 budget, C5 suite costs, C6 release (next free edition is v0.7.16 now), PR body, replies, CI.

2026-10-16 user-eb-addr-645: C3 3ab63b11f (n17 ceiling 550k), C5 29513905e, C6 papers 15ef1c27e, re-pin 6f379df6e, site cut v0.7.16 d5f16959c (main took v0.7.15 via #651). Next: C12 deferral bead, records tier, CI watch, PR body, dispositions.

2026-10-16 user-eb-addr-645: reviews C and D addressed on #645, head 1264010472 (CI green: Packing validation 38948810041, Certificate page 38948810109, Branch mergeability 38948803441). Dispositions posted: C https://github.com/jlevy/squares/pull/645#pullrequestreview-5552298675 , D https://github.com/jlevy/squares/pull/645#pullrequestreview-5552298818 . 20 fixed / 1 deferred (C12 -> think-odys, waits on #645 and #658) / 1 declined (C14). Site edition cut as v0.7.16 (main holds v0.7.15); coordinator re-cuts at merge. Draft flag could not be cleared over REST. Follow-up correctness round due.

2026-10-16 user-eb-addr-645: review E (round 2) addressed on #645 at 19e540d02: E1 68b6cb492, E2 51ffd8b27+176e5a27d, E3 17d61e1d8, E4 8ba12884d, E5 482b67c6b, E6 b33d78a86, E7 19e540d02; 7/0/0; C14 decline kept on a corrected premise. Reply https://github.com/jlevy/squares/pull/645#pullrequestreview-5553208961 . No main merge, re-cut or re-pin (integrator). PR dirty against main 8069b12e2, so Packing validation does not run; Branch mergeability 38959792477 failed on the conflict.

2026-10-19 lane-645: PR #645 merged at 9fb8e147c (site v0.7.33). think-wbh5 closed. Remaining child think-odys (C12, T-194 wording) waits on #658; this bead stays open until it closes. Post-merge: Pages deploy check for v0.7.33 and the News/changelog entry (not yet recorded).
2026-10-19 lane-645: v0.7.33 deployed 22:04:32Z on 19 October (Certificate page run 39331477560); its verify-deployment job 118333288717 passed 4706/4706 with v0.7.33-3025f3 on every page, so first_published (October 19) stands (review G1 needs no correction). A later local check_published_site --commit 9fb8e147c ran after #658 redeployed v0.7.34 and so fails only the version strings.
