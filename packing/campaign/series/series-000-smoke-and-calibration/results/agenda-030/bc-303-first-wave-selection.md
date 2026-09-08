# Agenda 030, BC-303: Independent replays of the first wave, and the selection

Retained record for BC-303 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), bead
`think-znzj`, session-107, 2026-09-08, one 2.5-hour block from 15:34Z on one worker of a
four-core machine shared with two other lanes (load average 0.1 to 1.7 beside every wall
time below). The cell asks which first-wave results earn the next sustained block and
what the strongest claim to freeze is.
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
| B (session-102, exp-130), Theorem C: `[0°, 10.3875°] ∪ [43.0737°, 45°]` excluded at `96/25` on grid 119 | the site set rebuilt, the class program proposed and decided by `decide_class_program` through my own driver | **agrees**, and reaches the lane’s rationalised point to the fraction: mass `11083/1024` over 296 atoms, least core `4101/4096`, all conditions holding |

Two disagreements with the lanes’ own readings are recorded in Section 5: the segment
length threshold is in `(7/100, 8/100]`, not `(7/100, 9/100]`, and lane E’s certified
domain misses a measure-zero sliver at the far walls that its stated constant does not
strictly absorb (mine closes it).
The selection (Section 6) funds the segment cover toward an ownership argument as the
next sustained block and the `B = 1` depth polisher as the efficiency block, and
recommends against funding the band ladder, the corner-pair anchored certificate and the
plateau’s full-dual pricing as blocks of their own.
The strongest claim to freeze is Theorem E.4 with its exact statement in Section 7.

## 1. Falsifiers, stated before each replay

Written in the lane checkpoint file before any run.

1. **Theorem E.4.** A closed unit square contained in `[0, 96/25]²` whose exact
   Euclidean distance to every one of the ten segments `[x − 1/20, x + 1/20] × {y}`,
   `(x, y) ∈ P10`, exceeds `3/500`, decided in `Fraction` arithmetic by a convex-polygon
   distance (an intersection test, then vertex-to-edge minima).
   A box my reader cannot certify is not a falsifier until its centre pose is decided
   exactly as an escape; an uncertified box with no exact escape is unresolved scope.
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
  invariant under `x → q − x` and `y → q − y` (its rows are `y = 1, 48/25, 71/25` and
  its columns are symmetric about `48/25`) but not under `x ↔ y`, so its symmetry group
  is the rectangle’s. The half-turn keeps `θ` and maps `cy → q − cy`, so poses with
  `cy ≤ q/2` suffice; then `x → q − x` keeps `cy` and maps a square at angle `θ` to one
  at `π/2 − θ`, so `θ ∈ [0, π/4]` suffices.
  The domain is `t ∈ [0, 27/64] ⊃ [0, √2 − 1]`, `cx ∈ [1/2, 7/2] ⊃ [1/2, q − 1/2]`,
  `cy ∈ [1/2, 2] ⊃ [1/2, q/2]`, with dyadic bounds so that every box of the bisection
  tree is an exact float and an exact `Fraction`, and the over-covered part is removed
  by the discard rule.
- **The bound.** Let `g(P, m)` be the signed Euclidean distance from the closed square
  `Q(P)` to segment `m`: the distance when they are disjoint, minus the greatest
  penetration depth of a point of `m` in `Q(P)` when they meet.
  For the rigid motion `φ` carrying `Q(P₀)` to `Q(P)`, every point of `Q(P₀)` moves by
  at most `h = |c − c₀| + (√2/2)|θ − θ₀|`, so a nearest point of `Q(P₀)` to `m` has an
  image in `Q(P)` within `h` of it, and a ball of radius `d` inside `Q(P₀)` about
  `p ∈ m` has as image a ball of radius `d` inside `Q(P)` about a point within `h` of
  `p`; in both regimes `g(P, m) ≤ g(P₀, m) + h`. Over a box with half-widths
  `(ht, hx, hy)` about its centre `P₀`, `|c − c₀| ≤ √(hx² + hy²)` and
  `|θ − θ₀| = 2|atan t − atan t₀| ≤
  2·ht/(1 + t₁t₀)` from `atan x ≤ x`. A box is **certified** when
  `min_m g(P₀, m) + √(hx² + hy²) + √2·ht/(1 + t₁t₀) ≤ δ` (with `√2 ≤ 665857/470832` in
  both stages and a `10⁻⁹` allowance in the float stage), **discarded** when it holds no
  contained pose (`x₂ < w_min` or `x₁ > q − w_min`, likewise in `y`, `w_min =
  min(w(t₁), w(t₂))` since `w = (cos θ + sin θ)/2` is unimodal), and otherwise split
  along the largest of `hx`, `hy`, `√2·ht`. A box whose scaled half-widths are all below
  the floor `2⁻¹⁴` and which is neither is a failure, and its centre pose is then
  decided exactly by the falsifier’s polygon distance.
- **The segment minimum.** `g(P₀, ·)` restricted to a segment is a convex function of
  the segment parameter; the float stage evaluates it at the analytic candidates (the
  endpoints, `u = 0`, `v = 0`, `|u| = |v|`, `|u| = 1/2`, `|v| = 1/2`, and the stationary
  points of the four corner pieces) and records the minimiser `s*` and the segment.
  Self-test 1 checks the candidate minimum against a 2001-point sampling of every
  segment at 400 random poses (worst discrepancy `1.1·10⁻¹⁶`); self-test 2 checks the
  float signed distance against the exact polygon distance at 60 random rational poses
  (no mismatch).
- **The exact stage.** Every certified leaf is re-decided in `Fraction`: `g` is
  evaluated at the recorded rational `s*`, which bounds the true segment minimum from
  above whatever the float search did, so soundness never rests on the float minimiser;
  the irrational terms enter only through rational upper bounds (`√2` by the convergent,
  `√(hx² + hy²)` by an integer square root plus one at `2⁻⁴⁰`); the inequality is
  `val + h ≤ δ` when `s*` is inside the square and `val ≤ (δ − h)²` with `δ ≥ h` when
  outside. Every discard is re-decided exactly, and the volumes of leaves, discards and
  failures are summed exactly against the domain’s. The lane’s constant is handled as
  `dist² ≤ 2·(2121/500000)²`.

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
`t = 384507/1048576`, `cx = 156707/65536`, `cy = 46211/65536` (a square at about `40.2°`
resting near the bottom wall) at distance `0.006365 > 3/500`.

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
in the square’s frame with the bound
`f(P, p) ≤ f(P₀, p) + hx + hy + 2·ht·(R + hx + hy)`, `R` the larger endpoint’s `L¹`
distance; I checked that bound line by line and it is sound, and its breakpoint set
(`u = 0`, `v = 0`, `u = ±v`) is complete for the piecewise-linear `f`. The two readers
differ in the domain (mine is `4.8×` smaller by the two symmetries), in the target (`δ`
on the Euclidean distance against `δ/√2` on the frame distance) and in the constant,
which together account for the `40×` difference in box count.
One defect: the lane’s tree domain is `[0.5, Q − 0.5]` computed in floats, and
`float(3.84) − 0.5 = 3.33999…986 < 3.34`, so its cover misses the poses with `cx` or
`cy` in `(3.34 − 1.4·10⁻¹⁶, 3.34]`, the axis square flush against a far wall among them.
At `3/500` the gap is harmless (`f` is 1-Lipschitz in the centre, and the stated
constant leaves `9·10⁻⁷` of room); for the constant `√2·2121/500000` as literally stated
it is a measure-zero hole, which the dyadic domain here closes.

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

