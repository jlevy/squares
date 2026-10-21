---
type: is
id: is-01m5fp8c6ssk2j8ftcn7ta5jmy
title: List homepage external resources on their authors profiles
kind: task
status: closed
priority: 2
version: 5
delegate: about_profiles_implementation
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T16:56:04.045Z
updated_at: 2026-10-21T17:05:36.185Z
started_at: 2026-10-21T16:56:23.152Z
closed_at: 2026-10-21T17:05:36.184Z
close_reason: Implemented shared resource model and shared account-link components; reviewed and validated locally, preview refreshed. Source remains uncommitted.
resolution: null
duplicate_of: null
---
Derive profile external-resource lists from the same homepage resource records and exact resolved author identities; preserve homepage byline links and avoid duplicate manually maintained lists.

## Notes

Shared site_resources model now drives homepage bylines/cards, profile Resources lists and directory Resources counts; preserves48exactURLs,45person-owned resources,47relationships across32profiles. No inferred repo ownership. Shared account_links renderer drives full profile accounts and compact table icons.9focused tests+2JS/noJS browser cases pass, Ruff/Biome/types clean, both source reviews passed. Targeted46pages rebuilt and600CSS references refreshed. Changes remain uncommitted.
