# 07 — The dated timeline, A01 → A243 (and the k0 series A244–A281), with the external events placed in it

**Abstract.** One line per campaign that produced a result, from `attempts/REGISTRY.md` (status | outcome) and the
first-commit date of each campaign directory, grouped by month.  Status vocabulary: done-success / done-negative
(recorded precisely so nobody repeats it) / done-mixed / running / abandoned.  External events (your register:
T-037, T-060, T-112; the Burns–Massaccesi n = 17 note) are placed where the lab met them.  The lab ran on one
desktop (≤ 10 Python processes) from 2026-08-16; the dates are commit dates, not wall-clock starts.

Repository https://github.com/Esummins/packing; `blob/master/attempts/REGISTRY.md` carries the full rows, and
`attempts/<id>/` the notes, code, certificates and logs of each.  Tags in outcomes: [T]/[M]/[F]/[C] as in `00`.

## August 2026 — foundations, the 3.82 bound, the walls, the stratification

| date | id | status | outcome (one line) |
|---|---|---|---|
| 08-16 | A01 literature | success | 3.788854 (Stromquist 2003) ≤ s(11) ≤ 3.8770835900228 (Trump 1979); no formalisation exists |
| 08-16 | A02 Stromquist analysis | success | the proof is a case split, not a pure point set; two errata; pure 10-point sets top out ≈ 3.74 |
| 08-16 | A03 Trump reconstruct | success | Trump's packing to 60 digits, 56 contact equations, rigid; the octic; equal gaps 0.02487… |
| 08-16 | A04 upper search | negative | 2,488 local optima, Trump rediscovered 276×, nothing below; runners-up 3.885618, 3.886746 |
| 08-16 | A05 unavoidable sets | negative | best pure 10-point unavoidable set ≈ 3.7505 < Stromquist: the point method is exhausted |
| 08-16 | A06 Lean setup | success | kernel-checked s(11) ≤ 3.877084 (`checkPacking trump11`); integer measure checker |
| 08-16..18 | A07/A08 LP dual + exact verifier | success | **s(11) ≥ 3.80, 3.81, 3.82** certified (`certs/measure_certificate_3.82.json`); τ*(3.83) = 11.000 |
| 08-18 | A09/A11 angle-lattice MILP | finder yes / certifier no | finds Trump ab initio in 43 s from two angles; no beat for any n ≤ 100; n = 18 rediscovered exactly |
| 08-18 | A10/A12 angle-box LP, region rank | negative | a ¼-weight fractional pinwheel holds τ = 11 at every box size; macroscopic cuts are escaped by sliding |
| 08-18 | A13/A14 case-LP tree at 3.84 | negative | three oracle bugs found; fixing corners never kills; 10⁵–10⁶ LPs |
| 08-19 | A15/A16 Lovász ϑ′ | success (pilot) | ϑ′ ∈ [10.38, 10.48] vs LP 11.000 on the same graph; kills every node the LP cannot — not a bound on s(11) |
| 08-19 | A17–A20 continuum kernels | negative, with a theorem | collapse theorem: every pair-free kernel class ≥ the LP value; τ*(3.84) ≥ 11 exactly |
| 08-20 | A21 structure at 3.88 | success [T] | corner-zone occupancy certified above ŝ (measure total 10.5611) |
| 08-20 | A22 local rigidity | success | Krawczyk enclosure at radius 5·10⁻⁴ around Trump: one contact solution; every packing there has s ≥ ŝ |
| 08-20 | A23/A25 wastage oracle, atlas | success [T] | the integral pinwheel is dead at ŝ by area; atlas 2.9–8.9 s per cell (≈ 2000× A23) |
| 08-21 | A26 wall ledger | negative, 3 theorems | ≥ 10 of 11 squares meet the width-1 band; charging dies on an exact zero |
| 08-24 | A28 Lean + Mathlib | success | Mathlib installed; s(11) ≤ 3.877084 as a statement about ℝ² (`eleven_unit_squares_in_3877084`) |
| 08-20..26 | A24/A27/A29 composed tree at 3.84 | negative / PAUSED | 123/216 cells discharged, 179 verified certificates; paused by the PI on 08-26 — bounds prune nothing in the exclusion programme |
| 08-26 | A30 T3 pilot | negative (cost) | critical-point exclusion as a configuration-space cover: c³³ ≈ 8·10⁸ cells; two corrections to the drain lemma |
| 08-26 | A31/A32 structure counts | negative, decisive | 4·10²⁹ contact structures; "any complete search that visits survivors of the current lemma set is dead" |
| 08-27 | A33 tight variety | mixed | grain conjecture refuted in range; **s(12) ≥ 3.90** certified as a by-product |
| 08-27 | A34 sparse SOS | negative [T] | collapse: a relaxation with cliques of m < n squares caps at s(m) |
| 08-27 | A35/A36/A37 escape complex, levers, CP atlas | success | Trump's basin certified at radius 3.7·10⁻³ (7.56× A22); 32 critical-point families collapse to 10 attractors |
| 08-28 | A38–A42 far-field tree, early cert, basin, seam, occupancy | mixed / NO-GO | the per-node LP decision cost at ŝ is the wall (0/60 decided); the occupancy family has zero forcing power |
| 08-28..29 | A43–A48 bulk kills, FJ-Maxwell, charging, wedges, majority, bridge | negative, with theorems | the enumeration–certificate mismatch law and its seven faces |
| 08-29..31 | A49–A52 flush-free hunts, wall termination, two-field probe | mixed | 252/252 drains acquire flush; θ* = 1.7347° near-flush exclusion for chain members; joint LPs collapse to one |
| 08-31 | **A53 simple-square strata (PI)** | success, load-bearing | census 1110 tuples / 163 D4 classes; k ≥ 7 empty; 32/33 k = 6 classes dead |
| 08-31 | A54/A55 stragglers, k = 4 sweep | success | k ≥ 6 tier closed unconditionally; 8 of 14 k = 4 classes killed exactly — **exactly sharp** (empty iff in no open k = 5 class) |
| 08-31 | A56 s-parametric window | success [T] | census stable on [191/50, s0]; atoms affine in s; 38/52 rows window-grade |

