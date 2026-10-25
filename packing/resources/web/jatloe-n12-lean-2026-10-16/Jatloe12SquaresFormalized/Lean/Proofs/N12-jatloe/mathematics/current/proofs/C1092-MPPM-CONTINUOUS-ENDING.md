# C1092 MPPM: the complete continuous ending from the original entrance

Retain C1092-ORIGINAL-ENTRANCE.txt: twelve actual open squares Q0,...,Q11
of one common side 1<a<=1001/1000, pairwise disjoint interiors, closures
in [0,4]^2, the original strict markers and paired-corner seeds, and
the complete original auxiliary-ownership alternatives. An owned point
is strictly inside its named actual square. An omitted point is
excluded from its indicated owner, with equality at a face allowed.

The closed MPPM wall-center conditions are

    Y8>=2, X9<=2, Y10<=2, X11>=2.                  (1)

Every change of coordinates below transports all actual owners,
markers, point exclusions and walls together. In particular the
quarter turn R(X,Y)=(4-Y,X) preserves the MPPM entrance and its
closed conditions (1).

**Theorem 1.** There is no configuration satisfying this entire
original C1092 MPPM entrance.

This chapter joins the completed actual-square arguments. It supplies
the endings that earlier reduction chapters identified as remaining,
while leaving their proved statements and original hypotheses intact.
The initial exhaustive marker and ownership entrance remains a retained
premise; no new claim about that initial classification is needed here.

## 1. The exhaustive actual wall-omission split

Consider precisely these four possible omissions:

| Actual wall square | Its indicated ordinary auxiliary |
|---|---|
| Q9 | F2=(1.6,1) |
| Q10 | G8=(3,1.6) |
| Q11 | F7=(2.4,3) |
| Q8 | G1=(1,2.4) |

Each indicated point either belongs strictly to that actual wall
square or is omitted from it. The number of these omissions is
therefore an exhaustive integer in {0,1,2,3,4}, including every
point-on-face possibility.

Section 7 of C1092-MPPM-MIXED-WALL-CENTER.md proves the following
literal consequences throughout the complete original entrance:

| Indicated wall omission | Actual central forced to contain O=(2,2) strictly |
|---|---|
| F2 omitted from Q9 | Q5 |
| G8 omitted from Q10 | Q6 |
| F7 omitted from Q11 | Q7 |
| G1 omitted from Q8 | Q4 |

Its proof first obtains the actual inward pair, the actual ordinary
neighbor and the actual mixed wall from the original owner lists.
Its continuous center and crosspoint arguments keep that mixed
wall's true center sign. Thus any two omissions put O strictly in
two distinct actual central squares, contradicting disjoint interiors.
This excludes every case with at least two omissions.

The complete theorem in
C1092-MPPM-ONE-OMISSION-CONTINUOUS-ENDING.md excludes exactly one
omission. Its simultaneous rotation reduces any such omission to
F2 absent from Q9. The proof supplies its own upper-core and top-origin
lemmas with the original mixed wall's correct center inequality before
applying any later local right-side theorem. It then excludes both
right-near alternatives and the remaining ordinary right component.
In particular its statement is for the entire original one-omission
family, with no prior reduced joint catalogue or unsupported wall
center sign.

It remains exactly zero indicated wall omissions. The original
wall-sign chord theorem supplies the complementary auxiliaries.
Consequently the actual wall pairs in this remaining branch are

    Q8:F1,G1; Q9:F2,G2; Q10:F8,G8; Q11:F7,G7.     (2)

This is precisely the no-omission entrance of
C1092-MPPM-NO-OMISSION-REDUCTION.md.

## 2. The no-omission central cover has no nonordinary case

The complete no-omission reduction uses (2) and the original central
covering alternatives. In each sector it gives the ordinary pair,
the inward pair, or the residual elbow alternative. Ordinary and
inward ownership may overlap; an owner with both pairs is counted
as ordinary.

Theorem 1 of C1092-MPPM-INWARD-CONTINUOUS-ENDING.md proves that
every actual central in this entrance owns its ordinary pair:

    Q4:F0,G0; Q5:F6,G5; Q6:F9,G9; Q7:F3,G4.      (3)

Its source chain is exhaustive. The residual elbow theorem removes
every elbow. A genuinely nonordinary inward owner forces an inward
opposite and two ordinary neighbors; the single-inward alternative
has its own complete ending. For the two opposite inward owners,
at most one can strictly contain O. The centered inward ending
excludes either centered case, and the opposed-missing inward ending
excludes the case where both omit O. Thus every possible inward
center status and outer-point alternative has been treated.

We may therefore retain the full OOOO entrance (2),(3), together
with its original corners, markers, walls and center signs. Nothing
in this step excludes extra inward auxiliary ownership from an
ordinary square.

The four forward points and four actual crosspoints in that entrance
are

| Actual central | Its designated forward point | Its crosspoint |
|---|---|---|
| Q4 | G3=(1.74,2) | (1.5,2) |
| Q5 | F4=(2,1.74) | (2,1.5) |
| Q6 | G6=(2.26,2) | (2.5,2) |
| Q7 | F5=(2,2.26) | (2,2.5) |

Retained forward membership means strict ownership in the owner
shown in this table. Every other membership is an omission from
that indicated owner only. The two sign arguments below exhaust
all such memberships, not merely the historical final assignment.

## 3. Every ordinary sector with a nonpositive central is excluded

