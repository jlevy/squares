---
type: is
id: is-01m2gyhzmdg3h1ptq6b2h74z4q
title: Remove the kind tag at the top-left of the stage
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:16.429Z
updated_at: 2026-09-14T21:53:51.930Z
---
Owner, 2026-09-14: "the labels at the top like this can just go away."

Read as the small-caps kind tag at the top-left of the stage, for example `1 -> 2 · PREFIX · MAX MOVE 0.00 · 0 ROTATE · 0 BLOCKS` (`#kind-tag`). The owner's pasted selection runs from the facts panel through the headline numerals and stops exactly where `#kind-tag` begins in DOM order, which is what a drag starting on that label produces. Capture mode already hides it, and it is transition metadata from the spike. If the owner meant a different label, reopen.

Fix: remove it from the stage. Check probes and checkers that read its text before deleting, and keep whatever they asserted about the transition where it still matters (the kind is also in `transition-stats.json`).
