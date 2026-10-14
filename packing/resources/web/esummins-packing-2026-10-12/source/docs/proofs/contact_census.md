# CONTACT CENSUS of a boxed node — Theorem CC (attainment + Fritz John on a boxed assignment), the candidate graph, and the LP form — A186, 2026-09-09

Target (A186 BRIEF; the PI's question of 19:15: "can we turn an assignment set into a contact graph, and is
there enough information to do that?"): a node in which EVERY square is boxed (A182's budget-0 leaves of
c0_Y1033: five pins, H, F1..F5, each with a compact set of poses = the multibox pieces) should be killed by
the drain route — the minimal side over a compact set of poses is attained at a STUCK configuration, a
Fritz-John point with some contact graph, and the node is dead if every such configuration realisable in
the boxes has side > s0.  This file settles the statement used (n-general), what the boxes determine and
what they do not, and how the census is solved.  Labels: [T] proved, [S] routine given cited items,
[M] measured (`attempts/A186-contact-census/`), [F] finding, [P] open.  Conventions: s0 = 969271/250000,
ŝ = 3.877083590022814; `local_certificate.md` (Lemma SAT, the signed selection rows g_σ, Lemma COVER,
Lemma LEAF, Lemma RELAX, Theorem LOCAL, Reduction DROP, Lemma GRAIN-LP); `drain_lemma.md` v3 (D1, D3′);
`structure_lemmas.md` (Fact 0, L1–L7); `fj_census_k0.md` (T1, Lemma H-LOC); the A57 frame (pins on slot
lines c = α + βs); `attempts/A171-multibox-invariant/notes/usage.md` (pieces, the two clips).

## 0. Verdict

> **Yes, and the boxes carry exactly three things: the CANDIDATE contact graph (which pairs and which
> walls can touch at all — certified by interval separation over the pieces), the loadable BOX FACES
> (the faces of the piece unions, which act as walls of the hypothesis), and the finite SELECTION MENU of
> every candidate pair.  What they do not carry is which subgraph bears the load: that is decided by
> SOLVING, never by counting — Theorem CC (a) proves the minimiser exists and is Fritz-John for every
> consistent selection with box rows included; (b) says the node is dead iff every such stuck
> configuration has side > s0; and the SOLVER is Theorem LOCAL transported to piece bodies (§3): the LP
> dual at a leaf IS the contact graph of the stuck configuration (GRAIN-LP), so the census is enumerated
> by the selection tree, not by subgraphs.  The counting side (m_H against 3k_H + 1, L1, L6) labels a
> structure; it prunes nothing on its own (T1(d): flexible supports are legitimate FJ points).**
> Applied to c0_Y1033 (§4): candidate graphs of 20–24 edges on the eight budget-0 assignments (four
> distinct geometries); the selection tree runs 2.5 ms a node, closed 8·10⁴ leaves on the first node
> with no exact-feasible point and no witness, and is CAPPED at 2·10⁵ nodes [P]; every measured search
> for a disjoint configuration inside the hull boxes fails, the least overlap being 0.06 in the left
> column P2 | F2 | F3 (the crowd the assignment stacks above BL(0,1)) — a coexistence obstruction the
> chord rows of A182 did not see.  No assignment is certified dead by this attempt; none has a witness.

## 1. The objects (n-general)

