# BOXED WINDOWS — the per-square pose-window clause of the case-measure certificate (A185, 2026-09-09)

Target (A185 BRIEF, PI 2026-09-09 ~19:40): the case-measure certificate (v1 `verify_case.py` sha `521cb01f…`,
`docs/proofs/local_certificate.md`; v3 = A135's polygon-core clause, sha `f578a8c9…`) constrains the adversary only
through the FREE squares; a boxed square enters only through its core, so a node with every square boxed has budget
`n − #cores = 0` and a vacuous certificate.  The clause below confines each boxed square to its WINDOW (the union of
its surviving pieces) and charges it one unit of measure at every pose of the window.  Labels: [T] proved, [S]
routine, [M] measured (`attempts/A185-boxed-windows-clause`), [F] finding, [C] open.  Notation as
`local_certificate.md`: container `C = [0,s]²`; a pose `π = (c, θ)`, `Q(π)` the closed unit square with centre `c`
and edge direction `θ`; `t = tan(θ/2) ∈ [0,1]` (θ mod π/2, v1's parametrisation, cos/sin rational in t); a
`(t, c)`-box is `[t0,t1] × [x0,x1] × [y0,y1]`; a pose is ADMISSIBLE iff `Q(π) ⊆ C`.

## 0. Verdict

> **Theorem W [T].**  The certificate gains one field, `windows` — per boxed square a finite list of `(t, c)`-boxes
> (its pieces) and, optionally, the index of its core — and one obligation per window: every admissible pose in
> the window whose square meets no core ATTACHED TO ANOTHER window (and lies in no NO-family) has `μ(Q) ≥ 1`.  The
> budget becomes `n − #cores + #(windows with a core)`, i.e. `n` when every boxed square is windowed and cored.
> Cores and windows combine WITHOUT double counting: the mass inside an attached core lies in every pose of its own
> window and is counted there and nowhere else (the disjointness of the packing), and an attached core exempts
> only the poses of OTHER squares (free poses, and other windows' poses).  The free clause is skipped when the
> count of free squares is `≤ 0`.  [F] A node whose windows all carry a non-empty `K'` has `τ ≤ #windows +
> τ_free` (one atom per `K'` covers a whole window), so a window kill must come from FRACTIONAL sharing between
> overlapping pose sets (§3, example): the clause is not vacuous at budget 0, but it is not a free lunch either.

## 1. The field `windows`

```
"hypotheses": { "cores": [...], "nofams": [...], "polycores": [...],           (v1 / v3, unchanged)
                "windows": [ { "name": "H", "core": 0 | null,
                               "pieces": [ {"x0","x1","y0","y1","t0","t1"}, ... ],   rational strings
                               "deg": [th0, th1] } , ... ] }
"budget": n − #cores            (v1's field, unchanged: v1's loader enforces it)
```

* `pieces` are `(t, c)`-boxes in `t = tan(θ/2) ∈ [0,1]` — SETTLED: the same coordinate v1's tree bisects, cos and
  sin rational, no wrap-around (a tilt range in degrees `[th0, th1] ⊆ [0°, 90°]` maps to `[t_lo(th0), t_hi(th1)]`
  with A57's outward rounding; a range crossing 0°/90° is two pieces).  `deg` is for humans only and is ignored.
* `core` (optional) names a v1 core; the attachment `κ` must be injective.  The verifier RE-DERIVES the link: the
  four corners of `cores[κ(i)]` pass A135's exact `point_in_all_poses` against EVERY piece of window `i` (HARD
  REJECT otherwise, as A135's (P1)/(P2)).  So `K_κ(i) ⊆ Q(π)` for all `π ∈ W_i` is a THEOREM about the file, not a
  hypothesis; the emitter's `grow_core` is data.
* The effective budget is `b₄ = n − m + r_c` with `m = #cores`, `r = #windows`, `r_c = #attached windows`; the
  number of FREE squares is bounded below by `f = n − r − (m − r_c)`; the free clause runs iff `f > 0`.

## 2. Theorem W and its proof

**Data.**  A finite non-negative atomic measure `μ` on `C` with `μ(C) = τ`; NO-families `𝒩`; cores `K_1..K_m`
(rational squares); polygon cores each refining one `K_j` (v3); windows `W_1..W_r ⊆ Π` (finite unions of
`(t, c)`-boxes) with an injective partial attachment `κ : [r] ⇀ [m]`.  Write `E₀(π)` ("free-exempt") for: `π` in a
NO-family, or `Q(π)` meets some `K_j` or a polygon core; and `E_i(π)` ("window-i-exempt") for: `π` in a NO-family, or
`Q(π)` meets `K_κ(i')` (or a polygon core refining it) for some `i' ≠ i` with `κ(i')` defined.

**Hypothesis H of a node** (what the certificate is conditional on).  A packing `Q_1..Q_n` of pairwise disjoint
closed unit squares in `C` (v1's convention; the dilation of `k0_route.md` §4.1 supplies disjointness of the closed
squares for side `< s`) such that (H1) there is an INJECTIVE `σ : [r] → [n]` with `pose(Q_σ(i)) ∈ W_i`; (H2) every
UNATTACHED core `K_j` (`j ∉ im κ`) is contained in some `Q`; (H3) no `Q` has its pose in a NO-family.

**Theorem W [T].**  Suppose
(V1) every admissible `π` with `¬E₀(π)` has `μ(Q(π)) ≥ 1` — required only if `f = n − r − (m − r_c) > 0`;
(V2) for every `i ∈ [r]`, every admissible `π ∈ W_i` with `¬E_i(π)` has `μ(Q(π)) ≥ 1`;
(V3) for every attached `i`, `K_κ(i) ⊆ Q(π)` for every `π ∈ W_i`, and every polygon core refining `K_κ(i)` lies in
`Q(π)` for every `π ∈ W_i` (the verifier checks each polygon's vertices against every piece of window `i`);
(V4) `τ < b₄ = n − m + r_c`.
Then no packing satisfies H.

*Proof.*  Let `A = σ([r])` (`|A| = r` by injectivity) and `B` = the set of squares containing some unattached core
(`|B| ≤ m − r_c` by (H2)); `F = [n] ∖ (A ∪ B)` has `|F| ≥ n − r − (m − r_c) = f`.
(i) *Windowed squares.*  Fix `i` and `π = pose(Q_σ(i)) ∈ W_i`.  `π` is admissible and not in a NO-family (H3).  If
`Q_σ(i)` met `K_κ(i')` (or a polygon core refining it) for some attached `i' ≠ i`, then by (V3) that set is inside
`Q_σ(i')` and `σ(i') ≠ σ(i)`, so two distinct squares of the packing would meet — contradiction.  Hence `¬E_i(π)`
and, by (V2), `μ(Q_σ(i)) ≥ 1`.
(ii) *Free squares* (only if `f > 0`).  Fix `j ∈ F`; `π = pose(Q_j)` is admissible, not in a NO-family.  `Q_j`
meets no attached core (it is `⊆ Q_σ(i)`, disjoint from `Q_j` as `j ∉ A`) and no unattached core `K` (some `Q_0 ⊇ K`
by (H2); `Q_j ≠ Q_0` because `j ∉ B`; so `Q_j ∩ K ⊆ Q_j ∩ Q_0 = ∅`), and no polygon core (each lies inside its
core's containing square by A135's (P1)/(P2)).  Hence `¬E₀(π)` and, by (V1), `μ(Q_j) ≥ 1`.
(iii) *Counting.*  The `Q_k` are pairwise disjoint, so `τ = μ(C) ≥ Σ_k μ(Q_k) ≥ Σ_{k ∈ A} + Σ_{k ∈ F} ≥ r + f =
n − m + r_c = b₄`, contradicting (V4).  When `f ≤ 0` the free sum is dropped and `Σ_{k∈A} ≥ r ≥ r + f = b₄` still
holds.  ∎

**No double counting [T].**  Each square of the packing is charged once, in exactly one of (i)/(ii); the mass an
attached core carries lies inside `Q_σ(i)` only (disjointness), so it serves window `i` and nothing else; an attached
core exempts poses of OTHER squares only (`E_i` excludes `κ(i)`; `E₀` is used only for squares outside `A`).  A
window's own core never exempts its own poses — the verifier removes `cores[κ(i)]` (and its polygon cores) from
the exemption list while walking window `i` — and UNATTACHED cores do not exempt window poses at all (a windowed
square may itself contain an unattached core).

**Relation to v1 [S].**  With `windows = []`: `r = r_c = 0`, `b₄ = n − m`, (V2)/(V3) are empty, `f = n − m`, and
Theorem W is v1's claim verbatim.  With every boxed square windowed and cored (`r = r_c = m`): `b₄ = n`,
`f = n − m` — the free clause is v1's with the same cores, plus one window obligation per boxed square.

**Soundness of the verifier's window walk [S].**  For a piece `[t0,t1] × [x0,x1] × [y0,y1]` the integer box is
`[⌊t0·2^K⌋, ⌈t1·2^K⌉] × [⌊x0·D⌋, ⌈x1·D⌉] × …` — rounded OUTWARD, a superset — then v1's own tree (`clip_int` to the
admissible region, `exempt` with the reduced core list, `covered`, bisection to `--depth`) runs on it unchanged.
Every predicate is the frozen one; the only new exact test is (V3) by `point_in_all_poses` (A135).

## 3. Why the clause can kill at budget 0, and when it cannot [F]

If every window `i` has a non-empty exact core `K'_i = ∩_{π∈W_i} Q(π)` (every alive node: the roles invariant),
`μ = Σ_i δ_{p_i}` with `p_i ∈ K'_i` satisfies (V2) at `τ = r`: the LP value is `≤ r + τ_free`, never above budget
by the windows alone.  A kill needs `τ < r + f`, i.e. FRACTIONAL sharing.  Example (`n = 2`, both windowed, `f = 0`):
`W_1 = {Q_a}`, `W_2 = {Q_b, Q_b'}` with `Q_b ∩ Q_b' = K'_2` disjoint from `Q_a` but `Q_a ∩ Q_b ≠ ∅ ≠ Q_a ∩ Q_b'`.
Atoms of weight ½ at a point of `Q_a ∩ Q_b`, of `Q_a ∩ Q_b'` and of `K'_2` give every pose ≥ 1 at `τ = 3/2 < 2`
— and indeed no packing exists (square 2 meets `Q_a` in both its poses) although `K'_1 ∩ K'_2 = ∅`, so the roles
invariant (shared point ⇒ same square) does not see it.  The clause is the LP relaxation of "the windows' pose sets
admit a pairwise-disjoint selection", of which A182's geometry tests only the always-overlap case (`ovl_roles`).

## 4. The n-general form

Nothing above uses `n = 11`, `s0`, or the class: for any `n`, side `s`, any node whose hypothesis names `r`
squares by pose windows (finite unions of `(t, c)`-boxes) and `m` cores, Theorem W applies with `b₄ = n − m + r_c`.
At a k0 cascade node (A168/A181/A183) the windows are the roles' surviving pieces and the attached cores are
A183's `grow_core` squares; at an A182 assignment leaf they are the journal's `capture[role].pieces` (the fixed
point of the normalisation) with the exact core of the pieces' bounding box where one exists (`core: null` else,
then the square is windowed but not cored: it counts in `r`, not in `r_c`).

## 5. Lean shape (no new axiom; the style of A144 §5 / A135)

```lean
structure Piece where (t0 t1 x0 x1 y0 y1 : ℚ)                 -- a (t,c)-box, t = tan(θ/2) ∈ [0,1]
structure Window where (pieces : List Piece) (core : Option ℕ)
/-- the exact box-tree checker of v1 over one piece with the reduced core list (Bool) -/
def checkWindowCover (μ : AtomicMeasure) (cores : List Core) (nofams : List NoFam)
    (polys : List PolyCore) (skip : Option ℕ) (p : Piece) (depth : ℕ) : Bool := ...
/-- A135's checker: the four corners of `K` lie in every pose of the piece -/
def checkCoreInPiece (K : Core) (p : Piece) : Bool := ...

theorem windowCover_sound (h : checkWindowCover μ cores nofams polys skip p depth = true) :
    ∀ π, InPiece p π → Admissible s π → ¬ ExemptExcept skip cores nofams polys π → 1 ≤ μ.measure (Q π)
theorem coreInPiece_sound (h : checkCoreInPiece K p = true) : ∀ π, InPiece p π → K.square ⊆ Q π
theorem sum_measure_le_total {N : ℕ} (Q : Fin N → Set (ℝ×ℝ)) (hdisj : Pairwise (Disjoint on Q))
    (hsub : ∀ k, Q k ⊆ C) : ∑ k, μ.measure (Q k) ≤ μ.measure C
theorem windowed_dead (n : ℕ) (s : ℝ) (μ) (cores) (nofams) (polys) (windows : List Window)
    (hV1 : 0 < freeCount n cores windows → checkFreeCover μ cores nofams polys depth = true)
    (hV2 : ∀ i p, p ∈ (windows.get i).pieces →
        checkWindowCover μ cores nofams polys (windows.get i).core p depth = true)
    (hV3 : ∀ i j, (windows.get i).core = some j →
        ∀ p ∈ (windows.get i).pieces, checkCoreInPiece (cores.get j) p = true)
    (hinj : (windows.filterMap Window.core).Nodup)
    (hV4 : μ.total < n - cores.length + (windows.filterMap Window.core).length) :
    ¬ ∃ (Q : Fin n → Set (ℝ×ℝ)), IsPacking s Q ∧ NodeHyp Q cores nofams windows
```
Obligations: `windowCover_sound` is v1's cover soundness (A139's `localDead_of_certOk` machinery over `t`) with
the exemption list a parameter; `coreInPiece_sound` is A135's `checkVertexInPBox_sound` applied to four points;
`sum_measure_le_total` is `MeasureTheory.measure_biUnion_finset` for pairwise disjoint measurable sets; the
counting is `Finset.card` arithmetic on `A`, `B`, `F` as in §2.  Roster expected: 4 theorems, 2 Bool checkers,
0 new axioms; `core_meet_same_square` (T5) untouched.

## 6. What the frozen chain sees [T]
A v4 kill is [C] under v4 only.  v1 and v3 are imported, never copied; their shas are asserted at import
(`521cb01f…`, `f578a8c9…`); a certificate without `windows` runs the identical v1 code path (A185 regression:
identical verdict and identical box-tree statistics on 100 v1 certificates).
