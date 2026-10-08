---
type: is
id: is-01m4eb8p5zxp3ydac3s0a2gk9p
title: "PR456 D2: align HTML source offsets with literal LF"
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
created_at: 2026-10-08T18:09:03.664Z
updated_at: 2026-10-08T18:14:42.405Z
started_at: 2026-10-08T18:12:57.968Z
closed_at: 2026-10-08T18:14:42.403Z
close_reason: |
  D2 fixed in 3d266f8cc81efb54826d80f3d9921d2d26c5d529. Offsets advance only on literal LF. All five separator controls verified exact source slices and repository-link admission and passed independently. Hosted CI and deployment remain tracked by parent think-easb and rollout think-7wlz.
resolution: null
duplicate_of: null
---
Astra review D2 (Medium) was fixed before commit 3d266f8cc81efb54826d80f3d9921d2d26c5d529. Source offsets follow HTMLParser's literal LF line boundaries. Five controls cover LF, CR, vertical tab, U+2028 and U+2029 and verify exact article content and record admission. Review: https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
