---
type: is
id: is-01m1xg4pqz8502g827thkjfs5t
title: Repair retrospective cost loss after a late compaction settings event
kind: bug
status: closed
priority: 1
version: 3
spec_path: packing/campaign/agendas/agenda-028-hybrid-strength-and-angular-release.md
assignee: codex
labels: []
dependencies: []
parent_id: is-01m1x7ec5zyqpznsx3ea5y1vqa
created_at: 2026-09-07T08:35:47.069Z
updated_at: 2026-09-07T08:57:48.180Z
closed_at: 2026-09-07T08:57:48.164Z
close_reason: Corrected the observed late-compaction ownership loss and adjacent foreign-metadata case; synthetic regressions failed before and pass after. Forty-nine focused tests, lint and types pass, and coordinator independent inspection/replay accepts the exact correction. Non-compaction legacy-boundary assumptions remain explicit. Published cost reconstruction follows the source commit.
resolution: null
duplicate_of: null
---
The existing codex_log_rollup legacy fallback treats the first thread_settings_applied event as inherited-history boundary even when there is no foreign session_meta. A later compaction can therefore erase previously counted owned work before a frozen cutoff. Three session092 descendants reproduce the error; the same07:36:15 snapshot falls from12 to9 sessions on replay. Repair ownership parsing with a late-settings append regression, retain true inherited-history exclusion and explicit ordinal controls, independently review, and rebuild cost receipts only after acceptance. Raw diagnosis stays in attic/agenda-028-overnight; do not publish private log prose.
