# C1092 MMMP: the actual left wall and corner force the top origin

All terminating decimals denote exact rationals. Every square is an actual open square. Owned points are strict; exclusions, genuine wall contacts and separating supports may be equality. The local theorem uses only a>1. Its MMMP application has the original side range 1<a<=1.001 through the earlier left-auxiliary theorem.

## 1. The local three-square obstruction

**Theorem 1.** Let L,K,T be pairwise disjoint open squares of common side a>1. Assume the following actual data in one common chart:

| Actual square | Strict points | Further conditions |
|---|---|---|
| L | S0=(-.086,0), O=(0,0), G=(0,.4) | Closure in x>=-1; center ordinate nonnegative; excludes X=(.5,0), Z=(.19,.2) |
| K | H=(0,.5), P=(0,1), P+=(0,1.086) | Closure in x>=-1 |
| T | A=(.2,1), A0=(.44,1), S=(1,1.086) | Closure in y<=2; excludes O_T=(1,1) |

Then these three actual squares cannot exist.

No center condition on K or T is imposed. The two isolated L exclusions need no owner in the local statement.

### 1.1. The corner sign and the forward left-to-corner cone

Convexity between L's O,G supplies (0,.39) strictly in that same L. The theorem in `CORNER-LEFT-WALL-SIGN.md` applies literally to L,K: its four L premises are O,(0,.39), the excluded X, and the displayed wall/center conditions; its K premises are H,P and excluded A0, the latter strict in the different actual T. Consequently K has a strictly negative canonical frame

    u_K=(c,-s), v_K=(s,c), c>=s>0, c^2+s^2=1.

Write its lower faces as U,V and its upper faces as U+a,V+a.

Section 2 of that same proof, with exactly these actual L/K data, proves two additional facts without any assumption on K's sign. The center abscissa of L is strictly negative, and every up-left separating normal from L to K is impossible. Indeed any such unit normal n=(-p,q), p,q>=0, has

    upper_L(n)>=a/2>.5,
    lower_K(n)<n.H=.5q<=.5.

Since O in L and H in K force the ordinate of every forward separating normal to be positive, only up-right actual face normals remain.

In a nonnegative L frame (d,t),(-t,d), that proof also gives t>0 and upper-u face J_L<=.5t. In a nonpositive L frame (d,-t),(t,d), it gives t>0 and upper-v face B_L<=.5d. These facts used weak exits at the actual foreign H and isolated X; no strict exterior gap was assumed.

## 2. The left square must also have negative angle

Suppose instead L has the nonnegative frame

    u_L=(d,t), v_L=(-t,d), d>=t>0, d^2+t^2=1.

Write J,B for its upper faces. Its strict G gives J>.4t and B>.4d. The only remaining separating-normal sources from L to K are u_L and v_K.

The excluded A has its lower u_K-band from K's P and its lower v_K-band from K's H. Hence it is upper u_K or upper v_K.

### 2.1. A is upper u_K

Then U+a<=.2c-s. Strict H gives U+a>-.5s, so

    s/c<.4, c>.9, s<.4.                              (1)

Also V<.5c by strict H. Put

    alpha=dc-ts>=0, beta=ds+tc>0.

On L's own direction its complete lower K support is alpha U+beta V. Subtracting the strict L projection .4t and replacing a by 1 gives a strict upper bound for lower_K(u_L)-upper_L(u_L), namely

    d F+t G0,
    F=.2c^2-.5cs-c<-.7,
    G0=.1+.5s^2+s-.2cs<.58.

Thus the difference is less than -.7d+.58t<=-.12d<0. This source cannot separate.

For v_K=(s,c), put alpha1=sd+ct and beta1=cd-st. Both are positive under (1). L's center sign gives

    B>=a(d+t)/(2d)-(t/d)J.

Therefore its full upper support satisfies

    upper_L(v_K)=alpha1 J+beta1 B
       > .4st/d+beta1(d+t)/(2d).

After subtracting .5c and multiplying by 2d, the last expression is

    cd(h-1)-st(h-.8), h=d+t.

By (1), this expression is greater than

    ct[2d^2/(h+1)-.4(h-.8)]>0.

Here h-1=2dt/(h+1), d^2>=1/2, h<3/2; the bracket exceeds .4-.28=.12. Thus upper_L(v_K)>.5c, whereas lower_K(v_K)=V<.5c. This source also fails.

### 2.2. A is upper v_K

Now V+a<=c+.2s. The direction v_K cannot separate, because its lower K support is less than c+.2s-1 while L's strict G projects to .4c, and

    .6c+.2s<=sqrt(.4)<1.

For u_L, strict P gives U<-s. Using the complete support alpha U+beta V and subtracting .4t yields a strict upper bound

    d(.2s^2-s)+t(.6-c+.2cs)<0.

