---
title: "X-011 — controls are not targets: weighted proofs, construction ladders, and precision-bounded surgery"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-011
  title: Controls are not targets — weighted proofs, construction ladders, and precision-bounded surgery
  date: '2026-08-31'
  author: OpenAI Codex, with three delegated read-only reviews, in the owner-directed W3 strategy session
  campaign: packing.squares
  brief: >-
    Reconcile the campaign's mature n = 5 control work, the newly recovered n = 17
    weighted-point certificates, the candidate cases n = 17--19, 37, 39, 41, 50,
    51, 53, 54 and 55, and the rounded UnitSquare n = 68/69 children into a
    mechanism-diverse strategy map. Separate controls from targets, current-value
    coverage from reproducibility coverage, and cheap falsifiers from premature record
    search. The owner then asked for the result to be codified as short agent-runnable
    blocks, so this exploration is the rationale for agenda-012.
  sources:
  - packing/campaign/ideas.md
  - packing/campaign/ledger.md
  - packing/campaign/agenda-map.md
  - packing/campaign/explorations/X-003-stratified-chunk-enumeration.md
  - packing/campaign/explorations/X-005-identity-relation-and-its-controls.md
  - packing/campaign/explorations/X-006-the-discriminating-control-at-n5.md
  - packing/campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md
  - packing/campaign/explorations/X-008-the-residue-is-axis-aligned.md
  - packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md
  - packing/campaign/explorations/X-010-two-lanes-two-ladders.md
  - packing/campaign/hypotheses/H-006-lp-dual-unavoidable-sets.md
  - packing/campaign/hypotheses/H-023-n5-terminal-connectivity.md
  - packing/campaign/hypotheses/H-030-public-parent-surgery.md
  - packing/campaign/hypotheses/H-034-fractional-piercing-ceiling.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-046-h-044-chunk-expressibility-verdict.md
  - packing/campaign/agent-sessions/session-049-reassess-and-first-sequenced-slice.md
  - packing/campaign/agent-sessions/session-060-verification-review.md
  - packing/frontier/n-017.md
  - packing/frontier/n-018.md
  - packing/frontier/n-019.md
  - packing/frontier/n-037.md
  - packing/frontier/n-039.md
  - packing/frontier/n-041.md
  - packing/frontier/n-050.md
  - packing/frontier/n-051.md
  - packing/frontier/n-053.md
  - packing/frontier/n-054.md
  - packing/frontier/n-055.md
  - packing/frontier/n-068.md
  - packing/frontier/n-069.md
  - packing/frontier/proof-strategies.yaml
  - packing/frontier/search-strategies.yaml
  - packing/frontier/source-coverage.yaml
  - packing/frontier/source-availability.yaml
  - packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
  - packing/resources/web/n17-lower-bounds-2026/README.md
  - packing/resources/web/kingbird-run-statistics-2026/README.md
  - packing/resources/web/unitsquare-release1-2026/README.md
  - packing/resources/web/unitsquare-release1-2026/results.json
  - packing/atlas/rendering/README.md
  - packing/atlas/known-best/README.md
  - packing/witnesses/known-best/n-068.yaml
  - packing/witnesses/known-best/n-069.yaml
  proposes: []
---
# X-011 — Controls Are Not Targets

**Date:** 2026-08-31

**Status:** Owner-directed W3 strategy synthesis.
It records source-backed proposals, repository measurements, and sequencing decisions.
It does not adopt the proposed `4.5058` lower bound, change a hypothesis verdict, infer
contacts from rounded SVGs, or claim that the literature search proves no omitted work
exists.

**Owns:** the portfolio comparison and the boundary between the next bounded blocks.
The underlying claims remain owned by the cited sources, witnesses, certificates, and
experiment records. Agenda-012 owns execution.

## The short answer

`n = 5` has paid for itself as an exact-method control, but it is not representative of
record search at `n = 17`, algebraic promotion at `n = 39` or `50`, rare basins at
`n = 51`, or source precision at `n = 68` and `69`. Twelve H-023 rounds have extracted
an exact fixed-angle face, an angle-and-slide sheet, complete first-order cones, and
several second-order obstructions without deciding the terminal-component relation.
One final bounded discriminator is defensible; another open-ended local-geometry series
is not. The discriminator must either transfer to `n = 10` or park the lane.