The argument needs exactly three facts and no more: a valid measure of mass `11 + ε` (so
the eleven pairwise disjoint cores of a packing, each of mass at least one by Condition
5, leave at most `ε` outside them); a set of atoms of mass above `ε` per corner (so one
of its atoms is in some core); and a cross-corner distance above the core’s diameter
`B√2` (so no core holds atoms of two corners).
Nothing about the bound, the column settlement or the floor enters.

**Verdict: agrees.** Every packing of eleven unit squares in `[0, 96/25]²` has four
distinct squares, one per corner, each containing in its interior at least one of its
corner’s two marks `(3152/3175, 2336/3175)` and `(2336/3175, 3152/3175)` (and their
images under the container’s symmetries).
Since `[0, s]² ⊂ [0, 96/25]²`, the same holds of every packing at side at most `96/25`
read in the `96/25` frame.

## 4. Replay of Theorem C (lane B, exp-130)

`theorem_c_replay.py` (Appendix) is a driver of my own around the library’s proposer and
verifier; nothing of lane B’s `bandlib.py` is imported.

| Input | Value |
| --- | --- |
| Side, shrink | `96/25`, `9977/10000` |
| Net | the retained 181 directions from `cases/n11_fractional_certificate/certificate.json`, half-tangent limit `207107/500000`, 180 equal steps |
| Class | cells `0–39 ∪ 172–180`; tangent bounds `[0, 12271089750000/66942386977163] ∪ [177594252500000/189956166180167, 1]`, read from `DirectionClasses.cell_bounds`, which are `[0°, 10.3875°] ∪ [43.0737°, 45°]` in folded degrees, closed ends |
| Site set | `build_site_grid(96/25, 119, 1/10)`: 14,161 sites in 1,830 D4 orbits |
| Composition, thresholds | `(11, 0)`; exact thresholds `(1, 0)` |
| Proposer | `solve_class_program` with `max_rounds = 100`, `rows_per_direction = 3`, tolerance `10⁻⁹` |
| Rationalisation | `rationalise` at scale `4096` (the library’s standard bump) on the weights divided by the float `w₀` |
| Machine | one process, `PACK_JOBS=1`, one BLAS thread; load 1.24 at the start, 1.36 at the end of the row loop |

| Reading | Value |
| --- | --- |
| Row loop | 81 rounds, 5,809 rows, stopped “converged: every placement carries its class threshold”, 332.9 s |
| Float `M` at `w₀ = 1` | `10.798077` (context) |
| Exact mass | `11083/1024 = 10.8232421875` over 296 rationalised atoms, equal to the lane’s fraction |
| Condition 1 | holds, 296 atoms closed under D4 |
| Condition 2′ | holds, `11083/1024 < 11·1 + 0·0` |
| Condition 3 | holds, `t² + 2t − 1 = 309449/250000000000 ≥ 0` |
| Condition 4 | holds, `B(1 + D) = 899996306539/900000000000 < 1` |
| Condition 5′, class 0 | holds, least covered core `4101/4096` at direction 0 over the 49 class directions |
| Condition 5′, class 1 | holds vacuously (no square of the composition; 132 cells unswept) |
| Exact decision wall | 2.6 s |

**Verdict: agrees.** The composition `(11, 0)` on the band is refuted exactly, so no
packing of eleven unit squares in `[0, 96/25]²` has every folded angle in
`[0°, 10.3875°] ∪ [43.0737°, 45°]`; the replay reaches the lane’s rationalised point to
the fraction, which is stronger than the verdict needed.
The row loop converged in 81 rounds here as in the lane, in 333 s at load 1.3 against
the lane’s 584 s at load 8.

## 5. Disagreements with the lanes’ own readings

- **Lane E, the threshold in the segment length.** The lane places it in
  `(7/100, 9/100]` because its reader left `8/100` at the floor.
  My reader decides `8/100` with no failure, so the threshold is in `(7/100, 8/100]`.
  The lane read its `8/100` result as needing a finer floor; what it needed was a
  smaller Lipschitz constant, since at the lane’s floor the bound’s own slack, not the
  floor, was the limit.
- **Lane E, the certified domain.** The far-wall sliver of Section 2.5. Harmless for the
  H-134 statement at `3/500`, a literal gap for the theorem’s sharper constant, closed
  here.
- **Lane C, what to run next.** Lane C asks for phase G (the pair orbit priced) to widen
  the margin `441/125000`. The theorem does not change with the margin, and what is
  unmeasured is not the margin but the value of the anchor to a certificate, which by
  X-021’s duality lemma is bounded by the restricted fractional packing value that
  BC-294 left undecided.
  The measurement should come before the anchored certificate.
- **Lane B, the ladder as a block.** Lane B’s first recommendation is to continue the
  end band at grids 119 and 159 from `(13, 13)` and `(40, 10)`. The registered band
  already clears H-130’s bar four times over, every further rung is a property of the
  site set as much as of the side, and a point costs ten minutes; this is queue filler
  under OR-3, not a sustained block.
- **The composition route.** BC-303’s exit asks for the branch list for geometric
  conditioning if the composition route ended.
  BC-296 did not run in the first wave, so the route has not ended and no branch list
  exists; it stays ready.

## 6. The selection

The candidates the cell names, ranked by what a block would buy toward a global
exclusion at `96/25` against what it costs, with the replays above as the evidence.

1. **Fund: the segment-mark cover toward an ownership argument and route (a)** (BC-302’s
   follow-up, bead `think-qfog`), as the next sustained block.
   It is the only first-wave result that is proved, independently replayed, and
   *strengthened* by the replay: the reader here decides a mark set in under a second
   and a false one in under a minute, so a block can run hundreds of exact decisions
   where the lane ran five.
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
   rule: a family verified by `verify_ceiling` at `96/25` of value at least eleven with
   a unit of weight outside Trump’s neighbourhood decides the ambitious tier negatively;
   a converged covering LP below eleven at `B = 1` moves H-129; anything in between is
   recorded with its bytes.
   The plateau’s full-dual pricing (lane F’s one-line `support_cap` diagnostic, about
   thirty minutes) rides inside this block as its first task, since it tells whether the
   instrument’s stops are the cap’s.
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

> **Theorem (segment localisation at `96/25`).** Let `q = 96/25` and let `M₁₀` be the
> ten closed horizontal segments `[x − 1/20, x + 1/20] × {y}` for `(x, y)` in
> `{(1, 1), (48/25, 1), (71/25, 1), (27/50, 48/25), (73/50, 48/25), (119/50, 48/25),
> (33/10, 48/25), (1, 71/25), (48/25, 71/25), (71/25, 71/25)}`. Every closed unit square
> contained in `[0, q]²`, at any angle, is at Euclidean distance at most
> `√2·2121/500000 < 3/500` from some segment of `M₁₀`. Consequently every square of
> every packing of eleven unit squares at side at most `96/25` is within `3/500` of one
> of these ten segments, and some segment is within `3/500` of two of them.

The same statement holds with the segments shortened to `9/100` (both readers) and to
`8/100` (this reader only, so that companion is certified but not yet independently
replayed). It needs an experiment id, the lane’s `set-S10-l0.1.json` and both readers as
its record, and no registry entry beyond that: it changes no bound on `s(11)`.

The corner-pair theorem (Section 3) is the second claim worth freezing, with the
exported measure as its whole record; it is cheaper to register than E.4 and should be.

