---
type: is
id: is-01m4eb8kz1h7j4ehrj1kzdkky0
title: "PR456 D1: reject global popover ID shadows"
kind: bug
status: closed
priority: 2
version: 4
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e37ersbgmvw7ana72wd5an
hold: null
hold_until: null
created_at: 2026-10-08T18:09:01.306Z
updated_at: 2026-10-08T18:14:40.246Z
started_at: 2026-10-08T18:12:57.695Z
closed_at: 2026-10-08T18:14:40.245Z
close_reason: |
  D1 fixed in 3d266f8cc81efb54826d80f3d9921d2d26c5d529. Global opening-tag ID accounting rejects completed, unclosed and void target shadows. All six final shadow controls passed independently. Final author suite: 99 passed; independent final controls: 15 passed. Hosted CI and actual deployment remain tracked by parent think-easb and rollout think-7wlz.
resolution: null
duplicate_of: null
---
Astra review D1 (Medium) was fixed before commit 3d266f8cc81efb54826d80f3d9921d2d26c5d529. The checker counts IDs on every opening tag and requires one global popover target, including completed, unclosed and void shadow elements. All six shadow controls pass. The author passed 99 cases and Astra independently passed 15 final controls. Review: https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
