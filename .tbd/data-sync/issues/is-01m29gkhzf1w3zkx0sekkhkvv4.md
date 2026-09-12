---
type: is
id: is-01m29gkhzf1w3zkx0sekkhkvv4
title: The controls are one register, and each group is addressable
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29g1hhddhwsqfr0fz4r175e
created_at: 2026-09-12T00:34:46.894Z
updated_at: 2026-09-12T00:34:46.894Z
---
Owner, 2026-09-11: "fix all the dashboard controls below the tab to be separable. There's no particular reason to make some in the white box and some in the main container. They're mostly the same anyway, and they'll be different on each tab regardless."

The controls below the mode tabs are drawn in two visual registers with no rule behind the split: some sit in bordered white cards (FORCE LAW, WALLS, SOLVER, WHO ATTRACTS WHOM, START SMALL AND GROW, THE SHAKE, THE VIEW) and some sit loose on the chrome (the n chooser, the transport, the quick picks, the start buttons, Optimize). The split is historical, not meaningful.

Two things follow, and the second is the reason this matters now:
1. **One register.** Every group of controls is a card, or none is. Pick one and apply it, so the panel reads as a set of groups rather than as a card layout with strays.
2. **Separable, because the two tabs will not carry the same controls.** Pack is one n optimised open-endedly; Animate is a range played. Several of the groups are meaningless in one or the other, and today they are all drawn always. A tab should be able to say which groups it shows, which means each group has to be an addressable thing rather than a region of markup.

That second half is the same requirement as think-ef9h -- the layer model -- one level down, and the two should be designed together rather than solved twice. A group that a mode hides and a group that a layer hides want the same mechanism.

Constraint already in the page: the panel's height feeds `layout()`, which scales the stage from what is left. Groups that appear and disappear change that height, so whatever is built has to work with the `ResizeObserver` added for think-6wd6 rather than around it.
