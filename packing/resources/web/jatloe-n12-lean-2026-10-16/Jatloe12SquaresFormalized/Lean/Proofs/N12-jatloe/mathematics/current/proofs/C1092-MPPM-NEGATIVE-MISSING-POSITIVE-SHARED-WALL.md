# C1092 MPPM: a negative missing predecessor and a positive forward owner cannot share the boundary when the preceding origin is owned

Every decimal below is an exact rational. Points stated to belong to an
actual square are strict interior points. Exclusion permits a point on
a face. All square interiors are disjoint, and every square in a local
theorem has the same side a>1. A real wall constrains its whole closure.

The first theorem is a continuous two-square statement. Its original
application in Section 5 retains one explicit wall-origin premise. No
unproved universal-origin conclusion is used.

## 1. The positive-square boundary-center theorem

Use coordinates centered at (2,2). Let C have positive canonical frame

    u=(c,s), v=(-s,c), c=cos p, s=sin p,
    0<p<=2 atan(3/10),
    U<u dot Z<A=U+a, V<v dot Z<H=V+a.

Suppose C strictly owns

    P=(-1,-.26), X=(-.5,0),

and its simultaneous actual faces obey

    U>=-c-s, A<=0, V>=.56s-c.                     (1)

Let L be an actual square of side a, disjoint from C, strictly owning

    R=(-1.086,0), D=(-1,0),

and with closure contained in x>=-2.

**Theorem 1.** The ordinate of the actual center of L satisfies

    yL>.2.                                        (2)

The orientation of L is unrestricted. Neither a boundary-center sign
nor a lower boundary origin is a premise of this local theorem.

Write x=s/(1+c). Throughout the stated closed angle interval,

    0<x<=.3, c>=91/109>5/6,
    0<s<=60/109<5/9.                              (3)

## 2. The complete actual normal cone

Suppose yL<=.2. Direct a possible separating normal n from C toward
L. Comparing strict P in C with D in L gives n_y>0. Comparing strict
X in C with R in L gives n_x<0. Thus the separating-axis theorem for
these two actual squares leaves only

    v=(-s,c),
    an actual northwest face normal of L.          (4)

Indeed C's u points northeast, and its other two signed normals point
downward. Every remaining actual normal of L has the form

    n=(-h,r), h=cos phi, r=sin phi,
    0<=phi<=pi/2.                                 (5)

The strict cone removes the coordinate endpoints, but we retain them
in the scalar proof. Every orientation and both signs of a canonical
angle of L are covered by (5).

We use one elementary square-width fact. If k is a square's unit-side
horizontal width and w its unit-side width in direction v=(-s,c), then

    k+w>=1+c+s, w>=1,
    s k+w>=1+s(c+s).                              (6)

For the first inequality, subdivide a full orientation period at the
zeros of the scalar products inside the two absolute-value widths.
On each resulting interval k+w is positive and its second derivative
is its negative, so its minimum is at an endpoint. At every endpoint
one width is 1 and the other is c+s. The inequality w>=1 is immediate
for a unit normal. Taking s times the first inequality plus 1-s times
the second gives the last inequality in (6). This proof includes all
coincident endpoints and has no orientation restriction on L.

## 3. C's own normal cannot separate

Let k,w be the widths in (6) for the actual L. Its real left wall and
the supposed yL<=.2 give

    lower_L(v)<=2s+.2c-(a/2)(s k+w).

On the other hand, (1) gives upper_C(v)=H>=a+.56s-c. The difference
of these actual supports is therefore strictly greater than

    F0(p)=1.5-1.2c-1.44s+.5s(c+s),                (7)

using a>1 in a positive coefficient and then (6).

The exact half-angle substitution gives

    50(1+x^2)^2 F0
      =135x^4-194x^3+250x^2-94x+15.              (8)

For 0<=x<=.3, the numerator is at least

    (959/5)x^2-94x+15
      =(959/5)(x-235/959)^2+3340/959>0.            (9)

Here -194x^3>=-58.2x^2 and 135x^4>=0. Thus F0>0 on the whole
interval. Consequently upper_C(v)>lower_L(v), excluding v.

## 4. Every actual normal of L also fails

For (5), the horizontal unit-side width of L is h+r, and its width
in its own face normal n is exactly 1. Its true left wall and center
bound imply

    lower_L(n)<=2h+.2r-(a/2)[1+h(h+r)].            (10)

The coefficients of this same normal in C's frame are

    lambda=-ch+sr=-cos(p+phi),
    kappa=cr+sh=sin(p+phi)>0,
    n=lambda u+kappa v.                           (11)

