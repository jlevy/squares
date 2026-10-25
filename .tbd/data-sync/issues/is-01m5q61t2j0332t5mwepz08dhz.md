---
type: is
id: is-01m5q61t2j0332t5mwepz08dhz
title: "Stage 4: review T-241 (Couzo's 304) and T-242 (Daniel's 268 and 304), then adopt 268 and 304"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-map-hx0e-1024
labels:
  - result-import
  - validation
  - packing
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5qsbkgnvjscxj2cv8bny4mz
hold: null
hold_until: null
created_at: 2026-10-24T14:46:47.122Z
updated_at: 2026-10-25T00:39:52.269Z
started_at: 2026-10-24T21:11:59.708Z
---
Stage 4 of the think-l49q import (PR #792, records lane c-import-l49q-1024). T-241 registers Francisco Couzo's certificates/best/n304.cert at franciscouzo/square-packing@fa6237e (Kirill Tymchishin's Kaggle packing, 2.53e-3 below T-186) and T-242 Evan Daniel's exact descents at evand/square-packing@8a8879a (268, 4.48e-12 below T-240, another placement of #763's arrangement; 304, 3.04e-9 below T-241, T-241's packing descended), both at V0/C0, drafts S3 and S2.

Owed: one mapped stage 4 review (tbd-strong-max) of both entries, separate from the records lane: the three certificates on a clean-room checker, the sharp controls at 1e-15 and 5e-21 margins, the side prints, the measured identities (packets' measure/identity.json; T-240's review RF-6 at 268), the credit chains at 268 and 304, and the drafted scores. Then one adoption change at 268 and 304 with both strong generators' regularization of each new house; at 268 the house credit follows the placement adopted (Daniel after Lavrentev, not #763's), so decide it together with T-240's 268 after think-zjus.

Inputs: packing/resources/web/evand-kaggle-descents-2026-10-24/, packing/resources/web/couzo-n304-2026-10-23/, campaign/issue-intake/upper-bounds-evand-20261024/. Price: replay under 0.02 CPU-h, review in tokens, regularization 10-50 CPU-min per count.

blocked_on: jlevy/squares#792, think-zjus

## Notes

2026-10-25 c-map-hx0e-1024 (H1 of think-hx0e and think-o4m0; coordinator coord-intake-1024). Branch claude/intake-2026-10-24-t241-t242-review (worktree /home/user/wt-hx0e) from main 2ed0ea740.

AUTHOR QUESTIONS (drafts, not posted; from the stage 4 review docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md)

For Francisco Couzo, for the next reply on #763 (C1, C3 and C4 overlap the #763 review's questions 1 and 6 and the packets' drafted questions; merge them):

C1. In your manifest, do `previous_source` and `previous_reference.seed_credit` name the packing your catalogue held before at that count, or the packing a search started from? At 303 they name Evan Daniel's certificate while `seed_credit` names Lavrentev. Did Tymchishin's "CPU Alternating Reclosure" v3 start from Polkovskyi's `70a033f` packing at 304? And at 364, 450 and 874, which packing did aqibrazadev's and kyleluecke's notebooks start from? (The record now reads the field as the catalogue's previous record and credits those three rows to the notebook authors alone; think-o4m0.)

C2. Your manifest credits the construction of Polkovskyi's `70a033f` 304 to Nate Chaoweeraprasit, and your `RECORD_PROVENANCE.md` keeps Daniil Ostashev's packing credit there. Which do you intend?

C3. At 268, is the `cuda` step before `kirilltym-seam-lp` in your lineage Lavrentev's "CUDA Packing Search", as at 303?

C4. Could you publish the notebooks' `SOURCE_NOTICES.md` files your manifest names at 268 and 304? No commit of the repository holds them.

For Evan Daniel (he has no issue; the coordinator decides where these go):

D1. What is `s268_lightning.predescent.txt`, Tymchishin's v4 packing to 2.47e-10, and did any step of the descent use it? Your JSON's input side is `.input.txt`'s.

D2. Is "finder unknown" at 304 the missing finder field your `TODO.md` notes for Kaggle imports? Do you know who first published that packing, and which notebook versions and dates hold Lavrentev's 268 and kozykappa's 304?

STAGING: select_houses.PENDING_ADOPTION[268] names think-hx0e (open and synced) as the bead that adopts T-242 at 268, reason "next pull request". Keep think-hx0e open until H2 (think-3anz) lands, or re-point the entry to think-3anz once it is synced; H2 takes 268 off the list.
