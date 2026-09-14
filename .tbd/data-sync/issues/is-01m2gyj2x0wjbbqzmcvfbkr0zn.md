---
type: is
id: is-01m2gyj2x0wjbbqzmcvfbkr0zn
title: The step row joins the regular controls, one vocabulary across tabs
kind: feature
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:19.773Z
updated_at: 2026-09-14T21:54:02.461Z
---
Owner, 2026-09-14: "the line just below the tabs with the n and min and max and + and - buttons should just be part of the regular UI not some special white block of controls at the top. These are pretty similar across the tabs, and we may as well just have a simple UI that's more consistent across each tab, with the appropriate controls in each one, reusing components where appropriate."

Today the tabs and the step row (n, minus, field, plus, the chips 5 10 11 17 26 29 100 110 272, and in Animate the range min and max) sit together in a white bordered block above the rest of the controls, which live in their own group boxes.

Direction: one control vocabulary across Pack, Search and Animate. The n selector is an ordinary group like the others; each tab shows the groups that apply to it; a component used by two tabs is one component. This is think-cz99's "controls in one register, each group addressable" with a concrete owner ask.

Scope note: PR #160 restructured these panels (`pack-panel.ts`, `search-panel.ts`, `animation-panel.ts`, `step-anim-box`). Do this restructure once, on the stack's tip, rather than in both page versions.
