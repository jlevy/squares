---
type: is
id: is-01m5kgc5tp1q991pqcza361c1j
title: Publish tutorial crops as shared assets and cover their deploy inputs
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5kg7j6t8j0twm81mzxpdd1h
hold: null
hold_until: null
created_at: 2026-10-23T04:30:14.868Z
updated_at: 2026-10-23T04:34:51.265Z
started_at: 2026-10-23T04:30:23.168Z
closed_at: 2026-10-23T04:34:51.264Z
close_reason: "Implemented and pushed in 020c7f73111c4c083e0cc21466ccea53668cec8d, https://github.com/jlevy/squares/pull/743. Pages push paths now cover kingbird29-overview.svg. Cropped tutorial SVGs publish through the shared content-addressed image pipeline, with asset hrefs and self-contained preview inlining. The advanced tutorial is 779389 bytes within the unchanged 800000-byte budget; basic tutorial is 106782 bytes. Focused Pages-input coverage, publication-budget, body-asset validity, and both tutorial visual tests passed: 5 tests in 12.24s. Shared-asset publication/inlining round-trip checks passed: 3 tests in 1.61s. Scoped Ruff passed. Reader-only caption alignment and paragraph rules preserve modern paper layout; independent Chromium review confirmed 40 retained paper captions remain centered. Implementation complete; no claim that hosted CI, merge, or deployment has completed."
resolution: null
duplicate_of: null
---
Repair PR743 CI after tutorial cropping: add Kingbird SVG to Pages push path coverage; publish cropped tutorial SVGs through the shared content-addressed image pipeline so advanced tutorial remains within its existing 800KB publication budget; adapt focused crop/visual tests to asset hrefs. Scope reader-caption alignment/paragraph rules to preserve modern paper layout. No budget relaxation or paper edition bump.
