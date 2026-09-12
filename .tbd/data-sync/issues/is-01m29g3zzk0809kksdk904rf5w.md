---
type: is
id: is-01m29g3zzk0809kksdk904rf5w
title: "L3: a red star where the lower bound is ours"
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29g1hhddhwsqfr0fz4r175e
created_at: 2026-09-12T00:26:16.944Z
updated_at: 2026-09-12T00:26:45.221Z
---
Owner: "for ones where the lower bound is ours it should have a red star and indicate it's a new result".

The page already has both halves of this and they are not connected. The panel carries a star line -- the `.star-line` row, scarlet, reading "new lower bound" -- and the facts record knows which lower bounds this project established. What is missing is the citation context: a bound that is ours should say so IN the sources block, not only as a separate line, so a reader seeing "Sources:" does not conclude the bound came from one of them.

So: in the sources layer, a lower bound that is ours is a scarlet star and a short "this work" rather than a citation, sitting where the citation would be. The existing star line either stays as the headline claim or folds into this -- decide with think-4kku in front of you rather than now.

Check the star glyph survives the page's font subset before relying on it. The panel's faces are subset to what the page uses, and an earlier bug had a relation glyph fall through to a different face at a different size because the subset did not carry it.
