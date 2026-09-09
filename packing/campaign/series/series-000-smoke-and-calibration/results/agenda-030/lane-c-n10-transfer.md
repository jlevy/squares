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

## Session-101 — corner-skeleton ownership at 96/25 (2026-09-08)

Research lane BC-293 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md), on
[H-128](../../../../hypotheses/H-128-corner-skeleton-ownership.md), bead `think-1136`,
session-101, 2.5 hours from 04:28Z on 2026-09-08. The planning report above is
untouched; this section is the lane’s result.
Scripts and raw outputs are in the appendix at the end of this section; nothing here is
a registered round, a new bound, or an edit to any registry.

### The question and its falsifiers

Question (the agenda cell, verbatim): does a valid D4-symmetric measure at 96/25 exist
with T-018’s four corner atoms at weight at least 3/20 and total mass below 11 + 3/20?

Falsifiers, stated before each run and recorded in the lane checkpoints: a bounded
column-generation run that converges with rationalised mass at or above 11 + 3/20 =
11.15; a final measure that the exact eighth-turn sweep refuses on Condition 1, 3, 4 or
5; or a bounded LP that does not converge inside its wall.
Only the exact sweep decides validity; every LP objective below is context.

**Handoff correction, 2026-09-08.** These were stopping criteria for the reported
finite-support attempt.
An above-threshold feasible measure or a time limit is not a falsifier of H-128’s
existence claim. A refutation needs an exact lower certificate over the entire declared
measure domain; the retained bound `10.785 < 11.15` does not provide one.

### The ownership step, exactly

Setting. Side `L = 96/25`, shrink `B = 9977/10000`, the retained net of 181 directions
(`t_k = k · 207107/500000 / 180`, `k = 0..180`, reaching `π/4`), a measure `μ` that is
D4-symmetric (Condition 1) and covers every reachable event cell at every net direction
with mass at least 1 (Condition 5); Conditions 3 and 4 are the net’s and hold as for
T-018. Write `M = μ(S) = 11 + ε`.

Lemma C′ (lane C, X-014 Corollary 1a restated).
In any packing of eleven unit squares in `[0, L]²`, each square contains, strictly
inside its interior, a closed `B`-square at a net direction (Condition 4); these eleven
cores `P_1, …, P_11` are pairwise disjoint, and by Condition 5 each has `μ(P_i) ≥ 1`.
Hence `Σ_i μ(P_i) ≤ M = 11 + ε` gives `μ(P_i) ≤ 1 + ε` for every `i` and
`μ(S ∖ ⋃ P_i) ≤ ε`. An atom `p` of weight `w > ε` therefore lies in at least one core
(else it contributes `w > ε` to the mass outside the cores) and in at most one (the
cores are disjoint).
So it lies in exactly one core.

Corollary C.2 at `96/25`. The four corner atoms are the D4 orbit of `(a, a)` with
`a = 1849127/1853400 · 384/381 = 29586032/29422725 ≈ 1.005550`, that is
`(a, a), (L − a, a), (a, L − a), (L − a, L − a)` — four members, the point being on the
diagonal mirror. Their least squared pairwise distance is `(L − 2a)² =
4633032392704/1385114794281 ≈ 1.82890²`; the diameter of a closed `B`-square is `B√2`
with `2B² = 99540529/50000000 ≈ 1.41096²`; and `4633032392704/1385114794281 >
99540529/50000000` (decided in `Fraction` arithmetic by the driver, which refuses to run
otherwise). So no core contains two corner atoms.

Theorem (conditional on the measure).
If a valid `μ` at `(96/25, 9977/10000, the net)` carries weight `w_c ≥ 3/20` on each
corner atom and has `M < 11 + 3/20`, then `ε <
3/20 ≤ w_c`, each corner atom lies in exactly one core by C′, the four cores are
distinct by C.2, and each core is strictly inside its own unit square: every packing of
eleven unit squares at side `96/25` has four distinct squares each containing one of the
four corner atoms in its interior.
No further geometry enters; the centre atom is not needed for this statement (H-128’s
fifth bound serves Lemma H’s two-pattern split, not the theorem).

What the LP variable is.
In `sqpack.fractional.colgen` the column for a D4 orbit `O` is one variable `w_O` with
objective coefficient `|O|` and row coefficient “members of `O` the placement covers”;
`rationalise_sites` gives every member of `O` the weight `w_O`. So `w_O` *is* the
per-atom weight, and the corner constraint is the single bound `w_O ≥ 3/20` on the
corner orbit (four members, orbit 122 of the scaled seed); the centre bound is
`w_O ≥ 1/8` on the centre orbit (one member).
The library fixes every bound at `(0, ∞)` (`colgen.solve_lp`), so the lane’s driver
re-implements `solve_rows` line for line with a bounded `linprog` call and drives
`generate_adaptive`’s column loop itself; `sqpack` is not edited.
Rounding up in `rationalise_sites` can only raise a weight, so the bound survives
rationalisation, and the driver checks it exactly on the rationalised atoms.

A proved floor from the bounded dual.
The bounded program’s dual gives more than a reading on a site set.
Let `(P_r, y_r)` be the final row placements and duals, `depth` the D4-symmetrised
closed-cover depth, `D = max(1, max depth)` decided exactly at the arrangement vertices
as `colgen.check_ceiling` does.
For every valid D4 measure `μ` on this `(L, B, net)` with `μ({p}) ≥ lb_p` at the bounded
atoms, `Σ_r y_r / D ≤ ∫ depth/D dμ ≤ μ(free atoms) + Σ_p (depth(p)/D) μ({p})`, hence
`M(μ) ≥ Σ_r y_r / D + Σ_p (1 − depth(p)/D) lb_p`. That floor holds for *every* site set
and every atom count, not only the one the run used; it is the statement that turns a
converged obstruction into a theorem about the net.

### Inputs common to every run

| Input | Value |
| --- | --- |
| Side, shrink | `L = 96/25`, `B = 9977/10000` |
| Net | `t_k = k · 207107/500000 / 180`, `k = 0..180` (181 directions; `D = 207107/90000000`, `B(1 + D) = 899996306539/900000000000 < 1`) |
| Seed | T-018’s 1121 atoms (`cases/n11_fractional_certificate/certificate.json`, mass `434547/40000` at `381/100`) with every coordinate scaled by `384/381 = 128/127`; 149 D4 orbits; the weights are not read |
| Grids | none (run 1); the library’s density rule `site_counts_for_side(96/25, 9977/10000)` = counts `25, 34, 42` at inset `1/2` (runs 2 and 4) |
| Corner orbit | `(29586032/29422725, 29586032/29422725)` and its three images; orbit 122 of the seed, size 4 |
| Centre orbit | `(48/25, 48/25)`; size 1 |
| Bounds | four-bound: corner `w ≥ 3/20`; five-bound: corner `w ≥ 3/20` and centre `w ≥ 1/8`; priced: corner orbit cost `3` (objective `M − w_c`); free: none |
| Column generation | `rows_per_direction 3`, `max_rounds 60`, `support_cap 32` for pricing, `settle 0`, one candidate orbit per column round, at most 10 column rounds per phase; rows carried across every phase |
| Rationalisation | `rationalise_sites` at scale `4 000 000` with the `1000001/1000000` bump (round-up only) |
| Verifier | `certificate.verify(workers=1)`: Conditions 1–5 exact; validity is 1, 3, 4, 5 (Condition 2 reports the mass against 11) |
| Machine | one process, `PACK_JOBS=1`, one BLAS thread; four cores shared with five other agents, load average 3–5 throughout; wall times are not comparable with the planning lane’s |
| Deadlines | four-bound 1500 s, free 1200 s, other phases 600 s each; no phase reached one |

Phases in one process, sharing one row set: B four-bound from scratch with column
rounds; A free, warm from B’s rows, with column rounds; C five-bound, one round; D free
on the final site set, one round; E four-bound on the final site set, one round (so D
and E are read on one site set and one row set); F priced, with column rounds.
Each final solution is rationalised, swept, and written with its atoms.

### Runs and exact verdicts

Every final measure below was rationalised and then decided by the exact eighth-turn
sweep in one worker; “valid” means Conditions 1, 3, 4 and 5 hold (Condition 2, mass
below 11, fails for every measure here and is reported as the mass).
Masses are the rationalised totals, exact; LP objectives are context.

**Run 1, seed only (control).** Site set: the scaled seed alone, 149 orbits, 1121 sites,
no grids; final 155 orbits, 1161 sites after six column rounds; 148 s wall.
Every phase converged.

| Phase | LP objective | Rationalised mass | Atoms | Corner weight | Centre weight | Least cell (direction) | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| four-bound, final site set | 12.504868914 | `50019567/4000000 = 12.50489175` | 181 | `600001/4000000` | `218727/4000000` | `4000007/4000000` (0) | yes |
| five-bound | 12.531451613 | `50125929/4000000 = 12.53148225` | 133 | `600001/4000000` | `500001/4000000` | `4000007/4000000` (0) | yes |
| free, final site set | 12.103825137 | `48415397/4000000 = 12.10384925` | 161 | none | `502733/4000000` | `800001/800000` (0) | yes |

The seed alone is a site artefact at `96/25`: its free value sits a unit above the
record’s `11.23` at `3.85`. It is retained as the control that shows why the grids are
needed, not as a reading of the geometry.

**Run 2 (decision) and run 4 (its replay with the dual saved and the priced phase).**
Site set: the density-matched grids `25, 34, 42` unioned with the scaled seed, 619
orbits and 4645 sites at the start, 637 orbits and 4777 sites after the column rounds
(18 orbits added, every one from the dual’s arrangement vertices); 8517 rows at the
final phases; 495 s wall for run 2. Every phase converged (no deadline was reached; the
four-bound phase spent its ten column rounds, the last candidate still at averaged depth
above 1, so the four-bound value is an upper reading on this site set and the floor
below is what bounds it from underneath).
Run 4 reproduced run 2’s objectives to the last printed digit.

| Phase | LP objective | Rationalised mass | Atoms | Corner weight | Centre weight | Least cell (direction) | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| four-bound, first converged LP on the 619-orbit set | 11.849054622 | — | — | — | — | — | — |
| four-bound, final site set (E) | 11.798148881 | `23596423/2000000 = 11.7982115` | 401 | `600001/4000000 ≥ 3/20` | `41/16000` | `400001/400000` (0) | yes |
| five-bound (C) | 11.819153276 | `47276821/4000000 = 11.81920525` | 369 | `600001/4000000` | `500001/4000000 ≥ 1/8` | `400001/400000` (0) | yes |
| free, final site set (D) | 11.262035287 | `22524199/2000000 = 11.2620995` | 377 | none (the orbit carries 0) | `9767/2000000` | `800003/800000` (0) | yes |
| priced `M − w_c` (F), first LP on the 637-orbit set | 11.262035287 | — | — | — | — | — | — |
| priced `M − w_c` (F), after nine more column rounds (646 orbits, 9934 rows) | 11.189559666 | `44758451/4000000 = 11.18961275` | 373 | none | `38307/4000000` | `250001/250000` (0) | yes |

**Verdict on the cell.** The falsifier stated before the run is met: the least
four-bound measure column generation reaches on this site set has mass
`23596423/2000000 ≈ 11.798 ≥ 11.15`, and it is a valid measure (so the reading is of a
real measure, not of an infeasible program).
The theorem is therefore *not* obtained at `96/25` on the retained shrink and net.

**The price.** On one site set (637 orbits) and one row set (8517 rows):
`M(forced) − M(free) = 23596423/2000000 − 22524199/2000000 = 33507/62500 = 0.536112`
exactly (LP: `0.5361136`). Four atoms at `3/20` add `3/5` of mass; the free optimum
recovers `0.064` of it elsewhere.
The free measure itself carries mass `11.262 > 11` at `96/25` on this net, `0.262` above
the certificate line, consistent with the record’s `11.23` unconverged at `3.85` and
with the plateau at `11.000` at `3.82`.

**The bound is not the obstacle; the position is.** Phase F prices the corner orbit at
`3` instead of `4`, so its objective is `M − w_c` and its optimum is `min_t (M(t) − t)`
over every bound `t ≥ 0`; the theorem needs that minimum below 11. On the 637-orbit site
set it equals the free value, `11.262035287`: the LP leaves T-018’s scaled corner site
at weight zero even when a unit of its weight is free, because the site’s orbit-averaged
depth under the free dual is `0.559`, below `3/4`. Nine further column rounds on the
priced program (646 orbits, 9934 rows) lowered the objective to `11.189559666` with the
corner orbit *still at zero*, so the fall is the free mass itself moving with columns,
not the corner site earning weight; the rationalised measure of that phase,
`44758451/4000000 = 11.18961275` over 373 atoms, is valid (least cell `250001/250000` at
direction 0) and is the lightest valid measure this lane holds at `96/25`. So no lower
bound at that position, of any size, yields the ownership theorem on these site sets;
H-128’s `3/20` is not a tunable that was set too high.
Every free reading here is an upper reading: each phase’s last candidate orbit still had
averaged depth above 1 (`1.09` to `1.29`) when its ten column rounds ran out.

