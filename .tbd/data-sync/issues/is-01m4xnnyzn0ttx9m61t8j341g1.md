---
type: is
id: is-01m4xnnyzn0ttx9m61t8j341g1
title: Link news people to profiles using reviewed preferred names
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: news-profile-implementation
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-14T16:59:40.916Z
updated_at: 2026-10-14T18:19:24.729Z
started_at: 2026-10-14T17:00:49.868Z
closed_at: 2026-10-14T18:19:24.728Z
close_reason: null
resolution: null
duplicate_of: null
---
Integrate the upstream news/changelog with explicit profile links and reviewed preferred real names. Preserve quotations, source handles and project branding; test site and Markdown rendering and document the attribution rule.

## Notes

Completed and pushed in draft PR #578 at 8270752fe. News uses reviewed preferred names and direct profile links; attribution policy and plan updated. Changelog tests 29 passed, profile whole modules 98 passed, publishing 47 passed; Astra review clean. Final hosted CI: 31 passed, 27 intentionally skipped, zero failures or pending. Broad local checks had a timeout and later low-scratch interruption; both documented in PR rather than claimed green.
