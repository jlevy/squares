# C1084: the ownership reduction used in the complete exclusion

**Updated status.** The two configurations isolated here are now both
excluded. Section 5 excludes the mixed-span configuration; the companion
C1084-DUPLICATE-POINT.md excludes the inward/outward configuration by
forcing one strict point into both actual central squares. The complete
argument retains the local ownership entrance stated in Section 2.

## 1. Two strict abscissa anchors force a long chord

Let Q be an open square of side a>1. Let h be a real number. If Q owns
one point whose abscissa is at most h-1/2 and another whose abscissa is
at least h+1/2, its vertical chord on x=h has length greater than one.
There is no assumption on the ordinates of these points or on the center.

To prove this, choose absolute canonical normal components c>=s>=0,
c^2+s^2=1, and let [x_-,x_+] be the closed horizontal projection of Q.
Strict ownership implies

    x_- < h-1/2,    x_+ > h+1/2.

Consequently

    min(h-x_-,x_+-h)>1/2>=cs.

For s>0 the chord length is the minimum of a/c and
min(h-x_-,x_+-h)/(cs). Both are greater than one. If s=0, the line is
strictly between the vertical sides and its chord has length a>1.
This includes equality in either stipulated anchor abscissa.

## 2. The four local alternatives for each central square

Use the original C1084 owner order from Chapter 04. The southeast central
owner is Q5; the northeast central owner is Q6. The supplied finite
ownership entrance has exactly the following necessary local alternatives:

| Owner | Label | Its strict auxiliary points |
|---|---:|---|
| Q5 | 65552 | (2,1.74), (2.26,2) |
| Q5 | 262160 | (2,1.74), (3,1.6) |
| Q5 | 65792 | (3,1.74), (2.26,2) |
| Q5 | 262400 | (3,1.74), (3,1.6) |
| Q6 | 65568 | (2,2.26), (2.26,2) |
| Q6 | 524320 | (2,2.26), (3,2.4) |
| Q6 | 66048 | (3,2.26), (2.26,2) |
| Q6 | 524800 | (3,2.26), (3,2.4) |

The labels specify exact auxiliary sets, not arbitrary selected subsets.
The original marker of Q5 is (2.35,1.65); that of Q6 is (2.35,2.35).
Both exclude the original right wall marker (3.086,2), which is owned by Q10.
These local alternatives are the established ownership entrance recorded in
`root_next/twenty_one_cases/C1084-complete-exclusion.txt`, Section 2, in the
recovered earlier collection. The argument below does not require its later
44-step geometric propagation, but it does retain this local ownership lemma.

## 3. Both mixed alternatives already give long chords

The preceding two-anchor theorem proves a chord longer than one on x=5/2
for Q5 in label 262160 and for Q6 in label 524320: the owned abscissae
are exactly 2 and 3.

For Q5 in label 65792, apply Theorem 1 of `OTHER-GEOMETRY.md` to the
simultaneous coordinate transformation

    (x,y) -> (3-x,y-2).

The actual owned point (3,1.74) becomes P=(0,-.26), the actual owned
point (2.26,2) becomes R=(.74,0), and the excluded original wall marker
(3.086,2) becomes E=(-.086,0). Thus the parameters are

    p=13/50,    d=43/500,    r=37/50,

and satisfy p>=d>0, d<=1/10, r>=29/40. The theorem gives a long chord
on transformed x=1/2, which is the original line x=5/2.

For Q6 in label 66048 use instead

    (x,y) -> (3-x,2-y).

Its point (3,2.26) becomes the same P, while (2.26,2) and (3.086,2)
become the same R and E. The same theorem proves its long chord.

Thus all four mixed alternatives in the table require no angle or center
analysis. Their long-chord conclusion is an actual physical consequence
of their strict points and the original wall-marker exclusion.

## 4. Exact reduction using the actual right wall owner

The established entrance gives Q10 precisely one of the labels

    262400: (3,1.74), (3,1.6),
    524800: (3,2.26), (3,2.4).

If Q10 has label 262400, its two points exclude the last three Q5
alternatives. Therefore Q5 must have label 65552, owning (2,1.74)
and (2.26,2). Its latter point then excludes labels 65568 and 66048
for Q6. The only remaining Q6 labels are

    524320 or 524800.

The first already has a long chord by Section 3. The second is the
outward pair (3,2.26),(3,2.4).

