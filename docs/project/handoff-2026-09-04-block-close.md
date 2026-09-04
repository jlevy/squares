# Handoff — 2026-09-04, close of the fractional-certificate block

Everything a session resuming from [PR #78](https://github.com/jlevy/squares/pull/78)
needs. The source block ran on `claude/agenda-017-plan-and-run`; this stacked review
continues it on `codex/pr78-s11-adversarial-review`. The next block is already planned
as
[Agenda 019](../../packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md);
begin there, at its `State at handoff` section, and not here.

## What moved

Seven registered cases, all from one instrument.
All are `V4`; `T-018` is `C5`, and `T-017`, `T-019`, and `T-020` are `C4`.

| Result | Bound | Was | Movement | Score |
| --- | --- | --- | --- | --- |
| `T-018` | `s(11) ≥ 381/100 = 3.81` | `2 + 4/√5 = 3.788854`, Stromquist’s 2003 value verified here by the Exp-017/T-010 repair | `+0.021146` | `S5` |
| `T-017` | `s(12) ≥ 99/25 = 3.96` | `3.788854`, inherited from `n = 11` | `+0.171146` | `S4` |
| `T-019` | `s(17), s(18) ≥ 459/100 = 4.59` | `22529/5000 = 4.5058`, Massaccesi 2026 | `+0.0842` | `S4` |
| `T-020` | `s(19), s(20), s(21) ≥ 24/5 = 4.80` | `4.59`; `1 + √13`; `1 + √14` | `+0.21`, `+0.194449`, `+0.058343` | `S4` |

`T-019` still claims `n = 19` and is superseded there by `T-020`; a superseded result
keeps its claim and gains a note, it is not narrowed.
In the verified register, Nagamochi’s 2005 closed form went from supplying 60 of the 65
open cases at `n ≤ 100` to 58, and every one of the seven exceptions is a certificate
held here. DS7’s reported `n = 21` value was already slightly stronger than Nagamochi’s
there but was not independently replayed.

Two corollaries: **`s(12) > s(11)` strictly**, since `3.96 > 3.877084 ≥ s(11)` by
Trump’s 1979 packing; and the new `n = 20` and `n = 21` verified floors also exceed
Friedman’s older DS7 reports (`6√2 − 4` and about `4.7438`, respectively).

`C4` is earned the same way everywhere: each certificate is decided twice from the same
frozen bytes, by the exact event-cell sweep and by an interval branch and bound with
directed rounding, and the two agree on the exact least covered mass.
`T-018` reaches `C5` through the mapped adversarial review on this stacked branch;
external peer review would strengthen it further but is not what the repository’s `C5`
definition requires.

## Two structural facts, both proved rather than guessed

**The ceiling.** No certificate for `n` exists above `⌈√n⌉ · B`: a wider container holds
`⌈√n⌉²` pairwise disjoint axis-parallel `B`-squares, direction `0` is always in the net,
**Condition 5** gives each mass at least `1`, and **Condition 2** forbids the total.
For a fixed finite net, the ceiling over every permitted shrink is `⌈√n⌉ / (1 + D)`. The
current net cannot reach the conjectured endpoint `4` at `n = 12` or exceed `4.9885` at
`n = 20` and `n = 21`. Those are necessary limits, not evidence that the ceilings are
attainable, and they do not exclude a family on refined nets plus a separate limiting
argument. At `n = 11`, `17`, `18`, and `19`, the best known packings bind before this
fixed-net ceiling does.

**n-independence.** Only **Condition 2** mentions `n`, and the covering program behind
the search does not contain `n` at all.
One atom set certifies its side for every integer above its own mass, so **Condition 2**
becomes strictly weaker as `n` increases; the other feasibility conditions do not
change. `T-020` illustrates this directly: it was generated for `n = 20`, its atoms are
too heavy for `n = 18`, and their mass below 19 certifies `n = 19`, `20`, and `21`
directly.

Together they produce
[`CERTIFICATE-REACH.md`](../../packing/frontier/CERTIFICATE-REACH.md), which ranks all
100 cases by what a certificate could add, and now also by what three certificates
actually attained: every retained certificate whose binding constraint is the best known
packing landed at `0.98171`–`0.98270` of it, mean `0.98229`. That ratio applied across
the register puts about `+0.40` at `n = 51`, `26`, `39`, `38`, and `37`, compared with
the largest prior single-case movement, `T-001` at about `+0.263935`. It is three points
and is labelled an extrapolation;
[`X-013`](../../packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md)
prices it and argues for `n = 26` first — a near-tie on predicted gain at roughly a
quarter of `n = 51`’s estimated cost, and a run that could provide the first retained
raw restricted-program measurement outside the `3.82`–`4.80` band.

## Where the next rungs are, and why not yet

- **The retention gate was rewritten, but its present cost is not yet measured.** Three
  operator-reported Fraction-sweep timings — `1473 s` at 1184 atoms, `4866 s` at 2097,
  and `5378 s` at 2260 — have no retained raw timing transcripts or machine/load
  records. Their least-squares log-log exponent is `2.04`; the 1184-to-2260 endpoint
  slope is `2.00`. The new integer-and-span implementation produced operator-reported
  pre-integration times of `21.8 s` at 1184 atoms and `38.7 s` or `29.4 s` at 2260, but
  those runs predate the integrated worker-memory cap and are not benchmarks for the
  current code. Correctness is guarded separately by the independent legacy cell/Fraction
  reduction, serial/parallel comparisons, and the unchanged interval decision.
  `BC-190` must now measure the integer and interval routes end to end; `BC-191` must
  measure row generation, site density, and rationalisation cost.
  Neither is yet proved to dominate a complete run.
- **`n = 18` at `117/25 = 4.68`** is open.
  An unretained operator report says three site sets returned exactly `18.000000`, the
  third after 157 row-generation rounds and 7056 s; there is no raw log, checkpoint, or
  candidate. The report does not separate a genuinely high unrestricted covering value
  from tested site sets that remain short of it or a restricted optimum on a degenerate
  vertex. `T-019`’s `next_rung`.
- **`n = 11` at `3.82`** has two site-set histories in the result narrative: both
  reached restricted objective 11, one reported convergence and the other stopped with
  violated placements.
  The rejection route is far from closing: exact maximum pointwise depth `1925/1152`,
  capping the feasible total at `1152/175` against the eleven a ceiling needs.
  `T-018`’s `next_rung`.
- **`C4 → C5`** for `T-017`, `T-019`, or `T-020` needs a mapped, non-superseded review
  artifact under the repository’s confirmation rubric.
  An outside mathematical review would strengthen every result.
  The third-party package at `packing/cases/n11_fractional_certificate/thirdparty/` lets
  a reviewer decide the `19/5` rung without trusting this repository.

## The instrument

`packing/src/sqpack/fractional/` — `certificate.py` (five numbered proof conditions, the
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
decides by both routes, and refuses unless they agree on the value and the retained
claim, total mass, and least-cell declaration match it.
`--quick` runs the interval route alone, which can reject and never retain.
Three detectors guard the record against the class of defect this block kept finding:
`check_rung_figures` (quoted figures recomputed from artifacts), `check_case_prose`
(case bodies against their own front matter), `check_nagamochi_bounds` (the closed-form
count).

## What not to repeat

- **`D-439`, `D-475`, `D-481` — the same class three times in one day.** A durable
  record described a rung, the rung moved, the sentence stayed true-when-written and
  became false. It happened in the results register, then in six case bodies six hours
  after the first detector was built, then in a generated document’s own hedge, supplied
  to a sub-agent from memory.
  A record has more than one place to describe a rung, and each needs its own check.
  Every figure in a brief to a sub-agent must be re-derived from the repository before
  use; that requirement is what caught the third.
- **Read the evidence, not a reconstruction of it.** Four solver lanes were reported
  dead on a harness notice while `ps` showed all four processes still live; that process
  listing established liveness, not health, progress, or correctness.
  An exact sweep was first reconstructed at `~13000 s` from contended wall-clock, while
  a later unretained operator report gave `4866 s`. Neither is benchmark-quality
  evidence.
- **A candidate counts only when its row loop stopped for want of a violated
  placement.** Report the loop’s final least covered mass beside the objective.
  An objective below `n` with the loop still finding violations was refused at nine
  directions once.
- **Round numbers are the artefact signature** — `11.000000`, `18.0`, `25.0`, `200/11`
  have all been restricted optima on a site set, never `τ*`.
- **Freeze before deciding.** Write the candidate to its path, reload it, decide the
  reload. `D-454`.
- Run `packing-validate --push` before any push, not `--records`; basedpyright has
  caught `Optional` errors in CI twice that ruff and pytest missed.

## How to run the block

[`three-lane-research-method.md`](three-lane-research-method.md) is the method, written
so it can be followed rather than reconstructed.
Its rule seven now carries four instances.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
