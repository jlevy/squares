import PackingCertMathlib.Statements.Open.Stuck4
import PackingCertMathlib.Statements.Open.SnapDown

/-!
# -- OPEN: STUCK-EXIST(11) -- no 12-stuck packing of eleven squares below side 4 (A246)

`docs/proofs/construct_towards.md`.  The PI (2026-09-16, 21:30): *"is there not a way we can try and
construct towards a ring, and show that it's not possible with s < 4?"*  The statement is PURE
EXISTENCE: no locks, no forces, no Ψ-minimality anywhere.

**The statement.**  `stuck_exist_eleven` [C]: no packing of eleven unit squares at a side `m < 4` is
12-STUCK (A245's `TwelveStuck`: all four corner boxes and all eight wall slots doubly met).  A244
measures its infimum at exactly the trivial side 4; A246 proves the propagation rules that a
construction must obey (all n-general: TWO-CORNERS, MAX-FIVE, SQUARE-IN-TRIANGLE, NOT-SELF-SUFFICIENT
-- now [T] -- TYPE-F-OWN, the free-count bound) and shows in prose why they do not compose to
`s ≥ 4` on their own: every wall pattern is locally feasible below 4 and the obstruction is global
(the note, §4).  So the theorem stays an axiom here; the consequence chain below is what it buys.

**The link.**  `wall_slot_link`: a teleport-stuck packing below 4 that is NOT 12-stuck exchanges, at
the SAME side, into a packing containing a corner slot square.  This is Lemma WALL-SLOT (b) [T] with
K0-FREE (`teleport_packing`) and SLOT-MET (A243 [S]; A246 certifies SLOT-MET(η) by interval
branch-and-bound for meetings of depth ≥ η down to the η the ladder reached, `results/slotmet246_*.json`;
the depth-free limit is the remaining [S] step).  Stated as an axiom with that dependence.

**What closes.**  `stuck4_unlocked_of_stuck_exist`: STUCK-EXIST + the link + the k1_00 kill exclude
every teleport-stuck packing below 4 -- the unlocked form of STUCK-4(11) with no lock and no A233.
`no_packing_of_stuck_exist`: with K0-FREE in its consumable form (`link`, as in `Stuck4.lean`) no
eleven-square packing exists at any side `m < 4` at which the kill holds -- k0_00 closed for the value,
by pure logic.  `twelve_stuck_of_snap_down_dual`: STUCK-EXIST also delivers A245's conclusion directly.

**n-general.**  The propagation lemmas hold for every `n` and every side in `(2 + √2, 4]`; only the
count of free squares (`11 - 8 = 3`) uses `n = 11`.

**Status (2026-09-16).**  `stuck_exist_eleven`: axiom [C]; `wall_slot_link`: axiom [T given SLOT-MET];
everything else: theorems.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **[OPEN] STUCK-EXIST(11)** -- the pure-existence statement: no packing of eleven unit squares at a
side below 4 has all twelve border cells doubly met.  Measured infimum 4 (A244); propagation rules
proved but not composed (A246). -/
axiom stuck_exist_eleven (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (h12 : TwelveStuck m z) : False

/-- **Lemma WALL-SLOT (b) + K0-FREE, given SLOT-MET.**  A teleport-stuck packing below 4 that is not
12-stuck has a wall slot with at most one meeter, which (SLOT-MET) is a meeter of the adjacent corner;
swapping it for the slot square leaves that corner singly met, and K0-FREE exchanges the corner's
remaining meeter for the corner slot square at the same side (`wall_slot243.md` §1). -/
axiom wall_slot_link (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hstuck : TeleportStuck m z) (hnot : ¬ TwelveStuck m z) :
    ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z'

/-- **STUCK-4-UNLOCKED from STUCK-EXIST.**  With the link and the k1_00 kill at side `m`, no packing
below 4 is teleport-stuck -- no lock, no selection. -/
theorem stuck4_unlocked_of_stuck_exist (m : ℝ) (hm : m < 4)
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z)
    (z : Cfg) (hz : CfgPacking m z) : ¬ TeleportStuck m z := by
  intro hstuck
  by_cases h12 : TwelveStuck m z
  · exact stuck_exist_eleven m hm z hz h12
  · obtain ⟨z', hz', c, hc⟩ := wall_slot_link m hm z hz hstuck h12
    exact kill c z' hz' hc

/-- **k0_00 for the value, from STUCK-EXIST.**  K0-FREE (`link`) sends a non-teleport-stuck packing
to one containing a corner slot square at the same side; the kill removes it.  So no eleven-square
packing exists at a side `m < 4` at which `kill` holds (the window `[3.82, ŝ]`). -/
theorem no_packing_of_stuck_exist (m : ℝ) (hm : m < 4)
    (link : ∀ z : Cfg, CfgPacking m z → ¬ TeleportStuck m z →
      ∃ z' : Cfg, CfgPacking m z' ∧ ∃ c : Fin 4, ContainsPins {⟨c, 0, 0⟩} m z')
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z)
    (z : Cfg) (hz : CfgPacking m z) : False := by
  obtain ⟨z', hz', c, hc⟩ := link z hz (stuck4_unlocked_of_stuck_exist m hm kill z hz)
  exact kill c z' hz' hc

/-- STUCK-EXIST gives A245's conclusion (`no_twelve_stuck_of_snap_down`) with no SNAP-DOWN. -/
theorem no_twelve_stuck_of_stuck_exist (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z) :
    ¬ TwelveStuck m z :=
  fun h12 => stuck_exist_eleven m hm z hz h12

/-- Conversely a 12-stuck packing below 4 would be teleport-stuck, so STUCK-4-UNLOCKED (the corner-only
form, `not_stuck_of_unlocked`) already implies STUCK-EXIST: the two open statements are ordered
STUCK-4-UNLOCKED ⇒ STUCK-EXIST, and the link closes the gap the other way. -/
theorem stuck_exist_of_unlocked (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (h12 : TwelveStuck m z) : False :=
  not_stuck_of_unlocked m hm z hz (twelve_stuck_teleport_stuck h12)

#print axioms stuck_exist_eleven
#print axioms wall_slot_link
#print axioms stuck4_unlocked_of_stuck_exist
#print axioms no_packing_of_stuck_exist
#print axioms no_twelve_stuck_of_stuck_exist
#print axioms stuck_exist_of_unlocked

end PackingCert.S11.OpenLemmas
