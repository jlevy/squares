# C1092 MMMP: the right square cannot own the inward auxiliary

Every decimal is an exact rational. All owned points are strict. An excluded point may touch a face. The local theorem below concerns two actual disjoint squares of the same side, not merely the convex hulls of their listed points. It uses no wall, center sign or side upper bound.

## 1. A two-square theorem

**Theorem 1.** Let E and R be disjoint open squares of a common side a>1. Suppose E owns

    M=(.35,.35), B=(.26,1), C=(.4,1),

and excludes

    P=(0,1.086), Z=(0,.5).

Suppose R owns

    A=(.26,0), S=(1.086,0), D=(1,.4),

and excludes F=(1,−.26). Then such E,R do not exist.

The point M is automatically excluded from R, and A is automatically excluded from E, because the owners are actual and disjoint.

### 1.1. The right square's angle and faces

Reflect Theorem 2 of `C974-C976-CONTINUOUS-REDUCTIONS.md` through the vertical axis and translate its origin to the present chart. Its three strict points are exactly A,S,D, and its two excluded points are F,M. Consequently R has a strictly negative canonical frame

    u_R=(b,−t), v_R=(t,b), b≥t>0, b²+t²=1,
    9/35<t/b<13/37.                                  (1)

If L,V are its lower face coordinates, the same proof gives the actual face bounds

    L≥.35(b−t), V≥t−.26b.                             (2)

For completeness, these are the reflected upper-u face at M and lower-v face at F in that theorem. Strict ownership of A also gives

    L<.26b, V<.26t.                                  (3)

In particular

    b>47/50=.94, 6/25=.24<t<1/3.                     (4)

Indeed the endpoint bounds in (1) give b>37/sqrt(1538)>.94 and 9/sqrt(1306)<t<13/sqrt(1538)<1/3; the lower endpoint is greater than .24.

### 1.2. Every possible separating direction

For a unit direction n, write lower_Q(n),upper_Q(n) for the minimum and maximum projections of the closure of Q. Since the actual interiors are disjoint, some face normal of E or R separates them. Orient that normal from R toward E, so

    upper_R(n)≤lower_E(n).                            (5)

Strict points on its two sides give strict differences. The pairs A_R,B_E and D_R,M_E imply

    n_y>0, n_x<(−1/13)n_y.                            (6)

The second bound uses D=(1,.4), so M−D=(−.65,−.05). The pair A_R,M_E additionally gives n_x>−(35/9)n_y. Thus the strict cone is

    n_y>0, −(35/9)n_y<n_x<−(1/13)n_y.                (7)

For R, its upward normal v_R is outside (7). Its sole remaining candidate is −u_R. For E with positive canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1,

the only candidate is v. For E with negative canonical frame

    u=(c,−s), v=(s,c), c≥s≥0,

the only candidate is −u, possible only when s/c>9/35. These statements also cover axes and the common diagonal endpoints. We now exclude all the listed candidates.

## 2. The E-normal candidates

First suppose E has the negative frame and lower faces U,W. At A its lower-u band follows strictly from B, and its upper-v band follows strictly from B. Thus A can only be upper u or lower v.

If A were upper u, strict ownership of M would imply

    .35(c−s)<.26c, hence s/c>9/35.

At P its upper-u band follows from B, its lower-v band from M, and its upper-v band from C. The respective strict differences are

    u(B)−u(P)=.26c+.086s>0,
    v(P)−v(M)=.736c−.35s>0,
    v(C)−v(P)=.4s−.086c>0.

Therefore P must be lower u. These opposite u faces would give

    a≤.26c+1.086s≤1.346/sqrt(2)<1,                    (8)

because this linear expression increases throughout 0≤s/c≤1 and 1.346²<2. This is impossible. Consequently A has its upper-u band strict and is lower v:

    W≥.26s.                                           (9)

This immediately excludes the candidate −u in (5), since the strict point A belongs to R.

It remains to exclude the candidate v=(−s,c) for positive E. Its coefficient along u_R is −sb−ct<0. Thus (2),(3) give a strict lower bound on upper_R(v) by using L<.26b and V+a>1+t−.26b. Direct expansion gives

    upper_R(v)−.35(c−s)>c A_0+s B_0,
    A_0=b+.74bt−.26b²−.35,
    B_0=.09−t−.74t²+.26bt.                            (10)

The elementary bounds (4) imply

    A_0>33/100=297/900,
    −293/900<B_0<0.                                   (11)

For the first inequality, discard .74bt and use b>.94,b²≤1. For the lower bound on B_0, discard .26bt and use t<1/3. For its upper bound, use b≤1 and t>.24 to obtain B_0<.09−.74(.24)<0.

Since 0≤s≤c, the expression in (10) is greater than c/225. Yet strict ownership of M gives lower_E(v)<v(M). This contradicts (5). Every candidate normal belonging to E is now excluded.

## 3. The R-normal when E has nonnegative angle

The remaining direction is n=−u_R. Its separation condition is equivalent to

    upper_E(u_R)≤lower_R(u_R)=L<.26b.                 (12)

For nonnegative E define

    alpha=bc−ts>0, k=bs+tc>0.

Then u_R=alpha u−k v. Strict ownership of C and M gives

    upper_E(u_R)>alpha(.4c+s)−.35k(c−s).

Writing r=t/b, subtraction of .26b yields the exact lower expression

    b[.14−.05s²+.65cs−r(.35+.65s²+.05cs)].            (13)

