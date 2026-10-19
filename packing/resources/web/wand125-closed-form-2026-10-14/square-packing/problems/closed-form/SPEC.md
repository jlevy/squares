# Public specification of a square-packing lower bound using a measure with seams

All numbers, including decimal notation, are exact rational numbers unless explicitly stated otherwise. This document specifies the mathematics, inputs, and acceptance rules for an independent checker of the computer-assisted proof. Verification requires recomputing the family structure, region coverage, and every leaf test; it does not require trusting the search order, linear programs, random choices, or running time of the search tools.

## 1. Claim and closed form

### 1.1 Notation and theorem

Let s(N) be the minimum side length of a square container holding N unit squares with pairwise disjoint interiors. Write the container side as a = k + δ with k an integer and 0 < δ ≤ 1; throughout, k ≥ 7. For a given N we take k = ⌊√N⌋. Square numbers N = k² are covered by the area bound s(N) ≥ k and are not considered further.

The interval (0, 1] is split into the 34 intervals I₁, …, I₃₄ listed in `INTERVALS.md` and `intervals.json`. For each interval the certificate proves the saving

  S_i(δ) = α_i δ + β_i   (δ ∈ I_i),

with exact rationals α_i (slope) and β_i (intercept) given in `intervals.json` as `certified_line.alpha` and `certified_line.beta`. Let S*(δ) be the largest S_i(δ) over the intervals containing δ.

**Theorem.** Let N ≥ 49 be a non-square integer and k = ⌊√N⌋. If δ ∈ (0, 1] satisfies (k + δ)² − 4 S*(δ) < N, then s(N) ≥ k + δ. Consequently s(N) ≥ a(N), where

  a(N) = k + sup { δ ∈ (0, 1] : (k + δ)² − 4 S*(δ) < N }.

**Closed form.** Since α_i ≤ 1.7496 and k ≥ 7, each T_i(δ) = (k + δ)² − 4(α_i δ + β_i) is strictly increasing in δ. On I_i the condition T_i(δ) < N therefore holds exactly below the root

  a_i(N) = 2α_i + √(4α_i² + N + 4β_i − 4α_i k)   (as a value of k + δ),

so

  a(N) = max { min(a_i(N), k + d1_i) : i with a_i(N) > k + d0_i },

where I_i has endpoints d0_i < d1_i (an interval that is open on the left needs no special case, because the supremum is the same). The maximum over intervals is needed because S* may jump at an interval border. In each interval the bound is a single square root.

The derivation: §1.2 shows that a measure μ on [0, a]² with μ(Q) ≥ 1 for every closed unit square Q ⊆ [0, a]² and total mass below N gives s(N) ≥ a. §1.3 shows that the measure built from the certified family has total mass (k + δ)² − 4S(δ), and the certificates show μ(Q) ≥ 1 for every Q (§§2–7) together with S(δ) ≥ S_i(δ) on I_i. Since the family's S is concave and piecewise affine on each interval, the chord S_i through its endpoint values is a lower bound.

