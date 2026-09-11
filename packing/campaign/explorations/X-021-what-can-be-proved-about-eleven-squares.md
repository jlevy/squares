---
title: X-021 — what can be proved about eleven squares, and what each proof buys
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-021
  title: What Can Be Proved About Eleven Squares, and What Each Proof Buys
  date: '2026-09-08'
  author: Claude coordinator (Fable), with four Fable mathematical lanes at maximum effort and two Opus lanes for bookkeeping and review
  campaign: packing.squares
  brief: >-
    Pursue X-019's exploration as a programme: find structural constraints on packings of
    eleven unit squares that can actually be proved — corner and wall structure, orientation
    classes, contacts and spanning — and measure what each proof buys toward a global
    exclusion at 96/25. Separately, read Stromquist's exact proof of s(10) for what transfers,
    and map the ambitious route: whether constraints can narrow the band below Trump's value
    until general arguments close it. Then lay the coming research sessions out as parallel
    lanes with disjoint deliverables. Planning only: no target run was registered.
  sources:
  - packing/campaign/explorations/X-019-structural-restrictions-and-conditional-dots.md
  - packing/campaign/agendas/agenda-029-structural-restrictions-and-conditional-dots.md
  - packing/campaign/explorations/X-014-closing-from-both-ends.md
  - packing/campaign/explorations/X-017-compatibility-and-complete-case-covers.md
  - packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md
  - packing/campaign/hypotheses/H-036-robust-restricted-orientation.md
  - packing/campaign/hypotheses/H-063-n11-class-certificate.md
  - packing/campaign/hypotheses/H-102-complete-restricted-angle-support-families.md
  - packing/campaign/hypotheses/H-111-resource-anchor-case-exclusion.md
  - packing/campaign/hypotheses/H-117-forced-angle-complexity.md
  - packing/campaign/hypotheses/H-121-axis-plus-one-minimizer.md
  - packing/campaign/hypotheses/H-126-insertion-saturation-corner-structure.md
  - packing/frontier/n-010.md
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/cases/n11_fractional_certificate/certificate.json
  - packing/cases/trump11/packing.py
  - packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
  - packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-ii-ten-unit-squares.md
  - docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md
  - packing/src/sqpack/fractional/classcert.py
  - packing/src/sqpack/fractional/ceiling.py
  proposes: [H-127, H-128, H-129, H-130, H-131, H-132, H-133, H-134]
---
# X-021 — What Can Be Proved About Eleven Squares, and What Each Proof Buys

**Structural constraints on eleven-square packings can be proved, several were proved
today, and the honest finding is that they give case splits more readily than
headroom.** Four mathematical lanes ran in parallel on the question X-019 posed: corner
and wall structure (lane A), orientation classes (lane B), the transfer of Stromquist’s
exact proof for ten squares (lane C), and contact lemmas together with the closing route
(lane D). Their reports are retained under
[`results/agenda-030/`](../series/series-000-smoke-and-calibration/results/agenda-030/README.md)
with every script they ran.
This document compresses them, separates what is proved from what is measured and what
is open, and hands
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) a set of
research sessions that can run at once.

The bracket is unchanged: `3.810025723614703 ≤ s(11) ≤ U = 3.877083590022814`. The
working target is `q = 96/25 = 3.84`. Nothing here is a new bound.

## The Question in Two Tiers

The owner’s question has a narrow form and an ambitious form, and they need different
evidence.

The **narrow form** asks whether *some* constraints on square placement can be proved —
squares in corners, a bound on the number of angles, forced adjacencies — and whether a
proved constraint gives a weighted-dot certificate room it does not otherwise have.
Even small progress shows the direction is real.

The **ambitious form** asks whether constraints could narrow the band `[L, U]` so far
that general arguments eliminate it entirely and settle `s(11)`. That is a question
about the shape of a complete proof, and it was answered by pricing the three candidate
architectures rather than by hoping.

Every statement carries one of four labels: **proved** (a proof is written in the lane
report), **exact-verified** (decided by the repository’s own exact verifier on stated
inputs, a theorem without a hand proof), **checked** (a numerical computation with its
script retained), or **open**.

## What Was Proved About Corners and Walls

