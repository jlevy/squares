# Task 06 — C581: assembled exclusion and simplified three-square ending

**Task status:** mathematical assembly and the simplifications below completed; **not a Lean acceptance receipt**.  
**Original task:** `06_PENDING_C581.md`.  
**Repository snapshot:** `EvolvingPrograms/SquaresLean`, commit `496092631bc25cde3baec0bcad56c1b1b0a231ad`.  
**Scope:** C581 only. No repository, registry, other task, or other agent's work was modified.

## 1. Result

C581 does not need a new packing search or a second case-specific three-square theorem. Its original-packing entrance and the existing shared terminal have matching hypotheses, including the additional disjointness of the two central squares. Their mathematical composition excludes the exact family

\[
\mathcal F_{581}=
\{1,2,8,48,192,512,1024,2304,4096,8196,16384,32768\}.
\tag{1}
\]

The unique occurrence of original ID 581 in the supplied 577-row cover is row **322**, with exactly this family. Consequently the family exclusion supplies the required exclusion for **every retained row with ID 581**, not merely a selected auxiliary assignment. The row identification was independently checked against source bytes whose Git blob matches the pinned repository file. [S1–S3, S9]

There are three substantive simplifications in this document:

1. **One wall-elimination lemma replaces the separate elimination of the right square's position in all four separating-face combinations.** It keeps that same physical square, its exact side, and its actual wall throughout.
2. **The ordered mixed-angle certificate is reduced from 36 degree-seven nonnegative terms to a cubic in one angular difference.** Monotonicity in the other variable leaves four positive Bernstein coefficients. The new proof gives the explicit stronger bound
   \[
   P(z,w)\ge\frac{64}{250047}>0
   \qquad
   \left(\frac19\le w\le z\le\frac27\right).
   \tag{2}
   \]
   This replaces the polynomial certificate in `NegativeMixedScalars.triangle`; it is proved in full in Section 7.
3. **The shallow right-owned/right-owned ending has a fixed rational wall excess** of at least
   \[
   \frac{34}{8405}>0,
   \tag{3}
   \]
   after applying its two existing support bounds. The other right-owned ending is a single division-free sum of nonnegative terms.

The original-family assembly uses the identified entrance, separating-axis, and analytic support lemmas from the supplied library. Those dependencies are explicit below; this is not a claim to rederive their entire ancestry from elementary geometry in this document. The new wall-elimination, cubic-certificate, and final wall-margin arguments are given here with their proofs. No Lean was written or compiled. The pinned live registry still lists C581 as pending; this document does not assert that a source adapter has been installed or accepted. [S19–S21]

## 2. The exact case: do not replace 8196 by 8192

A normalized packing has twelve actual congruent open square interiors, common side

\[
1<\ell\le\frac{1001}{1000},
\]

contained in the physical box \([0,4]^2\). A code is the exact set of owned markers, encoded as a bit mask. Write \(Q_m\) for the actual square with code \(m\).

For C581, the bottom square is **\(Q_{8196}\)**. Its marker indices are \(\{2,13\}\), because

\[
8196=2^2+2^{13}.
\]

The corresponding square in C580 has code 8192 and owns only marker 13. The two cases can share a parameterized geometric argument, but their exact family equalities cannot be interchanged. The selector used for C581 in `C580581Entrance.family` is **1**. [S2, S3]

The twelve owners in increasing-code order are:

| Code | Marker indices | Geometric role in this proof |
|---:|---|---|
| 1 | 0 | Southwest bottom singleton |
| 2 | 1 | Southwest left singleton |
| 8 | 3 | Southeast right singleton |
| 48 | 4, 5 | Northeast paired corner |
| 192 | 6, 7 | Northwest paired corner |
| 512 | 9 | Southeast central square, later called \(E\) |
| 1024 | 10 | Northeast central square, later called \(N\) |
| 2304 | 8, 11 | One merged left-central square |
| 4096 | 12 | Left wall square |
| 8196 | 2, 13 | Actual C581 bottom square |
| 16384 | 14 | Right wall square, later called \(R\) |
| 32768 | 15 | Top wall square |

These are twelve distinct owners; the merged code 2304 is **one square**, not two freely movable central squares. The codes partition the sixteen marker indices.

Every foreign-point argument below has the form

\[
x\in\operatorname{int}Q_n,\quad m\ne n
\quad\Longrightarrow\quad
x\notin\operatorname{int}Q_m.
\tag{4}
\]

It is not enough that a point is missing from a label. We retain an actual owner whenever a missing point is used to exclude another square.

## 3. The original ownership entrance collapses without a global label search

### 3.1 Ten forced G owners

The certified local domains in `C580581Entrance` give the following possible G indices. Each listed option is a singleton **complete G set** of that owner, not a selected point from an otherwise unspecified G set. For the C581 bottom square, the G5 claim is obtained directly from its seed hull. [S3]

| Owner | Initial G-index choices | Forced index | Reason for eliminating alternatives |
|---:|---|---:|---|
| 1 | 2 | 2 | Singleton local domain |
| 2 | 0 | 0 | Singleton local domain |
| 8 | 8 | 8 | Reflected singleton local domain |
| 2304 | 3 | 3 | Transposed merged-owner domain |
| 8196 | 5 | 5 | Actual bottom seed hull |
| 4096 | 0, 1, 3 | 1 | G0 is owned by 2; G3 by 2304 |
| 512 | 5, 6, 8 | 6 | G5 is owned by 8196; G8 by 8 |
| 16384 | 6, 8, 9 | 9 | G6 is owned by 512; G8 by 8 |
| 1024 | 6, 7, 9 | 7 | G6 is owned by 512; G9 by 16384 |
| 32768 | 4, 7 | 4 | G7 is owned by 1024 |

Thus the complete G ownership is forced by a short dependency chain. It is unnecessary to assume that the packing covers all G points: the ten distinct ownership claims **prove** that it does. In particular, the two remaining corner owners cannot own a G point.

An independent finite audit enumerated the Cartesian product of precisely these displayed choices: **162 candidates, one injective assignment**. This check validates the finite propagation from the displayed domains. It does not replace the upstream geometric proof that an actual owner belongs to its local domain.

### 3.2 Compulsory F points and the merged owner

The combined local domains, conditioned on those exact G sets, give

\[
\begin{array}{c|cccccccc}
\text{owner}&1&2&8&8196&4096&512&16384&32768\\
\hline
\text{owned F index}&2&0&8&6&1&4&9&3
\end{array}
\tag{5}
\]

