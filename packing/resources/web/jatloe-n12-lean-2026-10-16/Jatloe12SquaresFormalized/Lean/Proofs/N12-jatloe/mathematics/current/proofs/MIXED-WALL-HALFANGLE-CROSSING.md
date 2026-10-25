# A wall spanning both directions forces the missing half-angle crossing

All terminating decimals are exact rationals. All owned points are strict. Exclusions, container contacts, and separating supports may be equality. The squares are actual squares, with their common side satisfying 1<a≤1.001.

## 1. The actual wide wall has a forced sign and a large angle

**Theorem 1.** Suppose an open square W strictly owns

    S=(1.086,0), T=(1,−.39), B=(1,.4),

excludes

    E=(1,−.4), M=(.35,.35),

has its closure in x≤2, and has center ordinate Y_W≤0. Then W has a strictly negative canonical frame

    w=(d,−t), w_perp=(t,d),
    d>t>0, d²+t²=1,

and

    d+t>5/4.                                           (1)

Write L,H for W's lower faces in this negative frame. They also satisfy

    L≥.35(d−t), H≥t−.4d, L<d−.4t.                    (2)

**Proof.** First suppose W has a nonnegative canonical frame (d,t),(−t,d), with d≥t≥0. The point E has both upper bands strictly from T. Therefore E is lower longitudinal or lower transverse. The point M has its upper longitudinal band strictly from B, and its lower transverse band strictly from S, because the projection increments are

    u(B)−u(M)=.65d+.05t>0,
    v(M)−v(S)=.35d+.736t>0.

Thus M is lower longitudinal or upper transverse.

If E is lower transverse, an upper-transverse M would give the opposite-face width

    a≤v(M)−v(E)=.75d+.65t≤sqrt(.985)<1.

Consequently M is lower longitudinal in this case. Writing L,H for the lower faces of this positive frame gives

    L≥.35(d+t), H≥−t−.4d.

Its center ordinate then satisfies

    Y_W=t(L+a/2)+d(H+a/2)
       ≥a(d+t)/2−.4+.75t²−.65dt
       >.1+.25t²−.15t
       =31/400+(t−3/10)²/4>0.                       (3)

For the strict bound, use a>1, d≥1−t² and d≤1. This contradicts Y_W≤0. E must therefore be lower longitudinal:

    L≥d−.4t.                                         (4)

Strict ownership of B gives H>.4d−t−a. Combining this with (4), including t=0, yields

    Y_W>(d−t)[.4(d+t)−a/2].                          (5)

If d=t, this is already a contradiction. If d>t, the center condition forces a>.8(d+t). If d≤.8, then d+t≥1.4 on the canonical unit arc, so a>1.12, contrary to a≤1.001. Thus d>.8.

The actual right wall bounds the center abscissa by X_W≤2−a(d+t)/2. Since Y_W≤0,

    L=dX_W+tY_W−a/2
      ≤2d−a(1+d²+dt)/2.

Together with (4), this would imply

    (1+d²+dt)/2−d−.4t<0.                            (6)

But the exact left side is

    t(d/2−.4)+(1−d)²/2≥0

when d>.8, including t=0. This is impossible. Thus every nonnegative canonical frame has been excluded.

We may give W the negative frame in the statement, initially allowing d≥t>0. At M, its upper longitudinal band and both transverse bands follow strictly from B,T:

    w(B)−w(M)=.65d−.05t>0,
    w_perp(M)−w_perp(T)=.74d−.65t>0,
    w_perp(B)−w_perp(M)=.05d+.65t>0.

Hence M is lower longitudinal, giving the first bound in (2). At E, its lower longitudinal band follows from B and its upper transverse band from T. If E exited upper longitudinal, the preceding lower face would give

    a≤w(E)−w(M)=.65d+.75t≤sqrt(.985)<1.

Therefore E is lower transverse, giving the second bound in (2). The last bound in (2) is strict ownership of B.

The center ordinate in this negative frame now satisfies

    Y_W=−t(L+a/2)+d(H+a/2)
       >(d−t)[a/2−.4(d+t)].                          (7)

Strictness follows from t>0 and the strict upper bound on L. Equality d=t would contradict Y_W≤0. Thus d>t, and (7) forces d+t>a/.8>5/4. This proves all the claims. ∎

## 2. The crossing theorem for the actual inward square

**Theorem 2.** Let C,W be disjoint open squares of common side 1<a≤1.001. Suppose C has negative canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1,

