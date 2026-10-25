# C1092 MPPM: the predecessor caps a center-owned negative inward square

Every terminating decimal is an exact rational. All owned points below
are strict; excluded faces and separating supports may be equalities.
The common side is a>1. Retain the original no-omission MPPM entrance
and its twelve actual owners. Normalize a nonordinary inward owner to
Q4 and suppose that Q4 strictly owns O=(2,2) and has negative canonical
orientation. No ordinary status of the opposite Q6 is assumed.

Translate by (-2,-2), put C=Q4, E=Q5, W=Q7, and use C's frame

    u=(c,-s), v=(s,c), c>=s>0, c^2+s^2=1.

Write U,V and A=U+a,H=V+a for its lower and upper faces.

**Theorem 1.** In this actual configuration,

    A<=.14c+.5s, H<17/125=.136.                     (1)

The proof uses the actual ordinary neighbors E and W, the true right
bar, and the true top and paired-corner points. In particular (1) does
not assume a center status for any other owner.

## 1. The marker caps and one new strict point in E

The center-owned face calculation in
C1092-MPPM-NEGATIVE-INWARD-SUCCESSOR-SIGN.md, Section 6.1, gives

    U,V<0<A,H,
    A<=.35(c+s), H<=.35(c-s).                       (2)

It also supplies A>=a-c+.26s in both actual nonordinary alternatives:
G0 is omitted, or G0 is owned and F0 is omitted. The successor-sign
theorem therefore makes the one actual ordinary E strictly negative.
The whole-bar theorem
C1092-MPPM-NEGATIVE-SUCCESSOR-BAR-PROFILE.md supplies its full table

    u_E=(d,-t), v_E=(t,d), d>=t>0,
    L>=.26t, J=L+a<=d+t,
    K>=-1.086d, D=K+a<=t-.4d.                     (3)

The point Z_E=(.14,-.5) is strict in that E. Using (3), its four band
gaps are bounded below, respectively, by

    a-.86d-.5t,
    a-.14d-.24t,
    a-.1d-.86t,
    a-.586d-.14t.                                  (4)

The squared coefficient norms are .9896, .0772, .7496 and .362996,
all less than 1. Cauchy's inequality and a>1 make all four gaps strict.

The actual inward-center diagonal theorem
INWARD-CENTER-DIAGONAL-POINT.md, Corollary 2, applied after the half-turn,
puts (-.61,-.61) strictly in C. Its hypotheses are precisely C's
strict center and marker, and the two actual neighboring markers in
E,W. At the foreign point Z_E, C's lower u-band follows from O, since
u(Z_E)=.14c+.5s>0. Its upper v-band follows from O, because
v(Z_E)=.14s-.5c<0. Its lower v-band follows from the strict diagonal
point, with increment .75s+.11c>0. Therefore Z_E is upper u and

    0<A<=A0:=.14c+.5s.                              (5)

We will use D0=1-A0. On the entire canonical C interval,

    .54<D0<=.86.                                    (6)

Indeed A0 increases with p=arctan(s/c): its derivative is .5c-.14s>0.
Thus .14<=A0<=.64/sqrt(2)<.46. This proves (6).

## 2. The actual predecessor data and its face alternatives

The inward-neighbor theorem in
C1092-MPPM-NO-OMISSION-REDUCTION.md, Section 1, gives the actual ordinary
pair F3,G4 in W. Its strict centered points are

    M_W=(-.35,.35), T0=(-.26,1), T1=(-.4,1).         (7)

The following points are excluded from W by strict actual ownership:

    Z=(0,1.086)       in Q11,
    C0=(-1,1)        in Q3,
    C1=(-1,1.086)    in Q3.                         (8)

Here C1 is the original paired-corner marker (1,3.086), not an
additional point declared owned along a wall.

For either canonical sign of W write P,Q for its lower faces and
J_W=P+a,D_W=Q+a for its upper faces.

If W has nonnegative frame (b,r),(-r,b), b>=r>=0, then Z is upper u
or upper v. The point C0 is lower u or upper v. The point C1 is also
lower u or upper v. If Z is upper u and C1 is lower u, the opposing
faces give a<=b<=1. Consequently the following complete table holds:

    always:                 D_W<=1.086b+r;
    Z upper v:              D_W<=1.086b;
    Z upper u:              J_W<=1.086r;
    Z upper u,C0 upper v:   D_W<=b+r;
    Z upper u,C0 lower u:   P>=-b+r,
                             a<=b+.086r,
                             D_W<=1.086b+r.         (9)

