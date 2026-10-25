# C893: the owned corner marker forces one of two duplicate points

All decimals are exact. Squares are open, their side is a>1, and excluded points may lie on the boundary. The new point theorem below has no container-wall or side-upper-bound hypothesis.

## 1. A six-point theorem with the corner marker owned

**Theorem 1.** Suppose a square Q of side a>1 strictly owns

\[
M=(2.35,2.35),\qquad A=(3,2.26),\qquad H=(3.086,3),
\]

and excludes

\[
G=(2.26,2),\qquad R=(3.086,2),\qquad T=(2.88,3).
\]

Then Q strictly owns at least one of

\[
Z_0=(2.5,2),\qquad Z_1=(2.54,1.99). \tag{1}
\]

The ownership of H is part of the theorem. It is not an exclusion borrowed from a family with different original marker groups.

### 1.1. Negative and zero canonical angles are impossible

Translate by (−2,−2), so the points become

\[
M=(.35,.35),\ A=(1,.26),\ H=(1.086,1),
\quad G=(.26,0),\ R=(1.086,0),\ T=(.88,1).
\]

Use canonical coordinates u=cx−sy,v=sx+cy, with c≥s≥0,c²+s²=1, and strict bands U<u<U+a,V<v<V+a.

The point P=(1,1) is strictly in Q. Its two lower bands follow from M, and its two upper bands follow from H:

\[
u(P)-u(M)=.65(c-s)\ge0,\qquad
v(P)-v(M)=.65(c+s)>0,
\]

\[
u(H)-u(P)=.086c>0,\qquad
v(H)-v(P)=.086s\ge0.
\]

These comparisons give strict bands even when a displayed increment is zero.

The excluded T has both upper bands strictly from P and its lower-v band strictly from M, because v(T)−v(M)=.53s+.65c>0. Hence it fails lower-u:

\[
U\ge.88c-s.
\]

Strict ownership of M then gives

\[
.35c-.35s>.88c-s,\qquad s/c>53/65. \tag{2}
\]

At R, the lower-u band is strict from M, and the upper-v band is strict from P. Its lower-v band is also strict, since

\[
v(R)-v(M)=.736s-.35c>0
\]

by (2). Thus R fails upper-u, giving U+a≤1.086c. The two u-face bounds imply

\[
a\le.206c+s\le\frac{1.206}{\sqrt2}<1,
\]

where .206 cos θ+sin θ increases on the whole canonical interval and 1.206²=1.454436<2. This contradiction excludes this entire sign, including s=0 and the negative diagonal representative.

### 1.2. Positive angles have a short support interval

Now use u=cx+sy,v=−sx+cy with c≥s≥0. The excluded T has a strict upper-u band from H, because u(H)−u(T)=.206c>0. Its lower-u and lower-v bands are strict from M:

\[
u(T)-u(M)=.53c+.65s>0,
\qquad
v(T)-v(M)=.65c-.53s\ge.12c>0.
\]

Consequently

\[
V+a\le c-.88s. \tag{3}
\]

The excluded G has both upper bands strict from M. If it failed lower-v, (3) would give a≤c−.62s≤1. It must therefore fail lower-u:

\[
U\ge.26c. \tag{4}
\]

At R the lower-u band is strict from M and the upper-v band is strict from A. If R failed upper-u, (4) would give a≤.826c<1. Therefore R fails lower-v:

\[
V\ge-1.086s. \tag{5}
\]

Combining (3) and (5),

\[
1<a\le c+.206s. \tag{6}
\]

In particular s>0. Moreover

\[
0<s/c<1/2. \tag{7}
\]

Indeed, c+.206s is decreasing when s/c≥1/2, and at s/c=1/2 its value is 2.206/√5<1, since 2.206²=4.866436<5. That would contradict (6).

### 1.3. One of the two points is strictly owned

Write τ=s/c. If 0<τ<1/20, use Z₀=(.5,0). Its lower-u, upper-u and upper-v bands follow strictly from M,A:

\[
u(Z_0)-u(M)=.15c-.35s>.1325c>0,
\]

\[
u(A)-u(Z_0)=.5c+.26s>0,
\qquad
v(M)-v(Z_0)=.35c+.15s>0.
\]

The remaining lower-v band follows from (3), because

\[
v(T)-v(Z_0)=c-.38s<1<a.
\]

Thus Z₀ is strict in this angular sector.

If τ≥1/20, use Z₁=(.54,−.01). In view of (7), its lower-u band is strict from M:

\[
u(Z_1)-u(M)=.19c-.36s>.01c>0.
\]

Its two upper bands follow from A and M:

\[
u(A)-u(Z_1)=.46c+.27s>0,
\qquad
v(M)-v(Z_1)=.36c+.19s>0.
\]

Finally τ≥1/20 implies s≥1/√401>1/21. Hence

\[
v(T)-v(Z_1)=1.01c-.34s
<1.01-\frac{.34}{21}
=\frac{2087}{2100}<1<a.
\]

