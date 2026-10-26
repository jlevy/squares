# C1092 MPPM: the southeast sources on a missing-to-retaining positive edge

Every terminating decimal is an exact rational. Strict ownership means membership in the interior of the named actual square. Square separators may be tangent. This chapter treats two of the complete four actual central separating directions; it does not assert an entire positive-cycle ending.

## 1. Local faces and the weighted potential

Let two actual open squares C,E of common side a>1 have positive canonical angles p,q. Use the common physical frames

    u=(c,s), v=(-s,c), c=cos p, s=sin p,
    e=(d,t), f=(-t,d), d=cos q, t=sin q,
    0<p<=pi/4, 0<=q<=pi/4.

Write A,K for the upper u,v faces of C. For E write its lower e face as -K_E and its upper f face as A_E. Thus A_E,K_E are its upper faces in its own sector chart, whose first and second normals are f,-e. Set

    x=tan(p/2), y=tan(q/2),
    kappa=cos(q-p)>0, sigma=sin(q-p).

Suppose the same actual faces satisfy

    A>=a-c-s, A<=-.26c,
    A_E>-.26d, K_E<=t,
    x>13/87.                                      (1)

Define the edge expression

    Phi=K-K_E+y-(6/5)x.                            (2)

**Theorem 1.** If either -v or -f is a separating normal directed from C toward E, then Phi>0. More precisely, the source -v with q>=p gives Phi>1/60; each other case gives Phi>1/50.

The weight in (2) is the edge of the candidate cyclic coordinate

    eta(z,state)=z(1+state/5),

where state=1 for a missing forward point and state=0 for a retained forward point. Only this missing-to-retaining edge is proved here. No statement for the other memberships or the two remaining directions is implied.

## 2. A short global scalar bound

For every 0<=z<=sqrt(2)-1, let b=(1-z^2)/(1+z^2). Then

    b(.26+z)<.48.                                 (3)

Indeed, after multiplication by 1+z^2, the positive difference is

    g(z)=.22-z+.74z^2+z^3
        =z(z-3/8)^2
          +(149/100)(z-1825/4768)^2
          +26047/15257600>0.                     (4)

The identity is exact; its last term is strictly positive and the other two terms are nonnegative for z>=0. We also use

    x,y<=sqrt(2)-1<5/12,
    s,t<.71, c,d>.7.

On the missing-angle interval x>13/87, the exact lower endpoint gives

    s>.29, c+s>1.248, c-s<.665.                   (5)

The endpoint values are c=3700/3869 and s=1131/3869; monotonicity on the canonical interval proves (5).

## 3. The current square's southeast normal

Suppose -v separates C toward E. The actual lower E support uses its upper e face a-K_E when sigma>=0, and its lower e face -K_E when sigma<=0. Its f coefficient is -kappa. Comparing with upper_C(-v)=a-K yields exactly

    K+sigma K_E-kappa A_E
       >=a(1+max(sigma,0)).                       (6)

This retains both signed support alternatives of the same actual square E.

If q>=p, use (1) in (6). Since 1+sigma>0 and a>1,

    K-K_E>(1+sigma)(1-t)-.26kappa d
          >=1-t-.26d>.1.                         (7)

The last inequality follows because sin q+.26cos q increases on [0,pi/4] and its maximum is 1.26/sqrt(2)<.9. Also y>=x, so y-(6/5)x>=-x/5>-1/12. Therefore Phi>1/60.

If q<=p, then -1<sigma<=0. Equation (6) instead gives

    Phi>1-.26kappa d-(1+sigma)t+y-(6/5)x
        >=1-d(.26+y)-(6/5)x>1/50.                (8)

Here kappa<=1, sigma<=0, and t-y=dy. The last sign is (3), together with (6/5)x<1/2. The two calculations agree without difficulty at q=p.

## 4. The successor's southeast normal

Suppose -f separates C toward E. Its C coefficients are sigma on u and -kappa on v. Comparing the actual upper C support with lower_E(-f)=-A_E gives exactly

    kappa K-sigma A-A_E
       >=a[kappa+max(-sigma,0)].                 (9)