In the last row the exact half-angle identity implies

    r/(1+b)<.086, r<.172, b+r<29/25.                (10)

The sum b+r is increasing through the canonical interval, and at
half-angle .086 it equals 291151/251849<29/25.

For completeness, at Z both lower bands follow from T0,M_W. At C0
its upper u-band follows from T0 and its lower v-band from M_W. The
same bands at C1 have increments .74b-.086r>0 and .736b+.65r>0.
These are exactly the exits and the strict anchor sources in (9).

If W instead has nonpositive frame (b,-r),(r,b), its C0 has upper
u-band from T0 and both v-bands from M_W,T0. Thus it is lower u.
The lower bands of Z follow from T0,M_W; its upper-u alternative
would give a<=b-.086r<=1. Hence

    P>=-b-r, J_W>=a-b-r,
    D_W<=1.086b, Q<=1.086b-a.                     (11)

The zero increments at r=0 or b=r compare with strict anchors, so
every displayed band remains strict at those endpoints.

## 3. The complete normal list

Suppose, for contradiction, that H>=eta, where eta=.136. Orient a
separating normal from C toward W. Their strict markers force n_y>0.
C's upward left-facing source -u cannot separate, because (2) gives

    upper_C(-u)=a-A>1-.35(c+s)>.35(c+s)=(-u) dot M_W.

The strict inequality uses .7(c+s)<=.7sqrt(2)<1. Thus C's only
remaining source is v=(s,c).

For nonnegative W, its upward longitudinal source (b,r) is excluded
by strict O in C and its marker: (b,r) dot M_W=.35(r-b)<=0.
Only W's own transverse source (-r,b) remains alongside v. For
nonpositive W, its two upward sources (r,b),(-b,r) remain alongside
v. This is the full signed face-normal list. We exclude both closed
W sign domains below.

## 4. Nonnegative W: its own normal

Put

    k=cb-sr>=0, j=cr+sb>=0.

The exact upper C support on (-r,b) is j(a-A)+kH. Use (5), H>=eta
and the first row of (9). After subtracting Q, the support difference
is strictly greater than

    F=1-1.086b-r+jD0+k eta
      =1-b B_eta-r R_eta,                           (12)

where

    B_eta=1.086-s+.14cs+.5s^2-eta c,
    R_eta=1-c+.14c^2+.5cs+eta s.                   (13)

The coefficient of a before replacing a by 1 is 1+j>0. We prove a
single full-domain norm bound for these two coefficients. With
x=s/(1+c), direct expansion gives

    1-B_eta^2-R_eta^2
       =P_eta(x)/[250000(1+x^2)^2],                 (14)

    P_eta(x)=-1268221x^4+2172040x^3-2285146x^2
                  +727960x+19475.

Its second derivative is a quadratic with negative leading
coefficient and discriminant -108375454527936<0. Hence P_eta is
strictly concave on the whole real line. Its endpoint values on
0<=x<=5/12 are

    P_eta(0)=19475,
    P_eta(5/12)=932304275/20736.

Concavity therefore makes P_eta positive on the entire interval,
which contains every canonical half-angle. Thus

    B_eta^2+R_eta^2<1.                               (15)

Cauchy's inequality makes (12) positive, excluding W's own normal.

## 5. Nonnegative W: C's normal

The exact lower W support on v is jP+kQ. If Z is upper v, its strict
marker gives P<.35(r-b)<=0, and (9) gives Q<.086. Hence the lower
support is less than .086, and cannot reach H>=eta.

Suppose Z is upper u. If C0 is upper v, (9) gives

    lower_W(v)<=j(1.086r-a)+k(b+r-a)
                <c F0-s F1,                        (16)

    F0=.5(b+r-1)^2+.086r^2,
    F1=r^2+b-r-.086br.

Here F1>=0, since b>=r implies
b(1-.086r)+r(r-1)>=.914r^2>=0. Also
F0<=1.543-sqrt(2)<.13. Thus (16) is less than .13<H.

