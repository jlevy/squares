---
type: is
id: is-01m33ba5vyzekrecg2br1k5nes
title: Set s(n) on the same baseline as the legend's sentence, and hold it with a measured check
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T01:22:31.933Z
updated_at: 2026-09-22T01:57:08.928Z
closed_at: 2026-09-22T01:57:08.927Z
close_reason: "80f597f9e: the legend's sentence is inline text with its math in the flow. check_layout measures s(n) and the sentence's n on the sentence's baseline (zero-size markers) and in ink (the lowest inked row under each letter at 4x): 0.00 stage px on the built page, +1.00 on a control page with the math moved down one pixel. The earlier flex row measured 0.00 by baseline too, so the offset the owner saw was not in the layout's baseline; the ink rule now holds what the eye sees."
resolution: null
duplicate_of: null
---
The stage legend's first row reads 's(n) is the side of the smallest square holding n unit squares', with s(n) rendered by KaTeX (METRICS.bound_html.side_of) in a .note-math span inside a flex .note-row aligned on baseline (packages/workbench/src/application.js buildStageNote; assets/workbench.css .note-row, .note-math .katex). The owner has asked three or four times for s(n)'s baseline to match the text's, and each fix was judged by eye or by box positions and was still wrong on the page. The CSS comment claiming 'their baselines agree exactly' is not a measurement anyone can rerun.

Fix it, and make it a rule: measure the math glyphs' baseline and the sentence's baseline on the built page (a zero-size inline-block marker on each line, in the layout-metrics probe), require them within a fraction of a stage pixel in check_layout at every review viewport, prove the rule refuses a misaligned fixture in tests/test_check_layout.py, and confirm on a rendered frame before calling it done.

## Notes

Route, as the owner decided (2026-09-21): no kpress sans-math profile, and no swap to plain italic text. Keep the math as KaTeX, s(n) and the sentence's n (think-fz04) alike, and make its baseline coincide with the sentence's: measure both baselines on the built page with zero-size inline-block markers (the math's inside KaTeX's .base, the sentence's inside its own run), find what offsets them, fix that in the stylesheet or markup, and hold it with a check_layout rule at every review viewport, with a refusing fixture in tests/test_check_layout.py. Confirm on a rendered frame.
