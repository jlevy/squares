# C1090: a direct entrance, northeast selection, and two geometric endings

**Status: DONE_MATH.** This is a written exclusion of the C1090 marker family,
with an exact finite entrance and explicit transfers to the recovered continuous
geometric lemmas. It replaces the historical continuation rather than completing
its 531 missing dependencies. No Lean theorem, compilation, axiom audit, or
repository integration is claimed.

The main new reduction is that two actual wall bars force the northeast square
to own G7=(2.26,3). This determines the top square's auxiliary orientation before
any wall-center split. Starting with 154 complete auxiliary assignments, seven
necessary deductions leave four assignments, covered by two all-angle profiles.
The proof uses **zero wall-center sign splits**; its continuous terminal lemmas
still treat both canonical square-angle signs, including all endpoints.

Read this chapter in order. The three accompanying proof chapters are
[the merged-left seed](proofs/MERGED-LEFT-SEED.md),
[the northeast selection lemma](proofs/NE-SELECTION-LEMMA.md), and
[the explicit residual ending](proofs/RESIDUAL-ENDING.md).
All cited older local geometric proofs are included unchanged in
[the shared recovered library](../C1089/reference/recovered-lemmas/).

## 1. Exact theorem and actual owners

Let twelve actual congruent open squares have common side

    1 < a <= 1001/1000,

pairwise disjoint interiors, and closures in [0,4]^2. They can rotate
independently, and boundaries may touch. Suppose their exact marker masks are

    {1,12,48,192,256,512,1024,2048,4098,8192,16384,32768}.

**Theorem.** Such a packing does not exist.

Order the actual owners by their masks. Every decimal in this package is an
exact rational, not a rounded coordinate. Strict membership is always interior
membership; an excluded point can be on the square's boundary.

| Owner | Mask | Original strict marker(s) | Name |
|---|---:|---|---|
| Q0 | 1 | (1,.914) | southwest singleton |
| Q1 | 12 | (3,.914), (3.086,1) | southeast paired corner |
| Q2 | 48 | (3,3.086), (3.086,3) | northeast paired corner |
| Q3 | 192 | (1,3.086), (.914,3) | northwest paired corner |
| Q4 | 256 | (1.65,1.65) | A |
| Q5 | 512 | (2.35,1.65) | S |
| Q6 | 1024 | (2.35,2.35) | E |
| Q7 | 2048 | (1.65,2.35) | N |
| Q8 | 4098 | (.914,1), (.914,2) | L |
| Q9 | 8192 | (2,.914) | B |
| Q10 | 16384 | (3.086,2) | R |
| Q11 | 32768 | (2,3.086) | T |

In particular L is ONE square owning both markers 1 and 12. Marker 1 is not
missing from the packing. It is outside Q0 because the exact mask of Q0 is 1,
not because it is globally unowned. Q0 remains a singleton and never receives
the southwest paired-corner point without a proof.

The supplied CoverData has 577 raw rows, some placeholders; row 574 has original
ID 1090 and the family above. These are not 577 retained case IDs. The
[extracted row identities](reference/CoverData-row-identities.json) preserve
all raw positions, and the checker verifies that row 574 is the unique row with
ID 1090. Thus the mathematical family exclusion applies to every retained row
with this ID. This is textual row-identity checking, not formal row assembly.

Define the auxiliary arrays:

    F0=(1,1.74)  F1=(1,2.26)  F2=(1.6,1)  F3=(1.6,3)
    F4=(2,1.74)  F5=(2,2.26)  F6=(2.4,1)  F7=(2.4,3)
    F8=(3,1.74)  F9=(3,2.26)

    G0=(1,1.6)   G1=(1,2.4)   G2=(1.74,1) G3=(1.74,2)
    G4=(1.74,3)  G5=(2.26,1)  G6=(2.26,2) G7=(2.26,3)
    G8=(3,1.6)   G9=(3,2.4).

An auxiliary label m records all strict auxiliary memberships of that owner:
bit j is Fj, and bit 10+j is Gj. An omitted auxiliary is excluded from that
particular open square; omission alone does not supply another owner.

## 2. A complete entrance from the original packing

We reconstruct a necessary entrance directly. We do not assume a saved terminal
pose box or run a historical polygon propagation to obtain the conclusion.

