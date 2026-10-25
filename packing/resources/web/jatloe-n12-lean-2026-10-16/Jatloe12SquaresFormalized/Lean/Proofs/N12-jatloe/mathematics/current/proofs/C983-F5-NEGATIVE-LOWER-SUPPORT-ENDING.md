# C983 F5-only: the negative southeast branch with a full lower support is impossible

Every terminating decimal denotes an exact rational. Owned points are strict points of their named actual open squares. Foreign bars belong to one actual open square, throughout their full stated lengths. Exclusions and separating supports permit contact. The common physical side satisfies a>1; no upper bound on a is used here.

This chapter proves a local three-square ending for one of the two bottom-bar alternatives. It applies to every remaining strictly negative southeast square which owns F4. It does not assert the other bottom-bar alternative is impossible.

## 1. Actual entrance and the precise alternative being excluded

Use C983-F5-UPPER-RIGHT-REDUCTION.md. The still-open actual squares have

    W=Q7=8224, R=Q10=524800,
    N=Q6=131200, T=Q11=16392.

Translate the original coordinates by (−2,−2). Suppose the actual southeast square E=Q5 has strictly negative canonical angle and owns F4. Its strict anchors include

    M=(.35,−.35), I=(0,−.26), D=(.26,0).

These are its original marker,F4,G6. Its excluded O=(0,0) is strictly in the actual merged W. The foreign whole bottom bar

    [.26,.8]×{−1}

is strictly in actual Q9. The foreign R0=(1,0) is strict in actual R. The foreign Y=(.525,.125) is strict in actual N.

Use the canonical frame and full faces

    u_E=(c,−s), v_E=(s,c), c≥s>0, c²+s²=1,
    lower U,V; upper A=U+a,H=V+a.

At O both v bands follow from I,D and the upper u band follows from M. Therefore U≥0. At R0 its lower bands follow from D,I, while A≥a>1 gives its upper u band. Thus R0 is upper v. At Y both lower bands follow from D, and its upper u band follows from A>1. Consequently

    U≥0, A≥a>1, U<.26s, V<−.26c<0,
    H≤s, H≤.525s+.125c.                         (1)

The bottom-bar alternatives proved in Section 2 of C983-F5-TWO-RIGHT-AUXILIARIES-ENDING.md use only these anchors, O,R0 and this actual bottom bar. They remain literal here: its first endpoint forces V≥.26s−c; the second is either lower v or upper u. If it is not lower v, any interior intersection with y=−1 would fall strictly within the foreign bar. Since M is above that line, the complete closed lower support must then satisfy

    −sA+cV≥−1.                                  (2)

The other retained alternative is V≥.8s−c.

**Theorem 1.** Alternative (2) is impossible in the stated actual entrance.

The rest of this chapter proves the theorem. All the northeast and right-square information used below is universal in C983-F5-UPPER-RIGHT-REDUCTION.md; no bottom origin or merged vertical midpoint is assumed.

## 2. Consequences of the actual lower support

Equation (2) is equivalent to

    H≥a+(sA−1)/c
      ≥a(1+s/c)−1/c.                            (3)

Put

    q=angle(c,s),
    f(q)=1+(s−1)/c,
    e(q)=(1−c)(1−s)/c.

Then H>f(q)>0 and f(q)=s−e(q). The exact derivative is

    f'(q)=1/(1+s).                              (4)

Combining (3) with the last bound in (1) gives

    c+s−1−.525cs−.125c²<0.

The derivative of the left side with respect to q is

    (c−s)[1−.525(c+s)]+.25cs>0.

Here c+s<3/2, so the first bracket is positive. At s=7/20 and c=√351/20 the expression is

    (653√351−12155)/16000>0,

because 653²·351−12155²=1925534>0. Thus the whole allowed interval satisfies

    0<s<.35, c>.93.                             (5)

Two uniform consequences, including all endpoints needed below, are

    e(q)<.05,
    (962/3869)−s(1−s)/c>5785/1439268>0.          (6)

For the first, s²(1−s) increases on [0,.35], and

    e(q)=s²(1−s)/(c(1+c))
      <(.35)²(.65)/(.93·1.93)<.05;

