# 02 — The ladder requirements: double meeters going up and down k

**Abstract.** A packing that contains the pins of a class S and NOT those of a closed extension S ∪ {p} must meet
the slot box of p with two distinct non-pin squares — otherwise a teleport (replace the lone meeter by the slot
square, same side) climbs the packing into the closed class.  This one mechanism (Theorem FC / Lemma SLOT-CROWD)
is what the geometric toolkit acts on: closed strata at level k + 1 are the forced cells of level k, a class with
no closed extension gives the toolkit nothing (A238), and the local lemmas about the two meeters of a cell beside
a simple square (ONE-TILTED, WEDGED-SEAL, EPS, SNAP) are the leaf rules.  Tags [T]/[M]/[F]/[C] with lab sources.

Companion to `01-stratification-program.md`; repository https://github.com/Esummins/packing (paths under `blob/master/`; e.g. https://github.com/Esummins/packing/blob/master/docs/proofs/forced_corners.md).  "Meets" always means interior-to-interior;
the open corner box is (0,1)² in a corner's frame; a cell's slot box B_p(m) is the closed unit square at slot p at
side m and B_p⁺ its padded image on the s0 page (`01` §2).

## 1. The teleport, and Lemma SWAP

[T] **Lemma SWAP** (any n, any side; `ring_swap.md` §1.1; Lean `swap_packing`, 28 lines, standard axioms): replacing
a set X of squares of a packing by |X| unit squares inside (∪X) ∪ Free, pairwise interior-disjoint and interior-
disjoint from the rest, is again a packing at the same side.  **Teleport** = |X| = 1 (`teleport_of_swap`,
`teleport_packing`).  [T] **Lemma CELLS** (`cells_swap`): a packing exchanges into one containing a family Π of
pairwise disjoint unit cells iff |M(Π)| ≤ |Π|, M(Π) = the squares meeting some cell of Π.  **K0-FREE** is |Π| = 1
at a corner: a corner box met by ≤ 1 square exchanges, at the same side, into a flush corner (`k0_route.md` §3).

## 2. Theorem FC and Lemma SLOT-CROWD — the exact statements

