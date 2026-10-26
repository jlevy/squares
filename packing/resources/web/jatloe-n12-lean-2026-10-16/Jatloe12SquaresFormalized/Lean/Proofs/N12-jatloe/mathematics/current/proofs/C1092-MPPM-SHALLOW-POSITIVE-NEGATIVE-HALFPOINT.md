# C1092 MPPM: a shallow positive owner before a negative successor receives its halfpoint

All terminating decimals are exact rationals. Ownership is strict in an actual open square; exclusion and separation permit equality. The local argument uses common side a>1. Its actual application retains the original no-omission OOOO entrance and 1<a<=1.001.

## 1. A two-square support obstruction

Use coordinates centered at (2,2). Let C have positive canonical frame u=(c,s),v=(-s,c), c>=s>0, and lower faces U,V, upper faces A=U+a,H=V+a. Suppose C strictly owns its southwest marker M=(-.35,-.35) and forward point T=(-.26,0), and

    U>=-c-.5s, H<=s,
    0<x=s/(1+c)<=1/4.                             (1)

Let E have negative canonical frame e=(d,-t),f=(t,d), d>=t>0, with lower faces L,K and upper faces J=L+a,D=K+a. Suppose E strictly owns M_E=(.35,-.35), B0=(.26,-1), and

    J<=d+t, K>=-1.086d, D<=t-.56d,
    .7<d<.825, .566<t<.71, d+t>1.39.              (2)

**Theorem 1.** These two actual squares cannot have disjoint open interiors.

The precise local C/E source analysis in Sections 4–5 of C1092-MPPM-FLANKED-POSITIVE-HALFPOINT.md applies under exactly (1),(2). We spell out its dependency scope: those two sections use only the strict markers, T,B0, U>=-c-.5s, H<=s, the E faces (2), and the weaker ceiling x<=1/3. They do not use the predecessor W, its upper cap on C, a preceding origin, V>=.4s-c, or A<=0.

The complete normal cone consequently leaves u,-v,e. With

    k=cd-st>=0, ell=ct+sd>0,

the arguments in those two sections exclude u and -v with positive margins at least .17 and 49/5000, respectively. Those margins cover the present smaller angle interval including x=1/4. The only remaining actual source is e, and we now supply its new estimate using H<=s in place of a predecessor cap.

Its exact support difference is

    upper_C(e)-lower_E(e)
       =kA+ell(a-H)-L
       >=k(a-c-.5s)+ell(a-s)-(d+t-a).

The coefficient of a is 1+k+ell>0. Hence a>1 gives the strict lower bound

    F=1-Pd-Qt,
    P=2-c-s+.5cs,
    Q=1-c+s-.5s^2.                               (3)

Express the coefficients using the half-angle x:

    P=1-s(1-c/2-x),
    Q=s(1+x-s/2).

On 0<=x<=1/4, the first bracket decreases. Its derivative is

    2x/(1+x^2)^2-1<=-1/2,

and its value at x=1/4, c=15/17, is 21/68. The extra part of the second bracket is

    x-s/2=x^3/(1+x^2),

which increases on this interval and equals 1/68 at its right endpoint. Therefore

    P<=1-(21/68)s, Q<=(69/68)s.                   (4)

These two upper coefficients are nonnegative. Since s<=8/17, their exact squared-norm deficit is

    1-[1-(21/68)s]^2-[(69/68)s]^2
       =s[21/34-(2601/2312)s]
       >=(3/34)s>0.                              (5)

The endpoint simplification uses

    (2601/2312)(8/17)=9/17.

Cauchy's inequality and d^2+t^2=1 imply Pd+Qt<1. Thus F>0, and the last actual normal e also fails. This proves Theorem 1. The strictness at x=1/4 is explicit in (5); no limiting contact or numerical angle subdivision is omitted.

## 2. Actual halfpoint and origin before a missing negative successor

**Corollary 2.** In OOOO, suppose C=Q4 is positive, owns its forward G3, and has half-angle at most 1/4. If its actual ordinary successor E=Q5 is negative and omits its own forward F4, then C strictly owns (1,1.5), and actual Q9 strictly owns (2,1).

Suppose the local outer halfpoint H_out=(-1,-.5) were omitted from C. The exhaustive face proof in Section 8 of C1092-MPPM-FLANKED-POSITIVE-HALFPOINT.md uses only C's actual G0, marker and forward G3, together with the genuine foreign northwest marker. It gives U>=-c-.5s. In particular that local argument neither assumes a sign for the northwest square nor assigns H_out to another square.

The positive-forward D theorem gives H<=s. For the actual negative missing-forward successor, the literal E column of Section 7 of that same chapter supplies every face, marker and range in (2): its strict ordinary points are G5,F6, its missing forward is F4, its outer halfpoint comes from its own omission, its lower marker is actual Q9's marker, its corner is actual Q1, and its whole excluded right bar belongs to Q10. No bottom origin is required for that profile. Thus Theorem 1 contradicts actual disjointness and proves H_out strict in C.

The paired-corner transfer is then exactly Theorem 7 of C1092-DIRECT-WALL-POINT.md, with Q0,Q9, b=.914 and ell=1.6. Its strict corner anchors are (1,.914),(1,1), its strict bottom anchors are (2,.914),F2=(1.6,1), and its excluded corner-halfpoint is the point just proved in C. This yields Q9(2,1) strictly. All wall hypotheses are the original actual container walls.

## 3. A negative successor that retains its forward point

For completeness, suppose instead the same actual negative E strictly owns its forward I=(0,-.26). Its ordinary point B0=(.26,-1) and I put its own inner crosspoint E'=(0,-.5) strictly inside E, by all four exact bands:

    e(E')-e(I)=.24t>=0,
    e(B0)-e(E')=.26d+.5t>0,
    f(E')-f(B0)=.5d-.26t>=.24d>0,
    f(I)-f(E')=.24d>0.

An equality in the first increment still retains a strict band from I. Thus this argument also includes the axial nonpositive representative t=0.

Theorem 3 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md now applies to the actual C and its foreign E', because x<=1/4<1/3. It gives the same outer halfpoint in C and next wall origin. Consequently the conclusion of Corollary 2 holds for every nonpositive successor, regardless of that successor's own forward membership. In the missing-forward alternative, the actual missing-negative profile already excludes its axial angle.

All arguments rotate simultaneously with the actual owners. This chapter establishes the required strict points; it does not by itself assert a cyclic contradiction.
