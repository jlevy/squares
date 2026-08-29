September 11, 1984

INTERNAL MEMORANDUM

To: 450 File (Professional Leave)

From: W. R. Stromquist
Subject: Packing Unit Squares Inside Squares, I (Six Unit Squares)

(450)

This memorandum is the first of a series of rough technical notes on the subject

of packing unit squares into squares. The general problem is the following: For
which values of n ands can n unit squares be packed inside a square of side s?
The unit squares may have any orientation, but the rules of packing require that
the interiors of the unit squares may not intersect, and may not extend outside
the boundary of the larger square.

This memorandum settles the case of n = 6, which is the smallest value of
n for which no complete solution has been published or announced. We establish
that six unit squares can be packed inside a square of side s = 3, but not inside
any smalier square. In subsequent memoranda we will settle the case of n= 10,
and provide partial results in the cases of n = 11 and some larger values of n.

It is intended that the several parts will eventually be combined into a single,
more cohesive, survey paper. In that paper the more tedious arguments may
be omitted. These memoranda, however, will present the proofs in the fullest
detail.

In Section 1 we present some preliminaries, including a reformulation of the

problem which will make it easier to discuss the key impossibility proofs. Section 2

contains a series of lemmas, mostly elementary, and also contains self-contained
solutions to the square-packing problem in the cases of n< 5. The proof of the

main result for n = 6 appears in Section 3.

1. Preliminaries

The best known packings of two, five, or six unit squares are illustrated in
Figure 1. In the cases of n = 2 andn = 5, these packings are known to be the
best possible. The proof in the case of n = 5 appears in reference [a]. The case
ofn=l1is trivial, and the cases of n= 3 andn = 4 are also trivial in view of the
result for n = 2. In this memorandum we will prove that the packing of six squares
in Figure 1 cannot be improved. This will settle the case of n = 6, and the cases
of n=7,n= 8, andn= 9 as well.

The discussion will be easier if, rather than considering a reduction in the

size of the bounding squares, we instead consider an increase in the size of the

squares being packed. In particular, we will prove that six squares cannot be

FIGURE 1

BEST PACKINGS FOR n= 2,n=5,n=6

s = Q+4¥2 & 2.707

\\\

=
il
ol
a
u
op)


packed inside a square of side exactly 3, if the sides of the six squares are each

greater than 1. For the remainder of this memorandum, we establish a fixed

value of e, satisfying
0< e< 10-4,

and we define a block to be the interior of a square of side (1 + €).

We will almost never refer explicitly to «, but we will rely on it implicitly.
The significance of « is that whenever a calculation seems to produce an inequality
which is not strict, we can appeal to the ubiquitous € to convert it into a strict
inequality. Notice that blocks are open sets. Although we may refer to the
corners and sides of a block, the boundary is not part of the block. Thus, there
is no ambiguity about whether two blocks intersect or whether a block is contained
inside a certain region.

We will prove the following:

Theorem. Six pairwise nonintersecting blocks cannot exist in the interior

of a square of side 3.

The proof will be in Section 3, and will make use of lemmas to be proved

in Section 2.

2. Lemmas and Intermediate Results

We present a series of lemmas, most of them elementary. Some of these
lemmas are what we will call "nonavoidance lemmas;" these lemmas provide
that if the center of a block is in a certain region, then the block cannot avoid
intersecting particular edger or corners of the region.

Lemma 1. If a block B is contained in the interior of a square S with side

s < 2, then B contains the center of the square (Figure 2a).

Proof. Consider Figure 2b, which contains a smaller square 8’, inscribed in
the boundary of B but with the same orientation as S. Distances x, y,S ', and

zZ are marked.

FIGURE 2

LEMMA 1 AND PROOF

S Cside 5 $2) S
B
a *
S'
We have:

x+y z= \
(sy
2 = 39) *(4) x Coy similarity of triangles ) ;

2 z
x * Y

