---
type: is
id: is-01m2hcsz1mv40szm5dfn67xnez
title: "PR #125 review D22: unsupported_container_change_is_rejected passes for the wrong reason"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:18.035Z
updated_at: 2026-09-15T02:18:36.574Z
closed_at: 2026-09-15T02:18:36.573Z
close_reason: "Fixed in a6b53082: control renamed container_change_renders_one_outline_at_the_final_side, built on a rational side, asserting acceptance, one outline, byte equality with the fixed-side render and no container motion; unit test and docstring agree. Animating the outline is a follow-up bead."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F16 (Medium); triage row D22.

The check_svg_rendering control `unsupported_container_change_is_rejected` (packing/devtools/check_svg_rendering.py about :668-716) passes only because its probe puts a binary64 side on a certified frame, which is refused for evidence reasons. motion.py accepts container change, and packing/tests/test_render_motion.py `test_a_resizing_container_is_accepted` (about :94) asserts acceptance, while container_keyframes emits only opacity, so a resizing trajectory draws the final box throughout. Control name, code and test disagree.
