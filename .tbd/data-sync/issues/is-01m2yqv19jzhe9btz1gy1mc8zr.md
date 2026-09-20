---
type: is
id: is-01m2yqv19jzhe9btz1gy1mc8zr
title: Keep workbench API contract fixtures outside concurrent source scans
kind: bug
status: closed
priority: 1
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01m2ynhxeecetevy3sn2djwtpq
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T06:25:15.057Z
updated_at: 2026-09-20T06:35:18.116Z
closed_at: 2026-09-20T06:35:18.115Z
close_reason: null
resolution: null
duplicate_of: null
---
Publication audit pre-push with uv, jobs=7/inner_jobs=1 passed all 48 non-behavioral steps and 1,683 affected tests, but browser-floor source coverage saw transient packages/workbench/.api-contract-40OZ5b/{extra-helper,extra,incompatible,missing,valid}.ts created by concurrently running npm workbench tests. That fixture writes inside the source tree while the floor correctly scans nonignored untracked scripts; this is a real test concurrency race. Move the transient API contract compilation fixture outside the repository, preserve TypeScript import/module resolution and both positive and negative API compile cases, and keep the scanner strict. Acceptance: focused workbench/API tests and source-coverage test pass together, lint/type floor passes, and the final PR fast surface passes. Do not add a scanner exemption or relax timeouts. Sol high owns the bounded fix; root integrates it with think-kq00 publication audit on PR202.

## Notes

Fixed in PR202 commit 93e88a3f. A Sol high agent moved the contract fixture to tmpdir(), derived a portable import back to the authoritative API and asserted the scratch directory lies outside the package. One positive and four negative compile cases remain unchanged; no scanner exemption or ceiling change. All 202 workbench tests passed, all 3 focused API tests passed, source-coverage test passed concurrently with API compilation, and workbench TypeScript/Biome/ESLint checks passed. Independent Sol high review found no issue. Fresh hosted CI pending.

Focused repair receipt (Sol high task transcript; no output files were retained): `npm run typecheck --workspace @squares/workbench` passed. `npm test --workspace @squares/workbench -- --test-name-pattern='the public API rejects missing, extra, and incompatible members'` ran the entire suite because the option followed file arguments: 202/202 passed in 9.691s. Correctly focused `node --test packages/workbench/tests/api-contract.test.ts` passed 3/3 in 6.466s, launched concurrently with `.venv/bin/pytest -q tests/test_browser_floor_contract.py::test_every_first_party_script_is_in_a_type_program` from packing/ (1 passed in 6.00s). `biome ci --error-on-warnings packages/workbench/tests/api-contract.test.ts` and the workbench ESLint promise overlay passed. No source-scan ignore, timeout relaxation or contract assertion was removed.

Completion evidence: PR202 commit 93e88a3ff59a6fbe383aa59592b74793e6a79472 on base 2aaa296de815e5048b013ea268cc72d0c273b7ac passed packing validation https://github.com/jlevy/squares/actions/runs/35494422161 (all eight substantive fast jobs plus required aggregator, including macOS portability) and page/PDF checks https://github.com/jlevy/squares/actions/runs/35494422156. Branch mergeability also passed. Deferred run 35494422158 skipped and is not full-checkpoint evidence. The prior complete mathematical checkpoint is historical evidence for unchanged mathematics. The correction checkout and original checkout are clean. Publication audit and fixture correction complete; PR199–202 per-layer readiness and W7 improvements remain open, with H216 blocked behind both epics. No PR merged or new research started.
