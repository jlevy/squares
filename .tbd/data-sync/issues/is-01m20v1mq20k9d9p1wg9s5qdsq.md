---
type: is
id: is-01m20v1mq20k9d9p1wg9s5qdsq
title: Prevent math startup from shifting neighboring text and reduce parameter delay
kind: bug
status: in_progress
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
child_order_hints:
  - is-01m20vpyx7r06zay11688pb1n1
  - is-01m20vpz8e6ty6gpate34sfrms
  - is-01m20vpzkch50ejzwvpnjpx9h6
  - is-01m20wwftmtwqvpwcsxk52te7x
  - is-01m20y1bbmq2p2e5e867m2gzfn
  - is-01m20y36t8d4wbtxgxr2d7skhg
  - is-01m20y7ngqs7h070049rg7rg92
  - is-01m2109hrm68xk1gkbtkz23rfg
created_at: 2026-09-08T15:44:04.307Z
updated_at: 2026-09-08T17:15:46.320Z
---
User confirms the deployed no-swap fix works but math parameters still appear slowly. Deployment remains 33cd4760 with KPress7b20ae7. Source-confirmed avoidable dependencies: HOST_MATH_INIT sets allEmbeddedFonts:true and waits every declared face before boot; both certificate boots synchronously build 230x230 heat maps, including the hidden certificate, before initial readouts; root pending CSS keeps every .tex/.tex-d hidden until all static math and pending interactive renders settle. Diagnose normal first-visible parameter timing separately from the delayed-font regression probe. Prefer a Squares fix that renders/reveals each font-ready parameter independently and defers nonessential/hidden heat-map work; evaluate narrower upstream warmup separately. Preserve the no-swap, latest-input, no-JS/error fallback, and print contracts. Do not describe the three-second failure ceiling as an intentional startup delay.

## Notes

W7 implementation continuation from deployed33cd4760/KPress7b20ae7. User added fixed math geometry/no text shifting and requested PRs for everything plus finished HTML and PDF opened in the default browser. Three delegates own normal startup measurement (think-yygv), Squares prepared geometry + parameter-first scheduling (think-lkjf), and upstream synchronous staging/actual-face readiness/hydration (think-gnl0, upstream kpr-prsb). New source-discovered startup shift has its own bead think-tpsi: all default certificate figures initially hidden, then inserted by bottom-script show().

Bounded slices, control identity, hypotheses and pre-registered acceptance are retained in packing/benchmarks/math-startup/README.md and hypotheses/. No candidate timing measurement yet. Layout requires ≤1 CSS px math-box change across real held-font reveal, preserving wrapping at both widths in three browsers. Normal latency is all14 correct visible Figure6 labels/readouts; twelve interleaved control/candidate pairs per1280x720 and390x720, with the95% paired interval at least10% faster at both widths. Correctness can justify the layout fix even if the separate timing claim fails; record all outcomes honestly.

First boundary16:19UTC: initial records tier31/69 passed in32.93s;11 focused reporting/CI contracts passed in0.41s and typecheck clean. The new probe controls detect known160px movement and reject missing math/anchors/counters; real control calibration uncovered initially absent figure selection, requiring phase-aware validation. Root owns campaign records, Pages sharing of one prepared artifact across browser checks, cross-repo integration, PRs and final artifacts. Next critical path: finalize retained geometry guard, freeze instrument/control, run an otherwise-idle calibration and paired comparison, then integrate and validate both PRs. Earlier deployment and no-swap evidence remains in the existing spec and previous bead note history.

Second boundary 17:01 UTC: frozen control and corrected no-warmup eligibility committed f95150e4; baseline six valid runs retained, no candidate timing yet. Independent real-transfer geometry control caught WebKit exposing a lone relation before its fallback font arrived (think-zh5u), retained as exp-002. KPress PR61 first CI green at206d585; follow-up runtime now awaits per-family native load promises because check() lies in WebKit. Focused final upstream 29 browser/241 JS tests and lint/types green. Root has integrated current main PR130 session-record repair before final validation.

Additional owner requests tracked as think-06te (bullet optical offset and obsolete stretched-marker override) and think-jizt (canonical standalone KPress architecture). Bullet shape and 0.72px screen/0.64px print downward offset pass retained negative controls; architecture drafted via tbd architecture shortcut and independently reviewed. Host review corrected CSS-visible print certificate heat maps and native semantic fallback markers. Publication CI shares one prepared artifact across all browser checks. Next: commit/pin upstream, build final artifact, run full correctness matrix then an idle-host paired timing window, full checkpoint, PR and HTML/PDF previews.
