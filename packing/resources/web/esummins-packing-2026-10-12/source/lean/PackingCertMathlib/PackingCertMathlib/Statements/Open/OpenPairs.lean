import PackingCertMathlib.Statements.Open.LockedWall

/-!
# -- OPEN: OPEN PAIRS — the factorised miss-O test, the wedge notch, the common-tilt exchange, the
# non-ADJ count, the slab — A263

`docs/proofs/open_pairs.md`.  A260 left the room of an OPEN PAIR whose two touchers have DIFFERENT
tilts as a coupled certificate (≈ 50 CPU-h per open wall).  This file carries the pieces that make it
three 4-parameter jobs, and the leftovers of the non-ADJ family and of the tilt slab.

**What is a theorem here.**
* `principal_normal` [T]: a square missing `O` has `(q − O)·n ≥ ½` for the LARGEST of its four
  edge-normal values; so A259's case (i) (`n = −v`) carries `(q − O)·(−v) ≥ (q − O)·u` and case (ii)
  (`n = u`) the reverse — the PRINCIPAL-NORMAL clip.  Without it the two-square corner factor P2 is
  false (open_pairs.md §2.2).
* `clip_mono` [T]: in the corner frame the (i)-clip equals `q·(−v−u) + s sin ψ`, the (ii)-clip
  `q·(u+v) − s sin ψ`: each is nondecreasing in `s` on the half of the tilt range where it is imposed
  (`sin ψ ≥ 0` for (i), `≤ 0` for (ii)), so the certificate at `s_max` covers every `s ≤ s_max`.
