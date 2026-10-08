---
type: is
id: is-01m4eb8rf6wx3as03vsmqnn0dm
title: "PR456 D3: validate renderer-selected homepage membership"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e37ersbgmvw7ana72wd5an
hold: null
hold_until: null
created_at: 2026-10-08T18:09:06.021Z
updated_at: 2026-10-08T18:12:58.086Z
started_at: 2026-10-08T18:12:58.086Z
---
Initial Astra correctness review findingD3, High, fixed before head3d266f8cc81efb54826d80f3d9921d2d26c5d529. Expected page membership now comes from renderer predicates:51 home rows and all116 complete-table rows. Healthy filtered-table and both missing-required-row controls passed; live118 responses passed51/184 and116/392 rows/links. Public review https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
