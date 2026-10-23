---
type: is
id: is-01m5k19kqedc9vp30sk9wm3s5f
title: Resolve current-head CI integration failures and validate final site
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-ci-integration
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:06:42.157Z
updated_at: 2026-10-23T00:09:01.933Z
started_at: 2026-10-23T00:07:03.618Z
---
Track PR737 current-head hosted failures:1783 typecheck Optional bounding boxes, overview current-nav helper, stale Papers negative-fixture mutation, Contributor Profiles heading, and rollup formatting. Mechanical owners coordinate fixes. Keep open until final build and current-head CI pass; earlier Pages successes are not final certification. Sol owns narrow published-site/contributor expectations and rollup formatting only; root owns integration delivery.

## Notes

Current hosted1783bcc077337f3694bbc396bbad3ed5e4f16fa0: Certificate page39874817164 SUCCESS; Packing39874817155 still running frontend, with failed typecheck (6OptionalSubscript bbox annotations), suiteA (4current-control helper assertions), suiteC (stale Papers negative fixture), suiteD (Contributor Profiles labels), validate (rollup formatting). Owners coordinating type/helper fixes. Sol repaired Papers mutation to actual canonical tag and asserted byte change; Contributor Profiles H1/title and directory/profile plain-About/current-parent expectations now match canonical hierarchy while all tally/article/content assertions remain. Exact two-case validation2passed12.15s, log ci-integration-mechanical-verified.log. Ruff/diff clean. Rollup owner migrated new4semantic tests (4passed8.56s); Sol verified Ruff format/check clean, no semantic edit. Verification migration separate6rnk12passed101.35s. KEEP OPEN: latest runtime Verification/Recent changes not yet pushed/certified; final build and current-head hosted CI pending. Root owns commits/integration acceptance.
