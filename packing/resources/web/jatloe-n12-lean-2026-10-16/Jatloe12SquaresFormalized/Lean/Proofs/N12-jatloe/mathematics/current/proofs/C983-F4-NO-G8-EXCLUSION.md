# C983: the F4-only merged owner forces the southeast outer auxiliary

Every terminating decimal is an exact rational. All owned points are strictly interior to their actual open square. All excluded points and separating supports may be tangent. This chapter proves a complete branch exclusion, using full square supports for every orientation; it uses no samples or enumeration of joint ownership vectors.

## 1. Exact actual entrance

Suppose the actual merged western owner Q7 has label8208={F4,G3}, and suppose the actual southeast owner Q5 excludes G8=(3,1.6).

Because F4 belongs to Q7, every available original Q5 component avoiding F4 owns F8, as checked in `C983-F4-POINT-TRANSFERS.md`, Section3. Every such Q5 component that also avoids G8 owns G6. Equivalently, inspection of the original Q5 component list after deleting F4 and G8 leaves

    65792, 65824, 66304, 590592, 66336,

each of which contains F8,G6. Extra auxiliaries in these components will not be changed into exclusions in this proof.

Translate coordinates by (−2,−2), and denote these same actual squares by W=Q7 and E=Q5. The strict anchors in W include

    P=(−.35,−.35), Q=(−.35,.35),
    F=(0,−.26), D_W=(−.26,0), K=(−.05,−.05).          (1)

The first four points are its original markers and F4,G3. The point K follows from Theorem A of `MERGED-RIGHT-PATTERN-4.md`. Its four excluded points, before translation, are (1,1.65),(1,1.74) in actual singleton Q1 and (1.74,1),(1.65,1) in actual singleton Q0. Both singleton segments are strict in their respective actual owners, so the theorem applies to this merged square without splitting its two markers.

The following points are excluded from W:

    F_+=(0,.26), L=(−1,.26), J=(−1,−.4).              (2)

Here F_+ is its omitted F5, L is F1 strictly in actual Q8, and J is G0 strictly in actual Q1. An omitted auxiliary is an exclusion even if it has no other owner; L and J in fact have the displayed genuine strict owners.

The three strict anchors of E are

    M=(.35,−.35), D=(.26,0), A=(1,−.26).              (3)

The first elbow theorem in `ELBOW-CROSSPOINT.md` applies to this actual E: its excluded northeast marker belongs to actual Q6; G8 is absent by supposition; and the excluded right-wall marker belongs to actual Q10. It proves that E has a strictly negative canonical frame

    u_E=(c,−s), v_E=(s,c), c≥s>0, c²+s²=1,

and gives the weak upper face bounds

    U_E+a≤c+.4s, V_E+a≤.35(c+s),                     (4)

together with the strict point

    C=(0,−.5)∈E.                                     (5)

Section4 of `C983-F4-POINT-TRANSFERS.md` uses the genuinely excluded F4 in W to strengthen this to

    0<s/(1+c)<7/50, s<7/25, c>24/25.                (6)

Theorem1 of that same chapter also gives

    X=(.5,0)∈E.                                      (7)

Its additional excluded point (2.5,1), in original coordinates, lies in the strict actual Q9 bar [2.26,2.8]×{1}. The bar's genuine Q0, marker, and bottom-wall sources are recorded there. Thus (5) and (7) are strict points of E, and neither is assigned to W.

Write A_E=U_E+a and H_E=V_E+a. The exact increasing function c+.4s on the interval (6) gives

    U_E<c+.4s−1<182/2549,
    H_E>.5s.                                        (8)

Indeed, its derivative with respect to the positive angle is .4c−s>.4(.96)−.28>0. At half-angle7/50 its components are c=2451/2549, s=700/2549, and c+.4s−1=182/2549. The second inequality in (8) is strict ownership of X.

## 2. The exhaustive separating directions

Since W and E are disjoint open squares, the separating-axis theorem gives a separating normal among their actual edge normals. Orient that normal n from W toward E, so

    upper_W(n)≤lower_E(n).                            (9)

Strict ownership of the horizontally aligned P∈W and M∈E gives n_x>0. Strict ownership of F=(0,−.26)∈W and C=(0,−.5)∈E gives n_y<0.

If W has a nonnegative canonical frame u_W=(d,r), v_W=(−r,d), d≥r≥0, the only candidate directions are −v_W=(r,−d) and u_E=(c,−s). If W has a nonpositive canonical frame u_W=(d,−r), v_W=(r,d), the only candidates are u_W and u_E. A candidate that lies on the boundary of the strict cone may be retained; this only enlarges the list that will be excluded. In particular all axial and diagonal representatives are covered.

