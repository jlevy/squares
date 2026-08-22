ON  PACKING  SQUARESWITHEQUALSQUARES

bY

P.  Erd6s
R.  L  Graham

STAN-CS-75-483
MARCH  1975

COMPUTER   SCIENCE  DEPARTMENT
School  of  Humanities  and  Sciences
STANFORD  UNIVERSITY

ON PACKING SQUARES  WITH EQUAL SQUARES

P. Erdijs
Stanford University
arid
The Hungarian Academy of Sciences
and
R. L. Graham
Stanford University
and
Bell Labmatories,  Murray Hill, New Jersey

Abstract

The following problem arises in connection with certain multi-

dimensional  stock cutting problems:

How many-non-overlapping  open unit squares may be packed into
a large square of side Q! ?

Of course, if a is a positive  integer, it is trivial to see that
unit squares can be successfully  packed.

a*
integer, the problem becomes much more complicated.
feels that for a = N + & ,
pack  N2
border area (which is about @O ) as unusable waste. After all, how
could it help to place the unit squares at all sorts of various skew
angles?

unit squares in the obvious way and surrender the uncovered

say,  (where  N  is  an  integer),  one  should

However,  if  a  is  not  &111.

Intuitively,  one

In this note, we show how it helps.

In particular,  we prove that
we can always keep the amount of uncovered area down to at most propor-
tional to w-a
waste produced by the "natural"  packing above.

, which for large Q is much less than the linear

This research was supported in part by National Science Foundation
grant GJ 36473~ and by the Office of Naval Research contract NR 044-4o2.
Reproduction in whole or in part is permitted for any purpose  of the
United States Government.

L

a

ON  PACKING  SQUARES  WITH

EQUAL  SQUARES

by

P. Erd&
Stanford  University
and
The  Hungarian  Academy  of  Sciences

and

R. L. Graham
Bell  Laboratories
Murray  Hill,  New  Jersey

c

i

i
L

1

L

L

If  two  non-overlapping  squares  are  inscribed  in  a

unit  square,then  the  sum  of  their  circumferences  is  at  most

4,  the  circumference  of  the  unit  square.  As  far  as  we  know,

-,

this was first published by P. Erdgs and aappeared  as a problem

in a mathematical paper for high school students in Hungary.

A. Beck and M. N. Bleicher [l] proved that if a closed convex

curve @ has the property that for every two inscribed

non-overlapping  similar  curves  @1 and @2' the sum of the

circumferences of @1 and @2 is not greater than the circumferance

of @, then @ is either a regular polygon or a curve of constant

a

width.

It is c1ea.r   that  one  can  inscribe  k2 squares into
-a  unit square  so  that  the  sum  of  their  circumferences  is  4k.
P. Erdos  conjectured  40  years  ago  that  if  we  inscribe  k2 + 1
squares into a unit square, the  total  circumference  remains  at

most 4k.

For k = 1, this is true as we have j,ust  stated.

D. J. Newman [2] proved the conjecture for k = 2 'but the general

case is still unsettled.

Denote  by  f'(a)  the  maximal  sum  of  circumferences  of

a  non-overlapping  squares  packed  into  a  unit  squa.re.

The

conjecture we cannot prove is just f(k2+l) = &k.

In this

