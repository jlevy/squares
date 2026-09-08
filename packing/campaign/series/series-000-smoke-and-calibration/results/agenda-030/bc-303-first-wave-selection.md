# Agenda 030, BC-303: Independent replays of the first wave, and the selection

Retained record for BC-303 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-znzj`, session-107, 2026-09-08, one 2.5-hour block from 15:34Z on one worker of
a four-core machine shared with two other lanes (load average 0.1 to 1.7 beside every
wall time below). The cell asks which first-wave results earn the next sustained block
and what the strongest claim to freeze is.
Independent review here means each lane’s strongest claim was replayed with a reader
written from the statement alone, not by re-running the lane’s script; only exact
decisions count, and every float agreement is context.
Nothing here allocates an identifier, edits a hypothesis or a registry, or extends a
clock.

## 0. Verdicts in one page

| Lane, claim | My replay | Verdict |
| --- | --- | --- |
| E (session-104), Theorem E.4: the ten horizontal segments of length `1/10` centred on Stromquist’s Figure-13 points at `96/25` are robustly unavoidable at tolerance `3/500`, and at the sharper `√2·2121/500000` | a new interval reader over a symmetry-reduced pose space with a rigid-motion Lipschitz bound on the *signed* Euclidean distance; every certified leaf and every discard re-decided in `Fraction`; the cover’s volume identity checked exactly | **agrees**, at both constants, with 24,381 boxes and 10,960 certified leaves (the lane needed 404,613 and 184,756); also decides the `9/100` set and the `8/100` set the lane left unresolved, and finds exact escapes at `7/100` as the lane did |
| C (session-101), the four-corner pair containment theorem at `96/25` | `sqpack.fractional.certificate.verify` on the exported free measure, then the ownership step re-derived from the mass gap and exact distances | **agrees**: mass `22524199/2000000`, valid, margin `441/125000` |
| B (session-102, exp-130), Theorem C: `[0°, 10.3875°] ∪ [43.0737°, 45°]` excluded at `96/25` on grid 119 | the site set rebuilt, the class program proposed and decided by `decide_class_program` through my own driver | THEOREM-C-VERDICT |

Two disagreements with the lanes’ own readings are recorded in Section 4: the segment
length threshold is in `(7/100, 8/100]`, not `(7/100, 9/100]`, and lane E’s certified
domain misses a measure-zero sliver at the far walls that its stated constant does not
strictly absorb (mine closes it).
The selection (Section 5) funds the segment cover toward an ownership argument as the
next sustained block and the `B = 1` depth polisher as the efficiency block, and
recommends against funding the band ladder, the corner-pair anchored certificate and
the plateau’s full-dual pricing as blocks of their own.
The strongest claim to freeze is Theorem E.4 with its exact statement in Section 6.

## 1. Falsifiers, stated before each replay

Written in the lane checkpoint file before any run.

1. **Theorem E.4.** A closed unit square contained in `[0, 96/25]²` whose exact
   Euclidean distance to every one of the ten segments `[x − 1/20, x + 1/20] × {y}`,
   `(x, y) ∈ P10`, exceeds `3/500`, decided in `Fraction` arithmetic by a convex-polygon
   distance (an intersection test, then vertex-to-edge minima). A box my reader cannot
   certify is not a falsifier until its centre pose is decided exactly as an escape; an
   uncertified box with no exact escape is unresolved scope.
   Secondary falsifiers: a leaf my exact re-check rejects, or leaves and discards whose
   volumes do not sum to the domain’s.
2. **Corner-pair theorem.** `verify` reports a mass other than `22524199/2000000` or any
   of Conditions 1, 3, 4, 5 failing; the eight pair atoms absent or lighter than
   `106251/800000`; a per-corner pair mass at most `ε = M − 11`; or a least squared
   distance between marks of different corners at most `2B²`.
3. **Theorem C.** `decide_class_program` on the rationalised point reached from grid
   119, cells `0–39 ∪ 172–180`, composition `(11, 0)`, thresholds `(1, 0)`, reports
   Condition 2′ or 5′ failing, or the folded range of the cells differs from
   `[0°, 10.3875°] ∪ [43.0737°, 45°]`. Equality of the exact mass with `11083/1024` is
   context: the LP path may reach a different rationalised point.

## 2. Replay of Theorem E.4 (lane E)

### 2.1 The statement replayed

`q = 96/25`, `S = [0, q]²`, `δ = 3/500`. `P10` is Stromquist’s Figure-13 set at `q`,
which I recomputed from his formulas (`U = 3/2 − q/4 = 27/50`, `V = 1/2 + q/4 = 73/50`,
`C = q/2 = 48/25`) rather than copying the lane’s list: `(1, 1)`, `(48/25, 1)`,
`(71/25, 1)`, `(27/50, 48/25)`, `(73/50, 48/25)`, `(119/50, 48/25)`, `(33/10, 48/25)`,
`(1, 71/25)`, `(48/25, 71/25)`, `(71/25, 71/25)`. `M₁₀` is the ten closed horizontal
segments of length `1/10` centred on them.
Claim: every closed unit square contained in `S`, at any angle, is within `δ` of some
segment of `M₁₀`; the lane’s theorem states the sharper constant `√2·2121/500000`.

### 2.2 The reader, written from the statement

`e4_reader.py` (Appendix) is not a variant of the lane’s `cover_reader.py`, which I read
only after this design was fixed and run (Section 2.5 compares them).

- **Pose space and symmetry.** A pose is `(t, cx, cy)` with `t = tan(θ/2)`, the square’s
  frame `(cos θ, sin θ) = ((1 − t²)/(1 + t²), 2t/(1 + t²))`. The segment set is
  invariant under `x → q − x` and `y → q − y` (its rows are `y = 1, 48/25, 71/25` and its
  columns are symmetric about `48/25`) but not under `x ↔ y`, so its symmetry group is the
  rectangle’s. The half-turn keeps `θ` and maps `cy → q − cy`, so poses with `cy ≤ q/2`
  suffice; then `x → q − x` keeps `cy` and maps a square at angle `θ` to one at
  `π/2 − θ`, so `θ ∈ [0, π/4]` suffices.
  The domain is `t ∈ [0, 27/64] ⊃ [0, √2 − 1]`, `cx ∈ [1/2, 7/2] ⊃ [1/2, q − 1/2]`,
  `cy ∈ [1/2, 2] ⊃ [1/2, q/2]`, with dyadic bounds so that every box of the bisection
  tree is an exact float and an exact `Fraction`, and the over-covered part is removed by
  the discard rule.
- **The bound.** Let `g(P, m)` be the signed Euclidean distance from the closed square
  `Q(P)` to segment `m`: the distance when they are disjoint, minus the greatest
  penetration depth of a point of `m` in `Q(P)` when they meet.
  For the rigid motion `φ` carrying `Q(P₀)` to `Q(P)`, every point of `Q(P₀)` moves by at
  most `h = |c − c₀| + (√2/2)|θ − θ₀|`, so a nearest point of `Q(P₀)` to `m` has an image
  in `Q(P)` within `h` of it, and a ball of radius `d` inside `Q(P₀)` about `p ∈ m` has as
  image a ball of radius `d` inside `Q(P)` about a point within `h` of `p`; in both
  regimes `g(P, m) ≤ g(P₀, m) + h`. Over a box with half-widths `(ht, hx, hy)` about its
  centre `P₀`, `|c − c₀| ≤ √(hx² + hy²)` and `|θ − θ₀| = 2|atan t − atan t₀| ≤
  2·ht/(1 + t₁t₀)` from `atan x ≤ x`. A box is **certified** when
  `min_m g(P₀, m) + √(hx² + hy²) + √2·ht/(1 + t₁t₀) ≤ δ` (with `√2 ≤ 665857/470832` in
  both stages and a `10⁻⁹` allowance in the float stage), **discarded** when it holds no
  contained pose (`x₂ < w_min` or `x₁ > q − w_min`, likewise in `y`, `w_min =
  min(w(t₁), w(t₂))` since `w = (cos θ + sin θ)/2` is unimodal), and otherwise split
  along the largest of `hx`, `hy`, `√2·ht`. A box whose scaled half-widths are all below
  the floor `2⁻¹⁴` and which is neither is a failure, and its centre pose is then decided
  exactly by the falsifier’s polygon distance.
- **The segment minimum.** `g(P₀, ·)` restricted to a segment is a convex function of the
  segment parameter; the float stage evaluates it at the analytic candidates (the
  endpoints, `u = 0`, `v = 0`, `|u| = |v|`, `|u| = 1/2`, `|v| = 1/2`, and the stationary
  points of the four corner pieces) and records the minimiser `s*` and the segment.
  Self-test 1 checks the candidate minimum against a 2001-point sampling of every segment
  at 400 random poses (worst discrepancy `1.1·10⁻¹⁶`); self-test 2 checks the float
  signed distance against the exact polygon distance at 60 random rational poses (no
  mismatch).
- **The exact stage.** Every certified leaf is re-decided in `Fraction`: `g` is evaluated
  at the recorded rational `s*`, which bounds the true segment minimum from above
  whatever the float search did, so soundness never rests on the float minimiser; the
  irrational terms enter only through rational upper bounds (`√2` by the convergent,
  `√(hx² + hy²)` by an integer square root plus one at `2⁻⁴⁰`); the inequality is
  `val + h ≤ δ` when `s*` is inside the square and `val ≤ (δ − h)²` with `δ ≥ h` when
  outside. Every discard is re-decided exactly, and the volumes of leaves, discards and
  failures are summed exactly against the domain’s.
  The lane’s constant is handled as `dist² ≤ 2·(2121/500000)²`.

### 2.3 Inputs

| Input | Value |
| --- | --- |
| Marks | `P10` as above; segments `[x − ℓ/2, x + ℓ/2] × {y}` with `ℓ ∈ {1/10, 9/100, 8/100, 7/100}` |
| Tolerance | `3/500`; and, for `ℓ = 1/10`, `√2·2121/500000` |
| Domain | `t ∈ [0, 27/64]`, `cx ∈ [1/2, 7/2]`, `cy ∈ [1/2, 2]`; volume `243/128` |
| Floor, allowance, node budget | `2⁻¹⁴` on the scaled half-widths; `10⁻⁹`; `1.2·10⁷` nodes |
| Split rule | the largest of `hx`, `hy`, `√2·ht`, bisected |
| Arithmetic | IEEE doubles vectorised in numpy for the cover; `fractions.Fraction` for every leaf, discard, escape and the volume identity |
| Seeds | `numpy.random.default_rng(303)` for the self-tests only; the cover is deterministic |
| Machine | one process, `PACK_JOBS=1`, one BLAS thread; load average beside each wall time |

### 2.4 Results, exact

| Set | Nodes | Certified leaves | Discards | Floor boxes | Exact re-check | Volume | Wall (float, exact), load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ℓ = 1/10`, `δ = 3/500` | 24,381 | 10,960 | 1,231 | 0 | 0 leaves rejected, 0 discards rejected | `243/128` exact | 0.2 s, 0.5 s; 0.95 |
| `ℓ = 1/10`, `√2·2121/500000` | 24,381 | 10,960 | 1,231 | 0 | 0, 0 | exact | 0.2 s, 0.5 s; 0.95 |
| `ℓ = 9/100`, `3/500` | 29,939 | 13,556 | 1,414 | 0 | 0, 0 | exact | 0.4 s, 0.6 s; 0.95 |
| `ℓ = 8/100`, `3/500` | 39,515 | 18,004 | 1,754 | 0 | 0, 0 | exact | 0.5 s, 0.8 s; 0.95 |
| `ℓ = 7/100`, `3/500` | 3,291,749 | 187,496 | 53,159 | 1,405,220 | 0, 0 | exact | 39.6 s, 10.2 s; 1.5 |

