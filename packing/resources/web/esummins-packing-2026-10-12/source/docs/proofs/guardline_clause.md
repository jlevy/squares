# GUARD LINES — the chord-sum clause of the case-measure certificate: Theorem G, the verifier, the emitter, the Lean shape (A190, 2026-09-09)

Target (A190 BRIEF, PI 2026-09-09 ~22:30): A144's guard-line row (`attempts/A144-guard-lines/notes/spec.md`
§1–5, `lemmas_LINE.md` LINE-1/LINE-2, `code/guardline.py` `minchord_box`) had no certificate clause — A185's
`verify_case_v4.py` refused `guardlines` (exit 2) and no emitter wrote the field — while A188 showed that the 23
alive S01 pages and the 11 S03 pages are phantoms of exactly the kind the row kills: the LP's dual support puts
four unit chords across one axis-parallel line (side ≥ 4 > s0) and the atomic measure argument cannot see it.
Labels: [T] proved, [S] routine, [M] measured (`attempts/A190-guardline-clause`), [F] finding, [C] open.
Conventions as `boxed_windows.md`: container `C = [0,s]²`; a pose `π = (c, θ)`, `Q(π)` the closed unit square;
`t = tan(θ/2) ∈ [0,1]`; a `(t, c)`-box is `[t0,t1] × [x0,x1] × [y0,y1]`; a pose is admissible iff `Q(π) ⊆ C`.
A guard line `l` is `y = h` or `x = g` with a rational offset in `(0, s)`; `|l ∩ Q|` is the chord length.

## 0. Verdict

> **Theorem G [T].**  The certificate gains one field, `guardlines` — a finite list of axis-parallel lines `l`
> inside the container, each with a density `z_l ≥ 0` and a declared right-hand side `rhs_l` — and, optionally, a
> rational pose box `pbox_j` on each core.  The measure becomes `μ = Σ_k w_k δ_{p_k} + Σ_l z_l · H¹|_l`.  A PASS of
> `verify_case_v5` certifies Theorem W's (V1)/(V2)/(V3) for THIS `μ` together with
> `Σ_k w_k + Σ_l z_l · rhs*_l < b₄ = n − m + r_c`, where `rhs*_l = s − Σ_{j ∈ J_l} chord_lo(j, l)` is RE-DERIVED
> from the certificate's own data (`J_l` = the unattached cores with a positive lower chord, provably in pairwise
> distinct squares and in no window square).  Then no packing satisfies the node hypothesis.  A windowed square's
> chord enters ONLY through the measure side (its window walk lower-bounds `μ(Q)` by atoms + `Σ z_l · minchord`);
> an unattached core's square enters ONLY through `rhs*`; an attached core's square is counted by its window and
> enters `rhs*` not at all — so nothing is charged twice.  [C under v5 ONLY: v1, v3 and v4 are imported with their
> shas asserted and never edited; on a certificate without `guardlines` v5 is v4 byte-for-byte.]

## 1. The two lemmas the clause rests on

**Lemma LINE-1 (chord sum, OPEN chords) [T] (A144; scope corrected 2026-09-10 after the external review).**  If
`Q_1..Q_N` are closed unit squares with pairwise disjoint interiors in `[0,s]²` and `l` is an axis-parallel line
meeting the container, then `Σ_i |l ∩ int Q_i| ≤ s`, where `|l ∩ int Q_i|` is the OPEN chord (the length of
`l ∩ int Q_i`).
*Proof.*  Each `l ∩ int Q_i` is an open sub-interval of `l ∩ (0,s)²` (convexity of the open square); two of them
are disjoint because a common point would be interior to both squares; disjoint open intervals inside a segment
of length `s` have total length ≤ `s`. ∎
*Why the closed form is FALSE.*  With closed chords the statement fails whenever a square's EDGE lies on `l`: the
four unit squares tiling `[0,2]²` have closed chords of length 1 each on `y = 1`, sum 4 > 2.  A tilted square
meets `l` in a boundary point only at a vertex (closed chord 0), so open and closed chords differ exactly for
axis-parallel poses whose edge lies on `l`; `guardlines_v5.minchord` returns 0 for a box that admits such a pose
(the `t = 0 / t = 1` bins at distance `V ≥ a`).  For PAIRWISE DISJOINT CLOSED squares (the closed-disjoint family
of `closed_disjoint_bridge.md`, reached by the dilation transfer) the closed and open chords coincide up to the
endpoints and the closed form holds; the verifier does not rely on that and uses open chords throughout.

