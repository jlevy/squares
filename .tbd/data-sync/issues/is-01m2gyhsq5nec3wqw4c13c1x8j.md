---
type: is
id: is-01m2gyhsq5nec3wqw4c13c1x8j
title: The headline's n = stays still; only the number rolls
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:10.372Z
updated_at: 2026-09-14T22:16:22.406Z
closed_at: 2026-09-14T22:16:22.402Z
close_reason: "Fixed in c94054c4: n = is drawn once in #numeral-static, and the rolling slots hide n and = with visibility, so KaTeX spacing is identical. Measured 0 pixels of n = change through the 9 to 10 and 99 to 100 rolls; check_workbench.py step 19 asserts it through probe headline/still."
resolution: null
duplicate_of: null
---
Owner, 2026-09-14: "the n = 5 (or whatever number) animations should not change the n = part, they can change the number only."

Today each fading layer renders the whole KaTeX expression `n = 17`, and the step animation fades it out while translating it up 24 px, then fades the next one in from 24 px below (`workbench.js`, the `numeralA/B.style.transform` lines in `render`). A comment at `buildFacts` argues the crossfade of two identical `n =` halves is invisible, but the translate moves them, so it is not.

Fix: `n =` is drawn once, static, outside the rolling layers, and only the number fades and drifts. Keep KaTeX's exact spacing by rendering the full expression in all three places and hiding the parts that do not belong: the static copy hides the number, and the rolling copies hide `n` and `=`, with `visibility: hidden` so every copy keeps the same box.

Accept: across a step from 9 to 10 and from 99 to 100, the `n =` ink does not move by a pixel and never changes opacity; the number rolls as before.
