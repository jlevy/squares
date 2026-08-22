# Statistics and Verdicts

Two tests, chosen by evidence tier.
Anyone needing a third test should not be reaching for this method — the discipline
lives in pairing, pre-registration, and honest spreads, not in statistical
sophistication.

## Evidence tiers

Declare the tier per experiment, and let it choose the test:

| Tier | Test | Minimum | May claim |
| --- | --- | --- | --- |
| `exploratory` | median + range overlap | n≥3 per condition | a detected effect worth confirming; screening verdicts |
| `confirmatory` | paired bootstrap interval | n≥12 pairs | an accepted change; a number quoted outside the campaign |

A campaign that never leaves `exploratory` is legitimate — metabrowser’s whole loop
lives there, and it ships real verdicts.
The tier is recorded so a reader knows what kind of evidence they are holding, and a
confirmatory claim made on exploratory evidence is the thing the field exists to
prevent.

## The overlap test (exploratory)

Per condition: report the **median with its min–max range**, at three or more runs.
An effect is detected when the ranges do not overlap and the median moved in the
predicted direction.

Interpretation rules, both learned the expensive way:

- **Overlapping ranges mean “no detectable effect” — never “a small win”.** A cold web
  run’s DCL has spanned 152–1,176 ms with nothing changed; inside that spread, a story
  about a 5% improvement is a story about noise.
- **A median without its range is not a result.** Print them together, always
  (`650 (621–690)`), so a reader cannot be more confident than the data.

## The paired bootstrap (confirmatory)

Pair trials at equal ordinals — trial k of control against trial k of candidate — and
interleave arms so the machine’s drift (thermal state, background load, cache warmth)
hits both. The decision statistic is the **median of paired changes**, with a percentile
bootstrap interval. Deterministic seed, because a result that changes when the report is
re-rendered is not a result.

Copy this; it has no dependencies beyond the standard library (adapted from fdu’s
[measure.py](https://github.com/jlevy/fdu/blob/main/benchmarks/realtree/measure.py)):

```python
import random
import statistics
from typing import Optional, Sequence


def bootstrap_median_interval(
    values: Sequence[float], resamples: int = 2000, seed: int = 0x5EED
) -> tuple[Optional[float], Optional[float]]:
    """Deterministic 95% percentile bootstrap of the median."""
    if not values:
        return None, None
    generator = random.Random(seed)
    count = len(values)
    medians = sorted(
        statistics.median(values[generator.randrange(count)] for _ in range(count))
        for _ in range(resamples)
    )
    return medians[int(0.025 * (resamples - 1))], medians[int(0.975 * (resamples - 1))]


def paired_change(control: Sequence[float], candidate: Sequence[float]) -> dict:
    """Paired percent change at equal ordinals, lower-is-better metrics.

    The paired change is NOT the ratio of the two medians: under host drift the two
    disagree (in fdu's record, by >2 points on 21% of entries, sometimes in sign).
    Verdicts rest on the paired figure only.
    """
    pairs = list(zip(control, candidate))
    if len(pairs) < 3:
        raise ValueError("need at least 3 pairs")
    ratios = [(cand - ctrl) / ctrl for ctrl, cand in pairs if ctrl]
    low, high = bootstrap_median_interval(ratios)
    return {
        "pairs": len(pairs),
        "control_median": statistics.median(control),
        "candidate_median": statistics.median(candidate),
        "change_pct": round(statistics.median(ratios) * 100, 3),
        "ci95_change_pct": [round(low * 100, 3), round(high * 100, 3)],
    }
```

## Scoring a stochastic search (the `record` shape)

A search campaign’s spread is over **seeds and restarts**, not over repeated timings,
and the trap is different: the statistic that matters is not the best score, it is the
*distribution of best scores across independent seeds*.

- **One lucky seed is not a result.** Report the best reached, the median best across
  seeds, and the number of seeds.
  A strategy whose median is far from its best is telling you it needs restarts, not
  that it is good.
- **Report success rate against a declared target**, when the campaign has one —
  “reached within `1e-9` of the standing best on 3 of 40 seeds” says more about a method
  than any single number it produced.
- **Seeds are recorded and reproducible.** A best configuration nobody can regenerate is
  an anecdote. Record the seed alongside the score, and commit the winning configuration
  as data.
- **Budget is the denominator.** A score is meaningless without what it cost; two
  strategies compared at different budgets have not been compared.
  Fix the budget per round in the runbook and hold it across the arms of a comparison.
- **Beating the standing best is a `determination`, and it is confirmatory by
  construction** — the independent checker is the confidence.
  Re-verify a claimed record with the exact oracle, from the committed configuration, in
  a separate run before recording `beat_record: true`.

## Evidence flags are derived, never stored opinions

From the interval `[low, high]` (lower-is-better, negative = improvement):

- `ci_excludes_zero`: `high < 0` or `low > 0` — the measurement says *something*.
- `direction`: `improved` if `high < 0`; `regressed` if `low > 0`; else `unclear`.
- `passes_acceptance`: the whole interval clears the campaign’s threshold on the
  accepting side (e.g. `high < 0` with `change_pct ≤ -3`).

Keep them separate. One collapsed `significant` boolean once made a clear regression
indistinguishable from a null result.
And derive them from the bounds at artifact-writing time, so an artifact can never carry
flags that contradict its own interval.

## Writing the accept rule

Author it at campaign setup, before the first measurement, in the runbook.
Shape:

```
A candidate is accepted when:
  1. <outcome clause>      e.g. paired median change ≤ -3% on wall_ns
  2. <evidence clause>     e.g. the whole 95% interval below zero;
                           or: ranges do not overlap at n≥3
  3. <validity clause>     no sample rejected by the oracle/guards
  4. <guard clauses>       each guard metric within its pre-registered limit
  5. and the complexity is worth it.
```

Clauses 1–4 are arithmetic.
Clause 5 is a judgment and is *written as one* in the verdict’s reason — a 4% win that
adds a lock, a thread pool, and two failure modes is not automatically worth taking, and
declining it is a recorded decision, not a mood.

The threshold in clause 1 is the noise floor of your instrument, not a preference: fdu
uses 3% because a laptop drifts that much in minutes.
Measure your floor (run control against itself) before setting it.

For `record`-shape campaigns the clauses become: the score beats the standing best
(`beat_record`), the solution passes the independent validity checker, and the attempt
is reproducible from the recorded code ref.
For `determination`s: the outcome is what the declared checker says, nothing else.

## Validity guards refuse; they do not annotate

Whatever proves a run was real — output identical to control before timing, an oracle
digest, a viewport above the floor, a solution checker, a kernel check — apply it **at
record time and refuse the run** if it fails.
An invalid run annotated into the record will be averaged into someone’s conclusion
later; one refused with a clear message costs a re-run now.
Verify the guard itself by mutation once: feed it a run that should fail and watch it
refuse — a guard nobody has seen fire is not yet evidence.

## When a result surprises you

- **Run both orderings.** If A-then-B and B-then-A disagree on the sign, you measured
  position, not code.
- **Treat it as noise until it survives.** A plausible 3.4% regression with a clean
  interval once took three independent measurements to kill: more pairs dissolved it,
  reversed ordering flipped it, a second harness read +0.5% spanning zero.
  Mechanically plausible is exactly what a believable wrong number looks like.
- **Check the criterion.** If the moved metric is not the one the hypothesis named, the
  result is a new hypothesis to register, not an accept.
