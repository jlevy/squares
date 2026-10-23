---
type: is
id: is-01m5k6ez8h4y01f6pf35ceqfsj
title: Migrate stale tests to one canonical All Results table
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-all-results-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:37:00.687Z
updated_at: 2026-10-23T01:37:16.834Z
started_at: 2026-10-23T01:37:16.833Z
---
Own test_site_navigation.py, test_overview.py, test_overview_sections.py, test_site_urls.py and obsolete Recent-only test module/fixtures. Preserve complete canonical filters, replace removed producer assertions with compatibility-forwarder coverage; root alone commits/pushes.
