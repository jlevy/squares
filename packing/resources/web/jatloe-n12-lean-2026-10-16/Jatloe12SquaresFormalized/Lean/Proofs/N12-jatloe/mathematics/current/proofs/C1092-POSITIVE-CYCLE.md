# C1092: the positive cycle with its actual sector angles

## Status

This is a continuous positive-cycle theorem for the entire maximal positive
half-angle range through `7/64`. It uses each sector's actual central angle
as its local comparison angle. The auxiliary wall remainder theorem is
`C1092-WALL-REMAINDERS.md`; the two elementary rational inequalities used
at the end are recorded in `C1092-POSITIVE-EDGE-INEQUALITIES.md`.

The theorem is conditional on the geometric entrance stated immediately
below. It must be joined to actual C1092 endpoint or direct-geometry
entrance proofs; the theorem does not infer those hypotheses from the
original marker assignment by itself.

All constants are exact rational numbers. Put `A_*=1001/1000`.

## 1. Geometric theorem

There are four central and four boundary squares, all distinct, with common
side `1<a<=A_*`, pairwise disjoint open interiors, and contained in the
square `[0,4]^2`. Use the four sector charts under the quarter turn
`R(x,y)=(4-y,x)`. In one chart, write `C` for its central center, `J` for
the next central center, and `B` for the bottom boundary center.

The actual canonical central angles are `p_i`, with

    0 <= tan(p_i/2) <= 7/64.

The actual canonical boundary angles are `beta_i`, with

    |tan(beta_i/2)| <= 1/8.

In every sector assume:

* `C_x<=3/2<=C_y`.
* The central square strictly owns `(1,87/50)` and `(87/50,2)`,
  and excludes `(1,1)`.
* The actual boundary square strictly owns `P=(2,1)` and lies above
  the actual wall `y=0`.
* `-1/4<=C_x-B_x<=0` and `0<=C_y-B_y<=3/2`.
* `0<=J_x-B_x<=1` and `3/4<=J_y-B_y<=1`.

**Theorem.** Such eight actual squares cannot exist.

No common central angle is assumed; no square is replaced by its owned
points or by an independent support interval. Ties among the four angles
are allowed.

## 2. Forced faces and elementary bounds

Write `u_t=(cos t,sin t)` and `v_t=(-sin t,cos t)`. First,
`D=(1,2)` is strictly owned by the preceding boundary square: its local
point `(2,1)` becomes `R^(-1)(2,1)=(1,2)` in the present chart. All
eight owners are distinct, so D is outside the present central interior.
Its exclusion is a consequence, not an extra entrance premise.

In each sector the two owned points `(1,87/50)` and `(87/50,2)` force D
beyond the upper `v_p` face. The excluded point `A=(1,1)`
is then beyond the lower `u_p` face: it cannot leave through the opposite
lower `v_p` face since `|A-D|=1<a`, and the strict points exclude its other
two exits. Thus

    u_p·(C-A)>=a/2,       v_p·(D-C)>=a/2.                (1)

At `p=0` the first inequality would give `C_x>=1+a/2>3/2`. Therefore
every central angle is strictly positive.

Put `C=(3/2-X,3/2+Y)`, where `X,Y>=0`, and abbreviate
`c=cos p`, `s=sin p`, `w=c+s`. Equations (1) become

    cX-sY <=(w-a)/2,       sX+cY <=(w-a)/2.

Taking the first inequality with multiplier c and the second with
multiplier s, and using `a>=1`, proves

    X <= w(w-1)/2,       Y <= (w-1)/(2c).               (2)

Let

    c_*=4047/4145, s_*=896/4145, w_*=4943/4145,
    X_*=w_*(w_*-1)/2,   Y_*=(w_*-1)/(2c_*)=133/1349.

These are the endpoint sine, cosine, and resulting bounds at half-angle
`7/64`; the right sides of (2) increase over this interval. Hence
`0<=X<=X_*`, `0<=Y<=Y_*`. In particular,

    X_*<  3/25,       Y_*<1/10.

