# DESCENT (2) — grains: the three grains, their coverage precomputation, and the joint tilt/slide dynamics — A194

Companion to `descent.md` (Lemma CH, Theorems D1–D3); examples in `descent_examples.md`.  Tags as there.
Sources: `grain_flood.md` (Lemma GRAIN-LP, INHERIT, Theorem CONT, the chain menu Λ, Y, D, F_T), `local_certificate.md`
(Theorem LOCAL, Lemma STAB, DROP), A107 `shadows.json` (contact graphs, Fritz-John loads), A160/A163 (the pinwheel's
basin union, chain, slices, f0's slide), A76 (Trump's 78 rows, rigid/flex dichotomy), A128/A130 (`drain_sel.md`:
cluster screw, Gordan dual, BOX-FIELD-W), A171/A172 (pieces, per-piece K′), A190 (MINCHORD over a box).

## 4. What a grain is

**Definition [T, n-general].**  A GRAIN G = (I, E, Φ, s_G) is: a set I of k squares; an internal contact graph E
(pairs and walls, each with its contact type — vertex-on-edge, flush, exactly-opposite — and a signed selection);
a FREEDOM chart Φ: the internal configuration space of I with the contacts of E active is a semi-algebraic set whose
coordinates are the common tilt θ (when the load path shares one), the SLIDES u (rattler segments) and the residual
internal offsets; and the chain formula s_G(θ) = the length of G's wall-to-wall load path (Lemma GRAIN-LP: at fixed
tilts the side minimum with G's selection fixed is an LP whose dual is a balanced force system on E).  A grain is
RIGID when Φ is a point at fixed θ (Krawczyk rank, A76), FLEX otherwise.  The SHADOW of G in a class frame is the
placement of I (and of the slots G leans on) at s*; a node's support MATCHES G when A107's `inside()` injects G's
boxes into distinct support squares.

**The three grains named by the PI, as the corpus has them [M].**

| grain | squares I | internal contacts E (A107/A76) | freedoms Φ | load path / chain | where |
|---|---|---|---|---|---|
| **Trump 5-grain** (the tilted strip) | sq6 sq7 sq8 sq9 sq10 of ẑ, common tilt 2·atan(0.36577) = 40.0598° | the diagonal strip's flush and corner–edge rows among A76's 36 Trump rows; its TL end sq6 is a TL meeter (depth 0.168 unit / 0.194 widened) resting with sq4 | RIGID at ẑ (rank 34, A22/A76); as a free body: common tilt + the wedge freedom that F_T(θ) prices | F_T(θ) = 2 + (2 + sin θ)/(cos θ + sin θ): ŝ = F_T(θ_T) to 40 digits (TRUMP-GAP) | Trump's basin (Theorem U, the tube); k0 cell l1_153 = its sq9 |
| **Pinwheel 4-grain** (S02) | f0 f1 f2 f3 at θ* = 48.43512° | f0–f3 (vertex-on-edge, 2 rows), f0–BL(1,0), f1–f2 (exactly-opposite, 4 rows), f1–f3, f2–f3 (vertex-on-edge), f1–BL(0,1), f1–TL(0,0), f3–BR(0,1), f3–TR(0,0), f2–top wall | common tilt θ (spine s*(θ) > s0 on [3.4°, 88.4°], min Λ(θ*) = 3.886746 at the triple point sin θ cos θ = 2 sin θ − 1); f0 = strut: a SLIDE of length 0.298419 along e₂(θ*) with rails BL(1,0)/f3 and stops BR(0,1)/f1, tilt window ∝ √ε; BR(0,0) a second rattler (0.5357); f2/f3 tilts independently certifiable over the whole fundamental domain at f1's base box | load path {f1, f2, f3, BL(0,1), BR(0,1)}; Λ(θ) = 2 + 4u/(u² + 1), u = cos θ + sin θ, crossing D(θ) at θ* | basins: k5_11 (A160, 54 sets), k5_16 (A163, 52/54), trump5 (A163, 42/54 + 9 witnesses) |
| **V 3-grain** (a corner crowd with its presser) | a band meeter A on one of c's walls, the second meeter B, and the square C that presses B toward c (JAM/WEDGE/BLOCK of A85 `cases85`; FLUSH-JAM's A, B, T) | A–wall, A–B or B–slot-side, B–C; the contact normal of B–C is what makes B an intruder (Lemma CROSS) | A's slide along the wall (Cor. B2: δ > tan(θ/2) for a partner), B's tilt, the pair's 6-dim interior (K0-PAIR) | none of its own — it is the END of a chain (Trump's TL: sq4 = A, sq6 = B, sq7 = C) or a wedge; priced by the hook formulas HOOK-α/β (`lockfree.md`) when it sits on a held wall | every non-simple corner; Trump's TL; l1_104's BL support |