**Lemma MINCHORD [T] (A144 §2; `guardlines_v5.minchord`).**  For half-side `a`, `C = |cos θ|`, `S = |sin θ|`, `V`
the distance from the centre to `l`: `chord = max(0, min(2a/max(C,S), (a(C+S) − V)/(CS)))` (CH) — exact rational
in `t`.  It is antitone in `V`, independent of the coordinate along `l`, and depends on `θ` only through
`y = C + S ∈ [1, √2]`: `A(y) = 4a/(y + √(2−y²))` is increasing, and `B(y) = 2(ay − V)/(y² − 1)` has derivative of
the sign of `q(y) = −ay² + 2Vy − a` whose roots multiply to 1, so on `[1, √2]` `B` is decreasing or increasing-
then-decreasing and its minimum over a `y`-interval is at an endpoint.  Hence over a closed pose box the minimum
of the chord is `max(0, min(A(t0), A(t1), B(y(t0)), B(y(t1)), B(√2)·[45° in the bin]))` with `V` the largest
distance over the centre rectangle; `B(√2) = 2(√2 a − V)` is replaced by `2(√2_lo a − V)` with `√2_lo =
⌊√2·10²⁴⌋/10²⁴` (a lower bound; the "45° in the bin" test uses `[√2_lo − 1, √2_hi − 1] ∋ tan 22.5°`, so an extra
candidate can only lower the value); a zero-width bin is evaluated at its single `t`; at `y = 1` the one-sided
limit of `B` (`+∞`, `a`, `−∞` for `V <`, `=`, `> a`) is an infimum, hence a lower bound.  [M] The verifier's
primitive agrees with A144's `minchord_box` EXACTLY on 2,418 random boxes × lines (`code/test190.py`, the
cross-check in the commit log) and is never above the chord on 36,000 sampled poses.

## 2. The field and the bound objects

```
"hypotheses": { "cores": [ {kx, ky, tm, a, "pbox": {x0,x1,y0,y1,t0,t1}?}, ... ],      pbox optional, rational
                "nofams": [...], "polycores": [...], "windows": [...],                 (v1 / v3 / v4, unchanged)
                "guardlines": [ {"orient": "h"|"v", "off": q, "z": q, "rhs": q}, ... ] }
```

