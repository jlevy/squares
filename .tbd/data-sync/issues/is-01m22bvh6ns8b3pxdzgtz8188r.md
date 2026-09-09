---
type: is
id: is-01m22bvh6ns8b3pxdzgtz8188r
title: Repair non-monotone Codex wait timing across milestone usage cutoffs
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T05:57:04.340Z
updated_at: 2026-09-09T05:57:04.340Z
---
The existing devtools.codex_task_tree_delta refused the PR137 post-sprint interval for root01a082b3-057c-7c62-905c-1a543979e33a, start2026-09-09T05:16:31Z end2026-09-09T05:55:48Z: non-monotone tool_seconds_by_category.agent_wait 2208.02 -> 1840.904. No valid new delta receipt was emitted. Diagnose retrospective live-wait clipping versus refreshed child populations using native logs; add a meaningful regression, then re-meter the separate publication/documentation interval. Preserve session113 frozen receipt and do not clip negative deltas or mix accounting populations silently.
