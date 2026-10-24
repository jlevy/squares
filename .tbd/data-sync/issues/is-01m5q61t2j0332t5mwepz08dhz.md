---
type: is
id: is-01m5q61t2j0332t5mwepz08dhz
title: "Stage 4: review T-241 (Couzo's 304) and T-242 (Daniel's 268 and 304), then adopt 268 and 304"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
  - validation
  - packing
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T14:46:47.122Z
updated_at: 2026-10-24T14:46:47.122Z
---
Stage 4 of the think-l49q import (PR #792, records lane c-import-l49q-1024). T-241 registers Francisco Couzo's certificates/best/n304.cert at franciscouzo/square-packing@fa6237e (Kirill Tymchishin's Kaggle packing, 2.53e-3 below T-186) and T-242 Evan Daniel's exact descents at evand/square-packing@8a8879a (268, 4.48e-12 below T-240, another placement of #763's arrangement; 304, 3.04e-9 below T-241, T-241's packing descended), both at V0/C0, drafts S3 and S2.

Owed: one mapped stage 4 review (tbd-strong-max) of both entries, separate from the records lane: the three certificates on a clean-room checker, the sharp controls at 1e-15 and 5e-21 margins, the side prints, the measured identities (packets' measure/identity.json; T-240's review RF-6 at 268), the credit chains at 268 and 304, and the drafted scores. Then one adoption change at 268 and 304 with both strong generators' regularization of each new house; at 268 the house credit follows the placement adopted (Daniel after Lavrentev, not #763's), so decide it together with T-240's 268 after think-zjus.

Inputs: packing/resources/web/evand-kaggle-descents-2026-10-24/, packing/resources/web/couzo-n304-2026-10-23/, campaign/issue-intake/upper-bounds-evand-20261024/. Price: replay under 0.02 CPU-h, review in tokens, regularization 10-50 CPU-min per count.

blocked_on: jlevy/squares#792, think-zjus
