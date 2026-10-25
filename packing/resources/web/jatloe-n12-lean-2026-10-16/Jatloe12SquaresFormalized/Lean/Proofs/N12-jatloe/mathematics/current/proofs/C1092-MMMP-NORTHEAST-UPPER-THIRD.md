# C1092 MMMP: a strict upper bound of one third for the northeast half-angle

All terminating decimals are exact rational numbers. The squares are the original actual open squares, with common side a>1, disjoint interiors and the named strict points. Exclusions and separating supports may be tangent. Every angle interval in this proof is continuous.

**Main theorem.** In the original MMMP family, suppose the actual right Q10 owns F8 and the actual southeast Q5 excludes G8. Then the actual northeast Q6 has positive canonical angle theta satisfying

    tan(theta/2)<1/3.

In particular this holds in the double-right branch Q10=787200. The theorem is an upper bound for the remaining configuration; a contradictory lower bound is a separate obligation.

## 1. The literal positive inward entrance

Translate the original configuration by (-2,-2), and write

    W=Q7, N=Q6, E=Q5.

The proved northwest half-unit-square theorem supplies the whole strict rectangle

    [-.5,0] x [0,.5] in W.

In particular O=(0,0), L=(-.26,0), P=(0,.26) and (-.5,0) are strict in W. Its marker is (-.35,.35). The universal actual left owner Q8 strictly owns G1, so

    B=(-1,.4) is excluded from W.                    (1)

The actual southeast E strictly owns I=(0,-.26), D=(.26,0), and has positive frame

    u_E=(c,s), v_E=(-s,c), c>=s>0,
    c^2+s^2=1, s<.21, c>.97.                       (2)

These are precisely the conclusions of `C1092-MMMP-RIGHT-NEAR-BOTTOM-ORIGIN.md` under the two hypotheses of the present theorem. No owner of the omitted G8 is stipulated.

The northwest W is also strictly positive. To see the scope of this assertion without assuming the double-right label, use the complete proof in Sections1--3 of `C1092-MMMP-DOUBLE-RIGHT-NORTHWEST-SIGN.md`. Its local inputs are exactly the strict W rectangle points, the actual northeast face table, and E's inward pair and bounds (2). None of its separating-support inequalities uses another right-square point. For a supposed nonpositive W it gives simultaneously H<25/33 and, from E's normal, H>1459/1550; the other possible normal has strictly positive upper E support but negative lower W support. All those actual-square inputs are present here by the cited right-near theorem. Thus its same exhaustive two-normal contradiction excludes nonpositive W in this broader branch.

Write its positive frame and upper faces as

    u_W=(d,r), v_W=(-r,d), d>=r>0, d^2+r^2=1,
    A=upper_W(u_W), H=upper_W(v_W).

The full-interval positive-angle bound in Section2 of `C1092-MMMP-NORTHWEST-LEFT-TIP.md` is universal in MMMP and gives

    r/d<7/8, d>8/sqrt(113)>3/4,
    r<7/sqrt(113)<2/3.                              (3)

Strict O and (-.5,0) give

    0<A<a, 0<H<a, A-a<-d/2.                        (4)

Finally N has its strictly positive original frame

    u_N=(b,t), v_N=(-t,b), b>=t>0, b^2+t^2=1.

Let U_N,V_N be its lower faces and A_N=U_N+a,H_N=V_N+a its upper faces. Transporting the four faces of `C1092-MMMP-NORTHEAST-TOP-CAP.md` back from its quarter-turn gives

    U_N>=.4t, V_N>=.4b-t,
    A_N<=b+t, H_N<=b.                              (5)

Its marker (.35,.35) is strict. These are bounds for this one actual N, not independently placed copies of it.

## 2. The actual southeast square forces H>.92

Write p,q for the positive canonical angles of W,E, respectively, and put

    k=cos(p-q)=dc+rs>0,
    j=sin(p-q)=rc-ds.

Let U_E be E's lower u face and h_E its upper v face. The actual strict inward pair gives

    U_E<-.26s, h_E>-.26s.                           (6)

