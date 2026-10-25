# C983: the merged western square cannot reach the right auxiliary

All terminating decimals are exact rationals. Strict membership always
refers to the interior of the named actual square. Foreign points and
separating supports may be tangent. The physical squares have common
side 1<a≤1001/1000, disjoint interiors and closures in [0,4]².

## 1. The original owners and the conclusion

In C983 the actual owners are:

| Owner | Original role |
|---|---|
| Q0,Q1 | The two southwest singleton corners |
| Q2,Q3,Q4 | Paired southeast, northeast and northwest corners |
| Q5,Q6 | Southeast and northeast central squares |
| Q7 | The merged southwest–northwest central square |
| Q8,Q9,Q10,Q11 | Left, bottom, right and top wall squares |

**Theorem.** In every actual C983 configuration allowed by its retained
original ownership entrance, merged Q7 excludes G6=(2.26,2).

The proof uses three actual wall segments and one common southeast
support conclusion. Only two northeast alternatives remain: whether
Q6 owns F5. They are closed by previously proved continuous theorems
whose exact actual-owner premises are given below.

## 2. The forced ownership pattern under the contrary assumption

Suppose G6 is strict in Q7. The retained southeast labels avoiding
G6 are precisely

    262160={F4,G8}, 262400={F8,G8}, 262416={F4,F8,G8}.

The first alternative is impossible by
[MIXED-SPAN-FOUR-POINTS.md](MIXED-SPAN-FOUR-POINTS.md).
Its strict points A=F4=(2,1.74), B=G8=(3,1.6) belong to actual
Q5; D=G6 belongs to Q7; H=F8=(3,1.74) is excluded from the exact
label of Q5; and F=G5=(2.26,1), T=F6=(2.4,1) are strict in
actual Q9 under each of its retained labels32832,294976,32848.
Thus Q5 always owns both F8 and G8 in the remaining alternatives.

The only retained right-wall labels avoiding F8,G8,G6 are

    524800={F9,G9}, 524928={F7,F9,G9}.

Consequently Q10 owns F9=(3,2.26) and G9=(3,2.4). Northeast
Q6 must avoid G6,F9,G9. Its possible retained labels are

    131104,147488,147496,131200,131232,147616,147624.

Every one owns G7=(2.26,3), and every one owns F5 or F7. The
retained top labels avoiding G7 are16392 and16424, both owning
F3=(1.6,3) and G4=(1.74,3). Since these points now belong to
actual Q11, the three surviving northeast labels are exactly

    131104={F5,G7}, 131200={F7,G7}, 131232={F5,F7,G7}.

These are short deletions in the original local ownership families.
They do not enumerate twelve-square angle or center states, and no
unowned auxiliary has been treated as a point in a foreign owner.

## 3. Three wall consequences with their actual sources

### 3.1. The bottom square supplies the entire long bar

Actual Q9 owns its marker (2,.914), F6=(2.4,1), and
G5=(2.26,1). It excludes the southeast marker (2.35,1.65)
strict in Q5 and the two strict points

    (1.74,1), (1.87,.76) in actual singleton Q0.

The second singleton point is an original compulsory seed: for
an original-marker singleton0 the seed list contains
(28/25,1),(87/50,1),(187/100,19/25). Thus no additional
corner assumption is being introduced.

Transpose Theorem4 of
[C981-WALL-CYCLES.md](C981-WALL-CYCLES.md). Its actual lower
container wall and the listed strict and foreign points give
(2.8,1) strict in Q9. Convexity of that same actual owner gives

    [2.26,2.8]×{1} strictly in Q9.                    (1)

### 3.2. The actual northwest corner transfers the top origin

Q8 owns (.914,2) and G1=(1,2.4). It excludes F0=(1,1.74),
strict in singleton Q1, and the northwest marker (1.65,2.35),
strict in merged Q7. Theorem1 of
[C974-C976-CONTINUOUS-REDUCTIONS.md](C974-C976-CONTINUOUS-REDUCTIONS.md)
therefore gives (1,2.56) strict in Q8. Its strict point
(1,2.4) and convexity give (1,2.5) strict there too.

Paired northwest Q4 owns (1,3.086) and the compulsory strict
corner point (1,3), while excluding (1,2.5) from actual Q8.
Actual Q11 owns its marker (2,3.086) and F3=(1.6,3) by Section2.
Reflect this complete local configuration in y=2 and apply
Theorem7 of
[C1092-DIRECT-WALL-POINT.md](C1092-DIRECT-WALL-POINT.md), with

    K=Q4, B=Q11, b=.914, ell=1.6.

The reflected K closure lies in the first quadrant, the reflected
B lies above y=0, their actual interiors are disjoint and their
sides are the same. Every premise of the transfer is therefore
satisfied. Returning to the original coordinates gives

    (2,3) strictly in actual Q11.                     (2)

