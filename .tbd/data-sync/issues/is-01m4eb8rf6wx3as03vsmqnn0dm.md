---
type: is
id: is-01m4eb8rf6wx3as03vsmqnn0dm
title: "PR456 D3: validate renderer-selected homepage membership"
kind: bug
status: closed
priority: 1
version: 4
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e37ersbgmvw7ana72wd5an
hold: null
hold_until: null
created_at: 2026-10-08T18:09:06.021Z
updated_at: 2026-10-08T18:14:44.112Z
started_at: 2026-10-08T18:12:58.086Z
closed_at: 2026-10-08T18:14:44.110Z
close_reason: |
  D3 fixed in 3d266f8cc81efb54826d80f3d9921d2d26c5d529. Renderer-derived per-page membership requires the homepage's 51 selected rows and all 116 complete-table rows; required-row deletions still fail on both pages. Three independent D3 controls passed; coordinator live verification passed 118 responses, 51 home rows/184 links and 116 complete rows/392 links. Actual merged deployment remains tracked by parent think-easb and rollout think-7wlz.
resolution: null
duplicate_of: null
---
Astra review D3 (High) was fixed before commit 3d266f8cc81efb54826d80f3d9921d2d26c5d529. Expected homepage membership comes from renderer predicates: 51 home rows and all 116 complete-table rows. Healthy filtered tables and both required-row deletion controls pass. The live check fetched 118 responses and verified 51/184 and 116/392 rows/links. Review: https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
