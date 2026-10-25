import S12.Seeds
import S12.HullData
import S12.PackingBudget

namespace S12
set_option Elab.async false
open S12Pilot
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def hullRows : List ((Nat × Nat) × HullConflictCertificate) := conflictingPairs.zip hullCerts

def HullRowCheck (r : (Nat × Nat) × HullConflictCertificate) : Prop :=
  r.1.1≠r.1.2 ∧ r.2.Check ∧
  (∀ p∈r.2.leftSeeds, p∈seedPoints (maskSupport r.1.1)) ∧
  (∀ p∈r.2.rightSeeds, p∈seedPoints (maskSupport r.1.2))
instance decidableHullRowCheck (r : (Nat × Nat) × HullConflictCertificate) : Decidable (HullRowCheck r) :=
  inferInstanceAs (Decidable (_ ∧ _))

private theorem hullChecks_cons {c : HullConflictCertificate}
    {cs : List HullConflictCertificate} (hc : c.Check)
    (hcs : ∀ x ∈ cs, x.Check) : ∀ x ∈ c :: cs, x.Check := by
  intro x hx
  rcases List.mem_cons.mp hx with rfl | hx
  · exact hc
  · exact hcs x hx

/-- Reuse each already accepted rational certificate exactly once. -/
private theorem hullCertificates_checked : ∀ c ∈ hullCerts, c.Check := by
  exact hullChecks_cons hullCert0_checked <|
    hullChecks_cons hullCert1_checked <|
    hullChecks_cons hullCert2_checked <|
    hullChecks_cons hullCert3_checked <|
    hullChecks_cons hullCert4_checked <|
    hullChecks_cons hullCert5_checked <|
    hullChecks_cons hullCert6_checked <|
    hullChecks_cons hullCert7_checked <|
    hullChecks_cons hullCert8_checked <|
    hullChecks_cons hullCert9_checked <|
    hullChecks_cons hullCert10_checked <|
    hullChecks_cons hullCert11_checked <|
    hullChecks_cons hullCert12_checked <|
    hullChecks_cons hullCert13_checked <|
    hullChecks_cons hullCert14_checked <|
    hullChecks_cons hullCert15_checked <|
    hullChecks_cons hullCert16_checked <|
    hullChecks_cons hullCert17_checked <|
    hullChecks_cons hullCert18_checked <|
    hullChecks_cons hullCert19_checked <|
    hullChecks_cons hullCert20_checked <|
    hullChecks_cons hullCert21_checked <|
    hullChecks_cons hullCert22_checked <|
    hullChecks_cons hullCert23_checked <|
    hullChecks_cons hullCert24_checked <|
    hullChecks_cons hullCert25_checked <|
    hullChecks_cons hullCert26_checked <|
    hullChecks_cons hullCert27_checked <|
    hullChecks_cons hullCert28_checked <|
    hullChecks_cons hullCert29_checked <|
    hullChecks_cons hullCert30_checked <|
    hullChecks_cons hullCert31_checked <|
    hullChecks_cons hullCert32_checked <|
    hullChecks_cons hullCert33_checked <|
    hullChecks_cons hullCert34_checked <|
    hullChecks_cons hullCert35_checked <|
    hullChecks_cons hullCert36_checked <|
    by intro c hc; cases hc

private def HullSeedCheck (r : (Nat × Nat) × HullConflictCertificate) : Prop :=
  r.1.1 ≠ r.1.2 ∧
  (∀ p ∈ r.2.leftSeeds, p ∈ seedPoints (maskSupport r.1.1)) ∧
  (∀ p ∈ r.2.rightSeeds, p ∈ seedPoints (maskSupport r.1.2))

private instance (r : (Nat × Nat) × HullConflictCertificate) :
    Decidable (HullSeedCheck r) := inferInstanceAs (Decidable (_ ∧ _))

/-- Only the key inequalities and actual seed membership remain finite checks. -/
private theorem hullRows_seeds_checked :
    hullRows.all (fun r => decide (HullSeedCheck r)) = true := by decide +kernel

/-- The identities and every seed premise are checked, not merely the
number of certificates. -/
theorem hullRows_keys : hullRows.map Prod.fst = conflictingPairs := by rfl

