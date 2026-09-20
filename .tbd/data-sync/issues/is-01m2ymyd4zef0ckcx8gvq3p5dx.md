---
type: is
id: is-01m2ymyd4zef0ckcx8gvq3p5dx
title: Make PRs 199–202 independently ready to land
kind: epic
status: open
priority: 1
version: 14
labels:
  - correctness
  - stack-readiness
dependencies:
  - type: blocks
    target: is-01m2ymyxppsc63e2m2jd9w24hs
  - type: blocks
    target: is-01m2yn2rzrz9stg4manxy4y4nh
  - type: blocks
    target: is-01m2yn3dx6q07qwp7bhb6ycqdp
  - type: blocks
    target: is-01m2yn3txpz3vav8ys6kw7ek8d
  - type: blocks
    target: is-01m2yn5fgm4x4szv7gmxm7s2gj
  - type: blocks
    target: is-01m1x85bf7x32ewcd07348j8dq
  - type: blocks
    target: is-01m2y4rc2vd88gs3aht7295an5
child_order_hints:
  - is-01m2ymzj2ts1jh3bn536pkhtrp
  - is-01m2ymzy4tz2n47g8ttd8qspv0
  - is-01m2yn0dnnwcy69jb14mzznmga
  - is-01m2yn0rpa5aht3r3qd1mewpw0
  - is-01m2ynhxeecetevy3sn2djwtpq
created_at: 2026-09-20T05:34:39.774Z
updated_at: 2026-09-20T05:54:52.323Z
---
User-requested follow-up to the Session 142 senior review and PR 202 corrections. Prepare the existing stack for safe individual landing in dependency order 199 -> 200 -> 201 -> 202. Baselines: PR199 c877006b, PR200 a85d50ac, PR201 2aaa296d; corrected PR202 8cab8309 (implementation 8dbc1068). The corrected cumulative implementation passed 80 checkpoint steps, but that does not validate unchanged lower heads. Source: docs/project/reviews/review-2026-09-19-pr199-201-correctness.md and https://github.com/jlevy/squares/pull/202. Move or port every correction to the earliest applicable layer, regenerate each layer against its own retained results, and restack dependants without losing reviewed changes. Keep original failure receipts as historical evidence and record new head/base pairs. Done when every PR has an independent review disposition, passing complete validation for its current source/base and a truthful PR body, and the final tip retains all corrections. The four landing-layer repairs are planned for a later execution pass, which must preserve unrelated work and does not authorize merging. The owner subsequently requested an immediate publication audit of the existing corrected tip, tracked separately by child think-kq00; retain that follow-up when restacking. Child beads own implementation and final verification.
