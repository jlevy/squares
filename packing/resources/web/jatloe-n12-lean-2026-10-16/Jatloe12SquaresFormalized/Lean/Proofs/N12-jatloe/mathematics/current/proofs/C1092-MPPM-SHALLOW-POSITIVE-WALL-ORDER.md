# C1092 MPPM: the same-face wall order closes the all-positive ordinary cycle

All terminating decimals are exact rationals. Strict points belong to the interiors of the named actual open squares. Exclusion and separation permit equality. Every wall and every separating support in this chapter belongs to an actual square of the common side a>1. In particular, the two adjacent wall comparisons below retain one and the same central upper face K.

The scalar companion is C1092-MPPM-SHALLOW-POSITIVE-WALL-ORDER-SCALARS.md. Its two lemmas prove the full continuous inequalities used here, including coordinate and aligned endpoints.

## 1. Local actual-square theorem

Work in coordinates centered at (2,2). Let the central C have a positive canonical frame

    u=(c,s), v=(-s,c), c=cos p, s=sin p,
    0<p<=2 atan(1/4),
    U<u dot Z<A=U+a, V<v dot Z<K=V+a.

Suppose C strictly owns M=(-.35,-.35), P=(-1,-.26), and has the simultaneous actual faces

    U>=-c-s, V>=.56s-c, A<=-.5s, K<=s.           (1)

Let B and L be actual squares with interiors disjoint from C, with the following strict points and real walls:

| Actual square | Strict points | Real wall |
|---|---|---|
| B | B0=(0,-1.086), F2=(-.4,-1) | Closure contained in y>=-2 |
| L | R=(-1.086,0), D=(-1,0) | Closure contained in x>=-2 |

Their orientations are unrestricted. Write xB for B's actual center x-coordinate and yL for L's actual center y-coordinate.

**Theorem 1.** These same actual squares satisfy

    xB+yL>0.                                      (2)

For the proof put L_c=c+s and define

    b(K)=[a(3/2+cL_c/2)-K-2c]/s,
    ell(K)=[K-2s+(a/2)(1+sL_c)]/c.               (3)

We will prove xB>=b(K) and yL>-b(K). Their K is the one actual upper-v face in (1). The width between the two actual v-faces also gives the intrinsic bound

    a=K-V<=c+.44s,                               (4)

which supplies exactly the scalar companion's side premise. The local theorem does not need an extraneous upper side cutoff or a sign for either boundary center.

## 2. Every possible actual normal

A separating normal directed from B toward C must satisfy, by the two strict anchor differences P-B0 and M-F2,

    -nx+.826ny>0, .05nx+.65ny>0.

Thus ny>0 and nx<.826ny. A normal directed from C toward L similarly satisfies, by P,D and M,R,

    ny>0, nx<(175/368)ny.                         (5)

The only signed face normal of C in either cone is v=(-s,c): its other upward face normal u has nx/ny=c/s>=15/8, while the opposite normals point downward. The separating-axis theorem therefore leaves v, or an actual boundary face normal pointing northeast or northwest. We retain all of them, including repeated sources when the actual frames align.

For an arbitrarily oriented unit-side square let k_0 be its vertical, equivalently horizontal, width and let w_v be its width in direction v. The elementary square-width lemma in Section 2 of C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md gives

    c k_0+w_v>=1+cL_c,
    s k_0+w_v>=1+sL_c.                            (6)

These identities of width bounds cover every boundary orientation; no sign reduction is implicit in their use.

## 3. The bottom envelope

We prove xB>=b(K) by supposing xB<b(K) and excluding every B-to-C normal in Section 2.

For v itself, the actual bottom wall gives

    upper_B(v)>=-s xB-2c+(a/2)(c k_0+w_v).

By (3),(6), this is strictly greater than K-a=lower_C(v), so v cannot separate.

For a northeast actual boundary normal n=(h,t), h,t>=0, put

    lambda=ch+st>0, mu=ct-sh>0.

The strict cone (5), with its bottom constant .826, ensures mu>0. The upper caps in (1) give

    lower_C(n)<=lambda(-.5s-a)+mu(s-a).

Subtract n dot F2 and use a>1. The result is strictly less than

    h[-c+s+.4-s^2-.5cs]
       +t[1-c-s+cs-.5s^2]<0.                    (7)

The first bracket is negative because c-s>=7/17>.4. The second is the negative of the strictly positive expression (5) in the scalar companion. Thus lower_C(n)<n dot F2<upper_B(n), and this actual normal fails as well.

It remains a northwest actual B face normal

    n=(-h,t)=(-cos phi,sin phi), 0<=phi<=pi/2.

Put delta=st-ch, kappa=sh+ct and phi_C=pi/2-p. The exact lower C support is

    lower_C(n)=delta A+kappa(K-a)-a max(delta,0). (8)

