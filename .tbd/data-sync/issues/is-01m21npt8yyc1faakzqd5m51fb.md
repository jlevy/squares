---
type: is
id: is-01m21npt8yyc1faakzqd5m51fb
title: Unify sans regular weight at 410 and refine support text
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T23:30:01.117Z
updated_at: 2026-09-09T00:01:19.909Z
---
Owner requires regular sans text and sans math at 410 with one adjustable authoritative setting. Captions and end footnotes should share a slightly smaller size and more left/right inset. Keep font metrics and print instances matched to the weight; put reusable typography configuration in KPress and page-specific role sizing in Squares. Rebuild prepared geometry and verify HTML/PDF baseline, weight, size and wrapping.

## Notes

Root support-role slice reviewed independently: captions/endnotes0.92of sans base17.48pxscreen/11.6533ptprint, shared1.4rem inset; figurelabels stay0.95. Host CSS and font-pruning/print instance declarations derive regular weight from KPress generator.REGULAR_WEIGHT. Upstream kpr-3y8q freezes410token with matching outlines/metrics and200..500 supported adjustment range. Candidate commit/pin and final build/HTML/PDF checks pending.
