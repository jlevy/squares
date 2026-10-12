---
type: is
id: is-01m4mybh5kcffr8zqzm2ajg86e
title: "Address PR #406 review A: added-blob guard calibration, grandfathering, docs"
kind: task
status: closed
priority: 1
version: 12
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4aj1fjtr7gaa8x3p76rr12r
child_order_hints:
  - is-01m4myc15dmwhy5hh8dw0hhwmx
  - is-01m4myc470x5gxhz9djwy3xxsx
  - is-01m4myc8vpg4t7wycn46x9tgp9
  - is-01m4myccq01sqyzzw4tyxhz2xh
  - is-01m4mycgjrz4e4w2trtbfz54eh
  - is-01m4mycmsagpavh80zb4att6a8
  - is-01m4mycs5gyh74ystfyt32wy3j
  - is-01m4mycxk11twnpq9tkmj01akw
  - is-01m4myd1r991kj66tppaefvaz9
hold: null
hold_until: null
created_at: 2026-10-11T07:38:06.386Z
updated_at: 2026-10-11T18:58:32.029Z
started_at: 2026-10-11T07:39:04.408Z
closed_at: 2026-10-11T18:58:32.028Z
close_reason: "Review A on PR #406 addressed at 8811bd763; all nine findings fixed; follow-up think-xeav open. Disposition: https://github.com/jlevy/squares/pull/406#issuecomment-6112530517"
resolution: null
duplicate_of: null
---
Addressing review A (https://github.com/jlevy/squares/pull/406#pullrequestreview-5482287656) on jlevy/squares#406 at head 7f4114a. Owner decisions (coordinating session, 2026-10-11): fix A1 in the PR (aggregate once per path at the largest version, per-blob ceiling over all history, census built into the tool); grandfather at base for A2 (paths over the per-blob ceiling at base.sha are exempt; new large blobs on new paths refused; a bead tracks moving those files to hosted data).