**Where the mass went.** The free measure’s heaviest orbit is not T-018’s corner point
but T-018’s `(197/200, 73/100)` orbit scaled: the eight atoms `(3152/3175, 2336/3175)`,
`(2336/3175, 3152/3175)` and their images, `106251/800000 =
0.1328` each — a *pair* of marks per corner straddling the diagonal, `0.3635` apart, so
one core can hold both.
The next orbit carries `26087/250000 = 0.1043` at `(3.0818, 1.9630)`, a wall-midpoint
pair. At `3.84` the corner skeleton is a pair, not a point.

### A four-corner theorem the free measure does prove

Lemma C′ applies to sets as it does to atoms: with `M = 11 + ε` the mass outside the
eleven cores is at most `ε`, so any set of atoms of total weight above `ε` has at least
one atom inside some core.
The free measure of phase D (mass `22524199/2000000`, `ε =
524199/2000000 = 0.2620995`, exactly verified valid) carries `106251/800000` on each of
the eight atoms `(3152/3175, 2336/3175)`, `(2336/3175, 3152/3175)` and their images —
T-018’s `(197/200, 73/100)` orbit scaled by `128/127`. Per corner that pair has mass
`106251/400000 = 0.2656275 > ε`, margin `441/125000 = 0.003528`; the two marks of a
corner are `√(1331712/10080625) ≈ 0.3635` apart (one core can hold both, which is why
the pair and not either mark is the anchor); and the least squared distance between
marks of different corners is `34668544/10080625 ≈ 1.8545² > 2B² = 99540529/50000000`,
so no core meets two corners’ pairs.
Hence:

> **Theorem (four-corner pair containment at `96/25`).** Every packing of eleven unit
> squares in `[0, 96/25]²` has four distinct squares, one per corner, each containing in
> its interior at least one of its corner’s two marks `(3152/3175, 2336/3175)` and
> `(2336/3175, 3152/3175)` (and their images under the container’s symmetries).

It is proved by the phase-D measure and the exact sweep alone; it needs no bound, no
column settlement and no floor, because a single valid measure suffices.
It is the two-point form of what H-128 asked for at one point, and it is *not* implied
by insertion saturation’s blockers (which need only meet the open corner box).
The margin is `0.0035` of mass, so the phase-F measure (`ε = 0.1896`), which spreads its
corner mass differently, does not reproduce it: the theorem is a property of this
measure, and a measure built to widen the margin — phase G, the pair orbit priced at
`|O| − 2` — is run 5 below.

**Run 5 (phase G, the pair orbit priced at `|O| − 2`)** did not finish inside the lane’s
clock; its objective is `min (M − μ(pair))` and it is the next session’s first reading.

### The floor for the net

**Run 6 (four-bound only, `45` column rounds of six candidate orbits each, settle
threshold `0.005`, wall 35 min).** Final LP objective `11.730827068` on 883 orbits and
10364 rows; the last candidate orbit’s averaged depth was `nan`, so the dual did **not**
settle (`deadline reached after 4 rounds`). Its rationalised measure: mass
`2932721/250000 = 11.730884000`, valid = True, least cell `250001/250000`, corner
weights `['600001/4000000']`.

The floor from that dual, decided exactly: 70 of 70 dual rows kept (weight `11.130827`
of `11.130827`), symmetrised to 560 squares, 1487212 arrangement vertices, 3076 decided
exactly above the threshold `T = 1.058083`; exact maximum symmetrised depth found
`1.092857`, so `D = 1.092857` (`153`/140); depth at the four corner atoms `0.000000`,
`0.000000`, `0.000000`, `0.000000`; correction `Σ (1 − depth/D)·3/20 = 0.600000`;
**floor `Σy/D + correction = 10.785071`**. (that is `Σy/D = 10.185071` for the free part
plus the correction).
Every valid D4 measure on this `(L, B, net)` with the corner bound has mass at least
that floor. The four corner atoms have depth exactly 0 under this dual: no tight
placement of the final row set covers T-018’s corner site, so the bound’s price in the
dual is the full `4 · 3/20 = 3/5` with no substitution at all, which is the dual’s way
of saying what phase F said in the primal.
It is far below `11.15` because the dual is feasible at the sites and not pointwise —
the price of an unsettled column generation — so the obstruction is, in this block, a
reading on the site set and not yet a theorem for the net.
A settled dual (depth within `0.005` of 1 everywhere) would put the floor within half a
per cent of the LP value, which is what the next session should buy first.

### Lemma C dry run on T-018

T-018 at `381/100` (mass `434547/40000`, `ε = -5453/40000 < 0`, so every atom is owned):
the heaviest atom `(1849127/1853400, 1849127/1853400)` of weight `917/6250` and its
orbit moved together along the diagonal mirror (the only displacements that keep a
four-point orbit D4-closed); base sweep 48.2 s, least cell `4001/4000`. Surviving
displacements: 0 of 4.

| Radius | Direction | `d` | Valid | Least cell | Failed | s |
| --- | --- | --- | --- | --- | --- | --- |
| `1/1000` | +diag | `(1/1000, 1/1000)` | False | `85353/100000` | Condition 5 every reachable cell carries mass 1 | 60.1 |
| `1/1000` | -diag | `(-1/1000, -1/1000)` | False | `10951/12500` | Condition 5 every reachable cell carries mass 1 | 51.7 |
| `1/100` | +diag | `(1/100, 1/100)` | False | `85353/100000` | Condition 5 every reachable cell carries mass 1 | 45.4 |
| `1/100` | -diag | `(-1/100, -1/100)` | False | `85367/100000` | Condition 5 every reachable cell carries mass 1 | 46.9 |

Reading: with T-018’s least cell at `4001/4000`, a margin of `1/4000`, moving `917/6250`
of weight along the diagonal by the radii tried empties some tight cell, so `R(p) = {p}`
for the corner atom at this granularity and the transfer lemma has no slack to give at
`381/100` — the falsifier S5 named.
The automation itself (move an orbit, re-sweep, read the verdict) is the dry run’s
deliverable.

### Status of H-128 and what this feeds

H-128 remains open over the retained shrink and net.
The converged four-bound measure has mass `11.798`, so this finite-support attempt did
not obtain the theorem.
On that support the priced program identifies the corner position as the obstacle.
The global lower bound in the floor section is only `10.785 < 11.15`, which does not
refute the hypothesis.
This corrects the original recommendation to reject H-128 on the entire net.
The free value at `96/25` on this net (`11.19` to `11.26`) sits `0.19` to `0.26` above
the certificate line, which is the number BC-297’s ladder and BC-294’s duality readings
should be checked against.

What BC-299 (H-111, the anchored certificate) can pin from this lane: not a single
corner point, but a corner *pair* — four distinct squares each containing one of two
marks at `≈ (0.9928, 0.7357)` and `(0.7357, 0.9928)` from its corner.
That is a two-branch anchor per corner (sixteen patterns before symmetry, two up to D4
per corner choice), each branch a pinned point inside a named square, which is the input
the frame-conditioned certificate asked for in a weaker but proved form.
The ownership- conditioned split of Lemma H is unchanged: the centre atom carries
`≈ 0.005` in the free measure at `96/25`, so no centre anchor is available from the LP
at this side.

What the next session should do first: run phase G to settlement and read the largest
margin `μ(pair) − ε` the net allows (a proved margin is what makes the pair anchor
robust to the shrink tax); then settle the free program with many columns per round,
take its exact floor `Σy/D`, and record it against 11 — if it clears 11 it is the method
ceiling at `96/25` for this net, which BC-294 and BC-297 both need.

### Obstructions and mistakes worth recording

- **The seed alone is a site artefact.** T-018’s 1121 atoms scaled to `96/25` give a
  free value of `12.10`, a unit above the geometry’s; the density-matched grids bring it
  to `11.26`. A run “seeded with T-018” must union the grids, as the devtool does.
- **Column generation at this size does not settle in ten rounds.** Every phase’s last
  candidate orbit still had averaged depth `1.09` to `1.29`, so every reading is an
  upper reading and the ten-round duals are feasible at the sites only: their exact
  maximum symmetrised depth is `1.31` to `1.34` and the floors they give (`8.6` to
  `9.5`) say nothing. A floor for the net needs settlement, which run 6 buys with six
  columns per round and a `0.005` settle threshold.
- **The floor script’s first screen was unsound** (it re-decided only vertices within
  `1e-6` of the float maximum, and float depth over-counts at edge-touching vertices);
  it was replaced by the threshold rule stated above before any floor was read into the
  record.
- **The Lemma C dry run was started concurrently with run 4** by the lane’s own queue,
  against the one-worker rule, and its first moves exposed a bug: an off-diagonal
  displacement of a diagonal orbit is not D4-closed (the `d4_images` duplicates were
  mapped inconsistently), so the sweep refused Condition 1. It was killed on the
  coordinator’s steering, restricted to diagonal displacements, and requeued last.
- **Wall times are not comparable** with the planning lane’s: the load average ran from
  3 to 8 on four cores during the block.
- **Run 5 crashed after its free phase hit the wall.** The driver’s wall fallback hands
  back the last converged solution on its own site set, but the shared row matrix
  already carries the column added for the unconverged round, so the next phase’s warm
  solve fails on a dimension mismatch (`A_ub` columns against `c`). Run 6 escaped it
  because it ran one phase.
  The free phase of run 5 had reached LP `11.232919611` on 626 orbits before the wall
  (under load average 7–8 the from-scratch free phase took ten minutes, not four), and
  the pair-priced phase never ran: the pair theorem’s margin beyond the phase-D
  measure’s `441/125000` is unmeasured.
  The fix is one line (truncate the row matrix to the returned site set’s columns) and
  is left to the next session with the scripts.

### Appendix: scripts and outputs as run

Retained verbatim from the lane’s scratch directory on 2026-09-08. Every script imports
`sqpack` and was run through the project environment with `PACK_JOBS=1` and one BLAS
thread. None is promoted to `devtools/`; the first lane that reuses one owns that
promotion.

### `bounded_colgen.py`