### 2.1 Strict seeds and walls

The exact southwest singleton signature and its real walls give Q0 the three
strict seeds

    (1.12,1), (1.74,1), (1.87,.76).

This is the horizontal singleton seed, not its transpose. The proof and exact
identity checks are in the unchanged
[FOUNDATIONAL-ENTRANCE](../C1089/entrance/FOUNDATIONAL-ENTRANCE.md), using the
same mask-1 singleton input as here. Its nonownership of marker 1 is valid
because that marker belongs to distinct actual L.

The three paired-corner lemmas give (3,1) in Q1, (3,3) in Q2, and (1,3) in Q3.
The genuine merged L and its left wall give

    {1} x [1.25,1.75] strictly in L.                      (2.1)

A self-contained proof is in [MERGED-LEFT-SEED](proofs/MERGED-LEFT-SEED.md).
It uses the two original L markers together, not two independently movable
owners. It also proves 1.29<Y_L<1.71 for the center, but no subsequent step
uses a split or an assumed sign of that center.

### 2.2 Exact local reduction and coverage

Apply the proved marker-to-auxiliary covering alternatives and convex-hull
exclusions in [LOCAL-RULE](../C1089/entrance/LOCAL-RULE.txt), with the actual
owner set above. The exceptional paired-corner owners are exactly Q1,Q2,Q3.
All other owners, including merged L, retain the actual strict seeds and the
complete local covering alternatives. The standard slack-one bookkeeping and
small local impossibility tests delete only necessary-impossible labels.
Disjointness eliminates shared auxiliary bits between different owners.

The actual replay is [replay_c1090.py](checks/replay_c1090.py). It reuses the
unchanged exact rational engine, substitutes the correct merged marker group
and its proved seed segment, and regenerates, rather than trusts, the
[component labels](entrance/COMPONENTS.json),
[common hulls](entrance/COMMON-HULLS.json), and
[complete auxiliary assignments](entrance/ADMISSIBLE-VECTORS.json).

The twelve component counts are

    1, 2, 3, 6, 6, 5, 13, 25, 3, 2, 3, 10,

summing to **79 labels**, with **154** complete compatible assignments. They
match all twelve entrance component lists and hulls in the recovered historical
record. Only its entrance is used; its claimed 188-step continuation is not
part of this proof or verification receipt.

For comparison only, every reconstructed C1090 component and assignment also
occurs in the earlier C1089 entrance. This is auxiliary-data subsumption, NOT
an equality of marker families. We do not apply a C1089 family-exclusion theorem
to C1090. Every later transfer has its actual input owners shown.

The bitwise compulsory labels at this entrance are

    Q0:4100, Q1:0, Q2:0, Q3:0, A:8208, S:256,
    E:0, N:0, L:1025, B:32832, R:524800, T:0.

In words, Q0 owns F2,G2; A owns F4,G3; S owns F8; L owns F0,G0;
B owns F6,G5; R owns F9,G9. Zero here means no compulsory auxiliary bit,
not an empty physical square or absent marker.

## 3. Fixed bars, southwest crosspoints, and S's lower right point

### 3.1 Two genuine wall bars

Apply Theorem 4 of
[C981-WALL-CYCLES](../C1089/reference/recovered-lemmas/C981-WALL-CYCLES.md)
in its transposed bottom-wall chart to B. The strict inputs are B's original
marker and F6. The exclusions are G2 and (1.87,.76) in Q0 and the SE marker in S;
the wall is B's actual bottom wall. It gives (2.8,1) strictly in B. Since B
also owns G5, convexity gives the whole strict bar

    I_B=[2.26,2.8] x {1} in B.                           (3.1)

Theorem 1 of
[C974-C976-CONTINUOUS-REDUCTIONS](../C1089/reference/recovered-lemmas/C974-C976-CONTINUOUS-REDUCTIONS.md),
reflected in x=2, applies to R with its marker,G9 and actual right wall.
Its exclusions are F8 in S and the NE marker in E. It gives (3,2.56), hence

    I_R={3} x [2.26,2.56] in R.                          (3.2)

Each whole bar lies in one actual owner. Neither is formed by joining endpoints
from different squares.

### 3.2 Two crosspoints in A

