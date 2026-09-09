---
type: is
id: is-01m21j7e3h8j1r4fqwhcxn4q21
title: Align sans math and surrounding caption text baselines in the PDF
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T22:29:11.397Z
updated_at: 2026-09-08T23:12:31.061Z
---
Owner reports that sans math in figure captions of the final PDF sits slightly above surrounding text and can look uneven. Reproduce against the dfa0a422 publication and distinguish font-size, real baseline, and optical alignment. Correct the smallest demonstrated cause in Squares or KPress; preserve matching reserved geometry, inline/display text-size inheritance, font readiness and screen/PDF behavior. Add this dimension to the existing typography probe if missing. Do not add a new rendering framework or repeat unrelated numerical validation.

## Notes

Corrected source a10569d1 passed independent review, local pre-push (45 checks, 1,028 reachable tests) and hosted publication run 34288782889. Hosted Chromium reports all 13 caption baselines at 0 px in screen and print for light desktop and dark mobile; nine edge cases and both negative controls pass. PDF reproduction and provenance pass at 17 pages. Hosted PR merge tree d4f062eb is identical to a10569d1. Local HTML and reviewed PDF were opened in the default browser at port 64618. Merge and deployed verification remain on parent think-qcmi; unrelated suite timing-record correction is think-uwow.
