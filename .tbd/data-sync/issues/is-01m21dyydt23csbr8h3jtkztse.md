---
type: is
id: is-01m21dyydt23csbr8h3jtkztse
title: Restore the intended visual weight of PT Serif math
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:14:38.905Z
updated_at: 2026-09-09T03:00:31.082Z
closed_at: 2026-09-09T03:00:31.082Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
User reports PT Serif math looks thinner than before the current changes. Compare exact font assets, computed size/weight and rendering policy against the earlier deployed page at equal zoom; correct the demonstrated regression without unmeasured synthetic bold. Delegate caption_rendering.