and the disjunction

\[
F_5\in Q_{1024}\quad\text{or}\quad F_7\in Q_{1024}.
\tag{6}
\]

Here and below, membership of a named point in a square means strict interior membership. For the bottom seed segment from \((9/4,1)\) to \((11/4,1)\), G5 and F6 occur at the exact interpolation parameters \(1/50\) and \(3/10\), respectively. [S4]

The important next step is geometric, not a count that incorrectly forces the F-exempt merged owner to take an F point:

* \(Q_{512}\) owns \((41/20,39/20)\), by the reflected southwest-point lemma and genuine bottom/singleton foreign points.
* Were \(Q_{2304}\) to omit \(F_5=(2,113/50)\), the merged-near-point lemma would force it to own that **same** point \((41/20,39/20)\).
* These are distinct physical squares, a contradiction. Hence \(Q_{2304}\) owns F5, and (6) forces \(Q_{1024}\) to own F7.

The separate merged-center lemma also gives

\[
(2,2)\in Q_{2304}.
\tag{7}
\]

Its hypotheses include the actual left wall square; that square is not deleted or replaced by a few unrelated point constraints. [S5]

After this geometric step, all ten F points also have distinct actual owners. Consequently the full F/G assignment is now exact:

| Owner | Complete F set | Complete G set |
|---:|---|---|
| 1 | \(\{2\}\) | \(\{2\}\) |
| 2 | \(\{0\}\) | \(\{0\}\) |
| 8 | \(\{8\}\) | \(\{8\}\) |
| 48 | \(\varnothing\) | \(\varnothing\) |
| 192 | \(\varnothing\) | \(\varnothing\) |
| 512 | \(\{4\}\) | \(\{6\}\) |
| 1024 | \(\{7\}\) | \(\{7\}\) |
| 2304 | \(\{5\}\) | \(\{3\}\) |
| 4096 | \(\{1\}\) | \(\{1\}\) |
| 8196 | \(\{6\}\) | \(\{5\}\) |
| 16384 | \(\{9\}\) | \(\{9\}\) |
| 32768 | \(\{3\}\) | \(\{4\}\) |

This conclusion is downstream of the merged-owner geometry. It must not be fed back as an assumption in the proof that the merged owner takes F5.

## 4. From the actual packing to three actual squares

### 4.1 The noncircular wall and corner chain

The entrance uses the following consequences of the real owners. The sequence indicates the relevant dependency order, rather than assuming a convenient wall origin at the outset. [S5–S8]

| Consequence | Actual owner and source of the deduction |
|---|---|
| \((14/5,1)\) is owned | Bottom \(Q_{8196}\), from wall advance |
| \((5/2,2)\) is owned | \(Q_{512}\), using the real bottom segment and foreign central markers |
| \((1,14/5)\) is owned | Left wall \(Q_{4096}\), from wall advance |
| \((2,3)\) is owned | Top wall \(Q_{32768}\), using the actual northwest paired corner \(Q_{192}\) and the advanced left wall |
| \((5/2,3)\) is owned | \(Q_{1024}\), using its top-only configuration, the genuine top origin, and the foreign point \((5/2,2)\) |
| \((3,2)\) is owned | Right wall \(Q_{16384}\), using the actual northeast paired corner \(Q_{48}\); \((5/2,3)\) is foreign to that corner |
| \((3,14/5)\) is owned | Right wall \(Q_{16384}\), from wall advance using the southeast singleton and northeast central square |

Strict ownership of the endpoints of a segment by one open square implies strict ownership of the whole closed segment, by convexity of its interior. In particular,

\[
[113/50,14/5]\times\{1\}\subset\operatorname{int}Q_{8196},
\qquad
\{3\}\times[2,14/5]\subset\operatorname{int}Q_{16384}.
\tag{8}
\]

The northeast central square has the further strict points

\[
(101/40,17/8),\qquad (2,131/50),\qquad (5/2,3).
\tag{9}
\]

The first two follow from the upper-bar and top-only-left-point lemmas, respectively. Their foreign inputs are F5 owned by \(Q_{2304}\), the top origin owned by \(Q_{32768}\), the northeast corner point owned by \(Q_{48}\), and the right segment owned by \(Q_{16384}\). [S8]

No step assumes that a singleton owns the southeast corner point \((3,1)\).

### 4.2 Common translation, not independent movement

Use the common physical coordinates

\[
(X,Y)=(x+2,y+2).
\tag{10}
\]

Reindex the faces of each actual square as necessary, without changing its physical set. The resulting frames satisfy

\[
\begin{aligned}
(x,y)\in E&\iff(x+2,y+2)\in Q_{512},\\
(x,y)\in N&\iff(x+2,y+2)\in Q_{1024},\\
(x,y)\in R&\iff(x+2,y+2)\in Q_{16384}.
\end{aligned}
\tag{11}
\]

Therefore they have the same side \(\ell\), and **all three** pairs \((E,N),(E,R),(N,R)\) have disjoint open interiors. Face reindexing here is not a separate spatial rotation of any square.

The southeast sign is derived, not imposed. The nonnegative canonical sign contradicts the actual merged owner's marker, center, and inward point together with the actual bottom bar and southeast singleton. Thus the southeast frame has normal \((c,-t)\) with \(c>0\) and \(0<t\le c\). The northeast top-only frame has normal \((d,-r)\) with \(d,r>0\); **no ordering between \(d\) and \(r\) is assumed**. The right frame has normal \((a,-b)\), where \(a>0\), \(b\ge0\), again without an artificial canonical ordering. [S8, S10–S12]

### 4.3 The complete terminal input

For a square with normal \((c,-t)\), write its open bands as

\[
u<cx-ty<u+\ell,
\qquad
v<tx+cy<v+\ell.
\tag{12}
\]

Use subscripts \(E,N,R\) for their lower band coordinates, and put

\[
V=u_E+\ell,\qquad H=v_E+\ell.
\]

The southeast input is

\[
\begin{gathered}
c^2+t^2=1,\quad c>0,\quad 0<t\le c,\quad \ell>1,\\
u_E\ge0,\quad V>1,\quad u_E<\frac{13}{50}c,\quad v_E<0,\\
H\le t,\qquad H\le\frac{21}{40}t+\frac18c,\qquad
v_E\ge\frac{13}{50}t-c,
\end{gathered}
\tag{13}
\]

