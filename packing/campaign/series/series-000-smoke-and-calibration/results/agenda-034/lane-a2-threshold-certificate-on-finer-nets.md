# Agenda 033, lane A2: the frozen threshold certificate on finer direction nets

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a Fable
sub-agent on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds`. The report is reproduced as delivered, with its
own status labels; only its file references were rewritten to say where each file now
is, and the note on the retained records was extended to record the one edit made to
those bytes before registration.
X-024 carries the coordinator’s reading.

The three certificates measured here were frozen after the run.
The 720-step and 1440-step records are registered as `T-026`, whose proof packet is
[`t-026-dilation-limit-proof.md`](../../../../../cases/n11_threshold_certificate/t-026-dilation-limit-proof.md);
the numbers below are this lane’s measurement, not that packet’s statement.
**The registered bytes carry one added field.** Each of the two registered records
declares `"least_cell_charge": "1"` — the value both routes of the gate already return,
which the recommendation at the end of “The three derived certificates” asked for and
which the limit-record path requires of a threshold source.
Nothing else moved. So the measured records and the registered ones have different
digests, and both are given: the measured bytes are
`ece286d0f0b677a67026bc2a805ce167f1fc4de16b5f0a00f28519d996c81096` (720 steps) and
`5e6038abab81283e3ae5b9564b59d6907c9c703606c5dc35043534489991a7cd` (1440 steps), and the
registered files
[`certificate-191-50-net720.json`](../../../../../cases/n11_threshold_certificate/certificate-191-50-net720.json)
and
[`certificate-191-50-net1440.json`](../../../../../cases/n11_threshold_certificate/certificate-191-50-net1440.json)
are `fff8b2bcab95a0041e69fec30c704dd708908125883b6ed645bc2c653ecbf8cf` and
`dc2da20c75d952690c93d67fb4b3eb8552e879585902fde98eedc9b3179ed3d0`. Both registered
files were put through the same two-route gate again after the edit and returned the
same verdict, `RETAINABLE` with both routes agreeing at charge `1`.

Retained beside this report: the four per-net summaries and the 360-step certificate,
listed under [Files](#files).
The 48 per-direction `dirmin-*.jsonl` sweep logs (9.8 MB), the gate transcripts, the
measurement log and the interrupted first run’s logs are not retained (scratch only).

Labels: **EXACT** = a rational decision by repository primitives; **CHECKED** = a float;
**RECORD** = read from a file in the repository; **OPEN** = not measured.

**Headline.** The frozen atoms do *not* cover at the finer nets at their own shrink, but
they do at a slightly larger one, and the rescaled families are accepted by both routes
of the retention gate.
The strongest consequence is a weak limit bound

```text
s(11) >= 955000*sqrt(518400042893309449)/179696714646249 = 3.82644741057293974417...
```

from the 1440-step record, `0.006447410572939` above T-025’s endpoint `191/50 = 3.82`
and `0.009837907784` above T-024’s `3.816609502788862`. It is a limit, not an endpoint
certificate: it asserts no strict inequality at its own value.

## Findings

| # | Quantity | net 360 | net 720 | net 1440 | Label |
| --- | --- | --- | --- | --- | --- |
| 1 | `D`, largest half-gap tangent | `207107/180000000` | `207107/360000000` | `207107/720000000` | EXACT |
| 2 | `B_sharp`, largest `1e-7`-grid shrink with `B^2(1+D)^2 < 1+D^2` | `9988513/10000000` | `9994251/10000000` | `2499281/2500000` | EXACT |
| 3 | `B_coarse`, largest grid shrink with `B(1+D) < 1` | `9988507/10000000` | `39977/40000` | `2499281/2500000` | EXACT |
| 4 | least charge at the certificate’s own `B = 9977/10000` | `1559777/1600000` = 0.974860625 | `1559777/1600000` = 0.974860625 | `973862153/1000000000` = 0.973862153 | EXACT |
| 5 | does it still cover at its own `B`? (`> M/n = 685457679/687500000`) | **no** | **no** | **no** | EXACT |
| 6 | least charge at `B_sharp` | `100000203/100000000` | `100000203/100000000` | `100000203/100000000` | EXACT |
| 7 | does it cover at `B_sharp`? | yes | yes | yes | EXACT |
| 8 | **crossing shrink** `B*` (least grid `B` covering) | `9978363/10000000` | `249507/250000` | `249507/250000` | EXACT |
| 9 | largest grid shrink shown to fail | `4989181/5000000` = `9978362/1e7` | `9980279/10000000` | `9980279/10000000` (inherited from net 720) | EXACT |
| 10 | least charge `m` at `B*` | `997318663/1000000000` | `498684619/500000000` | `498684619/500000000` | EXACT |
| 11 | binding directions at `B*` (unique in every net) | index 229, `t = 47427503/180000000` | index 457, `t = 94647899/360000000` | index 914, `t = 94647899/360000000` | EXACT |
| 12 | that direction’s angle | 29.522300 deg | 29.460646 deg | 29.460646 deg | CHECKED |
| 13 | rescale factor `1/m` | `1000000000/997318663` | `500000000/498684619` | `500000000/498684619` | EXACT |
| 14 | rescaled total budget (must be `< 11`) | `10967322864/997318663` = 10.996809015 | `5483661432/498684619` = 10.996251384 | `5483661432/498684619` = 10.996251384 | EXACT |
| 15 | Condition 4 at `B*`, coarse `B(1+D) < 1` | holds | holds | holds | EXACT |
| 16 | dilation supremum `L sqrt(1+D^2)/(B*(1+D))`, surd | `38200000*sqrt(32400042893309449)/1798171928825841` | `955000*sqrt(129600042893309449)/89874194646249` | `955000*sqrt(518400042893309449)/179696714646249` | EXACT |
| 17 | the same, truncated to 20 places | `3.82388604850764671009` | `3.82534784591311198085` | `3.82644741057293974417` | EXACT |
| 18 | gate verdict, both routes | **RETAINABLE**, agree at `1` | **RETAINABLE**, agree at `1` | **RETAINABLE**, agree at `1` | EXACT |
| 19 | SHA-256 of the rescaled record as measured | `521ba257ebf216b9e0bfd4be3a0441d0b3455541d43cb1751e19a0d63bc4e43d` | `ece286d0f0b677a67026bc2a805ce167f1fc4de16b5f0a00f28519d996c81096` | `5e6038abab81283e3ae5b9564b59d6907c9c703606c5dc35043534489991a7cd` | EXACT |
| 20 | measurement wall time (2 workers, shared host) | 464.7 s | 969.4 s | 1762.0 s | CHECKED |
| 21 | gate wall time | 530.2 s (1 worker) | 1167.8 s (1 worker) | 1819.1 s (2 workers) | CHECKED |

Control row, the certificate’s own 181-direction net at `B = 9977/10000`: least charge
`100000203/100000000` at direction 69 (`t = 4763461/30000000`, 18.044443 deg), which
reproduces the registered `least_cell_charge` exactly (RECORD, reproduced EXACT). Total
budget `M = 685457679/62500000 = 10.967322864` and the covering threshold
`M/11 = 685457679/687500000 = 0.9970293512727273` (RECORD, recomputed EXACT).

Further findings, not in the table:

- **F-A (EXACT).** The theory lane’s caution (lane T2’s F12) is confirmed in direction
  and quantified as small.
  The frozen threshold atoms lose about 2.5% of the least charge when the net is doubled
  at a fixed shrink — from `1.00000203` to `0.974860625` — and need a larger shrink to
  recover it. Against T-024’s point atoms of the same shrink `9977/10000`, whose
  1440-step crossing is `2494953/2500000 = 0.99798120` (RECORD), the threshold crossing
  is `249507/250000 = 0.99802800`, higher by `4.68e-5`. So two-of-three charges are
  indeed more angle-sensitive than point masses, but by five parts in a hundred thousand
  of the shrink, worth about `0.00018` of the final bound.
- **F-B (EXACT).** The crossing shrink is *equal* at 720 and 1440 steps: `249507/250000`
  in both, with the same binding angle (`t = 94647899/360000000`, index 457 in the 720
  net and 914 in the 1440 net) and the same least charge `498684619/500000000`. The two
  rescaled records differ only in `direction_steps`; they are byte-identical otherwise.
  The 1440 record is therefore the 720 record with a finer net declared, and it is worth
  `0.0011` more in the bound purely because `D` halves.
- **F-C (EXACT).** The sharpened test and the coarse test are nearly the same decision
  on a `1e-7` grid here: they differ by 6 grid units at 360 steps, 1 at 720, and 0 at
  1440, where `B_sharp = B_coarse = 2499281/2500000`. Every crossing shrink found sits
  far below both, so the gate’s Condition 4 (which uses the *coarse* test `B(1+D) < 1`,
  not the sharpened one) never came near refusing these records.
  The sharpened test matters here only as the upper bracket of the bisection and as the
  dilation formula.
- **F-D (EXACT).** The rescaled budgets are tight: `10.9968` and `10.9963` against 11,
  where the frozen certificate sits at `10.9673`. The whole slack the refinement
  consumes is the 0.3% of charge the finer net costs.
  A further doubling would have to be paid for out of `0.0037`, so the atoms as frozen
  are close to the end of what net refinement alone can extract from them.
- **F-E (EXACT).** Each rescaled record is accepted with least cell charge exactly `1`
  by both routes, which agree on the number and not merely the verdict; zero stalled
  boxes, zero budget-exhausted directions, zero dense/slab disagreements at every net.
- **F-F (OPEN).** Whether a 2880-step net gains anything, whether re-running the LP at
  the finer net (rather than reusing frozen atoms) reaches further, and whether the
  `3.8264` limit can be registered as a result — the last needed a limit-record path
  that did not exist when this was measured (see below); it exists now and the result is
  `T-026`.

## The three derived certificates

Each is written in the frozen record’s own layout: identical top-level key order,
identical atom order, identical threshold-atom order and point order.
Only `direction_steps`, `square_side`, every weight, `point_mass`, `threshold_budget`
and `total_budget` move; `id` gains a `-net<N>` suffix (T-024’s own derived records use
the same convention) and `provenance` keeps its entries and gains `derived_from` and
`derivation`. The source declares no `least_cell_charge`, so neither do these, and the
gate says so and compares the two routes to each other instead.
**If any of these were to be registered, adding `"least_cell_charge": "1"` would
strengthen the gate**, since both routes already return exactly that.

| File | `direction_steps` | `square_side` | `total_budget` | SHA-256 as measured |
| --- | --- | --- | --- | --- |
| [`lane-a2-threshold-certificate-191-50-net360.json`](lane-a2-threshold-certificate-191-50-net360.json) | 360 | `9978363/10000000` | `10967322864/997318663` | `521ba257ebf216b9e0bfd4be3a0441d0b3455541d43cb1751e19a0d63bc4e43d` |
| [`certificate-191-50-net720.json`](../../../../../cases/n11_threshold_certificate/certificate-191-50-net720.json) | 720 | `249507/250000` | `5483661432/498684619` | `ece286d0f0b677a67026bc2a805ce167f1fc4de16b5f0a00f28519d996c81096` |
| [`certificate-191-50-net1440.json`](../../../../../cases/n11_threshold_certificate/certificate-191-50-net1440.json) | 1440 | `249507/250000` | `5483661432/498684619` | `5e6038abab81283e3ae5b9564b59d6907c9c703606c5dc35043534489991a7cd` |

The recommendation in bold above was taken for the two registered files, and only for
them: the 360-step record is retained here as measured, with no declaration added and
its measured digest intact.
The registered digests are in the note at the head of this report.

Gate transcripts are not retained.
No refusal and no route disagreement anywhere.
The 1440 run reads, in full:

```text
interval accepted=True enclosure=(Fraction(1, 1), Fraction(1, 1)) directions=2881
  boxes=11892823 stalled=0 budget-exhausted=0 (231.6s)
