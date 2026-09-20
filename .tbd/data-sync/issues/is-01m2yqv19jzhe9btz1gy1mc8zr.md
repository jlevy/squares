---
type: is
id: is-01m2yqv19jzhe9btz1gy1mc8zr
title: Keep workbench API contract fixtures outside concurrent source scans
kind: bug
status: in_progress
priority: 1
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01m2ynhxeecetevy3sn2djwtpq
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T06:25:15.057Z
updated_at: 2026-09-20T06:31:46.240Z
---
Publication audit pre-push with uv, jobs=7/inner_jobs=1 passed all 48 non-behavioral steps and 1,683 affected tests, but browser-floor source coverage saw transient packages/workbench/.api-contract-40OZ5b/{extra-helper,extra,incompatible,missing,valid}.ts created by concurrently running npm workbench tests. That fixture writes inside the source tree while the floor correctly scans nonignored untracked scripts; this is a real test concurrency race. Move the transient API contract compilation fixture outside the repository, preserve TypeScript import/module resolution and both positive and negative API compile cases, and keep the scanner strict. Acceptance: focused workbench/API tests and source-coverage test pass together, lint/type floor passes, and the final PR fast surface passes. Do not add a scanner exemption or relax timeouts. Sol high owns the bounded fix; root integrates it with think-kq00 publication audit on PR202.

## Notes

Fixed in PR202 commit 93e88a3f. A Sol high agent moved the contract fixture to tmpdir(), derived a portable import back to the authoritative API and asserted the scratch directory lies outside the package. One positive and four negative compile cases remain unchanged; no scanner exemption or ceiling change. All 202 workbench tests passed, all 3 focused API tests passed, source-coverage test passed concurrently with API compilation, and workbench TypeScript/Biome/ESLint checks passed. Independent Sol high review found no issue. Fresh hosted CI pending.