* `wedge_depth_common` [T]: WEDGE-NOTCH's principal depth `[c₁ sin(φ_W − ψ) + sin φ_W (k₁ − γ cos φ₁)]
  / cos(φ_W − φ₁)` reduces at common tilt `φ` and `ψ = φ` (`k₁ = 0`, `γ = e`) to `−e g c`: A260's
  OPEN-TOOTH depth `c (1 − e g)`.
* `factor_cover` [T]: the cover — a square that misses `O` at a corner violates P2, or WE, or WS
  (two squares, four parameters each), from the region split of its wall-nearest vertex.
* `nonadj_free_meeter` [T]: a slot whose ring meeters are only the two box meeters `{W, S′}` needs a
  THIRD, non-ring meeter under FAMILY-STUCK (`|M(Π)| > |Π|` for `Π = {slot, box}`).
* `openPairs_excludes`, `k0_value_of_factors` [T from `factor_pierce`]: the count and the chain.

**What is not.**
* `factor_pierce` [T-computed pending + C]: every free square of a hybrid normal ring (tilts of the two
  touchers of a wall INDEPENDENT) contains `O`.  Reduction [T] (this file); the three factor
  certificates P2 / WE / WS run detached (`run263.sh chain`, own verifier `verify263`); all-ADJ, shift
  `e ≤ ½`.  On the non-ADJ family (`e ≤ 1.2`) the statement is FALSE for wide gaps as a bare-ring
  statement (open_pairs.md §3.2) and the exclusion there is the structure lemma §3.3 [C].
* `slab_cube` -- DISCHARGED (A264, 2026-09-22): the all-near-flat cube `(0, 0.703°)⁴` of the mixed patterns
  is excluded by the theorem `slab_cube_264` (ThreeLemmas.lean, three_lemmas.md §3); the former axiom is removed.
-/

namespace PackingCert.S11.OpenLemmas.OpenPairs

open Set PackingCert.S11.OpenLemmas

/-- **PRINCIPAL NORMAL** [T]: if `max(x, y) ≥ ½` (the two candidate normals `−v`, `u` of a square missing
`O`), then `x ≥ ½ ∧ x ≥ y` or `y ≥ ½ ∧ y ≥ x`. -/
theorem principal_normal (x y : ℝ) (h : (1 : ℝ) / 2 ≤ max x y) :
    ((1 : ℝ) / 2 ≤ x ∧ y ≤ x) ∨ ((1 : ℝ) / 2 ≤ y ∧ x ≤ y) := by
  rcases le_total y x with hxy | hxy
  · left; exact ⟨by simpa [max_eq_left hxy] using h, hxy⟩
  · right; exact ⟨by simpa [max_eq_right hxy] using h, hxy⟩

/-- **The clips relax as `s` grows** [T]: `(q − O)·(−v − u) = q·(−v−u) + s·S` with `S = sin ψ ≥ 0`, and
`(q − O)·(u + v) = q·(u+v) − s·S` with `S ≤ 0`; both are nondecreasing in `s`. -/
theorem clip_mono (s t a S : ℝ) (hst : s ≤ t) :
    (0 ≤ S → a + s * S ≤ a + t * S) ∧ (S ≤ 0 → a - s * S ≤ a - t * S) := by
  constructor
  · intro hS; nlinarith
  · intro hS; nlinarith

/-- **WEDGE-NOTCH at common tilt** [T]: with `φ_W = φ₁ = φ`, `ψ = φ`, `k₁ = 0`, `γ = e` the principal depth
excess is `−e g c`, i.e. the depth is `c (1 − e g)` (A260's OPEN-TOOTH). -/
theorem wedge_depth_common (c g e : ℝ) :
    (c * 0 + g * (0 - e * c)) / 1 = -(e * g * c) ∧ c + (c * 0 + g * (0 - e * c)) / 1 = c * (1 - e * g) := by
  constructor <;> ring

/-- **The cover** [T]: a miss at a corner is one of the three factor events.  `i`, `ii` are A259's two cases
(after the principal-normal clip), `R` = "the miss-vertex lies over W's RIGHT region", `L` = "over S′'s LEFT
region"; P2 := (i ∧ R) ∨ (ii ∧ L), WE := i ∧ ¬R, WS := ii ∧ ¬L. -/
theorem factor_cover (i ii R L : Prop) (h : i ∨ ii) :
    ((i ∧ R) ∨ (ii ∧ L)) ∨ (i ∧ ¬ R) ∨ (ii ∧ ¬ L) := by
  by_cases hR : R <;> by_cases hL : L <;> rcases h with hi | hii <;> tauto

/-- **Non-ADJ needs a free meeter** [T]: if the meeters of `Π = {slot, box}` inside the ring are exactly the
box's two meeters and FAMILY-STUCK demands `|M(Π)| > |Π| = 2`, some meeter is not a ring square. -/
theorem nonadj_free_meeter {α : Type*} [DecidableEq α] (M ring : Finset α) (W S' : α) (hWS : W ≠ S')
    (hring : M ∩ ring = {W, S'}) (hfs : 2 < M.card) : ∃ x ∈ M, x ∉ ring := by
  by_contra hcon
  have hsub : M ⊆ ring := by
    intro x hx
    by_contra hxr
    exact hcon ⟨x, hx, hxr⟩
  have hM : M ∩ ring = M := Finset.inter_eq_left.mpr hsub
  rw [hM] at hring
  rw [hring, Finset.card_pair hWS] at hfs
  omega

/-- **FACTOR-PIERCE** [T-computed pending + C] (open_pairs.md §2, §6): on the window every non-ring square of
a packing of 11 that contains a hybrid normal ring — the two touchers of a wall at INDEPENDENT tilts —
contains the container centre.  [T] the reduction to P2 ∧ WE ∧ WS; [T-computed] when the three detached
certificate chains end with 0 OPEN and `verify263` reports bad = 0 (all-ADJ, `e ≤ ½`); [C] on the non-ADJ
family, where the bare-ring statement fails and open_pairs.md §3.3 must take over. -/
axiom factor_pierce (s : ℝ) (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q)
    (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (hring : HasNormalRing 11 4 s Q) :
    ∃ ι : Fin 8 → Fin 11, ∀ j, j ∉ Set.range ι → ((s / 2, s / 2) : RP) ∈ interior (Q j)

/-- **OPEN-PAIRS excludes** [T from `factor_pierce`]: a pierced pocket holds one square, `8 + 1 < 11`. -/
theorem openPairs_excludes (s : ℝ) (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q) : ¬ HasNormalRing 11 4 s Q := by
  intro hring
  obtain ⟨ι, hι⟩ := factor_pierce s Q hP hlo hhi hring
  have := NormalRoom.normalRoom_count 11 s Q hP ι hι
  omega

/-- **The chain to the value form** [T from `factor_pierce` and A258's `normal_ring` [C]]. -/
theorem k0_value_of_factors (s : ℝ) (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (hall : ∀ Q, IsPacking 11 s Q → FamilyStuckN 11 4 s Q) : ¬ ∃ Q, IsPacking 11 s Q := by
  refine normal_excludes_value 11 4 s ?_ ?_ (fun Q hQ => openPairs_excludes s hlo hhi Q hQ) hall
  · norm_num; linarith
  · norm_num; linarith

/- **SLAB-CUBE**: formerly the axiom `slab_cube` on the opaque `SlabCubeRing` (A263); discharged by the theorem
`slab_cube_264` (ThreeLemmas.lean, A264) and removed on 2026-09-23 so the audit no longer lists it. -/

#print axioms principal_normal
#print axioms clip_mono
#print axioms wedge_depth_common
#print axioms factor_cover
#print axioms nonadj_free_meeter
#print axioms openPairs_excludes
#print axioms k0_value_of_factors

end PackingCert.S11.OpenLemmas.OpenPairs
