# C1092 MPPM: a missing actual wall origin forces a shallow negative boundary square

Every terminating decimal is an exact rational. Owned points are strict
interior points of their actual open squares. Excluded points may lie on
faces, and separating and wall inequalities are weak. The local theorem
uses only a common side a>1. Its original application retains the reviewed
no-omission OOOO entrance and its range 1<a<=1.001.

## 1. The local statement

Use coordinates centered at (2,2) from the southwest sector. Let C,B be
actual open squares of side a>1 with disjoint interiors. Give C its
positive canonical frame and actual faces

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    U<u dot Z<A=U+a, V<v dot Z<H=V+a.

Suppose C strictly owns

    G=(-1,-.4), T=(-.26,0),

and its simultaneous actual faces satisfy

    U>=-c-.5s, A<=0, H<=s.                       (1)

Give B its negative canonical frame and faces

    w=(b,-r), z=(r,b), b>=r>0, b^2+r^2=1,
    L<w dot Z<J=L+a, K<z dot Z<D=K+a.

Suppose B strictly owns

    M_B=(0,-1.086), A_B=(-.26,-1),

excludes both

    P=(0,-1), S=(-1,-1.086),                     (2)

and has its entire closure in the real half-plane y>=-2.

**Theorem 1.** These actual-square conditions imply

    r/b<1/4.                                     (3)

There is no positive-central angle ceiling, boundary-center hypothesis,
successor assumption or upper side bound in this local theorem.

## 2. Simultaneous faces and the real wall of B

At P the lower-w band is strict by A_B, while the upper-w and lower-z
bands are strict by M_B. Their projection increments are .26b, .086r
and .086b. Thus its exclusion forces

    D<=-b.                                        (4)

The same conclusion would be impossible for r=0, since P and A_B would
then have the same z projection. Thus an axial B could not omit P even
if that endpoint had been included in the statement.

Both upper bands of S are strict by M_B. If S were lower z, then its
face and (4) would imply

    a=D-K<=r+.086b<.836<1,

using r<=1/sqrt(2)<3/4 and b<=1. Therefore S must be lower w:

    L>=-b+1.086r, J>=a-b+1.086r.                  (5)

The lowest vertex of the same actual B is (in its own coordinates)
the point with w coordinate J and z coordinate K=D-a. The real floor
therefore gives

    -rJ+b(D-a)>=-2,
    rJ-bD<=2-ab.                                  (6)

In particular (4)--(6) simultaneously give

    rJ<=2-ab-b^2,
    bD>=a(b+r)-2-br+1.086r^2.                     (7)

These are faces of one actual square. No independently chosen bounding
square is substituted for it.

## 3. The complete actual separating cone

Orient a separating normal n from B toward C. The strict pair A_B,T
gives n_y>0. The strict pair A_B,G gives

    -.74n_x+.6n_y>0,
    n_x<(30/37)n_y.                               (8)

C's positive longitudinal normal u has n_x/n_y=c/s>=1 and fails
(8). All downward normals fail n_y>0. The separating-axis theorem for
these two actual squares therefore leaves precisely the possible
sources

    v=(-s,c), -w=(-b,r), z=(r,b).                 (9)

A retained direction may also fail (8); excluding the larger list is
valid. Put p,beta for the positive magnitudes of their canonical angles,
and set

    k=cb-sr=cos(p+beta)>=0,
    ell=cr+sb=sin(p+beta)>0,
    eta=r/(1+b)=tan(beta/2).                       (10)

The diagonal endpoint k=0 is included. The exact decompositions are

    -w=-k u+ell v,
    v=-ell w+k z,
    z=ell u+k v.                                  (11)

## 4. B's northwest normal cannot separate

For -w the exact lower C support is -kA+ell V. Equation (1) supplies
A>=a-c-.5s and V<=s-a, so

    lower_C(-w)<=-k(a-c-.5s)+ell(s-a).

The actual upper B support is -L=a-J. Using (7), the support excess
therefore satisfies

    r[upper_B(-w)-lower_C(-w)]
      >=a[b+r+r(k+ell)]-2+b^2
                       -rk(c+.5s)-r ell s.

The coefficient of a is positive. Decreasing a to 1 makes the last
quantity strictly greater than

    F=b+r-2+b^2+r[k(1-c-.5s)+ell(1-s)].           (12)

On the whole positive canonical C interval,

    -.119<1-c-.5s<0, 1-s>.292,
    k<=b, ell>=r.                                 (13)

The first lower bound follows from c+.5s<=sqrt(5)/2<1.119. Its strict
upper bound follows by writing 1-c-.5s=s[x-.5], where
x=s/(1+c)<=sqrt(2)-1<.5. For ell>=r use b>=r and c+s>=1.

Equations (12),(13) give

    F>b+r-1-.708r^2-.119br.

Also

    b+r-1=2br/(1+b+r)>.828br,