## 3. A nonnegative W cannot separate by its own normal

Use u_W=(d,r), v_W=(−r,d). Denote W's lower faces by U,V and its upper faces by A_W=U+a,H_W=V+a. Strict ownership of P gives

    −V>.35(d−r).                                     (10)

For n=−v_W=(r,−d), its components in E's frame are

    α=cr+sd>0, β=sr−cd<0.

The second sign follows from (6): the sum of the two canonical angle magnitudes is less than π/4+2atan(7/50)<π/2. The lower support of the full E square is therefore

    lower_E(n)=αU_E+βH_E.

Using (8), its difference from .35(d−r) is strictly less than

    r A_0+d B_0,

where

    A_0=1.35−c−.5s²+.4cs>0,
    B_0=.5cs+.4s²−s−.35.

Since r≤d, this is at most d(A_0+B_0). The exact sum is

    A_0+B_0=1−c−s−.1s²+.9cs.

Here 1−c=s²/(1+c)<.511s² by c>.96, and c≤1−s²/2. Consequently

    A_0+B_0<s[−.1+.411s−.45s²]<0.                    (11)

For the last sign, the bracket is increasing on 0≤s≤.28, and its value at .28 is −101/5000. Thus lower_E(n)<.35(d−r)<−V=upper_W(n), contradicting (9). This excludes this full direction for every nonnegative W angle.

## 4. A nonnegative W cannot separate by the E normal

Continue with the same W frame. Its actual exclusion of C=(0,−.5), strictly in E, forces C to leave through the lower v_W face. Its lower u_W band follows from P, and its upper bands follow from F, with positive increments .35d−.15r, .24r and .24d; a zero .24r increment still gives a strict band through the strict anchor F. Hence

    V≥−.5d.                                         (12)

The excluded F_+=(0,.26) has its two lower bands from F and its upper v_W band from Q. Thus F_+ leaves through the upper u_W face:

    A_W≤.26r.                                       (13)

At L=(−1,.26), its upper u_W band follows from F, and its lower v_W band follows from P. If L were lower u_W, (13) would give a≤d≤1. Therefore it is upper v_W:

    H_W≤r+.26d.                                     (14)

Combining (12),(14) and a>1 gives 1<r+.76d. For the half-angle t=r/(1+d),

    r+.76d−1=2(1−t)(22t−3)/(25(1+t²)).

Therefore

    t>3/22,
    r>132/493>.26.                                  (15)

Set k=cd−sr>0 and h=cr+sd>0. The upper W-support in direction u_E is

    upper_W(u_E)=kA_W−hV.

The cap (14) gives V<r+.26d−1. We divide the W angle into two closed intervals to give elementary uniform lower bounds.

### 4.1. The interval r/d≤3/4

Use strict K in (1), which gives A_W>−.05(d+r). Then

    upper_W(u_E)−U_E>1+c(A_1−1)+sB_1,               (16)

where the exact expanded coefficients are

    A_1=r−.05d²−r²−.31dr,
    B_1=d−.26d²+.05r²−.95dr−.4.

Throughout this interval .26<r≤.6 and .8≤d<1. In particular

    A_1≥.69r−.95r²−.05≥.022>0,
    A_1≤r<1.                                        (17)

The quadratic lower bound is concave; its two endpoint values at r=.26 and r=.6 are .06518 and .022. Since c≤1, the right side of (16) is at least A_1+sB_1. If B_1≥0 this is positive by (17). If B_1<0, (6) gives

    A_1+sB_1>A_1+.28B_1=f(p),                        (18)

where p is W's positive angle and

    f(p)=r+.28d−.6664+.4316cos(2p)−.288sin(2p).

This function is strictly concave on

    2atan(3/22)≤p≤atan(3/4).