At `ℓ = 7/100` the reader does what a reader must when the claim is false: 162 of the
first 200 floor-box centres are exact escapes by the polygon distance, for instance
`t = 384507/1048576`, `cx = 156707/65536`, `cy = 46211/65536` (a square at about
`40.2°` resting near the bottom wall) at distance `0.006365 > 3/500`.

**Verdict on E.4: agrees.** The ten segments of length `1/10` are robustly unavoidable
at `3/500`, and at the lane’s sharper constant, on a domain that covers every contained
pose with no failure; the same holds at `9/100`, as the lane found, and at `8/100`,
which the lane’s reader left with 3,626 boxes at its floor.
The pose the lane’s reader certified that mine refutes: none.

The first version of my exact stage used `√2 ≤ 14143/10000` and rejected one leaf at the
lane’s constant (float margin `7·10⁻⁸` against the bound’s `2.7·10⁻⁷` of slack) and nine
at `ℓ = 7/100`; that is a mismatch between two conservative stages, not an unsoundness
(a rejected leaf is simply not certified), and disappears when both stages use one
convergent. It is recorded because it is the kind of thing a second reader is for.

### 2.5 Comparison with the lane’s reader, after the fact

The lane’s `cover_reader.py` certifies `f = max(|u| − 1/2, |v| − 1/2) ≤ τ = 2121/500000`
in the square’s frame with the bound `f(P, p) ≤ f(P₀, p) + hx + hy + 2·ht·(R + hx + hy)`,
`R` the larger endpoint’s `L¹` distance; I checked that bound line by line and it is
sound, and its breakpoint set (`u = 0`, `v = 0`, `u = ±v`) is complete for the
piecewise-linear `f`. The two readers differ in the domain (mine is `4.8×` smaller by the
two symmetries), in the target (`δ` on the Euclidean distance against `δ/√2` on the
frame distance) and in the constant, which together account for the `40×` difference in
box count.
One defect: the lane’s tree domain is `[0.5, Q − 0.5]` computed in floats, and
`float(3.84) − 0.5 = 3.33999…986 < 3.34`, so its cover misses the poses with `cx` or
`cy` in `(3.34 − 1.4·10⁻¹⁶, 3.34]`, the axis square flush against a far wall among them.
At `3/500` the gap is harmless (`f` is 1-Lipschitz in the centre, and the stated constant
leaves `9·10⁻⁷` of room); for the constant `√2·2121/500000` as literally stated it is a
measure-zero hole, which the dyadic domain here closes.

