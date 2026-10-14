---
type: is
id: is-01m4w2nr6jb3epjjrwp9vyc8h7
title: Reject executable math markup in changelog prose
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
created_at: 2026-10-14T02:08:16.590Z
updated_at: 2026-10-14T02:08:16.590Z
---
Candidate security B1 at84f736c: valid math tokens can emit script or javascript MathML href through actual KPress and About rendering. Enforce a safe rendering boundary and cover ordinary math plus malicious math through the full About output.