Orient a separating normal from E toward W. The strict pairs D to L and I to P force n_x<0 and n_y>0. Among all face normals of the two actual squares, exactly v_E and v_W can lie in this strict quadrant. Thus these are the complete possible separating sources.

First suppose p<q, so j<0 and r<s<.21. If v_W separates, the strict E point D has projection -.26r. Consequently

    H-a>=upper_E(v_W)>-.26r,
    H>1-.0546>.92.                                 (7)

If v_E separates, its lower W support is jA+k(H-a). Equations (4),(6), j<0 and k>=c>.97 give

    H>a+(-.26s-jA)/k
      >1-.0546/.97>.92.                            (8)

Now suppose p>=q, so j>=0 and k>=d>3/4. If v_W separates, its upper E support is -j U_E+k h_E. By (6),

    H>a+.26s(j-k)>1-.0546>.92,                     (9)

where k-j<=1. If v_E separates, its lower W support is j(A-a)+k(H-a). The strict last inequality in (4) gives

    H>a+(.5dj-.26s)/k
      >1-.0546/(3/4)=.9272>.92.                   (10)

All actual sources and both angle orders have been covered. Therefore

    H>.92.                                        (11)

## 3. The left auxiliary can leave W only through its lower u face

For B=(-1,.4), the upper u and lower v bands follow from strict O, since

    u_W(B)=-d+.4r<0<A,
    v_W(B)=r+.4d>0>H-a.

Thus its exclusion (1) permits only a lower-u exit or an upper-v exit. We exclude the latter, which would say H<=r+.4d.

If r<=.6, the function r+.4sqrt(1-r^2) is increasing on this interval and has value .92 at r=.6. This contradicts (11).

Suppose r>.6. Then p>q, and (2),(3) give

    j=rc-ds>(.6)(.97)-.21=.372.                    (12)

For the v_W source, (9) strengthens to

    H>1-(.0546)(1-.372)=.9657112>.96.

For the v_E source, (10) strengthens to

    H>a+[(.5)(.75)(.372)-.0546]/k
      =a+.0849/k>1.

But (3) and the monotonicity of r+.4d give in both cases

    r+.4d<10.2/sqrt(113)<.96.                       (13)

The last comparison is exact: 10.2^2=104.04<(.96)^2(113)=104.1408. Both sources contradict the proposed upper-v exit. Therefore B is lower u and

    A>=a-d+.4r.                                   (14)

Equations (11),(14) concern the same actual W. Their derivation retained every separating-normal source and every weak exterior contact.

## 4. Suppose the northeast half-angle reaches 1/3

Put theta0=2 arctan(1/3), so cos(theta0)=4/5 and sin(theta0)=3/5. Suppose theta>=theta0. Then

    b<=4/5, t>=3/5, theta<=pi/4.                   (15)

Orient a separating normal from W to N. Their strict markers (-.35,.35),(.35,.35) force n_x>0. The other positive-x face normals, -v_W and -v_N, cannot separate: their scalar product with the displacement from strict O in W to the N marker is respectively .35(r-d)<=0 or .35(t-b)<=0. Strict points on opposite sides of a separating support require a strictly positive displacement. Thus only

    u_W or u_N                                   (16)

can separate these two actual squares.

### 4.1. W's angle is at least theta

Suppose p>=theta. By (14),(15),

    A>1-d+.4r>=1-.8+.4(.6)=11/25.                 (17)

Set alpha=cos(p-theta)>0, gamma=sin(p-theta)>=0. If u_W separates, (5) yields

    A<=lower_N(u_W)
      =alpha U_N+gamma V_N
      <=alpha(b+t-a)+gamma(b-a)
      <sqrt(2)-1<21/50.

This contradicts (17). If u_N separates, its upper W support is alpha A-gamma(H-a). By (4),(17) it exceeds alpha(11/25). Also

    alpha>=cos(pi/4-theta0)=7/(5sqrt(2))>49/50.