exact  least cell charge 1 = 1.000000000 at direction 914; charge re-evaluated at the
  witness by membership counting 1 (agrees); dense/slab disagreements 0 (1587.4s)
RETAINABLE: both routes accept and agree at 1;
  sha256 5e6038abab81283e3ae5b9564b59d6907c9c703606c5dc35043534489991a7cd; 1819.1s
```

## Method

[`packing/devtools/measure_threshold_net_refinement.py`](../../../../../devtools/measure_threshold_net_refinement.py)
mirrors `devtools/measure_net_refinement.py` for threshold certificates.
It imports that module’s `half_gap_tangent`, `largest_sharp_side`,
`largest_coarse_side`, `sharp_containment`, `uniform_net` and `DENOM` rather than
retyping them, loads the frozen bytes with `devtools.decide_threshold_certificate.load`
(the gate’s own strict decoder), sweeps with
`sqpack.fractional.threshold.minimum_charge`, and builds the dilation supremum with
`devtools.dilation_corollary.PositiveQuadraticSurd`. Every decision is in `Fraction`s;
floats appear in the logs and the progress lines and decide nothing.

**Threshold, not 1.** A threshold certificate is stated normalised: Condition 5' wants a
least charge of at least 1 and Condition 2' a budget below `n`. Both are homogeneous in
the weights, so the *unscaled* atoms with least charge `m` give a certificate at the
same `(L, B, net)` under `w -> w/m`, with least charge exactly 1 and budget `M/m`,
admissible exactly when `m > M/n`. The sweeps therefore run unscaled and are read
against `M/11 = 685457679/687500000`, and the rescaling by the rational `1/m` is applied
only when a record is written out.

**Monotonicity, stated in the script’s docstring.** At a fixed side and net the least
charge is nondecreasing in `B`: a larger concentric closed core contains a superset of
the points of every atom at every centre; each threshold atom’s charge `w[|trace| >= k]`
is monotone in the trace; the point weights are nonnegative; and the admissible-centre
square shrinks. So a direction that clears the threshold at some `B` clears it at every
larger `B`, a bisection test sweeps only the directions not yet known to pass at its
`B`, and a failing test stops at its first failing direction.

**Nesting, used twice.** With `t_k = T k / N` and `N` doubling, the coarser net’s
directions are directions of the finer one.
A least charge decided at `(t, B)` is reused verbatim at every net containing `t` —
which is why the 1440 sweep at the certificate’s own shrink cost only its 720 new
directions. And a `B` at which the coarser net already fails is a failure for the finer
net, so the coarser net’s largest known failing shrink is a sound lower bracket for the
finer bisection. That is exactly what happened at 1440: its bracket opened at the 720
net’s failure `9980279/10000000`, all 14 bisection tests passed, and the crossing landed
one grid unit up at `249507/250000`.

**Resolution.** The bisection ran to a bracket of one `1e-7` grid unit, so each crossing
shrink in row 8 is the exact least grid value that covers, not an interval.

**Cost.** 48 per-`(net, shrink)` direction logs, `dirmin-N<N>-B<b>.jsonl` with `b` the
shrink’s numerator on the `1e-7` grid, 8,079 rows, 9.8 MB, not retained.
Per-net summaries land as `summary-N<N>.json` the moment a net is decided, and the
derived record is written immediately after, so an interruption loses at most the net in
flight. Measurement wall time was about 55 minutes at `--workers 2`; the host was shared
with two other agents throughout (load average around 10 on 4 cores), so the wall times
in rows 20 and 21 are upper bounds on a quiet machine.

## Tests

[`packing/tests/test_measure_threshold_net_refinement.py`](../../../../../tests/test_measure_threshold_net_refinement.py),
six tests, 0.9 s, run from `packing/` with

```bash
uv run --frozen --all-extras --group dev python -m pytest \
  tests/test_measure_threshold_net_refinement.py
