# C1092 MPPM with one omission: the actual mixed wall forces the top origin

Every terminating decimal is an exact rational. All squares are actual open squares of a common side a>1, all stated owned points are strict, and excluded points or separating supports may be equality. The local theorem below imposes no wall or center condition. Its application uses the proved one-omission upper core, within that chapter's original side range.

## 1. A local obstruction for the actual mixed wall and its corner

**Theorem 1.** Let L,K be disjoint open squares of the same side a>1. Give L the positive canonical frame

    u_L=(d,r), v_L=(-r,d), d>=r>0, d^2+r^2=1.

Write J for its upper u face and V for its lower v face. Suppose

    G=(0,.4) is strict in L,
    V>=-.4d.                                          (1)

Suppose K strictly owns H=(0,.5), P=(0,1), and excludes A=(.2,1). Then these two actual squares cannot exist.

The excluded A need only be absent from K. In the application it will be strict in the actual top square. The lower-face condition in (1) is essential: it is a proved face of the actual mixed wall, rather than a consequence of the two strict points alone.

### 1.1. The foreign halfpoint forces L's other face

Strict G gives J>.4r. Since H is strict in the different actual K, it is excluded from L. Its two lower bands follow strictly from G. Its upper v band follows from (1), because

    V+a>=a-.4d>.5d=v_L(H).

Hence H must be upper u, and

    .4r<J<=.5r.                                      (2)

### 1.2. Every up-left separating direction is impossible

Orient a separating normal from L toward K. The strict pair G,H forces its y component to be positive. We first exclude every unit direction

    n=(-s,c), c>0, s>=0, c^2+s^2=1,                  (3)

without imposing any order between c and s. Strict H gives lower_K(n)<.5c. Set

    k=cr-sd, alpha=cd+sr>0.

If k>=0, the full upper L support and (1)--(2) give

    upper_L(n)=kJ+alpha(V+a)
               >.4rk+alpha(1-.4d).

Its excess over .5c is therefore greater than cF+sG_0, where

    F=d-.9+.8r^2=.1+(1-d)(.8d-.2)>=.1,
    G_0=r(1-.8d)>0.                                (4)

Here d>=1/sqrt(2)>.7, so .8d-.2>0. Thus the excess is strictly positive.

If k<0, its full upper support instead uses L's lower u face:

    upper_L(n)=k(J-a)+alpha(V+a)
      >=k(.5r-a)+alpha(a-.4d)
      >k(.5r-1)+alpha(1-.4d).                       (5)

The coefficient of a in this step is alpha-k>0. After subtraction of .5c, the last expression is cF_1+sG_1, with

    F_1=d-r-.9d^2, G_1=d+r-.9dr>0.

The sign k<0 gives s/c>r/d. Consequently

    F_1+(s/c)G_1>F_1+(r/d)G_1=1/d-.9>=.1.           (6)

Again upper_L(n)>.5c>lower_K(n). This excludes all of (3), including the vertical direction s=0. Every forward separating direction must therefore be up-right.

The separating-axis theorem for the two full actual squares now leaves L's own u_L and the unique up-right face-normal axis of K. The negative u_L and the other L axis cannot have an admissible orientation. We check both canonical signs of K, including their endpoints.

## 2. A nonnegative corner angle is impossible

Give K the nonnegative canonical frame

    u_K=(c,s), v_K=(-s,c), c>=s>=0, c^2+s^2=1,

and write U,W for its lower faces. The only possible up-right K source is u_K, when its y component is positive; the horizontal endpoint is already outside the strict forward cone.

At the excluded A, its lower u band follows from P, its upper v band follows from P, and its lower v band follows from H. The corresponding nonnegative or positive gaps are .2c, .2s, and .5c-.2s>=.3c>0. Therefore

    U+a<=.2c+s,
    U<0,
    W<.5c,
    W+a>c.                                           (7)

The second inequality follows from .2c+s<=1.2/sqrt(2)<1<a. The final two are strict ownership of H and P.

On K's own direction, (7) gives

    lower_K(u_K)<=.2c+s-a<.2c+s-1.

L's strict G projects to .4s. The support gap is therefore greater than

    1-.2c-.6s>=1-sqrt(.4)>0.                         (8)

Thus u_K cannot separate.

For L's own direction put

    alpha=dc+rs>0, delta=rc-ds.

If delta<0, its exact lower K support is alpha U+delta(W+a)<0 by (7), while upper_L(u_L)=J>.4r>0. This relative-angle order is impossible.

If delta>=0, the lower support is alpha U+delta W. Using (7), a>1, and the positive coefficient alpha gives

    lower_K(u_L)-upper_L(u_L)
       <alpha(.2c+s-1)+.5c delta-.4r
       =dF_2+rG_2,                                  (9)

where

    F_2=.2c^2+.5cs-c<0,
    G_2=.1+.5s^2-s+.2cs,
    F_2+G_2=.3+.3s^2+.7cs-c-s<=-.2.                 (10)

For F_2 use c>.7, c^2<=1 and cs<=.5, which give F_2<-.25. For the sum use s^2<=.5, cs<=.5 and c+s>=1. If G_2<=0, the expression in (9) is negative directly. If G_2>0, r<=d gives dF_2+rG_2<=d(F_2+G_2)<0. Thus u_L cannot separate either. Equality delta=0 is explicitly included.

No nonnegative canonical K survives.

## 3. A nonpositive corner angle is impossible

Give K the nonpositive canonical frame

    u_K=(c,-s), v_K=(s,c), c>=s>=0, c^2+s^2=1,

