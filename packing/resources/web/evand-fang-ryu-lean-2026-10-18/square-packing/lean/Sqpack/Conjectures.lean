import Sqpack.Spec

/-!
# The open problems of the Atlas, as Lean statements

Each item on the site's Open problems page (`site/www/problems.html`) that has a precise form,
stated over the common specification `Sqpack/Spec.lean` (`Packs`, `minSide`).  Every statement is
a `def … : Prop`, not a `theorem … := sorry`, so importing this file adds no axioms: a proof of an
item is a `theorem` whose type is that `Prop`, and a disproof is one of its negation.

Status tags in each docstring:

* **conjecture** — someone has predicted the answer (the `Prop` states the predicted answer);
* **question** — no confident prediction (the `Prop` states one answer; its negation is the other);
* **known** — proved on paper; stated so that a formalisation has a target.  The two elementary
  ones (`TilingBound`, `CStarStepsOfTwo`) are proved in `Sqpack/ConjecturesProofs.lean`.

Conventions, chosen to avoid `sInf` junk values:

* "`s(n)` is not an integer" is `NonIntegral n : ∀ m : ℕ, minSide n ≠ m` (with `n ≥ 1`; `minSide 0`
  is `sInf ℝ = 0`).  Since `s(n) ≥ √n`, this is the same as `s(n) < ⌈√n⌉` for every `n ≥ 1`.
* "`s(k² − c) = k`" is `GridOptimal k c : ∀ s, Packs (k² − c) s → k ≤ s` (the canonical
  lower-bound shape; the grid gives `Packs (k² − c) k`).  Natural subtraction: for `c ≥ k²` it says
  `Packs 0 s → k ≤ s`, which is false, as it should be.
* Waste bounds are stated with an explicit packing (`∃ n, n ≥ s² − C·f(s) ∧ Packs n s`), not with
  `sSup` of the packable counts.

Items deliberately not stated: §4 *Symmetry*, §5 (data questions about families in the record
table), §6 (local optimality, alternatives, stability: definable, but they need the configuration
space and its paths; a later file), and §7's family targets.
-/

namespace UnitSquarePacking.Conjectures

open Set Real

/-- `s(n)` is not an integer. -/
def NonIntegral (n : ℕ) : Prop := ∀ m : ℕ, minSide n ≠ m

/-- `s(k² − c) = k`: removing `c` squares from the `k × k` grid allows no smaller box. -/
def GridOptimal (k c : ℕ) : Prop := ∀ s : ℝ, Packs (k ^ 2 - c) s → (k : ℝ) ≤ s

/-- A packing of `n` unit squares in `[0, s]²` whose angles take at most `m` values modulo `π/2`
(rotating a square by `π/2` does not change it). -/
def PacksWithAngles (n : ℕ) (s : ℝ) (m : ℕ) : Prop :=
  ∃ (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ container s) ∧
    (Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))) ∧
    (Set.range fun i => toIcoMod (by positivity : (0 : ℝ) < π / 2) 0 (θ i)).ncard ≤ m

/-! ## §1 Friedman's staircase -/

