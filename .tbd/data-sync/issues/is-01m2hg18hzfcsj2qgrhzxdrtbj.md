---
type: is
id: is-01m2hg18hzfcsj2qgrhzxdrtbj
title: "PR #160 review D43: tests do not pin the admission geometry or what their titles claim"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:58:42.878Z
updated_at: 2026-09-15T02:58:42.878Z
---
Canonical defect D43 from the 2026-09-14 stack triage. Source finding: #160 R17 (Medium): admission, runner, scheduler and Search-checker items. (R17's Pack key-map item is D62 and its check_pack_panel item belongs to lane D-page.)

Tests did not pin the admission geometry or what their titles claim:
- `packages/workbench/tests/test_benchmark_admission.py:106-113`: loosening `VALID_OVERLAP` to 0.05 left all admission and block-report tests green.
- `:284`: the sweep fixture was refused as `invalid-effective-configuration` (seed 1 against configuration seed 0), not for its geometry.
- `tests/search-pack-runner.test.ts:217-240`: 2 physics steps against a best-sampling interval of 10, so `bestObserved` was null and unasserted; the effective seed only `typeof number`; the objective assertion could not fail.
- `:272-289`: batch invariance ran 9 steps from an already-valid grid (repair `already-valid`, 0 iterations).
- `tests/search-scheduler.test.ts:207-224`: one wall-translation forgery only; the test there also uses a real clock with a 5 ms timeout and flakes.
- `tools/workbench_tools/check_search_panel.py`: n=1, one seed, one step; no cancel, rejected import, repair or keyboard case (the keyboard case is D12, lane D-page).
Related: think-wqf3 (batch invariance).