## 3. Replay of the corner-pair theorem (lane C)

`corner_pair_replay.py` (Appendix) loads
[`bc-293-measure-free-96-25.json`](bc-293-measure-free-96-25.json) into a
`sqpack.fractional.certificate.Certificate` and runs the library’s `verify(workers=1)`,
then re-derives the ownership step.

| Step | Exact reading |
| --- | --- |
| Inputs | `n = 11`, `L = 96/25`, `B = 9977/10000`, 377 atoms, the 181-direction net (`D = 207107/90000000`) |
| Mass | `22524199/2000000 = 11.2620995`, equal to the claimed fraction |
| Conditions | 1 (D4 closure of 377 atoms) holds; 3 holds (`t² + 2t − 1 = 309449/250000000000 ≥ 0`); 4 holds (`B(1 + D) = 899996306539/900000000000 < 1`); 5 holds, least cell `800003/800000` at direction 0; 2 fails at mass `11.262 > 11`, as expected of a non-certificate |
| Sweep wall | 14.9 s at load 1.65 |
| `ε = M − 11` | `524199/2000000 = 0.2620995` |
| Pair orbit | eight atoms, the D4 orbit of `(3152/3175, 2336/3175)`, each of weight `106251/800000` |
| Per-corner pair mass | `106251/400000 = 0.2656275`, exceeding `ε` by `441/125000 = 0.003528` at every corner |
| Cross-corner distance | least squared distance between marks of different corners `34668544/10080625 ≈ 1.8545²`, against `2B² = 99540529/50000000 ≈ 1.4110²` |
| Within a corner | the two marks are `√(1331712/10080625) ≈ 0.3635` apart, so one core can hold both, which is why the pair and not a mark is the anchor |