```text
"""BC-293: column generation at 96/25 with lower bounds on the corner-skeleton orbits.

A lane-owned driver that calls `sqpack.fractional` and changes exactly one thing
against `colgen.solve_rows`: the LP bounds, which the library fixes at ``(0, None)``
for every orbit. Nothing here decides a bound; the exact eighth-turn sweep
(`certificate.verify`) is the only thing that turns the final measure into a claim.

Phases share one row set (rows stay valid across bound changes and site additions):
  A  free LP on the seed site set, then column rounds;
  B  the four corner atoms bounded below, warm from A's rows, then column rounds;
  C  B plus the centre atom bounded below (H-128's five-bound criterion);
  D  the free LP re-solved on the final site set, so the price M(forced) - M(free)
     is read on one site set.
The B measure is rationalised and decided by the sweep with workers=1.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.colgen import (
    LpSolution,
    Rows,
    SiteSet,
    dual_squares,
    orbit_column,
    rank_candidates,
    rationalise_sites,
    site_counts_for_side,
    site_set_from_grids,
    site_set_from_points,
)
from sqpack.fractional.generate import (
    LP_FEASIBILITY,
    direction_net,
    net_half_tangents,
    placement_cells,
)


def log(handle, text: str) -> None:
    stamp = time.strftime("%H:%M:%S", time.gmtime())
    line = f"[{stamp}] {text}"
    print(line, flush=True)
    handle.write(line + "\n")
    handle.flush()


def solve_lp_bounded(sites: SiteSet, rows: Rows, lower: np.ndarray, cost: np.ndarray | None = None):
    """`colgen.solve_lp` with per-orbit lower bounds on the per-atom weight, and an
    optional objective vector (default: the orbit sizes, i.e. the mass)."""

    result = linprog(
        c=sites.sizes() if cost is None else cost,
        A_ub=-rows.stacked(),
        b_ub=-np.ones(len(rows)),
        bounds=[(float(lb), None) for lb in lower],
        method="highs",
    )
    if not result.success:
        return None
    duals = np.maximum(-np.asarray(result.ineqlin.marginals, dtype=float), 0.0)
    return np.asarray(result.x, dtype=float), duals, float(result.fun)


def solve_rows_bounded(
    sites: SiteSet,
    square_side: Fraction,
    half_tangents,
    rows: Rows,
    lower: np.ndarray,
    *,
    cost: np.ndarray | None = None,
    max_rounds: int,
    rows_per_direction: int = 3,
    tolerance: float = 1e-9,
    deadline: float | None,
    handle,
    tag: str,
) -> LpSolution:
    """`colgen.solve_rows`, line for line, with `solve_lp_bounded` in place of `solve_lp`."""

    points = sites.points()
    sizes = sites.sizes()
    membership = sites.membership()
    columns = len(sites.orbits)
    directions = direction_net(half_tangents)
    outer = float(sites.outer_side)
    side = float(square_side)
    if rows.matrix.shape[0] == 0:
        rows.matrix = np.zeros((0, columns))
    weights = np.zeros(columns)
    duals = np.zeros(len(rows))
    solution = LpSolution(weights, duals, rows=len(rows))
    if len(rows) > 0:
        warm = solve_lp_bounded(sites, rows, lower, cost)
        if warm is not None:
            weights, duals, objective = warm
            solution.weights, solution.duals, solution.objective = weights, duals, objective
            log(handle, f"{tag} warm solve on {len(rows)} rows: objective {objective:.9f}")
    for round_index in range(max_rounds):
        if deadline is not None and time.perf_counter() >= deadline:
            solution.stopped = f"deadline reached after {round_index} rounds"
            return solution
        solution.rounds = round_index + 1
        started = time.perf_counter()
        site_weights = weights[membership]
        support = int(np.count_nonzero(site_weights))
        violated = added = 0
        least = float("inf")
        least_covered = float("inf")
        for index, direction in enumerate(directions):
            for mass, cu, cv, covers in placement_cells(
                points, site_weights, direction, outer, side, keep=rows_per_direction
            ):
                least_covered = min(least_covered, mass)
                if mass >= 1 - tolerance:
                    break
                row = np.zeros(columns)
                np.add.at(row, membership[covers], 1.0)
                if row.sum() == 0:
                    solution.stopped = "a placement covers no site: the sites cannot cover"
                    return solution
                violated += 1
                least = min(least, mass)
                added += rows.add(index, (cu, cv), row)
        solution.rows = len(rows)
        solution.least_covered = least_covered
        sep = time.perf_counter() - started
        if violated == 0 or (added == 0 and least >= 1 - LP_FEASIBILITY):
            solution.objective = float((sizes if cost is None else cost) @ weights)
            solution.stopped = "converged: every placement covers mass 1"
            log(
                handle,
                f"{tag} lp round {round_index}: rows={len(rows)} support={support} "
                f"violated={violated} least_covered={least_covered:.9f} sep={sep:.1f}s "
                f"objective={solution.objective:.9f} | converged",
            )
            return solution
        if added == 0:
            solution.stopped = f"a held row is violated by {1 - least:.3e}: the solver's point is off"
            return solution
        lp_started = time.perf_counter()
        solved = solve_lp_bounded(sites, rows, lower, cost)
        lp_s = time.perf_counter() - lp_started
        if solved is None:
            solution.stopped = "linear program refused the generated rows"
            return solution
        weights, duals, objective = solved
        solution.weights, solution.duals, solution.objective = weights, duals, objective
        log(
            handle,
            f"{tag} lp round {round_index}: rows={len(rows)} added={added} support={support} "
            f"violated={violated} least={least:.6f} sep={sep:.1f}s lp={lp_s:.1f}s "
            f"objective={objective:.9f}",
        )
    solution.stopped = f"round limit {max_rounds} reached"
    return solution


def column_phase(
    tag: str,
    sites: SiteSet,
    rows: Rows,
    lower_for,
    *,
    cost_for=None,
    square_side: Fraction,
    half_tangents,
    column_rounds: int,
    max_rounds: int,
    settle: float,
    support_cap: int,
    columns_per_round: int = 1,
    deadline: float | None,
    handle,
) -> tuple[SiteSet, LpSolution, list[dict]]:
    """`colgen.generate_adaptive`'s loop with the bounded row solver."""

    record: list[dict] = []
    solution = LpSolution(np.zeros(len(sites.orbits)), np.zeros(0))
    last_converged: tuple[SiteSet, LpSolution] | None = None
    for index in range(column_rounds):
        started = time.perf_counter()
        lower = lower_for(sites)
        solution = solve_rows_bounded(
            sites,
            square_side,
            half_tangents,
            rows,
            lower,
            cost=None if cost_for is None else cost_for(sites),
            max_rounds=max_rounds,
            deadline=deadline,
            handle=handle,
            tag=f"{tag}.col{index}",
        )
        found = []
        depth = float("nan")
        note = solution.stopped
        if solution.converged:
            weighted = dual_squares(
                rows, solution.duals, half_tangents, sites.outer_side, square_side,
                support_cap=support_cap,
            )
            found = rank_candidates(sites, weighted, wanted=columns_per_round)
            if found:
                depth = float(found[0].averaged_depth)
                note = f"deepest candidate {found[0].point} depth {depth:.6f}"
            else:
                note = "no candidate orbit has averaged depth above 1"
        entry = {
            "phase": tag, "column_round": index, "rows": len(rows),
            "orbits": len(sites.orbits), "sites": sites.size,
            "objective": solution.objective, "lp_rounds": solution.rounds,
            "least_covered": solution.least_covered, "stopped": solution.stopped,
            "depth": depth, "seconds": round(time.perf_counter() - started, 1),
        }
        record.append(entry)
        log(handle, f"{tag} column round {index}: {json.dumps(entry)} | {note}")
        if solution.converged:
            last_converged = (sites, solution)
        if (
            not solution.converged or not found
            or found[0].averaged_depth <= 1 + settle or index + 1 == column_rounds
        ):
            break
        sites = SiteSet(sites.outer_side, (*sites.orbits, *(c.orbit for c in found)))
        for candidate in found:
            rows.add_column(orbit_column(rows, candidate.orbit, half_tangents, square_side))
    if not solution.converged and last_converged is not None:
        log(handle, f"{tag}: last column round unconverged ({solution.stopped}); returning the last converged solution")
        sites, solution = last_converged
    return sites, solution, record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", type=Fraction, default=Fraction(96, 25))
    parser.add_argument("--shrink", type=Fraction, default=Fraction(9977, 10000))
    parser.add_argument("--angle-limit", type=Fraction, default=Fraction(207107, 500000))
    parser.add_argument("--direction-steps", type=int, default=180)
    parser.add_argument("--seed-certificate", type=Path, required=True)
    parser.add_argument("--grid-counts", default="", help="optional comma list of grids to union")
    parser.add_argument("--corner-bound", type=Fraction, default=Fraction(3, 20))
    parser.add_argument("--centre-bound", type=Fraction, default=Fraction(1, 8))
    parser.add_argument("--column-rounds", type=int, default=4)
    parser.add_argument("--max-rounds", type=int, default=60)
    parser.add_argument("--settle", type=float, default=0.0)
    parser.add_argument("--support-cap", type=int, default=32)
    parser.add_argument("--columns-per-round", type=int, default=1)
    parser.add_argument("--scale", type=int, default=4_000_000)
    parser.add_argument("--deadline-a", type=float, default=1200.0)
    parser.add_argument("--deadline-b", type=float, default=1800.0)
    parser.add_argument("--deadline-c", type=float, default=600.0)
    parser.add_argument("--out", type=Path, required=True, help="output directory")
    parser.add_argument("--phases", default="BACDEF", help="phase letters to run, in this order: B A C D E F G")
    parser.add_argument("--pair-site", default="197/200,73/100",
                        help="T-018 coordinates of the near-corner pair orbit (scaled like the seed) for phase G")
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    handle = (args.out / "run.log").open("a")
    L, B = args.side, args.shrink
    half_tangents = net_half_tangents(args.angle_limit, args.direction_steps)

    record = json.loads(args.seed_certificate.read_text())
    ratio = L / Fraction(record["outer_side"])
    seed = {(Fraction(x) * ratio, Fraction(y) * ratio) for x, y, _ in record["atoms"]}
    points = set(seed)
    counts: tuple[int, ...] = ()
    if args.grid_counts == "auto":
        counts = site_counts_for_side(L, B)
    elif args.grid_counts:
        counts = tuple(int(c) for c in args.grid_counts.split(","))
    if counts:
        points |= set(site_set_from_grids(L, counts, Fraction(1, 2)).positions())
    sites = site_set_from_points(L, points)

    corner_source = max(record["atoms"], key=lambda a: Fraction(a[2]))
    corner = (Fraction(corner_source[0]) * ratio, Fraction(corner_source[1]) * ratio)
    centre = (L / 2, L / 2)

    def orbit_index(site_set: SiteSet, point) -> int:
        for index, orbit in enumerate(site_set.orbits):
            if point in orbit:
                return index
        raise KeyError(point)

    corner_orbit = sites.orbits[orbit_index(sites, corner)]
    d2 = min(
        (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
        for i, p in enumerate(corner_orbit) for q in corner_orbit[i + 1:]
    )
    premise = d2 > 2 * B * B
    inputs = {
        "side": str(L), "shrink": str(B), "angle_limit": str(args.angle_limit),
        "direction_steps": args.direction_steps, "seed": str(args.seed_certificate),
        "seed_ratio": str(ratio), "seed_sites": len(seed), "grid_counts": list(counts),
        "orbits": len(sites.orbits), "sites": sites.size,
        "corner_orbit": [[str(x), str(y)] for x, y in corner_orbit],
        "corner_orbit_size": len(corner_orbit),
        "corner_min_d2": str(d2), "two_B2": str(2 * B * B), "premise_d2_gt_2B2": premise,
        "corner_bound": str(args.corner_bound), "centre_bound": str(args.centre_bound),
        "column_rounds": args.column_rounds, "max_rounds": args.max_rounds,
        "scale": args.scale, "deadlines_s": [args.deadline_a, args.deadline_b, args.deadline_c],
        "argv": sys.argv,
    }
    log(handle, "inputs " + json.dumps(inputs))
    if not premise:
        log(handle, "the corner atoms are not pairwise farther than B*sqrt2 apart: stop")
        return 2

    def free_bounds(site_set: SiteSet) -> np.ndarray:
        return np.zeros(len(site_set.orbits))

    def four_bounds(site_set: SiteSet) -> np.ndarray:
        lower = np.zeros(len(site_set.orbits))
        lower[orbit_index(site_set, corner)] = float(args.corner_bound)
        return lower

    def five_bounds(site_set: SiteSet) -> np.ndarray:
        lower = four_bounds(site_set)
        lower[orbit_index(site_set, centre)] = float(args.centre_bound)
        return lower

    rows = Rows()
    common = dict(
        square_side=B, half_tangents=half_tangents, max_rounds=args.max_rounds,
        settle=args.settle, support_cap=args.support_cap, columns_per_round=args.columns_per_round, handle=handle,
    )
    results: dict = {"inputs": inputs, "phases": {}}
    t0 = time.perf_counter()

    pair = (Fraction(args.pair_site.split(",")[0]) * ratio, Fraction(args.pair_site.split(",")[1]) * ratio)
    pair_orbit = sites.orbits[orbit_index(sites, pair)]

    def priced_cost(site_set: SiteSet) -> np.ndarray:
        cost = site_set.sizes().copy()
        cost[orbit_index(site_set, corner)] -= 1.0  # M - w_c: the ownership criterion itself
        return cost

    def pair_cost(site_set: SiteSet) -> np.ndarray:
        cost = site_set.sizes().copy()
        cost[orbit_index(site_set, pair)] -= 2.0  # M - (mass of one corner's pair)
        return cost

    sol: dict[str, LpSolution] = {}
    site_of: dict[str, SiteSet] = {}
    plan = {
        "B": ("B-four", four_bounds, None, args.column_rounds, args.deadline_b),
        "A": ("A-free", free_bounds, None, args.column_rounds, args.deadline_a),
        "C": ("C-five", five_bounds, None, 1, args.deadline_c),
        "D": ("D-free-final", free_bounds, None, 1, args.deadline_c),
        "E": ("E-four-final", four_bounds, None, 1, args.deadline_c),
        "F": ("F-priced", free_bounds, priced_cost, args.column_rounds, args.deadline_c),
        "G": ("G-pair-priced", free_bounds, pair_cost, args.column_rounds, args.deadline_c),
    }
    for letter in args.phases:
        tag, lower_for, cost_for, col_rounds, wall = plan[letter]
        new_sites, solution, rec = column_phase(
            tag, sites, rows, lower_for, cost_for=cost_for, column_rounds=col_rounds,
            deadline=time.perf_counter() + wall, **common,
        )
        results["phases"][letter] = rec
        sol[tag] = solution
        site_of[tag] = new_sites
        if letter not in "DE":  # D and E are re-reads on the site set they were given
            sites = new_sites

    def finish(tag: str, site_set: SiteSet, solution: LpSolution, expect_corner: Fraction | None):
        if not solution.converged:
            log(handle, f"{tag}: not converged ({solution.stopped}); no measure is rationalised")
            return {"converged": False, "stopped": solution.stopped, "objective": solution.objective}
        atoms = rationalise_sites(site_set, solution.weights, scale=args.scale)
        cert = Certificate(n=11, outer_side=L, square_side=B, atoms=atoms, half_tangents=half_tangents)
        corner_weights = sorted({a.weight for a in atoms if (a.x, a.y) in corner_orbit})
        centre_weight = [a.weight for a in atoms if (a.x, a.y) == centre]
        w_c = corner_weights[0] if corner_weights else Fraction(0)
        priced_value = cert.total_mass - w_c
        pair_weights = sorted({a.weight for a in atoms if (a.x, a.y) in pair_orbit})
        w_pair = pair_weights[0] if pair_weights else Fraction(0)
        pair_value = cert.total_mass - 2 * w_pair
        log(handle, f"{tag}: rationalised mass {cert.total_mass} = {float(cert.total_mass):.9f} over {len(atoms)} atoms; corner weights {corner_weights}; centre {centre_weight}")
        started = time.perf_counter()
        verdict = verify(cert, workers=1)
        sweep_s = time.perf_counter() - started
        conds = [(c.name, c.holds, c.detail) for c in verdict.conditions]
        valid = all(h for n_, h, _ in conds if not n_.startswith("Condition 2"))
        log(handle, f"{tag}: sweep {sweep_s:.1f}s; conditions {conds}; valid(1,3,4,5)={valid}; least cell {verdict.minimum_cell_mass}")
        out = {
            "converged": True, "objective": solution.objective, "lp_rounds": solution.rounds,
            "mass": str(cert.total_mass), "mass_float": float(cert.total_mass), "atoms": len(atoms),
            "mass_minus_corner": str(priced_value), "mass_minus_corner_float": float(priced_value),
            "pair_weights": [str(w) for w in pair_weights], "pair_orbit_size": len(pair_orbit),
            "mass_minus_pair": str(pair_value), "mass_minus_pair_float": float(pair_value),
            "corner_weights": [str(w) for w in corner_weights], "centre_weight": [str(w) for w in centre_weight],
            "conditions": conds, "valid_1345": valid, "least_cell_mass": str(verdict.minimum_cell_mass),
            "worst_direction": verdict.worst_direction, "sweep_seconds": round(sweep_s, 1),
            "corner_bound_met": (expect_corner is None) or all(w >= expect_corner for w in corner_weights),
        }
        # The full dual support, exact, for the lane's bounded-ceiling check.
        duals = solution.duals
        if len(duals) < len(rows):
            duals = np.concatenate([duals, np.zeros(len(rows) - len(duals))])
        full = dual_squares(rows, duals, half_tangents, L, B, support_cap=10**9)
        (args.out / f"dual-{tag}.json").write_text(json.dumps({
            "tag": tag, "outer_side": str(L), "square_side": str(B), "objective": solution.objective,
            "priced": ([[str(x), str(y), "3/4"] for x, y in corner_orbit] if tag.startswith("F-") else [])
                      + ([[str(x), str(y), "3/4"] for x, y in pair_orbit] if tag.startswith("G-") else []),
            "bounded": [[str(x), str(y), str(lb)] for (x, y), lb in
                        ([(m, args.corner_bound) for m in corner_orbit] if expect_corner is not None else [])
                        + ([(centre, args.centre_bound)] if tag.startswith("C-") else [])],
            "squares": [[str(sq.ax), str(sq.ay), str(sq.u), str(sq.bx), str(sq.by), str(sq.v), str(sq.half), str(wt)]
                        for sq, wt in full],
        }, indent=0))
        (args.out / f"measure-{tag}.json").write_text(json.dumps({
            "id": f"bc-293-{tag}", "n": 11, "outer_side": str(L), "square_side": str(B),
            "angle_limit": str(args.angle_limit), "direction_steps": args.direction_steps,
            "total_mass": str(cert.total_mass), "least_cell_mass": str(verdict.minimum_cell_mass),
            "symmetry": "D4", "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in atoms],
        }, indent=1))
        return out

    results["final"] = {}
    for tag, solution in sol.items():
        expect = args.corner_bound if tag in ("E-four-final", "C-five", "B-four") else None
        results["final"][tag] = finish(tag, site_of[tag], solution, expect)
    sites_e = sites
    added = [o[0] for o in sites_e.orbits if o[0] not in seed]
    results["final_site_set"] = {"orbits": len(sites_e.orbits), "sites": sites_e.size,
                                 "added_orbits": [[str(x), str(y)] for x, y in added]}
    results["wall_seconds"] = round(time.perf_counter() - t0, 1)
    (args.out / "results.json").write_text(json.dumps(results, indent=1, default=str))
    log(handle, "done " + json.dumps({k: v for k, v in results["final"].items()}, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `bounded_ceiling.py`

```text
"""BC-293: an exact lower bound on the mass of every valid D4 measure on a fixed
(L, B, net) whose named atoms carry at least the named weights.

Weak duality for the bounded covering program. Let mu be valid (every closed B-square
at a net direction with centre in the centre domain has mass >= 1), D4-symmetric, with
mu({p}) >= lb_p at each bounded atom p. Let (P_r, y_r) be placements with y_r >= 0 and
let depth(q) = sum of y_r over the r with q in the closed P_r, symmetrised over D4 (the
symmetrised depth integrates the same against a D4-invariant mu). With
D = max(1, max_q depth(q)):

    sum_r y_r / D <= sum_r (y_r / D) mu(P_r) = integral of depth/D dmu
                  <= mu(free atoms) + sum_p (depth(p)/D) mu({p})

so  M(mu) = mu(free) + sum_p mu({p}) >= sum_r y_r / D + sum_p (1 - depth(p)/D) mu({p})
           >= sum_r y_r / D + sum_p (1 - depth(p)/D) lb_p,

because 1 - depth(p)/D >= 0. Everything below is decided in Fraction arithmetic: the
depth maximum is attained at a vertex of the arrangement of the squares' edge lines and
the walls (coverage by closed squares is upper semicontinuous), the float depths only
screen, and every vertex near the maximum is re-decided exactly, as `colgen.check_ceiling`
does for the free program.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from sqpack.fractional.colgen import (
    Square,
    _arrangement_lines,
    _depths,
    _exact_intersection,
    _float_squares,
    _vertices,
    symmetrise,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dual", type=Path, required=True)
    parser.add_argument("--decide", type=int, default=3000, help="vertices decided exactly, from the top")
    parser.add_argument("--support-cap", type=int, default=120,
                        help="keep the heaviest rows only; discarding dual weight only weakens the floor")
    args = parser.parse_args(argv)
    record = json.loads(args.dual.read_text())
    L = Fraction(record["outer_side"])
    weighted = tuple(
        (Square(*(Fraction(v) for v in row[:7])), Fraction(row[7])) for row in record["squares"]
    )
    full_total = sum((w for _, w in weighted), start=Fraction(0))
    weighted = tuple(sorted(weighted, key=lambda item: -item[1])[: args.support_cap])
    bounded = [((Fraction(x), Fraction(y)), Fraction(lb)) for x, y, lb in record["bounded"]]
    priced = [((Fraction(x), Fraction(y)), Fraction(c)) for x, y, c in record.get("priced", [])]
    family = symmetrise(weighted)
    total = sum((w for _, w in family), start=Fraction(0))
    axes, offsets, floats, half = _float_squares(family)
    lines = _arrangement_lines(family, L)
    points, sources = _vertices(lines, L)
    depths = _depths(points, axes, offsets, floats, half, slack=1e-9)
    # Soundness of the maximum. With the 1e-9 slack the float depth of a vertex is an
    # upper bound on its exact depth, so every vertex whose float depth is below a
    # threshold T has exact depth below T. Decide exactly every vertex at or above T and
    # take D = max(exact maximum found, T): an upper bound on the true maximum depth,
    # which is what the floor needs. T is the largest value that leaves at most
    # --decide vertices to decide, and never below 1.
    order = np.argsort(-depths)
    cut = min(args.decide, order.size) - 1
    T = max(1.0, float(depths[order[cut]])) if order.size else 1.0
    near = np.flatnonzero(depths >= T)
    worst = Fraction(0)
    worst_at = None
    for index in near:
        exact = _exact_intersection(lines[sources[index][0]], lines[sources[index][1]])
        if exact is None:
            continue
        depth = sum((w for sq, w in family if sq.covers(exact[0], exact[1])), start=Fraction(0))
        if depth > worst:
            worst, worst_at = depth, exact
    threshold = Fraction(T)
    D_from_vertices = max(worst, threshold)
    centre = L / 2
    # Priced atoms (per-atom objective cost c_p < 1): the dual needs depth(p) <= c_p D there,
    # so D also absorbs depth(p) / c_p; the floor is then total / D on the priced objective.
    priced_depths = []
    for (x, y), c in priced:
        depth = sum((w for sq, w in family if sq.covers(x - centre, y - centre)), start=Fraction(0))
        priced_depths.append({"atom": [str(x), str(y)], "cost": str(c), "depth": str(depth), "depth_over_cost": str(depth / c)})
    D = max(Fraction(1), D_from_vertices, *[Fraction(d["depth_over_cost"]) for d in priced_depths])
    per_atom = []
    correction = Fraction(0)
    for (x, y), lb in bounded:
        depth = sum((w for sq, w in family if sq.covers(x - centre, y - centre)), start=Fraction(0))
        term = (1 - depth / D) * lb
        correction += term
        per_atom.append({"atom": [str(x), str(y)], "lb": str(lb), "depth": str(depth), "term": str(term)})
    bound = total / D + correction
    out = {
        "dual": str(args.dual), "tag": record.get("tag"), "lp_objective": record.get("objective"),
        "squares": len(weighted), "squares_in_dual": len(record["squares"]), "full_dual_weight": str(full_total),
        "full_dual_weight_float": float(full_total), "symmetrised": len(family), "vertices": int(points.shape[0]),
        "decided_exactly": int(near.size), "threshold_T": T, "total_weight": str(total), "total_float": float(total),
        "max_exact_depth_decided": float(worst), "D_from_vertices": float(D_from_vertices),
        "max_depth_at": None if worst_at is None else [str(worst_at[0]), str(worst_at[1])],
        "D": str(D), "D_float": float(D), "bounded_atoms": per_atom, "priced_atoms": priced_depths, "correction": str(correction),
        "lower_bound": str(bound), "lower_bound_float": float(bound),
    }
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `transfer_dry_run.py`

```text
"""BC-293, Lemma C dry run: which D4-equivariant displacements of a heavy orbit keep a
measure valid at its own (L, B, net)?