```

- `test_crossing_shrink_is_monotone_in_the_net` — nets 4, 8, 16 on a tiny fixture, with
  the coarse crossing strictly below the fine one.
- `test_the_brackets_really_bracket` — the fixture’s bisection bracket really is a
  failure below and a pass above, so the monotonicity test is not vacuous.
- `test_rescaled_record_has_least_cell_charge_exactly_one` — writes a fixture record
  through `rescaled_record`, reads it back with the gate’s `load`, checks every
  declaration with the gate’s `_declarations`, and runs the gate’s `_exact_route`, which
  returns least cell charge exactly `1` with no objections.
- `test_largest_sharp_side_is_exact` — at `D = 1/2` the grid value is `7453559/10^7`,
  pinned by the exact integer inequalities `9 * 7453559^2 < 5 * 10^14` and
  `9 * 7453560^2 > 5 * 10^14`.
- `test_dilation_supremum_agrees_with_the_repository_form` — the script’s surd is
  `devtools.dilation_corollary.sharp_dilation_ceiling` scaled by `L`, coefficient and
  radicand both.
- `test_decimal_places_truncates_a_known_root` — `sqrt(2)` to 20 places.

Ruff (`check` and `format --check`) and basedpyright are clean at zero findings on both
files, run with the repository’s own `pyproject.toml`. The script carries a file-level
`# ruff: noqa: T201` because printing is a measurement tool’s interface, which is the
reason the repository waives T201 for `devtools/*`; the test file carries
`# pyright: reportPrivateUsage=false` because it calls the decide tool’s own
`_declarations` and `_exact_route` rather than reimplementing them, the same suppression
`sqpack/fractional/threshold.py` uses for the same reason.

