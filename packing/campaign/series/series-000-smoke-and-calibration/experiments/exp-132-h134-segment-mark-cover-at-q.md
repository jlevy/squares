---
title: exp-132 — the ten-segment robust unavoidable set at 96/25
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-132
  series: series-000
  title: >-
    Decide whether a robust unavoidable set of at most eleven marks exists at side 96/25,
    and certify the survivor's cover of pose space
  date: '2026-09-08'
  hypotheses: [H-134]
  tier: confirmatory
  subject:
    label: >-
      the robust unavoidable-set question at side 96/25 with every mark thickened by the
      transfer tolerance 3/500 — the ten horizontal segments of length 1/10 centred on
      Stromquist's Figure-13 points scaled to 96/25 (set-S10-l0.1.json), the same ten with
      the centre point added, and the shorter lengths 9/100, 8/100, 7/100 and 6/100 —
      decided over the whole pose space of closed unit squares contained in [0, 96/25]² at
      every angle, together with the thirteen candidate point sets built from T-018's atom
      skeleton and from Stromquist's rows
    engine: >-
      the lane's own instruments, reproduced verbatim in lane E's appendix of scripts and
      data as run — cover_reader.py, an interval reader over the pose space (t, cx, cy)
      with the Lipschitz bound of the lane's Section 6.1 and an exact fractions.Fraction
      re-certification mode; escape_engine.py, the falsifier (numpy grid, Nelder-Mead
      refinement, exact rational decision by two independent distance methods that must
      agree); reader.py, an independent standard-library reader; and variants.py,
      spotcheck.py and reader_sanity.py as their drivers. No repository code was modified;
      sqpack.cover and the exp-121 instruments were read, not run
    engine_commit: d04205fb
    assurance: verified
    method: interval-certified
    host_system: >-
      linux x86_64, four cores shared with seven other agents at load average 4 to 14, one
      worker (PACK_JOBS=1), the project's Python 3.14.7 with numpy 2.5.2 and scipy 1.17.1
      from the frozen environment
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Six self-tests of the falsifier, all passed before any candidate ran: lane C's exact
      escape of the ten Figure-13 points at 96/25 reproduced to its retained margin
      14979/1060025; exp-121's frozen square at 1939/500 reproduced as a strict escape and
      correctly refused as an escape against 3/500; the search rediscovering an escape of
      the ten points; and three no-escape controls (points on a 0.3 grid, three full-width
      horizontal segments at y = 1, 48/25 and 71/25, and a square placed just beside a
      segment on each side of the tolerance). Against the certified set the controls are the
      falsifier itself at grid step 0.02 and angle step 1.5°, the finer sweep at 0.01 and
      0.75°, 300 random contained poses, and 6 000 random poses inside 3 000 random
      certified leaves re-decided by the falsifier's exact distance. Every catalogued escape
      of a point set was re-read by reader.py, which shares no code with the engine.
    candidate: >-
      the ten closed horizontal segments of length 1/10 centred on Stromquist's Figure-13
      points scaled to 96/25, certified over pose space by the interval reader and then
      re-decided exactly leaf by leaf and discard by discard; the same set with the centre
      point added, and the segment lengths 9/100, 8/100, 7/100 and 6/100 run identically to
      locate the threshold. Against them, the point form: T-018's eleven heaviest atoms
      scaled by 384/381, a greedy cover from its 93 heaviest atoms, Stromquist's ten points,
      those ten plus the centre, those ten plus one point optimised by an adversarial
      min-max, the polished K4-symmetric optimum and a free 22-coordinate optimum, each run
      through the falsifier at the same resolution and decided exactly.
    runs_per_condition: 1
    interleaved: false
    operator: >-
      the BC-302 lane agent of agenda-030, bead think-qfog, session-104; the record was
      written by a separate record lane from the frozen result section
    commit: d04205fb
    dirty: false
    entry_point: >-
      the lane's cover_reader.py, with escape_engine.py, reader.py, variants.py,
      spotcheck.py and reader_sanity.py, whose full text is in lane E's "Appendix: scripts
      and data as run"
    command: >-
      from packing/, PACK_JOBS=1 uv run --frozen --all-extras --group dev python
      cover_reader.py set-S10-l0.1.json --exact for the certification of Theorem E.4, then
      python variants.py, python spotcheck.py and python reader_sanity.py, each taking the
      scratch directory as its one argument, for the other segment lengths, the fine spot
      check and the leaf sample; the scripts live in the session scratchpad and are
      reproduced verbatim in the result section's appendix, so the appendix is the artifact
      to re-run from, not a repository console script
    budget: >-
      the two research phases of session-104 — 30 minutes for the engine and its self-tests,
      90 for the candidates, the min-max and the reader — on one worker inside a 2.5-hour
      block clock, with the reader capped at a floor of 2·10⁻⁴ on the scaled half-widths and
      4·10⁶ nodes
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-e-ownership-set-at-q.md
  effort:
    timebox: 120m, the engine and search phases of session-104 inside its 150-minute block clock
    wall_seconds: 253.6
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Is there a set of at most eleven marks in the container of side 96/25 such that every
      contained closed unit square, at any angle, lies within 3/500 of one of them, with the
      cover certified rather than searched?
    outcome: criterion_met
    checked_by: >-
      cover_reader.py on set-S10-l0.1.json, the ten closed horizontal segments of length
      1/10 centred on Stromquist's Figure-13 points at 96/25. The adaptive cover of the pose
      space [0, 1] × [1/2, 96/25 − 1/2]² in (t, cx, cy) closed with 404 613 boxes, 184 756
      certified leaves, 17 551 discards and 0 failures at floor 2·10⁻⁴ in 8.0 s, every box
      certified against the frame threshold τ = 2121/500000 with an allowance of 10⁻⁹
      against an accumulated rounding error below 10⁻¹²; then every certified leaf and every
      discarded box was re-decided in fractions.Fraction with the rational τ and no
      allowance, 0 failures in 91.5 s. Since dist ≤ √2·max(f, 0) in the reader's frame norm,
      f ≤ τ gives distance at most √2·2121/500000 < 3/500. That is Theorem E.4: every closed
      unit square contained in [0, 96/25]², at any angle, is within √2·2121/500000 of one of
      the ten segments. The same certifies with the centre point added — 349 507 boxes,
      157 203 certified leaves, no failure, 8.3 s — and at segment length 9/100, 432 993
      boxes and 197 007 leaves, no failure, 10.2 s. Ten segments is at most eleven marks, so
      H-134's criterion is met in segment form.
  - shape: determination
    role: guard
    question: >-
      Did any declared falsifier occur — an exactly verified escape of a certified set, a
      box the reader could not certify at its floor, a certified leaf or discard the exact
      re-check rejects, or a sampled pose outside the tolerance?
    outcome: criterion_met
    checked_by: >-
      None on any set this record certifies. The falsifier found no escape of the ten
      segments at grid step 0.02 and angle step 1.5° (best float margin −0.006, best exact
      distance 0.00000); on the eleven-mark form it also found none at step 0.01 and 0.75°
      in 48 s and at 300 random contained poses, every one of them meeting a segment at
      exact distance 0. The reader reported 0 failures on the ten-segment set, on the
      eleven-mark set and at length 9/100. The exact re-check rejected no leaf and no
      discard. reader_sanity.py rebuilt the 184 756 leaves and drew 6 000 random poses
      inside 3 000 random leaves- 0 were outside 3/500 of every mark by the falsifier's exact
      distance, the largest least-distance lower bound seen being 0.002022. All six engine
      self-tests passed, and reader.py agreed with the engine on all 22 catalogued escapes.
  - shape: determination
    role: mechanism
    question: >-
      Does the point form of H-134 hold at 96/25 — is there a set of at most eleven points,
      thickened by 3/500, that every contained unit square meets?
    outcome: criterion_missed
    checked_by: >-
      Not established, and not refuted either. Thirteen point sets were decided negatively,
      each by an escape verified exactly and by two independent distance methods: T-018's
      eleven heaviest atoms scaled by 384/381 clear by 0.41449 (an axis square in the bare
      wall strip), the greedy cover of its 93 heaviest atoms by 0.06310, Stromquist's ten
      points and both eleven-point extensions of them by 0.03188 (a 45° square resting on a
      wall between two row points 0.92 apart, in four symmetric images that one added point
      cannot all kill), the polished K4-symmetric optimum of the adversarial min-max by
      0.01401, and the free 22-coordinate optimum from it by 0.01720. The independent reader
      agreed on all 22 catalogued escapes. The exact branch-and-bound that would refute the
      point form outright stayed alive — 28 rounds, 150 test squares, node count equal to
      tests plus one at every round — and was stopped, so no refutation of the point form is
      claimed: a surviving branch is not evidence either way.
  - shape: determination
    role: mechanism
    question: >-
      How short may the segments be before the cover fails, and what closes the gap that
      points cannot?
    outcome: criterion_met
    checked_by: >-
      The threshold lies in (7/100, 9/100]. Length 9/100 certifies; at 8/100 the reader left
      3 626 boxes uncertified at its floor with the falsifier's best pose at exact distance
      0.00409, inside the tolerance but not certified, so that length is unresolved; at 7/100
      and 6/100 the 45° square at the top wall is an exact escape again, clearing every mark
      by 0.00763 and 0.01116. The mechanism is a chord: a 45° square resting on a wall cuts
      a row line in a chord of half-length √2 − 1 = 0.4142 and clears the row's points by
      0.0319, while a segment of half-length 1/20 reaches 0.0354 along the diagonal towards
      it. That 0.0035 is the whole difference between 1/10 and 7/100, and it is why the marks
      that work are Stromquist's rows thickened along themselves and not the certificate's
      heavy atoms.
  verdict:
    decision: accepted
    primary_criterion: >-
      a set of at most eleven marks at side 96/25, thickened by 3/500, whose cover of every
      contained closed unit square at every angle is certified rather than searched
    reason: >-
      H-134's criterion is met in segment form: ten horizontal segments of length 1/10 on
      Stromquist's rows cover the whole pose space at tolerance 3/500, certified by an
      interval reader with every certified leaf and every discarded box re-decided in exact
      rational arithmetic and no failure, so every square of every packing of eleven unit
      squares at any side up to 96/25 is within 3/500 of a known mark; the point form of the
      same claim is untouched by this and stays open with thirteen candidate sets refuted.
    commit: d04205fb
    needs_review: true
