# C1092 MMMP: the two actual walls complete the northwest center

All terminating decimals denote exact rational numbers. All owned points
are strict; exclusions and supporting-line contacts may be equality.
The squares in every application are the actual original owners, with
their common side a>1. No numerical angle enclosure or history of local
domains is used.

The new ingredient is a wall-center crossing lemma. It supplies precisely
the strict half-angle point needed in the retained ordinary-wall support
argument. Together with the already proved exact remaining face profile,
it gives the center (2,2) in every original MMMP configuration.

## 1. An actual wall forces a half-angle crossing

**Theorem 1.** Let C,W be two disjoint open squares of common side a>1.
Give C the canonical negative frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,

and let U,V be its lower faces. Assume C strictly owns

    P=(0,.26), Q=(.26,0),

and that V≥0. Suppose W strictly owns

    S=(1.086,0), T=(1,.26),

its closure lies in x≤2, and its center has y-coordinate at least zero.
Then s>0 and, on putting z=s/(1+c),

    U<−z.                                               (1)

In particular C strictly owns Z=(z,1).

This is a statement about the two actual full squares. The wall-center
condition on W is a premise of the theorem, not a bound inferred from its
two strict anchors.

### 1.1. A hypothetical failure leaves exactly two separating directions

Strict ownership of Q gives V<.26s, so V≥0 rules out s=0. Thus

    0<z≤sqrt(2)−1<1/2,
    cz=s−z, sz=1−c.                                   (2)

Suppose, for contradiction, that U≥−z. Define

    r0=(1−z)²/2,  ρ=max(.4,r0),  R=(1,ρ).

Then .4≤ρ<.5. The point R is strictly in C. Its lower u-band follows
from P, since c−ρs>0>−.26s. Its lower v-band follows from Q.
The exact identities

    c−r0 s=1−z,  s+r0 c=1−r0                         (3)

give its two upper bands when ρ=r0: the first projection is at most
1−z<a−z≤U+a, and the second is less than 1<a+V. If ρ=.4,
then ρ≥r0 gives c−ρs≤1−z, while

    s+.4c≤.7(c+s)≤.7sqrt(2)<1<a+V.

Thus all four bands of R are strict in either case.

Orient a separating normal n from C to W. The strict pair Q,S has
equal y-coordinates and positive x-displacement .826, so n_x>0.
The strict pair R,T has equal x-coordinates and negative y-displacement
.26−ρ, so n_y<0. Hence the normal is in the open fourth quadrant.
Among the actual C axes only u can occur.

Reindex the actual W axes as

    w=(h,−b), w_perp=(b,h),
    h=cos φ, b=sin φ, 0≤φ≤π/2.

Only w can occur among its axes. Including both interval endpoints below
does no harm, although the strict cone itself excludes their axial
directions. The complete separating list is therefore u,w.

Write p for C's angle magnitude, so c=cos p,s=sin p and 0<p≤π/4.
Put

    α=ch+sb>0, δ=sh−cb.

The actual W wall and center sign imply

    center_x(W)≤2−a(h+b)/2,  center_y(W)≥0.

Consequently its full lower supports satisfy

    lower_W(u)≤2c−a[c(h+b)+α+|δ|]/2,
    lower_W(w)≤2h−a[1+h²+hb]/2.                      (4)

Both coefficients of a in (4) are positive. The C upper support in its
own direction is U+a≥a−z>1−z.

### 1.2. The central normal cannot separate

After replacing a by 1 in the direction favorable to separation, the
difference between this strict lower bound on upper_C(u) and the upper
bound on lower_W(u) in (4) is

    D=1−z−2c+[c(h+b)+α+|δ|]/2.

For 0≤φ≤p one has δ≥0, so

    D=1−z−2c+c h+(s/2)(h+b).

For p≤φ≤π/2 one has δ≤0, so

    D=1−z−2c+c(h+b)+(s/2)(b−h).

Each expression is concave as a function of φ on its stated interval:
its sine and cosine coefficients are nonnegative. At φ=0 and φ=π/2
the common endpoint value is

    D0=1−z−c+s/2=z²(2−z)/(1+z²)>0.                  (5)

At φ=p the common value is

    E=3/2−z−2c+c²/2+cs/2
     =z²(2−3z+4z²−z³)/(1+z²)²>0.                  (6)

