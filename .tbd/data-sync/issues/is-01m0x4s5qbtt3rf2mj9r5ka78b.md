---
type: is
id: is-01m0x4s5qbtt3rf2mj9r5ka78b
title: "PR37-S1: make generated recurrence wording match the recurrence list"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m0x4c75pqtywfdr4cfnzzvhp
created_at: 2026-08-25T19:01:33.027Z
updated_at: 2026-08-25T19:11:21.580Z
closed_at: 2026-08-25T19:11:21.579Z
close_reason: "Fixed in b450072: render_defects now reports the actual recurrence list without the false singular once qualifier; defects.md was regenerated, not hand-edited."
resolution: null
duplicate_of: null
---
PR #37 notes that render_defects says the unprotected-fix list has predicted a recurrence 'once' while it immediately enumerates many recurrence pairs. Replace the false singular wording in the generator, then regenerate defects.md; do not hand-edit the generated view.
