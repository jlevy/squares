# DESCENT (3) — the worked examples: l1_104 (k0), c0_Y1033 (trump5), the A163 witnesses, Trump as canary — A194

Companion to `descent.md` (Lemma CH, D1–D3) and `descent_grains.md` (grains, precomputation).  Numbers [M] from
`attempts/A194-descent/results/hurt194.json` (`code/hurt194.py`: depths at the WIDENED box c_b = 1 + w on the
dilate F, Theorem B's clauses scanned at 1/8°, partner search 2·10⁵ draws with the configuration's squares as
obstacles).  Frame convention: corner frame (u, v) = distances from the corner's two walls.

## 7.1 l1_104 — k0, all four corners non-simple

**The object.**  k0_00 level-1 cell, converged-alive at τ = 10 = budget (A115/A140), one conditioned square H:
x ∈ [2.4626, 2.5674], y ∈ [2.1482, 2.2530], tilt [30°, 45°]; M(c) = 0 at all four widened corners (A165 certified),
so every corner crowd is two FREE squares; nearest packing K04 = the k0 twin of S08 (3.914214), no basin in any
frame (A187); A168/A183's cascade: S1 28 alive, S2 64 alive / 47 dead, S3 7,235 open nodes.

**What its LP support is, corner by corner [M].**  The A115 record's dual support (weights y):

| corner | support columns meeting the widened box (pose; depth; weight) | reading | Lemma CH |
|---|---|---|---|
| BL | (0.84, 0.64, 20°) d 0.628 y ½; (0.97, 0.58, 10°) d 0.548 y ½; (0.58, 1.55, 10°) d 0.055 y ½; (0.64, 1.64, 20°) d 0.027 y ½ | a genuine fractional 2-crowd: a deep SE-cell pair + a shallow NW-cell pair, all non-lonely | d₁ = 0.628, d₂ = 0.548; waste ≥ (c_b − d₁)² = 0.158; conversion cost 0.548 |
| BR | the SLOT SQUARE (3.377, 0.5, 0°) d 1.026 y 1; (3.377, 1.4998, 0°) d 0.026 y 1 | the k1 POCKET: the slot square and its flush neighbour BR(0,1) grazing the pad | d₂ = 0.026 = the pad w; waste 0 |
| TL | the SLOT SQUARE (0.5, 3.377, 0°) y 1; three grazers at (1.37–1.41, 2.47–2.51, 16°–30°) d 0.016–0.025, y ¼ ¼ ½, ALL LONELY | the k1 pocket with lonely grazers | R3 removes weight 1.0 here |
| TR | the SLOT SQUARE (3.377, 3.377, 0°) y 1; (2.368, 3.215, 1.5°) d 0.026 y 1 | the k1 pocket: the slot square + a near-flush TR(1,0) | d₂ = 0.026 |

So the support at the budget is **a k3-skeleton configuration** — the exact slot squares at BR, TL, TR (weight 1
each) with grazers of depth ≤ 0.026 — plus one real crowd at BL.  K0-BLOCKED (two meeters of the UNIT box on P)
excludes it outright: on P the three pockets are singly met (the grazers meet only the pad, `k0_route.md` §4.4 (a)).

**What the descent theorems say.**
* D1 [T]: at a k0 corner the extension class is k1_00, whose minimum is ŝ (it contains Trump's images); so the
  licensed depth s_T − m = ŝ − m ≤ 0 **at every side of the window, not only at its top** — the conversion route can
  never remove a pocket.  The pockets live on the PAD: at pad 0 the slot square is lonely (Cor. B1) and the grazers
  are not meeters, so the fixed-side (m = s0) lonely NO-family removes weight ≥ 3 from the support; at the full pad
  w = 0.0255 the slot square admits the (P)-partner at depth ≤ w and only TL's lonely grazers (weight 1.0) go.  The
  exact row is therefore SLAB-WISE — pad w(m_lo) = (s0/m_lo − 1)(1 + 1/√2) per slab, 0.00044 on the top 10⁻³ slab —
  which is A155's 2 % pad seen from the LP: the pad is what lets the LP pay for a k1 pocket at every corner.  [S:
  the LP re-prices; the re-solve is not run here.]
* D2 [T]: no basin to descend from — K04/S08 has no certificate in any frame.  The precomputation that would give
  l1_104 a lookup is S08's basin in k5_16 (A116 campaign, 1–3 CPU-h to a first box set) and its pin-free descent
  (the DROP tree with the load-bearing slots as bodies, ≈ 1 CPU-h).  For the cell l1_159 (K06 = the pinwheel at
  3.886745 reached from k0) the pin-free descent of S02's existing 54 box sets is the whole cost: **≈ 1 CPU-h for
  one of the eleven cells** — the cheapest lookup the residue offers.
