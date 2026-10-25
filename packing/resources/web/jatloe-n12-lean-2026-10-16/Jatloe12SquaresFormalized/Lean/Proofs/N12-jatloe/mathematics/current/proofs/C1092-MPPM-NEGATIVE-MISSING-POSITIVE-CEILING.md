# C1092 MPPM: a negative missing predecessor bounds a positive forward owner

All terminating decimals are exact rational numbers. Strict points belong
to the named actual open squares. Exclusion permits a point on a face,
and every separating inequality is weak. The local theorem uses the
common side a>1 and no upper side bound. Its application retains the
original no-omission all-ordinary MPPM entrance.

## 1. The continuous two-square theorem

Work in coordinates centered at (2,2). Let C have the positive canonical
frame and faces

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    U<u dot Z<A=U+a, V<v dot Z<H=V+a.

Suppose C strictly owns

    M=(-.35,-.35), P=(-1,-.26), T=(-.26,0),

and its actual lower face satisfies

    V>=.4s-c.                                      (1)

Let the actual predecessor W have the negative canonical frame

    w=(b,-r), z=(r,b), b>=r>0, b^2+r^2=1,
    L<w dot Z<J=L+a, K<z dot Z<D=K+a.

Suppose W strictly owns M_W=(-.35,.35), and its simultaneous actual
faces and angle satisfy

    L>=-b-r, J<=-.26r, D<=1.1b,
    .7<b<.825, .566<r<.71.                         (2)

The weaker cap D<=1.1b in (2) is intentional. The genuine original
missing-forward profile gives the stronger D<=1.086b.

**Theorem 1.** If C and W have disjoint open interiors, then

    s/(1+c)<1/3.                                  (3)

The proof excludes the whole closed hypothetical interval

    p>=p0:=2 arctan(1/3),
    cos p0=4/5, sin p0=3/5,

where p is C's positive angle. No angle subdivision is used.

## 2. The exhaustive actual normal cone

Direct a possible separating normal n from C toward W. The two strict
markers give n_y>0. Comparing P in C with M_W in W gives

    .65 n_x+.61 n_y>0.                             (4)

The upward northwest normal -w=(-b,r) fails (4), since
-.65b+.61r<=-.04b<0. Every downward normal fails n_y>0. Therefore
the separating-axis theorem leaves only the following actual square
face normals:

    u=(c,s), v=(-s,c), z=(r,b).                     (5)

A listed normal may fail (4) at an endpoint; retaining it for exclusion
does no harm. Put

    k=cb-sr=cos(p+phi)>=0,
    ell=cr+sb=sin(p+phi)>0,

where phi is the positive magnitude of W's negative angle. Then

    u=k w+ell z, v=-ell w+k z, z=ell u+k v.         (6)

In particular k=0, which occurs at the two diagonal representatives,
is included throughout. The strict forward point T and (1) give

    A>-.26c, H>=a+.4s-c.                          (7)

All support estimates below concern these same two actual squares.

## 3. C's northeast normal is impossible

By J<=-.26r and D<=1.1b,

    lower_W(u)=kL+ell K
      <=k(-.26r-a)+ell(1.1b-a).

Subtract this from A>-.26c. Its strict support gap is greater than

    a(k+ell)-.26c+.26kr-1.1ell b.

The coefficient k+ell is positive, so a>1 makes this strictly greater
than

    F_u=c P0+s Q0,
    P0=b+r-.26-.84br,
    Q0=b-r-.26r^2-1.1b^2.                         (8)

We have Q0<.259-.55<0, using b-r<.259 and b^2>=1/2. Since s<=c,

    F_u>=c(P0+Q0),
    P0+Q0=2b-.52-.84b(b+r).                       (9)

As a function of phi, the last expression has derivative

    -2r-.84(b^2-r^2-2br)
      <=-2r+.84<-.292<0.

Here b^2-r^2>=0 and 2br<=1. Its minimum on the entire allowed
interval is therefore its diagonal endpoint:

    P0+Q0>=sqrt(2)-1.36>.054.                     (10)

