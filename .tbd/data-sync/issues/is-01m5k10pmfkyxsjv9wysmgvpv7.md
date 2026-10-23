---
type: is
id: is-01m5k10pmfkyxsjv9wysmgvpv7
title: Migrate Verification guide tests to the dedicated page
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-verification-tests
labels: []
dependencies: []
parent_id: is-01m5k0v6n93xzhawh8jb2038sb
hold: null
hold_until: null
created_at: 2026-10-23T00:01:50.217Z
updated_at: 2026-10-23T00:07:09.531Z
started_at: 2026-10-23T00:02:07.483Z
closed_at: 2026-10-23T00:07:09.530Z
close_reason: null
resolution: null
duplicate_of: null
---
Own only Verification-related assertions/fixture in test_overview.py. Retain diagram/rubric/status checks and legacy archive-fragment compatibility coverage after explanatory content moves to verification.html. Coordinate Recent/home edits; root owns runtime and commit.

## Notes

Added verification.html fixture and migrated12Verification-related tests in narrow shared-file hunks. Preserved ladder shape/rubric/tooltip levels, archived row-chip meanings, complete evidence/review-policy/status prose and status-filter links, canonical About guide link, post-table guide action, absence of repeated explanatory body, and legacy fragment forwarding/static fallback anchors. Targeted selection12passed442deselected101.35s; Ruff and diff checks pass. Evidence /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/verification-migration-tests.log. Root owns runtime and commits; Recent/home/helper hunks owned by landings were preserved.