note we show f(1) > 4k for -2 = k2 + o(k), (in fact, for
a = k2 + [&?'=I using just equal squares).

We do not know

as f(4) increases from &k to 4k + 4 how large the jumps are

and where they occur.

Instead  of  maximizing  the  circumference  sum  of

packings of a unit square by ar'bitrary squares, we shall

work  with  the  closely  related  problem  of  maximizing  the  area

sum of pac_kings   of  an  arbitrary  square  by  unit  squares.

For  each  positive  real  a,  define

w(a) = a2 - sup 16J1

P

where Q ranges over all packings of unit squares into a given

squa.re S(a)  of side ~1 and /p] denotes the number of unit squares

in 9.

Theorem.

(1)

Proof:

We  sketch  a  construction  which  will  prove  (1).  As

usual, the  notation  f(x)  =  n(g(x)) will  denote  the  existence
of  two  positive  constants  c  and  c' such that cg(x) < f(x) <  c'g(x)

for all sufficiently large x.

We  begin  by  packing  S(a>  with  N2 unit squares

which form a subsquare S(N) in the lower left-hand corner of

S(a) as shown in Fig. 1, where N = [o-a8'11] and ~1 is large.

The  remaining  uncovered  area  can  be  decomposed  into  two

rectangles, each  having  width  p = a-N and lengths > N.-

IL
1
1

L

L.

i

1

L

Fig. 1

Next, we pack a rectangle R(@, ^J) of sides f3 a,nd 7

with y

= n(a), @ = *(a8'11)  as follows .

Let n = @I.  Place
adjacent parallel rectangles R(l,n+l), each formed from n + 1

unit  squares, tilted at the appropriate angle 8 SO that all
R(l,n+l) *s  touch  both  the  top  and  bottom  edges  of  R(B, 7).

Furthermore , place  these  so  that  D  =  n(a2'11)  (see  Fig
Note  that  D'

= *(,4'11).

.

2).

Fig.  2

An  easy  calculation  shows  that  8 = n(a -4'11) and  so, each
of the small shaded right triangles on the border of R has

area  O(a m4'11).

The  total  area  of  the  triangles  is  therefore

o(J+ .

-.

There are,in addition,two right trapezoids T with

base  @ and vertical sides D and D'  which  have  not  been  covered

up to this point.

We next describe how to pack T.

Let m = [a 4/11 1.

Starting  from  the  right-hand  side  of

T, partition T into as many right trapezoids Tl,T2,...,Tr

as  possible, where the base of each Tk is m (see Fig. 3).

Fig. 3

Thus, r = n(a 4'11) and X'has  area O@ll). If the vertical

sides of Tk are 7j, and T]k+l, let hk = [T)k-a 2'11].

Pack the

bottom subrectangle R(m,hk) of Tk with mhk unit squares in

the  natural  waOy (as shown in Fig. 4) and let TL  denote  the

remaining  uncovered  subtrapezoid  of  Tk.

xL

Fig. 4

Now, for sk = [ri,]  - hk, pack Tk with rectangles

R(l,sk-bl) as shown in Fig. 4. Here, each R(l,skfl)   touches

both the top and bottom edges of Tk as well as the adjacent

As  before, the  uncovered  border  right  triangles

R(l,sk+l)'s.
on Tk  have  total  area  m n(a -ml) = *(,3/11 ).
of  the  triangular  regions  between  adjacent  R(l,sk+l)'s   is  also

The total area

just *(a3'11) since the sum of the angles at the top vertices

is n(a -l'll).  Finally, the  uncovered  triangle  X* has area

o(,3/11) .

Since r <= *(&Q )  then  the  total  uncovered  area

in T is just r ~(a 3/11) + *((-pp  = *(J+.

-__ _ .- _ .

_-__.

-__-

--- --~__

Hence  the  total  uncovered  area  of  S(a) is just

~(a~"~)  and the theorem is proved. m
1

The  previously  mentioned  assertion  that

*.

2

f(k +ck 7'11) > 4k

follows  immediately.

It is rather annoying that we do not

at present have any nontrivial lower estimate for W(a).

Indeed

we  cannot  even  rule  out  the  possibility  that  W(a)  =  O(1).
Perhaps  the  correct  bound  is  O(a l/2 ).

In the same spirit the following questions can be

asked.

Let @ be closed convex curve of circumference 1.

Inscribe

k  non-overlapping  curves  2n @ which are all similar to @.

Denote  by  f(@,k)   the  maximum  of  the  sum  of  the  circumferences

of these curves.

If @ is a parallelogram or a triangle then

clearly f(@,j2) = 1.

All that is needed is that @ can be

covered  with  a2 copies of @.

We do not know for which figures

other  cases  of  exact  coverings  are  possible  for  other  va,lues

L

of k although for every k, there  are @Is  which  have  an  exact

covering into k parts, e.g., a rectangle.

The  following

questions can be posed:

For  which  @  is  the  growth  of f(@,k)

e

the  slowest?

Could this @ be a circle?

Which @  permit  exact

coverings?

Which @  permit  exact  coverings  with  congruent  curves

similar  to @? For such @, let 1 < nl < n2 <

. . . be the integers

for which such an exa#ct  covering  is  possible.

What can be

said about these sequences?

For example, can nk = o(k2)?

REFERENCES

[l] A. Beck and M. N. Bleicher,  Packing convex sets into

a similar set, Acta. Math. Hung. Acad. Sci. 22 (1972)

283-303.

-.

[2]  D.  J.  Newman  (personal  communication).

--

L
L
i

