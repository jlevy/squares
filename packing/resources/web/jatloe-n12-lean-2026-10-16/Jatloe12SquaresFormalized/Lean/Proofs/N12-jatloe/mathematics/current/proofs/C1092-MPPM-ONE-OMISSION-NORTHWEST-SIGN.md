# C1092 MPPM with one omission: the northwest angle is strictly positive

All decimals are exact rationals. This chapter retains the twelve actual original squares and the normalized one-omission entrance of `C1092-MPPM-ONE-OMISSION-UPPER-CORE.md`. Its simultaneous transpose and actual names W,N,L are used without changing any square separately. We work in its centered transposed coordinates, so O=(0,0) is the strict center point of W. The side satisfies 1<a<=1.001; all owned points are strict and all exterior exits and separating supports may be equality.

**Theorem.** In the original MPPM family with exactly one omitted indicated wall auxiliary, normalize that omission to original F2 absent from Q9. Then the transposed northwest square W=Q5 has a strictly positive canonical angle. In particular every nonpositive representative, including the axis and the diagonal, is impossible.

The proof uses the true condition center_y(L)<=0 in this centered chart. It does not require the unproved top origin in T.

## 1. The full actual northwest--northeast support

Suppose W has a nonpositive canonical frame

    u_W=(c,-s), v_W=(s,c), c>=s>=0, c^2+s^2=1.

Let A,H be its upper faces and A-a,H-a its lower faces. Theorem2 of the upper-core chapter gives

    c+s<1.13, s<.14, c>.99,                           (1)

and eliminates all W--N face-normal sources except

    alpha A+kH<=b+t-a,
    alpha=bc-ts>0, k=bs+tc>0.                         (2)

Here N's positive frame is (b,t),(-t,b), with b>=t>0, b^2+t^2=1, and Theorem1 of that chapter gives

    z_N=t/(1+b)>157/843.                              (3)

Strict O gives A,H>0. Put h=c+s and g=c-s. Since b>=t, one has k>=th. Thus (2)--(3) imply

    H<(b+t-1)/k<=(b+t-1)/(th)
      =(1-z_N)/h<686/843<.82.                       (4)

The actual southwest marker S=(-.35,-.35), strictly owned by its distinct original square Q4, is excluded from W. Both its upper bands follow from strict O. Its lower u band follows from the strict W rectangle vertex (-.5,.5), with increment .15c+.85s>0. It must therefore exit the lower v face:

    H>=a-.35h>1-.35h.                                (5)

The actual northeast marker M=(.35,.35) in N has both lower W bands from O. Its upper v band follows from (-.5,.5), with projection gap

    .15c-.85s>.15(.99)-.85(.14)=.0295>0.

It consequently exits upper u, giving

    0<A<=.35g<g.                                     (6)

## 2. The same pair forces A<1/10 over the whole angle interval

Rewrite (2) using b^2+t^2=1:

    b(1-cA-sH)+t(1-cH+sA)>=a>1.

Cauchy--Schwarz therefore requires

    Q(A,H)=A^2+H^2-2gA-2hH+1>0.                     (7)

Suppose A>=.1. On the actual intervals (4),(6), Q strictly decreases in A and in H, because A<g and H<.82<h. Equations (5)--(6) thus give

    Q(A,H)<=Q(.1,1-.35h)=P(h),
    P(h)=2.01-2.7h+.8225h^2-.2sqrt(2-h^2).           (8)

For every 1<=h<=1.13, the radical is greater than .85, since

    2-1.13^2=.7231>.7225=.85^2.

Consequently, over this entire closed interval,

    P'(h)=-2.7+1.645h+.2h/sqrt(2-h^2)
          <-2.7+1.645(1.13)+.2(1.13)/.85
          =-195591/340000<0.                         (9)

Its endpoint is

    P(1)=-27/400<0.

Equations (7)--(9) are contradictory. We have proved the actual face cap

    A<.1.                                            (10)

No angle sample is used: (9) controls the whole canonical interval allowed by the earlier actual-pair theorem.

## 3. The full actual left square and every possible separating source

Give the same actual L the positive frame supplied by Theorem4 of the upper-core chapter:

    u_L=(d,r), v_L=(-r,d), d>r>0, d^2+r^2=1,
    d+r>5/4.

Write J for its upper u face and V for its lower v face. Its actual bar and its true center condition give

    J>-d+.4r,
    rJ+dV<=-a(d-r)/2.                                (11)

Moreover

    2dr=(d+r)^2-1>9/16,
    r>9/32, r/d>9/32.                                (12)

These weaker rational consequences are sufficient. The two strict actual bar points (-1,.35),(-1,-.39) belong to L because its entire bar { -1 }x[-.39,.4] is strict.

Orient any separating normal from L toward W. The strict pair (-1,.35) in L and (-.35,.35) in W forces its x component to be positive. The four remaining possible face sources are u_L,-v_L,u_W,v_W. Source -v_L=(r,-d) fails on the strict displacement

    (-.35,.35)-(-1,-.39)=(.65,.74),

whose scalar product is .65r-.74d<0. Source v_W=(s,c) fails on the actual strict pair (-1,.4) in L and O in W, because its displacement (1,-.4) has scalar product

    s-.4c<.14-.4(.99)<0.

Such nonpositive products cannot occur along a separating direction between strict points in two disjoint open squares. The exhaustive remaining choices are therefore

    u_W or u_L.                                      (13)

Put

    alpha_L=cd-sr>0, k_L=cr+sd>0.

The full-square support calculations below allow tangency of the separating faces.

## 4. W's normal is impossible using the true left-center inequality

Because u_W=alpha_L u_L-k_L v_L,

    upper_L(u_W)=alpha_L J-k_L V.

The center inequality in (11) gives

    V<=-(r/d)J-a(d-r)/(2d).

Consequently

    upper_L(u_W)>= (c/d)J+k_L a(d-r)/(2d)
                 >-c+.4c(r/d).                      (14)

In the last strict inequality we used J>-d+.4r and the positive term k_L a(d-r)/(2d). If u_W separated L from W, its exact lower W support A-a would therefore imply

    A>a-c+.4c(r/d)
      >.4(.99)(9/32)=891/8000>.1,                    (15)

where a-c>0 because a>1 and c<=1. This contradicts (10).

## 5. L's normal is impossible using both northwest face caps

Here u_L=alpha_L u_W+k_L v_W, with both coefficients positive. The full lower W support is

    lower_W(u_L)=alpha_L(A-a)+k_L(H-a).

Equations (4),(10) and a>1 give

    lower_W(u_L)<-.9alpha_L-.18k_L.

The upper L support is J>-d+.4r. Thus

    upper_L(u_L)-lower_W(u_L)
      >d(.9c+.18s-1)+r(.4-.9s+.18c).                (16)

The first bracket is negative: by Cauchy--Schwarz,

    .9c+.18s<=sqrt(.9^2+.18^2)=sqrt(.8424)<1.

It is also greater than -.109, using c>.99 and s>=0. Multiplication by 0<d<=1 therefore leaves it greater than -.109. The second bracket satisfies

    .4-.9s+.18c>.4-.9(.14)+.18(.99)=.4522.

By (12), the right side of (16) is consequently greater than

    -.109+.4522(9/32)=2909/160000>0.                 (17)

Hence L's own normal cannot separate the two actual squares either.

Both sources in (13) are impossible. The actual L and W cannot have disjoint interiors if W has a nonpositive canonical angle. This contradiction proves the theorem. All strictness used at the end comes from genuine strict anchors or a>1; exterior contacts and equality of separating supports were allowed throughout.
