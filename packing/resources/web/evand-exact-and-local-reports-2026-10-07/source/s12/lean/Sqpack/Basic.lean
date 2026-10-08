import Mathlib

/-!
# Weighted unavoidable sets and lower bounds for packing unit squares in a square

Let `s(n)` be the side of the smallest square into which `n` unit squares can be packed
(rotations allowed).  A **weighted unavoidable set** for the container `C` is a finite set of
points ("atoms") with non-negative weights such that *every* closed unit square contained in
`C` contains atoms of total weight at least `1`.

`packing_le_weight` : if such a set has total weight `W`, then any family of `n` squares of
side `L > 1`, contained in `C` and with pairwise disjoint interiors, satisfies `n ≤ W`.

`no_small_packing` : consequently, if `W < n` then `n` unit squares cannot be packed into any
square of side `s' < s`; that is, `s(n) ≥ s`.  (The passage from unit squares in the smaller
container to `L`-squares with `L > 1` in `C` is the classical scaling trick.)

The hypothesis `hcover` is what the exact checkers (`verify/`, `verify2/`, `search/zeromargin.py`) establish
for a given certificate.
-/

open Finset
open scoped Classical

namespace SquarePacking

/-- Rotated coordinates of `p` relative to centre `c` and angle `θ`. -/
noncomputable def coord (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  ((p.1 - c.1) * Real.cos θ + (p.2 - c.2) * Real.sin θ,
   (-(p.1 - c.1)) * Real.sin θ + (p.2 - c.2) * Real.cos θ)

/-- The closed square of side `L`, centre `c`, angle `θ`. -/
def sq (c : ℝ × ℝ) (θ L : ℝ) : Set (ℝ × ℝ) :=
  {p | |(coord c θ p).1| ≤ L/2 ∧ |(coord c θ p).2| ≤ L/2}

/-- The open square (interior) of side `L`, centre `c`, angle `θ`. -/
def sqInt (c : ℝ × ℝ) (θ L : ℝ) : Set (ℝ × ℝ) :=
  {p | |(coord c θ p).1| < L/2 ∧ |(coord c θ p).2| < L/2}

/-- A concentric closed unit square sits in the interior of any concentric square of side
`L > 1`.  This is the step that lets a *closed*-square certificate control a packing. -/
lemma unit_subset_interior {c : ℝ × ℝ} {θ L : ℝ} (hL : 1 < L) :
    sq c θ 1 ⊆ sqInt c θ L := by
  rintro p ⟨h1, h2⟩
  constructor
  · calc |(coord c θ p).1| ≤ 1/2 := h1
      _ < L/2 := by linarith
  · calc |(coord c θ p).2| ≤ 1/2 := h2
      _ < L/2 := by linarith

/-- A point lies in at most one member of a pairwise disjoint family. -/
lemma card_filter_le_one {n : ℕ} (S : Fin n → Set (ℝ × ℝ))
    (hdisj : ∀ i j, i ≠ j → Disjoint (S i) (S j)) (a : ℝ × ℝ) :
    ((univ : Finset (Fin n)).filter (fun i => a ∈ S i)).card ≤ 1 := by
  rw [card_le_one]
  intro i hi j hj
  simp only [mem_filter, mem_univ, true_and] at hi hj
  by_contra hne
  exact (Set.disjoint_left.mp (hdisj i j hne) hi) hj

/-- **Main reduction.**  A weighted unavoidable set of total weight `W` bounds the number of
squares of side `L > 1` that can be packed (disjoint interiors) inside `C`. -/
theorem packing_le_weight
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ))
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) ≤ ∑ a ∈ A, w a := by
  -- the concentric unit squares are inside C, and inside the (disjoint) interiors
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  have hU : ∀ i, sq (ctr i) (ang i) 1 ⊆ C := fun i =>
    subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  set S : Fin n → Set (ℝ × ℝ) := fun i => sq (ctr i) (ang i) 1 with hSdef
  have hSdisj : ∀ i j, i ≠ j → Disjoint (S i) (S j) := by
    intro i j hij
    exact Set.disjoint_of_subset (unit_subset_interior hL) (unit_subset_interior hL) (hdisj i j hij)
  have key : ∀ i : Fin n, (1:ℝ) ≤ ∑ a ∈ A.filter (fun a => a ∈ S i), w a := fun i =>
    hcover (ctr i) (ang i) (hU i)
  have h1 : (n:ℝ) ≤ ∑ i : Fin n, ∑ a ∈ A.filter (fun a => a ∈ S i), w a := by
    calc (n:ℝ) = ∑ _i : Fin n, (1:ℝ) := by simp
      _ ≤ _ := Finset.sum_le_sum fun i _ => key i
  have h2 : ∑ i : Fin n, ∑ a ∈ A.filter (fun a => a ∈ S i), w a
      = ∑ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) := by
    simp only [Finset.sum_filter]; exact Finset.sum_comm
  have h3 : ∀ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) ≤ w a := by
    intro a ha
    have hcard : (((univ : Finset (Fin n)).filter (fun i => a ∈ S i)).card : ℝ) ≤ 1 := by
      exact_mod_cast card_filter_le_one S hSdisj a
    have hEq : ∑ i : Fin n, (if a ∈ S i then w a else 0)
        = (((univ : Finset (Fin n)).filter (fun i => a ∈ S i)).card : ℝ) * w a := by
      rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
    rw [hEq]; nlinarith [hw a ha]
  have h4 : ∑ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) ≤ ∑ a ∈ A, w a :=
    Finset.sum_le_sum h3
  linarith [h1, h2 ▸ h1, h4]

