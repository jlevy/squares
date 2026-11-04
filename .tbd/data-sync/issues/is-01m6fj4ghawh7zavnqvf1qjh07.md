---
type: is
id: is-01m6fj4ghawh7zavnqvf1qjh07
title: "Licence follow-up: kenaznia-doga/s94-lower-bound@9d76ad5 states no licence (#890)"
kind: task
status: in_progress
priority: 3
version: 7
delegate: bold-ritchie-l44
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-03T01:59:44.938Z
updated_at: 2026-11-04T18:29:08.023Z
started_at: 2026-11-04T11:55:19.157Z
---
kenaznia-doga/s94-lower-bound@9d76ad5549e99e952c899462b36d2bd765517969 (#890) has no licence file and names no licence. The ozden-s94-lower-bound-2026-11-03 packet retains it under the presumption of permission for a source its author submits (owner, 24 October 2026, think-cnn7; licence follow-ups as think-m8f4 and think-nu37). Ask the author, in #890's acknowledgement, under which licence the certificate, receipts and second-checker code are published; record the answer in the packet's declaration and README. Does not hold the import (think-2agl).

## Notes

2026-11-04 coordinator: the licence question was put to the author in #890's closing comment (https://github.com/jlevy/squares/issues/890#issuecomment-6628729226, 10:46Z). think-2agl is closed; this bead now waits on the author's answer on #890 (closed issues still notify). When it arrives, record it in the ozden-s94-lower-bound-2026-11-03 packet's declaration and README and close this bead. The packet keeps the presumption of permission meanwhile (think-cnn7).
2026-11-04 coordinator (after #900, 7deb5209f): when the author answers the licence question, the follow-up reply on #890 that records it should also name E-ozden-890-n94-9965-sqverify-fast-replay and E-ozden-890-n94-9965-review-sample, which the sweep lists as owed (the #238 precedent: no comment posted only to name ids).
blocked_on: none
2026-11-04 bold-ritchie-l44 (lane L44; reassigned from bold-ritchie with --delegate on the coordinator's instruction): the lab answered on #890 (issuecomment-6637821113, 17:49:05Z): certificates, witnesses, receipts, data and write-ups CC BY 4.0, all source code (second checker included) MIT, copyright 2026 Doğa Özden; LICENSE.md added at kenaznia-doga/s94-lower-bound 484ad20f, s299-upper-bound 0c61a555, s204-upper-bound 06b0bf99 (17:48:55Z-17:48:57Z). Each commit adds only LICENSE.md (tree = pin tree + that file); the three files are byte-identical (1,484 B, blob 9803370f, SHA-256 5b8e1449...da4c). Question 2: no side between 9.965 and ~9.9729 was tried. Recorded in draft PR https://github.com/jlevy/squares/pull/905 (head 3773b3a72): each packet stays at its pin and retains licence/LICENSE.md; declaration, sources.json, README, report.json notes, bibliography.yaml, resources/README.md state the licence; three intake-watch reads; #890 read_through 17:49:05Z; no-public-change record (methods survey, 43 files identical x3 vs main 23362113f). Records gate 55/55. Close this bead (and think-mdxq) after #905 merges and the #890 follow-up is posted and recorded.

DRAFT follow-up for #890 (not posted; post after #905's merge and deploy, must end with the Generated-by footer):
---
@kenaznia-doga, thank you, and thank you to Doğa Özden, for answering both questions.

**The licence is recorded.** Certificates, witnesses, receipts, data and write-ups are under CC BY 4.0, and all source code, the second checker included, under MIT, copyright 2026 Doğa Özden. Each of your three licence commits adds only `LICENSE.md`, so the files kept here at the earlier pins are covered unchanged. Each packet now keeps its repository's `LICENSE.md` byte for byte, with its commit, and its declaration and README state the licence in place of the presumption of permission your submissions carried:

- `s94-lower-bound` at `484ad20f`, for this issue: [`ozden-s94-lower-bound-2026-11-03`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s94-lower-bound-2026-11-03/README.md)
- `s299-upper-bound` at `0c61a555`, for #893: [`ozden-s299-upper-bound-2026-11-03`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s299-upper-bound-2026-11-03/README.md)
- `s204-upper-bound` at `06b0bf99`, for #894: [`ozden-s204-upper-bound-2026-11-03`](https://github.com/jlevy/squares/blob/main/packing/resources/web/ozden-s204-upper-bound-2026-11-03/README.md)

**The finer net.** Noted: 9.965 is the only side the lab certified on the finer net, and no side between it and the route's ceiling, 99500/9977 ≈ 9.9729, was tried. The record claims nothing between them.

**The two evidence entries behind T-262.** The closing reply described them without naming them:

- `E-ozden-890-n94-9965-sqverify-fast-replay` is this repository's complete replay. `sqverify-fast`, built from its reviewed source, decided the retained certificate at all 600 directions of its declared net on 3 November, and the whole-net control passed on 4 November. It is **confirmed**, reproduced with the producer's code, since your lab ran the same checker, and it is the entry that holds T-262 at V3/C3.
- `E-ozden-890-n94-9965-review-sample` is the stage 4 review's own run, with code of its own. It decided direction 0 in full, held the least-bound box of each of the other 599 directions exactly, and refused five mutants. It is a **sample**, 1 of 600 directions: it decides the direction it ran and confirms nothing beyond it, so it sets no rung.

T-262, s(94) ≥ 1993/200, stands as before: **V3/C3, confirmed**, and current at n = 94.

**On `main` and the site.**
- [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md)
- [`packing/frontier/n-094.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-094.md)
- [T-262](https://squaremath.org/result/t-262.html)

Thank you also for correcting the READMEs. The packets keep the versions at their pins, and we will read the corrected ones when they land.

The issue stays closed; this reply only brings what the record says up to date.

---
_Generated by [Claude Code](https://claude.ai/code)_
---

DRAFT follow-up for #366 (not posted; same conditions):
---
@wand125, a short follow-up to our reply of 31 October, which gave T-110 as the current lower bound at n = 39.

**Correction.** T-110, your check2 certificate of 6 October, s(39) ≥ 133/20 = 6.65, still stands as a verified bound, **V3/C3, confirmed**. It is no longer the best known: on the frontier it now reads **superseded**.

**What superseded it.** T-176 is your own fine-net certificate of 13 October, `mixed_n39_L66625`, which proves s(39) ≥ 533/80 = 6.6625, 1/80 above T-110: a density of 687 rectangles of total mass 3899999/100000 on a declared net of 2,073 half-angle tangents of step 1/5002 at core side 4999/5000. This repository's `sqverify-fast` replayed it at all 2,073 directions on 2 November, its whole-net controls passed on 3 November, and the review of 14 October had read its mathematics. It was confirmed at V3/C3 on 4 November (#889), and both of n = 39's lower bounds are now 533/80. #446, where you reported it, has its own follow-up.

**On `main` and the site.**
- [`packing/frontier/n-039.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-039.md)
- [T-110](https://squaremath.org/result/t-110.html)
- [T-176](https://squaremath.org/result/t-176.html)

The issue stays closed; this reply only brings what the record says up to date.

---
_Generated by [Claude Code](https://claude.ai/code)_
---
blocked_on: none