the exact reserve in the last comparison is506/89745. For the second, s(1−s) increases on this interval and c>.93, so

    s(1−s)/c<(.35)(.65)/.93=91/372.

The full right support of E is strictly beyond x=1. Indeed, (3) and A≥a give

    x_max(E)=cA+sH
      ≥a(1/c+s)−s/c
      >(1+cs−s)/c
       =1+(1−c)(1−s)/c>1.                     (7)

This uses the actual lower support (2), not an extra container wall.

## 3. Northeast profile and all possible actual separating normals

The common northeast frame and profile from the preceding reduction are

    u_N=(d,−r), v_N=(r,d), d,r>0, d²+r²=1,
    lower P,Q; upper J=P+a,T_N=Q+a,

    P≥−r, Q≥.26d,
    J≤d−.56r, T_N≤d+r, Q<.62d.                  (8)

This is a frame of the same actual N for either original canonical sign. The strict point giving Q<.62d is N's proved (0,.62).

Let

    p0=2 atan(13/87), p1=2 atan(11/25),
    d0=3700/3869, r0=1131/3869,
    Hn=d0+r0=4831/3869.

The two complete widths in (8) prove

    p0<p=angle(d,r)<p1,
    d>2/3, r<3/4, d+r≥Hn, d+r<10/7.             (9)

In particular Hn−1=962/3869. These two-sign profile and interval deductions are proved in Sections 2–3 of C983-F4-FULL-8240-ENDING.md, using exactly the actual sources already supplied by the present upper-right reduction.

Choose the downward-right quadrant frame of actual R:

    u_R=(b,−t), v_R=(t,b),
    b,t≥0, b²+t²=1, theta=angle(b,t).

Its lower faces L,K satisfy, from its strict origin and real right container wall,

    L<b, K<t,
    b(L+a)+t(K+a)≤2.                            (10)

For disjoint open squares, an actual face normal separates the two full squares. Orient it from E toward R. The strict points D,R0 force its x component positive. E's u_E direction cannot separate because its upper support A>1 is greater than the strict R0 projection c. E's only other possible direction is v_E.

Of R's positive-x normals, u_R is also impossible. If theta≥q, its coordinates in E's frame are k=cb+st>0 and h_E=sb−ct≤0. The full E support is kA+h_E V. Here V<0 and

    k≥b/c≥b,

so the support is greater than b, whereas L<b. If theta≤q, that support is kA+h_E H. As a function of the normal angle on [0,q], its excess over b is a linear combination of b,t. At theta=0 this excess is x_max(E)−1>0 by (7); at theta=q it is A−c>0. Every intermediate normal is a positive linear combination of these two endpoint normals, so its support excess is positive too. This excludes u_R in both relative orders.

Thus the exhaustive E→R list is

    v_E or v_R.                                 (11)

For N→R the strict pairs

    (.5,1)→(1,0),
    (.525,.125)→(1,.56)

are available in these same actual squares. They give n_x>0 and n_y<.5n_x. Section 3 of C983-F4-FULL-8240-ENDING.md proves from precisely (8),(9) and these strict pairs that v_N and v_R cannot separate: the former fails the cone; the latter has full N support greater than t, against K<t. Explicitly the latter support bound uses

    A_N(p)=d+r−.74dr>1,
    B_N(p)=r−d−.26−.74r²<0

and gives upper_N(v_R)>t A_N−b B_N>t.

The exhaustive N→R list is therefore

    u_N or u_R.                                 (12)

If u_R supplies it, the second strict pair also gives

    95b>87t, b>2/3, t<3/4.                      (13)

All reverse normals have been excluded by the strict positive-x cones. Equations (11),(12) leave four complete-square separator combinations.

## 4. A universal lower face bound when R supplies the E separator

Use throughout

    j=ct−sb, k=cb+st>0.

Suppose E→R uses v_R. We prove the useful bound

    K>f(theta)=1+(t−1)/b.                        (14)

The b=0 endpoint cannot occur: then this separator is the positive x direction, and (7) contradicts K<t=1. The theta=0 endpoint is also already impossible because E's strict D has y=0 and K<0. We may assume b,t>0.