## September 1–8 — Lean, the k0 core, the reading loop

| date | id | status | outcome |
|---|---|---|---|
| 09-01 | A57 shadow trees (k5_11, k5_16) | running → paused | Lemma A57-1: both interior NO-children killed (τ = 3.000 vs budget 6); the priced compute item of the lab |
| 09-01 | A58 clear-corner teleport | success [T] | CC-2: at a k-maximal minimiser every completable slot is doubly met |
| 09-01 | A59/A60 trump5 programme | GO / running | residual zone tree contracts onto Trump at ratio 4.55 per level; lands in the basin |
| 09-01 | A61 window stragglers | running → done | 12 s0-only rows converted; k5_13 hung 40 CPU-h in an LP |
| 09-01 | A62/A63 trust ledger, hole closure | success | `TopLevel.lean` with 13 named axioms; three HIGH holes found by writing the composition; ŝ a definition |
| 09-01..04 | A64/A68/A70/A75/A78/A79/A86/A93 Lean waves | success | **s(11) ≥ 3.82 end to end in Lean**; attainment; the census a definition with L3 a theorem; axiom roster 16 → 3 |
| 09-02 | A65 Theorem U | success [C] | one-square rigidity of Trump: 11 re-insertion certificates PASS at depth 60 |
| 09-02..03 | A66/A71/A73/A74/A77/A80/A81 pair certificates (corners4) | mixed, negative | a quantified verification wall: complete trees retain 0.75–0.86 per level; pair route closed in that form |
| 09-02 | A67/A69/A72 D4 rerun, CIDL identity, census clean-room | success | the census independently re-enumerated and matched exactly; e·Δ⁸·octic identity certified |
| 09-02 | A82 side scan | mixed [T] | the aliveness cliff is a step of exactly one at ŝ (k4 classes alive at s0 only) |
| 09-02 | A83/A84 contraction tube, protected trees | success | tube reaches T = 0.0574 ≥ the whole window at r = 6.5·10⁻⁴; **Lemma P-TREE** |
| 09-02 | A85 k0 route | mixed | K0-FREE, K0-D4, K0-ROT proved; price 3,200–7,000 CPU-h, no order-of-magnitude cut |
| 09-02 | A87/A88 drain-flow, FJ census | success / mixed | DF-K0 in two lines; H1 as a cover loses on the count |
| 09-03 | A89–A92 tilt floor, NOCRIT, frame census, blocked side | mixed | no loaded tilt floor; NOCRIT-SEL [T]; 5.7·10²⁸ frames mod G; crowd certificate PASS only at δ = 0.3 |
| 09-03 | A94 slot crowds | mixed | **SLOT-CROWD [T]** ∀-packings; the crowd certificate does not certify (B₂–B₄ FAIL, 30–32 holes) |
| 09-04 | A96–A99 parametric A57, wall budget, exchange, k0 tree v2 | mixed | parametric window certificates at 0.2 of one side; j ≤ 3 jams [T]; the "10×" was never there |
| 09-04..05 | A100 protected pilot | mixed | the tier priced by LP: 3,500–4,200 CPU-h (k4_11, k3_02 end to end) |
| 09-05 | A101–A105 flood, rigidity drain, NOROOM, grid lock, lock-free | mixed | SNAP proved (destination form); every K0-BLOCKED packing below 4 drains; locks first appear at 4.000237 |
| 09-05..06 | A106/A107/A108 shadow gallery | success | 53 shadows explain 1,260 of 1,566 alive nodes; S07 = 2 + 4√2/3 exactly (Q(√2)) |
| 09-06 | A109/A111/A112/A115 crowd rows, load paths, dual branching, corner rows | negative / mixed | rows re-price rather than forbid; corner rows kill 0 of the genuinely alive cells |
| 09-06..08 | A116/A119/A126/A134/A138/A139 local certificates in Lean | success [L] | LocalDead S07 and S02 as kernel theorems (`native_decide` 571 s / 6,707 s) |
| 09-06 | A117 verifier v2 | success | frozen v2 byte-identical with v1 on 30/30; `nofamExemptIV_sound` in Lean |
| 09-07 | A118/A121 lane count, reading validator | mixed | 83/83 PI readings validated: 0 new kills, 9 node kills already booked |
| 09-07 | A122/A125 S33/S35/S38 | success | S33 = 3.9169308657… (50 digits); S35 a second distinct minimum |
| 09-07 | A123/A124/A137/A149 night and day shifts | success | work-owing 632 → 406; exact-core re-solve certifies 28.6 % of alive nodes |
| 09-07 | A129 net verifier (external) | success | the Burns–Massaccesi n = 17 note: their certificate is the same object as ours (an atomic measure, total < n) |
| 09-07 | A131/A132/A135/A145 pin clip, polygon core, exact cores | success | 132 open nodes clipped EMPTY in 4.1 s; K′/K area median 1.225; exact cores certifiable under the frozen verifier |
| 09-07 | A140/A141/A143/A148 k0 galleries, K′ lane, corner-first | mixed | s3_far certified dead; 47 k0 cells killed by the K′ lane; corner-first root not cheaper |
| 09-07 | A114/A146 window closers | success | **52/52 scoreboard rows FULL on the window** (k5_13 last, 58 slabs of 10⁻³) |
| 09-07..09 | A144/A161/A167 guard lines, chord lane, conditional lane | mixed | Theorem G (after a soundness fix); 27 + 11 new kills; 285 cells retired by exact two-crowd witnesses |
| 09-08 | A150–A159/A164/A166 corner-first line | negative | closed from every side: the "free lunch" leaf provably unavailable; UNDECIDED slots are real 2-crowds |
| 09-08 | A151/A160/A163 pinwheel basin | mixed | the basin is a union of boxes (growth directions trade off); transfers to k5_16 (52/54) |
| 09-08 | A165 cascade on l1_104 (PI) | negative | sound at every step, canary survives, cell not closed; killed by the PI at 00:35 |

