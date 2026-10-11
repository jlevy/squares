---
type: is
id: is-01m3st0ft2fa2av6mts8sc0v24
title: Measure coprime multiplication in the bounded full rectangle verifier
kind: task
status: closed
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3sqcscz61hcv90x46w4ck31
hold: null
hold_until: null
created_at: 2026-09-30T18:42:40.577Z
updated_at: 2026-09-30T19:19:44.659Z
started_at: 2026-09-30T18:51:25.186Z
closed_at: 2026-09-30T19:06:09.297Z
close_reason: "Preregistered bounded full-verifier comparison completed and independently audited by Astra: 12 exact matched reports; external child CPU median -14.4927%, invocation wall median -17.8519%, prereg criterion met. Receipt SHA8518e1a3; external angle1 remains INCONCLUSIVE, no production switch or proof credit. Adoption and remaining performance work stay with parent think-i5x7."
resolution: null
duplicate_of: null
---
Follow the completed 12.912% fixed-primitive ablation in PR251 with a source-bound production-default versus experimental-coprime comparison on the retained external angle1/1000-node workload. Use the complete201-angle analytic fixture and malformed/source/deadline controls for correctness. Freeze sources, build flags, effective cutoff, traversal, node counts, timing metrics and accept rule before three alternating pairs. Require identical normalized reports; capped external runs remain INCONCLUSIVE and earn no certificate credit. Report coordinator CPU, child CPU and wall separately. Adopt only if the measured benefit justifies the small canonical helper; do not conflate this with a GMP/library comparison. Keep GCD/operand-size/allocation profiling and one alternative engine as separately measured hypotheses under parent think-3cwg.

## Notes

Frozen prereg before trials at source SHAef07125f, tests SHA5141a2b0: analytic n3 all201/1781 VERIFIED and external n11 angle1/1000 INCONCLUSIVE, threshold1/common-core, 3 alternating default/coprime pairs, exact historical normalized report SHA on every run, supervised inner30/outer40/total300; any mismatch/refusal/timeout zero comparison credit. Material bounded-verifier criterion external Rust child CPU median<=90% default with nonoverlapping ranges, external wall median<=105%, analytic wall median<=105%. Two setup preflights failed before trials (module import, --no-default-features old-artifact hash); both recorded zero trials. Final actual default cargo build --offline --locked --release recorded SHA0a8714df/toolchain/source/flags in preflight log and receipt; coprime d25afa bound prior receipt95247e0c. Completed 12/12 exact matched reports in retained packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-bounded-verifier-ab-2026-09-30.json SHA8518e1a3. External Rust child CPU default median9.924059s range9.909474–9.992796, coprime median8.485798s range8.389309–8.632168, 14.49% lower; paired ratios0.84535/0.85633/0.86384. External invocation wall median11.742820→9.646504s, 17.85% lower, paired0.83657/0.80222/0.97124; wall ranges overlap slightly so do not claim uniform wall improvement. Analytic child CPU0.87695→0.669636, wall1.572126→1.359246. Total12 invocation wall75.04s plus separate default build6.43s. Preregistered bounded criterion met, but external remains INCONCLUSIVE and no complete n11 certificate, proof credit or production default change follows. Fast controls3 passed; Ruff/format/BasedPyright clean. Astra independent receipt review pending.

Published as PR252 and merged at48d30ff3356ba434296aa2e3143ff215aff24689 after all applicable checks passed on025afb12f2f5be448e081f01a0cb59dce48be5de. Astra max independently reviewed source/receipt/metrics and final report diff. Review comment5917952286 onPR252; originalPR246 update5918044750. Narrow production adoption is separate think-1ozu; production defaults unchanged.
