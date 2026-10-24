---
type: is
id: is-01m5pjxn8ykge4h67nqv0hgqer
title: "Import evand and franciscouzo: s(268) <= 16.874361715870 and s(304) <= 17.926898900357 (evand/square-packing 8a8879a), and s(304) <= 17.926898903393 (franciscouzo/square-packing fa6237e, Tymchishin's packing) (no issue)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-import-l49q-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T09:12:28.189Z
updated_at: 2026-10-24T14:47:31.000Z
started_at: 2026-10-24T13:38:16.088Z
---

## Notes

2026-10-24 coord-intake-1024, from think-6r5p's triage (c-triage-watch-1024; full verdicts in that bead's notes, tools and data in scratchpad triage-watch/). Report order: 268, #763 16.874361715873825 (23:35:51Z) then evand s268_lightning 16.874361715869346 (pushed 04:53:53Z), -4.48e-12, the exact KKT minimum of the same packing (0 squares beyond 0.1 against #763's and Tymchishin's v4 parent): recorded as a refinement (T-146 precedent), S2. 304 (not claimed by #763): franciscouzo certificates/best/n304.cert first committed in fa6237e, pushed 23:38:42Z, 17.926898903393 (-2.5289e-3 vs T-186; Couzo credits Tymchishin's 'CPU Alternating Reclosure' v3), S3; then evand s304_pub 17.926898900357 (-3.04e-9, the same packing, 4.6e-4 largest move), recorded. 303: evand's s303_cdeotte 17.907238274538 is above #763's 303 and is not recorded. Evan did not post them ('franciscouzo's open #763 already held all three'). Packet pinning 8a8879a (~0.45 MB) and n304.cert at fa6237e. Price < 2 CPU-h (replay < 0.02; two reviews; adoption and regularization at 268 and 304, 10-50 CPU-min each). PR B of #763 adopts 268 after this import (or Evan's packing) so 268 is re-housed once. Author questions (Evan): does he claim the 268 and 304 certificates, with this credit; notebook versions and dates for lightningv08's 268, Deotte's 303 and kozykappa's 304. Leaderboard side-only entries (pjmathematician 303, panpanpanda 268): not reports under 'Several Reports at One Count' (the order is the time a claim reached this repository: an issue, comment, PR or watched-repository commit), so no owner question; they bear only on credit wording, which the authors are asked.
blocked_on: think-ptkk

2026-10-24 c-import-l49q-1024 (records lane, coordinator coord-intake-1024): stages 1 to 3 done in draft PR #792 (https://github.com/jlevy/squares/pull/792), branch claude/intake-2026-10-24-evand-268-304. T-241: Couzo's 304 at fa6237e (packet couzo-n304-2026-10-23, which retains no byte and reads the issue-763 packet's copy), 2.53e-3 below T-186, draft S3. T-242: Daniel's 268 and 304 at 8a8879a (packet evand-kaggle-descents-2026-10-24), 4.48e-12 below T-240 and 3.04e-9 below T-241, draft S2; at 304 a regularization of T-241 (his input is T-241's packing to 2.05e-9); at 268 NOT a regularization of T-240: another placement of #763's arrangement, Lavrentev's placement descended (mirror image of #763's, 135 squares beyond 1e-3, 165 beyond 1e-9; T-240 review RF-6 agrees), credited Daniel after Lavrentev. 303 not recorded (2.60e-4 above T-240's). Ledger campaign/issue-intake/upper-bounds-evand-20261024. Both packets replayed on both routes with gross and sharp controls (18/18). #763's import reply of 13:37:28Z recorded (kind import). New beads: think-hx0e (stage 4 and adoption at 268 and 304), think-jv2s (OR-1 tools).

DRAFT ACKNOWLEDGEMENT FOR EVAN DANIEL (not posted; he opened no issue, so the coordinator decides where it goes; post only after #792 merges, since it names T-242):

Thank you, @evand. Your commit `8a8879a` on evand/square-packing (pushed 24 October at 04:53:53Z) added three certificates of public Kaggle packings that you did not post, since #763 already held the counts. This repository reads a certificate published in a watched repository as a report from its publication, so it has imported two of them, in report order after the reports that came first.

**What was received.** `search/packer/candidates/` at `8a8879a2972c32cbd2d906049228cc9f0762b02a`: `s268_lightning.cert`, `s304_pub.cert` and `s303_cdeotte.cert`, with their JSON reports, binary64 inputs, predescent and exact packings, prior-best comparisons and the 268 regularized view. They are retained under your MIT licence in the packet `evand-kaggle-descents-2026-10-24`, with CREDITS.md's statement that the work was produced by Claude (Anthropic) under human direction.

**268 and 304** are registered as reported, as T-242, at V0/C0. Both certificates pass this repository's two exact routes with their controls refused. Their margins (walls 5e-21, pairs about 1e-20) are below binary64 spacing, so sharp controls took each to exact contact and 1e-30 past it, and both routes decided all six as required at each count.
- 268: s(268) <= 8437180857934672912242411148233/(5*10^29), 4.48e-12 below Francisco Couzo's #763 (T-240), which moves the 12-place print from 16.874361715874 to 16.874361715870. Measured pose by pose, it is Lavrentev's placement descended (no square moves beyond 1e-3 from your input) and another placement of the arrangement #763 refines: the mirror image, with 135 squares differing by more than 1e-3. The record credits it "Daniel after Lavrentev", as your commit says.
- 304: s(304) <= 1792689890035674158972360842897/10^29, 3.04e-9 below Couzo's certificate of the same packing at franciscouzo/square-packing@fa6237e (T-241, reported first, at 23:38:42Z on 23 October). Your input is that packing to 2.05e-9, so the record lists yours as its regularization.
- 303: `s303_cdeotte.cert` is 2.60e-4 above #763's 303, which reached this repository first, so it is not recorded; it is retained as credit evidence.

A mapped review comes next, then adoption at 268 and 304 with both drawings regularized.

**Questions**, which hold nothing the record states:
1. Do you claim the 268 and 304 certificates at `8a8879a` as bounds, with this credit: at 268 "Daniel after Lavrentev" (your exact descent of Vladislav Lavrentev's public lightningv08 packing), and at 304 your exact descent of the public packing that Couzo's index credits to Kirill Tymchishin's "CPU Alternating Reclosure" v3, whose finder you name as unknown?
2. Which notebook versions and dates hold lightningv08's 268, Chris Deotte's 303 and kozykappa's 304? In particular, was Lavrentev's 268 public before #763 (23 October, 23:35:51Z)?
3. `s268_lightning.predescent.txt` is #763's Kaggle parent at 268 (Tymchishin's EDA+Seam LP v4 packing) to 2.5e-10, while `s268_lightning.input.txt` is Lavrentev's placement. What is the predescent file, and which of the two did the descent start from?