with lower faces U,W. Its only possible up-right source is v_K. At A the lower u band follows from P and the lower v band from H. Thus its only possible exits are upper u and upper v.

### 3.1. The upper-u exit

Suppose U+a<=.2c-s. Strict H gives U+a>-.5s, hence

    s/c<.4, c>.9, s<.4.                             (11)

Strict H also gives W<.5c. Put

    alpha=dc-rs>0, beta=ds+rc>0.

The exact lower K support on u_L is alpha U+beta W. Therefore

    lower_K(u_L)-upper_L(u_L)
      <dF_3+rG_3,
    F_3=.2c^2-.5cs-c<-.7,
    G_3=.1+.5s^2+s-.2cs<.58.                       (12)

These bounds follow directly from (11). Since r<=d, the expression is less than -.7d+.58r<=-.12d<0. This excludes u_L.

For v_K=(s,c), its coefficients along L's two normals are beta>0 and alpha>0. Its full upper L support satisfies

    upper_L(v_K)=beta J+alpha(V+a)
                  >.4r beta+alpha(1-.4d).

The excess over .5c is

    cF-sG_0,

where F,G_0 are exactly (4). By (11), this is strictly greater than c(F-.4G_0). The latter bracket has the exact decomposition

    F-.4G_0
       =.1-.08r+(1-d)(.8d-.2-.32r).                 (13)

The last factor is positive, because

    .8d-.2-.32r>=.48d-.2>.48(.7)-.2=.136>0.

Also r<=1/sqrt(2)<3/4, so .1-.08r>.04. Thus upper_L(v_K)>.5c, whereas lower_K(v_K)=W<.5c. This excludes v_K. In contrast to the MMMP top-origin argument, this estimate uses the actual mixed lower face V>=-.4d and requires no center sign.

### 3.2. The upper-v exit

Suppose W+a<=c+.2s. Its own K source is impossible, since

    upper_L(v_K)>.4c,
    lower_K(v_K)=W<c+.2s-1,
    1-.6c-.2s>=1-sqrt(.4)>0.                       (14)

For u_L, set alpha=dc-rs>=0 and beta=ds+rc>0. Strict P gives U<-s. Using W<=c+.2s-a and a>1 gives

    lower_K(u_L)-upper_L(u_L)
       <d(.2s^2-s)+r(.6-c+.2cs)<0.                 (15)

The first bracket is nonpositive. The second is at most .7-c<0, since cs<=.5 and c>=1/sqrt(2)>.7. Because r>0, the final inequality is strict even at s=0 or alpha=0. Thus u_L also fails.

Both possible exits of the genuinely excluded A have ruled out both actual normal sources. Every canonical orientation of K has been covered. Theorem1 follows.

## 4. Literal one-omission application

**Theorem 2.** Throughout the normalized one-omission MPPM family, in the transposed chart of `C1092-MPPM-ONE-OMISSION-UPPER-CORE.md`,

    (2,3) is strictly in the actual T=Q10,
    [1.44,2]x{3} is strictly in that same T.           (16)

Equivalently, in original coordinates (3,2) belongs strictly to Q10.

**Proof.** Suppose (2,3) were absent from T. Theorem7 of `C1092-DIRECT-WALL-POINT.md`, reflected in y=2, applies to the actual northwest paired corner K_NW=Q1 and actual T. Its independent strict inputs are K_NW's paired point (1,3) and marker (1,3.086), T's original marker (2,3.086) and owned F3=(1.6,3), and their genuine reflected container walls. By contraposition, the absent boundary origin forces

    (1,2.5) strictly in K_NW.                         (17)

The wall-origin alternative, Theorem11 of `C981-WALL-CYCLES.md`, applies to the same actual T in the chart (xi,eta)=(2-x,y-3), with e=.086,r=.4,z=.8. Its strict marker and anchor come from the original marker and F3, its real wall is eta<=1, and its missing origin is exactly the present supposition. The inequality .8<2sqrt(2)-2 follows from (7/5)^2<2. Hence

    (1.2,3) strictly in T.                            (18)

Use the simultaneous local chart (X,Y)=(x-1,y-2). The actual L is the mixed original Q9. Theorem4 of the upper-core chapter gives its positive frame (d,r),(-r,d). Its lower v face in centered transposed coordinates is at least r-.4d. The present translation increases x by one, so this local lower face is at least -.4d. The exact premise table for Theorem1 is therefore

| Local datum | Transposed actual datum | Genuine source |
|---|---|---|
| L's strict G=(0,.4) | G1=(1,2.4) in L | The original mixed Q9 bar |
| L's positive frame and V>=-.4d | The same actual L | UPPER-CORE, Theorem4, followed by the stated translation |
| K's strict H=(0,.5) | (1,2.5) in K_NW | The supposed missing origin through (17) |
| K's strict P=(0,1) | (1,3) in K_NW | The original paired-corner seed |
| A=(.2,1) excluded from K | (1.2,3) in T | The actual wall-origin alternative (18) |

These are distinct actual squares of the common side. Theorem1 contradicts their disjoint interiors. Thus (2,3) is strict in T. Its earlier actual point (1.44,3), supplied by the mixed-wall theorem, joins it by convexity to give the entire strict segment in (16).

The original mixed L center condition center_y(L)<=2 remains intact. It was used in the approved upper-core theorem to obtain the mixed sign and face, and no opposite center condition is invoked here. The new two-square local obstruction replaces that missing MMMP premise completely.