The argument needs exactly three facts and no more: a valid measure of mass `11 + ε`
(so the eleven pairwise disjoint cores of a packing, each of mass at least one by
Condition 5, leave at most `ε` outside them); a set of atoms of mass above `ε` per
corner (so one of its atoms is in some core); and a cross-corner distance above the
core’s diameter `B√2` (so no core holds atoms of two corners).
Nothing about the bound, the column settlement or the floor enters.

**Verdict: agrees.** Every packing of eleven unit squares in `[0, 96/25]²` has four
distinct squares, one per corner, each containing in its interior at least one of its
corner’s two marks `(3152/3175, 2336/3175)` and `(2336/3175, 3152/3175)` (and their
images under the container’s symmetries).
Since `[0, s]² ⊂ [0, 96/25]²`, the same holds of every packing at side at most `96/25`
read in the `96/25` frame.

## 4. Replay of Theorem C (lane B, exp-130)

THEOREM-C-SECTION

## 5. Disagreements with the lanes’ own readings

- **Lane E, the threshold in the segment length.** The lane places it in
  `(7/100, 9/100]` because its reader left `8/100` at the floor.
  My reader decides `8/100` with no failure, so the threshold is in `(7/100, 8/100]`.
  The lane read its `8/100` result as needing a finer floor; what it needed was a smaller
  Lipschitz constant, since at the lane’s floor the bound’s own slack, not the floor,
  was the limit.