Lane A started from X-019’s two elementary facts and confirmed both: the four corner
blockers are distinct, and `min_{p∈Q}(x+y) = g_x + g_y + sin φ` with the minimum at the
lowest or leftmost vertex.
It then proved seven further statements.
Write `κ = L − 2.96`, the margin the twelve-square certificate leaves at side `L`
(`0.88` at `q`, `0.9171` at `U`).

- **Insertion saturation with overhang** (proved).
  Every closed unit square in `[−d₁, L+d₂] × [−d₃, L+d₄]` with `d₁+d₂ ≤ 3.96 − L` and
  `d₃+d₄ ≤ 3.96 − L` meets the interior of some packed square.
  So in every corner some square meets the open box `(0, κ)²`, not merely the unit box,
  and along every wall every unit window of the strip of width `κ` is met.
- **Corner core** (proved, new).
  Every unit square in the closed quadrant that meets the corner triangle `x + y ≤ d`
  contains the closed box `[d, 1]²`, and the box is exact.
- **Uniqueness of the corner occupant, sharp threshold** (proved).
  For `ε < 1` at most one packed square meets the triangle `x + y ≤ ε`; X-019’s
  threshold `1/√2` is not sharp, and `1` is (two axis squares meet `x + y ≤ 1` with
  disjoint interiors).
- **Exact blocker-pose region** (proved).
  A closed formula decides whether a pose meets `(0, ρ)²`; every snug square of every
  angle blocks `(0, κ)²`, so no angular restriction on a blocker follows from blocking
  alone.
- **Occupancy from monotonicity** (proved).
  With `s(2) = 2`, `s(5)`, `s(6) = 3` and `s(10)`: at `q` at least ten squares meet the
  annulus of width `0.92`, at least seven the annulus of width `0.566`, and in each
  corner frame at least six squares meet the L-strip of width `0.84`. The corner form is
  tight on Trump’s packing.
- **Wall service** (proved).
  Two corner blockers alone cannot serve a wall strip of width `κ` once
  `L ≥ 1 + 2√2 = 3.8284`: a third square meets every wall strip at `q`, and Trump has
  four or five per wall.
  The third square can be shared by two adjacent walls, so this yields two extra
  distinct squares, not four.
- **Two sound certificate shapes** (proved, unrun).
  A *corner-class certificate* prices the four blockers’ cores at a threshold `w_c ≥ 1`
  and the other seven at `w_f`, a region analogue of X-014’s class certificate that the
  folded solver runs with one extra row predicate.
  A *complete corner cover by penetration depth* bins each corner’s penetration `δ_j`,
  banks the box `[d, 1]²` for a shallow corner, and clips the centre domain by the safe
  core half-plane `a + b > d + B cos θ` for a deep one; the clip is convex, so the
  retained sweep needs a clip rather than a new engine.
  The 2026-09-08 review corrected the former unit-square clip, which could omit cores of
  parents at angles between net directions; lane A’s Theorem B contains an exact
  counterexample and the repaired inclusion proof.

What lane A could **not** prove, and showed cannot be proved by any argument valid up to
`U`: no positive corner penetration, no bound on a blocker’s angle, no square vertex
within a fixed distance of a container corner.
Trump’s own fourth corner at side `U` has penetration `0.8445` and a free axis box of
side `0.8317`, and Trump’s packing placed in `[0, 3.95]²`, where insertion saturation
still holds, leaves a free corner box of side `0.9046` against a forced box of side
`0.99`. The strongest true statement is `δ_j < 2κ`.

## What Was Proved About Orientation Classes

Lane B sharpened the nine-point argument and then ran the repository’s class program at
`q` to turn bands into exact count theorems.

- **Nine-point theorem with exact constants** (proved).
  At most nine squares have folded tilt below `θ₀(L)` with `cos θ₀ + sin θ₀ = 4/L`:
  `2.44001°` at `q`, `1.84653°` at `U`. The pitch-`L/4` grid is exactly sharp, every
  nine-point axis-piercing set has one point in each of nine boxes of side `4 − L`, and
  product nine-point sets cannot reach beyond `5.24°` at `q`.
- **A wider nine-point band** (exact-verified).
  The nine points `{1 − 1/200, q/2,
  q − 1 + 1/200}²` pierce every admissible core in the leading eighteen half-gap cells
  of the retained net, so at `q` at most nine squares have folded tilt in those cells
  (upper angle approximately `4.6122°`); at `U` the same set’s reported endpoint is
  approximately `3.2953°`.
