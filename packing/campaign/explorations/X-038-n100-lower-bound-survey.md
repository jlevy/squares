---
title: X-038 — n<=100 lower-bound survey
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-038
  title: N<=100 Lower-Bound Survey
  date: '2026-09-19'
  author: Cursor session-140 coordinator
  campaign: packing.squares
  brief: >-
    Survey every n<=100 verified lower bound against the known-best or verified upper,
    compare each open gap to covering measurements already on the register, and rank
    which sides the stock colgen (seeded grids, four-grid, window lattices,
    freeze-then-decide) can still push. No new instrument. No bound claim.
  sources:
  - packing/frontier/n-001.md
  - packing/frontier/n-012.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  - packing/frontier/n-019.md
  - packing/frontier/n-020.md
  - packing/frontier/n-021.md
  - packing/frontier/covering-values.yaml
  - packing/frontier/RESULTS.md
  - packing/campaign/agent-sessions/session-139-n11-overnight-research.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/leftover-side-ranking.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-062-h-062-m5-midpoint-rung.md
  - packing/devtools/run_fractional_colgen.py
  proposes: [H-218]
---
# X-038: Which Lower Bounds the Stock Tools Can Still Move

Session-140 asked one question: of the open `s(n)` floors at `n <= 100`, which ones can
the instruments already on the branch still raise?

The instruments are `devtools.run_fractional_colgen` (auto grids, explicit four-grids,
`--seed-certificate`, `--seed-windows`), then `declare_least_cell_mass` and
`decide_certificate`. A freeze is a T-id only when that gate prints `RETAINABLE`.
Nothing here is a bound.

## What the Register Already Knows

Thirty-two sizes in `1..100` are proved equal (`n = 1..10`, `13..16`, `22..25`,
`33..36`, `46..49`, `62..64`, `79..81`). Their floors are not a covering target.

Sixty-eight sizes are open.
Most of those floors are the Nagamochi formula `1 + sqrt(n - 2 floor(sqrt(n)) + 1)`.
First-party fractional certificates sit on seven of them:

| n | Verified floor | Verified ceiling | Gap | Covering already tried above the floor |
| --- | ---: | ---: | ---: | --- |
| 11 | T-026 `3.826447…` | Trump `3.877083…` | 0.051 | Yes. Closest point-atom construction above T-026 is `11.14` at `383/100`. |
| 12 | T-017 `99/25` | grid `4` | 0.040 | Yes. Certificate-seeded `397/100` stopped at `12.016263` unconverged. Session-140 four-grid plus windows 7 at `397/100` converged at `12.133391`. Leftover `3969/1000` four-grid plus windows 7 stopped at `12.091168` unconverged. |
| 17 | T-019 `459/100` | grid `5` (reported packing `4.675…`) | 0.410 | Yes. T-019-seed plus windows 5 at `23/5` stopped at `17.042346`. Session-140 four-grid plus windows 8 stopped at `17.120106`. Leftover `461/100` stopped at `17.195968`. |
| 18 | T-028 `187/40` | `(7/2)+(1/2)sqrt(7)` | 0.148 | Rank 5 retained as T-028. `117/25` still sits on the `18.000000` plateau. |
| 19 | T-020 `24/5` | `4.885618…` | 0.086 | Three probes. T-020-seed windows 6 at `97/20` stopped at `19.808958`. Session-140 same construction at `481/100` stopped at `19.132115`. Leftover `241/50` stopped at `19.247109`. |
| 20 | T-021 `97/20` | grid `5` | 0.150 | Yes. Old cert-seed crossed at `20.000223`. Session-140 four-grid plus windows 7 stopped at `19.939212` unconverged after 2400 s. Leftover `971/200` stopped at `19.910044` unconverged. |
| 21 | T-021 `97/20` | grid `5` | 0.150 | Session-140 auto plus windows 6 stopped at `19.814820` unconverged. Same side as T-021; not a floor raise. |

