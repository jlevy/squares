import PackingCertMathlib.Statements.Open.CentreDisc

/-!
# -- OPEN: PEEL — the onion inequality `s ≥ 2 + s(n − 4(m − 2))` — A254

`docs/proofs/peel.md`.  Setting: `n` unit squares in `[0, s]²`, `m = ⌈√n⌉`, `m − 1 < s < m`.

**What is a theorem here** (any `n`, any `s`).
* `core_fits` [T]: the CORE squares of a packing at side `s` (those inside `[1, s − 1]²`,
  `IsCore`, A236) translate by `(−1, −1)` to a packing at side `s − 2`: if `k` of the squares are
  core then `Fits k (s − 2)`.
* `peel_no_straddler` [T]: PEEL-0.  If at most `B` squares of a packing are outside the core
  (in the flush limit: the band squares, `B ≤ 4(m − 2)` by `band_count`), then
  `Fits (n − B) (s − 2)`; with a lower bound `σ ≤ s(n − B)` this is `σ + 2 ≤ s`
  (`peel_side_bound`).  The tight flush pinwheel (four `1 × (m − 2)` wall blocks; HOLE-ONE is
  `m = 4`, `s(2) = 2`) is the case `B = 4(m − 2)`.
* `peel_inner_count` [T]: with `n = m² − k`, `k ≤ 6`, the inner count is `≥ (m − 2)² − 2`, so
  Nagamochi's `s(j² − 2) = j` gives `s ≥ m`: no tight pinwheel anywhere below `m`.

**What is not.**
* `band_count` [T-prose] (peel.md §2.1; A236 BAND-FLUSH + the corner-box claim count): at a side
  in `(m − 1, m)`, `s > 2 + √2`, at most `4(m − 2)` squares are band squares.
