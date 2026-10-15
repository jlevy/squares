---
type: is
id: is-01m4ybb1t86fyv3t8mr0j08dk9
title: Profile repeated site document rendering at the producer boundary
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:18:12.032Z
updated_at: 2026-10-15T00:11:00.063Z
started_at: 2026-10-15T00:07:56.148Z
---
Follow VE009 design withdrawal: retain existing lazy process-local caches and profile actual case_records(), iter_result_fragments() and static_content_page() using the current complete corpus. Main602 has324case and184result documents. Local oracle setup costs include36.56s case records and34.33s result documents. Identify repeated common shell/assets/math work before a bounded invocation-local producer improvement. Preserve full corpus, per-page metadata/rebasing, subsets and fresh independent patched/deterministic calls. No cross-worker transport, controller prebuild, new cache registry, ceiling increase or speed claim. Any candidate needs current-source oracle, measured inclusive cost, predeclared screen and maintenance-cost review. Work follows PR599 stabilization rather than expanding its delivery gate.

## Notes

Read-only Astra preparation at unchanged 6756bda8d completed. Retained VE009 local470pass110.380s versus shared470pass149.098s includes a91.151s serial controller barrier; no paired screen. Correction:36.56s is combined published/result-pages/records fixture setup, not isolated case_records;34.33s is result-pages setup. Source exposes repeated static_content_page shared asset/template/client-module reconstruction and full HTML parsing across324case/184result pages; base SharedAssets and font subset builders already cache initial construction. Next run two fresh serial cProfile processes on existing tests/test_case_pages.py::test_every_case_has_a_record_file_at_its_own_address and tests/test_result_overview.py::test_amended_result_address_notice_is_inside_the_complete_article after current gate releases host budget. Keep profiles separate from unprofiled validation_timing observations. Only consider invocation-local shell hoisting if attribution supports it; preserve standalone freshness, exact full HTML/asset inventories, subset equality, math provenance, link/context/refusal controls. No implementation or speed claim; current PR599 source and delivery gate stay frozen.