together with the **two genuine bottom alternatives**

\[
\boxed{
 v_E\ge\frac45t-c
 \quad\text{or}\quad
 -tV+cv_E\ge-1.
}
\tag{14}
\]

Call them B1 and B2. Both must be retained. They arise from omission of the actual bottom-owned segment in (8), not from a sampled pose box. The point inputs include

\[
(7/20,-7/20),\ (13/50,0)\in E.
\tag{15}
\]

The northeast profile is

\[
\begin{gathered}
d^2+r^2=1,\qquad d>0,\ r>0,\\
u_N\ge-r,\qquad v_N\ge\frac{13}{50}d,\\
u_N+\ell\le d-\frac{14}{25}r,\qquad
v_N+\ell\le d+r,
\end{gathered}
\tag{16}
\]

with

\[
(21/40,1/8),\quad(1/2,1),\quad(0,31/50)\in N.
\tag{17}
\]

The right input is

\[
\begin{gathered}
a^2+b^2=1,\qquad a>0,\ b\ge0,\\
(1,0),(1,14/25)\in R,\\
\boxed{W:=a(u_R+\ell)+b(v_R+\ell)\le2.}
\end{gathered}
\tag{18}
\]

The last inequality is the **actual physical right wall**: the rightmost closed vertex of the translated square has \(x\)-coordinate \(W\). It follows from containment by passing the affine wall bound to the closure. It is not a bound on a fictitious independently chosen center. [S10]

The source `RightTripleData.Input` contains the side equalities, (13)–(18), and the E/R and N/R disjointness. Its type does **not** contain E/N disjointness. The entrance supplies that last relation separately, and the shared ending consumes it separately. This is the critical interface check. [S8–S10]

## 5. Exactly four separating-face combinations

Write \(h_Q(n)\) and \(l_Q(n)\) for the upper and lower supports of the closed square \(\overline Q\) in direction \(n\). A legal separator has the weak form

\[
h_A(n)\le l_B(n).
\tag{19}
\]

The weak inequality includes legal boundary contact.

For E/R, the actual elbow \((13/50,0)\in E\), the actual origin \((1,0)\in R\), and the upper-right closed vertex of E force a separating direction from E towards R to have **both components positive**. The latter vertex has \(x>1\) and \(y<0\), using both alternatives in (14). Eliminating the other directed face axes from the separating-axis theorem leaves exactly

\[
S_E:\ h_E(t,c)\le l_R(t,c)
\quad\text{or}\quad
S_R:\ h_E(b,a)\le l_R(b,a).
\tag{20}
\]

For N/R, the strict point pairs in (17)–(18) force a forward separating direction \((n_x,n_y)\) to satisfy

\[
n_x>0,\qquad n_y<\frac12n_x,\qquad
\frac{19}{40}n_x+\frac{87}{200}n_y>0.
\tag{21}
\]

The full northeast profile rules out the otherwise possible right-transverse axis. The surviving alternatives are

\[
T_N:\ h_N(d,-r)\le l_R(d,-r)
\quad\text{or}\quad
T_R:\ h_N(a,-b)\le l_R(a,-b).
\tag{22}
\]

These are deductions from complete square disjointness, not guessed incidences. In the \(T_R\) branch, (21) additionally gives

\[
87b<95a,\qquad a>\frac23,\qquad b<\frac34.
\tag{23}
\]

The source reductions were checked at their actual statements and dispatch: `NegativeRightSeparation.separators` and `NegativeTripleNorthSeparation.separators`. [S13, S14]

Crossing the two disjunctions gives four cases, including all equalities at face-choice ties. No fifth geometric configuration or angle grid is needed.

## 6. Simplification I: one determinant wall-elimination lemma

### Lemma 1 — a common physical wall eliminates both position coordinates

Let the actual right square have orthonormal basis

\[
e=(a,-b),\qquad f=(b,a),\qquad a>0,\ b\ge0,
\]

side \(\ell>1\), lower band coordinates \(u,v\), and wall

\[
a(u+\ell)+b(v+\ell)\le2.
\]

Suppose the two selected separating directions are

\[
s=(x,y),\quad n=(z,-w),\qquad
x,w\ge0,\quad y,z>0,
\]

with

\[
h_E(s)\le l_R(s),\qquad h_N(n)\le l_R(n).
\]

Define

\[
D=xw+yz>0,
\]

\[
\mu_s=\min(ax-by,0)+\min(bx+ay,0),
\]

\[
\mu_n=\min(az+bw,0)+\min(bz-aw,0),
\]

and

\[
\Delta=D(a+b)-w\mu_s-y\mu_n.
\]

Then

\[
\boxed{w h_E(s)+y h_N(n)+\ell\Delta\le2D,}
\tag{24}
\]

and, because \(\Delta>0\) and \(\ell>1\),

\[
\boxed{w h_E(s)+y h_N(n)+\Delta-2D<0.}
\tag{25}
\]

**Proof.** Direct minimization over the two closed bands gives, for every direction \(q\),

\[
l_R(q)=(q\cdot e)u+(q\cdot f)v+
\ell\bigl(\min(q\cdot e,0)+\min(q\cdot f,0)\bigr).
\tag{26}
\]

The nonnegative combination of the two directions satisfies

\[
ws+yn=(D,0).
\]

Consequently

\[
w l_R(s)+y l_R(n)
=D(au+bv)+\ell(w\mu_s+y\mu_n).
\]

Add \(\ell\Delta\), apply the two weak separators, and use the actual wall to obtain (24). Finally \(\mu_s,\mu_n\le0\), so

\[
\Delta\ge D(a+b)>0.
\]

Replacing \(\ell\Delta\) by \(\Delta\) is therefore a **strict** weakening, proving (25). This proof also covers \(w=0\); it never divides by a sine or discards a touching configuration. ∎

### The four substitutions

Put

\[
J=cd+tr,\quad Q=ac+bt,\quad A=ad+br,\quad
P=at-bc,\quad B=ar-bd.
\tag{27}
\]

All of \(J,Q,A\) are positive. The complete substitution table is:

| Selected south/north faces | Weight on \(h_E\) | Weight on \(h_N\) | \(D\) | \(\Delta\) |
|---|---:|---:|---|---|
| \(S_E,T_N\) | \(r\) | \(c\) | \(J\) | \(J(a+b)-r\min(P,0)-c\min(-B,0)\) |
| \(S_E,T_R\) | \(b\) | \(c\) | \(Q\) | \(Q(a+b)-b\min(P,0)\) |
| \(S_R,T_N\) | \(r\) | \(a\) | \(A\) | \(A(a+b)+a\max(B,0)\) |
| \(S_R,T_R\) | \(b\) | \(a\) | \(1\) | \(a+b\) |