- **Lane E, the certified domain.** The far-wall sliver of Section 2.5. Harmless for the
  H-134 statement at `3/500`, a literal gap for the theorem’s sharper constant, closed
  here.
- **Lane C, what to run next.** Lane C asks for phase G (the pair orbit priced) to widen
  the margin `441/125000`. The theorem does not change with the margin, and what is
  unmeasured is not the margin but the value of the anchor to a certificate, which by
  X-021’s duality lemma is bounded by the restricted fractional packing value that BC-294
  left undecided. The measurement should come before the anchored certificate.
- **Lane B, the ladder as a block.** Lane B’s first recommendation is to continue the end
  band at grids 119 and 159 from `(13, 13)` and `(40, 10)`. The registered band already
  clears H-130’s bar four times over, every further rung is a property of the site set as
  much as of the side, and a point costs ten minutes; this is queue filler under OR-3,
  not a sustained block.
- **The composition route.** BC-303’s exit asks for the branch list for geometric
  conditioning if the composition route ended. BC-296 did not run in the first wave, so
  the route has not ended and no branch list exists; it stays ready.

## 6. The selection

The candidates the cell names, ranked by what a block would buy toward a global
exclusion at `96/25` against what it costs, with the replays above as the evidence.

1. **Fund: the segment-mark cover toward an ownership argument and route (a)**
   (BC-302’s follow-up, bead `think-qfog`), as the next sustained block. It is the only
   first-wave result that is proved, independently replayed, and *strengthened* by the
   replay: the reader here decides a mark set in under a second and a false one in under
   a minute, so a block can run hundreds of exact decisions where the lane ran five.
   It is also the ambitious tier’s only positive path in the agenda’s own words, and the
   replayed facts now give it a branch structure: every square of a packing is within
   `3/500` of one of ten short segments on three rows, so by pigeonhole some segment
   serves two squares; the corner-pair theorem names four of the eleven squares; Theorem
   C forces a square with folded angle in `(10.3875°, 43.0737°)`. Accept rule for the
   block: an exact-decided theorem beyond localisation — a mark set of at most eleven
   marks with the shared configurations confined to a named pattern (two squares within
   `δ` of one segment must touch along its line, or the like), or the exact threshold
   length, each certified by an interval reader with its exact re-check and a second
   reader; a float non-escape is never a result.
   First tasks: register the second reader of this record beside the lane’s; decide
   whether the free eleventh mark can be placed so that some sharing pattern is
   impossible; cost the case split that E.4, the corner pair and Theorem C define.
2. **Fund as the efficiency block (OR-12): the `B = 1` depth polisher** (BC-294’s
   follow-up, bead `think-7lp3`). `ν*₁(q)` is X-021’s decisive unmeasured number and the
   first wave located the loss in the instrument (depth scaling, not the LP); a polisher
   on the fixed support is a bounded instrument change with a kill test as its accept
   rule: a family verified by `verify_ceiling` at `96/25` of value at least eleven with a
   unit of weight outside Trump’s neighbourhood decides the ambitious tier negatively;
   a converged covering LP below eleven at `B = 1` moves H-129; anything in between is
   recorded with its bytes. The plateau’s full-dual pricing (lane F’s one-line
   `support_cap` diagnostic, about thirty minutes) rides inside this block as its first
   task, since it tells whether the instrument’s stops are the cap’s.
