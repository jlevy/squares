# Plan: Certify the Reported Upper Bounds, One Validation Block at a Time

**Date:** 2026-09-22

**Author:** Joshua Levy, with Claude Opus 5

**Status:** Draft. Epic `think-2716` owns the work, and its first three blocks are child
beads. No block has run.
One owner decision, the first [open question](#open-questions), sets how far the queue
can go.

**Owns:** How a reported upper bound becomes a certified one in this repository.
That means the record of how the 19 existing certificates were made, the queue of the
rest, the definition of one validation block, and the read-only command that prints the
queue.

**Does not own:**

- How the stage draws a reported bound.
  `think-n56i` decided that, and `think-zb78` and `think-ac22` build it.
- The evidence vocabulary, which [`conventions.md`](../../../../conventions.md) and the
  case schema own.
- Any lower-bound work, and any claim about optimality.

## Overview

Every frontier case carries two upper bounds:

- `reported_upper_bound` is the best known side.
  It is transcribed from a source, not endorsed.
- `verified_upper_bound` is the ceiling this repository can certify from its own
  evidence. Where no certificate reaches the reported packing, it falls back to the grid
  ceiling `ceil(sqrt(n))`
  ([`square-packing-case.schema.yaml:123-146`](../../../../packing/frontier/square-packing-case.schema.yaml)).

The two differ in 128 cases, and the stage shows the reported side in all of them.
On 2026-09-22 the owner decided to keep those sides on the stage, marked *reported*
(`think-n56i`). The same decision made turning a reported bound into a verified one
repeatable work: queued, and run later in blocks that can be scheduled on their own.

This plan makes that work runnable one block at a time.
It rests on three measurements, all given below:

1. Existing exact verifiers reach 18 of the 128 cases once new sizes are added to them.
2. A shipped command, rational promotion, already certifies decimal records within about
   `1e-29` of the reported side.
   It has been rehearsed and never run for the record.
3. The record’s current rule for a certified bound refuses such certificates in most
   cases, because the catalogue truncates the decimals it prints.
   So the rule has to be settled before any block but the exact ones can flip the
   stage’s mark.

## Goals

- Record, with commands and files, how each of the 19 certified non-grid upper bounds
  was certified, so a block repeats the method instead of rediscovering it.
- Put all 128 cases in one queue.
  For each: its blocker, the data it needs, whether that data is retained, and the
  instrument that would certify it.
- Define a validation block: its input, steps, stop condition, clock, and what it leaves
  in the record. When a block lands, the stage’s *reported* mark flips from regenerated
  data, with no hand edit to any view.
- Specify a read-only command that prints the queue and the next batch.

## Non-Goals

- Lower bounds, optimality, or any change to `status` beyond what already follows when
  verified bounds match.
- New packings. A block certifies a side a source already reports; a block that finds a
  better packing has left this plan.
- Contacting the UnitSquare Project or any other source.
  Asking a source for its certificate is a message sent on the owner’s behalf, so it is
  the owner’s call.
- Writing the queue command.
  This plan specifies it; its bead builds it.

## Background

### What “certified” means today, and why that rule cannot stay

The record calls a case’s upper bound certified when
`sqpack.assurance.bounds_agree_at_declared_precision(reported_upper_bound,
verified_upper_bound)` holds
([`packing/src/sqpack/assurance.py:171-215`](../../../../packing/src/sqpack/assurance.py)).
The assurance checks and the trailing-ceiling tripwire use the same rule
([`packing/tests/test_verified_upper_bound_contract.py:265-273`](../../../../packing/tests/test_verified_upper_bound_contract.py)).

**Measured on 2026-09-22 over all 324 records: 129 cases fail the rule, not 128.** The
extra case is $n = 29$. Its verified bound is $5.93383346267692918974379895098$, under
`E-n029-interval-certified-upper`: a Krawczyk interval certificate at a relaxation of
`1e-20` (`T-009` in
[`packing/frontier/results.yaml`](../../../../packing/frontier/results.yaml)). That
bound exceeds the reported $5.93383346267692$ by about `9.2e-15`, which is more than
half a unit of the reported value’s last printed place.
The tripwire expects 129 (`TRAILING_BY_CORPUS["n=1..324"]`,
`test_verified_upper_bound_contract.py:38`). The citation survey in `think-zb78` and the
128 in `think-n56i` both count $n = 29$ as certified.

That gap generalizes.
Each queued case’s reported decimal was compared with its retained witness side, which
carries more digits.

**The witness side minus the printed value is never below minus half a unit and never
above one unit, and in 71 of the 129 it is more than half a unit** (up to $0.995$ units
at $n = 239$). So the catalogue truncates rather than rounds.
In the no-closed-form cases, even a perfect certificate at the true side lands more than
half a unit above the printed value, so the rule calls it trailing.
The rule allows a full unit only when both fields carry the same exact form, which is
why the exact certificates pass it and $n = 29$ does not.

This plan counts the queue as 128, following `think-n56i`, and treats $n = 29$ as
certified at its own relaxation.
The stage, the tripwire and this queue must end up on one rule, and choosing it is the
first [open question](#open-questions).

### How the 19 were certified

Every certified non-grid upper bound came from one of three routes.
Each route is a `cases/<package>/` module that builds or lifts a packing, plus a
`verify_exact.py` (or, once, an interval driver) that decides every pair.
The evidence entries are in
[`packing/frontier/evidence.yaml`](../../../../packing/frontier/evidence.yaml).
Every replay runs from `packing/`.

| Route | $n$ | Evidence (evidence.yaml line) | Certificate | Replay |
| --- | --- | --- | --- | --- |
| Exact, derived from a published rule | 5 | `E-n005-gobel-upper` (340) | `cases/gobel5/packing.py` | `uv run --frozen python -m cases.gobel5.verify_exact` |
|  | 10 | `E-n010-gobel-upper` (410) | `cases/gobel10/exact.py` | `… -m cases.gobel10.verify_exact` |
|  | 40 | `E-n040-gobel-upper` (426) | `cases/gobel40/packing.py` | `… -m cases.gobel40.verify_exact` |
|  | 65, 89 | `E-gobel-family-upper` (445) | `cases/gobel_family/packing.py` | `… -m cases.gobel_family.verify_exact` |
|  | 27, 38, 52, 67, 84 | `E-gobel-strip-upper` (466) | `cases/gobel_strip/packing.py` | `… -m cases.gobel_strip.verify_exact` |
|  | 26, 85 | `E-gobel-offcentre-upper` (537) | `cases/gobel_offcentre/packing.py` | `… -m cases.gobel_offcentre.verify_exact` |
|  | 82 | `E-n082-gobel-l-upper` (560) | `cases/gobel82/packing.py` | `… -m cases.gobel82.verify_exact` |
| Exact, witness lifted into the published field | 19, 66 | `E-lifted-q2-upper` (490) | `cases/lifted_q2/packing.py` | `… -m cases.lifted_q2.verify_exact` |
|  | 18, 86 | `E-lifted-q7-upper` (513) | `cases/lifted_q7/packing.py` | `… -m cases.lifted_q7.verify_exact` |
|  | 11 | `E-n011-trump-upper` (674) | `cases/trump11/packing.py` | `… -m cases.trump11.verify_exact` |
| Interval (Krawczyk) at a declared relaxation | 29 | `E-n029-interval-certified-upper` (1046) | `witnesses/kingbird-n029-2026-interval.yaml` | `uv run --frozen packing-witness verify witnesses/kingbird-n029-2026-interval.yaml` |

Read from those entries and their code, the routes share six properties:

- **A certificate carries the construction’s coordinates, never a relabelled witness.**
  Two cases show why. The strip witnesses declare the exact side rounded *down* by about
  `4.85e-30`. The $n = 82$ witness’s layout matches none of the construction’s eight
  dihedral images (`E-gobel-strip-upper`, `E-n082-gobel-l-upper`, `D-398`).
- **The exact routes decide every pair by exact sign.** The fields are `Q(sqrt 2)`,
  `Q(sqrt 7)`, or the degree-8 field at $n = 11$. The arithmetic is
  `sqpack.field.NumberField` with the exact separating-axis test in
  `sqpack.verify.verify_packing`.
- **Each route has a negative control that fires.** The strip refuses one more diamond,
  the off-centre family one more column square, and $n = 82$ one more L square.
- **Each verifier declares `CERTIFIES`**, the sizes it decides.
  [`devtools.check_certificate_citations`](../../../../packing/devtools/check_certificate_citations.py)
  fails any declared size whose frontier record does not cite the package.
- **The lifts are pinned.** `lifted_q2` and `lifted_q7` carry a `SIDES` entry per size
  and lift only the witness’s 0° and 45° poses (or the shared `Q(sqrt 7)` tilt).
  A drifted witness fails; it does not certify something else.
- **The interval route is bespoke.** $n = 29$ needed a hand-written contact system
  (`cases/kingbird29/system.py`), then Newton refinement, a Krawczyk proof of existence
  and uniqueness, a layout map, and a relaxation
  ([`cases/kingbird29/certify_interval.py`](../../../../packing/cases/kingbird29/certify_interval.py),
  on `sqpack.promote.{refine,krawczyk,relax,interval}`). Its limitations put it below
  exact on the assurance ladder, because it rests on mpmath’s directed rounding.

Only two of the 19 carry a registered result: `T-011` ($n = 11$, exact, V4/C3) and
`T-009` ($n = 29$, interval, V4/C3). The Göbel and lifted certificates are evidence
entries only. Their limitations say the novelty is the exact verification of a side
published in 1979–1980.

**The precedent block is commit `65af39faf`** (“BC-089: six grid ceilings become exact
sides, by two published rules”). It changed:

- two new packages, `cases/gobel82` and `cases/gobel_strip`;
- two evidence entries and six case records;
- both verifiers, added to the exact-verification step of `packing-validate`
  ([`packing/src/sqpack/cli/validate.py:2291`](../../../../packing/src/sqpack/cli/validate.py));
- the regenerated `STATUS.md` and `INVENTORY.md`;
- the tripwire count, lowered on purpose.

Its sequencing came from
[X-009](../../../../packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md),
which ranked recognizing published constructions first.

### The instrument that exists and was never run for the record

`packing-witness promote --strategy robust-rational --max-side-increase X
--output-witness P` is shipped
([`packing/src/sqpack/cli/witness.py:733-829`](../../../../packing/src/sqpack/cli/witness.py)).
It works in three steps:

1. It reads a decimal center-angle witness.
2. It rounds the witness to rationals, taking each angle through the tangent of the half
   angle.
3. It climbs a centre-dilation ladder `1 + 10^-k` until every pair and containment
   decides exactly over $Q$.

What it certifies is the side plus a small increase, never the reported value itself.
`devtools.check_rational_witness_independent` is a second checker, pure `Fraction` and
sharing no code with `sqpack`, and it can confirm each output.

Two beads record what the command did in rehearsal.
Both are report evidence; neither has been replayed for this plan:

- `think-3nc4`: 34 of 36 decimal witnesses at `n <= 100` promote in about 33 s. $n = 68$
  and $69$ refuse, because their witnesses are in corners form.
- `think-stb5` (`BC-165` in
  [Agenda 017](../../../../packing/campaign/agendas/agenda-017-six-hour-generator-rigidity-ceilings-and-w9-block.md),
  lines 480–547): ten cases (37, 39, 41, 51, 55, 70, 71, 83, 87, 88) promoted and
  verified in 24 s. The side increases ran from `5.8e-31` to `7.9e-29`, and every
  certified pose touches the container exactly.
  The block was planned with its reviewer `think-vyff` (`BC-166`) and closed
  `never-opened`. Its claim boundary says the reported decimal *stays uncertified*.

That last line is the decision this plan cannot make.
A rational certificate at the reported side plus `7.9e-29` proves a bound that no
display of fifteen digits can tell apart from the reported one.
It does not prove the reported algebraic number.

### What each case retains

- **Kingbird geometry** is retained only as normalized centre-and-angle facts in
  `packing/witnesses/known-best/n-NNN.yaml`. All 122 queued Kingbird witnesses use the
  center-angle form. No raw Kingbird SVG is kept, because no redistribution terms were
  found
  ([`packing/resources/web/known-best-packings/README.md`](../../../../packing/resources/web/known-best-packings/README.md)).
  Each witness carries only a numerical feasibility receipt at tolerance `1e-8`. Its
  side has 16 to 58 significant digits.

- **Kingbird’s closed forms and minimal polynomials** are transcribed into each case’s
  `reported_upper_bound` (`exact_form`, `algebraic_degree`, `minimal_polynomial`). They
  come from the retained catalogue text,
  [`packing/resources/web/kingbird-squares-in-squares.md`](../../../../packing/resources/web/kingbird-squares-in-squares.md).

- **The published construction rules** are in
  [`packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md`](../../../../packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md)
  and the Göbel pages retained under `packing/resources/web/`.

- **UnitSquare** is retained whole, in three places:
  - the release record, `resources/web/unitsquare-release1-2026/` (`results.json`,
    `results.html`);
  - the SVGs for `n068` and `n069`, under
    `resources/web/known-best-packings/unitsquare/`;
  - the SVGs for `n103`, `n105`, `n110` and `n131`, under
    `resources/web/prospective-packings/unitsquare/`.

  The SVGs hold six-decimal polygon coordinates.
  The witnesses recovered from them are in corners form, checked at tolerance `2e-6`,
  and their squares are not exactly unit (one edge measures about $0.99999999977$). The
  release describes outward-rounded interval validation but publishes no boxes, receipt,
  or checker, and that absence is its whole blocker (`E-unitsquare-release1-report`,
  evidence.yaml line 205).

## Design

### The queue

The 128 cases fall into five groups by the route that would certify them.
The groups set the order of work.
Counts come from the records on 2026-09-22, read by a script in `attic/`. Each family
assignment carries one of two labels:

- **measured**: the family module’s own `count` rule was run and matched against the
  record’s `exact_form`;
- **inferred**: arithmetic on the side value, which the block must confirm by building
  the packing.

| Group | Cases | Blocker | What it needs | Rule-independent? |
| --- | ---: | --- | --- | --- |
| A. Existing exact family, new sizes | 18 | mathematics | new sizes in an existing verifier | yes |
| B. Closed form, new rule or lift | 39 | mathematics | a new `cases/` package per family, or a lift into the named field | yes |
| R. Decimal record, no closed form | 65 | mathematics | the shipped rational promotion; or an exact route over the minimal polynomial | no |
| C. UnitSquare release | 6 | source-evidence only | a first-party pose recovery and certificate, or the source’s own | no |

Groups A and B split the 57 cases that carry a catalogue `exact_form`. Exact
certificates at those forms agree with the reported field under any rule.
Group R has 65 cases: 35 with a minimal polynomial and 30 numerical only.
It depends on the open question.

Forty queued Kingbird cases also carry a `source-evidence` blocker.
It names Green’s missing lower-bound proof (MacIver’s at $n = 17$), so it is not about
the upper bound, and no block removes it.

#### Group A: existing instruments reach 18 cases (measured)

Running `count` in each module over its admissible parameters up to 324, and matching
the side against the record’s `exact_form`, gives 18 cases:

| Instrument | New sizes | Side | Via deletion |
| --- | --- | --- | --- |
| `cases/gobel_strip`, `a = 9..16` | 104, 125, 149, 174, 201, 231, 262, 296 | `a + 1 + sqrt(2)/2` | 295 from 296 |
| `cases/gobel_family`, $(a, b)$ = (5,7), (5,8), (6,8), (7,11), (8,11) | 109, 124, 148, 233, 265 | `a + 1 + b/sqrt(2)` | 147, 232, 264 |
| `cases/gobel_offcentre`, $(a, b) = (7, 10)$ | 227 | `a + 3/2 + (b/2) sqrt(2)` | — |

“Via deletion” is monotonicity: remove one square from a certified $n$-packing and you
have certified $n - 1$ at the same side.
The queue holds five pairs with equal reported sides: 147/148, 232/233, 264/265, 290/291
and 295/296. No verifier does deletion yet.
The honest form is for the verifier to build the $n$-packing, drop one named square, and
decide the $n - 1$ pairs itself, declaring both sizes in `CERTIFIES`.

The builders are already general: `gobel_strip.build(a)` accepts any `a >= 2`. Only each
verifier’s `SUBJECTS` tuple limits it (`gobel_strip/verify_exact.py:42`). The strip
stopped at $a = 8$ because $n = 84$ was the last size in the register when it was
written, on 2026-08-31. The atlas grew to 324 on 2026-09-07. The companion pricing tool
still carries `CEILING = 100` (`devtools/price_gobel_family.py:63`).

The pair count at $n = 296$ is 43,660, about eleven times $n = 89$’s. So the first block
measures the replay’s wall before it adds the replay to the fast tier.

#### Group B: new rules or lifts (39 cases, inferred)

Sub-grouped by the field and shape of the closed form:

- **The `k + (5/2) sqrt(2)` row**: 101, 122, 145, 170, 197, 226, 257, 290 and 291.
  Adding an L of `2 floor(s) - 1` squares at each step reproduces the chain 82 → 101 → …
  → 290 exactly (*inferred*). Then 291 fits one more square at 290’s side, so it is a
  composition, not an L. The survey sampled 101, 122, 145 and 290 and found only 0° and
  45° poses. So there are two routes: generalize the one L in `cases/gobel82`, or give
  `lifted_q2` a `SIDES` entry per size.
- **The `k + 4 sqrt(2)` row**: 173, 200, 229 and 260 follow from 148 by the same L count
  (*inferred*). 294 fits one more square than the rule gives.
- **The `k + (11/2) sqrt(2)` sides**: 298 extends 265 by one L (*inferred*). 150, 175
  and 203 are below the family’s admissible range, so they need a different
  construction.
- **`Q(sqrt 7)` sides**, `k + sqrt(7)/2`: 53, 127, 151, 176, 204, 234 and 299.
  `cases/lifted_q7` is the instrument.
  X-009 records that $n = 53$ refused recognition, because two of its four tilt classes
  gave no stable relation at the witness’s digits.
- **The $n = 54$ shape**, `k - sqrt(2)/2 + sqrt(1 + sqrt(2))`: 54, 107, 178 and 267,
  over a degree-4 field.
  `H-055` planned the lift and stopped on source provenance, never on the mathematics.
  `cases/n54_source_contract` holds only synthetic parser primitives.
- **Rational sides**: $k + 4/7$ at 50, 171 and 198; $k + 28/41$ at 230 and 261; and
  $17 + 26/41$ at 293. The $n = 50$ witness has 34 squares at 0° and 16 at `atan(3/4)`,
  so an exact rational lift at $53/7$ looks direct (survey inference).
  `H-054` and its experiments `exp-048` and `exp-050` stopped on source serialization,
  not on feasibility.
- **Singletons**: 202 (`2 + 9 sqrt(2)`), 237, 258 and 263.

These sub-groups sum to 39. With group A, they account for all 57 closed forms.

#### Group R: decimal records without a closed form (65 cases)

**Update, 2026-09-29.** 42 of these 65 were resolved by a route this plan did not
foresee: Francisco Couzo’s smaller packings (T-056, issue #227) became the reported
bound, and rational promotion certifies each of them at centre dilation 1. They are 102,
106, 123, 130, 152, 172, 177, 199, 228, 236, 259, 268, 269, 292 and 302 among the
minimal-polynomial cases, and every numerical-only case except 55, 71 and 179. At 206,
259 and 305 the certified ceiling still trails the printed side by 2 to 3 units of its
fifteenth decimal, so those three stay queued, with a much smaller gap; the other 39
left the queue. The same intake takes 237 and 263 out of group B and five of group C’s
six. The tables below are the queue as it stood on 2026-09-22.

The 35 cases with a minimal polynomial, by degree:

| Degree | Cases |
| ---: | --- |
| 4 | 70, 153, 302 |
| 5 | 39 |
| 6 | 28, 268 |
| 8 | 37, 102, 130, 172, 199, 259, 269, 292 |
| 12 | 51, 123, 228, 236 |
| 16 | 146 |
| 18 | 17 |
| 20 | 88, 129 |
| 24 | 83 |
| 32 | 106, 177, 266 |
| 40 | 128, 205, 300 |
| 42 | 41 |
| 44 | 87 |
| 59 | 126 |
| 83 | 235 |
| 84 | 152 |
| 144 | 108 |

The 30 numerical-only cases are all `simulated-annealing`: 55, 71, 132, 154–156,
179–182, 206–210, 238–241, 270–273, 297, 301 and 303–307.

Two routes certify group R. Which one clears the stage’s mark depends on the rule:

- **Rational promotion**, the `think-stb5` command, across all 65. Rehearsal says it
  runs in seconds per case (report evidence).
  Six witnesses carry only 16 or 17 significant digits (156, 179, 182, 206, 297, 304),
  so their side increase is bounded below by their own rounding.
  The block measures that increase; it does not assume `1e-29`.
- **Exact over the minimal polynomial.** `cases/trump11` is the precedent: a degree-8
  field, 14 exact zero-gap contacts.
  The route is realistic at degrees 4 to 8, which covers 14 cases.
  Above that, only a relaxed certificate is in reach, and it has the same standing as
  rational promotion.

#### Group C: UnitSquare (6 cases)

**Update, 2026-09-29.** At 68, 103, 105, 110 and 131 Francisco Couzo’s smaller packings
superseded the release and certify exactly here (T-056); only $n = 69$ remains in this
group.

68, 69, 103, 105, 110 and 131. These six alone carry no mathematics blocker; the source
reports an interval certificate it has not published.
The survey found that no attempt has ever certified their upper bounds.

`H-053`, `H-058` and experiments `exp-047`, `exp-051`, `exp-054` and `exp-057` under
`cases/unitsquare_precision/` all worked on something else: rebuilding UnitSquare’s
improvements from their Kingbird parents.
Each stopped on an instrument or provenance refusal.
Nothing was tried at 103, 105, 110 or 131. `promote` refuses these witnesses because
they are in corners form (`think-3nc4`).

A block here has to recover exact unit-square poses from six-decimal polygons.
It then runs rational promotion from a center-angle form, or the $n = 29$ interval route
with a hand-built contact system.
Either way the result is a relaxed certificate, so it depends on the rule.

Asking the source for its receipts is a second route, independent of the first.

### The order

1. **Group A**, three instruments’ worth.
   It moves 18 cases, needs no new mathematics, and depends on no decision.
2. **Group R by rational promotion**, if the owner accepts the rule change.
   Start with `think-stb5`’s ten cases and its reviewer `think-vyff`, as planned.
   Then sweep the other 55 in batches of about ten, lowest digit count last.
3. **Group B**, one family per block.
   The `k + (5/2) sqrt(2)` row goes first, because one instrument reaches nine cases.
4. **Group R by exact routes**, degree 4 to 8. This step replaces relaxed certificates
   with exact ones; it is the only route to any group R case if the owner keeps the
   current rule.
5. **Group C**, beginning with the three 47-digit sides (68, 69, 131).

Within a group, a block takes the whole sub-family that one instrument covers.
That way every block ends with one evidence entry per instrument, and no verifier is
left half extended.

### The validation block

A block is a W6 `research-loop` slice with a criterion declared in advance.
Where the block must first build or extend an instrument, that is a W7 phase inside it.
Moving the record is a reviewed change, never a side effect of a run; the docstring of
`cases/kingbird29/certify_interval.py` states the rule.

**Input.** The next batch the queue command prints: one sub-family, and the one
instrument that covers it.

**Criterion, declared before running.** For every $n$ in the batch, a verifier decides
every pair and every containment:

- at the record’s `reported_upper_bound.exact_form`, by exact sign, for groups A and B;
- at the side plus a stated increase, for rational promotion or an interval route.

A negative control fails as it should.
A size that refuses stays in the queue, with its refusal recorded.

**Steps.**

1. *Orient.* Run the queue command.
   In the block’s bead, name the batch, the instrument, the criterion, and the replay’s
   wall ceiling.
2. *Build or extend.* Add the sizes to the verifier’s `SUBJECTS` and `CERTIFIES`, or
   write the new `cases/<package>/{packing,verify_exact}.py` with its negative control.
   For rational promotion, write each output to
   `packing/witnesses/known-best-nNNN-rational.yaml`, beside the $n = 11$ control and
   not under `witnesses/known-best/`, which the atlas builder treats as generated.
   Certify the construction’s coordinates, not the witness.
3. *Replay.* Run the verifier from a clean root, confirm with
   `devtools.check_rational_witness_independent` where it applies, and keep the output.
4. *Record* in the files the precedent commit touched:
   - `packing/frontier/evidence.yaml`: one entry per instrument, shaped like
     `E-gobel-strip-upper`. It carries `claim: upper-bound`, `assurance: verified`, the
     method, the certificate path, the replay command, `replay_status: passed`, and
     limitations stating what is not claimed.
   - each `packing/frontier/n-NNN.md`:
     - set `verified_upper_bound` to the certified value, its `exact_form`, and its
       evidence;
     - append the new id to `reported_upper_bound.evidence` and to the case’s `evidence`
       (see `think-09q8`);
     - remove the one mathematics blocker about the upper bound, and no other blocker;
     - rewrite the body: remove “The verified upper bound is a ceiling” and say in the
       packing paragraph what certified it.
   - `packing/src/sqpack/cli/validate.py`: add the new verifier to
     `_exact_verification`, and re-point `devtools.check_basic_bounds`' grid replay
     wherever a move replaces `E-basic-grid-upper`.
   - `packing/tests/test_verified_upper_bound_contract.py`: lower `TRAILING_BY_CORPUS`
     by the batch’s size, on purpose, and update its comment.
   - `packing/frontier/results.yaml`: add an entry only for a first of its kind (a new
     method, field, or family), following `T-011` and `T-009`.
5. *Regenerate*, never hand-edit:
   - `devtools.render_research_tables` (`STATUS.md`);
   - `devtools.render_evidence_inventory --update` (`INVENTORY.md`);
   - `devtools.render_results --update`, if a result was added;
   - `devtools.build_composite_figure_data --update`;
   - once `think-zb78` has built it, the stage’s citation data.
6. *Check.* Run `packing-validate --records`, then `--push`. `devtools.check_case_prose`
   and `devtools.check_certificate_citations` are in that run, and they fail a body or a
   citation left behind.
7. *Review.* An agent that did not write the diff gives the record changes a W2 factual
   read before commit. For rational promotion that is `think-vyff`’s contract.
8. *Close.* Rerun the queue command.
   The batch is gone from it, or each size still in it is listed as a refusal.

**Stop condition.** The block stops in one of three states:

- The batch is certified and the gate is green.
- A size refuses. The refusal is recorded and the block closes on the rest.
- The instrument cannot be built inside the clock.
  That is recorded as a `checker` blocker on the batch’s cases, and it is not a
  mathematical negative.

**Clock.** One 30-minute slice per instrument for groups A and B, and one slice per
batch of about ten for rational promotion, each with the 20-minute evidence-checkpoint
default inside it
([bounded research cycle](../../../../packing/campaign/README.md#the-bounded-research-cycle)).
A replay whose wall would push the exact-verification step past its ceiling leaves the
fast tier, selected on purpose under `OR-17`.

**What it leaves.** Evidence entries, case records, the verifier or certificate files,
their gate entry, the tripwire count, regenerated views, a closed bead, and one line in
the owning agenda when the block runs inside one.

### How the stage’s mark flips

The stage marks an upper bound *reported* when the record does not count it as
certified.

- That mark must be computed from the two fields by the citation generator.
  It must never be stored in a file a person edits.
- The rule is one function in `sqpack.assurance`, shared by the generator, the tripwire,
  the assurance checks, and the queue command.
  Then the only change a block makes that the stage sees is `verified_upper_bound`.
- Regenerating the citation data and `composite-figure.json` flips the mark.
- The generator’s drift check (`--check`, which `think-zb78` requires) fails any commit
  that moves the record and not the data.

### The queue command

`uv run --frozen --all-extras --group dev python -m devtools.certification_queue` is
read-only and should finish in under a second.

- **Reads** `packing/frontier/n-*.md`, `packing/frontier/evidence.yaml`,
  `packing/witnesses/known-best/n-*.yaml`, and the `count` rules of the `cases/gobel_*`
  modules that group A uses.

- **Computes** the certified set with the shared rule, and derives each case’s group
  from its fields:
  - `source_key` UnitSquare → group C;
  - an `exact_form` matched by a family `count` → group A;
  - any other `exact_form` → group B;
  - everything else → group R.

  No case list is kept by hand, so a block that certifies a case removes it from the
  queue by changing the record alone.

- **Prints** one row per queued $n$, with these fields:
  - group and sub-family;
  - blocker kinds;
  - `exact_form`, or else the degree;
  - witness form and significant digits;
  - the gap between the witness side and the reported value, in units of its last place;
  - the instrument that would certify the case, or `none`;
  - whether its data is retained.

- **Options:**
  - `--next` prints only the next batch, in the order above;
  - `--group A` filters to one group;
  - `--json` emits the same rows for a bead or an agenda.

  No option writes a file.

- **Controls:** a test over the recorded register.
  It checks that group A’s sizes match each module’s `count` and that the queue’s total
  equals the tripwire’s count.

## Implementation Plan

### Phase 1: The rule-independent blocks

Three beads under `think-2716`, each runnable cold:

- [ ] Block 1: extend `cases/gobel_strip` to `a = 9..16`, and certify 295 by deletion
  from 296 (9 cases).
- [ ] Block 2: extend `cases/gobel_family` and `cases/gobel_offcentre` to the six new
  parameters, and certify 147, 232 and 264 by deletion (9 cases).
- [ ] Block 3: build the queue command and its controls.
  It is needed before the blocks that follow read their batch from it.

### Phase 2: After the rule decision

- [ ] If the rule changes: reopen `think-stb5` and `think-vyff` under this epic, then
  sweep the rest of group R in batches.
- [ ] Group B one family per block, starting with the `k + (5/2) sqrt(2)` row.
- [ ] Group R exact routes at degree 4 to 8, then group C.

## Testing Strategy

The controls are the ones the precedent already runs:

- each verifier’s negative control;
- `check_certificate_citations`;
- `check_case_prose`;
- the assurance checks in `--records`;
- the tripwire count, moved on purpose.

A rational-promotion block adds the refusal control `think-stb5` specified: mutate one
coordinate of one certificate, and `verify` refuses it.
The queue command’s own test pins group A to the modules’ `count` rules.

## Rollout Plan

Each block lands as one commit, or one per instrument, through the ordinary pull-request
gate. Blocks within a group are independent and can run as parallel lanes when their
`cases/` packages differ.
They all share `evidence.yaml`, `validate.py` and the tripwire, so one coordinator
integrates them.

## Open Questions

- **Which rule marks an upper bound certified?** This decides whether 71 cases can ever
  clear by any route but an exact one.
  Three options:
  1. Keep `bounds_agree_at_declared_precision`. Groups A and B clear, $n = 29$ stays
     trailing (129, not 128), and group R and group C clear only through an exact
     certificate whose form the record can compare.
     In the 70 queued cases where the catalogue truncated by more than half a unit, that
     means none can clear except through an exact form.
  2. Count a bound as certified when the certified ceiling is at most the reported value
     plus one unit in its last printed place.
     This matches the measured truncation.
     $n = 29$ and every rational-promotion certificate so far would clear, and the
     evidence entry states the increase.
  3. A third stage state, *certified to within δ*, shown distinctly.

  The plan recommends option 2 for the stage, with the increase kept in the evidence and
  the reported algebraic number left uncertified in the claim boundary, as `think-stb5`
  wrote it.

- **Does a certificate for $n - 1$ by deletion need its own evidence entry,** or can the
  $n$ entry’s scope carry both sizes?
  The plan proposes one entry scoped to both.

- **Should a family extension get a `T-NNN` result?** The existing 17 exact certificates
  have none. The plan registers a result only for a first of its kind.

- **Should the owner ask the UnitSquare Project for its interval receipts?** A reply
  would give group C an external route.

## References

- Beads: `think-2716` (this epic); `think-n56i` (the stage decision); `think-zb78` (the
  citation data); `think-stb5` and `think-vyff` (the unopened rational promotion block);
  `think-3nc4`, `think-tow1` and `think-09q8`
- [X-009](../../../../packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md),
  which sequenced recognition first
- [Interval certification](../done/plan-2026-08-28-interval-certification.md) and
  [promotion pipeline](../paused/plan-2026-08-28-promotion-pipeline-implementation.md),
  the instruments group R’s exact route and group C need
- [Atlas expansion to 324](plan-2026-09-07-atlas-expansion-to-324.md), which generated
  the records above 100
- Commit `65af39faf`, the precedent block

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