Therefore 2* = (S') + 2xy + (ay
> (s')* + 2xy

= xPa yr sdxy

nt

(x+y)? > 1, so

z>\,

Thus, the right boundary of S' lies to the right of the center of S. Since similar

conculsions apply to the other sides of S', the center must lie inside S' and hence

in B. Thus, lemma 1 is proved.

Corollary 1: Two nonintersecting blocks cannot exist in the interior of a

square of side 2.

This corollary settles the original problem in the case n = 2, and hence in
the cases n= 3 andn= 4.

Corollary 2: Consider the square bounded by the lines x = 0, x= 1, y = 90,

y =1. Any block whose center lies on or inside this square, and which does not

intersect either the x axis or the y axis, must contain the point (1,1). (Figure

3a.)

Lemma 2. Consider a triangle whose sides each have length at most 1. Any

block whose center lies on or inside the triangle must contain one of the vertices

of the triangle. (Figure 3b.)

Proof. Consider the quadrants formed by the diagonals of the block, as in
Figure 4. (Each quadrant includes its boundary.) If all of the vertices of the
triangle lie in one quadrant or in two adjacent quadrants, then the triangle could
not contain the center of the block. In any other case, two of the corners must
lie in opposite quadrants, and if both were outside the block, they would be separated
by a difference of length greater than 1. Therefore, one of the corners lies in
the block, and the lemma is proved.
Now, let a satisfy t¥V2<a <1, and consider the configuration in Figure 5a.
One corner of a block is on the x axis, and exactly one corner is above the line
y =a. One side of the block makes an angle of 8 with the x axis (where 0° < 6 < 90°).
This configuration is possible only for certain values of a and 9; in particular,
it is possible only when a > max(sin®,cos 8). We wish to calculate the length
of the block's intersection with the line y = a. The calculation is accomplished

in Figure 5b; the result is

sin6 +cos6 -a
sin8 cos 8

f(6,a) =

y N

7

a )
“i


FIGURE 4

PROOF OF LEMMA 2

/

FIGURE 5

MEASURING THE INTERSECTION OF A BLOCK WITH A
CERTAIN LINE SEGMENT

* us $in8-2c050-0 jor?
ya 1 C)
Ls ——! Ne _
A w
(“Kes 8
° Vein
Fed fe Orios O-@
Qa co. 8 Sin Ocos B
| 8 yid
#

Figure 5a Figure 5b

Note that this is a decreasing function of a. For each particular a, it assumes
its minimum value at 6 = 45°, and the minimum value is f(45°,a) = 27 2-2a.
(To see that f(8,a) achieves its minimum at 6= 45°, use the trigonometric

identity
sind cos6 = #(sin® + cos6)2 - +

to write

(sind + cos8) - a
(sind + cos6)2 - 1

f(6,a) = 2

This is an increasing function of (sin 6 + cos 8). )
This line of reasoning yields a series of useful lemmas.

Lemma 3. Let a <1, and suppose that the center of a block B is between

the lines y = 0 and y = a, or on one of these lines. Then B intersects these lines

in a segment or segments with total length greater than

min(1, 272- 2a).

Proof. If two corners of B are outside the strip on the same side of the strip
(Figure 6a), then B intersects one of the lines in a segment of length greater
than 1. The remaining cases are illustrated in Figures 6b and 6c. In each case
the result follows from the calculations surrounding Figure 5. Figure 6d illustrates
that Figure 6c produces the same total length of intersection as Figure 5. This
completes the proof.

Note that if a = 1, the total intersection is a least 22-2 ~.828, and if
a < 72-3 =%.914, then the total intersection is at least 1. The following lemma

follows directly.

yea

yro

FIGURE 6

PROOF OF LEMMA 3

<—— >|
t Sin Becos Q-a
Sm @ cos O
2W2- 20
Gt ast)
Figure 6a Figure 6b
y*a ne
eee
723-20 )
sum of seqmenty
2212-20 a
oo yFO a
Figure 6c

Figure 6d

Lemma 4. Consider a region R bounded by the x axis, the line y=a, and two

vertical lines separated by a distance b. Suppose that either

(1) a=land b< 2/2 - 2 ~.828 (Figure 3c), or

(2) b= Landa<V2-% %.914 (Figure 3d).

Then any block B whose center lies in the region, and which does not intersect

the x axis, must contain one of the corners of the region.

To illustrate the use of the preceding lemmas, we prove the following result,

which settles the square-packing problem in the case of n = 5.

Lemma 5. Let S be the square bounded by the x and y and the lines x = 2 + V2

