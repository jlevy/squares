---
type: is
id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
title: Inventory site hierarchy and plan intuitive navigation menus
kind: task
status: in_progress
priority: 2
version: 43
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
  - is-01m5k0t5bchr0e2n7cyczxwtjg
  - is-01m5jzwxrmhyeh1tcpxtg8cvjh
  - is-01m5jtq07e40trsr127y0aqbav
  - is-01m5jtnqawg0kc3zvzn1xcvytq
  - is-01m5jxfa9qhqbazdngmhnzzt91
  - is-01m5jzq7zrrkprq1echjh5vcaz
  - is-01m5k1gznm6j706s8hjy1ka2zs
  - is-01m5k1n0dpafhzby7d6d8p6jz5
  - is-01m5k1pebw6hndma4gsaf3ywfn
  - is-01m5k1ssny4wg6a5qbwfvctyw1
  - is-01m5k1tsn8htw7kk0md2ha31qm
  - is-01m5k1wgdjsqp2zwhbqwxqbs6w
  - is-01m5k28sb6vtczn8bf2sd3ke2f
  - is-01m5k2cd1a9qqqrcn3a14facfa
  - is-01m5k2k8bj1rk2msdmp4qhdq73
  - is-01m5k4374cmg5g8agqh26wq5h3
  - is-01m5k43m5fe3n8y79bk535ddtt
  - is-01m5k4ng2vy76gqr37x35s9qxm
  - is-01m5k51ees0skkkd01y57eh8j7
  - is-01m5k5w1hs929afqh5mzmf071t
hold: null
hold_until: null
created_at: 2026-10-22T20:45:47.321Z
updated_at: 2026-10-23T01:26:40.440Z
started_at: 2026-10-22T20:46:24.554Z
---
Implement and validate the site navigation redesign in PR #737: category menus, dedicated destination pages, canonical labels and breadcrumbs, shared typography and layout, and associated design-system refinements.

## Notes

PR #737 implementation and live review. Shared design rules: 35em/630px prose with card-group edges aligned; sans navigation/metadata; text-only footer; canonical destination labels except Overview H1 The Square Packing Problem; homepage sections Visual Atlas and Results; no breadcrumb on standalone Overview/News; plain category breadcrumbs; Report a Result last in Results. Menu keeps original down-closed/up-open endpoints and reverses its animation (-180deg opening). Button text uses the shared subtle caps-spacing token. Recent Results is one arrival-ordered table: every registered result once, newest seven calendar dates initially visible, earlier rows collapsed in the same table, all rows accessible without JavaScript; tracked by think-vasz and think-oala. Verification material moves off Results Archive into verification.html; detailed Project Epistemics remains epistemics.html, linked by a button and real-parent breadcrumb; tracked by think-7r1w and think-6rnk. think-kmpp tracks final rebuild, browser review, registry/link checks, CI fixes and current-head PR validation. Plan: docs/project/specs/active/plan-2026-10-22-site-navigation.md. Keep implementation and validation states distinct; PR remains draft while live review and current-head checks are incomplete.