Use the central-crosspoint theorem appended to
[C893-CONTINUOUS-EXCLUSION](../C1089/reference/recovered-lemmas/C893-CONTINUOUS-EXCLUSION.md)
after a half-turn about (2,2). Its strict anchors become A's marker,F4,G3;
its two foreign central markers are in S,N; its two lower left exclusions
(1,1.6),(1,1.5) lie in actual L by (2.1). It gives

    (2,1.5) strictly in A.                              (3.3)

Transpose the entire local application. The required lower points now are
(1.6,1),(1.5,1), both in Q0's strict horizontal seed segment. Thus

    (1.5,2) strictly in A.                              (3.4)

### 3.3 S necessarily owns G8

S's G-covering alternative is G6 or G8, because G5 is in actual B. If S
omitted G8, it would own G6. Theorem 1 of
[ELBOW-CROSSPOINT](../C1089/reference/recovered-lemmas/ELBOW-CROSSPOINT.md)
would apply to its marker,G6,F8 and excluded G8, E's marker, R's marker. It
would put (2,1.5) strictly in S, contradicting (3.3). Therefore S owns G8.
Its remaining labels are

    S in {262400,327936,327968}.                         (3.5)

The 154 complete assignments reduce to 118. B's optional G8 is also excluded,
so B is exactly 32832. No angle or wall-center assumption entered this step.

## 4. New selection: E owns G7, and G6 in E forces F7 in E

Apply [NE-SELECTION-LEMMA](proofs/NE-SELECTION-LEMMA.md) to actual S,E.
Its whole lower bar is (3.1), its corner points (3,1),(3.086,1) belong to Q1,
its right marker belongs to R, and its foreign NW marker belongs to N.
Its F9,G9 exclusions are strict in actual R. The two NE covering alternatives
are precisely F5 or F7 and G6 or G7, since F9,G9 are foreign.

The lemma proves, for every original packing reaching the entrance,

    G7 in E, and (G6 in E implies F7 in E).              (4.1)

Its proof combines two duplicate-point pairs and a six-point mixed-span
obstruction. Whenever E owns G6, the actual lower bar locks S's canonical
angle negative; this is a derived angle fact, not an assumed branch.
Neither T nor any top/left wall-center sign is required.

The 118 assignments reduce to 52. This deduction is the principal simplification:
it makes a top-wall center split unnecessary.

## 5. T and N are forced to the left top profile

Since G7 belongs to E, it is excluded from T. Every surviving T component
then contains F3,G4. N's G-covering alternative is G1,G3 or G4; G3 is in A and
G4 is now in T. Thus N owns G1. T cannot additionally own G1, leaving

    T in {16392,16424} = {F3,G4}, with optional F5.       (5.1)

Suppose N omitted F1. Its F-covering alternative is F1,F3 or F5. F3 is already
in T, so N would own F5. Apply the half-turn of
[MIXED-SPAN-FOUR-POINTS](../C1089/reference/recovered-lemmas/MIXED-SPAN-FOUR-POINTS.md).
Its strict points become F5,G1; its four excluded points become
G3,F1,G4,F3. Here G3 is in A, G4,F3 in T, and F1 is the assumed omission.
The theorem gives a contradiction. Hence

    F1,G1 strictly in N.                                (5.2)

This needs no top advance, top-center sign, or two-gap lemma. Filtering (5.2)
reduces 52 assignments to 37. N is 2050 or 2082, and L is now exactly1025.

The same uniform wall theorem used for (3.2), under (x,y)->(4-y,4-x), applies
to T. Its strict anchors are its original marker,F3; its exclusions G7 in E
and the NW marker in N; its wall is the actual top wall. Thus

    (1.44,3) in T, and [1.44,1.74] x {3} in T.           (5.3)

Apply [ORDINARY-MARKER-HALFPOINT](../C1089/reference/recovered-lemmas/ORDINARY-MARKER-HALFPOINT.md)
to N via (xi,eta)->(2-xi,2-eta). Its strict anchors are N's marker,F1,G1;
its excluded points are G3 in A, (.914,2) in L, (1,3) in Q3, and G4 in T.
It gives (1,2.5) strictly in N.