- **Band certificates at `q`** (exact-verified on a grid-79 site set with inset `1/10`,
  decided by the exact sweep).
  At `q`, at most nine squares have folded tilt in cells 0–24, ten in cells 0–39, nine
  in cells 171–180, ten in cells 149–169, and ten in cells 117–180. At `U`, the counts
  are nine in cells 0–24, ten in cells 0–29, and ten in cells 175–180.
  [H-131](../hypotheses/H-131-near-axis-counts-at-q.md) and
  [exp-131](../series/series-000-smoke-and-calibration/experiments/exp-131-h131-near-axis-counts-replay-at-q.md)
  give the exact rational cell boundaries.
  The 2026-09-08 review corrects the former degree summaries: the axis count ends at
  approximately `10.3874656704°`, and the forced low-angle square has tilt below the
  lower boundary of cell 117, approximately `30.0148587980°`; a tilt below `30°` is not
  established. The attempted wider bands that failed on grid 79 remain site-set readings.
- **A robust `{0°, 45°}` band excluded at `q`** (exact-verified, mass `10.702`). No
  packing of eleven at side `≤ 3.84` has every folded angle in
  `[0°, 1.45°] ∪ [43.76°, 45°]`. The next widenings, `3.3°` on each end and
  `[0°, 7.8°] ∪ [38.2°, 45°]`, are not refuted on grid 79, which a finer site set may
  change.
- **Stromquist’s Theorem 3 transported to `q`** (proved, modulo the source theorem).
  Every packing of eleven at side `≤ 3.84` has a square whose folded angle is farther
  than `0.6848°` from both `0°` and `45°`; the exact-verified band above is twice as
  wide and uses no Stromquist input.
  Both are far stronger than H-036’s `0.25°` in the band and weaker in the side; H-036
  stays open.
- **Fixed-angle packing floors** (checked, rigorous lower bounds).
  Nine squares at any common tilt up to `30°` fit in `[0, q]²`, and eight at `35°` to
  `45°`. So no near-axis band can force more than two squares out, by any covering
  method, and no band anywhere gets a count below eight.
- **Segment propagation and movability** (proved).
  Positive-length contacts equate orientations and give rank `11 − k` for `k` unanchored
  components; a square with fewer than three independent point contacts can move, so a
  locked orientation needs a segment, a corner coincidence, or three stressed point
  contacts. Neither statement bounds the number of orientation classes of an unknown
  packing.

The composition split itself refutes nothing at `q` for `n₀ ≤ 9` on grid 79: for three
to eight near-axis squares the optimal thresholds coincide to two per cent, so the
two-threshold program degenerates to the unconditional one, and the all-tilted
composition sits at `11.21`.

The diagnostic that matters most came from reading the retained `3.82` fractional dual:
of its `10.38` units of weight, `6.54` sit within `2.5°` of the axes, `1.33` near `29°`,
`0.69` near `8°`, and only `0.41` in `[38.2°, 45°]`. The obstruction the instrument sees
near `q` is not Trump-shaped.
It is seven near-axis cores plus fractional mass at angles no integral packing realises
beside them — an integrality gap of the covering relaxation — and that is where
geometric conditioning has to work, not angle counting.

## What Transfers From the Proof of `s(10)`

Lane C reconstructed Stromquist’s Theorem 1 step by step and confirmed the lemma
arithmetic, including the transcription’s flagged erratum (`f(√(4/5)) = 0.914538` at
`31.456°`, not `.926` at `24.1°`; the application at `b = .9` is unaffected).
The mechanism is: ten unavoidable points, exactly-one ownership at `|P| = n`,
alternative covers that transfer containments, an existential forced incidence with a
segment, and a packing-dependent thirteen-point final cover.

Three results are new.

- **Theorem 2 is an anchored certificate, not an unavoidable set** (proved).
  A `K4`-symmetric measure of mass `10` covers every box outside an escape class, and an
  asymmetric measure of mass `12` with threshold `3` on the anchored escapes closes it
  because `12 < 10 + 3`. The `K4`-average of the same atoms fails
  (`mass/threshold ≥ 34/3 > 11`, with an explicit witness box), so the symmetry-breaking
  anchor is load-bearing.
  X-019’s “asymmetric dots on a labelled case” was already realised in 1984.
