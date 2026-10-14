# LOCKED WALL — Lemma UNLOCK and the exact HELD condition; the open notch (OPEN-TOOTH); the hybrid corner PAIR; CORNER-NOTCH closed by the PLUG; GAP-DEPTH restated — A260, 2026-09-21

The last ROOM obligations of the k0 exclusion.  A258 (`normal_ring.md` §3.5, `family258.md` §7): in normal form a wall
of the ring is a common-tilt ROW OF TWO or an OPEN PAIR (s₁, W) whose normal cell T = s₁ + sec φ₁·e is met by W AND a
free square (a LOCK); 43 of 44 corpus ring + poker rows are locked.  A259 (`normal_room.md`): on the normal family D′
every free square contains the centre O — except the uncertified double-limit LAYER (CORNER-NOTCH) and with
GAP-DEPTH-ONE only measured.  Tags [T] proved, [T-computed] box-valid certificate with its own verifier, [M] measured,
[C] conjecture, [F] false.  Code `attempts/A260-locked-wall/code/` (`geom260`, `corpus260`, `adv260`, `tooth260`,
`pairh260`, `cert260`, `bench260`, `verify260`, `gapdepth260`, `pages260`, `run260.sh`; A258 / A259 code imported,
never edited); results, certs, logs beside it; pages `docs/residue_map/campaigns/A260-locked-wall/`; Lean
`Statements/Open/LockedWall.lean`.  Notation: c = cos φ, g = sin φ, w(θ) = cos θ + sin θ, O = (s/2, s/2); wall frame
(t, d); an open pair of COMMON tilt φ has W = T + (e, 0), e > 0 the SHIFT (family258's open gap).

## 0. Verdict

> **(U) [T] Lemma UNLOCK (any n, any s)** is Lemma CELLS on Π = {T, Q₁..Q_j}: it is A258's P2′ — not new — and what
> it leaves is exact: **a lock F survives in the maximiser iff it is HELD: the (n−1)-packing (P ∖ {W, F}) ∪ {T} is
> SATURATED** (no unit square of [0,s]² is interior-disjoint from all its members).  New: **LIFT [T]** — F + λv
> (v = s₁'s edge direction off the wall) never meets s₁ and clears T after λ_T = e·sin φ for ψ ≤ φ (≤ e·sin ψ / cos(ψ−φ)
> beyond), so HELD ⟹ another square meets that sweep, of length first order in e AND φ.  [M] corpus: 43/43 locks lift (exact check),
> lift ≤ 0.0200 ≤ e sin φ, the lifted square contains O.  **(U) alone closes nothing for r ≥ 2**: jointly unlocking
> two walls needs two cells in a pocket of capacity one (A259), so the holder cannot be argued away — (R) must do it.
> **(R) [T] reduction + [T-computed, running] certificate + [M].**  MISS ⟹ a HYBRID corner PAIR, s eliminated exactly
> as in A259; 4 + (number of open walls at the corner) parameters at common tilt per wall.  [T] OPEN-TOOTH: closed form
> of the least depth in the open notch, ≥ cos φ − (e/2) sin 2ψ ≥ cos φ − e/2 (POKE form), = cos φ (1 − e sin φ) at
> ψ = φ (checked against exact centre sets to 7·10⁻¹⁶).  The enlarged box R breaks HOLE-ONE's inequality exactly where
> cos φ₀ + cos φ₂ − (e₀+e₂)/2 < s − 2 (tilts ≳ 17° at ŝ with two opposite locks; 20.2° without locks) — there the
> PAIR form takes over: **certificates hybA / hybB (one open wall at the corner, 5 parameters) and hybAB (both, 6) on
> the all-ADJ common-tilt hybrid family, e ∈ (0, ½], priced 0.8 + 0.8 + 3.8 CPU-h, launched detached; every finished
> cell certified, 0 OPEN.**  [M] the sharp form survives: sup miss-margin over the hybrid family (16 coordinates,
> tilts of s₁ and W independent, adversary with hard feasibility) −0.0654 at ŝ < −(4−s)/2 = −0.0615; corpus 46/46.
> **CORNER-NOTCH: CLOSED, [T] + [T-computed].**  **PLUG [T] (any n, s, m):** if the START offset a′ ∈ (0.354 + ρ, 1)
> then no free unit square meets the corner box [0, ρ]² — every unit square of the quadrant reaching within ρ of the
> corner contains the open box (0.354 + ρ, 1)², hence the START square's lowest vertex (cos φ′, a′).  With the plug
> (ρ = ¼) as a fifth obstacle A259's layer certifies at once: **81 cells, 93 leaves, 6 s, verifier 0 bad.**
> **GAP-DEPTH-ONE: no longer needed at n = 11** (PAIR + LAYER cover D′); for m ≥ 5 the proof needs only
> GAP-DEPTH-COS (depth ≥ cos φ); [M] the s-free, m-free QUADRANT form of GAP-DEPTH-ONE: 2 046 pairs over all of
> (b, a′) ∈ (0,1)², 0 violations, least 1.0027 (→ 1 as φ′ → 0: sharp).  Analytic proof: still open ([T] the plug
> region and flat squares only).
> **ROOM now:** normal D′: [T-computed] on ALL of D′ once A259's tree index completes (LAYER done here); hybrid,
> common tilt per wall, all-ADJ: [T-computed] when this chain ends; open pairs with φ_W ≠ φ₁: **[C]** ([M] only).

## 1. (U) Lemma UNLOCK, HELD, LIFT

**1.1 Lemma UNLOCK [T] (any n, any s).**  P a packing at side s, s₁ a wall toucher of tilt φ₁ ∈ (0°, 45°),
T = s₁ + sec φ₁·e ⊆ [0,s]², M(T) = {W, F₁..F_j} the squares other than s₁ meeting int T.  If Q₁..Q_j ⊆ [0,s]² are unit
cells, pairwise interior-disjoint, interior-disjoint from T and from every square of P ∖ M(T), then
(P ∖ M(T)) ∪ {T, Q₁..Q_j} is a packing at side s in which (s₁, T) is a row.  *Proof.*  Lemma CELLS (`ring_swap.md`
§1.3, cells of any pose) with Π = {T, Q_i}: M(Π) ⊆ M(T), |M(Π)| ≤ |Π|.  ∎  (Lean `unlock_swap`, from `cells_swap`.)
In A258's potential the exchange keeps Φ₁ and raises Φ₂ when W's row is no longer than s₁'s: this is P2′.
**1.2 HELD (the exact condition) [T].**  In the lexicographic maximiser a wall is locked by ONE free square F only
if **P₁ := (P ∖ {W, F}) ∪ {T} is saturated**; by j locks only if no j pairwise disjoint cells fit beside P ∖ M(T) ∪ {T}.
**1.3 LIFT [T].**  Notch frame: origin the apex A = (a + sec φ₁, cos φ₁), axes u = (c, g), v = (−g, c); then
s₁ = [−1,0] × [tan φ − 1, tan φ], T = [0,1] × [−1,0].  Let F be interior-disjoint from s₁, meet int T, and have its lowest
vertex at wall depth > sin φ₁ (true by §2 when e < 2(c − g)).  Then F + λv is interior-disjoint from s₁ for all λ ≥ 0,
and from T for λ ≥ λ_T := −min_F y.  *Proof.*  If (x, y+λ) ∈ int s₁ with (x, y) ∈ F then x ∈ (−1, 0), y < tan φ, and
(x, y) ∉ int s₁ forces y ≤ tan φ − 1: F has a point under s₁'s lower-right edge, i.e. at wall depth < sin φ₁ — excluded.
F + λ_T v ⊆ {y ≥ 0}.  ∎  With §2 (common tilt): λ_T = e sin φ for ψ ≤ φ (the right vertex rests on W's edge line
y = −eg), and λ_T ≤ e sin ψ / cos(ψ − φ) for ψ > φ (P in the slot).  **So HELD ⟹ a square other
than s₁, W, F (or the container) meets {F + λv : 0 < λ ≤ λ_T}** — A258 §2.1's held poker, now for the lock, with the
sweep length explicit.  [M] `corpus260`: all 43 locked rows lift (exact SAT + containment of the lifted pose ≥ 0),
lift = dip into T ≤ 0.0200 (e = 0.1275, 14.5°, s = 3.99) ≤ e sin φ = 0.032; the poker is the only free square that fits
beside itself (tenth-square centre set empty, 44/44); the poker contains O (44/44, least 0.017) and so does the lift.
**1.4 What (U) does not do.**  r = 1: no lemma needed — remove F, normalise, two free squares in a normal pocket both
contain O (A259): contradiction.  r ≥ 2 (locks F, G + H): the joint exchange Π = {T₀, T_j, Q₁, Q₂} needs TWO cells in the
pocket of the normal ring (+ H), and A259 says it holds one.  So "every such Q is met by a third square" cannot be
refuted by exchange alone: the contradiction has to come from the room of the HYBRID pocket, i.e. from (R).

## 2. OPEN-TOOTH — the open notch in closed form  [T]; `tooth260.py` [T-computed check]

Open pair of common tilt φ, shift e.  In the notch frame s₁ is the quadrant {x ≤ 0, y ≤ tan φ} (corner = its top
vertex, the LIP), W the quadrant {x ≥ ec, y ≤ −eg} (corner = W's left vertex A_W = A + (e, 0)); between them the SLOT
of width ec.  A free square of tilt ψ (δ = ψ − φ) with its lowest vertex P = (x, y) over the notch has depth c + cy + gx:
* ψ ≤ φ: P on s₁'s edge line, its right vertex on W's edge line: y ≥ sin(φ−ψ) − eg, **τ = c (1 + sin(φ−ψ) − e g)**.
* ψ ≥ φ: two linear constraints each a union of two — LEFT: the lip on Q's left edge, x cos δ + y sin δ ≥ tan φ sin δ,
  or Q's far-left vertex right of s₁'s line, x ≥ sin δ; RIGHT: x ≥ ec and y ≥ −eg, or (P in the slot) A_W on Q's right
  edge, y cos δ − x sin δ ≥ −e sin ψ.  The objective (g, c) lies in the cone of the normals, so **τ = c + min(LIP, FAR)**,
  LIP = sin ψ (tan φ sin δ − e cos ψ) if tan φ sin δ ≤ e cos ψ (P in the slot), else −egc + g (tan φ + eg) tan δ;
  FAR = c (sin²δ − e sin ψ)/cos δ + g sin δ if sin δ ≤ ec, else −egc + g sin δ.   (e = 0: A259's TOOTH.)
* **POKE form, any tilts (φ₁, φ_W):** depth ≥ cos φ_W − (γ/2) sin 2ψ ≥ cos φ_W − γ/2, γ < 1 the horizontal distance from
  W's left vertex to s₁ (= e at common tilt).  *Proof.*  Below W's left vertex the part of Q under that height lies in
  the slot component (s₁ and W both reach the floor), so Q's horizontal chord there, of length h (tan ψ + cot ψ) ≥ 2h
  at height h above P, is ≤ γ.  ∎
`tooth260`: formula = exact centre-set value to 6.7·10⁻¹⁶ on 6 tilts × 5 shifts (0 … 0.3) × 19 ψ; POKE form never
violated.  At ψ = φ the dip below the closed tooth is e·g·c (0.031 at e = 0.13, 14.5°): small, first order in e.

## 3. (R) the hybrid corner PAIR

**3.1 Reduction [T].**  `normal_room.md` §2.2–2.3 verbatim with the corner's four squares: floor (s₁, W), right wall
(S′, W′): a free square missing O violates PAIR^h(b, φ, e; a′, φ′, e′; s) at one of the four corners; in the corner
frame the four squares do not depend on s, so PAIR^h(·; s_max) ⟹ PAIR^h(·; s), s ≤ s_max (`corner_frame_mono`).
Domain (all-ADJ, s ≥ 3.82): b, a′ < 1; a = s − b − e − span(φ) ∈ (0, 1); b′ likewise; reaches b + w(φ) ≥ s − 2,
b + e + sec φ ≤ 2 (s₁'s reach — s-free), same on the right wall.  This caps e at 2 − b − sec φ ≤ 4 − s + w − sec (0.31 at
14.5°); the cyclic corner conditions cut it to ≈ 0.13 but are not visible from one corner, and not needed.
**3.2 The BOX form and where it breaks [T given GAP-DEPTH-COS].**  Every free square lies in
R^h = [d₃, s−d₁] × [d₀, s−d₂], d_k = cos φ_k − e_k/2 (sharp: min_ψ τ); if d₀+d₂ ≥ s−2 and d₁+d₃ ≥ s−2 all free squares
contain the centre of R^h (HOLE-ONE): capacity 1.  At ŝ, common tilt: 2 cos φ − (e₀+e₂)/2 ≥ 1.8771, i.e. φ ≤ 20.2° with
no lock, φ ≤ 14.5° with e₀ + e₂ = 0.118 (sharp τ: e₀ + e₂ ≲ 0.24).  **Beyond that the enlarged R breaks the inequality —
as the closed R already does — and only the PAIR form holds.**
**3.3 The certificate [T-computed] (`cert260.py`, own verifier `verify260.py`).**  A259's method on
p = (b, φ, a′, φ′, e, e′): CORES inside the squares over the box (ρ of s₁ and W′ includes r_e and the sec·tan term),
KERNEL tilt bins, pocket OVER-approximated, PRUNE only off-domain or on core overlap, adaptive bisection, s_max =
3.8771, s_min = 3.82.  **Benchmark:** 0.05 s per box; 20/20 random boxes certify at radius (0.02, 0.01 rad); root
cells (5° × 5°): hybA 33–34 s (≈ 1 060 leaves), hybAB 167 s (5 300 leaves) ⟹ **hybA 0.8, hybB 0.8, hybAB 3.8 CPU-h**
— under the 50 CPU-h line, launched (`run260.sh chain`: layer → hybA → hybB → hybAB → verify260 → adversary).
At exit: layer 81/81 verified; hybA cells finished all `ok`, 0 OPEN (index: `certs/hyb*260_index.jsonl`).
**3.4 Not certified.**  (a) Open pairs with φ_W ≠ φ₁: one more parameter per open wall; a tilt radian costs ≈ 60
leaves per unit of the present tree, so ≈ 50 CPU-h for corners with one open wall and > 10³ for two — NOT launched;
[M] the adversary moves both tilts freely (|Δ| up to 7° reached) and finds nothing above −0.0654.  (b) Hybrid rings that
are not all-ADJ (a slot served by a free square): [M] only (`adv260 --adj 0`: −0.0654).  (c) s ∈ (ŝ, 4).

## 4. CORNER-NOTCH — the PLUG  [T], and the layer [T-computed]

Corner frame (X, Y) = distances from the two walls; S′ = the START toucher on the wall X = 0, tilt φ′ ∈ (0°, 45°],
offset a′: its lowest vertex is V′ = (cos φ′, a′).  **Lemma PLUG (any n, s, m).**  *Let 0 < ρ < 0.35 and
0.354 + ρ < a′ < 1.  No unit square Q of the quadrant, interior-disjoint from S′, meets [0, ρ]².*
*Proof.*  Let Q have tilt θ, centre q, width w = w(θ) ∈ [1, √2] in both axes.  Q ⊆ quadrant gives q ≥ w/2
coordinatewise; Q ∩ [0,ρ]² ≠ ∅ gives q ≤ w/2 + ρ.  Q contains the axis-parallel square of half-side 1/(2w) about q, so
int Q ⊇ (w/2 + ρ − 1/(2w), w/2 + 1/(2w))² ⊇ (√2/4 + ρ, 1)², because w/2 − 1/(2w) ≤ √2/4 < 0.354 and w/2 + 1/(2w) ≥ 1
(Lean `plug_kernel`).  cos φ′ ∈ [0.707, 1) and a′ ∈ (0.354 + ρ, 1): V′ ∈ int Q, and V′ ∈ S′.  ∎
This is the brief's "the gap is < 1 wide at the box", made exact: a square that reaches the corner must swallow the
vertex that D2's strictness (a′ < 1, φ′ > 0) keeps inside the unit box.  It uses the START side only; b < 1 is not needed.
**The layer.**  A259's tree could not certify {b, a′ ≥ 63/64} because the closed limit holds the square [0,1]².  With
the plug [0, ¼]² as a fifth obstacle (sound: a′ > 0.604 on the layer; the kernel of a free square misses the plug) the
limit square is gone: `cert260 --fam layer`: **81 tilt cells, 93 leaves, all CERT, worst margin −2.8·10⁻⁴, 6 s;
`verify260`: 93 re-derived with independent bins, tiling identity exact, 0 bad** (without the plug the same box FAILS
with margin +1.04 — checked).  **CORNER-NOTCH is closed; A259's obligation (O1) is discharged.**

## 5. GAP-DEPTH-ONE

Not used any more at n = 11.  For m ≥ 5 (`normal_room.md` §6, PEEL in normal form) the proof needs only
**GAP-DEPTH-COS: the wall-nearest vertex of a free square over a corner-gap zone has depth ≥ cos φ of that wall's row**
(then R ⊆ R_cos).  [M] the stronger ONE form in its s-free, m-free QUADRANT form (two rows at a corner of a large
container; `gapdepth260`): 2 046 pairs over ALL (b, a′) ∈ (0,1)², tilts (0°, 45°]: least END-gap depth 1.098, least
START-gap depth 1.0027 (φ′ = 0.5°; → 1 as φ′ → 0, so ONE is sharp and no box certificate closes the flat limit without
an analytic lemma there).  [T]: no free square within ρ of the corner (PLUG); a FLAT free square [X_P − 1, X_P] × [Y_P, Y_P + 1]
in the END-gap zone (1 ≤ X_P ≤ b + sin φ < 1 + cos φ′) with Y_P < 1 has cos φ′ inside its X-range, and its vertical
chord there meets S′'s chord (a′, a′ + sec φ′) because a′ < 1 ≤ Y_P + 1 and Y_P < 1 ≤ sec φ′ — so flat squares obey ONE.  The general tilt is open: **[C]**, a 4-parameter s-free statement.

## 6. Plainly — what ROOM is, the chain, the obligations

| family | side | ROOM ≤ 1 (every free square ∋ O) |
|---|---|---|
| normal D′ (four rows) | [3.82, 3.8771] | [T] reduction + [T-computed]: A259's tree on D′ ∖ LAYER (its index still filling, all `ok`) + LAYER here (verified) |
| hybrid, common tilt per wall, all-ADJ, e ≤ ½ | [3.82, 3.8771] | [T] reduction + [T-computed] when `run260.sh chain` ends with 0 OPEN and `verify260.json` bad = 0 |
| hybrid, φ_W ≠ φ₁; not all-ADJ; all-ADJ 17-dim | — | [C]; [M] adversary −0.0654 < −(4−s)/2, corpus 46/46 |
Chain: packing at s ⟹ [T, `normal_ring_value`] not family-stuck, or a normal-form family-stuck packing ⟹ [C]
NORMAL-RING(11) in hybrid form (A258 P1–P4 + A261's structure lemmas: TOUCH-NORMAL, two walls per box, window
exclusions) ⟹ a hybrid ring ⟹ [this note] every other square contains O ⟹ 8 + 1 < 11 ⟹ FAMILY-STUCK-EXIST(11) ⟹
k0_00 (Lean `lockedWall_excludes`, `k0_value_of_hybrid`).  **Remaining, exactly:** (O1) A259's tree + `verify259`;
(O2) this chain's index complete, 0 OPEN, `verify260` 0 bad; (O3) LOCK-TILT: open pairs with φ_W ≠ φ₁ — a certificate
with one more parameter per open wall (≈ 50 CPU-h one open wall, ≫ budget two) or an argument that the maximiser's open
pairs have a common tilt; (O4) hybrid rings that are not all-ADJ; (O5) NORMAL-RING(11) itself (A258 / A261); (O6) the
stretch (ŝ, 4); (O7) GAP-DEPTH-COS analytically (m ≥ 5 only); (O8) Lean: `hybrid_pierce` is an axiom.

## 7. What the brief had wrong

1. (U) is not new — it is A258's P2′ / (E3) — and it cannot close the locked wall: the second cell has to live in a
pocket of capacity one.  Its real content is HELD = "P₁ saturated" and the LIFT bound.  2. "POKE: depth ≤ e/2" is the
crude form; at the row's tilt the dip is e sin φ cos φ, first order in e AND φ, and 0.13 is not a bound on e (one corner
sees e ≤ 2 − b − sec φ ≈ 0.3).  3. "redo HOLE-ONE's inequality with the enlarged R": the box form already fails for the
closed R beyond 20°; the PAIR form is what holds, and it does not break anywhere found.  4. "both squares MISS the
corner box at b = a′ = 1": true but not the mechanism — one vertex (the START square's) suffices, b plays no role.
5. "all 17 coordinates": the certificate covers the common-tilt hybrid (≤ 6 per corner); unequal tilts stay [C].