---
# exp-132 — Ten Short Segments, and Every Square Within `3/500` of One

[H-134](../../../hypotheses/H-134-eleven-mark-ownership-set.md) asked whether the
mechanism that finishes Stromquist’s `n = 10` proof survives at the target side: is
there a set of at most eleven marks in `[0, 96/25]²`, thickened by the transfer
tolerance `δ = 3/500`, that every contained unit square at every angle must meet?
Lane BC-302 of
[agenda 030](../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-qfog`, spent
[session-104](../../../agent-sessions/session-104-ownership-set-at-q.md) on it and froze
one claim, Theorem E.4. This record registers it.
Every figure below is read from
[lane E’s report](../results/agenda-030/lane-e-ownership-set-at-q.md), which holds the
catalogue, the reader’s soundness argument, and the scripts and outputs as run.

## What was tested, and what would have refuted it

A *mark* is a point or a closed segment; a contained closed unit square `Q` *meets* the
mark `m` when `dist(Q, m) ≤ δ`, and an *escape* of a mark set is a contained closed unit
square at some angle that clears every mark by more than `δ`. Thickening is on the
hypothesis’s side — it enlarges every mark, making the cover easier and the escape
harder — so an escape is a real refutation of a candidate set and a cover is a real
statement about unit squares at any side up to `96/25`.

The falsifiers were fixed before the runs.
**Of a candidate set: a contained unit square at a rational pose with exact distance
`> 3/500` to every mark, decided by two independent exact formulas that must agree.
Of a survivor’s proof: a box of pose space the reader cannot certify at its floor, a
certified leaf the exact re-check rejects, or an error in the Lipschitz bound.** Neither
occurred on any set this record certifies; the first occurred on every point set tested,
which is the negative half of the round.

A “no escape found” is a search reading at its stated resolution and never a theorem.
That distinction does the work here: the falsifier reads that every contained square
*actually meets* a segment at distance `0`, and that reading is **not** proved and
cannot be by this reader, whose slack at a tangency is zero.
What is proved is the thickened statement, which is the one H-134 asked for.

## Inputs, fixed for every run

Side `q = 96/25`, container `S = [0, q]²`, tolerance `δ = 3/500`. Poses are
`(cx, cy, t)` with `t = tan(θ/2)` rational — exp-121’s frame, reused unchanged, along
with its closed membership and support-width containment tests.
The certified set is the ten closed horizontal segments of length `1/10` centred on
Stromquist’s Figure-13 points scaled to `q`, exactly
`{(1, 1), (48/25, 1), (71/25, 1), (27/50, 48/25), (73/50, 48/25), (119/50, 48/25),
(33/10, 48/25), (1, 71/25), (48/25, 71/25), (71/25, 71/25)}`, held as exact rationals in
`set-S10-l0.1.json`; the eleven-mark variant adds the centre `(48/25, 48/25)`. The
reader covers `[0, 1] × [1/2, q − 1/2]²`, which is every orientation modulo a quarter
turn and every centre a contained square can have, with floor `2·10⁻⁴` on the scaled
half-widths, node limit `4·10⁶`, frame threshold `τ = 2121/500000` and float allowance
`10⁻⁹`. The falsifier ran at grid step `0.02` and angle step `1.5°` for every row, with
the forty best grid poses refined by Nelder–Mead and rationalised at denominators `10³`
to `10⁶`. The candidate point sets take T-018’s atoms scaled from `381/100` to `q` by
`384/381`.

## The theorem, and exactly what certifies it

> **Theorem E.4.** Let `M₁₀` be the ten closed horizontal segments of length `1/10`
> centred at Stromquist’s Figure-13 points in `S = [0, 96/25]²`. Every closed unit
> square contained in `S`, at any angle, is at Euclidean distance at most
> `√2·2121/500000 <
> 3/500` from some segment of `M₁₀`.

The reader proves it by an adaptive cover of pose space.
For a point `p` at coordinates `(u, v)` in the square’s frame,
`f(P, p) = max(|u| − ½, |v| − ½)` satisfies `dist(Q(P), p)² ≤ 2·max(f, 0)²`, so `f ≤ τ`
gives `dist ≤ √2·τ < δ`; for a segment the minimum of `f` along it is attained at an
endpoint or at one of the three breakpoints `u = 0`, `v = 0`, `u = ±v`, each the root of
an affine equation. Over a box of half-widths `(ht, hx, hy)` about `P₀`,
`f(P, p) ≤ f(P₀, p) + hx + hy + 2·ht·(R + hx + hy)` with `R` the `L1` distance from the
box centre, because the centre moves by at most `hx + hy` and the frame vectors by at
most `2·ht`; a box is certified when that bound is at most `τ`, and discarded only when
it contains no contained pose at all, decided from the least half-width over its
`t`-range since `w` is unimodal on `[0, 1]`.

On `set-S10-l0.1.json` the cover closed with **404 613 boxes, 184 756 certified leaves,
17 551 discards and no failure**, in `8.0 s`. The certification is floating point with
an explicit `10⁻⁹` allowance against an accumulated error below `10⁻¹²`, four orders of
magnitude inside it — and that is not what the theorem rests on: **every certified leaf
and every discarded box was re-decided in `fractions.Fraction` with the rational `τ` and
no allowance, and none failed**, in `91.5 s`. The same set with the centre point added
certifies (`349 507` boxes, `157 203` leaves, no failure, `8.3 s`), and so does segment
length `9/100` (`432 993` boxes, `197 007` leaves, no failure, `10.2 s`).

Ten segments is at most eleven marks, so H-134’s criterion is met — in segment form.

## Where the threshold is, and why a segment beats a point

| Segment length | Falsifier at step `0.02`, `1.5°` | Reader |
| --- | --- | --- |
| `1/10`, ten segments | no escape; best exact distance `0.00000` | `404 613` boxes, `184 756` leaves, `0` failures — **certified** |
| `1/10`, plus the centre | no escape; also none at `0.01`, `0.75°` and at 300 random poses | `349 507`, `157 203`, `0` — **certified** |
| `9/100`, plus the centre | no escape; best pose at distance `0.00056` | `432 993`, `197 007`, `0` — **certified** |
| `8/100`, plus the centre | no escape; best pose at distance `0.00409 < δ` | `659 921`, `292 913`, **`3 626` failures at the floor** — unresolved |
| `7/100`, plus the centre | **escape**, clearance `0.00763` | — |
| `6/100`, plus the centre | **escape**, clearance `0.01116` | — |

So the threshold lies in `(7/100, 9/100]`, and `8/100` is neither certified nor refuted:
the reader’s floor was too coarse for a slack of `0.002`, and a finer floor was not run.

The mechanism is a chord.
A `45°` square resting on a wall cuts a row line in a chord of half-length
`√2 − 1 = 0.4142` and clears the row’s points by `0.0319`, while a segment of
half-length `1/20` reaches `0.0354` along that diagonal.
The `0.0035` between those is the whole difference between length `1/10` and `7/100` —
and it is why the marks that work are Stromquist’s three rows thickened along themselves
rather than anything drawn from the certificate.

## The point form, which stays open

Thirteen point sets were decided negatively, each by an escape verified exactly and by
two independent distance methods, and every catalogued escape was re-read by an
independent standard-library reader with no disagreement.

| Point set | Marks | Least exact clearance of its escape |
| --- | --- | --- |
| T-018’s eleven heaviest atoms scaled by `384/381` | 11 | `0.41449` |
| Greedy cover from its 93 heaviest atoms | 11 | `0.06310` |
| Stromquist’s ten points; the same plus the centre; the same plus one min–max point | 10, 11, 11 | `0.03188` |
| The polished K4-symmetric optimum of the adversarial min–max | 11 | `0.01401` |
| The free 22-coordinate optimum from it | 11 | `0.01720` |

T-018’s heavy atoms are corner and centre atoms and leave the wall strips bare; the best
point sets found are `0.008` short of the tolerance at the search resolution.
The exact branch-and-bound that would refute the point form outright — a sound
relaxation over octagonal `δ`-neighbourhoods with exact polygon clipping — stayed alive
through 28 rounds and 150 test squares and was stopped, its candidate generator being
too weak to drive the finite family towards infeasibility.
**A surviving branch is not evidence for the point form.** It is neither established nor
refuted, and the escape catalogue is the obstruction the closing route inherits.

Three structural facts were proved alongside, and they bound what any future attempt can
do. No LP, pigeonhole or counting argument can refute H-134, because T-018 scaled by
`384/381` is a fractional cover of mass `434547/40000 = 10.863675 < 11` for `δ`-rounded
unit squares at `q`. Ten marks of any robustly unavoidable set are localised to the
`δ`-neighbourhoods of the ten squares of the `n = 10` optimal packing scaled to `q`, and
no eleven such squares exist — so an eleven-mark set is ten localised marks plus one
free mark, and a ten-mark set is entirely localised.
No `D4`-symmetric eleven-set exists, and every `K4`- or `C2`-symmetric one contains the
centre.

## What it buys

In any packing of eleven unit squares in `S`, every square is within `δ` of one of ten
known segments, all lying on the three rows `y = 1, 48/25, 71/25`; and since a packing
at any side `s ≤ q` dilates into `S`, that holds for every side up to `96/25` with no
further tolerance. This is the localisation X-021 priced: route (a)’s tree branches over
about `10⁴⁰` feature selections without it, and with it the branching over which mark
each square sits near is at most `10¹¹` labelled choices before symmetry and exclusion.

It is **not** ownership.
Eleven squares against ten marks force one mark to serve two squares, and a segment can
be shared by two squares touching along a line that crosses it, so the pigeonhole that
finishes the `n = 10` proof does not apply and nothing here says eleven unit squares do
not fit at `96/25`. The eleventh mark H-134 allows is free; whether it can be placed to
restore an ownership argument is a question for the closing route.

## Limits

- **The proof is a computation, not a hand proof.** Stromquist’s Lemmas 1–4 were not
  used and not needed.
  Theorem E.4 rests on the Lipschitz bound above and on a cover whose every leaf and
  every discard was re-decided exactly; the record for it is the reader, its allowance,
  and the re-check, all reproduced in the lane’s appendix.
- **The independent replay is the pending factual review, and this round is filed with
  `needs_review` set for it.** A second reader with a different bound — the Hausdorff
  one on the Euclidean distance itself, `cover_reader2.py` — was written and did **not**
  finish: its float cover ran out of two bounded runs of `9` and `7` minutes at load
  `10` to `14`, and the exact pass it started was stopped after ten minutes.
  Until it or another independent reader replays the cover, the ledger holds H-134 at
  *needs review* rather than confirmed, which is the standard the lane itself asked for.
- **What is certified and what is only a search reading.** Certified: the cover at
  segment length `1/10` (ten marks and eleven), and at `9/100`. A search reading only:
  that every contained square actually *meets* a segment at distance `0`; that no escape
  exists at length `8/100`; that no eleven-point set works, which is thirteen refuted
  sets and a live branch-and-bound, not a theorem.
- **Wall times are not comparable.** Four cores shared with seven other agents at load
  average `4` to `14`, one worker per job.
  The declared `253.6` seconds is the sum of the segment-form measurements this record
  registers — the falsifier and reader rows of `variants.log`, the certification run’s
  float cover and exact re-check, the leaf sanity sample and the fine `0.01`/`0.75°`
  spot check — and nothing else; the point-set catalogue, the min–max and the
  branch-and-bound are reported here as context and their time is not counted in it.
- **Nothing about a packing bound.** The theorem localises the squares of a hypothetical
  packing of eleven. It establishes no side, and no result is written to the frontier
  register.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