[T] **Lemma SLOT-CROWD** (`slot_crowds.md` §2, A94; Lean `slot_crowd_stmt`, `slot_crowd_key`).  Let P be a packing
at side m containing the pins of a class S, and p a cell that is Young-completable for S, **unclipped** (its open
box meets no pin's interior), not a pin, and **usable**: the extension class T = S ∪ {p} is dead on a window
containing m.  Then ≥ 2 non-pin squares of P meet int B_p(m).  *Proof.*  If ≤ 1 meets it, replace that meeter (or
any non-pin square if none) by the slot square: a packing at side m containing T's pins, contradicting T's kill.  ∎
No selection, no minimality — a ∀-packings statement.

[T] **Theorem FC** (`forced_corners.md` §0, A178; Lean `fc_transfer_stmt` for the transfer step).  With the same
hypotheses and m ∈ W = [3.82, s0], let F = Δ_λ P be the dilate to s0 (λ = s0/m).  Then **two distinct NON-pin
squares of F meet the widened open slot box** B_p⁺ = (i, i+1+π_i) × (j, j+1+π_j) in c's frame, π_i =
(λ_max − 1)(i + 1 + 1/√2).  Corollaries: FC-corner (i = j = 0: both meeters are non-lonely poses, centres in
different cells of the 2 × 2 grid at threshold 1 + π₀ — Lemma A2 of `sideband.md`); FC-slot (i + j ≥ 1: the meeters'
centres are ≥ 1/√2 apart in ℓ∞ — a partner-existence cut only); FC-count (at every forced cell at least one FREE
square meets B_p⁺; two free squares when every conditioned square provably misses it).

**Reading it as a ladder.**  Going UP k: the single-meeter horn climbs into T (Lemma K1 then cites T's kill).  Going
DOWN k: a class S whose extension T is closed inherits p as a **forced cell** — a hypothesis of every node of S's
tree, free of charge.  The dichotomy that the n = 17 climb runs forward (`06-climb-17-19.md` §3):

    dead(S)  ⇐  dead(S with every candidate cell doubly met)  ∧  dead(T_p) for every candidate p.

[F] **What closed extensions do NOT give** (A241 §0, A94 §4.4): "every usable slot of C is doubly met" is not
"C is empty".  The crowd-counting certificate CS(S; s, m_lo; δ, e) that would promote it (one measure with slackened
pin cores and slot families, verified in 1 + r_max runs because a square can meet several slot boxes at once —
an axis-aligned square near (2.44, 2.44) meets all four of k5_11's usable boxes at s0) **does not certify**: LP
PASS at every window, runs B₂–B₄ FAIL with 30–32 exact holes; and the Trump-image ceiling δ_T(S) voids the chain
for k4_03 / k4_06 / k4_08 (a Trump image with S's pins has its slots doubly met at depths 3.61–3.72 below the
window floor).

## 3. The forced-cell traction finding (A238) and the row cascade (A241)

[M] **Every geometric rule of the k5 toolkit acts on forced cells** (`attempts/A238-k4-benchmark/notes/k4_238.md` §4):
rule CC, no-room + Lemma POCKET, Rule NS, Rule EPS, Rule SNAP all consume Theorem FC's cells, and a cell is usable
only when its extension class carries a FULL-window row.  Usable forced cells at n = 11 (`A241 results/rows241.md` §2):

| class | usable / completable | blocked by |
|---|---|---|
| trump5 | 6 / 6 | — |
| k4_08, k4_11 | 5 / 7 | the two cells whose extension is trump5 (one of them Trump's fifth simple square) |
| k4_03, k4_05, k4_06 | 3 / 5 | extensions into trump5 / k5_11 / k5_16 |
| corners4 (k4_13) | **0 / 8** | all eight extensions are the open k5_16 |
| every k ≤ 3 class | **0** | extensions are open k4 classes or s0-only A55 kills |

So the tier price is a cascade, not a flat number: closing k4 pays for k3, k3 for k2, down to k0 — Lemma K1 run
inside the tier.  [M] **The row cascade** (A241): a class gets a window row from (A) a direct parametric certificate
over [191/50, s0] (atoms and cores affine in s; the 4-D verifier; canary at three sides) or (B) Lemma K1(i) from a
rowed subclass.  The eight A55 k4 kills and k3_00 are "rowable today, blocked on nothing but CPU" — but their
parametric re-expression **PARAM-FAILed on every anchoring** (gap / nearest-wall / mid-band, rc = 1 or timeouts at
2,400 s; `rows241.md` §1), so no k ≤ 4 class has a window row yet and the k ≤ 3 tier still has 0 usable cells.
[C] A certificate form that rows the A55 kills on the window is the first thing a bigger machine could try
(`06` lists the inputs; `05-toolkit.md` §6 the pipeline).

## 4. The pressed fifth square: k4_11 (A238)

The PI's prediction (2026-09-16): *"the k4 classes that are parents of Trump shouldn't be able to get that close
to Trump, since a bunch of the geo tests will kill them when they try to press the fifth simple square into
place."*  [M] On A100's own level-1 cover cells of k4_11 (the Trump parent with pins BL(0,0), BL(0,1), BR(0,0),
TR(0,0); Trump's fifth simple square sits at BL(1,0), whose extension is trump5 — the one cell FC cannot force),
the plain geometry kills **at the root node by EmptyBox in 13–16 s of wall (stage 0 + tree)**, where A100's LP
spent 120–185 s per cell and killed none (τ = 6.000 = budget: LP-alive, deepen).  The class root (H = the whole
interior zone) survives, as it must — it holds the Trump image — but is productive: 50 nodes to depth 6 in 337 s,
kills EmptyBox ×17, REACH ×6, NOROOM-CN ×6, COUNT ×2, NOROOM-POCKET, S-CLIP, FC.  [M] On k3_02 the same toolkit
decides nothing (41/41 cells ALIVE in ≈ 4 s, 0 kills, depth 0) — the §3 finding.  [M] Rule SNAP evaluated on 210
fully named leaves: no candidate, no kill, no hand-off; the fifth square dies for lack of room, not by snapping.
[M] The TRUMP-TUBE leaf (a (D) discharge, canaried 10/10: a genuine image fits, three displaced copies and a moved
pin are refused) was never reached; every gated node ended tube-pending.

## 5. The local lemmas about the meeters of a cell beside a simple square (exact statements)

[T] **ONE-TILTED** (`wall_torque.md` §3, A219; Lean axiom `one_tilted`, any n, any side).  Two axis-parallel unit
squares inside the container that both meet the open corner box (0,1)² overlap.  So of the two meeters of a
doubly-met open corner at least one is tilted.  *Proof.*  A flat square in the quadrant meeting the open box is
[a, a+1] × [b, b+1] with 0 ≤ a, b < 1; two such have |a − a′|, |b − b′| < 1.  ∎

[T] **WEDGED-SEAL** (`wedged_seal.md` §0, A239; Lean theorem `wedged_seal` from the axiom `lemma_PUSH`; = Cor. B1 of
`sideband.md`, A169).  Let Q be a unit square in the closed quadrant of a corner with a vertex on the floor and a
vertex on the wall (tilt θ ∈ [0°, 90°]).  Then no unit square G of the quadrant with int G ∩ int Q = ∅ meets the
open corner box: **a wedged corner meeter is alone, at every tilt.**  Two proofs: the sealed triangle of area
sin θ cos θ/2 plus two wedges of apex angles θ and 90° − θ that no unit square can enter without crossing the wall
or Q's edge; and two lines from Lemma PUSH (the separating normal into Q has both components positive, the one into G
a positive component).  Consequence: in a doubly-met corner neither meeter touches both walls.

[T] **Lemma EPS** (`lemma_eps.md` §0, A227; Lean theorems `not_mem_iff_four`, `wedge_right_depth`,
`wedge_right_corner`, `coord_within_h`, `gate`).  Let C be a cell and F a unit square with centre z and tilt θ,
t = tan(θ/2).  (EPS-1) C \ F is the union of four convex wedges W_R, W_L, W_T, W_B, one along each side of C.
(EPS-2) In the unit cell with z = (½ + δx, ½ + δy): W_R = {x > 1 − w_R(y)}, w_R(y) tapering linearly from
w_R = t(1 − t − 2δy)/(1 − t²) − δx at the corner (1,1) to zero at y* = ½ + δy + t/2 + δx(1 − t²)/(2t); for a pure
rotation the feet form the PINWHEEL (right side upper half, top side left half, …); depth ≤ δ + t₀(1 + 2δ)/(1 − t₀²).
(EPS-3) A square M disjoint from F that meets C has an interior point in one of the four open wedges.  (EPS-4) over
a box of poses of F the wedge union is inside explicit convex polygons and K′ = C minus them lies in every F of the
box.  (EPS-5, GATE) a wedge along a BACKED side (a wall, or a pin whose core reaches the side) is enterable only
through its end zones at the cell's corners.  (EPS-6) the squares of tilt φ meeting a rectangle W have centres in
W ⊕ int Sq_φ, inside its h_φ = (cos φ + sin φ)/2 enlargement.  **Rule EPS**: at a node where a role is near-simple in
a forced cell, the second meeter must meet a wedge TARGET; roles whose pose sets miss every target exactly are
struck; none left ⇒ DEAD by FC + EPS.

[T] **Rule SNAP** (`snap_rule.md` §0, A224; Lean `snap_step`, `snap_dead`, `snap_diag_two`, all theorems).  P at side m
containing the pins of S, p a cell not in S whose slot box lies in the container, Q a non-pin square such that every
OTHER square of P misses int B_p(m): then (P \ {Q}) ∪ {B_p(m)} is a packing at side m containing the pins of
S ∪ {p}; if that class is dead on a window containing m, no such P exists.  SNAP-DIAG: k roles at k disjoint cells,
each blocked only by the others, snap together (Lemma SWAP with |X| = k).  The engine's certificate is exactly the
hypothesis: an exact separating-axis miss per other role against B_p⁺, the pins by the unclipped census, the target
stratum's row.  [F] The PI's expectation that SNAP kills the k5 leaves: over every node of every A211 g1 certificate
(72 pages, 294 candidate nodes) **0 kills, 0 hand-offs** — the near-simple role's own box (width ≈ 0.077) leaves a
sliver of positive area at the cell's far corner that the conditioned square H pokes by 0.008.  [C] The one-blocker
case (65 of 173 candidate slots, 107 of them H) is a Rule NS split whose MISSES child is an immediate SNAP kill.

Also used at corners: [T] Lemma PUSH / HOLD (`k0_count.md` §2–3), TWO-CONTACT (`wall_torque.md` §2), the sideband
Lemma A and Theorem B (`sideband.md`: exactly when a second meeter of a corner box exists; Lean `Sideband.lean`,
Theorem B's second-meeter criterion [C] in Lean), Lemma SEAL / WEDGE / NO-SECOND (`corner_seal.md`).

## What we ask

1. Check Theorem FC and Lemma SLOT-CROWD in your vocabulary: a usable slot is a cell whose extension stratum has a
   threshold certificate on the window; is there a k-of-m charge that prices "two distinct non-pin meeters of B_p⁺"
   directly (the two-square row that corners4 and k4_05 lack, `01` §5)?
2. The row cascade (§3) is CPU-bound and failed on our machine: re-express A55's eight k4 kills and k3_00 as window
   certificates (inputs: `attempts/A55-k4-sweep/certs/*.json`, A56's `make_param.py` / `verify_param.py`,
   `attempts/A241-row-cascade/code/param241.py`).  Success hands every k ≤ 3 class 2–5 forced cells.
3. Prove or refute the one-blocker SNAP conjecture of §5 on a page we supply (`k5_11_interior_Y0865`, A224 §4).

Sources (https://github.com/Esummins/packing/blob/master/): `docs/proofs/{ring_swap,slot_crowds,forced_corners,sideband,wall_torque,wedged_seal,lemma_eps,snap_rule,
k0_count,corner_seal}.md`; `attempts/A238-k4-benchmark/notes/k4_238.md`; `attempts/A241-row-cascade/{notes/cascade241.md,
results/rows241.md}`; `lean/AUDIT.md`.
