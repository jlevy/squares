---
type: is
id: is-01m4ybb1t86fyv3t8mr0j08dk9
title: Profile repeated site document rendering at the producer boundary
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:18:12.032Z
updated_at: 2026-10-15T00:33:45.082Z
started_at: 2026-10-15T00:07:56.148Z
---
Follow VE009 design withdrawal: retain existing lazy process-local caches and profile actual case_records(), iter_result_fragments() and static_content_page() using the current complete corpus. Main602 has324case and184result documents. Local oracle setup costs include36.56s case records and34.33s result documents. Identify repeated common shell/assets/math work before a bounded invocation-local producer improvement. Preserve full corpus, per-page metadata/rebasing, subsets and fresh independent patched/deterministic calls. No cross-worker transport, controller prebuild, new cache registry, ceiling increase or speed claim. Any candidate needs current-source oracle, measured inclusive cost, predeclared screen and maintenance-cost review. Work follows PR599 stabilization rather than expanding its delivery gate.

## Notes

Retained producer-profile-6756/analysis.json and raw cProfiles: case_records single-node passed, setup88.33s/profile wall89.86s; result_overview single-node passed, setup60.97s/profile wall62.92s. Diagnostic overhead unmeasured, no speed comparison. Case: site_math49.608s, formula sources29.193s,17500 visual merges18.179s; only one Node render0.829s, wrapper assets0.451s. Shell-only hoist lead retired. Results: math26.712s,155 Node calls10.060s,8750 merges8.391s, chain18.303s. Future hypothesis: invocation-local identical resolved visual variants, after measuring distinct identities and independent complete HTML/math/font oracles. Current CI failures take priority; no producer candidate implemented.