/-- **Threshold form of the reduction.**  If every closed unit square inside `C` with centre `c`
and angle `θ` captures weight `≥ t c θ`, then a packing of `n` squares of side `L > 1` satisfies
`∑ i, t (ctr i) (ang i) ≤ W`.  `packing_le_weight` is the case `t = 1`. -/
theorem packing_le_weight_thresh
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (t : ℝ × ℝ → ℝ → ℝ)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        t c θ ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    ∑ i : Fin n, t (ctr i) (ang i) ≤ ∑ a ∈ A, w a := by
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  have hU : ∀ i, sq (ctr i) (ang i) 1 ⊆ C := fun i =>
    subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  set S : Fin n → Set (ℝ × ℝ) := fun i => sq (ctr i) (ang i) 1 with hSdef
  have hSdisj : ∀ i j, i ≠ j → Disjoint (S i) (S j) := by
    intro i j hij
    exact Set.disjoint_of_subset (unit_subset_interior hL) (unit_subset_interior hL) (hdisj i j hij)
  have key : ∀ i : Fin n, t (ctr i) (ang i) ≤ ∑ a ∈ A.filter (fun a => a ∈ S i), w a := fun i =>
    hcover (ctr i) (ang i) (hU i)
  have h1 : ∑ i : Fin n, t (ctr i) (ang i) ≤ ∑ i : Fin n, ∑ a ∈ A.filter (fun a => a ∈ S i), w a :=
    Finset.sum_le_sum fun i _ => key i
  have h2 : ∑ i : Fin n, ∑ a ∈ A.filter (fun a => a ∈ S i), w a
      = ∑ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) := by
    simp only [Finset.sum_filter]; exact Finset.sum_comm
  have h3 : ∀ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) ≤ w a := by
    intro a ha
    have hcard : (((univ : Finset (Fin n)).filter (fun i => a ∈ S i)).card : ℝ) ≤ 1 := by
      exact_mod_cast card_filter_le_one S hSdisj a
    have hEq : ∑ i : Fin n, (if a ∈ S i then w a else 0)
        = (((univ : Finset (Fin n)).filter (fun i => a ∈ S i)).card : ℝ) * w a := by
      rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul]
    rw [hEq]; nlinarith [hw a ha]
  have h4 : ∑ a ∈ A, ∑ i : Fin n, (if a ∈ S i then w a else 0) ≤ ∑ a ∈ A, w a :=
    Finset.sum_le_sum h3
  linarith [h1, h2 ▸ h1, h4]

