# C1092 MPPM: exact three-square support reduction for a missing crosspoint

This chapter proves the geometric reduction, including all actual separating-axis sources and the literal original-owner ledger. The four scalar expressions are those defined in C1092-MPPM-STEEP-POSITIVE-BOUNDARY-SCALARS.md. No scalar positivity not yet proved is assumed in Theorem 1 below.

All decimals are exact rationals. Every square is open with side a>1. A strict point belongs to its interior, and disjointness means disjoint interiors; closures may touch. A real wall constrains the closure of the whole square.

## 1. Local theorem

**Theorem 1.** Let C,E,B be actual squares of the same side a>1, with B disjoint from both C and E. Suppose C has positive canonical frame

    u=(c,s), v=(-s,c), c=cos p,s=sin p,
    2 atan(1/3)<=p<=pi/4,

lower faces U,V and upper faces A=U+a,K=V+a, and satisfies

    U>=-c-s, A<=-.5c, K<=1.086s.                  (1)

Suppose C strictly owns M=(-.35,-.35), P=(-1,-.26). Suppose E has nonnegative canonical frame

    e=(d,t), f=(-t,d), d=cos q,t=sin q,
    0<=q<=pi/4,

lower faces L,Q and upper faces J=L+a,D=Q+a, and satisfies

    J<=d-.56t.                                    (2)

Suppose E strictly owns B1=(.4,-1), Y=(0,-.5). Finally suppose B strictly owns

    B0=(0,-1.086), F2=(-.4,-1), O=(0,-1),         (3)

and its closure lies in y>=-2. Then, for the actual orientation beta of B defined below, at least one of the four expressions G00,G01,G10,G11 is strictly negative.

Thus simultaneous nonnegativity of those four explicit scalar expressions rules out this local configuration. The theorem itself is an exact necessary consequence of the actual squares; it does not require replacing them by independently chosen hulls or sampled poses.

## 2. Complete normal cones

Orient a possible separator from B toward C. The two strict anchor comparisons P-B0=(-1,.826) and M-F2=(.05,.65) force

    -nx+.826ny>0, .05nx+.65ny>0,
    ny>0, nx<.826ny.                              (4)

The only signed C face normal in this cone is v=(-s,c). The positive normal u has nx/ny=c/s>=1, while the other two C normals point downward.

Any northeast normal n=(xi,eta), xi,eta>=0, in (4) cannot separate B and C. Indeed eta>0, and

    lambda=c xi+s eta>0, mu=c eta-s xi>0.

Using A<=-.5c<=-.26c, K<=1.086s and a>1,

    lower_C(n)-n·F2
       <xi[-c+s+.14-.826s^2]
             +eta[1-c-s+.826cs]<0.                 (5)

The first coefficient is increasing with p because its derivative c+s-1.652cs is positive; at pi/4 it equals -.273. The second is strictly negative because

    c+s-1=2cs/(1+c+s)>.826cs.                     (6)

The exact constant comparison is 2/(1+sqrt(2))>.826. Since F2 is strict in B, (5) implies lower_C(n)<upper_B(n), precluding separation. This includes a vertical northeast endpoint.

Now orient a separator from B toward E. The strict comparisons B1-O=(.4,0) and Y-O=(0,.5) force

    nx>0, ny>0.                                  (7)

The only possible signed E face normal in this cone is e=(d,t). The coordinate-axis case t=0 does not belong to (7), so that source would already be unavailable there.

For the actual B, choose one of its perpendicular side directions in the closed first quadrant, and write

    b=(h,r)=(cos beta,sin beta),
    w=(-r,h), 0<=beta<=pi/2.                       (8)

Every square orientation admits this representation, including both signs of its usual canonical angle. Its sole northeast normal is b and its sole northwest normal is w, with any duplicate coordinate representatives treated by the closed endpoints. The separating-axis theorem for the closures, including a weak supporting equality, now leaves the following exhaustive sources:

| Pair | Possible actual normal |
|---|---|
| B toward C | v or w |
| B toward E | e or b |

A listed endpoint that fails the strict cone (4) or (7) is simply unavailable. Allowing it in the subsequent scalar calculation only enlarges the alternatives.

## 3. The central support caps, with the actual side retained

