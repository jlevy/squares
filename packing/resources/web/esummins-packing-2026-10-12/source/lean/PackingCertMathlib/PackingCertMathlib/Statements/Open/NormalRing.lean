import PackingCertMathlib.Statements.Open.CommonSense

/-!
# -- OPEN: NORMAL-RING — what a family-stuck packing looks like after LEXICOGRAPHIC normalisation — A258

`docs/proofs/normal_ring.md`, `attempts/A258-normal-ring/notes/family258.md`.  Setting: `n` unit squares
in `[0, s]²`, `m = ⌈√n⌉`, `m − 1 < s < m`.

**What is a theorem here** (any `n`, any `s`).
* `exists_lex_max` [T]: two bounded `ℕ`-valued potentials have a LEXICOGRAPHIC maximiser on the packings
  at side `s` (one step, no iteration) — from `exists_max_potential` by the encoding `Φ₁ (B₂+1) + Φ₂`.
* `exists_normalForm` [T from `normal_form_step`]: a packing at side `s` exists only if one in NORMAL FORM
  (P1 touch-normal, P2 row-normal modulo longer rows, P2′ the blocker of a normal cell has nowhere to go,
  P4 RETREAT: no free square can be re-posed to meet fewer border cells — a poker is HELD in its ribbon).
* `alt_side_poly`, `row_three_poly` [T]: the polynomial cores (half-angle `u = tan(φ/2)`) of
  ALT-SIDE (an alternating-sense pinwheel of common-tilt pairs needs side `> 4`) and ROW-THREE (a row of
  three cannot have a doubly met end box beside a common-tilt row below side 4).
