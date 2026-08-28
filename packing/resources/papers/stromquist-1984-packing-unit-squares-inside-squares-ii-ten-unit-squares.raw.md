DANIEL H. WAGNER, ASSOCIATES (450)

H. R. RICHARDSON, MANAGER PAOLI OFFICE HOTRS.,PAOLI, PA
SARRY BELKIN, TECHNICAL niRecTOR DANtEL H. WAGNER, Pres.
SCOTT S. BROWN, SR. ASSOCIATE

ROBERT P. BUEM!, SA. ASSOCIATE STATION SQUARE ONE YORKTOWN OFFICE

18907 GEO. WASHINGTON HWY.
YORKTOWN, VA 23692

(215) 644-3400 (804) 898-7700
JOSEPH H. DISCENZA, mar.

LARRY K. GRAVES, $f. assoctate PAOLI, PENNSYLVANIA [930!
WALTER R. STROMQUIST, sR. assSocrATE
CAROL R. HOPKINS, SR. SOFTWARE ANALYST
KATHLEEN M, SOMMAR, SR. SOFTWARE ANALYST (800) 345-1252
RICHARD H. CLARK, SOFTWARE ANALYST SUNNYVALE OFFICE

October 15, 1984 1270 OAKMEAD PARKWAY

. SUITE 314
SUNNYVALE, CA 94086
(408) 732-8393

INTERNAL MEMORANDUM STANLEY J. BENKOSKI, Man.

WASHINGTON OFFICE
SUITE IW
. . 50! CHURCH STREET, N.E.
To: 450 File (Professional Leave) VIENNA, VA 22180
(703) 938-2032
LAWRENCE D. STONE, wGR.

From: W. R. Stromquist BERNARD J. McCABE, FIELo oR,

Subject: Packing Unit Squares Inside Squares, II (Ten Unit Squares)

This memorandum is the second of a series on the following general problem:
For which values of n and s can n unit squares be packed inside a square of side
s? The first memorandum, reference [a], dealt primarily with the case of n = 6,
and also settled the remaining cases withn < 9. This memorandum addresses
the case of n= 10. We will prove that ten unit squares can be packed inside
a square of side s = 3 + 2/2 = 3.707, but not inside any smaller square.

Three different packings of ten unit squares in a square of side s = 3 + #V2
are shown in Figure 1.

THREE PACKINGS OF TEN UNIT SQUARES

gs =3+472 ~3.707 g=3+3/2 s=3+4/72

CONSULTANTS: OPERATIONS RESEARCH, MATHEMATICS, SOFTWARE DEVELOPMENT

We will show that no packing of ten unit squares is possible if the bounding
square has side less than 3 + 4/2. Actually, we will prove an equivalent result,
that ten squares cannot be packed inside a square of side exactly 3 + 4/2, if
each of the smaller squares has side strictly greater than 1. Following reference
[a], we define a block to be the interior of any unit square of side (1 + €), where
0<e < 10-4. We will prove the following:

Theorem. Ten pairwise nonintersecting blocks cannot. exist in the interior

of a square of side s = 3+ 272.

The proof will be in Section 2, and will make use of lemmas presented in

Section 1.

1. Some Nonavoidance Lemmas

The four lemmas presented in this section are what are referred to in reference
[a] as "nonavoidance lemmas." Each lemma provides that if the center of a
block is in a certain region, then the block must have a nonempty intersection
with certain parts of the boundary of the region. All four lemmas are illustrated
in Figure 2.
The first two lemmas are proved in reference [a].

Lemma 1. Consider the square bounded by the lines x = 0, x =1, y=0,y=1.

Any block whose center lies on or inside this square, and which does. not intersect

either the x axis or the y axis, must contain the point (1,1). (See Figure 2a).

This is corollary 2 to lemma 1 of reference [a]. Clearly the lemma remains
valid if the lines x = 1, y = 1 are replaced by x = a, y = b, and the point (1,1)
is replaced by (a,b), provided a,b < 1.

Lemma 2. Consider a triangle whose sides. each have length at. most 1.

Any block whose center lies on or inside the triangle must contain one of the

vertices of the triangle. (See Figure 2b.)

This is lemma 2 of reference [a].

FIGURE 2

NONAVOIDANCE LEMMAS

Note: In each case, if the center of a block is in the shaded region,
the block must intersect one of the marked lines or points.

<1

—<

Figure 2a Figure 2b
(Lemma 1) (Lemma 2)
<2V2 - 2 =.828

97 1 7 75
Seen oererea?
< .96

Figure 2c Figure 2d Figure 2e
(Lemma 3) (Lemma 3) (Lemma 3)

Z

|

eel
+4V2=,853

wi
pls

loin

A

Figure 2f
(Lemma 4)

Lemma 3. Consider the quadrilateral R with vertices at (0,0), (0,1), (a,0),

(a,b). Suppose that

(1) a = 272-2 =.828 and b=1, or
(2) a = +472 = .853 and b = .97, or
(3) a = .96 andb=.75.

Then any block whose center lies on or inside R, and which does not intersect

the x axis, must contain one of the vertices (0,1) and (a,b). (See Figures 2c,

2d, and 2e.)

Proof. Part (1) is from reference [a], but an independent proof of all three
parts will be given here.

Let A = (0,1), and B = (a,b). In each case, the distance between A and B
is less than 1; therefore, any counterexample could not have two corners above
the line AB. By lemma 1, any counterexample must have one corner to the
left of x = 0, and one corner to the right of x= a. If there is a counterexample,
then without loss of generality it has a vertex on the x axis and has the point
A on its boundary, as in Figure 3. Let & be the angle between the boundary
of the block and the x axis, as shown in the figure.

Suppose that the block's upper boundary intersects the line x = a at the
point (a,y). We will show that even if 6 is chosen to minimize y, we have y > b,
showing that no counterexample is possible.

Figure 4 shows the derivation of the formula for y in terms of a and @:

1 1-a cos 6
+

=
'

y > f(@) =
l+cos 6 sin 0

FIGURE 3

GENERAL FORM OF ANY COUNTEREXAMPLE TO LEMMA 3

A= (0,1) B = (a,b)

Cn nme nee em

x=0 =a

FIGURE 4

DERIVATION OF f(6) IN PROOF OF LEMMA 3

Note: The two triangles
marked * are congruent.

Since z+ =1
z= cosé ,
ca 8 .
nae a \ (a, Fe) we have
Sin
{ l-a tos O zazl- 1
b
1+cosé
2 so that
g £0) =1 1 + l-a cos6
* 6 1+cos6 sind
x _~
Qa

(We would have y = f(6) if we were dealing with a unit square, but since the
block is larger than a unit square, we have y > f(8).) To minimize f(6), we
set its derivative equal to zero:

(a-cos 6) (1+cos 6) - sin 6 (1-cos 6)

flo) = = 0. (1)