* `pbox_j` declares the hypothesis "some packed square has its pose in `pbox_j`" (the case tree's own hypothesis
  on that square; v1's "some square contains `K_j`" is its consequence).  The verifier BINDS it: the four corners
  of `K_j` pass A135's exact `point_in_all_poses` against `pbox_j` (HARD REJECT otherwise), so `K_j ⊆ Q(π)` for
  every `π ∈ pbox_j` is a theorem about the file and v1's exemption bridge is unchanged.
* `chord_lo(j, l) := max( |l ∩ K_j| , minchord(½, pbox_j, l) )` (the second term only with a `pbox`): a lower
  bound of `|l ∩ Q|` for ANY square `Q ⊇ K_j` (resp. with pose in `pbox_j`) — [T] by `K_j ⊆ Q` and Lemma MINCHORD.
* `J_l := { j ∉ im κ : chord_lo(j, l) > 0 }`.  Distinctness (HARD REJECT if it fails): for `i ≠ j ∈ J_l` the
  pose boxes are disjoint (one square has one pose) OR two corners of `K_i`, `K_j` are more than `√2` apart (no
  closed unit square, diameter `√2`, contains both); for `j ∈ J_l` and every window `i`, every piece of `W_i` is
  disjoint from `pbox_j` OR some corner of `K_j` is further than `√2/2` from every centre of the piece
  (`Q(π)` lies in the closed disc of radius `√2/2` about its centre).  All four tests are exact rational.
* `rhs*_l := s − Σ_{j ∈ J_l} chord_lo(j, l)`; HARD REJECT if `rhs_l > rhs*_l`; the verifier uses
  `rhs_eff = min(rhs_l, rhs*_l)`.

## 3. Theorem G and its proof

**Hypothesis H** (as `boxed_windows.md` §2): a packing `Q_1..Q_n` of pairwise disjoint closed unit squares in `C`
with (H1) an injective `σ` placing `pose(Q_σ(i)) ∈ W_i`; (H2') for every unattached core `j`: some `Q ⊇ K_j`, and
if `pbox_j` is declared, some `Q` with pose in `pbox_j` (which then contains `K_j`); (H3) no pose in a NO-family.

**Theorem G [T].**  Suppose (V1), (V2), (V3) of Theorem W hold for `μ = atoms + Σ_l z_l H¹|_l`, the `guardlines`
entries pass §2's checks, and (V4') `Σ_k w_k + Σ_l z_l rhs*_l < b₄`.  Then no packing satisfies H.

*Proof.*  Let `A = σ([r])`, `B` = the squares containing an unattached core, `U = B ∖ A` (the UNCOUNTED squares),
`F = [n] ∖ (A ∪ B)`.  Theorem W's (i)/(ii) give `μ(Q_k) ≥ 1` for `k ∈ A ∪ F` (they use only the exemption
geometry, which does not read the lines); write `Cnt = A ∪ F = [n] ∖ U`, `|Cnt| = n − |U| ≥ n − (m − r_c) = b₄`.
The squares are pairwise disjoint, so an atom lies in at most one of them: `Σ_{k∈Cnt} μ_atoms(Q_k) ≤ Σ_k w_k`.
For a line `l`, Lemma LINE-1 over ALL `n` squares gives `Σ_{k∈Cnt} |l ∩ Q_k| ≤ s − Σ_{k∈U} |l ∩ Q_k|`.  For
`j ∈ J_l` pick `Q(j) ⊇ K_j` (with pose in `pbox_j` when declared): the distinctness checks make `j ↦ Q(j)`
injective on `J_l` and put every `Q(j)` outside `A`, i.e. in `U`; so `Σ_{k∈U} |l ∩ Q_k| ≥ Σ_{j∈J_l} chord_lo(j, l)`
and `Σ_{k∈Cnt} |l ∩ Q_k| ≤ rhs*_l`.  Hence
`b₄ ≤ |Cnt| ≤ Σ_{k∈Cnt} μ(Q_k) ≤ Σ_k w_k + Σ_l z_l rhs*_l < b₄`, a contradiction. ∎

**No double counting [T].**  Each packed square is in exactly one of `U` (uncounted: its chord is subtracted
from `rhs*` through its core / pbox, and its mass is never required) or `Cnt` (counted: its mass — atoms AND the
line density it crosses — is required to be ≥ 1 by (V1)/(V2), and its chord is never subtracted).  A windowed
square is in `Cnt` whether or not it has an attached core; hence a core attached to a window never contributes
to `rhs*`, and a window's minimum chord over its window is NOT an rhs term: it enters as `z_l · minchord(box, l)`
on every sub-box of that window's walk (G3), which is a lower bound of the line part of `μ(Q(π))` for every `π`
in the sub-box.  Unattached cores that might sit inside a window square are refused, not counted twice.

**Relation to v1 / v4 [S].**  `guardlines = []` gives `μ` atomic, `rhs*` unused and Theorem W verbatim; `windows =
[]` gives A144's LINE-2/LINE-3 with `U` = the core squares and `b₄ = n − m`, the certificate the A144 spec §4
describes (its "cores[j].box" is this `pbox`).

## 4. The verifier (`verify_case_v5.py`, over v4 over v3 over v1) [S]