If theta≥q, so j≥0, the full support and (3) give

    K≥jA+kH
      ≥(t/c)A+ka−k/c
      >t/c−k(1−c)/c.                            (15)

The deficit of the final expression below t is

    E_q=(1−c)[b−t(1−s)/c].

For fixed theta, (1−c) increases with q, and the bracket increases with q because (1−s)/c decreases. If E_q≤0, it is already less than the positive value E_theta. If E_q>0, both increasing positive factors give E_q≤E_theta for q≤theta. The endpoint is

    E_theta=(1−b)(1−t)/b.

Thus (15) implies K>t−E_theta=f(theta).

If theta≤q, the full support is jU+kH. Using (3) before dropping U, its coefficient is

    j+ks/c=t/c≥0.

Therefore K>k f(q). On the entire interval theta≤q≤pi/4,

    d[k f(q)]/dq
      =k/(1+s)−sin(q−theta)f(q)
      ≥c/(1+s)−s f(q)
       =c−s≥0.

At q=theta, k f(q)=f(theta), proving (14) in this order too.

When this R-axis separator is used, its exact bound (15) and K<t also give

    theta<atan(45/31).                           (16)

For theta≤q this follows already from (5). For theta≥q, (15) requires E_q>0 and hence

    t/b<c/(1−s)=(1+s)/c<1.35/.93=45/31.

No angle restriction on R is assumed apart from this derived one.

## 5. Strong northeast support when R supplies that separator

Suppose N→R uses u_R. The complete two-order bounds in Section 5 of C983-F4-FULL-8240-ENDING.md use exactly (8)–(10), and give

    theta≤p0 ⇒ L>b A*+t B*,
    theta≥p0 ⇒ L>min{b C*+t D*,1−t},             (17)

where

    A*=15594461/14969161,
    B*=−14778022/14969161,
    C*=12725114/14969161,
    D*=−5391122/14969161.

In particular

    1.04<A*<1.05, −1<B*<−.98.

We sharpen (17) to the convenient common conclusion

    L>1−t.                                      (18)

On [0,p0], the function b A*+t(B*+1)−1 is concave, with endpoint values A*−1>0 and0. Both trigonometric coefficients are positive, so this is its ordinary second-derivative concavity. Thus its value is nonnegative throughout.

For theta≥p0, (13) gives theta<atan(95/87)<atan(9/8). The function b C*+t(D*+1)−1 is also concave. At p0 it is0. At atan(9/8) its value is positive, since 8C*+9(D*+1)>0 and

    [8C*+9(D*+1)]²−145
      =2854238647278624/224075781043921>0.

This proves (18) for both terms of the minimum in (17).

### 5.1. R supplies both separators

Combine (14),(18) with the real wall (10). Its left side is strictly greater than

    b(2−t)+t[1+f(theta)]
      =2+(1−b)²(1−t)/b≥2,                     (19)

which is impossible. The theta=0 endpoint was already excluded in Section 4; (13) ensures b>0.

### 5.2. E supplies its own separator

Now E→R uses v_E. Its exact support ordering is

    H≤−jL+kK−a max(j,0).                         (20)

Combine this with (3) and the real wall, eliminating K. The coefficient of L is c, and the positive coefficient of a can be reduced using a>1. The necessary inequality is

    cL+t f(q)+k(b+t−2)+t max(j,0)<0.              (21)

We show its left side is positive.

First suppose theta≥q, so j≥0. By (18) it exceeds or equals

    G(q,theta)
      =(2−t)(c−k)+t f(q).                        (22)

For fixed theta this decreases with q on [0,theta]. Indeed

    partial_q G
      =−(2−t)[s(1−b)+ct]+t/(1+s)<0.

To justify the last sign even over this enlarged q interval, (13) gives cos q≥b>2/3 and tan(q/2)≤t/(1+b)<.45. Hence

    c(1+s)−1=s[c−tan(q/2)]≥0.

Consequently the negative ct term alone dominates t/(1+s), since 2−t>1. At the final endpoint q=theta,

    G(theta,theta)=(1−b)²(1−t)/b>0.

This excludes (21) in the whole theta≥q case.