* CH-A: the four corners waste ≥ 0.158 + 0 + 0 + 0 in the LP's picture and, in any genuine k0 packing with crowds
  of depth (d₁(c)), Σ_c (c_b − d₁(c))² ≤ s0² − 11 − 0.129 = 3.903 (A164's east-strip |U|): vacuous, as it must be.
* D3: the BL crowd of the support is not on any grain's load path (the support is room, K01/K04-type), so the
  completion dichotomy's case (i) applies — at BL the crowd hurts for nothing and the exchange at cost 0 lands in
  k1_00 whenever the exposure is empty; the exposure test is the lane on the BL cell with H as the only obstacle,
  which A118's leaf already found blocked ("the lane that stays open is always the same one").
**What it would have saved.**  Nothing on l1_104 itself today (no grain, no basin); the value is the diagnosis: the
cell is alive because the LP buys three k1 pockets with the pad, and the cascade (roles at all four corners) is
the only geometry that removes them.  For the k0 residue as a whole: l1_159 by lookup after ~1 CPU-h.

## 7.2 The A163 trump5 witnesses — Theorem D2(b) on nine real objects [M]

A163 re-ran S02's 54 box sets in the trump5 frame (TL(0,0) dropped) and got 42 certified, **9 refused by LIVE-LOW
witnesses**: 9-square partial packings of L ∪ P (f1 f2 f3 BR(0,1) + trump5's five pins) at sides 3.8205–3.8771.
Each witness dilated to s0 and read at the widened TL box:

| witness (box set) | side | TL meeters | f1's frame pose (u, v, θ) | depth | Theorem B | partner (2·10⁵ draws) |
|---|---|---|---|---|---|---|
| 021 chain −40.0° | 3.8205 | f1 only | (1.213, 1.271, 81.6°) | 0.202 | LONELY (best S at 89.9°, margin −0.30) | none |
| 022 chain −42.5° | 3.8200 | f1 only | (1.228, 1.290, 84.1°) | 0.197 | LONELY (−0.26) | none |
| 023 chain −45.0° | 3.8200 | f1 only | (1.247, 1.310, 86.6°) | 0.191 | LONELY (−0.22) | none |
| 029 RXY probe −10° | 3.8687 | f1 only | (1.019, 1.169, 51.6°) | 0.279 | LONELY (S 38.4°, −0.16) | none |
| 030 RXY probe −10° | 3.8523 | f1 only | (0.973, 1.157, 51.6°) | 0.306 | LONELY (−0.13) | none |
| 027 chain h10 −40° | 3.8200 | f1 only | (1.217, 1.244, 1.6°) | 0.295 | LONELY (S 88.5°, −0.26) | none |
| 031 slice f2 −20° | 3.8769 | f1 only | (0.863, 1.343, 4.1°) | 0.217 | LONELY (S 34.6°, −0.13) | none |
| 033 slice f3 −20° | 3.8771 | f1 only | (0.863, 1.299, 1.6°) | 0.240 | LONELY (−0.15) | none |
| 053 A151-B | 3.8739 | f1 only | (0.863, 1.341, 4.1°) | 0.219 | LONELY (−0.13) | none |

**Every one of the nine witnesses has f1 as the ONLY TL meeter, in a LONELY pose** (margins −0.13 to −0.30 on the
best clause; the sampled partner search agrees, 0 of 2·10⁵).  In a trump5 packing TL(0,0) is a forced corner
(k6_23 dead on the window, Theorem FC), so f1 in these poses cannot occur: **D2(b) kills all nine witnesses.**
What is NOT yet shown: that the nine box sets CLOSE after f1's box is clipped by the lonely set — the descended tree
must be re-run (a refusal can move to a non-lonely f1); the clip is large (f1's leaning-in poses near the corner are
lonely because a deep meeter pressing toward the corner blocks both wall approaches, Cor. B4's slide threshold), so
the expectation is that most of the 9 close, taking trump5's pinwheel basin from 42/54 toward 54/54 and its consumer
count from 3/12 up.  [C: the re-run, ≈ 9 × (4–445 s).]  This is the first place where the corner-hurt lemma converts a
higher-k certificate (S02's basin in k5_11, with the TL pin) into a lower-k kill (the same basin in trump5, without
it) by a clip instead of a tree.

## 7.3 c0_Y1033 — trump5, TL(0,0) and BR(0,1) forced

**The object.**  A60 level-1 trump5 page, H at x ∈ [2.4976, 2.6373], y ∈ [2.3578, 2.4976], tilt [14.25°, 28.07°],
τ = 5 = budget, family S01 (side 4.000); six forced cells (BL(0,2), BL(1,1), BR(0,1), TR(0,1), TR(1,0), TL(0,0)),
TL(0,0) the forced CORNER; A182: ALIVE under the forced-first assignment (BL(1,1) ← F1+F2; BR(0,1) six options;
TR(0,1) ← H+F1 under branch 1; TL(0,0) five options); A186: the eight budget-0 leaves have no witness and their
least overlap is 0.0615 in the upright column P2 | F2 | F3 above BL(0,1); A189: 5 NO-ROOM kills at k = 10.

**What the descent theorems say.**
* D1 at TL(0,0): T = k6_23 ⊂ S02's skeleton, so s*_T ≤ 3.886746 and the licensed depth is ≤ 0.0097 even after
  certifying k6_23 above s0; today 0.  At BR(0,1): T = k6_21, s*_T ≤ 3.9289 (S38 ∈ k6_21; 3.914 if S08's match is genuine), depth ≤ 0.052.  Nothing.
* CH-L at TL(0,0), the row A186 asked for (CC-5) [T].  The TL crowd's band meeter hugs the left wall (NW/SW cell,
  u_z < c_b) or the top wall (SE/SW, v_z < c_b).  LEFT case: on every vertical line x = g with |g − u_z| ≤ γ(θ) its
  chord is ≥ 1; the exact pins BL(0,0), BL(0,1) have chord exactly 1 on every x = g, g ∈ (0, 1) (slack h: g ∈ (h,
  1 − h)); since u_z < 1.0255 and γ ≥ 0.207 the two ranges meet, and on that line Σ chords ≥ 3, so every OTHER
  square crosses it with chord ≤ s0 − 3 = 0.877 — in particular an upright F2 or F3 at x ≈ 0.5 (chord 1) is
  impossible: **the column P2 | F2 | F3 dies whenever the TL band meeter is on the left wall and is not itself F2 or
  F3**; if it is (A186's assignment puts F2..F5 on the left/top walls), the count is pins 2 + uprights 2 = 4 > s0
  on x = 1/2 outright.  TOP case: the mirror on horizontal lines y = s0 − g with TR(0,0)'s chord: Σ ≥ 2, rest ≤
  1.877 — one more unit chord at most on the top strip (the PI's cascade step (b), now a row).  Emission [C4-type]:
  A190's `guardlines` clause takes FIXED lines, so the band meeter's box is cut into centre-slabs of height ≤ 2γ(θ_max
  of the piece) and each slab carries one line at its centre with `minchord ≥ 1` certified over the slab — a
  cheap pre-screen at every A182 node where a TL role is a wall-hugger.
* D2: S01's certificate is A188's LINE band (side = 4 exactly on the lock line); c0_Y1033's box is not in a band
  on a pin line with the three free chords supplied (A188: "15 of 23 pages inside a band, always on a line with ONE
  pin, the YES leaf owes two boxes to the NO children"), so containment gives nothing; the descended form of S01 is
  the chord row itself, which is CH-L above.
* D3: the S01 shadow's load path is {f3, BL(1,0), BR(0,0)} (the bottom row); the TL crowd is off it, so the completion
  dichotomy's case (i): if the exposure of TL's slot square is empty the page's configuration is a k6_23 packing at
  the same side — dead by k6_23's kill.  The exposure test at TL with H, the pins and the assigned roles as obstacles
  is A178/A182's lane on TL(0,0), which A182 branched five ways instead; the D3 form says the branch "TL(0,0) =
  two new squares" is dead whenever LANE(TL slot | roles) = 0 for the SLOT SQUARE ITSELF (the exchange placement),
  a single exact SAT test per node against the roles' K′ — not run by A182.
**What it would have saved [S].**  The TL-NW chord row at the assignment root removes every option in which a
wall-hugging TL meeter coexists with the upright column A186 found (the assignment's least-overlap configuration),
before any of the 584 multibox nodes / 3.0 CPU-h; the slot-square exposure test prunes the "two new" TL branch.
The page is not thereby dead — its S01 room is the k5-tree's genuine tail — but the branch A182 spent its budget on
is the one the row addresses.

## 7.4 Trump — the canary [M]

TL crowd on F: sq6 (tilted, 40.06° in the container, frame pose (1.536, 0.705, 49.8°)) at depth 0.194, sq4 (the
upright at the left wall, (0.5, 1.345)) at depth 0.181 — both NON-LONELY (sq6 by clause (W) at 49.75°, margin
+0.30; sq4 by (S) at 24.6°, +0.20), distinct cells (SE, NW), conversion cost d₂ = 0.181 (0.155 at the unit box),
sealed waste ≥ (1.0255 − 0.194)² = 0.692; and no THIRD meeter fits (partner search 0 of 2·10⁵ with all eleven as
obstacles — the crowd is exactly two).  The simple corners: BL's slot square with BL(1,0)/BL(0,1) grazing the pad
at depth exactly w; BR's and TR's slot squares with sq8/sq9 grazing at depth 0.0254/0.0252 < w in LONELY poses —
the pad's k1 pockets of §7.1, realised by Trump itself.  Every lemma of `descent.md` holds on ẑ; none kills it.

## 8. Pointers

`docs/proofs/descent.md` (Lemma CH, D1–D3, obligations C1–C4); `descent_grains.md` (grains, P1–P6, dynamics);
`attempts/A194-descent/{BRIEF.md, code/hurt194.py, results/hurt194.json, logs/}`; `docs/residue_map/descent.svg`
(`gen_descent.py`); `sideband.md` §3 (Theorem B), `forced_corners.md` §0 (Theorem FC), A163 `results/witnesses163.json`,
A160 `results/{slide_exact,N_boxes160}.json`, A186 `notes/census.md` (the column), A188 (the S01 line).
