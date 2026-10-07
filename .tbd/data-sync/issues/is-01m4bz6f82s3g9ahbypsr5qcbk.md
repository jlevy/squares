---
type: is
id: is-01m4bz6f82s3g9ahbypsr5qcbk
title: Make Codex cloud tbd sync reproducible and drain published PR outboxes
kind: task
status: in_progress
priority: 1
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T19:59:39.265Z
updated_at: 2026-10-07T20:02:07.095Z
started_at: 2026-10-07T20:02:03.477Z
---
User explicitly requires plain tbd sync to publish on tbd-sync and remove tracked fallback outboxes from PRs after proven preservation. Apply process-only GitHub-scoped official gh credential helper in reusable environment, preserve existing configuration and every issue/history, verify real sync/push with exact remote/native refs, then commit metadata cleanup and rerun CI at new heads.

## Notes

Applied and independently reviewed idempotent GitHub-host-scoped official gh helper configuration in /workspace/squares-env.sh. Existing GIT_CONFIG_COUNT entries and credentials/remote/proxy/TLS preserved. Plain tbd sync successfully pulled live remote41ac033 and drained research outbox; actual new-bead claim push verifies native write access. User now expressly requires empty tracked PR outboxes, permits merge after clean reviewed CI, and requires standard intake/results list/main-case graphics. Preserve raw research/lower/upper outbox archives and full native history before cleanup; source and math remain unchanged.
