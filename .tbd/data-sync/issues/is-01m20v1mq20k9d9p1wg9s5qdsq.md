---
type: is
id: is-01m20v1mq20k9d9p1wg9s5qdsq
title: Reduce avoidable delay before initial math parameters become visible
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-08T15:44:04.307Z
updated_at: 2026-09-08T15:45:57.001Z
---
User confirms the deployed no-swap fix works but math parameters still appear slowly. Deployment remains 33cd4760 with KPress7b20ae7. Source-confirmed avoidable dependencies: HOST_MATH_INIT sets allEmbeddedFonts:true and waits every declared face before boot; both certificate boots synchronously build 230x230 heat maps, including the hidden certificate, before initial readouts; root pending CSS keeps every .tex/.tex-d hidden until all static math and pending interactive renders settle. Diagnose normal first-visible parameter timing separately from the delayed-font regression probe. Prefer a Squares fix that renders/reveals each font-ready parameter independently and defers nonessential/hidden heat-map work; evaluate narrower upstream warmup separately. Preserve the no-swap, latest-input, no-JS/error fallback, and print contracts. Do not describe the three-second failure ceiling as an intentional startup delay.

## Notes

W7 continuation, bounded deployment and source diagnosis with three read-only delegates. Latest main and actual Pages deployment remain 33cd4760, with KPress7b20ae7; newer Pages runs were PR checks and did not deploy. Three sequential fresh Chromium actual-font checks passed with zero findings (199 formulas, 80 sans contexts), showing Source Sans caption/readout digits and PT Serif prose on screen and matching print instances. First-any-math visible-frame times from navigation: 1078.0, 941.4, 883.2 ms; median941.4, range883.2–1078.0 ms. These unheld diagnostic runs include network, parsing, rendering, decoding and observer overhead, and do not separately measure parameter paint or establish savings for any proposed change. Raw results: /tmp/squares-font-followup-faces-{1,2,3}.json. Repeated delayed-font checker also passed, preserving all four early readout values and readable no-JS fallback; /tmp/squares-font-followup-loading.json. Source review: render_explainer.py1192/1204 enables the all-font gate; KPress runtime194 and371 warm all faces before each render; shell1649/1463 runs heat maps before boot readouts; shell773/1720 hides .tex until whole-document completion. Initial ResizeObserver can request readouts earlier, so profile per-readout first call and first visible frame separately. Recommended next slice: retain normal timing instrumentation, release each completed formula independently, defer hidden/nonessential heat maps, and narrow KPress warmup under existing kpr-prsb while keeping all no-swap/fallback/input/print regressions. The three-second runtime limit is failure recovery, not a mandatory wait. No source or deployment changes were made in this confirmation turn.
