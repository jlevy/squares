import PackingCertMathlib.Statements.Open.Peel

/-!
# -- OPEN: COMMON-SENSE — the local lemma behind ONLY-RING, in NORMAL FORM — A255

`docs/proofs/common_sense.md`.  Setting: `n` unit squares in `[0, s]²`, `m = ⌈√n⌉`,
`m − 1 < s < m`.  The SENSE of a square is the sign of its global tilt taken in `(−45°, 45°]`
(a quarter turn fixes it, a reflection flips it: a pinwheel has ONE sense).

**What is a theorem here** (any `n`, any `s`).
* `exists_max_potential` [T]: a bounded `ℕ`-valued potential attains its maximum on the packings
  at side `s`.  This is the ONE-STEP normalisation (no iteration, so no termination question):
  the normal form is a maximiser of the longest common-tilt wall ROW.
* `value_form_normal` [T]: if every exchange that lengthens the longest row is available
  whenever the packing is not `Normal` (the hypothesis `hstep`, which is Lemma NORMAL-CELL =
  Lemma CELLS on the tilted cell `T = s₁ ± sec φ`, common_sense.md §2), then a packing at side
  `s` exists only if a `Normal` one does.  Motions and exchanges inside the fixed container keep
  the side by definition; the value form needs nothing else (the PI's correction, addendum).
* `only_ring_value` [T from the [C] axioms]: the chain COMMON-SENSE ⟹ ONLY-RING in VALUE form:
  if a packing exists at side `s` then a packing exists that is not family-stuck (the other
  classes' business) or one that contains the ring.
* `peel_excludes_value` [T from the [C] axioms + `ring_peel`]: with the room statement, no
  packing at side `s < 2 + s(n − 4(m−2))` unless some packing at `s` is not family-stuck.

**What is not.**
* `normal_cell_step` [T-prose] (common_sense.md §2.2–2.3): NORMAL-CELL + the row potential.
* `common_sense` [C]: in a normal family-stuck packing every wall toucher that meets a border
  cell has one sense.  FALSE without `Normal` (common_sense.md §3: 20 of 20 mixed local types
  have witnesses); with it, open — the local blocked search and the ring-level sense search are
  [M] only.
* `ring_of_common_sense` [C]: closing the pinwheel round the four corners and the poker count.

**Status (2026-09-20).**  `exists_max_potential`, `value_form_normal`, `only_ring_value`,
`peel_excludes_value`: theorems; `normal_cell_step`: axiom [T-prose]; `common_sense`,
`ring_of_common_sense`: axioms [C].  `only_ring` (Peel.lean) is NOT used: the chain delivers
ONLY-RING in value form, which is all `peel_excludes_value` needs.
-/

namespace PackingCert.S11.OpenLemmas

/-- **ONE-STEP NORMALISATION** [T].  A potential bounded by `B` attains its maximum on the
packings at side `s` (if there is one). -/
theorem exists_max_potential (n : ℕ) (s : ℝ) (Φ : (Fin n → Set RP) → ℕ) (B : ℕ)
    (hB : ∀ Q, Φ Q ≤ B) (h : ∃ Q, IsPacking n s Q) :
    ∃ Q, IsPacking n s Q ∧ ∀ Q', IsPacking n s Q' → Φ Q' ≤ Φ Q := by
  by_contra hne
  push_neg at hne
  have key : ∀ k : ℕ, ∃ Q, IsPacking n s Q ∧ k ≤ Φ Q := by
    intro k
    induction k with
    | zero =>
      obtain ⟨Q, hQ⟩ := h
      exact ⟨Q, hQ, Nat.zero_le _⟩
    | succ k ih =>
      obtain ⟨Q, hQ, hk⟩ := ih
      obtain ⟨Q', hQ', hlt⟩ := hne Q hQ
      exact ⟨Q', hQ', by omega⟩
  obtain ⟨Q, _, hQ⟩ := key (B + 1)
  have := hB Q
  omega

/-- **VALUE FORM, WLOG NORMAL** [T].  If every non-`Normal` packing at side `s` exchanges, at
the same side, into one of larger potential, then a packing at side `s` exists only if a
`Normal` one does. -/
theorem value_form_normal (n : ℕ) (s : ℝ) (Φ : (Fin n → Set RP) → ℕ) (B : ℕ)
    (hB : ∀ Q, Φ Q ≤ B) (Normal : (Fin n → Set RP) → Prop)
    (hstep : ∀ Q, IsPacking n s Q → ¬ Normal Q → ∃ Q', IsPacking n s Q' ∧ Φ Q < Φ Q')
    (h : ∃ Q, IsPacking n s Q) : ∃ Q, IsPacking n s Q ∧ Normal Q := by
  obtain ⟨Q, hQ, hmax⟩ := exists_max_potential n s Φ B hB h
  refine ⟨Q, hQ, ?_⟩
  by_contra hN
  obtain ⟨Q', hQ', hlt⟩ := hstep Q hQ hN
  have := hmax Q' hQ'
  omega

/-- The length of the longest common-tilt wall row (common_sense.md §2.3; opaque). -/
opaque rowPotential (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : ℕ

/-- ROW-NORMAL (common_sense.md §2.3; opaque): every end cell `T` of a longest row is met by
at least two squares, or leaves the container. -/
opaque RowNormal (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- COMMON-SENSE (common_sense.md §1; opaque): the wall touchers meeting border cells have one
sense. -/
opaque CommonSenseN (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) : Prop

/-- `rowPotential ≤ n` [T-prose: a row is a set of squares]. -/
axiom rowPotential_le (n : ℕ) (s : ℝ) (Q : Fin n → Set RP) : rowPotential n s Q ≤ n

/-- **NORMAL-CELL step** [T-prose, common_sense.md §2.2–2.3]: a packing that is not row-normal
has an end cell `T ⊆ [0,s]²` of a longest row met by at most one square; Lemma CELLS on `{T}`
(`cells_swap`; the cell is tilted) teleports that square onto `T`: a packing at the same side
whose longest row is longer. -/
axiom normal_cell_step (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hN : ¬ RowNormal n m s Q) :
    ∃ Q', IsPacking n s Q' ∧ rowPotential n s Q < rowPotential n s Q'

/-- **WLOG ROW-NORMAL** [T from `normal_cell_step`]. -/
theorem exists_rowNormal (n m : ℕ) (s : ℝ) (h : ∃ Q, IsPacking n s Q) :
    ∃ Q, IsPacking n s Q ∧ RowNormal n m s Q :=
  value_form_normal n s (rowPotential n s) n (rowPotential_le n s) (RowNormal n m s)
    (fun Q hQ hN => normal_cell_step n m s Q hQ hN) h

/-- **COMMON-SENSE** [C] (the PI, 2026-09-20).  FALSE without `RowNormal` (witnesses:
common_sense.md §3). -/
axiom common_sense (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : RowNormal n m s Q) : CommonSenseN n m s Q

/-- **RING-OF-COMMON-SENSE** [C]: a row-normal family-stuck packing of one sense contains the
ring (the four rows close round the corners; the rest are pokers / free squares). -/
axiom ring_of_common_sense (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : RowNormal n m s Q) (hcs : CommonSenseN n m s Q) : HasRing n m s Q

/-- **ONLY-RING(n), value form** [T from the two [C] axioms]. -/
theorem only_ring_value (n m : ℕ) (s : ℝ) (hlo : (m : ℝ) - 1 < s) (hhi : s < m)
    (h : ∃ Q, IsPacking n s Q) :
    (∃ Q, IsPacking n s Q ∧ ¬ FamilyStuckN n m s Q) ∨ (∃ Q, IsPacking n s Q ∧ HasRing n m s Q) := by
  obtain ⟨Q, hQ, hN⟩ := exists_rowNormal n m s h
  by_cases hfs : FamilyStuckN n m s Q
  · exact Or.inr ⟨Q, hQ, ring_of_common_sense n m s Q hQ hlo hhi hfs hN
      (common_sense n m s Q hQ hlo hhi hfs hN)⟩
  · exact Or.inl ⟨Q, hQ, hfs⟩

/-- **PEEL in value form**: below `2 + s(n − 4(m−2))`, if every packing at side `s` is
family-stuck then there is no packing at side `s`. -/
theorem peel_excludes_value (n m : ℕ) (s : ℝ) (hlo : (m : ℝ) - 1 < s) (hhi : s < m)
    (hno : ¬ Fits (n - 4 * (m - 2)) (s - 2))
    (hall : ∀ Q, IsPacking n s Q → FamilyStuckN n m s Q) : ¬ ∃ Q, IsPacking n s Q := by
  intro h
  rcases only_ring_value n m s hlo hhi h with ⟨Q, hQ, hnfs⟩ | ⟨Q, hQ, hring⟩
  · exact hnfs (hall Q hQ)
  · exact hno (ring_peel n m s Q hQ hlo hhi hring)

#print axioms exists_max_potential
#print axioms value_form_normal
#print axioms exists_rowNormal
#print axioms only_ring_value
#print axioms peel_excludes_value

end PackingCert.S11.OpenLemmas