## 8. What remains, and what this block could not do

- Theorem C’s replay took the block’s one long computation (333 s of row loop); it
  agreed to the fraction.
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
"""BC-303 independent reader for Theorem E.4 (lane E, session-104).

Claim replayed: every closed unit square contained in S = [0, 96/25]^2, at any angle, is
within delta = 3/500 (Euclidean) of one of the ten closed horizontal segments of length
1/10 centred on Stromquist's Figure-13 points at 96/25.

Design (fixed before reading the lane's cover_reader.py):
  * pose (t, cx, cy), t = tan(theta/2); domain t in [0, 27/64] (covers theta in [0, pi/4]
    by the reflection x -> q - x, which keeps the segment set and maps theta -> pi/2 - theta),
    cx in [1/2, 7/2], cy in [1/2, 2] (covers cy <= q/2 by the half-turn, which keeps theta);
    dyadic bounds so every bisection box is an exact float and an exact Fraction;
  * signed Euclidean distance g(P, m) from the square to segment m (negative = penetration
    depth); over a box with half-widths (ht, hx, hy) about the centre pose P0,
    g(P, m) <= g(P0, m) + sqrt(hx^2 + hy^2) + (sqrt 2 / 2) * |theta - theta0|,
    |theta - theta0| <= 2 ht / (1 + t1 t0); certified iff min_m g(P0, m) + h <= delta;
  * g(P0, seg) = min over the segment of a convex function; the float stage evaluates the
    analytic candidate minimisers, the exact stage re-evaluates g at the recorded rational
    minimiser (an upper bound on the minimum whatever the float stage did);
  * a box is discarded only if it holds no contained pose; a floor box that is neither is
    a failure, whose centre pose is then decided exactly by the falsifier's polygon distance.
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from math import isqrt
from pathlib import Path

import numpy as np

Q = Fraction(96, 25)
DELTA = Fraction(3, 500)
HALF_LEN = Fraction(1, 20)
SQRT2_UP = Fraction(665857, 470832)  # convergent from above: 665857^2 - 2*470832^2 = 1 > 0
assert SQRT2_UP * SQRT2_UP > 2
SQRT2F = float(SQRT2_UP)
P10 = [
    (Fraction(1), Fraction(1)), (Fraction(48, 25), Fraction(1)), (Fraction(71, 25), Fraction(1)),
    (Fraction(27, 50), Fraction(48, 25)), (Fraction(73, 50), Fraction(48, 25)),
    (Fraction(119, 50), Fraction(48, 25)), (Fraction(33, 10), Fraction(48, 25)),
    (Fraction(1), Fraction(71, 25)), (Fraction(48, 25), Fraction(71, 25)), (Fraction(71, 25), Fraction(71, 25)),
]
ALLOW = 1e-9

# ----------------------------------------------------------------------------- exact helpers


def sqrt_upper(fr: Fraction, bits: int = 40) -> Fraction:
    """A rational rho with rho^2 >= fr, within 2^-bits of sqrt(fr)."""
    if fr <= 0:
        return Fraction(0)
    n, d = fr.numerator, fr.denominator
    scale = 1 << bits
    return Fraction(isqrt(n * d * scale * scale) + 1, d * scale)


def frame(t: Fraction) -> tuple[Fraction, Fraction]:
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def half_width(t: Fraction) -> Fraction:
    c, s = frame(t)
    return (c + s) / 2


def exact_signed(t0: Fraction, x0: Fraction, y0: Fraction, px: Fraction, py: Fraction) -> tuple[bool, Fraction]:
    """Signed distance of point p from the closed unit square at pose (t0, x0, y0).

    Returns (inside, value): inside -> value is the signed distance (<= 0, exact);
    outside -> value is the squared distance (> 0, exact).
    """
    c, s = frame(t0)
    rx, ry = px - x0, py - y0
    u = rx * c + ry * s
    v = -rx * s + ry * c
    a = abs(u) - Fraction(1, 2)
    b = abs(v) - Fraction(1, 2)
    if a <= 0 and b <= 0:
        return True, max(a, b)
    a = max(a, Fraction(0))
    b = max(b, Fraction(0))
    return False, a * a + b * b


def square_vertices(t0: Fraction, x0: Fraction, y0: Fraction) -> list[tuple[Fraction, Fraction]]:
    c, s = frame(t0)
    out = []
    for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((x0 + (a * c - b * s) / 2, y0 + (a * s + b * c) / 2))
    return out


def _cross(ax, ay, bx, by) -> Fraction:
    return ax * by - ay * bx


def _point_seg_dist2(px, py, ax, ay, bx, by) -> Fraction:
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    tt = ((px - ax) * dx + (py - ay) * dy) / l2
    tt = min(max(tt, Fraction(0)), Fraction(1))
    cx, cy = ax + tt * dx, ay + tt * dy
    return (px - cx) ** 2 + (py - cy) ** 2


def _segments_cross(p1, p2, p3, p4) -> bool:
    """Closed segments p1p2 and p3p4 intersect (exact, with collinear cases)."""
    def orient(a, b, c):
        return _cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1])

    def on_seg(a, b, c):
        return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])

    o1, o2, o3, o4 = orient(p1, p2, p3), orient(p1, p2, p4), orient(p3, p4, p1), orient(p3, p4, p2)
    if ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0)) and o1 != 0 and o2 != 0 and o3 != 0 and o4 != 0:
        return True
    if o1 == 0 and on_seg(p1, p2, p3):
        return True
    if o2 == 0 and on_seg(p1, p2, p4):
        return True
    if o3 == 0 and on_seg(p3, p4, p1):
        return True
    if o4 == 0 and on_seg(p3, p4, p2):
        return True
    return False


def exact_square_segment_dist2(t0: Fraction, x0: Fraction, y0: Fraction, seg_index: int) -> Fraction:
    """Exact squared Euclidean distance between the closed square and the closed segment (0 if they meet)."""
    xm, ym = P10[seg_index]
    A = (xm - HALF_LEN, ym)
    B = (xm + HALF_LEN, ym)
    verts = square_vertices(t0, x0, y0)
    # endpoints inside the closed square?
    for px, py in (A, B):
        inside, _ = exact_signed(t0, x0, y0, px, py)
        if inside:
            return Fraction(0)
    edges = [(verts[i], verts[(i + 1) % 4]) for i in range(4)]
    for e0, e1 in edges:
        if _segments_cross(e0, e1, A, B):
            return Fraction(0)
    best = None
    for vx, vy in verts:
        d2 = _point_seg_dist2(vx, vy, A[0], A[1], B[0], B[1])
        best = d2 if best is None else min(best, d2)
    for px, py in (A, B):
        for e0, e1 in edges:
            d2 = _point_seg_dist2(px, py, e0[0], e0[1], e1[0], e1[1])
            best = min(best, d2)
    return best


def exact_contained(t0: Fraction, x0: Fraction, y0: Fraction) -> bool:
    return all(0 <= vx <= Q and 0 <= vy <= Q for vx, vy in square_vertices(t0, x0, y0))


def exact_escape(t0: Fraction, x0: Fraction, y0: Fraction, delta: Fraction = DELTA) -> tuple[bool, Fraction]:
    """Is the pose a contained square farther than delta from every segment? Returns (escape, least dist2)."""
    if not exact_contained(t0, x0, y0):
        return False, Fraction(-1)
    least = min(exact_square_segment_dist2(t0, x0, y0, k) for k in range(len(P10)))
    return least > delta * delta, least


# ----------------------------------------------------------------------------- float stage

SEG_X = np.array([float(p[0]) for p in P10])
SEG_Y = np.array([float(p[1]) for p in P10])
HL = float(HALF_LEN)


def float_g_min(t0, x0, y0):
    """min over segments of the signed distance at the centre poses; returns (g, seg, s*)."""
    n = t0.shape[0]
    den = 1.0 + t0 * t0
    C = (1.0 - t0 * t0) / den
    S = 2.0 * t0 / den
    rx = SEG_X[None, :] - x0[:, None]  # (n, 10) at s = 0
    ry = SEG_Y[None, :] - y0[:, None]
    u0 = rx * C[:, None] + ry * S[:, None]
    v0 = -rx * S[:, None] + ry * C[:, None]
    Cn = C[:, None]
    Sn = S[:, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        cands = [
            np.full_like(u0, -HL), np.full_like(u0, HL),
            -u0 / Cn,                       # u = 0
            v0 / Sn,                        # v = 0
            (0.5 - u0) / Cn, (-0.5 - u0) / Cn,   # u = +-1/2
            (v0 - 0.5) / Sn, (v0 + 0.5) / Sn,    # v = +-1/2
            (v0 - u0) / (Cn + Sn),          # u = v
            (-v0 - u0) / (Cn - Sn),         # u = -v
        ]
        for su in (1.0, -1.0):
            for sv in (1.0, -1.0):
                cands.append(-u0 * Cn + v0 * Sn + (su * Cn - sv * Sn) / 2.0)
    s = np.stack(cands, axis=2)  # (n, 10, 14)
    s = np.where(np.isfinite(s), s, HL)
    s = np.clip(s, -HL, HL)
    u = u0[:, :, None] + Cn[:, :, None] * s
    v = v0[:, :, None] - Sn[:, :, None] * s
    a = np.abs(u) - 0.5
    b = np.abs(v) - 0.5
    inside = (a <= 0) & (b <= 0)
    val = np.where(inside, np.maximum(a, b), np.hypot(np.maximum(a, 0.0), np.maximum(b, 0.0)))
    flat = val.reshape(n, -1)
    idx = np.argmin(flat, axis=1)
    g = flat[np.arange(n), idx]
    seg = idx // s.shape[2]
    cand = idx % s.shape[2]
    sstar = s.reshape(n, -1)[np.arange(n), idx]
    return g, seg, sstar, cand


def float_half_width(t):
    den = 1.0 + t * t
    return ((1.0 - t * t) / den + 2.0 * t / den) / 2.0


def run_cover(delta: float, floor: float, node_budget: int, chunk: int = 40000, log=print):
    dom = np.array([[0.0, 27 / 64, 0.5, 3.5, 0.5, 2.0]])  # t1 t2 x1 x2 y1 y2 (all dyadic)
    frontier = dom
    leaves = []      # certified: rows [t1 t2 x1 x2 y1 y2 seg sstar g h]
    discards = []    # rows [t1 t2 x1 x2 y1 y2]
    failures = []    # rows [t1 t2 x1 x2 y1 y2 g h]
    nodes = 0
    level = 0
    qf = float(Q)
    t_start = time.perf_counter()
    while frontier.shape[0] > 0:
        level += 1
        next_parts = []
        n_cert = n_disc = n_fail = 0
        for start in range(0, frontier.shape[0], chunk):
            B = frontier[start:start + chunk]
            nodes += B.shape[0]
            t1, t2, x1, x2, y1, y2 = (B[:, i] for i in range(6))
            t0 = (t1 + t2) / 2.0
            x0 = (x1 + x2) / 2.0
            y0 = (y1 + y2) / 2.0
            ht = (t2 - t1) / 2.0
            hx = (x2 - x1) / 2.0
            hy = (y2 - y1) / 2.0
            # discard test: no contained pose in the box
            wmin = np.minimum(float_half_width(t1), float_half_width(t2))
            disc = (x2 < wmin - ALLOW) | (x1 > qf - wmin + ALLOW) | (y2 < wmin - ALLOW) | (y1 > qf - wmin + ALLOW)
            # certification
            g, seg, sstar, _ = float_g_min(t0, x0, y0)
            h = np.hypot(hx, hy) + SQRT2F * ht / (1.0 + t1 * t0)
            cert = (~disc) & (g + h <= delta - ALLOW)
            rest = ~(disc | cert)
            if disc.any():
                discards.append(B[disc])
                n_disc += int(disc.sum())
            if cert.any():
                leaves.append(np.column_stack([B[cert], seg[cert].astype(float), sstar[cert], g[cert], h[cert]]))
                n_cert += int(cert.sum())
            if rest.any():
                R = B[rest]
                sw = np.stack([hx[rest], hy[rest], SQRT2F * ht[rest]], axis=1)
                atfloor = sw.max(axis=1) <= floor
                if atfloor.any():
                    failures.append(np.column_stack([R[atfloor], g[rest][atfloor], h[rest][atfloor]]))
                    n_fail += int(atfloor.sum())
                    R = R[~atfloor]
                    sw = sw[~atfloor]
                if R.shape[0]:
                    dim = np.argmax(sw, axis=1)  # 0 -> x, 1 -> y, 2 -> t
                    left = R.copy()
                    right = R.copy()
                    for d, (lo, hi) in ((0, (2, 3)), (1, (4, 5)), (2, (0, 1))):
                        m = dim == d
                        mid = (R[m, lo] + R[m, hi]) / 2.0
                        left[m, hi] = mid
                        right[m, lo] = mid
                    next_parts.append(left)
                    next_parts.append(right)
        frontier = np.concatenate(next_parts) if next_parts else np.zeros((0, 6))
        log(f"level {level:2d}: nodes {nodes:9d} cert +{n_cert:8d} disc +{n_disc:7d} fail +{n_fail:6d} "
            f"open {frontier.shape[0]:8d}  {time.perf_counter() - t_start:7.1f}s")
        if nodes > node_budget:
            log("node budget exhausted")
            failures.append(np.column_stack([frontier, np.full(frontier.shape[0], np.nan), np.full(frontier.shape[0], np.nan)]))
            break
    L = np.concatenate(leaves) if leaves else np.zeros((0, 10))
    D = np.concatenate(discards) if discards else np.zeros((0, 6))
    F = np.concatenate(failures) if failures else np.zeros((0, 8))
    return nodes, L, D, F


# ----------------------------------------------------------------------------- exact stage


def exact_certify_leaf(row, delta: Fraction, delta2_override: Fraction | None = None) -> bool:
    t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
    seg = int(row[6])
    sstar = Fraction(float(row[7]))
    sstar = min(max(sstar, -HALF_LEN), HALF_LEN)
    t0, x0, y0 = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
    ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
    h = sqrt_upper(hx * hx + hy * hy) + SQRT2_UP * ht / (1 + t1 * t0)
    xm, ym = P10[seg]
    inside, val = exact_signed(t0, x0, y0, xm + sstar, ym)
    if delta2_override is None:
        # certify: g + h <= delta
        if inside:
            return val + h <= delta
        room = delta - h
        return room >= 0 and val <= room * room
    # certify against sqrt(delta2_override): g + h <= sqrt(D2)  <=>  (inside) h + val <= sqrt(D2)
    if inside:
        lhs = val + h  # may be negative
        if lhs <= 0:
            return True
        return lhs * lhs <= delta2_override
    # sqrt(val) + h <= sqrt(D2)  <=> sqrt(val) <= sqrt(D2) - h ; need sqrt(D2) >= h: h^2 <= D2
    if h * h > delta2_override:
        return False
    # sqrt(val) <= sqrt(D2) - h  <=>  val <= D2 - 2 h sqrt(D2) + h^2 ; bound sqrt(D2) below by a rational
    # sqrt(D2) >= r with r = sqrt_lower(D2)
    r = sqrt_lower(delta2_override)
    if r < h:
        return False
    return val <= (r - h) * (r - h)


def sqrt_lower(fr: Fraction, bits: int = 40) -> Fraction:
    n, d = fr.numerator, fr.denominator
    scale = 1 << bits
    return Fraction(isqrt(n * d * scale * scale), d * scale)


def exact_discard_box(row) -> bool:
    t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
    wmin = min(half_width(t1), half_width(t2))
    return x2 < wmin or x1 > Q - wmin or y2 < wmin or y1 > Q - wmin


def volume(rows) -> Fraction:
    tot = Fraction(0)
    for r in rows:
        t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in r[:6])
        tot += (t2 - t1) * (x2 - x1) * (y2 - y1)
    return tot


# ----------------------------------------------------------------------------- self-tests


def selftest(log=print) -> None:
    rng = np.random.default_rng(303)
    # (1) candidate minimiser vs dense sampling along each segment at random poses
    n = 400
    t0 = rng.uniform(0, 27 / 64, n)
    x0 = rng.uniform(0.5, 3.5, n)
    y0 = rng.uniform(0.5, 2.0, n)
    g, seg, sstar, _ = float_g_min(t0, x0, y0)
    ss = np.linspace(-HL, HL, 2001)
    worst = 0.0
    for i in range(n):
        den = 1 + t0[i] ** 2
        C, S = (1 - t0[i] ** 2) / den, 2 * t0[i] / den
        best = np.inf
        for k in range(10):
            px = SEG_X[k] + ss
            py = SEG_Y[k]
            rx, ry = px - x0[i], py - y0[i]
            u = rx * C + ry * S
            v = -rx * S + ry * C
            a, b = np.abs(u) - 0.5, np.abs(v) - 0.5
            val = np.where((a <= 0) & (b <= 0), np.maximum(a, b), np.hypot(np.maximum(a, 0), np.maximum(b, 0)))
            best = min(best, val.min())
        worst = max(worst, g[i] - best)
    log(f"selftest 1: candidate min minus dense-sample min, worst over {n} poses = {worst:.3e} (must be <= ~1e-12; dense min >= true min so diff >= -0 expected)")
    assert worst <= 1e-9
    # (2) exact polygon distance vs float signed distance at random rational poses
    mism = 0
    for i in range(60):
        tq, xq, yq = Fraction(int(rng.integers(0, 4219)), 10000), Fraction(int(rng.integers(5000, 35000)), 10000), Fraction(int(rng.integers(5000, 20000)), 10000)
        gf, sg, sst, _ = float_g_min(np.array([float(tq)]), np.array([float(xq)]), np.array([float(yq)]))
        d2 = min(exact_square_segment_dist2(tq, xq, yq, k) for k in range(10))
        de = math.sqrt(float(d2))
        if abs(max(gf[0], 0.0) - de) > 1e-9:
            mism += 1
            log(f"  mismatch at {tq},{xq},{yq}: float {gf[0]} exact {de}")
    log(f"selftest 2: exact polygon distance agrees with max(float g, 0) at 60 random poses, mismatches {mism}")
    assert mism == 0
    # (3) lane C's exact escape of the *point* set at q: centre (73/50, 67/50), t = 49/200 -> with segments?
    esc, least = exact_escape(Fraction(49, 200), Fraction(73, 50), Fraction(67, 50))
    log(f"selftest 3: lane C's point-set escape pose against the segments: escape={esc}, least dist = {math.sqrt(float(least)):.6f}")
    # (4) an axis square touching a segment from above: centre (1, 1 + 1/2 + 1/1000) -> dist 1/1000
    d2 = exact_square_segment_dist2(Fraction(0), Fraction(1), Fraction(1) + Fraction(1, 2) + Fraction(1, 1000), 0)
    esc, least = exact_escape(Fraction(0), Fraction(1), Fraction(1) + Fraction(1, 2) + Fraction(1, 1000))
    log(f"selftest 4: axis square 1/1000 above segment 0: dist to segment 0 = {math.sqrt(float(d2)):.6f}; to the set {math.sqrt(float(least)):.6f} (it meets the (73/50, 48/25) segment), escape={esc}")
    assert not esc and d2 == Fraction(1, 1000) ** 2 and least == 0
    # (5) an axis square whose nearest segments are all more than delta away: centre (0.5 + 0.3, 0.5+0.3)? bottom-left corner box
    esc, least = exact_escape(Fraction(0), Fraction(1, 2), Fraction(1, 2))
    log(f"selftest 5: axis square in the corner (0.5, 0.5): dist = {math.sqrt(float(least)):.6f}, escape={esc}")
    # (6) segments at length 6/100 have an escape per the lane; not testable here without changing HALF_LEN. skip.
    log("selftests passed")


# ----------------------------------------------------------------------------- driver


def main(argv: list[str]) -> int:
    out_dir = Path(argv[1]) if len(argv) > 1 else Path(".")
    floor = float(argv[2]) if len(argv) > 2 else 2.0 ** -14
    mode = argv[3] if len(argv) > 3 else "delta"  # "delta" = 3/500, "lane" = sqrt2*2121/500000
    global HALF_LEN, HL
    if len(argv) > 4:
        HALF_LEN = Fraction(argv[4])
        HL = float(HALF_LEN)
        mode = f"{mode}-hl{HALF_LEN.numerator}-{HALF_LEN.denominator}"
    out_dir.mkdir(parents=True, exist_ok=True)
    logf = open(out_dir / f"reader-{mode}.log", "w")

    def log(msg):
        print(msg)
        logf.write(msg + "\n")
        logf.flush()

    log(f"E.4 reader: mode {mode}, half-length {HALF_LEN}, floor {floor}, load {open('/proc/loadavg').read().split()[:3]}")
    selftest(log)
    if mode.startswith("delta"):
        delta_f = float(DELTA)
        delta2 = None
    else:
        delta2 = 2 * Fraction(2121, 500000) ** 2
        delta_f = math.sqrt(float(delta2))
    t0 = time.perf_counter()
    nodes, L, D, F = run_cover(delta_f, floor, node_budget=12_000_000, log=log)
    tf = time.perf_counter() - t0
    log(f"float cover: nodes {nodes}, certified leaves {L.shape[0]}, discards {D.shape[0]}, failures {F.shape[0]}, "
        f"{tf:.1f}s, load {open('/proc/loadavg').read().split()[:3]}")
    np.save(out_dir / f"leaves-{mode}.npy", L)
    np.save(out_dir / f"discards-{mode}.npy", D)
    np.save(out_dir / f"failures-{mode}.npy", F)
    # failures: decide the centre poses exactly
    n_esc = 0
    for row in F[:200]:
        t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
        tq, xq, yq = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
        esc, least = exact_escape(tq, xq, yq)
        if esc:
            n_esc += 1
            log(f"EXACT ESCAPE at t={tq} cx={xq} cy={yq}: least dist2 {least} = {math.sqrt(float(least)):.6f}")
    if F.shape[0]:
        log(f"failures: {F.shape[0]} floor boxes undecided; exact escapes among the first 200 centres: {n_esc}")
    # exact re-check
    t0 = time.perf_counter()
    bad = 0
    for i, row in enumerate(L):
        if not exact_certify_leaf(row, DELTA, delta2):
            bad += 1
            if bad <= 10:
                log(f"EXACT RE-CHECK REJECTS leaf {i}: {row.tolist()}")
    te = time.perf_counter() - t0
    log(f"exact re-check of {L.shape[0]} certified leaves: {bad} rejected, {te:.1f}s, load {open('/proc/loadavg').read().split()[:3]}")
    rejected_escapes = 0
    if bad:
        for i, row in enumerate(L):
            if not exact_certify_leaf(row, DELTA, delta2):
                t1, t2, x1, x2, y1, y2 = (Fraction(float(v)) for v in row[:6])
                esc, least = exact_escape((t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2)
                rejected_escapes += int(esc)
        log(f"rejected leaves are counted as failures; exact escapes among their centres: {rejected_escapes}")
    t0 = time.perf_counter()
    badd = sum(0 if exact_discard_box(row) else 1 for row in D)
    log(f"exact re-check of {D.shape[0]} discarded boxes: {badd} rejected, {time.perf_counter() - t0:.1f}s")
    vol = volume(L) + volume(D) + volume(F)
    dom = Fraction(27, 64) * 3 * Fraction(3, 2)
    log(f"volume identity: leaves+discards+failures = {vol} vs domain {dom}: {'ok' if vol == dom else 'MISMATCH'}")
    summary = {
        "mode": mode, "delta": str(DELTA) if delta2 is None else f"sqrt({delta2})",
        "floor": floor, "nodes": int(nodes), "certified": int(L.shape[0]), "discarded": int(D.shape[0]),
        "failures": int(F.shape[0]), "exact_rejected_leaves": bad, "exact_rejected_discards": badd,
        "volume_ok": vol == dom, "float_seconds": round(tf, 1), "exact_seconds": round(te, 1),
        "exact_escapes_among_failures": n_esc, "exact_escapes_among_rejected_leaves": rejected_escapes,
    }
    (out_dir / f"summary-{mode}.json").write_text(json.dumps(summary, indent=1))
    log(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### `corner_pair_replay.py`

```text
"""BC-303 replay of lane C's four-corner pair containment theorem at 96/25 (session-101).

