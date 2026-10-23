---
type: is
id: is-01m5k0v6n93xzhawh8jb2038sb
title: Separate Verification guide from Results Archive and link detailed Project Epistemics
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-verification
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
child_order_hints:
  - is-01m5k10pmfkyxsjv9wysmgvpv7
hold: null
hold_until: null
created_at: 2026-10-22T23:58:50.023Z
updated_at: 2026-10-23T00:07:08.041Z
started_at: 2026-10-22T23:59:01.056Z
---
Move all explanatory content below Results Archive into a dedicated Verification page at verification.html. Keep Results Archive focused on its table. Link the detailed Project Epistemics page at epistemics.html with a button; it is not a category landing or menu entry. Use Results / Verification / Project Epistemics breadcrumbs, with plain category labels and a clickable real Verification parent. Register the new page and preserve old results.html verification fragments through forwarding and no-JavaScript fallback links. Migrate relevant tests and update plan/design references.

## Notes

Source implementation is present, including template extraction, renderer, page metadata/registry, build inputs and legacy-fragment forwarding. Registry generation reports 1156 rows and zero failures. Child think-6rnk owns test migration. Final assembled build, browser check and current-head CI remain pending; do not close on source completion alone.
