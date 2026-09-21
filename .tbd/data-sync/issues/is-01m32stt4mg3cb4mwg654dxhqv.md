---
type: is
id: is-01m32stt4mg3cb4mwg654dxhqv
title: Put the composite's explanatory text and an attribution in the stage's bottom right
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md
labels: []
dependencies: []
created_at: 2026-09-21T20:17:02.611Z
updated_at: 2026-09-21T20:17:02.611Z
---
Owner's request: carry the explanatory text from the main composite SVG onto the video stage, bottom right, in a smaller font, and add `github.com/jlevy/squares` as an attribution at the bottom lower right.

The source is `packing/atlas/known-best/known-best-1-324.svg`, whose long text nodes are:

- `s(n) is the side of the smallest square holding n unit squares; deg is the algebraic degree of that side length`
- `colors indicate distinct tilt angles`
- `shade indicates number of full-side contacts`
- `Diagram by Joshua Levy with assistance from Claude and Codex`

The first three explain what the viewer is looking at and are the ones worth carrying; the fourth is the composite's own byline and overlaps with the requested attribution. Confirm with the owner which set they want before finalising wording.

Constraints:
- The stage is 1920x1080 in its own coordinates and the panel column runs from x = 1160. The area below OPEN is empty at every n, so there is room without moving anything.
- Sizes on the stage are stage pixels under `--stage-*` tokens, not the UI scale; the type scale has a floor because a device scale below one blurs it.
- Capture preview hides everything that explains the PAGE. This text explains the PICTURE, so it must survive capture preview -- check it appears in a captured frame, not just in the browser.
- The design-system test refuses raw values for tokenised properties, so any new size or colour needs a token.