If Q10 has label 524800, the same disjoint-ownership argument gives
Q6 label 65568 and leaves Q5 labels 262160 or 262400. Reflection
in y=2 transports this entire alternative to the preceding one,
including the squares and their original marker groups.

Therefore, up to the actual container reflection, the central/right-wall
ownership analysis reduces to precisely two geometric configurations:

1. Q5 owns the inward pair (2,1.74),(2.26,2); Q6 owns the mixed pair
   (2,2.26),(3,2.4); Q10 owns the lower wall pair (3,1.74),(3,1.6).
2. Q5 owns the same inward pair; Q6 owns the outward pair
   (3,2.26),(3,2.4); Q10 owns the same lower wall pair.

The first configuration already supplies the Q6 chord. The second calls
for a coupled argument for Q5 and Q6, now supplied by the strict duplicate
point in the companion chapter. The outer Q9 and Q11 chords
are supplied in both configurations by Theorem 2 of `OTHER-GEOMETRY.md`.

## 5. The mixed-span configuration is impossible

Theorem 4 of C981-WALL-CYCLES.md applies to the C1084 bottom square
Q9 after transposing its local wall statement. Its strict anchors are
(2,.914),(2.4,1). The excluded points (1.74,1),(1.87,.76) belong to
the actual southwest singleton Q0, and (2.35,1.65) belongs to Q5.
Thus Q9 strictly owns (2.8,1), and hence the whole strict segment

    [2.26,2.8]×{1}.

Reflect this full argument in y=2, using the actual northwest singleton
Q3 and the northeast marker in Q6. It gives the strict top segment

    [2.26,2.8]×{3} ⊂ Q11.

Now consider configuration 1 from Section 4. Q6 has exact label 524320:
it owns (2,2.26),(3,2.4) and excludes (2.26,2),(3,2.26).
The first excluded point is also strict in Q5. The whole top segment
above is excluded from Q6 because its actual owner Q11 is distinct.

Reflect Q6 and all these premises in y=2. The strict anchors become
(2,1.74),(3,1.6), the isolated exclusions become (2.26,2),(3,1.74),
and the excluded segment becomes [2.26,2.8]×{1}. These are exactly
the premises of Theorem 5 of C981-WALL-CYCLES.md. Its continuous
contradiction excludes configuration 1 in full.

The reflected mixed-span possibility with Q5 label 262160 is excluded
by the identical application to Q5 and the actual bottom segment.
Thus neither mixed-span arrangement requires a remaining chord proof.

## 6. The inward/outward configuration is also excluded

The two-anchor theorem, the four mixed-label long-chord conclusions,
and the exhaustive reduction above are proved. The new two-anchor
obstruction also excludes configuration 1 completely.
They replace genuine parts of the ownership-specific reach analysis.
After Section 5, only configuration 2 remains up to reflection in y=2:
Q5 has label 65552, Q6 has label 524800, and Q10 has label 262400.

There is a further continuous sign restriction. Reflect the entire
configuration in y=2. The outward square Q6 then owns
(2.35,1.65),(3,1.6), and excludes (3,1), (3.086,2), (2.26,2), and
the whole actual bottom segment [2.26,2.8]×{1}. The reflected paired
corner Q2 supplies (3,1); the actual right wall Q10 supplies (3.086,2);
Q5 supplies (2.26,2); and the reflected actual Q11 supplies the whole
segment. Theorem 6 of C981-WALL-CYCLES.md therefore forces the
reflected Q6 angle to be strictly negative. Returning the whole
configuration to its original coordinates, the remaining Q6 has
strictly positive canonical angle. Axis alignment and the diagonal
orientation are excluded as part of that theorem.

Theorem 1 of C1084-DUPLICATE-POINT.md proves that Q5 strictly owns
K=(2.46,1.99) at every orientation, using its three actual anchors and
three genuine excluded points. Theorem 2 there proves that the now
positive-angle Q6 strictly owns the same K. Its extra exclusions come
from Q5, Q10, the actual top square Q11, and the actual northeast paired
corner Q2. That chapter identifies each of them explicitly.

Thus Q5 and Q6 have a strict common point, contradicting their disjoint
interiors. The simultaneous reflected alternative is excluded as well.
Together with Section 5, this completes the C1084 family under the
retained local ownership entrance. No remaining central chord bound is
needed for this new ending.