These bounds force one more useful strict interior point,
`L=(1,8/5)`, without any further ownership hypothesis. Indeed
`1<C_x<=3/2` and `3/2<=C_y<8/5`, so, using `s_p<1/4`,

    -1/2 < u_p·(L-C) <1/40,
       0 <= v_p·(L-C) <9/40.

Both absolute projections are smaller than `a/2`, since `a>1`.

The cyclic chart relation is

    J=(5/2-Y_next,3/2-X_next).

Consequently its displacement from C has positive horizontal and
nonpositive vertical coordinates, and for `0<=t<=2 arctan(7/64)`

    |v_t·(J-C)|
      <= s_*(1+X_*)+X_*+Y_* <11/24.                  (3)

The final strict rational inequality is a direct substitution of the
displayed fractions. Keeping their exact values is necessary here; the
two rounded upper bounds immediately above are not used to prove (3).

The actual support factor for two side-a squares at angle difference t is

    H(t)=(1+cos t+|sin t|)/2.

On the whole central difference range,

    H(t)>=1+(3/8)|t|.                                  (4)

Indeed its derivative for nonnegative t is `(cos t-sin t)/2`, which is at
least `(c_*-s_*)/2>3/8`. The function H is also globally `1/2`-Lipschitz
on the angle differences used here, with one-sided derivatives at zero.

## 3. The actual separating directions

The projection of `J-C` on a transverse normal has absolute value less
than one by (3). Its backward first projection is at most
`s_*(X_*+Y_*)<1`. Hence adjacent central squares separate along a forward
first normal of one of them. Because their displacement has positive
horizontal and nonpositive vertical coordinates, its first-normal
projection decreases with angle. Therefore the smaller of the two
central angles always satisfies the exact forward support bound:

    u_min(p,q)·(J-C) >= a H(q-p).                      (5)

This conclusion retains both possible original normal sources.

For B and C, every first-normal projection has absolute value at most
`1/4+(1/4)(3/2)=5/8<1`; every downward second-normal projection is at
most `1/16<1`. Thus only an upward second normal of B or C can separate
that pair.

For B and J the backward first projections and downward second projections
are less than one by the displayed gap bounds. The upward central-supplied
second normal is impossible because `P=(2,1)` lies in B, while the strict
point `R(1,87/50)=(113/50,1)` lies in J and has no larger second-normal
projection than P.

For the boundary-supplied upward normal, use the bottom-left vertex of J,

    V=(J_x-a(c_q-s_q)/2,J_y-a(c_q+s_q)/2).

The forced left face of J at P gives `u_q·(V-P)>=0`, while `V_y<1`.
Since `s_q>0`, this implies `V_x>2`. A nonnegative boundary angle then
gives `v_beta·(V-P)<0`. For a negative boundary angle put
`b=|sin beta|`, `h=cos beta`; the center quadrants give

    2v_beta·(V-P)
      <=(h+b)(1-c_q)-(h-b)s_q<0.

The final sign follows from

    (1-c_q)/s_q=tan(q/2)<=7/64,
    h+b<=79/65,       h-b>=47/65,
    (79/65)(7/64)<47/65.

Either sign contradicts upward separation from the strict point P of B.
Hence B and J separate along a forward first normal of B or J.

The horizontal wall-gap bounds also imply, throughout the central interval,

    v_t·(J-B) >= (3/4)c_*-s_*=8557/16580>A_*/2.        (6)

This is the favorable horizontal projection gain used below.

## 4. Quantitative wall comparison at the actual angle p

For one sector let p be its central angle and q the next central angle.
Put

    W=c_p v_p·C+s_p u_p·J,
    E=u_p·(J-C),       z=v_p·(J-C),
    delta_+=(q-p)_+,   delta_-=(p-q)_+.

**Wall comparison.** Under the above hypotheses,

    W >=(3/2)a(c_p+s_p)
         -(5/8)s_p delta_+
         -[(A_*/2)tan p+s_p/12]delta_-.               (7)