### 4.1. q>=p

The coefficient sigma is nonnegative, so use the actual lower bound A>=a-c-s. Equations (1),(9) imply

    Phi>F(p,q)/kappa,
    F=kappa[1-t+y-(6/5)x]
          +sigma(1-c-s)-.26d.                   (10)

For fixed q, differentiate in p and put L=1-t+y-(6/5)x. Since dx/dp=1/(1+c),

    (1/kappa) dF/dp
       =c+s-1-6/[5(1+c)]
          +(sigma/kappa)(L+s-c).                (11)

The function t-y=dy increases with q on the whole canonical interval: its derivative is d-1/(1+d)>0. Hence q>=p implies dy>=cx, and therefore

    L+s-c<=1-c-x/5=x(s-1/5).                    (12)

Also sigma/kappa<=tan(pi/4-p)=(c-s)/(c+s)<.533 by (5). Since s>1/5, the right side of (12) is positive. The exact rational estimates

    c+s-1<.415,
    6/[5(1+c)]>=.6,
    x(s-1/5)<(5/12)(.51)=17/80

now make the right side of (11) strictly less than

    -.185+.533(17/80)=-5739/80000<0.             (13)

Thus F decreases as p runs up to q. Its minimum on the actual ascending interval is its aligned value

    F(q,q)=1-d(.26+y)-(6/5)y>1/50                (14)

by (3). Because 0<kappa<=1, equations (10),(14) give Phi>1/50.

### 4.2. q<=p

Now sigma<=0. In (9) the cap A<=-.26c has the sign needed for a lower bound on sigma A. Equations (1),(9) imply

    Phi>F(p,q)/kappa,
    F=kappa[1-t+y-(6/5)x]
          -(1+.26c)sigma-.26d.                  (15)

Hold p fixed. Its derivative in q is

    dF/dq=-sigma L
       -kappa[1+.26c+d-1/(1+d)]+.26t,
    L=1-t+y-(6/5)x<=1.                          (16)

Since sigma<=0, -sigma L<=-sigma<.71. Moreover kappa>.7, c,d>.7, and 1/(1+d)<.59. Thus (16) is strictly less than

    .71-.7(1+.182+.7-.59)+.26(.71)
        =-49/5000<0.                            (17)

So F decreases up to q=p. At that endpoint it is

    F(p,p)=1-c(.26+x)-(6/5)x>1/50                (18)

by (3). Equations (15),(18) finish this case and Theorem 1. All aligned and axial successor endpoints were retained; strictness comes from the actual strict forward point or a>1 and the displayed positive margins.

## 5. Literal original edge and remaining directions

In the retained no-omission OOOO entrance, suppose Q4 is positive and omits G3, while Q5 is positive and strictly owns F4. Translate by (-2,-2). Their actual markers become (-.35,-.35) and (.35,-.35). Consequently any actual normal directed from Q4 toward Q5 must have positive horizontal component. The complete central separating-axis list is therefore

    u_Q4, u_Q5, -v_Q4, -v_Q5.

The source of every premise in (1) is explicit:

| Local premise | Actual source |
|---|---|
| A>=a-c-s, A<=-.26c and x>13/87 | The unconditional missing-positive profile for actual Q4 |
| A_E>-.26d | Strict F4 in actual Q5, the forward point in its own sector chart |
| K_E<=t | The unconditional preceding-origin exclusion and transverse cap for a positive forward-owned Q5 |
| Common side and disjoint interiors | The original actual square configuration |

The quarter turn takes Q5's own first normal to the common physical f and its own second normal to -e, which is exactly why its native upper face K_E equals minus its physical lower e face. Thus no face convention is changed in the comparison.

If one of the two southeast normals supplies separation, Theorem 1 proves the strict weighted edge inequality (2). Simultaneous quarter turns give all other missing-to-retaining edges. The remaining first-normal sources still require the actual intervening boundary square; they have not been discarded or declared impossible in this chapter.