/-- **Branch reduction.**  Let `R` be a region of poses (centre, angle) and `λ` a real number.
If every closed unit square inside `C` whose pose lies in `R` captures weight `≥ 1 + λ` and every
other one captures `≥ 1`, then a packing of `n` squares of side `L > 1` with exactly `k` squares
whose pose lies in `R` satisfies `n + λ k ≤ W`.  This is what a branch certificate
(`certificates/FORMAT.md`) asserts; with `λ = 0` it is `packing_le_weight`. -/
theorem packing_le_weight_region
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (R : ℝ × ℝ → ℝ → Prop) (lam : ℝ)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        (if R c θ then 1 + lam else 1) ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) + lam * (((univ : Finset (Fin n)).filter
        (fun i => R (ctr i) (ang i))).card : ℝ) ≤ ∑ a ∈ A, w a := by
  have h := packing_le_weight_thresh A w hw C (fun c θ => if R c θ then 1 + lam else 1) hcover
    n L hL ctr ang hin hdisj
  have e : ∀ i : Fin n, (if R (ctr i) (ang i) then (1:ℝ) + lam else 1)
      = 1 + lam * (if R (ctr i) (ang i) then 1 else 0) := by
    intro i; split_ifs <;> simp
  have hsum : ∑ i : Fin n, (if R (ctr i) (ang i) then (1:ℝ) + lam else 1)
      = (n : ℝ) + lam * (((univ : Finset (Fin n)).filter
          (fun i => R (ctr i) (ang i))).card : ℝ) := by
    simp_rw [e]
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_boole]
    simp
  simpa [hsum] using h

/-- **Several regions.**  Regions `R j` with multipliers `lam j`, `j : Fin m`: a square whose pose
lies in `R j` must capture `1 + lam j` more than a square outside every region (the
thresholds add if regions overlap); then `n + ∑ j, lam j · #{i | pose i ∈ R j} ≤ W`.  This is
the per-corner branch certificate (`lambda L1 L2 L3 L4 / k K1 K2 K3 K4`). -/
theorem packing_le_weight_regions
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (m : ℕ) (R : Fin m → ℝ × ℝ → ℝ → Prop) (lam : Fin m → ℝ)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        1 + ∑ j : Fin m, (if R j c θ then lam j else 0)
          ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) + ∑ j : Fin m, lam j * (((univ : Finset (Fin n)).filter
        (fun i => R j (ctr i) (ang i))).card : ℝ) ≤ ∑ a ∈ A, w a := by
  have h := packing_le_weight_thresh A w hw C
    (fun c θ => 1 + ∑ j : Fin m, (if R j c θ then lam j else 0)) hcover n L hL ctr ang hin hdisj
  have hsum : ∑ i : Fin n, (1 + ∑ j : Fin m, (if R j (ctr i) (ang i) then lam j else 0))
      = (n : ℝ) + ∑ j : Fin m, lam j * (((univ : Finset (Fin n)).filter
          (fun i => R j (ctr i) (ang i))).card : ℝ) := by
    rw [Finset.sum_add_distrib, Finset.sum_comm]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    congr 1
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]
  simpa [hsum] using h

/-- **Several regions, choice form.**  This is the hypothesis a *cell-based* verifier can actually
discharge, and it is weaker than `packing_le_weight_regions`'s: it asks only that a square whose
pose lies in `R j` capture `1 + lam j`, *separately for each* `j` containing the pose, i.e. that
it capture `1 + max {lam j : pose ∈ R j}`.  The regions need be neither disjoint nor exhaustive.