Steps, each decided exactly:
  1. load bc-293-measure-free-96-25.json into a sqpack Certificate and run the library's
     verify (Conditions 1-5 on the exact eighth-turn sweep, one worker); record mass and verdict;
  2. epsilon = M - 11; find the eight atoms of the pair orbit and their weights; per-corner
     pair mass against epsilon;
  3. the ownership step's geometry: least squared distance between marks of different
     corners against 2 B^2 (the squared diameter of a closed B-square), decided in Fraction;
  4. re-derive what the argument needs and print the theorem's exact statement.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.model import Atom

PATH = Path("campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-293-measure-free-96-25.json")
PAIR = (Fraction(3152, 3175), Fraction(2336, 3175))
CLAIMED_MASS = Fraction(22524199, 2000000)
CLAIMED_WEIGHT = Fraction(106251, 800000)


def load() -> tuple[Certificate, dict]:
    rec = json.loads(PATH.read_text())
    limit = Fraction(rec["angle_limit"])
    steps = int(rec["direction_steps"])
    atoms = tuple(
        Atom(f"{i:04d}", Fraction(a[0]), Fraction(a[1]), Fraction(a[2])) for i, a in enumerate(rec["atoms"])
    )
    cert = Certificate(
        n=int(rec["n"]), outer_side=Fraction(rec["outer_side"]), square_side=Fraction(rec["square_side"]),
        atoms=atoms, half_tangents=tuple(limit * k / steps for k in range(steps + 1)), symmetry=rec.get("symmetry", "D4"),
    )
    return cert, rec