* `normal_ring_value`, `normal_excludes_value` [T from the [C] axiom]: the chain to FAMILY-STUCK-EXIST in
  VALUE form, with the room statement as a HYPOTHESIS (it is A259's: `NormalRoom.lean`).

**What is not.**
* `touchPotential_le`, `rowVecPotential_le`, `normal_form_step` [T-prose] (normal_ring.md §1).
* `normal_ring` [C]: a normal-form family-stuck packing contains a HYBRID NORMAL RING — a pinwheel of four
  walls of one sense, each wall a common-tilt ROW OF TWO (a point of the domain `D′` of family258.md) or an
  OPEN PAIR locked by a free square.  The coordinator's form ("four rows of two") is this with no locked
  wall; A258 found that the ribbon poker LOCKS its wall on 43 of 44 corpus rings, so the locked walls
  cannot be dropped from the statement.

**Status (2026-09-21).**  theorems: `exists_lex_max`, `exists_normalForm`, `alt_side_poly`,
`row_three_poly`, `normal_ring_value`, `normal_excludes_value`; axioms [T-prose]: `touchPotential_le`,
`rowVecPotential_le`, `normal_form_step`; axiom [C]: `normal_ring`.
-/

namespace PackingCert.S11.OpenLemmas

/-- **LEXICOGRAPHIC ONE-STEP NORMALISATION** [T]. -/
theorem exists_lex_max (n : ℕ) (s : ℝ) (Φ₁ Φ₂ : (Fin n → Set RP) → ℕ) (B₁ B₂ : ℕ)
    (h₁ : ∀ Q, Φ₁ Q ≤ B₁) (h₂ : ∀ Q, Φ₂ Q ≤ B₂) (h : ∃ Q, IsPacking n s Q) :
    ∃ Q, IsPacking n s Q ∧ ∀ Q', IsPacking n s Q' →
      Φ₁ Q' < Φ₁ Q ∨ (Φ₁ Q' = Φ₁ Q ∧ Φ₂ Q' ≤ Φ₂ Q) := by
  have hB : ∀ Q, Φ₁ Q * (B₂ + 1) + Φ₂ Q ≤ B₁ * (B₂ + 1) + B₂ := by
    intro Q
    have hm : Φ₁ Q * (B₂ + 1) ≤ B₁ * (B₂ + 1) := Nat.mul_le_mul_right (B₂ + 1) (h₁ Q)
    have hb := h₂ Q
    omega
  obtain ⟨Q, hQ, hmax⟩ := exists_max_potential n s (fun Q => Φ₁ Q * (B₂ + 1) + Φ₂ Q)
    (B₁ * (B₂ + 1) + B₂) hB h
  refine ⟨Q, hQ, fun Q' hQ' => ?_⟩
  have hm : Φ₁ Q' * (B₂ + 1) + Φ₂ Q' ≤ Φ₁ Q * (B₂ + 1) + Φ₂ Q := hmax Q' hQ'
  have hb := h₂ Q
  have hb' := h₂ Q'
  rcases Nat.lt_trichotomy (Φ₁ Q') (Φ₁ Q) with hlt | heq | hgt
  · exact Or.inl hlt
  · right
    refine ⟨heq, ?_⟩
    rw [heq] at hm
    omega
  · exfalso
    have h3 : (Φ₁ Q + 1) * (B₂ + 1) ≤ Φ₁ Q' * (B₂ + 1) := Nat.mul_le_mul_right (B₂ + 1) hgt
    have h4 : (Φ₁ Q + 1) * (B₂ + 1) = Φ₁ Q * (B₂ + 1) + (B₂ + 1) := by ring
    omega

/-- Φ₁: the number of wall-touching squares (normal_ring.md §1.1; opaque). -/
opaque touchPotential (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : ℕ

/-- Φ₂: the pair (sorted descending row-length vector of the maximal common-tilt wall rows, RETREAT count
`N − #{(border cell, non-toucher) incidences}`), lexicographic, read as one number (normal_ring.md §1.1;
opaque).  The retreat count is upper semicontinuous ("meets" is an open condition) and integer-valued. -/
opaque rowVecPotential (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : ℕ

/-- A bound for Φ₂ (opaque: `(n+1)^n · (n (8m − 20) + 1)` serves). -/
opaque normalBound (n : ℕ) : ℕ

/-- NORMAL FORM (normal_ring.md §1.2; opaque): P1 ∧ P2 ∧ P2′ ∧ P4 (P4 = RETREAT: no free square can be
re-posed, alone or jointly with other non-touchers, so as to meet fewer border cells). -/
opaque NormalForm (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- [T-prose] at most `n` squares touch a wall. -/
axiom touchPotential_le (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : touchPotential n s Q ≤ n

/-- [T-prose] at most `n` rows, each of length `≤ n`; at most `n (8m − 20)` incidences. -/
axiom rowVecPotential_le (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) :
    rowVecPotential n s Q ≤ normalBound n

/-- **NORMAL-FORM step** [T-prose, normal_ring.md §1.2]: a packing violating P1, P2, P2′ or P4 exchanges
(Lemma CELLS on a family of at most three cells of any pose) into a packing at the same side that is
lexicographically larger in (wall touchers, (sorted row vector, retreat count)). -/
axiom normal_form_step (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hN : ¬ NormalForm n m s Q) :
    ∃ Q', IsPacking n s Q' ∧ (touchPotential n s Q < touchPotential n s Q' ∨
      (touchPotential n s Q = touchPotential n s Q' ∧ rowVecPotential n s Q < rowVecPotential n s Q'))

/-- **WLOG NORMAL FORM** [T from `normal_form_step`]. -/
theorem exists_normalForm (n m : ℕ) (s : ℝ) (h : ∃ Q, IsPacking n s Q) :
    ∃ Q, IsPacking n s Q ∧ NormalForm n m s Q := by
  obtain ⟨Q, hQ, hmax⟩ := exists_lex_max n s (touchPotential n s) (rowVecPotential n s) n
    (normalBound n) (touchPotential_le n s) (rowVecPotential_le n s) h
  refine ⟨Q, hQ, ?_⟩
  by_contra hN
  obtain ⟨Q', hQ', hlt⟩ := normal_form_step n m s Q hQ hN
  rcases hmax Q' hQ' with h1 | ⟨h1, h2⟩
  · rcases hlt with h3 | ⟨h3, _⟩ <;> omega
  · rcases hlt with h3 | ⟨_, h4⟩ <;> omega

/-- **ALT-SIDE, polynomial core** [T]: with `u = tan(φ/2) ∈ (0, 1/2]`,
`(s_alt(φ) − 4)(1 + u²)(1 − u²) = u − 2u² + 6u⁴ − u⁵ > 0`, where
`s_alt = 1 + cos φ (cos φ + sin φ − 1)/sin φ + sec φ + cos φ + sin φ` is the least side of the
alternating-sense pinwheel of common-tilt pairs (normal_ring.md §3.3). -/
theorem alt_side_poly (u : ℝ) (h0 : 0 < u) (h1 : u ≤ 1 / 2) :
    0 < u - 2 * u ^ 2 + 6 * u ^ 4 - u ^ 5 := by
  have e : u - 2 * u ^ 2 + 6 * u ^ 4 - u ^ 5 = u * (1 - 2 * u) + u ^ 4 * (6 - u) := by ring
  have a1 : 0 ≤ u * (1 - 2 * u) := mul_nonneg h0.le (by linarith)
  have a2 : 0 < u ^ 4 * (6 - u) := mul_pos (pow_pos h0 4) (by linarith)
  rw [e]
  linarith

/-- **ROW-THREE, polynomial core** [T]: with `u = tan(φ/2) ∈ (0, 1)`,
`(2 sec φ + cos φ + sin φ + tan(45° − φ/2) − 4)(1 + u²)(1 − u²) = 4u² − 4u³ + 8u⁴ > 0`
(normal_ring.md §3.2). -/
theorem row_three_poly (u : ℝ) (h0 : 0 < u) : 0 < 4 * u ^ 2 - 4 * u ^ 3 + 8 * u ^ 4 := by
  have e : 4 * u ^ 2 - 4 * u ^ 3 + 8 * u ^ 4 = 4 * u ^ 2 * (2 * (u - 1 / 4) ^ 2 + 7 / 8) := by ring
  rw [e]
  have : 0 < 2 * (u - 1 / 4) ^ 2 + 7 / 8 := by positivity
  exact mul_pos (by positivity) this

/-- The packing contains a HYBRID NORMAL RING with a HELD poker (normal_ring.md §3.5, family258.md §6;
opaque): eight wall touchers of one sense, each wall a common-tilt row of two (domain `D′`) or an open pair
locked by a free square, and a free square in a ribbon tooth that no re-posing of the free squares frees. -/
opaque HasNormalRing (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- **NORMAL-RING(n)** [C] (A258), meant on the window `s ≤ ŝ`.  Open: floating root meeters (N1); the
other pinwheels of rows are excluded below side 3.9298 by an LP scan over per-wall tilts only ([M]: mixed
senses + + + − exist from 3.9298, flat rows = type F from 3.9347 — both above `ŝ`, both below 4). -/
axiom normal_ring (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) : HasNormalRing n m s Q

/-- **NORMAL-RING, value form** [T from `normal_ring`]. -/
theorem normal_ring_value (n m : ℕ) (s : ℝ) (hlo : (m : ℝ) - 1 < s) (hhi : s < m)
    (h : ∃ Q, IsPacking n s Q) :
    (∃ Q, IsPacking n s Q ∧ ¬ FamilyStuckN n m s Q) ∨
      (∃ Q, IsPacking n s Q ∧ HasNormalRing n m s Q) := by
  obtain ⟨Q, hQ, hN⟩ := exists_normalForm n m s h
  by_cases hfs : FamilyStuckN n m s Q
  · exact Or.inr ⟨Q, hQ, normal_ring n m s Q hQ hlo hhi hfs hN⟩
  · exact Or.inl ⟨Q, hQ, hfs⟩

/-- **The chain**: if no packing at side `s` contains a hybrid normal ring (the ROOM statement, A259) and
every packing at side `s` is family-stuck, there is no packing at side `s`. -/
theorem normal_excludes_value (n m : ℕ) (s : ℝ) (hlo : (m : ℝ) - 1 < s) (hhi : s < m)
    (hroom : ∀ Q, IsPacking n s Q → ¬ HasNormalRing n m s Q)
    (hall : ∀ Q, IsPacking n s Q → FamilyStuckN n m s Q) : ¬ ∃ Q, IsPacking n s Q := by
  intro h
  rcases normal_ring_value n m s hlo hhi h with ⟨Q, hQ, hnfs⟩ | ⟨Q, hQ, hring⟩
  · exact hnfs (hall Q hQ)
  · exact hroom Q hQ hring

#print axioms exists_lex_max
#print axioms exists_normalForm
#print axioms alt_side_poly
#print axioms row_three_poly
#print axioms normal_ring_value
#print axioms normal_excludes_value

end PackingCert.S11.OpenLemmas
