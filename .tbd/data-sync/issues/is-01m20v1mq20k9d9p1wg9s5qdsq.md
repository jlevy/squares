---
type: is
id: is-01m20v1mq20k9d9p1wg9s5qdsq
title: Prevent math startup from shifting neighboring text and reduce parameter delay
kind: bug
status: closed
priority: 1
version: 33
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
  - is-01m212vmx03ddfr35psjtzk1k5
  - is-01m212vnnwz9d60e7yhsahx8qe
  - is-01m2152r3nckcg3we82828v7yh
  - is-01m21brwj6et9vbnf7fvnpva2x
  - is-01m21c9b3envq2cwh5q5s7wvgs
  - is-01m21dyxvmcggme4gkh8j849hx
  - is-01m21dyydt23csbr8h3jtkztse
  - is-01m21dyyygnr8mpt1vt77b26a4
  - is-01m21f1xf01nwz7jf9bgc3zgnr
  - is-01m21j7e3h8j1r4fqwhcxn4q21
  - is-01m21mgmrpatjx0n66y23mmjc8
  - is-01m21n690s638a0kpj17prevpn
  - is-01m21npsp1xbrxc957kfy1exjj
  - is-01m21npt8yyc1faakzqd5m51fb
  - is-01m21pvfmt41mpzpwgqc569tst
  - is-01m21qk3wymhc6m7g7d0fy4yfq
created_at: 2026-09-08T15:44:04.307Z
updated_at: 2026-09-09T03:00:31.017Z
closed_at: 2026-09-09T03:00:31.005Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
User confirms the deployed no-swap fix works but math parameters still appear slowly. Deployment remains 33cd4760 with KPress7b20ae7. Source-confirmed avoidable dependencies: HOST_MATH_INIT sets allEmbeddedFonts:true and waits every declared face before boot; both certificate boots synchronously build 230x230 heat maps, including the hidden certificate, before initial readouts; root pending CSS keeps every .tex/.tex-d hidden until all static math and pending interactive renders settle. Diagnose normal first-visible parameter timing separately from the delayed-font regression probe. Prefer a Squares fix that renders/reveals each font-ready parameter independently and defers nonessential/hidden heat-map work; evaluate narrower upstream warmup separately. Preserve the no-swap, latest-input, no-JS/error fallback, and print contracts. Do not describe the three-second failure ceiling as an intentional startup delay.

## Notes

W7 implementation continuation from deployed33cd4760/KPress7b20ae7. User added fixed math geometry/no text shifting and requested PRs for everything plus finished HTML and PDF opened in the default browser. Three delegates own normal startup measurement (think-yygv), Squares prepared geometry + parameter-first scheduling (think-lkjf), and upstream synchronous staging/actual-face readiness/hydration (think-gnl0, upstream kpr-prsb). New source-discovered startup shift has its own bead think-tpsi: all default certificate figures initially hidden, then inserted by bottom-script show().

Bounded slices, control identity, hypotheses and pre-registered acceptance are retained in packing/benchmarks/math-startup/README.md and hypotheses/. No candidate timing measurement yet. Layout requires ≤1 CSS px math-box change across real held-font reveal, preserving wrapping at both widths in three browsers. Normal latency is all14 correct visible Figure6 labels/readouts; twelve interleaved control/candidate pairs per1280x720 and390x720, with the95% paired interval at least10% faster at both widths. Correctness can justify the layout fix even if the separate timing claim fails; record all outcomes honestly.

First boundary16:19UTC: initial records tier31/69 passed in32.93s;11 focused reporting/CI contracts passed in0.41s and typecheck clean. The new probe controls detect known160px movement and reject missing math/anchors/counters; real control calibration uncovered initially absent figure selection, requiring phase-aware validation. Root owns campaign records, Pages sharing of one prepared artifact across browser checks, cross-repo integration, PRs and final artifacts. Next critical path: finalize retained geometry guard, freeze instrument/control, run an otherwise-idle calibration and paired comparison, then integrate and validate both PRs. Earlier deployment and no-swap evidence remains in the existing spec and previous bead note history.

