---
type: is
id: is-01m5k1ssny4wg6a5qbwfvctyw1
title: Use sans-serif for general site descriptions and serif for mathematical exposition
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-tracker-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:15:32.540Z
updated_at: 2026-10-23T01:36:52.787Z
started_at: 2026-10-23T00:15:39.803Z
closed_at: 2026-10-23T01:36:52.786Z
close_reason: Superseded by explicit latest user serif-introduction and All Results consolidation requests; replacement behavior/evidence and active owner references recorded in notes.
resolution: null
duplicate_of: null
---
Apply typography by content purpose: general site descriptions, collection introductions, contributor-directory summaries, contribution prompts and reading/navigation guidance use shared sans-serif. Substantive mathematical exposition, including the homepage square-packing problem explanation, remains serif. Audit analogous page introductions, use semantic shared classes rather than blanket paragraph overrides, document the rule and verify rendered examples.

## Notes

Source complete: general site/navigation guidance uses the existing shared site-navigation-copy role across Overview contribution/read/media/document/resource invitations, profile preview and Contributor Profiles directory introduction, Tutorials/Resources/Posters introductions, Project Documentation repository lead, Report instructions, About resource cross-link, and the Results Archive navigation-only lead. No blanket paragraph CSS change. Opening homepage explanation of square packing and upper/lower bounds, substantive mathematical narratives, and News bodies remain serif. Focused real-render semantic check passed as part of four passed in85.72s; Posters forwarder rerun separately passed in12.64s. Shared typography purpose distinction and all current request beads are recorded in the navigation plan; components owns the matching Design System entry. Ruff check/format and diff-check clean. Coordinator owns final full-build/browser/CI receipt.

SUPERSEDED by latest explicit user instruction: all bare standalone introductions are serif, including homepage contribution/Learn/report text and profile introduction; headings/navigation/buttons/filters/metadata remain sans. Shared site-navigation-copy now uses prose family/400. Replacement introduction contract passed1case35.32s and root pushed1f682c650. The prior sans-introduction implementation was completed earlier but is no longer the requested design; no remaining work under this obsolete direction.
