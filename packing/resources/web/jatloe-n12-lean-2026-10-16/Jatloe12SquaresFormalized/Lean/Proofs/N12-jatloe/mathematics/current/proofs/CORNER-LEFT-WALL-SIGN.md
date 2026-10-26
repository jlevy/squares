# A corner above the actual left wall cannot have nonnegative angle

All decimals are exact rationals. Points in an open square are strict; an
excluded point may touch any face. The two squares below have the same side
a>1 and disjoint open interiors.

**Theorem.** Suppose L strictly owns O=(0,0), T=(0,.39), excludes
X=(.5,0), has closure in x>=-1, and has center ordinate Y_L>=0.
Suppose K strictly owns H=(0,.5), P=(0,1), and excludes A=(.44,1).
Then K has a strictly negative canonical angle. In particular, no frame

    u_K=(c,s), v_K=(-s,c), c>=s>=0, c^2+s^2=1

can describe K. No wall condition or other marker for K is required.

## 1. The two forced K faces

Assume such a nonnegative frame exists. Write U,V for K's lower faces
and J=U+a,B=V+a for its upper faces. At the excluded A, the lower-u and
upper-v inequalities follow strictly from P. Its lower-v inequality
follows strictly from H, because

    v_K(A)-v_K(H)=.5c-.44s>=.06c>0.

Consequently A exits through upper u. Also H and P are strict, so

    U<=.44c+s-a, V<.5c, B>c.                         (1)

Orient a possible separating normal n from L toward K. The strict
points O in L and H in K force n_y>0. It suffices to consider the actual
face normals of the two squares: if their interiors are disjoint, at
least one such normal weakly separates their full supports.

## 2. The left square's center lies strictly to the left of O

First take a nonnegative canonical frame for L,

    u_L=(d,t), v_L=(-t,d), d>=t>=0, d^2+t^2=1.

Denote its lower faces by l,h and upper faces by J_L,B_L. Since O is
strict, l,h<0<J_L,B_L. The foreign H has both lower bands from T,
and therefore is upper u or upper v. The excluded X has its lower-u
and upper-v bands from O, so is upper u or lower v.

If H were upper v, then B_L<=.5d. A lower-v exit at X would imply
a<=.5(d+t)<1. An upper-u exit at X would instead give J_L<=.5d,
and hence

    Y_L=t J_L+d B_L-a(d+t)/2
       <=(d+t)(d-a)/2<0.

Both are impossible. Thus

    J_L<=.5t,
    d X_L+t Y_L=J_L-a/2<0,

and X_L<0. This also excludes t=0 in this sign.

Now take a nonpositive frame,

    u_L=(d,-t), v_L=(t,d), d>=t>=0.

The point X has both lower bands from O, so is upper u or upper v.
The point H has its upper-u band from O and its lower-v band from T,
so is lower u or upper v. If H were lower u, then l>=-.5t.
An upper-u exit at X would give a<=.5(d+t)<1. An upper-v exit at X
would give B_L<=.5t and

    Y_L=-t l+d B_L-a(d+t)/2
       <=(d+t)(t-a)/2<0.

Therefore H is upper v, and

    B_L<=.5d,
    t X_L+d Y_L=B_L-a/2<0.                          (2)

The center sign now forces t>0 and X_L<0 in this sign as well.

For any up-left unit normal n=(-p,q), p,q>=0, the complete square
support and these two center inequalities give

    upper_L(n)>=n dot center(L)+a/2>=a/2>.5,
    lower_K(n)<n dot H=.5q<=.5.                    (3)

The first bound uses |n dot u_L|+|n dot v_L|>=1. Thus every up-left
source is excluded, including an axis endpoint if it occurs.

K's own up-right normal u_K is also impossible: (1) and strict T give

    lower_K(u_K)-upper_L(u_K)
       <.44c+.61s-a
       <=sqrt(.44^2+.61^2)-a<0.                   (4)

We need only check the remaining up-right normal from L.

## 3. A nonnegative L

The remaining source is u_L=(d,t). Put

    alpha=dc+ts>0, delta=tc-ds.

If delta>=0, the full lower K support and (1) give

    lower_K(u_L)<=alpha(.44c+s-a)+.5c delta.