and y = 2 + 3/2, and consider the four points (1,1), (1,1 + #72), (1 + 372,1), and

(1 + 272,1+%/2). See Figure 7a. Any block in the interior of S must -contain

one of these four points.

Proof. In Figure 7b, the interior of S is divided into ten regions. If a block
B is contained in the interior of 8, its center must be in one of these regions.
Whichever region it is, one of lemmas 2 and 4 or corollary 2 to lemma 1 applies,

and forces B to contain one of the four points.

FIG-U-R-E-4
PROOF -OF LEMMA 5
= 27107 | i
|
1 1
e Of a @-—--®@------
1 an
| , I
ly 1
e e —_——— @--—--@-- -—----
} !
| |
j |
\ Hz \ |
(>| 2 |«__ ,
Figure 7a Figure Tb

-10-

Corollary 3. Five pairwise nonintersecting blocks cannot exist In the interior

of a square of side 2+ 3/2 = 2.707.

The next two lemmas are proved in the same way as Lemma 5, and will

be needed in Section 3.

Lemma 6. Let S be the square bounded by the x and y axes and the lines

x = 3 and y = 3, and consider the eight points (1,1), (12,1), (2,1), (2,12), (2,2),

(14,2), (1,2), (1,12). See Figure 8a. Any block B in the interior of S must-contain

one of these eight points.

Proof. Divide the interior of S into 18 regions as in Figure 8b. Whichever
region contains the center of B, one of lemmas 2 and 3 or corollary 2 to lemma

1 applies, forcing B to contain one of the eight points.

FIGURE 8

PROOF OF LEMMA 6

ul
Ok

s

x
3 | <3 (< —> |__|
e
@
1
|
|
'
an
I
|
ty,
‘“
l
|
|
j

Figure 8a Figure 8b

-i1-

Lemma 7. Let S be the square bounded by the x and y axes and the lines

x = 3 and y = 3, and consider the eight points (1,2), (14,2), (2,2), (1,1.7), (2,1.7),

(12,12), (1,0.9), (2,0.9). See Figure 9a. Any block in the interior of S must contain

one of these eight points.

Proof. Divide the interior of S into 18 regions as in Figure 9b, dnd proceed

as in Lemmas 5 and 6.

il
C,

$

FIGURE 9

PROOF OF LEMMA 7

\e—_——>| 9) 9 >|
e@°e
e 6®

k————>|e—k& > _ 1
1 + i 1
Figure 9a

-12-

Figure 9b

3. The Case of n= 6

We now state and prove the main result.

Theorem; Six pairwise nonintersecting blocks cannot exist in the interior

of a square of side 3.

Proof. Assume that the square, S, is bounded by the x and y axes and the
lines x = 3, y = 3. We use the term "key points" to refer to the nine points A = (1,1),
B = (12,1), C = (2,1), D = (1,14), E = (13,12), F = (2,14), G = (1,2), H = (12,2),
I = (2,2) in Figure 10. By lemma 6, any block in the interior of S must contain
one of the key points (this would be true even if the center point E were omitted).
If Sis to contain six nonintersecting blocks, then at least three of the key
points must be "isolated;" that is, contained in blocks which contain no other
key points. The point E cannot be isolated, by Lemma 6. We will not show that
two adjacent key points such as A and B cannot both be isolated. This is the
most difficult step in the proof of the theorem.

Lemma 8. Key points A and B cannot both be isolated.

Proof. We will focus on two line segments: one from (1,0) to A, and one
from A to B (see Figure 11). If A and B are both isolated, then the A-block and
B-block must each intersect both of these line segments. The B-block will leave
only certain portions of these segments uncovered in the neighborhood of A.

We will show that the total length of these uncovered portions is less than 2.
We will also show that the A-block necessarily covers portions of these segments
with total length greater than 2. This is a contradiction, and establishes that
A and B cannot both be isolated.
Consider first the B-block. See Figure 12. Without loss of generality, the

boundary of the block touches both point C and the x axis as shown in the figure,

-13-

FIGURE 10

THE NINE "KEY POINTS"

g=3

an
D e ra 2
A B ¢

FIGURE11

TWO LINE SEGMENTS USED IN PROOF OF LEMMA 8

~1 4-

and its side makes an angle of 9 with the x-axis as shown. Denote by u and v
the uncovered portions of the critical segments in the neighborhood of A. We

must show that u+v <2. We have:

sin@ + cos@ - 1
sin8 cos@

vel-

(from the calculation preceding Lemma 3) and

cos 8
sin 8

< ( snore IN (14 cot @
TN \~ eure +o)

(sm cas @- sin @-cos O41) (sin @+ cos @)

v, SO

nN

srn?@ cos 9
_ C\-sme) C= cos °) (sin 0+ cos @)
gnt cs O

