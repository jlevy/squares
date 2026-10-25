# Task 05 / C580 — complete mathematical exclusion

**Status: MATH_DONE; formal acceptance pending.**

This document completes the mathematical C580 case by composing its actual-owner entrance with a continuous three-square contradiction. It contains the case proof, the local geometric proofs used in that composition, and an optional exact finite checker. No Lean implementation, compilation, row registration, repository change, or acceptance receipt is claimed.

The decisive case-level simplification is

\[
\boxed{\text{19 local labels}\ \longrightarrow\ 8\text{ joint assignments}
\ \xrightarrow{\ F_5\in W\ }\ 1\text{ assignment}
\ \longrightarrow\ \text{one physical three-square theorem}.}
\]

The existing handoff correctly identified the shared ending as a source candidate already present. This continuation does **not** claim that its local geometric lemmas or terminal contradiction were newly discovered. It supplies the fresh finite reconstruction, the single-assignment reduction, the C580-specific proof composition, and explicit actual-owner and boundary checks. The proof below uses the stronger true C580 fact that the southeast square owns F4, rather than needing every generalization in the weaker shared source interface.

There is no remaining mathematical sector of the normalized C580 family in the theorem below. This is one case of the twelve-square proof, not a new assertion that every other case or the global theorem has been accepted. C581 is not marked complete here.

## 1. Exact theorem and physical owners

**Theorem.** There are no twelve congruent open squares of common side

\[
1<a\leq\frac{1001}{1000},
\]

with pairwise disjoint interiors, closures in \([0,4]^2\), and exact original-marker family

\[
\{1,2,8,48,192,512,1024,2304,4096,8192,16384,32768\}.
\tag{C580}
\]

A marker mask specifies the **exact** set of markers strictly inside its owner. A marker absent from a mask may touch that square's boundary. All terminating decimals in this document denote exact rationals.

Use ascending-mask order throughout:

| Index | Mask | Name | Original strict markers |
|---:|---:|---|---|
| Q0 | 1 | lower-left horizontal singleton | (1,.914) |
| Q1 | 2 | lower-left vertical singleton | (.914,1) |
| Q2 | 8 | lower-right singleton | (3.086,1) |
| Q3 | 48 | paired northeast corner | (3,3.086), (3.086,3) |
| Q4 | 192 | paired northwest corner | (1,3.086), (.914,3) |
| Q5 | 512 | E, southeast central | (2.35,1.65) |
| Q6 | 1024 | N, northeast central | (2.35,2.35) |
| Q7 | 2304 | W, merged western central | **(1.65,1.65), (1.65,2.35)** |
| Q8 | 4096 | L, left wall | (.914,2) |
| Q9 | 8192 | B, bottom wall | (2,.914) |
| Q10 | 16384 | R, right wall | (3.086,2) |
| Q11 | 32768 | T, top wall | (2,3.086) |

In particular, the actual bottom owner is **8192**, not the C581 owner8196. The marker (3,.914) is not owned by any square of this C580 family. Q2 is a genuine singleton; **(3,1) is never assumed to belong to it**. W is one physical square owning two western central markers, not two different central squares.

The retained original-row dictionary identifies this family as original case580, zero-based row321 among577 rows. This document proves the family contradiction. Applying it to any retained row with that exact group set is the mathematical row implication; a formal row adapter and registry update are separate, unperformed work.

### 1.1. Seed points are proved, not silently added

