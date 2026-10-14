import PackingCertMathlib.Statements.Open.NormalRing
import PackingCertMathlib.Statements.Open.NormalRoom
import PackingCertMathlib.Statements.Open.RingSwap

/-!
# -- OPEN: LOCKED WALL — UNLOCK / HELD, the open notch, the hybrid corner PAIR, the PLUG — A260

`docs/proofs/locked_wall.md`.  In A258's normal form a wall of the ring is a common-tilt ROW OF TWO
or an OPEN PAIR `(s₁, W)` whose normal cell `T = s₁ + sec φ₁ · e` is met by `W` and by a free square
(a LOCK).  A259 bounded the room of the normal ring; this file carries the locked wall.

**What is a theorem here.**
* `unlock_swap` [T]: Lemma UNLOCK — the two-cell exchange `W → T`, `F → Q` is a packing at the same
  side whenever `T`, `Q` are unit cells in the container, interior-disjoint from each other and from
  every square other than `W`, `F` (Lemma CELLS with `|Π| = 2`; from `cells_swap`).  So in the
  lexicographic maximiser a lock is HELD: `(P ∖ {W, F}) ∪ {T}` is saturated (A258's P2′).
* `plug_kernel` [T]: the algebra of Lemma PLUG — for a unit square of width `w ∈ [1, √2]` in both
  axes, `w/2 − 1/(2w) ≤ 0.354` and `w/2 + 1/(2w) ≥ 1`: a unit square of the quadrant that reaches
  within `ρ` of the corner contains the open box `(0.354 + ρ, 1)²`, hence the START square's lowest
  vertex `(cos φ′, a′)` when `0.354 + ρ < a′ < 1` — no free square meets the corner box `[0, ρ]²`.
* `poke_chord` [T]: `2 sin ψ cos ψ ≤ 1` — the horizontal chord of a square at height `h` above its
  lowest vertex is `h (tan ψ + cot ψ) ≥ 2h`; in a slot of width `γ` the vertex dips at most `γ/2`
  (OPEN-TOOTH, POKE form).
* `open_tooth_at_tilt` [T]: at the row's tilt the open notch is deeper than the closed one by
  `e sin φ cos φ ≤ e/2` exactly: `c (1 − e g) = c − e g c` and `e g c ≤ e/2`.
* `lockedWall_excludes`, `k0_value_of_hybrid` [T from `hybrid_pierce`]: the count and the chain.

**What is not.**
* `hybrid_pierce` [T-computed + C]: on the window every non-ring square of a packing of 11 that
  contains a (hybrid) normal ring contains the centre.  Reduction MISS ⟹ hybrid corner PAIR: [T]
  (locked_wall.md §3.1).  The corner PAIR: [T-computed] on the normal family `D′` (A259's tree +
  the CORNER-NOTCH layer closed here: `certs/layer260_*`, verified) and on the all-ADJ hybrid family
  with a COMMON tilt per wall (`certs/hyb{A,B,AB}260_*`, detached chain, own verifier `verify260`);
  [C] for open pairs whose two squares have different tilts and for rings that are not all-ADJ
  ([M]: adversary sup −0.0654 < −(4 − s)/2 at `ŝ`; corpus 46/46).
-/

namespace PackingCert.S11.OpenLemmas.LockedWall

open Set PackingCert.S11.OpenLemmas

/-- **Lemma UNLOCK** [T] (Lemma CELLS with `Π = {T, Q}`): if `T` and `Q` are unit cells inside the
container, interior-disjoint from each other and from every square other than `W = z iW` and the lock
`F = z iF`, then `W → T`, `F → Q` is a packing at the same side. -/
theorem unlock_swap {m : ℝ} {z : Cfg} (hz : CfgPacking m z) (iW iF : Fin 11) (hne : iW ≠ iF)
    (T Q : PSq) (hT : T.t ∈ Icc (0 : ℝ) 1) (hQ : Q.t ∈ Icc (0 : ℝ) 1)
    (hTbox : T.set ⊆ container m) (hQbox : Q.set ⊆ container m)
    (hTQ : Disjoint (interior T.set) (interior Q.set))
    (hmissT : ∀ j, j ≠ iW → j ≠ iF → Disjoint (interior T.set) (interior (z j).set))
    (hmissQ : ∀ j, j ≠ iW → j ≠ iF → Disjoint (interior Q.set) (interior (z j).set)) :
    CfgPacking m (Function.update (Function.update z iW T) iF Q) := by
  let ι : Fin 2 → Fin 11 := ![iW, iF]
  let F : Fin 2 → PSq := ![T, Q]
  have hι : ∀ j : Fin 11, (∀ a, ι a ≠ j) → j ≠ iW ∧ j ≠ iF := by
    intro j h
    exact ⟨fun e => h 0 (by simp [ι, e]), fun e => h 1 (by simp [ι, e])⟩
  refine cells_swap hz ι F _ ?_ ?_ ?_ ?_ ?_ ?_
  · intro a
    fin_cases a
    · simp [ι, F, Function.update_of_ne hne]
    · simp [ι, F]
  · intro j h
    obtain ⟨h1, h2⟩ := hι j h
    simp [Function.update_of_ne h2, Function.update_of_ne h1]
  · intro a
    fin_cases a
    · simpa [F] using hT
    · simpa [F] using hQ
  · intro a
    fin_cases a
    · simpa [F] using hTbox
    · simpa [F] using hQbox
  · intro a b hab
    fin_cases a <;> fin_cases b
    · exact absurd rfl hab
    · simpa [F] using hTQ
    · simpa [F] using hTQ.symm
    · exact absurd rfl hab
  · intro j h a
    obtain ⟨h1, h2⟩ := hι j h
    fin_cases a
    · simpa [F] using hmissT j h1 h2
    · simpa [F] using hmissQ j h1 h2

/-- **PLUG, the kernel algebra** [T]: `w ∈ [1, √2]` ⟹ `w/2 − 1/(2w) ≤ 0.354` and `w/2 + 1/(2w) ≥ 1`
(both cleared of the denominator `2w > 0`). -/
theorem plug_kernel (w : ℝ) (h1 : 1 ≤ w) (h2 : w * w ≤ 2) :
    w * w - 1 ≤ (708 : ℝ) / 1000 * w ∧ 2 * w ≤ w * w + 1 := by
  have hw : w ≤ (14143 : ℝ) / 10000 := by nlinarith
  constructor
  · nlinarith [mul_nonneg (sub_nonneg.2 h1) (sub_nonneg.2 hw)]
  · nlinarith [sq_nonneg (w - 1)]

/-- **POKE chord** [T]: `2 S C ≤ 1` on the unit circle, i.e. `tan ψ + cot ψ ≥ 2`. -/
theorem poke_chord (C S : ℝ) (h : C ^ 2 + S ^ 2 = 1) : 2 * S * C ≤ 1 := by
  nlinarith [sq_nonneg (C - S)]

/-- **OPEN-TOOTH at the row's tilt** [T]: the least depth `c (1 − e g)` of the open notch is the
closed tooth's `c` minus `e g c`, and `e g c ≤ e/2`. -/
theorem open_tooth_at_tilt (c g e : ℝ) (h : c ^ 2 + g ^ 2 = 1) (he : 0 ≤ e) :
    c * (1 - e * g) = c - e * g * c ∧ e * g * c ≤ e / 2 := by
  constructor
  · ring
  · have := poke_chord c g h
    nlinarith [mul_nonneg he (sub_nonneg.2 this)]

/-- **HYBRID-PIERCE** [T-computed + C] (locked_wall.md §3, §6): in a packing of 11 on the window that
contains A258's (hybrid) normal ring, the ring is carried by eight squares and every other square
contains the container centre in its interior. -/
axiom hybrid_pierce (s : ℝ) (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q)
    (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (hring : HasNormalRing 11 4 s Q) :
    ∃ ι : Fin 8 → Fin 11, ∀ j, j ∉ Set.range ι → ((s / 2, s / 2) : RP) ∈ interior (Q j)

/-- **LOCKED-WALL excludes** [T from `hybrid_pierce`]: a pierced pocket holds one square, 8 + 1 < 11. -/
theorem lockedWall_excludes (s : ℝ) (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (Q : Fin 11 → Set RP) (hP : IsPacking 11 s Q) : ¬ HasNormalRing 11 4 s Q := by
  intro hring
  obtain ⟨ι, hι⟩ := hybrid_pierce s Q hP hlo hhi hring
  have := NormalRoom.normalRoom_count 11 s Q hP ι hι
  omega

/-- **The chain to the value form** [T from `hybrid_pierce` and A258's `normal_ring` [C]]: if every
packing at side `s` on the window were family-stuck, there would be none. -/
theorem k0_value_of_hybrid (s : ℝ) (hlo : (382 : ℝ) / 100 ≤ s) (hhi : s ≤ (38771 : ℝ) / 10000)
    (hall : ∀ Q, IsPacking 11 s Q → FamilyStuckN 11 4 s Q) : ¬ ∃ Q, IsPacking 11 s Q := by
  refine normal_excludes_value 11 4 s ?_ ?_ (fun Q hQ => lockedWall_excludes s hlo hhi Q hQ) hall
  · norm_num; linarith
  · norm_num; linarith

#print axioms unlock_swap
#print axioms plug_kernel
#print axioms poke_chord
#print axioms open_tooth_at_tilt
#print axioms lockedWall_excludes
#print axioms k0_value_of_hybrid

end PackingCert.S11.OpenLemmas.LockedWall