Because n is an actual B face normal, its unit-side width in n is 1 and its vertical width is h+t. Its real bottom wall therefore gives

    upper_B(n)>=-h xB-2t+(a/2)(1+t^2+ht).        (9)

In the difference of (9), with xB replaced by b(K), and (8), the coefficient of K is -c delta/s. The allowed substitutions in the two complete angle intervals are consequently

| Interval | Substitutions giving a lower support difference |
|---|---|
| delta>=0 | A<=-.5s and K<=s |
| delta<=0 | A>=a-c-s and K>=a+.56s-c |

These produce exactly g_+ and g_- of Lemma 1 in the scalar companion. That lemma gives nonnegative differences throughout both intervals. The actual strict reverse hypothesis xB<b(K) adds the strictly positive term h[b(K)-xB] whenever h>0. At h=0 the scalar companion gives g_+(pi/2)>0 itself. Thus every proposed actual B normal is impossible. This proves

    xB>=b(K).                                    (10)

## 4. The left comparison: central and northeast sources

We now prove yL>-b(K). Suppose instead yL<=-b(K).

The sum of the two scalar functions in (3) is strictly positive. Indeed its K coefficient is 1/c-1/s<0, so K<=s permits replacement by s as a lower bound. Its a coefficient is positive. Dropping a>1 to one then gives the exact strict estimate

    b(K)+ell(K)
      >s(L_c-1)/[c(1+c)]>0.                     (11)

This is a calculation with the same K, not two independently chosen face values.

For the central source v, L's real left wall and (6) give

    lower_L(v)<=2s+c yL-(a/2)(s k_0+w_v)
              <=2s-c b(K)-(a/2)(1+sL_c)<K,

where the last inequality is precisely (11). Hence v cannot separate C from L.

For a northeast L face normal n=(h,t), h,t>=0, the cone again gives lambda=ch+st>0 and mu=ct-sh>0. The lower-face bounds in (1) imply

    upper_C(n)>=lambda(a-c-s)+mu(a+.56s-c).

Subtract n dot D. At a=1 the exact lower expression is

    h[c-s+.44s^2]+t[L_c-1-.44cs]>0.             (12)

The first bracket is positive. The second is positive because L_c-1=2cs/(1+L_c)>.8cs. The a coefficient is positive, so (12) gives upper_C(n)>n dot D>lower_L(n), excluding every northeast source.

## 5. Northwest left normals up to pi/4

Write a remaining actual L normal as n=(-h,t)=(-cos phi,sin phi). First suppose 0<=phi<=pi/4. Then delta=st-ch<0. Applying (1) to the exact upper C support gives

    upper_C(n)>=n dot Z,
    Z=(-a-s/2)u+(a+.56s-c)v.                     (13)

Here Z is a vector expressing this support lower bound; it is not asserted to be an additional owned point. Its coordinates are

    Z_x=-a(c+s)+.5cs-.56s^2,
    Z_y=a(c-s)+.56cs-.5s^2-c^2.

Let P_0=-Z_x-1. Then P_0>0, since

    P_0>L_c-1-.5cs+.56s^2>0.

This uses a>1 and L_c-1>.8cs.

The useful joint bound is

    P_0+Z_y>-(1-c)^2+.06s(c+s)
             =s[.06(c+s)-s x^2]>0,
    x=s/(1+c)<=1/4.                              (14)

For the last sign, c+s>=1 and s<=8/17 give the uniform bracket bound .06-1/34=13/425>0. Since h>=t,

    upper_C(n)-n dot D
      >=hP_0+tZ_y=(h-t)P_0+t(P_0+Z_y)>0.         (15)

The strict sign also covers t=0, where the first term is positive. This contradicts the strict D ownership in L, so no normal in this interval can separate the two actual squares.

## 6. The strict origin controls the same face K

It remains pi/4<=phi<=pi/2. Set beta=pi/2-phi, so

    0<=beta<=pi/4,
    n=(-r,d), r=sin beta, d=cos beta,
    k=cd+sr>0, tau=cr-sd.

The exact upper C support is

    S_C(n)=-tau A+kK+a max(tau,0).               (16)

The same actual L strictly owns D=(-1,0), with n dot D=r. Therefore any proposed C-to-L separation must satisfy the additional strict inequality

    S_C(n)<=lower_L(n)<r.                         (17)

This is the coupling that must be retained. It implies

    K<K_D(A):=[r+tau A-a max(tau,0)]/k.           (18)

No different central position or independently optimized K is introduced.

Because n is an actual L face normal, its horizontal unit-side width is r+d and its n-width is 1. The real left wall and the supposed yL<=-b(K) imply

    lower_L(n)<=2r+d yL-(a/2)(1+r^2+rd)
               <=2r-d b(K)-(a/2)(1+r^2+rd).      (19)