Ci-smt@) C= cost) (sin O+ cos @)

(\+sine) C13 ose) sntO cos 0

cos'@ sinte (sin @+eos e)
C+ sin 0) (1+ cos 8) (sin? cos 6)

cos & \( Sin Oe cos 2
| + cos @ “T+ sin
(2) 0

We now consider the A~block. We now use u and v to represent the portions
of the critical segments covered by the A-block, and we will show that u + v > 2.
Without loss of generality, the block is arranged in one of the ways shown in

Figure 13. In either case we have

sin 9 + cos 8 - |}

£
1
Ni-

Sin 8 cos &

In Figure 13a we have
Sn 9

Hn}

Nin

cos 9

-~15-

FIGURE 12

PROOF OF LEMMA 8 (PART 1)

FIGURE 13

PROOF OF LEMMA 8 (PART 2)

Figure 13a Figure 13b

-16-

and ,; gin G+ ws 9-2 , . Sin 9
Utv-4 ? Sin Geos G -

1, Sin’

z tas O Xu

~(i-sra 6) Cl- cos 8) + 4 sm? ©
Sn O cos O

i

- Cl- sin 8) (\- cos 0) + Sin 29 ( {+ cos 6)
sm O cas 3 6)

-(i-sme) +3 (i+ cos 6)

cos 6 ( {4 cos @) [Sin 9

ii}

It

3 Sin 9 + 4 Cen @ +605 4 -1)
2

_ 20.
~ cos @ (lt ees 0) / 5% 8

In Figure 13b we have

v= 8 u

Su 8

and gin @ + cos O- I -)(+ cos 8 ’

-i > {2 ————_—— ~ 2

UFV7 3 ( gin @ cas @ <n

-te? 8
(sin @ + cos ~~ 4 sin @ cos ©) (cos 6+ 58) + gin’ @ ees

sin *O cos O

- ( l-sin &) (1-38) (ees CERT e)+i sin Geos O (cov 2emO) - 2 5in7Bees oe
sin*@ co O

- Ct-sin @) C-cos BY Coos O+ sin ©) +4 sin & cos *@

gh te cos O

i

— Cyasin ®6) ((renr8) (on 84 50 8) 4 08 cs'0 (14 in 8)
gih*9@ cos 8 a

~ ()- Cos @ (cus O + Sin 0) +3 $n 0 (14cm)
swe (i410) feos O

tt

. . 4
Co @ Sin G OO HEOSAE Hint OZ Wee —7 H's

i

gmt ® (las @) /tos @

—_ Ci-sim e) (t-tes e\ + i sin @ Chose e)
$int oO Clits e) fs ¢

i

' e+: a] josv © ae)
- +4 % a
[ Cos 5 SN = (it sym 6) fas 6) - .

This completes the proof of Lemma 8.

-17-

Lemma 8 severely restricts the selection of points which can be isolated.
We observe that a block which contains exactly two key points must contain
two key points which are adjacent (i.e., at distance 7 apart). We can now verify
that (up to symmetry) there is only one possibility, the one illustrated in Figure 14.
In this arrangement, key points B, G, and I are isolated, and there is one block
{the "center block") which contains E, H, and no other key points.

From Lemma 8, we know that the center block must intersect the lines
x = 1 and x = 2:in segments with total length greater than 0.8. It is easy to check
that the intersections may not extend above y = 2. It follows that the center
block must contain the points J = (1,1.7) and K = (2,1.7).

We now introduce the points L = (1,0.9) and M = (2,0.9). See Figure 15.
By Lemma 7, every block in the interior of S must contain one of G, H, I, J, K,
E, L, M. But of those eight points, four (E, H, J, K) are all contained in the center
block, so in addition to the center block, the interior of S may contain only four
other blocks.

This completes the proof of the theorem.

aster Strength

Walter R. Stromquist

-18-

FIGURE 14

ONLY REMAINING ALLOCATION OF KEY
POINTS TO SiX BLOCKS

aa

)

FIGURE 15

COMPLETION OF PROOF OF MAIN THEOREM

0.3
9.2

0.6

0.9

j<-——> |< > }ole->

-19-