## What failed

1. **The first measurement run crashed after deciding net 360**, with
   `KeyError: (Fraction(0, 1), Fraction(1995673, 2000000))`. The bisection’s passing
   test deliberately skips directions that monotonicity has already settled, so it knows
   the crossing shrink passes and not by how much; the cache then had no charge at that
   shrink for most directions, and the least charge could not be read back from it.
   Fixed by sweeping the crossing shrink in full before rescaling — which the rescaling
   needs anyway, since `1/m` has to be the true minimum over the whole net or the
   rescaled least charge is not exactly 1. The first run’s logs are not retained; its
   net-360 crossing bracket `(9978360, 9978365]` contains the final exact answer
   `9978363`.

2. **Three candidate test fixtures had no net dependence at all.** A square lattice, a
   lattice plus cell centres, and a lattice plus its image under the rotation by the
   arc’s *end* angle all put the binding direction either at the arc’s endpoint or at
   its exact midpoint, both of which belong to every net in a nested family, so every
   net crossed at the same shrink and the monotonicity test was vacuous.
   The fixture that works rotates the second lattice by eleven sixteenths of the arc —
   an angle no net in the test contains — which moves the worst direction to an
   interior, off-centre place.

3. **`devtools.dilation_corollary --update-limit-record` refused the threshold record**,
   as expected at the time.
   Measured, writing outside the repository:

   ```text
   $ uv run --frozen --all-extras --group dev python -m devtools.dilation_corollary \
       cases/n11_threshold_certificate/certificate.json --update-limit-record $W/probe.json
   REFUSED: missing required field 'total_mass'
   ```

   No file was written.
   What a change would have to cover was enumerated in six points below; all six were
   implemented when `T-026` was registered, and the tool now reads a threshold source
   through the gate’s own decoder and emits a `v3` limit record.