The conclusion is then relative to an arbitrary *assignment* `σ` of each square of the packing to
one region containing its pose: `n + ∑ i, lam (σ i) ≤ W`.  So a certificate satisfying this
hypothesis refutes the occupancy pattern `k` **for every tie-break at a region boundary at once**:
a pose lying in two regions may be booked to either one, and the certificate is valid for both
readings.  With disjoint regions `σ` is unique and this is `packing_le_weight_regions`.

See `notes/branch-semantics.md`; `∑ i, lam (σ i) = ∑ j, lam j * #{i | σ i = j}` is
`sum_assign_eq_sum_counts` below. -/
theorem packing_le_weight_regions_choice
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (m : ℕ) (R : Fin m → ℝ × ℝ → ℝ → Prop) (lam : Fin m → ℝ)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C → ∀ j : Fin m, R j c θ →
        1 + lam j ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L))
    (σ : Fin n → Fin m) (hσ : ∀ i, R (σ i) (ctr i) (ang i)) :
    (n : ℝ) + ∑ i : Fin n, lam (σ i) ≤ ∑ a ∈ A, w a := by
  -- the threshold form with `t` = the captured weight itself is a tautology, and gives
  -- `∑ i, capture i ≤ W`
  have h := packing_le_weight_thresh A w hw C
    (fun c θ => ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a) (fun _ _ _ => le_rfl)
    n L hL ctr ang hin hdisj
  -- every unit square of the packing is inside `C` (the same step as in `packing_le_weight_thresh`)
  have hIntSub : ∀ (c : ℝ × ℝ) (θ : ℝ), sqInt c θ L ⊆ sq c θ L := by
    rintro c θ p ⟨h1, h2⟩; exact ⟨le_of_lt h1, le_of_lt h2⟩
  have hU : ∀ i, sq (ctr i) (ang i) 1 ⊆ C := fun i =>
    subset_trans (subset_trans (unit_subset_interior hL) (hIntSub _ _)) (hin i)
  have h1 : ∑ i : Fin n, (1 + lam (σ i))
      ≤ ∑ i : Fin n, ∑ a ∈ A.filter (fun a => a ∈ sq (ctr i) (ang i) 1), w a :=
    Finset.sum_le_sum fun i _ => hcover (ctr i) (ang i) (hU i) (σ i) (hσ i)
  have h2 : ∑ i : Fin n, ((1 : ℝ) + lam (σ i)) = (n : ℝ) + ∑ i : Fin n, lam (σ i) := by
    rw [Finset.sum_add_distrib]; simp
  linarith [h2 ▸ h1]

/-- Bookkeeping: an assignment's total multiplier is the multipliers weighted by the counts. -/
lemma sum_assign_eq_sum_counts {n m : ℕ} (lam : Fin m → ℝ) (σ : Fin n → Fin m) :
    ∑ i : Fin n, lam (σ i)
      = ∑ j : Fin m, lam j * (((univ : Finset (Fin n)).filter (fun i => σ i = j)).card : ℝ) := by
  have e : ∀ i : Fin n, lam (σ i) = ∑ j : Fin m, (if σ i = j then lam j else 0) := by
    intro i; simp
  simp_rw [e]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]

/-- **Cliques.**  A set of poses `K` is a *clique* if any two closed unit squares with poses in it
share a point.  In a packing (pairwise disjoint interiors of `L`-squares, `L > 1`) at most one
square has its pose in a clique: the concentric closed unit squares of two such squares would
share a point lying in both interiors. -/
lemma card_filter_clique_le_one {n : ℕ} (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L))
    (K : ℝ × ℝ → ℝ → Prop)
    (hK : ∀ (c c' : ℝ × ℝ) (θ θ' : ℝ), K c θ → K c' θ' → (sq c θ 1 ∩ sq c' θ' 1).Nonempty) :
    ((univ : Finset (Fin n)).filter (fun i => K (ctr i) (ang i))).card ≤ 1 := by
  rw [card_le_one]
  intro i hi j hj
  simp only [mem_filter, mem_univ, true_and] at hi hj
  by_contra hne
  obtain ⟨p, hpi, hpj⟩ := hK _ _ _ _ hi hj
  exact Set.disjoint_left.mp (hdisj i j hne) (unit_subset_interior hL hpi) (unit_subset_interior hL hpj)

