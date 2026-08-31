---
type: is
id: is-01m0x4kdeawv6s469m55ns3agb
title: "PR37-F3: align the review record with formal assurance terminology and current integration state"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0x4c75pqtywfdr4cfnzzvhp
created_at: 2026-08-25T18:58:24.329Z
updated_at: 2026-08-25T19:11:21.045Z
closed_at: 2026-08-25T19:11:21.044Z
close_reason: "Fixed in b450072: reserved verified for exact/formal conclusions, renamed the integrated hypothesis H-043, corrected defect and CI identities, and added integration dispositions."
resolution: null
duplicate_of: null
---
The review says broad headline claims were verified, although the set includes source comparisons and a finite numerical sweep; it also names branch-local status, stale D-320/D-321 identities, and e137bf9 as the CI head even though that is the base. Preserve exact-verification wording only for the exact certificate, use checked/replayed/rederived elsewhere, and label original versus current dispositions.