The first bracket is negative; the second is at most .7-c<0, since cs<=1/2 and c>=1/sqrt(2)>.7. Thus this source fails too.

Both weak face alternatives for A have ruled out both actual sources. Therefore L is necessarily negative:

    u_L=(d,-t), v_L=(t,d), d>=t>0.                    (2)

## 3. The new foreign point makes this left angle small

Continue to write J,B for L's upper faces in (2). Section 1.1 gives B<=.5d.

At Z=(.19,.2), the lower u-band follows from strict S0, with increment .276d-.2t>=.076d>0. The lower v-band follows from O. The upper v-band follows from G, with increment .2d-.19t>=.01d>0. Consequently

    J<=.19d-.2t, B<=.5d.

The least x coordinate of the actual L is d(J-a)+t(B-a). Its genuine wall and a>1 imply

    d+t<1+.19d^2+.3dt.                               (3)

We claim

    t/d<1/3, and hence t<1/3.                        (4)

Otherwise d^2<=9/10 and h=d+t>=4/sqrt(10). The right side of (3) is at most 1.021+.15h^2. But h-1.021-.15h^2 increases on [4/sqrt(10),sqrt(2)], and its value at the lower endpoint is

    4/sqrt(10)-1.261>0.

The last inequality is exact because 8/5>(1261/1000)^2. This contradicts (3), proving (4).

One useful full-face lower bound also follows from L's wall and center sign:

    B=t center_x(L)+d center_y(L)+a/2
      >=-t+a[1+t(d+t)]/2
      >(1-t)/2>1/3.                                 (5)

## 4. A corner-center inequality forced by actual L--K separation

Write K's actual center as

    center_x(K)=-1+a(c+s)/2+z, z>=0,
    center_y(K)=Y.

The nonnegative z is supplied by the genuine left wall for this same K.

**Lemma 2.** If a separating normal from L to K is the up-right unit vector n=(x,y), then it is one of v_L=(t,d), v_K=(s,c), and

    Y>=a-(x/y)z.                                    (6)

**Proof.** Section 1.1 gives the exhaustive two sources; both have 0<x<=y. For either source the actual left-wall and center conditions give

    upper_L(n)>=-x+(a/2)[x(d+t)+|xd-yt|+xt+yd]
               >=-x+(a/2)[1+x(x+y)].                 (7)

Here is the continuous orientation check for the second inequality. Allow L's angle to range over the larger interval [0,pi/2]. The expression in the first bracket is a positive sine/cosine expression on each side of xd=yt, so it is concave on each piece. At the two axial endpoints it is 2x+y. At the joining angle (d,t)=(y,x) it is 1+x(x+y). The axial excess is

    2x+y-1-x(x+y)=(x+y-1)(1-x)>=0.

The endpoint minima therefore prove (7) on both entire pieces.

The actual lower K support is

    x[-1+a(c+s)/2+z]+yY
       -(a/2)[|xc-ys|+xs+yc].

Comparing with (7), separation implies

    xz+yY >= (a/2) E,
    E=1+x^2+xy+|xc-ys|+xs+yc-x(c+s).                (8)

In fact E>=2. If xc>=ys, then c-s>=y-x, and

    E=1+x^2+xy+y(c-s)>=2.

If xc<=ys, the canonical angle order gives c<=y and c+s>=x+y; hence

    E=1+x^2+xy-2xc+y(c+s)>=2.

Thus (8) gives Y>=a/y-(x/y)z, which implies (6) because y<=1. The stronger inequality is retained here only to show that no angle endpoint loses the sign. ∎

## 5. Exact face consequences of the missing top origin

Choose T's up-right face frame

    u_T=(b,r), v_T=(-r,b), b,r>=0, b^2+r^2=1,

with lower faces p,q. This single quadrant parametrizes every square orientation, without requiring b>=r.

At O_T its lower u-band follows from A and its two upper bands follow from S. Thus its exclusion forces

    q>=b-r.                                         (9)

Both axial endpoints are impossible: at r=0 the strict A would have the same v projection as this lower bound; at b=0 the strict S would have it. Hence b,r>0. Put

    rho=atan(r/b) in (0,pi/2), h=r/(1+b) in (0,1).

T's real top wall is

    r(p+a)+b(q+a)<=2.

Together with (9) and a>1 it gives the strict cap

    p<b+r-1+h=:f,
    f=1-(1-h)^3/(1+h^2)<1.                         (10)

Orient a possible separating normal from K to T. The strict pair P,A forces its first component positive. The strict pair P+,A gives, whenever its second component is positive,

    n_y/n_x<100/43<5/2.                             (11)

The possible actual sources are u_K,v_K,u_T,-v_T. We next eliminate the two downward sources without imposing any angle order.

### 5.1. T's downward normal is impossible

For -v_T=(r,-b), equations (9) and a>1 give

    lower_T(-v_T)=-(q+a)<r-b-1<=-b.