For the last sign, use z<1/2, so 2−3z>1/2 and 4z²−z³≥0.
Concavity and the positive endpoint values show D>0 on both intervals.
Thus upper_C(u)>lower_W(u), ruling out this direction.

### 1.3. The wall normal cannot separate

First suppose 0≤φ≤p, so δ≥0. The full support formula gives

    upper_C(w)=α(U+a)+δ(V+a)
              ≥a(α+δ)−αz
              >α(1−z)+δ.

Subtracting the bound (4) at a=1 gives

    F1(φ)=1/2+h²/2+hb/2+h(c+z−2)+b(s−1).            (7)

Here (2) was used to simplify

    (1−z)c+s=c+z,  (1−z)s−c=s−1.

Its endpoints are

    F1(0)=c+z−1=z(1−s)>0,  F1(p)=E>0,

and direct differentiation gives

    F1''+F1=(3/2)b(b−h)≤0.                           (8)

The elementary sine-interpolation principle on an interval of length
less than π now gives F1>0. A complete justification is as follows.
Let g be the solution of g''+g=0 having the same positive endpoint
values as F1. The sine formula for g makes it positive on [0,p]. If
F1−g had a negative component between two zero endpoints of distance
L≤p<π, multiply its differential inequality by the positive first sine
function on that component and integrate twice by parts. The integral
would equal

    [1−(π/L)²] ∫(F1−g) sin(πx/L) dx>0,

contrary to the nonpositive differential inequality. Thus F1≥g>0.

It remains that p≤φ≤π/2, where δ≤0. Strict Q gives V<.26s.
The full upper support, with the appropriate changed source face, is

    upper_C(w)=α(U+a)+δV
              >α(1−z)+.26s δ.

The resulting support difference is

    F2(φ)=1/2+h²/2+hb/2+h(A2−2)+b B2,
    A2=(1−z)c+.26s²,
    B2=(1−z)s−.26sc=c+s−1−.26cs.                    (9)

These coefficients have the useful signs A2<1 and B2>0. Indeed,

    1−A2=z(c+s)−.26s²
         ≥s/2−.26s²>0,

and, since c+s+1<5/2,

    B2=cs[2/(c+s+1)−.26]>.54cs>0.

Therefore

    F2'(φ)≥1/2−b(h+b−1)
            ≥3/2−sqrt(2)>0.                         (10)

At φ=p, F2(p)=E>0. Hence F2>0 throughout the remaining interval.
The wall normal is impossible as well. Both actual separating axes
have been exhausted, proving (1).

Finally u(Z)=−z and v(Z)=1 by (2). Its lower u-band is (1); its
upper u-band follows from P because z≥s/2>.26s. Its lower v-band
follows from V<.26s<1, and its upper v-band follows from V+a>1.
Thus Z is strict in C, as asserted. ∎

## 2. The downstream ordinary-wall obstruction, with its exact inputs

The following is the part of the complete retained ordinary two-wall
proof that begins after its half-angle crossing has been established.
We reproduce its geometric reduction and state precisely the two
continuous scalar lemmas that it uses. Their full elementary proofs
are Sections A.8–A.9 of `C981-RETAINED-CONTINUOUS-LEMMAS.md`.

**Lemma 2.** Let A,R be disjoint open squares of common side a>1.
Let A have positive frame (c,s),(−s,c), c≥s>0, and lower faces L,H.
Set z=s/(1+c), and suppose 0<z<.4. Assume

    L≥0, H≥−.35(c+s),

and that A strictly owns

    P=(0,.26), Q=(.26,0), E=(.35,.65), Z=(1,z).

Suppose R strictly owns N=(1.086,0), B=(1,.4), and its closure lies
in x≤2. Then these two actual squares cannot be disjoint.

No center sign or auxiliary-label assumption is imposed on R.

### 2.1. The actual wall gives its angle and the two surviving axes

Reindex R with first-quadrant normal (r,t), r>0,t≥0, and transverse
normal (−t,r); write its lower faces as l,h. Since z∈(0,.4), the
point Z is strictly inside both transverse bands of R by comparison
with N,B, and below its upper longitudinal face by B. Its exclusion
from R must therefore be through its lower longitudinal face:

    l≥r+zt.