The V 3-grain is the crowd itself, seen as a rigid sub-configuration: its "coverage" is Lemma CH's region (Theorem B ×
Lemma A2 × the container), and its basin is nothing on its own — a V is dead only through the chain it terminates.

## 5. The precomputation — per grain, once, then lookup

For each grain G and each class frame Σ (pins P_Σ), the table T(G, Σ) holds, over a cover of Φ by (θ, u, position)
boxes:

 (P1) **Validity** V_G: the boxes in which I's squares are pairwise interior-disjoint at every pose and inside the
      container at every side of W — A171's exact dead test per pair on pieces (interval SAT), the container clip per
      tilt sub-bin; cost seconds per box.  [T: what the machinery certifies; M: the cover]
 (P2) **Obstacle** K′_G(box) := ⋃_{i ∈ I} K′(box_i) — the union of the per-piece polygon cores (A172), sound because a
      point in some K′(box_i) is inside square i at every pose of the box; the intersection over poses of the UNION
      ⋃ Q_i is larger but non-convex and not needed.  Cost: A172's builder, seconds.  [T]
 (P3) **Chords**: for every guard line ℓ of the lab's list (A188's 72 pin lines per frame, the wall lines at distance
      1/2 and 1 + w, and the band meeter's centre lines of CH-L) the certified `minchord(box_i, ℓ)` per square (A190's
      exact rational formula over the box, antitone in the distance) and the sum Σ_i minchord — the grain's
      contribution to LINE-1's right-hand side s − Σ.  Cost: microseconds per (box, line).  [T]
 (P4) **Basin** Dead_{I ∪ P_Σ}(box, s0): Theorem LOCAL's tree — exists for S02 in three frames and S07 in trump5;
      cost 4–445 s per box set (A116/A160), the growth ladders 1–10 CPU-h per frame (A151/A160/A163).
 (P5) **Descended basins** (Theorem D2): for each pin p ∈ P_Σ that a lower class lacks, and for the pin-free (k0)
      frame: the DROP tree + lonely clip + partner lane per surviving leaf.  Cost: one A163-type re-run per dropped
      pin (≈ 1–7 CPU-h for the 54 pinwheel sets), and for k0 the DROP tree with the load-bearing slots as BODIES in
      slot-sized boxes instead of pins (5 bodies for the pinwheel: f1 f2 f3 BL(0,1) BR(0,1)) — A116's base tree is
      205 s with 4 bodies; ≈ 10× with 5, so ~1 CPU-h per grain for the k0 descent.  [M for the costs, T for the tree]
 (P6) **Lookup**: a node dies when its support matches G inside a T(G, Σ_node) box whose (P4)/(P5) entry is closed —
      A187's `cons` column, no LP; its LP is re-priced, not killed, by (P2) as an exemption of K′_G (a cored obstacle
      for the free columns) and by (P3) as `guardlines` rows.

**What exists / what is missing / what it costs [M].**
* S02: (P1)–(P4) exist in three frames (the union of 54 box sets: A151-B, the common-tilt chain of 31 links, 22
  independent-tilt slices; A163's re-emission through A133's generator, 94 VALID); (P5) exists ONLY as A163's DROP
  step (k5_16: 52/54; trump5: 42/54) — the lonely/partner steps of D2 were never run; `descent_examples.md` §7.2
  measures what they do on the nine trump5 witnesses.  The k0 descent (P5, pin-free) does not exist: ~1 CPU-h.
* S07: (P4) in trump5 (two sets, the Trump-boundary cut at θ_T + 6·10⁻⁵°); no (P5).
* Trump's 5-grain: its basin is Theorem U / the tube (A65, A83) — already pin-free (the tube is a statement about
  all eleven squares); (P2)/(P3) trivial (the strip is rigid).  Nothing missing.
* S01 (23 alive pages), S03 (11), S08/K04, S05, S10, S36, S11, S53, K01–K06: NO basin in any frame (A187 §2), so
  D2 has nothing to descend.  S01 is the plateau {side = 4} of the four-chord lock and its certificate is A188's
  LINE band (72 entries per frame; basin half-width 0.207 across the line, unbounded along it) — pin-free already
  except that the lock line carries ONE pin; its descent is the chord row itself.  S03 (3.9428, 8 slots + 3 free) and
  S08 (3.9142, 5 slots + 6 free) need first certificates: one A116 campaign each, 1–3 CPU-h to the first box set,
  10–50 CPU-h to a union comparable to S02's.  These are the missing objects that would make D2 bite on 34 of the
  52 alive A57/A60 pages (A187: 23 S01 + 11 S03).
