# The annealing benchmark’s runbook

How to run one round of `think-7umw`, and what makes a round valid.
The record it produces is the `.jsonl` files beside this one, the hypotheses under
`../../hypotheses/`, and the experiment artifacts under `../../series/`.

## One round

```bash
# from packing/
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --n 5 10 11 17 26 29 --seeds 2000 --anneal 6
```

A grid, in one invocation and one table:

```bash
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --n 5 11 --seeds 3000 --sweep anneal=0,3,6,10 inflate=1.06,1.12,1.25
```

Re-report an existing file without re-running it:

```bash
uv run --frozen --all-extras --group dev python -m devtools.bench_annealing \
    --replay campaign/results/annealing/<file>.jsonl
```

A trial costs half a millisecond plus the resolver, so a hundred thousand of them is a
couple of minutes. Budget is not the constraint here; asking the right question is.

## What makes a round valid

**Three things, and the first is the one this campaign learnt the hard way.**

1. **The arrangement has to be a packing.** The harness projects every run to one and
   scores the projection; a trial whose resolved arrangement still overlaps by more than
   `VALID_OVERLAP` is *refused*, not recorded as poor.
   Two entire rounds were run before this existed and every number in them was a
   bounding box around overlapping squares.
2. **The tolerance is measured, not chosen.** `VALID_OVERLAP` is 1e-5 because the
   snapped trajectory — which ends on the record’s own poses by construction — scores
   5.5e-7 to 1.0e-6, and the smallest real overlap is two orders above that.
   Re-measure it if the page’s pose precision changes.
3. **The instrument has to prove it was measuring something.** `GUARD_JS` refuses a page
   with no API, no `setSeed` or no pairs before any trial runs.

## The metric

`closed` — the fraction of the record-to-grid gap a **resolved** run closes.
1 is the record, 0 is the trivial grid `ceil(sqrt(n))`, negative is worse than the grid.

It is the only column that compares across n. Raw excess cannot: at `n = 29` the grid is
1.1% above the record and at `n = 5` it is 10.8%, so the same excess means opposite
things.

## The accept rule

A parameter set beats the shipped defaults when its **best-of-k at equal k** is higher
on a set of n it was not tuned on, with the trials valid and the cost reported beside
it. A better median is not a result on its own: the median is below the grid everywhere,
so a method is only worth running as restarts.

## Resuming

Everything needed to pick this up mid-stream is in three places, and nothing is only in
someone’s head:

- **What to try next and why** — the hypotheses `H-206` … `H-210` under
  `../../hypotheses/`.
- **What has been tried** — `exp-206` and `exp-207` under
  `../../series/series-000-smoke-and-calibration/experiments/`, and `X-028` under
  `../../explorations/`.
- **How to run one round** — this file.

## What is open

- Whether a resolver that **rotates** scores these same runs higher.
  Every number recorded so far is a lower bound, because the resolver only translates.
- Whether the physics can be given a **resolution phase of its own**, which would make
  the animation honest as well as the search — the blind and free styles currently draw
  arrangements that are not packings.
- `H-208`, whether the drop or the schedule decides, which is now cheap to test and was
  not tested while the numbers were invalid.
