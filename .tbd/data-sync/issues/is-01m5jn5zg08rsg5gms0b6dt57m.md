---
type: is
id: is-01m5jn5zg08rsg5gms0b6dt57m
title: "PR #724: hosted CI is the full test gate for draft PRs (owner decision 22 Oct); merge after #729, dropping its site cut"
kind: task
status: open
priority: 1
version: 2
labels:
  - process
dependencies: []
created_at: 2026-10-22T20:35:00.224Z
updated_at: 2026-10-22T20:44:54.684Z
---
Branch claude/process-hosted-ci-gate (cbb892a06); review A approved (coordinator). Its site v0.9.1 cut collides; after #729 merges, merge main and drop the site cut (no edition), then merge.

## Notes

2026-10-22 20:47Z (c-lane-process-1022): merged origin/main 59b1ec594 (#729) into claude/process-hosted-ci-gate as merge 44b87a9fa; dropped the site v0.9.1 cut by taking main's release.py, five claim documents and README edition line, so the PR is docs-only (7 files). Local at 44b87a9fa: check_release_impact --baseline-ref origin/main, release_pin --check, check_documentation, render_operating_rules --check, check_readme all pass; pre-commit hook green. Pushed; hosted CI pending. PR body updated.