Here is an explicit continuous check. Its third derivative is

    f'''(p)=−d+.28r+3.4528sin(2p)+2.304cos(2p)>0.

Indeed d≤1, r≥.26, sin(2p)=2dr≥.416 and cos(2p)≥.28 already give a positive lower bound. Hence f'' is increasing. At the upper endpoint, where d=.8,r=.6, its value is

    f''=−r−.28d−1.7264cos(2p)+1.152sin(2p)
       =−.201472<0.

Thus f''<0 on the whole interval. The two exact endpoint values of f are

    f(2atan(3/22))=11210749/121524500>0,
    f(atan(3/4))=123/62500>0.                         (19)

Concavity puts f above the chord joining those positive endpoint values. Equations (16)–(19) show upper_W(u_E)>U_E throughout this entire interval.

### 4.2. The interval r/d≥3/4

Use Q in (1), which gives A_W>.35(r−d). The corresponding exact expansion is

    upper_W(u_E)−U_E>1+c(A_2−1)+sB_2,               (20)

with

    A_2=r−r²−.35d²+.09dr,
    B_2=d−.26d²−.35r²−.65dr−.4.

Now .6≤r≤1/sqrt(2), 1/sqrt(2)≤d≤.8, and dr≥.48. Therefore

    .0592≤A_2<1,
    −.33<B_2≤−.172.                                 (21)

For the first lower bound, rewrite A_2=r−.35−.65r²+.09dr. The expression r−.65r² increases for .6≤r≤1/sqrt(2)<5/7, and dr≥.48, so A_2≥.6−.35−.65(.6)²+.09(.48)=.0592. The upper bound A_2<1 follows already from A_2≤r<1. For the lower bound on B_2, write it as d+.09d²−.75−.65dr and use d>.7,d²≥.5,dr≤.5. For the upper bound use d≤.8, .26d²+.35r²≥.26 and dr≥.48.

Cauchy–Schwarz now gives the uniform lower bound

    1+c(A_2−1)+sB_2
       ≥1−sqrt((1−A_2)²+B_2²)
       >1−sqrt(.9408²+.33²)>0.                      (22)

The final exact squared margin is

    1−.9408²−.33²=37471/6250000>0.

This excludes the E normal on the second interval as well. Together with Section3 it excludes every possible separator when W has a nonnegative canonical angle.

## 5. A nonpositive W cannot have r≤.39

Use instead u_W=(d,−r), v_W=(r,d), with d≥r≥0 and d²+r²=1. At the excluded F_+=(0,.26), both u_W bands and the lower v_W band follow from the strict anchors Q,F,P. Thus

    H_W≤.26d.                                       (23)

At C=(0,−.5), its lower u_W band follows from F and its upper v_W band follows from F. A lower v_W exclusion, together with (23), would give a≤.76d<1. Its only remaining exit is upper u_W:

    A_W≤.5r.                                        (24)

Strict Q and (23) also imply

    .35(d−r)<.26d, hence r/d>9/35.                  (25)

Suppose r≤.39. At J=(−1,−.4), both upper bands follow from P, with increments .65d−.05r>0 and .65r+.05d>0. Its lower v_W band follows strictly from (23), since

    H_W−v_W(J)≤.66d+r
       ≤.66+r−.33r²
       ≤999807/1000000<1<a.                         (26)

The middle bound uses d≤1−r²/2; the following quadratic is increasing on 0≤r≤.39. Consequently J is lower u_W, U≥−d+.4r. Combining this with (24) gives

    1<a≤d+.1r.

Its exact half-angle identity forces 0<r/(1+d)<.1. It follows that r/d<20/99<9/35, contradicting (25). This excludes the entire interval r≤.39, including its endpoint and the axis.

## 6. Both actual normals fail when W is nonpositive and r>.39

It remains to consider r>.39. Let p,q be the positive magnitudes of the W and E angles, respectively. By (6), s<.28<r, so p>q. Put

    k=cos(p−q)=cd+sr>0,
    h=sin(p−q)=cr−sd>0.

For n=u_E, the full W-support is

    upper_W(u_E)=kA_W+hH_W.

Strict F,Q give A_W>.26r and H_W>.35(d−r)≥0. Moreover k≥d≥1/sqrt(2)>707/1000. Thus

    upper_W(u_E)>.26(.39)(.707)>182/2549>U_E.        (27)

The exact margin in the middle comparison is

    .26(.39)(.707)−182/2549
       =3686501/12745000000>0.

The E normal therefore cannot satisfy (9).

For n=u_W, the full lower E-support is

    lower_E(u_W)=kU_E−hH_E<182/2549,

by (8), k≤1 and H_E>0. But its required upper W-support is

    upper_W(u_W)=A_W>.26r>.26(.39)>182/2549.         (28)

This is the opposite strict inequality to separation. It excludes the other actual normal. The negative canonical sign is now exhausted.

## 7. Proven ownership consequence and remaining scope

Every possible canonical sign and every separating edge normal of the two actual squares W,E has been excluded. Therefore the supposition in Section1 is impossible:

    Q7=8208  ⇒  G8=(3,1.6) belongs strictly to Q5.

The conclusion is derived from the original component list and actual continuous square geometry. It does not presume a label for Q6, Q10 or Q11, beyond their original markers and the universal wall/auxiliary facts explicitly used above. Every extra point in the preliminary Q5 component list was retained as an owned point, never repurposed as an exclusion.

This chapter closes the entire no-G8 southeast subbranch under merged label8208. It does not yet exclude every configuration having merged label8208, nor the other two remaining merged labels8224 and8240.
