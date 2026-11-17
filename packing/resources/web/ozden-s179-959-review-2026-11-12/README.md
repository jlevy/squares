# Stage 4 Review of #959: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L108’s blind stage 4 review of
issue [#959](https://github.com/jlevy/squares/issues/959), Doğa Özden’s
$s(179) \le 13.880960371559$:
[`docs/project/reviews/review-2026-11-12-ozden-959.md`](../../../../docs/project/reviews/review-2026-11-12-ozden-959.md).

The source is `n-179-candidate.yaml` of
[kenaznia-doga/s179-upper-bound-13880960371@6ab3cfe](https://github.com/kenaznia-doga/s179-upper-bound-13880960371/tree/6ab3cfe60db4d081092bed3b6bbb44c76b067230),
SHA-256 `77ee3dd21e35ca6abd1410ad3a7ff25b44c5bbc0fe5ebd1031ae112126bf61fc`. It is not
retained here; an import lane would retain it in its own packet. This directory is
review-only.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched, and the
  run scripts.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L108’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of the review of #954 (lane L101), whose text was the model and whose programs were
not opened. Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a
checkout of `main` at `c8448724e`, through `uv run --frozen --all-extras --group dev`,
under `nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l108_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l108_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l108_clip.py` | method B: unit squares, walls and pairs by exact clipping of closed polygons in `fractions.Fraction` | integers from the reader | nothing (a module) |
| `l108_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n179.json` |
| `l108_geom.py` | nothing: builds squares, moves and closing times for the self-test and the controls | fractions | nothing (a module) |
| `l108_selftest.py` | both methods and the reader against 8,453 cases, and two broken copies | nothing | `out/selftest.json` |
| `l108_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, the check receipt | `out/plan-facts-n179.json` |
| `l108_make_plan.py` | nothing: states the 19 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l108_controls.py` | the 19 controls, by both methods or the reader | the certificate, the plan, the plan facts, the check receipt | `out/controls-n179.json` |

`run_frozen.sh SOURCE_DIR OUT_DIR` reruns the self-test, the check, the plan facts, the
plan and the controls.

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l108_wit.py` | nothing: reads Witness/v2 files (corners, center-basis rational or number field, center-angle decimal) into 60-digit poses | witness files | nothing (a module) |
| `l108_sides.py` | the claim’s arithmetic: the side’s prints, both gains, $s(70) + 5$, $s(207)$, the leaderboard values | the certificate, #954’s certificate, `programs/issue-959.json`, the case record and witnesses at 179, 70 and 207, the author’s README and printed outputs | `out/sides.json` |
| `l108_house.py` | decides a house witness and #954’s certificate with the frozen `l108_check.decide` | T-174’s or T-291’s witness, #954’s certificate and twin | `out/house-n179.json`, `out/house-t291-main.json` |
| `l108_pose.py` | a certificate against its decimal pose at 60 digits, every pair’s relative gap, the uniform contraction and the near-wall clearances | a certificate, its pose, the 70 witness | `out/pose-n179.json`, `out/pose-n954.json` |
| `l108_s70.py` | the 70 and 207 packings placed in the 179 box, the band’s angles, the lattice squares, the stated seed | the certificate, the 70 and 207 witnesses | `out/s70-n179.json` |
| `l108_identity.py` | the certificate against T-174, #954 and T-291, pose by pose, under eight symmetries and five anchorings | the certificate, the three references | `out/identity-n179.json` |
| `l108_contract.py` | decides the certificate’s squares contracted uniformly, with the frozen `l108_check.decide` | the certificate and its twin, the 70 witness | `out/contract-n179.json` |
| `l108_custody.py` | read-only Git plumbing on the clone and this repository | the clone, this repository, the issue | `out/custody.json` |
| `l108_digests.py` | every frozen digest against the kept bytes, and the digest of every file here | this directory | `out/program-digests.json` |

`run_after.sh SOURCE_DIR SOURCE954_DIR T291_HOUSE REPO_DIR OUT_DIR` reruns them, except
`l108_digests.py`. `SOURCE954_DIR` holds #954’s certificate, twin and decimal pose as
retained in `packing/resources/web/ozden-s179-upper-bound-2026-11-11/source/`;
`T291_HOUSE` is `packing/witnesses/known-best/n-179.yaml` from `main` at `b5b12c206`;
`REPO_DIR` is a checkout of `main` at `c8448724e`.

## What They Printed

- `l108_selftest.py`: `PASSED 8453 cases, 0 failed`; broken method A fails 832, broken
  method B 908.
- `l108_check.py`: `ACCEPT`, 15,931 pairs apart by both methods, wall contacts square 67
  bottom, 123 left and 162 top, least gap $1.99223328482862 \times 10^{-13}$ at (104,
  105).
- `l108_controls.py`: `EVERY_CONTROL_AS_STATED`, 19 of 19.
- `l108_house.py`: T-174 `ACCEPT` with one touching pair (119, 122); #954 and T-291
  `ACCEPT`, least gap $2.03083381521852 \times 10^{-13}$ at (14, 15).
- `l108_contract.py`: contractions by $10^{-13}$, $1.9 \times 10^{-13}$ and
  $1.99 \times 10^{-13}$ `ACCEPT` (the last at side 13.88096037155566185), by
  $2 \times 10^{-13}$ `REFUSE`.
- `l108_digests.py`: `ALL_FROZEN_DIGESTS_HOLD`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files and the receipts they had written | 2026-11-11T22:03:30Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l108_controls.py` existed | 2026-11-11T22:05:38Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-11T22:11:47Z |
| `frozen/review-2026-11-12-ozden-959.frozen.md` | the review as frozen, before the author’s checkers, outputs or README, or this repository’s verifier, were read | 2026-11-11T22:11:47Z, pushed as `5dc328b67` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