Thus the position-elimination stage of every branch is one lemma with four literal substitutions. The source's separate wall calculations are instances or weakenings of (24). This refactoring does **not** eliminate the branch-specific support bounds; it eliminates their duplicated use of the right square's two position variables.

## 7. Simplification II: replace the degree-seven mixed-angle certificate by a cubic

This section proves a smaller substitute for the exact polynomial certificate in `NegativeMixedScalars.triangle`. The polynomial and half-angle substitution are inherited; the cubic decomposition, monotonicity reduction, four-coefficient certificate, and explicit margins below are the simplification made here. [S18]

### 7.1 The inherited scalar target

In the ordered \(S_E,T_R\) subcase, the needed scalar expression is

\[
\mathcal R=c(1-b)+b\left(1-\frac{1-t}{c}\right)
-(ac+bt)(2-a-b).
\tag{28}
\]

The available hypotheses are

\[
\begin{gathered}
c^2+t^2=a^2+b^2=1,\quad c,t,a>0,\quad b\ge0,\\
c>\frac67,\qquad b\ge\frac9{41},\qquad bc\le at.
\end{gathered}
\tag{29}
\]

Define the half-angle coordinates

\[
z=\frac{t}{1+c},\qquad w=\frac{b}{1+a}.
\]

They give

\[
c=\frac{1-z^2}{1+z^2},\quad t=\frac{2z}{1+z^2},\quad
 a=\frac{1-w^2}{1+w^2},\quad b=\frac{2w}{1+w^2}.
\tag{30}
\]

The exact domain implications are:

* \(c>6/7\) gives \(z^2<1/13<4/49\), hence \(z<2/7\).
* \(b\ge9/41\) gives \(a\le40/41\), hence \(w\ge(9/41)/(81/41)=1/9\).
* The identity
  \[
  (1+z^2)(1+w^2)(at-bc)=2(z-w)(1+zw)
  \]
  gives \(w\le z\).

In particular, the closed triangle

\[
\frac19\le w\le z\le\frac27
\tag{31}
\]

contains the entire needed domain, including ordering and threshold equalities.

The positive-denominator identity is

\[
(1+w^2)^2(1+z^2)(1+z)\,\mathcal R=P(z,w),
\tag{32}
\]

where

\[
\begin{aligned}
P(z,w)={}&4wz(1+w^2)(1+z^2)\\
&-\bigl((1-w^2)(1-z^2)+4wz\bigr)
  (1-2w+3w^2)(1+z)\\
&+(1-z^2)(1-w)^2(1+w^2)(1+z).
\end{aligned}
\tag{33}
\]

The source proves \(P\ge0\) using 36 positive terms of homogeneous degree seven in the three triangle gaps. That identity is no longer needed for this scalar step.

### 7.2 An exact cubic decomposition

Set \(y=z-w\). Direct expansion gives

\[
\boxed{P(w+y,w)=4w\,Q_w(y),}
\tag{34}
\]

where

\[
Q_w(y)=A_0(w)+A_1(w)y+A_2(w)y^2+A_3(w)y^3
\]

and

\[
\begin{aligned}
A_0(w)&=w^3(1-w)(1+w^2),\\
A_1(w)&=w^2(4-3w)(1+w^2),\\
A_2(w)&=-3w^4+5w^3-2w^2+5w-1,\\
A_3(w)&=1+2w^2-w^3.
\end{aligned}
\tag{35}
\]

Although \(A_2\) need not be positive, **all four coefficients are increasing** on \([1/9,2/7]\). Indeed,

\[
\begin{aligned}
A_0'(w)&=w^2(3-4w+5w^2-6w^3),\\
A_1'(w)&=w(8-9w+16w^2-15w^3),\\
A_2'(w)&=5-4w+15w^2-12w^3,\\
A_3'(w)&=w(4-3w).
\end{aligned}
\tag{36}
\]

Using \(0<w\le2/7\), the bracketed factors in the first two lines, the third line, and the factor \(4-3w\) are bounded below respectively by

\[
\frac{589}{343},\qquad
\frac{1742}{343},\qquad
\frac{1227}{343},\qquad
\frac{22}{7}.
\tag{37}
\]

For example, the first bound follows by dropping \(5w^2\) and bounding \(4w\) and \(6w^3\) by their values at \(2/7\). All bounds are strictly positive.

Since \(y\ge0\), it follows coefficient by coefficient that

\[
Q_w(y)\ge Q_{1/9}(y).
\tag{38}
\]

Also, (31) gives

\[
0\le y\le\frac27-\frac19=\frac{11}{63}.
\tag{39}
\]

Replacing the triangle by this larger rectangle is safe precisely because (38) has been proved on the whole relevant interval.

### 7.3 Four positive coefficients prove the remaining univariate inequality

The left-edge cubic is

\[
Q_{1/9}(y)=
\frac{2}{531441}
\bigl(271917y^3-122958y^2+12177y+328\bigr).
\tag{40}
\]

Set \(\eta=63y/11\), so \(0\le\eta\le1\). The exact identity

\[
\begin{aligned}
Q_{1/9}\left(\frac{11}{63}\eta\right)
={}&\beta_0(1-\eta)^3
+3\beta_1\eta(1-\eta)^2\\
&+3\beta_2\eta^2(1-\eta)
+\beta_3\eta^3
\end{aligned}
\tag{41}
\]

has coefficients

\[
\boxed{
(\beta_0,\beta_1,\beta_2,\beta_3)=
\left(
\frac{656}{531441},
\frac{4838}{1240029},
\frac{200}{107163},
\frac{16}{27783}
\right).
}
\tag{42}
\]

Each coefficient is at least \(16/27783\). The four nonnegative Bernstein weights, including their displayed binomial factors, sum to one. Therefore

\[
Q_{1/9}(y)\ge\frac{16}{27783}
\quad\left(0\le y\le\frac{11}{63}\right).
\tag{43}
\]

Combining (34), (38), and \(w\ge1/9\) proves

\[
\boxed{P(z,w)\ge\frac{64}{250047}>0.}
\tag{44}
\]

This argument is over continuous intervals. The four coefficients are not four sampled angle values.