As s²≤cs and r<13/37, its bracket is at least

    .14−.35(13/37)+[.6−.7(13/37)]cs
    =63/3700+(131/370)cs>0.                           (14)

This contradicts (12), including s=0 and c=s.

## 4. The R-normal when E has negative angle

Retain (9), put

    alpha=bc+ts>0, delta=bs−tc,

and split only at the relative order of the two actual angles.

### 4.1. The E angle is smaller: delta<0

Now s/c<t/b<13/37<3/7. At Z its upper-u band follows from M, its lower-v band follows from M, and its upper-v band follows from B. The only nontrivial comparison is

    v(Z)−v(M)=.15c−.35s>0.

Hence Z must be lower u, giving U≥−.5s. Strict M gives W<.35(c+s). Because delta<0 and a>1,

    upper_E(u_R)>alpha(1−.5s)+.35delta(c+s).

Subtracting .26b and expanding gives bF+tG, where

    F=c−.15cs+.35s²−.26,
    G=s−.35−.15s²−.35cs.                              (15)

Using c≥1/sqrt(2)>.7, s²≤1/2 and cs≤1/2,

    F>73/200, G≥−3/5.

Therefore

    bF+tG>b[73/200−(3/5)(13/37)]
          =(1141/7400)b>0.                            (16)

This contradicts (12).

### 4.2. The E angle is at least the R angle: delta≥0

Now s/c≥t/b>9/35. The same three projection comparisons at P used in Section 2 show that P is lower u, independently of the rejected upper-u possibility at A. Hence U≥−1.086s. Combining this with (9) and a>1 gives

    upper_E(u_R)>alpha(1−1.086s)+delta(1+.26s).

After subtracting .26b, this is bF+tG with

    F=c+s−1.086cs+.26s²−.26,
    G=s−c−1.086s²−.26cs≤0.                            (17)

Put r_0=13/37. Since t/b<r_0 and G≤0, the bracket F+(t/b)G is at least F+r_0G. Its exact expression is

    (1−r_0)c+(1+r_0)s−(1.086+.26r_0)cs
      +(.26−1.086r_0)s²−.26.

Both coefficients of cs and s² are negative. Using cs≤s and s²≤s reduces it to

    (24/37)c+(97/1850)s−13/50>359/1850>0.             (18)

Here only c>.7 was used in the final bound. This again contradicts (12). Equality of the two angles belongs to this case, with delta=0; every inequality needed for the contradiction remains strict because a>1.

All actual separating axes have been excluded. Theorem 1 follows. ∎

## 5. The exact original MMMP application

**Theorem 2.** In every original C1092 MMMP configuration, Q10 excludes G6=(2.26,2).

**Proof.** Suppose instead that G6 belongs strictly to Q10. The original compulsory G-covering set for Q5 is {G5,G6,G8}. Since G5 belongs to Q9 by the direct wall-sign chord and G6 now belongs to Q10, Q5 must own G8.

We claim that Q5 must also own F8. If F8 were absent, its compulsory F-covering set {F4,F6,F8} would give F4 or F6. Simultaneous F6,G8 ownership is impossible by `OUTWARD-CORNER-TWO-GAPS.md`, reflected through y=2, with parameters r=.39,t=.26. Its two strict outer anchors are exactly F6,G8; its gap exclusions are (2.39,1) in Q9 and the hypothesized absent F8; its corner exclusion is (3,1) in the actual paired corner Q1. The squared-distance condition is .61²+.74²=.9197<1. Thus F6 is absent and F4 is owned. But the untransformed `MIXED-SPAN-FOUR-POINTS.md` then applies to Q5: its strict pair is F4,G8, and its four excluded points are G6,F8,G5,F6. This contradiction proves F8 ownership.

Only a five-row inspection of the original combined component list M_10 is now needed. Its entries containing G6 are exactly

| Original label | F points | G points |
|---|---|---|
| 327936 | F8 | G6,G8 |
| 590336 | F9 | G6,G9 |
| 328448 | F8,F9 | G6,G8 |
| 590592 | F8,F9 | G6,G9 |
| 852736 | F8,F9 | G6,G8,G9 |

Because F8 is strict in Q5, only 590336 remains. In particular Q10 strictly owns G9. This is a literal original component-list consequence, not a sweep over the 55,126 ownership vectors.

Apply Theorem 1 after translating all actual points by (−2,−2), with E=Q6 and R=Q10. Every premise has the following original owner:

| Local datum | Original point | Actual owner or exclusion reason |
|---|---|---|
| M | (2.35,2.35) | Q6's original marker |
| B | G7=(2.26,3) | Q6, MMMP core theorem |
| C | F7=(2.4,3) | Q6, MMMP core theorem |
| P | (2,3.086) | Q11's original marker |
| Z | (2,2.5) | Q7, full MMMP center-crosspoint theorem |
| A | G6=(2.26,2) | Q10, present hypothesis |
| S | (3.086,2) | Q10's original marker |
| D | G9=(3,2.4) | Q10, five-row deduction above |
| F | F8=(3,1.74) | Q5, proved above |

These are two distinct actual squares of the common side a>1. The local theorem gives a contradiction, proving the exclusion of G6 from Q10. ∎

## 6. Scope

The MMMP proof has now excluded G6 from both Q6 and Q10. This chapter does not assume that any other square owns G6: the original covering lists, and not an invented requirement to cover every auxiliary point, must govern the remaining ownership deductions. The new local two-square obstruction itself needs no wall, center-sign condition, upper side bound or corner marker.
