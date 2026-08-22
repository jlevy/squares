Square packing with O(x0.6) wasted area

Hong Duc Bui1*

Corresponding author(s). E-mail(s): buihd@u.nus.edu;

We show a new construction for square packing, and prove that it is more efficient
than previous results.

Abstract

1 Introduction

Square packing is a well-studied problem. Formally, we consider a large square S with
side length x and ask what is the maximum number of unit squares that can be packed
without overlap into S.

We define W (x) to be the area of wasted space when a square of side length x is
packed with unit squares. In other words, W (x) is x2 minus the maximum number of
unit squares that can fit in. (For convenience, our definition of W (x) is the same as
in [1–3].)

In this article, we are concerned with the behavior of W (x) as x → ∞.
The trivial packing method allows ⌊x⌋2 squares to fit in, which shows W (x) ≤
x2 −⌊x⌋2 ∈ O(x). However, a long line of research [1–3] has given much better bounds,
the best one gives W (x) ∈ O(x0.625). Also, [4] claims W (x) ∈ O(x0.6), but [5] shows
that there is a technical error in the calculation of W5, with W5 defined on [4, p. 8].
This article extends the insights in [3] to improve the result, namely W (x) ∈

O(x0.6).

On the opposite direction, [6] proved W (x) /∈ o(x1/2). This is a lower bound on

W (x). Note that W (x) /∈ Ω(x1/2), as W (x) = 0 for all positive integer x.

In a high level, the packing is done as follows. First, packing a square is reduced to
packing a right trapezoid, this reduction is described in Section 5. Then, the trapezoid
is packed by a certain kind of quadrilateral, this reduction is described in Section 4.
Finally, Section 3 describes how to pack such a quadrilateral.

Within these three steps, Section 3 is the most technical, Section 4 is less technical,

and Section 5 is standard, and the idea already appear in prior works.

1

6
2
0
2

r
a

M
5
1

]

