# 01 — The simple-square stratification: a proof strategy for s(n), with its n = 11 scoreboard

**Abstract.** We stratify the packings of n unit squares in a container of side m by k = the number of *simple*
squares (axis-aligned unit squares settled at exact lattice slots built out from the container's corners).  A
stratum is a D4-reduced Young class of slot sets; a certificate kills a class on a side window; kills climb UP
containment (Lemma K1), so the trees are solved from high k down and each class is a hypothesis with a geometric
meaning.  At n = 11 the window layer is closed (52/52 classes certified on the whole window), the k ≥ 6 tier is
empty, and what remains is three k = 5 classes, sixteen protected low-k classes and k = 0.  Every claim below is
tagged [T] proved / [M] measured / [F] refuted / [C] obligation, with its lab source and Lean name.

Written for the Squares Project (jlevy/squares) by the n = 11 lab of E. Summins (PI) — see `00-README.md` for
the series, the ask, and the retained package.  Repository: https://github.com/Esummins/packing (public); paths below are under `blob/master/`, e.g. https://github.com/Esummins/packing/blob/master/docs/proofs/instratum_bridge.md.

## 1. Why a stratification, and the PI's framing

The PI's programme: *"gain deeper insight into the square packing problem for all n; the solutions posted seem in
many ways to be refinements of a general search that don't tell us much about the underlying STRUCTURE."*  The
registered n = 11 results of the Squares Project — T-037 (Kleddamag's threshold certificate s(11) > 31/8, which we
replayed, `08-t037-replay.md`), T-060 (the global equality s(11) = T, V3/C3/S5 on your record) and T-112 (uniqueness)
— decide the VALUE.  The stratification is a different object: a case split of the packing space by a discrete,
geometric invariant, in which each case is a statement a human can read ("a packing with flush squares at
BL(0,0), BL(0,1), BR(0,0) and TR(0,0) …") and each kill is a theorem about that case on a side window.  Its
purpose is transfer to higher n (`06-climb-17-19.md`), not a second proof of s(11).

## 2. Definitions (n-general; your vocabulary in parentheses)

* **Packing at side m**: n closed unit squares in [0, m]², pairwise interior-disjoint, independent rotations.
* **Slot** (c, i, j): the axis-aligned unit cell with offsets i, j ∈ {0, 1, 2, …} from container corner c; its
  **slot square** is the closed unit square there.  A **simple square** is a square of the packing that IS a slot
  square.  **Skeleton** Simp(P): per corner, the largest down-closed (Young) set of slots occupied by simple
  squares.  [T] `skeleton` (Lean `Census.lean`); A53 `docs/proofs/contact_census.md`.
* **Class**: a D4-orbit of 4-tuples of Young diagrams whose slot squares are pairwise interior-disjoint; k = |S|.
  **Pins** of a class = its slot squares (your "parents settled in corner slots").  A packing **contains the pins
  of S** (`ContainsPins`, the monotone form) when |S| of its squares are exactly those slot squares; it is **of
  class S** when Simp(P) = S exactly (`InStratum`).
* **Census**: at every side in an integer-free range (m ∈ (3, 4) at n = 11; (4, 5) at n = 17, 19) the set of
  classes is finite and side-stable.  [T] n = 11: 1110 tuples / 163 classes, exhaustive for every packing at
  m ∈ (3, 4) — Lean `skeleton_in_census`, `exists_stratum_stmt`, `stratification` (`Statements/Stratification.lean`,
  standard axioms only); independently re-enumerated (A72) and matched by `native_decide` (A78).  The census depends on
  the side range, not on n — the same 2,500-class census serves n = 17 and n = 19 (`06-climb-17-19.md`).
* **Window**: the side interval on which a class must be empty for the stratification to decide the optimum: at
  n = 11, W = [3.82, s0] with s0 = 969271/250000 (a rational ceiling of Trump's side ŝ = 3.8770835900228…).  With
  T-037 adopted it is W′ = [31/8, s0] (`08-t037-replay.md` §4).
* **Kill of a class S on a window**: no packing at any m in the window contains the pins of S.  Lean: one
  `ClassKilledAt i m` per class; the composed obligation is the axiom `stratum_kill` (`Statements/Open/StratumKill.lean`):
  for every non-Trump class i and every m ∈ W, no packing at side m is of class i.
* **Pads and dilation semantics** (how a statement at one side becomes a window statement).  A tree is solved on a
  PAGE at the fixed rational side s0; a packing P at side m ∈ W is carried to s0 by the dilation Δ_λ, λ = s0/m ≤
  λ_max = s0/3.82 = 1.01494, which moves every centre by (λ − 1)·centre and leaves sizes and tilts alone (Lemma B.0,
  `closed_disjoint_bridge.md`).  A pin of S therefore lands within (λ − 1)·|slot centre| of its s0 slot — the
  **pin slack** — and a cell's open slot box widens by the **pad** π_i = (λ_max − 1)(i + 1 + 1/√2): π₀ = 0.025509,
  π₁ = 0.040452, π₂ = 0.055395 (`forced_corners.md` §2, [T]; Lean `fc_transfer`).  A page statement proved with
  slack pins and padded cells is a statement on the whole window.  Pads shrink ×1/27.8 on W′ (A242).

## 3. Lemma K1 — the direction of the climb (corrected per A241)

[T] **Lemma K1(i)** (`instratum_bridge.md` E.1; Lean `containsPins_mono`, `kill_mono`): if S ≤ S′ as Young
4-tuples then every packing containing the pins of S′ contains the pins of S; hence a kill of S (monotone form)
empties every S′ ≥ S.  **Kills climb UP containment.**  [T] **Lemma M→E** (Lean `class_kill`): a monotone kill of
some S ≤ g·T, g ∈ D4, empties the EXACT class of T.  [T] **K1(ii)** (completeness, not formalised): if S′ is alive
(an LP witness family exists) then so is every S ≤ S′ — no measure certificate can exist for a subset of an alive
class.  So the K1-protected remainder at n = 11 — the six k = 4 classes ≤ an open k = 5 class and the ten open
k ≤ 3 classes — can never be closed by a measure certificate; they need the tree route of §5.

[F] **What K1 does NOT say** (A241, `attempts/A241-row-cascade/notes/cascade241.md` §0): "a class C is empty when
every one-slot extension of C is empty" is UNSOUND — a packing of class exactly C has no (k+1)-th simple square, so
C's extensions never apply to it.  Closed extensions give **forced cells** (Lemma SLOT-CROWD, `02-ladder-requirements.md`),
not emptiness.  We record the correction because our own brief got it wrong first.

## 4. Why it is constructive, against the centre-cell census

The centre-cell / charge method (your threshold certificates: a measure on the container, cores captured k-of-m)
prices a packing globally and says nothing about which packing was excluded.  A stratum is a hypothesis with a
picture: pins at named slots, a widened box that two distinct non-pin squares must meet (Theorem FC), a pocket
with no room (NOROOM), a near-simple square that snaps into its slot (SNAP).  Each leaf certificate names the
geometric reason, every lemma is stated for all n, and the kills of one n are the forced cells of the next
(`06-climb-17-19.md`).  The cost: the strata are many (163 at n = 11; 2,500 at n = 17) and the low-k strata are
expensive, which is why the climb starts at high k and why ONE-FLUSH(n) (`04-simple-square-conjecture.md`) matters —
it would let every search start at k ≥ 1.

## 5. The n = 11 scoreboard (history and status, 2026-10-11)

| tier | status | source |
|---|---|---|
| k ≥ 7 | [T] every tuple contains a certified k = 6 sub-tuple → empty by K1 | A53 L5, `instratum_bridge.md` E.3 |
| k = 6 | [C] 33/33 classes killed by exact case-measure certificates (frozen verifier `verify_case.py` sha 521cb01fe656) | A53/A54 |
| k = 5 | [C] 19 classes killed; k5_11, k5_16 (A57 shadow trees) and trump5 (Trump's own class) open | A53/A55/A57 |
| **window layer** | **[C] 52 of 52 k5/k6 scoreboard rows FULL on [191/50, s0]**, each a parametric certificate (atoms affine in s, a 4-D verifier over the window, canary at 191/50, midpoint, s0) swept in slabs of 10⁻³ | A56, A61, A114, A146; `docs/residue_ledger.md` §2 |
| k = 4 | [C] 8 classes killed at s0 (A55, exactly sharp: a k = 4 class is certifiably empty iff contained in no open k = 5 class); NOT yet window rows (A241 §1: an s0-anchored PASS instantiates the kill only within 4·10⁻¹⁰ of s0) | A55, A241 |
| k ≤ 4 protected | 16 classes (k4_03, k4_05, k4_06, k4_08, k4_11, corners4 = k4_13; ten k ≤ 3) — K1(ii) forbids any certificate; tree route only | `protected_trees.md` |
| k = 0 | one class k0_00; see `03-k0-status.md` | `k0_route.md` |

**The three k = 5 classes.**  trump5 is Trump's class (alive by design; its residual tree ends in Trump's certified
basin, A60/A83/A256: [M] no trump5 node admits a contracted Trump image anywhere in the window except the basin).
k5_11 and k5_16 are "Trump's ghost with re-decorated boundaries" (A54).  Their frontier today: [M] on the pad-0
page (s0 itself) the k5 killer closed the gallery pages (A209–A211, A268: the last live k5 node died in 10 s by an
infeasible joint count); on the window slabs A270's pad-g4 campaign (pin slack 9/400, pad = the whole window)
stands at k5_11 735 of 790 records DEAD / k5_16 767 of 876, with G1 (3.861637, s0] still OPEN at 11 + 10 priority-1
records and the lower slabs at 55 + 109 records, cap 150 CPU-h reached (`attempts/A270-k5-lower-slabs/results/progress270.md`).
**k5 is not closed on the window.**  The A242 dry run (`08-t037-replay.md`) shows W′ kills 99 of the 1,795
frontier nodes at once and leaves 252 alive on W′.

**The protected tier and the tube.**  [T] Lemma P-TREE (`protected_trees.md` §0): for a protected class S, a zone
tree at s0 over the monotone hypothesis with (K) certificate leaves, (C) logic leaves and (D) leaves that localise all
11 − k free squares within (r_c, r_θ) of a compatible Trump image proves, with Lemma B for (K) and the **contraction
tube** in the class's own direction for (D), that no packing at m ∈ [ŝ − δ_basin(S), ŝ) contains S's pins, and every
packing at ŝ containing them is a Trump image.  [M] tube reach in the class directions T = 0.0457–0.130 (the whole
window is 0.0571).  [M] A100 priced the tier by LP at 3,500–4,200 CPU-h; A238 re-priced k4_11 by geometry
(`02-ladder-requirements.md` §4).  corners4 and k4_05 have no Trump image: no (D) leaf and, on the window, no forced
cell (all eight corners4 extensions are the open k5_16) — [C] THEORY-LIMITED (`writeup/05_status_sheet.md` §3).

## 6. The Lean layer (what is a theorem, what is an axiom)

`lean/PackingCertMathlib/PackingCertMathlib/Main.lean` states `main_lower_bound`, `main_value`, `main_uniqueness`
from exactly three project axioms — `stratum_kill`, `trump_residual`, `a22_exact_structure` — plus `native_decide`
evaluations of named checkers; `lean/AUDIT.md` (generated, build exit 0, no `sorry`) lists every statement with its
axiom roster.  Theorems with standard axioms only: `attainment`, the census and `stratification`, `case_verifier_kill`
(the checker is byte-faithful to the frozen Python), `parametrization`, `slot_crowd_stmt` / `fc_transfer_stmt`,
`snap_*`, `swap_leaf_*`, `windows_clause_kill`, `lower_bound_382` (s(11) ≥ 3.82 end to end, via `check_3_82`).
Prose lemmas we have not formalised are declared as documented axioms under `Statements/Open/` (`theorem_FC`,
`one_flush`, `locked_crowd_free`, `threshold_bound_31_8`, …) so that `#print axioms` shows exactly what a
downstream theorem rests on.  Nothing here claims s(11) = ŝ.

## 7. Strategy-catalogue entry (proposed; `packing/frontier/proof-strategies.yaml`, kind: proof)

```
- name: Simple-square stratification (Young slot-set census with monotone kills)
  family: modern_machinery            # or a new family `structural_case_split`
  mechanism: Stratify packings by the D4-class of their lattice-slot skeleton; prove each
    class empty on a side window by exact per-class certificates and geometric trees; kills
    climb containment (Lemma K1); the k-th stratum's closed extensions are forced cells of the
    (k-1)-th (Theorem FC); start at k >= 1 under Conjecture ONE-FLUSH(n).
  status: used                         # n = 11: 52/52 window rows; n = 17: k = 16, 15 dead
  note: 'Case split by structure, not by position; each kill is a readable theorem; cost
    concentrates in the low-k strata.'
  refs: [https://github.com/Esummins/packing/blob/master/docs/proofs/instratum_bridge.md, https://github.com/Esummins/packing/blob/master/docs/proofs/forced_corners.md, https://github.com/Esummins/packing/blob/master/docs/proofs/slot_crowds.md]
```

## What we ask

1. Register the strategy in your proof catalogue (text above; we will revise to your schema).
2. Read `02`–`04` for the ladder lemmas and the conjecture; `06` for the climb at n = 17, 19, which is the
   concrete compute we would like run on a larger machine (inputs supplied).
3. Tell us where your vocabulary and ours should be unified (pins ↔ parents settled in slots; stratum kill ↔ a
   per-class threshold certificate; pad ↔ dilation of the parent side).

Sources (https://github.com/Esummins/packing/blob/master/): `docs/proofs/{contact_census,instratum_bridge,closed_disjoint_bridge,forced_corners,protected_trees}.md`,
`attempts/REGISTRY.md` rows A53–A61, A100, A114, A146, A209–A212, A238, A241, A270; `lean/AUDIT.md`;
`writeup/05_status_sheet.md`.
