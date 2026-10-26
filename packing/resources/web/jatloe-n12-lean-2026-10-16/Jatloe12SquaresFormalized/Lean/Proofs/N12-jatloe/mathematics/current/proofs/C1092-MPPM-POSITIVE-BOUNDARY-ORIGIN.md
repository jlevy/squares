# C1092 MPPM: a positive boundary square cannot miss its wall origin

Every terminating decimal is an exact rational. A point described as owned is strict in its actual open square. Excluded faces and separating supports may meet with equality. The local theorem uses a common side a>1, actual square supports and the real bottom wall. It has no upper side bound and no boundary-center premise.

The application uses the original no-omission OOOO entrance and its explicitly retained range 1<a<=1.001, because the universal positive central cap was proved in that range.

## 1. Local statement

Use coordinates translated by (-2,-2) from a southwest sector. Let C,B be actual open squares of side a>1 with disjoint interiors. Suppose C has nonnegative canonical frame

    u=(c,s), v=(-s,c), c>=s>=0, c^2+s^2=1,

lower faces U,V and upper faces A=U+a,H=V+a, with

    U>=-c-.5s, A<=0, V<=s-a.                     (1)

Suppose C strictly owns

    G=(-1,-.4), T=(-.26,0).

Suppose B has nonnegative canonical frame

    e=(b,r), f=(-r,b), b>=r>=0, b^2+r^2=1,

has its closure in y>=-2, and strictly owns

    M_B=(0,-1.086), L_B=(-.4,-1), T_B=(-.26,-1).

Retain the genuinely excluded whole corner segment

    I_K={-1} x [-1.086,-1],                       (2)

which, for example, may be strict in one different actual square.

**Theorem 1.** The actual B strictly owns P_B=(0,-1).

Neither the angle of C nor that of B has an incoming subdivision. The proof keeps their two relative-angle orders only to identify the correct actual supporting vertices.

## 2. What a missing origin would imply for B

Write L,K for the lower faces of B and J=L+a,D=K+a for its upper faces. Suppose P_B were missing. Its lower e-band and both f-bands are strict by M_B,L_B. Thus it could leave B only through its upper e-face:

    J<=-r.                                        (3)

The direct wall-and-corner-segment lemma in Section2 of C1092-DIRECT-WALL-POINT.md applies after adding (2,2). Its strict marker and anchor are (2,.914),(1.6,1), its actual bottom wall is y>=0, and its excluded segment is exactly the translated (2). That lemma proves P_B whenever ab>=.914, including equality. Consequently the supposed missing P_B forces

    ab<457/500, hence b<457/500.                   (4)

In particular r>0. A convenient exact consequence of (4) is

    r/b>5/12>sqrt(2)-1.                           (5)

Indeed

    (457/500)^2[1+(5/12)^2]
       =1-704519/36000000<1,

so b<457/500 implies 1-b^2>(25/144)b^2. The second strict inequality in (5) is equivalent to sqrt(2)<17/12, whose square is 2<289/144.

The real bottom wall is the exact inequality

    rL+bK>=-2.

Equivalently,

    rJ+bD>=a(b+r)-2.                              (6)

Equations (3),(6) are simultaneous inequalities for the faces of the same actual B. In particular

    D>=[a(b+r)-2+r^2]/b.                          (7)

No pointwise hull support has replaced this actual-square constraint.

## 3. The two actual separating normals

Orient a proposed separating normal from B toward C. The strict pair T_B,T gives n_y>0. The strict pair T_B,G then gives

    -.74n_x+.6n_y>0,
    n_x<(30/37)n_y.                               (8)

In the nonnegative canonical frames, neither upward longitudinal normal u or e can satisfy (8), because its horizontal component is at least its vertical component. Both negative transverse normals point downward, and both negative longitudinal normals have nonpositive vertical component. The separating-axis theorem therefore leaves only

    v=(-s,c), f=(-r,b).                            (9)

At a canonical endpoint a listed direction may also fail the strict cone; retaining it for exclusion loses nothing.