But strict K point P projects to -b. Thus this direction cannot separate.

### 5.2. K's downward normal is impossible

Put

    alpha=cb-sr, k=cr+sb>0.

If alpha>=0, the full lower T support in direction u_K is alpha p-k(q+a). Eliminate p using the actual top wall. The coefficient of q is -c/r<0, and the coefficient of a is negative. Substituting (9) and then weakening a to 1 gives the strict bound

    lower_T(u_K)<c X0-s Y0,
    X0=-h(1-r)<0, Y0=2-r>1.                         (12)

For an explicit check, (X0,Y0) is the vertex f u_T+(b-r+1)v_T; its coordinates simplify exactly to the displayed expressions. Thus (12) is strictly less than -s, the projection of K's strict P.

If alpha<0, use instead strict S, which gives p+a>b+1.086r. The exact lower support is alpha(p+a)-k(q+a). Therefore

    lower_T(u_K)<c-s+.086alpha r-a k
                <c-s+.086alpha r-k<-s.              (13)

To verify the last sign, alpha<0 gives sb>cb^2/r, and hence

    c-k=c(1-r)-sb<c(1-1/r)<0.

The remaining .086alpha r is negative. Both signs of alpha have contradicted strict P. Thus u_K cannot separate either.

Only the up-right actual sources v_K and u_T remain.

## 6. K's up-right normal cannot separate K from T

Suppose the K-to-T normal is v_K=(s,c).

If L-to-K separation also uses v_K, then (using strict G in L)

    upper_K(v_K)=lower_K(v_K)+a
       >=upper_L(v_K)+a>.4c+1>c+.2s.

The last sign follows from .6c+.2s<1. But T's strict A projects to c+.2s, contradicting separation.

Otherwise L-to-K separation uses v_L=(t,d). Apply Lemma 2 with lambda=t/d.

If s/c>=lambda, the coefficient s-c lambda is nonnegative. Formula (6) and z>=0 give

    upper_K(v_K)>=-s+a[s(c+s)/2+c+1/2].

Subtracting c+.2s and weakening a to 1 leaves

    1/2-1.2s+s(c+s)/2
       >=1/2-.7s>=1/2-.7/sqrt(2)>0.                (14)

Thus T's A again forbids separation.

If s/c<lambda, put alpha2=tc-ds>0, beta2=ts+dc<=1. The actual L-to-K inequality is

    B<=lower_K(v_L)=alpha2 U+beta2 V.

Strict P gives U<-s<0, and (5) gives B>1/3. Consequently V>1/3. Hence upper_K(v_K)=V+a>4/3, whereas

    v_K(A)=c+.2s<=sqrt(26/25)<4/3.

This final angle order is impossible too. The source v_K has been eliminated exhaustively.

## 7. T's up-right normal cannot separate K from T

It remains to suppose separation on u_T=(b,r). Put

    alpha=bc-rs, beta=bs+rc>0.

### 7.1. One exceptional relative-angle combination has a direct width contradiction

If L-to-K separation uses v_K and alpha<0, then V>=upper_L(v_K)>.4c. Since U<0, the full upper K support is

    upper_K(u_T)=alpha U+beta(V+a)>beta(1+.4c).

Here alpha<0 means pi/2<rho+theta_K, where theta_K=atan(s/c)<=pi/4. Equation (11) for u_T gives rho<atan(5/2), and therefore

    beta=sin(rho+theta_K)>7/sqrt(58)>9/10.

Also c>7/10. Thus upper_K(u_T)>144/125>1, whereas (10) gives lower_T(u_T)=p<1. This combination is impossible.

### 7.2. The actual corner-center comparison for all other combinations

In every other case Lemma 2 supplies (6) with a coefficient lambda satisfying b-r lambda>=0. Indeed, if L-to-K uses v_K, then alpha>=0 gives b-r(s/c)>=0. If it uses v_L, (4),(11) give r lambda<b.

Consequently the actual center of K satisfies

    b center_x(K)+r center_y(K)
       >=-b+a[b(c+s)/2+r].

After adding K's full half-width, its upper support is bounded below by

    -b+(a/2)[b(c+s)+2r+|alpha|+beta].                (15)

The coefficient of a is positive. Subtract the strict T cap f from (10) and weaken a to 1. The resulting continuous difference is

    D+=b(c+s-2)+(r/2)(c-s)+1-h,    if alpha>=0,
    D-=b(s-2)+(r/2)(c+s)+1-h,      if alpha<=0.       (16)

We prove both differences positive over their full domains, including the joining equality.

For fixed rho, each expression is concave as a function of theta_K on its relevant interval. In D+ the nonconstant trigonometric part is b(c+s)+(r/2)(c-s)>0; in D- it is bs+(r/2)(c+s)>0. Their second derivatives are the negatives of these positive expressions. It therefore suffices to check the interval endpoints.

