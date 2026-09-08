# Agenda 030, lane C: The transfer of the s(10) proof

Retained planning-lane report for
[X-021](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md),
written by a Fable sub-agent at maximum effort on 2026-09-08 under BC-291 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md).
The report is reproduced as delivered, with its own status labels; X-021 carries the
coordinator’s reading of it.
Nothing here is a registered round or a new bound.

## C — What the exact proof of s(10) = 3 + 1/√2 teaches for n = 11

Date 2026-09-08. Scope: Stromquist, Memo II (1984) / EJC 2003 Theorem 1 (n = 10),
Theorem 2 (n = 11 at 2 + 4/√5, repaired by exp-017), Theorem 3 (0/45° class), read
against the repository’s weighted fractional certificates (T-018/T-022), X-014 Lemmas
1–3, X-017/X-019 anchors, BC-255, and the 3.84 target.
Repository read-only; scripts and outputs live in `scratchpad/n10transfer/`. Python 3.11
standard library only (the project venv did not build: `uv-sync.log` ends in “No
download found for cpython-3.14.7”), so no repository code was run; every numerical
statement below is from the scratch scripts named in Section 2.

Conventions. Container S = [0, L]². Stromquist’s *box* = open square of side > 1 inside
S. The repository’s *core* = closed B-square (B = 9977/10000) at a net direction
strictly inside a packed unit square.
Both are devices for strict interiority: disjoint interiors of packed squares ⇒ pairwise
disjoint witnesses ⇒ no atom is counted twice.
A *measure* μ is a finite nonnegative atom measure on S; M = μ(S) its mass; a witness W
is *covered* if μ(W) ≥ 1. K4 = the two centreline reflections of S; D4 = all eight
symmetries. Angles mod π/2.

## 0. Findings in one page

1. **Theorem 2 is a conditional (anchored) certificate, not an unavoidable set.** With
   μ0 = the ten Figure-13 points, μ1 = the twelve (repaired) Figure-14 points, E0 =
   boxes avoiding μ0 with centre in R = [1, s/2] × [0, 1], and w = 3, it is exactly the
   instance (M0, w, M1) = (10, 3, 12) of Lemma B below: M1 < 10 + w. The two
   “structural” nodes (localization, A-forcing) are the *verification* of “E = K4·E0”
   and “μ1 ≥ 3 on E0”; the symmetry reduction is load-bearing: **no fixed K4-averaged
   measure built from the same atoms certifies** (Corollary A.2: mass/threshold ≥ 34/3 >
   11), so the anchored form is strictly stronger than any symmetric fixed measure on
   those atoms. This is X-019’s “asymmetric dots on a labelled case” already realised in
   1984/2003.
2. **Theorem 1 (n = 10) uses three mechanisms that a fixed measure cannot express**:
   exactly-one ownership at |P| = n; alternative-cover *transfer* ("B' is in the
   B-box"); and *existential* forced incidences (the H-box meets a segment at an unknown
   point) that feed a packing-dependent 13-point final cover.
   Only the first two have weighted analogues (Lemma C: atom transfer; Corollary 1a of
   X-014); the third is an H-097 “witness menu” object with no measure counterpart.
   Theorem 1 works at the exact optimum, where every fixed certificate must fail (τ* ≥ n
   there); that is the same regime as the 3.82 plateau.
3. **Stromquist’s n = 11 scheme cannot be pushed past 2 + 4/√5 by changing
   coordinates.** The Figure-13 localization is rigid: every sloping edge and the
   Lemma-4 distance condition equal (L/2 − 1)·√5/2, which is 1 exactly at L = 2 + 4/√5
   (Proposition D). Explicit exact rational interior escapes exist at L = 3.79, 3.80,
   3.82, 3.84 (margins 0.00013, 0.0029, 0.0083, 0.0141), centred at height ≈ 1.34,
   outside every wall rectangle; the 3.84 escape contains only A3 of the A-triple, so w
   collapses from 3 to 1 and the count 12 < 10 + w fails.
   What breaks first is node 2 (localization), immediately above 2 + 4/√5; the forcing
   lemmas would survive at 3.84 with moved coordinates (Lemma 4: f(0.92) = 0.868; Lemma
   6: apex 1.090), and the Figure-14 mesh needs one more point at 3.82/3.84, which
   raises M1 to 13 and needs w = 4.
4. **The “escaping-box route” is the two-branch split {no core in E} ∪ {a core in E0}**;
   branch 1 is a covering LP with a pose class exempted (a relaxation of the
   unconditional certificate), branch 2 is a class certificate with anchor weight w and
   coverage required only off the anchor’s forced region.
   It is not a new counting mechanism, but its symmetry reduction is a genuine gain over
   symmetric measures (Corollary A.2), and at 3.84 its first branch is the whole
   difficulty: a K4-symmetric measure of mass < 11 covering every core outside a thin
   class E. Nothing measured says whether that exists.
5. **What transfers as a proved lemma**: ownership of heavy atoms (weight > M − 11),
   atom transfer (Lemma C), and the corner-skeleton corollary: for T-018’s atom geometry
   a core holds at most one corner atom (distance 1.8146 > B√2 = 1.4110), so *any* valid
   measure at side L with those four corner atoms of weight w_c and mass M < 11 + w_c
   proves that every packing at L has four distinct squares each containing one corner
   atom — a global structural theorem obtainable from the LP alone, stronger than
   insertion saturation’s “meets the corner box” (H-126). Whether such a measure exists
   at 3.84 (M < 11.147) is unmeasured; the 3.85 run stood at 11.23 unconverged.
6. **Integral 11-point unavoidable sets** at 3.82 are not excluded by any known bound
   (τ*_B(3.82) ≤ 11 ⇒ τ*_unit(3.82) ≤ 11), but they would prove nothing by themselves;
   the count needs (|P|, swallowed) with |P| − swallowed < 10, i.e. 12 points and w = 3,
   and the localization that produces w is what dies.
   The decisive unmeasured quantity for both integral and fixed-measure routes at 3.84
   is the fractional value **at B = 1** (open squares, continuous angle): ν*_unit(3.84)
   \> 10 kills every 10-point set; > 11 kills every fixed measure and leaves only
   conditional/ownership routes.

## 1. Results proved

### 1.1 Reconstruction of the n = 10 proof (Theorem 1), step by step

Fix s = 3 + 1/√2 = 3.7071. Points A = (1, 1), B = (.97, s/2), and their D4 images give
ten points A, …, J (four corner points A, C, E, G; four wall-midpoint points B, D, F, H;
two inner points I, J on a centreline; Memo II has the transpose B = (s/2, .97), J =
(s/2, 1.4)).

