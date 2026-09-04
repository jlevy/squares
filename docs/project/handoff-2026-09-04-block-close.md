# Handoff — 2026-09-04, close of the fractional-certificate block

Everything a session resuming from [PR #78](https://github.com/jlevy/squares/pull/78)
needs. Branch `claude/agenda-017-plan-and-run`. The next block is already planned as
[Agenda 019](../../packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md);
begin there, at its `State at handoff` section, and not here.

## What moved

Seven registered cases, all from one instrument, all `V4/C4`.

| Result | Bound | Was | Movement | Score |
| --- | --- | --- | --- | --- |
| `T-018` | `s(11) ≥ 381/100 = 3.81` | `2 + 4/√5 = 3.788854`, Stromquist 2003 | `+0.021146` | `S5` |
| `T-017` | `s(12) ≥ 99/25 = 3.96` | `3.788854`, inherited from `n = 11` | `+0.171146` | `S4` |
| `T-019` | `s(17), s(18) ≥ 459/100 = 4.59` | `22529/5000 = 4.5058`, Massaccesi 2026 | `+0.0842` | `S4` |
| `T-020` | `s(19), s(20), s(21) ≥ 24/5 = 4.80` | `4.5058` inherited; `1 + √13`; `1 + √14` | `+0.2942`, `+0.194449`, `+0.058343` | `S4` |

`T-019` still claims `n = 19` and is superseded there by `T-020`; a superseded result
keeps its claim and gains a note, it is not narrowed.
Nagamochi’s 2005 closed form went from holding 60 of the 65 open cases at `n ≤ 100` to
58, and every one of the seven exceptions is a certificate held here.

Two corollaries: **`s(12) > s(11)` strictly**, since `3.96 > 3.877084 ≥ s(11)` by
Trump’s 1979 packing; and twenty and twenty-one squares now have a bound of their own
for the first time, having carried a general formula since 2005.

`C4` is earned the same way everywhere: each certificate is decided twice from the same
frozen bytes, by the exact event-cell sweep and by an interval branch and bound with
directed rounding, and the two agree on the least covered mass to the digit.
`C5`, a review by someone outside the project, is what none of them has.

## Two structural facts, both proved rather than guessed

**The ceiling.** No certificate for `n` exists above `⌈√n⌉ · B`: a wider container holds
`⌈√n⌉²` pairwise disjoint axis-parallel `B`-squares, direction `0` is always in the net,
`C4` gives each mass at least `1`, and `C1` forbids the total.
Over every shrink a net admits the ceiling is `⌈√n⌉ / (1 + D)`. `n = 12` is foreclosed
against its conjectured `4`; `n = 20` and `n = 21` can be brought to within `0.0115` of
their upper bound and no nearer; `n = 11`, `17`, `18` and `19` are limited by their best
known packings, which bind before the ceiling does.

**n-independence.** Only `C1` mentions `n`, and the covering program behind the search
does not contain `n` at all.
One atom set certifies its side for every integer above its own mass, so a larger `n` is
strictly easier at the same side.
`T-020` is the first result to spend this deliberately: its atoms are too heavy for
`n = 18` and exactly right for 19, 20 and 21.

Together they produce
[`CERTIFICATE-REACH.md`](../../packing/frontier/CERTIFICATE-REACH.md), which ranks all
100 cases by what a certificate could add, and now also by what three certificates
actually attained: every retained certificate whose binding constraint is the best known
packing landed at `0.98171`–`0.98270` of it, mean `0.98229`. That ratio applied across
the register puts about `+0.40` at `n = 51`, `26`, `39`, `38` and `37`, against the
`+0.21` that is the largest movement on record.
It is three points and is labelled an extrapolation;
[`X-013`](../../packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md)
prices it and argues for `n = 26` first — a near-tie on predicted gain at a quarter of
`n = 51`’s cost, and the first covering-value measurement outside the `3.82`–`4.80` band
every existing point sits in.

## Where the next rungs are, and why not yet

- **The retention gate was the dominant cost, and is not now.** The exact sweep was
  measured at `atoms^2.00` over three paired runs on frozen bytes — `1473 s` at 1184
  atoms, `4866 s` at 2097, `5378 s` at 2260. The same evening it was rewritten to decide
  in `int64` on the weights’ common scale, with spans in place of expanded cells and the
  directions in parallel: `21.8 s` and `38.7 s` on the same box, same verdicts, the
  `Fraction` route kept as the reference and matched cell for cell.
  What still binds is the search itself: row generation is 79–94% of every round, site
  density has never been set as a function of side, and one untuned grid cost `8.8×` at
  `n = 20`’s own side.
  That is `BC-191`, and it comes before any retarget; `BC-190` now starts from the
  integer sweep as its baseline.
- **`n = 18` at `117/25 = 4.68`** is open with the evidence gathered: three site sets
  returned exactly `18.000000`, the third after 157 rounds and 7056 s. Either the
  covering value is at or above eighteen, or the optimum sits on a degenerate vertex;
  the run was stopped on cost and did not separate them.
  `T-019`’s `next_rung`.
- **`n = 11` at `3.82`** stops at exactly eleven on two independent site sets, and the
  rejection route is far from closing: exact maximum pointwise depth `1925/1152`,
  capping the feasible total at `1152/175` against the eleven a ceiling needs.
  `T-018`’s `next_rung`.
- **`C4 → C5`** on any result needs a reviewer outside the project.
  The third-party package at `packing/cases/n11_fractional_certificate/thirdparty/`
  exists so that one can decide the `19/5` rung without trusting this repository.

## The instrument

`packing/src/sqpack/fractional/` — `certificate.py` (five conditions `C0`–`C4`, the
verifier, the ceiling family, `least_size_certified`), `sweep.py` (the exact event-cell
reduction), `interval.py` (the second decision), `generate.py` (covering LP by row
generation), `colgen.py` (dual-driven column generation), `ceiling.py` (the fractional
packing dual).

Certificates live under `packing/cases/n{11,12,17,20}_fractional_certificate/`, each
with a replay gate, e.g.

```shell
cd packing && uv run --frozen --all-extras python -m cases.n20_fractional_certificate
```

The retention gate is `devtools.decide_certificate`: it reads the bytes back from disk,
decides by both routes, and refuses unless they agree on the *value*. `--quick` runs the
interval route alone, which can reject and never retain.
Three detectors guard the record against the class of defect this block kept finding:
`check_rung_figures` (quoted figures recomputed from artifacts), `check_case_prose`
(case bodies against their own front matter), `check_nagamochi_bounds` (the closed-form
count).

## What not to repeat

- **`D-439`, `D-442`, `D-443` — the same class three times in one day.** A durable
  record described a rung, the rung moved, the sentence stayed true-when-written and
  became false. It happened in the results register, then in five case bodies six hours
  after the first detector was built, then in a generated document’s own hedge, supplied
  to a sub-agent from memory.
  A record has more than one place to describe a rung, and each needs its own check.
  Every figure in a brief to a sub-agent must be re-derived from the repository before
  use; that requirement is what caught the third.
- **Read the evidence, not a reconstruction of it.** Four solver lanes were reported
  dead on a harness notice while `ps` showed all four running; an exact sweep was
  reported at `~13000 s` off contended wall-clock where the gate measured `4866 s`. When
  a status message and a `ps` line disagree, the `ps` line wins.
- **A candidate counts only when its row loop stopped for want of a violated
  placement.** Report the loop’s final least covered mass beside the objective.
  An objective below `n` with the loop still finding violations was refused at nine
  directions once.
- **Round numbers are the artefact signature** — `11.000000`, `18.0`, `25.0`, `200/11`
  have all been restricted optima on a site set, never `τ*`.
- **Freeze before deciding.** Write the candidate to its path, reload it, decide the
  reload. `D-441`.
- Run `packing-validate --push` before any push, not `--records`; basedpyright has
  caught `Optional` errors in CI twice that ruff and pytest missed.

## How to run the block

[`three-lane-research-method.md`](three-lane-research-method.md) is the method, written
so it can be followed rather than reconstructed.
Its rule seven now carries four instances.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