There are exactly two relative-angle orders.

### 4.1. The order phi<=pi/2-p

Here lambda<=0. The actual cap A<=0 gives U<=-a, while (1) gives
H>=a+.56s-c. Hence

    upper_C(n)=lambda U+kappa H
       >=a(kappa-lambda)+kappa(.56s-c).

Subtracting (10), and lowering a to 1 in the positive coefficient
kappa-lambda+[1+h(h+r)]/2, shows that the support difference is
strictly greater than

    F(phi)=.5+.5h^2+.5hr+A1 h+B1 r,
    A1=c+s-2+.56s^2-cs,
    B1=c-s-1.2+s^2+.56cs.                         (12)

We have A1>=-1. Indeed

    A1+1=s^2[.56-(1-s)/(1+c)]>=.06s^2>=0,         (13)

because c+2s>=1 gives (1-s)/(1+c)<=1/2.

Also B1>-.36 on (3). Here is an exact continuous verification. Its
derivative with respect to x is

    dB1/dx=2[39x^4-150x^3-84x^2+50x-11]
                   /[25(1+x^2)^3]<0.             (14)

For 0<=x<=.3, the bracket is at most -80x^2+50x-11, whose
discriminant is -1020. Thus B1 decreases, and its exact endpoint is

    B1(.3)=-21103/59405=-.36+1414/297025>-.36.     (15)

It follows from (12) that

    F(phi)>=.5(1-h)^2+r(.5h-.36).                 (16)

Put w=r/(1+h), so 0<=w<=1. The right side of (16) equals

    2w[w^3-(43/50)w^2+7/50]/(1+w^2)^2.           (17)

The cubic in brackets attains its minimum on [0,1] at w=43/75:

    w^3-(43/50)w^2+7/50>=19309/421875>0.          (18)

Its derivative is w(3w-43/25), which proves that minimum over the
whole interval. Thus (16) is nonnegative, including w=0. The strict
a>1 support reserve retained before (12) excludes separation even at
that zero endpoint. Every normal in this relative-angle order fails.

### 4.2. The order phi>=pi/2-p

Here lambda>=0. Use the actual lower-face consequence A>=a-c-s
instead of the upper cap, and retain the same H lower bound. Then

    upper_C(n)=lambda A+kappa H
       >=a(lambda+kappa)-lambda(c+s)+kappa(.56s-c).

After subtracting (10), its positive a coefficient again gives a
strict lower bound of the same form

    F(phi)=.5+.5h^2+.5hr+A2 h+B2 r,
    A2=s-c-1-.44s^2,
    B2=c+s-1.2-.44cs.                             (19)

Throughout (3),

    -A2>=16844/11881>7/5, B2>=-1/5.              (20)

For the first bound, 1+c-s+.44s^2 strictly decreases with p, since
its derivative is -c-s+.88cs<0; its right endpoint is the fraction
in (20). For the second, use
c+s-1=2cs/(1+c+s)>=.8cs>=.44cs.

In this order h<=s<5/9 and r>=c>5/6. Differentiating (19) and using
(20) gives

    F'=-hr+.5(h^2-r^2)-A2 r+B2 h
       >r(7/5-h-r/2)-h/5
       >19/108>0.                                (21)

The last estimate uses r<=1, h<5/9 and r>5/6:
7/5-h-r/2>31/90 and
(5/6)(31/90)-(1/5)(5/9)=19/108.

Therefore the minimum is at phi=pi/2-p, where h=s,r=c and direct
substitution gives

    F(pi/2-p)=F0(p)>0.                            (22)

Every normal in the second relative-angle order also fails, including
the joining angle. Equations (4), (7), (16) and (22) exhaust all
actual-square separating axes. This contradicts disjoint interiors,
proving Theorem 1. The proof allows tangent closures and uses no angle
samples or independently chosen replacement square. ∎

## 5. The literal negative-missing/positive-owned edge

Retain the original no-omission OOOO MPPM entrance and its actual
owners. Suppose Q7 has negative canonical angle and omits its forward
F5=(2,2.26), while Q4 has positive canonical angle and strictly owns
its forward G3=(1.74,2). Add the explicit premise

    (2,3) is strict in actual Q11.                 (23)

**Corollary 2.** These simultaneous original conditions are impossible.

**Proof.** Set C=Q4 and L=Q8 in coordinates translated by (-2,-2).
Corollary 3 of C1092-MPPM-NEGATIVE-MISSING-POSITIVE-CEILING.md gives

    x_C<7/24<.3.

