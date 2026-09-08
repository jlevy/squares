---
type: is
id: is-01m20v1mq20k9d9p1wg9s5qdsq
title: Prevent math startup from shifting neighboring text and reduce parameter delay
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
child_order_hints:
  - is-01m20vpyx7r06zay11688pb1n1
  - is-01m20vpz8e6ty6gpate34sfrms
  - is-01m20vpzkch50ejzwvpnjpx9h6
  - is-01m20wwftmtwqvpwcsxk52te7x
created_at: 2026-09-08T15:44:04.307Z
updated_at: 2026-09-08T16:19:39.757Z
---
User confirms the deployed no-swap fix works but math parameters still appear slowly. Deployment remains 33cd4760 with KPress7b20ae7. Source-confirmed avoidable dependencies: HOST_MATH_INIT sets allEmbeddedFonts:true and waits every declared face before boot; both certificate boots synchronously build 230x230 heat maps, including the hidden certificate, before initial readouts; root pending CSS keeps every .tex/.tex-d hidden until all static math and pending interactive renders settle. Diagnose normal first-visible parameter timing separately from the delayed-font regression probe. Prefer a Squares fix that renders/reveals each font-ready parameter independently and defers nonessential/hidden heat-map work; evaluate narrower upstream warmup separately. Preserve the no-swap, latest-input, no-JS/error fallback, and print contracts. Do not describe the three-second failure ceiling as an intentional startup delay.

## Notes

W7 implementation continuation from deployed33cd4760/KPress7b20ae7. User added fixed math geometry/no text shifting and requested PRs for everything plus finished HTML and PDF opened in the default browser. Three delegates own normal startup measurement (think-yygv), Squares prepared geometry + parameter-first scheduling (think-lkjf), and upstream synchronous staging/actual-face readiness/hydration (think-gnl0, upstream kpr-prsb). New source-discovered startup shift has its own bead think-tpsi: all default certificate figures initially hidden, then inserted by bottom-script show().

Bounded slices, control identity, hypotheses and pre-registered acceptance are retained in packing/benchmarks/math-startup/README.md and hypotheses/. No candidate timing measurement yet. Layout requires ≤1 CSS px math-box change across real held-font reveal, preserving wrapping at both widths in three browsers. Normal latency is all14 correct visible Figure6 labels/readouts; twelve interleaved control/candidate pairs per1280x720 and390x720, with the95% paired interval at least10% faster at both widths. Correctness can justify the layout fix even if the separate timing claim fails; record all outcomes honestly.

First boundary16:19UTC: initial records tier31/69 passed in32.93s;11 focused reporting/CI contracts passed in0.41s and typecheck clean. The new probe controls detect known160px movement and reject missing math/anchors/counters; real control calibration uncovered initially absent figure selection, requiring phase-aware validation. Root owns campaign records, Pages sharing of one prepared artifact across browser checks, cross-repo integration, PRs and final artifacts. Next critical path: finalize retained geometry guard, freeze instrument/control, run an otherwise-idle calibration and paired comparison, then integrate and validate both PRs. Earlier deployment and no-swap evidence remains in the existing spec and previous bead note history.