Finally, throughout (31), the positive denominator in (32) is at most

\[
\left(\frac{53}{49}\right)^3\frac97.
\]

Hence we obtain the stronger version of the source scalar lemma:

\[
\boxed{
\mathcal R\ge
\frac{153664}{976781997}>0.
}
\tag{45}
\]

The original terminal only needs \(\mathcal R\ge0\). Equations (34), (36), (40), (41), and (32) were independently checked by exact symbolic expansion; every comparison in (37), (42)–(45) was checked with rational arithmetic.

## 8. Simplification III: the two right-owned face endings

Suppose both selected separating directions belong to R, namely \(S_R,T_R\).

### 8.1 Universal support floors: one division-free identity

The existing analytic support lemmas give, in the B2 case and in the B1 case with \(b\ge9/41\),

\[
h_N(a,-b)>1-b,
\qquad
h_E(b,a)>1-\frac{1-b}{a}.
\tag{46}
\]

The first bound uses \(b<3/4\), already established from the actual \(T_R\) separator in (23). The second bound retains the correct bottom alternative and applies for either sign of the relative supporting-vertex coefficient. [S17]

The separators imply

\[
u_R>1-b,
\qquad
av_R>a+b-1.
\tag{47}
\]

Using \(a^2+b^2=1\), the following identity is exact:

\[
\begin{aligned}
a(W-2)={}&a^2(u_R+b-1)
+b(av_R-a-b+1)\\
&+a(a+b)(\ell-1)
+(1-b)(1-a)^2.
\end{aligned}
\tag{48}
\]

Every term is nonnegative and the first and third are strictly positive. Here \(0\le b\le1\) follows from the unit equation. Thus \(W>2\), contradicting the real wall (18).

This form introduces no auxiliary quotient, no case split at \(b=0\), and no new geometric assumption. It is an explicit factorization of the inherited universal-floor wall argument.

### 8.2 Shallow first-bottom alternative: a fixed excess

For B1 and \(0\le b\le9/41\), the two source support bounds are instead

\[
h_N(a,-b)>\frac{26}{25}a-b,
\qquad
h_E(b,a)>1+\frac45b-a.
\tag{49}
\]

They imply, using the actual weak separators and \(\ell>1\),

\[
W>
\frac{26}{25}a^2+\frac45b^2-2ab+a+2b.
\tag{50}
\]

The excess of the right-hand side over 2 is

\[
\frac1{25}-(1-a)(1-2b)-\frac6{25}b^2.
\tag{51}
\]

Because \(a^2+b^2=1\), \(a>0\), and \(b\le9/41\), we have

\[
\frac{40}{41}\le a\le1,
\qquad 0\le1-2b\le1.
\]

Consequently (51) is at least

\[
\frac1{25}-\frac1{41}
-\frac6{25}\left(\frac9{41}\right)^2
=\boxed{\frac{34}{8405}}>0.
\tag{52}
\]

Thus the shallow B1 configuration also contradicts the real wall, including the endpoint \(b=9/41\). This replaces the source's separate deficit estimate and small-square estimate by a single explicit rational margin. [S17]

## 9. Joining all four endings without strengthening the entrance

This section records the complete dispatch and the analytic dependencies that remain reused from the shared library. It is important not to present the two simplifications above as though they alone cover the other face combinations.

### 9.1 Both foreign faces: \(S_E,T_N\)

The actual E/N disjointness gives

\[
t<r.
\tag{53}
\]

Here is the logic of the source order lemma. B1 already gives \(t<29/100\), whereas the N profile gives \(r>29/100\). In B2, suppose \(r\le t\). The actual E/N separating-axis reduction leaves their two forward transverse axes. In the E-transverse direction the profile yields

\[
h_E(t,c)=H>c+t-1\ge l_N(t,c),
\]

contradicting that separator. In the N-transverse direction it yields

\[
h_E(r,d)>d+r-1>v_N=l_N(r,d),
\]

again a contradiction. These bounds retain both physical central squares and their side equality. [S15]

The same profile lemmas give \(c>6/7\), \(r<3/4\), and hence \(r<c\). Define

\[
F=J(a+b)-r\min(at-bc,0)-c\min(bd-ar,0).
\]

The exact angular support bound is

\[
F\ge m:=\min(J+cr,cJ+r).
\tag{54}
\]

For clarity, (54) does not arise from an angle grid. As the right normal \((a,b)\) traverses the first quadrant, the formula is linear on the three arcs separated by \((c,t)\) and \((d,r)\). Its values at the four arc endpoints are

\[
J+cr,\quad cJ+r,\quad c+rJ,\quad J+cr.
\]

Also

\[
(c+rJ)-(cJ+r)=(c-r)(1-J)\ge0.
\]

A linear form bounded below by a nonnegative number at the endpoints of an arc shorter than a semicircle has the same lower bound along that unit-circle arc: express an intervening unit vector as a nonnegative combination of the endpoint vectors; the coefficients sum to at least one by the triangle inequality. This proves (54), including its endpoints. [S16]

The source's two endpoint-margin inequalities are

\[
\begin{aligned}
rH+c(1-r)+(J+cr)&>2J,\\
rH+c(1-r)+(cJ+r)&>2J.
\end{aligned}
\tag{55}
\]

Their hypotheses are exactly the profiles (13)–(16), side \(\ell>1\), and (53). The source proves them from B1 using the split \(t\le9/41\) or \(t\ge9/41\), and from B2 using \(cH>c+t-1\). No extra angle hypothesis is inserted. These endpoint scalar lemmas are reused here, not claimed to have been fully rederived in this document. [S16]

Apply Lemma 1 with weights \(r,c\). Since \(h_E(t,c)=H\), \(h_N(d,-r)=u_N+\ell>1-r\), and \(\ell F\ge m\), it gives

\[
rH+c(u_N+\ell)+m\le2J.
\]

But either choice of the minimum in (54), together with (55), makes the left-hand side strictly greater than \(2J\). This excludes \(S_E,T_N\).

### 9.2 Southeast-owned / right-owned: \(S_E,T_R\)

Here Lemma 1 gives

\[
bH+c\,h_N(a,-b)
+\ell\bigl(Q(a+b)-b\min(P,0)\bigr)\le2Q.
\tag{56}
\]

Both bottom alternatives imply

\[
H>\frac45t.
\tag{57}
\]

The complete source split is as follows. [S18, S22]

**Shallow right normal, \(b\le9/41\).** The existing shallow northeast support gives

