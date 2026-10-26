# C1092 MPPM: every nonpositive predecessor supplies the next ordinary halfpoint

Retain the original no-omission OOOO family, its twelve actual open squares of common side 1<a<=1.001, and the sector rotation R(x,y)=(4-y,x). Write

    C_i=Q_(4+i), (B_0,B_1,B_2,B_3)=(Q9,Q10,Q11,Q8),

with indices modulo four. Each sector is examined in the chart R^(-i). Its ordinary outer halfpoint is H=(1,1.5), and its next actual boundary origin is P=(2,1). Forward membership means strict ownership by the designated central square; omission never assigns the point a different owner.

## 1. The universal transfer

**Theorem 1.** If an ordinary central C_i has nonpositive canonical angle, then the next actual ordinary central C_(i+1) strictly owns its ordinary outer halfpoint. Consequently its next actual boundary B_(i+1) strictly owns its local origin.

There is no condition on the forward membership of C_i, on the sign or forward membership of C_(i+1), or on either remaining central square. In particular no preceding wall origin is assumed.

If C_(i+1) is nonpositive, its own halfpoint and actual next origin are the unconditional conclusion of Corollary 2 of C1092-MPPM-ORDINARY-NEGATIVE-HALFPOINT.md. If C_(i+1) omits its forward point, the ordinary missing-forward halfpoint and paired-corner transfer in Corollary 3 of C1092-MPPM-ORDINARY-CENTRAL-REDUCTION.md supply the same strict points, for either sign.

It remains to treat C=C_(i+1) positive and forward-owned. If the predecessor C_i retains its forward point, Corollary 3 of C1092-MPPM-NEGATIVE-FORWARD-POSITIVE-H.md gives exactly the required halfpoint and next origin. That theorem explicitly retains possible backward-inner overlap in C and does not require either unproved adjacent origin.

Suppose, therefore, that W=C_i is nonpositive and omits its forward point. Its missing-negative profile rules out an axial angle. Corollary 3 of C1092-MPPM-NEGATIVE-MISSING-POSITIVE-CEILING.md then applies to the actual W,C pair and gives

    0<x_C=tan(p_C/2)<7/24<3/10<1/3.              (1)

Let E=C_(i+2) denote the next actual ordinary central after C. The remaining proof uses the following exhaustive literal alternatives.

## 2. A successor that retains its forward point

If E is positive and owns its forward point, Theorem 2 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md gives its inner crosspoint X strictly, without an angle restriction on E.

The same inner crosspoint belongs strictly to any nonpositive E that retains its forward point. To check this directly, normalize C to the present centered southwest chart, so E's strict forward and ordinary points include

    I=(0,-.26), B0=(.26,-1).

Write E's nonpositive frame as e=(d,-t),f=(t,d), d>=t>=0. At E'=(0,-.5), the exact strict-band increments are

    e(E')-e(I)=.24t>=0,
    e(B0)-e(E')=.26d+.5t>0,
    f(E')-f(B0)=.5d-.26t>=.24d>0,
    f(I)-f(E')=.24d>0.

Even at t=0 the first band remains strict because it has the same projection as the strict I. Thus E' is strict in E for both signs of a forward-owned E.

That crosspoint is therefore foreign to C. Theorem 3 of the positive-crosspoint seed chapter, together with (1), supplies C's strict outer halfpoint and its next actual wall origin. This completes every forward-owned E alternative without assuming an owner for any other auxiliary.

## 3. A successor that omits its forward point

If E is nonpositive and omits its forward point, its missing-negative profile again excludes an axial representative. Both actual W and E are negative missing-forward squares flanking the positive forward-owned C. Corollary 2 of C1092-MPPM-FLANKED-POSITIVE-HALFPOINT.md supplies C's strict outer halfpoint and its next actual origin. Its complete three-square proof uses the actual W,C,E support functions and the ceiling (1); no previously owned wall origin is a premise.

It remains that E is positive and omits its forward point. If its own half-angle is at most 1/3, Theorem 2 of the positive-crosspoint seed chapter places its inner crosspoint strictly in E. The same application of Theorem 3 as in Section 2, with C's bound (1), supplies the desired points.

If instead E has half-angle greater than 1/3, Corollary 2 of C1092-MPPM-SHALLOW-STEEP-POSITIVE-HALFPOINT.md applies. Its actual predecessor C is positive and forward-owned with half-angle less than 3/10 by (1), and its actual successor E is precisely a positive missing-forward square above 1/3. The corollary proves C's strict outer halfpoint and its next boundary origin using the full positive missing-forward E profile and both actual C/E supports.

These alternatives exhaust the actual sign and forward membership of E, including all canonical endpoints in their cited local proofs. Theorem 1 follows.

## 4. Literal cyclic output and the remaining scope

The strict transferred points in the four sectors are:

| Actual central receiving the halfpoint | Its strict outer halfpoint | Actual boundary receiving its origin |
|---|---|---|
| Q4 | (1,1.5) | Q9 owns (2,1) |
| Q5 | (2.5,1) | Q10 owns (3,2) |
| Q6 | (3,2.5) | Q11 owns (2,3) |
| Q7 | (1.5,3) | Q8 owns (1,2) |

Every transfer of a halfpoint to a boundary origin is the same literal paired-corner theorem: in the local southwest chart use Theorem 7 of C1092-DIRECT-WALL-POINT.md with b=.914,ell=1.6, strict corner anchors (1,.914),(1,1), strict bottom anchors (2,.914),(1.6,1), and the real two corner walls and bottom wall. All are original actual owners; the newly proved halfpoint is strict in the central square and hence excluded from the paired corner.

**Corollary 2.** If a local boundary origin is still missing in OOOO, then its preceding central square is positive and forward-owned, and the central square immediately before that one is also positive.

Indeed a missing forward point or a nonpositive angle in the first central would supply the origin through its own halfpoint. If the central immediately before it were nonpositive, Theorem 1 would supply the same origin. Thus a remaining missing origin can occur only inside a consecutive positive run. This is an exact restriction on actual signs and memberships; the chapter does not claim that such a run, or a complete mixed-sign cycle, has already been excluded.