(G1) `rederive` as §2 at load time; (G2) the total printed and tested is `Σ w + Σ z·rhs_eff`; (G3) `VerifierV5`
subclasses A135's `VerifierV3` and overrides `covered` ONLY by computing `L = Σ_l z_l · minchord(½, sub-box, l)` in
Fractions on the verifier's own `(t, c)` sub-box (rationals from the integer scale), then calling the FROZEN
`covered` with `NEED` lowered to `NEED − ⌊L·WD⌋` (`WD` = v1's common weight denominator; the floor is conservative):
`atom_int ≥ NEED − ⌊L·WD⌋` implies `atom_mass + L ≥ need`.  A sub-box with `⌊L·WD⌋ ≥ NEED` is covered by the lines
alone.  `minchord` grows monotonically under bisection, so the walk terminates as before.  The same verifier
serves the free walk and every window walk (`make_verifier`), so (G3) applies to both clauses uniformly; exemption
is decided before mass (G4), so the guard clause never touches the core / NO-family / polygon disjuncts.  Witness
reports add the exact line chord at the sampled pose (`exact_mass_at`).  `--scale-weights` scales `z` with `w`.
Machine independence: the only irrational is `√2` through the fixed rational `√2_lo`; every decision is a
Fraction / integer comparison, so `--replay` is bit-identical across machines.  Exit 2 on any re-derivation or
distinctness failure.  [M] `test190.py`: a line-only certificate (4 densities `z = 3` at spacing 0.85, no atoms,
`n = 100`) PASSes with 0 atom checks and 240 line-only covers; one line alone FAILs with mass-0 holes; rhs above
`rhs*`, a core outside its `pbox`, two cores in one unit square are each refused; the re-derived `rhs*` on
Y0147's line with pin P2 and H's box equals A144's `469271/250000` exactly.

## 5. The LP column and the emitter (`lines190.py`, `emit190.py`, `run190.py`) [S]

(LINE-3, A144.)  In the covering LP a guard line is a COLUMN `z_l ≥ 0` with objective coefficient `rhs*_l` and
coefficient `|l ∩ Q_p|` in every placement row (A144's `guardlp.GuardModel`, injected into A57's `lpbox` without
editing it; the row coefficient uses the shrunk half-side `½ − EPS_GEO`, conservative on both sides).  Adding
columns can only lower `τ`; `τ < budget` still kills by the bridge above.  The emitter (A144's in-vitro path:
A135 exact cores on every box through `ExactHyp`, A57's warm start, 8 lines chosen by their offline violation on
the stored dual support plus the page's own best band line) writes `pbox_j` = the node's boxes (`x`, `y` exact
binary rationals of the record's floats; `t` through A57's outward `t_lo` / `t_hi`, clamped to `[0, 1]` — the same
superset A135's exact core is certified against), the exact cores (A170's rule: never smaller than the carried
one), `z_l` scaled and rounded UP with the atom weights, `rhs_l = rhs*_l` exact; then `verify_case_v5` with A57's
witness-feedback loop (witness placements fed back as extra rows, the line columns kept) inside the 1,500 s wall.

**The line grid [S/F].**  Per node: A144's family (pin core edges and midlines, `K'(H)`'s extreme and mid `x`/`y`,
the container eighths) plus the container SIXTEENTHS, plus A188's pin-row / pin-column lines at the quartiles of
the pins' full-chord interval, plus the page's own best band line from `consumer188.jsonl` (the `c` maximising
`minchord(H, l)`), deduplicated and capped at 64; the 8 with the largest offline violation on the stored support
carry the LP, the consumer's line always among them.  Why this is complete enough for the S01/S03 phantoms: the
row kills a support iff some line has `Σ_p y_p |l ∩ Q_p| > rhs*(l)`, a condition open in the offset; on the S01
lock the four unit-chord bands (half-width ≥ `γ(θ) ≥ 0.207` each, `local_certificate_s01.md` Lemma CHORD-BAND)
intersect in an interval of length 0.805 on the representative, and on a page the pin band `[y_p − ½ + h, y_p + ½
− h]` meets H's band in an interval of length ≥ `2(γ(θ_max) − box half-height) ≥ 0.27` (box height 0.14, tilt bins
≤ 14°), against a sixteenth spacing of 0.242 and the consumer's line placed at its centre.  What the grid cannot
promise is a violation the LP's NEXT support does not have: A144's finding that a deep offline violation is
necessary, not sufficient, stands (the LP may re-optimise onto a support the family does not cut).

## 6. The n-general form [T]

Nothing above uses `n = 11`, `s0` or the class.  For any `n`, side `s`, any node with `m` cores, `r` windows and
`b₄ = n − m + r_c`, Theorem G holds for any finite family of axis-parallel lines inside the container.  The row is
the LENGTH-charging sibling of the slot-crowd rows (A94/A109) and subsumes A121's `st4`: a stack of `⌈√n⌉`
axis-aligned unit squares against a wall gives `s ≥ ⌈√n⌉` on one line, and the LP finds it with only SOME of the
squares pinned (A144 §6).

## 7. Lean shape (A144 §5 + `boxed_windows.md` §5; no new axiom)

```lean
structure GuardLine where (horizontal : Bool) (offset : ℚ)
def chordLen (a : ℝ) (c : ℝ×ℝ) (θ : ℝ) (l : GuardLine) : ℝ := (volume (l.param ⁻¹' Q a c θ)).toReal
/-- LINE-1 -/
theorem chord_sum_le_side {N} (s) (Q : Fin N → Set (ℝ×ℝ)) (hsq : ∀ i, IsUnitSquare (Q i))
    (hsub : ∀ i, Q i ⊆ Icc 0 s ×ˢ Icc 0 s) (hdisj : Pairwise fun i j => interior (Q i) ∩ interior (Q j) = ∅)
    (l : GuardLine) (hl : l.offset ∈ Icc 0 s) : (∑ i, chordLen (1/2) (centre (Q i)) (tilt (Q i)) l) ≤ s
/-- the five-point checker and its soundness (Lemma MINCHORD) -/
def checkMinChordBox (a : ℚ) (B : ParamBox) (l : GuardLine) (m : ℚ) : Bool := ...
theorem minchord_of_box (h : checkMinChordBox a B l m = true) : ∀ c θ, InBox B c θ → (m : ℝ) ≤ chordLen a c θ l
/-- the distinctness checkers -/
def checkBoxesDisjoint (P Q : ParamBox) : Bool := ...        -- one pose per square
def checkCornersFar (K K' : Core) : Bool := ...              -- squared distance > 2 => no common unit square
def checkCoreOffPiece (K : Core) (p : Piece) : Bool := ...   -- corner further than √2/2 from every centre
theorem distinct_of_check ... ; theorem offWindow_of_check ...
/-- the measure with line densities, and the mass lower bound the walk uses (G3) -/
def LineMeasure (μ : AtomicMeasure) (ls : List (GuardLine × ℚ)) : Measure (ℝ×ℝ)
theorem lineMass_ge (h : checkMinChordBox (1/2) B l m = true) : ∀ π ∈ B, z * m ≤ z * chordLen (1/2) π.1 π.2 l
/-- Theorem G -/
theorem guarded_dead (n) (s) (μ) (cores) (pboxes) (nofams) (polys) (windows) (lines)
    (hV1 hV2 hV3 : as windowed_dead, with μ := LineMeasure μ lines and checkCover using lineMass_ge)
    (hbind : ∀ j, pboxes j = some B → ∀ p ∈ corners (cores j), checkPointInBox p B = true)
    (hdist : ∀ l, Pairwise distinct on J l ∧ ∀ j ∈ J l, ∀ w, offWindow (cores j) (pboxes j) w)
    (hV4 : μ.total + ∑ l, z l * rhsStar l < n - cores.length + attached.length) :
    ¬ ∃ Q : Fin n → Set (ℝ×ℝ), IsPacking s Q ∧ NodeHyp Q cores pboxes nofams windows
```
Obligations: `chord_sum_le_side` (LINE-1: `Set.Icc_inter_Icc`, `Real.volume_Icc`, `measure_biUnion_finset` with
a.e.-disjointness of the chords); `chordLen_eq` ((CH) once, the only transcendental step); `chordLen_antitone_offset`,
`chord_A_mono`, `chord_B_endpoint_min`, `y_range_of_tilt` (A144's seven supporting lemmas); `minchord_of_box`;
the three distinctness soundness lemmas (elementary: one pose per square; diameter `√2`; `Q(π) ⊆ closedBall c (√2/2)`);
`lineMass_ge`; `windowCover_sound` / `coreInPiece_sound` / `sum_measure_le_total` from `boxed_windows.md` re-run with
`LineMeasure` (the atoms' part unchanged, the line part by `lineMass_ge` and `chord_sum_le_side`); the counting in
§3 as `Finset.card` arithmetic.  Roster expected: 3 theorems + 1 `Bool` five-point checker + 3 `Bool` distinctness
checkers + ~10 supporting lemmas, **0 new axioms**; `core_meet_same_square` (T5) untouched.

## 8. What the frozen chain sees [T]

A v5 kill is [C] under v5 only.  v1 (`521cb01f…`), v3 (`f578a8c9…`) and v4 (`b36acb01…`) are imported with their
shas asserted at import and never copied or edited; a certificate without `guardlines` runs the identical v4 code
path (A190 regression `results/regress190.json`: identical verdicts and box-tree statistics on the v1 corpus and on
every A185 v4 certificate).
