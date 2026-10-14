---
type: is
id: is-01m4w2nt19c83ngs7xswsa8vhs
title: Isolate disposable release-impact Git fixtures from inherited Git environment
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
created_at: 2026-10-14T02:08:18.456Z
updated_at: 2026-10-14T02:08:18.456Z
---
Candidate security B2: tests/test_release_impact.py Repository.git inherits Git redirection and can commit/update refs in an unrelated repository. Scrub Git routing variables, disable inherited hooks before init, and test an unchanged external sentinel.
