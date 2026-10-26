# C1092 MPPM: the positive crosspoint angle dichotomy and isolated missing wall origins

All terminating decimals are exact rationals. Retain the original no-omission OOOO entrance, its actual twelve open square owners, pairwise disjoint interiors and common side 1<a<=1.001. Every asserted owned point is strict. A point excluded from a square may lie on its boundary; its exclusion does not assign it to another square.

The completed crosspoint propagation in C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md implies that every still-possible all-positive OOOO configuration has all four actual crosspoints. Indeed an owned forward point gives an unconditional crosspoint seed, and the positive-successor theorem propagates it backwards through a run of omitted forward points. The all-forward-missing alternative was already excluded by the independent wall-order cycle. We use these four crosspoints below.

## 1. Two separated angle ranges for a retained forward point

Normalize the current actual central owner as C=Q4 and translate by (-2,-2). Use its strictly positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    x=s/(1+c), U<u·Z<A=U+a, V<v·Z<K=V+a.

The strict ordinary points are

    M=(-.35,-.35), P=(-1,-.26), G=(-1,-.4).

Suppose the forward point T=(-.26,0) is strict in C. The actual next central owns Y=(0,-.5), so Y is excluded from C. The reviewed positive-forward face theorem gives the simultaneous actual bounds

    U>=-c-s, V>=.4s-c, A<=0, K<=s.                 (1)

**Theorem 1.** Exactly one of the following two alternatives holds:

| Exit of the actual foreign Y | Necessary continuous angle range and actual face |
|---|---|
| Upper u | s/c<13/25 and A<=-.5s |
| Lower v | x>1/3 and V>=-.5c |

In the first alternative the backward point I=(0,-.26) is excluded from C, and the outer halfpoint H=(-1,-.5) is strict in C. Its paired-corner transfer therefore supplies the actual next wall origin.

**Proof.** The lower-u band at Y is strict by M, with increment

    u(Y)-u(M)=.35c-.15s>=.20c>0.

Its upper-v band is strict by M, with increment

    v(M)-v(Y)=.35s+.15c>0.

Thus every exclusion of Y must occur at its upper-u face or lower-v face, allowing equality. In the upper-u alternative A<=-.5s. The strict forward point gives A>u(T)=-.26c. Consequently .26c>.5s, which is precisely s/c<13/25. Also

    u(I)=-.26s>-.5s>=A,

so I is excluded. The inequality s/c<13/25 implies x<1/3, since at x=1/3 the slope is 3/4 and x↦2x/(1-x^2) increases. The actual hypotheses of Theorem 3 in C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md are now supplied, and that complete face proof gives strict H.

In the lower-v alternative, V>=-.5c and K<=s imply

    1<a<=s+.5c.

The exact identity

    1-s-.5c=(1-x)(1-3x)/(2(1+x^2))               (2)

therefore forces x>1/3. Here x<1, as for every canonical angle. Conversely the upper-u alternative was already confined to a range with x<1/3. The two exits thus cannot occur together, even as weak face equalities, and they exhaust the possibilities. The strict H-to-wall-origin transfer uses the same actual paired corner as in the original entrance. This proves the theorem. ∎

## 2. An actually missing wall origin forces strict backward ownership

**Theorem 2.** In an all-positive OOOO configuration with its four actual crosspoints, suppose the actual next wall B=Q9 does not strictly own O_B=(2,1). Then the normalized C=Q4 satisfies

    x>1/3,
    U>=-c-.5s, V>=-.5c, A<=0, K<=s,             (3)

and it strictly owns both T=(-.26,0) and I=(0,-.26). The actual successor Q5 therefore omits its own forward F4=(2,1.74).

The missing wall B has strictly negative canonical orientation. Both neighboring actual walls Q8 and Q10 strictly own their own origins.

**Proof.** If C omitted its forward T, the already proved missing-forward halfpoint and actual paired-corner transfer would supply O_B. Thus T is strict in C.

The actual corner Q0 owns its two original outer points and its inner (1,1). The contrapositive of the all-angle paired-corner transfer shows that, under the missing O_B hypothesis, Q0 strictly owns the normalized H=(-1,-.5). Consequently H is excluded from C. Section 6 of C1092-MPPM-POSITIVE-BOUNDARY-ORIGIN.md proves, using precisely this actual corner halfpoint and the foreign northwest marker, that its exit is lower u:

    U>=-c-.5s.                                    (4)

The same section retains the unconditional positive-forward faces A<=0 and K<=s; neither face presumes ownership of the preceding wall origin.

Theorem 1 cannot have its upper-u alternative because that alternative puts H strictly in C, whereas H is already strict in Q0. Therefore its lower-v alternative applies, giving x>1/3 and V>=-.5c. This proves (3).

Suppose I were not strict in C. The complete backward-point face argument in Corollary 2 of C1092-MPPM-FORWARD-OWNED-POSITIVE-D.md then gives A<=-.26s. Together with (4), this would imply

    a=A-U<=c+.24s.

On the closed interval p0=2 atan(1/3)<=p<=pi/4, the function cos p+.24 sin p decreases strictly, since its derivative is -sin p+.24 cos p<0. At p0 its value is

    4/5+(6/25)(3/5)=118/125<1.                   (5)

This contradicts a>1. Thus I is strict in C. Its literal original value is (2,1.74), the successor Q5's forward point. Disjointness of the two actual squares excludes that point from Q5; this is a strict-owner implication, not an assignment from omission.

Corollary 2 of C1092-MPPM-POSITIVE-BOUNDARY-ORIGIN.md says every boundary square with nonnegative canonical orientation owns its origin. Hence this actually missing B must be strictly negative.

Since Q5 omits its forward point, its actual halfpoint/corner transfer supplies the next wall Q10 origin (3,2). For the other neighbor, suppose Q8 omitted (1,2). Apply the just-proved part of this theorem after a simultaneous backward quarter turn: its preceding central Q7 would then strictly own its backward point G3=(1.74,2). But this is the strict T already owned by C=Q4, a contradiction. Therefore Q8 strictly owns (1,2). Both neighboring origin conclusions refer to the actual walls, and no assumption of the conclusion has been used in proving (3) or (5). ∎

## 3. Literal cyclic map and scope

Let R(x,y)=(4-y,x), and rotate every strict point, excluded point, corner, wall and frame together. The relevant map is

| Current actual C | Its forward T | Its backward I | Next actual wall origin | Preceding / following wall origins |
|---|---|---|---|---|
| Q4 | G3=(1.74,2) | F4=(2,1.74) | Q9(2,1) | Q8(1,2), Q10(3,2) |
| Q5 | F4=(2,1.74) | G6=(2.26,2) | Q10(3,2) | Q9(2,1), Q11(2,3) |
| Q6 | G6=(2.26,2) | F5=(2,2.26) | Q11(2,3) | Q10(3,2), Q8(1,2) |
| Q7 | F5=(2,2.26) | G3=(1.74,2) | Q8(1,2) | Q11(2,3), Q9(2,1) |

Thus actually missing wall origins, if any remain, are isolated around the four-wall cycle. The current central strictly owns both adjoining inner points, its following central omits forward, and both outer neighboring walls retain their origins. This is a continuous structural reduction. It does not claim that a steep positive forward owner always owns its backward point: that additional strict ownership was proved under the actual missing-wall-origin hypothesis in Theorem 2.

A further actual-owner argument is still required to exclude these isolated missing-origin blocks and the all-origin positive mixed-forward alternative. No weakened corner/central/wall model is asserted to be impossible here.
