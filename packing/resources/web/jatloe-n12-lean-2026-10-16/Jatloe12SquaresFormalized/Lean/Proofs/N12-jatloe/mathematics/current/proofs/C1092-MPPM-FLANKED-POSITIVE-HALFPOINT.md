# C1092 MPPM: a positive forward owner between two negative missing owners receives its halfpoint

Every terminating decimal denotes an exact rational. A strict point belongs to the named actual open square. Excluded points and separating faces may meet with equality. The local theorem below concerns three actual squares of common side a>1; it does not replace those squares by their point hulls. The final application retains the original no-omission OOOO entrance and its range 1<a<=1.001.

## 1. Local statement and simultaneous faces

Use southwest coordinates centered at (2,2). Let C have positive canonical frame

    u=(c,s), v=(-s,c), c>=s>0, c^2+s^2=1,

with lower faces U,V and upper faces A=U+a,H=V+a. Suppose it strictly owns

    M=(-.35,-.35), P=(-1,-.26), T=(-.26,0),

and satisfies the simultaneous bounds

    U>=-c-.5s, V>=.4s-c, H<=s,
    x=s/(1+c)<=3/10.                               (1)

Let its actual predecessor W have negative canonical frame

    w=(b,-r), z=(r,b), b>=r>0, b^2+r^2=1,

with lower faces L_W,K_W and upper faces J_W,D_W. Suppose W strictly owns M_W=(-.35,.35), and

    L_W>=-b-r, J_W<=-.26r, D_W<=1.086b,
    .7<b<.825, .566<r<.71, br>.46.                (2)

Let its actual successor E have negative canonical frame

    e=(d,-t), f=(t,d), d>=t>0, d^2+t^2=1,

with lower faces L_E,K_E and upper faces J_E,D_E. Suppose E strictly owns

    M_E=(.35,-.35), B0=(.26,-1),

and

    J_E<=d+t, K_E>=-1.086d, D_E<=t-.56d,
    .7<d<.825, .566<t<.71, d+t>1.39.              (3)

**Theorem 1.** Three pairwise disjoint actual open squares C,W,E cannot satisfy these hypotheses.

The bounds involving W and E are the actual missing-forward profiles. The first lower face in (1) will come from a supposed omission of C's outer halfpoint. No upper-u cap A<=0 or ownership of either adjacent wall origin is a hypothesis of the local theorem.

## 2. The complete C-to-W normal list

Direct a separating normal from C toward W. The two strict markers force n_y>0. The strict pair P,M_W also gives

    .65 n_x+.61 n_y>0.                            (4)

The upward northwest normal -w=(-b,r) fails (4), because -.65b+.61r<=-.04b<0. All downward normals fail n_y>0. Consequently the separating-axis theorem leaves exactly the possible sources

    u=(c,s), v=(-s,c), z=(r,b).                   (5)

A source may itself fail the strict cone at an endpoint; retaining it for exclusion is harmless. Put

    k=cb-sr=cos(p+phi), ell=cr+sb=sin(p+phi),

where p,phi are the nonnegative angle magnitudes. Then

    u=k w+ell z, v=-ell w+k z, z=ell u+k v.

The ceiling in (1) gives

    c>=91/109, s<=60/109, c-s>=31/109.

Since phi<=pi/4,

    k>=cos(p+pi/4)=(c-s)/sqrt(2)>1/5.             (6)

The last strict comparison is the exact integer inequality 155^2>2(109^2). Also 0<ell<=1.

## 3. W forces a strict upper transverse cap on C

### 3.1. C's northeast normal

For this source we may weaken D_W<=1.086b to D_W<=1.1b. The strict point T gives A>-.26c, while

    lower_W(u)=k L_W+ell K_W
       <=k(-.26r-a)+ell(1.1b-a).

Their support gap is strictly greater, after lowering a to 1 in its positive coefficient k+ell, than

    F_u=c P+s Q,
    P=b+r-.26-.84br,
    Q=b-r-.26r^2-1.1b^2.                         (7)