G
C
.
s
c
[

2
v
3
0
6
4
0
.
8
0
5
2
:
v
i
X
r
a

 
 
 
 
 
 
Fig. 1 Trivial packing method of the space between two parallel lines.

1.1 Note on independent discovery

After putting this manuscript on arXiv, we learnt that an equivalent result was
independently discovered by McClenagan [7, 8], with a somewhat different method.

The two methods can be compared as follows.
The “second packing algorithm” in [8, Section 3] is similar to the packing method
in Section 3, except that it is specialized to have ∆1 + ∆2 = 1, so ij = j for every j.
In particular, im = m, that is, the packing has the same number of rows as columns.
By only analyzing the case where im = m, the analysis of wasted area becomes
significantly simpler. For comparison, in our article, in the application of Section 3 in
Section 4, we only use the case where im ∈ Θ(m). On the other hand, by analyzing
the general case where no restriction between im and m are imposed, we allow for
more flexibility on the method in Section 4. In particular, we don’t need to use and
analyze the dual packing method. Besides, by analyzing the general case, we were able
to analyze in Section 6.3 why having im ∈ Θ(m) appear to be the best choice with
this packing method.

The “first packing algorithm” in [8, Section 2] is a vertical reflection of the so-called

dual packing method we briefly mentioned in Section 6.2.

The method used to pack a right trapezoid in Section 4 of our article and [8,

Section 4] are completely different, as explained above.

The reduction from packing a square and packing a right trapezoid in Section 5 of

our article and [8, Section 4] are the same, and the same as prior works.

2 Summary of Existing Techniques

The fundamental method used to overcome the trivial bound x2 −⌊x⌋2 is the following.
Consider two parallel lines at a distance x apart, we wish to pack the space between
them with unit squares. If the trivial packing method is used as in Figure 1, we would
get Ω(x − ⌊x⌋) area of wasted space per unit distance. However, if we take vertical
stacks of ⌈x⌉ unit squares and tilt them as little as possible such that they fit between
the two lines, the angle of rotation needed will be O(x−1/2), therefore the wasted area
is only O(x−1/2) per unit distance. See Figure 2 for an illustration.

More generally, the height of each vertical stack can be any integer m ≥ x such
that m − x ∈ O(1). On a first-order approximation, the angle of rotation is usually
(cid:113) 2(m−x)
x

, as can be computed by an application of Pythagorean theorem.

2

Fig. 2 Improved packing method of the space between two parallel lines, which reduces the wasted
area to O(x−1/2) per unit distance.

This result can be interpreted as follows: it provides a family of parallelograms
that can be packed with small waste. These parallelograms can then be assembled
together to pack a larger shape.

The reason why this is so commonly used [1–3] is that the parallelogram can have
arbitrary (possibly nonintegral) height x, which allows us to eliminate one obstruction
in square packing—two parallel or almost-parallel sides with distance x apart where
x is not an integer. Unfortunately, it creates another obstruction: the other side of the
parallelogram is not perfectly vertical or horizontal.

Previously, there was no good way around this: for example, [2, Figure 9] cuts away
small triangles (denoted ei in that article) from the side of the slanted trapezoid in
order to make the two sides parallel.

In Section 3, we will describe another family of quadrilaterals that can be packed
similarly tightly (wasted area = perimeter × slope angle), but have two opposite sides
non-parallel. This is the main primitive that we assemble together for the final packing.

3 A Primitive Tightly-packed Quadrilateral

In this section, we prove the existence of a family of quadrilaterals with the following
properties:
• Each interior angle is 90◦ ± o(1). Intuitively, the quadrilateral looks almost like a

rectangle (unless the side length is too large, see Section 6.6).

• Consider one such quadrilateral. It is approximately an axis-aligned rectangle, as
above. Let m and im be some positive integers such that the almost-horizontal sides
have length ≈ m, the almost-vertical sides have length ≈ im. Let θ > 0 such that
the top left interior angle has measure 90◦ − θ.
Then there is a packing of the quadrilateral with total wasted area ∈ O((m + im)θ).
• This packing uses only almost-axis-aligned unit squares, that is, each unit square

can be rotated by an angle of o(1) to become perfectly axis-aligned.

The whole packing is illustrated in Figure 8, where the quadrilateral to be packed

is ABCD.

We would like to note that this packing method is inspired from [3]. The connection

is described in Section 6.5.

3

Symbol
m
im
θ
σ1
Si,j
Ti,j
∆1
∆2
∆3
Γj

ij
σ2

Meaning
Number of columns
Number of rows

Note
None

See ij below; im ≈

(cid:113) σ2
σ1

m

Angle between AB and horizontal
Angle between Ax and By
Unit square on i-th row, j-th column
Modified unit square
Amount Si,j+1 is to the right of Si,j
Amount Si+1,j is to the right of Si,j
Amount Si+1,j is below of Si,j
Amount Tij ,j−1 is below Tij ,j−2
Some row index (see Section 3.1.1)
Angle between AB and CD

None
None
Sloped by θ
Perfectly axis-aligned
∆1 = cos θ ≈ 1 − θ2
∆2 = sec(θ + σ1) sin σ1 ≈ σ1
∆3 ≈ 1 + θ(θ+2σ1)

2

Γj ≈ θ4
4σ1
(cid:108) (j−1)(1−∆1)
∆2
4σ1σ2 ≈ θ4

2
+ θ
(cid:109)
+ 1 ≈ θ2
2σ1

j

ij =

Table 1 Summary of notations in Section 3.

Fig. 3 First step in the packing method.

Furthermore, when im ∈ Θ(m), our packing method has the asymptotically small-
est wasted area among all packings for this family of quadrilaterals. This is shown in
Section 3.3.

For the convenience of the reader, all notations used in this section are listed in
Table 1. Some of the notations (in particular, θ, σ1 and σ2) are used again in later
chapters.

3.1 Description of the Packing Method

3.1.1 Initial Configuration

Consider the configuration illustrated in Figure 3. In words: There are two points
A and B, the line segment AB is slightly sloped downwards and makes an angle θ

4

Fig. 4 Illustration of ∆1, ∆2 and ∆3.

with the horizontal line, the ray Ax points downward vertically, the ray By points
downward and make an angle σ1 with the vertical line, such that the rays opposite
Ax and By intersect above A.

Define a coordinate system such that x-axis points to the right, y-axis points up,

and point A has x-coordinate 0. (Its y-coordinate is unimportant.)

We will pack the area inside the region xABy with horizontal stacks of squares,
each m unit squares, where m is some integer. We assume we can put a stack of m
squares (S1,1, . . . , S1,m), which we denotes S1,•, top right corner touching B, top edge
lying on the edge AB, and bottom left corner touching the ray Ax.

Note that the last requirement forces segment AB to have length m + tan θ.
Then, we keep adding stacks S2,•, S3,•, . . . , each having m squares, top edge parallel
to and touching the bottom edge of the previous one, and top right corner touching
the ray By. Number the individual unit squares as in Figure 3.

Define ∆1 = cos θ, ∆2 = sec(θ + σ1) sin σ1, ∆3 = sec(θ + σ1) cos σ1.

Lemma 1 For every (i, j), square Si,j+1 is ∆1 to the right of square Si,j , and square Si+1,j
is ∆2 to the right and ∆3 below Si,j .

See Figure 4 for illustration. This can be shown by applying the definition of

trigonometric functions on the two right triangles depicted in Figure 5.

Since ∆1 < 1, the leftmost point of S1,2 has x-coordinate < 1. Since ∆2 > 0, for

sufficiently large i, the leftmost point of Si,2 has x-coordinate > 1.

For each j, define ij to be the smallest value such that Sij ,j has x-coordinate of
leftmost point ≥ (j − 1). (Clearly i1 = 1. By the argument above, i2 exists and is > 1.)
Note that Sij ,j has x-coordinate of leftmost point (ij − 1)∆2 + (j − 1)∆1, therefore
ij =

+ 1.

(cid:109)

(cid:108) (j−1)(1−∆1)
∆2
Note that if 1−∆1
∆2
We have ∆1 ≈ 1 − θ2

< 1, some ij values might coincide.
2 , ∆2 ≈ σ1, so ij ≈ θ2

j.

2σ1

5

Fig. 5 Calculation of ∆1, ∆2 and ∆3 from θ and σ1.

Fig. 6 Illustration for introduction of the unit squares labeled Ti,j .

3.1.2 Modification of the Packing

We perform some modifications as illustrated in Figure 6. Formal description follows.
For each j ≥ 2, we remove Si′,j−1 for all i′ ≥ ij. Then we add a perfectly vertical
stack of squares with the leftmost point having x-coordinate j − 2, and the top right
point touching the bottom side of (ij − 1)-th row. For each positive integer ∆i, let
Tij +∆i−1,j−1 be the ∆i-th unit square from the top of this stack. (So, for example,
Tij ,j−1 should almost overlap Sij ,j−1 that has just been removed.)
We note that none of the unit squares Si,j or Ti,j overlap.
Define Γj = (ij − ij−1)(sec θ − 1) + tan θ. Since ij − ij−1 ≈ θ2
2σ1

, Γj ≈ θ4
4σ1

+ θ.

Lemma 2 For 3 ≤ j ≤ m, then Tij ,j−1 is Γj below of Tij ,j−2.

6

Fig. 7 Illustration for proof of Lemma 2. Some important squares are highlighted.

Fig. 8 Illustration of what happens as the vertical stacks T•,j reaches the right edge.

Proof We construct a few points as in Figure 7. Formally, let A be the corner of Tij−1,j−2
that touches the ij−1 − 1-th row. Extend the right side of T•,j−1 upward to intersect the top
and bottom side of row Sij−1,• at B and C respectively.

Then, B is 1 to the right and tan θ below A. Also, C is sec θ below B.
Therefore, Tij ,j−1 is (ij − ij−1) sec θ + tan θ below Tij−1,j−2. We also have Tij ,j−2 is
□

(ij − ij−1) below Tij−1,j−2, so we get the desired result.

We look at the im-th row of the packing after the modification above. There are
unit squares Tim,1, Tim,2, . . . , Tim,m−1 being perfectly axis-aligned and Sim,m sloped
by angle θ. See Figure 8.

7

Fig. 9 Zooming in around vertex C.

We delete all unit squares with row number greater than im. Then we will construct
point C on ray By and D on ray Ax such that all unit squares constructed so far lies
inside the quadrilateral ABCD.
Define σ2 = arctan (cid:0) 1−∆1
∆2

· (sec θ − 1) + tan θ(cid:1) − θ. Then we get

σ2 ≈ tan(σ2 + θ) − tan θ =

1 − ∆1
∆2

· (sec θ − 1) ≈

θ4
4σ1

.

Point C and D are constructed as follows. The slope of segment CD is determined
as follows: walking from D to C, for each unit to the right, it moves tan(θ + σ2)
units down. The vertical position of segment CD will be determined by the following
discussion.

For simplicity of analysis, we delete Sim,m from the packing. This results in

additional wasted area of 1 unit.

From the construction above, it follows that:

Proposition 1 Ray BA and CD intersect to the left of vertical line AD, and form with each
other an angle σ2.

Consider the unit squares near vertex C. Let B, C and D be the unit squares

Sim−1,m, Tim,m−1, Sim,m respectively, as in Figure 9.

Recall that Tij ,j−1 is Γj below Tij ,j−2. Therefore Tim,j−1 is also Γj below Tim,j−2,

so for each integer 1 ≤ j ≤ m − 1, Tim,j is

Γ3 + Γ4 + · · · + Γj + Γj+1 = (ij+1 − i2)(sec θ − 1) + (j − 1) tan θ

=

(cid:18)(cid:24) 1 − ∆1

∆2

(cid:25)

j

−

(cid:24) 1 − ∆1
∆2

(cid:25)(cid:19)

(sec θ − 1) + (j − 1) tan θ

8

Fig. 10 Illustrations for analysis of wasted area.

≤

=

(cid:18) 1 − ∆1
∆2
(cid:18) 1 − ∆1
∆2

(cid:19)

(j − 1) + 1

(sec θ − 1) + (j − 1) tan θ

· (sec θ − 1) + tan θ

· (j − 1) + (sec θ − 1)

(cid:19)

= tan(θ + σ2) · (j − 1) + (sec θ − 1)

below Tim,1. As such, if we select the vertical position of segment CD such that point
D is (sec θ − 1) below the bottom left corner of Tim,1, then all the Tim,j unit squares
will be above segment CD.

3.2 Analysis of the Wasted Area

There are 7 groups of wasted areas. See Figure 10 for an illustration.
• W1, triangles to the left of each row Si,• (colored yellow). There are im of them,

each has area 1

2 tan θ, so the total area is O(θim).

• W3, triangles above each column T•,j (colored blue). There are m of them, each has

area 1

2 tan θ, so the total area is O(θm).

• W2, small vertical strips to the left of W1 (colored magenta). Since ij − ij−1 ∈
+1)) = O(θ2 +σ1),

