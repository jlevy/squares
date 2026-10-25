# C1092 MPPM: the complete ordinary ending with exactly two positive central angles

Retain the original no-omission OOOO MPPM entrance, its twelve actual
open square owners, pairwise disjoint interiors, and common side
1<a<=1.001. Every point described as owned is a strict interior point.
An omitted point is merely excluded from its designated owner, allowing
a face equality. All terminating decimals are exact rationals.

**Theorem 1.** The four ordinary central canonical angles cannot contain
exactly two strictly positive angles.

This is a composition of the reviewed continuous local obstructions.
The source checks below retain the actual central squares and their
actual boundary bars; no global boundary-origin conclusion is required.

## 1. The literal cyclic data

Use the simultaneous sector rotation R(X,Y)=(4-Y,X). In the coordinates
centered at (2,2), it is (x,y)->(-y,x). The actual ordinary pairs,
forward points, crosspoints and following boundaries are

| Central | Strict ordinary pair | Designated forward point | Its crosspoint X | Following boundary |
|---|---|---|---|---|
| Q4 | F0,G0 | G3=(1.74,2) | (1.5,2) | Q9 |
| Q5 | G5,F6 | F4=(2,1.74) | (2,1.5) | Q10 |
| Q6 | F9,G9 | G6=(2.26,2) | (2.5,2) | Q11 |
| Q7 | G4,F3 | F5=(2,2.26) | (2,2.5) | Q8 |

Write P for a strictly positive central angle and N for a nonpositive
one. Write R when that owner strictly retains its designated forward
point and M when it omits it. These are statements about the membership
of the displayed point in the displayed actual square.

The signed-edge conclusion in Section 2 of
C1092-MPPM-NEGATIVE-MISSING-POSITIVE-MISSING-EXCLUSION.md gives

    every remaining N -> P edge is N_R -> P_M.       (1)

It incorporates both recipient memberships and both predecessor
memberships from the earlier signed-edge exclusions.

Every P owner has its strict X by
C1092-MPPM-UNIVERSAL-POSITIVE-CROSSPOINTS.md. Every N_R owner also
has its strict X. For completeness this last assertion needs only its
ordinary G=(-1,-.4) and retained T=(-.26,0) in its own southwest
chart. At X=(-.5,0), in the frame (c,-s),(s,c), the increments from
G in the two lower bands are .5c-.4s>=.1c>0 and .5s+.4c>0.
The increments to T in the two upper bands are .24c>0 and .24s>=0.
The strictness of T covers equality in the latter projection as well.
Thus all four bands at X are strict, including the axial case.

Every N owner supplies its strict outer halfpoint and the origin of
its one actual following boundary, by the unconditional ordinary
nonpositive halfpoint theorem and the actual paired-corner transfer.
The ordinary advances are independent of central sign or forward
membership. Consequently the following full strict bar is available
whenever its indicated preceding central is N:

| Preceding N owner | Actual following boundary and full strict bar | Origin source | Far-advance source |
|---|---|---|---|
| Q4 | Q9: [1.44,2] x {1} | Q4 outer (1,1.5), actual Q0 | G5 in Q5 |
| Q5 | Q10: {3} x [1.44,2] | Q5 outer (2.5,1), actual Q1 | F9 in Q6 |
| Q6 | Q11: [2,2.56] x {3} | Q6 outer (3,2.5), actual Q2 | G4 in Q7 |
| Q7 | Q8: {1} x [2,2.56] | Q7 outer (1.5,3), actual Q3 | F0 in Q4 |

Each entire displayed interval is strict in its one actual boundary
square by convexity. In the preceding central's own southwest chart it
is exactly [-.56,0] x {-1}. The far sources in the last column are
ordinary points, including when their owner has positive angle.

## 2. The precise local consequences used below

Normalize any N_R owner as C in its own southwest chart and write

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,
    U<u dot Z<A=U+a, V<v dot Z<H=V+a.

The actual ordinary points, retained forward point, outer halfpoint,
corner and foreign preceding marker give the complete common table

    U>=-c, V>=-c-s, A>=a-c>0,
    -.26s<H<=.35(c-s).                            (2)

The origin D=(-1,0) needed for U>=-c is genuinely excluded by
C1092-MPPM-UNIVERSAL-CENTRAL-ORIGIN-EXCLUSIONS.md. The face
argument uses its exclusion only: the three other bands are strict
from C's own ordinary and forward points. It does not require that
the preceding boundary strictly own D. In particular s=0 is
impossible, since strict P=(-1,-.26) would then have the same
u projection as excluded D. Thus every N_R used below is strictly
negative. A missing N owner is also strictly negative by its
missing-forward width profile.

Call the following the narrow-angle conditions:

    0<p<atan(1/4), H<.086, c>.97, s<.25,          (3)

where c=cos p and s=sin p. We use four local consequences.

**Local consequence A.** If the actual predecessor W of C is N_M,
then (2),(3) hold for C.

This is the continuous proof in Sections 5.1--5.3 of
C1092-MPPM-ALL-NEGATIVE-MIXED-FORWARD-ENDING.md, with its exact
local scope recorded in Lemma 1 of
C1092-MPPM-ONE-POSITIVE-CONTINUOUS-ENDING.md. W's strong missing
profile needs only its genuine preceding-D exclusion, now universal.
The comparison of W and C gives

    H<c f(phi)-s g(phi), f<.086, .48<g<=.5,
    tan p<43/110.