For a valid measure mu of mass 11 + eps and an atom p of weight w > eps, Lemma C says
that if mu' = mu - w delta_p + w delta_{p'} is also valid then the core owning p contains
p'. The whole D4 orbit is moved together so that Condition 1 survives; the orbit members
are pairwise farther apart than B sqrt 2 plus twice the displacement, so no core meets
two moved atoms and the lemma applies to each member separately.

Every verdict here is the exact eighth-turn sweep (`certificate.verify`, workers=1);
mass is irrelevant to validity and is reported only as context.
"""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate, d4_images, verify
from sqpack.fractional.model import Atom


def load(path: Path) -> Certificate:
    record = json.loads(path.read_text())
    atoms = tuple(
        Atom(f"{i:04d}", Fraction(x), Fraction(y), Fraction(w))
        for i, (x, y, w) in enumerate(record["atoms"])
    )
    steps = int(record["direction_steps"])
    limit = Fraction(record["angle_limit"])
    return Certificate(
        n=11,
        outer_side=Fraction(record["outer_side"]),
        square_side=Fraction(record["square_side"]),
        atoms=atoms,
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
    )


def valid(cert: Certificate) -> tuple[bool, list, Fraction | None]:
    verdict = verify(cert, workers=1)
    conds = [(c.name, c.holds, c.detail) for c in verdict.conditions]
    ok = all(h for n_, h, _ in conds if not n_.startswith("Condition 2"))
    return ok, conds, verdict.minimum_cell_mass


def moved(cert: Certificate, source: tuple[Fraction, Fraction], d: tuple[Fraction, Fraction]) -> Certificate:
    """Move the orbit of `source` by the D4-equivariant image of `d`."""

    L = cert.outer_side
    # Map each orbit member to its own displacement: the image of (source + d) under the
    # same symmetry that produced the member.
    images = d4_images(source[0], source[1], L)
    targets = d4_images(source[0] + d[0], source[1] + d[1], L)
    move = {img: tgt for img, tgt in zip(images, targets, strict=True)}
    atoms = []
    for a in cert.atoms:
        key = (a.x, a.y)
        if key in move:
            tx, ty = move[key]
            atoms.append(Atom(a.label, tx, ty, a.weight))
        else:
            atoms.append(a)
    return Certificate(
        n=cert.n, outer_side=L, square_side=cert.square_side, atoms=tuple(atoms),
        half_tangents=cert.half_tangents,
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measure", type=Path, required=True)
    parser.add_argument("--radii", default="1/1000,1/200,1/50")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    cert = load(args.measure)
    L, B = cert.outer_side, cert.square_side
    heaviest = max(cert.atoms, key=lambda a: a.weight)
    source = (heaviest.x, heaviest.y)
    # The heaviest atom is on the diagonal mirror in every measure here; pick the member
    # nearest the origin corner as the representative.
    source = min(d4_images(source[0], source[1], L))
    mass = cert.total_mass
    eps = mass - 11
    w = heaviest.weight
    started = time.perf_counter()
    base_ok, base_conds, base_least = valid(cert)
    base_s = time.perf_counter() - started
    report = {
        "measure": str(args.measure), "L": str(L), "B": str(B), "atoms": len(cert.atoms),
        "mass": str(mass), "eps": str(eps), "heavy_atom": [str(source[0]), str(source[1])],
        "heavy_weight": str(w), "w_gt_eps": w > eps,
        "base_valid": base_ok, "base_least_cell": str(base_least), "base_sweep_s": round(base_s, 1),
        "moves": [],
    }
    print(json.dumps({k: v for k, v in report.items() if k != "moves"}), flush=True)
    if not base_ok:
        print("base measure is not valid; nothing to transfer", flush=True)
        args.out.write_text(json.dumps(report, indent=1))
        return 1
    radii = [Fraction(r) for r in args.radii.split(",")]
    # The heavy atom lies on the diagonal mirror, so only displacements along that mirror
    # keep its orbit a four-point orbit and the moved measure D4-closed; an off-diagonal
    # displacement would split the orbit into eight, which is the disjunctive form of
    # Lemma C and not the dry run's object.
    directions = [("+diag", (1, 1)), ("-diag", (-1, -1))]
    for r in radii:
        for name, (dx, dy) in directions:
            d = (r * dx, r * dy)
            started = time.perf_counter()
            cert2 = moved(cert, source, d)
            ok, conds, least = valid(cert2)
            entry = {
                "radius": str(r), "direction": name, "d": [str(d[0]), str(d[1])],
                "valid": ok, "least_cell": str(least),
                "failed": [n_ for n_, h, _ in conds if not h and not n_.startswith("Condition 2")],
                "seconds": round(time.perf_counter() - started, 1),
            }
            report["moves"].append(entry)
            print(json.dumps(entry), flush=True)
            args.out.write_text(json.dumps(report, indent=1))
    surviving = [m for m in report["moves"] if m["valid"]]
    report["surviving"] = len(surviving)
    args.out.write_text(json.dumps(report, indent=1))
    print(f"surviving displacements: {len(surviving)} of {len(report['moves'])}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Command lines

```text
# every run: from <worktree>/packing, one process, PACK_JOBS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
# run1 (seed only, control)
uv run --frozen --all-extras --group dev python bounded_colgen.py --seed-certificate cases/n11_fractional_certificate/certificate.json --out run1 --column-rounds 4 --deadline-b 1800 --deadline-a 1200 --deadline-c 600
# run2 (decision; phases B A C D E)
uv run --frozen --all-extras --group dev python bounded_colgen.py --seed-certificate cases/n11_fractional_certificate/certificate.json --grid-counts auto --out run2 --column-rounds 10 --deadline-b 1500 --deadline-a 1200 --deadline-c 600
# run4 (replay of run2 with the duals saved and phase F)
uv run --frozen --all-extras --group dev python bounded_colgen.py --seed-certificate cases/n11_fractional_certificate/certificate.json --grid-counts auto --out run4 --column-rounds 10 --deadline-b 1500 --deadline-a 1200 --deadline-c 600
# floors on run4's duals (the sound threshold rule)
uv run --frozen --all-extras --group dev python bounded_ceiling.py --dual run4/dual-<tag>.json --support-cap 120 --decide 3000
# run6 (four-bound only, settling attempt)
uv run --frozen --all-extras --group dev python bounded_colgen.py --seed-certificate cases/n11_fractional_certificate/certificate.json --grid-counts auto --out run6 --phases B --column-rounds 60 --columns-per-round 6 --settle 0.005 --support-cap 200 --deadline-b 2100
uv run --frozen --all-extras --group dev python bounded_ceiling.py --dual run6/dual-B-four.json --support-cap 200 --decide 3000
# run5 (free, then the pair orbit priced)
uv run --frozen --all-extras --group dev python bounded_colgen.py --seed-certificate cases/n11_fractional_certificate/certificate.json --grid-counts auto --out run5 --phases AG --column-rounds 10 --deadline-a 600 --deadline-c 600
# Lemma C dry run on T-018
uv run --frozen --all-extras --group dev python transfer_dry_run.py --measure cases/n11_fractional_certificate/certificate.json --radii 1/1000,1/100 --out transfer-t018.json
```

### `run1/run.log` (column rounds, rationalisation and sweep lines)

```text
[04:35:20] inputs {"side": "96/25", "shrink": "9977/10000", "angle_limit": "207107/500000", "direction_steps": 180, "seed": "cases/n11_fractional_certificate/certificate.json", "seed_ratio": "128/127", "seed_sites": 1121, "grid_counts": "", "orbits": 149, "sites": 1121, "corner_orbit": [["29586032/29422725", "29586032/29422725"], ["29586032/29422725", "83397232/29422725"], ["83397232/29422725", "2
[04:36:58] B-four column round 0: {"phase": "B-four", "column_round": 0, "rows": 2337, "orbits": 149, "sites": 1121, "objective": 12.583458646615542, "lp_rounds": 17, "least_covered": 0.9999999999996468, "stopped": "converged: every placement covers mass 1", "depth": 1.1353383458646618, "seconds": 97.8}
[04:37:01] B-four column round 1: {"phase": "B-four", "column_round": 1, "rows": 2381, "orbits": 150, "sites": 1125, "objective": 12.583458646612968, "lp_rounds": 4, "least_covered": 0.9999999999985756, "stopped": "converged: every placement covers mass 1", "depth": 1.4454887218045114, "seconds": 2.8}
[04:37:06] B-four column round 2: {"phase": "B-four", "column_round": 2, "rows": 2615, "orbits": 151, "sites": 1133, "objective": 12.582926829268368, "lp_rounds": 9, "least_covered": 0.99999999999978, "stopped": "converged: every placement covers mass 1", "depth": 1.228658536585366, "seconds": 5.8}
[04:37:09] B-four column round 3: {"phase": "B-four", "column_round": 3, "rows": 2726, "orbits": 152, "sites": 1141, "objective": 12.547549770291615, "lp_rounds": 3, "least_covered": 0.9999999999996898, "stopped": "converged: every placement covers mass 1", "depth": 1.4687978560490047, "seconds": 2.5}
[04:37:17] A-free column round 0: {"phase": "A-free", "column_round": 0, "rows": 2984, "orbits": 152, "sites": 1141, "objective": 12.248000000000012, "lp_rounds": 10, "least_covered": 0.9999999999999764, "stopped": "converged: every placement covers mass 1", "depth": 1.54, "seconds": 7.7}
[04:37:22] A-free column round 1: {"phase": "A-free", "column_round": 1, "rows": 3287, "orbits": 153, "sites": 1149, "objective": 12.208602150537564, "lp_rounds": 7, "least_covered": 0.9999999999998801, "stopped": "converged: every placement covers mass 1", "depth": 1.5989247311827957, "seconds": 5.3}
[04:37:27] A-free column round 2: {"phase": "A-free", "column_round": 2, "rows": 3521, "orbits": 154, "sites": 1153, "objective": 12.103825136612095, "lp_rounds": 6, "least_covered": 0.9999999999996054, "stopped": "converged: every placement covers mass 1", "depth": 1.5778688524590163, "seconds": 4.8}
[04:37:28] A-free column round 3: {"phase": "A-free", "column_round": 3, "rows": 3525, "orbits": 155, "sites": 1161, "objective": 12.103825136612485, "lp_rounds": 2, "least_covered": 0.9999999999995376, "stopped": "converged: every placement covers mass 1", "depth": 1.6120218579234973, "seconds": 1.6}
[04:37:29] C-five column round 0: {"phase": "C-five", "column_round": 0, "rows": 3525, "orbits": 155, "sites": 1161, "objective": 12.531451612902355, "lp_rounds": 1, "least_covered": 0.9999999999990206, "stopped": "converged: every placement covers mass 1", "depth": 1.4516129032258065, "seconds": 0.6}
[04:37:30] D-free-final column round 0: {"phase": "D-free-final", "column_round": 0, "rows": 3525, "orbits": 155, "sites": 1161, "objective": 12.103825136612485, "lp_rounds": 1, "least_covered": 0.9999999999995376, "stopped": "converged: every placement covers mass 1", "depth": 1.6120218579234973, "seconds": 1.0}
[04:37:32] E-four-final column round 0: {"phase": "E-four-final", "column_round": 0, "rows": 3570, "orbits": 155, "sites": 1161, "objective": 12.504868913858248, "lp_rounds": 3, "least_covered": 0.9999999999995878, "stopped": "converged: every placement covers mass 1", "depth": 1.4302434456928839, "seconds": 2.1}
[04:37:32] E-four-final: rationalised mass 50019567/4000000 = 12.504891750 over 181 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(218727, 4000000)]
[04:37:38] E-four-final: sweep 5.8s; conditions [('Condition 1 atoms carry the declared symmetry', True, '181 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 50019567/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 
[04:37:38] C-five: rationalised mass 50125929/4000000 = 12.531482250 over 133 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(500001, 4000000)]
[04:37:42] C-five: sweep 4.4s; conditions [('Condition 1 atoms carry the declared symmetry', True, '133 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 50125929/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 9977/1
[04:37:42] D-free-final: rationalised mass 48415397/4000000 = 12.103849250 over 161 atoms; corner weights []; centre [Fraction(502733, 4000000)]
[04:37:48] D-free-final: sweep 5.5s; conditions [('Condition 1 atoms carry the declared symmetry', True, '161 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 48415397/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 
```

### `run2/run.log` (column rounds, rationalisation and sweep lines)

```text
[04:38:25] inputs {"side": "96/25", "shrink": "9977/10000", "angle_limit": "207107/500000", "direction_steps": 180, "seed": "cases/n11_fractional_certificate/certificate.json", "seed_ratio": "128/127", "seed_sites": 1121, "grid_counts": [25, 34, 42], "orbits": 619, "sites": 4645, "corner_orbit": [["29586032/29422725", "29586032/29422725"], ["29586032/29422725", "83397232/29422725"], ["83397232/294
[04:39:28] B-four column round 0: {"phase": "B-four", "column_round": 0, "rows": 5256, "orbits": 619, "sites": 4645, "objective": 11.849054621847776, "lp_rounds": 20, "least_covered": 0.9999999999944693, "stopped": "converged: every placement covers mass 1", "depth": 1.262079831932773, "seconds": 63.4}
[04:39:37] B-four column round 1: {"phase": "B-four", "column_round": 1, "rows": 5331, "orbits": 620, "sites": 4653, "objective": 11.849054621847934, "lp_rounds": 2, "least_covered": 0.9999999999979068, "stopped": "converged: every placement covers mass 1", "depth": 1.0172284823020117, "seconds": 8.4}
[04:39:44] B-four column round 2: {"phase": "B-four", "column_round": 2, "rows": 5340, "orbits": 621, "sites": 4661, "objective": 11.849054621848705, "lp_rounds": 2, "least_covered": 0.9999999999998193, "stopped": "converged: every placement covers mass 1", "depth": 1.388422035480859, "seconds": 6.9}
[04:39:49] B-four column round 3: {"phase": "B-four", "column_round": 3, "rows": 5340, "orbits": 622, "sites": 4665, "objective": 11.849054621849463, "lp_rounds": 1, "least_covered": 0.9999999999964111, "stopped": "converged: every placement covers mass 1", "depth": 1.333732308712959, "seconds": 4.8}
[04:40:01] B-four column round 4: {"phase": "B-four", "column_round": 4, "rows": 5424, "orbits": 623, "sites": 4673, "objective": 11.84905462185005, "lp_rounds": 2, "least_covered": 0.9999999999990465, "stopped": "converged: every placement covers mass 1", "depth": 1.344500300120048, "seconds": 12.0}
[04:40:08] B-four column round 5: {"phase": "B-four", "column_round": 5, "rows": 5424, "orbits": 624, "sites": 4681, "objective": 11.849054621868067, "lp_rounds": 1, "least_covered": 0.9999999999478997, "stopped": "converged: every placement covers mass 1", "depth": 1.3684799233386489, "seconds": 7.0}
[04:40:17] B-four column round 6: {"phase": "B-four", "column_round": 6, "rows": 5424, "orbits": 625, "sites": 4689, "objective": 11.849054621848865, "lp_rounds": 1, "least_covered": 0.9999999999999787, "stopped": "converged: every placement covers mass 1", "depth": 1.323741515837104, "seconds": 8.9}
[04:40:54] B-four column round 7: {"phase": "B-four", "column_round": 7, "rows": 6162, "orbits": 626, "sites": 4697, "objective": 11.798148880686648, "lp_rounds": 9, "least_covered": 0.9999999999986957, "stopped": "converged: every placement covers mass 1", "depth": 1.331111611542067, "seconds": 37.1}
[04:41:04] B-four column round 8: {"phase": "B-four", "column_round": 8, "rows": 6334, "orbits": 627, "sites": 4705, "objective": 11.798148880652594, "lp_rounds": 2, "least_covered": 0.999999999990242, "stopped": "converged: every placement covers mass 1", "depth": 1.2937024222728948, "seconds": 9.7}
[04:41:25] B-four column round 9: {"phase": "B-four", "column_round": 9, "rows": 6338, "orbits": 628, "sites": 4713, "objective": 11.798148880656132, "lp_rounds": 2, "least_covered": 0.9999999999971597, "stopped": "converged: every placement covers mass 1", "depth": 1.289960946491203, "seconds": 21.2}
[04:42:31] A-free column round 0: {"phase": "A-free", "column_round": 0, "rows": 7468, "orbits": 628, "sites": 4713, "objective": 11.262576058879532, "lp_rounds": 11, "least_covered": 0.9999999999977146, "stopped": "converged: every placement covers mass 1", "depth": 1.38908865132656, "seconds": 65.7}
[04:42:38] A-free column round 1: {"phase": "A-free", "column_round": 1, "rows": 7468, "orbits": 629, "sites": 4721, "objective": 11.262576058892813, "lp_rounds": 1, "least_covered": 0.9999999999996492, "stopped": "converged: every placement covers mass 1", "depth": 1.3906804636751324, "seconds": 7.2}
[04:42:52] A-free column round 2: {"phase": "A-free", "column_round": 2, "rows": 7515, "orbits": 630, "sites": 4725, "objective": 11.262576058892462, "lp_rounds": 2, "least_covered": 0.9999999999985315, "stopped": "converged: every placement covers mass 1", "depth": 1.3906804636743664, "seconds": 13.9}
[04:43:16] A-free column round 3: {"phase": "A-free", "column_round": 3, "rows": 7612, "orbits": 631, "sites": 4729, "objective": 11.262035286698529, "lp_rounds": 4, "least_covered": 0.9999999999947481, "stopped": "converged: every placement covers mass 1", "depth": 1.3190576756470451, "seconds": 24.5}
[04:43:47] A-free column round 4: {"phase": "A-free", "column_round": 4, "rows": 7657, "orbits": 632, "sites": 4737, "objective": 11.262035286701805, "lp_rounds": 5, "least_covered": 0.9999999999995222, "stopped": "converged: every placement covers mass 1", "depth": 1.3041445140201637, "seconds": 31.0}
[04:44:01] A-free column round 5: {"phase": "A-free", "column_round": 5, "rows": 7664, "orbits": 633, "sites": 4745, "objective": 11.262035286704627, "lp_rounds": 2, "least_covered": 0.999999999999859, "stopped": "converged: every placement covers mass 1", "depth": 1.3738332939508506, "seconds": 13.2}
[04:44:07] A-free column round 6: {"phase": "A-free", "column_round": 6, "rows": 7664, "orbits": 634, "sites": 4753, "objective": 11.262035286704469, "lp_rounds": 1, "least_covered": 0.9999999999999958, "stopped": "converged: every placement covers mass 1", "depth": 1.3738332939508506, "seconds": 6.2}
[04:44:27] A-free column round 7: {"phase": "A-free", "column_round": 7, "rows": 8112, "orbits": 635, "sites": 4761, "objective": 11.26203528670447, "lp_rounds": 3, "least_covered": 0.9999999999999984, "stopped": "converged: every placement covers mass 1", "depth": 1.245532713715606, "seconds": 19.7}
[04:44:43] A-free column round 8: {"phase": "A-free", "column_round": 8, "rows": 8349, "orbits": 636, "sites": 4769, "objective": 11.262035286704448, "lp_rounds": 2, "least_covered": 0.999999999999968, "stopped": "converged: every placement covers mass 1", "depth": 1.1120968218327665, "seconds": 16.0}
[04:45:16] A-free column round 9: {"phase": "A-free", "column_round": 9, "rows": 8371, "orbits": 637, "sites": 4777, "objective": 11.26203528670448, "lp_rounds": 2, "least_covered": 0.9999999999999976, "stopped": "converged: every placement covers mass 1", "depth": 1.133869427378702, "seconds": 33.1}
[04:45:47] C-five column round 0: {"phase": "C-five", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.81915327612074, "lp_rounds": 4, "least_covered": 0.9999999999999989, "stopped": "converged: every placement covers mass 1", "depth": 1.22776063487776, "seconds": 30.5}
[04:45:55] D-free-final column round 0: {"phase": "D-free-final", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.262035286704476, "lp_rounds": 1, "least_covered": 0.9999999999999993, "stopped": "converged: every placement covers mass 1", "depth": 1.2057382738654523, "seconds": 8.0}
[04:46:01] E-four-final column round 0: {"phase": "E-four-final", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.798148880653619, "lp_rounds": 1, "least_covered": 0.9999999999999812, "stopped": "converged: every placement covers mass 1", "depth": 1.1036015574918459, "seconds": 6.1}
[04:46:01] E-four-final: rationalised mass 23596423/2000000 = 11.798211500 over 401 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(41, 16000)]
[04:46:15] E-four-final: sweep 13.7s; conditions [('Condition 1 atoms carry the declared symmetry', True, '401 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 23596423/2000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B =
[04:46:15] C-five: rationalised mass 47276821/4000000 = 11.819205250 over 369 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(500001, 4000000)]
[04:46:27] C-five: sweep 12.5s; conditions [('Condition 1 atoms carry the declared symmetry', True, '369 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 47276821/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 9977/
[04:46:27] D-free-final: rationalised mass 22524199/2000000 = 11.262099500 over 377 atoms; corner weights []; centre [Fraction(9767, 2000000)]
[04:46:40] D-free-final: sweep 12.7s; conditions [('Condition 1 atoms carry the declared symmetry', True, '377 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 22524199/2000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B =
```

### `run4/run.log` (column rounds, rationalisation and sweep lines)

```text
[04:48:32] inputs {"side": "96/25", "shrink": "9977/10000", "angle_limit": "207107/500000", "direction_steps": 180, "seed": "cases/n11_fractional_certificate/certificate.json", "seed_ratio": "128/127", "seed_sites": 1121, "grid_counts": [25, 34, 42], "orbits": 619, "sites": 4645, "corner_orbit": [["29586032/29422725", "29586032/29422725"], ["29586032/29422725", "83397232/29422725"], ["83397232/294
[04:49:42] B-four column round 0: {"phase": "B-four", "column_round": 0, "rows": 5256, "orbits": 619, "sites": 4645, "objective": 11.849054621847776, "lp_rounds": 20, "least_covered": 0.9999999999944693, "stopped": "converged: every placement covers mass 1", "depth": 1.262079831932773, "seconds": 69.4}
[04:49:51] B-four column round 1: {"phase": "B-four", "column_round": 1, "rows": 5331, "orbits": 620, "sites": 4653, "objective": 11.849054621847934, "lp_rounds": 2, "least_covered": 0.9999999999979068, "stopped": "converged: every placement covers mass 1", "depth": 1.0172284823020117, "seconds": 9.3}
[04:49:59] B-four column round 2: {"phase": "B-four", "column_round": 2, "rows": 5340, "orbits": 621, "sites": 4661, "objective": 11.849054621848705, "lp_rounds": 2, "least_covered": 0.9999999999998193, "stopped": "converged: every placement covers mass 1", "depth": 1.388422035480859, "seconds": 8.2}
[04:50:05] B-four column round 3: {"phase": "B-four", "column_round": 3, "rows": 5340, "orbits": 622, "sites": 4665, "objective": 11.849054621849463, "lp_rounds": 1, "least_covered": 0.9999999999964111, "stopped": "converged: every placement covers mass 1", "depth": 1.333732308712959, "seconds": 5.6}
[04:50:16] B-four column round 4: {"phase": "B-four", "column_round": 4, "rows": 5424, "orbits": 623, "sites": 4673, "objective": 11.84905462185005, "lp_rounds": 2, "least_covered": 0.9999999999990465, "stopped": "converged: every placement covers mass 1", "depth": 1.344500300120048, "seconds": 10.5}
[04:50:21] B-four column round 5: {"phase": "B-four", "column_round": 5, "rows": 5424, "orbits": 624, "sites": 4681, "objective": 11.849054621868067, "lp_rounds": 1, "least_covered": 0.9999999999478997, "stopped": "converged: every placement covers mass 1", "depth": 1.3684799233386489, "seconds": 5.1}
[04:50:26] B-four column round 6: {"phase": "B-four", "column_round": 6, "rows": 5424, "orbits": 625, "sites": 4689, "objective": 11.849054621848865, "lp_rounds": 1, "least_covered": 0.9999999999999787, "stopped": "converged: every placement covers mass 1", "depth": 1.323741515837104, "seconds": 5.1}
[04:51:16] B-four column round 7: {"phase": "B-four", "column_round": 7, "rows": 6162, "orbits": 626, "sites": 4697, "objective": 11.798148880686648, "lp_rounds": 9, "least_covered": 0.9999999999986957, "stopped": "converged: every placement covers mass 1", "depth": 1.331111611542067, "seconds": 50.2}
[04:51:32] B-four column round 8: {"phase": "B-four", "column_round": 8, "rows": 6334, "orbits": 627, "sites": 4705, "objective": 11.798148880652594, "lp_rounds": 2, "least_covered": 0.999999999990242, "stopped": "converged: every placement covers mass 1", "depth": 1.2937024222728948, "seconds": 15.6}
[04:51:50] B-four column round 9: {"phase": "B-four", "column_round": 9, "rows": 6338, "orbits": 628, "sites": 4713, "objective": 11.798148880656132, "lp_rounds": 2, "least_covered": 0.9999999999971597, "stopped": "converged: every placement covers mass 1", "depth": 1.289960946491203, "seconds": 18.1}
[04:53:27] A-free column round 0: {"phase": "A-free", "column_round": 0, "rows": 7468, "orbits": 628, "sites": 4713, "objective": 11.262576058879532, "lp_rounds": 11, "least_covered": 0.9999999999977146, "stopped": "converged: every placement covers mass 1", "depth": 1.38908865132656, "seconds": 97.5}
[04:53:39] A-free column round 1: {"phase": "A-free", "column_round": 1, "rows": 7468, "orbits": 629, "sites": 4721, "objective": 11.262576058892813, "lp_rounds": 1, "least_covered": 0.9999999999996492, "stopped": "converged: every placement covers mass 1", "depth": 1.3906804636751324, "seconds": 11.3}
[04:54:01] A-free column round 2: {"phase": "A-free", "column_round": 2, "rows": 7515, "orbits": 630, "sites": 4725, "objective": 11.262576058892462, "lp_rounds": 2, "least_covered": 0.9999999999985315, "stopped": "converged: every placement covers mass 1", "depth": 1.3906804636743664, "seconds": 21.9}
[04:54:35] A-free column round 3: {"phase": "A-free", "column_round": 3, "rows": 7612, "orbits": 631, "sites": 4729, "objective": 11.262035286698529, "lp_rounds": 4, "least_covered": 0.9999999999947481, "stopped": "converged: every placement covers mass 1", "depth": 1.3190576756470451, "seconds": 34.0}
[04:55:22] A-free column round 4: {"phase": "A-free", "column_round": 4, "rows": 7657, "orbits": 632, "sites": 4737, "objective": 11.262035286701805, "lp_rounds": 5, "least_covered": 0.9999999999995222, "stopped": "converged: every placement covers mass 1", "depth": 1.3041445140201637, "seconds": 47.2}
[04:55:43] A-free column round 5: {"phase": "A-free", "column_round": 5, "rows": 7664, "orbits": 633, "sites": 4745, "objective": 11.262035286704627, "lp_rounds": 2, "least_covered": 0.999999999999859, "stopped": "converged: every placement covers mass 1", "depth": 1.3738332939508506, "seconds": 20.3}
[04:55:54] A-free column round 6: {"phase": "A-free", "column_round": 6, "rows": 7664, "orbits": 634, "sites": 4753, "objective": 11.262035286704469, "lp_rounds": 1, "least_covered": 0.9999999999999958, "stopped": "converged: every placement covers mass 1", "depth": 1.3738332939508506, "seconds": 11.0}
[04:56:26] A-free column round 7: {"phase": "A-free", "column_round": 7, "rows": 8112, "orbits": 635, "sites": 4761, "objective": 11.26203528670447, "lp_rounds": 3, "least_covered": 0.9999999999999984, "stopped": "converged: every placement covers mass 1", "depth": 1.245532713715606, "seconds": 31.9}
[04:56:47] A-free column round 8: {"phase": "A-free", "column_round": 8, "rows": 8349, "orbits": 636, "sites": 4769, "objective": 11.262035286704448, "lp_rounds": 2, "least_covered": 0.999999999999968, "stopped": "converged: every placement covers mass 1", "depth": 1.1120968218327665, "seconds": 20.9}
[04:57:10] A-free column round 9: {"phase": "A-free", "column_round": 9, "rows": 8371, "orbits": 637, "sites": 4777, "objective": 11.26203528670448, "lp_rounds": 2, "least_covered": 0.9999999999999976, "stopped": "converged: every placement covers mass 1", "depth": 1.133869427378702, "seconds": 23.3}
[04:57:49] C-five column round 0: {"phase": "C-five", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.81915327612074, "lp_rounds": 4, "least_covered": 0.9999999999999989, "stopped": "converged: every placement covers mass 1", "depth": 1.22776063487776, "seconds": 38.2}
[04:58:02] D-free-final column round 0: {"phase": "D-free-final", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.262035286704476, "lp_rounds": 1, "least_covered": 0.9999999999999993, "stopped": "converged: every placement covers mass 1", "depth": 1.2057382738654523, "seconds": 13.2}
[04:58:13] E-four-final column round 0: {"phase": "E-four-final", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.798148880653619, "lp_rounds": 1, "least_covered": 0.9999999999999812, "stopped": "converged: every placement covers mass 1", "depth": 1.1036015574918459, "seconds": 11.3}
[04:58:26] F-priced column round 0: {"phase": "F-priced", "column_round": 0, "rows": 8517, "orbits": 637, "sites": 4777, "objective": 11.262035286704473, "lp_rounds": 1, "least_covered": 0.9999999999999982, "stopped": "converged: every placement covers mass 1", "depth": 1.2352340304032767, "seconds": 13.2}
[04:59:29] F-priced column round 1: {"phase": "F-priced", "column_round": 1, "rows": 8985, "orbits": 638, "sites": 4785, "objective": 11.252735350531731, "lp_rounds": 6, "least_covered": 0.9999999999999948, "stopped": "converged: every placement covers mass 1", "depth": 1.1898630114595954, "seconds": 63.0}
[05:00:14] F-priced column round 2: {"phase": "F-priced", "column_round": 2, "rows": 9192, "orbits": 639, "sites": 4789, "objective": 11.2496854513501, "lp_rounds": 4, "least_covered": 0.9999999999999847, "stopped": "converged: every placement covers mass 1", "depth": 1.3095893778880068, "seconds": 44.8}
[05:01:18] F-priced column round 3: {"phase": "F-priced", "column_round": 3, "rows": 9391, "orbits": 640, "sites": 4797, "objective": 11.208349397971096, "lp_rounds": 6, "least_covered": 0.9999999999999918, "stopped": "converged: every placement covers mass 1", "depth": 1.114541130739816, "seconds": 64.0}
[05:01:39] F-priced column round 4: {"phase": "F-priced", "column_round": 4, "rows": 9421, "orbits": 641, "sites": 4805, "objective": 11.208349397971116, "lp_rounds": 2, "least_covered": 0.9999999999999976, "stopped": "converged: every placement covers mass 1", "depth": 1.0207352337009765, "seconds": 20.8}
[05:01:50] F-priced column round 5: {"phase": "F-priced", "column_round": 5, "rows": 9421, "orbits": 642, "sites": 4813, "objective": 11.208349397971125, "lp_rounds": 1, "least_covered": 0.9999999999999958, "stopped": "converged: every placement covers mass 1", "depth": 1.298353506304712, "seconds": 10.2}
[05:01:59] F-priced column round 6: {"phase": "F-priced", "column_round": 6, "rows": 9421, "orbits": 643, "sites": 4821, "objective": 11.208349397971112, "lp_rounds": 1, "least_covered": 0.9999999999999969, "stopped": "converged: every placement covers mass 1", "depth": 1.1254420408937205, "seconds": 9.6}
[05:03:55] F-priced column round 7: {"phase": "F-priced", "column_round": 7, "rows": 9934, "orbits": 644, "sites": 4829, "objective": 11.18957355796806, "lp_rounds": 8, "least_covered": 0.9999999999999994, "stopped": "converged: every placement covers mass 1", "depth": 1.1292533636470434, "seconds": 115.6}
[05:04:11] F-priced column round 8: {"phase": "F-priced", "column_round": 8, "rows": 9934, "orbits": 645, "sites": 4837, "objective": 11.189559665759083, "lp_rounds": 1, "least_covered": 0.9999999999999991, "stopped": "converged: every placement covers mass 1", "depth": 1.1936672612900197, "seconds": 16.1}
[05:04:29] F-priced column round 9: {"phase": "F-priced", "column_round": 9, "rows": 9934, "orbits": 646, "sites": 4845, "objective": 11.189559665759083, "lp_rounds": 1, "least_covered": 0.9999999999999987, "stopped": "converged: every placement covers mass 1", "depth": 1.0882441919903192, "seconds": 17.3}
[05:04:29] E-four-final: rationalised mass 23596423/2000000 = 11.798211500 over 401 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(41, 16000)]
[05:04:56] E-four-final: sweep 27.3s; conditions [('Condition 1 atoms carry the declared symmetry', True, '401 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 23596423/2000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B =
[05:04:56] F-priced: rationalised mass 44758451/4000000 = 11.189612750 over 373 atoms; corner weights []; centre [Fraction(38307, 4000000)]
[05:05:19] F-priced: sweep 22.6s; conditions [('Condition 1 atoms carry the declared symmetry', True, '373 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 44758451/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 997
[05:05:19] C-five: rationalised mass 47276821/4000000 = 11.819205250 over 369 atoms; corner weights [Fraction(600001, 4000000)]; centre [Fraction(500001, 4000000)]
[05:05:41] C-five: sweep 21.9s; conditions [('Condition 1 atoms carry the declared symmetry', True, '369 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 47276821/4000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 9977/
[05:05:41] D-free-final: rationalised mass 22524199/2000000 = 11.262099500 over 377 atoms; corner weights []; centre [Fraction(9767, 2000000)]
[05:05:57] D-free-final: sweep 16.5s; conditions [('Condition 1 atoms carry the declared symmetry', True, '377 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 22524199/2000000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B =
```

### `run5/run.log` (column rounds, rationalisation and sweep lines)

```text
[05:48:43] inputs {"side": "96/25", "shrink": "9977/10000", "angle_limit": "207107/500000", "direction_steps": 180, "seed": "cases/n11_fractional_certificate/certificate.json", "seed_ratio": "128/127", "seed_sites": 1121, "grid_counts": [25, 34, 42], "orbits": 619, "sites": 4645, "corner_orbit": [["29586032/29422725", "29586032/29422725"], ["29586032/29422725", "83397232/29422725"], ["83397232/294
[05:50:28] A-free column round 0: {"phase": "A-free", "column_round": 0, "rows": 4775, "orbits": 619, "sites": 4645, "objective": 11.386020301400558, "lp_rounds": 21, "least_covered": 0.9999999999999554, "stopped": "converged: every placement covers mass 1", "depth": 1.4692955083610197, "seconds": 105.3}
[05:51:11] A-free column round 1: {"phase": "A-free", "column_round": 1, "rows": 5696, "orbits": 620, "sites": 4653, "objective": 11.312613843371556, "lp_rounds": 7, "least_covered": 0.9999999999908187, "stopped": "converged: every placement covers mass 1", "depth": 1.3544512750455373, "seconds": 42.8}
[05:51:33] A-free column round 2: {"phase": "A-free", "column_round": 2, "rows": 5966, "orbits": 621, "sites": 4657, "objective": 11.312613843349265, "lp_rounds": 4, "least_covered": 0.9999999999997173, "stopped": "converged: every placement covers mass 1", "depth": 1.1522939435336976, "seconds": 22.1}
[05:51:53] A-free column round 3: {"phase": "A-free", "column_round": 3, "rows": 5986, "orbits": 622, "sites": 4665, "objective": 11.31261384335261, "lp_rounds": 3, "least_covered": 0.9999999999994427, "stopped": "converged: every placement covers mass 1", "depth": 1.3186902322404372, "seconds": 19.6}
[05:52:05] A-free column round 4: {"phase": "A-free", "column_round": 4, "rows": 6097, "orbits": 623, "sites": 4673, "objective": 11.312613843527284, "lp_rounds": 2, "least_covered": 0.9999999998135564, "stopped": "converged: every placement covers mass 1", "depth": 1.325165072859745, "seconds": 11.8}
[05:56:09] A-free column round 5: {"phase": "A-free", "column_round": 5, "rows": 7998, "orbits": 624, "sites": 4681, "objective": 11.237568832493164, "lp_rounds": 20, "least_covered": 0.9999999999999996, "stopped": "converged: every placement covers mass 1", "depth": 1.3276819944165668, "seconds": 244.6}
[05:58:02] A-free column round 6: {"phase": "A-free", "column_round": 6, "rows": 8351, "orbits": 625, "sites": 4685, "objective": 11.236212568665737, "lp_rounds": 10, "least_covered": 0.9999999999998073, "stopped": "converged: every placement covers mass 1", "depth": 1.0873280492096766, "seconds": 112.7}
[05:58:45] A-free column round 7: {"phase": "A-free", "column_round": 7, "rows": 8406, "orbits": 626, "sites": 4693, "objective": 11.232919611437643, "lp_rounds": 3, "least_covered": 0.9999999999991993, "stopped": "converged: every placement covers mass 1", "depth": 1.1960211304194466, "seconds": 42.7}
[05:58:52] A-free column round 8: {"phase": "A-free", "column_round": 8, "rows": 8406, "orbits": 627, "sites": 4701, "objective": 11.232919611436921, "lp_rounds": 0, "least_covered": Infinity, "stopped": "deadline reached after 0 rounds", "depth": NaN, "seconds": 6.5} | deadline reached after 0 rounds
[05:58:52] A-free: last column round unconverged (deadline reached after 0 rounds); returning the last converged solution
```

### `run6/run.log` (column rounds, rationalisation and sweep lines)

```text
[05:12:29] inputs {"side": "96/25", "shrink": "9977/10000", "angle_limit": "207107/500000", "direction_steps": 180, "seed": "cases/n11_fractional_certificate/certificate.json", "seed_ratio": "128/127", "seed_sites": 1121, "grid_counts": [25, 34, 42], "orbits": 619, "sites": 4645, "corner_orbit": [["29586032/29422725", "29586032/29422725"], ["29586032/29422725", "83397232/29422725"], ["83397232/294
[05:14:18] B-four column round 0: {"phase": "B-four", "column_round": 0, "rows": 5256, "orbits": 619, "sites": 4645, "objective": 11.849054621847776, "lp_rounds": 20, "least_covered": 0.9999999999944693, "stopped": "converged: every placement covers mass 1", "depth": 1.5273109243697478, "seconds": 109.2}
[05:14:29] B-four column round 1: {"phase": "B-four", "column_round": 1, "rows": 5256, "orbits": 625, "sites": 4685, "objective": 11.84905462184874, "lp_rounds": 1, "least_covered": 0.9999999999999996, "stopped": "converged: every placement covers mass 1", "depth": 1.4204397276151841, "seconds": 10.8}
[05:15:23] B-four column round 2: {"phase": "B-four", "column_round": 2, "rows": 5964, "orbits": 631, "sites": 4733, "objective": 11.84905462184874, "lp_rounds": 7, "least_covered": 0.9999999999999996, "stopped": "converged: every placement covers mass 1", "depth": 1.4453996510885057, "seconds": 53.9}
[05:15:39] B-four column round 3: {"phase": "B-four", "column_round": 3, "rows": 5964, "orbits": 637, "sites": 4769, "objective": 11.84905462184874, "lp_rounds": 1, "least_covered": 0.9999999999999999, "stopped": "converged: every placement covers mass 1", "depth": 1.3503526410564226, "seconds": 15.3}
[05:16:50] B-four column round 4: {"phase": "B-four", "column_round": 4, "rows": 6604, "orbits": 643, "sites": 4817, "objective": 11.837323804342452, "lp_rounds": 10, "least_covered": 0.9999999999999993, "stopped": "converged: every placement covers mass 1", "depth": 1.3676492408130967, "seconds": 70.5}
[05:18:26] B-four column round 5: {"phase": "B-four", "column_round": 5, "rows": 7457, "orbits": 649, "sites": 4861, "objective": 11.786100263011079, "lp_rounds": 10, "least_covered": 0.9999999999999954, "stopped": "converged: every placement covers mass 1", "depth": 1.2249898714168062, "seconds": 95.6}
[05:19:14] B-four column round 6: {"phase": "B-four", "column_round": 6, "rows": 7555, "orbits": 655, "sites": 4897, "objective": 11.786100263011082, "lp_rounds": 4, "least_covered": 0.9999999999999662, "stopped": "converged: every placement covers mass 1", "depth": 1.2135420817725353, "seconds": 47.7}
[05:19:59] B-four column round 7: {"phase": "B-four", "column_round": 7, "rows": 7722, "orbits": 661, "sites": 4945, "objective": 11.78610026301108, "lp_rounds": 3, "least_covered": 0.999999999999986, "stopped": "converged: every placement covers mass 1", "depth": 1.2112805850003985, "seconds": 44.7}
[05:20:29] B-four column round 8: {"phase": "B-four", "column_round": 8, "rows": 7732, "orbits": 667, "sites": 4993, "objective": 11.786100263011091, "lp_rounds": 2, "least_covered": 0.9999999999999967, "stopped": "converged: every placement covers mass 1", "depth": 1.2193900932493824, "seconds": 29.7}
[05:20:49] B-four column round 9: {"phase": "B-four", "column_round": 9, "rows": 7732, "orbits": 673, "sites": 5041, "objective": 11.786100263011079, "lp_rounds": 1, "least_covered": 0.999999999999993, "stopped": "converged: every placement covers mass 1", "depth": 1.206139913923647, "seconds": 18.8}
[05:21:50] B-four column round 10: {"phase": "B-four", "column_round": 10, "rows": 7980, "orbits": 679, "sites": 5089, "objective": 11.780396549418214, "lp_rounds": 7, "least_covered": 0.9999999999999983, "stopped": "converged: every placement covers mass 1", "depth": 1.1904824796041193, "seconds": 61.6}
[05:22:10] B-four column round 11: {"phase": "B-four", "column_round": 11, "rows": 8015, "orbits": 685, "sites": 5137, "objective": 11.778824888595476, "lp_rounds": 2, "least_covered": 0.9999999999999996, "stopped": "converged: every placement covers mass 1", "depth": 1.2022404687242119, "seconds": 19.1}
[05:23:12] B-four column round 12: {"phase": "B-four", "column_round": 12, "rows": 8293, "orbits": 691, "sites": 5185, "objective": 11.778824888595448, "lp_rounds": 7, "least_covered": 0.9999999999999885, "stopped": "converged: every placement covers mass 1", "depth": 1.2624195411784123, "seconds": 61.3}
[05:23:29] B-four column round 13: {"phase": "B-four", "column_round": 13, "rows": 8293, "orbits": 697, "sites": 5221, "objective": 11.778824888595476, "lp_rounds": 1, "least_covered": 0.9999999999999977, "stopped": "converged: every placement covers mass 1", "depth": 1.181187077075425, "seconds": 16.9}
[05:24:43] B-four column round 14: {"phase": "B-four", "column_round": 14, "rows": 8642, "orbits": 703, "sites": 5269, "objective": 11.77566883909169, "lp_rounds": 8, "least_covered": 0.9999999999999294, "stopped": "converged: every placement covers mass 1", "depth": 1.1493802636669346, "seconds": 73.4}
[05:25:24] B-four column round 15: {"phase": "B-four", "column_round": 15, "rows": 8888, "orbits": 709, "sites": 5317, "objective": 11.771324009191703, "lp_rounds": 4, "least_covered": 0.9999999999999725, "stopped": "converged: every placement covers mass 1", "depth": 1.1195494907656955, "seconds": 41.4}
[05:26:01] B-four column round 16: {"phase": "B-four", "column_round": 16, "rows": 8933, "orbits": 715, "sites": 5365, "objective": 11.771324009191757, "lp_rounds": 2, "least_covered": 0.999999999999994, "stopped": "converged: every placement covers mass 1", "depth": 1.1156699480468761, "seconds": 36.7}
[05:27:19] B-four column round 17: {"phase": "B-four", "column_round": 17, "rows": 9096, "orbits": 721, "sites": 5409, "objective": 11.767953949285923, "lp_rounds": 6, "least_covered": 0.9999999999999979, "stopped": "converged: every placement covers mass 1", "depth": 1.1313301515593122, "seconds": 77.0}
[05:28:14] B-four column round 18: {"phase": "B-four", "column_round": 18, "rows": 9108, "orbits": 727, "sites": 5457, "objective": 11.767953949285923, "lp_rounds": 5, "least_covered": 0.9999999999999989, "stopped": "converged: every placement covers mass 1", "depth": 1.1561498105508599, "seconds": 54.2}
[05:28:39] B-four column round 19: {"phase": "B-four", "column_round": 19, "rows": 9108, "orbits": 733, "sites": 5493, "objective": 11.767953949285921, "lp_rounds": 1, "least_covered": 0.9999999999999992, "stopped": "converged: every placement covers mass 1", "depth": 1.1576617604197028, "seconds": 24.6}
[05:29:02] B-four column round 20: {"phase": "B-four", "column_round": 20, "rows": 9108, "orbits": 739, "sites": 5541, "objective": 11.767953949285893, "lp_rounds": 1, "least_covered": 0.9999999999999674, "stopped": "converged: every placement covers mass 1", "depth": 1.1085712073739435, "seconds": 22.8}
[05:29:30] B-four column round 21: {"phase": "B-four", "column_round": 21, "rows": 9134, "orbits": 745, "sites": 5589, "objective": 11.767953949285928, "lp_rounds": 2, "least_covered": 0.999999999999999, "stopped": "converged: every placement covers mass 1", "depth": 1.1427863596619061, "seconds": 27.0}
[05:29:44] B-four column round 22: {"phase": "B-four", "column_round": 22, "rows": 9134, "orbits": 751, "sites": 5629, "objective": 11.767953949285927, "lp_rounds": 1, "least_covered": 0.9999999999999998, "stopped": "converged: every placement covers mass 1", "depth": 1.1631630719906734, "seconds": 14.2}
[05:30:13] B-four column round 23: {"phase": "B-four", "column_round": 23, "rows": 9200, "orbits": 757, "sites": 5677, "objective": 11.767953949285927, "lp_rounds": 2, "least_covered": 0.999999999999998, "stopped": "converged: every placement covers mass 1", "depth": 1.1095370366017618, "seconds": 28.5}
[05:30:30] B-four column round 24: {"phase": "B-four", "column_round": 24, "rows": 9200, "orbits": 763, "sites": 5725, "objective": 11.767953949285918, "lp_rounds": 1, "least_covered": 0.9999999999999964, "stopped": "converged: every placement covers mass 1", "depth": 1.152552098513553, "seconds": 16.4}
[05:30:49] B-four column round 25: {"phase": "B-four", "column_round": 25, "rows": 9200, "orbits": 769, "sites": 5773, "objective": 11.767953949285918, "lp_rounds": 1, "least_covered": 0.999999999999993, "stopped": "converged: every placement covers mass 1", "depth": 1.254552409846056, "seconds": 18.4}
[05:31:39] B-four column round 26: {"phase": "B-four", "column_round": 26, "rows": 9256, "orbits": 775, "sites": 5809, "objective": 11.767953949285923, "lp_rounds": 2, "least_covered": 0.9999999999999984, "stopped": "converged: every placement covers mass 1", "depth": 1.2263917225298746, "seconds": 49.2}
[05:32:00] B-four column round 27: {"phase": "B-four", "column_round": 27, "rows": 9256, "orbits": 781, "sites": 5857, "objective": 11.767953949285925, "lp_rounds": 1, "least_covered": 0.9999999999999998, "stopped": "converged: every placement covers mass 1", "depth": 1.1220216409210142, "seconds": 21.3}
[05:33:14] B-four column round 28: {"phase": "B-four", "column_round": 28, "rows": 9362, "orbits": 787, "sites": 5905, "objective": 11.762900948154126, "lp_rounds": 5, "least_covered": 0.9999999999999989, "stopped": "converged: every placement covers mass 1", "depth": 1.1154596193934503, "seconds": 73.5}
[05:34:32] B-four column round 29: {"phase": "B-four", "column_round": 29, "rows": 9599, "orbits": 793, "sites": 5953, "objective": 11.748950151195261, "lp_rounds": 6, "least_covered": 0.9999999999999967, "stopped": "converged: every placement covers mass 1", "depth": 1.1019630032997276, "seconds": 77.3}
[05:35:44] B-four column round 30: {"phase": "B-four", "column_round": 30, "rows": 9659, "orbits": 799, "sites": 6001, "objective": 11.73870050317217, "lp_rounds": 6, "least_covered": 0.9999999999999998, "stopped": "converged: every placement covers mass 1", "depth": 1.1091664843579085, "seconds": 70.9}
[05:36:32] B-four column round 31: {"phase": "B-four", "column_round": 31, "rows": 9825, "orbits": 805, "sites": 6045, "objective": 11.730827067669175, "lp_rounds": 4, "least_covered": 0.9999999999999918, "stopped": "converged: every placement covers mass 1", "depth": 1.1274592731829574, "seconds": 47.5}
[05:37:15] B-four column round 32: {"phase": "B-four", "column_round": 32, "rows": 9846, "orbits": 811, "sites": 6093, "objective": 11.730827067669194, "lp_rounds": 2, "least_covered": 0.9999999999999986, "stopped": "converged: every placement covers mass 1", "depth": 1.1413533834586467, "seconds": 43.0}
[05:37:42] B-four column round 33: {"phase": "B-four", "column_round": 33, "rows": 9846, "orbits": 817, "sites": 6141, "objective": 11.730827067669185, "lp_rounds": 1, "least_covered": 0.9999999999999991, "stopped": "converged: every placement covers mass 1", "depth": 1.1027255639097744, "seconds": 26.1}
[05:38:11] B-four column round 34: {"phase": "B-four", "column_round": 34, "rows": 9846, "orbits": 823, "sites": 6189, "objective": 11.730827067669152, "lp_rounds": 1, "least_covered": 0.9999999999999943, "stopped": "converged: every placement covers mass 1", "depth": 1.0971052631578948, "seconds": 27.7}
[05:38:43] B-four column round 35: {"phase": "B-four", "column_round": 35, "rows": 9846, "orbits": 829, "sites": 6237, "objective": 11.730827067669157, "lp_rounds": 1, "least_covered": 0.9999999999999774, "stopped": "converged: every placement covers mass 1", "depth": 1.1399436090225563, "seconds": 31.3}
[05:39:04] B-four column round 36: {"phase": "B-four", "column_round": 36, "rows": 9846, "orbits": 835, "sites": 6285, "objective": 11.730827067669177, "lp_rounds": 1, "least_covered": 0.9999999999999989, "stopped": "converged: every placement covers mass 1", "depth": 1.0796992481203007, "seconds": 20.5}
[05:41:29] B-four column round 37: {"phase": "B-four", "column_round": 37, "rows": 10021, "orbits": 841, "sites": 6333, "objective": 11.730827067669182, "lp_rounds": 2, "least_covered": 0.9999999999999984, "stopped": "converged: every placement covers mass 1", "depth": 1.118703007518797, "seconds": 144.6}
[05:41:55] B-four column round 38: {"phase": "B-four", "column_round": 38, "rows": 10035, "orbits": 847, "sites": 6381, "objective": 11.730827067669175, "lp_rounds": 2, "least_covered": 0.999999999999982, "stopped": "converged: every placement covers mass 1", "depth": 1.1219924812030075, "seconds": 25.1}
[05:42:24] B-four column round 39: {"phase": "B-four", "column_round": 39, "rows": 10035, "orbits": 853, "sites": 6413, "objective": 11.730827067669146, "lp_rounds": 1, "least_covered": 0.9999999999999899, "stopped": "converged: every placement covers mass 1", "depth": 1.1633458646616541, "seconds": 28.7}
[05:42:59] B-four column round 40: {"phase": "B-four", "column_round": 40, "rows": 10043, "orbits": 859, "sites": 6461, "objective": 11.730827067669157, "lp_rounds": 2, "least_covered": 0.9999999999999953, "stopped": "converged: every placement covers mass 1", "depth": 1.1158834586466166, "seconds": 34.5}
[05:43:30] B-four column round 41: {"phase": "B-four", "column_round": 41, "rows": 10043, "orbits": 865, "sites": 6509, "objective": 11.730827067669175, "lp_rounds": 1, "least_covered": 0.9999999999999916, "stopped": "converged: every placement covers mass 1", "depth": 1.080827067669173, "seconds": 29.8}
[05:45:08] B-four column round 42: {"phase": "B-four", "column_round": 42, "rows": 10237, "orbits": 871, "sites": 6557, "objective": 11.730827067669196, "lp_rounds": 4, "least_covered": 0.9999999999999807, "stopped": "converged: every placement covers mass 1", "depth": 1.1113408521303259, "seconds": 97.3}
[05:46:12] B-four column round 43: {"phase": "B-four", "column_round": 43, "rows": 10237, "orbits": 877, "sites": 6605, "objective": 11.730827067669138, "lp_rounds": 1, "least_covered": 0.9999999999999314, "stopped": "converged: every placement covers mass 1", "depth": 1.0851503759398495, "seconds": 62.5}
[05:47:37] B-four column round 44: {"phase": "B-four", "column_round": 44, "rows": 10364, "orbits": 883, "sites": 6653, "objective": 11.727692307692307, "lp_rounds": 4, "least_covered": 0.9938461538461519, "stopped": "deadline reached after 4 rounds", "depth": NaN, "seconds": 84.3} | deadline reached after 4 rounds
[05:47:37] B-four: last column round unconverged (deadline reached after 4 rounds); returning the last converged solution
[05:47:37] B-four: rationalised mass 2932721/250000 = 11.730884000 over 328 atoms; corner weights [Fraction(600001, 4000000)]; centre []
[05:47:54] B-four: sweep 17.4s; conditions [('Condition 1 atoms carry the declared symmetry', True, '328 atoms closed under D4 about the centre'), ('Condition 2 total mass below n', False, 'total 2932721/250000 against n = 11'), ('Condition 3 net reaches pi/4', True, 'final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000'), ('Condition 4 containment B(1 + D) < 1', True, 'B = 9977/10
```

### Replaying an exported measure

```text
from fractions import Fraction
import json
from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.model import Atom
m = json.load(open('bc-293-measure-free-96-25.json'))
steps, limit = m['direction_steps'], Fraction(m['angle_limit'])
cert = Certificate(n=11, outer_side=Fraction(m['outer_side']), square_side=Fraction(m['square_side']),
    atoms=tuple(Atom(str(i), Fraction(x), Fraction(y), Fraction(w)) for i, (x, y, w) in enumerate(m['atoms'])),
    half_tangents=tuple(limit * k / steps for k in range(steps + 1)))
v = verify(cert, workers=1)
print([(c.name, c.holds) for c in v.conditions], v.total_mass, v.minimum_cell_mass)
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