/-- **Box cliques are cliques.**  If the poses of a family are split into pieces `B i` (the boxes),
each piece has a *core* `core i` contained in every closed unit square with a pose in the piece,
and the cores pairwise meet, then any two squares of the family share a point.  This is exactly
what the verifier checks for a `cliques` block (`certificates/FORMAT.md`): the core of a box is the
concentric shrunk square common to all its poses, and the pairwise test is an exact separating-axis
test.  The inclusion `core i ⊆ sq c θ 1` is the verifier's shrink lemma (a unit square at any
angle of a bin contains the concentric `σ_k`-square at the bin's first angle), stated here as the
hypothesis `hcore`. -/
lemma clique_of_cores {ι : Type*} (B : ι → ℝ × ℝ → ℝ → Prop) (core : ι → Set (ℝ × ℝ))
    (hcore : ∀ i (c : ℝ × ℝ) (θ : ℝ), B i c θ → core i ⊆ sq c θ 1)
    (hmeet : ∀ i j, (core i ∩ core j).Nonempty) :
    ∀ (c c' : ℝ × ℝ) (θ θ' : ℝ), (∃ i, B i c θ) → (∃ j, B j c' θ') →
      (sq c θ 1 ∩ sq c' θ' 1).Nonempty := by
  rintro c c' θ θ' ⟨i, hi⟩ ⟨j, hj⟩
  exact (hmeet i j).mono (Set.inter_subset_inter (hcore i c θ hi) (hcore j c' θ' hj))

/-- **Anchor cliques are cliques** (Lemma 0 of `notes/clique-family.md`).  The poses of the family
are split into pieces `P i`; piece `i` holds only poses whose square *contains* the anchor `anc i`
(`hcontains`) and *meets* the anchor `anc j` for every `j` that piece `i` filters (`hmeets`).  The
well-formedness hypothesis `hpair` is what the verifier checks for an `anchors` block: for every
ordered pair of pieces, either the two anchors intersect or one of the pieces filters the other's
anchor.  Then any two squares of the family share a point — three cases, no geometry, no shrink
lemma.  (`clique_of_cores` stays for box cliques: it is the case of pairwise meeting anchors with
no filters.) -/
lemma clique_of_anchors {ι : Type*} (P : ι → ℝ × ℝ → ℝ → Prop) (anc : ι → Set (ℝ × ℝ))
    (Filters : ι → ι → Prop)
    (hcontains : ∀ i (c : ℝ × ℝ) (θ : ℝ), P i c θ → anc i ⊆ sq c θ 1)
    (hmeets : ∀ i j (c : ℝ × ℝ) (θ : ℝ), P i c θ → Filters i j → (sq c θ 1 ∩ anc j).Nonempty)
    (hpair : ∀ i j, (anc i ∩ anc j).Nonempty ∨ Filters i j ∨ Filters j i) :
    ∀ (c c' : ℝ × ℝ) (θ θ' : ℝ), (∃ i, P i c θ) → (∃ j, P j c' θ') →
      (sq c θ 1 ∩ sq c' θ' 1).Nonempty := by
  rintro c c' θ θ' ⟨i, hi⟩ ⟨j, hj⟩
  rcases hpair i j with h | h | h
  · -- the anchors share a point, and each square contains its own anchor
    exact h.mono (Set.inter_subset_inter (hcontains i c θ hi) (hcontains j c' θ' hj))
  · -- the first square meets `anc j`, which the second square contains
    obtain ⟨p, hp1, hp2⟩ := hmeets i j c θ hi h
    exact ⟨p, hp1, hcontains j c' θ' hj hp2⟩
  · -- symmetrically
    obtain ⟨p, hp1, hp2⟩ := hmeets j i c' θ' hj h
    exact ⟨p, hcontains i c θ hi hp2, hp1⟩