Next suppose p0≤theta≤q. Here j≤0, and (18) gives the lower bound

    G(q,theta)
      =t[(b+t−1)(s−c tan(theta/2))−e(q)].         (23)

Since theta≤q, we have s−c tan(theta/2)≥tan(q/2). Also theta≤q and (5) place theta below pi/4, so b+t≥Hn. Thus (23) is at least

    t tan(q/2)[Hn−1−s(1−s)/c]>0

by (6).

It remains to include every theta in [0,min(q,p0)]. Use the stronger first bound in (17). The resulting lower bound in (21) is

    G_small(theta)
      =c[b²+bt+(A*−2)b+B*t]
        +s[bt+t²−2t]+f(q)t.                    (24)

For fixed actual q its second derivative is exactly

    G_small''
      =−2(c−s)(b²−t²)−4(c+s)bt
        +c(2−A*)b−cB*t+[2s−f(q)]t.

Throughout [0,p0], b>.95 and t<.3. Using c−s≥0, c+s≥1, A*>1.04, −B*<1, f(q)>0, and (5), this is strictly less than

    2s−c A*+4t²−2.1t
      ≤2s−c A*−.9t
      <.7−(.93)(1.04)=−167/625<0.               (25)

Thus (24) is concave on the complete interval. At theta=0 it is c(A*−1)>0. At the other endpoint, theta=q or theta=p0, the respective preceding proof (22) or (23) applies, because the bound b A*+t B* is at least1−t. Both endpoints are positive, so concavity proves positivity throughout. This contradicts (21) and completes every case in which R supplies the N separator.

## 6. N supplies its axis and R supplies the E separator

Retain (14),(16), and suppose the N separator is u_N. Put

    delta=db+rt>0, h=rb−dt.

The exact N inequality and J≥a−r give

    delta L≥a[1+max(h,0)]−r+hK.

Multiply by b and combine with delta times the real wall (10). The exact identity b h+t delta=r eliminates the mixed K coefficient. Using a>1 and K>f(theta), the necessary inequality is

    F=delta(b+t−2)+b(1−r)+r f(theta)
         +b max(h,0)<0.                         (26)

First let 0<theta≤pi/4. If p≥theta, an exact expansion gives

    F=b−b(2−b)d−r epsilon,
    epsilon=(1−b)²(1−t)/b.

Here d≤b, so

    F≥(1−b)²(1−t)(1+t−r)/b>0.                 (27)

If p≤theta, the last term of (26) vanishes. For fixed theta its p derivative is

    −(2−b−t)sin(theta−p)+d[f(theta)−b]<0.

The second bracket is negative on this whole interval: after multiplication by b its numerator is b+t+t²−2≤√2−3/2<0. Therefore F is minimized at p=theta, where F=epsilon>0. At theta=0 equation (26) instead directly gives F=1−d>0, since p>p0.

For the remaining theta≥pi/4, (16) implies

    2/5<z=tan(theta/2)<11/20.

The lower endpoint follows from √2−1>2/5. For the upper endpoint,

    tan[2 atan(11/20)]=440/279>45/31.

Drop the nonnegative last term of (26), and define

    A_theta=b(2−b−t),
    B_theta=t(2−b−t)+b−1+(1−t)/b.

Then

    F≥b−A_theta d−B_theta r
      ≥b−sqrt(A_theta²+B_theta²).

The exact half-angle identity is

    b²−A_theta²−B_theta²
      =−(z−1)² P(z)/[(z+1)²(z²+1)³],            (28)

where

    P(z)=17z⁶+8z⁵−5z⁴−8z³−5z²+1.

It is strictly negative throughout [2/5,11/20]. Indeed

    P(2/5)=−4507/15625<0,

and, since z>0,

    P'(z)/z
      =102z⁴+40z³−20z²−24z−10
      ≤102(11/20)⁴+40(11/20)³−24(2/5)−10
       =−288909/80000<0.

Thus (28) is strictly positive, proving F>0 in this final angular range as well. This contradicts (26) and excludes the third separator combination.

## 7. Both neighbors supply their own axes

Only

    H≤−jL+kK−a max(j,0),
    J≤delta L−hK−a max(h,0)                    (29)