\[
h_N(a,-b)>U:=\frac{26}{25}a-b.
\]

The shared shallow scalar lemma, with (57), gives

\[
cU+bH-Q(2-a-b)\ge0.
\tag{58}
\]

Since \(-b\min(P,0)\ge0\), (58) and the strict support bound contradict (56).

**Right normal at least as steep, \(P=at-bc\le0\).** The actual E-owned separator can be upgraded to the right-owned transverse separator \(S_R\). The source obtains this by comparing actual support vertices and band endpoints of E and R; it does not replace one square by a surrogate angle. More explicitly, with \(V=u_E+\ell\), the available bounds give

\[
QV+PH<u_R+\ell,
\qquad
H\le P(u_R+\ell)+Qv_R.
\]

Using \(P^2+Q^2=1\), \(Q>0\), and \(P\le0\), these imply

\[
h_E(b,a)=-PV+QH\le v_R.
\]

Now Section 8 applies. The cap \(QV+PH<u_R+\ell\) is the `steeper` comparison in the source; it uses the genuine northeast floor, \(b<3/4\), the E elbow bound, and equal sides. [S22]

**Remaining ordered normal, \(b>9/41\) and \(P>0\).** The unit equations give \(b<t\), so \(t\ge9/41\). Both bottom alternatives then imply

\[
H>1-\frac{1-t}{c}.
\]

Also \(h_N(a,-b)>1-b\), and \(c>6/7\). Section 7 applies to exactly these ordered angles and proves that the expression in (28) is positive. Substituting the two strict floors into (56), where now \(\min(P,0)=0\), gives a contradiction.

This finishes the mixed branch. It is the last subcase above whose 36-term certificate has been replaced by the cubic proof.

### 9.3 Right-owned / northeast-owned: \(S_R,T_N\)

Define the exact residual

\[
\Psi(v)=a(1-r)+rv+(a+b-2)A+a\max(B,0).
\tag{59}
\]

The \(T_N\) separator, the actual wall, and \(\ell>1\) imply

\[
\Psi(v_R)<0.
\tag{60}
\]

For example,

\[
l_R(d,-r)=Au_R-Bv_R-\ell\max(B,0),
\]

The exact identity

\[
A W-a\,l_R(d,-r)
=rv_R+\ell\bigl(A(a+b)+a\max(B,0)\bigr)
\]

then gives (60), because \(l_R(d,-r)\ge u_N+\ell>1-r\), \(W\le2\), and the coefficient of \(\ell\) is positive. This is the same determinant cancellation before replacing the right-owned lower support \(v_R\) by a bound involving E. We do not incorrectly replace the smaller quantity \(h_E(b,a)\) by \(v_R\) in an already established upper-bound inequality.

The actual \(S_R\) separator supplies lower bounds for \(v_R\). In particular, E's upper-right vertex has \(x>1\) and \(y>-1/7\), so

\[
v_R>b-\frac a7.
\tag{61}
\]

The source's continuous scalar bounds are:

\[
\begin{array}{ll}
\Psi(v)\ge0,
&\text{if }b\le9/41,\ r>29/100,\
 v\ge1+\frac45b-a;\\[2mm]
\Psi(v)\ge0,
&\text{if }r<3/4,\ d+r/7<1,\
 v\ge1-\frac{1-b}{a},\ v\ge b-a/7.
\end{array}
\tag{62}
\]

The positive unit equations and \(a,d,r>0,b\ge0\) are understood in (62). The northeast profile supplies \(29/100<r<3/4\) and \(d+r/7<1\). B1 uses the first line when \(b\le9/41\) and the second line otherwise; B2 uses the second line for every right normal. The relevant southeast support floors are precisely those already identified in Section 8, with the \(S_R\) separator transferring them to \(v_R\). [S15, S17, S23]

Thus (62) contradicts (60). The two scalar inequalities in (62) remain inherited analytic lemmas. Their source handles both signs of \(B\) and the steep interval \(b\ge4/5\), so no missing orientation-order assumption is being supplied here.

### 9.4 Both right-owned faces: \(S_R,T_R\)

Section 8 covers B2, B1 with \(b\ge9/41\), and B1 with \(b\le9/41\). The threshold equality is included. This excludes the fourth and final combination.

All four branches now contradict the genuine three-square input. Only the first branch uses the separately supplied E/N disjointness in the terminal's dispatch, although E/N disjointness is also used earlier to justify the southeast sharp-point omission. It has not been dropped at either stage.

## 10. The original-family theorem and retained-row adapter

Assume an actual normalized packing \(p\) has the exact coded family (1).

Apply the C580/C581 entrance with selector **1**. Sections 3–4 identify its outputs as the translated, face-reindexed versions of the actual owners 512, 1024, and 16384. They supply the full `RightTripleData.Input` and the additional E/N disjointness. Sections 5 and 9 exhaust the two E/R and two N/R separating-face alternatives. Every combination is impossible. Therefore no such \(p\) exists.

In the public contract's notation, this proves the mathematical family statement

\[
\operatorname{ExcludesFamily}(\mathcal F_{581}).
\tag{63}
\]

Now let \(q\) be any retained original row with \(q.\mathrm{originalId}=581\). A retained row belongs to the original cover. The exact row audit establishes

\[
\{q\in\mathrm{coverRows}:q.\mathrm{originalId}=581\}
=\{\mathrm{rowAt}(322)\},
\]

and

\[
\mathrm{rowAt}(322).\mathrm{groups}=\mathcal F_{581}.
\tag{64}
\]

Hence \(q.\mathrm{groups}=\mathcal F_{581}\), and (63) excludes it. This is the required mathematical

\[
\boxed{\operatorname{ExcludesCase}(581).}
\tag{65}
\]

The existing source adapter `RowIdentity.family_at` expresses this transfer using retained-ID injectivity. For the paper argument, the independently checked uniqueness of ID 581 in **all 577 rows** is already sufficient. No row-domain list has been zipped against sorted owner codes.

### Source integration boundary

At the pinned commit, `C580581TripleEntrance.entrance` and `NegativeTripleEnd.impossible` are present with the matching interfaces above. However, C581 is absent from both the symbolic and new-case registries and remains in the source assembly's pending set. Therefore this file is a mathematical result and integration specification, not evidence that the repository already exports an accepted unconditional adapter. [S19–S21]