/-- **Clique reduction.**  Points `A` with weights `w ≥ 0` and cliques `K j` with weights `v j ≥ 0`
(`j : Fin m`): if every closed unit square inside `C` is covered by weight `≥ 1` by the points it
contains together with the cliques it belongs to, then a packing of `n` squares of side `L > 1`
satisfies `n ≤ ∑ w + ∑ v`.  Points are the special case of cliques (`K = {poses containing p}`),
and `packing_le_weight` is the case `m = 0`. -/
theorem packing_le_weight_cliques
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (m : ℕ) (K : Fin m → ℝ × ℝ → ℝ → Prop) (v : Fin m → ℝ) (hv : ∀ j, 0 ≤ v j)
    (hK : ∀ j (c c' : ℝ × ℝ) (θ θ' : ℝ), K j c θ → K j c' θ' → (sq c θ 1 ∩ sq c' θ' 1).Nonempty)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a
              + ∑ j : Fin m, (if K j c θ then v j else 0))
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hin : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) ≤ ∑ a ∈ A, w a + ∑ j : Fin m, v j := by
  have h := packing_le_weight_thresh A w hw C
    (fun c θ => 1 - ∑ j : Fin m, (if K j c θ then v j else 0))
    (fun c θ hc => by linarith [hcover c θ hc]) n L hL ctr ang hin hdisj
  have hsum : ∑ i : Fin n, (1 - ∑ j : Fin m, (if K j (ctr i) (ang i) then v j else 0))
      = (n : ℝ) - ∑ j : Fin m, v j * (((univ : Finset (Fin n)).filter
          (fun i => K j (ctr i) (ang i))).card : ℝ) := by
    rw [Finset.sum_sub_distrib, Finset.sum_comm]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    congr 1
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]
  have hcard : ∀ j : Fin m, v j * (((univ : Finset (Fin n)).filter
      (fun i => K j (ctr i) (ang i))).card : ℝ) ≤ v j := by
    intro j
    have h1 : (((univ : Finset (Fin n)).filter (fun i => K j (ctr i) (ang i))).card : ℝ) ≤ 1 := by
      exact_mod_cast card_filter_clique_le_one L hL ctr ang hdisj (K j) (hK j)
    nlinarith [hv j]
  have h2 : ∑ j : Fin m, v j * (((univ : Finset (Fin n)).filter
      (fun i => K j (ctr i) (ang i))).card : ℝ) ≤ ∑ j : Fin m, v j :=
    Finset.sum_le_sum fun j _ => hcard j
  rw [hsum] at h
  linarith

/-- **Anchor-clique certificate, end to end.**  `m` anchor cliques, the `j`-th a union of pieces
`P j i` with anchors `anc j i` and filter relation `Filters j`, all satisfying Lemma 0's
hypotheses; a pose belongs to clique `j` iff it belongs to one of its pieces.  If every closed unit
square inside `C` captures weight `≥ 1` from the points it contains together with the cliques it
belongs to, then a packing of `n` squares of side `L > 1` in `C` has `n ≤ ∑ w + ∑ v`.  This is
`packing_le_weight_cliques` with its clique hypothesis discharged by `clique_of_anchors`, i.e.
exactly what a certificate with an `anchors` block asserts (`certificates/FORMAT.md`). -/
theorem packing_le_weight_anchor_cliques
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (m : ℕ) {ι : Type*}
    (P : Fin m → ι → ℝ × ℝ → ℝ → Prop) (anc : Fin m → ι → Set (ℝ × ℝ))
    (Filters : Fin m → ι → ι → Prop) (v : Fin m → ℝ) (hv : ∀ j, 0 ≤ v j)
    (hcontains : ∀ j i (c : ℝ × ℝ) (θ : ℝ), P j i c θ → anc j i ⊆ sq c θ 1)
    (hmeets : ∀ j i i' (c : ℝ × ℝ) (θ : ℝ),
        P j i c θ → Filters j i i' → (sq c θ 1 ∩ anc j i').Nonempty)
    (hpair : ∀ j i i', (anc j i ∩ anc j i').Nonempty ∨ Filters j i i' ∨ Filters j i' i)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a
              + ∑ j : Fin m, (if ∃ i, P j i c θ then v j else 0))
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hsub : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) ≤ ∑ a ∈ A, w a + ∑ j : Fin m, v j :=
  packing_le_weight_cliques A w hw C m (fun j c θ => ∃ i, P j i c θ) v hv
    (fun j => clique_of_anchors (P j) (anc j) (Filters j) (hcontains j) (hmeets j) (hpair j))
    hcover n L hL ctr ang hsub hdisj