Here and below `(r)_+=max(r,0)`. The proof uses the four exact wall
identities in the handoff, with their K set equal to zero. No central
normal has been replaced by a global maximum angle.

Here are the identities and their coefficient conventions explicitly.
Put `b=sin beta`, `h_b=cos beta`, `C_0=cos(p-beta)`, and
`D_0=sin(p-beta)`. A label's first letter chooses
`V=v_p·(C-B)` for C and `V=v_beta·(C-B)` for B; its second chooses
`U=u_p·(J-B)` for C and `U=u_beta·(J-B)` for B. In every case

    W=lambda_V V+lambda_U U+lambda_C E+lambda_Z z+B_y.

| Label | lambda_V | lambda_U | lambda_C | lambda_Z |
|---|---|---|---|---|
| CC | `c_p` | `s_p` | `0` | `0` |
| BC | `c_p/C_0` | `b/C_0` | `c_p D_0/C_0` | `0` |
| CB | `h_b/C_0` | `s_p/C_0` | `0` | `s_p D_0/C_0` |
| BB | `h_b` | `b` | `h_b D_0` | `b D_0` |

Expanding `u_beta=C_0 u_p-D_0 v_p` and
`v_beta=D_0 u_p+C_0 v_p` verifies these four identities.

### 4.1. Common bounds used in all four source alternatives

The bottom wall gives `B_y>=a(cos beta+|sin beta|)/2`. The forced top face
of C and the forced bottom face of J give

    a-c_p-2s_p-(5/8)delta_+ <= z <=0.                  (8)

To check the only new term in (8), the bottom face of J is forced at
`(3,1)` in its own actual angle q. Throughout the angle interval,

    -5/8 < u_t·(J-(3,1)) <0,

by (2), `J_x in [5/2-Y_*,5/2]`, and
`J_y in [3/2-X_*,3/2]`. Since the derivative of its second-normal
projection is the negative of this expression, transporting q down to p
can lose at most `(5/8)(q-p)`; transporting q up to p is favorable.

Equations (3)--(5) give

    E>=a-(1/12)delta_-,        E-a<=1/7.               (9)

For the first inequality, descending transport loses less than
`(11/24)delta_-`, while the exact support gains at least
`(3/8)delta_-`; ascending transport is favorable. For the second,
`E<=J_x-C_x<=1+X_*<8/7` and `a>=1`.

The negative-horizontal-weight cases also have the required actual box
upper bounds. From `0<=J_x-B_x,J_y-B_y<=1`,

    u_p·(J-B)<=c_p+s_p<=a(c_p+s_p).

If `beta<0`, the same gap bounds give

    u_beta·(J-B)<=cos beta<=1<=a.

These are used, respectively, for BC and BB whenever their horizontal
weight is negative.

The positive remainder theorem gives `f>=0` for all four wall identities.
Two quantitative consequences of its factor proof will be useful:

    beta<0:     f >=(9/20)|beta|;                      (10)
    beta>p:     f >=(47/65)sin(beta-p).                (11)

For (10), the derivative of the CC remainder with respect to `gamma=-beta`
is exactly

    c_p^2 cos gamma-(1+c_p s_p)sin gamma
      =c_p cos(p+gamma)-sin gamma
      >=(63/65)(7/8)-16/65=313/520>3/5.

Here `p+gamma<1/2` implies `cos(p+gamma)>7/8`, and the remainder
at gamma zero is nonnegative. CB dominates CC.
The grouped BC and BB numerators in the remainder proof give respectively
the lower slopes `(3/4)(64/65)^4` and
`(255/512)(64/65)^3`, both larger than `9/20`.
For (11), CB and BB equal

    sin(beta-p)(1-x-y-xy)/(1+xy),

with `x=tan(p/2)`, `y=tan(beta/2)`, and the fraction is at least
`47/65`; CC and BC dominate them in this region.