Use the notation kC,deltaC,kE,deltaE of (1) in the scalar chapter. Its quantities C0,E0,FC,FE are defined at unit side solely to simplify the final scalar expressions. The actual-side caps are

    lower_C(v)<=C0-(a-1),
    lower_E(e)<=E0-(a-1),                         (9)

and

    lower_C(w)<=FC-(a-1)(kC+|deltaC|),
    lower_E(b)<=FE-(a-1)kE.                       (10)

Here is the complete signed-face verification of (10). Since w·u=-deltaC and w·v=kC>0, if deltaC>=0 then

    lower_C(w)=-deltaC A+kC(K-a)
       <=deltaC(c+s)+kC alpha s-a(kC+deltaC),      (11)

using A>=a-c-s from (1). If deltaC<=0, instead

    lower_C(w)=-deltaC(A-a)+kC(K-a)
       <=.5c deltaC+kC alpha s-a(kC-deltaC).       (12)

Both expressions agree at deltaC=0. These are exactly the first cap in (10).

For E, the coefficients of b in the e,f frame are kE>=0 and deltaE. If deltaE>=0, strict B1 gives Q<-d-.4t, so

    lower_E(b)=kE L+deltaE Q
       <=kE(d-.56t-a)+deltaE(-d-.4t).             (13)

If deltaE<=0, strict Y gives D>-.5d, so

    lower_E(b)=kE L+deltaE D
       <=kE(d-.56t-a)-.5d deltaE.                 (14)

This proves the second cap in (10), including the weak zero-coefficient cases. The proof retains each actual upper or lower face according to the coefficient sign. It makes no independent change of the same face between the two actual supports.

## 4. Eliminate the same actual boundary center

Let (xB,yB) be the center of B. Its unit-side vertical width is h+r, so its real bottom wall yields

    yB>=-2+(a/2)(h+r).                            (15)

For every upward unit normal n, if omegaB(n) is its unit-side projection width, (15) gives

    upper_B(n)>=nx xB-2ny
                       +(a/2)[ny(h+r)+omegaB(n)]. (16)

Suppose the chosen actual separator toward C is m in {v,w}, and the chosen one toward E is n in {e,b}. Put

    Delta=nx my-mx ny.

The selected cones give -mx>=0, nx>=0, and the explicit directions have Delta>0. Multiply the C separation by nx and the E separation by -mx. The xB terms in (16) cancel exactly. The resulting necessary inequality is

    (a/2)[Delta(h+r)+nx omegaB(m)-mx omegaB(n)]
       -2Delta-nx lower_C(m)+mx lower_E(n)<=0.    (17)

The relevant unit-side widths are

    omegaB(v)=kC+|deltaC|,
    omegaB(e)=kE+|deltaE|,
    omegaB(b)=omegaB(w)=1.                        (18)

Substitute the actual-side support caps (9)--(10) into (17). In each of the four source alternatives its left side is at least

    Gij+(a-1)Hij,                                (19)

where the Gij are exactly (4)--(7) of the scalar chapter and the side coefficients are

    H00=.5[k(h+r)+d(kC+|deltaC|)+s(kE+|deltaE|)]
                       +d+s;

    H01=.5[kC(h+r)+h(kC+|deltaC|)+s]+h+s kE;

    H10=.5[kE(h+r)+d+r(kE+|deltaE|)]
                       +d(kC+|deltaC|)+r;

    H11=h+r+h(kC+|deltaC|)+r kE.                 (20)

Every Hij is strictly positive on the full closed angle domain. For H00 use d,s>0. For H01 its bracket contains the positive s. For H10 its bracket contains the positive d. For H11 use h+r>=1. Thus a>1 makes (19) strictly greater than Gij. The necessary inequality (17) therefore forces its corresponding Gij<0. This proves Theorem 1, with strictness supplied even at a weak face or an aligned scalar endpoint. ∎

## 5. Literal OOOO application

Retain the original no-omission all-four-ordinary MPPM entrance, its twelve actual owners, and the original common side 1<a<=1.001. Suppose Q4 is strictly positive, omits forward G3=(1.74,2), and also omits its crosspoint (1.5,2). Suppose its actual successor Q5 is strictly positive and strictly owns its crosspoint (2,1.5). Translate the entire physical configuration by (-2,-2), without changing any owner.