/-- **Monotone** (conjecture; Friedman's Conjecture 1, DS7 1998): `c*(k+1) ≥ c*(k)`, i.e. if
`s(k² − c) = k` then `s((k+1)² − c) = k + 1`.  Proved on paper for `c ≤ 4`. -/
def FriedmanMonotone : Prop := ∀ k c : ℕ, 1 ≤ k → GridOptimal k c → GridOptimal (k + 1) c

/-- **Unbounded** (question; claimed 2026 by Ryu's preprint `squarepacker/k2-minus-c`, unrefereed,
`c*(k) ≥ 0.0353 log k − 1`; not formalized): `c*(k) → ∞`, i.e. for every `c`,
`s(k² − c) = k` for all large `k`.  Proved on paper for `c ≤ 4`. -/
def CStarUnbounded : Prop := ∀ c : ℕ, ∃ K : ℕ, ∀ k ≥ K, GridOptimal k c

/-- **Unit steps** (question; stated here): `c*(k+1) ≤ c*(k) + 1`. -/
def CStarUnitSteps : Prop := ∀ k c : ℕ, 1 ≤ k → GridOptimal (k + 1) (c + 1) → GridOptimal k c

/-- **Steps of two** (known; proved: `cStarStepsOfTwo` in `Sqpack/ConjecturesProofs.lean`):
`c*(k+1) ≤ c*(k) + 2`, by an L-shaped border. -/
def CStarStepsOfTwo : Prop := ∀ k c : ℕ, 1 ≤ k → GridOptimal (k + 1) (c + 2) → GridOptimal k c

/-- **`s(k² − k) = k`** for one `k` (question for `k = 4, …, 10`; true for `k = 2, 3`, false for
`k ≥ 11`). -/
def GridMinusRowOptimal (k : ℕ) : Prop := GridOptimal k k

/-! ## §2 Wasted space -/

/-- **Square-root waste** (conjecture; Erdős–Graham 1975, Friedman's Conjecture 2):
`W(s) = O(s^{1/2})`.
Chung and Graham (2020) doubt it. -/
def SqrtWaste : Prop :=
  ∃ C : ℝ, ∀ s : ℝ, 1 ≤ s → ∃ n : ℕ, s ^ 2 - C * s ^ (1 / 2 : ℝ) ≤ n ∧ Packs n s

/-- **Waste `O(s^{3/5})`** (known: Bui 2025, McClenagan 2026, preprints; Erdős–Graham 1975 had
`7/11`).  Not in Lean. -/
def ThreeFifthsWaste : Prop :=
  ∃ C : ℝ, ∀ s : ℝ, 1 ≤ s → ∃ n : ℕ, s ^ 2 - C * s ^ (3 / 5 : ℝ) ≤ n ∧ Packs n s

/-! ## §3 Plateaus and families -/

/-- `n` is a **non-integer plateau**: `s(n) = s(n+1)` and `s(n)` is not an integer. -/
def NonIntPlateau (n : ℕ) : Prop := 1 ≤ n ∧ minSide n = minSide (n + 1) ∧ NonIntegral n

/-! The plateau statements, strongest first.  The implications between them are proved in
`Sqpack/ConjecturesProofs.lean`:

* `NoNonIntegerPlateau → FinitelyManyPlateaus → PlateausBounded` and
  `FinitelyManyPlateaus → FinitelyManyPlateausPerFract`;
* `FinitelyManyPerFract → FinitelyManyPlateausPerFract` (a different strengthening, about all `n`);
* `FinitelyManyPlateausPerFract ∧ PlateauFractsFinite → FinitelyManyPlateaus`: the per-fractional-part
  form plus finitely many fractional parts at plateaus gives the finite form back.

So each weaker form is a step toward the stronger ones, and a fallback if they fail. -/

/-- **A non-integer plateau** (question; in the best-known table, first at `n = 147`):
some `n` has `s(n) = s(n+1) ∉ ℤ`. -/
def NonIntegerPlateauExists : Prop := ∃ n : ℕ, NonIntPlateau n

/-- **No non-integer plateau** (the negative answer to `NonIntegerPlateauExists`): the strongest
form.  Every best-known candidate (`n = 147, 232, 264, 290, 295`) would have to be beaten. -/
def NoNonIntegerPlateau : Prop := ∀ n : ℕ, ¬ NonIntPlateau n

/-- **Finitely many non-integer plateaus** (conjecture; stated here). -/
def FinitelyManyPlateaus : Prop := {n : ℕ | NonIntPlateau n}.Finite

/-- **Plateaus are eventually short** (conjecture; stated here; follows from
`FinitelyManyPlateaus`): some `L` bounds the length of every non-integer plateau, i.e.
`s(n) < s(n + L)` whenever `s(n) ∉ ℤ`.  (Every best-known candidate has length 2.) -/
def PlateausBounded : Prop :=
  ∃ L : ℕ, ∀ n : ℕ, 1 ≤ n → NonIntegral n → minSide n < minSide (n + L)

/-- **Finitely many plateaus at each fractional part** (conjecture; stated here).  This is what
the fixed-shape-family evidence supports directly: a family keeps one fractional part, wastes
area linearly in `k`, and so is optimal only finitely often. -/
def FinitelyManyPlateausPerFract : Prop :=
  ∀ β : ℝ, {n : ℕ | NonIntPlateau n ∧ Int.fract (minSide n) = β}.Finite

/-- **Finitely many fractional parts at plateaus** (question; stated here): the missing half of
`FinitelyManyPlateaus` given `FinitelyManyPlateausPerFract`. -/
def PlateauFractsFinite : Prop :=
  ((fun n => Int.fract (minSide n)) '' {n : ℕ | NonIntPlateau n}).Finite

/-- **Each fractional part finitely often** (conjecture; stated here), for all `n`, not just
plateaus.  It implies `FinitelyManyPlateausPerFract` but **not** `FinitelyManyPlateaus`:
infinitely many plateaus could each have their own fractional part. -/
def FinitelyManyPerFract : Prop :=
  ∀ β : ℝ, 0 < β → {n : ℕ | 1 ≤ n ∧ Int.fract (minSide n) = β}.Finite

/-! ## §4 How complicated are optimal packings? -/

/-- **`s(n)` is algebraic** (known: Tarski–Seidenberg).  Not in Lean. -/
def MinSideAlgebraic : Prop := ∀ n : ℕ, IsAlgebraic ℚ (minSide n)

/-- **Algebraic degree → ∞** along the non-integer values (question).  (If some `s(n)` were
transcendental its `minpoly` would be `0`; `MinSideAlgebraic` rules that out.) -/
def DegreeTendsToInfinity : Prop :=
  ∀ D : ℕ, ∃ N : ℕ, ∀ n ≥ N, NonIntegral n → D < (minpoly ℚ (minSide n)).natDegree

/-- **Eventually not built from square roots**, strong form (question).  The page asks whether
there is a last `n` whose `s(n)` is built from square roots alone (a constructible number, whose
degree is then a power of two).  This states the stronger claim that eventually the degree is not
even a power of two; its truth answers the page's question with "yes, there is a last one". -/
def EventuallyNotTwoPower : Prop :=
  ∃ N : ℕ, ∀ n ≥ N, NonIntegral n → ∀ j : ℕ, (minpoly ℚ (minSide n)).natDegree ≠ 2 ^ j

/-- **A rational optimal non-integer side** (question; rational records exist at
`n = 50, 230, 261, 293`, none proved optimal). -/
def RationalNonIntegerOptimum : Prop :=
  ∃ n : ℕ, 1 ≤ n ∧ NonIntegral n ∧ ∃ q : ℚ, minSide n = q

/-- **Boundedly many angles waste linearly** (question; stated here): for each `m` and each
fractional part `β ∈ (0, 1)`, packings with at most `m` angles in a box of side `k + β` waste at
least a constant times `k`. -/
def FewAnglesWasteLinearly : Prop :=
  ∀ m : ℕ, ∀ β : ℝ, 0 < β → β < 1 → ∃ c : ℝ, 0 < c ∧ ∀ (k n : ℕ), 1 ≤ k →
    PacksWithAngles n (k + β) m → (n : ℝ) ≤ ((k : ℝ) + β) ^ 2 - c * k

/-- **Optimal packings need ever more angles** (question): for each `m`, no large `n` with
`s(n) ∉ ℤ` has an optimal packing with at most `m` angles.  `FewAnglesWasteLinearly` with
`ThreeFifthsWaste` would give this for the `n` whose `s(n)` has any one fixed fractional part. -/
def OptimaNeedManyAngles : Prop :=
  ∀ m : ℕ, ∃ N : ℕ, ∀ n ≥ N, NonIntegral n → ¬ PacksWithAngles n (minSide n) m

/-- **Tilings are never optimal** (conjecture; stated here, Evan 2026-10-07): if `s(n)` is not an
integer then `s(k²n) < k·s(n)` for every `k ≥ 2`.  Tiling a `k × k` array of copies gives `≤`.
Known on paper for `k ≥ K(n)` (`TilingsEventuallyNotOptimal`); open at `k = 2`. -/
def TilingsNeverOptimal : Prop :=
  ∀ n k : ℕ, 1 ≤ n → 2 ≤ k → NonIntegral n → minSide (k ^ 2 * n) < k * minSide n

/-- The large-`k` case of `TilingsNeverOptimal` (known on paper: the tiling wastes `≍ k²`, optimal
packings `O(k^{7/11})` by Erdős–Graham).  In Lean conditionally: `ThreeFifthsWaste` and
`AreaStrict` imply it (`tilingsEventuallyNotOptimal_of`, `Sqpack/ConjecturesProofs.lean`). -/
def TilingsEventuallyNotOptimal : Prop :=
  ∀ n : ℕ, 1 ≤ n → NonIntegral n → ∃ K : ℕ, ∀ k ≥ K, minSide (k ^ 2 * n) < k * minSide n

/-- **Positive waste at non-integer sides** (known: area gives `n ≤ s(n)²`, and a square of
non-integer side cannot be tiled exactly by unit squares).  Not in Lean. -/
def AreaStrict : Prop := ∀ n : ℕ, 1 ≤ n → NonIntegral n → (n : ℝ) < minSide n ^ 2

/-- The tiling bound `s(k²n) ≤ k·s(n)` (known, elementary; proved: `tilingBound` in
`Sqpack/ConjecturesProofs.lean`). -/
def TilingBound : Prop := ∀ n k : ℕ, 1 ≤ n → 1 ≤ k → minSide (k ^ 2 * n) ≤ k * minSide n

/-! ## §7 Single values and packing targets -/

/-- **`s(12) = 4`** (conjecture; best proved floor 3.9715). -/
def S12 : Prop := IsLeast {s | Packs 12 s} 4

/-- **`s(90) < 10`** (packing target): would show the last `k` with `s(k² − k) = k` is `≤ 9`. -/
def S90Below10 : Prop := ∃ s < (10 : ℝ), Packs 90 s

/-- **`s(133) < 12`** (packing target; the best bet among the borderline grids). -/
def S133Below12 : Prop := ∃ s < (12 : ℝ), Packs 133 s

/-! ## §8 Neighbouring problems -/

/-- `n` unit squares pack in the rectangle `[0, a] × [0, b]`. -/
def PacksRect (n : ℕ) (a b : ℝ) : Prop :=
  ∃ (c : Fin n → ℝ × ℝ) (θ : Fin n → ℝ), (∀ i, unitSq (c i) (θ i) ⊆ Icc 0 a ×ˢ Icc 0 b) ∧
    Pairwise fun i j => Disjoint (interior (unitSq (c i) (θ i))) (interior (unitSq (c j) (θ j)))

/-- The `a × b` grid with `c` squares removed is optimal: no box `a' × b'` with `a' ≤ a`,
`b' ≤ b`, other than `a × b` itself, holds `ab − c` squares. -/
def GridOptimalRect (a b c : ℕ) : Prop :=
  ∀ a' b' : ℝ, PacksRect (a * b - c) a' b' → a' ≤ a → b' ≤ b → a' = a ∧ b' = b

/-- **Rectangles, one side at a time** (conjecture; stated here): `c*(a, b)` is nondecreasing in
`a` (and so, by symmetry, in `b`). -/
def RectMonotone : Prop :=
  ∀ a b c : ℕ, 1 ≤ a → 1 ≤ b → GridOptimalRect a b c → GridOptimalRect (a + 1) b c

/-- `n` open unit cubes, placed by isometries of `ℝ³`, pack disjointly in the open cube `(0, s)³`
(formal-conjectures' style, one dimension up). -/
def CubePacks (n : ℕ) (s : ℝ) : Prop :=
  ∃ e : Fin n → (EuclideanSpace ℝ (Fin 3) ≃ᵢ EuclideanSpace ℝ (Fin 3)),
    (Pairwise fun i j => Disjoint (e i '' {p | ∀ t, 0 < p t ∧ p t < 1})
      (e j '' {p | ∀ t, 0 < p t ∧ p t < 1})) ∧
    ∀ i, e i '' {p | ∀ t, 0 < p t ∧ p t < 1} ⊆ {p | ∀ t, 0 < p t ∧ p t < s}

/-- **Cubes** (question; stated here): for each `c`, `s₃(k³ − c) = k` for all large `k`.  Even
`c = 1` seems not to be in print. -/
def CubesGridOptimal : Prop :=
  ∀ c : ℕ, ∃ K : ℕ, ∀ k ≥ K, ∀ s : ℝ, CubePacks (k ^ 3 - c) s → (k : ℝ) ≤ s

/-! ## Sanity: the definitions behave -/

/-- Fewer squares still pack. -/
theorem packs_of_le {m n : ℕ} {s : ℝ} (h : Packs n s) (hmn : m ≤ n) : Packs m s := by
  obtain ⟨c, θ, hin, hdis⟩ := h
  exact ⟨c ∘ Fin.castLE hmn, θ ∘ Fin.castLE hmn, fun i => hin _,
    fun i j hij => hdis (fun h => hij (Fin.castLE_injective hmn h))⟩

/-- `GridOptimal k` is antitone in `c`, so `c*(k)` is a threshold. -/
theorem GridOptimal.mono {k c c' : ℕ} (h : GridOptimal k c) (hc : c' ≤ c) : GridOptimal k c' :=
  fun s hs => h s (packs_of_le hs (Nat.sub_le_sub_left hc _))

/-- The steps-of-two bound follows from unit steps. -/
theorem CStarUnitSteps.stepsOfTwo (h : CStarUnitSteps) : CStarStepsOfTwo :=
  fun k c hk h2 => h k c hk (h2.mono (Nat.le_succ _))

end UnitSquarePacking.Conjectures