3. **Retain, do not fund as a block: the band ladder at grids 119 and 159.** Run it as
   filler beside the funded blocks; freeze the widest success when it appears.
4. **Retain, defer: the corner-pair anchors for BC-299’s conditional certificate.** The
   anchors are proved and replayed and stay the input BC-299 asked for, but a
   conditional certificate’s value is bounded by the restricted fractional packing value
   (X-021, Lemma D), which is undecided; the polisher block measures it first.
5. **Fold in, do not fund: the plateau’s full-dual pricing.** Diagnostic, cheap, and
   unable to produce a certificate below eleven at `191/50` on its own (H-133 refuted as
   stated); it is task one of the efficiency block.

Dispositions of the first-wave hypotheses, as recommendations to the coordinator: H-134
accepted for the segment form (now independently replayed), open for the point form;
H-128 rejected at `96/25` on the retained shrink and net, with the corner-pair theorem
retained as its proved by-product; H-130 confirmed (exp-130); H-131 confirmed (exp-131);
H-129 open; H-133 refuted as stated; H-127 and H-132 untested (BC-292 and BC-298 did not
run).

## 7. The strongest claim to freeze

Theorem E.4, in this exact form, with two independent readers agreeing (the lane’s
`cover_reader.py` and `e4_reader.py` here):

> **Theorem (segment localisation at `96/25`).** Let `q = 96/25` and let `M₁₀` be the ten
> closed horizontal segments `[x − 1/20, x + 1/20] × {y}` for `(x, y)` in
> `{(1, 1), (48/25, 1), (71/25, 1), (27/50, 48/25), (73/50, 48/25), (119/50, 48/25),
> (33/10, 48/25), (1, 71/25), (48/25, 71/25), (71/25, 71/25)}`. Every closed unit square
> contained in `[0, q]²`, at any angle, is at Euclidean distance at most
> `√2·2121/500000 < 3/500` from some segment of `M₁₀`. Consequently every square of every
> packing of eleven unit squares at side at most `96/25` is within `3/500` of one of
> these ten segments, and some segment is within `3/500` of two of them.

The same statement holds with the segments shortened to `9/100` (both readers) and to
`8/100` (this reader only, so that companion is certified but not yet independently
replayed). It needs an experiment id, the lane’s `set-S10-l0.1.json` and both readers as
its record, and no registry entry beyond that: it changes no bound on `s(11)`.

The corner-pair theorem (Section 3) is the second claim worth freezing, with the
exported measure as its whole record; it is cheaper to register than E.4 and should be.

## 8. What remains, and what this block could not do

- Theorem C’s replay is the one computation whose wall time is set by the LP row loop;
  its outcome is in Section 4.
- The `8/100` companion has one reader; a second reader of a different design (the
  lane’s, run at a finer floor, or a third) would freeze it.
- No pose the lane certified was refuted, and no falsifier of any of the three claims
  occurred.
- Not done: any new mathematics on the ownership question, any run of the polisher, the
  registrations themselves (the coordinator’s, with the ids), and the document-map row,
  close report, ledger and synopsis re-renders that the record gate will name.

## Appendix: scripts as run

All scripts ran from the worktree’s `packing/` as
`PACK_JOBS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 uv run --frozen --all-extras
--group dev python <script> ...` under the project’s Python 3.14; none modifies the
repository.

### `e4_reader.py`

```text
E4-READER-SOURCE
```

### `corner_pair_replay.py`

```text
CORNER-PAIR-SOURCE
```

### `theorem_c_replay.py`

```text
THEOREM-C-SOURCE
```

### `corner-pair.out`

```text
CORNER-PAIR-OUT
```

### `theorem-c-g119.out`

```text
THEOREM-C-OUT
```

### `summary-*.json` of the E.4 reader

```text
E4-SUMMARIES
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
