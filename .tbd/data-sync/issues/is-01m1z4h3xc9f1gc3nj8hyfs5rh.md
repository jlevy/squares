---
type: is
id: is-01m1z4h3xc9f1gc3nj8hyfs5rh
title: Cut the v0.2.4 publication edition for the revised explainer
kind: task
status: in_progress
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-07T23:51:19.722Z
updated_at: 2026-09-08T00:14:09.149Z
---
Assess the user-requested patch version after the paper revisions. development.md separates the editorial PUBLICATION_VERSION from the code package version and defines how to cut an edition. Bump the publication from v0.2.3 to v0.2.4, pin PUBLICATION_REVISION to the committed final content, keep the draft status and current publication date, regenerate atlas-family and claim-document stamps, and run the documented edition checks. Include all artifacts in PR #117, ensure it is up to date with origin/main and mergeable, rebuild/open final web and PDF previews, and keep package version0.2.0 unchanged.

## Notes

Prepared DRAFT v0.2.4 with content revision8ea1ca0d, committed all stamped artifacts in1a32a118 and pushed PR #117. The version stays fixed until merge; development.md and release.py record at most one publication patch bump per merge. Package version0.2.0, September7 date and mathematical data are unchanged. All45 final pre-push checks passed in244.15s; the publication checklist105 tests passed in253.68s, and both final known-best atlas checks passed in135.78s. Final Chromium layout/touch/self-check passed. Root reviewed the17-page PDF, including examples and footnote. HTML/Markdown/PDF were rebuilt at1a32a118, web preview and Preview PDF opened. Fresh fetch shows0 commits behind origin/main373beb36; GitHub reports MERGEABLE. Hosted CI is running.
