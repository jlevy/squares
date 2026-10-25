import Compact.Cases.FourSquare
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! Whole original-case obligations discharged by the shared symbolic theorem.
The row/family identity is kernel checked against the original retained rows. -/
namespace N12Compact.FourSquareCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {28,78,537,556,565,567,569,570,575,576,577,585,1085,1086,1087}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(28,family28),(78,family78),(537,family537),(556,family556),(565,family565),(567,family567),(569,family569),(570,family570),(575,family575),(576,family576),(577,family577),(585,family585),(1085,family1085),(1086,family1086),(1087,family1087)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact case28_impossible
  · exact case78_impossible
  · exact case537_impossible
  · exact case556_impossible
  · exact case565_impossible
  · exact case567_impossible
  · exact case569_impossible
  · exact case570_impossible
  · exact case575_impossible
  · exact case576_impossible
  · exact case577_impossible
  · exact case585_impossible
  · exact case1085_impossible
  · exact case1086_impossible
  · exact case1087_impossible

private theorem row28_checked :
    (RowIdentity.rowAt 67).originalId = 28 ∧
    (RowIdentity.rowAt 67).groups = family28 := by decide +kernel

private theorem row78_checked :
    (RowIdentity.rowAt 117).originalId = 78 ∧
    (RowIdentity.rowAt 117).groups = family78 := by decide +kernel

private theorem row537_checked :
    (RowIdentity.rowAt 278).originalId = 537 ∧
    (RowIdentity.rowAt 278).groups = family537 := by decide +kernel

private theorem row556_checked :
    (RowIdentity.rowAt 297).originalId = 556 ∧
    (RowIdentity.rowAt 297).groups = family556 := by decide +kernel

private theorem row565_checked :
    (RowIdentity.rowAt 306).originalId = 565 ∧
    (RowIdentity.rowAt 306).groups = family565 := by decide +kernel

private theorem row567_checked :
    (RowIdentity.rowAt 308).originalId = 567 ∧
    (RowIdentity.rowAt 308).groups = family567 := by decide +kernel

private theorem row569_checked :
    (RowIdentity.rowAt 310).originalId = 569 ∧
    (RowIdentity.rowAt 310).groups = family569 := by decide +kernel

private theorem row570_checked :
    (RowIdentity.rowAt 311).originalId = 570 ∧
    (RowIdentity.rowAt 311).groups = family570 := by decide +kernel

private theorem row575_checked :
    (RowIdentity.rowAt 316).originalId = 575 ∧
    (RowIdentity.rowAt 316).groups = family575 := by decide +kernel

private theorem row576_checked :
    (RowIdentity.rowAt 317).originalId = 576 ∧
    (RowIdentity.rowAt 317).groups = family576 := by decide +kernel

private theorem row577_checked :
    (RowIdentity.rowAt 318).originalId = 577 ∧
    (RowIdentity.rowAt 318).groups = family577 := by decide +kernel

private theorem row585_checked :
    (RowIdentity.rowAt 326).originalId = 585 ∧
    (RowIdentity.rowAt 326).groups = family585 := by decide +kernel

private theorem row1085_checked :
    (RowIdentity.rowAt 569).originalId = 1085 ∧
    (RowIdentity.rowAt 569).groups = family1085 := by decide +kernel

private theorem row1086_checked :
    (RowIdentity.rowAt 570).originalId = 1086 ∧
    (RowIdentity.rowAt 570).groups = family1086 := by decide +kernel

private theorem row1087_checked :
    (RowIdentity.rowAt 571).originalId = 1087 ∧
    (RowIdentity.rowAt 571).groups = family1087 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h | h | h | h | h | h | h | h | h | h | h | h | h | h
  · have hf := RowIdentity.family_at 67 28 family28 row28_checked r hr h
    simpa only [h, hf] using
      (show (28, family28) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 117 78 family78 row78_checked r hr h
    simpa only [h, hf] using
      (show (78, family78) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 278 537 family537 row537_checked r hr h
    simpa only [h, hf] using
      (show (537, family537) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 297 556 family556 row556_checked r hr h
    simpa only [h, hf] using
      (show (556, family556) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 306 565 family565 row565_checked r hr h
    simpa only [h, hf] using
      (show (565, family565) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 308 567 family567 row567_checked r hr h
    simpa only [h, hf] using
      (show (567, family567) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 310 569 family569 row569_checked r hr h
    simpa only [h, hf] using
      (show (569, family569) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 311 570 family570 row570_checked r hr h
    simpa only [h, hf] using
      (show (570, family570) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 316 575 family575 row575_checked r hr h
    simpa only [h, hf] using
      (show (575, family575) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 317 576 family576 row576_checked r hr h
    simpa only [h, hf] using
      (show (576, family576) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 318 577 family577 row577_checked r hr h
    simpa only [h, hf] using
      (show (577, family577) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 326 585 family585 row585_checked r hr h
    simpa only [h, hf] using
      (show (585, family585) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 569 1085 family1085 row1085_checked r hr h
    simpa only [h, hf] using
      (show (1085, family1085) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 570 1086 family1086 row1086_checked r hr h
    simpa only [h, hf] using
      (show (1086, family1086) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 571 1087 family1087 row1087_checked r hr h
    simpa only [h, hf] using
      (show (1087, family1087) ∈ coveredFamilies from by simp [coveredFamilies])

/-- Each covered identifier is the full original retained-row obligation. -/
theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareCases
