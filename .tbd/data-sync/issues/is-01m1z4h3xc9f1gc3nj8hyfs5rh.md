---
type: is
id: is-01m1z4h3xc9f1gc3nj8hyfs5rh
title: Cut the v0.2.4 publication edition for the revised explainer
kind: task
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-07T23:51:19.722Z
updated_at: 2026-09-08T00:03:54.067Z
---
Assess the user-requested patch version after the paper revisions. development.md separates the editorial PUBLICATION_VERSION from the code package version and defines how to cut an edition. Bump the publication from v0.2.3 to v0.2.4, pin PUBLICATION_REVISION to the committed final content, keep the draft status and current publication date, regenerate atlas-family and claim-document stamps, and run the documented edition checks. Include all artifacts in PR #117, ensure it is up to date with origin/main and mergeable, rebuild/open final web and PDF previews, and keep package version0.2.0 unchanged.

## Notes

The publication patch is v0.2.4 and will stay fixed for this PR until merge, as explicitly requested. development.md records at most one patch bump per merge, and release.py now uses the same rule. The separate package stays0.2.0, draft status and September7 date remain. The initial edition generation passed both known-best checks in65.11 seconds and all45 pre-push checks in159.46 seconds. Subsequent user-requested examples are committed at8ea1ca0d; the edition is being repinned to that content commit without another version increment. Regeneration is limited to the atlas edition stamp/embedded source receipts and claim permalinks. Mathematical data and source verifiers are unchanged. Final PR update, preview build and hosted CI remain.