The rational comparison sqrt(2)>1.414 follows by squaring positive
sides. Thus F_u>.054c>0. The actual normal u cannot separate.

## 4. W's own northeast normal is impossible above p0

From (6),(7), the actual upper C support satisfies

    upper_C(z)=ell A+kH
      >-.26ell c+k(a+.4s-c).

Its difference from lower_W(z)=K<=1.1b-a is strictly greater than

    a(1+k)-1.1b-.26ell c+k(.4s-c).

The coefficient 1+k is positive. After replacing a by 1, the resulting
strict lower bound is exactly

    F_z=1-P1 b-Q1 r,
    P1=1.1-c+c^2-.14cs,
    Q1=s-cs+.26+.14s^2.                            (11)

We prove P1^2+Q1^2<1 on the whole hypothetical interval p>=p0.
Set x=s/(1+c). Then 1/3<=x<=sqrt(2)-1<5/12, and direct substitution
gives the exact identity

    1-P1^2-Q1^2=R(x)/[1250(1+x^2)^2],
    R(x)=-10847x^4-4770x^3+4344x^2+770x-347.        (12)

On the slightly wider interval [1/3,5/12],

    R''(x)=-130164x^2-28620x+8688
           <=R''(1/3)=-45944/3<0.

Thus R is concave. Both exact endpoint values are positive:

    R(1/3)=6622/81,
    R(5/12)=1161433/20736.                         (13)

A concave function lies above its endpoint chord, so R>0 throughout
this full interval. By Cauchy--Schwarz and b^2+r^2=1,

    P1 b+Q1 r<=sqrt(P1^2+Q1^2)<1.

Hence F_z>0, excluding W's actual normal z. This calculation makes
no sign assumption on P1 or Q1.

## 5. C's northwest normal is impossible above p0

For the remaining source v, the exact lower W support is

    lower_W(v)=-ell J+kK.

Using J>=a-b-r from the lower face in (2), and K<=1.1b-a, gives

    lower_W(v)<=-ell(a-b-r)+k(1.1b-a)
                <c f1+s g1,                      (14)

where the strict inequality uses a>1 and k+ell>0, and the exact
coefficient expansion is

    f1=1+br-b-r+.1b^2,
    g1=b^2-b+r-.1br.                               (15)

To bound these two coefficients on the full W interval, first note

    1+br-b-r=(b+r-1)^2/2
             <=1.5-sqrt(2)<.086.

Since b^2<.825^2<.681,

    f1<.086+.1(.681)=.1541<.155.                  (16)

Also the derivative of b^2-b+r with respect to phi is
b+r-2br>0, so its maximum on [0,pi/4] is 1/2. Consequently

    g1<=1/2.                                      (17)

Separation on v would give H<=lower_W(v). On the other hand,
(1) and a>1 give H>1-c+.4s. Equations (14)--(17) would therefore
require

    1<1.155c+.1s.                                 (18)

The function 1.155 cos p+.1 sin p is strictly decreasing on
[p0,pi/4], since its derivative is -1.155 sin p+.1 cos p<0 there.
At p=p0 its value is

    1.155(4/5)+.1(3/5)=123/125<1.                 (19)

This contradicts (18). All sources in (5) have now been excluded,
including their tangent and diagonal endpoints. Hence the hypothetical
p>=p0 is impossible, proving Theorem 1.

## 6. Literal application to the original four actual owners

Retain the original no-omission OOOO MPPM entrance. Suppose the actual
ordinary predecessor Q7 has negative canonical angle and omits its
forward F5=(2,2.26), while the actual ordinary Q4 has positive angle
and strictly owns its forward G3=(1.74,2).

For C=Q4, the points M,P,T in Theorem 1 are its original southwest
marker, F0=(1,1.74), and the stipulated strict G3. Its bound (1) is
the simultaneous positive-forward face bound in
C1092-MPPM-FORWARD-OWNED-POSITIVE-D.md, or Theorem 1 of
C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md. That theorem proves the
genuine preceding-D exclusion even if Q8 does not own its origin;
no wall-origin assumption is inserted here.