Equation (3) supplies the strict lower-v band. Thus Z₁ is strict in this sector, including τ=1/20.

The two sectors exhaust (7). Every excluded-face equality, axial limit, and diagonal representative has been covered. This proves the theorem.

## 2. Retained C893 entrance and exact owner data

The original C893 order is

\[
(1,2,12,16,192,512,1056,2304,4096,8192,16384,32768).
\]

The label families and compulsory strict hulls are retained from `root_next/twenty_one_cases/C893-complete-exclusion.txt`, Sections 2–3, in the original completed package. They use the existing finite local ownership rule. This chapter replaces the subsequent propagated-domain and capacity ending; it does not claim to replace that entrance rule.

Write Aₛ=Q₅ for the southeast central square, N=Q₆ for the northeast square which also owns the original right-top corner marker, W=Q₇ for the merged left-central square, B=Q₉ for the actual bottom-wall square, and Rₛ=Q₁₀ for the actual right-wall square. The top-right singleton is Q₃.

The two possible Aₛ labels, 65552 and 65584, both strictly own

\[
(2.35,1.65),\quad(2,1.74),\quad(2.26,2).
\]

The two possible N labels, 524800 and 524832, both strictly own (3,2.26),(3,2.4). Its exact original mask 1056 supplies both (2.35,2.35) and (3.086,3). Thus the new theorem's data have the following actual sources:

| Theorem datum | Actual owner |
|---|---|
| Strict M=(2.35,2.35) | N's original northeast marker |
| Strict A=(3,2.26) | N's auxiliary 9 |
| Strict H=(3.086,3) | N's original corner marker 5 |
| Excluded G=(2.26,2) | Aₛ's auxiliary 16 |
| Excluded R=(3.086,2) | Rₛ's original wall marker |
| Excluded T=(2.88,3) | Q₃'s compulsory strict singleton hull |

Theorem 1 therefore places at least one of the two points (1) strictly in N. This deduction holds for both possible auxiliary labels and does not distinguish the optional owner of (2,2.26).

## 3. Both points are strictly in the actual southeast square

The inward point theorem and its stronger-point Corollary 3 in `C1084-DUPLICATE-POINT.md` apply directly to Aₛ. Its strict anchors are the three displayed southeast points. Its excluded southwest and northeast markers lie in W and N, respectively, and its excluded point (2.4,1) is strict in B. Hence

\[
Z_1=(2.54,1.99)\in A_s\quad\text{strictly}. \tag{8}
\]

To obtain Z₀, first advance the actual bottom wall. Under x↔y, Theorem 4 of `C981-WALL-CYCLES.md` applies to B's strict (2,.914),(2.4,1). Its three foreign points are (1.74,1),(1.87,.76), both in the actual Q₀ singleton, and (2.35,1.65), the Aₛ marker. The actual bottom wall supplies the wall hypothesis. Therefore B strictly owns (2.8,1), and its strict segment from (2.26,1) to that point contains both

\[
(2.4,1),\qquad(2.5,1). \tag{9}
\]

Now use the retained all-angle central crosspoint lemma from Section 5 of `C981/02_C981_original_points_and_crosspoints.txt` in the original completed package. Its exact statement is: a side-a>1 square owning (2,2.26),(2.26,2),(2.35,2.35), and excluding (2.35,1.65),(1.65,2.35),(3,2.4),(3,2.5), strictly owns (2,2.5). That established lemma is a continuous face proof and uses no container, center, or orientation hypothesis. Its complete short proof is reproduced in the appendix below for independent review.

Apply it to Aₛ under the rotation

\[
(X,Y)=(4-y,x).
\]

Its complete mapping is:

| Crosspoint datum | Original C893 point | Actual source |
|---|---|---|
| Owned (2,2.26) | (2.26,2) | Aₛ |
| Owned (2.26,2) | (2,1.74) | Aₛ |
| Owned (2.35,2.35) | (2.35,1.65) | Aₛ |
| Excluded (2.35,1.65) | (1.65,1.65) | W's original marker |
| Excluded (1.65,2.35) | (2.35,2.35) | N's original marker |
| Excluded (3,2.4) | (2.4,1) | B, by (9) |
| Excluded (3,2.5) | (2.5,1) | B, by (9) |

The strict conclusion (X,Y)=(2,2.5) becomes

\[
Z_0=(2.5,2)\in A_s\quad\text{strictly}. \tag{10}
\]

## 4. Complete continuous exclusion

The new six-point theorem puts either Z₀ or Z₁ strictly in N. Equations (8) and (10) put both points strictly in the distinct actual square Aₛ. In either alternative the two squares have a common strict point, contradicting their disjoint interiors.

**This excludes the entire original C893 family.** The proof preserves N's actual ownership of the corner marker (3.086,3), covers both retained auxiliary labels and every optional auxiliary assignment, and uses only continuous geometric theorems after the retained local ownership entrance. No missing corner point is assigned an owner, no excluded marker is changed into an owned one, and no finite orientation or center enclosure is used in the ending.

## Appendix. Complete retained central crosspoint proof

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