Write p,beta for the nonnegative C,B angles, and set

    k=cb+sr=cos(beta-p)>0,
    delta=cr-sb=sin(beta-p), h=b+r.

Thus v=delta e+k f. We use only the two actual vertex formulas corresponding to the signs of delta.

## 4. C's transverse normal

The exact upper B support on v is

    delta J+kD+a max(-delta,0).

From (6),

    delta J+kD
       >=(delta-kr/b)J+k[a h-2]/b
        =-(s/b)J+k[a h-2]/b
       >=sr/b+k[a h-2]/b,                         (10)

where the last step uses (3). Since lower_C(v)=V<=s-a, multiplication of the support excess by the positive b gives the lower bound

    a[b+kh+b max(-delta,0)]-2k+s(r-b).

Its coefficient of a is positive. The actual support excess is therefore strictly positive whenever

    F_v=b+k(h-2)+s(r-b)+b max(-delta,0)>=0.        (11)

We in fact prove the scalar strictly positive.

### 4.1. beta>=p

Here delta>=0. Put

    A0=b(2-h)>0, B0=b-r(h-1)>0.

The positivity of B0 follows from r<=b and h<2. Exact expansion gives

    F_v=b-A0 c-B0 s.

For 0<=p<=beta,

    dF_v/dp=A0 s-B0 c
       <=c[A0(r/b)-B0]=c(r-b)<=0.                 (12)

Consequently its minimum on this entire interval is at p=beta. At that endpoint,

    F_v=2b+r-2+r^2-br
        =r^2(h-1)/(1+b)>0,                        (13)

because r>0 and h>1.

### 4.2. beta<=p

Here delta<=0. The exact expansion is

    F_v=b-b(2-b)c+[1+br-b-r]s
       =b-b(2-b)c+[(h-1)^2/2]s.                   (14)

Its p-derivative is nonnegative throughout the canonical interval. Hence its minimum for p>=beta is again the endpoint p=beta, with the strictly positive value (13). This excludes C's source v for both relative-angle orders. Notice that this part of the proof needed only r>0, not the stronger angle bound (5).

## 5. B's transverse normal

The exact lower C support in direction f has coefficient -delta on u and k on v. There are two orders.

If beta>=p, then delta>=0 and the upper face A is used with its negative coefficient. From A>=a-c-.5s and V<=s-a,

    lower_C(f)=-delta A+kV
       <=-delta(a-c-.5s)+k(s-a).                  (15)

If beta<=p, then delta<=0 and the lower face U is used with its nonnegative coefficient. Since A<=0 gives U<=-a,

    lower_C(f)=-delta U+kV
       <=a delta+k(s-a).                          (16)

Compare (15),(16) with the genuine lower bound (7) for upper_B(f)=D. After multiplying by b and decreasing a to 1, the two sufficient scalar margins are respectively

    F_+=h-2+r^2+b Phi_+(p),
    Phi_+=k(1-s)+delta(1-c-.5s),                  (17)

and

    F_-=h-2+r^2+b Phi_-(p),
    Phi_-=k(1-s)-delta.                           (18)

The coefficients of a before the decrease were h+b(k+delta) in (17) and h+b(k-delta) in (18). They are positive in their respective orders. Hence proving these scalars nonnegative already excludes a weak separating equality for a>1.

### 5.1. A single curvature calculation for both orders

Let H0=c+s and Z0=c-s. The exact identities are

    Phi_+=b(c-s+.5s^2)+r(c+s-1-.5cs),

    Phi_+''=b Z0(H0-1)-r(H0-2cs),
    Phi_-'=-Phi_+''.                              (19)

The primes are derivatives with respect to p, holding the actual B angle fixed. On the full canonical interval,

    H0-2cs>0,
    H0-2cs-Z0=2s(1-c)>=0,
    0<=H0-1<=sqrt(2)-1<5/12.

Together with (5), these give the strict sign

    Phi_+''
      <=[b(H0-1)-r](H0-2cs)<0.                    (20)

