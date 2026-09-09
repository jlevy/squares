---
type: is
id: is-01m21j7e3h8j1r4fqwhcxn4q21
title: Align sans math and surrounding caption text baselines in the PDF
kind: bug
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T22:29:11.397Z
updated_at: 2026-09-09T03:00:31.076Z
closed_at: 2026-09-09T03:00:31.076Z
close_reason: "Implemented, reviewed, merged in Squares PR #135 (merge 171bba339321b8d63d85a59ab5f2db946270be0e) with reusable work in KPress PR #68 (merge a6203389c0a6d1f6e542b1f50fa177121eae7f4a). All PR and post-merge CI passed; Pages serves edition 171bba33; live publication 34/34 and delayed-font smoke pass. HTML/PDF opened locally. Native reload retains 3000px exactly in Chromium, Firefox, and WebKit with JS on/off. Bullet raster-shape follow-up think-x65m remains open because measured geometry is already square."
resolution: null
duplicate_of: null
---
Owner reports that sans math in figure captions of the final PDF sits slightly above surrounding text and can look uneven. Reproduce against the dfa0a422 publication and distinguish font-size, real baseline, and optical alignment. Correct the smallest demonstrated cause in Squares or KPress; preserve matching reserved geometry, inline/display text-size inheritance, font readiness and screen/PDF behavior. Add this dimension to the existing typography probe if missing. Do not add a new rendering framework or repeat unrelated numerical validation.

## Notes

Corrected source a10569d1 passed independent review, local pre-push (45 checks, 1,028 reachable tests) and hosted publication run 34288782889. Hosted Chromium reports all 13 caption baselines at 0 px in screen and print for light desktop and dark mobile; nine edge cases and both negative controls pass. PDF reproduction and provenance pass at 17 pages. Hosted PR merge tree d4f062eb is identical to a10569d1. Local HTML and reviewed PDF were opened in the default browser at port 64618. Merge and deployed verification remain on parent think-qcmi; unrelated suite timing-record correction is think-uwow.