The highest-payoff immediate block is now the proposed Massaccesi lower certificate at
`n = 17`. Its exact-rational source verifier replays in seconds and reports 168 atoms,
total mass `9744/576 < 17`, 181 rational directions, and exact minimum `576/576`. That
is strong evidence and a weak independence story: the implementation descends from
Burns’s architecture, and no independent program has checked the fixed certificate.
Building that checker can move a proved lower frontier at `n = 17`, `18`, and `19`, or
find a precise defect, while leaving a reusable weighted-point instrument either way.

The `n = 68/69` colors also mean something, but less than an exact contact diagram.
The house atlas maps hue to orientation class and shade to contact count.
The retained `n = 68` witness really contains near-wall orientations about `0.009` to
`0.080` degrees off axis, well outside the `1e-6`-radian grouping tolerance.
Those offsets are in the retained numerical witness, not display antialiasing.
The witness itself is reconstructed from six-decimal SVG polygons, however, so its many
displayed digits are not independent source precision.
The reported 45-digit sides come from the UnitSquare release’s interval claims, whose
boxes, receipts, high-precision coordinates, and checker inputs were not publicly
released. A rigid-pose reconstruction under an explicit rounding envelope is the
necessary bridge before contact analysis or blinded surgery.

Three disjoint blocks should therefore begin together: the independent `n = 17` checker,
the `n = 68/69` precision bridge, and `n = 50` as a rational cross-scale exact-promotion
control. The first integration checkpoint then decides whether to adopt the weighted
bound, run blinded `n = 68` surgery, and take `n = 54` or `n = 39` as the next
construction-certification rung.

## What changed after X-010

Four facts reprice the program.

1. **A stronger proof opportunity appeared at `n = 17`.** Sam Burns proposed
   `s(17) >= 4.4811`; Gustavo Massaccesi then proposed `s(17) >= 4.5058` with a smaller
   LP-derived weighted certificate.
   The latter would improve the repository’s verified `4.426213` at `n = 17` and `18`,
   and Nagamochi’s `4.464102` at `n = 19`. It does not improve the `n = 20` lower bound
   `4.605551...`.
2. **Recent finite-case progress is not one method.** The 2024--2026 upper-bound events
   include stochastic searches, extensions of smaller constructions, constructed seeds
   followed by annealing, and UnitSquare results whose discovery method is undisclosed.
   X-010’s original description of every movement as stochastic was too broad.
3. **The apparently awkward medium cases form an instrument ladder.** `n = 18`, `50`,
   and `54` are positive controls over increasingly demanding exact fields; `n = 39` is
   a degree-five, non-radical interval target; `n = 19` and `53` are refusal controls;
   `n = 55` is an adversarial seven-angle case; and `n = 51` measures basin rarity
   rather than symbolic difficulty.
4. **The large public children are evidence-rich but coordinate-poor.** UnitSquare gives
   reported sides and a strong first-party verification narrative at `n = 68/69`, but
   the public geometry is a rounded rendering.
   BC-050 is blocked for the right reason: the missing object is a surgery-grade
   witness, not another contact tolerance.

## Why `n = 5` helps—and where it stops helping

`n = 5` is unusually valuable because the optimum is known and the exact arithmetic is
small enough to expose false shortcuts.
It has already caught errors in active-row ownership, tangent reasoning, tied supports,
second-order jets, and the temptation to equate a key or contact signature with a
connected component.
That makes it a permanent control for exact LP, continuation, contact grammars, and
identity machinery.

It is not representative along the dimensions that drive the open frontier:

| Dimension | `n = 5` | Cases that exercise it |
| --- | --- | --- |
| Oblique multi-block record geometry | one small exact mechanism | `17`, `39`, `41`, `55` |
| Weighted lower certificates | absent | `17`--`19` |
| Algebraic/interval promotion | quadratic and tiny | `18`, `39`, `50`, `54` |
| Rare stochastic basin | not established | `51`, `55` |
| Rounded-source uncertainty | absent | `68`, `69` |
| Construction surgery | no public parent/child pair | `68`, `69` |