Here Q<.259-.55<0. Since s<=c,

    F_u>=c(P+Q),
    P+Q=2b-.52-.84b(b+r).

The derivative of the last expression with respect to phi is

    -2r-.84(b^2-r^2-2br)<=-2r+.84<-.292.

Its minimum on the allowed interval is therefore its diagonal value

    P+Q>=sqrt(2)-1.36>.054>0.

The final rational comparison follows from 1.414^2<2. Thus u cannot separate the actual squares.

### 3.2. W's northeast normal

The two lower faces in (1) give

    A>=a-c-.5s, H>=a+.4s-c.

Hence

    upper_C(z)-lower_W(z)
       >=ell(a-c-.5s)+k(a+.4s-c)-(1.086b-a).

Its coefficient of a is 1+k+ell>0. Lowering a to 1 leaves the strict lower bound

    F_z=1-1.086b+ell(1-c-.5s)+k(1-c+.4s).         (8)

We have 1-c-.5s=s(x-.5)<0, so ell<=1 bounds its ell term from below. The other bracket is positive, and (6) therefore gives

    F_z>2081/20000+1.2(1-c)-.42s
        >=2081/20000+1-c-.42s.

Cauchy's inequality and the exact squared comparison

    c+.42s<=sqrt(1+.42^2)<217/200

give the explicit margin

    F_z>381/20000>0.                              (9)

Thus W's source z is also impossible. The simultaneous use of the two actual C faces in (8) is essential.

### 3.3. The surviving source and its cap

Only v remains in (5). Its exact lower W support is

    lower_W(v)=-ell J_W+k K_W.

Use J_W>=a-b-r and K_W<=1.1b-a. Since a>1 and k+ell>0, a possible separation would force

    H<=lower_W(v)<c f_0+s g_0,                    (10)

where exact expansion gives

    f_0=1+br-b-r+.1b^2,
    g_0=b^2-b+r-.1br.

On the full canonical interval,

    1+br-b-r=(b+r-1)^2/2<=1.5-sqrt(2)<.086.

As b^2<.825^2<.681, this gives f_0<.1541<.155. The function b^2-b+r has derivative b+r-2br>0 and diagonal value 1/2. Thus br>.46 gives

    g_0<=.5-.1br<.454.

The same actual C therefore satisfies the strict cap

    H<.155c+.454s.                                (11)

## 4. The complete C-to-E normal list

Direct a proposed separating normal from C toward E. The strict markers imply n_x>0. The strict pair T,B0 gives

    .52 n_x-n_y>0.                               (12)

The actual E normal f=(t,d) cannot satisfy (12), because d>=t>0. All normals with nonpositive horizontal component also fail. The separating-axis theorem consequently leaves only

    u=(c,s), -v=(s,-c), e=(d,-t).                (13)

Put, for this different pair,

    k=cd-st=cos(p+q)>=0,
    ell=ct+sd=sin(p+q)>0.

Thus u=k e+ell f, -v=ell e-k f, and e=k u-ell v. The formulas below retain these actual vertex choices. In fact (1) makes k>1/5 just as in (6), although its nonnegativity suffices in the ensuing estimates.

## 5. C cannot supply either normal in (13)

### 5.1. Its northeast normal u

From (1),(3),

    A>=a-c-.5s,
    L_E<=d+t-a, K_E<=t-.56d-a.

The support excess A-lower_E(u) is therefore bounded below by an expression with positive a-coefficient 1+k+ell. After decreasing a to 1, its strict lower bound is

    F_u=1-P_u c-Q_u s,
    P_u=2-d-t+.44dt,
    Q_u=-.5+t-d+.44d^2.                           (14)

Since d+t>1.39 and dt<=1/2, P_u<.83. Also Q_u<0, using t<=d and d^2<=1. Hence

    F_u>1-.83c>=.17>0.

This excludes u.

### 5.2. Its southeast normal -v