The remaining formal work is specifically: create the original-family/row adapter from these interfaces, replay its complete pinned import closure, inspect the actual axiom output, and register the accepted whole-case contract. The source's `#print axioms` commands are **not** axiom receipts. The old row-classification route also contains inherited `native_decide` sites; none is silently reclassified here as a kernel-only check. No global twelve-square optimality acceptance is claimed.

The new scalar replacement in Section 7 can be substituted for `NegativeMixedScalars.triangle` or its `large` conclusion during that work. The shared theorem can continue to serve C580 and the relevant C983 entrance, but no status for those separate tasks is changed by this document.

## 11. What was actually checked in this task

The following checks were run with exact integers, `fractions.Fraction`, and symbolic polynomial arithmetic. They were run normally and with `python -O`; the respective JSON receipts were byte-identical. The check functions raise exceptions explicitly and do not depend on Python assertions.

**Entrance/data audit — 57 checks.** This authenticated the complete 199,146-byte `CoverData` blob; recovered 577 rows and 117 distinct expected IDs; located the unique C581 at position 322; checked its exact family, twelve codes, marker partition, and bottom bits; regenerated the one injective G assignment from 162 candidates; checked the three distinct terminal owner pairs; checked fourteen common-translation coordinate pairs, the two bottom-seed interpolation weights, and the right-bar subinterval; and checked the wall-balance identities, specialization algebra, shallow margin, and arc endpoint algebra.

**Cubic-certificate audit — 25 positive checks and six negative controls.** This checked the exact factorization (34), all four derivative identities and their positive rational bounds, the left-edge cubic, all four Bernstein lower bounds, the Bernstein identity and partition of unity, the uniform numerator and residual bounds, the half-angle denominator identity, and the ordering/threshold implications. The six deliberately corrupted alternatives were rejected: wrong factor sign, changed cubic coefficient, changed Bernstein coefficient, enlarging the gap interval while retaining its old coefficients, altered denominator, and doubling the claimed minimum. All six were rejected again under optimized Python: twelve rejection events across the two modes.

These checks establish the stated finite calculations and symbolic identities. They do **not** prove the geometric soundness of the inherited local domains, replace the written monotonicity and separator arguments, replay every inherited continuous scalar lemma, or compile any Lean source. Those distinctions are why the status of this file is `DONE_MATH`, not formal acceptance.

### Exact authentication values

```text
Input handoff SHA-256:
e2df3217980c8f4be3b2eca1febc95c87ae309a3d8d1ed2779cb41027ea2edc4

CoverData byte count:
199146

CoverData Git blob SHA-1:
d8fd673715d0d32b05c877bcb633cec2ef5c3f51

CoverData SHA-256:
663a4e43053099d3781da982ca148dfec3402da0ba33a603859f19fa20f5e7f4

C581 original ID / zero-based row:
581 / 322

Mixed numerator lower bound:
64/250047

Mixed scalar residual lower bound:
153664/976781997

Shallow right-wall excess:
34/8405
```

## 12. Pinned source references

All paths below are relative to `projects/n12-refactored/` in `EvolvingPrograms/SquaresLean`, commit

```text
496092631bc25cde3baec0bcad56c1b1b0a231ad
```

The branch was resolved before the audit and subsequent substantive reads were pinned to this immutable commit. A source reference below identifies the proof dependency or source fact being used, not a fresh compilation claim. The new cubic and wall-algebra proofs are contained in Sections 6–8 rather than assumed from these references.

| Ref. | Source path | Git blob SHA-1 |
|---|---|---|
| S1 | `source/S12/CoverData.lean` | `d8fd673715d0d32b05c877bcb633cec2ef5c3f51` |
| S2 | Original task `06_PENDING_C581.md`, retained-row and family specification | SHA-256 above |
| S3 | `Compact/Completion/FiniteCases/C580581Entrance.lean` | `cca93f2e9c0ebfbf43ed1e8dd2c8e2a85177ce70` |
| S4 | `Compact/Completion/FiniteCases/C580581Points.lean` | `813f13249c359414abe2124aec9679b40850dfad` |
| S5 | `Compact/Completion/FiniteCases/C580581CentralEntrance.lean` | `a1b1985a293e2b458a426f28d9299cadb0d76050` |
| S6 | `Compact/Completion/FiniteCases/C580581PilotInputs.lean` | `4e4455c855695ebb7097a12e6781ab75fd18d74a` |
| S7 | `Compact/Completion/FiniteCases/C580581UpperChain.lean` | `4196f3732dd0350d7ea1e78b9759d2b2e4bab228` |
| S8 | `Compact/Completion/FiniteCases/C580581TripleEntrance.lean` | `31e990698278d100f4db83680866a3646b5bbcd4` |
| S9 | `Compact/Assembly/RowIdentity.lean` | `b654acc1caa03ab4ff993c44fc9d1610eb237942` |
| S10 | `Compact/Completion/OtherCases/RightTripleData.lean` | `fca3f9342a24f6046f9cc539a23b31a95c0aec32` |
| S11 | `Compact/Completion/OtherCases/NegativeTripleFaces.lean` | `0d1919dad8e31a1ab1f634f4f2ddda9bab3f664c` |
| S12 | `Compact/Completion/OtherCases/TopOnlyQuadrantProfile.lean` | `92212b7b1c8115b06570b64885b58e57dea9c66e` |
| S13 | `Compact/Completion/OtherCases/C983/NegativeRightSeparation.lean` | `4110bb186223bf7855760c2fe0b871f9aeaaa919` |
| S14 | `Compact/Completion/OtherCases/NegativeTripleNorthSeparation.lean` | `7c512659e269fc5dc4b1ca3ac7d310f383ae2580` |
| S15 | `Compact/Completion/OtherCases/C983/NegativeCentralOrder.lean` | `b17e3a990c89393d1a46822a3999741d7096bf86` |
| S16 | `Compact/Completion/OtherCases/C983/NegativeForeignFaces.lean` | `ce7a5209922cc8b30106e3a8f009f562b30ee6bb` |
| S17 | `Compact/Completion/OtherCases/C983/NegativeRightOwned.lean` | `20ffe8b8fb2482323ca8fd8749e4745078741cf8` |
| S18 | `Compact/Completion/OtherCases/C983/NegativeMixedScalars.lean` | `5840354ad915128463ea698eb9abea26056f7547` |
| S19 | `Compact/Assembly/SymbolicRegistry.lean` | `d844de2ceb5b2f66985811659d6996e71e92dcaf` |
| S20 | `Compact/Assembly/NewCases.lean` | `06e33d2bb7f84f4b66a97526b30c4adcca03a2aa` |
| S21 | `Compact/Assembly/SourceAssembly.lean` | `c621604e5062e546eb838b59a054a0f332dc1749` |
| S22 | `Compact/Completion/OtherCases/C983/NegativeMixedSouth.lean` | `4b9f411a548da08d9d1926a4ecebf2fffff3a784` |
| S23 | `Compact/Completion/OtherCases/C983/NegativeMixedRight.lean` | `a3a3ad2f74a02b32746e10f053af133a592129ca` |
| S24 | `Compact/Completion/OtherCases/C983/NegativeTripleEnd.lean` | `dca4adb742fb8c5860862444cdedcfcd73a3689f` |