sin26@ (1+cos 6)

When 2/72 - 2 <a <1, equation (1) has two roots in [0°, 90°], and the smaller
of them (with 9 < 45°) is a local minimum for f(8). (In the interval [0,90°],
f(6) also has a local minimum at 6 = 90°, when f(6) = 1 > b.)

The relevant root of f'(6) can be found either by solving a cubic in (cos 9)
or by search. The following table shows the root 6, and the value of f(8), for

the relevant values of a.

6=
smaller root
a of eq. (1) f(6) db
(1) QV2 - 2 ~=.828 45° 1 1
(2) av2 + % = .853 39.514° 9722 .97
(3) -96 17.708° -7689 75)

Since f(@) > b in each case, the lemma is proved.

Lemma 4. Consider the pentagon with vertices at (.88, 0), (.88, .90), (1,1),

(2,1), and (2,0). Any block whose center lies on or inside this pentagon must

intersect either

(a) the x axis, or

(b) the segment joining (.88, .90) and (1,1), or

(c) the segment joining (2, 1) and (2, .788).


Proof. By lemma 1, any counterexample would need to include a point
to the right of the line x = 2. Without loss of generality, the block's boundary
includes a point on the x axis and the point (2, .788). See Figure 5. Let 6 be
the angle with the x axis, as shown.