The strict marker and actual rightmost vertex then give

    zt<.086r,
    rtz<1−r−.086t².                                  (11)

For the second, combine r(l+a)−th≤2 with h<−1.086t and a>1.
In particular t=0 is impossible. If z≥1/5, the first inequality gives
t/r<.43 and r>.9. Dividing the second by rt gives

    z<(t/r)[1/(1+r)−.086].

Multiplication by z and the first inequality of (11) would imply

    z²<.086(10/19−.086)=179869/4750000<1/25,

a contradiction. Hence

    z<1/5, 12s<5c, c>12/13.                          (12)

Moreover R's first-quadrant angle is strictly larger than A's:

    k=ct−sr>0.                                       (13)

Otherwise r≥c>12/13 and its half-angle z_R=t/(1+r) is at most z.
But (11) would give

    z<z_R[1−.086(1+r)]/r<z_R,

since r>12/13>457/543. This is impossible.

The strict point B has its transverse projection strictly inside A's
transverse interval. Its lower band follows from Q and
.4c−.74s>0 by (12). For its upper band use H≥−.35(c+s) and

    v_A(B)+.35(c+s)=.75c−.65s<1<a.

Thus neither order on A's transverse axis can separate. Neither order
on R's transverse axis can separate because Z is strict in A and has
its R projection strictly between the projections of N,B. The reverse
orders on the longitudinal axes are excluded by Q,N, which have equal
y-coordinates and x-displacement .826>0.

Put d=cr+st>0. The only two possible separators are consequently

    L+a≤lower_R(c,s),
    upper_A(r,t)≤l.                                  (14)

These are actual full-square supports, whose exact formulas are

    lower_R(c,s)=d l−k(h+a),
    upper_A(r,t)=d(L+a)+k(H+a).

### 2.2. The central normal

Suppose the first alternative in (14) holds. It first forces t<r.
Indeed, if t≥r, the two strict R anchors give

    lower_R(c,s)<1.086c−k(.4r+.086t)≤c.

The second inequality follows by the exact expansion

    k(.4r+.086t)−.086c
      =r[(t−r)(.4c−.086s)+r(.314c−.486s)]≥0,

using (12). This contradicts L+a≥a>1≥c.

For t<r the actual wall and marker yield the full support bound

    r lower_R(c,s)≤2cr+.914st−ar(d+k).                (15)

For direct verification, expand its left side as

    d[r(l+a)−th]+s h−ar(d+k),

then use r(l+a)−th≤2 and h<−1.086t. Thus the separator and L≥0
would require

    ar(1+d+k)≤2cr+.914st.                             (16)

The retained scalar Lemma P states that, for positive unit normals
with 12s≤5c, 0≤t≤r and ct≥sr,

    1+(c−s)r+(c+s)t−2c−.914s(t/r)≥0.                 (P)

Its exact polynomial endpoint certificate is written out in Section
A.8 of the retained companion. Since d+k=(c−s)r+(c+s)t, (P)
makes r(1+d+k) at least the right side of (16). The coefficient is
positive, so a>1 contradicts (16).

### 2.3. The wall's own normal

For the second alternative in (14), the two lower A faces give

    upper_A(r,t)≥rX+tY+a(d+k),
    X=.35s²+.35cs,
    Y=−.35+.35s²−.35cs.                              (17)

The strict point E, the separator, and the strict marker N give
.65t<.736r. Thus, with p=s/c, q=t/r and w=1/r,

    p<q<23/20, w=sqrt(1+q²).

The wall and marker also give

    rl+ar+1.086t²≤2.

Combine this with (17) and divide by r². Separation would imply

    M+(a−1)J≤0,
    J=w+(c−s)+q(c+s)>0,
    M=J+X−2+qY−.914q².                              (18)

The retained scalar Lemma L states that M≥0 for c≥12/13,
0≤s≤2/5, p≤q≤23/20. In its original displayed notation the source
coordinates are X_old=2+X and Y_old=2+Y, so its formula

    w+(c−s)+q(c+s)+X_old−4+q(Y_old−2)−.914q²

is exactly M in (18). Section A.9 of the retained companion proves
this inequality continuously in its two elementary q regimes, with
all endpoint margins displayed. Equation (12) supplies its entire
domain here. Since (a−1)J>0, (18) is impossible.