## September 9–16 — the k0 cascade, the k5 killer, the exact kernels, the k0 lemmas

| date | id | status | outcome |
|---|---|---|---|
| 09-09 | A168–A176 cascade, sideband, invariant library, lonely clip | mixed | **SIDEBAND (a) [T] sharp; Theorem B**; the clipping rule is code with a guard; 42 of 146 nodes die by the lonely clip |
| 09-09 | A177–A187 queues, assignment, basin map, contact census | negative / mixed | one closure by the entry rule; c0_Y1033 ALIVE (23 complete assignments); the residue is not basin-shaped |
| 09-09 | A185/A189/A190 boxed windows, no-room, guard-line clause | mixed | Theorem W (v4, Lean end to end); no-room leaf 47 s vs 850 s LP; v5 soundness bug found and fixed |
| 09-10 | A191 combined cascade | success | **first k0 node kills under the frozen verifier**: 17 of 64 S2 + 23 S3 nodes of l1_104 |
| 09-10 | A193/A194 high-k probes, descent | negative / theory | corners4 and k4_05 theory-limited (0 kills); Lemma CH: a non-simple corner forces nothing alone, everything jointly |
| 09-10 | A196–A200 Y0491, slot-pair pass, fastprop, corner seal, k5_16 quick | mixed | the PI's reading refuted with an explicit counterexample; SEAL / WEDGE / NO-SECOND [T] |
| 09-10 | A202/A203 fast30, CSP | mixed | stage 0 at 8–28 s a pad; the CSP on pieces; H forced on 34 pads |
| 09-10..11 | A204–A208 polyclip, clip tree, named split, basin clip, no-room leaves | running → done | Y0839 DEAD at the window pad in 526 s; Rule NS closes the fully named leaves |
| 09-12 | A209/A210/A211 k5 killer, corner cover, **coarse tree** | running | rule CC decisive at named nodes; an internal node 16–36 s against 277–296 s (8–9×) |
| 09-13 | A212 trump5 tree | running | the gate is false on the whole population at the root: the Trump-containing residue was discharged by A60/A83 |
| 09-14 | A213/A214/A215 integer polycore, C kernel, benchmark | DONE | bit-exact ×7–×29 per call; 16 ns a pair; **7.22× geometric mean on closed nodes** |
| 09-14 | A216 Lean readable layer | DONE | `Main.lean` + `Statements/` + `Open/` + `AUDIT.md` (build + audit exit 0, no sorry) |
| 09-14 | A217/A218/A219 torque probe, K0-COUNT, wall torque | DONE | [F] no torque sign rule; [T] PUSH, HOLD, CEIL, TWO-CONTACT, ONE-TILTED; [M] 0 of 883 FJ points are four-crowds |
| 09-14 | A220/A221 exact-first, lane cover | DONE | Lemma BUDGET; pocket-rooted cover **5.0×** on no-room nodes, 0 regressions |
| 09-14 | A222/A223 ring swap, two grains | DONE | **Lemma SWAP / CELLS [T]**; the sweep count fails; FLUSH [T]; CLICK-DOWN ⟺ STUCK-4 |
| 09-14..15 | A224/A226/A227 SNAP, ONE-FLUSH, EPS | DONE | Rule SNAP sound (0 kills measured); the 21-record survey; **Lemma EPS [T], Lean theorems** |
| 09-15 | A225/A228/A229/A230 page progress, segfault, shards, EPS branch | done | the crash was in the g1 pad; Lemma PAR; the NS-at-wedge split kills for free |
| 09-15 | A231–A237 realign, swap leaf, local lock, handedness, no-VV, ring capacity, pocket waste | mixed / negative | WALL-EXCESS [T]; swap leaf [T] (does not fire on the 11 cells); **extremal route [T], residue LOCKED-CROWD-FREE(n)**; TORQUE-ID an identity; NO-CLOSURE; TILT-MIN binds upward |
| 09-16 | **A238 k4 benchmark** | running → done | k4_11 cells die at the root by geometry in 13–16 s where A100's LP killed none; traction = closed extensions |
| 09-16 | A239/A240 rings below 4, CROSS | mixed / negative | WEDGED-SEAL [T] for every n and tilt (Lean); Lemma OPPOSE false (215 : 11) |
| 09-16 | **A241 row cascade** | running | the brief's cascade rule is UNSOUND (K1 climbs up); the (A)+(B) cascade; A55's kills PARAM-FAIL on every anchoring |
| 09-16 | A242 crowd root, A243 reach root (first use of the ids) | negative | the crowd route is sound and unaffordable; no leaf inequality valid over a summary cell |
| 09-16..17 | A244–A253 twelve-stuck, snap-down, construct-towards, perimeter walk, corner chase, family-stuck, ring pocket, centre disc, min tilt | mixed | STACK [T]; propagation rules n-general; n ≥ 4⌊s⌋ − 3 [T]; **θ_min(s) = 0 on [3.82, 4)** [F for tilt floors] |