For W=Q7, apply Lemma 1 of
C1092-MPPM-MISSING-NEGATIVE-WALL-ORDER.md in W's own southwest
chart. The complete actual-source map is as follows. The displayed
points in the middle column use the present centered coordinates.

| Source in W's southwest chart | Present point | Literal actual source |
|---|---|---|
| Marker (-.35,-.35) | (-.35,.35) | Q7's northwest marker |
| P=(-1,-.26) | (-.26,1) | G4=(1.74,3), ordinary Q7 |
| G0=(-1,-.4) | (-.4,1) | F3=(1.6,3), ordinary Q7 |
| H=(-1,-.5) | (-.5,1) | Q7's strict halfpoint from its own F5 omission |
| Corner (-1,-1) | (-1,1) | Actual paired Q3 inner point (1,3) |
| Preceding marker (-1.086,0) | (0,1.086) | Actual Q11 marker (2,3.086) |
| Missing T=(-.26,0) | (0,.26) | F5 omitted from Q7, with no new owner asserted |
| Whole [-.56,-.26] x {-1} | {-1} x [.26,.56] | The whole actual Q8 segment from (1,2.26) to (1,2.56) |

The last segment has one actual owner: Q8 owns F1=(1,2.26), and its
ordinary advance (1,2.56) follows from the genuine F0 in Q4 by
Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md. Convexity of
that actual open square supplies the entire strict segment. Q7's
halfpoint in the table follows from the ordinary-marker halfpoint
theorem with the literal sources recorded in the ordinary-central
reduction. Neither source requires a preceding wall origin.

The inverse quarter-turn sends W's own negative-frame bounds to the
simultaneous present faces

    L>=-b-r, J<=-.26r, K>=.56b-r, D<=1.086b,
    r/(1+b)>237/763.

The exact endpoint pair

    b0=263000/319169, r0=180831/319169

gives precisely the bounds in (2), and 1.086b<1.1b. Therefore all
hypotheses of Theorem 1 hold for these same two actual squares.

**Corollary 2.** A positive forward-owned ordinary central immediately
after a negative missing-forward ordinary central has canonical
half-angle strictly less than 1/3. This holds at every sector by the
simultaneous quarter-turn R(x,y)=(4-y,x).

The corollary is independent of both remaining central signs and
forward memberships, both adjacent wall-origin memberships, and
the positive square's backward-inner membership. It provides a
continuous mixed-sign angle bound; a further origin or cyclic
conclusion must still use its own genuine hypotheses.

## 7. The genuine cap sharpens the ceiling to 7/24

The original application also has D<=1.086b and br>.46, both from
the very same missing-negative profile. Keeping these two genuine
bounds sharpens the preceding conclusion.

**Corollary 3.** Under the literal hypotheses of Corollary 2,

    s/(1+c)<7/24.                                 (20)

**Proof.** Suppose instead x>=7/24. The proof of Section 3 excluded
u for every p, so it needs no change. The proof of Section 4 works
on [7/24,5/12] with the identical norm polynomial R: its second
derivative is strictly decreasing for x>=0, and

    R''(7/24)=-515159/48<0,
    R(7/24)=16679857/331776>0.

Together with R(5/12)>0 from (13), the same concavity argument
excludes z on this whole interval.

For v use the actual cap D<=1.086b in (14), rather than its rounded
version. It gives the exact stronger inequality

    H<c f2+s g2,
    f2=1+br-b-r+.086b^2,
    g2=b^2-b+r-.086br.

The bounds already recorded above now give

    f2<.086+.086(.681)<.145,
    g2<.5-.086(.46)=.46044<.461.

Thus the same strict lower H>1-c+.4s would require

    1<1.145c+.061s.

This expression strictly decreases for p>=2 arctan(7/24). At its
left endpoint the exact pair is (c,s)=(527,336)/625, and

    1.145(527/625)+.061(336/625)=623911/625000<1.

The last possible normal is impossible, proving (20). All actual
source and owner requirements are unchanged. This stronger form
still makes no statement that the next wall origin is already owned.