+1) for every j, the width of each strip is at most O(∆2 ·( θ2
σ1

O( θ2
σ1
so the total area is O((θ2 + σ1) · im).
Here is more details why the width of each strip is at most O(∆2 · ( θ2
+ 1)). For
σ1
illustration, see Figure 7. Any horizontal section of the magenta strip is to the left
of a row Si,• for some integer i. Find integer j such that ij−1 ≤ i < ij. Then the
width of this horizontal section of the magenta strip is the distance between the
bottom left corner of Si,j−1 and the right side of column T•,j−2. By definition of
ij−1, the square Sij−1−1,j−1 have x-coordinate of bottom left corner < (j − 2). Now

9

look at the square right below it, Sij−1,j−1. By Lemma 1, the distance between the
bottom left corner and the right side of T•,j−2 is < ∆2. Similarly, when we look at
the square Si,j−1, which is ≤ ij − ij−1 squares below Sij−1,j−1, the distance between
the bottom left corner of Si,j−1 and the right side of T•,j−2 is < ∆2 · (ij − ij−1 + 1).
• W6, small horizontal strips below each column T•,j (colored cyan). There are m of
them, the height of each is bounded by O(sec θ−1) (we have shown above during the
placement of segment CD that Tim,j is ≤ tan(θ+σ2)·(j −1)+(sec θ−1) below Tim,1,
using a similar argument we can also show Tim,j is ≥ tan(θ + σ2) · (j − 1) − (sec θ − 1)
below Tim,1), so the total area is O(θ2m).

• W4, triangles to the right of each row of Si,• (colored green). There are im of them,
2 tan(θ + σ1), so the total area is O((θ + σ1)im).
• W5, triangles below each column of T•,j (colored red). There are m of them, each

each has area 1

has area 1

2 tan(θ + σ2), so the total area is O((θ + σ2)m).

• W7, unaccounted-for area below Sim,m (colored brown). This is O(1) as long as all

of θ, σ1, σ2 are ∈ o(1).
Summing them up, we get the total wasted area to be O(( θ3
σ1

+ θ) · m + 1). This
is because each angle θ, σ1, σ2 is ∈ O(1), and 4σ1σ2 ≈ θ4. Also this can be written
more symmetrically as O((m + im) · θ + 1).

Remark 1 There is an alternative way to calculate the wasted area: count the number of
squares, then subtract that from the area of the trapezoid ABCD.

Clearly the number of squares (including Sim,m) is m · im. If we can show that the area
of the trapezoid ABCD is ≤ m · im + O(θ · (m + im) + 1), we would be able to conclude that
the total wasted area is O(θ · (m + im) + 1).

Calculating the area of the trapezoid ABCD appears to be difficult. See Appendix A.

3.3 Lower Bound on the Wasted Area

As mentioned in Section 2, the existing method for packing the area between two
parallel lines a distance x apart can be interpreted as giving an efficient packing method
for a family of parallelograms. We illustrate such a parallelogram in Figure 11.

If we have to pack the interior of such a parallelogram, this packing method is in

fact asymptotically optimal in certain cases.

Proposition 2 Consider a parallelogram that can be perfectly packed by the method illustrated
in Figure 11. Let x be its height. Suppose ⌈x⌉ − x ∈ Θ(1) and the width of the parallelogram
is ∈ Θ(x). Then the internal angle of the parallelogram is 90◦ ± Θ(1/
x), and the packing
method has wasted area Θ(

x).

√

√

Proof Suppose the horizontal edge is parallel to the x-axis. Let θ be the tilt of the almost-
vertical edge, and w ∈ Θ(x) be the number of almost-vertical stack of squares illustrated
in Figure 11. Then, the wasted area consists of 2w small triangles, each have area 1
2 tan θ.
Therefore, the total wasted area is w tan θ ∈ Θ(xθ). An easy calculation shows that if ⌈x⌉−x ∈
□
Θ(1) then θ ∈ Θ(1/

x).

√

10

Fig. 11 Illustration of the tightly-packed parallelogram formed by a stack of squares packed between
two parallel lines.

Proposition 3 A parallelogram with height x, width Θ(x), and internal angle 90◦ ± θ for
θ ∈ Θ(1/

x) has the minimum wasted area of a packing with unit squares Ω(

x).

√

√

The following is a more formal version of the statement of Proposition 3. For
x), there exists a function
all functions w1(x), w2(x) ∈ Θ(x), θ1(x), θ2(x) ∈ Θ(1/
a(x) ∈ Ω(
x) such that for any parallelogram with height x, width between w1(x)
and w2(x), and one internal angle 90◦ + θ for θ1(x) ≤ θ ≤ θ2(x) the minimum wasted
area of a packing of that parallelogram is ≥ a(x).

√

√

Proof We prove that any packing requires wasted area ∈ Ω(xθ). Pick Θ(x) equidistant points
each along the left and bottom edge of the parallelogram, and connect the corresponding
points, getting Θ(x) parallel line segments. This is depicted with red downwards-sloping line
segments in Figure 11. Let these paths be γ1, γ2, . . . , γk with k ∈ Θ(x).

Because the width and the height of the parallelogram are both Θ(x), the paths are at a
distance Θ(1) apart. Using [9, Proposition 21] (with minor adaptation to make it work with
two sides of the boundary instead of two unit squares) on each of the paths γ1, γ2, . . . , γk,
because the left and bottom edges are sloped by θ with respect to each other, for each such
path, the total wasted area in a region near each path is ∈ Ω(θ). Since the k paths are at
distance Θ(1) apart, each point is only near O(1) paths, therefore the total wasted area in
□
any packing of the parallelogram is ∈ Ω(kθ) = Ω(xθ), finishing the proof.

Using a very similar argument, we can see that when m/im ∈ Θ(1), a quadrilateral
with almost-vertical and almost-horizontal sides with width Θ(m), height Θ(im), and
an interior angle 90◦ − Θ(θ) must have wasted area Ω((m + im) · θ). Therefore, for the
quadrilaterals formed by our packing method described in this section, our method is
asymptotically optimal up to a multiplicative constant factor.

4 Packing a Right Trapezoid

We consider a right trapezoid with height x, base Θ(xβ), slope of right edge Θ(x−γ),
where β and γ are some positive constants. We will describe a packing method that
results in the wasted area being Θ(x1−γ/2) under some choices of β and γ.

This packing method is illustrated in Figure 12. Informally, we first pack the cyan
quadrilateral E0G0M0N0 with the method in Section 3, leave a gap N0M0G1E1 with
integral height that can be almost perfectly packed and segment E1G1 has length

11

Symbol
β
σ1
γ
θ, θi
ω
σ2

Note
Top edge has length Θ(xβ )
Slope of right edge
σ1 ∈ Θ(x−γ )
Slope of horizontal stacks
θ ∈ Θ(x−ω)
σ2 ∈ Θ(x−(4ω−γ))

Table 2 Summary of notations in Section 4.

Fig. 12 Illustration for packing of a right trapezoid. Each cyan region is packed according to the
method in Section 3.

slightly more than an integer, which allows us to continue packing the cyan quadrilat-
eral E1G1M1N1 with the same method in Section 3. In doing so, the edge M0N0, and
thus E1G1, is slightly more tilted than E0G0. Similarly, E2G2 is slightly more tilted
than E1G1, etc.

Later, we will specialize to γ = 1

2 and β = 1 − γ

2 = 3

4 . All notations used in this

section are listed in Table 2.

4.1 Details of the Packing Method

We perform the following procedure. See Figure 12 for demonstration.

First, define ω = γ

2 and pick θ ∈ Θ(x−ω), the exact constant factor to be decided
later. Then pick E0 on segment AD, its exact position to be determined later. Pick
G0 on segment BC such that the angle AE0G0 is (90 + θ)◦.

Proposition 4 The set of locations of E0 on segment AD such that segment E0G0 has
length tan θ more than an integer is a discrete set of points, each Θ(xγ ) spaced apart from
its nearest neighbor.

12

This comes immediately from the fact that line BC makes with line AD an angle
of Θ(x−γ). Therefore, there exists a choice of E0 such that segment AE0 has length
Θ(xγ).

Using this choice of E0, construct a tightly-packed quadrilateral (as described in
Section 3) right below segment E0G0. Let the two bottom vertices of it be M0 and N0
respectively, with M0 on BC and N0 on AD.

Let θ, σ1, σ2 be as in Section 3, where we use quadrilateral E0G0M0N0 here in
place of the quadrilateral ABCD in Section 3. Notice that the θ as in Section 3 agrees
with our definition of θ at the start of this section, and σ1 ∈ Θ(x−γ) is the slope of
the right edge.

Then, define θ1 to be the angle that N0M0 makes with the horizontal line. We

have θ1 = θ + σ2.

We will construct points E1 and G1 on segments N0D and BC respectively such

that E1G1 is parallel to N0M0.

Arguing similar to Proposition 4, the set of possible locations of E1 such that the
length of E1G1 is tan θ1 more than an integer is a discrete set of points, each Θ(xγ)
spaced apart from its nearest neighbor. Thus we can pick E1 being one of those points
such that segment N0E1 has length Θ(xγ).

Move E1 slightly downwards (by a length of O(1)) so that the segment N0E1 has

integral length. Move G1 accordingly, keeping E1G1 parallel to N0M0.

Construct a quadrilateral E1G1M1N1 similar to above. Because of the movement
of E1 above, we might have to trim away a vertical strip of height approximately E1N1
and width O(x−γ) from the left side of the quadrilateral, near segment E1N1. Since
the height of the right trapezoid is x, the total wasted area caused by this trimming is
O(x1−γ). This is asymptotically smaller than the Θ(x1−γ/2) that will be shown later,
thus can be safely ignored.

Then, keep constructing quadrilaterals {EiGiMiNi}i following the same procedure
until the bottom edge is reached. Let k be the maximum integer for which the quadri-
lateral EkGkMkNk was constructed and entirely contained in the right trapezoid
ABCD.

Next, for each gap NiMiGi+1Ei+1, we fill it with vertical stacks of unit squares

with height equal to the length of segment N0E1. An illustration is in Figure 13.

Note that there is some overlap with the region above N0M0, but this is fine—
recall the construction in Section 3, these columns merely extends the T•,j columns.
The right end near M0G1 is sloped, they can be filled in naively.

The top and bottom part can be filled in naively with waste proportional to the

total perimeter of quadrilaterals ABG0E0 and NkMkCD.

4.2 Analysis of the Wasted Area

First, we consider the quadrilateral E0G0M0N0. We use the notation θ, σ1, σ2, m and
im for width and height as in Section 3.

Proposition 5 σ2 ∈ Θ(x−γ ) and im ∈ Θ(xβ).

13

Fig. 13 Method of filling in the gaps NiMiGi+1Ei+1. Illustrated with i = 0.

Proof We have m ≈ E0G0 ∈ Θ(xβ). Since θ ∈ Θ(x−ω) and 4σ1σ2 ≈ θ4, we get σ2 ∈
m ∈ Θ(xβ).
Θ(x−(4ω−γ)) = Θ(x−γ ). So im ≈
□

(cid:113) σ2
σ1

Let θi be the angle that EiGi makes with the horizontal line. Note that θ1 agrees

with the definition above, and θ0 = θ.

We want to fill the whole trapezoid ABCD with such quadrilaterals, leaving the
bottom region small. The following proposition describes a sufficient condition to do
that.

Proposition 6 If β ≥ 1 − γ and 1 − max(β, γ) ≤ γ
2 , and θ is chosen with sufficiently small
constant factor, then we can fill the whole trapezoid ABCD with quadrilaterals as above, while
keeping θi ∈ Θ(x−ω) for all i.

Here, β ≥ 1 − γ is just a convenient assumption, so that each length EiGi is
∈ Θ(xβ). (Otherwise for sufficiently large i, length of EiGi may grow to Θ(x1−γ). See
also discussion in Section 6.6.)

Note that the height of each quadrilateral plus a gap is Θ(xβ +xγ). As such, assum-
ing the height of the quadrilaterals remains roughly the same, we need Θ(x1−max(β,γ))
such quadrilaterals.

If 1 − max(β, γ) ≤ γ

2 , the angle θi remains in Θ(x−ω) since the sum of σ2 values

over all quadrilaterals are ∈ O(x−γ) · O(xγ/2) = O(x−γ/2) = O(x−ω).

The formal proof follows. We have σ1 ∈ Θ(x−γ), and the length of the top edge is

∈ Θ(xβ) where β = 1 − γ
2 .

Because we only need to consider sufficiently large x, we can assume there are
constants 0 < l < u such that l · x−γ < sin σ1 < σ1 < u · x−γ, and the top edge has
length > l · xβ + 1.

Let d = 0.12 · l2u−1. Pick θ0 = arctan(d · x−ω).

14

Now assume x is large enough such that the conditions above hold, and in addition,

ux−γ + 2dx−ω < 1
8 .

For each i ≥ 1, define θi = arctan
Then

(cid:16)

1−cos θi−1
sec(θi−1+σ1) sin σ1

· (sec θi−1 − 1) + tan θi−1

(cid:17)

.

tan θi − tan θi−1 =

1
sec(θi−1 + σ1)

·

(1 − cos θi−1) · (sec θi−1 − 1)
sin σ1

.

Lemma 3 If 0 < θ + σ1 < 1

8 then 1 < sec(θ + σ1) < 1.01.

Lemma 4 If 0 < θ < 1

8 then (1 − cos θ)(sec θ − 1) < (tan θ)4

4

.

Lemma 5 If 0 < θ < 1

8 then 1 − cos θ > 0.49(tan θ)2.

The three lemmas above can be verified with a combination of interval arithmetic

and differentiating the expression, noticing equality holds at θ = 0.

Lemma 6 For 0 ≤ i ≤ ⌊ l

4d3 xω⌋ + 1, tan θi ≤ tan θ0 + 4d4i

l x−γ .

Proof The statement is true for i = 0.

We prove by induction. Assume tan θi−1 ≤ tan θ0 + 4d4(i−1)
8 , so tan θi − tan θi−1 < (tan θi−1)4

4d3 xω⌋, tan θi−1 ≤ 2d · x−ω < 1
⌊ l
so we’re done.

4 sin σ1

l

x−γ . Then since i − 1 ≤
4lx−γ ≤ 4d4
l x−γ ,
□

< (2dx−ω)4

Lemma 7 The total height of the first (cid:6) l

4d3 xω(cid:7) trapezoids is ≥ x.

4d3 xω(cid:7).
Proof Consider a particular trapezoid with slope of top edge being θi, where 0 ≤ i < (cid:6) l
The number of columns m is ≥ the length of the top edge, which is > l · xβ + 1. Therefore
≥ l·xβ ·0.49(tan θi)2
the number of rows is ≥
.
1.01·u·x−γ
Since each tan θi is ≥ tan θ0 = d · x−ω, each number of rows above is ≥ 0.48x1−ωd2 l
u .

+ 1. This is ≥ l·xβ ·(1−cos θi)
sec(θi+σ1) sin σ1

(cid:108) (m−1)(1−cos θi)
sec(θi+σ1) sin σ1

(cid:109)

Therefore the total height is ≥ l
We have shown that we need no more than (cid:6) l

4d3 xω · 0.48x1−ωd2 l

du x = x.

u = 0.12 l2
4d3 xω(cid:7) quadrilaterals to fill the
4d3 xω(cid:7) quadrilaterals have θi ∈ Ω(x−ω), so

□

whole trapezoid ABCD, and the first (cid:6) l
Proposition 6 is proven.

Next, we analyze the wasted area.
The top and bottom part have wasted area O(xβ + xγ).
There are O(x1−max(β,γ)) such quadrilaterals, and roughly as many gaps. For each
quadrilateral, the waste is O((m + im)θ) = O(xβ−ω). For each gap, the waste caused

15

by the naive filling near the segments MiGi+1 is O(xγ), and the waste below each
vertical stack can be discounted because they’re equal to the amount of space reused
by overlapping with the quadrilateral above N0M0.

Adding them up, the total wasted area is

O(cid:0)xβ + xγ + x1−max(β,γ) · (xβ−γ/2 + xγ)(cid:1).

Finally, specialize to γ = 1

2 and β = 3

4 . All hypotheses are satisfied, and the total

wasted area is O(x3/4).

5 Reduction from Packing a Square to Packing a

Right Trapezoid

We will state a proposition which describes a packing method that allows one to
reduces the problem of packing a square to the problem of packing a right trapezoid,
special cases of which has already been used several times in previous works.

Define Wβ,ϵ(x) = x
2 and β.

mean of 1

2β
2β+1 log

ϵ

2β+1 x. We would like to note that

2β
2β+1 is the harmonic

Proposition 7 If there exists real 1
2 , real ϵ such that for all
real m, for all w ∈ Θ(mν ), the right trapezoid with height m, smaller base w, larger base
m) can be packed with wasted area O(mβ logϵ m), then W (x) ∈ O(Wβ,ϵ(x)).
w + Θ(

2 < β < 1, real 0 < ν < β + 1

√

This trapezoid is roughly the same as a “type 2” shape in [2, 3], except that we

make the constant factor implicit rather than explicit.

The wasted area is O(mβ logϵ m + x√

quantity above is minimized, being O(x

m ). By selecting m = (x log−ϵ x)
2β
2β+1 log

2β+1 x) = Wβ,ϵ(x).

ϵ

2

2β+1 , the

Note that ν cannot be too large otherwise it may happen that mν > x.
√
We see this being applied in previous results as follows. Note that 4−
2
7 < 1.

Article mβ logϵ m

[1]

[2]
[3]

m

m7/8

√

2

2+
4

m5/6

Choice of m
x8/11

x3/4

log m x2−2α, with α = 3+
7

√

√

2

2

x

3+
7

4−

√
2
7 x

Wβ,ϵ(x)
x7/11

log
x5/8

In this article, when β = 3

4 , we get:

Theorem 1 W (x) ∈ O(x3/5).

That proves the claim in the introduction.

16

Fig. 14 Dual of the packing described above.

6 Discussion

6.1 Symmetry of the Construction

We discuss a symmetry in the construction described in Section 3.

Note that if we shift each T•,j stack down until they touch segment CD, the small
rectangles in W6 will disappear, instead, some small rectangles will appear above
the stacks T•,j—and we see the symmetry of the construction between W1 ↔ W3,
W2 ↔ W6, W4 ↔ W5, σ1 ↔ σ2, S ↔ T .

The symmetry is also shown in the following formula that relates θ, σ1 and σ2:

sec(θ + σ1) sin σ1 · sec(θ + σ2) sin σ2 = (1 − cos θ)2.

And the following formula (this can be derived from im ≈ θ2
2σ1

m):

im√
σ2

≈

m
√
σ1

.

While the square root may look weird, a better way to look at it is the following:
if θ and m are fixed, in order to double σ2, you need to multiply im by roughly the
same factor 2. In formula: im ≈ 2σ2

Note that the area of W6 does not have a O(σ2m) term likely because our analysis is
not exactly symmetric, in particular the width of W2 is measured being perpendicular
to AD but the height of W6 is measured being parallel to AD instead of perpendicular
to AB. Nevertheless, the result is not affected.

θ2 m.

6.2 Dual of the Packing Method

We would like to note that there is a natural dual to the method in Section 3. See
Figure 14.

17

Fig. 15 Horizontally cut a right trapezoid into Θ(x1−γ/2) smaller right trapezoids.

Here, the horizontal stacks are angled upwards instead of downwards, and it is
necessary that θ > σ1. We don’t analyze this configuration because it appears to be
not particularly useful.

6.3 Limitation of the Packing Method

Consider the packing method in Section 4. Suppose we choose some value of ω different
from γ
2 .
If ω < γ

2 , then θ > x−γ/2 for large enough x, then the waste comes from the

quadrilaterals alone is ≥ Ω(x · θ) which is more than x1−γ/2.

If ω > γ

2 , the height of each quadrilateral is Θ(xβ+γ−2ω) which is much less than
the width Θ(xβ). Consequently, the total perimeter of the quadrilaterals is much more
than the sum of the heights. Assume at least a constant factor of the height comes
from the quadrilaterals instead of the gaps (that is β + γ − 2ω ≥ γ), then the wasted
area (again comes from the quadrilaterals alone) is Θ(x2ω−γ · x · θ) = Θ(x1+ω−γ), and
1 + ω − γ > 1 − γ
2 .

As such, it appears that Ω(x1−γ/2) is a natural lower bound for our method. And,
2 , our method of packing naively the top/bottom/right side area in Section 4

with β = 1
does not hurt us, since naive packing already gives O(x1−γ/2).

There is another interpretation for Ω(x1−γ/2). Consider Figure 15. If the trapezoid
ABCD is subdivided into smaller right trapezoids by cutting horizontally, such that
each triangle formed by drawing a vertical line from the top right corner to the bottom
edge has area Θ(1) (colored cyan in the figure), then you need Θ(x1−θ/2) such triangles.
It appears unlikely that it is possible to pack each of these small trapezoid with average
wasted area o(1) each.

As such, we make the following conjecture:

18

Fig. 16 Example of packing where the naive attempt to prove Conjecture 1 fails.

Fig. 17 An illustration of the waste area being O(x) without any of the known bottlenecks.

Conjecture 1 For 0 < γ < 1, a right trapezoid with height x and difference between two
bases Θ(x1−γ ) cannot be packed in o(x1−γ/2).

Unfortunately, the most straightforward method to prove this—proving that each
such right trapezoid has wasted area Ω(1)—doesn’t work (when β > γ > 0), as
depicted in the configuration in Figure 16.

We consider the right trapezoid colored gray. Draw a blue diagonal line as in the
figure, then draw a yellow line parallel to the bottom side and a red line parallel to
the top side. Pack each region with stacks of squares with tilt Θ(x−β/2).

Then the difference in the x-coordinate of the two endpoints of the blue diagonal
line is Θ(xβ/2), which is larger than the distance Θ(xγ/2) marked on the figure. The
total wasted area inside the gray right trapezoid is then O(xγ/2 ·(x−β/2 +x−γ)) ⊆ o(1).

Nonetheless, we hope it is possible to adapt the methods in [6].
However, getting from the x1−γ/2 barrier to a better lower bound for square packing
is still highly nontrivial, since there is no reason why a packing method must use a
reduction of the form Proposition 7. See Figure 17 for an illustration.

6.4 Packing Other Shapes

We have shown in Section 4 that for certain values of β and γ, a right trapezoid with
height x, width Θ(xβ), slope of right angle Θ(x−γ) can be packed with wasted area
Θ(x1−γ). (Note that, assuming β ≥ 1 − γ, when β is too small, the wasted area is
dominated by x1−β/2, and when β is too large the wasted area is dominated by xβ−1/2.)
2 . Additional considerations, such as
packing the top/bottom/right area of the gap intelligently by recursively using the
original method (the method of recursive packing can be found in [2]) may make it

Our method as is only works for γ up to 1

19

work for higher γ. Further research is needed to determine the behavior at various
values of γ.

In fact, we make the following conjecture:

Conjecture 2 For any value β ≥ 0 and γ ≥ 0, the optimal exponent in the wasted area
asymptotic of packing a trapezoid with height x, width Θ(xβ), slope of right angle Θ(x−γ ) is

(cid:16)

max

1 −

max(β, 1 − γ)
2

, 1 −

γ
2

, β −

(cid:17)

.

1
2

,

3
5

The wasted area of the trivial packing method is Θ(x(x − ⌊x⌋)), therefore, when
x − ⌊x⌋ ∈ o(x−2/5) then it is possible to get the wasted area o(x3/5). That poses the
question:

Question 1 Is it possible to get wasted area o(x3/5) when x − ⌊x⌋ ∈ Θ(x−2/5)?

When x − ⌊x⌋ ∈ Θ(x−2/5), [6] gives the lower bound x3/10.
Our reason for focusing on right trapezoid is that the problem of packing arbitrary
almost-rectangular quadrilaterals can often be reduced to packing right trapezoids by
dividing such quadrilaterals into a small number of right trapezoids. The reduction
may not be optimal, however.

6.5 Inspiration for the Primitive Tightly-packed Quadrilateral

Here we explain the connection between [3] and our construction in Section 3.

(cid:113) 2δ

w , when δ
w remains roughly the same,

In [3], noticing that the slope of each horizontal stack is roughly

changes by a small amount, say w−0.9, in order to make 2δ
the denominator should be scaled by roughly the same factor as the numerator.

Suppose δ ∈ Θ(1). Then δ − Θ(w0.1) ≈ δ · (1 − Θ(w−0.9)). We want to scale the
numerator by the same factor, namely changing the numerator from w to w · (1 −
Θ(w−0.9)), which is w − Θ(w0.1).

In this article, we made two modifications:

• we change w (and thus the slope) gradually, instead of in bulk;
• we work backward: instead of using δ and the desired slope to determine w as in [3],
we use the slope of the stack of squares and δ to determine w. As such, we can ensure
the slope difference is exactly zero, at the cost of a small wasted area elsewhere.

6.6 On Packing of Triangle-like Right Trapezoid

Consider a right trapezoid T (x, Θ(xβ), Θ(x−γ)) where β > 0 and γ > 0. Even though
γ > 0, it is not necessarily true that the trapezoid will look approximately like a
rectangle. This is because the top (smaller) side has length Θ(xβ), the bottom (larger)
side has length Θ(xβ) + Θ(x1−γ), if 1 − γ > β, then the right trapezoid in fact looks
like a triangle. See Figure 18.

20

Fig. 18 Illustration of a triangle-like right trapezoid.

We would like to note that it is possible to split a triangle-like trapezoid to O(log x)
right trapezoids, with each of them having bottom side no more than twice the top
side. This would allow us to only focus on packing trapezoids with ratio of two bases
∈ Θ(1).

In fact, we conjecture the following:

Conjecture 3 The strategy of packing a triangle-like right trapezoid by first subdividing into
O(log x) right trapezoids as above, then packing each of them optimally, is asymptotically no
worse than the optimal strategy.

7 Conclusion

We have shown that the wasted area when packing a large square with side length x
can be as small as O(x3/5). Further research is needed to prove or disprove various
bounds, such as the bound x1−γ/2 pointed out earlier, and extending the result to
non-square shapes.

8 Acknowledgements

We would like to thank anonymous reviewers for their enthusiasm, and for many
helpful suggestions to improve the manuscript.

References

[1] Erd˝os, P., Graham, R.: On packing squares with equal squares. Journal of
Combinatorial Theory, Series A 19(1), 119–123 (1975) https://doi.org/10.1016/
0097-3165(75)90099-0

21

[2] Chung, F., Graham, R.: Packing equal squares into a large square. Journal of Com-
binatorial Theory, Series A 116(6), 1167–1175 (2009) https://doi.org/10.1016/j.
jcta.2009.02.005

[3] Wang, S., Dong, T., Li, J.: A New Result on Packing Unit Squares into a Large

Square (2016). https://arxiv.org/abs/1603.02368

[4] Chung, F., Graham, R.: Efficient packings of unit squares in a large square. Dis-
crete & Computational Geometry 64(3), 690–699 (2019) https://doi.org/10.1007/
s00454-019-00088-9

[5] Arslanov, M.Z., Bui, H.D.: Note on “efficient packings of unit squares in a large
square”. Discrete & Computational Geometry (2025) https://doi.org/10.1007/
s00454-025-00767-w

[6] Roth, K.F., Vaughan, R.C.: Inefficiency in packing squares with unit squares.
Journal of Combinatorial Theory, Series A 24 (1978) https://doi.org/10.1016/
0097-3165(78)90005-5

[7] McClenagan, R.: Asymptotic square packing problems. Master’s thesis, University
of Northern British Columbia. https://doi.org/10.24124/2024/59553 . http://dx.
doi.org/10.24124/2024/59553

[8] McClenagan, R.: Optimally Packing a Large Square by Unit Squares (2026). https:

//arxiv.org/abs/2602.01484

[9] Bui, H.D.: Square Packing with Asymptotically Smallest Waste Only Needs Good

Squares (2025). https://arxiv.org/abs/2504.09489v1

22

Fig. 19 Illustration for alternative method of calculating wasted area in Remark 1.

A Alternative Method of Wasted Area Calculation

In this section, we try to show that the area of the trapezoid ABCD in Remark 1 is
≤ m · im + O(θ · (m + im) + 1).

Draw segments BH, CJ, CK perpendicular to AD, CJ parallel to AB, with H

and K on line AD, J on line HB, L on line AB. See Figure 19 for an illustration.

Intuitively, segment AD has length im + O(θ), the perpendicular CK has length
m+O(θ+σ1), therefore triangle ACD has area 1
2 (im+O(θ))·(m+O(θ+σ1)). Similarly,
segment AB has length m + O(θ), the perpendicular CL has length im + O(θ + σ2),
therefore triangle ABC has area 1
2 (im + O(θ + σ2)) · (m + O(θ)). So the total area is
m · im + O(θ · (m + im) + 1). The difference gives the expected result.

There is an extra term mσ2 or imσ1, but imσ1 ≈ θ2
2σ1

mσ1 = θ

2 · θm ≤ θm, and

similar for the other direction.

Let us compute the total area more formally.
We have mentioned above that segment AB has length m + tan θ. We see that
the top edge of Ti2,1 is tan θ + (i2 − 1) sec θ below A, so the bottom edge of Tim,1 is
tan θ + (i2 − 1) sec θ + (im − i2 + 1) below A, so segment AD has length tan θ + (i2 −
1) sec θ + (im − i2 + 1) + (sec θ − 1) = im + tan θ + (sec θ − 1)i2.

Then, segment BH has length (m + tan θ) · cos θ and segment AH has length

(m + tan θ) · cos θ.

Let x be the length of segment KC. This is also equal to length HJ, so BJ =

x − BH, so HK = JC = (x − BH) cot σ1, so KD = ((x − BH) cot σ1 − DH).
Therefore x = ((x − BH) cot σ1 − DH) cot(θ + σ2). Solving for x gives

x =

=

BH + DH tan σ1
1 − tan(θ + σ2) tan σ1
(m + tan θ) cos θ(1 − tan σ1) + tan σ1(im + tan θ + (sec θ − 1)i2))
1 − tan(θ + σ2) tan σ1

.

This appears to be difficult to analyze, so let us try to analyze it in a different way.
Let E be the top right corner of C, G be the top right corner of D, F on segment CD
such that EF is vertical, and drop perpendicular CM to line EF . See Figure 20 for
an illustration. Here C and D are unit squares defined the same way as in Figure 9.

Then, segment EG has length ≤ 1 + tan(θ + σ1) by an analysis similar to Figure 5.

To compute the length of segment EF , note that:

23

Fig. 20 More detailed illustration for the argument in Remark 1.

• point D is sec θ − 1 below the bottom left corner of Tim,1,
• point F is (m − 1) tan(θ + σ2) below D,
• the square C is Γ3 + · · · + Γm below the square Tim,1,
therefore

EF = 1 + (m − 1) tan(θ + σ2) + (sec θ − 1) − (Γ3 + · · · + Γm)

= 1 + (m − 2)(tan(θ + σ2) − tan θ) + tan(θ + σ2) − (im − i2 − 1)(sec θ − 1)

= 1 +

= 1 +

(cid:16) 1 − ∆1
∆2
(cid:18)(cid:16) 1 − ∆1

∆2

(m − 2) − (im − i2 − 1)

(cid:17)

(sec θ − 1) + tan(θ + σ2)

(m − 1) − im

(cid:17)

− (

1 − ∆1
∆2

(cid:19)

− i2) + 1

(sec θ − 1) + tan(θ + σ2)

≤ 1 + 2(sec θ − 1) + tan(θ + σ2).

Asymptotically, we can assume EF < 3
sufficiently small. Then GC < 2, so CM = EG cos θ + GC sin σ1 ∈ 1 + O(θ + σ1).

2 and both σ1 and θ + σ2 are

2 , EG < 3

24