- **The ten-point scheme is rigid at `2 + 4/√5`** (proved).
  Every sloping edge of the Figure-13 localisation equals `(L/2 − 1)√5/2`, which is `1`
  exactly at `2 + 4/√5`; exact rational interior escapes exist at `3.79`, `3.80`, `3.82`
  and `3.84` (at `q`: centre `(73/50, 67/50)`, `tan(ψ/2) = 49/200`, least margin
  `14979/1060025`). The forcing lemmas survive at `q` with moved coordinates, but the
  localisation that produces the anchor weight does not, and the Figure-14 mesh would
  need a thirteenth point.
  Nothing in the ten-point scheme reaches past `3.7889`.
- **Ownership and transfer for weighted atoms** (proved).
  With mass `11 + ε`, every atom of weight above `ε` lies in exactly one core; if moving
  weight `w > ε` from atom `p` to `p′` keeps the measure valid, the core owning `p`
  contains `p′`; and per-pattern measures on a heavy-atom skeleton give an
  ownership-conditioned certificate whose `ε = 0` form is an exact cover, the “plateau
  certificate”. The corollary with teeth: T-018’s four corner atoms (weight `917/6250`,
  pairwise `1.8146 > B√2`) cannot share a core, so **any valid measure at `q` with those
  atoms and mass below `11.147` proves that every packing at `q` has four distinct
  squares each containing its corner atom** — sharper than insertion saturation’s
  blockers, obtained from the LP alone.
  Whether such a measure exists at `q` is unmeasured.

What does not transfer: exactly-one ownership at `|P| = n`, the existential segment
incidence (an H-097 object with no measure form), the packing-dependent final cover
(only a case tree hosts it), and the open-box endpoint device (replaced by T-022’s
dilation). Integral eleven-point unavoidable sets at `q` are not excluded by anything
known, but they would prove nothing by themselves; the count Stromquist actually uses
needs twelve points and an anchor weight of three, and the anchor is what dies.

## What Was Proved About Contacts, and the Duality That Prices Every Dot

Lane D proved the spanning statements a side-minimal packing must satisfy and then the
result that quantifies the whole conditional-certificate programme.

- **Spanning** (proved).
  Some contact component of a side-minimal packing joins two opposite walls.
  “Or”, not “and”: the two-square minimiser spans one direction only, so both directions
  cannot be forced by the shrinking argument, though Trump spans both.
  Point contacts suffice (Göbel’s `n = 5` optimum spans through four corner-on-edge
  contacts), so nothing forces positive-length contacts.
- **Chain projections** (proved, checked).
  Along a spanning chain `Σ (cos θ_i + sin θ_i) ≥ L`. At `q` a chain needs at least
  three squares; a three-chain has every member tilted at least `0.667°`, two at least
  `14.05°`, one at least `19.84°`, and no axis square.
  A four-chain forces nothing.
  A free case split with no headroom for the current instruments.
- **Fixed-angle representatives** (proved; contact inference corrected September 10).
  Every preselected SAT cell containing a minimiser has a vertex with twenty-two
  independent active selected rows, but a tight selected pair row need not be a physical
  contact. Separately, every connected component of the full fixed-angle feasible space
  at a fixed side has a representative with twenty-two independent genuine contact rows;
  each physical contact component touches the left and bottom walls.
  This second statement chooses a suitable cell after minimizing over the full
  component, so it does not restore the stronger contact claim in every preselected cell
  or force a literal corner occupant.
  Angular rank is not forced (the `n = 6` rattler).
  At most three squares are flush on any wall.
  See the
  [structural review](../../../docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md).
- **Robust transfer** (proved).
  Facts that use optimality hold at the unknown side, not automatically at `q`; dilation
  turns their contacts into near-contacts with tolerance `0.01113` at `q` and walls
  `0.00556`. The fixed-side genuine-contact representative above is proved directly at
  every feasible `q` and needs no dilation.
  Every other optimum-only structural lemma handed to a certificate must state the
  required tolerance.