Thus Phi_+ is strictly concave and Phi_- is strictly increasing throughout the whole canonical C-angle interval. This continuous sign argument replaces any division into numerical angle bins.

### 5.2. beta>=p

The scalar F_+ is concave for 0<=p<=beta, so its minimum occurs at one of the two endpoints. The exact endpoint values are

    F_+(0)=h-1>0,
    F_+(beta)=r^2(h-1)/(1+b)>0.                    (21)

Therefore F_+ is positive throughout this whole interval.

### 5.3. beta<=p

The scalar F_- is increasing for p>=beta, so its minimum is at p=beta. Its value there is again

    F_-(beta)=r^2(h-1)/(1+b)>0.                    (22)

Thus B's source f fails in the other angle order as well.

Both actual sources in (9) have been excluded. The supposed missing origin contradicts disjointness, proving Theorem1. The diagonal B endpoint b=r, equal C/B angles, and all weak face or wall contacts were retained throughout. The axial B endpoint was already excluded by the direct origin lemma in Section2.

## 6. The actual positive-central profile under a missing wall origin

Retain the original no-omission OOOO family and suppose actual Q9 omits (2,1). Its preceding actual Q4 must own its forward G3: otherwise the missing-forward halfpoint and paired-corner transfer would give that Q9 origin. Q4 must also have strictly positive canonical angle by the unconditional ordinary-nonpositive halfpoint theorem. Normalize the coordinates as above.

The actual paired Q0 strictly owns (1,.914),(1,1). By contraposition of the all-angle paired-corner transfer, its failure to supply the omitted Q9 origin implies that Q0 strictly owns (1,1.5). Hence the different C=Q4 excludes the local H0=(-1,-.5).

We verify its lower face directly. H0 has both upper bands strict by G=(-1,-.4), so it is lower u or lower v. A lower-v exit would give V>=s-.5c. Strict M=(-.35,-.35) would then imply s/c<3/13. In that range the actual northwest marker N=(-.35,.35) has its other three bands strict by P=(-1,-.26),M,T: the only restrictive increment is .09c-.35s>0, valid because 3/13<9/35. Thus N would be upper v, with H<=.35(c+s). The two v-faces would give the impossible width

    a<=.85c-.65s<1.

Therefore the actual missing H0 forces

    U>=-c-.5s.                                    (23)

The independently proved C1092-MPPM-POSITIVE-FORWARD-UPPER-CAP.md gives A<=0, including the ordinary/inward overlap. The genuine preceding-origin exclusion from C1092-MPPM-FORWARD-OWNED-POSITIVE-D.md gives H<=s, hence V<=s-a. These are exactly the simultaneous faces (1). No backward auxiliary is silently assumed foreign.

## 7. Literal boundary application and scope

**Corollary 2.** In the original no-omission OOOO family, every actual boundary square with nonnegative canonical orientation strictly owns its local wall origin.

If the origin is missing, Section6 supplies the actual positive C profile regardless of the other central signs or forward memberships. If B=Q9 is nonnegative, Theorem1 then applies on the literal data

| Local datum | Original strict owner or source |
|---|---|
| C's G,T | G0 and forward G3, strict in Q4 |
| B's M_B,L_B,T_B | Q9 marker,F2,G2 |
| Real bottom wall y>=-2 | Original container wall y>=0 |
| Whole corner segment (2) | Between (1,.914),(1,1), both strict in actual Q0 |
| C's lower U floor | The actual Q0 halfpoint and Q7 marker argument (23) |
| C's cap A<=0 | The reviewed universal positive forward cap, with both backward memberships retained |
| C's transverse cap H<=s | The genuine D exclusion, not an assumed Q8 origin |

No condition on the center of B is used. Simultaneously rotate the entire actual owner table to obtain Q10,Q11,Q8. At an axial boundary angle the direct origin lemma applies immediately, so the corollary includes that endpoint.

Consequently any still-missing actual wall origin in OOOO must belong to a strictly negative boundary square. This chapter leaves that complementary boundary sign to a separate actual-support argument.