Theorem 7 of
[C1092-DIRECT-WALL-POINT](../C1089/reference/recovered-lemmas/C1092-DIRECT-WALL-POINT.md),
reflected in y=2 with b=.914 and ell=1.74, now applies to actual Q3,T.
Q3 owns (1,3.086),(1,3), excludes the new N point, and has its real two corner
walls. T owns its original marker,G4 and has its real top wall. Therefore

    (2,3) in T, and I_T=[1.44,2] x {3} in T.             (5.4)

All top-origin prerequisites have been derived from the original packing.

## 6. The optional top F5 is impossible

Suppose T owns F5. Its own strict segment from F5 to its original marker
contains {2} x [2.26,3.086]. E must omit F5. In view of (4.1), the surviving
E labels without F5 are131200 and196736, both owning F7,G7.

Theorem 1 of
[C981-COMMON-CYCLE](../C1089/reference/recovered-lemmas/C981-COMMON-CYCLE.md)
applies to E. Its excluded (2,2.4),(2,3) belong to T's single vertical segment;
(3,2.4),(3,2.56) belong to actual R; (3,3) belongs to Q2. It gives (2,2.65)
strictly in E and in T, a contradiction. Consequently

    T=16392={F3,G4}.                                    (6.1)

There remain32 complete assignments. The possible NE labels are now

    E in {131104,131200,131232,196736,196768}.            (6.2)

## 7. Five structural exclusions reduce the central pair to two profiles

The following local continuous reductions are the explicit ones in
[C1089-REVERSE-CYCLIC-ENDING, Section4.2](../C1089/reference/recovered-lemmas/C1089-REVERSE-CYCLIC-ENDING.md).
We use their literal antecedents, not that case's marker-family theorem.
The full proofs of the local lemmas in the next table are retained, and every
additional prerequisite is established in Sections2-6 above.

The common actual-input ledger is:

| Input required by a local reduction | Actual C1090 source |
|---|---|
| SW marker,F4,G3,(2,1.5),(1.5,2) | A |
| SE and NE original markers | S,E |
| Foreign NW original marker | N, not an absent marker |
| Whole lower bar I_B | B by (3.1) |
| Whole right bar I_R | R by (3.2) |
| Right original marker | R |
| Top original marker and (2,3) | T by (5.4) |
| (3,1),(3.086,1) | the single paired corner Q1 |
| (3,3) | paired corner Q2 |

The eliminations proceed in this order:

| Alternative | Geometric contradiction with the above ledger |
|---|---|
| E=131104={F5,G7} | Theorem1 and its quarter-turn in ELBOW-CROSSPOINT give (2.5,2),(2.525,2.125) in E. If S is outward262400, the actual bar forces the latter point in S. Otherwise S owns G6, and crossed-elbow Theorem2, with A's (2,1.5) and B's (2.8,1), forces the former point in S. |
| E=196736={F7,G6,G7} | Theorems1-2 of OUTWARD-BAR-AND-UPPER-SPAN give (2.525,2.125) in E and in S. E's G6 forces S to be outward262400; E's upper-span inputs use the actual top origin and NE corner. |
| S=327968={F8,G6,G8,F5} | ELBOW-CROSSPOINT Theorem3 gives (2.525,2.125) in S using its marker,G6,F8,F5 and excluded A crosspoint. E must omit F5,G6, so only131200 remains. Theorem3 of OUTWARD-BAR-AND-UPPER-SPAN gives the identical point in E. |
| S=262400 and E=131200 | Theorems1 and3 of OUTWARD-BAR-AND-UPPER-SPAN again duplicate (2.525,2.125), using the actual lower bar, top origin, right bar and NE corner. |
| S=262400 and E=131232 or196768 | The complete two-square theorem in C974-C976-OUTWARD-PAIR applies. Its genuine S angle and two faces follow from I_B. E owns its marker,F5,G7 and excludes N's actual marker,T's origin,Q2's corner. The theorem rules out all actual-square separating supports. |

The three source chapters, with proofs, are
[ELBOW-CROSSPOINT](../C1089/reference/recovered-lemmas/ELBOW-CROSSPOINT.md),
[OUTWARD-BAR-AND-UPPER-SPAN](../C1089/reference/recovered-lemmas/OUTWARD-BAR-AND-UPPER-SPAN.md), and
[C974-C976-OUTWARD-PAIR](../C1089/reference/recovered-lemmas/C974-C976-OUTWARD-PAIR.md).