Second boundary 17:01 UTC: frozen control and corrected no-warmup eligibility committed f95150e4; baseline six valid runs retained, no candidate timing yet. Independent real-transfer geometry control caught WebKit exposing a lone relation before its fallback font arrived (think-zh5u), retained as exp-002. KPress PR61 first CI green at206d585; follow-up runtime now awaits per-family native load promises because check() lies in WebKit. Focused final upstream 29 browser/241 JS tests and lint/types green. Root has integrated current main PR130 session-record repair before final validation.

Additional owner requests tracked as think-06te (bullet optical offset and obsolete stretched-marker override) and think-jizt (canonical standalone KPress architecture). Bullet shape and 0.72px screen/0.64px print downward offset pass retained negative controls; architecture drafted via tbd architecture shortcut and independently reviewed. Host review corrected CSS-visible print certificate heat maps and native semantic fallback markers. Publication CI shares one prepared artifact across all browser checks. Next: commit/pin upstream, build final artifact, run full correctness matrix then an idle-host paired timing window, full checkpoint, PR and HTML/PDF previews.

18:55 UTC integration: KPress PR61 merged20a7d2b with complete CI34256487179 green; runtime, WebKit, architecture-creation and upstream CI beads closed/synced. Merged Squares main38ca2892 atcadaf4df, preserving PR131 paper, bold-sans and print repairs. Review found supported saved settings lost prepared reservations; think-fatc now owns four-context declarative preparation and complete formula coverage, locally validated with52focusedtests and held-font/default/representative saved-setting controls. Canonical architecture follow-up is KPressPR64. H003 remains unmeasured and its pre-run protocol now identifies the combined publication; H004 extends correctness to all settings. Root reporter14tests/types and durable documentation869-file coverage pass. Final committed push gate, hosted full checkpoint/Pages matrix and isolated timings remain before publication, followed by browser/PDF opening.

2026-09-08 20:33 UTC integration checkpoint: final product source d122d19c passed45 selected checks and1188 reachable tests in137.83s, retained in runs/push-final-ui-2026-09-08.json.gz. Full hosted checkpoint at25e66d7b passed69/69 Linux steps with no skips plus4 macOS steps. Final Pages34274946315 passes print and Firefox loading but reports one WebKit early_math observation after3170ms; kpress_font_pipeline is isolating observer overhead versus a real pending-node watchdog gap. H005 has exactly12pairs each width and provisional paired improvements13.50% desktop/37.57% mobile; no accepted product claim before complete correctness evidence. PDF atd122d19c has17 pages,26 embedded subsets, clean full visual review and reproducibility. Main advanced tofbc790b3; validation-only PR129/132 integration committedde5013d9 using main shared -n/--numprocesses interface, preserving branch fault/scope controls; all123 focused tests pass (two required ps permission replay). Three delegates active on final Pages diagnosis, PDF, and evidence closeout. Squares PR/merge/deploy remain incomplete. Scope fixed to these repairs.

2026-09-08 final merge integration: Squares main PR134 at 7ef80525b35a8e77e00b460a7e08f1489134d0cc had Pages run https://github.com/jlevy/squares/actions/runs/34283872995 fail only in font-loading (webkit), step Render the page and check mobile font loading. Build and Firefox passed. The sole reported finding is the old all-declared-font first-paint predicate: KaTeX AMS/Caligraphic/Main/Size faces reported error and two composite bold Greek subsets loading at 2998ms. All four Planetaire Mono Text faces reported loaded; early_math=null, fallback=null, and there were no page errors or stale input findings. This is not evidence of a mono asset failure. Source comparison confirms combined dfa0a422 retains the corrected per-visible-formula, per-family glyph-load observer, later-unready-face rejection, narrowed render readiness, prepared publication and queued-watchdog protection. The old log does not identify which errored declarations a later formula might require, so no claim that every listed font error is harmless is made. Disposition: covered by the existing font startup/loading work; final combined PR CI will run the corrected observer against the merged publication, without a separate old-main reproduction or a new work item. Raw failed log retained at /private/tmp/squares-main-34283872995-failed.log and exact job metadata at /private/tmp/squares-main-34283872995-status.json.
