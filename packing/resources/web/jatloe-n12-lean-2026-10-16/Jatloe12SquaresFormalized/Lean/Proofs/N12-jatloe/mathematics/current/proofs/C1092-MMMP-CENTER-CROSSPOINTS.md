# C1092 MMMP: the actual left wall gives the second center crosspoint

All terminating decimals are exact rationals. Owned points are strictly inside their named actual open squares. Excluded points, container contacts, and separating supports may be tangent. No upper side bound or numerical angle enclosure is used.

## 1. A conditional center-to-crosspoint theorem

**Theorem 1.** Let C and W be disjoint open squares of the same side a>1. Suppose C strictly owns

    O=(0,0), M=(.35,.35), P=(0,.26), Q=(.26,0),

and excludes

    N=(−.35,.35), D=(.35,−.35).

Suppose W has its closure in x≤2, its center ordinate is nonnegative, and it strictly owns

    S=(1.086,0), T=(1,.26),
    the entire segment I={1}×[0,.39].

Then C strictly owns Y=(0,.5).

The premise that O belongs to C is explicit. The proof uses the complete actual W and its wall and center sign; the foreign segment alone does not replace this square.

## 2. The positive central sign and the forced negative faces

First use a nonnegative canonical frame for C,

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1,

with lower faces U,V. At D its lower u-band follows from O, its upper u-band from M, and its upper v-band from O. Its exclusion therefore forces

    V≥−.35(c+s).

The target Y has its lower u-band from O, upper u-band from M, and lower v-band from P. The respective comparisons allow s=0; equality of a projection with that of a strict anchor still supplies a strict band. For the last upper v-band,

    v(Y)−V≤.85c+.35s≤sqrt(.845)<1<a.

Thus Y is strict in every nonnegative canonical orientation.

For the remaining sign write

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,             (1)

and again let U,V be the lower faces. Since O is strict,

    U<0, V<0.                                      (2)

At N its upper u-band and lower v-band follow from O, and its upper v-band follows from M. Hence

    U≥−.35(c+s).                                   (3)

At D its lower u-band and upper v-band follow from O. If D exited upper u, (3) would give the impossible width

    a≤.7(c+s)≤.7sqrt(2)<1.

Consequently D is lower v and

    V≥−.35(c−s).                                   (4)

For Y its upper u-band follows from M, its lower v-band from P, and its upper v-band follows from

    v(Y)−V≤.85c−.35s≤.85<1<a.

If Y were missing, its only possible exit would therefore be

    U≥−.5s.                                       (5)

At s=0 this contradicts (2). From now on s>0 and p=atan(s/c) lies in (0,pi/4].

## 3. A strict point fixes the whole actual normal cone

Put

    z=s/(1+c), rho=.5−z,
    Delta(z)=.15−.30z+1.85z²−z³.

The canonical interval gives 0<z≤sqrt(2)−1<1/2. On this entire interval,

    Delta(z)≥.15−.30z+1.35z²
            =(27/20)(z−1/9)²+2/15>0.               (6)

The identities c+sz=1 and s−cz=z imply that R=(1,rho) has projections

    u(R)=1−.5s, v(R)=z+.5c.

Both lower bands of R follow from strict O. Equation (5) and a>1 give its strict upper u-band. Equation (4) gives its strict upper v-band, because

    v(R)−V≤z+.85c−.35s<1,
    1−(z+.85c−.35s)=Delta(z)/(1+z²)>0.             (7)

Thus R is a strict point of this same actual C.

If z≥.11, then 0<rho≤.39, so R also lies on the actual strict W segment I. This is impossible. We are left with

    0<z<.11, rho>.39>.26.                          (8)

Orient any separating normal n from C toward W. Comparing Q in C with S in W gives

    n·(S−Q)=.826 n_x>0.

Comparing the newly proved R in C with T in W gives

    n·(T−R)=(.26−rho)n_y>0.