## September 20–28 — the normal-ring chain for k0 (`k0_route.md` §13)

| date | id | status | outcome |
|---|---|---|---|
| 09-20..21 | A254/A255 peel, common sense | partial | PEEL-0 [T] (Lean `core_fits`); COMMON-SENSE false as a local lemma |
| 09-21 | A256/A257 trump5 passes, window | running | no trump5 node admits a contracted Trump image anywhere in the window; slabs do not stack |
| 09-21 | A258/A259/A260 normal ring, normal room, locked wall | done / running | **NORMAL-FORM [T]** (Lean); every free square of the normal pocket contains the centre: 8 + 1 = 9 < 11 (certificate chains) |
| 09-21..22 | A261–A266 box meeters, no-jam, open pairs, three lemmas, strip plug, last two | running | SAME-WALL [T]; COUNT + ROOM ⟹ n ≤ 9 per corner type (Lean); the miss-O test factors; STRIP₂ [F] as first stated |
| 09-23 | A267–A274 strip enclosure, terminal leaves, trump5 re-emit, **k5 lower slabs**, ring domain, strip jam, disc lemma, flat corner | mixed | WEDGE-FLOAT [T]; the last live k5 node dead in 10 s; k5_11/k5_16 NOT dead on G1 (290 boxes never emitted); DISC LEMMA false, DROP LEMMA certified outside the corner |
| 09-23..28 | A275–A281 k0 knowledge, flat X, float2, no-float2, nest, drop steep, corner cost | done / partial | the 1,103-line compilation (72 [T], 38 [F], 18 [C]); FLAT-X / CORNER [T] close the corner by hand; the NEST residual named |
| 09-22 | **external: T-037** | — | Kleddamag's s(11) > 31/8 verified on your record (2026-09-22) |
| 09-29 | **external: T-060** | — | Ahmed's global equality s(11) = T registered (V3/C3/S5 on your record; Lean formalisation reported 10-06) |

## October 2026 — the replay and the climb

| date | id | status | outcome |
|---|---|---|---|
| 10-06 | **external: T-112** | — | uniqueness of Trump's packing at T registered as a corollary of T-060 |
| 10-07 | A242 replay 31/8 | done | T-037 replayed row by row (12,028/12,028, 0 differ), independent spot-check PASS; adoption dry run: 99 nodes dead at once (`08`) |
| 10-07 | **A243 climb 17/19** | running | the toolkit generalised to any n; census 2,500 classes; n = 17 k = 16, 15 dead at the root; k = 14 67/68; k = 13 running (`06`) |
| 10-11 | A244 outreach series | this | the eight pieces and `ISSUES.md` |

Sources (https://github.com/Esummins/packing/blob/master/): `attempts/REGISTRY.md`; `writeup/03_lab_timeline.md` (phases I–VII with the stuck/unblock episodes);
`LOG.md`; your `packing/frontier/n-011.md` (T-037, T-060, T-112 dates).
