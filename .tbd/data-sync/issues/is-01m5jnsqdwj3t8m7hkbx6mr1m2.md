---
type: is
id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
title: Inventory site hierarchy and plan intuitive navigation menus
kind: task
status: in_progress
priority: 2
version: 22
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
  - is-01m5jxkb9be0mqtaf9g2136t09
  - is-01m5jzm40218cv1bv0z37gg25h
  - is-01m5jzpg6q6mjmf5zff98wga9e
  - is-01m5jzz6zg2fabzmkps0fghd5t
  - is-01m5k0v6n93xzhawh8jb2038sb
  - is-01m5k0vqb7h3a15ntqvb15fz23
  - is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-22T20:45:47.321Z
updated_at: 2026-10-23T00:06:42.157Z
started_at: 2026-10-22T20:46:24.554Z
---
Implement and validate the site navigation redesign in PR #737: category menus, dedicated destination pages, canonical labels and breadcrumbs, shared typography and layout, and associated design-system refinements.

## Notes

PR #737 implementation and live review. Shared design rules:35em/630px prose with card-group edges aligned; sans navigation/metadata; text-only footer; canonical destination labels except Overview H1 The Square Packing Problem; homepage sections Visual Atlas and Results; no breadcrumb on standalone Overview/News; plain category breadcrumbs; Report a Result last in Results. Menu keeps original down-closed/up-open endpoints and reverses its animation (-180deg opening). Button text uses shared subtle caps-spacing token. Latest slice: Recent Results becomes one chronological table with last seven days shown and older rows collapsed in that same table. Child beads and docs/project/specs/active/plan-2026-10-22-site-navigation.md track scope and validation. PR remains draft during review and current-head CI.
