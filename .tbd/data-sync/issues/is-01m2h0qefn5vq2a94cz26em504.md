---
type: is
id: is-01m2h0qefn5vq2a94cz26em504
title: The facts panel fades only what changes, in a quick crossfade
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T22:31:12.628Z
updated_at: 2026-09-14T22:36:20.688Z
closed_at: 2026-09-14T22:36:20.685Z
close_reason: "Fixed in a63da6cd and pushed. The facts panel hands over per slot and per glyph: unchanged text is held, and changed glyphs crossfade over at most 0.2 s with opacities summing to one. The headline number crossfades in place. The container went 971 to 954 px, with the headline raised 8 px, so the moving drawing clears the headline by 8.4 px; space above and below is 54/54. check_workbench.py asserts the handover (probe facts/handover) and the clearance (probe stage/lowest-drawn). All page checkers pass."
resolution: null
duplicate_of: null
---
Owner, 2026-09-14: "the animations fade away the text and then put it back, even when the text stays the same. That's kind of ugly. They should fade in with a little more of a clean, rapid transition. If the thing isn't changing, then it shouldn't fade away and fade back."

Cause: every step faded both facts layers whole over a 0.4 s window: the n layer out over 45 %, a blank beat, then the n + 1 layer in. "Proven", the badges, "Open" and its items, identical for most steps, blinked with everything else.

Fix: a per-slot, then per-glyph handover.
- A slot drawn identically in both layers swaps at the midpoint, which cannot be seen.
- In a slot that changes, a glyph with the same markup in the same box in both layers is held the same way (`4.59 <=` in front of `s(17)` and `s(18)`); only the glyphs that differ crossfade.
- The crossfade runs over the middle half of the window, 0.2 s at most, with opacities summing to one, so there is no blank beat.
- The number under the packing crossfades in place; its drift used to stack the two numbers into a ghost.

Found while checking it: a moving drawing reaches up to 47 px below the settled floor, so the earlier 971 px container touched the headline mid-step at n = 6, 12 and 20. The container is now 954 px with the headline raised 8 px: 54 px above and below, 8 px clear of the deepest moving frame. check_workbench.py asserts the handover (no unchanged glyph dips; changed glyphs sum to one) and the clearance at the worst steps.