since 2/(1+sqrt(2))>.828; equivalently 293^2>2(207)^2.
Consequently

    F>.709br-.708r^2
       =.001br+.708r(b-r)>0.                     (14)

Thus upper_B(-w)>lower_C(-w), contradicting separation on this
actual normal throughout its entire canonical range.

## 5. C's northwest normal cannot separate

The exact upper B support on v is -ell L+kD. Rewrite (6) as
rL-bD<=2-a(b+r). The coefficient identity rk-ell b=-s, followed by
(4), gives

    upper_B(v)>= [ell(a(b+r)-2)-sD]/r
               >=[ell(a(b+r)-2)+sb]/r.

Since lower_C(v)=V<=s-a, its support excess multiplied by r is at
least

    a[ell(b+r)+r]-2ell+s(b-r).

Again the a coefficient is positive. At a=1 the exact remaining
scalar is

    F_v=r[1-P0 c-Q0 s],
    P0=2-b-r, Q0=(1-b)(b+r)/r=eta(b+r).          (15)

Both P0,Q0 are nonnegative, and

    b-P0=r(1-2eta)>0,
    r-Q0=eta(1-r)>0,                             (16)

because 0<eta<=sqrt(2)-1<1/2. It follows that
P0^2+Q0^2<b^2+r^2=1. Cauchy--Schwarz now gives P0c+Q0s<1, so
F_v>0. C's actual normal v cannot separate.

## 6. B's remaining northeast normal forces (3)

The caps A<=0 and H<=s give U<=-a and V<=s-a. Thus

    lower_C(z)=ell U+kV<=ks-a(k+ell).

Separation on the last source z would require D<=lower_C(z). Combine
this with the second inequality in (7). The necessary inequality is

    a[b+r+b(k+ell)]-2-br+1.086r^2-bks<=0.

Its a coefficient is positive. Hence a>1 forces the strict scalar
condition

    F0=b+r-2-br+1.086r^2
              +b^2(c+s-cs)+br(c-s+s^2)<0.         (17)

Both remaining C-angle factors have uniform canonical lower bounds:

    c+s-cs>=sqrt(2)-.5>.914,
    c-s+s^2>=.5.                                 (18)

For the first, write h=c+s in [1,sqrt(2)]; the expression is
h-(h^2-1)/2 and decreases with h. The second decreases with p because
its derivative is -c-s+2cs<0, and equals .5 at p=pi/4.

Thus (17) is strictly greater than

    f(beta)=b+r-1.086+.172r^2-.5br.               (19)

This scalar strictly increases over 0<beta<=pi/4:

    f'=(b-r)[1-.5(b+r)]+.344br>0.                (20)

At beta0=atan(1/4), b=4/sqrt(17), r=1/sqrt(17), and

    f(beta0)=5/sqrt(17)-2029/1700>0.              (21)

The exact positive comparison is

    8500^2-17(2029)^2=2263703>0.

Therefore beta>=beta0 makes F0>0, contradicting (17). All other
actual normals were already excluded in Sections 4--5. This proves
beta<beta0, equivalently (3), with all weak-support and diagonal
endpoints retained. ∎

## 7. Literal consequence for every still-missing OOOO origin

**Corollary 2.** In the original no-omission OOOO family, if an actual
boundary square omits its local wall origin, its canonical angle is
strictly negative and its magnitude beta satisfies

    0<tan(beta)<1/4.                              (22)

**Proof.** Normalize that boundary to Q9. Section 6 and Corollary 2 of
C1092-MPPM-POSITIVE-BOUNDARY-ORIGIN.md give exactly the following
facts: the actual predecessor C=Q4 is positive and forward-owned;
its faces satisfy (1); and the actual B=Q9 is strictly negative.
The local face proof there uses the actual paired corner's ownership
of (1,1.5), forced by the missing origin, the actual northwest marker,
the universal cap A<=0 and genuine preceding-D exclusion. It does
not assume any backward auxiliary to be foreign.

The remaining exact sources for Theorem 1 are:

| Local datum | Actual original source |
|---|---|
| C's G=(-1,-.4), T=(-.26,0) | G0 and forward G3, strict in Q4 |
| B's M_B=(0,-1.086), A_B=(-.26,-1) | Q9 marker and G2 |
| B exclusion of P=(0,-1) | The stated omission of (2,1) from Q9 |
| B exclusion of S=(-1,-1.086) | The original (1,.914), strict in actual Q0 |
| Entire real floor y>=-2 | Original bottom container wall y>=0 |

These are one actual C and one actual B with the same side. Theorem 1
therefore gives (22). Simultaneous quarter turns R(x,y)=(4-y,x)
transport the entire table to Q10,Q11,Q8. No conclusion here assigns
an omitted auxiliary or missing origin to any unspecified owner. ∎

This result is a conditional boundary-angle theorem. It does not by
itself assert that every origin is owned; a companion actual successor
will be used to contradict (22) when that origin has an inappropriate
strict owner.
