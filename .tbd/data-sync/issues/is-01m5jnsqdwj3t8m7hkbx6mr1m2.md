---
type: is
id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
title: Inventory site hierarchy and plan intuitive navigation menus
kind: task
status: in_progress
priority: 2
version: 13
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-planner
labels: []
dependencies: []
child_order_hints:
  - is-01m5jq8b32egqx16z724xngj59
  - is-01m5jq8bjb8er6jweszgp9x5mj
  - is-01m5jq8c0kfqxsnqmrgvm0ym10
  - is-01m5jq8cemstqzfjt2dn134wh1
  - is-01m5jq9hg33d9asv584eysj0zq
  - is-01m5jqhrkzpwj9djae1zf261c7
  - is-01m5jqhs3kdd35n4fb15c8mc54
  - is-01m5jqhsjcznm3w2f8kv5sw2b5
  - is-01m5jwa8f3se8mazs5yyrf7dq6
hold: null
hold_until: null
created_at: 2026-10-22T20:45:47.321Z
updated_at: 2026-10-22T23:00:27.533Z
started_at: 2026-10-22T20:46:24.554Z
---
Inventory every current page family, each named page/subpage, top tabs, local tabs, breadcrumbs and cross-links. Model as a tree and propose top-level tabs with menu items. Planning only, in parallel with landing PR733; keep its implementation unchanged.

## Notes

Implementation is in PR #737 on codex/site-navigation-plan-20261022. The navigation split, dedicated Learn/About pages, breadcrumbs, 33em reading measure, and shared menu motion are implemented and locally rebuilt. Current follow-up: split Results into Recent Results, Results Archive, Visual Atlas, and Verification and Ratings without a category landing page. CI failures from the prior head are being triaged and fixed; PR remains draft until current-head validation passes.