with lower faces U,V, and strictly owns

    M=(.35,.35), P=(0,.26), Q=(.26,0).

Assume V≥0. Suppose W owns S,T,B, excludes E, and has the actual wall and center condition of Theorem 1. Then, with z=s/(1+c),

    U<−z, and (z,1) belongs strictly to C.             (8)

There is no wall or center assumption on C. M is genuinely excluded from W because it is strict in the different actual C.

**Proof.** Strict Q gives V<.26s, so V≥0 implies s>0. Thus 0<z≤sqrt(2)−1. Theorem 1 applies to W and supplies its negative frame, (1), and (2).

Suppose instead U≥−z. Put

    r0=(1−z)²/2, rho=max(.4,r0), R=(1,rho).

The point R is strict in C. Its lower u-band follows from P and its lower v-band from Q. For its upper bands use

    c−sr0=1−z, s+cr0=1−r0.

When rho=r0, these projections are below U+a and V+a because a>1, U≥−z and V≥0. When rho=.4, the u-projection is at most 1−z and the v-projection is at most .7(c+s)≤.7sqrt(2)<1. The upper bands are again strict.

If rho=.4, this is exactly the point B already strict in W, contradicting disjointness. Hence r0>.4 and

    z<1−sqrt(4/5)<53/500,
    c>97/100, s<21/100.                              (9)

The last two bounds follow directly from c=(1−z²)/(1+z²), s=2z/(1+z²); the latter function increases on this interval.

For W, (1) gives 2dt=(d+t)²−1>9/16. Since d≤1,

    t>9/32>7/25.                                     (10)

Orient any separating normal from C to W. The strict pair Q,S has positive horizontal displacement and equal ordinates, so n_x>0. The strict pair R,B has equal abscissae and negative vertical displacement, so n_y<0. Only the actual normals u=(c,−s) and w=(d,−t) can lie in this open quadrant.

Put

    alpha=cd+st>0, k=ct−sd.

Equations (9),(10) give

    k/t=c−sd/t>97/100−(21/100)/(7/25)=11/50>0.         (11)

We exclude both actual normal sources by their full-square supports.

### The inward square's normal

The actual wall and the strict B anchor give

    dL+tH≤2−a(d+t), L<d−.4t.

Since alpha−kd/t=s/t>0, they imply

    lower_W(u)=alpha L+kH
      <(s/t)(d−.4t)+(k/t)[2−a(d+t)].                 (12)

The actual upper C support is U+a≥a−z. Subtracting (12), and using a>1 with its positive coefficient, shows that the support difference is strictly greater than

    D1=1−z−c+.4s+(k/t)(d+t−1).                       (13)

Here 1−c≥0 and z=s/(1+c)<.51s by (9). Therefore

    1−z−c+.4s>−.11s>−231/10000.

Equations (1),(11) now yield

    D1>−231/10000+(11/50)(1/4)
       =319/10000>0.                                (14)

Thus u cannot separate the actual squares, even with tangent supports.

### The wall square's normal

The frame coefficient of w along C's transverse normal is −k<0. Since V<.26s and U+a≥a−z,

    upper_C(w)=alpha(U+a)−kV
       >alpha(1−z)−.26sk.

Also lower_W(w)=L<d−.4t. Their difference is therefore strictly greater than

    D2=d[(1−z)c+.26s²−1]
       +t[(1−z)s−.26sc+.4].                         (15)

The exact first bracket is −z(c+s)+.26s². Moreover

    z(c+s)=s(c+s)/(1+c)≤s(1+s)/2<.605s,
    (1−z)s−.26sc>.634s,

using (9) and c≤1. Thus

    D2>−.605s+.4t+.634ts
       >.112−.42748s
       >.112−.42748(.21)
       =55573/2500000>0.                            (16)

In the second inequality use t>7/25; in the third use s<.21 and the negative coefficient. The wall's normal cannot separate either. These are all possible separating-axis sources, a contradiction.

Therefore U<−z. Finally the target Z=(z,1) has projections u(Z)=−z and v(Z)=1. Its lower u-band is now strict; its upper u-band follows from strict P because z≥s/2>.26s. Its lower v-band follows from V<.26s<1, and its upper v-band from V+a>1. Thus Z is strict in the same actual C, proving (8). ∎

The two normal estimates are uniform continuous inequalities. No discrete angle value, inferred foreign segment, or enlarged surrogate wall owner occurs in the proof.
