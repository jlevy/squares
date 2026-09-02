---
type: is
id: is-01m1j1jhw3qr55pme675hj58cp
title: Rename W1 research-pass workflow to research-survey
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-02T21:49:33.442Z
updated_at: 2026-09-02T23:21:24.177Z
closed_at: 2026-09-02T23:21:24.176Z
close_reason: "Fully migrated W1 to research-survey, added stale-token and cross-schema guards, updated generated documentation and PR #75, and passed local plus hosted validation on the final head."
resolution: null
duplicate_of: null
---
Fully migrate the W1 workflow identifier and reader-facing name from research-pass to research-survey across schemas, historical structured records, source documentation, generated views, validation controls, tests, and PR #75. Preserve unrelated generic uses of research pass only if they do not name W1; require a repository check that no stale workflow token remains. Validate, commit, push, update PR #75, and wait for hosted checks.