**Comparison with published formulas.** Nagamochi's formula F(N) = 1 + √(N − 2k + 1) is the bound obtained in the same way from the saving δ/2, that is from (k + δ)² − 2δ = N. Karakuş's formula 1/2 + √(N − k + 1/4) (arXiv:2609.37410, Corollary 6.2) corresponds to the saving δ/4. A gap in the proof of the key lemma behind F(N) has been publicly discussed (chelokot; jlevy/squares#295). Karakuş (arXiv:2609.37410) constructs counterexamples to the scoring assertion in Lemma 1 of Nagamochi's paper, which show that the published proof of Nagamochi's rectangle bound is incomplete; the paper states that they do not disprove the bound itself. It then proves a weaker rectangle bound with a strip measure, from which it derives s(N) ≥ 1/2 + √(N − k + 1/4) for every non-square N ≥ 8 and s(k² − 1) = k; it does not establish Nagamochi's full bound or s(k² − 2) = k. Our proof uses neither Nagamochi's lemma nor Karakuş's bound. Our certified saving satisfies S*(δ) − δ/2 = (α₁ − 1/2)δ > 1.229δ on (0, 1/50] and S*(δ) − δ/2 > 0.0226 on [1/50, 1]. Since trivially s(N) ≤ k + 1, compare with F(N) capped at k + 1. For every non-square N ≥ 49:

- a(N) = F(N) = k + 1 for N = (k + 1)² − 1 and N = (k + 1)² − 2;
- a(N) > F(N) for every other N.

Indeed, if F(N) < k + 1, then F(N) = k + δ_F with (k + δ_F)² − 2δ_F = N and 0 < δ_F < 1. Every certified line exceeds δ/2 on the closure of its interval (by more than 0.0226 at every endpoint with δ ≥ 1/50, including open left endpoints, and by (α₁ − 1/2)δ on I₁). Let I_i be an interval with d0_i ≤ δ_F < d1_i (if δ_F is a right endpoint, take the next interval). For δ ∈ I_i close to δ_F we have (k + δ)² − 4S_i(δ) < (k + δ)² − 2δ, and the right-hand side is continuous and equals N at δ_F, while the gap 4S_i(δ) − 2δ stays bounded away from 0 near δ_F (S_i is affine and S_i(δ_F) > δ_F/2 holds also when δ_F = d0_i is an open endpoint, as a limit). Hence (k + δ)² − 4S*(δ) < N for some δ > δ_F, and a(N) > F(N). This does not use the value of S* at δ_F itself, which matters at δ_F = 2/5 and 4/5, where S* drops to the right. If F(N) ≥ k + 1, that is N ≥ (k + 1)² − 2, then (k + 1)² − 4S*(1) < (k + 1)² − 2 ≤ N, so a(N) = k + 1. Likewise a(N) is strictly larger than Karakuş's value except at N = (k + 1)² − 1, where both are k + 1.

Because S*(1) > 3/4 (interval I₃₄ gives S*(1) ≈ 0.853), the bound gives s(N) = k + 1 for N = (k + 1)² − 1, (k + 1)² − 2 and (k + 1)² − 3 (k ≥ 7). These values are not new. s(n² − 1) = s(n² − 2) = n were stated by Nagamochi (2005); the proof of a key lemma there has a publicly discussed gap (jlevy/squares #295). Our bound gives these values for n ≥ 8 without using that lemma; Karakuş (arXiv:2609.37410) gives a proof of s(n² − 1) = n that also avoids it. s(n² − 3) = n for n ≥ 6 was proved by Evan Daniel (the Valid7 certificate, github.com/evand/square-packing; an independent check is in github.com/wand125/square-packing/tree/main/checks/valid7). Here they follow from the same general bound.

References: H. Nagamochi, Packing unit squares in a rectangle, Electron. J. Combin. 12(1) (2005), #R37, doi:10.37236/1934. H. Karakuş, A counterexample to Nagamochi's scoring lemma and a new rectangle packing bound, arXiv:2609.37410v1 [math.CO] (2026), https://arxiv.org/abs/2609.37410. jlevy/squares issue #295 (github.com/jlevy/squares/issues/295). E. Daniel, the Valid7 certificate for s(n² − 3) = n, github.com/evand/square-packing.

### 1.2 The measure lower-bound principle

If a finite nonnegative measure μ satisfies μ(Q) ≥ 1 for every closed unit square Q ⊆ [0,a]² and μ([0,a]²) < N, then s(N) ≥ a.

Indeed, suppose N squares fit in a container of side b < a. Scale the entire packing by a/b, and place a unit square of the same orientation at the center of each enlarged square. These N closed unit squares are mutually separated and lie in [0,a]². The total measure is therefore at least the sum of their masses, which is at least N, a contradiction. This scaling argument avoids double counting singular segment measure on shared contact edges of the original packing.

### 1.3 Total mass

Let α = 9/5, W = 2+δ, R = 2, and let the corner rectangle be C = [0,W]×[0,R]. Let M_C(δ) be the total segment measure assigned to the corner, and m_v the total mass of the vertical line at phase 0 at the end of the wall profile.

area(C ∖ U) = 2(2+δ) − (2+δ−9/5)(2−9/5) = 99/25 + (9/5)δ.

S(δ) = 99/25 + (9/5)δ − M_C(δ) − m_v.

The central U has area (k+δ−18/5)². Each wall has k−4 periods of mass 9/5 each and a terminal line of mass m_v, and each corner has mass M_C. Thus

μ_{k,δ}([0,a]²) = (a−18/5)² + 4[(k−4)9/5 + M_C(δ) + m_v] = a² − 4S(δ).

The term m_v must not be omitted. M_C is a sum of constant-mass pieces and variable-length pieces of constant density, so it is affine in δ, as is S.

## 2. Construction and localization of the covering family

### 2.1 Global arrangement

Place the lower-left corner at the origin. The bottom wall carries the fractional part δ, and the left wall has aligned integer periods. Arrange the segments in C, the bottom-wall profile, and the terminal line by rotations through 0, 90, 180, and 270 degrees under ρ(x,y) = (a−y,x). This gives C4 symmetry; reflection symmetry (D4) must not be assumed. In the center, place Lebesgue measure of density 1 on U_global = [9/5,a−9/5]².

Describe one wall period in bottom-wall coordinates (t,y). All pieces lie on the 1/5 grid.

- Horizontal pieces: y=j/5 (j=1,…,9), t∈[p/5,(p+1)/5] (p=0,…,4), with total mass h_{j,p}.
- Vertical pieces: t=q/5 (q=0,…,4), y∈[i/5,(i+1)/5] (i=0,…,8), with total mass v_{q,i}.
- Σ h_{j,p} + Σ v_{q,i} = 9/5. The respective densities are 5h_{j,p} and 5v_{q,i}.
- m_v = Σ_i v_{0,i}. The phase 1 line is the next period's phase 0 line; only the final endpoint requires the additional m_v.

On the bottom wall, substitute x−W−n for t, with n=0,…,k−5, giving k−4 periods and the terminal line at x=W+k−4. The local left-wall profile is the transpose (x,y)=(t_y,2+n+t_x). The family model imposes h_{j,p}=h_{j,4−p} and v_{q,i}=v_{(5−q) mod 5,i}. To identify the global construction with this local transpose, also verify the periods, phases, and reversal identities from the JSON.

Multiple rows on the same segment are added. A corner boundary line coinciding with a period's phase 0 line is also added, not deduplicated.

### 2.2 Reduction to k ≥ 7

A unit square has coordinate width √2 < 2. In the interior, Lebesgue measure suffices. Near a corner, use the corner and adjacent wall structure, which is independent of k. Away from corners, an integer translation along a wall preserves the mass. For k=7 there are k−4=3 periods, enough for width √2 and a phase shift of width 1. C4 rotations handle the other walls and corners. The local structural identities and placement ranges must hold throughout each δ interval; checking finitely many δ values alone is insufficient.

Local calculations use U_local = {x≥9/5,y≥9/5}. A finite polygon with upper boundary 20 or 1000 may represent this quadrant if the checker verifies that the local squares cannot reach the truncation edges. Identifying this local measure with the global measure is a separate obligation from the numerical leaf tests.

### 2.3 Coverage of the entire container by local checks

Let a = k + δ (k ≥ 7, 0 < δ ≤ 1), W = 2 + δ, R = 2, and let Q have center z and half-width w ≤ √2/2 < 0.7072 (=: r). The global covering measure μ is the C4-symmetric arrangement of §2.1. The local measure μ_loc consists of F, T(δ), and V(δ) from the family JSON and U_loc = [9/5, ∞)².

**(1) Rotate to the lower left.** Since the C4 rotation ρ preserves μ, assume z ∈ [0, a/2]²: the four closed quarters map to one another by rotation.

**(2) In the lower left, μ = μ_loc.** A square centered at z ∈ [0, a/2]² lies in [0, a/2 + r]². The only global pieces reaching this range are the lower-left corner pieces in [0, W]×[0, R], its bottom wall at x ∈ [W, W + k − 4] with period 1, the left wall obtained by rotating the upper-left corner's bottom wall, at y ∈ [R, a − W], and the interior Lebesgue measure on [9/5, a − 9/5]². Indeed:

- The lower-right corner pieces have x ≥ a − R, and the upper-left corner pieces have y ≥ a − W. The inequality a/2 + r < a − W ⇔ a > 2W + 2r holds for k ≥ 7 and 0 < δ ≤ 1 (§2.3 (5)(i)).
- The bottom-wall endpoint x = W + k − 4 = a − R and left-wall endpoint y = a − W likewise cannot be reached. Neither can the right or top wall.
- The upper and right boundaries a − 9/5 of U cannot be reached, since a/2 + r < a − 9/5.

Thus the global pieces agree with the local model inside [0, a/2 + r]². For each family, verify this identity, including periods, phases, transposition, corner windows, and terminal lines, by constructing the k = 7, 8, 9 containers and checking δ = d0 and d1 with rational arithmetic. Positions and masses are affine in δ and the structure is fixed on the interval, so endpoint identities imply identities throughout the interval. For k ≥ 10, only the number of wall periods changes; the window agrees with those for k = 7, 9 after integer shifts.

The local family is read as its periodic extension: the walls repeat with period 1 without end and U_loc = [9/5, ∞)². The family file stores only finitely many whole periods (up to x = 9 and y = 9 in the published families); this is a finite representation of the periodic model. Two equivalent ways to check "global = local on [0, a/2 + r]²" are: (a) compare the global measure with the periodic extension of the local family on the whole window [0, a/2 + r]²; or (b) compare them on [0, 24/5]² and check separately that every global wall period equals the extracted profile (integer shifts) and that the terminal line has phase 0. The structure tool uses (b) for k = 7, 8, 9 at δ = d0 and d1. Every square whose center lies in one of the four checked regions stays inside [0, 24/5]² in local coordinates (the right region after the shift by δ), since 3.8 + r < 24/5.

**(3) Truncate the window using periodicity.** In the local model:

- If z_y > R + r, the threshold is below 2.7072, so z_y ≥ 2.71 is sufficient. Then Q reaches neither the corner rectangle nor the bottom wall (y ≤ 9/5). Only the left wall, periodic in y with period 1, and U_loc, invariant under the relevant y translations, contribute. Integer shifts therefore preserve μ_loc(Q) and can place z_y ∈ [2.71, 3.71]. If also z_x ≥ 9/5 + r, then Q ⊂ U_loc and μ_loc(Q) ≥ 1.
- If z_y < 2.71 and z_x > W + r, Q reaches neither the corner rectangle (x ≤ W) nor the left wall (x ≤ 9/5). Only the bottom wall, periodic in x − W with period 1, and U_loc contribute. Since Q ⊂ {x ≥ 9/5}, the relevant x translations preserve the interior contribution. An integer shift places z_x − δ ∈ [2.71, 3.71].

Both windows need extend only to 3.8, which contains the full period [2.71, 3.71]. This remains sufficient when (7 + δ)/2 exceeds 3.8 because of the periodic shifts.

**(4) Check the remaining centers directly.** The remaining z ∈ [0, a/2]² lie in z_y ≤ 3.8 and z_x ≤ 3.8 + δ. They are covered by the left region (z_x ∈ [0, 1.67], z_y ∈ [0, 3.8]), straddle region (z_x ∈ [1.67, 2.51 + d1], z_y ∈ [0, 2.72]), top region (z_x ∈ [1.67, 2.51 + d1], z_y ∈ [2.72, 3.8]), and right region (z_x − δ ∈ [2.51, 3.8], z_y ∈ [0, 3.8]).

For the right region, shift coordinates back by δ to fix T, discard the F pieces in the strip and V, and shrink U to [9/5, ∞)². This gives the right-side family; all these changes decrease mass, so its test is a lower bound. If z_x ≥ 2.51 + d1 ≥ 2.51 + δ, then z_x − δ ≥ 2.51 lies in the right region. The right edge of the straddle and top regions is 2.51 + d1 for each interval; in §4.2, d1 = 2/5 gives 2.91.

**(5) Conclusion.** If the family on [d0, d1] passes the structural checks and every leaf in all four regions passes recomputation, then for every k ≥ 7, δ ∈ [d0, d1], and closed unit square Q ⊂ [0, k + δ]², μ(Q) ≥ 1. Combined with total mass = a² − 4S(δ) < N, this gives s(N) ≥ a (§1).

**The claim starts at exactly N = 49 (k = ⌊√N⌋ ≥ 7).** Three requirements use k ≥ 7. (i) The inequality a/2 + r < a − W in (2) follows from a > 2W + 2r, or k > 4 + δ + √2 ≈ 5.414 + δ. This holds for all δ ≤ 1 when k ≥ 7 (at δ = 1 it needs k > 6.414); k = 6 fails when δ > 0.586. (ii) The structural checks construct k = 7, 8, 9, and integer shifts reduce k ≥ 10 to these cases. (iii) The reduction in §2.2 uses k − 4 ≥ 3 bottom-wall periods. For N = k², the area bound gives a(N) = k (§1.1). For every non-square N ≥ 49, a(N) = k + δ with δ ∈ (0, 1] and k = ⌊√N⌋ ≥ 7, so the argument applies (the container of side k + 1 at δ = 1 is treated with this k). No claim is made for N ≤ 48.

## 3. Family JSON format

### 3.1 Basic format

One file contains one JSON object. Exact input numbers are strings representing integers or "p/q", where p is an integer and q is a positive integer. Read them at arbitrary precision; do not convert large numerators or denominators to floating-point or fixed-width integers. Zero may be "0".

| Key | Meaning |
|---|---|
| `d0`, `d1` | The family's closed interval [d0,d1], with d0<d1. Every leaf's δ interval is contained in it. |
| `UA` | α; "9/5" in the standard family. |
| `eps` | Metadata for the corner margin factor used in export; for example, the JSON number `0.003`. Never multiply by it during leaf verification. |
| `F` | Array of fixed-segment rows `[ax,ay,bx,by,m]`. |
| `T` | Array of translated-segment rows of the same form. Coordinates give the position at δ=0; actual endpoints are (ax+δ,ay), (bx+δ,by). |
| `V` | Array of variable-length rows `[xl,y,rho]`, giving density ρ on [xl,2+δ]×{y}. |
| `S_d0`, `S_d1` | Endpoint savings S, or conservatively reduced guaranteed values. Recompute rather than trusting these fields alone. |
| `U` (optional) | Counterclockwise vertices `[[x,y],…]` of a convex polygon with density 1. Replaces the standard U constructed from UA. |
| `bumps`, `edge_variant` (optional) | Provenance metadata; never interpret these as instructions to add mass. |

For F and T, m is **total segment mass**, not density. A segment of nonzero length L has density m/L and contributes mℓ/L when length ℓ lies in the square. The third entry of V is **density**; its total mass is ρ(2+δ−xl). Check nonnegativity and xl≤2+d0. A zero-length V segment is the zero measure. F and T must be axis-parallel and nonnegative; a zero-length segment with positive mass is invalid. Point masses are not represented. Silently dropping malformed rows is not a substitute for input validation.

The standard U in stage A is [(α,α),(1000,α),(1000,1000),(α,1000)]; the stage-B area lower bound uses the analogous polygon with upper boundary 20. If `U` is present, both use that same polygon. The B3U/B3T and EDGE lemmas require the standard quadrant or an explicitly specified variant; do not apply them unconditionally to arbitrary `U`.

An example family has d0="19/50", d1="2/5", 490 F rows, 375 T rows, and 9 V rows. Example rows are:

```json
{"F":[["2/5","1/5","3/5","1/5","12323/200000000"]],
 "T":[["2","0","2","1/5","40001/100000000"]],
 "V":[["11/5","1/5","3730451/1000000000"]]}
```

These are partial row examples, not a valid standalone family.

### 3.2 Recomputing savings and walls

An exporter may multiply only corner and seam masses by (1+eps) and round upward with denominator 10⁹. Wall periods must sum exactly to 9/5; an exact rational profile may be exported without rounding. The stored masses already include such adjustments. Do not reapply eps or bumps.

The sum of all F/T rows includes repeated walls in a finite window and is not M_C. Extract one wall period, verify that the other periods agree as measures, and separate the corner contribution and m_v. Combine rows on identical supports and compare densities on the open intervals between all segment endpoints. There are no endpoint point masses.

For the example family, the following extraction gives exactly the stored values, using the δ=0 coordinates of T:

- A full period is x∈[3,4): include horizontal segments with both endpoints in [3,4] and vertical segments with x∈[3,4). Their total mass is 9/5.
- The sum of vertical T segments at x=3 is m_v.
- M_fixed = Σ(vertical F segments with upper endpoint y≤2) + Σ(horizontal F segments with y≤2) + Σ(vertical T segments at x=2) − 2m_v.
- M_C(δ) = M_fixed + Σ_V ρ(2+δ−xl). Subtracting 2m_v removes the wall phase 0 contributions included at y=2 on the left wall and x=2 on the bottom wall.

Before using this extraction for another family structure, check the corner supports, period starting positions, and agreement including missing zero-mass pieces.

All 34 published families have the same structure. In δ=0 coordinates, T contains exactly 7 whole periods of the bottom wall, x∈[2,9), and F contains the transposed left wall, y∈[2,9), with one period read from x∈[3,4) (resp. y∈[3,4)). Subtracting the 7 periods from T leaves only vertical segments on x=2 with y∈[0,2]; subtracting the transposed periods from F leaves segments inside [0,2+d0]×[0,2]; both remainders are nonnegative. M_fixed is the total mass of the two remainders, which equals the formula above. The local family contains no terminal line at x=9; the terminal line (m_v) belongs to the global construction (§2.1). F and T contain no rows of mass 0; V contains rows of density 0, which are the zero measure. For the example, S(19/50)≈0.589900810970916 and S(2/5)≈0.624200093890916. The recomputed rational values equal the stored rational values at both endpoints, exceeding (3/2)δ by approximately 0.01990081 and 0.02420009 respectively. This verifies savings, not coverage of all square poses.

The guaranteed line is S_cert(δ)=S_d0+(S_d1−S_d0)(δ−d0)/(d1−d0). A conservative adjustment for a variable-length density increment (`vrho`) may subtract its maximum-length added mass from both endpoints, making S_cert smaller than the actual saving. An independent checker need only verify S_actual≥S_cert at both endpoints. Savings stored in right-side and X/Y variants are inherited information about the original family, not the variants' own total masses.

### 3.3 Right-side family

The right-side JSON has `F_right = T_original`, `T_right=[]`, `V_right=[]`, and the same UA, d0, and d1. Use the shifted center c'=(c_x−δ,c_y). The original F and V are nonnegative and may be discarded. The shifted original U is {x'≥α−δ,y≥α}. Since δ≥0, the right-side quadrant {x'≥α,y≥α} is a subset and gives a lower bound. This inclusion, rather than general translation invariance of U in x, justifies the bound. In the example, the right-side F agrees row for row with the original T, with 375 rows and empty T/V.

### 3.4 X and Y variants

Apply the following exact operations to the original family. Preserve d0, d1, UA, and other metadata; replace any existing `U`.

| Variant | Removed segments | New `U` |
|---|---|---|
| X | Every F segment with both endpoint x coordinates equal to α | [(-1000,α),(1000,α),(1000,1000),(-1000,1000)] |
| Y | Every F/T segment with both endpoint y coordinates equal to α, and every V segment with y=α | [(α,-1000),(1000,-1000),(1000,1000),(α,1000)] |

X is the local half-plane measure {y≥α}; Y is {x≥α}. Set `edge_variant` to "X" or "Y". Always use the **original family** for the one-sided density conditions of EX/EY, and the variant for the leaf's A/B test.

## 4. Local regions and root grid

### 4.1 Poses

u=tan(θ/2), c(u)=(1−u²)/(1+u²), s(u)=2u/(1+u²).

The square is Q(z,u)=z+R_θ[-1/2,1/2]². Its four normals n_j are (c,s) rotated j times through 90 degrees, and its vertices relative to z are

v=( (cε_x−sε_y)/2, (sε_x+cε_y)/2 ), (ε_x,ε_y)=(1,1),(-1,1),(-1,-1),(1,-1).

Thus Q is described by n_j·(p−z)≤1/2. Its half-width is w(u)=(c(u)+|s(u)|)/2 in this document's range |u|<1. Locally admissible centers satisfy z_x,z_y≥w(u). Stage B also imposes w(u)≤z_x,z_y≤20−w(u), using the computational side=20. Verify that these upper constraints are inactive in the published local windows.

Because the square's orientation has period π/2, the range [-13/32,7/16] suffices for u. In general, let U0<0<U1, a_u=−U0<1, b_u=U1<1. The condition for covering at least 90 degrees is a_u+b_u+a_u b_u≥1. In the example, 523/512≥1. The symbol a_u is distinct from the container side a.

### 4.2 The four regions for δ∈[19/50,2/5]

| Region | Center x interval | Center y interval | Family | Roots |
|---|---|---|---|---:|
| Straddle | [167/100,291/100] | [0,272/100] | Original family | 9,828 |
| Left | [0,167/100] | [0,19/5] | Original family | 17,442 |
| Top | [167/100,291/100] | [272/100,19/5] | Original family | 3,861 |
| Right | [251/100,19/5], with x'=x−δ | [0,19/5] | Right-side family | 13,338 |

Subdivide each x/y interval from its left endpoint in steps of 1/10, truncating only the final step at the right endpoint. For u, use the 27 intervals with endpoints j/32, j=−13,…,14; for δ, use the single interval [19/50,2/5]. The Cartesian-product counts are respectively 13·28·27, 17·38·27, 13·11·27, and 13·38·27, as in the table. Root counts must be recomputed from the record's own subdivisions; subdividing δ into 4 pieces changes the counts.

In original coordinates, the right region begins at x≥251/100+δ. Since δ≤2/5, this left endpoint is at most 291/100, leaving no gap to the straddle and top regions. Its right endpoint is 19/5+δ≥19/5. Thus the four regions cover [0,19/5]² in original coordinates; overlaps are allowed. The names "left" and "top" do not permit omitting T/V: the straddle, left, and top regions use the same original four-dimensional family.

### 4.3 Truncating the window

Away from corners, period-1 translations along walls and interior Lebesgue measure justify truncation. In this example, the upper edge of the k=7 C4 fundamental region satisfies (7+δ)/2≤3.7, within the center window ending at 3.8. Also verify noninterference from opposing walls when replacing the local measure by the global measure (§2.3). For general δ ≤ 1, (7+δ)/2 can reach 4.0; using 3.8 throughout therefore requires the periodic reduction of §2.3. The coarse classification x_hi≤2, x_lo≥2+d1, and the remaining case is distinct from the four actual checking regions.

### 4.4 Root grids of the published records

The checker does not fix a pitch: it requires that the roots of a region form exactly the Cartesian product of four
partitions (of [x0, x1], [y0, y1], the u-range and the δ interval) with no duplicates (§6.2). The published records
use the following grids. x and y are cut at x0 + j/10 and y0 + j/10, the last piece being shorter when the length
is not a multiple of 1/10 (for example 7/100, 1/25, 3/100 or 2/25). u is cut at j/32 for j = −13, …, 14
(27 pieces), so u = 0 is a cut and never interior. δ: in the straddling region the interval [d0, d1] is cut into
⌈(d1 − d0)/(1/50)⌉ equal pieces (pieces of 1/50 or shorter, e.g. 1/200, 1/80, 19/1000); in the other three regions
it is a single piece.

## 5. Leaf kinds and recomputation

A leaf box is b=(x0,x1,y0,y1,u0,u1,e0,e1). Every width is positive, and δ∈[e0,e1]⊆[d0,d1]. All calculations below use rational numbers, polynomials with rational coefficients, and exact real algebraic numbers.

### 5.1 Shared geometry

To clip a polygon by the closed half-plane a·p≤b, compute f_P=a·P−b and f_Q=a·Q−b at each edge's endpoints P,Q. Retain P if f_P≤0; if the signs are strictly opposite, add P+[f_P/(f_P−f_Q)](Q−P). For counterclockwise vertices, area is (1/2)Σ_i(x_i y_{i+1}−x_{i+1}y_i). An empty polygon or one with fewer than 3 vertices has area 0.

To clip a segment A+t(B−A), 0≤t≤1, by half-planes, start with t_lo=0,t_hi=1. For each half-plane, set num=b−a·A and den=a·(B−A). If den>0, set t_hi=min(t_hi,num/den); if den<0, set t_lo=max(t_lo,num/den). If den=0 and num<0, the intersection is empty. The final contribution is m·max(0,t_hi−t_lo). A segment coinciding with the boundary is counted as part of the closed set.

The minimum width W_min is 1 if u0≤0≤u1, and otherwise the smaller endpoint value of |c|+|s|. Width is concave separately on the positive and negative θ ranges, so its minimum occurs at an endpoint.

For the half-width upper bound H=hmax(u0,u1), set m=max(|u0|,|u1|):

- If m≤2/5, H=(1−m²+2m)/(2(1+m²)).
- If m>2/5, H=7072/10000.

The first uses monotonic increase for |u|≤2/5; the second uses √2/2<7072/10000.

### 5.2 EMPTY and CORE (stage A)

EMPTY passes only if x1<W_min/2 or y1<W_min/2. Equality is not empty. Before CORE, restrict the center box by x0←max(x0,W_min/2), y0←max(y0,W_min/2). If x0>x1 or y0>y1, bound is None. A CORE leaf requires a defined bound≥1; None is rejected.

Take the center midpoint z and radii (rx,ry). Construct the angular core as follows. For each j=0,…,3, compute endpoint normals n0,n1 at u0,u1 and p0=n0/2, and list

- n0·p≤1/2;
- if u0≠u1, also n1·p≤1/2 and (n0+n1)·p≤(n0+n1)·p0.

Replace each half-plane's right-hand side b in a·p≤b by b−|a_x|rx−|a_y|ry. Clip [-2,2]² successively and translate by z to obtain the core P.

**Core lemma.** The intersection of the endpoint half-planes and the origin side of the chord joining their contact points lies in every intermediate half-plane. Let h be half the angular difference and t∈[0,h] the angle from one endpoint. The intermediate unit normal is

[sin(h−t)/sin h]n0+[sin t/sin h]n_mid.

Substituting the chord condition n_mid·p≤cos(h)/2 and the endpoint condition gives the upper bound cos(t)/2≤1/2. The second half is symmetric. The reduction of the right-hand side by the center box's support function ensures that P lies in every admissible square.

Construct the outer polygon O as a convex hull. For each square vertex, take its angular endpoint positions v0,v1 and the tangent intersection t satisfying v0·t=v1·t=1/2; omit t when the determinant is 0. Add z+(±rx,±ry) to each point and take the convex hull of all resulting points. The vertex arc lies in the triangle of its endpoints and tangent intersection, so O contains every square in the box.

Set L_U=max(area(P∩U), 1−area(O)+area(O∩U)). The first term follows from P⊆Q; the second from area(Q)=1 and Q∖U⊆O∖U. Let P_T=(P−e0 e_x)∩(P−e1 e_x), using just one set if e0=e1. Convexity gives P_T⊆P−δe_x for every δ. Thus

bound = μ_F(P) + μ_T0(P_T) + μ_V(e0)(P) + L_U.

Since V only lengthens, use its shortest instance e0. If the core has fewer than 3 vertices, set its segment contribution to 0. CORE passes if this value is at least 1. The area-only bound `poly_lower` also takes the maximum with 0 and returns 0 for an empty core; call it P_lo. When the inner area is nonnegative, the additional max(0) leaves the value unchanged.

### 5.3 B3D: piecewise-affine segment mass (Lemma B3')

A leaf with u0<0<u1 is forbidden. Check u≠0 on the open interval J=(u0,u1). Bound U by P_lo from §5.2 and use the segment-only threshold τ=1−P_lo.

**Lemma B3'.** For fixed u, segment mass is continuous in (z_x,z_y,δ) and affine on each convex polyhedron of the arrangement below. Clipping points of a segment against a non-axis-parallel square are affine in these three variables. Their formulas change only when a square vertex meets a support line or a square edge meets a density breakpoint. V contributes ρ·length, so no variable-length denominator remains. On each polyhedron of the compact admissible domain, an affine function attains its minimum at a vertex. It therefore suffices to enumerate intersections of 3 planes.

For localization, expand the center box by 7072/10000 in each direction and retain all segments that can intersect it. For T0, use the center box [x0−e1,x1−e0]×[y0,y1]. Sum overlapping segment densities on each support line; breakpoints are endpoints at which the density changes. Using all pieces and endpoints without localization is also safe. Point masses are forbidden.

Write candidate planes as α_p z_x+β_p z_y+γ_p δ=k_p; α_p is not UA. Let l_x x+l_y y=l_k be an F/T support line, P a density breakpoint, v a square vertex, and n an outward unit normal.

| Contact | (α_p,β_p,γ_p,k_p) |
|---|---|
| F support line and vertex v | (l_x,l_y,0,l_k−l_x v_x−l_y v_y) |
| T0 support line and vertex v | (l_x,l_y,−l_x,l_k−l_x v_x−l_y v_y) |
| F breakpoint P and edge n | (n_x,n_y,0,n·P−1/2) |
| T0 breakpoint P+δe_x and edge n | (n_x,n_y,−n_x,n·P−1/2) |
| V support line y=y_v and vertex v | (0,1,0,y_v−v_y) |
| V fixed endpoint (xl,y_v) and edge n | (n_x,n_y,0,n_x xl+n_y y_v−1/2) |
| V moving endpoint (2+δ,y_v) and edge n | (n_x,n_y,−n_x,2n_x+n_y y_v−1/2) |

Add the 6 box faces z_x=x0,x1, z_y=y0,y1, δ=e0,e1 and the 4 admissibility faces z_x=w,20−w, z_y=w,20−w. Here w=(c+s)/2 on the u≥0 side and w=(c−s)/2 on the u≤0 side. All coefficients are rational functions of u.

Candidate pruning is optional. A plane may be removed only if α_p z_x+β_p z_y+γ_p δ−k_p has the same **strictly** positive or negative sign throughout J at all 8 box corners. One sufficient test requires each sign polynomial to be nonzero, root_free on the closed interval, and of the same sign at u0. Deduplicate planes by exact coefficient equality, never solely by hash equality.

For three plane rows, let M be the coefficient matrix and D=det M. Skip the triple if D is identically 0. Let D_x,D_y,D_δ be the determinants obtained by replacing the first, second, or third column with the right-hand side. Set p=(D_x/D,D_y/D,D_δ/D). Membership requires all **10 conditions** to be nonnegative:

p_x−x0, x1−p_x, p_y−y0, y1−p_y, p_δ−e0, e1−p_δ,
p_x−w, 20−w−p_x, p_y−w, 20−w−p_y.

For a rational function r=N/D_r, use the sign polynomial N·D_r. Split J at the real roots of the sign polynomials for the 10 conditions and det M. Test membership at a rational sample in each open component. Skip components outside the domain; apply `check_value3` below on every component inside it. Isolated angles at which the determinant vanishes are covered by continuity for u≠0; discarding degeneracies must not leave gaps.

### 5.4 check_value3, guards, and polynomial nonnegativity

The segment value at a vertex p(u) is

v(u)=μ_F(Q(p_x,p_y,u))+μ_T0(Q(p_x−p_δ,p_y,u))+μ_V(p_δ)(Q(p_x,p_y,u)).

Execute the clipping procedure of §5.1 symbolically over rational functions. Decide comparisons at a rational sample u=s_* and record the sign polynomial N·D of each tested difference as a guard. Identical equalities need no guard. If a nonidentically-zero expression vanishes at the sample, choose another sample (Resample). If a bounded implementation fails to find a sample within its limit of 60 attempts, reject; do not accept by omitting the proof.

**B1 (fixed branches).** On an open interval with no guard roots, every comparison retains its truth value, so the same symbolic expression applies throughout. Isolate any guard root in the interior exactly, split there, and repeat on each open component. Once a component (A,B) has no guard roots and v=N/D, prove (N−τD)D≥0 using `nonneg_open`. Do not test N−τD alone by assuming a positive denominator.

The specification of `nonneg_open(p,A,B)` is:

1. If p≡0, accept.
2. If a rational sufficient condition proves the interval root-free, accept if p(s)>0 at a rational sample A<s<B.
3. Otherwise, square-free factor p=c∏q_i^{m_i}. Reject if the product of factors with odd multiplicity m_i has a root in (A,B).
4. If it has no such interior root, choose a rational sample with p(s)≠0 and accept only if p(s)>0. Resample if p(s)=0.

A nonzero polynomial has finitely many roots, so resampling is possible. The test is justified because signs change at odd-multiplicity roots and do not change at even-multiplicity roots. For example, evaluating p=−(u−s)² only at its root s and accepting p(s)≥0 is invalid. The final sign must be positive at a nonroot.

An independent implementation may omit root-free shortcuts and always use Sturm's method. Form the Sturm sequence from the square-free polynomial f and f', followed by negative remainders. The difference in sign-variation counts at rational nonroot endpoints l,r gives the root count. Isolate roots by rational bisection. Represent an algebraic endpoint by a square-free defining polynomial and a rational interval containing exactly one root. If a bisection point is a rational root, treat it separately as an exact rational root. Decide root equality using gcd and isolating intervals, and order by refining intervals. Exclude roots only in (A,B); endpoint zeros are permitted.

**B2 (completion at boundaries).** For u≠0, axis-parallel support lines are not parallel to square edges, so clipped lengths and U's area are continuous. The admissible center domain also varies continuously. Values at the finitely many guard roots, membership roots, and angular endpoints therefore follow by limits of neighboring admissible poses. Handle u=0 by the upper semicontinuity in §6.3.

A general B4 method also handles critical values on edges for piecewise-quadratic expressions containing polygon terms. Ordinary B3D separates U into P_lo and does not use B4. Adding an arbitrary area term to the affine segment expression does not justify checking vertices alone.

The B4 argument for a general polygon term with a two-dimensional center is as follows. On an arrangement cell, area g is quadratic, and concavity of √g implies that Hess g has at most 1 positive eigenvalue. The segment term has Hessian 0, so the total cannot be a positive-definite quadratic with a strict minimum only in the cell interior; a minimum can be moved to the boundary. On an edge p+t(q−p), 0≤t≤1, write total mass as f(t)=f(0)+Bt+At², where

A=2[g(p)−2g((p+q)/2)+g(q)], B=f(1)−f(0)−A.

Only if A>0 and 0<−B/(2A)<1 is the interior critical value f(0)−B²/(4A) also a candidate. Otherwise, endpoints suffice. Proving each candidate over the angle interval by B1/B2 gives B4. B4U (§5.11) uses vertex and edge tests in (z_x,z_y,δ); its polygon term is independent of δ. The other arrangement tests use P_lo or the concavity and tangent lemmas to reduce to vertex tests.

### 5.5 EDGE: the two-edge lemma

Let α=UA and z_x,z_y≥α. The actual protrusion depths are h_X=max(0,α−z_x+w), h_Y=max(0,α−z_y+w). Suppose segment density is at least ρ_X along the entire chord x=α and at least ρ_Y along y=α. If h_X≤ρ_X and h_Y≤ρ_Y for the positive depths h_X,h_Y, then μ(Q)≥1.

**Proof.** The vertical cross-section length ℓ(x) of Q is symmetric about its center and nondecreasing up to the center. Since α≤z_x, the area lost to x<α is at most h_Xℓ(α). The segment on x=α contributes ρ_Xℓ(α), covering that loss. The same argument applies to y. Overestimating the area outside U by the sum of the two half-plane losses is safe for a lower bound. The intersection of the vertical and horizontal lines has segment measure 0.

For a box, use H from §5.1, hX=α−x0+H, hY=α−y0+H, and require:

- x0≥α, y0≥α;
- hX≤0 or hX≤D_X([y0−H,y1+H]);
- hY≤0 or hY≤D_Y([x0−H,x1+H],[e0,e1]).

D_X is the minimum, more precisely the essential infimum, of the sum of densities of vertical F pieces on x=α over the requested interval. Sort all endpoints together with the query endpoints, sum densities at each midpoint between consecutive endpoints, and take the minimum. An uncovered interval has density 0. Group entries and exits at identical endpoints.

D_Y minimizes the total density on y=α,

f_δ(x)=Σ_F ρ_i 1_{s_i<x<t_i}+Σ_V ρ_j 1_{xl_j<x<2+δ}+Σ_T ρ_i 1_{s_i<x−δ<t_i},

over x∈[lo,hi], δ∈[e0,e1]. **Sum first, then minimize.**

1. Use x breakpoints lo,hi, both endpoints of F, xl of V, 2+e0,2+e1, and each T endpoint+e0,+e1, sorted within [lo,hi].
2. Take the midpoint x of each open interval. Use δ breakpoints e0,e1, x−2, and x minus each T endpoint, sorted within [e0,e1].
3. Evaluate f_δ(x) exactly at each open δ interval's midpoint, and take the overall minimum. Return 0 for an empty list.

Density changes lie on constant-x lines or x−δ=constant lines; these subdivisions represent every open arrangement region. Segment endpoints carry no point mass, so density values at endpoints do not affect mass. Endpoint δ values follow by limits of the moving segment measures. Summing separate lower envelopes of F, V(e0), and T gives a different conservative lower bound; D_Y here is the minimum of their sum.

### 5.6 EX and EY: the one-sided edge lemma

EX requires x0≥α and (hX≤0 or hX≤D_X). EY requires y0≥α and (hY≤0 or hY≤D_Y). Compute D_X,D_Y from the original family. Once the condition holds, recompute CORE or B3D for the X/Y variant of §3.4. The four leaf names are `EX:CORE`, `EX:B3D`, `EY:CORE`, and `EY:B3D`.

**Proof for X.** area(Q∩U) equals area(Q∩{y≥α}) minus part of the area on the x<α side. That loss is at most the entire area of Q on x<α, hence at most h_Xℓ(α), and is covered by the removed x=α segment measure. Therefore the original μ(Q)≥μ_X(Q). For Y, interchange coordinates. In the variant's B3D test, compute P_lo with that variant's U and use τ=1−P_lo.

### 5.7 B3U:x and B3U:y: the concavity lemma

The condition `concave_ok` is:

- x: x0≥α and y0−H≥α;
- y: y0≥α and x0−H≥α.

Include the standard U area and use threshold 1. Include exactly one density-1 U polygon in locF and no polygon in locT. Add U's edge support lines and vertices to the F support lines and breakpoints in §5.3. At each candidate vertex, add area(Q∩U) to segment mass and use the same guarded rational-function test as in §5.4.

**Proof for x.** Since y0−H≥α, Q lies entirely in y≥α, and the area depends only on z_x. Let ℓ(t) be the vertical cross-section length relative to the center. The lost area is g(z_x)=∫_{−∞}^{α−z_x}ℓ(t)dt. For z_x≥α, ℓ is nondecreasing on t≤0, so g''=ℓ'(α−z_x)≥0. Thus 1−g is concave, with one-sided derivatives at breakpoints, and adding the affine segment expression preserves concavity on each arrangement polyhedron. Every point is a convex combination of vertices; a concave function's value is at least the minimum vertex value. The vertex-only B3' test applies without B4 critical values.

### 5.8 B3T:x and B3T:y: the tangent lemma

The condition `tangent_ok` is:

- x: x1≤α and y0−H≥α;
- y: y1≤α and x0−H≥α.

Use threshold 1 and segments only in locF/locT; do not combine this mode with B3U. For x, let c*=(x0+x1)/2 and c_o=y0, and define

A(u)=area(Q((c*,c_o),u)∩{x≥α}), D(u)=length(Q((c*,c_o),u)∩{x=α}),
L(u,p)=A(u)+D(u)(p_x−c*).

For y, use c*=(y0+y1)/2, c_o=x0, center (c_o,c*), half-plane y≥α, chord y=α, and displacement p_y−c*. Represent the half-plane by a polygon truncated at ±1000 and the chord by a segment of length 2000 and mass 2000, hence density 1. Compute A,D as guarded rational functions of u, not as numerical values at a fixed sample. At the vertices of the segment-only arrangement from §5.3, prove segment mass+L≥1 by §5.4.

**Proof for x.** For z_x≤α, the area is g(z_x)=∫_{α−z_x}^{w}ℓ(t)dt. We have g'=ℓ(α−z_x), g''=−ℓ'(α−z_x)≥0 because ℓ is nonincreasing for t≥0. Thus g is convex and lies above its tangent L. Segment mass+L is affine on each arrangement polyhedron and attains its minimum at a vertex, proving a lower bound for the true mass. Negative tangent values at some positions do not invalidate the lower bound.

### 5.9 CORE1 family: common segment pieces at box corners

Write B=[x0,x1]×[y0,y1]×[e0,e1], J=(u0,u1), α=UA, and H=hmax(u0,u1) from §5.1. All nine CORE1 kinds require positive widths in all four leaf coordinates, u1≤0 or u0≥0, and

x0≥H, y0≥H, x1≤20−H, y1≤20−H.

These are tests on the entire box: do not clip its center intervals to the admissible domain. Let C be the eight corners p=(p_x,p_y,p_δ) of B. Use the F and T segment localization of §5.3, with their stored total masses and no mass scaling. For each segment A+t(B−A), compute the parameter width h=t_hi−t_lo by §5.1 at every corner, with num=1/2−n·(A−(p_x,p_y)) and den=n·(B−A). For T, replace p_x by p_x−p_δ. Preserve negative widths instead of replacing them by zero. A parallel constraint with den=0 and num<0 makes that segment unavailable. Retain a segment only if it is available and h≥0 at all eight corners; a zero width is allowed. At corner p its contribution is m h. For a V row use endpoints (xl,y_v) and (2+p_δ,y_v), apply the same all-corners test, and contribute ρ(2+p_δ−xl)h. Discard every piece failing this test at any corner. Denote the retained sum at p by M_ret(u,p). The family format contains no point masses.

All these comparisons use exact rational functions of u with guards. On each component of J without guard roots, the retained pieces and clipping branches are fixed. For fixed u, their physical intersection lengths are concave on B when their widths are nonnegative at all corners, so corner lower bounds extend to the box. The following U terms are either concave or affine under the specified hypotheses.

Define U_f as the family's stage-B polygon: [α,20]² by default, or the supplied U polygon. Put G_U(u,p)=area(Q((p_x,p_y),u)∩U_f). Define H_x=[α,20]×[0,20], H_y=[0,20]×[α,20], and G_x,G_y as the corresponding intersection areas. These rectangles represent the two half-planes on admissible squares. Let L_x,L_y be the tangent terms of §5.8, with c*=(x0+x1)/2, c_o=y0 for x and c*=(y0+y1)/2, c_o=x0 for y; their polygon and chord truncation is at ±1000. Polygon areas and tangent terms are computed symbolically by the exact clipping rules, including all guards. The quadrant-based concavity and half-plane lower-bound arguments require the standard U geometry as in §3; the numerical G_U test uses U_f literally and does not test an arbitrary supplied polygon for concavity.

For the two-cut condition define ℓ=min(|u0|,|u1|), m=max(|u0|,|u1|) and

D_diag = max((1−ℓ²)/(1+ℓ²), 2m/(1+m²)) if m≤1; D_diag=1 if m>1.

On a one-sided angular interval this bounds max(|c(u)|,|s(u)|). The guard x0+y0−D_diag≥2α ensures that the two portions cut off below the quadrant edges do not overlap in positive area.

- **CORE1:P.** No additional coordinate hypothesis. Compute P_lo by the exact rational polygon bound of §5.2. At every p∈C require M_ret(u,p)≥1−P_lo. This bounds segment mass while P_lo bounds the area contribution.
- **CORE1:Tx.** Require x1≤α and y0−H≥α. At every p∈C require M_ret(u,p)+L_x(u,p)≥1.
- **CORE1:Ty.** Require y1≤α and x0−H≥α. At every p∈C require M_ret(u,p)+L_y(u,p)≥1.
- **CORE1:TxHy.** Require x1≤α and y0≥α. At every p∈C require M_ret(u,p)+L_x(u,p)+G_y(u,p)≥2. The area lower bound is L_x+G_y−1.
- **CORE1:TyHx.** Require y1≤α and x0≥α. At every p∈C require M_ret(u,p)+L_y(u,p)+G_x(u,p)≥2. The area lower bound is L_y+G_x−1.
- **CORE1:x.** Require x0≥α and y0−H≥α. At every p∈C require M_ret(u,p)+G_U(u,p)≥1.
- **CORE1:y.** Require y0≥α and x0−H≥α. At every p∈C require M_ret(u,p)+G_U(u,p)≥1.
- **CORE1:xy.** Require x0≥α, y0≥α, and x0+y0−D_diag≥2α. At every p∈C require M_ret(u,p)+G_U(u,p)≥1.
- **CORE1:xyh.** Require x0≥α and y0≥α, with no disjointness guard. At every p∈C require M_ret(u,p)+G_x(u,p)+G_y(u,p)≥2. Inclusion-exclusion gives the area lower bound G_x+G_y−1.

For each kind, let v=N/D be the left-hand side and τ the stated right-hand side. Acceptance requires (N−τD)D≥0 on every open guard component for all eight corners, using §5.4. Split at interior guard roots and reevaluate; reject if any value fails or 60 sampling attempts cannot resolve a component. Angular boundary values are completed by §5.4 and §6.3. Replay uses exact rational functions and polynomial sign tests for every CORE1 kind, including P; it has no interval-enclosure pretest or fallback to another leaf kind.

### 5.10 B3U:xy and B3U:xyh: two-cut concavity bounds

Both kinds require positive box widths and u1≤0 or u0≥0. Use B, J, α, H, D_diag, H_x, H_y, G_x, and G_y as in §5.9. The tested domain is B intersected with w(u)≤z_x,z_y≤20−w(u); the stronger CORE1 whole-box domain guard is not imposed. Let M(u,p) be the full segment mass from §5.4, without the CORE1 piece selection.

- **B3U:xy.** Require x0≥α, y0≥α, and x0+y0−D_diag≥2α. Construct U_q=[α,20]² of density 1, irrespective of a supplied U field, and set G_q(u,p)=area(Q((p_x,p_y),u)∩U_q). Its local-polygon guard requires α<20 and, with r=7072/10000, 20≥x0−r, α≤x1+r, 20≥y0−r, α≤y1+r. Add its edge support lines and vertices to the F arrangement data of §5.3, with no T polygon. At every admissible arrangement vertex require M(u,p)+G_q(u,p)≥1. The disjointness guard makes the quadrant area the sum of the two concave half-plane areas minus 1.
- **B3U:xyh.** Require x0≥α and y0≥α. Construct the two density-1 rectangles H_x,H_y, with no local-polygon intersection guard and no T polygon. Add both polygons' edge support lines and vertices to the F arrangement data. At every admissible arrangement vertex require M(u,p)+G_x(u,p)+G_y(u,p)≥2. Here G_x+G_y−1 is a lower bound for the quadrant area even when the cut-off portions overlap. This mode uses two polygons, not the single-polygon condition of §5.7.

For each kind enumerate the three-plane intersections and apply all ten membership inequalities of §5.3. Compute segment and polygon terms as exact guarded rational functions and apply §5.4 with τ=1 for xy or τ=2 for xyh: every required value v=N/D must satisfy (N−τD)D≥0 on every applicable open component. Complete the boundaries by §5.4 and §6.3. There is no interval-enclosure acceptance route, edge-critical-value stage, or fallback after a failed hypothesis or value. These tests use the constructed quadrant or half-planes; they do not validate their relation to an arbitrary supplied U, which remains subject to the geometry requirements of §3.

### 5.11 B4U: polygon mass with arrangement-edge critical values

Require positive widths in all four coordinates and u1≤0 or u0≥0. Use the actual stage-B polygon U_f of §5.9, with density 1, in F and no polygon in T. No concavity, tangent, or CORE1 whole-box domain condition is imposed. Localize F and T as in §5.3. With r=7072/10000, reject if U_f has fewer than three vertices or all its vertices satisfy any one of x<x0−r, x>x1+r, y<y0−r, or y>y1+r. Require exactly one local density-1 F polygon, no T polygon, and no point masses in either local measure. For each directed polygon edge P→R, insert and verify the F support line

(R_y−P_y)x+(P_x−R_x)y=(R_y−P_y)P_x+(P_x−R_x)P_y,

and insert and verify P among the F breakpoints. The polygon's validity and orientation are subject to §3 and §7.1.

Form the arrangement of §5.3 including these polygon contacts, the six box faces, and the four admissibility faces. Let

g(u,p)=area(Q((p_x,p_y),u)∩U_f), f(u,p)=M(u,p)+g(u,p),

where M is the full F/T/V segment mass. Acceptance requires both of the following stages, with threshold exactly 1.

1. **Vertices.** Enumerate all three-plane intersections whose determinant is not identically zero, split at determinant and membership roots, and impose all ten inequalities of §5.3. At each admissible vertex prove f(u,p)≥1 by §5.4, including polygon clipping guards.
2. **Edges.** For each pair of retained arrangement planes, form the cross product d of their coefficient vectors. Skip the pair only if d is identically zero. Intersect the pair with every other plane, omitting identically zero three-plane determinants, and retain points satisfying the same ten membership inequalities at the guarded sample. Sort these points by d·p using guarded comparisons. For every consecutive pair p,q that is not identical as a triple of rational functions, put m_pq=(p+q)/2 and compute

   A=2[g(u,p)−2g(u,m_pq)+g(u,q)], B=f(u,q)−f(u,p)−A.

   If A>0 and 0<t*=−B/(2A)<1, require

   f(u,p)+B t*+A(t*)² = f(u,p)−B²/(4A) ≥ 1.

   Otherwise this pair produces no interior critical value; the vertex stage supplies its endpoint checks. Membership, sorting, polygon clipping, A>0, and both strict inequalities for t* are guarded.

All coordinates, areas, coefficients, and values are exact rational functions of u. For every edge value v=N/D prove (N−D)D≥0 on its open guard component by the polynomial sign test of §5.4. The edge stage uses the odd-multiplicity-root test without the root-free shortcut; if the sign sample is a zero, resample toward the right endpoint until a nonzero sign is obtained.

The edge components must cover J without gaps. Start a frontier at u0 and reset the sampling cap to u1 after each completed component. Refine the frontier until its rational upper isolating bound lo is below the cap, and start sampling at (lo+cap)/2. A guarded run gives the maximal open component (L,R) containing its rational sample and having no guard roots. Accept that component only when L≤frontier and all its critical values pass; then set frontier=R. If L>frontier, reduce the sampling cap to a rational lower isolating bound of L and retry. Each sampling sequence permits 60 attempts, with a resample s replaced by lo+(s−lo)·2/3, where lo is the current rational upper isolating bound of the frontier. Exhaustion rejects. With a limit of 2000 completed runs, reject when runs+1≥2000 on a cap-reduction branch, or when runs≥2000 after a completed component, even if that component reaches u1. Acceptance requires the frontier to equal u1 and both stages to pass; errors or exhausted limits do not invoke another test. Roots and endpoints are completed by §5.4 and §6.3. For fixed u, the area depends only on the two center coordinates and segment mass is affine on each arrangement cell; the quadratic minimum argument of §5.4 reduces the remaining checks to vertices and these edge critical values.

### 5.12 Dispatch

`replay4d` matches complete, case-sensitive kind strings. EMPTY and CORE select §5.2; B3D selects §§5.3–5.4; EDGE selects §5.5; B3U:x/y select §5.7; B3T:x/y select §5.8; the nine CORE1 strings select §5.9; B3U:xy/xyh select §5.10; and B4U selects §5.11. The slash notation here lists alternatives, not literal kind strings. Exactly EX:CORE, EX:B3D, EY:CORE, and EY:B3D select §5.6: first check the appropriate side condition on the original family, then run the named base test on the derived X or Y family. EX: and EY: are not general-purpose prefixes.

Reject all other strings, including bare CORE1 or B3U, CORE1I:P, F3D, B1, B2, TIERB, and any other prefixed combination. Every dispatched leaf must have positive coordinate widths. All B3D, B3U, B3T, CORE1, and B4U tests reject u0<0<u1, including B3D under EX/EY; zero as an endpoint is permitted. A failed side condition, domain guard, value proof, arithmetic operation, or caught calculation failure rejects the leaf; dispatch does not try a different kind. Full record acceptance also requires the independent root and tiling checks of §6.

## 6. Record JSONL format and tiling

### 6.1 Lines

JSONL contains one JSON value per line. A typical initial line has this form:

```json
{"header":{"argv":["search-tool","family.json","..."],"roots":9828}}
```

`argv` and `roots` describe provenance and an expected count; they are not proof. The checker skips lines containing `header`, so it must verify the actual roots, region, and family separately. A header need not contain a family hash. Bind the family actually used for recomputation through the results and hashes.

A root line has the following form; this example illustrates syntax only:

```json
{"root":["0","1/10","0","1/10","-1/32","0","19/50","2/5"],
 "leaves":[[["0","1/10","0","1/10","-1/32","0","19/50","2/5"],"EMPTY"]],
 "uncert":[],"cpu":0.01,"f3d":[]}
```

| Key | Specification |
|---|---|
| `root` | Eight rational strings in the order (x0,x1,y0,y1,u0,u1,e0,e1). |
| `leaves` | Array of `[box,kind]`; box has the same eight entries in the same order, and kind is a leaf-kind string. |
| `uncert` | Array of unproved `[box,reason]` entries. Must be empty for every root used as proof. |
| `cpu` | Measured elapsed wall-clock seconds for the root; not used for acceptance. |
| `f3d` | Auxiliary F3D records `[[box4,[[box3,kind3],…]],…]`, where box3 is (x0,x1,y0,y1,u0,u1). Empty in the standard published records covered by this specification. |

`F3D` denotes a route using F+V(e0)+U and the lower density envelope over δ of horizontal T pieces, followed by three-dimensional A/B tests. It discards vertical T pieces and uses the horizontal density g(x)=inf_{δ∈[e0,e1]}f_0(x−δ), giving a measure lower bound. Its auxiliary kinds CORE/EMPTY/B1/B2/TIERB and three-dimensional tiling do not provide full recomputation of its B-type auxiliary leaves under this specification. Reject F3D as unsupported for proof acceptance. Outputs containing `box`, `F`, and `T`, or only leaf counts, are not interchangeable with this JSONL format.

### 6.2 Tiling by leaves and roots

Every box must have lower endpoint<upper endpoint in every coordinate. Leaf interiors within a root must be disjoint; shared boundaries are permitted. Equality of summed volumes is insufficient. Require reconstruction of this bisection tree:

- If there is one leaf and it equals the root, accept.
- Otherwise, try axes in order u, δ, x, y, taking the root's **midpoint** m on that axis.
- Partition all leaves into those with upper endpoint≤m and those with lower endpoint≥m. Choose an axis for which both groups are nonempty and no leaf crosses m.
- Bisect the root exactly on that axis and recurse on both children. Reject if no axis permits a split.

Exact equality at the terminal boxes also detects leaves outside the root, missing leaves, and extra duplicates.

Extract the interval sets Xs,Ys,Us,Ds from all root lines. Each must consist of positive-width adjacent intervals without gaps or interior overlaps. They must partition the specified [X0,X1], [Y0,Y1], the family's [d0,d1], and [U0,U1], respectively. The root set must be exactly Xs×Ys×Us×Ds, with each root appearing once. An equivalent test checks membership in this product, uniqueness, and count equal to the product of the four interval counts. Reject integer overflow in that product. Also require the 90-degree angular coverage condition of §4.1.

When assembling a record from multiple sources, retain exactly one completed row for each root. Duplicate roots are forbidden even if their rows agree.

### 6.3 u=0 and boundaries

No root may contain u=0 in its interior. B3D, EX/EY:B3D, B3U, B3T, CORE1, and B4U leaves likewise forbid u0<0<u1. Intervals [-h,0] and [0,h] with u=0 as an endpoint are permitted. CORE/EDGE give direct lower bounds on closed intervals and can handle u=0, but the root rule is common to all kinds.

The mass of a closed square is upper semicontinuous in its pose: the upper limit of the indicator functions is at most the indicator of the limiting closed set, and integration against a finite measure gives the result. Translations of T and length changes of V are also covered by this finite-measure limiting argument. Every admissible u=0 pose is the limit of admissible u≠0 poses, moving the center continuously if necessary. Thus mass≥1 nearby implies mass≥1 at u=0. This upper semicontinuity closes the boundary; u=0 is not left as a hole. At box boundaries, the required neighboring poses may lie in adjacent boxes, so apply the argument together with the verified tiling of the entire domain.

## 7. Verification procedure, intervals, and completion

### 7.1 Acceptance order

1. Validate the family format, nonnegativity, axis alignment, V lengths, and U's orientation, shape, and truncation boundaries.
2. Verify with rational arithmetic the wall-period mass 9/5, reversal, transpose and repetition identities, corner and terminal assignments, and the formulas for M_C and S. Verify the right-side and X/Y derivations as well.
3. Fix the δ interval and required local regions. For each region, check the Cartesian product of roots, empty unproved lists, bisection trees, leaf kinds, and u=0 conditions.
4. Recompute **every leaf** using its mathematical acceptance test. Passing samples, a search tool's VERIFIED status, or the recorded leaf-kind string cannot substitute for this recomputation.
5. Verify the union of local regions and the reduction to the global construction. Then verify that the family's S(δ) is at least the certified line S_i(δ) on each interval.
6. Verify that the union of δ intervals covers (0, 1], establishing all measure hypotheses used to prove the theorem in §1.

In the published bundle these steps are done by two tools:

| Step | Tool | Receipt |
|---|---|---|
| 1, 2, the saving at both ends against the certified line, k = 7, 8, 9 global/local agreement, wall shifts and terminal line (part of 5) | `structure/validate_family.py`, run on all 68 families by `structure/structure_all.py` | `receipts/structure.json` |
| the certified line equals the line through the recomputed endpoint savings; region bounds as required by §2.3 (4) (part of 5) | `structure/structure_all.py` | `receipts/structure.json` |
| 3, 4 | `replay4d` (via `checker/replay_all.py`) | `receipts/replay.json`, `receipts/published_checker.json` |
| 6 | `intervals.json` (endpoints) and `INTERVALS.md` | — |

Comparison of affine expressions requires only their endpoints.  To reuse a record after increasing a family's measure, either verify original measure≤modified measure for every δ or recompute all leaves against the modified family. Recompute savings to include the reduction caused by the additional mass.

### 7.2 Certified intervals and full replay

The 34 intervals cover (0, 1]. Every leaf of every record—187,183,108 leaves in 136 records—was recomputed once with `replay4d` and accepted. This full replay is the basis for the verified claim.

The per-interval list is in `INTERVALS.md` and the machine-readable `intervals.json`. For each interval, these identify the δ range and open/closed endpoints, hashes of the original and right-side families, the certified line S_cert(δ) = αδ + β, and the four regions' record hashes, roots, leaf counts by kind, and region bounds. Full replay results are in `receipts/`.

**Coverage check.** Sort intervals by their exact rational endpoints. Verify that the first starts at 0, the last ends at 1, consecutive right and left endpoints agree without a gap or interior overlap, and each shared endpoint belongs to at least one adjacent interval. Right endpoints are closed; left endpoints follow their declared status. Summed interval lengths alone are insufficient. The published intervals satisfy these conditions.

### 7.3 Structural transitions and joining intervals

At δ=j/5, where j is an integer and W=2+δ crosses the 1/5 grid, the model structure can change because a final horizontal segment has length 0 or a fixed grid line appears. Within one family, keep the F/T/V classification fixed and maintain xl≤2+d0 for V. Split intervals at these transitions and certify the transition itself through the left family's closed right endpoint or the right family's closed left endpoint. The two measures need not agree, but each must satisfy segment validity and saving requirements. Do not use floating-point approximate equality to decide membership at δ=j/5.

`INTERVALS.md` identifies the intervals owning each shared endpoint. All right endpoints are closed, and left endpoints are closed by default. The open-left intervals are (0, 1/50], (2/5, 81/200] and (99/100, 1]. The value δ = 0 is excluded; square numbers use the area bound.

- δ = 2/5, the target's jump, belongs to the left-branch interval [19/50, 2/5] through its closed right endpoint. The next interval (2/5, 81/200] is open on the left.
- δ = 99/100 belongs to [4/5, 99/100]; the next interval (99/100, 1] is open on the left.
- Every other shared endpoint belongs to both adjacent closed intervals. Both families satisfy the structural and saving checks there, so either may cover it.

No adopted family spans a structural transition: no interval contains a grid transition δ = j/5 in its interior.

## 8. Pitfalls

1. **Boundary mass at u=0.** A segment coinciding with a square edge is counted in full as part of the closed set. Intersection at a single endpoint has segment mass 0. Mass is upper semicontinuous, not necessarily continuous, and its value at a grid point can exceed limits from open cells. For an affine wall-profile expression, approach each corner of an open cell from within and take the limit using 2m(c+εd)−m(c+2εd). This concerns u=0 wall constraints, not proof for tilted poses.
2. **Wall mass cannot be multiplied by (1+eps).** Raising period mass above 9/5 adds excess over 4(k−4) periods proportional to k, invalidating the k-independent formula for S. Distinguish a corner mass margin from the exact wall equality. Scaling all segments for a fixed N is not a valid family export rule for general k.
3. **Sampling can miss configurations.** Examples of configurations requiring care include (i) a slight tilt touching a wall, u=−11/2500, c_y=2899/1000, c_x=w; (ii) a 45-degree configuration, c≈(2.40711,2.70), δ=0.38; (iii) a non-axis-parallel configuration with a vertex on a U-edge line, c≈(2.56990,2.30716), u≈0.43451, δ≈0.38047; and (iv) a center crossing a T corner line, c=(2.4,1), u≈−0.150472, δ=0.40. Approximate coordinates alone are not exact counterexample certificates. The example family includes an additional 1/2500 on each applicable T row at x=2; this mass is already stored and must not be added again.
4. **Floating point is not an acceptance criterion.** An f64 search can identify counterexample candidates, but failure to find one is not proof. Branch decisions, determinants, root isolation, densities, savings, and grid identities must all be exact. Floating point is permissible for timing displays or search-order choices.
5. **Even-multiplicity roots and hashes.** Require the positive sign at a nonroot in §5.4, and never decide plane or value equality solely by hashes.

## 9. Reproduction and file identity

### 9.1 Published bundle layout

Release `closed-form-v1` of `wand125/square-packing` contains one asset per interval, named `interval_<d0>_<d1>.tar.gz`, with d0 and d1 written in decimal. Each archive unpacks to:

```text
interval_<d0>_<d1>/
  family.json
  family_right.json
  straddle.rec
  left.rec
  top.rec
  right.rec
  SHA256SUMS
```

`family_right.json` is the right-side family. The four `.rec` files contain the JSONL records of the four regions. A region whose record was split for replay is still published as a single record. The release also includes a top-level `SHA256SUMS` covering the 34 tarballs.

The repository layout is:

```text
problems/closed-form/
  README.md
  SPEC.md
  INTERVALS.md
  intervals.json
  checker/
  receipts/
  ASSET.json
```

`checker/` is a Rust workspace with crates `seam4d_core` and `replay4d`. `receipts/` contains the full replay results. `intervals.json` has `schema`, `release_tag` and `intervals`. Each interval entry has `index` (1–34), rational
strings `d0`, `d1` and their decimal forms `d0_decimal`, `d1_decimal`, `open_left`, `closed_right`, `asset`,
`asset_sha256`, `asset_bytes`, `family_sha256`, `family_right_sha256`, `certified_line` with `alpha` (slope α_i) and
`beta` (intercept β_i), and `regions`. The region keys are `straddle`, `left`, `top` and `right`; each has `file`,
`sha256`, `bytes`, `bounds` (x0, x1, y0, y1 as rational strings), `family` (`family.json` or `family_right.json`),
`roots`, `leaves`, `leaf_kinds` and `replay_ok`.

The repository folder also contains `a_of_n.py` (computes a(N) from `intervals.json`), `LICENSE`, and in
`checker/` the script `replay_all.py`.

### 9.2 What the published checkers cover

`replay4d` checks the records: the domain and tiling conditions of §6 and every leaf test of §5. It reads the
family but does not check its structure (rows of weight ≤ 0 are dropped when the cover is built, not
rejected). The structure of the families is checked by `structure/validate_family.py` (Python 3, standard
library only, exact rational arithmetic), which `structure/structure_all.py` runs on all 68 families; see the
table in §7.1. `validate_family.py` takes the certified line as `--line-alpha=α --line-beta=β` and requires the
recomputed saving to be at least that line, and above δ/2, at both ends of the interval.

The published families differ from the ones used for the full replay only by the removal of two keys that no
checker reads (`note`, a free-text comment, and `target`, a search target); `receipts/families.json` lists the
old and new SHA-256 of every family. Intervals 1 and 34 were replayed again with the published families and
the published build.

### 9.3 Rust full replay

For each region, run:

```sh
replay4d family.json <region>.rec --region x0 x1 y0 y1 --threads T
```

Use `family_right.json` for the right region. Replace `<region>` with `straddle`, `left`, `top`, or `right`, use the exact region bounds from `intervals.json`, and set T to the desired thread count. Verify all four records for each of the 34 intervals.

Success is `REPLAY OK` with exit code 0; verification failure is `REPLAY BAD` with exit code 1; input or argument errors use exit code 2. Also check the result JSON fields `ok`, `bad_count`, and `mode`. The `--leaves` mode checks only extracted `[box,kind]` lines and omits domain and tiling checks, so it is not a full-domain proof.

The published checker supports all leaf kinds appearing in the records: EMPTY, CORE, B3D, EDGE, the EX/EY variants, B3U:x/y/xy/xyh, B3T:x/y, the CORE1 variants P, x, y, xy, xyh, Tx, Ty, TxHy, TyHx, and B4U. The corresponding CORE1 leaf names are `CORE1:P`, `CORE1:x`, `CORE1:y`, `CORE1:xy`, `CORE1:xyh`, `CORE1:Tx`, `CORE1:Ty`, `CORE1:TxHy`, and `CORE1:TyHx`.

The Rust checker is a port of the development checker, not an independent second implementation. Reproduction with the published checker and independent implementation are distinct forms of verification.

### 9.4 SHA-256

Verify the 34 archive hashes against the release's top-level `SHA256SUMS`, then verify each unpacked bundle against its own `SHA256SUMS`. Compare the family and record hashes with `intervals.json` and the replay receipts. Hash raw bytes: changing JSON whitespace or line order changes the hash even when the represented measure is unchanged.

Replay result fields include `family.sha256`, each `records[].sha256`, `version`, and `source_sha256`. The source hash concatenates, in the checker's specified source order, each relative UTF-8 name, a NUL byte, the content length as a 64-bit big-endian integer, and the content bytes, then hashes that concatenation. It is not a concatenation of individual source-file hashes. The covered files are, in order, `replay4d/Cargo.toml`, the workspace `Cargo.toml`, `Cargo.lock`, `replay4d/src/main.rs`, `replay4d/src/sha256.rs`, `seam4d_core/Cargo.toml` and `seam4d_core/src/{lib,fast,b3d,replay}.rs`; `seam4d_core/src/b3d_sort.rs` and the test files are not covered. For inputs, hash the same bytes that are actually parsed. Hashes establish identity, not mathematical correctness.

## Appendix A. Formula and acceptance checklist

This table summarizes the mathematical checks and their acceptance semantics without relying on the search tools.

| Item | Required formula or check |
|---|---|
| A/B and branches of a(N) | Use the ordered cases in §1.1; a(N) need not solve the equality at a jump or cutoff. |
| S and m_v | Recompute corner mass and the terminal-line term exactly, including endpoint savings. |
| F/T/V | T translates by +δ; V stores density; eps is not a loading-time multiplier. |
| Right-side family | F_right=T_original and T/V are empty; U gives a lower bound by inclusion. |
| X/Y | Check removal conditions, vertex order, and preservation of UA and the δ interval. |
| W_min and EMPTY | Use the endpoint/0 minimum and the strict EMPTY inequalities. |
| Core P and outer polygon O | Check endpoint normals, chord constraints, support-function reduction, and tangent intersections. |
| CORE | Use both endpoint erosions for T, V(e0), and the maximum of the inner and outer area bounds. Reject None. |
| P_lo and τ | P_lo=max(inner area bound,outer area bound,0); τ=1−P_lo. |
| Planes and 10 membership conditions | Use T coefficients γ=−l_x/−n_x, the V moving endpoint 2+δ, and side=20. |
| Guards and threshold | Symbolic clipping must prove (N−τD)D≥0. |
| nonneg_open | Exclude interior odd-multiplicity roots, resample at even roots, and require the final >0 at a nonroot. |
| hmax | Use the formula for m≤2/5 and otherwise 7072/10000. |
| D_X | Midpoint evaluation or an endpoint sweep must compute the minimum of the same piecewise-constant total density. |
| D_Y | Subdivide x and δ and minimize the total density, rather than summing separate envelopes. |
| EDGE | Require x0,y0≥α; compare densities only for positive protrusion depths. |
| EX/EY | Check density conditions using the original family; perform CORE/B3D with the variant. |
| concave_ok | Require x0≥α,y0−H≥α, or interchange x and y. |
| tangent_ok | Require x1≤α,y0−H≥α, or interchange x and y. |
| Tangent term | c* is the relevant axis midpoint, the other coordinate is its lower endpoint, the truncation bound is 1000, and the term is A+D(p−c*). |
| CORE1:P | §5.9 common domain and all-corners piece selection; all eight M_ret≥1−P_lo by exact guarded polynomial tests, with no interval pretest. |
| CORE1:Tx | §5.9 common rules; x1≤α, y0−H≥α; all eight M_ret+L_x≥1. |
| CORE1:Ty | §5.9 common rules; y1≤α, x0−H≥α; all eight M_ret+L_y≥1. |
| CORE1:TxHy | §5.9 common rules; x1≤α, y0≥α; all eight M_ret+L_x+G_y≥2. |
| CORE1:TyHx | §5.9 common rules; y1≤α, x0≥α; all eight M_ret+L_y+G_x≥2. |
| CORE1:x | §5.9 common rules; x0≥α, y0−H≥α; all eight M_ret+G_U≥1 using the actual stage-B U polygon. |
| CORE1:y | §5.9 common rules; y0≥α, x0−H≥α; all eight M_ret+G_U≥1 using the actual stage-B U polygon. |
| CORE1:xy | §5.9 common rules; x0,y0≥α, x0+y0−D_diag≥2α; all eight M_ret+G_U≥1. |
| CORE1:xyh | §5.9 common rules; x0,y0≥α; all eight M_ret+G_x+G_y≥2, with two half-plane rectangles. |
| B3U:xy | §5.10; x0,y0≥α, x0+y0−D_diag≥2α and local-quadrant guard; M+G_q≥1 at every admissible arrangement vertex by §5.4. |
| B3U:xyh | §5.10; x0,y0≥α; two half-plane rectangles and their contacts; M+G_x+G_y≥2 at every admissible arrangement vertex by §5.4. |
| B4U | §5.11 polygon and locality guards; f≥1 at admissible vertices and f(p)−B²/(4A)≥1 when A>0 and 0<−B/(2A)<1 on adjacent arrangement edges; exact §5.4 tests and complete edge-component coverage required. |
| Dispatch | §5.12 exact kind matching; only EX/EY:CORE and EX/EY:B3D use variants; reject unsupported kinds and failed tests without fallback. |
| Root generation | The example uses pitch=1/10, angular spacing 1/32, 27 angular intervals, and one δ interval; verify all four root counts in §4.2. |
| Leaf tiling | Reconstruct midpoint bisections in the order u,δ,x,y. |
| Domain | Verify four axis partitions, their exact Cartesian product, no duplicate roots, a_u+b_u+a_u b_u≥1, and no interior u=0. |
| Recomputation scope | Every leaf must be recomputed; a structural check or a sample is insufficient. |

For Cartesian-product verification, membership, uniqueness, and the product cardinality are equivalent to explicit product equality. Positive widths are mandatory. A CORE result of None is rejected, regardless of whether a sampling implementation would omit that comparison. B3U/B3T/CORE1/B4U support is required for the published records.