A restricted optimum above `n` refutes that site set only.
Remaining rows can only raise it.
Adding sites can still lower it.
Session-139’s `397/100`, `23/5`, and `97/20` rows are therefore open rungs, not walls.

H-062 already accepted a wall at `n = 20`, side `973/200`, on the two site sets it named
(auto grid and the 97/20 seed).
That wall does not bind a windows lattice or a four-grid.
Those are new named site sets of the same producer.

## Ranked Queue

Priority is “how close is a stock construction to mass `< n` at a side strictly above
the current floor”, then remaining gap, then whether a seed certificate exists.

| Rank | Bead | n | Next side | Why this first | First named site set |
| ---: | --- | ---: | --- | --- | --- |
| 1 | think-d2ad | 20 | `973/200` | Surplus `0.000223` on the old seed. One extra construction class can finish the rung. | T-021 seed, grids `34,46,56,64`, windows 7 |
| 2 | think-h02v | 12 | `397/100` | Surplus `0.016263` on the old seed. Remaining window to the grid is `0.04`. | T-017 seed, grids `28,38,46,54`, windows 7 |
| 3 | think-5q81 | 17 | `23/5` | Surplus `0.042346` on windows 5. Reported packing sits at `4.675`, so `4.60` is still inside the interesting interval. | T-019 seed, grids `34,45,56,64`, windows 8 |
| 4 | think-zoq4 | 19 | `481/100` then `97/20` | Only one probe, and it is `0.81` above 19. A side just above `24/5` is the cheap test. | T-020 `certificate-24-5.json`, auto plus windows 6 |
| 5 | think-15qo | 18 | `187/40` | Retained as T-028. `4.68` still plateaus at 18. | T-027 seed, auto plus windows 5 |
| 6 | think-b6n9 | 21 | `97/20` | Same certificates as n=20, almost no covering data. Run only if the n=20 lane is idle. | T-021 seed, auto plus windows 6 |
| 7 | — | 11 | none this block | Point covering at sides above T-026 is already `11.14` and rising. Not this campaign’s win condition. | — |

`think-8ujs` is not a probe.
It is the retain step, and it stays idle unless `decide_certificate` prints
`RETAINABLE`.

## Second Wave: Nagamochi-Only Floors

The remaining open sizes have no first-party covering row.
The smallest block is `n = 26..32` (floors `5.12..5.80`, ceilings 6 or a published
packing). After that `n = 37..45`, `50..61`, `65..78`, `82..100`.

Those sizes need a seed.
The stock move is the same producer with `--grid-counts auto` at a side just above the
Nagamochi floor. That is a calibration, not a promised bound, and it is deferred until
ranks 1–5 have either frozen or exhausted their named site sets.
`think-b6n9` owns the triage note, not a T-id.

## What Would Count as Progress

A covering row on a new `(n, side, site_set)` is progress even when it stays above `n`.
A verified floor moves only after a freeze with mass `< n` that both routes of
`decide_certificate` accept.
Session-140 landed T-028 at n=18 (`187/40`). That retain is off the H-218 sweep and does
not confirm H-218. Session-139 left the landing recipe; this session copied it and did
not invent a case class.

n=11 stays T-026. H-216 stays a calibration at n=6. exp-161 stays unresolved with no
`--search`.

## Autonomous Loop

One coordinator owns identifiers, covering-values, T-id landing, ledger render, and the
stacked PR. Each probe bead owns one `(n, side)` family and writes under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-038/`. The
walker is `python -m devtools.run_covering_queue` over `first-wave-queue.yaml`, then
`leftover-queue.yaml`, then `second-wave-queue.yaml`. Ranking for the leftover list is
`leftover-side-ranking.md`: untried sides or site sets only.
Do not replay a set whose restricted optimum is already above `n`. Kill a probe at its
deadline. If the freeze mass is below `n`, stop new probes and run the retain recipe.
If not, record the row and take the next rank.

Session-141 re-ranks from these masses in
[X-039](X-039-n100-re-rank-after-session-140.md). Leftover n=18 `1871/400` and the
Nagamochi second wave did not start here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