Its promotion to (3) uses C's own actual following origin and whole
bar, and its own corner and faces (2). That origin and bar are
supplied by the preceding table because C is N. No origin belonging
to a boundary after a positive central enters those sections. The
complete proof therefore applies in the present mixed-sign entrance.

**Local consequence B.** If the actual predecessor of C is P, and
the actual successor of C strictly owns its X, then (2),(3) hold
for C.

This is Corollary 2 of
C1092-MPPM-POSITIVE-NEGATIVE-RETAINING-SHALLOW.md. Its two-square
support comparison and strict actual-bar promotion use C's own
following boundary, whose full bar is supplied above. The predecessor
may have either forward membership. The successor contributes its
one genuine strict X, with no sign premise beyond that ownership.

**Local consequence C.** A C satisfying (2),(3) cannot be immediately
followed by a P_M owner.

This is exactly Lemma 2 of
C1092-MPPM-ONE-POSITIVE-CONTINUOUS-ENDING.md. The positive missing
recipient supplies its strict X and the two simultaneous actual faces
in equation (5) of that proof. C's genuine following bar supplies
its strict lowest-vertex clearance. The three possible actual
separating normals are all excluded there for the full positive
recipient angle interval. It uses neither the predecessor sign nor
an origin after that positive recipient.

**Local consequence D.** A C satisfying (2),(3) cannot be immediately
followed by an N_R owner E when the actual central after E strictly
owns its X.

Here apply Sections 3.1--3.3 of the same one-positive chapter. The
negative missing predecessor in that chapter's Lemma 3 is used only
to establish (2),(3) for C. Its subsequent proof starts from those
conditions and the actual retaining E. Section 3.1 proves

    0<q<atan(1/2), d>.89, t<.45.

Section 3.2 uses the genuinely foreign next X and E's own full
following boundary bar to obtain, in the common C/E chart,

    K_E>=-d, D_E>=a-d, dJ_E+tD_E<1.

The same universal preceding-D exclusion supplies the first face;
the latter strict bound is clearance from that actual bar. E is N,
so its bar and origin are genuine by Section 1 here. Section 3.3
then excludes both remaining actual normals in both relative-angle
orders, retaining equality. Its inputs are only these E bounds,
(2),(3), the two markers and E's own ordinary and forward points.
Thus the earlier source of C's narrow angle can be replaced by B,
without adding a predecessor hypothesis to this two-square conclusion.

All four consequences keep the strict entire-bar ownership and
the actual common side. Their cited scalar proofs cover whole
angle intervals, rather than selected orientations.

## 3. Alternating signs

Suppose the two positive angles alternate with the two nonpositive
angles. Rotate so that the cyclic signs are P,N,P,N at Q4,Q5,Q6,Q7.
Applying (1) at both changes from N to P forces exactly

    Q4=P_M, Q5=N_R, Q6=P_M, Q7=N_R.              (4)

Apply local consequence B to the positive Q4, retaining negative
Q5 and the strict crosspoint X=(2.5,2) in actual Q6. It gives
(2),(3) for Q5 in its own chart. Local consequence C now excludes
the same Q5 followed by positive missing Q6.

The boundary used in both steps is the same actual Q10. Its origin
(3,2) comes from Q5's nonpositive halfpoint and actual Q1; its far
point (3,1.44) comes from ordinary F9 in Q6. Thus the strict whole
bar remains available even though Q6 is positive. This excludes
the alternating sign pattern.

## 4. Consecutive positive angles

Otherwise rotate so that the signs at Q4,Q5,Q6,Q7 are P,P,N,N.
The change from Q7 to Q4 gives, by (1),

    Q4=P_M, Q5=P, Q6=N, Q7=N_R.                  (5)

There is no restriction on Q5's forward membership in the argument.
Split only the actual forward membership of Q6.

If Q6 is missing, local consequence A applied to Q6,Q7 gives
(2),(3) for Q7. Consequence C then excludes Q7 followed by the
positive missing Q4. Its actual bar is Q8's full segment from
(1,2) to (1,2.56), whose origin comes from Q7 and whose far point
comes from ordinary F0 in the same actual Q4. No property of
Q5's following boundary is used.

If Q6 is retaining, its following Q7 has its genuine strict X by
the elementary retaining-negative band proof in Section 1. Apply
local consequence B to Q5,Q6,Q7. It gives (2),(3) for Q6.
Now apply local consequence D to C=Q6 and E=Q7; the central
after E is actual Q4, whose X=(1.5,2) is strict by the universal
positive crosspoint theorem. This is a contradiction.

For clarity, the two actual bars in this last application are
Q11's [2,2.56] x {3}, supplied by Q6's own halfpoint/corner and
ordinary G4 in Q7, and Q8's {1} x [2,2.56], supplied by Q7's
own halfpoint/corner and ordinary F0 in Q4. Both negative owners
therefore have precisely the strict bars required by the two local
proofs. No forward auxiliary omitted by Q4 has been assigned to
either of them.

The missing and retaining alternatives exhaust Q6. Both cyclic
arrangements of two positive angles have now been excluded. This
proves Theorem 1. ∎

The conclusion is confined to the exactly-two-positive sign sector.
It does not claim that a general positive-to-negative edge is
impossible in isolation, or that every actual boundary origin is
unconditionally owned. The required origins above were obtained
from the stated actual nonpositive owners separately.
