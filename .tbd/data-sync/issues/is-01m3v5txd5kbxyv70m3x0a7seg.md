---
type: is
id: is-01m3v5txd5kbxyv70m3x0a7seg
title: Awaiting-replay rows show V and C chips but no significance
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:28:35.234Z
updated_at: 2026-10-06T08:24:19.650Z
closed_at: 2026-10-06T08:24:19.650Z
close_reason: "Superseded: PR 277 (merged 2026-10-01, 3cbbfd1c2) removed the separate awaiting-replay block, and its rows joined the one results table with real rungs and status (think-d04u, think-ai94)."
resolution: canceled
duplicate_of: null
---
The awaiting-replay group rows and popovers parse their chips from the register lane text (T-xxx V4/C3), so no S chip prints. Thread the register lookup through _lane_results so the chips read S, V, C like every other row. Owner to say whether it is wanted.

## Notes

Folded into think-d04u / think-ai94 (2026-10-01): the awaiting-replay block is being removed and its rows join the one results table with their real rungs and status.