theorem hullRows_checked : hullRows.all (fun r => decide (HullRowCheck r))=true := by
  apply List.all_eq_true.mpr
  intro row hrow
  apply decide_eq_true
  have seeds := of_decide_eq_true (List.all_eq_true.mp hullRows_seeds_checked row hrow)
  have cert : row.2.Check := hullCertificates_checked row.2 (List.of_mem_zip hrow).2
  exact ⟨seeds.1,cert,seeds.2⟩

theorem certified_pair_overlap (m n : Nat) (hmn : (m,n)∈conflictingPairs)
    (q r : OpenSquare) (hq : 1<q.side) (hr : 1<r.side)
    (hqs : q.side≤1001/1000) (hrs : r.side≤1001/1000)
    (hqb : InsideContainer q) (hrb : InsideContainer r)
    (hqe : ExactMarkers q (maskSupport m)) (hre : ExactMarkers r (maskSupport n)) :
    m≠n ∧ ∃ x y, q.Inside x y ∧ r.Inside x y := by
  rw [← hullRows_keys] at hmn
  obtain ⟨row,hrow,heq⟩ := List.mem_map.mp hmn
  have hc := of_decide_eq_true (List.all_eq_true.mp hullRows_checked row hrow)
  obtain ⟨hne,hw,hl,hr'⟩ := hc
  have hm : row.1.1=m := congrArg Prod.fst heq
  have hn : row.1.2=n := congrArg Prod.snd heq
  simp only [hm,hn] at hne hl hr'
  refine ⟨hne, hull_conflict_certificate_sound row.2 hw q r ?_ ?_⟩
  · intro p hp
    exact seed_points_sound q hq hqs hqb _ hqe p (hl p hp)
  · intro p hp
    exact seed_points_sound r hr hrs hrb _ hre p (hr' p hp)

theorem coded_exact (p : NormalizedPacking) (i : Fin 12) :
    ExactMarkers (p.square i) (maskSupport (markerCode p i)) := by
  intro m
  rw [(markerCode_spec p i).2]
  exact (mem_markerOwners p i m).symm

theorem packing_no_conflicting_pair (p : NormalizedPacking) (m n : Nat)
    (hmn : (m,n)∈conflictingPairs) :
    ¬(m∈codedMarkerFamily p ∧ n∈codedMarkerFamily p) := by
  rintro ⟨hm,hn⟩
  obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hm
  obtain ⟨j,_,rfl⟩ := Finset.mem_image.mp hn
  obtain ⟨hne,x,y,hx,hy⟩ := certified_pair_overlap _ _ hmn (p.square i) (p.square j)
    (by rw [p.congruent]; exact p.side_gt_one) (by rw [p.congruent]; exact p.side_gt_one)
    (by rw [p.congruent]; exact p.side_le) (by rw [p.congruent]; exact p.side_le)
    (p.contained i) (p.contained j) (coded_exact p i) (coded_exact p j)
  have hij : i≠j := by intro h; subst j; exact hne rfl
  exact p.disjoint i j hij x y ⟨hx,hy⟩

theorem packing_earlyOK (p : NormalizedPacking) : earlyOK (codedMarkerFamily p)=true := by
  have hb := packing_pair_budgets p
  have hall : conflictingPairs.all (fun z =>
      !(decide (z.1∈codedMarkerFamily p) && decide (z.2∈codedMarkerFamily p)))=true := by
    apply List.all_eq_true.mpr
    intro z hz
    have h := packing_no_conflicting_pair p z.1 z.2 hz
    by_cases h0 : z.1∈codedMarkerFamily p
    · have h1 : z.2∉codedMarkerFamily p := fun h1 => h ⟨h0,h1⟩
      simp [h0,h1]
    · simp [h0]
  unfold earlyOK
  rw [hall]
  simp [badMasks,hb.1,hb.2]

/-- The complete geometric reduction to the 577 representatives. -/
theorem packing_reduction_to_577 (p : NormalizedPacking) :
    ∃ r∈coverRows, codedMarkerFamily p∈orbit r.groups :=
  reduction_to_577 _ (codedMarkerFamily_admissible p) (codedMarkerFamily_card p) (packing_earlyOK p)

#print axioms packing_earlyOK
#print axioms packing_reduction_to_577
end S12
