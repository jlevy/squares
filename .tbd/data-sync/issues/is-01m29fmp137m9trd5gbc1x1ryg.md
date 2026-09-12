---
type: is
id: is-01m29fmp137m9trd5gbc1x1ryg
title: The stage collapses as the window narrows, because the controls take the height first
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T00:17:55.222Z
updated_at: 2026-09-12T00:17:55.222Z
---
Reported as 'the size of the upper diagram and the bottom diagram is not stable when I reload, or at different zoom levels'. Measured, and it is worse than unstable.

`layout()` computes `s = Math.min(vw / 1920, (vh - ch) / 1080)` where `ch` is `controls.offsetHeight`. The controls panel wraps as the window narrows, so it gets TALLER exactly when there is less height to share -- and it is subtracted first, so the stage gets what is left. The two effects compound:

  viewport     controls   stage scale
  1920 x 1080    596       0.448
  1512 x  982    705       0.256
  1280 x  800    734       0.061

At 1280x800 the packing is drawn at six per cent. Browser zoom changes the CSS viewport the same way a smaller window does, which is why it shows up as 'unstable at different zoom levels'.

Across four reloads at a fixed viewport the scale is identical every time, so the reload instability is the same mechanism at a slightly different window size rather than a separate race -- but `layout()` runs only on `resize` and at startup, and nothing re-runs it when the panel's own height changes after fonts load or when a control appears, so a stale `ch` is also possible.

Two parts to the fix, and both are needed:
1. Cap the share of the viewport the controls may take, and let them scroll past it, so the stage can never be starved.
2. Observe the controls' height so the layout converges rather than depending on when `layout()` happened to run.

The cap has to leave 1920x1080 exactly as it is today -- the owner is happy with that layout -- which puts it at about 0.58 of the viewport height (596/1080 = 0.552).
