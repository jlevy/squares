# C1092 MPPM: a steep positive missing-crosspoint owner has a shallow negative retaining successor

All decimals are exact rationals. Strict points belong to the same actual open squares throughout. Face exclusions and separating supports allow equality. The local statement uses a common side a>1 and has no boundary-center premise.

## 1. Local actual-square inputs

Use coordinates centered at (2,2). Let C have positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,
    p0=2 atan(1/3)<=p<=pi/4,

lower faces U,V and upper faces A=U+a,H=V+a. Suppose C strictly owns

    M=(-.35,-.35), P=(-1,-.26),

and has the simultaneous actual bounds

    U>=-c-s, A<=-.5c, H<=s.                      (1)

Let E have negative canonical frame

    e=(d,-t), f=(t,d), d>=t>=0, d^2+t^2=1,

with lower faces L,K and upper faces J=L+a,D=K+a. Suppose E strictly owns

    M_E=(.35,-.35), B0=(.26,-1), B1=(.4,-1),
    I=(0,-.26),

and excludes both

    O=(0,-1), Q0=(1,-1).                          (2)

The two actual squares C and E are disjoint. The strict owner of O, when the statement is applied below, will be the same actual bottom square used by the following three-square argument.

**Theorem 1.** Under these hypotheses,

    0<t/d<3/8.                                   (3)

The following actual faces also hold:

    K>=-d, J<=d+t, L<.26t, K<.26t-d,
    L>=-.35(d-t).                                (4)

## 2. The actual negative faces and every separating source

At O both e-bands are strict, using I and B0; its upper f-band is strict by I. Thus O is lower f and K>=-d. At Q0 the lower e-band is strict by M_E, while its two f-bands follow from B0 and M_E. The latter comparison remains strict at d=t because M_E is strict. Hence Q0 is upper e and J<=d+t. The strict I and B0 give L<.26t and K<.26t-d. If t=0, this last inequality contradicts K>=-d. Therefore t>0.

Direct a separating normal from C toward E. The strict marker pair gives n_x>0. The strict M,B0 pair additionally gives

    .61n_x-.65n_y>0.                             (5)

Among the actual signed face normals only

    u, -v, e                                     (6)

can remain: the upward E-normal f has n_y/n_x=d/t>=1>61/65, and every other unlisted source has nonpositive horizontal component. A listed normal that also violates (5) at an endpoint is harmlessly retained for exclusion.

Put

    k=cd-st>=0, ell=ct+sd>0.

The exact changes of frame are

    u=k e+ell f,
    -v=ell e-k f,
    e=k u-ell v.                                 (7)

## 3. C's two normals are impossible

For u, the actual caps in (1),(4) give

    upper_C(u)>=a-c-s,
    lower_E(u)<=k(d+t-a)+ell(.26t-d).

The positive a-coefficient of the support excess is 1+k. At a=1 its exact value is

    F_u=1-P_u c-Q_u s,
    P_u=2-d-.74t^2, Q_u=t(1-.74d).                (8)

For y=t/(1+d), direct substitution gives

    1-P_u^2-Q_u^2
      =y^2(1031-5000y^2)/[625(1+y^2)^2]>0.        (9)

Indeed y<=sqrt(2)-1<5/12 and 1031-5000(5/12)^2>0. Cauchy's inequality makes (8) positive. This excludes u.

For -v, strict I and the lower K face give

    upper_C(-v)>=a-s,
    lower_E(-v)<.26ell t-k(a-d).

After dropping a to 1 in its positive coefficient 1+k, the strict gap is

    F_v=1-P_v c-Q_v s,
    P_v=.26+.74d^2-d=(d-1)(.74d-.26)<=0,
    Q_v=1+t-.74dt.                               (10)

Since d> .7 and t<.71, Q_v<1+.71(.482)<1.4<sqrt(2). Thus P_v c+Q_v s<1, using s<=1/sqrt(2). The source -v also fails.

## 4. The last normal gives the continuous shallow bound

In the only remaining actual direction e, (1) and strict I give

    upper_C(e)>=k(a-c-s)+ell(a-s),
    lower_E(e)<.26t.

The a-coefficient k+ell is positive. At a=1 the exact gap is

    F_e=-d f(p)+t B(p),
    f(p)=1+cs-c-s=(1-c)(1-s),
    B(p)=c-s+s^2-.26.                            (11)

On p0<=p<=pi/4, f increases, because

    f'(p)=(c-s)(c+s-1)>=0.

Consequently f<=1.5-sqrt(2)<.086. Also B decreases, since B'=-(c+s)+2cs<0, so B>=.24. If t/d>=3/8, (11) would therefore be strictly greater than

    d[-.086+.24(3/8)]=d/250>0.

This contradicts the last possible separating source, proving (3).

Finally the actual foreign C marker M has its upper e-band strict from M_E. Its lower f-band follows from B0 with increment .65d-.61t>0 under (3), and its upper f-band follows from I with increment .09d+.35t>0. It is therefore lower e in E, giving L>=-.35(d-t). This completes (4) and Theorem 1.

## 5. Scope in the OOOO entrance

Suppose the actual positive ordinary Q4 omits both its forward G3=(1.74,2) and its crosspoint (1.5,2). The unconditional missing-positive profile gives U>=-c-s. The crosspoint's other three bands are strict by the profile, so its omission gives A<=-.5c and p>p0. These are precisely the strict-band calculations in Section 5 of C1092-MPPM-STEEP-POSITIVE-SUCCESSOR-FAR-CAP.md.

Assume explicitly that Q4 excludes its preceding origin (1,2). This is automatic when that point is strict in actual Q8, but an exclusion rather than a named owner is sufficient. The other three bands at that point are strict by Q4's ordinary anchors and marker, so its exit is upper v and H<=s. This genuine premise is necessary here; no origin is silently assigned to Q8.

Let actual Q5 be nonpositive and retain its own forward F4=(2,1.74). Its marker,G5,F6,F4 are exactly M_E,B0,B1,I. The actual paired southeast corner Q1 owns Q0=(3,1). Q4's own missing-forward halfpoint supplies actual Q9's origin O=(2,1) by the paired-corner transfer. Both points are therefore excluded from Q5. Theorem 1 applies and yields the profile (3),(4) for that same actual Q5.

The following companion C1092-MPPM-STEEP-POSITIVE-NEGATIVE-WALL-SCALARS.md proves the complete continuous scalar obstruction after retaining the shared actual Q9. The full source composition and resulting conditional crosspoint transfer are recorded separately; this profile by itself does not claim that the actual Q4,Q5 pair is impossible.
