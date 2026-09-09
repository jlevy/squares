---
type: is
id: is-01m22bvh6ns8b3pxdzgtz8188r
title: Repair non-monotone Codex wait timing across milestone usage cutoffs
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T05:57:04.340Z
updated_at: 2026-09-09T07:26:40.204Z
---
The existing devtools.codex_task_tree_delta refused the PR137 post-sprint interval for root01a082b3-057c-7c62-905c-1a543979e33a, start2026-09-09T05:16:31Z end2026-09-09T05:55:48Z: non-monotone tool_seconds_by_category.agent_wait 2208.02 -> 1840.904. No valid new delta receipt was emitted. Diagnose retrospective live-wait clipping versus refreshed child populations using native logs; add a meaningful regression, then re-meter the separate publication/documentation interval. Preserve session113 frozen receipt and do not clip negative deltas or mix accounting populations silently.

## Notes

Reproduced the original 05:16:31Z-05:55:48Z refusal exactly. Cause: legacy-child replay filtering compared client active duration symmetrically with wall time; a valid owned turn spanning 04:30:10.546Z-05:19:32.145Z reported 2755.580s client duration versus 2961.599s wall. It was live and retained at the first cutoff, then discarded after completion, removing 513.989s of prior agent_wait. Fix in codex_log_rollup accepts client durations shorter than wall time (pauses may be excluded) while retaining rejection when client duration impossibly exceeds the compressed log interval. Regression exercises a wait item completed after the first cutoff. 32 focused tests pass; Ruff check/format and BasedPyright are clean. Original short interval now writes without clamping. Separate 05:16:31Z-07:05:32Z receipt is /private/tmp/pr137-publication-delta-051631-070532.yaml and validates; it is a lower bound with 2 live sessions.