### 7.3. Endpoints of D+

At theta_K=0,

    D+ =1-b+r/2-h
       =(1-b)[1-r/(2(1+b))]>0.                     (17)

If rho<=pi/4, the other endpoint is theta_K=pi/4, with value

    b(sqrt(2)-2)+1-h.

Its derivative in rho is (2-sqrt(2))r-1/(1+b)<0: its first term is at most sqrt(2)-1<1/2, and its second is at least 1/2. The minimum on this rho interval is therefore its value at pi/4, namely

    3-2sqrt(2)>0.                                   (18)

If rho>=pi/4, the other endpoint is theta_K=pi/2-rho, where c=r,s=b and alpha=0. Exact half-angle substitution gives the value

    E(h)=h^2[2-3h+4h^2-h^3]/(1+h^2)^2>0.            (19)

For 0<h<1 the bracket is at least 2-3h+3h^2=3(h-1/2)^2+5/4>0. Thus every endpoint of D+ is positive.

### 7.4. Endpoints of D-

This case occurs only when rho>=pi/4. At theta_K=pi/2-rho its value is the same positive E(h). At theta_K=pi/4 its value is

    (b+r)/sqrt(2)-2b+1-h.                            (20)

It increases on pi/4<=rho<pi/2. To check this directly, put q0=1/sqrt(2); its derivative is

    (2-q0)r+q0 b-1/(1+b)>0.

The first two terms form a positive concave sinusoid on this interval. Its endpoint values are sqrt(2) and 2-q0, both greater than one; the subtracted term is at most one. Thus (20) is at least its value at rho=pi/4, again 3-2sqrt(2)>0.

All endpoint values in (16) are positive. Concavity proves positivity throughout both entire relative-angle regions. Equations (10),(15) therefore contradict separation on u_T.

Every possible actual K-to-T normal has failed. This completes the local three-square contradiction and proves Theorem 1. No discarded angle interval, sampled value, or hypothetical support of a replacement square occurs in the argument.

## 8. Literal application to the entire original MMMP entrance

**Theorem 3.** Throughout the entire original C1092 MMMP family,

    (2,3) belongs strictly to actual Q11.             (21)

**Proof.** Suppose this point were absent. The contrapositive of Theorem 7 in `C1092-DIRECT-WALL-POINT.md`, reflected in y=2 with actual corner Q3 and actual boundary Q11, then gives (1,2.5) strictly in Q3. The independent strict inputs for that transfer are Q3's original paired point and corner marker, Q11's original marker and its proved F3, and their genuine container walls. No left-wall halfpoint is presumed.

The wall-origin alternative, Theorem 11 of `C981-WALL-CYCLES.md`, applies to this same Q11 in the chart (xi,eta)=(2-x,y-3), with e=.086,r=.4,z=.8. Its marker and anchor are the actual top marker and F3; its missing origin is the present supposition. The condition .8<=2sqrt(2)-2 follows from (7/5)^2<2. It gives (1.2,3) strictly in Q11.

Use the common local chart (X,Y)=(x-1,y-2), with L=Q8,K=Q3,T=Q11. The complete premise map for Theorem 1 is:

| Local datum | Original datum | Actual source |
|---|---|---|
| S0,O,G in L | (.914,2),(1,2),(1,2.4) | Original Q8 marker; wall transfer; `C1092-MMMP-LEFT-FAR-AUXILIARY.md` |
| X,Z excluded from L | (1.5,2),(1.19,2.2) | Strict in actual Q7 by the crosspoint and upper-strict-point theorems |
| H in K | (1,2.5) | Contrary top-origin hypothesis through the actual paired-corner transfer |
| P,P+ in K | (1,3),(1,3.086) | Original paired point and marker of Q3 |
| A in T | (1.2,3) | The wall-origin alternative just applied to actual Q11 |
| A0 in T | (1.44,3) | `C1092-MMMP-WALL-TRANSFER.md` |
| S in T | (2,3.086) | Original Q11 marker |
| O_T excluded from T | (2,3) | The contrary hypothesis |
| L,K closure in X>=-1 | Original x>=0 | Their genuine left container wall |
| T closure in Y<=2 | Original y<=4 | Its genuine top container wall |
| Center_Y(L)>=0 | Original Y8>=2 | Original closed MMMP sign |

All three roles are distinct actual original squares with the same side and disjoint interiors. Theorem 1 contradicts exactly these facts. Thus the supposed missing point is impossible, proving (21).

Together with the earlier strict top advance, (21) gives the entire actual strict segment [1.44,2] x {3} in Q11. This conclusion holds for all remaining left-wall components, including those that own F0; no additional ordinary-wall exclusion was used. The full MMMP family still requires its final coupled-central contradiction, which is separate from this completed top-origin theorem. ∎