If 6 > tan] (5/6) = 39.8°, then the block must contain the point (1,1).
To see this, we estimate the x~coordinate of the point (x,1) at which the block's

left boundary intersects the line y= 1. As shown in Figure 6, x is given by

sin 8 +cos 6-1
x = 2 - .212 tan 0 - ~ (2)
sin 8-cos6

The last term is derived in reference [a], where its absolute value is shown to
be at least .828, whatever the value of 8. The next-to~last term in (2) must
have absolute value at least (.212) (5/6) > .176. It follows that x < 2-.176 ~ .828 = .996,
so that the block's boundary passes to the left of (1,1) as claimed.
If 6 < tan7}(5/6) but 8 > cos"1(.9) = 25.8°, then the block must contain
the point (.88, .90). To see this, we compute the x-coordinate of the point (x, .90)
at which the block's left boundary intersects the line y = .90. By the same method

as in the previous paragraph, we obtain

FIGURE 5

GENERAL FORM OF ANY COUNTEREXAMPLE TO LEMMA 4

(8,90)


FIGURE 6

PROOF OF LEMMA 4: INTERSECTION OF BLOCK WITH LINE y = 1

212 tan O
nA )
ee!
sin@rcasQ-1 \(2,.788)

Sin Gass @

sin8 + cos6 -1
x=2-.212tan?d -

sin8 + cosé

FIGURE 7

CALCULATION OF x-COORDINATE IN PROOF OF LEMMA 4

(x,y)

(S225(.118)

, (2,0)

Siw 8 —__
3 @

sin 1
x= 2 +— (.788) - - sind
cosd cosé

sin 6 + cos 6 - .90

x = 2 - .112 tan 6 - -
sin 6 cos 9

This function of 6 reaches its maximum at 9 = 37.40°, when x = .87441. Thus,

the block's left boundary passes to the left of (.88, .90) as claimed.

If 6 < cos1(.9), we need to calculate the coordinates (x,y) of the block's

leftmost vertex. We have:

y = cos 9, and
788 sin 6 1
x = 2+ - - sin 96
cos 8 cos 8

where the last formula is derived in Figure 7. Since .9 < y < 1, the vertex

will be to the left of the segment if (1-x)/(1-y) > 1.2. We calculate:

. 1 - .788 sin 6
sin@ -1 + —————
1-x cos 8

1l-y 1- cos 8

If @ < 20°, we have (since cos @ < 1):

1-x sin -1+(1-.788 sin 6)

>
l-y 7 1- cos 6
sin 8
= (.212)
1 - cos 8
1 6 1+co
= (.212) (.212) —
sin sin


is

If 20° < 6 < cos7l(.9), simpler estimating techniques establish that i
~y

always greater than 1.6. Thus, the block has a vertex directly to the left of

the segment, and must intersect the segment. This completes the proof of

lemma 4.

2. Proof of the Theorem

In this section, s always represents the number 3 + z¥2. Consider the square
S bounded by the axes and the lines x = s, y=s. We will suppose that ten nonoverlapping
blocks are contained in the interior of $, and argue to a contradiction.

Consider the ten points A, B, .... J marked in Figure 8. As shown in the

figure, the coordinates of A, B, J are A = (1, 1), B =(5, .97), J = G, 1.4); the
other points are placed symmetrically in the square. We claim that any block
contained in S must contain one of these ten points. The proof is in Figure

9, where S is divided into regions, to each of which Lemma 1, 2, or 3 applies.

