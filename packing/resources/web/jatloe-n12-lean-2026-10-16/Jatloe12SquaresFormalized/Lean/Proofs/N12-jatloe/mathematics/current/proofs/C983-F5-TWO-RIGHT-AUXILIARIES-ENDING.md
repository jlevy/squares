# C983 F5-only: all three right-wall components owning both F8 and F9 are impossible

Every terminating decimal is an exact rational. Strict bars belong to one stated actual open square, and every isolated owned point retains its actual owner. Exclusions and supports may be tangent. The common side satisfies a>1. This chapter needs no side upper bound, favorable northeast angle, or unproved merged vertical midpoint.

## 1. Exact actual entrance and statement

Assume merged label8224 and the proved reductions in `C983-F5-CENTRAL-REDUCTION.md`, `C983-F5-UNIVERSAL-ORIGINS.md`, `C983-F5-MERGED-CENTER.md` and `C983-F5-LOWER-RIGHT-EXCLUSION.md`.

**Theorem 1.** None of the following three actual right-wall components is possible:

    Q10=262912={F8,F9,G8},
    Q10=525056={F8,F9,G9},
    Q10=787200={F8,F9,G8,G9}.                     (1)

The exact single-owner table already proved in the central reduction shows that (1) leaves only

    Q5=65552={F4,G6}
    or Q5=327696={F4,G6,G8},                     (2)

the second alternative being possible only in the middle row of (1). In particular the actual southeast square E=Q5 owns F4,G6 and omits F8. The theorem `C983-F5-INWARD-SIGN.md` applies using the actual merged square W=Q7, its strict F5 and proved center, and the universal actual bottom bar. Hence E has strictly negative canonical angle.

Translate by (−2,−2). Every input to the rest of the proof has the following actual source:

| Input in the translated chart | Actual C983 source |
|---|---|
| E owns M=(.35,−.35), I=(0,−.26), D=(.26,0) | Its original southeast marker and F4,G6 from (2) |
| E excludes O=(0,0) | The universal strict merged center in actual Q7 |
| E excludes B0 B1=[.26,.8]×{−1} | The complete strict universal bar in one actual Q9 |
| E excludes A0=(1,−.26), R0=(1,0) and their whole segment | F8 from (1), the universal right origin, and convexity of this one actual Q10 |

Thus the actual right neighbor supplies a strict continuous segment, not just two isolated exclusions. We show that this entrance is impossible for a negative E. The argument below in fact proves a local negative-angle center theorem from these two foreign bars.

## 2. Initial negative-frame faces

Use

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,
    lower faces U,V; upper faces A=U+a,H=V+a.

At O both v bands follow from I,D, while the upper u band follows from M. Its exclusion gives

    U≥0, A≥a>1.                                  (3)

The strict I has u projection .26s. Equation (3) therefore implies s>0, including exclusion of the axial representative.

At R0=(1,0), the lower u band follows from D and the lower v band from I. The upper u band follows from A>1≥c. Its only exit is upper v:

    H≤s.                                         (4)

At B0=(.26,−1), the lower u and upper v bands follow from D. An upper-u exit would give

    a≤A≤.26c+s≤1.26/sqrt(2)<1,

by (3), which is impossible. Thus

    V≥.26s−c.                                    (5)

At B1=(.8,−1), the lower u band follows from M with gap .45c+.65s>0, and the upper v band follows from D with gap c−.54s≥.46c>0. Hence its two possible exits are

    V≥.8s−c  or  A≤.8c+s.                        (6)

If the first alternative does not hold, the second does. In that case any interior point of E on y=−1 would, from (5) and that upper-u face, satisfy .26<x<.8. It would belong to the excluded whole bottom bar. There is no such intersection. Since the strict M is above that line, convexity forces the full lower closed support to satisfy

    y_min=−sA+cV≥−1.                              (7)

The proof may therefore split into the first alternative of (6), or the actual support bound (7). When both endpoint exits hold, it may retain the first alternative.