The mathematical join is: S3–S8 provide the original entrance; S10–S12 specify its exact profiles; S13–S14 prove the exhaustive face disjunctions; S15–S18 and S22–S23 supply the shared analytic endings; S24 dispatches them; S1 and S9 bind the result to every retained C581 row. Sections 6–8 simplify specified algebraic parts of that join.

## Appendix A. Reproduce the new cubic-certificate audit

The following is the exact arithmetic audit used for the new certificate, including its six deliberately corrupted alternatives. It requires Python and SymPy, uses no network and no floating-point angle sampling, and can be copied from this Markdown file into a script. Its checks remain active under `python -O`.

```python
from __future__ import annotations
import json
from fractions import Fraction as F
import sympy as s

records=[]
def check(name, ok):
    if not bool(ok): raise ValueError(name)
    records.append(name)

z,w,y,h,c,t,a,b=s.symbols('z w y h c t a b')
P=4*w*z*(1+w*w)*(1+z*z)-((1-w*w)*(1-z*z)+4*w*z)*(1-2*w+3*w*w)*(1+z)+(1-z*z)*(1-w)**2*(1+w*w)*(1+z)
coeff=[w**3*(1-w)*(1+w*w), w*w*(4-3*w)*(1+w*w), -3*w**4+5*w**3-2*w*w+5*w-1, 1+2*w*w-w**3]
Q=sum(co*y**k for k,co in enumerate(coeff))
check('cubic_factorization',s.expand(P.subs(z,w+y)-4*w*Q)==0)
diffs=[w*w*(3-4*w+5*w*w-6*w**3), w*(8-9*w+16*w*w-15*w**3),5-4*w+15*w*w-12*w**3,w*(4-3*w)]
for k in range(4):check(f'coefficient_derivative_{k}',s.expand(s.diff(coeff[k],w)-diffs[k])==0)
lo=s.Rational(1,9);hi=s.Rational(2,7);T=s.Rational(11,63)
check('gap_interval',hi-lo==T)
q0=s.factor(Q.subs(w,lo))
check('left_edge_cubic',s.expand(q0-2*(271917*y**3-122958*y*y+12177*y+328)/531441)==0)
betas=[s.Rational(656,531441),s.Rational(4838,1240029),s.Rational(200,107163),s.Rational(16,27783)]
bern=sum(s.binomial(3,k)*betas[k]*h**k*(1-h)**(3-k) for k in range(4))
check('four_term_Bernstein_identity',s.expand(q0.subs(y,T*h)-bern)==0)
for k,v in enumerate(betas):check(f'Bernstein_lower_bound_{k}',v>=betas[3])
check('Bernstein_partition_of_unity',s.expand(sum(s.binomial(3,k)*h**k*(1-h)**(3-k) for k in range(4))-1)==0)
check('uniform_numerator_bound',4*lo*betas[3]==s.Rational(64,250047))
for k,x in enumerate((3-4*hi-6*hi**3,8-9*hi-15*hi**3,5-4*hi-12*hi**3,4-3*hi)):
    check(f'derivative_positive_coefficient_{k}',x>0)
check('derivative_margin_values', [3-4*hi-6*hi**3,8-9*hi-15*hi**3,5-4*hi-12*hi**3,4-3*hi]==[s.Rational(589,343),s.Rational(1742,343),s.Rational(1227,343),s.Rational(22,7)])
sub={c:(1-z*z)/(1+z*z),t:2*z/(1+z*z),a:(1-w*w)/(1+w*w),b:2*w/(1+w*w)}
res=c*(1-b)+b*(1-(1-t)/c)-(a*c+b*t)*(2-a-b)
scale=(1+w*w)**2*(1+z*z)*(1+z)
check('original_residual_numerator_identity',s.cancel((scale*res).subs(sub)-P)==0)
check('height_half_angle_identity',s.cancel((1-(1-t)/c).subs(sub)-2*z/(1+z))==0)
check('ordered_half_angles',s.cancel(((1+z*z)*(1+w*w)*(a*t-b*c)).subs(sub)-2*(z-w)*(1+z*w))==0)
check('cosine_to_z_bound',s.Rational(1,13)<hi**2)
check('right_half_angle_threshold',s.Rational(9,41)/(1+s.Rational(40,41))==lo)
residual_bound=s.factor(s.Rational(64,250047)/((1+hi*hi)**3*(1+hi)))
check('uniform_residual_bound_positive',residual_bound>0)

# Deliberate corruption tests, using the same exact checks.
mutations={
 'wrong_factor_sign': s.expand(P.subs(z,w+y)+4*w*Q)==0,
 'wrong_cubic_coefficient': s.expand(P.subs(z,w+y)-4*w*(Q+y*y))==0,
 'wrong_Bernstein_coefficient': s.expand(q0.subs(y,T*h)-(bern+h*h*(1-h)))==0,
 'enlarged_gap_without_recalculation': s.expand(q0.subs(y,s.Rational(1,5)*h)-bern)==0,
 'wrong_numerator_denominator': s.cancel(((scale+1)*res).subs(sub)-P)==0,
 'claim_twice_minimum': all(v>=2*betas[3] for v in betas)
}
for name,accepted in mutations.items():check('reject_'+name,not accepted)
print(json.dumps({'result':'PASS','checks':len(records),'check_names':records,
 'numerator_lower_bound':'64/250047','residual_lower_bound':str(residual_bound),
 'Bernstein_coefficients':list(map(str,betas)),
 'mutation_rejections':len(mutations),'sampling_used':False},indent=2))
```

Expected result: `PASS`, 31 checks including six corruption rejections; numerator lower bound `64/250047`; residual lower bound `153664/976781997`.