Hence every separating normal belongs to the open fourth quadrant. The separating-axis theorem for two squares leaves only C's actual u-normal in (1), or W's actual face normal in that quadrant. Represent the latter, including its limiting axes as harmless extra cases, by

    w=(h,−b), w_perp=(b,h),
    h=cos(phi), b=sin(phi), 0≤phi≤pi/2.

Set

    alpha=ch+sb=cos(p−phi)>0,
    delta=sh−cb=sin(p−phi).                         (9)

No other face direction can belong to the strict cone. Both separation orders on every original face axis are accounted for by orienting n from C toward W.

## 4. Full support bounds from the real wall and its center sign

The actual W center (X_W,Y_W) satisfies

    X_W≤2−a(h+b)/2, Y_W≥0.

Consequently its full lower supports obey

    lower_W(w)≤2h−a[1+h²+hb]/2
               <2h−[1+h²+hb]/2,                    (10)

    lower_W(u)≤2c−a[c(h+b)+alpha+|delta|]/2
               <2c−[c(h+b)+alpha+|delta|]/2.        (11)

For (11), the projections of u on W's two orthonormal face directions have magnitudes alpha and |delta|. All coefficients multiplying a in these estimates are positive. These are supports of the complete original W, not of a substituted segment or an independently chosen square.

Writing A_C=U+a, equations (2), (4), (5) give

    A_C>1−.5s,
    V+a>1−.35(c−s), V<0.                           (12)

We exclude the two remaining actual normal sources in turn.

## 5. C's own normal cannot separate

Subtract the bound in (11) from 1−.5s. When 0≤phi≤p, so delta≥0, the difference is

    G1(phi)=1−2c+ch+(s/2)(h+b−1).

It is concave in phi, since its h and b coefficients are c+s/2>0 and s/2>0. Its two endpoint values are

    G1(0)=1−c>0,
    G1(p)=E=(1−c)(3−c−s)/2>0.                      (13)

Thus G1>0 throughout this complete relative-angle interval.

When p≤phi≤pi/2, so delta≤0, the difference is

    G2(phi)=1−2c+c(h+b)+(s/2)(b−h−1).

It is also concave: its h and b coefficients are c−s/2>0 and c+s/2>0. Its endpoint values are G2(p)=E>0 and G2(pi/2)=1−c>0. Thus G2>0 throughout this second interval, including delta=0.

In both cases lower_W(u)<1−.5s<A_C=upper_C(u). C's own actual normal cannot separate the squares.

## 6. The actual wall square's normal cannot separate

### 6.1. The order 0≤phi≤p

Here delta≥0. The exact upper support of C is

    upper_C(w)=alpha A_C+delta(V+a)
      >alpha(1−.5s)+delta[1−.35(c−s)]
      =h A1+b B1,

where

    A1=c+s−.85cs+.35s²,
    B1=s−c+.35c²−.35cs−.5s².

Subtract the upper bound (10) from this lower bound. The difference is

    F1(phi)=1/2+h²/2+hb/2+h(A1−2)+b B1.

Its endpoint values are

    F1(0)=c+s−1−.85cs+.35s²
          =2z Delta(z)/(1+z²)²>0,
    F1(p)=E>0.                                      (14)

Direct differentiation gives

    F1''+F1=(3/2)b(b−h)≤0

on 0≤phi≤p≤pi/4. The sine-interpolation lemma, proved in Section 3 of `INWARD-EXTENDED-ANCHOR-CENTER.md`, therefore gives

    F1(phi)≥[F1(0)sin(p−phi)+F1(p)sin(phi)]/sin(p)>0.

For completeness, that lemma follows by subtracting the displayed sine interpolant. If the difference were negative on an interval with zero endpoints, integration of g''+g≤0 against the positive first sine on that interval would give a positive integral: its length is less than pi and the integral of g times that sine is negative. This contradiction proves the inequality. The endpoints in (14) cover the endpoints of the present interval too.

Hence lower_W(w)<upper_C(w) throughout the first order interval.

### 6.2. The order p≤phi≤pi/2