remains. Let D0=cd+sr=cos(p−q)>0. The exact positive-multiplier identities are

    c delta−r j=D0 b,
    −c h+r k=D0 t.

Multiply the N inequality by c and the E inequality by r. Use J≥a−r, (3), the real right wall, and a>1. The necessary inequality becomes

    F(theta)<0,                                (30)

where

    F(theta)=D0(b+t−2)+c(1−r)+r f(q)
                +c max(h,0)+r max(j,0).         (31)

For fixed actual p,q this is a positive linear combination of cos theta and sin theta, plus a constant, on each interval obtained by splitting at p,q. Its two coefficients are:

| Interval | Coefficient of b | Coefficient of t |
|---|---:|---:|
| 0≤theta≤min(p,q) | D0+cr | sr |
| q≤theta≤p, if q≤p | c(d+r) | r(c+s) |
| p≤theta≤q, if p≤q | D0 | D0 |
| max(p,q)≤theta≤pi/2 | cd | D0+cr |

All are positive. Therefore F is strictly concave on each full interval, and it suffices to check theta=0,q,p,pi/2. Both possible relative angle orders are retained.

### 7.1. Outer endpoints

The two outer values coincide:

    F(0)=F(pi/2)
      =c(1−d)−r e(q)
      =r[c tan(p/2)−e(q)]>0.                    (32)

For example c>.93, tan(p/2)>13/87 and e(q)<.05 give a strictly positive bracket.

### 7.2. The endpoint theta=q

If p≥q, exact expansion gives

    F(q)=c−c(2−c)d−r epsilon_q,
    epsilon_q=(1−c)²(1−s)/c.

Since d≤c,

    F(q)≥(1−c)²(1−s)(1+s−r)/c>0.              (33)

If p≤q, the h term vanishes. For fixed q its derivative with respect to p is

    −(2−c−s)sin(q−p)+d[f(q)−c]<0.

Here f(q)<c follows from (5), or from the same elementary bound used in Section 6. Its minimum on p≤q is consequently at p=q, where the value is epsilon_q>0. This proves the q endpoint in both orders.

### 7.3. The endpoint theta=p

If q≤p, its exact formula is

    F(p)=c(1−d)(2−r)+s(r²−2r)+r f(q).            (34)

It decreases with q on the whole enlarged interval [0,p]. Its derivative is

    −s(1−d)(2−r)+cr(r−2)+r/(1+s)<0.

For this enlargement p≤p1 gives c≥d>2/3 and tan(q/2)≤11/25<2/3. Hence c(1+s)≥1, so 1/(1+s)≤c, and the last two terms are at most cr(r−1)<0. At q=p the value of (34) is

    (1−d)²(1−r)/d>0.

Therefore (34) is positive for every q≤p, whether or not p itself is in the original canonical southeast range.

If q≥p, the j term vanishes, and the exact expression is

    F(p)=r[(d+r−1)(s−c tan(p/2))−e(q)].

Since s−c tan(p/2)≥tan(q/2), (9) and (6) give

    F(p)≥r tan(q/2)[Hn−1−s(1−s)/c]>0.           (35)

Thus all four endpoints are positive. The interval concavity statements prove F(theta)>0 for every theta∈[0,pi/2], contradicting (30). This excludes the last separator combination.

## 8. Conclusion and retained scope

Every actual face-normal combination for E–R and N–R has failed. Thus the full actual southeast square cannot satisfy the lower support (2), proving Theorem 1.

The theorem applies to all remaining negative E components which own F4: the F4-only components65552,327696 and, conditionally on their negative sign, the F4+F8 components65808,327952. It does not require F8 to belong to any particular square. All northeast profile points and the right origin/bar come from their actual owners already proved in C983-F5-UPPER-RIGHT-REDUCTION.md.

Consequently, any such still-possible negative southeast square must use the other bottom-bar alternative

    V_E≥.8s_E−c_E.

That is a genuine remaining alternative; this chapter does not replace it with an assumed lower support. The proof includes both original signs of the actual N, all relative angle orders, all full-square separator choices, and weak support contacts. Every scalar interval used above was covered by a monotonicity, concavity, factorization or exact endpoint argument.