The singleton and paired-corner lemmas in [Appendix A](#appendix-a) give:

| Actual owner | Additional strict points used here |
|---|---|
| Q0 | (1.12,1), (1.74,1), (1.87,.76) |
| Q1 | (1,1.12), (1,1.74), (.76,1.87) |
| Q2 | (3,1.12), (3,1.74), (3.24,1.87) |
| Q3 | (3,3) |
| Q4 | (1,3) |

Q1's seeds are the transpose of the Q0 seed theorem; Q2's are its images under \((x,y)\mapsto(4-y,x)\). Each singleton excludes **all other original markers**, exactly as the seed theorem requires. No globally absent-marker premise is substituted for an individual exclusion.

The closed convex hull of finitely many strict points lies inside the same open square. Thus segments below are strict in their named owner, including their endpoints.

## 2. Exact finite entrance: nineteen labels, eight assignments

The two auxiliary sets, with their exact ordering, are:

| j | Fj | Gj |
|---:|---|---|
| 0 | (1,1.74) | (1,1.6) |
| 1 | (1,2.26) | (1,2.4) |
| 2 | (1.6,1) | (1.74,1) |
| 3 | (1.6,3) | (1.74,2) |
| 4 | (2,1.74) | (1.74,3) |
| 5 | (2,2.26) | (2.26,1) |
| 6 | (2.4,1) | (2.26,2) |
| 7 | (2.4,3) | (2.26,3) |
| 8 | (3,1.74) | (3,1.6) |
| 9 | (3,2.26) | (3,2.4) |

Encode a strict auxiliary membership set by

\[
m=\sum_{F_j\text{ owned}}2^j+\sum_{G_j\text{ owned}}2^{10+j}.
\]

For F, the exceptional owners in the non-avoidance lemma are Q3,Q4,W: three owners. Every other owner has one or two F points; each exceptional owner has zero or one. For G there are only two exceptional owners, Q3,Q4. Consequently every other owner has **exactly one** G point, and Q3,Q4 have none. These bounds follow by counting ten points among twelve disjoint actual owners; they are not assumptions about a prospective arrangement.

Apply the sound local rule of Appendix A: include the genuine seeds; reject an auxiliary label only by a forbidden point in its strict convex hull, a proved local point obstruction, or the strict four-point crossing obstruction; then delete labels conflicting with another owner's compulsory point. The true labels of any packing survive every deletion.

Fresh exact reconstruction for the groups in (C580) gives the complete necessary component lists:

| Actual owner | Every surviving component label |
|---|---|
| Q0 | 4100 |
| Q1 | 1025 |
| Q2 | 262400 |
| Q3 | 0,128 |
| Q4 | 0 |
| E | 65552,65584 |
| N | 131104,131200,131232 |
| W | 8192,8224 |
| L | 2050 |
| B | 32832 |
| R | 524800,524928 |
| T | 16392,16424 |

There are **19 component labels** in total. The consistency passes delete50, then11, then0 labels from the pre-deletion lists. Complete pairwise-disjoint choices give exactly the following eight assignments. Fixed entries Q0=4100,Q1=1025,Q2=262400,Q4=0,L=2050,B=32832 are suppressed in this table only.

| Assignment | Q3 | E | N | W | R | T |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 65552 | 131104 | 8192 | 524800 | 16392 |
| 1 | 0 | 65552 | 131104 | 8192 | 524928 | 16392 |
| 2 | 0 | 65552 | 131200 | 8192 | 524800 | 16392 |
| 3 | 0 | 65552 | 131200 | 8192 | 524800 | 16424 |
| 4 | 0 | 65552 | 131200 | **8224** | 524800 | 16392 |
| 5 | 0 | 65552 | 131232 | 8192 | 524800 | 16392 |
| 6 | 0 | 65584 | 131200 | 8192 | 524800 | 16392 |
| 7 | 128 | 65552 | 131104 | 8192 | 524800 | 16392 |

These are complete auxiliary **membership assignments**, not eight sampled packings. Centers, orientations and boundary contacts still vary continuously in each entry. Their completeness is supplied by the geometric rule and exact enumeration, not by a numerical optimizer.

## 3. One geometric ownership implication leaves a single assignment

**Lemma.** The actual merged owner W strictly contains \(F_5=(2,2.26)\).

**Proof.** E always owns its marker, F4 and G6. Q2 owns F8, and B owns G5,F6. Hence

\[
[2.26,2.35]\times\{1\}\subset B
\]

strictly, and this entire segment is excluded from E. Translate E by \((-2,-2)\). Its three strict anchors are

\[
(.35,-.35),\quad(0,-.26),\quad(.26,0),
\]

its excluded point is \((1,-.26)\), and its excluded segment is \([.26,.35]\times\{-1\}\). The all-angle short-bar theorem in [Appendix B](#appendix-b) proves

\[
(2.05,1.95)\in E\quad\text{strictly}.\tag{1}
\]

Suppose W omitted F5. W's two markers are strict. It excludes F4 because E owns F4; it excludes F0 because Q1 owns F0; and it excludes F1 and (.914,2) because L owns them. Apply the single isometry

\[
(x,y)\longmapsto(2-x,y-2)
\]

to W and all these points together. The strict markers become \((.35,-.35),(.35,.35)\). Its five excluded points become

\[
(0,-.26),(0,.26),(1,-.26),(1,.26),(1.086,0).
\]

The two-short-chord theorem in Appendix B forces \((-.05,-.05)\) into this transformed W. In physical coordinates that is precisely \((2.05,1.95)\), contradicting (1) and E/W disjointness. Thus W owns F5. ∎

Only assignment4 in Section2 has the corresponding W label8224. Every hypothetical C580 packing therefore has the **single exact auxiliary profile**

| Owner | Exact strict auxiliary points |
|---|---|
| Q0 | F2,G2 |
| Q1 | F0,G0 |
| Q2 | F8,G8 |
| Q3,Q4 | none |
| E | **F4,G6** |
| N | **F7,G7** |
| W | **F5,G3** |
| L | F1,G1 |
| B | F6,G5 |
| R | F9,G9 |
| T | F3,G4 |

In particular, the opposite E/F4 membership used in some other C983 arguments is **not** imported. F4 genuinely belongs to E here.

## 4. Actual wall segments, the merged center, and the southeast sign

### 4.1. Three genuine wall advances

[Appendix C](#appendix-c) proves the following all-angle theorem: an open square of side greater than1, with its actual wall \(x\ge0\), owning (.914,2),(1,2.4) and excluding (1,1.74),(.76,1.87),(1.65,2.35), owns (1,2.8).

All three applications below use the actual container wall and carry **every** point through the indicated isometry:

| Wall owner | Map from the theorem's coordinates to physical coordinates | Two near exclusions and their actual owner | Central exclusion and its actual owner | Result |
|---|---|---|---|---|
| L | (x,y) | (1,1.74),(.76,1.87) in Q1 | (1.65,2.35) in W | (1,2.8) in L |
| B | (y,x) | (1.74,1),(1.87,.76) in Q0 | (2.35,1.65) in E | (2.8,1) in B |
| R | (4−x,y) | (3,1.74),(3.24,1.87) in Q2 | (2.35,2.35) in N | (3,2.8) in R |

The owned marker and the owned (1,2.4) source are, respectively, the original wall marker and G1/F6/G9. Convexity with the near auxiliary points now gives the strict actual segments

\[
\{1\}\times[2.26,2.8]\subset L,\qquad
[2.26,2.8]\times\{1\}\subset B,\qquad
\{3\}\times[2.26,2.8]\subset R.\tag{2}
\]

No segment has endpoints in different owners.

### 4.2. W owns the actual center

Translate by \((-2,-2)\). W strictly owns

\[
(-.35,-.35),(-.35,.35),(-.26,0),(0,.26),
\]

from its two original markers,G3,F5. It excludes \((-1,-.26)\), which is F0 in Q1. L owns

\[
(-1.086,0),(-1,.26),(-1,.8),
\]

from its marker,F1 and (2), and its actual left wall becomes \(x\ge-2\). W and L are distinct congruent squares. The full two-square theorem proved in [Appendix D](#appendix-d) therefore gives

\[
(2,2)\in W\quad\text{strictly}.\tag{3}
\]

This step treats both signs of W and both signs of L. It does not assume a left-wall origin, a favorable W angle, or a missing western marker.

### 4.3. E's canonical angle is strictly negative

The all-angle sign theorem of [Appendix E](#appendix-e), again translated by \((-2,-2)\), has precisely these inputs:

| Local input | Actual C580 source |
|---|---|
| W owns (−.35,−.35),(0,0),(0,.26) | W's southwest marker, (3), and F5 |
| E owns (.35,−.35),(0,−.26),(.26,0) | E's marker,F4,G6 |
| E excludes (1,−.26) | F8 strictly in Q2 |
| E excludes [.26,.8]×{−1} | The full B segment in (2) |
| W,E are congruent and disjoint | Actual distinct owners2304 and512 |

It excludes every nonnegative canonical orientation, including zero and the diagonal endpoint. Thus, after relabeling E's own faces without moving the physical square, its normals are

\[
u_E=(c,-s),\qquad v_E=(s,c),\qquad c\ge s>0,\quad c^2+s^2=1.\tag{4}
\]

This is a local face relabeling, not a reflection of selected points or a symmetry imposed on the other squares.

## 5. The upper-right entrance, with no fictitious southeast corner

The next deductions are in dependency order; none uses the final three-square contradiction.

**First, E owns (2.5,2).** Apply the crosspoint theorem of [Appendix G](#appendix-g) under \((x,y)\mapsto(y,4-x)\). Its three strict anchors become G6,F4 and E's original marker. Its two foreign central markers are W's southwest marker and N's marker. Its two right-hand exclusions become (2.4,1),(2.5,1), both strictly in the one B segment (2). The target becomes (2.5,2).

**Second, T owns (2,3).** Use the all-angle paired-corner boundary transfer in [Appendix F](#appendix-f), with \(b=.914,\ell=1.6\), under \((x,y)\mapsto(x,4-y)\). The wall square is actual T and the corner square is actual Q4. T owns its marker and F3. Q4 owns its northwest marker and paired point (1,3); it excludes (1,2.5), which lies in L's strict segment (2). The theorem's bottom and first-quadrant walls are exactly the physical top and northwest walls. Its target is (2,3).

**Third, N owns (2.5,3).** The top-only extension theorem of Appendix G, translated by (2,2), uses N's marker and F7. Its three exclusions are F5 in W, the just-proved top origin in T, and the just-proved (2.5,2) in E. The target is (2.5,3).

**Fourth, R owns (3,2).** Apply Appendix F with the same \(b=.914,\ell=1.6\), this time under \((x,y)\mapsto(4-y,4-x)\). The wall square is R and the corner square is actual Q3. The two wall anchors become R's marker and G9; the two corner anchors become Q3's marker (3.086,3) and paired point (3,3). The corner's excluded (2.5,3) belongs strictly to N by the preceding paragraph. The genuine northeast and right walls supply all containment premises. The target is (3,2).

In conjunction with (2), this gives the longer strict R segment

\[
\{3\}\times[2,2.8]\subset R.\tag{5}
\]

**Fifth, N has a complete top-only profile.** The upper-square theorem in [Appendix H](#appendix-h) uses N's marker and F7, with these exclusions:

| Excluded point or segment for N | Actual owner |
|---|---|
| F5=(2,2.26) | W |
| (2,3) | T |
| (3,3) | Q3 |
| {3}×[2.26,2.56] | R, by (5) |

It proves \((2.525,2.125)\in N\) strictly. The top-only left-point theorem in the same appendix, using N's marker,G7 and this sharp point with the same exclusions, proves \((2,2.62)\in N\) strictly and all four required face bounds.

For clarity, the final local point and segment data in coordinates \((x,y)=(x_{\rm physical}-2,y_{\rm physical}-2)\) are:

| Actual owner | Strict local data used in the ending |
|---|---|
| E, owner512 | (.35,−.35), (0,−.26), (.26,0), (.5,0) |
| N, owner1024 | (.35,.35), (.4,1), (.26,1), **(.525,.125), (.5,1), (0,.62)** |
| R, owner16384 | (1,0), (1,.56), in fact {1}×[0,.8] |
| W, owner2304 | (0,0), in addition to its earlier strict data |
| B, owner8192 | [.26,.8]×{−1} |

All E/N, E/R and N/R disjointness relations hold because they are distinct actual owners. The same translation is used for all three. No square has been shrunk or rescaled after fixing its ownership.

## 6. The exact local three-square problem

From this point, names E,N,R refer to the translated actual squares. They still have common side \(a>1\). For a square with orthonormal normals u,v, write its bands as

\[
U<u\cdot x<U+a,\qquad V<v\cdot x<V+a.
\]

For a direction n, put \(\alpha=n\cdot u,\beta=n\cdot v\). Its closed-square supports are exactly

\[
\begin{aligned}
\operatorname{upper}_Q(n)&=\alpha U+\beta V
+a\max(\alpha,0)+a\max(\beta,0),\\
\operatorname{lower}_Q(n)&=\alpha U+\beta V
+a\min(\alpha,0)+a\min(\beta,0).
\end{aligned}\tag{6}
\]

Disjoint open squares have a separating face-normal direction from one of the two squares. The support inequality is weak: touching boundaries are permitted. If \(x\in Q\), \(y\in Q'\) are strict and n is oriented from Q toward Q', separation requires \(n\cdot(y-x)>0\). This strict projection comparison removes directions, not tangencies.

### 6.1. E's true faces and the exhaustive bottom alternative

Use (4), lower faces U,V, and write \(A=U+a,H=V+a\). At the excluded center (0,0), three bands are strict from E's anchors, so \(U\ge0\). At the excluded R origin (1,0), three bands are strict and \(A\ge a>1\), so \(H\le s\). At the excluded sharp N point (.525,.125), comparison with E's anchors and \(A>1\) gives \(H\le .525s+.125c\). The true F4 anchor also gives \(U<.26s,V<-.26c\). Thus

\[
U\ge0,\quad A\ge a>1,\quad U<.26s,\quad V<-.26c<0,
\quad H\le s,\quad H\le .525s+.125c.\tag{7}
\]

At the first bottom-bar endpoint \((.26,-1)\), the lower-u and upper-v bands follow from E's strict anchor \((.26,0)\). An upper-u exit would imply \(a\le .26c+s\le1.26/\sqrt2<1\). Hence

\[
V\ge .26s-c.
\]

At the second endpoint \((.8,-1)\), lower-u follows from the marker and upper-v from \((.26,0)\). Its exits are lower-v or upper-u. Therefore either

\[
\boxed{V\ge .8s-c}\tag{F}
\]

or \(A\le .8c+s\). In the latter case any interior intersection with \(y=-1\) would have abscissa strictly between .26 and .8, by these u/v bounds. It would lie in the actual foreign B segment. Such an intersection is impossible. Since E has a strict marker above that line, convexity gives

\[
\boxed{-sA+cV\ge-1.}\tag{S}
\]

This is a **proved full lower support**, not an extra container wall imposed on E. (F) and (S) cover all possibilities, including overlapping endpoint exits and tangency.

### 6.2. N has one quadrant frame for both original signs

Appendices H and I allow N to be represented by

\[
u_N=(d,-r),\quad v_N=(r,d),\quad d,r>0,\quad d^2+r^2=1.
\]

For lower faces P,Q and upper faces \(J=P+a,T_N=Q+a\),

\[
P\ge-r,\quad Q\ge .26d,\quad
J\le d-.56r,\quad T_N\le d+r,\quad Q<.62d.\tag{8}
\]

For an original positive canonical N frame \((c_N,s_N),(-s_N,c_N)\), the exact relabeling is

\[
d=s_N,\ r=c_N,\ P=-(V_N+a),\ J=-V_N,\ Q=U_N,\ T_N=U_N+a.
\]

For the negative canonical sign, retain its frame. Thus (8) does not assume a favorable physical orientation. The opposite widths give

\[
1<a\le d+.44r,\qquad1<a\le .74d+r.
\]

With \(p=\operatorname{angle}(d,r)\) and \(z=\tan(p/2)\), exact factorization yields

\[
\frac{13}{87}<z<\frac{11}{25},\qquad
p_0<p<p_1,\quad
p_0=2\arctan\frac{13}{87},\quad p_1=2\arctan\frac{11}{25}.
\tag{9}
\]

In particular

\[
d_0=\frac{3700}{3869},\quad r_0=\frac{1131}{3869},\quad
H_n=d_0+r_0=\frac{4831}{3869},\quad
d>\frac23,\quad r<\frac34,\quad H_n\le d+r<\frac{10}{7}.
\]

### 6.3. The actual right wall and the complete separator list

Choose R's downward-right quadrant frame

\[
u_R=(b,-t),\quad v_R=(t,b),\quad b,t\ge0,\quad b^2+t^2=1.
\]

If L_R,K_R are its lower faces, the strict origin and its real wall are

\[
L_R<b,\quad K_R<t,\qquad
b(L_R+a)+t(K_R+a)\le2.\tag{10}
\]

The proofs in Appendices J–K show that the only surviving **actual** separating directions are

\[
E\longrightarrow R:\quad v_E\ \text{or}\ v_R;
\qquad
N\longrightarrow R:\quad u_N\ \text{or}\ u_R.\tag{11}
\]

For E, its strict elbow and R's origin force the positive-x direction; its own u face cannot separate because \(A>1\), and R's u direction is excluded by the full E support. Both alternatives (F),(S) imply \(x_{\max}(E)>1\), which is used in that exclusion.

For N, the actual strict pairs

\[
(.5,1)\longrightarrow(1,0),\qquad
(.525,.125)\longrightarrow(1,.56)
\]

force \(n_x>0,n_y<.5n_x\). Its own v direction fails the cone. A prospective R-v separator is excluded by N's complete support, not merely by its owned-point hull. If the N separator is R-u, the second pair additionally gives

\[
95b>87t,\qquad b>2/3,\qquad t<3/4.\tag{12}
\]

The detailed exclusions, including both relative angle orders and R's axial endpoints, are printed in Appendix J, Section3. No possible separating normal has been silently omitted.

## 7. Terminal contradiction and completion of C580

**Local three-square theorem.** No three distinct, pairwise interior-disjoint squares with common side \(a>1\) satisfy E's strict anchors and faces (7), either actual bottom alternative (F) or (S), N's strict points and full profile (8), and R's strict origin/upper point with its actual right-wall inequality (10).

The complete proof is in [Appendix J](#appendix-j) for (S) and [Appendix K](#appendix-k) for (F). Both proofs cover each of the four choices in (11):

| E→R separator | N→R separator | Mechanism |
|---|---|---|
| R-v | R-u | Both strict lower faces of R exceed the room allowed by its actual right wall |
| E-v | R-u | Eliminate R's other face against the wall; its required negative residual is nonnegative |
| R-v | N-u | Eliminate the two R bands using N's full profile and E's lower support |
| E-v | N-u | Positive multipliers reduce the wall contradiction to a piecewise trigonometric residual; each complete arc has positive endpoints |

For example, write

\[
j=ct-sb,\quad k=cb+st,\quad
\delta=db+rt,\quad h=rb-dt,\quad D_0=cd+sr.
\]

In the last row, the exact support inequalities are

\[
H\le-jL_R+kK_R-a\max(j,0),\qquad
J\le\delta L_R-hK_R-a\max(h,0).
\]

The identities

\[
c\delta-rj=D_0b,\qquad -ch+rk=D_0t
\]

eliminate both R band positions against the **real wall** (10). Under (F) they imply the strict negative residual

\[
D_0(b+t-2)+c+r-2cr+.8rs
+c\max(h,0)+r\max(j,0)<0.\tag{13}
\]

Its coefficients on the complete arcs \([0,q],[q,p],[p,\pi/2]\), where \(q=\operatorname{angle}(c,s)<p_0<p\), are positive. Concavity reduces its proof of positivity to four endpoints, not to sampled orientations. At the two interior endpoints the explicit lower bounds are

\[
F(q)\ge\frac{842514839}{107105701105}>0,\qquad
F(p)\ge\frac{106787119}{13547090705}>0.
\]

The derivative bounds establishing these minima and both outer endpoints are included in full in Appendix K. Under (S), the same positive-multiplier argument retains **both** orders of p,q; Appendix J supplies the separate endpoint proofs and the other three separator rows. In particular the (S) proof is not replaced by an unjustified choice of (F).

Now suppose a C580 packing existed. Sections1–2 put its true strict auxiliary labels in the complete eight-assignment entrance. Section3 forces the unique assignment. Sections4–5 construct every point, whole segment, wall and face needed by the local theorem in the **actual** owners512,1024,16384. Section6 retains both bottom alternatives and every possible full-square separating direction. The local theorem contradicts their pairwise interior disjointness. Therefore the hypothesized packing does not exist. **QED.**

The proof never assumes a southwest or southeast paired corner that this family does not have. All three pairwise disjointness relations are retained; boundary contacts remain legal throughout, until strict owned points or \(a>1\) supply the contradictions.

## 8. What was checked, and what is not being claimed

The following computations were performed for this continuation; the optional checker is embedded in [Appendix L](#appendix-l).

**Finite entrance.** The exact integer-coordinate rule was instantiated with the actual C580 groups and the actual transformed singleton seeds. It reconstructed every component list, not merely the list sizes. It produced19 labels and8 complete disjoint assignments; exactly1 survives the proved W/F5 implication. The regenerated lists also match the retained historical C580 table. No historical terminal-success flag is used.

**Foundational small geometry.** The recovered exact rational checker was rerun on its explicit triangle fans and wall-polynomial identities:13 rectangle covers and6 positive polynomial intervals passed. The useful C580 singleton and auxiliary non-avoidance arguments are printed in Appendix A. This finite planar check is separate from the later continuous square-orientation proofs.

**Exact arithmetic and maps.** The embedded checker verifies the rational endpoint margins, polynomial coefficient identities and physical-owner coordinate maps listed in its source. It uses explicit exceptions, so checks remain active under optimized Python. The final receipt below records the actual results rather than treating numerical sampling as proof.

| Check | Ordinary Python | Optimized Python (`-O`) |
|---|---|---|
| Complete finite entrance | PASS: 19 component labels, 8 joint assignments | PASS, identical |
| Proved F5 ownership filter | Exactly 1 assignment | Exactly 1 assignment |
| Symbolic polynomial identities modulo the unit-circle equations | PASS: 14 identities | PASS: 14 identities |
| Named exact rational equalities/positive margins | PASS: 38 checks | PASS: 38 checks |
| Literal physical point maps | PASS: 69 points under 10 isometries | PASS: 69 points under 10 isometries |
| Foundational planar fan and wall-polynomial replay | PASS: 13 rectangle covers, 6 polynomial intervals | PASS: same counts |

The ordinary and optimized embedded-checker reports were byte-identical. The script's scope is the finite rule and the listed exact identities/maps; these counts are not numbers of separately certified real configurations.


The Python checks are not a formal proof kernel for the continuous geometric arguments. No ordinary or native Lean evaluation was performed; no source import closure was compiled or axiom-audited. The source candidate itself and the recovered analytic proofs are credited below. The mathematical conclusion rests on the displayed finite soundness argument and all-angle geometric proofs, not on the existence of a theorem name or a saved compiler receipt.

The formal row321 adapter for original case580 and its registry entry are therefore **formal pending**, not a remaining mathematical sector. Other task bodies and Library archives were left unchanged.

## 9. Source reconciliation and attribution

The starting task was `tasks/05_PENDING_C580.md` in the attached `twelve-square-handoffs-C1091-complete.zip`. Its exact C580 family, selector0, bottom8192, physical maps, and warning about the extra E/N disjointness were preserved. The original task-body SHA-256 is `36fe397a012705ed2ebea1e78b96bb1e2fe513a191ba60636b851d40ff0d2c7f`.

The connected repository was read, not changed: `EvolvingPrograms/SquaresLean`, branch `codex/n12-initial-programs-2026-10-14`, project `projects/n12-refactored`. The following source interfaces were inspected:

| Source path within the project | Content/blob identifier returned by the connector |
|---|---|
| `Compact/Completion/FiniteCases/C580581CentralEntrance.lean` | `a1b1985a293e2b458a426f28d9299cadb0d76050` |
| `Compact/Completion/FiniteCases/C580581PilotInputs.lean` | `4e4455c855695ebb7097a12e6781ab75fd18d74a` |
| `Compact/Completion/FiniteCases/C580581UpperChain.lean` | `4196f3732dd0350d7ea1e78b9759d2b2e4bab228` |
| `Compact/Completion/FiniteCases/C580581TripleEntrance.lean` | `31e990698278d100f4db83680866a3646b5bbcd4` |
| `Compact/Completion/OtherCases/NegativeTripleFaces.lean` | `0d1919dad8e31a1ab1f634f4f2ddda9bab3f664c` |
| `Compact/Completion/OtherCases/C983/NegativeTripleEnd.lean` | `dca4adb742fb8c5860862444cdedcfcd73a3689f` |
| `Compact/Completion/OtherCases/C983/NegativeForeignFaces.lean` | `ce7a5209922cc8b30106e3a8f009f562b30ee6bb` |

The live declaration supplies the two-neighbor/two-face dispatch and requires the real E/N disjointness in addition to its bundled input. The case-specific entrance supplies that extra disjointness and identifies all three frames with their actual owners. Reading these sources does not establish compiler acceptance.

The fetched `Compact/Assembly/NewCases.lean` list did not contain580 or581; its returned blob identifier was `06e33d2bb7f84f4b66a97526b30c4adcca03a2aa`. No stronger claim about every registry or every concurrent branch is made. The handoff's recorded HEAD was `f66b17565533d0db6fc7274932e4ddf4d68e3508` plus working-tree source; the separate source reads are not claimed to be an atomic checkout at that HEAD.

The mathematical appendices specialize recovered ordinary-math chapters from `12-square-mathematical-simplifications-complete.zip` and the earlier organized handoff. In particular, the name C983 in a source filename indicates where a **local** theorem was developed; no C983 exact-family exclusion is applied to C580. Its actual point-level hypotheses are re-established above. Source-byte SHA-256 fingerprints appear at the end of this document. Within each appendix, theorem, equation and subsection numbers are local; preserved legacy numbers make the source arguments traceable. The C580 proof itself is Sections 1–7.



---

<a id="appendix-a"></a>

## Appendix A. Retained foundational geometry and the sound finite rule

### 1. Two elementary geometric principles

**Short-triangle principle.** A square of side `a>1` whose center belongs to a
closed triangle of diameter at most one contains a vertex strictly.

To prove this, use orthonormal coordinates centered on the square. Suppose all
three vertices are excluded. Assign an excluding face to each vertex. Opposite
parallel faces cannot occur: they would give a projected separation at least
`a>1`, while each vertex pair is at distance at most one. The selected faces
therefore consist of one face or two adjacent faces. One face strictly separates
all vertices from the center. In the adjacent-face case, relabel the axes so the
faces are `u>=a/2` and `v>=a/2`. Every vertex on the former has `v>=a/2-1`, by
comparison with a vertex on the latter, and conversely. Hence `u+v>=a-1>0` at
every vertex. This too strictly separates their convex hull from the origin.
Either conclusion contradicts the center's membership in that hull. Boundary
centers and side-length-one triangle edges are included.

**Wall supports.** Relabeling a square's faces permits an edge frame
`u=(c,s), v=(-s,c)` with `c,s>=0`, `c²+s²=1`; here it is not necessary to require
`c>=s`. A square in `y>=0` with center `(X,Y)` satisfies
`Y>=a(c+s)/2`. A square in the first quadrant also satisfies
`X>=a(c+s)/2`. These follow directly by minimizing the coordinates at vertices.

### 2. A corner point and a general wall pair

**Corner lemma.** If the square is in the first quadrant, `a>1`, and `X,Y<=1`,
it strictly contains `(b,1)` for every `.9<=b<=1`.

Put `z=c+s`. The projections of `(b,1)` relative to the center are
`p=c(b-X)+s(1-Y)` and `q=-s(b-X)+c(1-Y)`. The wall supports give

```
p >= -.1c > -a/2,
p <= z-a z²/2 < a/2,
q >= -s+a s z/2 > -a/2,
q <= .1s+c-a c z/2 < a/2.
```

For the second inequality use `z²+1-2z=(z-1)²>=0`; for the third use
`1+sz-2s=(1-s)²+cs>=0`. For the last use
`1+cz-2c-.2s=(1-c)²+s(c-.2)>=0`: this is immediate when `c>=.2`, and when
`c<=.2` it is at least `.64-.2>0`. Strictness comes from `a>1`.

**General wall-pair lemma.** Suppose a square is in `y>=0`, has side `a>1`,
and its center satisfies `0<=X<=w`, `Y<=d`. Assume

```
0<=w<=1,  .75<=b<=d<=1,  w²+(d-b)²<=1,
b c²+d s²+wcs <= c+s   for all c,s>=0 with c²+s²=1.       (W)
```

Then the square contains `(0,b)` or `(w,d)` strictly.

Here is a proof covering every orientation. Write `z=c+s`, with `1<=z<=sqrt(2)<1.5`.
Relative to the center, the two points have projections

```
P: pU=-cX+s(b-Y),       pV=sX+c(b-Y),
Q: qU=c(w-X)+s(d-Y),    qV=-s(w-X)+c(d-Y).
```

The wall bound and `b,d<=1` imply `pU<a/2`, `qV<a/2` using
`1+sz-2s=(1-s)²+cs>=0` and its exchanged version.
Also `pV>=-.25c>-a/2` and `qU>=0>-a/2`.
Thus, if both points were excluded, `P` would exit lower `U` or upper `V`, and
`Q` would exit upper `U` or lower `V`.

The two opposite-face combinations contradict their distance at most one.
For two lower exits, take `s pU+c qV`; the result gives

```
a z/2 <= wcs+(d-b)s² <= cs+s²/4 <= z/2.
```

The last bound has the explicit identity

```
z/2-cs-s²/4
 = (1/5)(3/2-z)(z-1) + (1/2)(c-3s/5)² + (7/100)s² >= 0.
```

This contradicts `a>1`. For two upper exits, `c pV+s qU>=az/2`, and the wall
support implies `bc²+ds²+wcs>=az>z`, contradicting (W). This proves the lemma.
Translation gives arbitrary horizontal positions; reflection exchanges the two
heights, and transposition gives the corresponding vertical-wall statement.

**Normal bounds used here.** Condition (W) holds when `w<=.826` and `b,d<=1`.
Indeed, with `z=c+s<=99/70`,

```
z-1-.826cs = (z-1)[1-.413(z+1)] >= 0.
```

The bracket is positive on that interval. It also holds for `w=1`, `b=d=.914`,
since

```
z-.914-cs = .086-(z-1)²/2
          >= .086-(29/70)²/2 = 9/49000 > 0.
```

Three remaining unequal-height bounds are recorded in Section 6, with exact
positive polynomial identities, not sampled orientations.

### 3. Correct singleton seeds, including the missing-inner-corner variant

Let a square in `[0,4]²` have `1<a<=1.001`, strictly own marker
`A=(1,.914)`, and exclude every other original marker. It then strictly owns

```
(1.12,1), (1.74,1), (1.87,.76).                         (S)
```

The second point is **horizontal**, `(1.74,1)`, not `(1,1.74)`.
If the same square also excludes `(1,1)`, it additionally owns

```
(1.82,1), (1.96,.76).                                  (S+)
```

For a proof, its center is at distance less than `a/sqrt(2)<1` from `A`, so
`X<2`, `Y<2`. If `X<=.914` and `Y<=1`, the corner lemma forces the excluded
marker `B=(.914,1)`. If `X<=.914` and `1<=Y<=2`, the width-one, height-.914
wall pair, transposed, forces `B` or `C=(.914,2)`, again impossible. Thus
`.914<X<2` and `Y<2`.

Set

```
S=(1.65,1.65), B=(.914,1), C=(.914,2),
D=(1.65,2.35), E=(2.35,1.65), F=(2,.914).
```

Every one of these points is excluded by the exact singleton marker signature.
Consider the four fixed triangles

```
(S,B,C), (S,C,D), (S,D,E), (S,E,F).                      (FAN)
```

Their side lengths are at most one. For a proposed seed `T=(p,q)`, append
`(S,F,T)` and `(S,T,B)`. For each of the three targets in (S), all six triangles
have side lengths at most one and cover both rectangles

```
[.914,p] x [1,2],       [p,2] x [d,2],
where d=1 when q=1, and d=.914 when q=.76.               (R)
```

These are explicit small planar fans, not a mesh of square orientations.
The vertices and triangles are explicitly specified by (FAN) and the two target triangles. Their exact edge-length and closed-rectangle checks are recorded in Section 8.
The geometric checking method is explained in Section 7.

If the center is in either rectangle, the short-triangle principle forces
`T`, because every other vertex of the covering triangle is an excluded marker.
Below the left rectangle, the wall pair `B,T` forces `T` because `B` is
excluded. Below the right rectangle, the wall pair `T,F` forces `T` because
`F` is excluded. The applicable wall widths and heights are

| T | Left pair | Right pair |
|---|---|---|
| (1.12,1) | width .206, heights 1,1 | width .88, heights 1,.914 |
| (1.74,1) | width .826, heights 1,1 | width .26, heights 1,.914 |
| (1.87,.76) | width .956, heights 1,.76 | width .13, heights .76,.914 |

All pair lengths are at most one. Equal-height pairs use the small-width
normal bound; the two wider unequal-height pairs use Section 6. This covers
every possible center and proves (S), without borrowing a paired-corner marker.

For (S+), write `I=(1,1)`, now additionally excluded. The four fixed triangles
and `(S,B,I)` cover `[.914,1] x [1,2]`. Their edges are at most one. Below that
rectangle, the corner lemma forces `I`. Hence `X>1`.
For each proposed target in (S+), use the seven triangles consisting of (FAN),
`(S,B,I)`, `(S,F,T)`, `(S,T,I)`. They cover
`[1,p] x [1,2]` and `[p,2] x [d,2]` and have side lengths at most one.
The wall pairs below them are now `I,T` and `T,F`. Their left widths are
`.82` and `.96`; the second requires the third bound in Section 6.
The same argument proves both strict ownership conclusions in (S+).

### 4. Auxiliary non-avoidance from actual geometry

Recall the ten `F` points in the task. A square in the container which avoids
all ten must own a complete pair from

```
{0,1}, {2,3}, {4,5}, {6,7}, {8,11}, {9,10}.             (AF)
```

Suppose it owns no corner pair. Choose an excluded marker at each corner.
Reflect the physical square, all points and the container through its vertical
and/or horizontal midline so that its center has `X<=2`, `Y<=2`. These two
reflections preserve the set F. At the lower-left corner choose its excluded
marker, either `(1,.914)` or `(.914,1)`.

The following wall-pair argument forces `X>1` and `Y>1`.
If both coordinates are at most one, the corner lemma and its transpose force
both corner markers. If `X<=1` and `1<=Y<=1.74`, use the vertical wall pair
from the excluded corner marker to `F0=(1,1.74)`: after transposition its width
is `.826` or `.74`, and its heights are `1,1` or `.914,1`. If instead
`1.74<=Y<=2`, use the vertical pair `(1,1.74),(1,2.26)` of width `.52`.
All endpoints are excluded, so these possibilities are impossible.
Now if `Y<=1` and `1<X<=1.6`, use the corresponding bottom pair from the absent
corner marker to `F2=(1.6,1)`, of width `.6` or `.686`. If `1.6<=X<=2`, use
`F2` and `F6=(2.4,1)`, of width `.8`. These exhaust the wall regions.
All these wall inequalities are instances of Section 2.

If additionally `Y<=1.74`, the rectangle `[1,2] x [1,1.74]` is covered by
three short triangles:

```
(absent corner marker, F2, F0),
(F0,F2,F4), (F2,F6,F4),     with F4=(2,1.74).
```

For either choice of absent corner marker, exact coverage and the edge lengths
are checked in the data file. Every vertex is excluded. The short-triangle
principle therefore gives a contradiction. Consequently `Y>1.74`.
Undoing the two reflections localizes the center to

```
[1,2] x [1.74,2.26]   or   [2,3] x [1.74,2.26].        (L)
```

In the left rectangle each of `(1.65,1.65)` and `(1.65,2.35)` is at distance
less than one from all four vertices; the maximum squared distance is `.7946`.
The rectangle edges have length at most one. Join either proposed marker to
every rectangle edge. These triangles cover the rectangle: extend the ray from
the proposed marker through the center to its last intersection with the
rectangle, then use the boundary edge containing that intersection. This works
whether the proposed marker is inside or outside the rectangle.
The four rectangle vertices are F points and excluded, so both central markers
are forced. The right rectangle similarly forces `(2.35,1.65),(2.35,2.35)`.
This proves (AF).

Transposition, carrying the whole square and all labels with it, takes F to G
and proves the G-pair list

```
{0,1}, {2,3}, {4,5}, {6,7}, {8,9}, {10,11}.             (AG)
```

No assertion about packing thirteen squares has been imported into this proof.
The short-triangle principle is the familiar local non-avoidance argument,
here proved directly.

### 6. Six continuous polynomial certificates for the remaining wall bounds

For nonnegative `c,s` with `c²+s²=1`, put

```
t=c/(1+s),  0<=t<=1,
c=2t/(1+t²),  s=(1-t²)/(1+t²).
```

These formulas include both axis directions. Define

```
P(w,delta;t)=(1-w)+(2delta-1)t+(1+w)t²-t³.
```

Expansion gives the exact identity

```
[c+s-1+delta c²-wcs](1+t²)² = 2t P(w,delta;t).           (P)
```

Thus `P>=0` implies `(1-delta)c²+s²+wcs<=c+s`. Exchanging `c,s` handles
reversed endpoint heights. For each row of this table, the identity is
`P=sum_{j=0}^3 k_j (t-l)^j (h-t)^(3-j)`; every coefficient is positive:

| w | delta | [l,h] | (k0,k1,k2,k3) |
|---|---|---|---|
| 22/25 | 43/500 | [0,1/3] | (81/25,567/250,57/125,107/250) |
| 22/25 | 43/500 | [1/3,1] | (107/2000,147/400,3789/2000,1161/2000) |
| 239/250 | 6/25 | [0,1/6] | (1188/125,1224/125,351/125,38/25) |
| 239/250 | 6/25 | [1/6,1] | (38/3125,333/3125,6012/3125,2592/3125) |
| 24/25 | 6/25 | [0,1/6] | (216/25,36/5,6/25,17/25) |
| 24/25 | 6/25 | [1/6,1] | (17/3125,276/3125,5976/3125,2592/3125) |

The factors are nonnegative on the stated closed intervals, whose unions are
`[0,1]`. All six identities were expanded and checked exactly. These replace
the recovered finer wall-polynomial subdivisions with two pieces per bound.
They concern the entrance's wall lemma, not a sampling of square orientations.

### 7. What the finite checker establishes

For each displayed triangle, the checker uses rational coordinates and confirms
that all three squared edge lengths are at most one. For each rectangle, it
clips the triangles by its four closed half-planes using exact line
intersections. It checks zero pairwise overlap area between the fan triangles
and that the sum of their clipped areas is exactly the rectangle area.
All coordinates needed for these fans are displayed above. The triangles are closed. If they missed a point of the rectangle, their finite
closed union would have a nonempty relatively open complement; a rectangle's
nonempty relatively open subset has positive area. This contradicts the checked
area equality. Thus the finite calculation proves closed, not merely
almost-everywhere, coverage. It checks 13 rectangle covers and the six exact
polynomial expansions.

These checks and the geometric arguments in Sections 1–6 discharge the
singleton and auxiliary-cover inputs of the local catalogue. They do not by
themselves check every later analytic lemma in the recovered sector library.


### Paired-corner seed

Corner pair: if g contains {0,1}, include (1,1), and use the reflected
version for the other three pairs. A short proof is as follows. An edge
excluding (1,1) while the two corner markers are interior has outward
unit normal (c,s) with c,s>0. The two container walls put the center at
X,Y>=a(c+s)/2. The upper support on that edge is at least a(1+cs),
whereas exclusion requires it to be at most c+s. With t=c+s this yields

    a<=2t/(1+t^2)<=1,

contradicting a>1.



4. TWO SMALL LOCAL CONTRADICTIONS

The finite rule uses the following conservative four-point test:
if owned A,B and excluded p,q have properly crossing segments AB,pq,
|p-q|<1 and both (p-A).(q-A)>0 and (p-B).(q-B)>0, that proposed label
is impossible. Using only this strict version retains extra boundary
possibilities and never loses a real square.


Here is a proof of that strict four-point test. Assign excluding faces to p,q.
They cannot be the same face: their segment would remain in its exterior
half-plane and could not cross the strict segment AB. They cannot be opposite
faces because |p-q|<1<a. Thus they are adjacent perpendicular faces.
Place their common corner at the origin, with the square in x<0,y<0,
p_x>=0 and q_y>=0. The crossing implies p_y<0 and q_x<0. The portion of
this quadrant on the origin side of the line pq is the triangle bounded by
that line and the two axes. Its two nonzero vertices lie on the segment pq
and hence in the closed disc with diameter pq. The origin is also in that
disc because p·q<=0. The disc is convex, so the whole triangle is in it.
Since AB properly crosses pq, one of A,B is in this triangle, giving
(Z-p)·(Z-q)<=0. This contradicts both asserted positive scalar products. ∎

Five-point configuration. Put A=(0,0), B=(d,k), C=(w,0),
D=(d,-h), Q=(w,t), where 0<d<w, h>0, 0<t<k and the pairwise
distances among A,B,C are at most 1. A square of side greater than 1
cannot own D,Q and exclude A,B,C.

To see this, choose an excluding face for each excluded point. Opposite
faces are impossible because their points would have distance at least
a>1. Segments AC and BC both cross the interior segment DQ; therefore
C cannot use the same excluding face as either A or B. The only possible
assignment puts A,B on one excluding face and C on an adjacent face.
Let u,v be the respective outward normals. Strict ownership gives

    u.(B-D)>0, u.(A-Q)>0, v.(C-Q)>0, v.(C-D)>0.

The first two imply u_y>0 and u_x<0; the second two imply v_y<0 and
v_x>0. Hence u.v<0, contradicting perpendicularity. Reflection proves
the version with Q=(0,t).

The two exact instances used in the lists have interior points

    (1.65,1.65), (1,2.26)   or   (1.65,1.65), (2,2.26),

and excluded points

    (1,1.74), (1.65,2.35), (2,1.74).                    (E6)

Translate by (1,1.74): w=1,d=.65,h=.09,k=.61,t=.52.
The excluded squared distances are 1,.7946,.4946. Include all eight
symmetry images of these two configurations.

Six-point side configuration. A square owning

    P=(.914,2), Q=(1,1.74), R=(1.74,2)

must contain one of

    A=(1,1.6), B=(1,2.4), C=(1.65,1.65).                (E7)

Suppose it excludes all three. Their squared distances are .64,.425,.985,
so again only two adjacent excluding faces can occur. Segments AB and
BC cross PR at (1,2) and (101/75,2). Thus A,C use one excluding face,
with outward normal u, while B uses the adjacent one, with normal v.
The owned point (1,2) gives u_y<0 and v_y>0. Up to positive scales,
perpendicularity gives two possibilities with c,s>0:

    u=(c,-s), v=(s,c);     or     u=(-c,-s), v=(-s,c).

In the first case comparison of A and B with R gives
37c<20s and 37s<20c, impossible. In the second, compare C with Q
and B with P: 65c<9s and 43s<200c, implying 2795<1800.
If u_x=0 then v_y=0, already impossible. This proves (E7).
Include its eight container-symmetry images as well.


5. THE EXACT FINITE LIST RULE

For each original group g and each of the two auxiliary sets S=F,G,
let MAND(g,S) consist of the points of S in K(g). Enumerate every subset
T of S satisfying

    MAND(g,S) subset T,       l_i<=|T|<=l_i+sigma.       (E8)

Form H=conv(K(g) union T). Declare outside every original marker absent
from g and every auxiliary point of S absent from T. Discard T precisely
when at least one of these finite conditions holds:

    (i) an outside point lies in H;
    (ii) a configuration (E6) or (E7), or its symmetry image, has all its
         required interior points in H and its excluded points outside;
    (iii) a pair of vertices A,B of H and two outside points p,q satisfy
          the conservative four-point test in Section 4.

Call the surviving lists M_i^F and M_i^G. Combine one entry from each
list, take their union as a twenty-point label, and apply the same three
tests with outside points from the full F union G. This gives M_i.

Finally perform the following elementary deletion repeatedly. In owner
order 0,...,11, intersect all labels currently in M_i to obtain its
universally owned set T_i. In order j=0,...,11, j!=i, delete from M_j
any label meeting T_i. Repeat complete passes until no label is deleted.
All lists are finite, so this terminates. If a list is empty, the case
is already impossible.

The displayed M_i in the case tables are exactly the result of this
finite rule. Their presentation order is inherited from the two-cover
enumeration; order is irrelevant to the resulting family of labels.
The rule uses only rational scalar products, squared distances, convex
hulls and membership tests. Hull membership in a two-dimensional polygon
means all counterclockwise edge cross products are nonnegative. For a
segment, require collinearity and both coordinate interval conditions;
for a point, equality. These conventions retain equalities.

Soundness is immediate by induction. The true label obeys the covering
budget and includes all genuine seed points. None of the three geometric
contradictions can hold for it. A universally owned point belongs to the
actual owner and hence cannot belong to another actual owner. Thus every
deletion preserves the actual complete ownership vector.

For each i define the common compulsory hull

    H_i = conv(K(g_i) union intersection_{m in M_i} m).  (E9)

Its vertices are listed explicitly in the case certificates. They are
genuine owned points or convex combinations of genuine owned points.
For a particular label m, the label-specific hull is conv(K(g_i) union m).
Its excluded point set is the union of all absent original markers and
all absent auxiliaries.



---

<a id="appendix-b"></a>

## Appendix B. The two point lemmas that force F5 into the merged owner

### 1. The local strict-point theorem

**Theorem.** Let A be an open square of side a>1. Suppose A strictly owns

    M=(.35,−.35), D=(.26,0), P=(0,−.26),

excludes F=(1,−.26), and excludes the entire segment

    S=[.26,.35]×{−1}.

Then A strictly owns K=(.05,−.05).

Write R=(.26,−1) and T=(.35,−1) for the endpoints of S.
The segment premise is essential to the positive-angle proof: separate
unowned endpoints are not substituted for one actual foreign segment.

### 2. Positive canonical angles

Use u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. Write the open
bands as U<u·X<U+a and V<v·X<V+a. Suppose K is excluded.
Its lower-u, upper-u, and lower-v bands are strict by P,M,M:

    u(K)−u(P)=.05c+.21s>0,
    u(M)−u(K)=.30(c−s)≥0,
    v(K)−v(M)=.30(c+s)>0.

Even when a displayed increment is zero, the anchor is strict. Thus

    V+a≤v(K)=−.05(c+s).                              (1)

At F its lower-u band follows from M, its upper-v band from P, and
its lower-v band follows from the opposite cap (1). The three gaps are

    u(F)−u(M)=.65c+.09s>0,
    v(P)−v(F)=s≥0,
    v(K)−v(F)=.21c+.95s≤sqrt(.9466)<1<a.

Consequently F is upper-u:

    U+a≤c−.26s.                                      (2)

At R its upper-u band follows from D and its upper-v band from M.
Its lower-v band again follows from (1), since

    u(D)−u(R)=s≥0,
    v(M)−v(R)=.65c−.09s>0,
    v(K)−v(R)=.95c+.21s≤sqrt(.9466)<1<a.

Hence R is lower-u:

    U≥.26c−s.                                       (3)

In particular (2),(3) imply a≤.74(c+s), so s>0. At T its
upper-v band is strict by M, with gap .65c. A lower-u exclusion
would contradict (2), since the resulting width would be
.65c+.74s≤sqrt(.9701)<1. An upper-u exclusion would contradict
(3), giving width .09c<1. Thus T is lower-v. Both its u bands
are strict and

    V≥−.35s−c.                                      (4)

On y=−1 put

    x_u=(U+s)/c,        x_v=(−c−V)/s.

The conclusions at R,T give

    .26≤x_u<.35,        .26<x_v≤.35.

Throughout S the upper-u band is strict by T and the upper-v band
is strict by M. If x_u<x_v, every abscissa strictly between them
would also satisfy both lower bands and would be a strict point of
A on S. Since the entire segment is excluded, x_u≥x_v. Multiplication
by cs>0 yields

    sU+cV≥−1.                                       (5)

The left side is the ordinate of A's lowest closed vertex. The two
upper caps (1),(2) instead give

    sU+cV≤.95cs−.21s²−.05−a(c+s).

Together with (5), this would imply

    a(c+s)≤.95+.95cs−.21s².                         (6)

Let w=c+s. The identity w−1=2cs/(w+1) gives w−1≥(4/5)cs,
because w≤sqrt(2)<3/2. Therefore

    w−(.95+.95cs−.21s²)
       ≥.05−.15cs+.21s²
       ≥.05−.15s+.21s²
       =(21/100)(s−5/14)²+13/560>0.

This contradicts (6), since a>1. The target is strict in the entire
nonnegative canonical sector, including its axial and diagonal limits.

### 3. Negative canonical angles

Now use u=(c,−s), v=(s,c), with the same c≥s≥0. The target's
upper-u, lower-v, and upper-v bands are strict by M,P,D:

    u(M)−u(K)=.30(c+s)>0,
    v(K)−v(P)=.05s+.21c>0,
    v(D)−v(K)=.21s+.05c>0.

If K were excluded, it would therefore be lower-u:

    U≥.05(c+s).                                      (7)

At F both lower bands are strict by M and P respectively. If F
were upper-u, (7) would imply

    a≤.95c+.21s≤sqrt(.9466)<1.

Thus F must be upper-v:

    V+a≤s−.26c.                                      (8)

At T its lower-u and upper-v bands follow from M, with gaps .65s≥0
and .65c>0. Its lower-v band follows from (8), because

    v(F)−v(T)=.65s+.74c≤sqrt(.9701)<1<a.

The excluded T is consequently upper-u, U+a≤.35c+s. Together
with (7) this gives

    a≤.30c+.95s≤sqrt(.9925)<1,

which is impossible. This sign uses only F,T as exclusions. Both
signs preserve weak exterior inequalities and prove all four target
bands strictly, completing the theorem. ∎

**Theorem 11 (two-short-chord near-center completion).** Let Q be an open square of side a>1, strictly owning (.35,−.35) and (.35,.35). Suppose it excludes

\[
(0,-.26),\quad(0,.26),\quad(1,-.26),\quad(1,.26),\quad(1.086,0).
\]

Then Q strictly owns both points

\[
K_-:=(-.05,-.05),\qquad K_+:=(-.05,.05). \tag{41}
\]

This theorem uses point exclusions only. It requires no container, foreign segment, neighbor orientation, or upper bound on a.

**Proof.** We include the short-chord part to make this completion independently usable. Both lines y=±k, where k=.26, meet Q's strict owned vertical segment and exclude x=0,1. Their nonempty open chords therefore lie in (0,1) and have lengths at most one. Axis alignment would give length a>1, so it is impossible.

Reflection in y=0 preserves every hypothesis and exchanges the two targets. We may consequently prove both targets for a positive canonical frame u=(c,s), v=(−s,c), c≥s>0. Write the lower band values U,V, the center ordinate Y, and the vertical support radius H=a(c+s)/2. If Y≤−k, the short upper-side chord at y=−k gives Y+H+k≤cs by the exact square-chord formula. The upper support would be at most cs−k≤.24, contrary to ownership at height .35. The reflected argument excludes Y≥k. Thus −k<Y<k.

The plateau chord has length a/c>1. Both short chords are therefore strictly outside the plateau and adjacent to the bottom and top vertices respectively. Their four endpoints, with supporting-line tangency permitted, give exactly

\[
U\ge-ks,\quad V\ge-kc-s,\quad
V+a\le kc,\quad U+a\le c+ks. \tag{42}
\]

For completeness, their left/right abscissas are

\[
\left(\frac{U+ks}{c},\frac{-kc-V}{s}\right)
\quad\text{at }y=-k,\qquad
\left(\frac{kc-V-a}{s},\frac{U+a-ks}{c}\right)
\quad\text{at }y=k.
\]

In particular 1<a≤s+(13/25)c. With t=s/(1+c), this is 19t²−25t+6<0. The roots are 6/19 and 1, so

\[
t>6/19,\qquad
\theta>\theta_0,\qquad
(\cos\theta_0,\sin\theta_0)=(325/397,228/397). \tag{43}
\]

Put B=(1.086,0). Its lower u-band is strict by the owned point (.35,−.35), and its upper v-band is strict by (.35,.35). If B left through the lower v-face, then V≥−1.086s; (42) would imply

\[
a\le .26c+1.086s\le\frac{673}{500\sqrt2}<1.
\]

The middle bound is the value at θ=π/4, since the expression increases on the canonical interval; the last inequality is 673²<2·500². Hence B leaves through the upper u-face:

\[
U+a\le1.086c. \tag{44}
\]

For either Kσ=(−.05,σ.05), σ∈{−1,1}, the upper u-band and lower v-band are strict by the owned point (.35,−.35). Indeed its u-projection is .35(c−s)≥0≥u(Kσ), and

\[
v(K_\sigma)-v(.35,-.35)=.4s+(.35+\sigma .05)c>0.
\]

For the upper v-band, use V≥−.26c−s from (42). Then

\[
v(K_\sigma)-V
\le(.26+\sigma .05)c+1.05s
\le .31c+1.05s
\le\frac{1.36}{\sqrt2}<1<a.
\]

Finally,

\[
u(B)-u(K_\sigma)
=1.136c-\sigma .05s
\le1.136c+.05s
\le\frac{1.136(325)+.05(228)}{397}
=\frac{1903}{1985}<1<a.
\]

The penultimate inequality follows from (43), since 1.136 cos θ+.05 sin θ decreases for θ≥θ₀. Together with (44), it proves the lower u-band. All four bands are strict. Reflection supplies the negative sign, with the pair of targets exchanged. All axis and diagonal endpoints and every exterior tangency have been covered. ∎



---

<a id="appendix-c"></a>

## Appendix C. A wall square advances to 2.8 from its actual singleton neighbor

### 4. Using the actual central marker advances both walls to 2.8

**Theorem 4.** Let W be an open square of side a>1 contained in x≥0. Suppose W strictly owns (.914,2),(1,2.4), and excludes the three points

    F=(1,1.74), H=(.76,1.87), M=(1.65,2.35).

Then W strictly owns P=(1,2.8).

The point M is the genuine C981 marker owned by Q7; H is the singleton corner seed owned by Q1. This theorem does not need the inward auxiliary exclusion (1.74,2).

### A scalar wall inequality

For l>0,h≥0,l²+h²=1,

    l+h−1+.24h²≥.93lh.                                  (13)

Here is an exact proof on the entire quarter circle. Put t=h/(1+l), so 0≤t<1, l=(1−t²)/(1+t²), and h=2t/(1+t²). Multiplication by the positive denominator (1+t²)² gives

    (1+t²)²[l+h−1+.24h²−.93lh]
       =2t[.07−.52t+1.93t²−t³].

For 0≤t≤1/2, the bracket is at least

    .07−.52t+1.43t²
       =(143/100)(t−2/11)²+1/44>0.

For 1/2≤t≤1, it is at least

    .07−.52t+.93t²
       =.93(t−1/2)²+.41(t−1/2)+17/400>0.

Thus (13) holds, including h=0.

### Proof of the wall theorem

Choose a frame u=(l,h), v=(-h,l), l>0,h>=0, l²+h²=1, with lower face values U,V. No ordering of l,h is imposed, so this represents every square orientation. The wall gives lU≥h(V+a), and exclusion of F gives

    U≥l+1.74h    or    V≥−h+1.74l.                       (14)

The target has both lower bands strictly from (1,2.4).

If the second lower bound

    V≥−.76h+1.87l                                       (15)

is ever obtained, the target upper U band is automatic. Indeed, its failure U+a≤l+2.8h would imply, using the actual wall,

    a(l+h)≤1−.24h²+.93lh≤l+h

by (13), contradicting a>1. We will use this implication below. Also, a lower U bound U≥.76l+1.87h automatically gives the target upper U band, since

    U(P)−(.76l+1.87h)=.24l+.93h
       ≤sqrt(.24²+.93²)=sqrt(.9225)<1<a.               (16)

**First branch of (14).** Suppose U≥l+1.74h. At M, the lower U band follows from (.914,2), and the upper V band follows from (1,2.4). Its upper U band follows because

    U(M)−(l+1.74h)=.65l+.61h
       ≤sqrt(.65²+.61²)=sqrt(.7946)<1<a.

The exclusion of M therefore forces

    V≥−1.65h+2.35l.                                     (17)

This gives the target upper V band, since

    V(P)−(−1.65h+2.35l)=.65h+.45l
       ≤sqrt(.625)<1<a.

At H, the upper U band follows from the owned marker. Its upper V band follows from (17), since

    V(H)−(−1.65h+2.35l)=.89h−.48l≤.89<1<a.

Thus H must escape at a lower face. If it gives U≥.76l+1.87h, use (16); if it gives (15), use the scalar wall implication. This closes the first branch for every angle.

**Second branch of (14).** Suppose V≥−h+1.74l. At H the upper U band follows from the owned marker, and the upper V band follows because

    V(H)−(−h+1.74l)=.24h+.13l<1<a.

Thus H again escapes at a lower face.

If it gives (15), its upper U consequence has already been proved, while the upper V band follows from

    V(P)−(−.76h+1.87l)=−.24h+.93l≤.24h+.93l<1<a.

Suppose instead that U≥.76l+1.87h. The target upper U band follows from (16). If 1.06l≤1, its upper V band follows directly from the second branch of (14). In the only remaining subcase l>50/53, we have

    h²<1−(50/53)²=309/2809<1/9,
    0≤h<1/3.

On this interval the function .89sqrt(1−h²)+.48h is increasing: its derivative is .48−.89h/l>0, since h≤1/3 and l≥2sqrt(2)/3. Its value at h=1/3 is strictly less than one, because

    .89(2sqrt(2)/3)+.16<1
    ⇔ sqrt(2)<126/89,

and 2·89²=15842<15876=126². Consequently

    U(M)−(.76l+1.87h)=.89l+.48h<1<a.

The other strict bands of M are exactly those used above: lower U from (.914,2), and upper V from (1,2.4). Its exclusion therefore forces (17), which gives the target upper V band as before. This closes the last subcase and proves the theorem. ∎



---

<a id="appendix-d"></a>

## Appendix D. The genuine merged western square contains the center

**Theorem 1.** Let W,L be open squares of the same side 1<a≤1001/1000 with disjoint interiors. In the following local coordinates suppose that W strictly owns

    P=(−.35,−.35), Q=(−.35,.35),
    D=(−.26,0), F=(0,.26),                         (1)

and excludes F0=(−1,−.26). Suppose that the actual square L strictly owns

    M=(−1−e,0), B=(−1,.26), R=(−1,.8),
    e=43/500=.086,                                (2)

and lies in the genuine half-plane x≥−2. Then O=(0,0) lies strictly in W.


We prove this local theorem next. All supports are those of the complete actual squares.

### 2. Missing center forces a short negative angle

First give W a positive canonical frame

    u=(d,r), v=(−r,d), d≥r≥0, d²+r²=1.

At O its lower u and v bands follow from P, whose projections are −.35(d+r) and .35(r−d). Its upper u band follows from F, whose u projection is .26r≥0. Its upper v band follows from Q, whose v projection is .35(d+r)>0. Strictness of the anchors gives all four strict bands, including r=0 and r=d. Thus O is already in W in this orientation.

For a contradiction we may consequently assume a negative canonical frame

    u_W=(d,−r), v_W=(r,d), d≥r≥0, d²+r²=1,
    lower faces U,V; upper faces A=U+a,H=V+a.      (5)

At O the lower u band follows from D, the lower v band from P, and the upper v band from F. A missing O must therefore satisfy

    A≤0, U≤−a.                                   (6)

The excluded F0=(−1,−.26) satisfies the upper u band by comparison with D, the projection gap being .74d−.26r>0, and the upper v band by comparison with F, the gap being r+.52d>0. If it exited through lower u, then U≥−d+.26r and (6) would give a≤d−.26r≤1. Hence its exit is necessarily

    V≥−r−.26d.                                   (7)

The strict P gives V<−.35(d+r), so

    r/d>9/65, in particular r>0.                 (8)

The foreign point B satisfies both upper bands of W: compare its u projection with D and its v projection with F, with respective gaps .74d+.26r and r. Its two possible exits are lower u and lower v.

Suppose B exited through lower v. Then V≥−r+.26d and the strict P would give

    r/d>61/65.                                   (9)

In this case d>.7, r>.65 and d+r>1.35. Put z=r/(1+d). Equation (9) also gives z>.26: otherwise r/d=2z/(1−z²)≤1300/2331<61/65.

Consider the closed vertex of W at the two lower faces,

    Z=(dU+rV, −rU+dV).

Using (6) and the strict P,

    Z_x<−d−.35r(d+r)
       <−.7−.35(.65)(1.35)<−1.                  (10)

The lower bound V≥−r+.26d gives

    Z_y≥ar−dr+.26d²
       >.26+r²(z−.26)>.26.                      (11)

The strict F gives U>−a−.26r. Using this and the strict P for the opposite bound,

    Z_y<ar+.26r²−.35d(d+r)
       <1.001(5/7)+.13−.175=.67<.8.             (12)

Here r≤1/sqrt(2)<5/7, r²≤1/2 and d(d+r)≥1/2. The strict point Q=(−.35,.35) lies to the right of x=−1. The segment from Q to the closed vertex Z crosses x=−1 at a height strictly between .26 and .8. Except for Z, this segment lies strictly in the open square W. Its crossing therefore belongs both to W and to the actual bar (3), a contradiction.

B must exit through lower u. Combining U≥−d−.26r with (6) gives

    1<a≤d+.26r.

The exact half-angle formula now yields

    0<z=r/(1+d)<13/50.                            (13)

Indeed d+.26r−1=2z(.26−z)/(1+z²). We will repeatedly use the consequences

    d>2331/2669>.873,
    r<1300/2669<.49,
    r/d<1300/2331<.56,
    d−(3/2)r>0.                                  (14)

Let p be the angle with d=cos p,r=sin p. Thus 0<p<2 arctan(13/50)<π/4.

### 3. Every possible separating face

Orient a prospective separating direction n from L toward W. Strict B in L and F in W have difference (1,0), so

    n_x>0.

Strict R in L and P in W have difference (.65,−1.15), so also

    n_y<(13/23)n_x.                               (15)

Of W's face normals only u_W=(d,−r) remains: its other normal with nonnegative first coordinate is (r,d), whose slope is at least 1, and the reverse directions have nonpositive first coordinate.

For L choose either a negative canonical frame (b,−t),(t,b) or a positive canonical frame (b,t),(−t,b), where

    b=cos q, t=sin q, 0≤q≤π/4.

In the negative frame, (t,b) fails (15), leaving only (b,−t). In the positive frame retain (b,t) and (t,−b). These are a covering list; retaining a direction even if its slope happens to fail (15) only enlarges the list to be excluded. Their zero-angle cases are covered as well.

Thus there are exactly the following families to disprove:

    L negative: u_W or (b,−t);
    L positive: u_W, (b,t), or (t,−b).             (16)

For L alone translate once more to a chart centered at (−1,0). Its strict marker is now (−e,0), its strict points B,R are (0,.26),(0,.8), and its real wall is x≥−1. A projection computed in this L chart is shifted by −n_x when expressed back in the W chart.

### 4. Negative L: its full support on W's axis

Give L the negative frame (b,−t),(t,b), with lower faces ℓ,m. Its strict marker and genuine leftmost vertex give

    ℓ<−eb, m<−et,
    bℓ+tm≥−1.                                   (17)

In particular its own upper u face J=ℓ+a satisfies

    J>a−1/b+et²/b.

Set

    k=db+rt=cos(q−p)>0,
    j=dt−rb=sin(q−p).

The full upper support of L in direction u_W, in its local chart, is

    k(ℓ+a)+jm+a max(j,0).

Eliminate ℓ using (17). The coefficient of m is j−kt/b=−r/b. Since m<−et and a>1, after the shift −d its upper support is strictly greater than

    B_−(q)=k−2d−(1−e)rt/b,       0≤q≤p,
    B_+(q)=k+j−2d−(1−e)rt/b,     p≤q≤π/4.        (18)

Each function is strictly concave on its indicated interval:

    B_−''=−k−2(1−e)rt/b³<0,
    B_+''=−(k+j)−2(1−e)rt/b³<0.

Here k+j>0 on the second interval. At the endpoints,

    B_−(0)=−d>−1,

    B_−(p)=B_+(p)
      =−1+[er²−(1−d)²]/d
      =−1+r²(e−z²)/d>−1,                        (19)

because e−z²>.086−.26²=23/1250>0. At the remaining endpoint,

    B_+(π/4)=(sqrt(2)−2)d−(1−e)r>−1.             (20)

For completeness, (2−sqrt(2))d+(1−e)r increases with p on (13): its derivative is −(2−sqrt(2))r+(1−e)d>−.586(.49)+.914(.873)>0. Since sqrt(2)>707/500, its value at the upper endpoint in (14) is strictly less than

    [293·2331+457·1300]/[500·2669]
      =1277083/1334500<1,

with exact margin 57417/1334500. This proves (20). Concavity and all three endpoint bounds show that the upper support of L on u_W is greater than −1 everywhere. The lower support of W on that axis is U≤−a<−1. This direction cannot separate.

### 5. Negative L: its own axis when q≤p

The upper support of L on its own direction (b,−t), now in the W chart, is strictly greater than

    Λ(q)=1−b−1/b+et²/b.                           (21)

Put h=rb−dt. For q≤p we have h≥0, so the full lower support of W on this axis is

    kU+hV<−k−.35h(d+r).                           (22)

Define the constants, with p fixed,

    A_−=d+.35r(d+r),
    C_−=r−.35d(d+r).

The exact difference identity is

    b[Λ+k+.35h(d+r)]
      =G_−(q)
      =b−2+A_−+(1+e−A_−)t²+C_−bt.               (23)

We have

    A_−−1=r[.35(d+r)−z]>0,
    C_−+.35=r[1−.35d+.35r]>0.

On 0≤q≤p, b≥d>.873 and cos(2q)≥0. Consequently

    G_−''=−b+2(1+e−A_−)(b²−t²)−4C_−bt
           <−.873+.172+.7=−.001<0.              (24)

If 1+e−A_− is negative its contribution is nonpositive; otherwise it is less than e. We also used bt≤1/2 and C_−>−.35. The two endpoint values are

    G_−(0)=A_−−1>0,
    G_−(p)=er²−(1−d)²=r²(e−z²)>0.               (25)

Concavity makes the whole gap positive. Equations (21)–(25) contradict the support ordering required for separation.

### 6. Negative L: its own axis when q≥p

Now h≤0. The strict F gives H>.26d, so the full lower support of W is

    kU+hH<−k+.26dh.                               (26)

Put

    A_+=d−.26dr,
    C_+=r+.26d²>0.

The corresponding wall gap is

    b[Λ+k−.26dh]
      =G_+(q)
      =b−2+A_++(1+e−A_+)t²+C_+bt.               (27)

Here A_+<1 and, using dr≤1/2 and (14),

    0<1+e−A_+<1.086−.873+.13=.343.

Thus on the whole canonical interval

    G_+''=−b+2(1+e−A_+)(b²−t²)−4C_+bt
           <−.7+.686=−.014<0.                   (28)

For the far end of the interval we will use the actual strict marker as a second support bound. Set

    b_*=1−e=.914,
    t_*=sqrt(1−b_*²), q_*=arccos(b_*).

The exact inequalities .4<t_*<.406 follow by squaring. At q=q_* the wall bound (21) equals the marker projection:

    Λ(q_*)=−(1+e)b_*.

The marker itself gives, for every q,

    upper_L(b,−t)>−(1+e)b.

Its difference from the bound (26) is

    D(q)=−(1+e)b+k−.26dh
        =b(A_+−1−e)+tC_+.                        (29)

The first coefficient is negative and the second positive, so D strictly increases with q.

If p≥q_*, then at q=p,

    D(p)=1−(1+e)d≥1−(1+e)(1−e)=e²>0.

The increasing marker gap excludes the entire interval q≥p in this case.

It remains to treat p≤q_*. On [p,q_*], use (27),(28). Its first endpoint is again

    G_+(p)=r²(e−z²)>0.

At its second endpoint the gap equals b_*f(p), where

    f(p)=b_*d+t_*r+.26t_*d²−.26b_*dr−1+e².       (30)

This is strictly positive on 0≤p≤q_*. Indeed its exact second derivative is

    f''=−b_*d−t_*r−.52t_*(d²−r²)+1.04b_*dr
        ≤b_*²(−1+1.04t_*)<0.                     (31)

We used d≥b_*, d²−r²≥0 and dr≤b_*t_* on this interval. Its endpoint values satisfy

    f(0)=−e+e²+.26t_*
          >−.086+.007396+.104
          =6349/250000>0,
    f(q_*)=e²=1849/250000>0.                     (32)

Concavity proves f(p)>0. Therefore both endpoints of G_+ on [p,q_*] are positive, so that entire wall gap is positive as well. For q≥q_*, the increasing marker gap D starts at this same positive value and remains positive. This excludes every remaining negative-L direction, with q=p and q=q_* included.

### 7. Positive L: its full support on W's axis

Give L the positive frame (b,t),(−t,b), again with lower faces ℓ,m. Its marker and its genuine leftmost vertex give

    m<et,
    bℓ−t(m+a)≥−1.                               (33)

Set

    k=db−rt>0, h=dt+rb>0.

The first positivity follows from b≥t and d>r. The full upper support of L on u_W, in the L chart, is k(ℓ+a)−hm. Eliminating ℓ with (33) gives coefficient kt/b−h=−r/b on m. After using m<et, a>1 and the shift −d, this upper support is strictly greater than

    B(q)=d(b+t−2)+r g(q),
    g(q)=t[(1−e−t)/b−1].                         (34)

The following scalar bound holds over the whole canonical interval:

    g(q)≥−(3/2)(b+t−1).                           (35)

To see it without sampling, multiply its left-minus-right expression by b. The exact expansion is

    b[g+(3/2)(b+t−1)]
      =(3/2)(1−b)+(1−e)t+(1/2)bt−(5/2)t²
      ≥t[(1−e)+(1/2)b−(7/4)t]
      ≥t[(1−e)−(5/4)t]≥0.

The first inequality uses 1−b=t²/(1+b)≥t²/2, the second uses b≥t, and the last uses t<5/7 and 1−e=.914>25/28. With (14), (34),(35) imply

    B(q)≥−d+[d−(3/2)r](b+t−1)≥−d>−1.

Again W's lower support is U≤−a<−1, so its own normal cannot separate.

### 8. Positive L: both of its own remaining normals

On L's normal (b,t), its strict point R=(−1,.8) has projection −b+.8t. The full lower support of W is, with the k,h of Section 7,

    kU+hV<−k−.35h(d+r).

The strict support gap is therefore bounded below by

    −b+.8t+k+.35h(d+r)
      =b[d−1+.35r(d+r)]
         +t[.8−r+.35d(d+r)]>0.                   (36)

The first coefficient is r[.35(d+r)−z]>0 and the second is greater than .8−r>0. This axis cannot separate.

For the remaining normal (t,−b), its W-frame coefficients are h>0 and −k<0. Thus W's full lower support is

    hU−kH<−h−.26dk.

The strict marker of L has projection −(1+e)t in the W chart. The gap is

    h+.26dk−(1+e)t
      =b[r+.26d²]+t[d−.26dr−1−e].                (37)

The second coefficient is negative. Since b≥t, (37) is at least

    b[d+r−1+.26d²−.26dr−e].

For d²+r²=1 and d,r≥0,

    d+r−1=2dr/(d+r+1)≥.8dr,

because sqrt(2)<3/2. Consequently the expression in brackets is at least

    .26d²+.54dr−e≥.13−.086=11/250>0.             (38)

This final direction also fails. Together Sections 4–8 exhaust the full face-normal list (16), contradicting disjointness of the two actual squares under the missing-center assumption. O must be strictly in W, completing Theorem 1. ∎



---

<a id="appendix-e"></a>

## Appendix E. The actual southeast square has strictly negative canonical angle

**Theorem 1.** Let W,E be disjoint open squares of common side a>1. Suppose W strictly owns

    P=(−.35,−.35), O=(0,0), F=(0,.26),             (1)

and E strictly owns

    M=(.35,−.35), I=(0,−.26), D=(.26,0).           (2)

Suppose E excludes A0=(1,−.26) and the whole segment

    B0 B1=[.26,.8]×{−1}.                          (3)

Then E has a strictly negative canonical angle.


### 2. The positive-frame face table

Suppose, for a contradiction, that E has a nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Write its lower faces U,V and upper faces A=U+a,H=V+a. At its excluded O the lower u and v bands follow from I and M, respectively, while the upper u band follows from D. Therefore

    H≤0.                                         (4)

The strict D gives H>−.26s. In particular s=0 is impossible; hence s>0 and c<1.

At the excluded A0=(1,−.26), the lower u band follows from I, the upper v band from D, and the lower v band from V=H−a<−1. For the last comparison,

    v(A0)=−s−.26c>−1,

because s+.26c≤1.26/sqrt(2)<1 over the canonical interval. Thus A0 can exit only through upper u:

    A≤c−.26s,
    U≤c−.26s−a<c−.26s−1.                         (5)

At B0 both upper bands follow from D, so it exits through lower u or lower v. We retain both weak alternatives, even when both hold:

    U≥.26c−s  or  V≥−.26s−c.                     (6)

If the second alternative holds, then

    H≥a−c−.26s>1−c−.26s.                         (7)

If it does not hold, the first does. At B1 the lower u band follows from I, with gap .8c−.74s≥.06c>0, and the upper v band from D. Were B1 upper u, (6) would give

    a≤(.8c−s)−(.26c−s)=.54c<1,

which is impossible. Consequently

    U≥.26c−s, V≥−.8s−c.                          (8)

Any interior intersection of E with y=−1 would, by (8), have .26<x<.8 and would belong to the whole excluded segment (3). There is no such intersection. The strict marker M is above that line, so convexity forces the full closed lower support of E to satisfy

    y_min=sU+cV≥−1.                              (9)

Equation (9) has been proved from the one actual foreign bar; it is not an assumed wall on E. We shall call (7) the first case and (9) the second. They cover every possibility in (6).

### 3. The exhaustive W-to-E normal list

Orient a prospective separating direction n from W toward E. The strict pair P,M gives n_x>0. The strict pair F,I gives n_y<0. E's only face-normal direction in this cone is

    −v_E=(s,−c).                                  (10)

If W has negative canonical frame (d,−r),(r,d), with d≥r≥0, its only additional possible direction is (d,−r). If W has positive canonical frame (d,r),(−r,d), its only additional possible direction is (r,−d). Retaining their axial endpoints only enlarges the list. Every reverse or other face direction fails one of the two strict component inequalities.

On direction (10), E's lower support is −H and the strict P in W has projection

    (−v_E)·P=.35(c−s).                            (11)

We will use that projection, and the strict O in W where indicated, to exclude each of these full actual-square directions.

### 4. First bottom-bar case: the lower v bound

Assume (7), along with (4),(5). Equation (7) and H≤0 imply

    c+.26s>1,
    0<z=s/(1+c)<13/50.

The half-angle identity is c+.26s−1=2z(.26−z)/(1+z²). Consequently

    c>2331/2669>.873,
    s<1300/2669<.49,
    .35(c−s)>2681/20000>.134.                    (12)

Also, throughout the entire unit circle,

    c+.26s−1≤sqrt(1+.26²)−1<.034,                 (13)

where 1.034²>1+.26² is an exact squared comparison. From (7), −H<c+.26s−1. Equations (11)–(13) immediately exclude E's normal (10).

### 4.1. W has negative canonical frame

Put

    k=cd−sr≥0, h=sd+cr>0.

The full lower support of E in direction (d,−r) is kU−hH. By (5),(7), it is strictly less than

    k(c−.26s−1)−h(1−c−.26s)
      =d D1+r R1,                                (14)

where

    D1=(c−1)(c+s)+.26s(s−c)<0,
    R1=(c−1)(c−s)+.26s(c+s).

The exact other endpoint is

    D1+R1=2c(c−1)+.52s²
          =(1−c)(.52−1.48c)<0.                    (15)

The last sign follows from c≥1/sqrt(2)>.7. Since 0≤r/d≤1, the affine expression D1+(r/d)R1 is negative at both endpoints and therefore negative throughout. Thus (14) is negative. The strict O gives a positive upper support of W on this direction, contradicting separation.

### 4.2. W has positive canonical frame

Set

    delta=cr−sd, k=cd+sr>0.

First suppose delta≥0. E's full lower support in direction (r,−d) is delta U−kH. Subtract the strict P projection .35(d−r). Equations (5),(7) bound this difference strictly above by

    delta(c−.26s−1)−k(1−c−.26s)−.35(d−r)
      =d D2+r R2,                                (16)

where

    D2=(c−1)(c−s)+.26s(c+s)−.35<0,
    R2=(c−1)(c+s)+.26s(s−c)+.35.

Indeed s(c+s)≤1 gives D2≤.26−.35=−.09. The sum D2+R2 is exactly the negative expression in (15). The same affine endpoint argument on 0≤r/d≤1 shows that (16) is negative, contradicting separation.

If delta≤0, the W angle is at most the E angle. Thus d−r≥c−s. Now E's full lower support is delta A−kH. Its strict D gives A>.26c>0, while k≤1. Hence, using (7),(13),

    lower_E(r,−d)
       <k(c+.26s−1)≤c+.26s−1<.034.

But the strict P in W has projection .35(d−r)≥.35(c−s)>.134 by (12). This also contradicts separation. The common endpoint delta=0 is included without division. Every direction has failed in the first bottom-bar case.

### 5. Second bottom-bar case: the proved lower support

Assume (9). Recalling V=H−a, it gives

    H≥a−1/c−(s/c)U.                              (17)

With (5) and a>1, this also yields

    H>[c+s−1−cs+.26s²]/c.

Let

    F0=c+s−1−cs+.26s².

The gap needed for E's normal (10) is strictly positive:

    F0+.35c(c−s)
      =c+s−1−1.35cs+.26s²+.35c²
      ≥.35c²−.55cs+.26s²
      ≥.06c²>0.                                  (18)

The first inequality uses c+s−1≥.8cs, which follows from c+s<3/2. For the second, put t=s/c∈[0,1]; the quadratic .35−.55t+.26t² decreases on [0,1] and equals .06 at1. Therefore −H<.35(c−s), opposite to the support ordering required by the strict W point P. E's own normal is excluded.

We will use the common negative quantity

    X=(1−c)(c+s−1)−.26s<0.                       (19)

Indeed 1−c=sz, with z=s/(1+c)≤sqrt(2)−1, and c+s−1≤sqrt(2)−1. Hence

    X=s[z(c+s−1)−.26]
      ≤s[(sqrt(2)−1)²−.26]<0.

The last strict inequality is exact because (sqrt(2)−1)²=3−2sqrt(2)<.26, equivalently sqrt(2)>137/100.

### 5.1. W has negative canonical frame

Use k,h from Section 4.1. By (17),

    lower_E(d,−r)=kU−hH
       ≤(d/c)U−ah+h/c,

where the exact elimination identity is ck+sh=d. Substituting (5), and then a>1, makes the last expression strictly less than

    (d/c)(c−.26s−1)−h+h/c.

After multiplication by c, its numerator is

    (1−c)(h−d)−.26ds
      =d[(1−c)(s−1)−.26s]+rc(1−c)
      ≤d[(1−c)(c+s−1)−.26s]
      =dX<0.                                     (20)

We used r≤d. Thus the full lower support of E is negative, whereas the strict O supplies positive upper support in W. This direction cannot separate.

### 5.2. W has positive canonical frame, with either relative angle order

Use delta,k from Section 4.2. Its full lower E support is

    delta U−kH+a min(delta,0)
       ≤delta U−kH.

By (17) and the exact identity c delta+sk=r, this is at most

    (r/c)U−ak+k/c.

Apply (5) and a>1. After subtracting the strict P projection .35(d−r) and multiplying by c, the resulting strict upper bound is

    (1−c)(k−r)−.26rs−.35c(d−r)
      =d D3+r R3,                                (21)

where

    D3=c(.65−c)<0,
    R3=(1−c)(s−1)−.26s+.35c.

The exact endpoint sum is D3+R3=X<0. Again the expression D3+(r/d)R3 is affine on [0,1] and negative at both endpoints. Equation (21) is negative for every W angle and every relative order of the two angles. The strict P projection already exceeds the full lower E support, excluding this final direction.

Both cases from (6) have now exhausted every actual face-normal direction in the strict separating cone. W and a nonnegative E cannot have disjoint interiors. E's canonical angle is therefore strictly negative, proving the local theorem. ∎



---

<a id="appendix-f"></a>

## Appendix F. All-angle paired-corner to wall-origin transfer

### 6. A corner profile forced by one excluded upper point

The following theorem supplies a full support profile from one excluded point above an actual corner square.

### Theorem 6

Let K be an open square of side a>1 whose closure lies in the first
quadrant. Suppose that K strictly owns A=(1,1) and excludes H=(1,3/2).
Then, for every c,s>=0 with c^2+s^2=1,

    upper_K(c,-s)>=a F(c,s),
    F(c,s)=c-s(c+s)/(1+c)=2c-1-cs/(1+c).             (15)

The orientation of K is unrestricted. Neither an upper bound for a nor
any marker other than A is a premise of this theorem.

### 6.1. A continuous scalar envelope

For r,t>=0 with r^2+t^2=1, put

    tau=t/(1+r),
    G=ct+sr+max(cr-st,0)+s tau-3s/2.

Then

    G>=F(c,s).                                      (16)

To prove this over the whole two-angle quadrant, write

    r=cos theta, t=sin theta,
    c=cos phi,   s=sin phi,
    0<=theta,phi<=pi/2.

First consider theta+phi<=pi/2. Here

    G=(c+s)r+(c-s)t+s tau-3s/2,

and differentiation with respect to theta gives

    G''=-c(r+t)-s(r-t)+st/(1+r)^2.

If r,s>0, the defining condition cr>=st yields

    G''<=s[-1/r+t/(1+r)^2]<0.

If s=0, directly G''=-c(r+t)<0. Values at r=0 follow by
continuity. Thus G is concave on this interval, and its minimum occurs
at one of its endpoints.

On theta+phi>=pi/2, instead

    G=ct+sr+s tau-3s/2,
    G'=r[c-s J(r)],
    J(r)=[sqrt(1-r^2)-1/(1+r)]/r.

For 0<r<1,

    J'(r)={ (1+2r)/(1+r)^2-1/sqrt(1-r^2) }/r^2<0.

Indeed (1+2r)/(1+r)^2<1 and 1/sqrt(1-r^2)>1.
As theta increases, r decreases, so c-sJ(r) is nonincreasing.
Therefore G' can change sign only from positive to negative. The
minimum of G on this second interval is again at an endpoint. The
degenerate endpoint cases follow by continuity.

It remains to inspect only theta=0, theta=pi/2, and
theta=pi/2-phi. The first two values are both c-s/2. If

    kappa=(c+s)/(1+c),

then 1/2<=kappa<=1, and consequently c-s/2>=c-s kappa=F.
The bound kappa>=1/2 follows from c+2s>=1: for example,
c+s>=1 already suffices.

At the middle endpoint r=s,t=c,

    G=1-3s/2+sc/(1+s).

With z=s/(1+c), so 0<=z<=1, direct substitution of
c=(1-z^2)/(1+z^2), s=2z/(1+z^2) gives the exact identity

    G-F(c,s)=z^3(3-z)/[(1+z)(1+z^2)]>=0.

This proves (16) on the entire continuous quadrant.

We will also use

    1-kappa=(1-s)/(1+c)<=c/2.                        (17)

For c>0, use 1-s=c^2/(1+s) and
2c<=(1+s)(1+c). The latter follows already from
1+c>=2c and 1+s>=1. For c=0, (17) is immediate.

### 6.2. Exact support and the two possible upper faces

Every nonaxis orientation of K admits face normals

    u=(r,t), v=(-t,r),      r,t>0,      r^2+t^2=1.

There is no requirement r>=t. Write its lower face values as U,V:

    U<u·x<U+a,       V<v·x<V+a.

For the target direction n=(c,-s), set

    d=cr-st,       e=ct+sr.

Since n=d u-e v, its exact upper support is

    S=upper_K(n)=dU-eV+a max(d,0).                   (18)

The actual x wall gives

    rU-t(V+a)>=0.                                  (19)

Since H-A=(0,1/2), both lower face inequalities for H are strict.
Therefore exclusion of H implies at least one of

    U+a<=r+3t/2,       V+a<=-t+3r/2.                (20)

We cover both alternatives, retaining their possible overlap.

If the first inequality in (20) holds, (19) gives
V<=(r/t)U-a. Substitution in (18), followed by its upper bound
for U, gives

    S>=-(s/t)U+a[e+max(d,0)]
      >=aG+(a-1)s(r/t+3/2)
      >=aF.

The displayed identity uses 1/t-tau=r/t. It is valid for either
sign of d.

Now suppose the second inequality in (20) holds and d>=0.
From (19), U>=(t/r)(V+a). Thus

    S>=-(s/r)V+ad(1+t/r)
      >=a[c(r+t)+s(r-t)]+s(t/r-3/2).

Subtracting aG in this sign regime gives exactly

    S-aG>=s[t/r-tau+(a-1)(3/2-tau)]>=0.

Here t/r>=tau and 0<=tau<=1. This proves S>=aF in this
case too. This exact difference avoids assigning an unjustified sign
to the upper face value -t+3r/2.

Finally suppose the second inequality in (20) holds and d<0.
Strict ownership of A gives U<r+t, so (18) yields

    S>d(r+t)-e(-t+3r/2-a)=L+(a-1)e,
    L=c-s+(1-r/2)e.

The condition cr<st implies e>=c. Indeed

    e-c=r[s-cr/(1+t)]>=0.

Also F<=c, and, using (17),

    L-F=(1-r/2)e-s(1-kappa)
        >=c/2-s(1-kappa)>=0.

Consequently S>aF. This completes the nonaxis corner cases for
c,s>0.

If s=0, the x width of a square is at least a, and its least x
coordinate is nonnegative, so upper_K(1,0)>=a. If c=0,
strict ownership of A implies min_K y<1, and hence
upper_K(0,-1)>-1>-a=aF(0,1).

It remains to handle an axis-parallel corner. Write its lower coordinates
as k,h>=0. Since A is strict, x=1 lies strictly in its horizontal
interval. The excluded point H therefore forces h+a<=3/2. Its
rightmost x coordinate is k+a>=a, so

    S>=ac-s(3/2-a)
      >=a(c-s/2)>=aF.

The middle inequality has difference 3s(a-1)/2>=0. This proves
Theorem 6 for every orientation and every target direction.

### 7. All-angle boundary transfer from the corner profile

### Theorem 7

Let B and K be distinct open squares of the same side a>1 with disjoint
interiors. Suppose B's closure lies in y>=0, K's closure lies in the
first quadrant, and, for some 0<b<1 and 1<ell<2,

    B strictly owns (2,b), (ell,1);
    K strictly owns (1,b), (1,1) and excludes (1,3/2).

Then B strictly owns P=(2,1). Neither square has an angle restriction.

### Proof

Theorem 6 supplies the support profile (15) for K. Also
I={1} x [b,1] is strictly inside K.

If B is axis parallel, P takes its x coordinate from the strict point
(2,b) and its y coordinate from the strict point (ell,1), so it is
strict in B. Otherwise choose its actual face normals in the form

    u=(p,-q), v=(q,p),      p,q>0,      p^2+q^2=1.

Such a choice is possible for every nonaxis square. No restriction
p>=q is made: a square of positive canonical angle is represented by
reindexing and changing the sign of one of its original normals.

The u projection of P lies strictly between the u projections of
(ell,1) and (2,b), while its v projection exceeds both. Thus, if P
were missing, its only possible exit would be

    V_B+a<=v·P=2q+p.                                (21)

Let Z be B's leftmost vertex. With its center denoted by B_0,

    Z=(B_0x-a(p+q)/2, B_0y-a(p-q)/2).

This vertex lies on B's lower u and lower v faces. The actual bottom
wall gives Z_y>=aq. From (21),

    q(2-Z_x)+p(1-Z_y)>=a,

and therefore

    q Z_x<=2q+p-a(1+pq)
          <q-(1-p)(1-q)<=q.

Hence Z_x<1.

In fact Z_y<b. If Z_y>=1, let A=(1,1). Its lower u inequality
is strict because

    u·(A-Z)=p(1-Z_x)+q(Z_y-1)>0.

Its lower v inequality follows from (21):

    v·A=v·P-q>=V_B+a-q>V_B,

since a>1>q. Both upper inequalities are strict by comparison with
the strict point (ell,1). Thus A would belong to B, contrary to
its ownership by K.

If instead b<=Z_y<1, the segment from the closure point Z to the
strict point (ell,1) crosses x=1 at a strict point of B whose
height lies strictly between b and 1. This contradicts I being
strictly in K. Both alternatives are impossible, proving Z_y<b.

Orient any possible separating normal n from K toward B. Since the
strict points (1,b) in K and (2,b) in B differ by (1,0), n_x>0.
If n_y>=0, then Z_x<1 and Z_y<b<1 give

    lower_B(n)<=n·Z<n·(1,1)<upper_K(n),

which contradicts separation. Consequently every possible separating
normal has the form n=(c,-s), with c,s>0 and c^2+s^2=1.

The boundary support cap proved at the end of this appendix now applies over
the full orientation quadrant p,q>0. Its proof did not use p>=q:
its half-angle tau=q/(1+p) is simply in (0,1). Explicitly,

    lower_B(c,-s)
      <=a[c(2-p-tau)-sq+min(cq-sp,0)]
           -(a-1)(2c+cp/q)
       <aF(c,s).

The two exact factor identities below prove the last inequality
on all 0<=tau<=1. But Theorem 6 gives
upper_K(c,-s)>=aF(c,s). Thus no normal from either actual square
can separate them, a contradiction to their disjoint interiors.
The supposition that P is missing is impossible. This proves Theorem 7.

### 4.2. The boundary support cap

Define, for `r,t>=0` on the unit circle,

    F(r,t)=2r-1-r t/(1+r)
          =r-t(r+t)/(1+r).                            (8)

For every target normal (r,-t), with r,t>0 and r²+t²=1, the assumption that P is missing implies

    lower_B(r,-t)<a F(r,t).                           (9)

Here is a direct proof. Write `tau=s/(1+c)`. The leftmost vertex V of the boundary square
has `V_y>=as`, by the actual bottom wall. The missing point P=(2,1) supplies the upper-v cap, which gives

    s(2-V_x)+c(1-V_y)>=a.

Since `n·u=rc+ts>0`, the exact support at that vertex is

    lower_B(n)=rV_x-tV_y+a min(rs-tc,0).

Eliminate V_x using the previous inequality, then use `V_y>=as`:

    lower_B(n)
      <=a[r(2-c-tau)-ts+min(rs-tc,0)]
         -(a-1)(2r+rc/s).                             (10)

The last subtracted term is strictly positive. It remains to prove

    r(2-c-tau)-ts+min(rs-tc,0)<=F(r,t).                (11)

Put `z=t/(1+r)`, so `0<=z,tau<=1`. After multiplication by
`1+tau^2`, the right side of (11) minus its left side is exactly

    (tau-z)[r tau^2-(1+r)tau+r+t]       if tau>=z,

    (z-tau)[-r tau^2+(1+r+t)tau+1-t]   if tau<=z.

In the first region, the bracket decreases on `[0,1]` and is at least
its value `r+t-1>=0` at one. In the second, the bracket equals

    1-t+tau[1+t+r(1-tau)]>=0.

These factor identities prove (11), and (10) proves the strict cap (9).



---

<a id="appendix-g"></a>

## Appendix G. Central crosspoint and the top-only extension

### Appendix. Complete retained central crosspoint proof

Let D strictly own

\[
P=(2,2.26),\quad Q=(2.26,2),\quad M=(2.35,2.35),
\]

and exclude

\[
G=(2.35,1.65),\quad B_0=(1.65,2.35),\quad
R_0=(3,2.4),\quad R_1=(3,2.5).
\]

We prove that Z=(2,2.5) is strict. Relabel face normals so that u=cx+sy,v=−sx+cy with c>0,s≥0,c²+s²=1. Here no ordering between c and s is imposed, so this single positive-quadrant choice covers every square orientation. Write U,V for the lower faces.

The lower-u band of Z follows from P, with increment .24s≥0. Its lower-v band follows from Q, with increment .26s+.5c>0. The point G has both upper bands strict from M,P. It therefore fails lower-u or lower-v.

First suppose V≥v(G). The point B₀ has strict upper-u from M and strict lower-v from Q. Its upper-v band is also strict, since

\[
v(B_0)-v(G)=.7(c+s)\le.7\sqrt2<1<a.
\]

Hence B₀ fails lower-u, so U≥u(B₀). The two remaining upper bands of Z now follow from

\[
u(Z)-u(B_0)=.35c+.15s\le\sqrt{.145}<1<a,
\]

\[
v(Z)-v(G)=.85c+.35s\le\sqrt{.845}<1<a.
\]

Now suppose U≥u(G). Strict ownership of P implies

\[
.35c<.61s. \tag{11}
\]

The upper-u band of Z follows immediately from u(Z)−u(G)=−.35c+.85s≤√.845<1<a.

The point R₀ has its lower-u band strict from M and its upper-u band strict from the assumed lower face, because

\[
u(R_0)-u(G)=.65c+.75s\le\sqrt{.985}<1<a.
\]

Its upper-v band is strict from P: v(R₀)−v(P)=.14c−s<0 by (11). It must therefore fail lower-v, giving V≥2.4c−3s.

If 20s≤99c, the exact identity

\[
(s+.1c)^2-1=.01c(20s-99c)\le0
\]

shows s+.1c≤1<a. Since v(Z)−(2.4c−3s)=s+.1c, this gives Z's upper-v band.

If 20s>99c, use R₁ instead. Its lower-u band is strict from M, and its upper-u band follows from

\[
u(R_1)-u(G)=.65c+.85s
<\left(\frac{13}{99}+.85\right)s<1<a.
\]

Its upper-v band is strict from P because .24c−s<0. Hence V≥2.5c−3s, and

\[
v(Z)-(2.5c-3s)=s\le1<a
\]

proves the last upper band. The strict case split includes every angle; when s=0, (11) is impossible and the first lower-face alternative applies. All tangencies at excluded points remain permitted. This completes the retained crosspoint proof.

### 3. A top-only square extends past the half-unit point

**Theorem.** Let Q be an open square of side a>1 strictly owning

    M=(.35,.35), A=(.4,1),

and excluding

    L=(0,.26), P=(0,1), X=(.5,0).

Then Q strictly owns H=(.5,1). No container, upper side bound, or foreign segment is needed.

**Proof.** Let U,V denote lower face coordinates. First use a nonnegative canonical frame u=(c,s), v=(−s,c), where c≥s≥0 and c²+s²=1. At H its lower u band follows from A, its lower v band from M, and its upper v band from A:

    u(H)−u(A)=.1c>0,
    v(H)−v(M)=.65c−.15s≥.5c>0,
    v(A)−v(H)=.1s≥0.

Suppose H is not strict. It must be upper u, so U+a≤.5c+s. At P its upper u band follows from A and its lower v band from M. A lower u exclusion would give the impossible width a≤u(H)−u(P)=.5c≤.5. Hence P is upper v, V+a≤c.

At L its upper u band follows from M and its upper v band from A; the increments are .35c+.09s>0 and .74c−.4s≥.34c>0. A lower v exclusion would give a≤v(P)−v(L)=.74c<1. Consequently L is lower u, U≥.26s. The two u faces now yield

    a≤.5c+.74s≤sqrt(.7976)<1,

a contradiction. Thus H is strict for every nonnegative canonical representative, including the axial and diagonal endpoints.

Use the nonpositive frame u=(c,−s), v=(s,c). Both lower bands of H follow from A, so an excluded H must be upper u or upper v. At P the upper u band follows from A, the upper v band from A, and the lower v band from M: their increments are .4c>0, .4s≥0, and .65c−.35s≥.30c>0. Therefore P is lower u, U≥−s. If H were upper u, the opposite width would be a≤.5c≤.5. Thus

    V+a≤v(H)=.5s+c.                                     (3)

At X its lower u band follows from M and its upper v band from M, with increments .15c+.35s>0 and .35c−.15s≥.20c>0. Its lower v band is strict by the cap (3), because

    v(H)−v(X)=c≤1<a.

Therefore the excluded X must be upper u, U+a≤.5c. At L its upper u band follows from M and its upper v band from A:

    u(M)−u(L)=.35c−.09s≥.26c>0,
    v(A)−v(L)=.4s+.74c>0.

Its lower u band follows strictly from the opposite cap at X, since

    u(X)−u(L)=.5c+.26s≤sqrt(.3176)<1<a.

Thus L is lower v. Together with (3) this gives

    a≤v(H)−v(L)=.5s+.74c≤sqrt(.7976)<1,

again impossible. Both canonical signs and their axis and diagonal limits are covered. Every exterior face inequality was weak, and each target band obtained from an owned anchor or an opposite face was strict. ∎



---

<a id="appendix-h"></a>

## Appendix H. The sharp northeast point, left point, and all four faces

### 4. The upper square needs only its marker and outer top point

**Theorem 3.** Let Q have side a>1 and strictly own

    M=(.35,.35), A=(.4,1).

Suppose Q excludes L=(0,.26), P0=(0,1), P1=(1,1), and the entire segment

    B={1}×[.26,.56].

Then Q strictly owns Y=(.525,.125).

This point conclusion does not require ownership of either (.26,0) or (.26,1). In particular the strict span in Theorem 2 is unnecessary for this weaker, unoriented conclusion.

**Proof.** Suppose Y is excluded. Write B0=(1,.26), B1=(1,.56), and let U,V be lower face coordinates.

First use a nonpositive canonical frame u=(c,−s), v=(s,c), with c≥s≥0 and c²+s²=1. At P0 both upper bands follow from A and its lower v band follows from M. Hence P0 is lower u: U≥−s. At Y its lower u and upper v bands follow from M, with increments .175c+.225s>0 and −.175s+.225c≥.05c>0. It is upper u or lower v. Upper u would give

    a≤u(Y)−u(P0)=.525c+.875s≤1.4/sqrt(2)<1.

Thus Y is lower v. At P1 both lower bands follow from M. An upper v exclusion would imply

    a≤v(P1)−v(Y)=.475s+.875c≤sqrt(.99125)<1.

Therefore P1 is upper u, and opposite u faces at P0,P1 give a≤c≤1. This contradiction excludes the entire nonpositive sign under the supposition that Y is missing.

Now take the nonnegative frame u=(c,s), v=(−s,c). The upper v band of Y is strict by M, with difference .175s+.225c>0. It can therefore be lower u, upper u, or lower v.

Suppose first that Y is lower u. At P1 both lower bands follow from M, and its upper u band follows from the opposite lower face at Y because

    u(P1)−u(Y)=.475c+.875s≤1.35/sqrt(2)<1<a.

Thus P1 is upper v. At B0 its lower u band follows from M and its upper v band from A. Its upper u band follows from

    u(B0)−u(Y)=.475c+.135s≤sqrt(.24385)<1<a.

Hence B0 is lower v. These two v faces give a≤v(P1)−v(B0)=.74c<1. Thus Y cannot be lower u.

Suppose next that Y is upper u. At P0 its upper u band follows from A and its lower v band follows from M. If it were lower u, the gap u(Y)−u(P0)=.525c−.875s≤.525 would contradict a>1. Therefore P0 is upper v. At L both upper bands follow from M,A: the positive increments are .35c+.09s and .74c−.4s≥.34c. If L were lower v, its opposite-face gap to P0 would be .74c<1. Hence L is lower u. But then a≤u(Y)−u(L)=.525c−.135s≤.525<1. Thus Y cannot be upper u either.

The only remaining possibility is

    V≥v(Y)=−.525s+.125c.                               (18)

At P1 both lower bands are strict by M. Its upper v exclusion would give a≤.875c−.475s≤.875, so P1 is upper u. At P0 the upper u and lower v bands follow from A,M; a lower u exclusion would give width c≤1 opposite P1. Hence P0 is upper v. At L both upper bands follow from M,A as above; lower v would give width .74c opposite P0, so L is lower u. At B0 its lower u band follows from M and its upper v band from A. Its upper u band is strict because the lower face at L gives u(B0)−U≤c≤1<a. Therefore

    U≥.26s,  V≥−s+.26c,  V+a≤c.                       (19)

The actual whole segment now forces s+.44c>1 by the same explicit vertex argument as Theorem 2. To repeat its short derivation, if s+.44c≤1, B1 has its lower u band from M and upper v band from A. Lower v would give width at most s+.44c opposite the cap V+a≤c, so B1 must be upper u: U+a≤c+.56s. The closed rightmost vertex Z then obeys

    Z_x≥a(c+s)−.74cs>1,
    .26<Z_y≤.56+c(s+.44c−a)<.56.

Here the lower ordinate bound is .26+s(a−c)>.26; s=0 is already impossible from (19), which would give a≤1. Interpolation from strict M crosses B at a strict point before Z, a contradiction.

Thus the half-angle t=s/(1+c) exceeds7/18. But (18) and (19) give

    a≤c−v(Y)=.875c+.525s<14917/14920<1,

because at half-angle 7/18 the exact value is 14917/14920, and .875c+.525s decreases throughout the required interval (its derivative is -.875s+.525c<0 there). This final contradiction proves that Y is strict in Q. Every canonical sign and endpoint has been covered, and excluded points and segment contacts were allowed to be tangent. ∎

### 1. Statement and the two strict short chords

**Theorem 1.** Suppose Q strictly owns

    M=(.35,.35), G=(.26,1), Y=(.525,.125),

and excludes P=(0,.26), O=(0,1), C=(1,1), and the whole segment

    B T={1}×[.26,.56].

Then Q strictly owns X=(0,.62).

**Proof.** The strict segment M Y crosses y=.26 at an abscissa strictly between zero and one. The point G is strict on y=1. On each horizontal line, the two endpoints at x=0 and x=1 are excluded. Thus both open chords are positive and lie in (0,1), with lengths at most one. An axis-parallel square would have chord length a>1 and is impossible.

Choose c≥s>0, c²+s²=1 in either canonical frame. The square's horizontal chord function, where positive, is

    ell(y)=min(a/c, (a(c+s)/2−|y−y0|)/(cs)),

where y0 is its center ordinate. Both chords have length at most one, whereas the plateau has length a/c>1, so neither chord is on the plateau.

The center lies strictly between .26 and1. If it were below both lines or above both lines, the two nonplateau chord lengths would differ by

    .74/(cs)≥1.48>1,

impossible for two positive lengths at most one. A center on either chord line would itself give the plateau length greater than one. Therefore the lower chord is in the lower vertex region, and the upper chord is in the upper vertex region. The next two sections write all four endpoint inequalities in each sign. Endpoints may touch the two excluded points, so the resulting inequalities are weak.

### 2. Positive canonical sign

Use u=(c,s), v=(−s,c), with lower faces U,V. On y=.26 the left and right chord endpoints are

    (U−.26s)/c, (.26c−V)/s.

On y=1 they are

    (c−V−a)/s, (U+a−s)/c.

Their containment in [0,1] gives

    U≥.26s, V≥.26c−s,
    V+a≤c, U+a≤c+s.                                  (1)

At the upper bar endpoint T=(1,.56), the lower u band follows from M, and its upper v band follows from G. Its exclusion is consequently upper u or lower v.

Suppose T were not lower v. Then it would be upper u, U+a≤c+.56s. Any hypothetical interior point of Q on x=1 would have, from this upper u face and the lower v face at B in (1),

    y<.56,  y>.26.

It would lie on the excluded whole segment B T. The square therefore has no interior intersection with x=1. Its strict marker M is to the left of that line, so convexity forces its rightmost closed support to be at most one.

But (1) gives the contradictory lower bound

    xmax=c(U+a)−sV≥a(c+s)−.74cs>1.                    (2)

For the final inequality, c+s−1=2cs/(c+s+1)≥(2sqrt(2)−2)cs>.74cs, and a>1. This argument explicitly keeps the weak tangency possibility xmax=1. It follows that T must be lower v:

    V≥.56c−s,  a≤s+.44c.                              (3)

Set t=s/(1+c)∈(0,sqrt(2)−1]. The exact factorization

    s+.44c−1=2(18t−7)(1−t)/(25(1+t²))

and a>1 show that t>7/18. The target X has its upper u band from M, lower v band from M, and upper v band from G. The increments are .35c−.27s≥.08c>0, .35s+.27c>0, and .38c−.26s≥.12c>0, respectively.

Its remaining lower u band follows from U+a≤c+s: the opposite gap is

    (c+s)−u(X)=c+.38s.

This expression decreases once s/c>.38. At t=7/18 the exact components are c=275/373, s=252/373, and its value is 9269/9325<1. Thus in the required interval c+.38s<1<a, proving the final strict target band.

### 3. Negative canonical sign

Use u=(c,−s), v=(s,c). The lower horizontal chord has endpoints

    (V−.26c)/s, (U+a+.26s)/c,

and the upper chord has endpoints

    (U+s)/c, (V+a−c)/s.

Consequently

    V≥.26c, U+a≤c−.26s,
    U≥−s, V+a≤c+s.                                   (4)

In particular a≤.74c+s. The factorization

    .74c+s−1=(87t−13)(1−t)/(50(1+t²))

gives t>13/87.

At T both lower bands follow from M. An upper v exclusion would give, using (4),

    a≤v(T)−.26c=s+.30c≤1.30/sqrt(2)<1,

which is impossible. The displayed canonical bound holds because s+.30c increases on 0≤theta≤pi/4. Thus

    U+a≤c−.56s.                                       (5)

The target's upper u band follows from M, with increment .35c+.27s>0. Its upper v band follows from G, with increment .26s+.38c>0. Its lower v band follows strictly from the opposite upper face V+a≤c+s because

    (c+s)−v(X)=.38c+s≤1.38/sqrt(2)<1<a.

Finally (5) gives the opposite gap for its lower u band:

    (c−.56s)−u(X)=c+.06s<1<a.

For this last strict comparison, c+.06s−1=2t(.06−t)/(1+t²)<0 since t>13/87>.06. Hence all four target bands are strict in the negative sign too. Both canonical diagonal endpoints have been included, and the axial case was excluded by the two strict short chords. ∎



---

<a id="appendix-i"></a>

## Appendix I. A single northeast frame and its uniform support bounds

### 2. One northeast face table covers both of its canonical signs

Appendix H applies to N by the actual-owner table in Section 5. In its positive canonical frame (c_N,s_N), its complete chord/bar faces are

    U_N≥.26s_N, V_N≥.56c_N−s_N,
    U_N+a≤c_N+s_N, V_N+a≤c_N.

In its negative canonical frame they are

    U_N≥−s_N, V_N≥.26c_N,
    U_N+a≤c_N−.56s_N, V_N+a≤c_N+s_N.

These are all four faces in Sections 2–3 of that theorem, including the whole right-bar argument. For the negative sign retain its frame. For the positive sign choose the other downward-right axis, namely −v_N, as its first axis. In both cases we obtain the single quadrant frame

    u_N=(d,−r), v_N=(r,d), d,r>0, d²+r²=1,

with lower faces P,Q and upper faces J=P+a,T=Q+a satisfying

    P≥−r, Q≥.26d,
    J≤d−.56r, T≤d+r.                                (4)

For the positive original sign the exact relabeling is

    d=s_N, r=c_N,
    P=−(V_N+a), J=−V_N,
    Q=U_N, T=U_N+a.

Thus (4) concerns the same actual N in either case. Its strict point (0,.62) additionally gives

    Q<.62d.                                         (5)

The two opposite widths in (4) give

    1<a≤d+.44r, 1<a≤.74d+r.

Let p=angle(d,r) and z=tan(p/2). The exact identities

    d+.44r−1 = 2z(.44−z)/(1+z²),
    .74d+r−1 = (1−z)(87z−13)/(50(1+z²))

therefore prove

    p0<p<p1,
    p0=2 atan(13/87), p1=2 atan(11/25).              (6)

Put

    d0=cos p0=3700/3869,
    r0=sin p0=1131/3869,
    h0=tan(p0/2)=13/87,
    Hn=d0+r0=4831/3869.

The following rational bounds will be used:

    .95<d0<1, .29<r0<.3,
    d0−r0>.66, 1.24<Hn<1.25,
    d>2/3, r<3/4, d+r≥Hn, d+r<10/7.               (7)

For the last lower bound, d+r increases up to p=pi/4 and decreases afterwards. Its endpoint at p1 is527/373>Hn. This checks the whole interval in (6), including the possible positive original sign of N.

### 5. Northeast support bounds when R supplies that separator

Suppose the N→R separator is u_R=(b,-t), with lower face L; the point cone gives 95b>87t and hence b>2/3,t<3/4. Put

    delta=db+rt>0, h=rb−dt.

The full N support, (4),(5), and a>1 give

    h≥0 ⇒ L>b A(p)+t B(p),
    h≤0 ⇒ L>b Cn(p)+t Dn(p),                        (21)

where

    Cn(p)=d−.38dr,
    Dn(p)=r−.62−.38r².

At h=0 both expressions equal1−r, so the shared endpoint is included. In the second line, the support is delta J+hQ; the actual strict point (0,.62) gives precisely Q<.62d.

At p0 the four exact constants are

    A*=15594461/14969161,
    B*=−14778022/14969161,
    C*=12725114/14969161,
    D*=−5391122/14969161.                             (22)

Thus1.04<A*<1.05, B*<−.98, and D*>−.37. We claim that (21) implies

    theta≤p0 ⇒ L>b A*+t B*;
    theta≥p0 ⇒ L>min{b C*+t D*, 1−t}.               (23)

For the first line, p≥p0≥theta means h≥0. We have B'(p)=d+r−1.48dr>.5 by (7). Moreover A(p)≥A(p0): its concave expression in H=d+r has its smaller endpoint at Hn, since

    A(10/7)−A(p0)=124461293/73348888900>0.

Therefore both terms bA+tB are at least their values at p0.

For the second line, first suppose p≥theta. Then w=t/b≥r0/d0>.3. On the entire relevant p interval,

    A'(p)=(d−r)[1−.74(d+r)]>−.06,
    B'(p)>.5.

For the first estimate, a negative value with d≥r is bounded below by −2/35; if d<r then d+r>41/30>50/37, so the product is positive. Thus bA+tB increases with p, since its derivative divided by b exceeds −.06+.3(.5)>0. At p=theta its value is1−t.

If p≤theta, the second expression in (21) can instead be written

    g(p)=cos(p−theta)(1−.38 sin p)−.62 sin theta.

On the enlarged interval p0≤p≤theta its second derivative is

    g''=cos(p−theta)(−1+.76 sin p)
           −.76 cos p sin(theta−p)<0.               (24)

This interval is legitimate even if theta exceeds p1: the point cone ensures sin theta<3/4 and theta<pi/2, so every sign in (24) still holds. Concavity gives

    g(p)≥min{g(p0),g(theta)}
         =min{b C*+t D*,1−t}.

This proves (23) for every angle and both relative orders.



---

<a id="appendix-j"></a>

## Appendix J. Complete three-square ending: the full-lower-support alternative

Translate the original coordinates by (−2,−2). Suppose the actual southeast square E has strictly negative canonical angle and owns F4. Its strict anchors include

    M=(.35,−.35), I=(0,−.26), D=(.26,0).

These are its original marker,F4,G6. Its excluded O=(0,0) is strictly in the actual merged W. The foreign whole bottom bar

    [.26,.8]×{−1}

is strictly in the actual bottom owner. The foreign R0=(1,0) is strict in actual R. The foreign Y=(.525,.125) is strict in actual N.

Use the canonical frame and full faces

    u_E=(c,−s), v_E=(s,c), c≥s>0, c²+s²=1,
    lower U,V; upper A=U+a,H=V+a.

At O both v bands follow from I,D and the upper u band follows from M. Therefore U≥0. At R0 its lower bands follow from D,I, while A≥a>1 gives its upper u band. Thus R0 is upper v. At Y both lower bands follow from D, and its upper u band follows from A>1. Consequently

    U≥0, A≥a>1, U<.26s, V<−.26c<0,
    H≤s, H≤.525s+.125c.                         (1)

The bottom-bar alternatives proved in Section 6 of this document use only these anchors, O,R0 and this actual bottom bar. They remain literal here: its first endpoint forces V≥.26s−c; the second is either lower v or upper u. If it is not lower v, any interior intersection with y=−1 would fall strictly within the foreign bar. Since M is above that line, the complete closed lower support must then satisfy

    −sA+cV≥−1.                                  (2)

The other retained alternative is V≥.8s−c.

**Theorem 1.** Alternative (2) is impossible in the stated actual entrance.

The rest of this chapter proves the theorem. All the northeast and right-square information used below is supplied in Section 5 and Appendices H–I; no bottom origin or merged vertical midpoint is assumed.

### 2. Consequences of the actual lower support

Equation (2) is equivalent to

    H≥a+(sA−1)/c
      ≥a(1+s/c)−1/c.                            (3)

Put

    q=angle(c,s),
    f(q)=1+(s−1)/c,
    e(q)=(1−c)(1−s)/c.

Then H>f(q)>0 and f(q)=s−e(q). The exact derivative is

    f'(q)=1/(1+s).                              (4)

Combining (3) with the last bound in (1) gives

    c+s−1−.525cs−.125c²<0.

The derivative of the left side with respect to q is

    (c−s)[1−.525(c+s)]+.25cs>0.

Here c+s<3/2, so the first bracket is positive. At s=7/20 and c=√351/20 the expression is

    (653√351−12155)/16000>0,

because 653²·351−12155²=1925534>0. Thus the whole allowed interval satisfies

    0<s<.35, c>.93.                             (5)

Two uniform consequences, including all endpoints needed below, are

    e(q)<.05,
    (962/3869)−s(1−s)/c>5785/1439268>0.          (6)

For the first, s²(1−s) increases on [0,.35], and

    e(q)=s²(1−s)/(c(1+c))
      <(.35)²(.65)/(.93·1.93)<.05;

the exact reserve in the last comparison is506/89745. For the second, s(1−s) increases on this interval and c>.93, so

    s(1−s)/c<(.35)(.65)/.93=91/372.

The full right support of E is strictly beyond x=1. Indeed, (3) and A≥a give

    x_max(E)=cA+sH
      ≥a(1/c+s)−s/c
      >(1+cs−s)/c
       =1+(1−c)(1−s)/c>1.                     (7)

This uses the actual lower support (2), not an extra container wall.

### 3. Northeast profile and all possible actual separating normals

The common northeast frame and profile from Section 5 are

    u_N=(d,−r), v_N=(r,d), d,r>0, d²+r²=1,
    lower P,Q; upper J=P+a,T_N=Q+a,

    P≥−r, Q≥.26d,
    J≤d−.56r, T_N≤d+r, Q<.62d.                  (8)

This is a frame of the same actual N for either original canonical sign. The strict point giving Q<.62d is N's proved (0,.62).

Let

    p0=2 atan(13/87), p1=2 atan(11/25),
    d0=3700/3869, r0=1131/3869,
    Hn=d0+r0=4831/3869.

The two complete widths in (8) prove

    p0<p=angle(d,r)<p1,
    d>2/3, r<3/4, d+r≥Hn, d+r<10/7.             (9)

In particular Hn−1=962/3869. These two-sign profile and interval deductions are proved in Appendices H–I, using exactly the actual sources already supplied by the present upper-right reduction.

Choose the downward-right quadrant frame of actual R:

    u_R=(b,−t), v_R=(t,b),
    b,t≥0, b²+t²=1, theta=angle(b,t).

Its lower faces L,K satisfy, from its strict origin and real right container wall,

    L<b, K<t,
    b(L+a)+t(K+a)≤2.                            (10)

For disjoint open squares, an actual face normal separates the two full squares. Orient it from E toward R. The strict points D,R0 force its x component positive. E's u_E direction cannot separate because its upper support A>1 is greater than the strict R0 projection c. E's only other possible direction is v_E.

Of R's positive-x normals, u_R is also impossible. If theta≥q, its coordinates in E's frame are k=cb+st>0 and h_E=sb−ct≤0. The full E support is kA+h_E V. Here V<0 and

    k≥b/c≥b,

so the support is greater than b, whereas L<b. If theta≤q, that support is kA+h_E H. As a function of the normal angle on [0,q], its excess over b is a linear combination of b,t. At theta=0 this excess is x_max(E)−1>0 by (7); at theta=q it is A−c>0. Every intermediate normal is a positive linear combination of these two endpoint normals, so its support excess is positive too. This excludes u_R in both relative orders.

Thus the exhaustive E→R list is

    v_E or v_R.                                 (11)

For N→R the strict pairs

    (.5,1)→(1,0),
    (.525,.125)→(1,.56)

are available in these same actual squares. They give n_x>0 and n_y<.5n_x. The following explicit support argument proves from precisely (8),(9) and these strict pairs that v_N and v_R cannot separate: the former fails the cone; the latter has full N support greater than t, against K<t. Explicitly the latter support bound uses

    A_N(p)=d+r−.74dr>1,
    B_N(p)=r−d−.26−.74r²<0

and gives upper_N(v_R)>t A_N−b B_N>t.

The exhaustive N→R list is therefore

    u_N or u_R.                                 (12)

If u_R supplies it, the second strict pair also gives

    95b>87t, b>2/3, t<3/4.                      (13)

All reverse normals have been excluded by the strict positive-x cones. Equations (11),(12) leave four complete-square separator combinations.

### 4. A universal lower face bound when R supplies the E separator

Use throughout

    j=ct−sb, k=cb+st>0.

Suppose E→R uses v_R. We prove the useful bound

    K>f(theta)=1+(t−1)/b.                        (14)

The b=0 endpoint cannot occur: then this separator is the positive x direction, and (7) contradicts K<t=1. The theta=0 endpoint is also already impossible because E's strict D has y=0 and K<0. We may assume b,t>0.

If theta≥q, so j≥0, the full support and (3) give

    K≥jA+kH
      ≥(t/c)A+ka−k/c
      >t/c−k(1−c)/c.                            (15)

The deficit of the final expression below t is

    E_q=(1−c)[b−t(1−s)/c].

For fixed theta, (1−c) increases with q, and the bracket increases with q because (1−s)/c decreases. If E_q≤0, it is already less than the positive value E_theta. If E_q>0, both increasing positive factors give E_q≤E_theta for q≤theta. The endpoint is

    E_theta=(1−b)(1−t)/b.

Thus (15) implies K>t−E_theta=f(theta).

If theta≤q, the full support is jU+kH. Using (3) before dropping U, its coefficient is

    j+ks/c=t/c≥0.

Therefore K>k f(q). On the entire interval theta≤q≤pi/4,

    d[k f(q)]/dq
      =k/(1+s)−sin(q−theta)f(q)
      ≥c/(1+s)−s f(q)
       =c−s≥0.

At q=theta, k f(q)=f(theta), proving (14) in this order too.

When this R-axis separator is used, its exact bound (15) and K<t also give

    theta<atan(45/31).                           (16)

For theta≤q this follows already from (5). For theta≥q, (15) requires E_q>0 and hence

    t/b<c/(1−s)=(1+s)/c<1.35/.93=45/31.

No angle restriction on R is assumed apart from this derived one.

### 5. Strong northeast support when R supplies that separator

Suppose N→R uses u_R. The complete two-order bounds in Appendix I use exactly (8)–(10), and give

    theta≤p0 ⇒ L>b A*+t B*,
    theta≥p0 ⇒ L>min{b C*+t D*,1−t},             (17)

where

    A*=15594461/14969161,
    B*=−14778022/14969161,
    C*=12725114/14969161,
    D*=−5391122/14969161.

In particular

    1.04<A*<1.05, −1<B*<−.98.

We sharpen (17) to the convenient common conclusion

    L>1−t.                                      (18)

On [0,p0], the function b A*+t(B*+1)−1 is concave, with endpoint values A*−1>0 and0. Both trigonometric coefficients are positive, so this is its ordinary second-derivative concavity. Thus its value is nonnegative throughout.

For theta≥p0, (13) gives theta<atan(95/87)<atan(9/8). The function b C*+t(D*+1)−1 is also concave. At p0 it is0. At atan(9/8) its value is positive, since 8C*+9(D*+1)>0 and

    [8C*+9(D*+1)]²−145
      =2854238647278624/224075781043921>0.

This proves (18) for both terms of the minimum in (17).

### 5.1. R supplies both separators

Combine (14),(18) with the real wall (10). Its left side is strictly greater than

    b(2−t)+t[1+f(theta)]
      =2+(1−b)²(1−t)/b≥2,                     (19)

which is impossible. The theta=0 endpoint was already excluded in Section 4; (13) ensures b>0.

### 5.2. E supplies its own separator

Now E→R uses v_E. Its exact support ordering is

    H≤−jL+kK−a max(j,0).                         (20)

Combine this with (3) and the real wall, eliminating K. The coefficient of L is c, and the positive coefficient of a can be reduced using a>1. The necessary inequality is

    cL+t f(q)+k(b+t−2)+t max(j,0)<0.              (21)

We show its left side is positive.

First suppose theta≥q, so j≥0. By (18) it exceeds or equals

    G(q,theta)
      =(2−t)(c−k)+t f(q).                        (22)

For fixed theta this decreases with q on [0,theta]. Indeed

    partial_q G
      =−(2−t)[s(1−b)+ct]+t/(1+s)<0.

To justify the last sign even over this enlarged q interval, (13) gives cos q≥b>2/3 and tan(q/2)≤t/(1+b)<.45. Hence

    c(1+s)−1=s[c−tan(q/2)]≥0.

Consequently the negative ct term alone dominates t/(1+s), since 2−t>1. At the final endpoint q=theta,

    G(theta,theta)=(1−b)²(1−t)/b>0.

This excludes (21) in the whole theta≥q case.

Next suppose p0≤theta≤q. Here j≤0, and (18) gives the lower bound

    G(q,theta)
      =t[(b+t−1)(s−c tan(theta/2))−e(q)].         (23)

Since theta≤q, we have s−c tan(theta/2)≥tan(q/2). Also theta≤q and (5) place theta below pi/4, so b+t≥Hn. Thus (23) is at least

    t tan(q/2)[Hn−1−s(1−s)/c]>0

by (6).

It remains to include every theta in [0,min(q,p0)]. Use the stronger first bound in (17). The resulting lower bound in (21) is

    G_small(theta)
      =c[b²+bt+(A*−2)b+B*t]
        +s[bt+t²−2t]+f(q)t.                    (24)

For fixed actual q its second derivative is exactly

    G_small''
      =−2(c−s)(b²−t²)−4(c+s)bt
        +c(2−A*)b−cB*t+[2s−f(q)]t.

Throughout [0,p0], b>.95 and t<.3. Using c−s≥0, c+s≥1, A*>1.04, −B*<1, f(q)>0, and (5), this is strictly less than

    2s−c A*+4t²−2.1t
      ≤2s−c A*−.9t
      <.7−(.93)(1.04)=−167/625<0.               (25)

Thus (24) is concave on the complete interval. At theta=0 it is c(A*−1)>0. At the other endpoint, theta=q or theta=p0, the respective preceding proof (22) or (23) applies, because the bound b A*+t B* is at least1−t. Both endpoints are positive, so concavity proves positivity throughout. This contradicts (21) and completes every case in which R supplies the N separator.

### 6. N supplies its axis and R supplies the E separator

Retain (14),(16), and suppose the N separator is u_N. Put

    delta=db+rt>0, h=rb−dt.

The exact N inequality and J≥a−r give

    delta L≥a[1+max(h,0)]−r+hK.

Multiply by b and combine with delta times the real wall (10). The exact identity b h+t delta=r eliminates the mixed K coefficient. Using a>1 and K>f(theta), the necessary inequality is

    F=delta(b+t−2)+b(1−r)+r f(theta)
         +b max(h,0)<0.                         (26)

First let 0<theta≤pi/4. If p≥theta, an exact expansion gives

    F=b−b(2−b)d−r epsilon,
    epsilon=(1−b)²(1−t)/b.

Here d≤b, so

    F≥(1−b)²(1−t)(1+t−r)/b>0.                 (27)

If p≤theta, the last term of (26) vanishes. For fixed theta its p derivative is

    −(2−b−t)sin(theta−p)+d[f(theta)−b]<0.

The second bracket is negative on this whole interval: after multiplication by b its numerator is b+t+t²−2≤√2−3/2<0. Therefore F is minimized at p=theta, where F=epsilon>0. At theta=0 equation (26) instead directly gives F=1−d>0, since p>p0.

For the remaining theta≥pi/4, (16) implies

    2/5<z=tan(theta/2)<11/20.

The lower endpoint follows from √2−1>2/5. For the upper endpoint,

    tan[2 atan(11/20)]=440/279>45/31.

Drop the nonnegative last term of (26), and define

    A_theta=b(2−b−t),
    B_theta=t(2−b−t)+b−1+(1−t)/b.

Then

    F≥b−A_theta d−B_theta r
      ≥b−sqrt(A_theta²+B_theta²).

The exact half-angle identity is

    b²−A_theta²−B_theta²
      =−(z−1)² P(z)/[(z+1)²(z²+1)³],            (28)

where

    P(z)=17z⁶+8z⁵−5z⁴−8z³−5z²+1.

It is strictly negative throughout [2/5,11/20]. Indeed

    P(2/5)=−4507/15625<0,

and, since z>0,

    P'(z)/z
      =102z⁴+40z³−20z²−24z−10
      ≤102(11/20)⁴+40(11/20)³−24(2/5)−10
       =−288909/80000<0.

Thus (28) is strictly positive, proving F>0 in this final angular range as well. This contradicts (26) and excludes the third separator combination.

### 7. Both neighbors supply their own axes

Only

    H≤−jL+kK−a max(j,0),
    J≤delta L−hK−a max(h,0)                    (29)

remains. Let D0=cd+sr=cos(p−q)>0. The exact positive-multiplier identities are

    c delta−r j=D0 b,
    −c h+r k=D0 t.

Multiply the N inequality by c and the E inequality by r. Use J≥a−r, (3), the real right wall, and a>1. The necessary inequality becomes

    F(theta)<0,                                (30)

where

    F(theta)=D0(b+t−2)+c(1−r)+r f(q)
                +c max(h,0)+r max(j,0).         (31)

For fixed actual p,q this is a positive linear combination of cos theta and sin theta, plus a constant, on each interval obtained by splitting at p,q. Its two coefficients are:

| Interval | Coefficient of b | Coefficient of t |
|---|---:|---:|
| 0≤theta≤min(p,q) | D0+cr | sr |
| q≤theta≤p, if q≤p | c(d+r) | r(c+s) |
| p≤theta≤q, if p≤q | D0 | D0 |
| max(p,q)≤theta≤pi/2 | cd | D0+cr |

All are positive. Therefore F is strictly concave on each full interval, and it suffices to check theta=0,q,p,pi/2. Both possible relative angle orders are retained.

### 7.1. Outer endpoints

The two outer values coincide:

    F(0)=F(pi/2)
      =c(1−d)−r e(q)
      =r[c tan(p/2)−e(q)]>0.                    (32)

For example c>.93, tan(p/2)>13/87 and e(q)<.05 give a strictly positive bracket.

### 7.2. The endpoint theta=q

If p≥q, exact expansion gives

    F(q)=c−c(2−c)d−r epsilon_q,
    epsilon_q=(1−c)²(1−s)/c.

Since d≤c,

    F(q)≥(1−c)²(1−s)(1+s−r)/c>0.              (33)

If p≤q, the h term vanishes. For fixed q its derivative with respect to p is

    −(2−c−s)sin(q−p)+d[f(q)−c]<0.

Here f(q)<c follows from (5), or from the same elementary bound used in Section 6. Its minimum on p≤q is consequently at p=q, where the value is epsilon_q>0. This proves the q endpoint in both orders.

### 7.3. The endpoint theta=p

If q≤p, its exact formula is

    F(p)=c(1−d)(2−r)+s(r²−2r)+r f(q).            (34)

It decreases with q on the whole enlarged interval [0,p]. Its derivative is

    −s(1−d)(2−r)+cr(r−2)+r/(1+s)<0.

For this enlargement p≤p1 gives c≥d>2/3 and tan(q/2)≤11/25<2/3. Hence c(1+s)≥1, so 1/(1+s)≤c, and the last two terms are at most cr(r−1)<0. At q=p the value of (34) is

    (1−d)²(1−r)/d>0.

Therefore (34) is positive for every q≤p, whether or not p itself is in the original canonical southeast range.

If q≥p, the j term vanishes, and the exact expression is

    F(p)=r[(d+r−1)(s−c tan(p/2))−e(q)].

Since s−c tan(p/2)≥tan(q/2), (9) and (6) give

    F(p)≥r tan(q/2)[Hn−1−s(1−s)/c]>0.           (35)

Thus all four endpoints are positive. The interval concavity statements prove F(theta)>0 for every theta∈[0,pi/2], contradicting (30). This excludes the last separator combination.



All four actual separator combinations have been contradicted. Therefore the full-lower-support alternative is impossible. ∎



---

<a id="appendix-k"></a>

## Appendix K. Complete three-square ending: the bottom-face alternative

### 2. Complete local face and angular data

The same forced faces at O,Y and the right origin, already proved from these actual sources in Section 6 of the main proof, give

    U≥0, A≥a>1, U<.26s, V<−.26c<0,
    H≤s, H≤.525s+.125c.

In the present bar alternative,

    V≥.8s−c.

Put

    H0=1+.8s−c>0.

Thus H>H0. The two v faces give

    1<a≤(9/8)c−(11/40)s.

The last expression decreases with q=angle(c,s), and at half-angle7/48 it equals94083/94120<1. Therefore

    0<tan(q/2)<7/48,
    c>c0=2255/2353>239/250,
    0<s<s0=672/2353<143/500.                    (1)

The actual E has right support beyond x=1:

    x_max(E)=cA+sH
      >c+s−cs+.8s²
       =1+s²[.8−(1−s)/(1+c)]>1.                (2)

For the last sign, c> .95 gives (1−s)/(1+c)<20/39<.8.

The actual N,R profile and frame are exactly those in Appendices I and J:

    u_N=(d,−r), v_N=(r,d), d,r>0,
    P≥−r, Q≥.26d, J=P+a≤d−.56r,
    T_N=Q+a≤d+r, Q<.62d,

    p0<p<p1,
    p0=2 atan(13/87), p1=2 atan(11/25),
    d0=3700/3869, r0=1131/3869,
    Hn=d0+r0=4831/3869,
    d>2/3, r<3/4, Hn≤d+r<10/7.                (3)

These are full faces of the same actual N, for both its original canonical signs. In particular q<p0<p by (1).

The downward-right quadrant frame of actual R has

    u_R=(b,−t), v_R=(t,b), b,t≥0, b²+t²=1,
    L<b, K<t,
    b(L+a)+t(K+a)≤2.                            (4)

These are its strict actual origin and genuine right container wall.

Exactly the normal argument in Appendix J, Section 3 applies. Its exclusion of E's u_E uses A>1; its exclusion of R's u_R uses V<0 and x_max(E)>1, now supplied by (2). Its N argument uses only (3), N's strict points (.5,1),(.525,.125), and R's strict points (1,0),(1,.56). Consequently the exhaustive lists are

    E→R: v_E or v_R,
    N→R: u_N or u_R.                            (5)

If R supplies the N separator, it necessarily satisfies

    95b>87t, b>2/3, t<3/4.                      (6)

No lower support from the preceding chapter is used in (1)–(6).

### 3. The southeast projection bounds with only A≥a

Define

    j=ct−sb, k=cb+st>0,

    C(q)=c−s−c²+.8cs,
    D(q)=c+s−cs+.8s²,
    kappa=b C(q)+t D(q).                        (7)

If E→R uses R's axis v_R, then

    K>kappa.                                   (8)

Indeed, for j≥0 the full E support is jA+kH>j+kH0. For j≤0 it is jU+kH; because U<.26s<1, this is also strictly greater than j+kH0. The exact identity

    j+kH0=b C(q)+t D(q)

proves (8), including both relative angle orders. In particular A≥a is sufficient; no F4 exclusion from E has been substituted for its true F4 ownership.

The following uniform bounds will replace the older, stronger southeast-face bounds:

    D(q)>1, C(q)>−.05,                           (9)

    0≤t/b≤1/3 ⇒ kappa>1.09t−.05b,
    t/b≥.3     ⇒ kappa>t−.02b.                  (10)

Here and below a ratio t/b is used only when b>0. To prove (9), use the exact identities

    D−1=s²[.8−(1−s)/(1+c)]>0,
    −C=s(1−.8c)−[c/(1+c)]s².

Equation (1) gives 1−.8c<147/625 and c/(1+c)>.48. Thus

    −C<(147/625)s−.48s²
       ≤7203/250000<1/20.                      (11)

Now put w=t/b. The deficit below the strict-origin projection is

    (t−kappa)/b=−C−w(D−1).                      (12)

At w=1/3 its exact expansion is

    −C−(D−1)/3
      =(4/3)(1−c)+(2/3)s−(7/15)cs−(19/15)s².

Using 1/(1+c)<64/125 and s<143/500,

    −C−(D−1)/3
      <.2s−(73/125)s²+(448/1875)s³
      ≤.2s−(120859/234375)s²
      ≤9375/483436<1/50.                       (13)

The exact last margin is7343/12085900. At w=0, (11) gives a deficit less than .05. For fixed q the deficit in (12), minus(.05−.09w), is affine in w. Its negative values at0 and1/3 prove the first assertion of (10) on the complete interval.

For the second assertion, D>1 makes the deficit decrease with w. At w=.3, its exact expansion gives

    −C−.3(D−1)
      =1.3(1−c)+.7s−.5cs−1.24s²
      <.2s−(359/625)s²+(32/125)s³
      ≤.2s−(7831/15625)s²
      ≤625/31324<1/50.                         (14)

Its exact final margin is37/783100. This proves (10) for every allowed q and right-frame angle, without angle sampling.

The b=0 endpoint in an R-axis E separator is impossible: (8) would give K>D>1=t. We therefore have b>0 whenever (8) is used. We do not claim that such a separator forces theta<pi/4.

### 4. R supplies the northeast separator

The northeast estimates in Appendices I and J use only the actual N profile and R cone, so apply unchanged:

    theta≤p0 ⇒ L>b A*+t B*,
    L>1−t throughout the cone (6),              (15)

where

    A*=15594461/14969161,
    B*=−14778022/14969161,
    1.04<A*<1.05, −1<B*<−.98.

First we show that either E separator in (5) gives K>kappa.

If R supplies that separator, (8) already does so. Otherwise E's own separator is

    H≤−jL+kK−a max(j,0).

Using H>H0 and a>1 yields the exact strict comparison

    k(K−kappa)>j[L−k+jH0]+max(j,0).              (16)

The N-owned point Y and its u_R separator, together with (6), give

    L>.525b−.125t>1/4.

For j≥0 the right side of (16) is nonnegative because L+1−k+jH0>0. If j<0, then theta<q, k≥c and |j|≤s. The half-angle bound (1) gives H0−s=1−c−.2s<0. Consequently

    k−jH0−b
      =k(1−c)−j(1−c−.2s)
      ≥(c+s)(1−c)−.2s²
       =s²[(c+s)/(1+c)−.2]>0.                 (17)

Since L<b, the bracket L−k+jH0 in (16) is negative, making its product with j<0 positive. The equality j=0 retains strictness from H>H0. Thus in both cases

    K>kappa.                                   (18)

### 4.1. The interval theta≤p0

Here t/b≤r0/d0<1/3. Equations (10),(15),(18) and the genuine wall force

    2>b+t+A*b²+(B*−.05)bt+1.09t².               (19)

Subtract2 from the right side, obtaining f(theta). Its derivative satisfies

    f'<(b−t)+.10bt−1.03(b²−t²)
       =−.03(b−t)
          +bt[.10−2.06(b−t)/(b+t+1)]<0.

The final sign holds on the entire interval because b−t≥d0−r0>.66 and b+t+1≤Hn+1<2.25. Thus f is minimized at p0. Its exact endpoint is

    f(p0)
      =(1−d0)(Hn−1)+.09r0²−.05d0r0
       =6846749/1496916100>0.                  (20)

This contradicts (19).

### 4.2. The interval theta≥p0

Now t/b>.3, so K>t−.02b. With L>1−t, the genuine wall has left side strictly greater than

    b(2−t)+t(1+t−.02b).

Its excess over2 is

    (1−b)(b+t−1)−.02bt
      ≥t[(13/87)(Hn−1)−.02]>0.                (21)

For theta≤pi/4 the bound b+t≥Hn is monotonicity. Above pi/4, (6) gives b+t>2/3+.7>Hn. The exact bracket in (21) is288697/16830150>0. This excludes every remaining angle in the actual R-axis N cone.

Thus both combinations with R supplying the N separator have been excluded.

### 5. N supplies its axis and R supplies the E separator

Put

    delta=db+rt>0, h=rb−dt.

The N separator is

    J≤delta L−hK−a max(h,0),                    (22)

with J≥a−r. We have K>kappa from (8).

### 5.1. The interval p0≤theta≤pi/4

Equation (10) gives K>t−.02b>0. If h≥0, (22) implies

    delta L>1−r+h.

The identity

    1−r+h−delta(1−t)=1−delta+h(1−b)≥0

gives L>1−t. If h≤0, the strict origin K<t instead gives

    delta L>1−r+ht,
    1−r+ht−delta(1−t)=1−delta+h(t−b)≥0,

because t≤b. Again L>1−t. The real wall now contradicts exactly (21). The common h=0 endpoint is included.

### 5.2. The interval theta≤p0

Here h≥0, since p≥p0≥theta. Let Delta=p−theta. The full N inequality gives

    L>sec Delta−t+(1+K−b)tan Delta.              (23)

For fixed actual R, its right side increases with p. Its derivative has numerator sin Delta+1+K−b, and by (9),(10),

    sin Delta+1+K−b
      >1+(r0−1.05)b+(1−d0)t
      ≥r0−.05>0.

Thus p may be replaced by p0 in (23). Combining this lower bound with the genuine wall and K>1.09t−.05b gives the necessary inequality F(theta)<0, where the exact expanded numerator is

    F(theta)
      =d0b²+r0bt+r0
        +(1−2d0−1.05r0)b−.91r0t.               (24)

It is strictly concave on [0,p0]. Indeed

    F''=−2d0(b²−t²)−4r0bt
           +(2d0+1.05r0−1)b+.91r0t
       <−2(.95)(.82)+1.315+.0819
        =−.1611<0.

Its exact endpoint values are

    F(0)=2249/77380>0,
    F(p0)=6846749/1496916100>0.                 (25)

Concavity proves F>0 throughout, contradicting (24).

### 5.3. Every right angle theta≥pi/4

This interval must be treated because the weaker present southeast faces do not supply the old restriction theta<pi/4. Equation (9) already excluded b=0, so take b>0 and extend the scalar expressions continuously to theta=pi/2 only for their endpoint estimates.

Equation (10) gives K>t−.02b. Combine b times the N inequality in (22) with delta times the genuine wall. The identity b h+t delta=r and a>1 give the necessary inequality

    delta(b+t−2)+b(1−r)+r(t−.02b)
        +b max(h,0)<0.

Drop the nonnegative final term and divide by b. The resulting expression is

    Z(theta)
      =1−2d−1.02r+(d−r)b+(d+r)t
                    +r(1−t)/b.                (26)

For fixed actual p, its exact second derivative is

    Z''=−d(b+t)+r[b−t+b/(1+t)²].

Since b≤t in this interval,

    Z''≤−d(b+t)+rb≤(r−2d)b<0

away from its final endpoint; the exact endpoint derivative is negative too. Thus Z is concave on the entire closed interval [pi/4,pi/2], using the continuous extension (1−t)/b→0.

At its first endpoint,

    Z(pi/4)
      =1−(2−√2)(d+r)−.02r
      >3−2√2−3/200
      >179/1400>0.

Here d+r≤√2, r<3/4 and √2<10/7. At its final endpoint,

    Z(pi/2)=1−d−.02r
      ≥1−d0−.02r0
       =7319/193450>0.                         (27)

The function d+.02r decreases with p on (3), since its derivative is −r+.02d<0. These two endpoint bounds prove Z>0 throughout, contradicting (26). This completes the third separator combination with every large right angle retained.

### 6. Both neighbors supply their own axes

Only the two inequalities

    H≤−jL+kK−a max(j,0),
    J≤delta L−hK−a max(h,0)                    (28)

remain. Put D0=cd+sr>0. Multiplying by r,c respectively, and using

    c delta−r j=D0 b,
    −c h+r k=D0 t,

the genuine wall, J≥a−r, and H≥a+.8s−c give the necessary inequality

    F(theta)<0,

where

    F(theta)=D0(b+t−2)+c+r−2cr+.8rs
                 +c max(h,0)+r max(j,0).        (29)

This is exactly the local scalar obstruction in the complete endpoint argument at the end of this appendix. That section uses only H≥a+.8s−c, J≥a−r, the same actual real right wall, the unified N range (3), and the southeast range (1). It uses neither a lower bound U≥.26s nor F4 exclusion or F8 ownership. Its reuse therefore has precisely the present actual inputs.

For completeness, its all-domain structure and endpoint margins are as follows. Since q<p0<p, the three complete intervals are [0,q],[q,p],[p,pi/2]. The respective positive coefficients of b,t in (29) are

    c(d+r)+sr, sr;
    c(d+r), r(c+s);
    cd, c(d+r)+sr.

Thus F is concave on each interval. The outer endpoints are

    F(0)=F(pi/2)
      =r[c tan(p/2)+(1−c)−.2s]>0.

The endpoint proof below differentiates the exact q and p endpoint expressions over the full parameter rectangle (1),(3). Their minima occur at c=c0,s=s0,d=d0,r=r0, where

    F(q)≥842514839/107105701105>0,
    F(p)≥106787119/13547090705>0.

Those endpoint formulas, derivatives and rational evaluations are unchanged in the present (29). Therefore F(theta)>0 over the complete right quadrant, contradicting (29). This excludes the fourth separator combination.



### 6.1. Full endpoint proof for the last separator combination

We prove that the residual F in (29) is positive on the whole right quadrant. Because q<p, its three intervals are[0,q],[q,p],[p,pi/2]. On each interval it is a positive linear combination of cos theta and sin theta plus a constant:

| Interval | Coefficient of b | Coefficient of t |
|---|---:|---:|
| 0≤theta≤q | c(d+r)+sr | sr |
| q≤theta≤p | c(d+r) | r(c+s) |
| p≤theta≤pi/2 | cd | c(d+r)+sr |

All coefficients are positive. Thus F is strictly concave on each of the three complete intervals. It suffices to check theta=0,q,p,pi/2.

The two outer endpoints coincide:

    F(0)=F(pi/2)
      =c(1−d)+r(1−c−.2s)
      =r[c tan(p/2)+(1−c)−.2s]>0.                  (43)

For example c>.95, tan(p/2)>h0>.14, and s<.3 bound the brackets below by .133−.06>0.

At theta=q the exact expression is

    Fq=c−c(2−c)d+r[2+cs−2c−1.2s].                 (44)

It increases with p on the whole interval (6). Writing Bq=2(1−c)+s(c−1.2), its p derivative is

    c(2−c)r+Bq d>.95(.29)−.075>0.

At the lower endpoint p0 it decreases with q. Its q derivative is

    −s+2d0s(1−c)
      +r0[2s+1−2s²−1.2c]
      <−.9s+.6s−.14(.29)<0.                       (45)

Consequently its minimum on the enlarged closed parameter rectangle is at c=c0,s=s0,d=d0,r=r0. Direct rational substitution gives

    Fq≥842514839/107105701105>0.                    (46)

At theta=p the exact expression is

    Fp=c[2−2d−2r+dr]+s[r²−1.2r]+r.                (47)

It decreases with q. To verify this, put H=d+r. The first bracket is negative and its negative is

    2(H−1)−dr=dr[4/(H+1)−1]≤dr.

Therefore its q derivative is at most

    sdr−cr(1.2−r)<r[.3−.95(.45)]<0.               (48)

It also increases with p. The exact derivative is

    d−c(d−r)(2−H)+sd(2r−1.2).                     (49)

If d≥r, use H≥Hn>1.24, d>.7, r>.29, and s<.3. The first two terms exceed .24d+.76r>.3884, while the last is greater than−.36. Thus (49) is positive. If d<r, then its middle term is positive and2r−1.2>0, so (49) is positive directly.

The minimum of (47) is consequently at the same rational endpoints, where

    Fp≥106787119/13547090705>0.                     (50)

Equations (43),(46),(50) prove positivity at all four endpoints. The three concavity statements then give F(theta)>0 everywhere on[0,pi/2], contradicting the necessary strict negative residual. This excludes the last separator combination.

Thus the face alternative V≥.8s−c is impossible as well. Together with Appendix J this proves the complete three-square contradiction. ∎



---

<a id="appendix-l"></a>

## Appendix L. Single-file exact finite and rational verification

This optional Python 3 checker uses only the standard library. It recomputes the finite entrance and the exact checks described in Section 8. It is not a proof checker for the real-variable geometric arguments.

```python
#!/usr/bin/env python3
"""C580: exact finite reconstruction and specified arithmetic/map checks.

The geometric soundness and continuous lemmas are proved in the Markdown.
This script is not a general proof checker. It requires only Python 3.10+
and its standard library. It writes no files and has no network dependency.
Checks remain active with python -O.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations, product
from fractions import Fraction as Rat
import json

P = tuple[int,int]
MARKERS: tuple[P,...] = ((1000,914),(914,1000),(3000,914),(3086,1000),
 (3000,3086),(3086,3000),(1000,3086),(914,3000),(1650,1650),
 (2350,1650),(2350,2350),(1650,2350),(914,2000),(2000,914),
 (3086,2000),(2000,3086))
F: tuple[P,...] = ((1000,1740),(1000,2260),(1600,1000),(1600,3000),
 (2000,1740),(2000,2260),(2400,1000),(2400,3000),(3000,1740),(3000,2260))
G: tuple[P,...] = tuple(sorted((y,x) for x,y in F))
AUX = F+G
GROUPS = ((0,),(1,),(3,),(4,5),(6,7),(9,),(10,),(8,11),(12,),(13,),(14,),(15,))
BASE = ((1000,914),(1120,1000),(1740,1000),(1870,760))
SEEDS = (BASE, tuple((y,x) for x,y in BASE),
 tuple((4000-y,x) for x,y in BASE),
 ((3000,3086),(3086,3000),(3000,3000)),
 ((1000,3086),(914,3000),(1000,3000)),
 (MARKERS[9],),(MARKERS[10],),(MARKERS[8],MARKERS[11]),
 (MARKERS[12],),(MARKERS[13],),(MARKERS[14],),(MARKERS[15],))
PAIRS_F = ((0,1),(2,3),(4,5),(6,7),(8,11),(9,10))
PAIRS_G = ((0,1),(2,3),(4,5),(6,7),(8,9),(10,11))

def cross(a:P,b:P,c:P)->int:
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def dot_at(p:P,q:P,a:P)->int:
    return (p[0]-a[0])*(q[0]-a[0])+(p[1]-a[1])*(q[1]-a[1])

def hull(points:tuple[P,...])->tuple[P,...]:
    ps=sorted(set(points))
    if len(ps)<2: return tuple(ps)
    lo=[]; hi=[]
    for p in ps:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(ps):
        while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    return tuple(lo[:-1]+hi[:-1])

def in_hull(p:P,h:tuple[P,...])->bool:
    if len(h)==1:return p==h[0]
    if len(h)==2:
        a,b=h
        return cross(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
    return bool(h) and all(cross(a,h[(j+1)%len(h)],p)>=0 for j,a in enumerate(h))

def sym(p:P,swap:bool,rx:bool,ry:bool)->P:
    x,y=p
    if swap:x,y=y,x
    return (4000-x if rx else x,4000-y if ry else y)

PATTERNS=[]
for inside,outside in [
 (((1650,1650),(1000,2260)),((1000,1740),(1650,2350),(2000,1740))),
 (((1650,1650),(2000,2260)),((1000,1740),(1650,2350),(2000,1740))),
 (((914,2000),(1000,1740),(1740,2000)),((1000,1600),(1000,2400),(1650,1650)))]:
    for args in product((False,True),repeat=3):
        PATTERNS.append((tuple(sym(p,*args) for p in inside), frozenset(sym(p,*args) for p in outside)))

@lru_cache(maxsize=None)
def four_block(a:P,b:P,outs:tuple[P,...])->bool:
    for p,q in combinations(outs,2):
        if (p[0]-q[0])**2+(p[1]-q[1])**2>=1000**2:continue
        if dot_at(p,q,a)<=0 or dot_at(p,q,b)<=0:continue
        if cross(a,b,p)*cross(a,b,q)<0 and cross(p,q,a)*cross(p,q,b)<0:return True
    return False

def allowed(i:int,mask:int,S:tuple[P,...],offset:int=0)->bool:
    inside=SEEDS[i]+tuple(p for j,p in enumerate(S) if mask&(1<<(offset+j)))
    h=hull(inside)
    out=tuple(p for j,p in enumerate(MARKERS) if j not in GROUPS[i])+tuple(p for j,p in enumerate(S) if not(mask&(1<<(offset+j))))
    if any(in_hull(p,h) for p in out):return False
    outset=set(out)
    if any(excl<=outset and all(in_hull(p,h) for p in own) for own,excl in PATTERNS):return False
    return not any(four_block(a,b,tuple(sorted(out))) for a,b in combinations(h,2))

def count_budget(groups,pairs):
    exceptional=[any(set(pair)<=set(g) for pair in pairs) for g in groups]
    e=sum(exceptional)
    if e<2:raise ValueError('No packing can meet the covering budget.')
    return exceptional,e-2

def build_components():
    local=[];stats=[]
    for i in range(12):
        choices=[]
        for S,offset,pairs in ((F,0,PAIRS_F),(G,10,PAIRS_G)):
            exc,sigma=count_budget(GROUPS,pairs)
            low=0 if exc[i] else 1
            mandatory=sum(1<<(offset+j) for j,p in enumerate(S) if in_hull(p,hull(SEEDS[i])))
            candidates=[]
            for k in range(low,low+sigma+1):
                for subset in combinations(range(10),k):
                    m=sum(1<<(offset+j) for j in subset)
                    if m&mandatory==mandatory and allowed(i,m,S,offset):candidates.append(m)
            choices.append(candidates)
        both=sorted({a|b for a,b in product(*choices) if allowed(i,a|b,AUX)})
        stats.append({'owner':i,'F_count':len(choices[0]),'G_count':len(choices[1]),'combined_before_deletion':len(both)})
        local.append(both)
    passes=[]
    while True:
        removed=0
        for i in range(12):
            if not local[i]:raise ValueError(f'Empty owner {i} before final table.')
            common=(1<<20)-1
            for m in local[i]:common&=m
            for j in range(12):
                if j!=i:
                    old=len(local[j]);local[j]=[m for m in local[j] if not(m&common)]
                    removed+=old-len(local[j])
        passes.append(removed)
        if not removed:break
    return local,stats,passes

def tuples_of(local):
    out=[]
    def visit(i,used,row):
        if i==12:out.append(tuple(row));return
        for m in local[i]:
            if not(m&used):visit(i+1,used|m,row+[m])
    visit(0,0,[])
    return out


EXPECTED = [
 [4100],[1025],[262400],[0,128],[0],[65552,65584],
 [131104,131200,131232],[8192,8224],[2050],[32832],
 [524800,524928],[16392,16424]]
VARIABLE = [
 (0,65552,131104,8192,524800,16392),
 (0,65552,131104,8192,524928,16392),
 (0,65552,131200,8192,524800,16392),
 (0,65552,131200,8192,524800,16424),
 (0,65552,131200,8224,524800,16392),
 (0,65552,131232,8192,524800,16392),
 (0,65584,131200,8192,524800,16392),
 (128,65552,131104,8192,524800,16392)]
TARGET = (4100,1025,262400,0,0,65552,131200,8224,2050,32832,524800,16392)
COUNTS = {'rational_checks':0,'point_maps':0,'isometries':0,'polynomial_identities':0}

def require(ok, message):
    if not ok: raise ValueError(message)

def rational(name, actual, expected=None):
    if expected is None: require(actual>0,name)
    else: require(actual==expected,name)
    COUNTS['rational_checks'] += 1

def fp(x): return Rat(str(x))
def point(x,y): return (fp(x),fp(y))

def map_points(name, matrix, shift, pairs):
    for i in range(2):
        for j in range(2):
            require(sum(matrix[k][i]*matrix[k][j] for k in range(2))==(i==j),
                    name+': not an isometry')
    COUNTS['isometries'] += 1
    for source, target in pairs:
        got=tuple(sum(matrix[i][j]*source[j] for j in range(2))+shift[i] for i in range(2))
        require(got==target,name+': wrong point map')
        COUNTS['point_maps'] += 1

def mapped(name, matrix, shift, raw):
    map_points(name,matrix,point(*shift),[(point(*a),point(*b)) for a,b in raw])

### A small exact multivariate polynomial implementation. Variables are
### c,s,d,r,b,t. Unit reduction uses c²=1-s², d²=1-r², b²=1-t².
class Poly:
    def __init__(self, terms=None): self.terms={k:Rat(v) for k,v in (terms or {}).items() if v}
    @staticmethod
    def scalar(x): return x if isinstance(x,Poly) else Poly({(0,)*6:Rat(x)})
    @staticmethod
    def variable(i):
        k=[0]*6;k[i]=1;return Poly({tuple(k):Rat(1)})
    def __add__(self, other):
        other=Poly.scalar(other);out=dict(self.terms)
        for k,v in other.terms.items():out[k]=out.get(k,Rat(0))+v
        return Poly(out)
    __radd__=__add__
    def __neg__(self): return Poly({k:-v for k,v in self.terms.items()})
    def __sub__(self,other): return self+-Poly.scalar(other)
    def __rsub__(self,other): return Poly.scalar(other)+-self
    def __mul__(self,other):
        other=Poly.scalar(other);out={}
        for k,v in self.terms.items():
            for l,w in other.terms.items():
                m=tuple(a+b for a,b in zip(k,l));out[m]=out.get(m,Rat(0))+v*w
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly.scalar(1)
        for _ in range(n):out=out*self
        return out
    def reduced(self):
        todo=list(self.terms.items());out={}
        while todo:
            k,v=todo.pop()
            i=next((i for i in (0,2,4) if k[i]>=2),None)
            if i is None:out[k]=out.get(k,Rat(0))+v;continue
            j=list(k);j[i]-=2;todo.append((tuple(j),v))
            j[i+1]+=2;todo.append((tuple(j),-v))
        return {k:v for k,v in out.items() if v}

def identity(name, expr):
    require(not expr.reduced(),name+': polynomial identity')
    COUNTS['polynomial_identities'] += 1

def polynomial_checks():
    c,s,d,r,b,t=[Poly.variable(i) for i in range(6)]
    j=c*t-s*b;k=c*b+s*t;delta=d*b+r*t;h=r*b-d*t;D=c*d+s*r
    identity('first positive multiplier',c*delta-r*j-D*b)
    identity('second positive multiplier',-c*h+r*k-D*t)
    identity('N-wall elimination',b*h+t*delta-r)
    identity('rotated unit j,k',j*j+k*k-1)
    identity('rotated unit delta,h',delta*delta+h*h-1)
    C=c-s-c*c+fp('.8')*c*s
    DD=c+s-c*s+fp('.8')*s*s
    H0=1+fp('.8')*s-c
    identity('E support projection',j+k*H0-(b*C+t*DD))
    identity('strict x support gap',(1+c)*(DD-1)-s*s*(fp('.8')*(1+c)-(1-s)))
    identity('support deficit',(1+c)*(-C)-(1+c)*s*(1-fp('.8')*c)+c*s*s)
    identity('relative support bound',k-j*H0-b-(k*(1-c)-j*(1-c-fp('.2')*s)))
    identity('N parallel comparison',1-r+h-delta*(1-t)-(1-delta+h*(1-b)))
    identity('N reverse comparison',1-r+h*t-delta*(1-t)-(1-delta+h*(t-b)))
    identity('full-support residual at alignment',
             b*(b*(2-t)+2*t-2)+t*(t-1)-(1-b)**2*(1-t))
    # The previous identity is b times equation (19) in Appendix J.
    # Two exact algebraic endpoint formulas for the face alternative.
    base=c+r-2*c*r+fp('.8')*r*s
    Fq=D*(c+s-2)+base+c*(r*c-d*s)
    Fp=D*(d+r-2)+base+r*(c*r-s*d)
    identity('face residual at q',Fq-(c-c*(2-c)*d+r*(2+c*s-2*c-fp('1.2')*s)))
    identity('face residual at p',Fp-(c*(2-2*d-2*r+d*r)+s*(r*r-fp('1.2')*r)+r))

def scalar_checks():
    c=Rat(2255,2353);s=Rat(672,2353);d=Rat(3700,3869);r=Rat(1131,3869)
    rational('E rational unit',c*c+s*s,Rat(1))
    rational('N rational unit',d*d+r*r,Rat(1))
    rational('E half-angle',s/(1+c),Rat(7,48))
    rational('N half-angle',r/(1+d),Rat(13,87))
    rational('upper p rational unit',Rat(252,373)**2+Rat(275,373)**2,Rat(1))
    rational('bar-angle endpoint',Rat(9,8)*c-Rat(11,40)*s,Rat(94083,94120))
    rational('bar-angle endpoint less than one',1-Rat(94083,94120))
    A=d+r-Rat(37,50)*d*r;BB=r-d-Rat(13,50)-Rat(37,50)*r*r
    CC=d-Rat(19,50)*d*r;DD=r-Rat(31,50)-Rat(19,50)*r*r
    for name,act,exp in [('A*',A,Rat(15594461,14969161)),
                         ('B*',BB,-Rat(14778022,14969161)),
                         ('C*',CC,Rat(12725114,14969161)),
                         ('D*',DD,-Rat(5391122,14969161))]:rational(name,act,exp)
    fq=c-c*(2-c)*d+r*(2+c*s-2*c-Rat(6,5)*s)
    fp_=c*(2-2*d-2*r+d*r)+s*(r*r-Rat(6,5)*r)+r
    rational('foreign q endpoint',fq,Rat(842514839,107105701105))
    rational('foreign p endpoint',fp_,Rat(106787119,13547090705))
    rational('foreign q positive',fq);rational('foreign p positive',fp_)
    rational('shallow face endpoint',(1-d)*(d+r-1)+Rat(9,100)*r*r-Rat(1,20)*d*r,
             Rat(6846749,1496916100))
    rational('large-angle face endpoint',1-d-Rat(1,50)*r,Rat(7319,193450))
    rational('wall margin',Rat(13,87)*(d+r-1)-Rat(1,50),Rat(288697,16830150))
    rational('mixed-zero endpoint',1-d-Rat(1,20)*r,Rat(2249,77380))
    rational('N projection margin',(8*CC+9*(DD+1))**2-145,
             Rat(2854238647278624,224075781043921))
    z=Rat(2,5)
    p=lambda z:17*z**6+8*z**5-5*z**4-8*z**3-5*z**2+1
    rational('large-angle polynomial endpoint',p(z),-Rat(4507,15625))
    rational('large-angle derivative cap',102*Rat(11,20)**4+40*Rat(11,20)**3-24*Rat(2,5)-10,
             -Rat(288909,80000))
    for name,value in [
        ('shortbar norm1',1-Rat(95,100)**2-Rat(21,100)**2),
        ('shortbar norm2',1-Rat(65,100)**2-Rat(74,100)**2),
        ('shortbar norm3',1-Rat(30,100)**2-Rat(95,100)**2),
        ('shortbar quadratic remainder',Rat(13,560)),
        ('merged upper norm',2-Rat(136,100)**2),
        ('merged wall bound',2*500**2-673**2),
        ('merged target gap',1-Rat(1903,1985)),
        ('sharp-point squared margin',1-Rat(475,1000)**2-Rat(875,1000)**2),
        ('sharp-point halfangle margin',1-Rat(14917,14920)),
        ('top-left target margin',1-Rat(9269,9325)),
        ('wall norm1',1-Rat(24,100)**2-Rat(93,100)**2),
        ('wall norm2',1-Rat(65,100)**2-Rat(61,100)**2),
        ('wall quadratic low',Rat(1,44)),
        ('wall quadratic high',Rat(17,400)),
        ('support shallow error',Rat(1,20)-Rat(35,100)**2*Rat(65,100)/(Rat(93,100)*Rat(193,100))),
        ('support sine error',Rat(962,3869)-Rat(91,372))]:rational(name,value)

def coordinate_checks():
    # Each row has both explicit local and physical coordinates. Owner meanings
    # are the actual-owner tables in Sections 3--5, not implicit point relabeling.
    mapped('short bar -> E',((1,0),(0,1)),(2,2),[
        ((.35,-.35),(2.35,1.65)),((0,-.26),(2,1.74)),((.26,0),(2.26,2)),
        ((1,-.26),(3,1.74)),((.26,-1),(2.26,1)),((.35,-1),(2.35,1)),
        ((.05,-.05),(2.05,1.95))])
    mapped('merged near -> W',((-1,0),(0,1)),(2,2),[
        ((.35,-.35),(1.65,1.65)),((.35,.35),(1.65,2.35)),
        ((0,-.26),(2,1.74)),((0,.26),(2,2.26)),((1,-.26),(1,1.74)),
        ((1,.26),(1,2.26)),((1.086,0),(.914,2)),((-.05,-.05),(2.05,1.95))])
    wall=[(.914,2),(1,2.4),(1,1.74),(.76,1.87),(1.65,2.35),(1,2.8)]
    for name,mat,shift,targets in [
        ('left wall',((1,0),(0,1)),(0,0),wall),
        ('bottom wall',((0,1),(1,0)),(0,0),[(2,.914),(2.4,1),(1.74,1),(1.87,.76),(2.35,1.65),(2.8,1)]),
        ('right wall',((-1,0),(0,1)),(4,0),[(3.086,2),(3,2.4),(3,1.74),(3.24,1.87),(2.35,2.35),(3,2.8)])]:
        mapped(name,mat,shift,list(zip(wall,targets)))
    mapped('central crosspoint',((0,1),(-1,0)),(0,4),[
        ((2,2.26),(2.26,2)),((2.26,2),(2,1.74)),((2.35,2.35),(2.35,1.65)),
        ((2.35,1.65),(1.65,1.65)),((1.65,2.35),(2.35,2.35)),
        ((3,2.4),(2.4,1)),((3,2.5),(2.5,1)),((2,2.5),(2.5,2))])
    corner=[(2,.914),(1.6,1),(1,.914),(1,1),(1,1.5),(2,1)]
    mapped('top origin',((1,0),(0,-1)),(0,4),list(zip(corner,
        [(2,3.086),(1.6,3),(1,3.086),(1,3),(1,2.5),(2,3)])))
    mapped('right origin',((0,-1),(-1,0)),(4,4),list(zip(corner,
        [(3.086,2),(3,2.4),(3.086,3),(3,3),(2.5,3),(3,2)])))
    mapped('N top extension',((1,0),(0,1)),(2,2),[
        ((.35,.35),(2.35,2.35)),((.4,1),(2.4,3)),((0,.26),(2,2.26)),
        ((0,1),(2,3)),((.5,0),(2.5,2)),((.5,1),(2.5,3))])
    mapped('N sharp and left',((1,0),(0,1)),(2,2),[
        ((.35,.35),(2.35,2.35)),((.4,1),(2.4,3)),((.26,1),(2.26,3)),
        ((0,.26),(2,2.26)),((0,1),(2,3)),((1,1),(3,3)),
        ((1,.26),(3,2.26)),((1,.56),(3,2.56)),
        ((.525,.125),(2.525,2.125)),((0,.62),(2,2.62))])

def disjoint(row):
    used=0
    for x in row:
        if used&x:return False
        used|=x
    return True

def main():
    require(tuple(sum(1<<j for j in g) for g in GROUPS)==
        (1,2,8,48,192,512,1024,2304,4096,8192,16384,32768),'wrong original family')
    fam,stats,passes=build_components()
    require(fam==EXPECTED,'complete component table differs')
    rows=tuples_of(fam)
    require(len(rows)==8 and all(disjoint(row) for row in rows),'joint catalogue')
    require([tuple(row[j] for j in (3,5,6,7,10,11)) for row in rows]==VARIABLE,
            'complete joint list differs')
    require([row for row in rows if row[7]&(1<<5)]==[TARGET],'F5 filter')
    require(passes==[50,11,0],'consistency deletion passes')
    require(len({512,1024,16384})==3 and all(x in
        [sum(1<<j for j in g) for g in GROUPS] for x in (512,1024,16384)),
        'three distinct actual owners')
    polynomial_checks();scalar_checks();coordinate_checks()
    print(json.dumps({'status':'PASS','scope':'finite entrance and listed exact arithmetic/maps; not Lean',
        'component_labels':sum(map(len,fam)),'joint_assignments':len(rows),
        'after_merged_F5':1,'consistency_deletions':passes,**COUNTS},sort_keys=True))

if __name__=='__main__': main()
```



---

## Source fingerprints

The proof appendices above retain and specialize mathematical arguments from these recovered source texts. They are credited as recovered work, not new discoveries of this continuation. The hashes identify the source bytes before adaptation.

| Source text | SHA-256 |
|---|---|
| `C1092-DIRECT-WALL-POINT.md` | `9c1ab20abe6fc630887b92c0d099c0a44d0f50c9fe44fc9e10a6021893a83e5c` |
| `C893-CONTINUOUS-EXCLUSION.md` | `c7801569040fdb6e332ffe4aa5a09172e40ff174fe57b1629f5396215ddca716` |
| `C974-C976-CENTRAL-CROSSPOINTS.md` | `a2cf3ba21679b1c594ae633337d7f39f9d235512a6a26c2c6ea44e6479f6344d` |
| `C981-WALL-CYCLES.md` | `d2cfc40749324c65d2c298c5c0646a3b6bcbeee9c9001f39c011f0673bfe5cc4` |
| `C983-F4-FULL-8240-ENDING.md` | `5e021913dfb888384256602e04c536a77a9c71dce1f9a0ef68059684a5d1cabf` |
| `C983-F5-INWARD-SIGN.md` | `16d96c7745a47fc7cc2f7fc17c3b930414d0cc7b680236f6f60284f2a5adb48e` |
| `C983-F5-MERGED-CENTER.md` | `af51fa32980902edb713313d716a09c46a771d6c3e4379db9d2f76a3bb9b23e4` |
| `C983-F5-NEGATIVE-BAR-FACE-ENDING.md` | `ef47273e65b9705d4ebcac40316fcd42a3b310d83a6a47968e88a1a566f9e190` |
| `C983-F5-NEGATIVE-LOWER-SUPPORT-ENDING.md` | `e03b603cdf14217a87422eb067e63423ecd8d0731b8551cf1857ff8aaace3c20` |
| `INWARD-SHORT-BAR-POINT.md` | `a7dd47edcfdf534349b70da3c36d47e2ced13b512bfeed6ccb99e22a3508a79f` |
| `OTHER-GEOMETRY.md` | `f059784c3c98ac9b7da4530fec7fce16845bf0804951b6d82f83a8c42d8b9600` |
| `OUTWARD-BAR-AND-UPPER-SPAN.md` | `f8ae8f5bcf43fedf550aa0ea813d785a9c8ebb5067e959bce36269892812d1d1` |
| `TOP-ONLY-LEFT-POINT.md` | `5d37a3d7291ad99572d2e38b2f9c97f30260f78bd7a9618cd0405cf85a3fbffd` |
| `FOUNDATIONAL-ENTRANCE.md` | `1308586f5b140f754221c0c47350a91d52a018b5e8be15e7033eb0f314140f45` |
| `LOCAL-RULE.txt` | `7c6d7514e2acd263eb52e9db2741832c64015b1cf792e34e1ba725ca7e9f6a0e` |
