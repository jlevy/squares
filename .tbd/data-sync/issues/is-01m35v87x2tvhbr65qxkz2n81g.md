---
type: is
id: is-01m35v87x2tvhbr65qxkz2n81g
title: Stop timing-record findings and a red main from failing pull requests that did not cause them
kind: task
status: open
priority: 1
version: 1
spec_path: packing/campaign/agendas/agenda-042-efficiency-block-the-development-cycle.md
labels:
  - focus-efficiency
  - ci
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-23T00:39:34.561Z
updated_at: 2026-09-23T00:39:34.561Z
---
agenda-042 BC-377. Of 15 sampled red runs across the last 20 merged PRs, 4 were gate-budget findings (a stale or flattering record in devtools/gate-budgets.yaml: PRs 200, 205, 212, 218) and 4 were inherited from a red main (PRs 208, 209, 211 failed the identical test_session_gate assertion within about two hours while main was red at c2cc1cf6; PR 200 a suite-a concurrency assertion). Neither class is caught by any local tier, and neither is caused by the change under review. Owner decision wanted: which gate-budget rules (ceiling, drift, stale) should fail a pull request, and which should report there and fail on main or a scheduled re-baseline via devtools.read_tier_walls; and how a red main is kept from propagating into open branches.