* `only_ring` [C] (the PI's ONLY-RING(n), 2026-09-20): a family-stuck packing below `m` contains
  the ring.  `FamilyStuckN`, `HasRing` are opaque (peel.md §1 defines them).
* `ring_peel` [C] (MONOTONE-ROOM(n)): the pocket of a ring holds no more than the hole of its
  flush limit, i.e. the non-ring squares fit at side `s − 2`.  Proved only AT the tight flush
  limit and, for `m = 4`, on a non-effective neighbourhood of it (upper semicontinuity).
* `peel_excludes` [T from the two axioms]: no family-stuck packing at a side `s < 2 + s(n')`.

**Status (2026-09-20).**  `core_fits`, `peel_no_straddler`, `peel_side_bound`,
`peel_inner_count`, `peel_excludes`: theorems; `band_count`: axiom [T-prose]; `only_ring`,
`ring_peel`: axioms [C].
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The translation `p ↦ p + (−1, −1)` of the plane. -/
noncomputable def peelShift : RP ≃ₜ RP := Homeomorph.addRight ((-1 : ℝ), (-1 : ℝ))

theorem peelShift_apply (p : RP) : peelShift p = (p.1 - 1, p.2 - 1) := by
  change p + ((-1 : ℝ), (-1 : ℝ)) = (p.1 - 1, p.2 - 1)
  ext <;> simp [sub_eq_add_neg]

theorem peelShift_sqSet (p0 e : RP) : peelShift '' sqSet p0 e = sqSet (p0.1 - 1, p0.2 - 1) e := by
  ext q
  constructor
  · rintro ⟨p, ⟨a, b, ha0, ha1, hb0, hb1, rfl⟩, rfl⟩
    refine ⟨a, b, ha0, ha1, hb0, hb1, ?_⟩
    rw [peelShift_apply]
    simp only [aff]
    ext <;> simp <;> ring
  · rintro ⟨a, b, ha0, ha1, hb0, hb1, rfl⟩
    refine ⟨aff p0 e a b, ⟨a, b, ha0, ha1, hb0, hb1, rfl⟩, ?_⟩
    rw [peelShift_apply]
    simp only [aff]
    ext <;> simp <;> ring

/-- **CORE-FITS** [T].  The core squares of a packing at side `s` form, after the translation
`(−1, −1)`, a packing at side `s − 2`. -/
theorem core_fits (n k : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (ι : Fin k → Fin n) (hι : Function.Injective ι) (hcore : ∀ j, IsCore s (Q (ι j))) :
    Fits k (s - 2) := by
  refine ⟨fun j => peelShift '' Q (ι j), ?_, ?_, ?_⟩
  · intro j
    obtain ⟨p0, e, he, hS⟩ := hP.unit (ι j)
    exact ⟨(p0.1 - 1, p0.2 - 1), e, he, by rw [hS, peelShift_sqSet]⟩
  · rintro j _ ⟨p, hp, rfl⟩
    have h := hcore j hp
    simp only [centreClosed, container, mem_prod, mem_Icc] at h ⊢
    rw [peelShift_apply]
    constructor <;> constructor <;> simp <;> linarith [h.1.1, h.1.2, h.2.1, h.2.2]
  · intro i j hij
    have hne : ι i ≠ ι j := fun h => hij (hι h)
    have hd := hP.interiorDisjoint (ι i) (ι j) hne
    rw [← peelShift.image_interior, ← peelShift.image_interior]
    exact (Set.disjoint_image_iff peelShift.injective).2 hd

/-- **PEEL-0** [T]: a packing with `k` core squares at side `s`, and any proved lower bound
`σ ≤ s(k)` (in the form: `Fits k t → σ ≤ t`), has `σ + 2 ≤ s`. -/
theorem peel_side_bound (n k : ℕ) (s σ : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (ι : Fin k → Fin n) (hι : Function.Injective ι) (hcore : ∀ j, IsCore s (Q (ι j)))
    (hLB : ∀ t : ℝ, Fits k t → σ ≤ t) : σ + 2 ≤ s := by
  have h := hLB (s - 2) (core_fits n k s Q hP ι hι hcore)
  linarith

/-- **PEEL-0, contrapositive** [T]: below `2 + s(k)` no packing has `k` core squares. -/
theorem peel_no_straddler (n k : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hno : ¬ Fits k (s - 2)) (ι : Fin k → Fin n) (hι : Function.Injective ι) :
    ∃ j, ¬ IsCore s (Q (ι j)) := by
  by_contra h
  simp only [not_exists, not_not] at h
  exact hno (core_fits n k s Q hP ι hι h)

/-- The inner count [T, arithmetic]: `n = m² − k`, `k ≤ 6` ⟹ `n − 4(m − 2) ≥ (m − 2)² − 2`, the
range of Nagamochi's `s(j² − 2) = j` at `j = m − 2`. -/
theorem peel_inner_count (m k : ℤ) (hk : k ≤ 6) : (m - 2) ^ 2 - 2 ≤ (m ^ 2 - k) - 4 * (m - 2) := by
  have h : (m ^ 2 - k) - 4 * (m - 2) = (m - 2) ^ 2 + 4 - k := by ring
  rw [h]
  linarith

/-- **BAND-COUNT, general form** [T-prose, peel.md §2.1].  At a side `s ∈ (m − 1, m)`,
`s > 2 + √2`, at most `4(m − 2)` squares of a packing are band squares (a band square is flush
and touches a wall, A236 BAND-FLUSH; at most `m − 3` touchers of a wall miss both its corner
boxes; each corner box is met by at most one band square). -/
axiom band_count (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hs : 2 + Real.sqrt 2 < s)
    (S : Finset (Fin n)) (hS : ∀ i ∈ S, IsBand s (Q i)) : S.card ≤ 4 * (m - 2)

/-- FAMILY-STUCK(n) for the border-cell system of peel.md §1 (opaque: `8m − 20` cells). -/
opaque FamilyStuckN (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- "`Q` contains the ring": `4(m − 2)` tilted wall touchers, `m − 2` per wall (peel.md §1.3). -/
opaque HasRing (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- **ONLY-RING(n)** [C] (the PI, 2026-09-20): below `m` the only family-stuck structure is the
ring (+ pokers).  Evidence: peel.md §1.4; NOT proved for any `n`. -/
axiom only_ring (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q) : HasRing n m s Q

/-- **MONOTONE-ROOM(n) / RING-PEEL** [C]: the squares off the ring fit at side `s − 2` (the hole
of the tight flush limit).  [T] only at the tight flush limit (`core_fits`). -/
axiom ring_peel (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hring : HasRing n m s Q) :
    Fits (n - 4 * (m - 2)) (s - 2)

/-- **PEEL ⟹ no family-stuck packing below `2 + s(n − 4(m − 2))`** (from the two [C] axioms). -/
theorem peel_excludes (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hno : ¬ Fits (n - 4 * (m - 2)) (s - 2)) :
    ¬ FamilyStuckN n m s Q :=
  fun hfs => hno (ring_peel n m s Q hP hlo hhi (only_ring n m s Q hP hlo hhi hfs))

#print axioms core_fits
#print axioms peel_side_bound
#print axioms peel_no_straddler
#print axioms peel_inner_count
#print axioms band_count
#print axioms only_ring
#print axioms ring_peel
#print axioms peel_excludes

end PackingCert.S11.OpenLemmas
