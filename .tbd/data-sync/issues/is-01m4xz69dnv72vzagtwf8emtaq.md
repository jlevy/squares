---
type: is
id: is-01m4xz69dnv72vzagtwf8emtaq
title: Clean inactive News and tutorial build scratch and duplicate environments
kind: chore
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T19:45:53.064Z
updated_at: 2026-10-14T20:08:41.322Z
started_at: 2026-10-14T19:48:57.750Z
closed_at: 2026-10-14T20:08:41.321Z
close_reason: Staged only the verified inactive duplicate604.venv(643.1MiB) and superseded node_modules(94.2MiB) in their volume Trash; manifest/news-significance/disk-cleanup-v7jf-staged.json retained. Trash unemptied, no physical-free claim. Active runtimes/preview/source/evidence preserved. UV_PROJECT_ENVIRONMENT now points at existing externalenv to prevent duplicate regrowth.
resolution: null
duplicate_of: null
---
User explicitly requests ongoing disk cleanup. Audit only known task-owned scratch, duplicate environments and obsolete previews; verify no active process/open file and recreatability, preserve source/review/release evidence and active preview/runtime, stage eligible files safely with a manifest. Keep temporary work on external scratch and report actual recovered versus merely staged bytes honestly.