## What it would take for `--update-limit-record` to accept a threshold record

Nothing was changed in `devtools/dilation_corollary.py` by this lane.
What follows is what a change would have to cover, as written at the time; it is the
specification the registration then implemented.
The mathematics is already there; the obstruction is entirely that the tool is wired to
the *point* certificate’s loader, verifier, field names and record schema.

1. **The loader.** `build_limit_record` calls `devtools.decide_certificate.read_bounded`
   and `load_frozen_bytes`. That decoder refuses the threshold record twice over: first
   on `missing required field 'total_mass'` (the threshold schema calls the same
   quantity `total_budget`), and then, if that were supplied, on
   `field 'variant' must be one of ('unconditional', 'class', 'conditional'), got
   'threshold'` from `_require_unconditional`. **The dangerous part is what it does not
   refuse**: the decoder simply ignores an unknown `threshold_atoms` key, so a record
   patched past those two checks would build a `Certificate` from the 584 point atoms
   alone and decide a strictly weaker object that is not the certificate on disk.
   So the fix cannot be “add the missing fields to the record”; it has to be a
   variant-aware load path that uses `devtools.decide_threshold_certificate.load` when
   `variant == "threshold"`.
2. **The decision.** `_decide_limit` calls `sqpack.fractional.certificate.verify`, the
   point route. It would need `sqpack.fractional.threshold.verify_threshold`. Then
   `_accepted_source` needs generalising: its `has_condition_five` test matches
   `name.startswith("Condition 5 ")`, with a trailing space, and a threshold verdict
   names the condition `Condition 5' every reachable cell is charged at least 1`; its
   `verdict.total_mass != certificate.total_mass` comparison has to become the budget
   comparison; and `verdict.minimum_cell_mass` is the least *charge* here.
