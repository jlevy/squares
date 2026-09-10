---
type: is
id: is-01m21hj6cz7pw7bbatr29aznez
title: "Certificate page red on main: WebKit reports embedded math faces as errors and the Figure 5 readout reads empty"
kind: bug
status: closed
priority: 0
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-08T22:17:35.379Z
updated_at: 2026-09-09T00:08:30.655Z
closed_at: 2026-09-09T00:08:30.654Z
close_reason: "Shipped: squares#136 merged to main; the cause was host renders painting before the readiness gate resolved, not a WebKit font failure, and main's Certificate page run is green with the deploy running again"
resolution: null
duplicate_of: null
---

## Notes

Cause, measured on ubuntu-latest.

**Failure 1, `font-loading (webkit)`.** Not a WebKit fault and not a font failure. The
page paints a formula before `squaresMath.ready` resolves: `kpressMathText.render` holds
each node until that node's own glyph faces arrive, so an event delivered during startup
-- a slider input, a resize, the print media change, all three of which
`check_math_loading` dispatches on purpose -- shows its formula the moment its few glyphs
are ready, while the rest of the page's math faces are still in flight. Replaying the
real check flow six times per browser on the runner: WebKit 4 of 6 and Chromium 1 of 6
painted before ready, and in every one of those the first paint preceded ready by 200-300
ms; in every passing run ready came first. PR #134's four Planetaire faces took the boot
burst from 30 to 34 faces and turned a race the page had been winning into one it loses.

Why it read as a font error: KaTeX ships `font-display: swap`, WebKit maps its internal
`TimedOut` state onto `FontFace.status === "error"`, and swap is a zero-length block
period. Minimal fixture on the runner, three identical data-URI faces differing only in
`font-display`: at 8 ms swap=error, block=loading, auto=loading; at 52 ms all three
loaded, with all three `load()` promises resolved. Nothing had failed.

**Failure 2, the build job's print layout.** `figure.locator("#kval-19-5").inner_text()`
returned `""` in 7 of 72 runs while the readout's `textContent` carried all 134
characters, every element from the readout up to `<html>` was displayed, visible, opaque,
unanimated and had a client rect, and `_PROVER_LAYOUT` found that subtree's fraction
digits laid out at full size. The document's own `innerText` was short by exactly those
characters, on the first read, on a retry and after a forced reflow. Chromium's
rendered-text collection, not the page.

**Fix.** Gate every host render on the page's readiness; bring KaTeX's faces to
`font-display: block`; read typeset readouts by `textContent`.