Theorem 1 of C1092-MPPM-CENTRAL-SIGN-REDUCTION.md excludes every
configuration in the full OOOO entrance with at least one nonpositive
central canonical angle. It retains every ordinary/inward overlap
and every forward membership.

For clarity, its exhaustive sign count uses the following complete
endings. Let n be the number of strictly positive canonical angles.

| n | Completed continuous theorem |
|---|---|
| 0 | C1092-MPPM-ALL-NEGATIVE-MIXED-FORWARD-ENDING.md, Theorem 1 |
| 1 | C1092-MPPM-ONE-POSITIVE-CONTINUOUS-ENDING.md, Theorem 1 |
| 2 | C1092-MPPM-TWO-POSITIVE-CONTINUOUS-ENDING.md, Theorem 1 |
| 3 | C1092-MPPM-POSITIVE-NEGATIVE-RETAINING-SHALLOW.md, Corollary 3 |

The common actual inputs include universal exclusion of each central's
preceding wall origin and strict positive crosspoints. Each nonpositive
central independently supplies its own outer halfpoint and the origin
of its own following actual wall. Its ordinary neighbor supplies the
far endpoint of that same wall's strict bar. Thus the mixed-sign
proofs use genuine complete bars in their stated owners, without
presuming that every wall origin is available at once.

The key new transition theorem makes a retaining negative recipient
of a positive predecessor satisfy tan q<1/4 and H<.086, whenever
its next actual crosspoint is foreign. Its exact support envelope
and strict whole-bar clearance give that bound on the same actual
negative square. The local shallow-successor comparisons then close
all mixed sign runs. The count in the table covers n=0,1,2,3;
zero canonical angles are included in the nonpositive alternatives
and ruled out by their genuine strict-point/face comparisons.

It remains only n=4, the all-positive OOOO entrance.

## 4. The all-positive actual wall-center cycle is impossible

The completed
C1092-MPPM-POSITIVE-RETAINING-ANGLE-AND-ORIGINS.md gives the
simultaneous all-positive entrance. Every central has its strict
crosspoint and outer halfpoint, and every actual wall has its own
strict origin. In a central's southwest chart write its positive
frame as (c,s),(-s,c), its lower faces as U,V and its upper faces
as A=U+a,K=V+a. The simultaneous actual bounds are

    U>=-c-s, V>=.56s-c, K<=s,
    A<=-.26c when forward is missing,
    A<=-.5s and tan(p/2)<1/4 when forward is retained.  (4)

Theorem 1 and Sections 7--8 of
C1092-MPPM-SHALLOW-POSITIVE-WALL-ORDER.md now supply the complete
all-positive ending. Its scalar companion is
C1092-MPPM-SHALLOW-POSITIVE-WALL-ORDER-SCALARS.md.

For a retained forward point, the local theorem keeps the central
square and its two actual adjacent walls B,L together. If xB is
the actual bottom-wall center abscissa and yL is the actual left-wall
center ordinate in that central's chart, it proves

    xB+yL>0.                                      (5)

Its two support comparisons retain the same central upper face K.
In particular the actual strict preceding origin supplies an extra
bound on K in a boundary-supplied separating direction. That bound
is combined with the bottom envelope before K is eliminated. The
two continuous scalar lemmas include all boundary angles, relative
angle orders, coordinate endpoints and aligned axes.

For a missing forward point, Corollary 3 of
C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md gives the same (5).
Its hypotheses are literal in the all-positive entrance: ordinary
marker and pair, strict outer halfpoint, actual paired corner,
genuine preceding wall origin, stated forward omission and the
actual far bottom segment. The origins and the simultaneous faces
needed for this application were proved before the wall comparison.

Here is the exact cancellation on the original four actual wall
centers. In cyclic order at Q4,Q5,Q6,Q7, the two terms in (5) are

| Central sector | Its xB | Its yL |
|---|---|---|
| Q4 | X_Q9-2 | Y_Q8-2 |
| Q5 | Y_Q10-2 | 2-X_Q9 |
| Q6 | 2-X_Q11 | 2-Y_Q10 |
| Q7 | 2-Y_Q8 | X_Q11-2 |

Every row is strictly positive by the actual theorem applicable to
that central's forward membership. Their sum is exactly zero.
Thus (5) at all four sectors yields 0>0. This excludes the complete
all-positive OOOO family, including every mixture of retained and
omitted forward points.

## 5. Completion and precise inherited scope

The wall-omission count in Section 1 is exhaustive. At least two
omissions contradict the actual common-center theorem, exactly one
contradicts its continuous ending, and zero omissions enters (2).
Within that no-omission entrance, Section 2 forces (3). Sections
3--4 then exclude every possible sign count for those four actual
ordinary central squares. No branch remains. Theorem 1 follows. ∎

The conclusion uses the original bound 1<a<=1001/1000 and the
original exhaustive marker/ownership entrance, exactly as stated
at the start. Local proofs that permit larger a were used only
within that inherited range. The proof distinguishes strict point
ownership from a weak excluded face at every case split, retains
the original real container walls and center conditions, and treats
each shared boundary center as one actual coordinate in both
neighboring sectors.

This completes the MPPM representative in the retained original
sixteen-wall-sign cover. Together with the completed MMMM and MMMP
continuous endings and the retained opposite-pair MMPP theorem,
it supplies the final original C1092 wall-class ending. It replaces
the previously open MPPM ending obligation; it does not replace
the initial exhaustive ownership rule by a newly assumed assignment.