For clarity, the last row's derived S support data, in (xi,eta)=(x-2,y-2),
are the negative frame with

    13/87 < s/(1+c) < 143/500,
    U+a <= c+s,   V >= -c+.8s,
    (.525,.125) strictly in S.

They come from the actual excluded whole bottom bar, not from a pose enclosure.
Their exact origin and the complete eight-directed-support treatment are given
in the cited bar and coupled-support proofs. Square tangency remains allowed.

The first two rows reduce32 assignments to18; the third to17; the last two
together leave4. S is now327936, so G6 is in S and the remaining NE label196768
is also excluded by disjointness. Therefore the only central profiles are

    (S,E)=(327936,131200) or (327936,131232).             (7.1)

The four complete remaining vectors, in Q0,...,Q11 order, are

    4100,0,0,0,8208,327936,131200,2050,1025,32832,524800,16392
    4100,0,0,0,8208,327936,131200,2082,1025,32832,524800,16392
    4100,0,0,0,8208,327936,131232,2050,1025,32832,524800,16392
    4100,0,0,0,8240,327936,131200,2050,1025,32832,524800,16392.

This is complete compatible-assignment coverage, not a claim that any of these
vectors is geometrically realizable.

## 8. Every one of the four remaining vectors is impossible

Apply the theorem of [RESIDUAL-ENDING](proofs/RESIDUAL-ENDING.md).
Its antecedent is written as an explicit table of strict points and whole
segments in the SAME twelve actual owners, with no wall-center or assumed
angle premise. All its inputs have just been proved:

* A has its two crosspoints; N has F1,G1; L has its strict vertical seed.
* B,R,T have their actual bars, and T has the top origin.
* S has F8,G6,G8; E has F7,G7 and optionally F5, exactly as in (7.1).
* Q0 keeps the horizontal singleton seed; Q1,Q2,Q3 keep their genuine corner
  points. No extra southwest corner or fictitious owner is introduced.

The chapter derives additional central points, an actual bottom origin, and
A's support point(1.27,1.96). These force N's positive frame to satisfy

    2/3 < h/l < 8/11,

and force (1.28,3),(1.4,3) strictly in N. Either nonnegative NE profile then
makes T own a point of N's upper segment. For a negative NE angle, the actual
NE/top support theorem forces T's remaining angle to have

    0 < tan(beta) < 2/3.

The actual N/T support obstruction excludes that entire range. All points,
segments, coordinate charts, and foreign owners are displayed in the chapter.
The canonical angle endpoints and weak separating equalities are retained.
Thus both profiles and all four assignments are impossible. The C1090 theorem
follows. End of the mathematical exclusion.

## 9. What was simplified, and what has been checked

This route replaces the proposed incomplete continuation altogether. It does
not certify any missing historical operation, assume an unreached terminal,
or count a small instruction list as a small proof. It retains the actual
merged owner4098 throughout.

The mathematical changes are the direct merged-owner entrance, the early
NE-selection lemma, the immediate deduction of T's F3,G4 and N's F1,G1, and a
literal transfer to two already proved local profiles. There is no wall-center
branch tree and no numerical angular enumeration. The shared analytic lemmas
are reused, not advertised as newly discovered or newly formalized.

Reproduce the exact checks from this directory with Python3.10+:

    python3 -B checks/replay_c1090.py
    python3 -B checks/check_reduction.py
    python3 -B checks/check_geometry_inputs.py
    python3 -B checks/run_checks.py

Only the Python standard library is required. The first script recomputes the
entrance, including its complete label catalogue and original-packing seeds;
the second recomputes the finite consequences of the SEVEN proved necessary
filters and checks the four-profile coverage. The third verifies literal
coordinate maps, same-owner segment tests and exact rational inequalities.
The test harness runs all three normally and with Python optimization enabled,
and checks that deliberately damaged inputs are rejected.

The reduction receipt's counts are

    154 -> 118 -> 52 -> 37 -> 32 -> 18 -> 17 -> 4.

The final contradiction is the written all-angle proof in Section8, NOT an
extra machine filter asserted to make4 become0. The scripts do not verify
all real-variable lemmas of the recovered library. This is mathematical
completion with explicit reused proofs and exact supporting checks; formal
acceptance and integration remain for a subsequent Lean task.