The remaining H-023 question is real, but its marginal program value is now bounded.
BC-010 gets one final block: decide one connection/separation discriminator, exercise
the same observable at `n = 10`, and stop if the transfer is unavailable.
`n = 5` may continue appearing as a known-answer control; it should not be reported as
target progress merely because another local stratum was classified.

## The weighted proof lane: `17` to `19`

The proposed argument assigns nonnegative rational weight to atoms inside a square of
side `L`. If every possible unit-square pose captures mass at least one while total mass
is less than 17, seventeen disjoint unit squares cannot fit.
The continuous pose space is reduced by a rational angle cover and an exact event-cell
sweep.

The source-backed state is unusually good for a web result:

- Burns publishes a proof note, 268-atom certificate, exact verifier, and explicit
  proposed/not-independent status at `4.4811`.
- Massaccesi publishes a 168-atom certificate at `4.5058`; the extracted verifier
  replays under the repository’s Python 3.14 environment in under five seconds.
- The exact totals and minimum reproduce.
  A read-only audit found the angle cover, shrunken-square containment, sweep, and
  scaling argument coherent.
- The audit also found concrete source defects: the float LP generator omits an
  inclusive endpoint, the illustration divides by 29 where the verifier uses 28
  intervals, and the prose contains two transpositions.
  None changes the final verifier’s reported result, but all matter when the method is
  generalized.

The decisive missing evidence is not another run of the same program.
It is an independent exact implementation with a different accumulation mechanism, plus
mutations that must fail.
The block should freeze the certificate data, harden the source-faithful replay against
optimized-Python `assert` removal, then compute the arrangement-cell minimum without
copying the published two-dimensional difference-array sweep.

If the independent result agrees, a later assurance block can determine adoption at
`n = 17` and monotone transfer to `18` and `19`. If it disagrees, the disagreement is
already a publishable-quality defect localization.
In either case the generic weighted-point certifier is a higher-leverage proof
instrument than another bespoke point-set search.

Burns’s separate near-record construction at side about `4.677648`, just above the
`4.675530` record, also matters strategically.
Its topology differs from Bidwell’s. That does not improve the upper bound, but it is
direct evidence that the `n = 17` landscape has more than one competitive structural
basin. It strengthens `n = 17` as a search calibration while remaining separate from the
lower-bound certificate.

## The construction and certification ladder

Visual complexity is not a reliable difficulty measure.
Algebraic degree, local mobility, source precision, and basin rarity are nearly
independent. The useful order is therefore a ladder of instrument demands rather than a
ranking of pretty pictures.

| Role | Case | Why it is informative | Cheapest next decision |
| --- | ---: | --- | --- |
| exact positive control | 18 | verified `Q(sqrt(7))` pose; proves the lift can leave `Q(sqrt(2))` | keep as known answer |
| refusal control | 19 | exact `Q(sqrt(2))` construction, but a different mechanism | ensure the recognizer does not overfit `n = 18` |
| rational large control | 50 | reported side `53/7`; large enough to test scale without field complexity | reconstruct and verify exactly first |
| non-radical interval target | 39 | side has degree five and Galois group `S5` | certify an isolating interval and pose; do not search for radicals |
| rare-basin benchmark | 51 | 4 of 3,004 categorized source runs refined to the record | benchmark a proposer only after a mechanism-matched control passes |
| representation refusal | 53 | reported side lies in `Q(sqrt(7))`, retained pose does not stably lift there | require typed refusal, not forced recognition |
| nested-radical positive | 54 | explicit quartic/nested-radical side | take after the rational `n = 50` control |
| adversarial representation | 55 | seven retained orientation classes and substantial slides | held-out stress test, not first implementation target |

`n = 37` remains useful as an older algebraic reconstruction control, while `n = 41` is
a high-degree hard discriminator for a mature interval pipeline.
They should not be the first block.
The immediate cross-scale sequence is `18 -> 50 -> 54 -> 39 -> 55`, with `19/53` as
refusals and `51` in a separate search-cost lane.

The first-party run statistics quantify why direct record chasing is not low-hanging
fruit. On Ellsworth’s stated RTX 3080 Ti setup, `n = 51` produced four record-refinable
instances among 3,004 categorized runs, with a source estimate of 4.917 hours per hit;
the `n = 55` source estimate is 40.604 minutes per screened-and-refinable hit.
These are regime-specific observations, not portable forecasts.
Without the source program, settings, and seeds, matching the wall clock is not a
reproducibility test.