**A boxed node** N = (P, B, Π, h): pins P on slot lines (pin p's centre α_p + β_p s + (u, v), |u|, |v| ≤ h,
tilt 0), boxed bodies i ∈ B with COMPACT pose sets Π_i ⊂ ℝ² × [0, π/2], each a finite union of pieces
(boxes [x0, x1] × [y0, y1] × [t0, t1] in (centre, tilt), A171's representation).  A CONFIGURATION of N at
side s: unit squares Q_i (i ∈ P ∪ B), pins as above, z_i ∈ Π_i for i ∈ B, every square inside [0, s]²,
pairwise interior-disjoint.  N(s) = the set of configurations at side s; for a side window W = [s_lo, s_hi]
put Dead_W(N) :⟺ N(s) = ∅ for every s ∈ W ∩ (−∞, s0].

**Reading of a multibox record [S].**  A182's node carries the hypothesis on the dilate F = Δ_λ P of a
packing of the page (Theorem ASSIGN, `attempts/A180-forced-first-assignment/notes/assignment.md` §0): eleven
unit squares inside [0, s0]², the pins at the s0 slots (the record's pin boxes are 4·10⁻⁸ wide, tilt bins
3.4·10⁻⁶ deg: absorbed by h = 10⁻⁶, a corner moving ≤ tilt·√2/2), every other square's pose in its piece
set (A171: a clip removes only poses proved impossible by CONTAINER or DISJOINT, so the surviving pieces
contain every pose of F's square in that role).  Hence F ∈ N(s0), and **N(s0) = ∅ ⇒ the record's node is
dead**; with s_lo = s0 the window form and the record form coincide.  (The journal flags
`invariant: False` on these leaves — the A171 report's failing check is not recorded there; the only
check that could affect soundness is K-DISJOINT, which would make the node dead outright, and the pieces
are supersets at every pass regardless [S].)

**Reduction DROP [T, `local_certificate.md` §1].**  A node with unboxed squares (budget > 0) is dead if its
boxed sub-node is dead: the boxed squares of any configuration form a configuration of the sub-node.
So everything below is stated for the boxed squares only, and the 15 alive budget-1/2 assignments are
the same problem on 9–10 bodies.

## 2. Theorem CC

**Theorem CC (attainment and Fritz John on a boxed node) [T].**  Let N be a boxed node, W = [s_lo, s_hi]
with s_lo ≤ s0 < s_hi, and m_N := inf { s ∈ W : N(s) ≠ ∅ } (+∞ if N(s) = ∅ on W).

(a) *Attainment.*  If m_N < ∞ it is attained: some (z*, m_N) with z* ∈ N(m_N).

(b) *Kill.*  Dead_W(N) ⟺ m_N > s0.

(c) *Fritz John with box rows.*  Let (z*, m_N) attain the minimum and let S be any selection consistent
with z* — for every pair (i, j) a signed axis row g_σ ≥ 0 (Lemma SAT: owner o, axis k, sign ε,
g_σ = ε (c_other − c_o)·a_k(θ_o) − ½ − w(θ_o − θ_other)/2) that holds at z*, written in D3′'s smooth form
(nearest-corner row plus its three dominance rows) whenever the pair is at a kink of w.  For each i ∈ B
let Q_i be a piece of Π_i containing z*_i.  Then (z*, m_N) is a global minimiser of the smooth NLP

  NLP_N(S):  min s  s.t.  wall rows c_i·e_k − h(θ_i) ≥ 0, s − c_i·e_k − h(θ_i) ≥ 0 (i ∈ P ∪ B, k = 1, 2);
             pin rows h ± u_p ≥ 0, h ± v_p ≥ 0;  S's pair rows;  BOX rows x_i − x0 ≥ 0, x1 − x_i ≥ 0,
             y likewise, t_i − t0 ≥ 0, t1 − t_i ≥ 0 for the piece Q_i of every boxed body;

and the Fritz-John conditions hold: (λ₀, λ) ≥ 0, (λ₀, λ) ≠ 0, λ₀ ∇s = Σ_k λ_k ∇g_k, λ_k g_k(z*) = 0.

(d) *The support structure.*  Define H(z*, λ): squares, four wall nodes, and one FACE node per boxed
body; an edge per pair row with λ > 0 (Fact 0: one edge per pair), per wall row with λ > 0, and per box
row with λ > 0 (an x/y face row is a CENTRE row of the body with normal ±e; a t face row is a torque-only
row).  Then: **L1′** every body with a loaded centre row has ≥ 2 loaded centre rows (contacts, walls,
pin contacts, x/y faces);  **L6′** λ₀ = Σ (far-wall multipliers), so λ₀ > 0 forces a loaded far-wall row,
and the H-component of that body reaches a near wall, a pin, or a loaded face (pins and faces are
GROUND: a pin's own stationarity is absorbed by its slack rows, a face by its row);  the λ₀ = 0 branch
is a self-stress of H including the faces.  **L3, L4, L5** hold verbatim for the contact part.

(e) *Census form.*  Dead_W(N) ⟺ for every selection S of the finite menu and every FJ-supporting structure
H realisable in the boxes, every FJ point of NLP_N(S) with support H and z ∈ Π has s > s0.

*Proof.*  (a) The set {(z, s) : s ∈ W, z ∈ N(s)} is closed (interior-disjointness is a closed condition on
the coordinates — D1's Lean proof `mem_interior_iff_uv`; Π_i closed; wall, pin and slot rows closed) and
bounded (s ≤ s_hi bounds every centre), hence compact; s is continuous.  (b) ⟸: a configuration at side
s ≤ s0 in W would give m_N ≤ s0.  ⟹: if m_N ≤ s0 then N(m_N) ≠ ∅ by (a) and m_N ∈ W ∩ (−∞, s0].
(c) The S-feasible set of NLP_N(S) is contained in {(z, s) : z ∈ N(s)} (its rows imply containment,
interior-disjointness by Lemma SAT / D3′'s dominance, and z ∈ Q_i ⊆ Π_i) and contains (z*, m_N); so
(z*, m_N) minimises s over it, and F. John's theorem (no constraint qualification) gives the multipliers.
(d) L1′: the stationarity rows in c_i read Σ λ·n = 0 over the rows involving c_i; one nonzero term cannot
vanish (a flush pair contributes two positive multiples of one normal, `structure_lemmas.md` L1).  L6′:
∂/∂s of stationarity is λ₀ = Σ_{far-wall rows} λ; summing the x-stationarity over a component of H whose
internal contact forces cancel in pairs leaves the external rows, which are walls, pin contacts (the
pin's side of the row is balanced by its slack rows) and faces; if none were loaded the far-wall load
could not be balanced (L6).  (e) ⟸ by (a)–(c): a minimiser with m_N ≤ s0 would be an FJ point of some
consistent S with s ≤ s0 in Π.  ⟹: such an FJ point lies in N(s) with s ≤ s0.  ∎

**Remarks.**  (i) The box rows are not optional: the pieces ARE the hypothesis, a face is a wall of the
hypothesis, and a minimiser pushed against a face is a legitimate stuck configuration (dropping the face
would let the configuration descend OUT of the node — into a neighbouring page).  A t-face of a body
whose tilt range is the whole [0, π/2] is not a constraint (the square's own 90° symmetry).  (ii) With
s_lo = s0 exactly, m_N > s0 ⟺ N(s0) = ∅, the record's question; (b) with s_lo = 3.82 is the window
form.  Both are relaxations in the same direction (a packing of the node at s0 is feasible in both), so
either kills.  (iii) Nothing in (a)–(e) uses n = 11 or the class: n bodies, any pins, any target.

## 3. What the boxes determine, and the solver

**Lemma CAND (candidate contacts) [T].**  For pieces A ⊆ Π_i, B ⊆ Π_j let gap_lo(A, B) := max_σ inf_{A×B} g_σ
(interval enclosure, `a116lib.gap_sel_iv`).  If min over piece pairs of gap_lo > 0 then no configuration of
N has i and j in contact (Lemma SAT: touching squares have SAT gap 0), so (i, j) is never an edge of any
support structure.  Likewise a body whose certified minimum of c·e − h(θ) (or s0 − c·e − h(θ)) over its
pieces is > 0 never touches that wall.  The remaining pairs and walls are the CANDIDATE GRAPH G_N.
*Proof.*  gap ≥ gap_lo > 0 on every pose pair.  ∎   (`contacts186.py`; the same enclosure gives, per pair,
the POSSIBLE selections — the menu of Theorem LOCAL.)

**Theorem CC-LP (the solver) [T].**  Let 𝒦 be a finite cover of the tilt box ∏_{i∈B} [t_i^lo, t_i^hi] by
cells; for a cell K let Π_i(K) be the hull of the pieces of Π_i whose tilt interval meets K's i-th factor
(a box ⊇ every pose of Π_i with tilt in K).  Then
  Dead_W(N) ⟸ for every K ∈ 𝒦 and every possible leaf λ on K: inf_{θ∈K} v_λ(θ) > s0,
where v_λ(θ) is Lemma LEAF's LP (walls, pins, the box rows of Π_i(K), λ's pair rows, tilts fixed at θ),
and conversely a leaf with v_λ(θ) ≤ s0 whose LP point lies in Π (not only in the hulls) is a
configuration of N at side ≤ s0.  The multipliers of a leaf LP are a balanced contact-force system
(Lemma GRAIN-LP) — the support structure H of Theorem CC (d) at that leaf's minimiser, faces included.
*Proof.*  Lemma COVER (every configuration with tilts in K lies in some P_λ(θ), the hull boxes containing
the pieces) and Lemma LEAF verbatim; Lemma RELAX gives the affine relaxation over K with second-order loss,
so the bisection tree of A116 (`Tree`) closes a cell iff the relaxed value exceeds s0.  ∎
(`tree186.py`: A116's tree with `PieceBody`, the centre box re-derived from the pieces at every cell;
`descend186.py` / `global186.py`: the leaf LP with an ELASTIC slack τ ≥ 0 on the pair rows — τ* = 0 iff
the leaf polyhedron is non-empty — as the measured search for the stuck configuration.)

**[F] What counting does not do.**  Theorem T1(d) (`fj_census_k0.md`): the census splits into
rigid-possible (m_H ≥ 3k_H + 1) and flex-only structures and neither is empty of genuine minimisers; a
support with m_H < 3k_H + 1 is a positive-dimensional critical manifold, admissible.  So "rigid enough to
be stuck" is not a prune; the sound prunes are L1′, L6′, planarity (L4, on the kiss-free support) and
the candidate graph.  The subgraph census of G_N (2^|E|, |E| ≈ 20–29 with walls) is therefore not the
object to enumerate; the selection tree enumerates leaves (≤ 8^k, pruned by interval FAR/IMPOSSIBLE and
by the LP) and the LP picks the support.

**What a certificate contains.**  For a DEAD assignment: the cell cover, and per (K, λ) the Farkas
multipliers of the relaxed LP (A116's O1–O4 object, exact rows via A133's Bernstein verifiers), consumed
by Theorem CC (b)/(e) through Theorem CC-LP, Reduction DROP for budget > 0, and the A171 soundness of the
pieces [S].  For a WITNESS: an exact-tilt LP point in Π with check_packing ≥ 0 at side ≤ s0 — a packing
of the boxed squares inside the boxes (then the unboxed squares, if any, are a sub-packing question).

## 4. Applied to c0_Y1033 (numbers in `attempts/A186-contact-census/notes/census.md`) [M]

Eight budget-0 assignments = four distinct geometries (the F2+F4 / F3+F4 choice at BL(0,2) leaves the
same pieces).  Candidate graphs: 24 / 20 / 24 / 22 edges (free–free 15 / 13 / 15 / 15; pin–free 9 / 7 /
9 / 7); H can touch only P4 and F1..F5; F2 the left wall; F3, F4 the left and top walls; F5 the top wall;
exterior faces 98–155 per body.  Selection tree (s_lo = s0, root cells ≤ 45°, min cell 0.5°): 2.5 ms a
node; node 0 at 2.1·10⁵ nodes — 8.4·10⁴ closed leaves, 5.1·10⁴ impossible cells, 0 exact-feasible
points, 0 unresolved, CAPPED; the lowest closed leaves are ROOT cells (45° wide) at v = s0 + 1.0·10⁻⁴,
i.e. the coarse relaxation is what keeps the tree open, not a near-packing.  Measured stuck configurations
(elastic exact LP over the tilts, 36 Nelder-Mead starts on node 0, 8 each on nodes 1–3): NO disjoint
configuration of the hull boxes found; least overlap τ = 0.0615 at s = s0 (node 0; support F2|F3, P2|F2:
the column above BL(0,1)), 0.12 / 0.079 / 0.17 on nodes 1–3.  **Verdict per assignment: [P] — not
certified dead (the tree is capped), no witness; the measured obstruction is the vertical crowd
P2 | F2 | F3 (| F4, F5) in x ∈ [0, 1.7] that the assignment stacks above BL(0,1).**  Figure:
`docs/residue_map/c0_Y1033_contacts.svg`.

## 5. Obligations

| # | item | status |
|---|---|---|
| CC-1 | Theorem CC (a)–(e) | [T] this file |
| CC-2 | Lemma CAND, Theorem CC-LP | [T] (A116 lemmas transported; hull-of-pieces boxes) |
| CC-3 | the multibox reading (pieces ⊇ poses of F; `invariant: False` flag) | [S]; the failing check to be re-derived on one node |
| CC-4 | the eight budget-0 assignments | [P] capped tree; measured obstruction τ ≥ 0.06 |
| CC-5 | a coexistence/column row for the crowd P2 | F2 | F3 | F4 | F5 (the certified form of the measured obstruction) | [P] next lever |
