---
type: is
id: is-01m5k1ssny4wg6a5qbwfvctyw1
title: Use sans-serif for general site descriptions and serif for mathematical exposition
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-landings
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:15:32.540Z
updated_at: 2026-10-23T00:24:35.140Z
started_at: 2026-10-23T00:15:39.803Z
---
Apply typography by content purpose: general site descriptions, collection introductions, contributor-directory summaries, contribution prompts and reading/navigation guidance use shared sans-serif. Substantive mathematical exposition, including the homepage square-packing problem explanation, remains serif. Audit analogous page introductions, use semantic shared classes rather than blanket paragraph overrides, document the rule and verify rendered examples.

## Notes

Source complete: general site/navigation guidance uses the existing shared site-navigation-copy role across Overview contribution/read/media/document/resource invitations, profile preview and Contributor Profiles directory introduction, Tutorials/Resources/Posters introductions, Project Documentation repository lead, Report instructions, About resource cross-link, and the Results Archive navigation-only lead. No blanket paragraph CSS change. Opening homepage explanation of square packing and upper/lower bounds, substantive mathematical narratives, and News bodies remain serif. Focused real-render semantic check passed as part of four passed in85.72s; Posters forwarder rerun separately passed in12.64s. Shared typography purpose distinction and all current request beads are recorded in the navigation plan; components owns the matching Design System entry. Ruff check/format and diff-check clean. Coordinator owns final full-build/browser/CI receipt.