Here upper_C(-v)=a-H>=a-s. The actual E support satisfies

    lower_E(-v)=ell L_E-k D_E
       <=ell(d+t-a)-k(a-1.086d).

The a-coefficient of their support difference is again 1+k+ell>0. Its strict lower bound at a=1 is

    F_v=1-P_v c-Q_v s,
    P_v=1+dt-d-t+.086d^2,
    Q_v=1-d+t+d^2-.086dt.                         (15)

As above, 1+dt-d-t<.086 and d^2<.681, so P_v<.145. The derivative of Q_v with respect to q is

    d+t-2dt-.086(d^2-t^2)>1.39-1-.086>0.

Consequently Q_v is at most its diagonal value 1.457. The function

    .145 cos p+1.457 sin p

is increasing on the slightly wider interval 0<=p<=2 arctan(1/3): its derivative is at least 1.457(.8)-.145(.6)>0. At that endpoint it equals .9902. Thus throughout the range (1),

    F_v>49/5000>0.                                (16)

This excludes -v, with the axial C endpoint of the scalar estimate retained.

## 6. E's remaining normal contradicts the predecessor cap

Use the same lower face A>=a-c-.5s and the genuinely coupled upper cap (11). The exact upper C support is

    upper_C(e)=k A-ell V=k A+ell(a-H).

Its difference from lower_E(e)=L_E<=d+t-a has positive a-coefficient 1+k+ell. By a>1 and (11), it is strictly greater than

    F_e=1-Pd-Qt,                                  (17)

where exact expansion gives

    P=2-c-s-.546s^2+.655cs,
    Q=1-c+s+.155c^2-.5s^2-.546cs.                 (18)

The ceiling in (1) gives c>=91/109>5/6 and

    1-c=s^2/(1+c)<=.545s^2.

Rearranging (18) therefore yields the simultaneous bounds

    P=1+(1-c)-s(1-.655c)-.546s^2
       <=1-.345s,

    Q=.155+(1-c)+s(1-.546c)-.655s^2
       <=.155+.545s.                              (19)

The last comparison uses c>5/6, so 1-.546c<.545. No sign of P or Q is presumed when passing to these upper bounds; d,t are positive.

If 0<s<=.1, equations (3),(19) give

    Pd+Qt<.825+.2095(.71)=.973745,
    F_e>5251/200000>0.                            (20)

If .1<=s<=60/109<.6, the two positive upper coefficients in (19) have squared norm strictly below 1. The exact deficit is

    G(s)=1-(1-.345s)^2-(.155+.545s)^2
        =[-961+20842s-16642s^2]/40000.             (21)

This quadratic is concave. Its values at the endpoints of the wider closed interval [.1,.6] are

    G(.1)=47839/2000000>0,
    G(.6)=138827/1000000>0.

Hence G>0 on that entire interval. Cauchy's inequality with d^2+t^2=1 then makes F_e>0 in (17). Both ranges include their shared endpoint. E's last possible normal is impossible as well.

All actual normal sources in (13) have failed, after the complete source reduction for W. Every replacement of a by 1 used a strictly positive coefficient. This proves Theorem 1, including all weak face and support contacts.

## 7. The actual three-owner entrance

Retain OOOO and normalize C=Q4. Suppose C is positive and owns its forward G3, while both actual neighboring ordinary squares W=Q7 and E=Q5 have negative canonical angles and omit their own forward points F5 and F4 respectively.

Corollary 3 of C1092-MPPM-NEGATIVE-MISSING-POSITIVE-CEILING.md applies to the actual pair W,C and gives

    x<7/24<3/10.                                  (22)

Its premises do not require any wall origin or any backward-inner exclusion. For C, the reviewed positive-forward D theorem gives precisely V>=.4s-c and H<=s, and its strict M,P,T are the original marker,F0,G3.

For both missing neighbors, apply Lemma 1 of C1092-MPPM-MISSING-NEGATIVE-WALL-ORDER.md in the neighbor's own southwest chart. Its actual lower corner face V>=-c-s is retained together with its three displayed caps. The literal strict or excluded inputs are:

| Local input of the missing-negative lemma | Present W=Q7 datum | Present E=Q5 datum |
|---|---|---|
| Ordinary marker | (-.35,.35), Q7 marker | (.35,-.35), Q5 marker |
| Ordinary P,G pair | (-.26,1),(-.4,1), G4,F3 | (.26,-1),(.4,-1), G5,F6 |
| Ordinary outer halfpoint | (-.5,1), strict from Q7's own omission | (.5,-1), strict from Q5's own omission |
| Excluded corner | (-1,1), actual Q3 | (1,-1), actual Q1 |
| Excluded preceding marker | (0,1.086), actual Q11 | (0,-1.086), actual Q9 |
| Omitted forward point | (0,.26), F5 omitted by Q7 | (0,-.26), F4 omitted by Q5 |
| Whole excluded bar | {-1}×[.26,.56], actual Q8 | {1}×[-.56,-.26], actual Q10 |

Each whole bar belongs strictly to one actual wall square. Its near endpoint is original no-omission data, and its far endpoint is the universal ordinary advance in Section 5 of C1092-MPPM-NONORDINARY-ISOLATION.md. The strict outer halfpoints in this table are the ordinary missing-forward halfpoints; they do not assume an owner for an omitted forward point.

The inverse quarter turn for W and the forward quarter turn for E transform the local lemma's actual faces into

    W: L_W>=-b-r, J_W<=-.26r,
       K_W>=.56b-r, D_W<=1.086b,

    E: L_E>=.26t, J_E<=d+t,
       K_E>=-1.086d, D_E<=t-.56d.                 (23)

Both negative half-angles exceed 237/763. The exact endpoint pair is

    (cos theta0,sin theta0)=(263000,180831)/319169.

Canonical monotonicity gives all the numerical bounds in (2),(3), including br>.46 and d+t>1.39. For the latter,

    d+t>(263000+180831)/319169>139/100.

Thus every hypothesis of Theorem 1 except U>=-c-.5s has an explicit source in the original actual-owner configuration.

## 8. The halfpoint and boundary-origin conclusion

**Corollary 2.** Under the actual assumptions of Section 7, C strictly owns its outer halfpoint H_out=(-1,-.5), or original (1,1.5). Consequently the next actual boundary square Q9 strictly owns its origin (2,1).

Suppose H_out were not strict in C. Both its upper bands follow strictly from G=(-1,-.4), with increments .1s,.1c. Thus it can leave only through lower u or lower v.

If it were lower v, then V>=s-.5c. The strict marker M would imply

    s/c<3/13.

The actual foreign northwest marker M_W=(-.35,.35) has both lower bands strict by P,M. Its upper-u band follows from T because .09c-.35s>0 when s/c<3/13<9/35. Hence it would have to be upper v, with H<=.35(c+s). The two v-faces would then imply the impossible width

    a=H-V<=.85c-.65s<1.

Therefore the supposed missing H_out must be lower u and gives U>=-c-.5s. Theorem 1 now applies to the actual three squares in Section 7 and contradicts disjointness. This proves H_out strictly in C. In particular no assumption assigning H_out to a corner square was necessary for this argument.

Apply Theorem 7 of C1092-DIRECT-WALL-POINT.md with actual Q0 and Q9, b=.914 and ell=1.6. Q0's original strict anchors are (1,.914),(1,1); Q9's original strict anchors are its marker (2,.914) and F2=(1.6,1). Their real southwest and bottom container walls are exactly the theorem's wall hypotheses. The just-proved Q4 halfpoint is foreign to Q0 and supplies the transfer's excluded-halfpoint premise. Its conclusion is the strict origin (2,1) in Q9.

Simultaneously rotating the entire actual-owner table proves the same assertion in each sector: a positive forward-owned ordinary square flanked by two negative missing-forward ordinary squares receives its outer halfpoint and its next actual wall origin. The result does not exclude that sign pattern by itself; it supplies the actual point that the remaining cyclic argument may use.
