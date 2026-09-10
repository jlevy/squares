---
type: is
id: is-01m21npsp1xbrxc957kfy1exjj
title: Align Planetaire Mono with surrounding prose in HTML and PDF
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T23:30:00.512Z
updated_at: 2026-09-09T03:00:31.053Z
closed_at: 2026-09-09T03:00:31.053Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
Owner reports the sans math baseline now looks correct but Planetaire Mono appears slightly too high. Reproduce on the current reviewed page and PDF; distinguish actual baseline offset from optical x-height/font-size mismatch. Fix in KPress when generic, preserve matching print font provenance, compare inline code to adjacent serif and sans support text, and retain a focused regression in the existing typography checks.

## Notes

All11inline code spans have0px baseline offset in screen/print; flat-bottom Hnx ink also aligns. Independent Astra review supports balancing KPress inline-code padding from.25em top/.1em bottom to.175em on both sides. This preserves total padding, wrapping, and glyph baseline, moving only pill edges down. Generic upstream patch requested; retained code baseline inventory and raised2px negative control in existing Squares typography inspector.