### 3.3. The right square supplies the upper vertical bar

Q10 owns (3.086,2), F9=(3,2.26) and G9=(3,2.4). It
excludes F8=(3,1.74) strict in Q5 and the northeast marker
(2.35,2.35) strict in Q6. Reflect Theorem1 of
`C974-C976-CONTINUOUS-REDUCTIONS.md` in x=2. It gives
(3,2.56) strict in actual Q10, and hence

    {3}×[2.26,2.56] strictly in Q10.                  (3)

Each segment in (1) and (3) is the convex hull of strict points
in one actual square. These whole segments are therefore foreign
to both central squares. The unrelated foreign exclusions have
not been joined to form artificial segments.

## 4. The southeast square has the common outward support

Actual Q5 strictly owns its marker M_S=(2.35,1.65) and
G8=(3,1.6). It excludes G6 from Q7, the compulsory corner
point (3,1) from actual Q2, the right marker (3.086,2)
from actual Q10, and the whole bar (1) from actual Q9.
Theorem6 of `C981-WALL-CYCLES.md` therefore puts Q5 in a
strictly negative canonical frame. This includes the exclusion
of both axial and diagonal sign ambiguities stated in that theorem.

Q5 also strictly owns F8=(3,1.74). Apply Theorem1 of
[OUTWARD-BAR-AND-UPPER-SPAN.md](OUTWARD-BAR-AND-UPPER-SPAN.md)
in coordinates (ξ,η)=(x−2,2−y). Its owned points are the
images of M_S,F8. Its four isolated exclusions are the images of

    G6=(2.26,2) in Q7,
    (3.086,2) in Q10,
    (3,1),(3.086,1) in actual paired corner Q2.

Its excluded whole segment is exactly the image of (1). All
these inputs concern the same physical configuration. On returning
to translated original coordinates (x−2,y−2), with Q5's frame
u=(c,−s), v=(s,c) and lower faces U,V, that theorem gives

    13/87<t=s/(1+c)<143/500,
    U+a≤c+s, V≥−c+.8s,                              (4)
    Y=(2.525,2.125) strictly in Q5.                  (5)

Optional ownership of F4 in the label262416 affects none of
the premises. In particular, no exclusion of F4 has been used.

## 5. Both northeast alternatives are impossible

Suppose first that Q6 excludes F5=(2,2.26). Section2 then
supplies its strict point F7=(2.4,3), in addition to its
original northeast marker. Theorem3 of
`OUTWARD-BAR-AND-UPPER-SPAN.md`, translated by (2,2), applies
to that actual Q6. Its other exclusions are (2,3) from actual
Q11 by (2), (3,3) from the paired corner Q3, and the whole
vertical bar (3) from actual Q10. The theorem gives the same
point Y=(2.525,2.125) strictly in Q6. This contradicts (5)
and the disjoint interiors of Q5,Q6.

Finally suppose Q6 owns F5. It also owns G7 by Section2.
Translate the two actual central squares by (−2,−2) and use
the coupled-support theorem of
[C974-C976-OUTWARD-PAIR.md](C974-C976-OUTWARD-PAIR.md).
For clarity, its complete inputs are:

| Local theorem input | Genuine C983 source |
|---|---|
| Southeast angle and face bounds | Equation(4) for actual Q5 |
| Southeast strict M_S=(.35,−.35), Y=(.525,.125) | Original Q5 marker and equation(5) |
| Northeast strict M_N=(.35,.35), F=(0,.26), G=(.26,1) | Original Q6 marker, F5 and G7 |
| Northeast excluded L=(−.35,.35) | Northwest marker, strict in actual merged Q7 |
| Northeast excluded P0=(0,1) | Top point(2,3), strict in actual Q11 |
| Northeast excluded P1=(1,1) | Paired northeast corner point(3,3), strict in actual Q3 |
| Common side and disjoint interiors | The original physical Q5,Q6 |

The theorem rules out their disjointness by exhausting all face
normal sources and proving two strict continuous support margins.
All its premises have just been established here, so this is
another contradiction.

Both possibilities for F5 have been exhausted. The assumption
G6∈Q7 is therefore impossible. ∎

## 6. Resulting merged-owner family

Combine this theorem with
[C983-MERGED-TOP-EXCLUSION.md](C983-MERGED-TOP-EXCLUSION.md).
Its remaining G6 labels73744,73760,73776 are now all excluded.
The necessary original Q7 family is reduced to the five labels

    8192,8208,8224,8240,24608.

Equivalently, Q7 owns G3 and may own F4 or F5; its only remaining
top extension is G4 with F5 and a strictly positive canonical angle.
This is a completed continuous elimination of the entire merged-G6
branch of C983. A whole-family ending for the five displayed
merged-owner possibilities remains a separate obligation.