Theorem 1 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md supplies the
simultaneous actual bounds U>=-c-s and A<=0. Its Theorem 2 gives the
strict crosspoint X=(-.5,0) for this forward owner without an angle
condition. The strict point P is original F0=(1,1.74).

We also need the stronger V bound in (1), and derive it here from its
actual source. The far point F=(-.56,-1), original (1.44,1), belongs
strictly to actual Q9 by the retained ordinary wall advance. It is
therefore excluded from C. Three of its bands are strict by original
G0, the southwest marker, and F0:

    u(F)-u(G0)=.44c-.6s>0,
    u(M)-u(F)=.21c+.65s>0,
    v(P)-v(F)=.44s+.74c>0.

For the first sign use s/c<=60/91<11/15. Hence F can only exit
through lower v, proving V>=.56s-c. No bottom-origin premise is
needed for this far point.

The F5 omission in actual Q7 supplies its outer halfpoint (1.5,3),
and the already audited paired-corner transfer gives (1,2) strictly
in actual Q8. Thus L has the genuine strict D=(-1,0). Its R is the
original Q8 marker (.914,2), and its real wall is the original x>=0.
Every premise of Theorem 1 is now supplied by the same actual squares,
so in the present coordinates

    y_center(Q8)>.2.                              (24)

For the opposite inequality, apply Lemma 1 and Theorem 2 of
C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md to Q7 and Q8. The literal
map from that theorem's southwest chart (xi,eta) into the present
coordinates is (x,y)=(eta,-xi). Its entire source ledger is

| Source in the local negative theorem | Present point | Actual original source |
|---|---|---|
| C marker (-.35,-.35) | (-.35,.35) | Q7 northwest marker |
| P=(-1,-.26) | (-.26,1) | G4=(1.74,3) in Q7 |
| G0=(-1,-.4) | (-.4,1) | F3=(1.6,3) in Q7 |
| H=(-1,-.5) | (-.5,1) | Q7 halfpoint from its F5 omission |
| Excluded corner (-1,-1) | (-1,1) | (1,3) in actual Q3 |
| Excluded preceding D=(-1,0) | (0,1) | Explicit strict Q11 origin (23) |
| Excluded forward T=(-.26,0) | (0,.26) | F5 omitted from Q7; no new owner assigned |
| Excluded whole [-.56,-.26] x {-1} | {-1} x [.26,.56] | One actual Q8 bar from F1 to (1,2.56) |
| B marker (0,-1.086) | (-1.086,0) | Actual Q8 marker |
| B point (-.4,-1) | (-1,.4) | G1=(1,2.4) in Q8 |
| B real bottom wall | Present left wall x>=-2 | Original Q8 container wall x>=0 |

The whole bar is in Q8 because its strict F1=(1,2.26) and its strict
ordinary advance (1,2.56) have that one actual owner. The common side
is unchanged by the quarter-turn. Lemma 1 therefore supplies all its
simultaneous strong faces and half-angle >7/18. Theorem 2 then gives
x_B>-.2 in the southwest chart. Since x_B is exactly the negative of
the present center ordinate of Q8, this is

    y_center(Q8)<.2,                              (25)

contradicting (24). This proves Corollary 2. ∎

Simultaneous quarter turns R(x,y)=(4-y,x) transport the entire proof,
its actual shared wall and its explicit preceding-origin hypothesis.
In cyclic notation: a negative missing-forward ordinary central
followed by a positive forward-owned ordinary central is impossible
when the boundary origin preceding the negative central is strict.

## 6. The stronger strict point forced by the same argument

**Corollary 3.** Without assuming (23), a negative missing-forward
Q7 immediately before a positive forward-owned Q4 must itself strictly
own (2,3). In particular actual Q11 omits that origin.

**Proof.** All inputs giving (24) were independent of (23). Suppose
(2,3) were not strict in Q7. In the source table for the negative
theorem, replace only the row for excluded preceding D by this stated
Q7 exclusion. Lemma 1 of MISSING-NEGATIVE-BOUNDARIES requires merely
that D be excluded from its actual central square; it does not require
a different owner for D. Every other source in the table is unchanged.
Its Theorem 2 again gives (25), contradicting (24). Hence (2,3) is
strict in Q7, and disjoint interiors exclude it from Q11. ∎

Simultaneous quarter turns give the analogous strict point in each
negative predecessor. This conclusion concerns membership in that
actual central square. It does not assign any other omitted auxiliary
or assert ownership of the remaining boundary origins.