Consequently this upper support exceeds 539/1250>21/50, whereas the lower N support is U_N<=b+t-a<sqrt(2)-1<21/50. This source also fails.

### 4.2. W's angle is below theta: W's normal

Now let p<theta and write

    alpha=bd+tr=cos(theta-p)>0,
    beta=td-br=sin(theta-p)>0.

If u_W separates, its lower N support uses the full N width:

    A<=alpha U_N-beta H_N
      <=alpha(b+t-a)-beta(a+.4b-t).                (18)

The last inequality uses A_N<=b+t and V_N>=.4b-t from (5); thus its negative coefficient uses a genuine lower bound on H_N. Combining (14),(18) and a>1 would require F2<0, where

    F2=1-d+.4r-alpha(b+t-1)+beta(1+.4b-t)
      =1-Kd-Lr,
    K=2-b-t+.6bt, L=b-t+.6t^2.                     (19)

Both K,L are positive on theta0<=theta<=pi/4 and are decreasing there. Indeed,

    K'=(b-t)[-1+.6(b+t)]<=0,
    L'=-t-b+1.2bt<0.

Their values at theta0 are111/125 and52/125. Hence Cauchy--Schwarz gives the exact uniform bound

    Kd+Lr<=sqrt(K^2+L^2)
           <=sqrt(111^2+52^2)/125
            =sqrt(601)/25<1.

Thus F2>0, contradicting (18).

### 4.3. W's angle is below theta: the northeast normal

For the final possible source u_N, the separating inequality and (5) are

    alpha A+beta H<=U_N<=b+t-a.

Equations (11),(14) and a>1 would therefore require F1<0, where

    F1(theta,p)=1-b-t+alpha(1-d+.4r)+(.92)beta.     (20)

We prove F1>0 over its entire two-angle domain. For fixed p, differentiation gives

    partial_theta F1=t-b-beta(1-d+.4r)+(.92)alpha.

Here t-b>=-1/5 by (15), 0<1-d+.4r<13/25 by (3), beta<71/100, and alpha>7/10. The latter two bounds follow from 0<=theta-p<=pi/4. Thus

    partial_theta F1>
      -1/5-(71/100)(13/25)+(23/25)(7/10)
       =187/2500>0.                               (21)

It suffices to check theta=max(theta0,p).

If p>=theta0, then

    F1(p,p)=2-2d-.6r.

This has value1/25 at p=theta0 and is increasing afterwards, since its derivative2r-.6d is at least18/25. It is positive throughout this part of the interval.

If 0<=p<=theta0, put w=tan(p/2) and x=3w, so0<=x<=1. Direct substitution of d=(1-w^2)/(1+w^2), r=2w/(1+w^2) gives

    (1+w^2)^2 F1(theta0,p)
      =(19-104w+220w^2+36w^3-319w^4)/125.           (22)

The polynomial on the right has the exact Bernstein expansion

    sum_{i=0}^4 B_i binom(4,i) x^i(1-x)^(4-i),

with coefficients

    (B_0,B_1,B_2,B_3,B_4)
      =(19/125,31/375,31/675,2/45,4/81).

Every coefficient is strictly positive. For every0<=x<=1 the five displayed weights are nonnegative and sum to1. Thus (22) is strictly positive on the complete interval, including both endpoints. This is an exact polynomial identity and positivity argument, not finite angle sampling. Together with (21), it proves F1>0 everywhere required, contradicting the last separating source.

## 5. Conclusion and retained scope

Both relative angle orders and both possible actual W--N face-normal sources are impossible under theta>=theta0. Therefore theta<theta0 and tan(theta/2)<1/3, as claimed.

All actual point sources used in the proof were identified in Section1. In particular B is the genuine Q8-owned G1, the inward pair is in the actual Q5, and every northeast face belongs to the same Q6. No ownership is assigned to G8 outside Q5. The proof permits tangent closure supports throughout and excludes equality at theta0 by strict positive margins. A lower bound from the actual right-hand configuration is still needed for a whole-branch contradiction.
