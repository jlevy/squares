# C1092 MPPM: only first normals can separate a positive owner from a positive retaining successor

All decimals are exact rational numbers. Owned points are strict interior points. Supports may agree at tangency. The proof uses the simultaneous faces of the same actual squares, with common side a>1.

## 1. Local theorem

Let C and E have nonnegative canonical physical frames

    u=(c,s), v=(-s,c), e=(d,t), f=(-t,d),
    c=cos p, s=sin p, d=cos q, t=sin q,
    0<=p,q<=pi/4.

Let A,K be the upper u,v faces of C. Write E's lower e face as -K_E and its upper f face as A_E. Suppose

    a-c-s<=A<=0, K<=s,
    A_E>-.26d, 0<K_E<=t.                         (1)

**Theorem 1.** Neither -v nor -f is a separating normal directed from C toward E.

The condition 0<K_E<=t excludes q=0 automatically. Keeping that coordinate endpoint in the formulas below does not remove any possible configuration.

Put

    kappa=cos(q-p)>0, sigma=sin(q-p).

The exact signed support inequalities required by the two proposed sources are

    -v: K+sigma K_E-kappa A_E
                    >=a[1+max(sigma,0)],       (2)
    -f: kappa K-sigma A-A_E
                    >=a[kappa+max(-sigma,0)].  (3)

For completeness, upper_C(-v)=a-K. When sigma>=0, the lower E support is sigma K_E-a sigma-kappa A_E; when sigma<=0 it is sigma K_E-kappa A_E. These give (2). Similarly the C coefficients of -f are sigma,-kappa, so its upper support is sigma A-kappa K+a[kappa+max(-sigma,0)]. Its comparison with lower_E(-f)=-A_E gives (3). Thus each sign selects the actual face with the correct coefficient.

## 2. Excluding the current transverse normal

If sigma>=0, the left side of (2) is strictly less than

    s+sigma t+.26kappa d.

Subtracting 1+sigma gives at most

    s+.26d-1+sigma(t-1)<.71+.26-1<0.             (4)

Here t<=1 and kappa<=1. The right side of (2) is strictly greater than 1+sigma, so (2) is impossible.

If sigma<=0, strict K_E>0 instead gives a left side strictly less than s+.26kappa d<.97<1. The required right side is a>1. This excludes -v in the other order, including sigma=0.

## 3. Excluding the successor transverse normal

### 3.1. q>=p

Here sigma>=0. Use K<=s, A>=a-c-s and A_E>-.26d in (3). Separation would require

    kappa s+sigma(c+s)+.26d>=a(kappa+sigma).

Its right side exceeds kappa+sigma. But the exact remaining difference is

    kappa(s-1)+sigma(c+s-1)+.26d
       =d[.26-c+s-s^2]+t(1-c)(1-s)<0.           (5)

Indeed the first bracket increases with p, since its derivative is c+s-2cs>0, and its endpoint at pi/4 is -.24. The nonnegative second factor (1-c)(1-s) increases with p: its derivative is (c-s)(c+s-1)>=0. Its maximum is 1.5-sqrt(2)<.09. Since t<=d, the last side of (5) is strictly less than -.15d. This contradicts the necessary separation.

### 3.2. q<=p

Now sigma<=0. Use A<=0, K<=s and A_E>-.26d in (3). Separation would require

    kappa s+.26d>=a(kappa-sigma).

The difference from kappa-sigma is exactly

    kappa(s-1)+sigma+.26d
       =d[.26-c+cs-s]+t[c+s^2-s].               (6)

The second bracket is positive, because c+s^2-s>=c-1/4>0. Moreover q<=p gives t/d<=s/c. Thus the last side of (6) is at most

    d[.26-c+cs-s+(s/c)(c+s^2-s)]
       =d[.26-(1-s)/c]<0.                       (7)

The last sign follows from (1-s)/c=c/(1+s)>=sqrt(2)-1>.4. Hence (7) is strictly less than -.14d. Again a>1 only strengthens the contradiction. This finishes Theorem 1, including p=q and every weak face equality.

## 4. Complete actual-source consequence

In the retained no-omission OOOO entrance, suppose C=Q4 is positive and its successor E=Q5 is positive and retains F4. Translate by (-2,-2). The universal positive faces in C1092-MPPM-UNIVERSAL-POSITIVE-CROSSPOINTS.md give

    a-c-s<=A<=0, K<=s

for C, independently of C's designated forward membership. For E, the positive retaining theorem gives its native transverse cap K_E<=t. Its actual strict forward point has native coordinates (-.26,0), so its two upper bands give

    A_E>-.26d, K_E>.26t>=0.

The native first and second normals of E become physical f,-e after the actual quarter turn; hence K_E is indeed minus its physical lower e face, as in the local theorem. Every premise of (1) is supplied by the same actual owners.

Their strict markers (-.35,-.35) and (.35,-.35) force the horizontal component of any separator directed from C toward E to be positive. The full separating-axis theorem consequently leaves exactly

    u, e, -v, -f

as possible signed actual central normals. Theorem 1 removes the last two. Therefore only the two actual first normals u,e can separate this edge. Simultaneous quarter turns give every positive-to-positive-retaining edge.

This is a direction theorem, not a complete edge potential or cyclic contradiction. In particular it does not choose the smaller of the two first-normal angles without separately proving the center-coordinate comparison needed for that choice.
