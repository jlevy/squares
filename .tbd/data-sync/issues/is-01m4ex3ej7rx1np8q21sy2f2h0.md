---
type: is
id: is-01m4ex3ej7rx1np8q21sy2f2h0
title: Add shared Headroom navigation on desktop and mobile
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
labels:
  - website
dependencies:
  - type: blocks
    target: is-01m4ex3gpzxxh9eqemc2r78p4e
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
created_at: 2026-10-08T23:20:46.406Z
updated_at: 2026-10-08T23:20:48.607Z
---
The owner confirmed usual Headroom behavior: hide while scrolling down and reappear immediately when scrolling up. Keep the header visible at the top, while it contains focus, and while its theme menu is open. Implement once across KPress pages, generated case/result/synopsis pages, the paper shells, Visualize tabs and the Workbench. Preserve reduced-motion and static fallback behavior, responsive wrapped height, anchor offsets and theme-menu attachment. The Workbench document does not scroll, so its header stays visible. See L5 in the spec.