/-- **Regions and cliques together.**  This is what a *branch* certificate carrying a clique block
asserts (`certificates/FORMAT.md`), which is what `search/branch.py --cliques` produces: points `A`
with weights `w ≥ 0`, regions `R j` with multipliers `lam j`, cliques `K i` with weights `v i ≥ 0`,
and every closed unit square inside `C` capturing `1 + ∑_j [pose ∈ R j]·lam j` from the points it
contains together with the cliques it belongs to.  Then a packing of `n` squares of side `L > 1`
satisfies `n + ∑_j lam j · #{i : pose i ∈ R j} ≤ ∑ w + ∑ v`, so a certificate whose
`∑ w + ∑ v − ∑_j lam j k_j` is `< n` refutes every packing with that occupancy pattern.  It is
`packing_le_weight_regions` and `packing_le_weight_cliques` in one. -/
theorem packing_le_weight_regions_cliques
    (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ) (hw : ∀ a ∈ A, 0 ≤ w a)
    (C : Set (ℝ × ℝ)) (mr : ℕ) (R : Fin mr → ℝ × ℝ → ℝ → Prop) (lam : Fin mr → ℝ)
    (mk : ℕ) (K : Fin mk → ℝ × ℝ → ℝ → Prop) (v : Fin mk → ℝ) (hv : ∀ i, 0 ≤ v i)
    (hK : ∀ i (c c' : ℝ × ℝ) (θ θ' : ℝ), K i c θ → K i c' θ' → (sq c θ 1 ∩ sq c' θ' 1).Nonempty)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ C →
        1 + ∑ j : Fin mr, (if R j c θ then lam j else 0)
          ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a
              + ∑ i : Fin mk, (if K i c θ then v i else 0))
    (n : ℕ) (L : ℝ) (hL : 1 < L) (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ)
    (hsub : ∀ i, sq (ctr i) (ang i) L ⊆ C)
    (hdisj : ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) L) (sqInt (ctr j) (ang j) L)) :
    (n : ℝ) + ∑ j : Fin mr, lam j * (((univ : Finset (Fin n)).filter
        (fun i => R j (ctr i) (ang i))).card : ℝ) ≤ ∑ a ∈ A, w a + ∑ i : Fin mk, v i := by
  have h := packing_le_weight_thresh A w hw C
    (fun c θ => 1 + ∑ j : Fin mr, (if R j c θ then lam j else 0)
                  - ∑ i : Fin mk, (if K i c θ then v i else 0))
    (fun c θ hc => by linarith [hcover c θ hc]) n L hL ctr ang hsub hdisj
  have e1 : ∑ i : Fin n, (1 + ∑ j : Fin mr, (if R j (ctr i) (ang i) then lam j else 0))
      = (n : ℝ) + ∑ j : Fin mr, lam j * (((univ : Finset (Fin n)).filter
          (fun i => R j (ctr i) (ang i))).card : ℝ) := by
    rw [Finset.sum_add_distrib, Finset.sum_comm]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    congr 1
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]
  have e2 : ∑ i : Fin n, ∑ l : Fin mk, (if K l (ctr i) (ang i) then v l else 0)
      = ∑ l : Fin mk, v l * (((univ : Finset (Fin n)).filter
          (fun i => K l (ctr i) (ang i))).card : ℝ) := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun l _ => ?_
    rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, mul_comm]
  have hsum : ∑ i : Fin n, (1 + ∑ j : Fin mr, (if R j (ctr i) (ang i) then lam j else 0)
                              - ∑ l : Fin mk, (if K l (ctr i) (ang i) then v l else 0))
      = ((n : ℝ) + ∑ j : Fin mr, lam j * (((univ : Finset (Fin n)).filter
            (fun i => R j (ctr i) (ang i))).card : ℝ))
        - ∑ l : Fin mk, v l * (((univ : Finset (Fin n)).filter
            (fun i => K l (ctr i) (ang i))).card : ℝ) := by
    rw [Finset.sum_sub_distrib, e1, e2]
  have hcard : ∀ l : Fin mk, v l * (((univ : Finset (Fin n)).filter
      (fun i => K l (ctr i) (ang i))).card : ℝ) ≤ v l := by
    intro l
    have h1 : (((univ : Finset (Fin n)).filter (fun i => K l (ctr i) (ang i))).card : ℝ) ≤ 1 := by
      exact_mod_cast card_filter_clique_le_one L hL ctr ang hdisj (K l) (hK l)
    nlinarith [hv l]
  have h2 : ∑ l : Fin mk, v l * (((univ : Finset (Fin n)).filter
      (fun i => K l (ctr i) (ang i))).card : ℝ) ≤ ∑ l : Fin mk, v l :=
    Finset.sum_le_sum fun l _ => hcard l
  rw [hsum] at h
  linarith