Since there are ten blocks and ten of these points, each block must contain
exactly one of the points. We will refer to the blocks by the points they contain;
e.g., the A-block, the B-block, etc.

The above reasoning would work just as well if I and J were replaced by
the points U = (1.4, s/2) and V = (s - 1.4, s/2) (Figure 10). Clearly points U and
V are contained in the L-block and J-block (in either order).

The same reasoning would also work if the point B in Figure 8 were replaced
by the point W = (s - 1.96, 0.75). The proof is as in Figure 9, the only difference
being that part 3 of Lemma 3 applies, rather than part 2. Therefore, the point
W must be contained in the B-block.

Now consider the eleven points marked in Figure 11: that is, points C through
J, point W, and the points (1, 1.2) and (.788, 1). By an argument similar to Figure
9, every block must contain one of these eleven points. The A~-block, therefore,

must contain one of the last two points.

~10-

FIGURE 8

J

TEN POINTS A,..

He

ec

1.4)

s
‘9?

J=¢

A=(1,1)

=, .97)

(

B=!

FIGURE 9

J

EACH BLOCK CONTAINS ONE OF A,..

-li-


FIGURE 10

POINTS U, V ARE CONTAINED IN THE I-,J-BLOCKS

®

s f
I
e

U

e 2 eo -¢
ey

@ e ¢

FIGURE 11

EVERY BLOCK CONTAINS ONE OF THESE ELEVEN POINTS

2
s
Hy
tr

FH
e e D

(1, 1.2) oJ
e .

e Cc
(.788, 1) °

W =(s~1.96, .75)

~12~

We now assert that the H-block must contain a point on the segment from
(1,2) to (.9, 2.12). This is easy to see if the A-block contains (1, 1.2); in that
case the H-block must contain (1,2). If the A-block contains (.788, 1), then
it contains the entire segment from (.788, 1) to (1, 1) and lemma 4 applies, as
shown in Figure 12.

In either case, the H~block must contain some point of the indicated segment.
In Figure 13, the -point of intersection is marked with an asterisk. Seven other
asterisks mark other points which must be contained in the B-, D-, F-, and H-blocks

by symmetrical arguments. Although we do not know the exact positions of

FIGURE 12

THE H-BLOCK MUST CONTAIN A POINT ON THE INDICATED SEGMENT

e @
Nun .
!
ed
2 9
— “ey 6B ©

-13-

FIGURE 13

EIGHT POINTS WHICH MUST BE CONTAINED
IN THE B-, D-, F-, AND H-BLOCKS

*® *”

<1 »@center
Ve” *
*

<

aN

FIGURE 14

EVERY BLOCK MUST CONTAIN ONE OF
THESE THIRTEEN POINTS, BUT EACH IS DENIED
TO THE I-BLOCK

G
rss Mn 4
4 \ f ‘4
* \ 2 ‘3

— we omy oe ~

aS Pe teeta
' - '
t

a oe Om KH a A ee oe oe
Al * j iC
{ .

i j
boy ,
b4 i

-14-

these points, we know that each asterisk is within 1 of the center of the square,
and within 1 of each of the two asterisks nearest to it.

Now, of the I- and J-blocks, both cannot contain the center of the square.
Without loss of generality, assume that the I-block does not contain the center.
Consider the thirteen points marked in Figure 14: these are the eight asterisks,
the four corner points A, C, E, G, and the center of the square. An application
of the lemmas as shown in the figure shows that every block must contain one
of these thirteen points, but all are denied to the I-block, and that is a contradiction,

which completes the proof of the theorem.

(Jaktir Stroma ust

Waiter R. Stromquist

WRS/megn
Reference
[a] Packing Unit Squares Inside Squares I (Six Unit Squares), Daniel H. Wagner,

Associates Internal Memorandum to 450 File by W. R. Stromquist, September
11, 1984.

-15-