## Precision-bounded surgery at `n = 68/69`

The color observation is valid under the house renderer and invalid under the raw source
SVG palette. House hue encodes orientation modulo a quarter turn; house shade encodes
full-side contact count.
The source SVG’s colors are decorative/index-based and carry no angle claim.

The retained UnitSquare witnesses pass the repository’s rendering-level check, but their
square-shape residuals are about `1.927e-8` at `n = 68` and `1.491e-8` at `n = 69`,
versus roughly `5.1e-50` or better for the other contact-screen witnesses.
They are therefore excluded from contact and translation-motion claims.
Appending decimal digits during reconstruction does not recover source precision.

The first block must build the missing bridge as a reusable tool:

1. interpret each six-decimal SVG coordinate as a declared rounding interval;
2. fit the nearest rigid unit-square pose and preserve all compatible solutions or an
   explicit ambiguity bound;
3. verify a conservative relaxed container bound and pair separation;
4. classify which apparent contacts survive the whole envelope; and
5. emit a surgery-grade candidate or a typed source-precision refusal.

Only then should H-030 hide a released child and attempt public-parent surgery.
`n = 68` goes first: its released improvement, `7.68618e-5`, is about twelve times
`n = 69`’s `6.54811e-6`. That makes success easier to distinguish from the numerical
floor. A cold global search, an optimality attempt, and exactification of the superseded
`n = 69` parent are premature.

## What the literature audit establishes

The additional author, phrase, arXiv, and case-number searches through 2026-08-31 found
no overlooked 2020--2026 paper that establishes a new finite-case record or exact value
for the prioritized cases.
The relevant recent papers in the retrieved corpus concern asymptotic waste, not these
finite records. The new finite-case evidence lives in first-party catalogue pages, SVGs,
run-statistic files, public repositories, and the two August 2026 `n = 17` posts.

That is a bounded search result, not a proof of absence.
More importantly, the research record is complete along only one axis: the named current
upper values agree with the live sources checked on the audit date.
Three other axes remain incomplete:

- **source and witness coverage:** high-precision child coordinates and some generating
  equations are missing;
- **record chronology:** the dated event chain and construction genealogy are partial;
- **method reproducibility:** Schadt/Ellsworth code, exact settings and seeds, and the
  UnitSquare interval artifacts are not public in the retained sources.

Trevor Green’s older lower bounds illustrate the distinction.
Friedman’s 2009 survey prints stronger formulas for ranges including `17--18`, `37--39`,
`40--41`, and `50--53`, but cites Green’s 2000 private communication rather than a
retrievable proof. Those values are useful targets and provenance gaps; they are not
overlooked modern papers and cannot be promoted as verified bounds from the survey table
alone.

## Routes to avoid now

- more `n = 5` local analysis without a transferred `n = 10` discriminator;
- treating a source-verifier replay as independent certification;
- a cold global search or the registered 100-times annealer;
- recovering exact contacts from six-decimal SVG coordinates;
- exact optimality work at `n = 68/69` before a surgery-grade witness exists;
- exhaustive chunk enumeration beyond the measured `K <= 3` tractable class;
- reusing the bar/L/rectangle grammar as though exp-046 had validated it for tilted
  contact assemblies; and
- treating all recent records as stochastic or visual complexity as a difficulty score.

## Decision and handoff

Agenda-012 starts three disjoint blocks, each with its own bead and owned paths:

1. `BC-108`: independently verify or reject the fixed `n = 17` weighted certificate;
2. `BC-109`: build the `n = 68/69` rounding-envelope rigid-pose bridge; and
3. `BC-110`: exactify `n = 50` as the large rational positive control.

`BC-111` is a 45-minute evidence checkpoint, not a fourth experiment.
It can promote the already-lined successors: assurance and a generic weighted proof tool
(`BC-112`), blinded `n = 68` surgery (`BC-113`), and one construction-certification rung
(`BC-114`). Existing BC-010 remains the sole `n = 5` commitment and is capped as above.

This portfolio has three independent ways to pay: a stronger lower bound, a validated
construction method, or a precision-aware route into high-`n` surgery.
A negative in any lane removes a specific assumption without invalidating the other two.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
