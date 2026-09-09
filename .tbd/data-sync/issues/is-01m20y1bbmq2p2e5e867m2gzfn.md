---
type: is
id: is-01m20y1bbmq2p2e5e867m2gzfn
title: Lower list bullets slightly to align with the text crossbars
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T16:36:20.460Z
updated_at: 2026-09-09T03:00:31.121Z
closed_at: 2026-09-09T03:00:31.121Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
User reports the list bullets are very slightly too high and wants their optical center nearer the region between the A and E crossbars. Inspect the actual shipped marker glyph/CSS and apply the smallest downward adjustment in the cleanest owner. Verify both screen and PDF, preserving list wrapping, alignment, and marker font provenance. Assigned to caption_rendering; include the fix in the current PR integration and final default-browser HTML/PDF preview.
