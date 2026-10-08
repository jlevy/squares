---
type: is
id: is-01m4eb8p5zxp3ydac3s0a2gk9p
title: "PR456 D2: align HTML source offsets with literal LF"
kind: bug
status: open
priority: 2
version: 1
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e37ersbgmvw7ana72wd5an
created_at: 2026-10-08T18:09:03.664Z
updated_at: 2026-10-08T18:09:03.664Z
---
Initial Astra correctness review findingD2, Medium, fixed before head3d266f8cc81efb54826d80f3d9921d2d26c5d529. HTMLParser positions advance on LF only; source offsets now use literal LF boundaries. Allfive LF/CR/vertical-tab/U+2028/U+2029 controls verify exact article content and record admission. Public review https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