3. **The declaration check.** `build_limit_record` requires `declared["total_mass"]` and
   `declared["least_cell_mass"]` to match the decision.
   A threshold record declares `total_budget` and `least_cell_charge` — and, as noted
   above, the three records produced here declare no least charge at all, because the
   frozen source does not.
   A threshold limit-record path should require `least_cell_charge` and refuse a source
   without it, which is a second reason to add `"least_cell_charge": "1"` before
   registering any of these.
4. **`dilate`, for the explicit-`--factor` mode.** It scales `outer_side`, `square_side`
   and each `Atom`’s coordinates.
   For a threshold certificate it must also scale every point of every `ThresholdAtom`:
   those points are container coordinates, and `rectangle_terms` refuses a threshold
   point outside `[0, L]^2`. Weights and thresholds `k` are untouched.
5. **The record schema.** `LIMIT_RECORD_SCHEMA` is
   `packing.squares:FractionalDilationLimitCorollary/v2`, and its `source` block is
   written in point-atom vocabulary (`total_mass`, `minimum_cell_mass`,
   `accepted_conditions`). A threshold limit record wants either a `v3` schema or a
   `variant` discriminator carrying the budget and charge names, and
   `--check-limit-record` — which is a byte comparison against `_record_text` — then has
   to know which shape belongs to which source.
6. **The proof text, and only the proof text, on the mathematics.** No new theorem is
   needed. `sharp_dilation_ceiling` reads only `square_side` and
   `largest_half_gap_tangent`, both of which a `ThresholdCertificate` exposes through
   its `point_certificate`. Conditions 1 and 1' are equivariant under common scaling,
   Conditions 2' and 3 are unchanged, and Condition 5' is preserved by inverse dilation
   of placements for exactly the reason Condition 5 is: the charge of a core is a
   function of which atom points it contains, dilation is a bijection on placements, and
   it preserves containment.
   The `invariants` list in the emitted record needs one more line saying so for the
   threshold atoms; the argument itself carries over verbatim.

A smaller alternative, if only the number is wanted and not the record: the surd is
already computed exactly here, and `dilation_corollary`’s no-argument mode prints the
ceiling from a point certificate’s `B` and `D` alone.
Since the derived records above are accepted at `least cell charge 1` by both routes,
the limit follows from `sharp_dilation_ceiling` applied to their `(B, D)` scaled by `L`,
which is precisely `955000*sqrt(518400042893309449)/179696714646249` for the 1440 record
— the value in row 17.

## Files

Retained beside this report:

- [`lane-a2-summary-N180.json`](lane-a2-summary-N180.json),
  [`lane-a2-summary-N360.json`](lane-a2-summary-N360.json),
  [`lane-a2-summary-N720.json`](lane-a2-summary-N720.json) and
  [`lane-a2-summary-N1440.json`](lane-a2-summary-N1440.json): the per-net summaries,
  each written the moment its net was decided, carrying that net’s `D`, the two largest
  admissible shrinks, the crossing bracket, the binding direction and the surd.
- [`lane-a2-threshold-certificate-191-50-net360.json`](lane-a2-threshold-certificate-191-50-net360.json):
  the 360-step rescaled record, retainable but not registered, as measured.

Promoted into the repository by the registration: the measurement
`packing/devtools/measure_threshold_net_refinement.py` with its tests
`packing/tests/test_measure_threshold_net_refinement.py`, and the two registered
certificates with their limit records under `packing/cases/n11_threshold_certificate/`.

Not retained (scratch only): the 48 `dirmin-N<N>-B<b>.jsonl` direction logs (9.8 MB),
the three gate transcripts and the frozen baseline transcript, the measurement’s own
progress log, and the interrupted first run’s logs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