If C0 is instead lower u, use (10) and the cap at C1 to obtain

    lower_W(v)<=j(1.086r-a)+k(1.086b+r-a)
                <c G0-s G1,                        (17)

    G0=.086+.5(b+r-1)^2<.0988,
    G1=r^2+b-r>=0.

This is again less than eta. The strict coefficient of a in each
line is j+k>0. All faces and both actual nonnegative-W sources fail.

## 6. Nonpositive W: C's normal and the upward right-facing normal

Use (11), and put

    k=cb+sr=cos(phi-p)>0,
    delta=cr-sb=sin(phi-p).

First consider C's own normal v. If phi<=p, then delta<=0 and

    lower_W(v)=(-delta)P+kQ<.086,

because P is strictly below the negative u_W marker projection and
Q<.086. If phi>=p, then

    lower_W(v)=-delta J_W+kQ
       <=delta(b+r-a)+k(1.086b-a)
       <c f-s g,                                    (18)

    f=.086b^2+.5(b+r-1)^2,
    g=b^2-.086br-b+r>=0.

For the last sign, b(1-b)=br^2/(1+b)<=r^2/2 gives
g>=r(.914-r/2)>=0.

The scalar f<.136 throughout the canonical W range. Here is its
complete exact certificate. Put w=r/(1+b), 0<=w<5/12, and h=w-1/3.
Then

    500(1+w^2)^2(.136-f)
      =-975w^4+2000w^3-778w^2+25
      =16/27+(32/9)h+h^2(572+700h-975h^2).

For -1/3<=h<=1/12 the parenthesis is at least 691/3. The resulting
quadratic 16/27+(32/9)h+(691/3)h^2 has positive leading coefficient
and discriminant -1600/3. It is strictly positive. Consequently
(18) is less than .136c<=eta and cannot separate.

Next consider W's upward right-facing source (r,b). If delta>=0,
its upper C support is delta A+kH. If delta<=0, it is
(-delta)(a-A)+kH. Both A and a-A are positive by (2), so in either
case this support is at least kH. Since k>=1/sqrt(2)>7/10,

    upper_C(r,b)>=kH>(.7)(.136)=.0952>.086>Q.

This source is impossible in both angle orders.

## 7. Nonpositive W: its upward left-facing normal

For n=(-b,r), first suppose phi>=p. Its upper C support is
k(a-A)+delta H. By (11), its lower W support is -J_W<=b+r-a.
The difference is strictly greater than

    F=1-b-r+kD0+delta eta
      =1-b R_eta-r(B_eta-.086).                    (19)

The coefficients B_eta,R_eta are the same functions of C as in
(13). Also B_eta>1.086-s-eta>.24>.043. Subtracting .086 therefore
strictly reduces its squared norm:

    R_eta^2+(B_eta-.086)^2<B_eta^2+R_eta^2<1.

Thus (19) is positive by Cauchy's inequality.

Suppose instead phi<=p and put e=-delta>=0. The upper C support is
k(a-A)+e(a-H). Use the cap H<=.35(c-s) in (2). After subtracting
b+r-a the support difference is strictly greater than

    F=1-b-r+kD0+e E0,
    E0=1-.35(c-s)>0.                               (20)

Write F=1-P0 b-Q0 r, where

    P0=1-cD0-sE0, Q0=1-sD0+cE0.

One has Q0>0 and

    Q0-P0=(c-s)D0+(c+s)E0>0.

Therefore P0 cos phi+Q0 sin phi is nondecreasing through the
canonical interval, by the same elementary derivative check whether
P0 is positive or negative. On 0<=phi<=p, its maximum is at phi=p.
At that endpoint (20) is

    2-1.14c-1.5s
      >=2-sqrt(1.14^2+1.5^2)
      =2-sqrt(3.5496)>0.                            (21)

This excludes the last actual source. The coefficient of a in (19)
is 1+k; in (20) it is 1+k+e. Both are strictly positive. Thus every
weak support equality has been covered too.

Sections 3-7 exhaust both canonical signs of the actual W and every
normal in the strict marker cone. They contradict H>=eta, proving
H<.136. Together with (5), this proves Theorem 1.

The source table (7)-(11) and the complete normal lists are retained
as a local predecessor profile for subsequent steps. This chapter
asserts the two bounds (1), not a complete ending of the negative
center-owned inward branch.
