import Sq17Lean.HalfPlaneWindowSeed
import Sq17Lean.HalfPlaneTable
import Sq17Lean.CaptureSummarySound
import Sq19Lean.Capture.SummaryFast

/-! Capture pieces for 19 squares.

A piece is one engine run from the census cells with a separately chosen angle window for every owner
(`windowSeedOK`). It either excludes every packing whose poses lie in the windows, or confines each
owner to a target (closed angle interval and half-planes): `summaryCheckN_sound` is the 17 project's
`summaryCheck_sound` with the number of owners as a parameter. `config_poses` normalizes a family of unit
squares into windows of width at least π/2; the per-state files split one owner's window into pieces.

No finite data is checked in this file. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneInt
open Sq17.Propagation.HalfPlaneState.CaptureSummary

theorem summaryCheckN_sound (n : ℕ) (T : Array Entry) (S : HState) (targets : Array Target)
    (h : summaryCheckN n T S targets = true) (p : ℕ → AnglePose) (hp : Rep T S p) :
    ∀ i : Fin n, (targets[i.val]!).Holds (p i.val) := by
  have h' := Bool.and_eq_true_iff.mp h
  have hlen := (of_decide_eq_true h'.1).1
  intro i
  have hi : i.val < S.length := by omega
  obtain ⟨r, hr, hp'⟩ := hp i.val hi
  have hi' := List.all_eq_true.mp h'.2 i.val (List.mem_range.mpr i.isLt)
  exact rowCheck_sound T _ r (List.all_eq_true.mp hi' r hr) _ hp'

/-- Poses in the windows and the cells, pairwise disjoint, inside the trace container. -/
def Admissible (n : ℕ) (side shift : ℚ) (windows : ℕ → ℚ × ℚ) (cells : List (List (ℚ × ℚ)))
    (p : ℕ → AnglePose) : Prop :=
  (∀ i, i < n → (p i).center ∈ convexHull ℝ (realPoint '' {v | v ∈ cells.getD i []})) ∧
  (∀ i, i < n → (p i).angle ∈ Set.Icc ((windows i).1:ℝ) ((windows i).2:ℝ)) ∧
  Packing n p ∧ Fits n side shift p

/-- An excluded piece. -/
theorem piece_excluded (T : Array Entry) (B : Array (TrigBounds × TrigBounds)) (side shift : ℚ)
    (n : ℕ) (windows : ℕ → ℚ × ℚ) (cells : List (List (ℚ × ℚ))) (S : HState) (steps : List Step)
    (htable : tableOK 44 T B = true) (hseed : windowSeedOK T windows cells S = true)
    (hlen : S.length = n) (hex : excludes T side shift n S steps = true)
    (p : ℕ → AnglePose) (hp : Admissible n side shift windows cells p) : False := by
  subst hlen
  obtain ⟨hc, ha, hpack, hfit⟩ := hp
  exact excludes_sound T (tableOK_sound T B htable) side shift S.length S steps le_rfl hex
    ⟨p, windowSeedOK_sound T windows cells S hseed p hc ha, hpack, hfit⟩

/-- A captured piece: every owner lies in its target. -/
theorem piece_captured (T : Array Entry) (B : Array (TrigBounds × TrigBounds)) (side shift : ℚ)
    (n : ℕ) (windows : ℕ → ℚ × ℚ) (cells : List (List (ℚ × ℚ))) (S : HState) (steps : List Step)
    (targets : Array Target)
    (htable : tableOK 44 T B = true) (hseed : windowSeedOK T windows cells S = true)
    (hlen : S.length = n) (hrun : runSummary n T side shift S steps targets = true)
    (p : ℕ → AnglePose) (hp : Admissible n side shift windows cells p) :
    ∀ i : Fin n, (targets[i.val]!).Holds (p i.val) := by
  subst hlen
  obtain ⟨hc, ha, hpack, hfit⟩ := hp
  have hrep := windowSeedOK_sound T windows cells S hseed p hc ha
  unfold runSummary at hrun
  split at hrun
  · next E hE =>
    obtain ⟨hrepE, _⟩ := runAll_sound T (tableOK_sound T B htable) side shift steps S E p hE hrep hpack hfit
    exact summaryCheckN_sound S.length T E targets hrun p hrepE
  · simp at hrun

/-- Normalization: a family of unit squares has poses with angles in any windows of width at least π/2. -/
theorem config_poses (n : ℕ) (windows : ℕ → ℚ × ℚ)
    (hwidth : ∀ i, i < n → Real.pi/2 ≤ ((windows i).2:ℝ)-((windows i).1:ℝ))
    (c u : ℕ → ℝ × ℝ) (hunit : ∀ i, i < n → (u i).1^2+(u i).2^2 = 1) :
    ∃ p : ℕ → AnglePose, ∀ i, i < n → (p i).center = c i ∧
      (p i).angle ∈ Set.Icc ((windows i).1:ℝ) ((windows i).2:ℝ) ∧
      (p i).square = Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 := by
  have H : ∀ i, ∃ θ : ℝ, i < n →
      θ ∈ Set.Icc ((windows i).1:ℝ) ((windows i).2:ℝ) ∧
      Sq17.sq (c i).1 (c i).2 (Real.cos θ) (Real.sin θ) =
        Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 := by
    intro i
    by_cases hi : i < n
    · obtain ⟨θ, hθ, heq⟩ := square_unit_direction_normalize_window
        (c i).1 (c i).2 (u i).1 (u i).2 (windows i).1 (windows i).2 (hunit i hi) (hwidth i hi)
      exact ⟨θ, fun _ => ⟨hθ, heq⟩⟩
    · exact ⟨0, fun h => (hi h).elim⟩
  choose θ hθ using H
  exact ⟨fun i => ⟨c i, θ i⟩, fun i hi => ⟨rfl, (hθ i hi).1, (hθ i hi).2⟩⟩

/-- Replace one owner's window. -/
def setWindow (base : ℕ → ℚ × ℚ) (o : ℕ) (w : ℚ × ℚ) : ℕ → ℚ × ℚ :=
  fun i => if i = o then w else base i

/-- One half of the decimal upper bound in `Real.pi_lt_d20`. -/
def halfPiUpper : ℚ := 314159265358979323847 / 200000000000000000000

theorem half_pi_le (q : ℚ) (h : halfPiUpper ≤ q) : Real.pi/2 ≤ (q:ℝ) := by
  have hp := Real.pi_lt_d20
  have hq : ((halfPiUpper:ℚ):ℝ) ≤ (q:ℝ) := by exact_mod_cast h
  simp only [halfPiUpper] at hq
  push_cast at hq
  linarith

end Sq19.Capture

#print axioms Sq19.Capture.summaryCheckN_sound
#print axioms Sq19.Capture.piece_excluded
#print axioms Sq19.Capture.piece_captured
#print axioms Sq19.Capture.config_poses