## 3. F8 is forced to the upper u face

At A0=(1,−.26), the lower u band follows from D, with gap .74c+.26s>0, and the lower v band follows from I, with gap s>0. Thus its exclusion is upper u or upper v.

Suppose it were upper v:

    H≤s−.26c.                                    (8)

If B1 exited through lower v, then (6),(8) would give

    a≤(s−.26c)−(.8s−c)=.2s+.74c
       ≤sqrt(.2²+.74²)=sqrt(.5876)<1,

which is impossible. Consequently (7) holds. Equations (3),(8) then bound that same full lower support by

    y_min=−sA+c(H−a)
       ≤cs−.26c²−a(c+s).

Together with (7) this implies

    a(c+s)≤1+cs−.26c².                            (9)

But c+s−1≥.8cs, and c≥s give

    c+s−1−cs+.26c²
      ≥.26c²−.2cs≥.06c²>0.

Since a>1, (9) is impossible. The upper-v alternative (8) is excluded, including a simultaneous upper-face contact. Thus A0 must exit through upper u:

    A≤c+.26s.                                    (10)

No favorable relative angle or auxiliary owner has been used in this face deduction.

## 4. The actual right bar supplies a full right support

Consider any hypothetical interior intersection of E with x=1. Its upper-u band and (10) would give

    c−sy<A≤c+.26s, hence y>−.26.

Its upper-v band and (4) would give

    s+cy<H≤s, hence y<0.

Such a point would belong to the whole strict segment A0 R0 in the one actual Q10. Therefore E has no interior intersection with x=1. Its strict marker M has x=.35<1, so convexity forces

    x_max=cA+sH≤1.                                (11)

This is a derived support on the actual E from the actual right bar, not an assumed extra container constraint.

## 5. Both bottom-bar alternatives contradict that right support

If the first alternative of (6) holds, then by U≥0,

    x_max=c(U+a)+s(V+a)
       ≥.8s²−cs+a(c+s)
       >.8s²−cs+c+s>1.                            (12)

For the last strict inequality the exact difference is

    .8s²−cs+c+s−1
      =s²[.8−(1−s)/(1+c)]>0.

Here s>0, c≥1/sqrt(2)>.7 and (1−s)/(1+c)≤1/(1+c)<10/17<.8. Equation (12) contradicts (11).

Otherwise the proved lower support (7) holds. In terms of A,H, the two actual supports (7),(11) read

    cA+sH≤1,
    −sA+cH≥ac−1.

Multiply the first by c and the second by s, and subtract. This gives

    A≤c+s−acs.

Using A≥a from (3),

    a(1+cs)≤c+s<1+cs.                             (13)

The last strict inequality is the exact identity

    1+cs−c−s=(1−c)(1−s)>0,

since s>0 and 0<c,s<1. Equation (13) contradicts a>1. This excludes the second bottom-bar alternative as well.

Every possible negative-angle face choice has failed. The sign theorem already excluded the nonnegative angle. Thus the original actual southeast square cannot exist in any of the three right-wall components (1), proving Theorem 1. ∎

## 6. The sole remaining C983 right component

Combining this theorem with the lower-right exclusion leaves, throughout the still-open F5-only branch,

    Q10=524800={F9,G9},
    Q6=131200={F7,G7},
    Q11=16392={F3,G4}.                            (14)

The exact southeast list is now

    65552={F4,G6}, 327696={F4,G6,G8},
    65792={F8,G6}, 327936={F8,G6,G8},
    65808={F4,F8,G6}, 327952={F4,F8,G6,G8}.        (15)

The actual merged center, all three remote wall origins proved for these owners, and the conditional left/corner conclusions now apply throughout (14). The first two southeast components in (15) have the proved strictly negative sign; the other four retain both signs until further argument. This chapter closes all three components in (1), including the former G7-absent northeast alternative, and leaves only the actual geometry (14),(15) for the final C983 ending.