| Step | Content | Lemma used | Kind |
| --- | --- | --- | --- |
| 1 | The ten points are unavoidable: S is partitioned into corner cells (Lemma 1), Lemma-4 quadrilaterals with (a, b) = (1/2 + √(1/8), .97) and Lemma-2 triangles | 1, 2, 4 | coverage verification |
| 2 | Ten boxes, ten points ⇒ each box contains exactly one point ("ownership") | — | counting (pigeonhole at equality) |
| 3 | Replacing B by B' = (.75, s − 1.96) keeps the set unavoidable (Lemma 4, (a, b) = (.96, .75)); hence B' ∈ B-box | 4 | **transfer** via ownership |
| 4 | Replacing A by A' = (1, s − 2.92) and A'' = (1.2, 1) keeps the 11-set unavoidable ⇒ A-box ∋ A' or A'' | 1, 2, 4 | transfer, disjunctive |
| 5 | Case A'' ∈ A-box: {A, A'', B', C..G, I, J, (2, 1)} is unavoidable (Lemma 3); all but (2, 1) are owned by other boxes ⇒ H-box ∋ (2, 1) | 3 | transfer with denial |
| 6 | Case A' ∈ A-box: A-box ⊇ segment A’A ⊇ [(1, .788), (1, 1)] by convexity; the H-box is denied that segment and B..G, I, J; Lemma 5 on the pentagon (1,0),(1,1),(2,1),(2.12,.9),(2.12,0) ⇒ H-box meets the segment from (2, 1) to (2.12, .9) | 5 | **structural: existential forced incidence** |
| 7 | By symmetry, eight “asterisks”, two in each of the B-, D-, F-, H-boxes; each within 1 of the centre and of its two neighbours | metric facts | structural |
| 8 | The thirteen points (8 asterisks, A, C, E, G, centre) are unavoidable (Lemma-2 mesh with all edges ≤ 1, which is what step 7 supplies); all but the centre are owned by the eight named boxes; I and J cannot both contain the centre | 2 | counting with a **packing-dependent** cover |

Counting steps: 2, 8 (and the denial bookkeeping in 5). Structural steps: the lemma
cells in 1 (which are geometric verifications of coverage rows), 6 and 7. Transfer steps
3–5 are the bridge: they convert ownership plus an alternative cover into forced
containments. Step 8 is a count with box-dependent thresholds (A, C, E, G: ≥ 1; B, D, F,
H: ≥ 2 each; I, J: ≥ 1 each; total ≥ 14 > 13), but the atoms (asterisks) are functions
of the packing, so it is not a fixed measure.
Memo II’s version replaces B by W = (s − 1.96, .75), A by (1, 1.2) and (.788, 1), I, J
by U = (1.4, s/2), V = (s − 1.4, s/2), and uses its Lemma 4 = the paper’s Lemma 5 with
the pentagon (.88, 0), (.88, .90), (1, 1), (2, 1), (2, 0); same mechanism, transposed.

Arithmetic of Lemmas 1–6 (checked in `lemmas.py`; Section 2 has the outputs):

- Lemma 4 table: f(1/2 + √(1/8)) = 0.97224 at 39.51° (paper .972, 39.5° ✓); f(.96) =
  0.76892 at 17.71° (paper .769, 17.7° ✓); **f(√(4/5)) = 0.914538 at 31.456°**, not .926
  at 24.1°: the paper’s 24.08° root has cos θ = 0.913 > a = 0.894 and violates the
  unsquared condition (1 − x)√(1 − x²) = (1 + x)(a − x), so it is extraneous — the
  transcription’s flagged erratum is confirmed, and the application b = .9 < .9145 is
  unaffected. Also f(.95) = 0.79815 < .8 (the exp-016 gap) and f(.92) = 0.86820 (needed
  at L = 3.84).
- Lemma 5: eq. (4) at tan θ = 1.2 gives x = 2.0071 > 2.004 ✓ (min_θ D(θ) = 2√2 − 2 =
  .8284 ✓); eq. (5) minimum x = 2.12559 at 52.60° ✓; the ratio (x − 2)/(1 − y) ≥ 1.6536 >
  1.2 on sin θ > .9 ✓ (paper: ≥ .6 + 1).
- Lemma 6: θ0 = ½ asin(5 − 2√5) = 15.9306° ✓, D(θ0) = √(4/5) ✓, cos + sin = √5 − 1 =
  1.236 > 1.12 ✓, apex-line height 1.12765 at θ0 and increasing ✓.
- Lemma 3 bottom rectangle of Figure 14: a + 2b = 2.694 ≤ 2√2 ✓ (still fine at 3.84:
  2.72).

### 1.2 Reconstruction of Theorem 2 (n = 11 at s = 2 + 4/√5) as an anchored certificate

The five nodes certified by exp-017 (with G' = (.79, 1.85)):

1. eleven boxes, ten Figure-13 points ⇒ some box avoids all ten;
2. every avoider has its centre in a K4-image of R = [1, s/2] × [0, 1] (18 covered
   cells: 4 Lemma-1 corners, 4 Lemma-4 side quadrilaterals with (a, b) = (√(4/5), 3/2 −
   s/4), 10 Lemma-2 triangles with edges 1, 1, √(4/5));
3. an avoider centred in R contains A1 = (1, .9), A2 = (s/2, .9) (Lemma 4 twice, b = .9
   < f(√(4/5)) = .9145) and A3 = (1/2 + s/4, 1.12) (Lemma 6);
4. the twelve points are unavoidable (26-face complex);
5. 3 + 10 > 12.

**Lemma B (anchored escape certificate).** Let 𝒲 be the admissible witnesses at side L
(boxes, or B-cores at net directions with the fold of Condition 1), G ≤ D4 a group of
container symmetries acting on 𝒲, n = 11. Suppose:

- μ0 is G-invariant with mass M0 < n, E ⊂ 𝒲 is G-invariant, and μ0(W) ≥ 1 for all W ∈ 𝒲
  ∖ E;
- E0 ⊂ E satisfies E = G·E0;
- μ1 is a measure (no symmetry required; for cores this means its coverage is checked on
  a quarter-turn net) and w ≥ 1 with μ1(W) ≥ 1 for all W ∈ 𝒲 and μ1(W) ≥ w for all W ∈
  E0;
- M1 < (n − 1) + w.

Then no packing of n unit squares exists in [0, L]².

*Proof.* Let W1, …, Wn be the pairwise disjoint witnesses of a packing and e = #{i : Wi
∈ E}. Then n − e ≤ Σ_{Wi ∉ E} μ0(Wi) ≤ Σ_i μ0(Wi) = μ0(⋃Wi) ≤ M0 < n, so e ≥ 1. Pick Wk
∈ E and g ∈ G with g⁻¹Wk ∈ E0. The witnesses g⁻¹Wi are pairwise disjoint and admissible,
and Σ_i μ1(g⁻¹Wi) ≥ w + (n − 1) > M1 ≥ μ1(⋃ g⁻¹Wi) = Σ_i μ1(g⁻¹Wi), a contradiction.
∎

Refinement B′ (BC-255’s obstacle).
Put I(E0) = ⋂_{W ∈ E0} W. Every witness other than the anchored one is disjoint from
I(E0), so μ1(W) ≥ 1 need only hold for W ∈ E0 ∪ {W : W ∩ I(E0) = ∅}; mass placed inside
I(E0) counts toward w and toward nothing else.
This is exactly the “ten other cores and nine points” reduction of the BC-255
assessment, with I(E0) ⊇ the diamond D.

**Theorem A.** Stromquist’s Theorem 2 (as certified in exp-017) is the instance of Lemma
B with 𝒲 = open boxes of side > 1, G = K4, μ0 = unit atoms on the ten Figure-13 points
(M0 = 10), E = {boxes avoiding μ0}, E0 = {W ∈ E : centre(W) ∈ R}, μ1 = unit atoms on the
twelve repaired Figure-14 points (M1 = 12), w = 3. Node 1 is “M0 < 11”; node 2 is “E =
K4·E0”; node 3 is “μ1 ≥ 3 on E0”; node 4 is “μ1 ≥ 1 on 𝒲”; node 5 is “12 < 10 + 3”.
*Proof.* Match the hypotheses; μ0 is K4-invariant because the ten points are, and E is
K4-invariant because μ0 is.
∎

**Corollary A.2 (the anchor is load-bearing).** Let ν = λ·P10 + Σ_{g ∈ K4} a_g · g(P12′)
with λ, a_g ≥ 0, threshold t = inf_{W ∈ 𝒲} ν(W), and a = Σ_g a_g. Then mass(ν)/t ≥ 34/3
\> 11 whenever the a_g are equal; in particular the K4-average of Stromquist’s data is
not a certificate. *Proof.* Two explicit boxes bound t. (i) The closed unit square
centred at (1.4739, .6913) tilted 30.30° avoids P10 and contains exactly 3 points of
P12′ and exactly 1 point of each other image (`symmetrization_witness.py`), so t ≤ 3a_id
\+ Σ_{g ≠ id} a_g = a + 2a_id = 1.5a for equal weights.
(ii) The corner square [δ, 1 + δ]² contains exactly one point of P10 and one of each
image, so t ≤ λ + a. If 10λ + 12a < 11t then 10λ + 12a < 11(λ + a) gives a < λ, and 10λ
\+ 12a < 16.5a gives λ < 0.45a; contradiction.
∎ (With unequal a_g the same argument gives t ≤ a + 2·min_g a_g ≤ 1.5a and the same
contradiction.)

So the K4 case split — “name the escaping box, move it to the bottom-left by a symmetry
of the whole packing” — is where Theorem 2 beats every symmetric fixed measure on its
own atoms. It is precisely X-019’s remark that asymmetric measures help on a labelled
case, and BC-255’s anchored reduction for H-036 is the same scheme with E0 = near-45°
P10-avoiders in R.

### 1.3 Ownership and transfer in the weighted setting

Setting: side L, shrink B, net satisfying Conditions 3–4; μ valid (Conditions 1, 5) with
mass M = 11 + ε, ε ≥ 0 (a certificate iff ε < 0). For a packing, Lemma 1 of X-014 gives
pairwise disjoint cores P1, …, P11 with μ(Pi) ≥ 1, hence μ(Pi) ≤ 1 + ε and μ(S ∖ ⋃Pi) ≤
ε.

**Lemma C′ (ownership; X-014 Corollary 1a restated).** Every atom of weight > ε lies in
exactly one core. If ε = 0 every atom lies in exactly one core and every core has mass
exactly 1.

**Lemma C (atom transfer).** Let μ′ = μ − w·δ_p + w·δ_{p′} be also valid at the same (L,
B, net) with w > ε, where p is an atom of μ of weight ≥ w. Then in every packing at side
L the core that contains p also contains p′. *Proof.* p has weight ≥ w > ε, so by C′ it
lies in exactly one core P. Validity of μ′ gives 1 ≤ μ′(P) = μ(P) − w + w·[p′ ∈ P] ≤ 1 +
ε − w + w·[p′ ∈ P], so [p′ ∈ P] = 1. ∎ This is Stromquist’s step 3 ("B′ is in the
B-box") with points replaced by atoms and the equality |P| = n replaced by w > ε; the
disjunctive step 4 is the same argument with μ′ = μ − w δ_p + w δ_{p′} + w δ_{p″}: if μ′
satisfies Condition 5 (its mass is irrelevant here), then 1 ≤ μ′(P) ≤ 1 + ε − w +
w([p′ ∈ P] + [p″ ∈ P]) forces p′ ∈ P or p″ ∈ P. The “denial” steps (5) are the statement
that other cores avoid P’s atoms, which is C′ again.

**Corollary C.2 (corner skeleton).** In T-018’s atom set the four heaviest atoms sit at
the orbit of (0.99769, 0.99769), weight 917/6250 = 0.14672, pairwise distance ≥ 1.8146 >
B√2 = 1.41096, so no core contains two of them.
Hence: *if a valid measure at side L (any L) contains four such corner atoms of weight
w_c each and has mass M < 11 + w_c, every packing at side L has four distinct squares
each containing one of the four corner atoms in its interior.* At L = 3.81 this is
vacuous (M < 11). At L = 3.84 it is a theorem if a measure with M < 11 + w_c exists
there — unmeasured (Section 4, S3). It is strictly sharper than insertion saturation’s
four blockers (X-019, H-126): the blocker must contain a point at distance ≈ 0.0033 from
(1, 1)·(L/3.81), not merely meet the open corner box.

**Hybrid Lemma H (ownership-conditioned certificate).** Let μ be valid at (L, B, net)
with mass 11 + ε and let H′ ⊂ {atoms of weight > ε} be a chosen skeleton.
A *pattern* is a map σ: H′ → {1, …, 11} such that each fibre S_i = σ⁻¹(i) lies in some
admissible core; two patterns are equivalent under relabelling.
Suppose that for every pattern σ there is a measure μ_σ (any symmetry; quarter-turn net)
of mass M_σ < 11 such that μ_σ(P) ≥ 1 for every admissible core P that, for some i,
contains S_i, contains no atom of H′ ∖ S_i, and is disjoint from conv(S_j) for all j ≠
i. Then no packing of 11 unit squares exists at side L. *Proof.* A packing’s cores are
disjoint convex sets; by C′ each atom of H′ lies in exactly one core, defining σ; P_i ⊇
S_i, P_i ∩ (H′ ∖ S_i) = ∅, and P_i ∩ P_j = ∅ with P_j ⊇ conv(S_j). So every P_i is in
μ_σ’s covered family and 11 ≤ Σ μ_σ(P_i) ≤ M_σ < 11. ∎

What is new relative to X-014: (a) Lemma C lets ownership propagate without enumerating
patterns (Stromquist’s steps 3–5 mechanised: each single-atom move that keeps validity
is a forced containment); (b) the skeleton H′ can be tiny — with H′ = the four corner
atoms and the centre atom (weights 0.147 and 0.139; corner-to-centre distance 1.283 <
1.411, so the centre may share a core with one corner) there are exactly two patterns up
to D4, and each is an anchored four-plus-seven frame with *pinned* anchors; (c) at ε = 0
(the plateau) H′ may be taken as the whole atom set and the pattern is an exact cover of
the atoms by eleven mass-1 cells — a decidable finite question whose infeasibility
proves s(11) ≥ L without a mass-below-11 certificate ("plateau certificate"). Is it a
genuinely new mechanism?
It is the union of Corollary 1a with Stromquist’s transfer and anchoring; the measure
μ_σ per pattern is a conditional certificate of X-014 Lemma 2 type with several boxes at
once. The new content is the *source of the anchors*: the near-certificate’s own heavy
atoms, at any side where M < 11 + w.

### 1.4 Rigidity of the Figure-13 localization

**Proposition D.** (i) For Stromquist’s Figure-13 coordinates at side L — P0 = (1, 1),
P1 = (L/2, 1), M0 = (3/2 − L/4, L/2), M1 = (1/2 + L/4, L/2) and K4 images — every
sloping Lemma-2 edge and the Lemma-4 distance condition |(a, b) − (0, 1)| for the side
cells equal (L/2 − 1)·√5/2. They satisfy the lemma hypotheses (≤ 1) iff L ≤ 2 + 4/√5.
(ii) For L ∈ {379/100, 19/5, 191/50, 96/25} there is an exact rational closed unit
square inside S, centred at height 1.34–1.35 (in no wall rectangle) and tilted
24.8°–28.1°, whose distance margin to every one of the ten points is positive;
explicitly at L = 96/25: centre (73/50, 67/50), tan(ψ/2) = 49/200, least margin
14979/1060025 = 0.01413 at P1, wall clearance 0.6655; hence every open box of side <
1.02826 with that centre and orientation avoids all ten points.
At L = 191/50: centre (291/200, 27/20), tan(ψ/2) = 11/50, least margin 1087/131050 =
0.00830. At 19/5 and 379/100 the margins are 0.00294 and 0.00013. (iii) The 3.84 escape
of (ii) contains A3 but neither A1 = (1, .9) nor A2 = (1.92, .9), so for this E0 the
best anchor weight is w = 1.

*Proof of (i).* |M0 − P0|² = (L/4 − 1/2)² + (L/2 − 1)² = (L/2 − 1)²(1/4 + 1) and the
side cell has local (a, b) = (L/2 − 1, 3/2 − L/4) with |(a, b) − (0, 1)|² = (L/2 − 1)² +
(L/4 − 1/2)², the same number; it is ≤ 1 iff L/2 − 1 ≤ 2/√5. (ii) and (iii) are exact
rational computations (`interior_escape.py`, `interior_escape_search.py`,
`symmetrization_witness.py`). ∎

The general obstruction behind (i): the region just above the top edge of the
exceptional rectangle must be covered by interior cells, and all of Stromquist’s lemmas
except Lemma 2 need a container wall, so those cells are triangles with vertices in P
and edges ≤ 1; a triangle on the edge P0P1 (length L/2 − 1) has its apex within the lens
of height √(1 − (L/4 − 1/2)²), which is 0.894 = L/2 − 1 exactly at 2 + 4/√5 and 0.888 <
0.92 at 3.84. Any repair puts an eleventh point below the middle row, and eleven points
force no escape.

**Consequence for 3(b).** The sharpest side at which Stromquist’s scheme (formula P10,
K4, w = 3, twelve points) can work is exactly 2 + 4/√5 = 3.7889; node 2 breaks first, at
rate √5/4 per unit side in edge length.
The forcing lemmas survive at 3.84 with moved coordinates (Lemma 4 at a = 0.92: f =
0.8682, so A1 could sit at (1, .86); Lemma 6 at a = 0.92: θ0 = 11.11°, apex-line height
≥ 1.0903, so A3 at (1.46, 1.09)), i.e. w = 3 is available for a *narrow* E0 — but only
if localization confines the escape to such an E0, which it cannot with ten points.
The Figure-14 mesh with the same formulas has edge D–I = 1.018 at 3.82 and D–I = 1.047,
G′–F = 1.012 at 3.84 (and the F_G Lemma-4 cell’s distance condition fails, 1.024), so it
needs a thirteenth point, which needs w = 4.

### 1.5 The endpoint: enlarged boxes versus shrunken cores

Stromquist proves the closed endpoint s(10) = 3 + 1/√2 by making the packed objects open
and larger than 1; the repository proves open bounds with cores smaller than 1 and
reaches endpoints by dilation (T-022). Trump’s packing at U illustrates the necessity:
with closed unit squares the Figure-13 formulas at L = U give *no* escape (each of the
eleven squares contains ≥ 1 of the ten points; squares 4 and 5 share T0 = (1, U − 1) on
their common boundary), so the pigeonhole fails at the endpoint for closed squares.
Both devices remove boundary sharing; the box device is free in angle because the hand
lemmas are continuous in θ, the core device pays B(1 + D) < 1 for a finite net.
That angular price is the one place where Stromquist’s hand verification is still ahead
of the sweep (Section 4, S1).

## 2. Numerical checks (scripts in `scratchpad/n10transfer/`)

All scripts are standard-library Python 3.11; outputs were pasted from the runs.

| Script | What it checks | Key output |
| --- | --- | --- |
| `lemmas.py` | Lemma 4 f(a) by 1-D minimisation and the cubic’s roots with the unsquared filter; Lemma 5 eqs (4)–(5) and the ratio bound; Lemma 6 constants at a = √(4/5) and a = 0.92; Lemma 3 at 3.79/3.82/3.84 | f(.8536) = .97224 @39.51°; **f(√.8) = .914538 @31.456°** (paper’s 24.08° root has cos θ > a, extraneous); f(.96) = .76892 @17.71°; f(.95) = .79815; f(.92) = .86820; f(.90) = .90523. Lemma 5: x = 2.0071 at tan θ = 1.2; min x = 2.12559 @52.60°; ratio ≥ 1.6536. Lemma 6: θ0 = 15.9306°, apex ≥ 1.12765; at a = .92: θ0 = 11.107°, cos + sin = 1.1739, apex ≥ 1.0903 |
| `fig13_fig14_scaling.py` | Figure-13 edges / Lemma-4 distance vs L; Figure-14 mesh edges and cell parameters at 3.789, 3.82, 3.84 | edge = (L/2 − 1)√5/2: 1.0000 (3.7889), 1.0174 (3.82), 1.0286 (3.84); strip bound 2√(1 − a²) = .894/.829/.784 vs spacing a = .894/.910/.920; Figure 14: D–I 1.018 at 3.82; D–I 1.047, G′–F 1.012, F_G cell distance² 1.024 at 3.84 |
| `interior_escape.py`, `interior_escape_search.py` | exact rational escapes from the ten Figure-13 points at 3.79–3.84 with margins and wall clearance | see Proposition D(ii); box sides up to 1.00026 / 1.00588 / 1.01659 / 1.02826 |
| `two_tier_check.py` | 400k random closed unit squares at s = 2 + 4/√5: coverage by 2·P10 + P12′ | minimum sampled coverage **1** (escapes in the top rectangles contain only E), 112 P10-escapes with P12′ counts {1: 89, 3: 23}; exp-016 witness: (P10, P12) = (2, 0) with G = .8 and (2, 1) with G′ = .79 |
| `symmetrization_witness.py` | explicit boxes for Corollary A.2; A-triple content of the 3.84 escape | BL avoider at (1.4739, .6913), 30.30°: counts (3, 1, 1, 1) over the four K4 images; corner box: (1, 1, 1, 1) and one P10 point; 3.84 escape contains (A1, A2, A3) = (F, F, T) |
| `trump_at_U.py` | Trump’s exact pose (u = 0.36577, U = 3.877083590) against P10/P12′/9-grid formulas at L = U | every closed square hits ≥ 1 P10 point (sum 14: no escape for closed squares, T0 shared by squares 4, 5); 2·P10 + P12′ total 42; corner boxes met by squares {0}, {1}, {3}, {2, 10} |
| `skeleton.py` | T-018 heavy-atom skeleton | 1121 atoms, 149 D4-orbits; > 0.005: 649 atoms/9.969 mass; > 0.01: 289/7.020; > 0.02: 93/4.282; > 0.05: 29/2.265; > 0.1: 5/0.726 (four corners 0.14672 + centre 0.13950); corner pair distance 1.8146 > B√2 = 1.4110; corner–centre 1.283; 8.964 of 10.864 mass within 1 of a wall; folded rows y ≈ 0.99–1.0 carry 3.94 |

Rung masses (from the frozen certificates): 3.78 → 10.5894 (373 atoms), 3.80 → 10.8478
(425), 3.81 → 10.8637 (1121), 3.82 → 11.0000 restricted (not retained).
The slope is erratic (13/unit, 1.6/unit, 13.6/unit), so the “shrink tax” B ↦ τ* cannot
be read off; it must be measured (S1).

## 3. Obstructions: what does not transfer, and why

| n = 10 idea | Transfers? | Why / what replaces it |
| --- | --- | --- |
| Exactly-one ownership ( | P | = n, unit weights) |
| Alternative covers ⇒ forced containment (steps 3–5) | Yes | Lemma C (atom transfer), provided the moved atom has weight w > ε; it needs a second *valid* measure, i.e. a second sweep per move |
| Forced incidence with a segment at an unknown point (Lemma 5, asterisks) | No | An existential witness ("the H-box meets this segment somewhere"), not a mass statement; a segment measure gives only length-proportional mass (H-098). It is H-097’s witness-menu object. No fixed or conditional measure expresses it |
| Packing-dependent final cover (13 points, step 8) | No, as a measure | It is the adaptive branch of Corollary 1a: the cover is chosen after the pattern is known. Only a case tree can host it |
| Open boxes of side > 1 for the endpoint | Replaced | T-022’s dilation limit; the box device is free in angle (hand lemmas continuous in θ), the core device pays B(1 + D) < 1 |
| K4 symmetry reduction (Theorem 2, “WLOG bottom-left”) | Yes, as Lemma B | Must act on the whole packing; the anchored branch’s measure is asymmetric and needs a quarter-turn net (X-014 Lemma 2’s remark) |
| Figure-13 three-row localization with ten points | No | Rigid at 2 + 4/√5 (Proposition D); eleven points force no escape; interior cells must be Lemma-2 triangles |
| A-forcing (Lemmas 4, 6) | Yes, with moved coordinates | Survives at 3.84 for a narrow E0 (f(.92) = .868, apex 1.090), but E0 must be produced by a localization that no longer exists |
| Integer weights, threshold 1 | Generalised | Theorem 2 already uses thresholds (3 on E0); Theorem 3 is a class certificate on {0°, 45°}; the LP is the natural home |

Specific answers to the task’s questions.

**3(a) Integral unavoidable sets of 11 points at 3.82 or 3.84.** Not excluded by
anything known: the grid-site run at 3.82 converged at exactly 11 on B-cores, so
τ*_B(3.82) ≤ 11 and hence τ*_unit(3.82) ≤ 11 (a B-cover is a unit cover).
But (i) an 11-point set proves nothing by pigeonhole (11 boxes, 11 points), and the
ownership route it would open is Theorem 1’s, whose final step is packing-dependent;
(ii) the integral gap seen at 3.789 — the best known integral set there has 12 points
(Figure 14) against τ*_unit(3.789) ≤ τ*_B(3.81) = 10.864 by monotonicity — makes 11
points at 3.82 implausible though not refutable here; (iii) the count that Stromquist
actually uses needs |P1| − (swallowed) ≤ 9, i.e. twelve points with w = 3 or thirteen
with w = 4, and the swallowing is what dies (Proposition D). The only lower bound on
integral sets available is the trivial one, ≥ 10, from the 10-packing; a proof that 10
points never suffice at 3.84 is equivalent to ν*_box(3.84) > 10 (a depth-≤-1 family of
unit squares of weight > 10), and that 11 never suffice to ν* > 11 — both unmeasured
(S6). Note the direction of the shrink: ν*_B ≥ ν*_unit and τ*_unit ≤ τ*_B, so exp-060’s
ν*_B(3.82) ≥ 9.908 says nothing about unit-square piercing.

**3(b) The escaping-box route at 3.84.** By Theorem A and Lemma B it is the two-branch
split {no core in E} ∪ {a core in E0}. Branch 1 needs a K4-symmetric measure of mass <
11 that covers every admissible core outside E; branch 2 needs (μ1, w) with M1 < 10 + w,
coverage required only off I(E0). Stromquist’s specific instance stops at 2 + 4/√5
because branch 1 with E = “P10-avoiders” and localization to four rectangles is rigid
there. At 3.84 the route is only as good as branch 1’s LP — an unconditional covering
program with a pose class exempted — and no measure of mass < 11 is known at 3.84 even
with a class exempted.
The gain available is quantified by Corollary A.2: the anchored form beats symmetric
measures by the asymmetry of μ1, worth 1/3 of a unit of mass at 3.789 (34/3 versus
10.667). Whether a thin E at 3.84 lowers M0 below 11 is the measurement S4 proposes;
nothing in the record predicts it.

**3(c) The ownership route at the 3.82 plateau.** With M = 11 exactly (ε = 0), C′ says
every atom is owned and every core has mass exactly 1: the packing’s eleven cores are
eleven event cells of mass exactly 1 partitioning the atom set, with interior-disjoint
enclosing unit squares.
The case tree is an exact cover: rows = tight cells (mass = 1) at the 181 directions,
columns = atoms (≈ 6600–24000 sites in the 3.82 runs), plus the geometric compatibility
(disjointness of enclosing unit squares, checked by SAT on the two angle-cell
endpoints).
The heavy-atom skeleton of T-018 suggests the branching: four corner atoms in
four distinct cores, the centre atom with one of them or a fifth, then the 33/500 orbit
near (0.61, 0.995) and the 513/8000 orbit near (0.995, 1.82) — the near-wall row y ≈
0.99 carries 3.9 of the mass, so roughly four cores are wall cores.
Cost: the sweep already fills the per-direction mass grid (T-018’s 567 M cells sweep in
about a minute single-threaded), so a tight-cell census is a readout; the exact cover’s
size is the census count, unknown (X-014 measurement 3). A cheaper prior question (S2,
step 0): the exactly-11.000000 plateau on two site sets is consistent with the n = 21
artefact mechanism — eleven B-cores of Trump’s shape scaled to 3.82 overlap only in
strips of width ≈ 0.0124 (0.9977 − 3.82/3.877), which a grid of pitch ≈ 0.047 misses —
in which case the plateau is a site artefact, τ*_B(3.82) may be well below 11, and the
exact-cover tree is moot.

**4. Ceilings for Stromquist-style methods, in the spirit of the ceiling theorem.**
Write τ*_unit(L) for the fractional covering value with open unit squares at all angles
(no shrink, no net) and L_τ = sup{L : τ*_unit(L) < 11} ≤ s(11).
- Pure point sets of ≤ 10 points (pigeonhole alone): ceiling sup{L : τ_box(L) ≤ 10}; the
  record suggests it is below 3.789, where twelve points and an anchor were already
  needed.
- Fixed weighted certificates verified by hand lemmas (integer or rational weights, B =
  1, continuous θ): ceiling L_τ, the same quantity that bounds the repository’s method
  but without the shrink and net loss: the instrument’s cap is min(L_τ(B), U·B·max(cos δ
  \+ sin δ)) = min(·, 3.8690), and L_τ(B) ≤ L_τ.
- Anchored/conditional certificates (Theorem 2 type, Lemma B; X-014 Lemma 2; X-017/X-019
  anchors): no ceiling below s(11) in principle, since each branch is a covering program
  on a restricted family and finitely many branches exhaust the packings; the cost is
  the branch design. Corollary A.2 shows the gain over symmetric measures is real.
- Adaptive/ownership arguments (Theorem 1 type; Lemma H at ε = 0): these are the only
  ones that work on a plateau τ* = 11 exactly, and at the exact optimum; their ceiling
  is s(11) itself, at the price of an exact-cover tree whose size is unmeasured.
  The hybrid of Lemma H is not a fourth counting principle; it is the weighted form of
  Stromquist’s ownership plus transfer, with anchors supplied by the near-certificate’s
  heavy atoms. Its genuinely new consequence is Corollary C.2: a global four-corner
  containment theorem at any side where a valid measure with mass < 11 + 0.147 exists.

## 4. Proposed research sessions (each 2–4 h; S1, S3, S4, S6 are mutually independent)

All need the project venv (`uv sync` failed here on the 3.14.7 download) and the
retained instruments; none needs a new soundness surface except where noted.
Headroom mechanism = what the session buys toward a global exclusion at 96/25.

**S1 — Shrink tax at 3.82 (B → 1 by net refinement).** Question: does the restricted
covering value at 191/50 fall below 11 when the net has 1800 directions and B =
99977/100000 (check B(1 + D) < 1 with D ≈ 2.3·10⁻⁴)? Entry: T-018 atoms scaled by
382/381 as the seed site set; the column generator with `direction_steps` = 1800; pilot
first at 600 directions to time the row loop (the 181-direction sweep took ~1 min in
`minimal_verify.py`, so verification scales to ~10 min).
Instrument: `sqpack.fractional` column generation + exact sweep.
Falsifier: converged restricted value ≥ 11 at 1800 directions on both the grid and the
seeded site set. Exit: a frozen certificate at 3.82 (new bound, retention gate as usual)
or the measured tax Δτ*/Δ(1 − B) at 3.82. Buys for 3.84: if the tax is of order 0.1 the
ladder’s plateau is the instrument’s, not the geometry’s, and 3.84 may fall to the plain
certificate with a finer net; if the tax is ≈ 0 the plateau is geometric and only
S3/S4/S2 routes remain.
Hours: 3–4.

**S2 — The 3.82 plateau: artefact test, then the plateau certificate (Lemma H at ε =
0).** Step 0 (30 min): regenerate the grid site set at the tool’s default density at
191/50 and test whether the eleven B-cores at Trump’s centres and angle scaled by
382/387.7 (shifted inward by ≤ 0.006 to fit) overlap only in site-free regions; if so
the exactly-11 value is the n = 21 artefact and the session switches to adding sites in
those strips and re-running (likely a certificate below 11). Otherwise: re-run the grid
LP to convergence at exactly 11.000000, sweep-verify the measure (mass exactly 11), read
the per-direction census of cells with mass exactly 1, and run an exact cover
(atom-based branching: corner atoms first) over tight cells with pairwise
interior-disjointness of enclosing unit squares (angle-cell endpoints, SAT). Falsifier:
tight-cell census above 10⁶ with no clustering (then the tree is not a 4 h object;
record the census). Exit: infeasible cover ⇒ s(11) ≥ 3.82 as a theorem via Corollary 1a;
feasible skeleton ⇒ eleven cells to test as an actual packing (a packing would be a new
record; a non-packing shows the plateau is an integrality artefact of the core
relaxation). Hours: 4. Depends on: nothing; parallel with all others.

**S3 — Corner-skeleton ownership at 96/25 (Corollary C.2).** Question: is there a valid
measure at 3.84 with the four corner atoms at (0.99769·384/381, ·) of weight ≥ 3/20 (and
the centre atom ≥ 1/8) and total mass < 11 + 3/20? Entry: the column generator with
lower bounds on those five atom weights (an LP bound change, no geometry change); seed
with T-018 scaled. Instrument: column generation + exact sweep on the eighth-turn net
(the measure stays D4-symmetric).
Falsifier: converged mass ≥ 11.15 with the forced skeleton.
Exit: the theorem “every packing at 3.84 has four distinct squares containing the four
corner atoms” (a proved structural restriction with all alternatives closed), with the
price M(forced) − M(free) recorded; or the obstruction.
Buys for 3.84: pinned anchors for BC-287/H-111 (four anchored cores with I_i ∋ corner
atom), and the input to Lemma H’s two-pattern case split (centre atom with a corner core
or not). Hours: 3–4.

**S4 — Escape-tolerant certificate at 96/25 (Lemma B, branch 1).** Question: for E =
K4-orbit of E0 = {cores with centre in [1, L/2] × [0, h] that avoid the two bottom
corner atoms and the (L/2, 1)-orbit atom}, h ∈ {1, 1.1, 1.2}, what is the least mass
M0(E) of a K4-symmetric measure covering every admissible core outside E?
Implementation: E is a filter on event cells (centre in a rectangle and atom mask
excluding three named atoms) — skip those cells in `sweep.minimum_covered_mass` and in
the row generator’s separation; no non-convex domain is needed.
Then branch 2: for the best E, solve max (w − M1) over asymmetric μ1 on a quarter-turn
net with μ1 ≥ 1 off I(E0) and ≥ w on E0, and test M1 < 10 + w. Falsifier: M0(E) ≥ 11 for
all h in the menu. Exit: a two-branch certificate at 3.84 (new bound), or the trade-off
curve h ↦ (M0(E), w(E0)) showing which pose classes carry the binding rows.
Hours: 4. New soundness surface: the cell filter (small; mutation-test it against the
unfiltered sweep at 3.81).

**S5 — Transfer-lemma automation (Lemma C).** Given a valid measure (T-018 at 3.81 as a
dry run; S3’s measure at 3.84 as the target), for each heavy atom p compute the set of
displacements d such that μ − w δ_p + w δ_{p+d} stays valid, by an incremental sweep
(only cells whose mask changes).
Deliverable: forced-containment regions R(p) that the owning core must contain, which
enlarge the anchors of S3/S4. Falsifier: R(p) = {p} for every heavy p (no slack to move
atoms). Hours: 3. Depends on S3 for a 3.84 measure; the dry run does not.

**S6 — ν* at B = 1, the decisive quantity for integral routes.** Run the depth-≤-1
family builder (`sqpack.fractional.cutting`/`ceiling`) with B = 1 and open squares at
3.84 (Condition 4 is not needed for a packing lower bound; any finite direction set is
admissible). Falsifier: total weight ≤ 10 after 2 h. Exit: ν*_unit(3.84) > 10 ⇒ no
10-point unavoidable set exists at 3.84 (kills the pure pigeonhole dream); > 11 ⇒ no
fixed measure at B = 1 exists at 3.84 (the B = 1 ceiling theorem for the fractional
method there), so only conditional/ownership routes remain — which is the decision the
3.84 plan needs. Hours: 3. Parallel with all.

Dependencies: S3 → S5 (target run only).
Everything else is independent.
If only three run, take S1, S3, S6: they decide, respectively, whether the plateau is
the instrument’s, whether the corner anchors are free at 3.84, and whether any fixed
measure can exist at 3.84.

## 5. Open questions ranked by expected value

1. Is the exactly-11.000000 plateau at 3.82 a site artefact (Trump-shaped B-cores
   overlapping in site-free strips)?
   Cheapest question in this report (S2 step 0), and if yes it changes the ladder’s
   status at 3.82 immediately.
2. τ*_unit(3.84) versus 11 at B = 1 (S6 from below, S1 from above): decides whether the
   3.84 objective is a fixed-measure problem or a conditional one.
3. Does a valid measure at 3.84 with mass < 11 + 0.147 exist (S3)? If yes, the
   four-corner containment theorem is free and BC-285/H-126’s missing premise is
   supplied by the LP.
4. The trade-off E ↦ (M0(E), w(E0)) at 3.84 (S4): the only quantitative handle on the
   escaping-box route above 2 + 4/√5.
5. The tight-cell census at the top of the ladder (X-014 measurement 3; S2): the size of
   the ownership tree, unknown by orders of magnitude.
6. A general lower bound on |P| for point sets whose escapes localize to wall rectangles
   at side L (the general form of Proposition D): would settle that no ten-point scheme
   of any row structure exists above 2 + 4/√5; the lens argument covers the three-row K4
   family only.
7. Whether Theorem 1’s existential incidences (Lemma 5 type) admit a
   *conditional-measure* surrogate: given the ownership pattern, the H-core’s admissible
   family is restricted to cores disjoint from the other cores’ convex hulls; the LP on
   that family may force mass that the segment statement forced by hand (this is Lemma
   H’s per-pattern measure).

Standards note. Proved: Lemma B, B′, Theorem A (given exp-017’s certified nodes),
Corollary A.2 (given the two explicit witness boxes, checked numerically with margins ≥
0.05 — an exact rational replay is a ten-line addition), Lemmas C′, C, H, Corollary C.2
(premise conditional), Proposition D(i) exactly, D(ii)–(iii) by exact rational
arithmetic. Numerically checked: the lemma tables, the sampling of the two-tier measure,
Trump’s counts, the skeleton statistics.
Conjectured: the plateau-artefact mechanism, the shrink-tax magnitude.
Open: every quantity in Section 5.

## Appendix: scripts and outputs as run

Retained verbatim from the lane’s working directory on 2026-09-08. Scripts that import
`sqpack` were run through the project environment; the rest are standard-library Python.
None has been promoted to `devtools/`; the first lane that reuses one owns that
promotion.

### `fig13_fig14_scaling.py`

```text
"""Figure 13 / Figure 14 geometry evaluated with Stromquist's coordinate formulas at other sides."""
import math
S0 = 2 + 4/math.sqrt(5)

def dist(p, q): return math.hypot(p[0]-q[0], p[1]-q[1])

def fig13(L):
    U = 1.5 - L/4; V = 0.5 + L/4; C = L/2
    P = {"P0": (1,1), "P1": (C,1), "P2": (L-1,1), "M0": (U,C), "M1": (V,C), "M2": (L-V,C), "M3": (L-U,C),
         "T0": (1,L-1), "T1": (C,L-1), "T2": (L-1,L-1)}
    tris = [("M0","P0","M1"),("P0","P1","M1"),("M1","P1","M2"),("P1","P2","M2"),("M2","P2","M3"),
            ("T0","M0","M1"),("T0","M1","T1"),("T1","M1","M2"),("T1","M2","T2"),("T2","M2","M3")]
    maxedge = 0
    for t in tris:
        for i in range(3):
            maxedge = max(maxedge, dist(P[t[i]], P[t[(i+1)%3]]))
    # Lemma 4 side cell: origin (0,1), u-axis vertical, v-axis horizontal: a = C-1, b = U; distance of (a,b) to (0,1)
    a, b = C-1, U
    d = math.hypot(a, b-1)
    return maxedge, a, b, d

print("Figure 13 with Stromquist's formulas:")
for L in [S0, 3.79, 3.80, 3.81, 3.82, 3.84, 3.877]:
    me, a, b, d = fig13(L)
    print(f"L={L:.6f}: max Lemma-2 edge = {me:.6f}; Lemma-4 side cell a={a:.4f}, b={b:.4f}, |(a,b)-(0,1)|={d:.6f}; both need <= 1 -> {'OK' if me<=1+1e-12 and d<=1+1e-12 else 'FAIL'}")
print("closed form: edge = (L/2-1)*sqrt(5)/2; equals 1 iff L = 2+4/sqrt5 =", S0)
print("strip argument: max horizontal offset for a cross edge <= 1 between rows L/2-1 apart:")
for L in [S0, 3.82, 3.84]:
    a = L/2-1
    print(f"  L={L:.5f}: sqrt(1-a^2) = {math.sqrt(max(0,1-a*a)):.5f}; bottom-row spacing a = {a:.5f}; need spacing <= 2*sqrt(1-a^2) = {2*math.sqrt(max(0,1-a*a)):.5f}")

def fig14(L, gx=0.79):
    C = L/2; V = 0.5 + L/4
    P = {"A1": (1,.9), "A2": (C,.9), "A3": (V,1.12), "B": (L-1,1), "C": (L-.9,C), "D": (L-1,L-1), "E": (C,L-.9),
         "F": (1,L-1), "G": (gx,1.85), "H": (1.5,2.1), "I": (2.1,2.1), "J": (2.1,1.5)}
    tris = [("F","E","H"),("E","I","H"),("E","D","I"),("D","C","I"),("C","J","I"),("I","J","H"),("C","B","J"),
            ("B","A2","J"),("A2","A3","J"),("A3","H","J"),("A3","G","H"),("G","F","H"),("G","A3","A1")]
    bad = []
    for t in tris:
        for i in range(3):
            e = dist(P[t[i]], P[t[(i+1)%3]])
            if e > 1: bad.append((t[i], t[(i+1)%3], round(e,4)))
    # Lemma 4 cells (a, b): A2_B etc use a = C-1 (=L/2-1), b = .9 ; F_G: a = L-2.85, b = gx ; G_A1: a = .95, b = gx
    cells = {"A2_B/B_C/C_D/D_E/E_F": (C-1, .9), "F_G": (L-2.85, gx), "G_A1": (.95, gx)}
    return bad, cells

print()
print("Figure 14 (repaired G'=(.79,1.85)) with the formulas at other sides; central-mesh edges > 1 and Lemma 4 cell parameters:")
for L in [S0, 3.82, 3.84]:
    bad, cells = fig14(L)
    print(f"L={L:.6f}: long edges: {bad}")
    for k, (a, b) in cells.items():
        print(f"   Lemma4 cell {k}: a={a:.5f}, b={b:.5f}, |(a,b)-(0,1)|^2={a*a+(b-1)**2:.5f}")
```

### `interior_escape.py`

```text
"""Exact rational witnesses: at L = 3.82 and L = 3.84 a unit square centred in the triangle P0 P1 M1 of
Stromquist's Figure-13 formulas avoids all ten P10 points (strictly) and sits inside the container,
so the escape localisation to the four wall rectangles fails there."""
from fractions import Fraction as F
import math

def p10(L):
    C = L/2; U = F(3,2) - L/4; V = F(1,2) + L/4
    return {"P0":(F(1),F(1)),"P1":(C,F(1)),"P2":(L-1,F(1)),"M0":(U,C),"M1":(V,C),"M2":(L-V,C),"M3":(L-U,C),
            "T0":(F(1),L-1),"T1":(C,L-1),"T2":(L-1,L-1)}

def witness(L, t, cy):
    """t = tan(psi/2) rational; centre x = midpoint of P0P1, centre y given; returns margins."""
    c = (1-t*t)/(1+t*t); s = 2*t/(1+t*t)
    assert c*c + s*s == 1
    P = p10(L)
    cx = (1 + L/2)/2
    margins = {}
    for k,(x,y) in P.items():
        dx, dy = x-cx, y-cy
        u = c*dx + s*dy; v = -s*dx + c*dy
        margins[k] = max(abs(u), abs(v)) - F(1,2)   # > 0 means the closed unit square misses the point
    h = (abs(c)+abs(s))/2
    wall = min(cx-h, L-h-cx, cy-h, L-h-cy)          # > 0 means the closed unit square is strictly inside
    return cx, cy, c, s, margins, wall

for L, t, cy in [(F(96,25), F(4,17), F(67,50)), (F(191,50), F(4,17), F(133,100)), (F(96,25), F(1,4), F(27,20))]:
    cx, cy, c, s, m, wall = witness(L, t, cy)
    psi = math.degrees(2*math.atan(float(t)))
    worst = min(m.items(), key=lambda kv: kv[1])
    print(f"L={L}={float(L)}: centre=({cx},{cy})=({float(cx):.4f},{float(cy):.4f}), tan(psi/2)={t}, psi={psi:.3f} deg")
    print("   point margins (max(|u|,|v|)-1/2):", {k: round(float(v),5) for k,v in m.items()})
    print(f"   worst point {worst[0]} margin {worst[1]} = {float(worst[1]):.6f}; wall clearance {float(wall):.6f}; centre in a wall rectangle? {cy<=1 or cy>=L-1}")
    ok = all(v > 0 for v in m.values()) and wall > 0
    print("   ESCAPE CERTIFIED (exact rationals):", ok, "-> every open box of side < 1 + 2*min(margin, clearance) =", float(1+2*min(worst[1], wall)), "avoids P10 and fits")
```

### `interior_escape_search.py`

```text
from fractions import Fraction as F
import math
from interior_escape import witness
for L in [F(191,50), F(96,25), F(38,10), F(379,100)]:
    best=None
    for k in range(60, 140):
        t = F(k, 400)
        for j in range(120, 160):
            cy = F(j, 100)
            cx, cy2, c, s, m, wall = witness(L, t, cy)
            mm = min(min(m.values()), wall)
            if best is None or mm > best[0]:
                best = (mm, t, cy, m, wall)
    mm, t, cy, m, wall = best
    worst = min(m.items(), key=lambda kv: kv[1])
    print(f"L={L}={float(L):.4f}: best t={t} (psi={math.degrees(2*math.atan(float(t))):.2f} deg), cy={cy}; min point margin {worst} = {float(worst[1]):.6f}, wall {float(wall):.4f}; certified: {mm>0}; box side up to {float(1+2*mm):.5f}")
```

### `lemmas.py`

```text
"""Scratch checks of Stromquist's Lemmas 3-6 arithmetic (EJC 2003) and their L=3.84 analogues."""
import math

def bstar(a, th):
    c, s = math.cos(th), math.sin(th)
    return c/(1+c) + (1 - a*c)/s

def fmin(a):
    # minimise b*(theta) over theta in (0, pi/2); golden section on a fine bracket
    best = None
    N = 20000
    for i in range(1, N):
        th = (math.pi/2) * i / N
        v = bstar(a, th)
        if best is None or v < best[0]:
            best = (v, th)
    v, th = best
    lo, hi = th - (math.pi/2)/N, th + (math.pi/2)/N
    gr = (math.sqrt(5)-1)/2
    for _ in range(200):
        x1 = hi - gr*(hi-lo); x2 = lo + gr*(hi-lo)
        if bstar(a, x1) < bstar(a, x2): hi = x2
        else: lo = x1
    th = (lo+hi)/2
    return bstar(a, th), math.degrees(th)

def cubic_roots(a):
    # 2c^3 - (2a+2)c^2 + (a^2-2a+3)c - (1-a^2) = 0 in c = cos(theta), c in (0,1)
    f = lambda c: 2*c**3 - (2*a+2)*c**2 + (a*a-2*a+3)*c - (1-a*a)
    roots = []
    N = 200000
    prev = f(0.0)
    for i in range(1, N+1):
        c = i/N
        cur = f(c)
        if prev == 0 or prev*cur < 0:
            lo, hi = (i-1)/N, c
            for _ in range(100):
                mid = (lo+hi)/2
                if f(lo)*f(mid) <= 0: hi = mid
                else: lo = mid
            roots.append((lo+hi)/2)
        prev = cur
    return roots

print("=== Lemma 4: f(a) = min_theta b*(theta) (true minimum) vs paper table ===")
for name, a in [("1/2+sqrt(1/8)", 0.5+math.sqrt(1/8)), ("sqrt(4/5)", math.sqrt(0.8)), (".96", .96),
                (".95 (Fig14 G cell)", .95), (".92 (=3.84/2-1)", .92), (".90", .90), (".91", .91), (".93", .93), (".94", .94),
                ("s-2.85 at s=2+4/sqrt5", 2+4/math.sqrt(5)-2.85), ("3.84-2.85", 3.84-2.85)]:
    v, th = fmin(a)
    roots = cubic_roots(a)
    print(f"a={a:.6f} ({name}): f(a)={v:.10f} at theta*={th:.4f} deg; cubic roots cos={['%.6f'%r for r in roots]} -> angles {['%.3f'%math.degrees(math.acos(r)) for r in roots]}; roots with cos<=a: {['%.3f'%math.degrees(math.acos(r)) for r in roots if r<=a]}")

print()
print("=== Lemma 5 checks (pentagon (1,0),(1,1),(2,1),(2.12,.9),(2.12,0)) ===")
D = lambda th: (math.sin(th)+math.cos(th)-1)/(math.sin(th)*math.cos(th))
print("min over first quadrant of D(theta) (length of intersection with y=1):", min(D(math.radians(t/100)) for t in range(1, 9000)))
th = math.atan(1.2)
x4 = 1 + .212/math.tan(th) + D(th)
print(f"eq (4) at tan theta = 1.2: x = {x4:.5f} (paper: > 2.004)")
best = min((1 + .112/math.tan(math.radians(t/100)) + (math.sin(math.radians(t/100))+math.cos(math.radians(t/100))-.9)/(math.sin(math.radians(t/100))*math.cos(math.radians(t/100))), t/100) for t in range(3000, 8999))
print(f"eq (5) minimum: x = {best[0]:.5f} at theta = {best[1]:.2f} deg (paper: 2.1256 at 52.6 deg)")
# ratio bound for sin theta > .9
worst = min(((1-math.cos(th))/math.sin(th) + .212*(1+math.sin(th))/(math.sin(th)*math.cos(th))) for th in [math.asin(.9)+1e-9 + k*(math.pi/2-math.asin(.9)-2e-9)/2000 for k in range(2000)])
print(f"ratio (x-2)/(1-y) minimum over sin theta > .9: {worst:.4f} (need > 1.2)")

print()
print("=== Lemma 6 constants, a = sqrt(4/5) (s = 2+4/sqrt5) and a = .92 (L = 3.84) ===")
def lemma6(a, apex):
    # theta0: D(theta0) = a, smallest positive
    lo, hi = 1e-6, math.pi/4
    for _ in range(200):
        mid = (lo+hi)/2
        if D(mid) > a: lo = mid
        else: hi = mid
    th0 = (lo+hi)/2
    height = lambda th: 1 + (D(th) - a/2)*math.tan(th)
    hs = [height(th0 + k*(math.pi/2 - 2*th0)/2000) for k in range(2001)]
    return th0, math.cos(th0)+math.sin(th0), height(th0), min(hs)
for a, apex in [(math.sqrt(.8), 1.12), (.92, 1.12), (.92, 1.10), (.92, 1.08)]:
    th0, cs, h0, hmin = lemma6(a, apex)
    print(f"a={a:.6f}: theta0={math.degrees(th0):.4f} deg, cos+sin at theta0={cs:.5f} (need > apex {apex}), apex-line height at theta0={h0:.5f}, min over [theta0, pi/2-theta0]={hmin:.5f} (need >= apex)")
print("half-asin(5-2sqrt5) =", math.degrees(0.5*math.asin(5-2*math.sqrt(5))))

print()
print("=== Lemma 3 bottom rectangle: a + 2b <= 2 sqrt 2 with b = .9 ===")
for L in [2+4/math.sqrt(5), 3.82, 3.84]:
    a = L/2 - 1
    print(f"L={L:.5f}: a={a:.5f}, a+2b={a+1.8:.5f} vs 2sqrt2={2*math.sqrt(2):.5f} ->", a+1.8 <= 2*math.sqrt(2))
```

### `skeleton.py`

```text
"""Heavy-atom skeleton of the T-018 certificate: what Corollary 1a ownership would look like."""
import json, math
from fractions import Fraction as F
d=json.load(open('/home/user/squares/packing/cases/n11_fractional_certificate/certificate.json'))
atoms=[(F(x),F(y),F(w)) for x,y,w in d['atoms']]
L=F(d['outer_side']); B=F(d['square_side']); M=sum(a[2] for a in atoms)
print("L",L,"B",B,"M",M,float(M),"eps=M-11 =",float(M-11))
ws=sorted((a[2] for a in atoms), reverse=True)
print("distinct weights (top 12):",[str(w) for w in sorted(set(ws),reverse=True)[:12]])
# if a hypothetical valid measure at 3.84 had M = 11 + eps, heavy atoms are those with w > eps.
for eps in [F(1,1000),F(1,200),F(1,100),F(1,50),F(1,25),F(1,20),F(1,10)]:
    H=[a for a in atoms if a[2]>eps]
    print(f"eps={float(eps):.4f}: |H|={len(H)} heavy atoms carrying {float(sum(a[2] for a in H)):.4f}")
# corner atoms: (0.99769..,0.99769..) orbit of 4, weight 917/6250 each; pairwise distances vs B*sqrt2 (max diameter of a B-square)
corner=[a for a in atoms if a[2]==F(917,6250)]
print("corner atoms:",[(float(a[0]),float(a[1])) for a in corner])
dmin=min(math.hypot(float(p[0]-q[0]),float(p[1]-q[1])) for i,p in enumerate(corner) for q in corner[i+1:])
print("min pairwise distance between corner atoms",dmin,"; B-square diameter",float(B)*math.sqrt(2),"-> a core holds at most one corner atom:",dmin>float(B)*math.sqrt(2))
# centre atom
ctr=[a for a in atoms if a[0]==L/2 and a[1]==L/2]
print("centre atom",[(float(a[0]),float(a[1]),float(a[2])) for a in ctr])
# mass near walls (within 1 of a wall) versus interior
near=sum(a[2] for a in atoms if min(a[0],L-a[0],a[1],L-a[1])<=1)
print("mass within distance 1 of a wall:",float(near),"interior mass:",float(M-near))
# 'row' structure: mass at y in [0.99,1.0] (the (1,1)-row analogue) 
rows={}
for x,y,w in atoms:
    key=round(float(min(y,L-y)),2)
    rows[key]=rows.get(key,0)+w
top=sorted(rows.items(), key=lambda kv:-kv[1])[:12]
print("folded y-level mass (top 12):",[(k,round(float(v),3)) for k,v in top])
```

### `symmetrization_witness.py`

```text
"""Explicit witnesses for Corollary A.2 (symmetrisation fails) and the A-triple content of the 3.84 escape."""
import math, random
random.seed(3)
L = 2 + 4/math.sqrt(5); C = L/2; U = 1.5 - L/4; V = 0.5 + L/4
P10 = [(1,1),(C,1),(L-1,1),(U,C),(V,C),(L-V,C),(L-U,C),(1,L-1),(C,L-1),(L-1,L-1)]
P12 = [(1,.9),(C,.9),(V,1.12),(L-1,1),(L-.9,C),(L-1,L-1),(C,L-.9),(1,L-1),(.79,1.85),(1.5,2.1),(2.1,2.1),(2.1,1.5)]
imgs = {"id": lambda p: p, "gx": lambda p: (L-p[0], p[1]), "gy": lambda p: (p[0], L-p[1]), "gxy": lambda p: (L-p[0], L-p[1])}
def contains(cx, cy, th, p):
    c, s = math.cos(th), math.sin(th); dx, dy = p[0]-cx, p[1]-cy
    return abs(c*dx+s*dy) <= 0.5 and abs(-s*dx+c*dy) <= 0.5
def counts(cx, cy, th):
    return {k: sum(contains(cx,cy,th,f(p)) for p in P12) for k,f in imgs.items()}, sum(contains(cx,cy,th,p) for p in P10)
# find a BL avoider of P10 (closed unit square inside the container, centre in R=[1,C]x[0,1])
best=None
for _ in range(300000):
    th = random.uniform(-0.6, 0.6); h=(abs(math.cos(th))+abs(math.sin(th)))/2
    cx = random.uniform(max(1,h), min(C, L-h)); cy = random.uniform(h, 1)
    c10 = sum(contains(cx,cy,th,p) for p in P10)
    if c10 == 0:
        cs, _ = counts(cx, cy, th)
        tot = sum(cs.values())
        if best is None or tot < best[0]: best = (tot, cx, cy, math.degrees(th), cs)
print("BL avoider with least total count over the four K4 images of P12':", best)
# corner box witness: axis-parallel unit square at (0.5+d, 0.5+d)
d = 1e-3
print("corner box (0.5+d,0.5+d):", counts(0.5+d, 0.5+d, 0.0))
# membership of the A-triple at L=3.84 for the certified escape (centre (1.46,1.34), tan(psi/2)=49/200)
L2 = 3.84; C2 = L2/2; V2 = 0.5 + L2/4
th = 2*math.atan(49/200)
A = [(1,.9),(C2,.9),(V2,1.12)]
print("3.84 escape centre (1.46,1.34) psi=%.2f deg contains A1,A2,A3:" % math.degrees(th), [contains(1.46,1.34,th,p) for p in A])
```

### `trump_at_U.py`

```text
"""Trump's packing numerically; which squares escape Stromquist's P10 formulas evaluated at L=U, coverage counts."""
import math
# u = tan(a/2): root in (0.36,0.37) of 5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1
co = [5,-10,-2,14,12,-6,2,2,-1]
f = lambda u: sum(c*u**(8-i) for i,c in enumerate(co))
lo, hi = 0.36, 0.37
for _ in range(200):
    m=(lo+hi)/2
    if f(lo)*f(m) <= 0: hi=m
    else: lo=m
u=(lo+hi)/2
ca=(1-u*u)/(1+u*u); sa=2*u/(1+u*u)
side=(6*u+4)/(1+2*u-u*u)
print("u=",u,"angle=",math.degrees(math.atan2(sa,ca)),"side U=",side)
r1 = 1-(side-3)*ca; u1=((1+r1)*ca-1)/sa; v1=ca-sa; v2=(side-1)/sa - r1 - (3+u1)*(ca/sa); x0 = 1+2/ca-(side-2)*(sa/ca)
def axis(x,y): return [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
def tilted(ox,oy):
    out=[]
    for dx,dy in ((0,0),(1,0),(1,1),(0,1)):
        px,py=ox+dx,oy+dy-r1
        out.append((1+ca*px-sa*py, 1+sa*px+ca*py))
    return out
sq=[axis(0,0),axis(side-1,0),axis(x0,side-1),axis(0,side-1),axis(1,side-1),axis(0,side-2),
    tilted(0,0),tilted(u1,-1),tilted(1,v1),tilted(u1+1,v1-1),tilted(u1+2,-v2)]
def centre(q): return (sum(p[0] for p in q)/4, sum(p[1] for p in q)/4)
def contains(q,p,eps=1e-12):
    # closed convex quadrilateral membership via cross products (ccw order assumed)
    n=len(q); sgn=[]
    for i in range(n):
        ax,ay=q[i]; bx,by=q[(i+1)%n]
        sgn.append((bx-ax)*(p[1]-ay)-(by-ay)*(p[0]-ax))
    return all(s>=-eps for s in sgn) or all(s<=eps for s in sgn)
L=side; C=L/2; Uu=1.5-L/4; V=0.5+L/4
P10=[(1,1),(C,1),(L-1,1),(Uu,C),(V,C),(L-V,C),(L-Uu,C),(1,L-1),(C,L-1),(L-1,L-1)]
P12=[(1,.9),(C,.9),(V,1.12),(L-1,1),(L-.9,C),(L-1,L-1),(C,L-.9),(1,L-1),(.79,1.85),(1.5,2.1),(2.1,2.1),(2.1,1.5)]
grid9=[(i*L/4,j*L/4) for i in (1,2,3) for j in (1,2,3)]
print("square: centre, angle, #P10, #P12, #grid9")
tot10=tot12=0
for k,q in enumerate(sq):
    c=centre(q); ang = 0 if k<6 else math.degrees(math.atan2(sa,ca))
    n10=sum(contains(q,p) for p in P10); n12=sum(contains(q,p) for p in P12); n9=sum(contains(q,p) for p in grid9)
    tot10+=n10; tot12+=n12
    print(k, tuple(round(v,4) for v in c), round(ang,3), n10, n12, n9)
print("sum P10 hits",tot10,"sum P12 hits",tot12,"weighted 2*P10+P12 total",2*tot10+tot12, "(a certificate would need every square >= 3, total >= 33 > 32)")
# corner boxes: which squares meet interior of unit corner boxes
def meets_corner_box(q, cx, cy):
    # test sample points of the square against the open box (cx,cx+1)x(cy,cy+1) crudely via vertices and edge midpoints and centre
    pts=list(q)+[centre(q)]+[((q[i][0]+q[(i+1)%4][0])/2,(q[i][1]+q[(i+1)%4][1])/2) for i in range(4)]
    return any(cx<p[0]<cx+1 and cy<p[1]<cy+1 for p in pts)
for cx,cy in [(0,0),(L-1,0),(0,L-1),(L-1,L-1)]:
    print("corner box",(round(cx,3),round(cy,3)),"met by squares",[k for k,q in enumerate(sq) if meets_corner_box(q,cx,cy)])
```

### `two_tier_check.py`

```text
"""Numerical sanity check: at s = 2+4/sqrt5, weights 2 on P10 and 1 on repaired P12 give coverage >= 3
for every closed unit square inside the container (sampled), and the printed-G set fails."""
import math, random
random.seed(7)
L = 2 + 4/math.sqrt(5); C = L/2; U = 1.5 - L/4; V = 0.5 + L/4
P10 = [(1,1),(C,1),(L-1,1),(U,C),(V,C),(L-V,C),(L-U,C),(1,L-1),(C,L-1),(L-1,L-1)]
def P12(gx): return [(1,.9),(C,.9),(V,1.12),(L-1,1),(L-.9,C),(L-1,L-1),(C,L-.9),(1,L-1),(gx,1.85),(1.5,2.1),(2.1,2.1),(2.1,1.5)]

def contains(cx, cy, th, p, eps=0.0):
    c, s = math.cos(th), math.sin(th)
    dx, dy = p[0]-cx, p[1]-cy
    u = c*dx + s*dy; v = -s*dx + c*dy
    return abs(u) <= 0.5+eps and abs(v) <= 0.5+eps

def inside(cx, cy, th):
    h = (abs(math.cos(th)) + abs(math.sin(th)))/2
    return h <= cx <= L-h and h <= cy <= L-h

def coverage(cx, cy, th, gx):
    m0 = sum(1 for p in P10 if contains(cx,cy,th,p))
    m1 = sum(1 for p in P12(gx) if contains(cx,cy,th,p))
    return m0, m1

def scan(gx, N):
    worst = (99, None); esc0 = 0; esc_cov = {}
    for _ in range(N):
        th = random.uniform(0, math.pi/2)
        h = (abs(math.cos(th)) + abs(math.sin(th)))/2
        cx = random.uniform(h, L-h); cy = random.uniform(h, L-h)
        m0, m1 = coverage(cx, cy, th, gx)
        tot = 2*m0 + m1
        if m0 == 0:
            esc0 += 1
            esc_cov[m1] = esc_cov.get(m1, 0) + 1
        if tot < worst[0]:
            worst = (tot, (cx, cy, math.degrees(th), m0, m1))
    return worst, esc0, esc_cov

for gx in [0.79, 0.80]:
    w, e, ec = scan(gx, 400000)
    print(f"G.x={gx}: min sampled 2*P10+P12 coverage = {w[0]} at {w[1]}; P10-escapes sampled: {e}, their P12 counts: {ec}")

# exp-016 witness: tan theta = 2.7, centre (37L'/(2 sqrt829), 11/8) with L' = 1.0001 (open box side), here evaluate as unit square
th = math.atan(2.7); cx = 37*1.0001/(2*math.sqrt(829)); cy = 11/8
print("exp-016 witness (unit square approx):", coverage(cx, cy, th, 0.80), "inside:", inside(cx,cy,th), " with G'=.79:", coverage(cx,cy,th,0.79))
# also hill-climb from escapes to minimise m1 among P10-avoiders for gx=.79
best = None
for _ in range(200000):
    th = random.uniform(0, math.pi/2); h=(abs(math.cos(th))+abs(math.sin(th)))/2
    cx = random.uniform(h, L-h); cy = random.uniform(h, L-h)
    m0, m1 = coverage(cx, cy, th, 0.79)
    if m0 == 0 and (best is None or m1 < best[0]): best = (m1, cx, cy, math.degrees(th))
print("min P12 count among sampled P10-avoiders (G'=.79):", best)
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
