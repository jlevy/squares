---
type: is
id: is-01m2et4nx6fn7ea6mnqvwyqrk1
title: "Speed up simple transitions: axis-aligned grid fills play at double speed"
kind: feature
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T01:57:37.310Z
updated_at: 2026-09-14T02:05:06.445Z
---
Owner request 2026-09-13. A checkbox, checked by default, labelled 'speed up simple transitions'. A step is simple when every square in both its source and target records is axis-aligned and the container side is unchanged: only the last row of an n x n grid is being filled, so the phases carry nothing to watch. Those steps play every phase at double speed; the step that adds square k^2+1 and starts a new size plays at normal speed.
Census of the built corpus (n 1..324): the geometric rule selects 159 steps, all of kind prefix, all inside the owner's k^2-k -> k^2 range. The range also contains 110, 132, 156, 182, 210, 240, 241, 272, 273, 306, 307, whose k^2-k (or k^2-k+1) best packing is tilted; those involve real motion and stay at normal speed.
Done when: pure detection and timing live in the package with Node tests; the page wires the checkbox and API; a served-page check covers on/off durations; the change is on the PR branch.

## Notes

2026-09-13 implementation, uncommitted in .claude/worktrees/pr160-workbench on 4a1bf3b8:
- src/data/corpus.ts: isSimpleTransition(source, target) — same side, every angle within 1e-6 degrees of a multiple of 90 (catalogue angles are exact or at least 1e-4 degrees off).
- src/animation/timeline.ts: TimelineConfiguration.simple/fastSimple, SIMPLE_TRANSITION_SPEED = 2, isSpedUpPair; pairTiming divides all four phases for sped-up pairs in single-step and continuous timing, so durations, sequence length and seeking follow.
- application.js: SIMPLE computed once from the frames; state.continuous.fastSimple defaults true; setContinuous({fastSimple}) keeps the playhead's fraction of the pair; continuous() reports fastSimple and simplePairs; the timing box has a checked "speed up simple transitions" checkbox.
- Tests: two new Node tests (114 pass); check_animation_editor asserts the checkbox default, 2x on 6->7, unchanged 4->5, and the toggle round trip. check_frontend passes on a fresh build with Chrome.
Remaining: commit and push to the PR branch after owner review.
