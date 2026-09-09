# Agenda 033, lane E: fixed-site row completion at 61/16 and the 3.82 cutting loop

Retained measurement-lane report for
[X-023](../../../../explorations/X-023-three-losses-and-a-new-atom.md), written by an
Opus sub-agent on 2026-09-09 under the breadth survey.
The report is reproduced as delivered, with its own status labels; X-023 carries the
coordinator’s reading.
Retained beside it: the frozen depth-one family at `191/50`
([`lane-e-cutting-191-50-family.json`](lane-e-cutting-191-50-family.json)), the loop’s
summary ([`lane-e-cutting-191-50-summary.json`](lane-e-cutting-191-50-summary.json)),
and the row-completion receipt at `61/16`
([`lane-e-completion-61-16-receipt.json`](lane-e-completion-61-16-receipt.json)); the 3
MB loop state and the 4.5 MB completion input are not retained.
Nothing here is a registered round or a new bound.
The ceiling family it cites lives at `ceiling-family-191-50.json` in this directory (the
lane wrote `agenda-031`, the directory’s name before the reconciliation renumbering).

Run 2026-09-09, 00:02–01:57 UTC, from `/home/user/squares/packing`, `PACK_JOBS=1` on
each process, both jobs concurrent at one core each (2 cores total, the budget).
Nothing was committed.
Every number below comes from a file the tools published; paths are listed under
[Receipts](#receipts).

## Findings

| # | Finding | Status |
| --- | --- | --- |
| 1 | **Job 1 is outcome (c): the row loop did not converge.** 16 rounds, then `deadline reached after 16 rounds`; `status: unresolved`, exit 1, no candidate. Final LP objective **10.717926569845675**, least covered mass **0.9840911650687152**, 96 placements still violated in the last round. **This is not a bound on anything.** | CHECKED (receipt) |
| 2 | Completion is not close. The 16 rounds bought +3.64e-4 of objective (10.717562 → 10.717927) for 5,696 s and 1,508 new rows. The last four rounds moved the objective by < 2.4e-11 while still adding 9–47 rows and finding 21–96 violated placements each: a flat objective over an incomplete row set, the degenerate pattern Lane F named at 3.82. | CHECKED |
| 3 | The two-round limit was not what pinned exp-116’s number. The limit was raised 2 → 40 and 16 rounds ran before the clock; exp-116’s 10.7176 at 11,885 rows and this run’s 10.7179 at 13,393 rows differ by 3.6e-4. Lifting the limit changed the objective in the fourth decimal, not the first. | RECORD + CHECKED |
| 4 | **Job 2 raised the depth-one floor at 3.82** from BC-200’s 9.9079 to **29359986576/2903321381 = 10.112551358639962**, at exact maximum depth **1** over 4,234,712 arrangement vertices, 952 placements. Independently replayed from the frozen bytes: `check: reproduced`. | EXACT (replay) |
| 5 | The 96-row support cap **was** truncating the pricing, as Lane F suspected. Dual support per iteration: 117, 94, 107, 88, 119 — iterations 0 and 4 exceed 96. At `--support-cap 200` nothing was truncated. | RECORD |
| 6 | The restricted covering objective at 3.82 fell monotonically 11.055617 → 11.038636 → 11.024472 → 11.009981 → 11.009995 as the site set grew 12,761 → 17,449, and **never passed below 11**. Only iteration 0 was row-converged; 1–4 stopped at `round limit 8 reached`, so those four values are under-estimates of their own site sets’ restricted optima and bound nothing. | CHECKED |
| 7 | **Spike B’s ceiling closes the 3.82 line and explains finding 6.** `agenda-031/ceiling-family-191-50.json` is a D4-symmetric depth-one family of 88 placements, total weight exactly **11**, exact maximum depth exactly **1** over 20,376 vertices, `proved: true`. By weak duality no covering measure of mass below 11 exists at L = 191/50 for this B and net, **on any site set**. Job 2’s loop could not have gone below 11 and no further site refinement at 3.82 will. | RECORD (retained file, verifier’s own verdict) |
| 8 | **That ceiling does not reach 61/16.** Its statement covers “this side or any larger side”, and 61/16 = 3.8125 < 191/50 = 3.82. The 61/16 objective sits at 10.7179, 0.28 below 11. The 61/16 site set is still the live question; it was not answered here. | RECORD + CHECKED |
| 9 | Tool gap, no candidate reached it: `run_fixed_site_completion` writes `"least_cell_mass": null`, and `decide_certificate` refuses a null declaration at parse, `--quick` included. `devtools/declare_least_cell_mass.py` is the documented step between them. Reproduced against a retained candidate. | CHECKED |
| 10 | Tool gap: `RoundTiming` publishes no per-round least-covered mass, so a per-round least-covered *trajectory* cannot be recovered from a receipt — only the single final `least_covered` on the solution. | CHECKED (dataclass fields) |

## Job 1 — fixed-site row completion at L = 61/16

Command as briefed, flags checked against the tool first (`--state --output --n --side
--core --angle-limit --steps --rows-rounds --rows-per-direction --deadline-seconds`,
plus optional `--scale`; `--output` uses `mkdir()` with no `exist_ok`, so it must not
exist). Instance parameters agree with `bc-234-scalar-61-16-leg-01-summary.json`: side
61/16, square_side 9977/10000, angle_limit 207107/500000, direction_steps 180, n 11. The
state carries no `half_tangents`, so the receipt records
`net_binding: caller-declared; source state does not contain its net`; the declared net
is the one the state’s own `best_family` uses (first nonzero half-tangent
207107/90000000).

Result: `status: unresolved`, `stop_reason: deadline reached after 16 rounds`,
`exit_code: 1`, `candidate: null`, `rational_mass: null`, `exact_verification: not-run`,
`finite_site_dual_verification: not-implemented`. Rows 11,885 → 13,393 (+1,508). Wall
5,701.6 s, CPU 4,967.4 s (tool’s scope: run entry to terminal publication).
Rounds cost 5,696 s of that — 1,563 s separation, 4,133 s LP — i.e. 345 s per round
after a 172 s warm solve, against the 214–454 s per *two-round* phase the earlier legs
cost.

Round −1 is the warm solve on the 11,885 rows carried in.

| round | objective | rows held | added | violated | s sep | s lp |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| −1 | 10.717562359067584 | 11885 | 0 | 0 | 0.0 | 172.2 |
| 0 | 10.717652120792668 | 12116 | 231 | 402 | 68.8 | 214.4 |
| 1 | 10.717732740231050 | 12385 | 269 | 426 | 67.3 | 211.0 |
| 2 | 10.717860106418783 | 12575 | 190 | 360 | 84.3 | 184.1 |
| 3 | 10.717898685157094 | 12725 | 150 | 294 | 78.1 | 161.4 |
| 4 | 10.717909333024949 | 12846 | 121 | 231 | 76.9 | 333.2 |
| 5 | 10.717922299531446 | 12969 | 123 | 228 | 86.7 | 234.1 |
| 6 | 10.717923640631666 | 13024 | 55 | 120 | 81.1 | 146.9 |
| 7 | 10.717925457501174 | 13050 | 26 | 54 | 79.1 | 195.2 |
| 8 | 10.717926154859862 | 13106 | 56 | 105 | 114.5 | 322.7 |
| 9 | 10.717926173752710 | 13142 | 36 | 84 | 129.9 | 227.8 |
| 10 | 10.717926299322706 | 13163 | 21 | 39 | 110.9 | 199.8 |
| 11 | 10.717926548659320 | 13270 | 107 | 159 | 149.6 | 169.8 |
| 12 | 10.717926569869126 | 13314 | 44 | 81 | 121.9 | 424.6 |
| 13 | 10.717926569869240 | 13337 | 23 | 51 | 103.3 | 508.3 |
| 14 | 10.717926569869249 | 13346 | 9 | 21 | 92.4 | 229.1 |
| 15 | 10.717926569845675 | 13393 | 47 | 96 | 117.8 | 198.8 |

Read it plainly:

- The row loop **stopped on the clock, not for want of a violated placement**. The
  solution’s own `converged` is `false` and its `stopped` string says so.
  The objective is the value of a relaxation over 13,393 of the site set’s rows; adding
  the rest can only raise it.
  It is therefore **not** an upper bound on the restricted covering optimum of this site
  set, and the restricted optimum is in turn not a bound on the unrestricted covering
  value except from above.
  Nothing here certifies s(11) ≥ 61/16.
- The **least covered mass** trajectory the brief asked for does not exist in the
  receipt: `RoundTiming` carries `index, separation_seconds, lp_seconds, rows_held,
  rows_added, violated, objective, support` and no least-covered field.
  The one published value is the solution’s final `least_covered = 0.9840911650687152` —
  a placement short of mass 1 by 1.6e-2, which is four orders of magnitude above the
  solver’s feasibility tolerance.
  So the row set is genuinely incomplete, not incomplete-within-noise.
- Rounds 12–14 agree to 1e-13 and round 15 is 2.4e-11 *lower*. Adding rows cannot lower
  an LP optimum; that step is solver noise, and it is the size of the signal now.

## Job 2 — cutting-plane loop at L = 191/50, warm-started from BC-200

`--warm` took the BC-200 state at the same side (`warm_start` refuses only a *smaller*
new side; equal sides shift by zero).
The driver echoed
`warm from …bc-200-state-191-50.json at side 191/50: 12761 sites, 9868 rows`. Stopped
`deadline reached before iteration 5` after 5 iterations; loop 5,014 s wall, 4,564 s
CPU. Iteration 0 cost 169 s, so the 20-minute restart rule never triggered; iteration 4
cost 2,067 s, all of it after the deadline had already been crossed inside the row
solve.

| it | sites | support | rows_objective | rows stopped | raw total | exact max depth | depth-scaled total |
| ---: | ---: | ---: | ---: | :--- | :--- | :--- | :--- |
| 0 | 12761 | 117 | 11.055616942909715 | converged | 2763904237/250000000 | 8930931557/8000000000 | 88444935584/8930931557 = 9.903215 |
| 1 | 13929 | 94 | 11.038635981857930 | round limit 8 | 2207727197/200000000 | 9673106001/8000000000 | 6793006760/744085077 = 9.129341 |
| 2 | 15097 | 107 | 11.024471680442990 | round limit 8 | 2756117919/250000000 | 8782442273/8000000000 | 88195773408/8782442273 = 10.042283 |
| 3 | 16289 | 88 | 11.009981285090472 | round limit 8 | 11009981287/1000000000 | 2376302601/2000000000 | 22019962574/2376302601 = 9.266481 |
| 4 | 17449 | 119 | 11.009994970063806 | round limit 8 | 5504997483/500000000 | 8709964143/8000000000 | 29359986576/2903321381 = 10.112551 |

Per-iteration cost (s rows / s lp / s separation): 36/31/101, 488/28/33, 728/88/111,
985/197/118, 1410/114/543. Every iteration added its full 150 orbits.

Iteration 0 reproduces BC-200’s row-converged restricted optimum exactly (11.055617,
`converged: every placement covers mass 1`), which is the evidence that the warm start
restored the retained state rather than a neighbour of it.

**Independent replay of the frozen family** (`replay_ceiling_family --check`, its own
vertex enumeration, 520.8 s):

```
placements 952
total_weight    29359986576/2903321381 = 10.112551358639962
max_depth       1                       (exact)
vertices        4234712    decided_exactly 4703
proved false    failures ["K3 total weight at least n"]
check "reproduced"
```

The same command also replayed the state file’s `best_family` — the same iteration-4
family, enumerated again from different bytes, 718.0 s — and reproduced every number:
952 placements, weight `29359986576/2903321381`, exact max depth `1`, 4,234,712
vertices, `recorded.scaled_total 29359986576/2903321381`, `check: reproduced`. `--check`
passed on both paths.

`proved: false` is the expected and correct verdict: a depth-one family certifies
nothing unless its weight reaches n, and 10.1126 < 11. What the family *is* is a **lower
bound on the fractional packing value** ν*(191/50) at this B and net, and it raises that
floor from BC-200’s 9.9079 to 10.1126. It remains below the 10.3842 of the transported
unit family in `agenda-030/pr127-unit-control.json`.

### Why the restricted objective stalled just above 11

Spike B settled this while these jobs ran.
`agenda-031/ceiling-family-191-50.json` is a D4-symmetric depth-one family of 88
placements with total weight exactly **11** and exact maximum depth exactly **1** over
20,376 vertices, `proved: true`, whose retained statement reads: *no D4-symmetric
measure of mass below 11 captures mass 1 in every closed B-square at a net angle in the
container.* That is a statement about the side, the shrink and the net — not about a
site set. So the covering optimum at 191/50 is at least 11 no matter which sites are
used, iterations 1–4’s descent toward 11.0100 was descending to a floor it cannot cross,
and refining sites at 3.82 for this B cannot produce a certificate.
It also means job 2’s depth-one family has 11 as its ceiling: 10.1126 of a maximum 11.

## Timings and core budget

|  | wall | CPU | notes |
| --- | ---: | ---: | --- |
| Job 1 (61/16 completion) | 5,701.6 s | 4,967.4 s | 00:02–01:37; 5,400 s cooperative row deadline plus reconstruction |
| Job 2 (3.82 cutting loop) | 5,014 s (loop) | 4,564 s | 00:03–01:36; 75-minute loop deadline |
| Job 2 replay (frozen family) | 520.8 s | — | one core, after both jobs ended |

Both jobs held ~100 % of one core each throughout (`pcpu` 97–100 for job 1, 109–117 for
job 2 — the excess is BLAS threads inside the LP), peak RSS 3.4 GB and 2.0 GB against 15
GB. Sequential execution would have needed 90 + 75 minutes of solver deadline plus
tails, over the 3-hour wall budget, so they ran concurrently at the 2-core cap.

## Receipts

All under
`/tmp/claude-0/-home-user-squares/cd8c0aac-f931-5096-97c8-3cccdcaa8ba9/scratchpad/spike-e/`:

- `completion-61-16/receipt.json` — job 1, 12.5 MB: parameters, `round_timings`,
  `row_solution`, all 13,393 `exact_rows`, the site orbits.
  `completion-61-16/input.json` is the byte copy of the source state; `stdout.log` holds
  the one-line verdict.
- `cutting-191-50-summary.json`, `-state.json` (5 iterations, 17,449 sites, 11,589
  rows), `-family.json` (952 placements), `cutting-191-50.log`, `job2-driver.log`.
- `replay-191-50.log` — the independent replay above, both paths.
- `trajectories.md` and `summarize.py` — the tables, regenerated from the receipts.
- `job1.sh`, `job2.sh`, `make_leg2_state.py`, `leg2-state-61-16.json`.

`leg2-state-61-16.json` (24,653 sites, 13,393 rows, net bound in) is job 1’s row set
rebuilt into the state shape the tool reads, ready for a continuation leg.
A leg 2 was launched at 01:39 and stopped a minute later on the coordinator’s
instruction; its started receipt remains at `completion-61-16-leg-02/receipt.json` with
`status: started` and no solver result.
Nothing else was run.

## What remains open

- **s(11) ≥ 61/16 is undecided, and this run neither supports nor rejects it.** The site
  set was not rejected: rejection needs a *converged* row solve at or above 11, and this
  one did not converge.
  Outcome (b) was not reached either way.
- **Does the 61/16 row loop converge at all?** The measurement that would settle it is a
  continuation leg from `leg2-state-61-16.json` run to convergence rather than to a
  clock, with the violation count as the stop signal instead of the objective — the
  objective has been flat since round 12 while violations have not gone away.
  At 345 s per round and 96 violations still arriving, a leg long enough to decide it is
  hours, not a 90-minute slice.
- **Is 61/16 under a ceiling too?** The cheapest discriminating measurement left is to
  point spike B’s ceiling search at 61/16 with the same B and net.
  If a depth-one family of weight 11 exists there as it does at 191/50, the whole 61/16
  site set question closes at once and the 5,700 s spent above is answered rather than
  merely unfinished. If it does not, the 0.28 gap between 10.7179 and 11 is the real
  target.
- **Job 2’s line is closed at this shrink.** Raising the depth-one floor further at 3.82
  is bounded by 11, and the certificate route there is refuted by spike B’s family.
  The method’s reach at this B is what has to move.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
