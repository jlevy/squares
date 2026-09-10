---
type: is
id: is-01m1z1str69ztdk6y35ayg3ccb
title: "No font swap on the explainer's math at load: verify the composite faces are loaded before the first render"
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T23:03:39.523Z
updated_at: 2026-09-08T10:26:58.063Z
closed_at: 2026-09-08T10:26:58.063Z
close_reason: "Merged in Squares #128 with KPress #59/#60. Final pre-merge browser/PDF gates and post-merge Pages run 34214731528 passed. The live v0.2.4-33cd4760 page passes delayed-font checks in Chromium, Firefox, and WebKit and actual-font/metric checks on screen and in print; caption and PDF visuals reviewed. Failure paths and negative controls are covered by retained regressions. Detailed evidence is in think-z7ab; full numerical post-merge CI remains tracked by think-h31m."
resolution: null
duplicate_of: null
---
Owner (2026-09-07): digits in formulas visibly change font when the page loads, on the built page and the live site. Cause and fix are kpress bead (see the kpress fonts epic kpr-b4mq): katex-init renders before the composite's PT Serif slot is decoded, and the faces have no font-display. Adopt the kpress fix (gitlink bump) and add a check to inspect_explainer_typography (or a Playwright test) that loads the built page with an init script recording the first .katex insertion against each KPress Math Text face's status, asserting every composite face and every KaTeX face the page inlines is loaded before the first math node is inserted, in screen and print media; run it against the live site once deployed. Record the measured timeline before and after in the plan spec's Font Consistency section.

## Notes

Measured 2026-09-08 on main at 2980c5bc (kpress aee6df7), Playwright with an init script recording first-contentful-paint and each FontFace.loaded time: FCP at 96 to 176 ms; every inlined face finishes decoding after it. PT Serif (four faces) and Source Sans 3 Variable (two) at about +163 ms, font-display block, so prose is invisible then appears once in the right face. KaTeX_Main, KaTeX_Math, KaTeX_Size1 and Size2 and the three composite faces at about +274 ms, font-display swap, so every formula paints in the browser's fallback serif and swaps a quarter second later: this is the visible change on load. The first .katex node is inserted at 123 to 216 ms, before those faces are ready, by the page's own inlined init. Fix, two parts: (1) port kpress #58's wait so no formula is inserted before the composite and KaTeX faces are loaded (both composites once sans math is adopted), and (2) have the inliner rewrite font-display: swap to block on the KaTeX faces and the composite it inlines (kpress main already uses block on the composite since #58), so a face that is still decoding hides its text for the 300 ms it needs rather than painting a fallback; with data-URI faces the block period is short and bounded. Verify with the same probe: no face used by a formula may finish after the first .katex insertion, and no text run may resolve to a non-custom font at first paint.