Now delta≤0. Since V<0, the exact support and (12) give

    upper_C(w)=alpha A_C+delta V
      >alpha(1−.5s)=h A2+b B2,

where

    A2=c−.5cs≤1, B2=s−.5s²≥0.

The difference from (10) is

    F2(phi)=1/2+h²/2+hb/2+h(A2−2)+b B2.

Its derivative satisfies

    F2'=(h²−b²)/2−hb+(2−A2)b+B2h
        ≥1/2−b(h+b−1)
        ≥3/2−sqrt(2)>0.                              (15)

Thus F2 increases on the whole interval. At its left endpoint F2(p)=E>0 by (13), so it is positive everywhere. This excludes W's normal in the second order as well.

Both actual normal sources and all relative-angle cases have been exhausted. The hypothesized missing Y is impossible, proving Theorem 1. Axial C was handled before division by its sine; diagonal C, either W sign, W's axial limits, equal relative angles, and weak exterior contacts are all included. ∎

## 7. Exact application to the original MMMP squares

**Corollary 2.** Throughout the original C1092 MMMP entrance, Q7 strictly owns the whole triangle with vertices

    (2,2), (1.5,2), (2,2.5).                         (16)

In fact (1.5,2) and (1.46,2.01) are strict in Q7 without this center premise.

First the direct core and wall-transfer chapters give Q7's original marker, F5=(2,2.26), G3=(1.74,2), and the actual top points (1.6,3),(1.5,3) in Q11. Apply the retained central-crosspoint theorem in the appendix of `C893-CONTINUOUS-EXCLUSION.md` using the simultaneous transformation

    (x,y)↦(4−y,x).

Its three strict anchors become Q7's marker, G3, F5. Its two foreign central markers become the actual northeast marker in Q6 and the actual southwest marker in Q4. Its two foreign wall points become (1.6,3),(1.5,3), both in actual Q11. Its target becomes (1.5,2), proving that unconditional strict point.

Likewise Corollary 3 of `C1084-DUPLICATE-POINT.md` applies after the simultaneous half-turn (x,y)↦(4−x,4−y). Its strict southeast marker and inward pair become Q7's marker, F5, G3. Its excluded southwest and northeast markers become the actual Q6 and Q4 markers. Its excluded lower auxiliary (2.4,1) becomes F3=(1.6,3), strictly in actual Q11. The strict target (2.54,1.99) becomes (1.46,2.01).

Theorem 3 of `C1092-MMMP-FULL-INWARD-CENTER.md` proves (2,2) strictly in actual Q7 for every original MMMP alternative. Its proof does not use either crosspoint in this chapter. For the second crosspoint in (16), apply Theorem 1 to C=Q7 and W=Q8 in the simultaneous chart

    (xi,eta)=(2−x,y−2).

The complete actual-owner ledger is

| Local datum | Original datum | Actual source |
|---|---|---|
| O | (2,2) | Theorem 3 of `C1092-MMMP-FULL-INWARD-CENTER.md` |
| M,P,Q | Q7 marker, F5,G3 | `C1092-MMMP-CORE-OWNERS.md` |
| Excluded N | (2.35,2.35) | Actual Q6 marker |
| Excluded D | (1.65,1.65) | Actual Q4 marker |
| S | (.914,2) | Original Q8 marker |
| T | (1,2.26) | Actual Q8 wall-sign chord |
| Whole I | {1}×[2,2.39] | Actual Q8, `C1092-MMMP-WALL-TRANSFER.md` |
| Wall x≤2 | Original x≥0 | Genuine Q8 container wall |
| Nonnegative center ordinate | Original Y8≥2 | Original closed MMMP sign |

The theorem's target Y=(0,.5) is the original (2,2.5). Thus every vertex of (16) lies strictly in the same actual Q7, and convexity makes the whole triangle strict. This argument makes no G1 ownership assumption and does not infer an artificial owner for any missing auxiliary.

The full-sector center theorem discharges the local theorem's center premise before this application. Thus (16) is unconditional throughout the original MMMP family. A final MMMP exclusion still requires its own actual-square contradiction.