Both possible separating normals have been excluded. This proves
Lemma 2, including weak contact between closure supports. ∎

## 3. Application to every original MMMP northwest square

**Theorem 3.** Every original C1092 MMMP configuration satisfies

    (2,2) strictly in Q7.                              (19)

**Proof.** Suppose otherwise. The complete earlier direct reduction
`C1092-MMMP-INWARD-CENTER.md`, Proposition 3, gives the exact
remaining negative frame in the chart

    (ξ,η)=(2−x,y−2):

    C=Q7, u=(c,−s), v=(s,c), c≥s>0,
    U≥−.35(c+s), V≥0,
    U+a≤c−.4s, V+a≤c+.4s,
    0<z=s/(1+c)<.4.                                  (20)

The strict points P=(0,.26),Q=(.26,0) are the actual F5,G3 in Q7.
For Theorem 1 take W to be the actual Q8 in the same chart. Its strict
marker (.914,2) becomes S=(1.086,0), and its strict F1=(1,2.26)
becomes T=(1,.26). The real original wall x≥0 becomes ξ≤2, and
the closed MMMP sign Y8≥2 becomes center_η(W)≥0. All hypotheses
are genuine original or previously proved ownership facts. Theorem 1
therefore gives the strict point

    (z,1)∈C.                                         (21)

Transpose this entire local chart, putting

    (X,Y)=(η,ξ)=(y−2,2−x).

The same actual Q7 now has positive frame (c,s),(−s,c), with lower
faces L=V,H=U. It has L≥0,H≥−.35(c+s), and owns the strict
P,Q in Lemma 2 (interchanged), and Z=(1,z) by (21).

It also owns E=(.35,.65), as follows directly from (20). Its lower
u-band follows from the strict marker M=(.35,.35), while its upper
u-band follows from L≥0, a>1, and

    u(E)=.35c+.65s≤sqrt(.35²+.65²)=sqrt(.545)<1.

Its lower v-band follows from H+a≤c−.4s, because

    (c−.4s)−v(E)=.35c−.05s<1<a.

Its upper v-band follows from H≥−.35(c+s), because

    v(E)+.35(c+s)=c≤1<a.

Finally take R in Lemma 2 to be the actual top wall square Q11 in
this transposed chart. Its original strict marker (2,3.086) becomes
(1.086,0); its original strict F3=(1.6,3) becomes (1,.4); and its
genuine original wall y≤4 becomes X≤2. Strict F3 was established
for every original alternative in `C1092-MMMP-CORE-OWNERS.md`.
No extra top-wall center sign or backward auxiliary exclusion is
needed in this application.

All inputs of Lemma 2 now belong to the same actual Q7,Q11 pair,
which is disjoint and has the original common side a>1. Lemma 2
contradicts their existence. The assumed missing center was therefore
impossible. This proves (19) for all original MMMP alternatives. ∎

## 4. Source ledger and scope

The application uses no newly assigned owner. Its complete nontrivial
owner ledger is:

| Datum | Original source |
|---|---|
| Remaining profile (20) | The root-audited Proposition 3, derived from Q7's strict F5,G3, foreign original markers, and genuine absent/foreign auxiliaries |
| Theorem 1's S,T | Q8's original marker and its direct wall-sign F1 |
| Theorem 1's wall and center sign | Original x≥0 wall and Y8≥2 |
| Lemma 2's N,B | Q11's original marker and the direct core ownership of F3 |
| Lemma 2's wall | Original y≤4 wall |
| Both strict half-angle points | Theorem 1 in the same actual Q7, followed by a simultaneous transposition |
| Strict E in Lemma 2 | The explicit four-band proof from the same Q7 faces (20) |

The initial nonpositive-angle and extended-anchor regimes remain
covered by the earlier audited center theorem; its Proposition 3
reduces every other possible failure to (20). No historical selector,
sampled angle, numerical side maximum, or enclosure is inserted at
that reduction or afterward. The strict comparisons use a>1, while
every separator and exterior face may be tangent.

This chapter completes the actual northwest center point for the whole
MMMP sector. A separate support contradiction involving the remaining
actual owners is still required for the full MMMP exclusion.