* The V 3-grain: (P1) is Lemma CH-C's region — the lonely raster exists (A169 `lonely_exact.json`, pitch 0.02, ten
  tilts) and the exact criterion is a quartic in tan(ζ/2) per piece (R3's box test); the pair census at A60's box
  width is ≈ 5·10³ pairs per corner after R1/R3 (`sideband.md` §6).  No basin, by definition.
* D1's precomputation (extension classes certified above s0, `descent.md` §3.1 table): parametric slabs on
  [s0, s*_T − ε] per k6 class; by the slab-width law the cost per class is comparable to A56's whole-window run
  (2–30 CPU-h) for a licensed depth ≤ s*_T − s0 ≤ 0.01–0.05 — and the k0 corners' extension class k1_00 has minimum
  ŝ, so **at a k0 corner D1 licenses depth 0 at every side, forever** [T].  Not worth buying.

## 6. Joint tilt/slide dynamics — how a grain moves, and how a move descends

**6.1 The moves [T/M].**  (a) COMMON TILT: along θ the loaded rows stay loaded and the side is s_G(θ) (Lemma
INHERIT, Theorem CONT); the pinwheel's spine rises on both sides of θ* (3.9968 at 3.4°, 3.9741 at 88.4°), S07's
ladder crosses Y at 45° and drops into Trump's grain at 41.565° (f0's vertex reaching BL(0,1)'s corner: the basis
changes to F_T).  (b) SLIDES: a rattler moves on a segment at FIXED tilt between two stops, its tilt window closing
like √ε (f0: 0.298 along its own body axis; BR(0,0): 0.536); the side is unchanged along a slide.  (c) COUPLED
MOVES: a cluster screw and its Gordan dual certify "held" on a box (A128); the non-rigid field with flush kinks
charged exactly (BOX-FIELD-W, A130) certifies the 4.001525 lock at all eight intruders; Trump is first-order
isolated at all nine subjects.  (d) The MODE accumulation at the flush stratum (Lemma MODE) is why a fixed field
misses the deep meeter's retreat at a slot-plus-flush corner — the only place where the k0 window holds survive.

**6.2 Descent along a move [T].**  The basin region R of T(G, Σ) is a union of boxes in (θ, u, positions); every
statement of D2 is made on a box, so a node whose support sits at (θ, u) is priced by the box containing it, and a
move of the grain inside R changes nothing: **kills are constant along moves inside a certified box, by construction
— the move is the coordinate, not the mechanism.**  What a move CAN do is leave R: A160's witnesses are exactly the
grain moved (f1 to 83°, f2 up by 20° together with A151-B's grown f1) to a pose where the nine bodies fit below s0.

**6.3 The completion dichotomy [T].**  Let P be an S-packing at side m containing the grain G (matching a box of
T(G, T-frame)) with the corner p non-simple, crowd {A, B}.
 (i) If neither A nor B is on G's load path and Lemma EXPOSE's exposure of the slot square at p together with a
     re-fit Q₀ is met by no untouched square, then P ∖ {A, B} ∪ {slot, Q₀} is a T-packing at the SAME side m
     (FLOOD-M), so m > s_T: **the non-simple corner hurts for nothing — P is dead by T's own kill.**
 (ii) If A or B is on G's load path (Trump: sq6 is both the TL meeter and the strip's end), the exchange breaks the
     chain, the completed configuration has a different load path, and its side is the new chain's value — D3(ii)'s
     cost s_G′ − s_G — which may be LOWER (Trump beats its k6 completions by exactly this: the crowd's overhang is the
     strip's wedge).  Then P is not dead by descent; it is a candidate of a different grain, and its basin is that
     grain's.
So **the non-simple corner is harmless to the kill unless its crowd is LOAD-BEARING**, and whether it is load-bearing
is decided by the leaf LP's dual (GRAIN-LP), never by counting: the same existential-filter law as A89–A110.

**6.4 What the LP sees of a move [M].**  The dual support at an alive node is a shadow at ONE (θ, u) with the
rattler at an arbitrary point of its slide (A160: the gallery's f0 sits at u = 0.120 of the segment) and the strut
at an off-family tilt (A110's c0_Y0324: the rattler at 53°–64°); the box → grain map is one-to-many (A106: 62 boxes
flow to eight shadow values).  Lookup (P6) therefore matches on the LOAD-BEARING squares only (A116's `LOADBEARING`,
`inside()` over L), never on the rattlers — f0 as a required box costs 96/42 → 15/8 consumers (A160 T2).
