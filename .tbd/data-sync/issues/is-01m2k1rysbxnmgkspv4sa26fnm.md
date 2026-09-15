---
type: is
id: is-01m2k1rysbxnmgkspv4sa26fnm
title: Page scripts inside HTML shells come under Biome
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T17:27:59.530Z
updated_at: 2026-09-15T17:27:59.530Z
---
Found by PR #181 (think-3pox): some of the explainer page's script (the kpress wrapper and the atom declarations) lives in `explainer-shell.html`, and Biome reads no `*.html`, so that JavaScript is outside the floor. It was outside the floor before #181 too; #181 moved some script frames there. The same may hold for other HTML shells or templates (the workbench's `assets/template.html`, the motion-lab pages).

The owner's direction is 'high biome and lint floors with auto formatting on all JavaScript, no exceptions'. Done when every script that a generator inlines into a page comes from a `.js` or `.ts` file under Biome and a `tsc` program, the HTML shells hold no inline script bodies beyond a one-line module loader, and the browser-floor contract test fails on an inline script body in a tracked HTML shell. Keep the published pages byte-identical apart from formatting, and show it.
