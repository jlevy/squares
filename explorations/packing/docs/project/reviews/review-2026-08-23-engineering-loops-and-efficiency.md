# Review: Loop Speed, Iteration Cost, and What Actually Gates the Research (PR #17)

**Date:** 2026-08-23

**Author:** Claude (agent), for joshuadlevy@gmail.com

**Status:** Complete; fixes landed on `review/pr17-engineering`, stacked on the PR
branch

**Reviewed:** [PR #17](https://github.com/jlevy/thinking-scratchpad/pull/17)
(`codex/packing-unattended-research-readiness`, 34 files, +1,747/−617), from a strict
process, efficiency, and software-correctness standpoint.
Mathematical correctness is another reviewer’s brief and is deliberately out of scope
here, with one exception noted below that engineering surfaced and cannot settle alone.

Every number in this document was measured on the branch, on a 10-core Apple-silicon
machine with warm caches, and each is reproducible from the command given beside it.

## Verdict

**The discipline in this directory is unusually good and the loops it runs in are
unusually slow, and the second thing was quietly eating the first.**

The gate is the most carefully reasoned test harness I have read in a research codebase:
every skip is accounted for, every guard has a negative control, and the comments record
why each check exists and which defect it descends from.
It was also 170 seconds of wall time delivering 133 seconds of CPU on a ten-core
machine, with no way to run any part of it on its own.
That is the number that decides whether an agent’s edit-check cycle is thirty seconds or
ten minutes, and it had drifted well past the point where a careful agent starts
batching changes and guessing instead of checking — which is precisely how the class of
defect this directory’s log is full of gets in.

Nothing needed to be given up to fix it.
The gate now runs in **22 seconds** with the same twenty-five steps and the same
assertions, the handover gate (`--strict`) in **40 seconds** instead of 93, and a single
named check can be run on its own in **0.3 seconds**. No check was weakened, removed, or
made conditional, and one latent race was found and fixed on the way.

The more important finding is that **the gate was never the research bottleneck**, and
neither is the search engine.
The bottleneck is the quench, it is roughly 95% Python and scipy overhead rather than
arithmetic, and it sits directly on the critical path the PR itself names.
That is where the next engineering investment belongs, and there is a correctness
question that has to be settled before it can safely be made.

## 1. The loops, measured

Being strategic about this means knowing which loops are hot.
A thing that happens once per LLM call does not need to be fast — the LLM call is
already slow. A thing that happens 19,466 times inside one gate step does.

| Loop | Frequency | Before | After | Verdict |
| --- | --- | --- | --- | --- |
| Anneal move (`sqsearch`) | ~10⁹ per campaign round | 35 ns | 35 ns | **Already fast.** 28.7M moves/s. Leave it alone. |
| LP solve (`solve_cell`) | ~1,600 per quench | 1456 µs | 1456 µs | **The bottleneck.** ~95% wrapper, not simplex. |
| One quench (`quench_bracket`) | 1 per search endpoint | 2.5 s | 2.5 s | **Gates the planned census.** |
| Targeted check | many per agent edit | *impossible* | 0.3–10 s | **New.** `./test.sh --only` |
| Full gate (`./test.sh`) | 1 per agent edit | 170 s | **22 s** | Fixed. |
| Handover gate (`--strict`) | 1 per unattended launch | 93 s | **40 s** | Fixed. |

Reproduce the top rows:

```
./sqsearch/target/release/sqsearch --n 11 --seed 1 --chains 4 --budget-moves 4000000
```

That is 16M moves in 0.56s. The soundness perimeter’s three engine cells cost about 1.7
seconds of a step that ran for 36. **The engine is three orders of magnitude faster than
the thing standing next to it**, and every instinct to optimise it further should be
spent elsewhere first (`think-r33j` records the real wins that exist there, so nobody
has to re-derive them, and says not to do them yet).

## 2. What the gate was doing with its three minutes

The steps were run one at a time, and the four longest were each internally serial too.
The fixes are all the same fix — the work was already independent, nothing was sharing
state, and the machine had nine idle cores.

| Step | Before | After | What changed |
| --- | --- | --- | --- |
| soundness perimeter | 36 s | 10.4 s | 18 independent quench trials, pooled |
| negative controls | 34 s | 7.0 s | 30 controls, isolated in clones, pooled |
| historical regressions | 23 s | 8.8 s | 5 independent checks, pooled |
| golden basins (`--deep`) | 93 s | 21 s | 7 rungs + 20 census quenches, pooled |

Two of these are worth more than their seconds.

**The negative controls were corrupting the working tree.** `tools/negctl.py` edited
tracked files in place and restored them after.
That is why `.gate-running` existed, why the thirty controls had to run one at a time,
and why *the entire rest of the gate* had to run one at a time around them — any
concurrent step might read a half-corrupted file.
It also meant an agent could not safely run the gate while editing, could not run two
gates, and would leave the tree corrupt if killed between mutate and restore, which
`finally` does not cover.
On APFS a copy-on-write clone of the repository costs ~0.2 s and no disk, so isolation
turned out to be cheaper than the workaround for the lack of it.
The step went from 34 s to 7 s, and the reason the whole gate had to be serial went away
with it.

**Nothing else in the gate writes anything.** Every renderer, the ledger, and the golden
map only write under `--update`. Once the controls were isolated there was no shared
mutable state left anywhere, which is what made the rest of it a scheduling problem
rather than a design problem.

### 2.1 A race, found by making things concurrent

Sweeping the new `--jobs` width turned the negative controls red at `--jobs 10`,
reproducibly, on exactly one control.
The bug was mine: I handed control *i* the clone at index `i % workers`, assuming item
*i* runs on worker `i % workers`. A pool promises no such thing — it promises a free
thread takes the next item, so one slow control puts item *i* and item *i + workers* in
flight together, both claiming one tree, one restoring `defects.yaml` while the other
was still watching for its guard to fire.

The control “passed” because its evidence had been tidied away underneath it.
Trees are now checked out of a queue for the duration of one control; verified at
`-j 1, 2, 3, 5, 10`.

Worth sitting with: **a negative control caught a check that had quietly stopped
checking.** That is exactly what `tools/negctl.py` exists for, and it took making the
gate concurrent to give it something to catch.

## 3. The real bottleneck: the quench is ~95% overhead

This is the finding that matters for the research rather than the ergonomics.

```
n = 11, solve_cell's LP is 99 rows x 23 columns

  scipy.optimize.linprog(method="highs") + required tolerances   1456 µs/solve
  the same model passed straight to HiGHS via highspy             380 µs/solve
  identical objective, to the last digit
```

A 99×23 dense LP is single-digit-microsecond work.
Essentially none of that 1456 µs is simplex; it is scipy’s wrapper — validation,
sparse-matrix construction, option checking — repeated per call.

Per quench: **~1,600 LP solves, ~2.5 seconds**. `tools/perimeter_test.py` alone issued
**19,466 `linprog` calls** in one gate step.

Two other things compound it, both now fixed on the branch:

- `choose_cell` recomputed each square’s `cos`/`sin` for every pair, and computed the
  pair half-extent separately for each of four candidate axes.
  At n=11 that is ~1,100 transcendental calls where 22 suffice.
  The angles are *fixed* for the whole LP — that is the premise the cell rests on — so
  this was pure waste.
  It is ~3× faster now.

- **There is no Python parallelism anywhere in the tree.**
  `grep -rn "multiprocessing\|concurrent.futures\|ProcessPool"` over the branch returned
  nothing. The Rust engine uses rayon; everything downstream of it was single-threaded,
  on a ten-core machine, for work that is embarrassingly parallel by construction.

### Why this is the critical path, not a nice-to-have

The PR names the next critical path as `H-023` (terminal-component identity) and `H-021`
(endpoint identifiability).
Both are basin censuses, and a basin census is a pile of independent quenches.

At 2.5 s per quench, a 10,000-endpoint census is **~7 hours single-threaded**. With a
process pool alone it is under an hour.
With the LP in Rust — where the geometry kernel already lives, and already has the
closed form for the pair half-extent that the Python side was missing — it is
**minutes**.

That ratio decides how many hypotheses can be tested per session.
It is a bigger lever on the research than anything in the annealer.
Filed as `think-y91x`, with the sequencing caveat in the next section.

### The building block that is missing

An agent that wants a 10k-endpoint census today has to write a serial Python loop.
The natural primitive — *“quench these N endpoints and give me their canonical keys, in
parallel, deterministically”* — does not exist as a tool, so every hypothesis that needs
one re-implements it, serially, at 2.5 s a go.
That primitive is the thing to build, and building it in Rust and building it fast are
the same task.

## 4. The correctness finding engineering cannot settle alone

**A change of 2.2 × 10⁻¹⁶ in one constraint coefficient changed a published basin
count.**

The `choose_cell` fix above is an identity — the pair half-extent really is the same on
all four candidate axes, `1/2 + 1/2(|cos D| + |sin D|)`, and `sqsearch::geom` already
relies on it and already tests it against the naive four-axis form.
Verified over 17k rows at n ∈ {5, 10, 11, 17}: identical axis and sign choices, `h`
agreeing to 1 ulp.

It changed `golden/basin-maps.yaml`:

```
  - n: 3
-   converged: 3
-   distinct_basins: 3
+   converged: 4
+   distinct_basins: 2
...
-   - side: 2.0176058468
-     closed_form: null
-     converged_frequency: 0
```

What disappeared was **a quench that ran out of iterations, recorded as a distinct
basin**. The proposal that produced it now converges to the proved optimum 2. Nothing
else in the map moved by a digit.

Two things follow, and they point in opposite directions:

1. **This particular diff is an improvement.** Sampling 20,000 random pairs, the old
   per-axis computation had the four axes disagree on a mathematically identical
   quantity in **9.7% of pairs**, by up to 4.4e-16 — noise that entered the `argmax`
   over `gap = |d| − h` and could pick a different separating axis than the geometry
   does. With one shared `h` the term cancels exactly.

2. **`distinct_basins` is not stable to ulp-scale perturbation, and it counts solver
   stalls as basins.** It is the primary observable of `H-003`, `H-008`, `H-012`,
   `H-021` and `H-023`. If it moves under 2.2e-16 it also moves under a scipy or HiGHS
   version bump, a different CPU, or a different build — silently, in whatever direction
   the numerics went that day.

I read the diff as an improvement and regenerated on that basis, in a single revertible
commit, because otherwise the branch cannot pass its own handover gate.
**It is a claim about the research record and it wants a second pair of eyes**
(`think-sk15`).

### The golden map cannot tell “improved” from “broke”

`tools/golden_basins.py --deep` compares re-quenched output to the committed file with
`GOLDEN.read_text() != rendered` — an exact string comparison over floats.
The file’s own docstring argues the oracles should be *mathematics*, not a captured run
("A golden captured from a previous RUN would only freeze whatever the code did that
morning"). The fast path honours that.
The deep path adds a byte comparison that does not — and `--strict` forces the deep
path, so this is the gate standing between the campaign and an unattended night.

Consequences, all observed here:

- A mathematically identical refactor of the quench fails the handover gate.
- It will fail on a different CPU or a different HiGHS build.
  This is also why `-C target-cpu=native` must stay off, despite being the obvious
  10–30% on this kernel: it licenses FMA contraction, which changes float results and
  breaks both this and the engine’s `(seed, chain)` determinism (`think-uvmb`).
- Because it cannot discriminate, the safe-looking response to a red deep gate is to
  regenerate — which is exactly how a real regression gets accepted.

Suggested split: keep byte-exact comparison for the structural and categorical fields
(n, proved value, closed-form name, validity, converged flag), compare floats at a
declared tolerance, and make a change in the *partition* loud while a change in the
tenth decimal stays quiet (`think-lwao`).

## 5. Smaller findings

**`solve_to_fixed_point` decides convergence by exact float equality of the cell
tuple**, and caps at `max_iters = 12` with no recorded justification.
Hitting the cap and converging are reported the same way (`think-9qz0`).

**`quench_bracket`’s budget is wall-clock.** `time_budget=90.0` means machine load
decides how much work a quench does, and therefore whether it certifies convergence.
D-036 is already the defect where an incomplete sweep returned as if every angle had
been checked; this is the same hazard one level up.
Currently benign — a quench is ~2.5 s against a 90 s budget, and the parallel `--deep`
regeneration still reproduces the map byte-for-byte — but it stops being benign the
moment a census runs many-wide on a shared box, which is what the campaign plans
(`think-u97a`).

**There is no CI.** No `.github/workflows`; `make check` runs `skills-check` alone;
lefthook runs only the Markdown formatter.
`test.sh` is the entire gate and nothing runs it automatically, so every check has only
ever run on one machine.
At 22 seconds this is now cheap to wire up, and a second job on a *different*
architecture is what would surface the golden’s cross-machine fragility before an
unattended cloud run does (`think-lrsk`).

## 6. What changed on the review branch

Six commits, stacked on the PR branch, each independently revertible:

| Commit | Effect |
| --- | --- |
| `quench: one shared half-extent per pair` | ~3× on `choose_cell`; removes ulp noise from the axis choice; regenerates the golden (**read this one**) |
| `gate: run the two slowest check files across cores` | perimeter 36→10.4 s, regressions 23.5→8.8 s |
| `negctl: corrupt a private clone, not the checkout` | 34→7 s; the gate stops writing to the working tree |
| `gate: run the steps concurrently, and let a step be run on its own` | 170→22 s; adds `--jobs`, `--only`, `--list` |
| `golden: regenerate the map across cores` | `--deep` 93→21 s, byte-identical output |
| `gate: one worker budget shared by both layers` | fixes nested-pool oversubscription; fixes the tree-checkout race |

Preserved deliberately: the strict/deep coupling and its exact wording (a negative
control anchors on both), the skip accounting and its summary, the `$PY` runner
detection, and building the engine up front before any step that reads the binary.
`--only` is refused under `--strict` and its summary says “N of 25 … this is not a full
gate” rather than “ALL CHECKS PASSED” — a partial gate printing a pass is the exact
failure the skip accounting exists to stop.

## 7. Recommended order

1. **Settle `think-sk15`** — whether `distinct_basins` counting non-converged endpoints
   is intended, and how stable the census actually is.
   Everything downstream of the quench depends on the answer, and no optimisation is
   safe to accept until the golden can tell improvement from regression (`think-lwao`).
2. **Then move the LP.** `highspy` is ~3.8× for a dependency change; Rust is the real
   answer and is where the census primitive should live (`think-y91x`).
3. **Wire CI**, including one job on a different architecture (`think-lrsk`).
4. **Leave the engine alone** until 1–3 are done (`think-r33j`).

* * *

*Tracked under epic `think-9a7v`.*

## Status Addendum: 2026-08-24

The original **Complete** label was premature.
A delta review against PR #17 head `7d019ab` accepted the central performance diagnosis
and the shared half-extent identity, but found pre-absorption defects in the gate
contract, portable snapshot cost, defect record, and branch stack.
Those findings are addressed as follows.

### Fixed Before Absorption

- The branch was rebased onto PR #17 head `7d019ab`.
- `--only` now builds sqsearch only when a selected step consumes the engine.
  Skip accounting is printed before any partial-run disposition, so an engine check that
  did not run is never called passed (D-122, `think-bdv1`).
- `--jobs`, `GATE_JOBS`, and `GATE_INNER_JOBS` reject noninteger and nonpositive values.
  `--jobs 1` exports one inner worker and is serial at both layers (D-121,
  `think-wo4p`).
- `PACK_JOBS` is now described as the measured per-step cap it implements, not a global
  semaphore (D-123, `think-mmw8`).
- Negative-control snapshots copy a 2.9 MiB source surface and refuse above 32 MiB. Five
  trials measured median materialization at 0.0779 seconds through APFS cloning and
  0.1944 seconds through a forced plain-copy fallback (D-124, `think-lyzi`).
- The first parallel tree-assignment race is recorded as D-125. The explicit checkout
  queue remains the fix (`think-oxwd`).
- The shared half-extent correction is recorded as D-120. The resulting n=3 golden
  change remains evidence of solver-stall and partition sensitivity, not evidence that a
  mathematical basin disappeared.
- The original 170-second serial gate and missing targeted loop are recorded as D-128.
- The first integrated gate caught the defect-link control’s newly nonunique anchor;
  D-130 records the failure and its bead-plus-path replacement.
- The Python lint floor now requires BasedPyright’s exact zero-error, zero-warning
  summary. Intentional private access in the benchmark and same-module field arithmetic
  is suppressed at the individual call sites rather than widening the public API (D-131,
  `think-6cbn`).

Implementation corrections are in `2a2b215` and `a7c4b49`. The branch-level findings are
tracked individually under `think-f7km`; this addendum is D-127.

On the integrated rebased stack, the normal gate passed all 25 steps in 26 wall seconds
and the strict/deep gate passed them in 48 wall seconds.
Both runs exercised all 30 negative controls, reconciled all 131 defect records, and
reported zero Python errors, warnings, or notes.
These are local gate results; PRs #17 and #18 have no configured GitHub checks.

### Retained Open Work

The addendum does not close the mathematical or experimental questions exposed by the
engineering work:

- D-050 / `think-sk15` and `think-31k1`: keep censored or nonconverged observations
  separate from promoted basin or terminal-component representatives.
- D-059 / `think-lwao`: replace byte-frozen stochastic golden semantics with comparisons
  that distinguish structural changes from harmless floating-point drift.
- D-126 / `think-u97a`: budget scientific quench work in solves or iterations and use
  wall time only as a recorded outer safety deadline.
- D-129 / `think-cns0`: bound each negative-control checker and reap its process group;
  snapshots protect source integrity but do not make a stuck child finish.
- `think-y91x`: build the deterministic batch-census primitive after the identity and
  stability contract is settled.
- `think-lrsk`: add cross-host CI after the golden comparison has portable semantics.

These are explicit deferrals, not claims that the stacked branch solved unattended
research readiness.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