Since t=alpha s+delta c and 0<=delta<=alpha, subtracting the strict
L point's projection .39t bounds this difference above by

    alpha(.44c+.61s-a)+.11c delta
       <=alpha(.55c+.61s-a)<0,                     (5)

because .55^2+.61^2<1. If delta<=0, the upper-v face B>c is used
instead of the lower face V, and the corresponding bound is

    alpha(.44c+.61s-a)+.61c delta<0.               (6)

Both relative angle orders, including equality, are covered. No L
source can separate the squares in this sign.

## 4. A nonpositive L

Here the remaining source is v_L=(t,d), with t>0 by (2). Put

    alpha=tc+ds>0, beta=dc-ts>=0.

The complete lower K support is bounded by

    lower_K(v_L)<=alpha(.44c+s-a)+.5c beta.         (7)

The actual left wall gives X_L>=-1+a(d+t)/2. Together with Y_L>=0,
this gives the full, actual L support bound

    upper_L(v_L)>=-t+a[1+t(d+t)]/2.               (8)

The difference of (7) and (8) decreases strictly as a increases.
At a=1 that difference is

    F=(tc+ds)(.44c+s-1)+.5c(dc-ts)
         +t-[1+t(d+t)]/2.                         (9)

The following exact coefficient identity proves F<0 on the whole
canonical domain with t>0. It is a single polynomial certificate over
a continuous rectangle, not a collection of angle tests.

Set z=s/(1+c), w=t/(1+d), so

    0<=z,w<=sqrt(2)-1<1/2,
    c=(1-z^2)/(1+z^2), s=2z/(1+z^2),
    d=(1-w^2)/(1+w^2), t=2w/(1+w^2).

Define X=2z/(1-2z), Y=2w/(1-2w). These are finite and nonnegative,
and Y>0. Direct substitution into (9) gives

    -6400 F (1+z^2)^2(1+w^2)^2(1+X)^4(1+Y)^4
       = sum_{i=0}^4 sum_{j=0}^4 C_ij X^i Y^j,     (10)

with the following exact integer coefficients (row i, column j):

| i \\ j | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| 0 | 0 | 384 | 5952 | 9248 | 4080 |
| 1 | 3584 | 12672 | 35712 | 40928 | 15680 |
| 2 | 7552 | 22720 | 54048 | 57872 | 21120 |
| 3 | 6656 | 18976 | 40992 | 41768 | 14680 |
| 4 | 2688 | 7768 | 14676 | 13554 | 4415 |

Every coefficient is nonnegative, and the term 384Y is strictly
positive. Thus F<0. Equations (7)--(9), and a>1, exclude the last
possible source.

All actual separating-normal sources have failed for both canonical
signs of L. This contradicts disjointness and proves the theorem.
The axial K case was included throughout; both diagonal representatives
are included by the closed canonical inequalities. No exclusion was
strengthened to a strict exterior inequality.

## 5. Conditional actual MMMP application

In C1092 MMMP, suppose that the actual top square Q11 omitted (2,3).
The contrapositive of Theorem 7 of C1092-DIRECT-WALL-POINT.md, reflected
through y=2 and applied to the actual paired corner Q3 and actual Q11,
then gives (1,2.5) strictly in Q3. Its other corner anchors and physical
walls are original facts; its top auxiliary F3 is supplied by the
MMMP core-owner theorem.

Translate the present theorem by (1,2), and use L=Q8,K=Q3:

| Local datum | Original datum | Actual source |
|---|---|---|
| O,T strict in L | (1,2),(1,2.39) | MMMP wall transfer and original wall-sign chord |
| X excluded from L | (1.5,2) | Strict in the actual Q7 by the MMMP crosspoint theorem |
| Left wall, Y_L>=0 | x>=0, Y8>=2 | Genuine container wall and original MMMP sign |
| H,P strict in K | (1,2.5),(1,3) | Contrary top-origin hypothesis and original paired corner |
| A excluded from K | (1.44,3) | Actual Q11 advance from C1092-MMMP-WALL-TRANSFER.md |

Therefore such a missing top origin forces a strictly negative canonical
angle of the same actual Q3. This is a conditional sign reduction only.
The remaining negative-angle coupling with the actual top square is not
claimed as a theorem here, and the top origin is not yet deduced.