For clarity, all subsequent error estimates can be read from the following
single consequence of the identities. Put
`DeltaH=H(q-beta)-H(p-beta)` and let `I_C` equal 1 when the horizontal
letter is C, and 0 otherwise. Then

    W >=(3/2)aw+a f
         +(lambda_U)_+[a DeltaH-I_C delta_+
                                      +(a/2)I_C delta_-]
         -(lambda_C)_+ delta_-/12-(-lambda_C)_+/7
         -(lambda_Z)_+(5/8)delta_+.                  (11a)

To obtain (11a), both vertical sources have their exact lower bound
`aH(p-beta)`. A positively weighted horizontal source has the lower
bound `aH(q-beta)-delta_+ +(a/2)delta_-` if its letter is C, by
normal transport and (6), or simply `aH(q-beta)` if its letter is B.
Negative horizontal weights use the just-proved box upper bounds. Use
(9) in the proper direction for either sign of lambda_C, and (8) for a
positive lambda_Z or `z<=0` for a negative one. The non-error terms are
exactly `(3/2)aw+a f`: in the positive-z term use
`a-c_p-2s_p>=a(1-c_p-2s_p)`. This also explains why no negative
coefficient is silently treated as positive in the estimates below.

### 4.2. An elementary weighted support minimum

When `0<=p<=q<=2 arctan(7/64)` and `|tan(beta/2)|<=1/8`,

    c_p H(p-beta)+s_p H(q-beta)
          +(cos beta+|sin beta|)/2
      >=(3/2)(c_p+s_p)+s_p[H(q-p)-1].                (12)

Here is a complete short verification. On every interval cut by
`beta=0,p,q`, the angle-dependent part of the left side is a positive
linear combination of sine and cosine widths. Its second derivative is
the negative of that positive combination. Hence it is concave, and its
minimum on such an interval is at an endpoint. Below zero it decreases
toward zero, and above q it increases away from q: all relevant
`cos t-sin t` factors are positive, since the differences have magnitude
less than `1/2<pi/4`. It suffices to compare beta zero, p, and q.

At beta p there is equality. Write `delta=q-p`, `c=c_p`, `s=s_p`,
`w=c+s`, `d=c-s`. The excess at beta q is

    d sin delta-c(1-cos delta)>=0,

since `tan(delta/2)<=1/8<d/c`. Twice the excess at beta zero is

    (w-1)^2-s(w-1)(1-cos delta)-s(1-d)sin delta.

Using `w-1>=7s/8`, `w-1<=s`, `1-d<=9s/8`,
`delta<1/4`, `1-cos delta<=1/32`, and `sin delta<=1/4`, this is at
least `(29/64)s^2>=0`. Thus all three endpoints satisfy (12).

### 4.3. Ascending edge: q>=p

For a central-supplied horizontal normal, transporting q down to p loses
at most `delta_+`, because `v_t·(J-B)<=1`. In the CC identity, (12) and
(4) therefore give exactly the allowed loss

    s_p[1-a(3/8)]delta_+ <=(5/8)s_p delta_+.

If `0<=beta<=p`, the BC horizontal weight satisfies
`sin beta/cos(p-beta)<=s_p`; its remainder dominates CC's. Replacing the
CC weight by this smaller nonnegative weight only improves the bound,
because the projection loss `delta_+` is at least the support increment.
For `beta<0`, the BC horizontal weight is negative and its prescribed box
upper bound has no q-transport cost. Its central coefficient is positive,
and `E>=a`, so its remainder alone suffices.

For CB or BB with `0<=beta<=p`, the horizontal normal is supplied by the
boundary. Its support increment is at least `(3/8)delta_+`. The extra
loss from (8), divided by that horizontal weight, is at most
`(5/8)sin(p-beta)delta_+<(3/8)delta_+`. Thus the support increment pays
that entire loss. For negative beta, BB uses negative horizontal and
z weights and has no new cost. In CB put `gamma=-beta`; its horizontal
weight is at most `(8/7)s_p<=2/7`. The derivative of H changes by at
most `(3/4)gamma`, and `sin(p+gamma)<=s_p+gamma`. Consequently its
support increment minus its additional z cost is at least
`-(11/8)gamma delta_+` per unit horizontal weight. Since
`delta_+<1/4`, the total extra loss is at most `(11/112)gamma`, which
is paid by (10).