def main() -> int:
    load_avg = open("/proc/loadavg").read().split()[:3]
    cert, rec = load()
    L, B = cert.outer_side, cert.square_side
    print(f"loaded {PATH.name}: n={cert.n} L={L} B={B} atoms={len(cert.atoms)} net={len(cert.half_tangents)} dirs, "
          f"D={cert.largest_half_gap_tangent}, declared mass {rec['total_mass']}, declared least cell {rec.get('least_cell_mass')}; load {load_avg}")
    M = cert.total_mass
    print(f"step 1a: total mass {M} == claimed {CLAIMED_MASS}: {M == CLAIMED_MASS}; float {float(M):.7f}")
    t0 = time.perf_counter()
    v = verify(cert, workers=1)
    wall = time.perf_counter() - t0
    for c in v.conditions:
        print(f"  {c.name}: holds={c.holds}; {c.detail}")
    valid = all(c.holds for c in v.conditions if not c.name.startswith("Condition 2"))
    print(f"step 1b: verify wall {wall:.1f}s load {open('/proc/loadavg').read().split()[:3]}; Conditions 1,3,4,5 hold: {valid}; "
          f"least cell {v.minimum_cell_mass} at {v.worst_direction}; Condition 2 (mass < 11) {'holds' if M < 11 else 'fails, as expected'}")

    eps = M - 11
    print(f"step 2: epsilon = M - 11 = {eps} = {float(eps):.7f}")
    # the D4 orbit of PAIR: images under x->L-x, y->L-y, x<->y
    def images(p):
        x, y = p
        out = set()
        for a in (x, L - x):
            for b in (y, L - y):
                out.add((a, b))
                out.add((b, a))
        return out
    orbit = images(PAIR)
    print(f"  pair orbit size {len(orbit)}")
    found = {}
    for a in cert.atoms:
        if (a.x, a.y) in orbit:
            found[(a.x, a.y)] = found.get((a.x, a.y), Fraction(0)) + a.weight
    print(f"  atoms found on the orbit: {len(found)} of {len(orbit)}; weights: {sorted(set(str(w) for w in found.values()))}")
    all_weight_ok = len(found) == 8 and all(w == CLAIMED_WEIGHT for w in found.values())
    print(f"  every orbit atom present with weight {CLAIMED_WEIGHT}: {all_weight_ok}")
    # per-corner pairs: the two marks of the corner at (0,0) are (px,py) and (py,px)
    corners = {}
    for (x, y), w in found.items():
        cx = 0 if x < L / 2 else 1
        cy = 0 if y < L / 2 else 1
        corners.setdefault((cx, cy), []).append(((x, y), w))
    for k, lst in sorted(corners.items()):
        mass = sum(w for _, w in lst)
        print(f"  corner {k}: marks {[(str(x), str(y)) for (x, y), _ in lst]} pair mass {mass} = {float(mass):.7f}; "
              f"mass - epsilon = {mass - eps} = {float(mass - eps):.6f}; > epsilon: {mass > eps}")
    pair_ok = all(sum(w for _, w in lst) > eps for lst in corners.values()) and len(corners) == 4

    # step 3: geometry
    diam2 = 2 * B * B  # squared diameter of a closed B-square
    least_cross = None
    for (k1, l1), (k2, l2) in combinations(sorted(corners.items()), 2):
        for (p, _), (r, _) in ((a, b) for a in l1 for b in l2):
            d2 = (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2
            least_cross = d2 if least_cross is None else min(least_cross, d2)
    within = None
    for lst in corners.values():
        (p, _), (r, _) = lst[0], lst[1]
        d2 = (p[0] - r[0]) ** 2 + (p[1] - r[1]) ** 2
        within = d2 if within is None else min(within, d2)
    print(f"step 3: 2B^2 = {diam2} = {float(diam2):.6f} (diameter {float(diam2) ** 0.5:.5f}); least squared distance between marks of "
          f"different corners {least_cross} = {float(least_cross) ** 0.5:.5f}^2; > 2B^2: {least_cross > diam2}")
    print(f"  the two marks of one corner are {float(within) ** 0.5:.5f} apart (squared {within}); one core can hold both: {within <= diam2}")

    # step 4: the ownership step, restated
    print("step 4: the argument needs exactly: (i) a valid measure (Conditions 1,3,4,5) of mass 11 + eps;")
    print("        (ii) each corner's pair mass > eps, so at least one mark of each corner lies in some core;")
    print("        (iii) cross-corner mark distance > B*sqrt(2), so no core holds marks of two corners.")
    print("        Not needed: the two marks of one corner being within a core, any bound, any floor.")
    verdict = M == CLAIMED_MASS and valid and all_weight_ok and pair_ok and least_cross > diam2
    print(f"VERDICT: corner-pair theorem replays: {verdict}")
    print(f"  Theorem: every packing of eleven unit squares in [0, 96/25]^2 has four distinct squares, one per corner, each")
    print(f"  containing in its interior at least one of its corner's marks ({PAIR[0]}, {PAIR[1]}) or ({PAIR[1]}, {PAIR[0]})")
    print(f"  (images under the container's symmetries), with margin mu(pair) - eps = {CLAIMED_WEIGHT * 2 - eps}.")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
```

### `theorem_c_replay.py`

```text
"""BC-303 replay of lane B's Theorem C (session-102, exp-130) at 96/25.

Claim: the composition-(11, 0) class program on cells 0-39 union 172-180 of the retained
181-direction net (folded band [0, 10.3875 deg] union [43.0737 deg, 45 deg], closed ends) at
side 96/25, shrink 9977/10000, site set build_site_grid(96/25, 119, 1/10), is refuted by an
exactly decided measure: mass 11083/1024 < 11 with every class direction's least covered
core at least 1 (least core 4101/4096 over 49 directions), 296 atoms.

This driver is written from the statement: it calls the library's proposer and its exact
verifier directly, records every input, and reports the verdict of decide_class_program.
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.classcert import (
    ClassThresholds,
    Composition,
    DirectionClasses,
    decide_class_program,
    solve_class_program,
)
from sqpack.fractional.generate import build_site_grid, net_half_tangents, rationalise

NET = Path("cases/n11_fractional_certificate/certificate.json")


def deg(t: Fraction) -> float:
    return math.degrees(math.atan(float(t)))


def main(argv: list[str]) -> int:
    grid_count = int(argv[1]) if len(argv) > 1 else 119
    max_rounds = int(argv[2]) if len(argv) > 2 else 100
    out = Path(argv[3]) if len(argv) > 3 else Path("theorem-c.json")
    spec = json.loads(NET.read_text())
    ht = net_half_tangents(Fraction(spec["angle_limit"]), int(spec["direction_steps"]))
    shrink = Fraction(spec["square_side"])
    side = Fraction(96, 25)
    cells = frozenset(range(0, 40)) | frozenset(range(172, 181))
    classes = DirectionClasses(ht, cells)
    lo_a, hi_a = classes.cell_bounds(0)[0], classes.cell_bounds(39)[1]
    lo_b, hi_b = classes.cell_bounds(172)[0], classes.cell_bounds(180)[1]
    print(f"net: {len(ht)} directions, limit {ht[-1]}, shrink {shrink}, side {side}; load {open('/proc/loadavg').read().split()[:3]}")
    print(f"class cells 0-39 and 172-180: tangent bounds [{lo_a}, {hi_a}] and [{lo_b}, {hi_b}]")
    print(f"  in folded degrees: [{deg(lo_a):.4f}, {deg(hi_a):.4f}] and [{deg(lo_b):.4f}, {deg(hi_b):.4f}]")
    grid = build_site_grid(side, grid_count, Fraction(1, 10))
    print(f"site set: build_site_grid({side}, {grid_count}, 1/10): {len(grid.positions())} sites, {len(grid.orbits)} orbits")
    comp = Composition(11, 0)
    t0 = time.perf_counter()
    weights, log = solve_class_program(grid, shrink, classes, comp, max_rounds=max_rounds)
    t_float = time.perf_counter() - t0
    print(f"float proposer: rounds {log.rounds}, rows {log.rows}, stopped '{log.stopped}', objective {log.objective}, thresholds {log.thresholds}, "
          f"wall {t_float:.1f}s, load {open('/proc/loadavg').read().split()[:3]}")
    if not log.thresholds[0] > 0:
        print("proposer returned w0 = 0; nothing to decide")
        return 2
    print(f"  float M at w0 = 1: {log.objective / log.thresholds[0]:.6f}")
    atoms = rationalise(grid, weights / log.thresholds[0], scale=4096)
    t1 = time.perf_counter()
    v = decide_class_program(atoms, side, shrink, classes, comp, thresholds=ClassThresholds(Fraction(1), Fraction(0)))
    t_exact = time.perf_counter() - t1
    print(f"exact decision on {len(atoms)} rationalised atoms (scale 4096): total mass {v.total_mass} = {float(v.total_mass):.10f}; wall {t_exact:.1f}s")
    for c in v.conditions:
        print(f"  {c.name}: holds={c.holds}; {c.detail}")
    for m in v.minima:
        print(f"  minimum: class {m.label} over {m.cells} cells: {m.mass} at direction {m.direction}")
    holds_5 = all(c.holds for c in v.conditions if not c.name.startswith("Condition 2'"))
    print(f"refutes (11, 0): {v.refutes}; Conditions 1, 3, 4, 5' hold: {holds_5}; failures {list(v.failures)}")
    claimed = Fraction(11083, 1024)
    print(f"claimed mass 11083/1024 = {float(claimed):.10f}; equal to the fraction: {v.total_mass == claimed}; claimed least core 4101/4096, 296 atoms")
    rec = {
        "grid": grid_count, "sites": len(grid.positions()), "orbits": len(grid.orbits), "cells": sorted(cells),
        "tangent_bounds": [[str(lo_a), str(hi_a)], [str(lo_b), str(hi_b)]],
        "deg_bounds": [[deg(lo_a), deg(hi_a)], [deg(lo_b), deg(hi_b)]],
        "rounds": log.rounds, "rows": log.rows, "stopped": log.stopped, "float_M": log.objective / log.thresholds[0],
        "atoms": len(atoms), "exact_M": str(v.total_mass), "refutes": v.refutes, "holds_5": holds_5,
        "conditions": [(c.name, c.holds, c.detail) for c in v.conditions],
        "minima": [(m.label, str(m.mass), m.direction) for m in v.minima if m.mass is not None],
        "float_seconds": round(t_float, 1), "exact_seconds": round(t_exact, 1),
        "atoms_list": [[str(a.x), str(a.y), str(a.weight)] for a in atoms],
    }
    out.write_text(json.dumps(rec, indent=1))
    print(f"VERDICT: Theorem C {'replays (refuted, exactly)' if v.refutes and holds_5 else 'DOES NOT replay'} on this run")
    return 0 if v.refutes and holds_5 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

### `corner-pair.out`

```text
loaded bc-293-measure-free-96-25.json: n=11 L=96/25 B=9977/10000 atoms=377 net=181 dirs, D=207107/90000000, declared mass 22524199/2000000, declared least cell 800003/800000; load ['1.65', '0.97', '0.78']
step 1a: total mass 22524199/2000000 == claimed 22524199/2000000: True; float 11.2620995
  Condition 1 atoms carry the declared symmetry: holds=True; 377 atoms closed under D4 about the centre
  Condition 2 total mass below n: holds=False; total 22524199/2000000 against n = 11
  Condition 3 net reaches pi/4: holds=True; final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000
  Condition 4 containment B(1 + D) < 1: holds=True; B = 9977/10000, D = 207107/90000000, B(1 + D) = 899996306539/900000000000
  Condition 5 every reachable cell carries mass 1: holds=True; least cell mass 800003/800000 at direction 0
step 1b: verify wall 14.9s load ['1.73', '1.03', '0.80']; Conditions 1,3,4,5 hold: True; least cell 800003/800000 at 0; Condition 2 (mass < 11) fails, as expected
step 2: epsilon = M - 11 = 524199/2000000 = 0.2620995
  pair orbit size 8
  atoms found on the orbit: 8 of 8; weights: ['106251/800000']
  every orbit atom present with weight 106251/800000: True
  corner (0, 0): marks [('2336/3175', '3152/3175'), ('3152/3175', '2336/3175')] pair mass 106251/400000 = 0.2656275; mass - epsilon = 441/125000 = 0.003528; > epsilon: True
  corner (0, 1): marks [('2336/3175', '1808/635'), ('3152/3175', '9856/3175')] pair mass 106251/400000 = 0.2656275; mass - epsilon = 441/125000 = 0.003528; > epsilon: True
  corner (1, 0): marks [('1808/635', '2336/3175'), ('9856/3175', '3152/3175')] pair mass 106251/400000 = 0.2656275; mass - epsilon = 441/125000 = 0.003528; > epsilon: True
  corner (1, 1): marks [('1808/635', '9856/3175'), ('9856/3175', '1808/635')] pair mass 106251/400000 = 0.2656275; mass - epsilon = 441/125000 = 0.003528; > epsilon: True
step 3: 2B^2 = 99540529/50000000 = 1.990811 (diameter 1.41096); least squared distance between marks of different corners 34668544/10080625 = 1.85449^2; > 2B^2: True
  the two marks of one corner are 0.36346 apart (squared 1331712/10080625); one core can hold both: True
step 4: the argument needs exactly: (i) a valid measure (Conditions 1,3,4,5) of mass 11 + eps;
        (ii) each corner's pair mass > eps, so at least one mark of each corner lies in some core;
        (iii) cross-corner mark distance > B*sqrt(2), so no core holds marks of two corners.
        Not needed: the two marks of one corner being within a core, any bound, any floor.
VERDICT: corner-pair theorem replays: True
  Theorem: every packing of eleven unit squares in [0, 96/25]^2 has four distinct squares, one per corner, each
  containing in its interior at least one of its corner's marks (3152/3175, 2336/3175) or (2336/3175, 3152/3175)
  (images under the container's symmetries), with margin mu(pair) - eps = 441/125000.
```

### `theorem-c-g119.out`

```text
net: 181 directions, limit 207107/500000, shrink 9977/10000, side 96/25; load ['1.24', '0.99', '0.80']
class cells 0-39 and 172-180: tangent bounds [0, 12271089750000/66942386977163] and [177594252500000/189956166180167, 1]
  in folded degrees: [0.0000, 10.3875] and [43.0737, 45.0000]
site set: build_site_grid(96/25, 119, 1/10): 14161 sites, 1830 orbits
float proposer: rounds 81, rows 5809, stopped 'converged: every placement carries its class threshold', objective 0.9816433566433445, thresholds (0.09090909090909091, 0.0), wall 332.9s, load ['1.36', '1.27', '1.01']
  float M at w0 = 1: 10.798077
exact decision on 296 rationalised atoms (scale 4096): total mass 11083/1024 = 10.8232421875; wall 2.6s
  Condition 1 atoms carry the declared symmetry: holds=True; 296 atoms closed under D4 about the centre
  Condition 2' mass below n0 w0 + n1 w1: holds=True; total 11083/1024 against 11 * 1 + 0 * 0 = 11
  Condition 3 net reaches pi/4: holds=True; final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000
  Condition 4 containment B(1 + D) < 1: holds=True; B = 9977/10000, D = 207107/90000000, B(1 + D) = 899996306539/900000000000
  Condition 5' class 0 carries w0: holds=True; least cell mass 4101/4096 at direction 0 over 49 cells, against w0 = 1
  Condition 5' class 1 carries w1: holds=True; class holds no square in this composition; 132 cells unswept
  minimum: class 0 over 49 cells: 4101/4096 at direction 0
  minimum: class 1 over 132 cells: None at direction None
refutes (11, 0): True; Conditions 1, 3, 4, 5' hold: True; failures []
claimed mass 11083/1024 = 10.8232421875; equal to the fraction: True; claimed least core 4101/4096, 296 atoms
VERDICT: Theorem C replays (refuted, exactly) on this run
```

### `summary-*.json` of the E.4 reader

```text
summary-delta-hl1-20.json: {"mode": "delta-hl1-20", "delta": "3/500", "floor": 6.103515625e-05, "nodes": 24381, "certified": 10960, "discarded": 1231, "failures": 0, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 0.2, "exact_seconds": 0.5, "exact_escapes_among_failures": 0, "exact_escapes_among_rejected_leaves": 0}
summary-delta-hl1-25.json: {"mode": "delta-hl1-25", "delta": "3/500", "floor": 6.103515625e-05, "nodes": 39515, "certified": 18004, "discarded": 1754, "failures": 0, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 0.5, "exact_seconds": 0.8, "exact_escapes_among_failures": 0, "exact_escapes_among_rejected_leaves": 0}
summary-delta-hl7-200.json: {"mode": "delta-hl7-200", "delta": "3/500", "floor": 6.103515625e-05, "nodes": 3291749, "certified": 187496, "discarded": 53159, "failures": 1405220, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 39.6, "exact_seconds": 10.2, "exact_escapes_among_failures": 162, "exact_escapes_among_rejected_leaves": 0}
summary-delta-hl9-200.json: {"mode": "delta-hl9-200", "delta": "3/500", "floor": 6.103515625e-05, "nodes": 29939, "certified": 13556, "discarded": 1414, "failures": 0, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 0.4, "exact_seconds": 0.6, "exact_escapes_among_failures": 0, "exact_escapes_among_rejected_leaves": 0}
summary-delta.json: {"mode": "delta", "delta": "3/500", "floor": 6.103515625e-05, "nodes": 24381, "certified": 10960, "discarded": 1231, "failures": 0, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 0.2, "exact_seconds": 0.5, "exact_escapes_among_failures": 0}
summary-lane-hl1-20.json: {"mode": "lane-hl1-20", "delta": "sqrt(4498641/125000000000)", "floor": 6.103515625e-05, "nodes": 24381, "certified": 10960, "discarded": 1231, "failures": 0, "exact_rejected_leaves": 0, "exact_rejected_discards": 0, "volume_ok": true, "float_seconds": 0.2, "exact_seconds": 0.5, "exact_escapes_among_failures": 0, "exact_escapes_among_rejected_leaves": 0}
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