- **Duality bounds a specified single-core covering program** (proved in the form
  corrected in lane D on 2026-09-08). A depth-one family with sufficient weight in that
  program’s admissible class gives a weak-duality obstruction on every site set.
  For strict capture, the core family must lie outside the stated captured set `N`. A
  family outside `N` does not by itself obstruct a geometric conditional program or a
  certificate involving several squares.
  Two corollaries were checked on retained data:
  - with `B = 9977/10000`, `t = 207107/500000` and `δ = 2 arctan t − π/4 > 0`, the
    `{0°, 45°}` packing of side `2 + (4/3)√2` supplies the retained-net obstruction for
    strict capture of the stated Trump-neighbourhood set at sides strictly above
    `C_B = B(2 + (4/3)√2)(cos δ + sin δ)`. The signed-angle correction is recorded in
    lane D. Since `√2 < 665857/470832`,
    `C_B < 22275352724718225/5745980944770482 < 38767/10000 < U`. The strict side
    inequality places the closed cores in their parents’ interiors; no assertion is made
    at equality. With `B = 1` this particular obstruction below `U` disappears;
  - BC-200’s depth-one family at `191/50`, moved to `q`, keeps `≥ 8.8732` of its
    `9.9079` off a unit corner box, `9.0293` off a half-unit box and `7.0992` off a
    central unit box. Boxing one blocker removes about one unit of fractional weight, the
    integral count and no more; corner conditioning is neither killed nor shown to have
    headroom.
- **A correction to X-014’s equality run** (proved).
  The run at a rational side `L₁ > U` is sound only if `L₁ − U < κρ₀/4 ≈ 6.6 × 10⁻⁶`,
  because translates of Trump’s pose are packings at side `U + σ` at chart distance `σ`
  and nearby packings extend to distance up to `2σ/κ`, and only with `B = 1`. The two
  sound closing designs are an exact-side tree over `Q(u)` finished by the modulus
  lemma, or a `B = 1` capture run at `U + σ` with `σ < 10⁻⁵`.

## Obstructions Worth Recording

- **No lemma forces positive corner penetration, an axis-aligned blocker, or a
  positive-length contact.** Trump’s fourth corner and Göbel’s `n = 5` optimum are the
  counterexamples to any statement valid up to `U`; a `45°` square snug in a corner
  blocks the box while touching nothing flush and is neither refuted nor realised in a
  packing below `3.96`.
- **Angle counting cannot get below the fixed-angle floors.** Nine near-axis squares are
  the best possible count at `q` by any covering method, and the only room is in the
  width of the band. The composition route can close only a down-set complement of the
  class-weighted fractional packing polytope, and the `3.82` dual’s support says the
  survivors are near-axis compositions with fractional mass at `29°`.
- **The ten-point scheme has a ceiling.** Stromquist’s localisation is rigid at
  `2 + 4/√5`; no coordinate change pushes it past `3.7889`.
- **H-121 has three precise obstructions.** Single-square motions cannot merge classes
  (a confined square can have a feasible angle interval avoiding `0°`, `45°` and every
  neighbour’s class); a locally isolated multi-class packing makes the elimination lemma
  a comparison of global optima, not a perturbation; and the `n = 17` and `n = 29`
  records carry two and five distinct non-axis orientations, so any proof must use
  `n = 11` geometry. A packing at side `≤ U` with no segment contacts at all is obtained
  from Trump’s by shrinking each square about its centre, so a bound on the number of
  orientation classes can only hold for minimisers, which no test below `U` can reach.
- **“Narrow enough” is the wrong frame.** Narrowing `[L₁, U]` from `3.84` to `3.869`
  shrinks the discard ball around Trump’s pose (`0.054 → 0.025`, floor `0.004`), weakens
  the nine-point forcing (`2.44° → 1.97°`), widens the transfer tolerance, and does not
  touch the competitor question.
  The tree of a proof is governed by how much of configuration space a general argument
  discards *at side `U`*, not by the band’s width.
- **The retained shrink limits the specified covering programs.** The stated strict
  capture program has an obstruction above `C_B < 3.8767`, as corrected above; this is
  not a cap on all geometric conditional or multi-square certificates.
  With `B = 1` this particular obstruction below `U` disappears and the corresponding
  covering value remains to be established.

## The Ambitious Route, Priced

Three architectures could settle `s(11) = U`. Each was priced with the constants the
record already holds.