It remains to cover beta above p for BC, CB, and BB. Put
`gamma=beta-p>0`. All z weights in question are negative, so (8)'s
lower-bound loss is irrelevant. In BC the horizontal weight is

    lambda_U=s_p+c_p tan gamma<=16/63,

and its central coefficient is `-c_p tan gamma`. The support increment
satisfies

    H(q-beta)-H(p-beta)>=H(q-p)-1-gamma.

This follows twice from the `1/2`-Lipschitz property of H. Using
`H(q-p)-1>=(3/8)delta_+` directly in (11a), the BC horizontal term
is bounded below by

    -(5/8)lambda_U delta_+-a lambda_U gamma.

Since `lambda_U-s_p=c_p tan gamma`, after reserving the permitted loss
`(5/8)s_p delta_+`, the extra negative contributions are at most

    c_p tan gamma[1/7+delta_+]+a lambda_U gamma
      <=(65/63)sin gamma[1/7+A_*·(16/63)+1/4].

Here `cos gamma>=63/65` and `gamma<=(65/63)sin gamma`. This argument
has kept the full BC remainder available. Its displayed costs are
dominated by (11), because

    47/65-65/441-A_*·1040/3969-65/252
       =286133/5159700>0.

For CB, use `DeltaH>=-gamma`; its only possible cost is
`a(s_p/C_0)gamma<=A_*·(16/63)(65/63)sin gamma`. For BB, the possible
costs are `a b gamma+h_b sin gamma/7`, bounded by
`[A_*·(16/63)(65/63)+1/7]sin gamma`. Both bounds are smaller than the
BC allowance already paid above. This completes the ascending case of
(7).

### 4.4. Descending edge: q<=p

A central-supplied horizontal normal gains at least `(a/2)delta_-`
when transported q up to p, by (6). Since H is `1/2`-Lipschitz, this
pays its entire possible support loss. A boundary-supplied horizontal
normal with positive weight loses at most `(a/2)lambda_U delta_-`.

First suppose `0<=beta<=p`. Every nonnegative central coefficient in the
K-zero identity is at most `s_p`; every boundary-supplied horizontal
weight is at most `tan p`. Equations (9) and the preceding support bound
therefore give the loss

    [(a/2)tan p+s_p/12]delta_-,

as required. CC has no cost, and BC has only its central-coefficient cost.

For `beta<0`, the negative horizontal weights in BC and BB use their
prescribed box upper bounds. The excess of their positive central
coefficient above `s_p` is at most `(8/7)|beta|` for BC and at most
`|beta|` for BB. In fact, writing `gamma=-beta`, the exact differences
are

    c_p tan(p+gamma)-s_p=sin gamma/cos(p+gamma)<=(8/7)gamma,
    cos gamma sin(p+gamma)-s_p=sin gamma cos(p+gamma)<=gamma.

Multiplied by the deficit `delta_-/12`, these extra
losses are at most `|beta|/42` and `|beta|/48`, respectively, and (10)
pays them. In CB, put `gamma=-beta`. Its horizontal weight exceeds
`tan p` by at most `(27/80)gamma`: use

    c_p-cos(p+gamma)<= (9/8)gamma,
    1/[c_p cos(p+gamma)]<=6/5,
    s_p<=1/4.

The extra support loss is at most
`(27027/640000)gamma`, again paid by (10). CC still has no cost.

Finally take `beta>p`, and put `gamma=beta-p`. In BC the only possible
extra cost is its negative central coefficient, at most
`(65/441)sin gamma` by (9), and (11) pays it. In CB, the horizontal
weight in excess of `tan p` is at most `s_p tan gamma`, so its extra
loss is at most `A_*(65/2016)sin gamma`, also paid by (11). In BB,
the horizontal weight exceeds `tan p` by at most gamma; its extra
support loss and negative-central-weight cost total at most

    [A_*·65/504+1/7]sin gamma <(47/65)sin gamma.

