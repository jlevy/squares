---
type: is
id: is-01m21j7e3h8j1r4fqwhcxn4q21
title: Align sans math and surrounding caption text baselines in the PDF
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: caption_rendering
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T22:29:11.397Z
updated_at: 2026-09-08T22:58:08.294Z
---
Owner reports that sans math in figure captions of the final PDF sits slightly above surrounding text and can look uneven. Reproduce against the dfa0a422 publication and distinguish font-size, real baseline, and optical alignment. Correct the smallest demonstrated cause in Squares or KPress; preserve matching reserved geometry, inline/display text-size inheritance, font readiness and screen/PDF behavior. Add this dimension to the existing typography probe if missing. Do not add a new rendering framework or repeat unrelated numerical validation.

## Notes

Reproduced on dfa0a422: all 13 visible caption formulas align within 1/64 CSS px on screen but sit 0.21875 CSS px above surrounding text in print. Ordinary client-rendered KaTeX aligns at zero. Fixed by copying the already measured outer height/depth onto each clone’s existing top-level KaTeX strut and removing the prepared base’s redundant font-dependent line height. Outer reserved dimensions stay the same; no offset constant, new font, extra DOM node or media variant. Final corrected artifact reports all 13 caption baselines at zero in both media. Nine real punctuation/script/fraction/radical/limit/smash/spacing cases pass; the original strut behavior and an imposed upward shift are rejected. Existing print/loading geometry controls, 77 focused tests and static checks pass. Final pre-push, updated PR CI and deployed verification remain on parent think-qcmi.