| Route | Closing step | Raw tree | The lemma that collapses it |
| --- | --- | --- | --- |
| (a) Trump’s combinatorial type, then exact algebra over `Q(u)` and the modulus lemma | cheap, exists (exp-013, BC-199) | `10^40` to `10^42` feature selections | an **ownership lemma**: a robust unavoidable set of at most eleven marks at `q` would localise every square and leave about `2^20` exact LPs |
| (b) Conditional certificates on a finite cover, the modulus ball inside | X-014 Lemmas 1–3 exist; the domain generalisation does not | `10^17` to `10^24` boxes before pruning | a valid **integer-hull cut family** (corner-triangle cliques, subset capacities, composition rows) pushing the fractional value below `11`; by the duality above, the only way boxes can beat the plateau |
| (c) Shrink-free ladder (`B = 1`, open placements, interval-decided directions) | a ladder, no tree | none | nothing; it inherits the `B = 1` plateau, which is the decisive unmeasured number |

The honest assessment is that dot certificates alone cannot finish.
A complete proof needs a structure theorem (ownership or a normal form) plus exact
fixed-angle algebra plus the modulus lemma, and the earliest point at which hopelessness
could be known is a `B = 1` fractional packing of value at least `11` at some side below
`U` with a unit of weight away from Trump’s placements: by the duality lemma that kills
every one-body certificate, conditioned or not, and leaves only cuts whose sufficiency
is unproved.

What the narrow tier buys the ambitious one is concrete.
Corner banking, the four-corner containment corollary and the wall-service lemma are
exactly integer-hull information; whether it moves the fractional value at `q` is a
measurement the lanes below make before any engine is built.

## The Lanes

Agenda 030 turns the lane reports’ twenty-two session proposals into eleven research
lanes with disjoint deliverables and files, plus a selection cell and a closeout cell.
Nine run in parallel from the start; two wait on a measurement.
The full specifications, entry and exit conditions, falsifiers, instruments and budgets
are in the agenda; this table is the map.

| Lane | Question | Decides |
| --- | --- | --- |
| Corner-class LP and corner cover | Does pricing the four blockers or banking their boxes give surplus at `q`? | whether corner information has value for a certificate |
| Corner-skeleton ownership | Does a valid measure at `q` with T-018’s corner atoms and mass below `11.147` exist? | the four-corner containment theorem |
| Kill tests and the `B = 1` value | Restricted fractional values at `q`; `ν*` at `B = 1` at `3.84`, `3.86`, `3.87` | routes (b) and (c), and every capture design |
| Angle-band theorems at `q` | The robust `{0°, 45°}` band, the optimal nine-point band, the ladder toward the Trump band | the first new band theorem below `U`; where the fractional obstruction lives in angle |
| Composition split at `q` | Which compositions `(n₀, 11 − n₀)` close, with a fractional-packing certificate for the rest | the end of the composition route, or its branch list |
| The `3.82` plateau | Site artefact test, shrink tax, then the plateau certificate as an exact cover | whether the ladder’s top is the instrument’s or the geometry’s |
| Rectangle no-fit and wall proximity | Largest `H₀` with no packing in `3.84 × H₀` | the strongest symmetry-breaking premise available |
| Localisation and the anchored certificate at `q` | The ten-point band at `q`; an escape-tolerant two-branch certificate | whether Stromquist’s anchor mechanism works above `3.7889` |
| Adversarial witnesses and the mixed pocket | Packings below `3.96` with unusual corners; realisability of a confined rattler | which branches cannot close, and whether H-121’s local step has any hope |
| Ownership set at `q` | A robust unavoidable set of at most eleven marks | the collapse of route (a) |
| The closing design | Exact-side tree and `B = 1` capture priced as one architecture | the endpoint, honestly |

## What This Document Does Not Establish

No bound changed. Every count theorem at `q` above was decided in a planning lane on a
stated site set and is registered as a hypothesis for replay under an experiment record
before it is cited as a result; a non-refutation on a finite site set is never evidence.
The four-corner containment corollary is a theorem only if its measure exists, and the
existence is the lane’s first measurement.
The lane reports’ scripts are retained beside them, but none was promoted to
`devtools/`; the first lane that reuses one owns that promotion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