Subtract the right side of (19) from (16). Its K coefficient is k-d/s<0: indeed k<=1 while d/s>1 because d>=1/sqrt(2) and s<=8/17<1/2. Thus the strict bound (18), applied to this same difference, makes it strictly greater than

    d/s [a(3/2+cL_c/2)-2c-K_D(A)]
                            -r+(a/2)(1+r^2+rd). (20)

The A coefficient in (20) is -d tau/(s k). If beta>=p, then tau>=0 and A<=-.5s gives the lower bound Gamma_+ in (10) of the scalar companion. If beta<=p, then tau<=0 and A>=a-c-s gives Gamma_- in (11). At equality beta=p either formula is valid. Lemma 2 there proves both expressions strictly positive on their full intervals.

Consequently S_C(n)>lower_L(n), contrary to the proposed separation. Every actual northwest L source has been excluded, as have the central and northeast sources. The supposition yL<=-b(K) was therefore impossible. Together with (10), this proves

    yL>-b(K), xB+yL>0,

and finishes Theorem 1. ∎

## 7. Literal all-positive OOOO application

Retain the original no-omission MPPM all-four-ordinary family, with 1<a<=1.001. Suppose all four central canonical angles are positive. The fully proved C1092-MPPM-POSITIVE-RETAINING-ANGLE-AND-ORIGINS.md gives all four actual wall origins and the simultaneous facts below:

| Central forward membership | Actual facts already proved |
|---|---|
| Retained | Half-angle<1/4, A<=-.5s, strict outer halfpoint and X |
| Omitted | The ordinary-marker theorem gives the strict outer halfpoint; the universal positive theorem gives strict X |
| Either | U>=-c-s, V>=.56s-c, K<=s; all four actual wall origins are strict |

For a retaining C=Q4, every local premise of Theorem 1 comes from the following actual sources after translation by (-2,-2):

| Local datum | Actual datum and owner |
|---|---|
| M,P strict in C | SW marker (1.65,1.65) and F0=(1,1.74), both in Q4 |
| Shallow angle and A<=-.5s | The retaining-recipient theorem with actual Q7 predecessor and actual Q5 crosspoint |
| U>=-c-s, K<=s | The universal positive actual-face theorem |
| V>=.56s-c | Actual far point (1.44,1) in Q9, proved from genuine G5=(2.26,1) in Q5 |
| B0,F2 strict in B | Original marker (2,.914), F2=(1.6,1), both in Q9 |
| R,D strict in L | Original marker (.914,2) and proved origin (1,2), both in Q8 |
| Bottom and left walls | Original container walls of Q9 and Q8 |

The other rows are simultaneous quarter turns R(x,y)=(4-y,x), including the actual square owners and the real walls. Theorem 1 consequently gives xB+yL>0 at every retaining positive sector.

For a missing-forward positive sector, Corollary 3 of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md gives the same strict actual wall-center sum. Its hypotheses are also literal here: the strict ordinary marker and pair, the strict outer halfpoint, the paired-corner point, the omitted forward point, the actual preceding origin, and the whole genuine far bottom bar. The same actual origins proved above supply its L premise. No point is assigned a new owner merely because the central omits it. All orientation cases in that boundary theorem were proved continuously and allow tangent exclusions.

Thus every one of the four sectors, with either forward membership, satisfies the same strict order.

## 8. The cyclic contradiction

Let C_i=Q_(4+i), with indices modulo four, and let

    B_0=Q9, B_1=Q10, B_2=Q11, B_3=Q8.

Define w_i to be the x-coordinate, relative to (2,2), of the center of the actual B_i in the chart R^(-i). The preceding actual boundary L_i is B_(i-1) viewed after one additional inverse quarter turn. Its y-coordinate in the current chart is therefore exactly -w_(i-1). The preceding section proves

    w_i-w_(i-1)>0

for every i. The literal coordinate cancellation is

| Current central | Current xB | Preceding yL |
|---|---|---|
| Q4 | X_Q9-2 | Y_Q8-2 |
| Q5 | Y_Q10-2 | 2-X_Q9 |
| Q6 | 2-X_Q11 | 2-Y_Q10 |
| Q7 | 2-Y_Q8 | X_Q11-2 |

Adding the four strict inequalities yields 0>0. This contradiction proves that the entire all-positive no-omission OOOO family is empty, for every pattern of retained and omitted forward points.

Together with the independently completed nonpositive and mixed-sign chapters recorded in C1092-MPPM-CENTRAL-SIGN-REDUCTION.md, this closes the full OOOO branch. The proof uses actual common faces and actual wall centers throughout; no terminal center history or finite angular search is an additional premise.