These estimates exhaust the four source labels and all boundary-angle
regions. Replacing a in the allowed error by `A_*` proves (7).

## 5. A potential that compares consecutive actual squares

For each actual central square in its own chart write

    C_i=(2-X_i,2-Y_i),
    G_i=c_i X_i+s_i Y_i,
    L_i=-s_i X_i+c_i Y_i.

The X and Y here are the coordinates relative to `(2,2)`; they are not
the nonnegative offsets in Section 2. The forced faces and the strict
interior point `(1,8/5)` derived there give

    G_i<=w_i-1/2,
    c_i+(2/5)s_i-A_*/2 <= G_i <=w_i-1/2.               (13)

Let `x=tan(p/2)`, `y=tan(q/2)`,
`kappa=cos(q-p)>0`, and `sigma=sin(q-p)`. Direct expansion of the
quarter-turn relation gives

    W=2-c_p L_i+s_p(kappa L_j+sigma G_j),              (14)
    u_p·(J-C)=G_i+kappa L_j+sigma G_j,                 (15)
    u_q·(J-C)=kappa G_i+sigma L_i+L_j.                 (16)

### Ascending: y>=x

The smaller-angle support inequality is (15). Multiply it by

    lambda=c_p/kappa-s_p>0

and add (14), using the wall bound (7). The coefficient of `L_j-L_i`
is exactly `c_p`. Because `sigma>=0`, use the upper G bounds in (13).
Also `(q-p)<=2(y-x)`. The result is

    L_j-L_i >= B_+(x,y),                              (17)

where

    B_+(x,y) = [ (3/2)w_p+lambda H(q-p)-2
                  -lambda(w_p-1/2)
                  -c_p(sigma/kappa)(w_q-1/2)
                  -(5/4)s_p(y-x)]/c_p.

All positive multiples of `a-1` have only been dropped here. The first
scalar inequality in the companion file proves

    B_+(x,y) >= f(x)-(y-x),
    f(x)=(1-c_p)(2c_p-1)/c_p.                         (18)

### Descending: y<=x

Use the smaller-angle support inequality (16). Set

    lambda=(c_p-s_p kappa)/(1+sigma)>0,
    omega=s_p kappa+lambda>0.

The coefficient of `L_i` in `W+lambda u_q·(J-C)` is `-omega`, while
that of `L_j` is `omega`. Because `sigma<=0`, use the lower G_j bound
and upper G_i bound in (13). Using `(p-q)<=2(x-y)` gives

    L_j-L_i >= B_-(x,y),                              (19)

where

    B_-(x,y) = [(3/2)w_p+lambda H(q-p)-2
                 -lambda kappa(w_p-1/2)
                 -s_p sigma(c_q+(2/5)s_q-A_*/2)
                 -(A_* tan p+s_p/6)(x-y)]/omega.

The second scalar inequality in the companion file proves

    B_-(x,y) >= f(x)+(11/10)(x-y).                    (20)

At equality `x=y`, both formulas give exactly f(x), so all angle ties
are included.

## 6. Summation and strict contradiction

Let `x_i=tan(p_i/2)`. On a closed cycle the total of the positive
increments `x_(i+1)-x_i` equals the total of the negative increments
`x_i-x_(i+1)`; call this common nonnegative number V. Summing
(18),(20) around the actual four squares gives

    0=sum_i(L_(i+1)-L_i)
       >=sum_i f(x_i)+(1/10)V.

But Section 2 proved that every `p_i>0`. Also `c_i>1/2`, and therefore

    f(x_i)=(1-c_i)(2c_i-1)/c_i>0.

The right side is strictly positive. This contradiction proves the
positive-cycle theorem, including equal central angles, tangencies, and
every normal-source tie.
