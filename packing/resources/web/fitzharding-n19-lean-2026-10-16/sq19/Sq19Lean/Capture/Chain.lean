import Sq19Lean.Capture.Basic
import Sq17Lean.CaptureRunSound

/-! Chunked checking of one long run, so that the pieces can be checked in parallel modules.

* The angle table is checked in slices of `S` entries: `rangeOK` on slice `c` checks entries `c*S .. c*S+S-1`
  against the bounds of that slice (entries past the end of the table need nothing). Slices covering the table
  give `TableValid` (`tableValid_of_slices`).
* The run is cut into `K` segments with explicit boundary states `E 0, ..., E K`; each segment is accepted by
  the 17 project's `runToCheck` (the replay ends exactly at the next boundary state). `chain_sound` composes the
  segments with `open_segment_sound`.

No finite data is checked in this file. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState Sq17.Propagation.HalfPlaneInt

def rangeOK (n : ℕ) (T : Array Entry) (B : Array (TrigBounds × TrigBounds)) (a : ℕ) : Bool :=
  (List.range B.size).all fun j =>
    match T[a+j]? with
    | none => true
    | some e => match B[j]? with
      | some b => entryOK n e b
      | none => false

theorem rangeOK_sound (T : Array Entry) (B : Array (TrigBounds × TrigBounds)) (a : ℕ)
    (h : rangeOK 44 T B a = true) (j : ℕ) (hj : j < B.size) (e : Entry) (he : T[a+j]? = some e) :
    e.Valid 44 := by
  have h1 := List.all_eq_true.mp h j (List.mem_range.mpr hj)
  simp only [he] at h1
  split at h1
  · next b hb =>
    simp only [entryOK, Bool.and_eq_true] at h1
    exact ⟨⟨e.core b.1 b.2, h1.1, rfl, rfl, rfl, rfl, rfl⟩, ⟨e.wallRow b.1 b.2, h1.2, rfl, rfl, rfl⟩⟩
  · simp at h1

theorem tableValid_of_slices (T : Array Entry) (S C : ℕ) (bnds : ℕ → Array (TrigBounds × TrigBounds))
    (hS : 0 < S) (hT : T.size ≤ C * S) (hsize : ∀ c, c < C → (bnds c).size = S)
    (hok : ∀ c, c < C → rangeOK 44 T (bnds c) (c * S) = true) : TableValid T 44 := by
  intro k e hk
  have hlt : k < T.size := by
    by_contra hn
    rw [Array.getElem?_eq_none (not_lt.mp hn)] at hk
    simp at hk
  have hc : k / S < C := by
    rw [Nat.div_lt_iff_lt_mul hS]; omega
  have hk' : T[k / S * S + k % S]? = some e := by rw [Nat.div_add_mod' k S]; exact hk
  exact rangeOK_sound T (bnds (k / S)) (k / S * S) (hok _ hc) (k % S)
    (by rw [hsize _ hc]; exact Nat.mod_lt k hS) e hk'

theorem chain_sound (T : Array Entry) (hT : TableValid T 44) (side shift : ℚ)
    (E : ℕ → HState) (st : ℕ → List Step) :
    ∀ K : ℕ, (∀ k, k < K → runToCheck T side shift (E k) (st k) (E (k+1)) = true) →
    ∀ p : ℕ → AnglePose, Rep T (E 0) p → Packing (E 0).length p → Fits (E 0).length side shift p →
      Rep T (E K) p ∧ (E K).length = (E 0).length
  | 0, _, p, hr, _, _ => ⟨hr, rfl⟩
  | K+1, h, p, hr, hp, hf => by
    obtain ⟨hrK, hlK⟩ := chain_sound T hT side shift E st K (fun k hk => h k (by omega)) p hr hp hf
    obtain ⟨hr', hl'⟩ := open_segment_sound T side shift (E K) (E (K+1)) (st K) hT (h K (by omega)) p hrK
      (by rw [hlK]; exact hp) (by rw [hlK]; exact hf)
    exact ⟨hr', hl'.trans hlK⟩

/-- A captured piece checked in chunks. -/
theorem chunked_captured (T : Array Entry) (side shift : ℚ) (n : ℕ) (windows : ℕ → ℚ × ℚ)
    (cells : List (List (ℚ × ℚ))) (E : ℕ → HState) (st : ℕ → List Step) (K : ℕ)
    (targets : Array CaptureSummary.Target) (hT : TableValid T 44)
    (hseed : windowSeedOK T windows cells (E 0) = true) (hlen : (E 0).length = n)
    (hrun : ∀ k, k < K → runToCheck T side shift (E k) (st k) (E (k+1)) = true)
    (hsum : summaryCheckN n T (E K) targets = true)
    (p : ℕ → AnglePose) (hp : Admissible n side shift windows cells p) :
    ∀ i : Fin n, (targets[i.val]!).Holds (p i.val) := by
  subst hlen
  obtain ⟨hc, ha, hpack, hfit⟩ := hp
  have hrep := windowSeedOK_sound T windows cells (E 0) hseed p hc ha
  obtain ⟨hrK, _⟩ := chain_sound T hT side shift E st K hrun p hrep hpack hfit
  exact summaryCheckN_sound _ T (E K) targets hsum p hrK

end Sq19.Capture

#print axioms Sq19.Capture.tableValid_of_slices
#print axioms Sq19.Capture.chunked_captured