| Local premise | Actual original source |
|---|---|
| C=Q4 strict M,P | SW marker (1.65,1.65), ordinary F0=(1,1.74) |
| U>=-c-s, K<=1.086s | Unconditional missing-positive profile, C1092-MPPM-MISSING-POSITIVE-WALL-ORDER.md, Lemma 1 |
| A<=-.5c and p>p0 | The three other bands of the hypothetically omitted (1.5,2), established in STEEP-POSITIVE-SUCCESSOR-FAR-CAP, Section 5 |
| E=Q5 strict B1,Y | Ordinary F6=(2.4,1), stated strict crosspoint (2,1.5) |
| Q5 positive cap D<=0 in this common chart | Its own-sector upper-u cap, C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md, Theorem 1, transported by the quarter turn |
| J<=d-.56t | STEEP-POSITIVE-SUCCESSOR-FAR-CAP, Theorem 1, with the same actual Q4 and Q5 |
| Whole foreign right bar needed by that theorem | Convex segment from strict (3,1.44) to G8=(3,1.6) in actual Q10 |
| B=Q9 strict B0,F2 | Original marker (2,.914), original F2=(1.6,1) |
| B strict O | Actual (2,1), supplied by Q4's missing-forward halfpoint and the paired-corner transfer |
| B real floor | Original closure in y>=0 |

The right-bar advance (3,1.44) is the already proved ordinary-wall advance in the same no-omission entrance. The whole segment has one actual owner Q10. Q4's missing-forward halfpoint is (1,1.5); its transfer to the actual Q9 origin is the retained ordinary-central reduction. No preceding origin is presumed and no omitted forward auxiliary is assigned to a different square.

All these premises therefore hold simultaneously for the same three actual squares. Theorem 1 reduces their impossibility precisely to nonnegativity of the four scalar modes. C1092-MPPM-STEEP-POSITIVE-CENTRAL-SCALAR.md proves G00>=1/3125 everywhere, supplying both explicit aligned inputs of the boundary-scalar chapter. That chapter then proves G01,G10,G11>=0. The strictly negative alternative required by Theorem 1 is impossible.

**Corollary 2 (positive crosspoint propagation).** In the retained OOOO entrance, if a strictly positive missing-forward central has a strictly positive successor which owns its local crosspoint, then that missing-forward central also strictly owns its local crosspoint.

**Proof.** Suppose its crosspoint were not strict, allowing a boundary point. Its other three strict bands imply the upper face and strict angle bound in the preceding table. The same actual-square ledger therefore supplies Theorem 1. The four completed scalar inequalities contradict its conclusion. This excludes every non-strict position of the crosspoint and proves the strict ownership claimed. ∎

Simultaneous quarter turns R(x,y)=(4-y,x) preserve this complete ledger. The four strict propagation outputs are

| Missing-forward positive central | Hypothetical missing crosspoint | Strict crosspoint in its positive actual successor |
|---|---|---|
| Q4 | (1.5,2) | (2,1.5) in Q5 |
| Q5 | (2,1.5) | (2.5,2) in Q6 |
| Q6 | (2.5,2) | (2,2.5) in Q7 |
| Q7 | (2,2.5) | (1.5,2) in Q4 |

Each full proof rotates its actual intervening boundary square and its actual foreign far-bar owner at the same time.

**Corollary 3 (all-positive crosspoint cycle).** If all four ordinary central squares are strictly positive and at least one owns its designated forward point, then every central strictly owns its local crosspoint in the displayed table.

**Proof.** A positive forward-owned central has its strict local crosspoint by Theorem 2 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md, without an angle restriction. Move backwards through the four-sector cycle. A forward-owned predecessor has its own unconditional crosspoint. A missing-forward predecessor receives its crosspoint from Corollary 2, with the actual successor just established. At most three such steps supply all four distinct actual owners. No omitted forward auxiliary is reassigned and no central angle bound is added by this propagation argument. ∎

The already proved all-forward-missing cycle excludes the alternative where none is a seed. Consequently any remaining all-positive OOOO configuration has all four strict crosspoints. This chapter does not claim that those four crosspoints alone already give a final OOOO contradiction.