/-- Scaling by `μ > 0` turns a unit square into a square of side `μ`. -/
lemma sq_scale (c : ℝ × ℝ) (θ μ : ℝ) (hμ : 0 < μ) (p : ℝ × ℝ) (hp : p ∈ sq c θ 1) :
    (μ * p.1, μ * p.2) ∈ sq (μ * c.1, μ * c.2) θ μ := by
  obtain ⟨h1, h2⟩ := hp
  have e1 : (coord (μ * c.1, μ * c.2) θ (μ * p.1, μ * p.2)).1 = μ * (coord c θ p).1 := by
    simp only [coord]; ring
  have e2 : (coord (μ * c.1, μ * c.2) θ (μ * p.1, μ * p.2)).2 = μ * (coord c θ p).2 := by
    simp only [coord]; ring
  refine ⟨?_, ?_⟩
  · rw [e1, abs_mul, abs_of_pos hμ]; nlinarith [abs_nonneg (coord c θ p).1]
  · rw [e2, abs_mul, abs_of_pos hμ]; nlinarith [abs_nonneg (coord c θ p).2]

/-- Interiors scale the same way. -/
lemma sqInt_scale (c : ℝ × ℝ) (θ μ : ℝ) (hμ : 0 < μ) (p : ℝ × ℝ) (hp : p ∈ sqInt c θ 1) :
    (μ * p.1, μ * p.2) ∈ sqInt (μ * c.1, μ * c.2) θ μ := by
  obtain ⟨h1, h2⟩ := hp
  have e1 : (coord (μ * c.1, μ * c.2) θ (μ * p.1, μ * p.2)).1 = μ * (coord c θ p).1 := by
    simp only [coord]; ring
  have e2 : (coord (μ * c.1, μ * c.2) θ (μ * p.1, μ * p.2)).2 = μ * (coord c θ p).2 := by
    simp only [coord]; ring
  refine ⟨?_, ?_⟩
  · rw [e1, abs_mul, abs_of_pos hμ]; nlinarith [abs_nonneg (coord c θ p).1]
  · rw [e2, abs_mul, abs_of_pos hμ]; nlinarith [abs_nonneg (coord c θ p).2]

end SquarePacking
