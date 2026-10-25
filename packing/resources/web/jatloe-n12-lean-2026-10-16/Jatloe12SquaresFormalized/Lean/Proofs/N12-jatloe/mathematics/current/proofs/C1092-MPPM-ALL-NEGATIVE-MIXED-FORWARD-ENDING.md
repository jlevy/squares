# C1092 MPPM: the complete all-nonpositive ordinary ending

All terminating decimals are exact rationals. Strict points belong to
their named actual open squares. An omitted point may lie on a face,
and every separating support inequality permits equality. All squares
have the same side a>1. No upper bound on a, numerical angle sample,
or ownership of an omitted forward point is used in this chapter.

## 1. The actual entrance and the statement

Retain the original no-omission MPPM entrance and the all-four-ordinary
conclusion. The actual ordinary pairs and forward points are

| Owner | Its strict ordinary pair | Its forward point |
|---|---|---|
| Q4 | F0=(1,1.74), G0=(1,1.6) | G3=(1.74,2) |
| Q5 | G5=(2.26,1), F6=(2.4,1) | F4=(2,1.74) |
| Q6 | F9=(3,2.26), G9=(3,2.4) | G6=(2.26,2) |
| Q7 | G4=(1.74,3), F3=(1.6,3) | F5=(2,2.26) |

The actual wall squares are Q8,Q9,Q10,Q11 with their original exact
pairs and markers. By Corollary 2 of
C1092-MPPM-ORDINARY-NEGATIVE-HALFPOINT.md, if all four central
canonical angles are nonpositive, then all four actual outer
halfpoints and wall origins are strict:

    Q4:(1,1.5), Q5:(2.5,1), Q6:(3,2.5), Q7:(1.5,3),
    Q8:(1,2),   Q9:(2,1),   Q10:(3,2),  Q11:(2,3).  (1)

This transfer is independent of every forward-point membership.
The ordinary wall advances from Section 5 of
C1092-MPPM-NONORDINARY-ISOLATION.md therefore give the four whole
strict segments in their one actual owner:

    Q8: {1} x [2,2.56],    Q9: [1.44,2] x {1},
    Q10:{3} x [1.44,2],    Q11:[2,2.56] x {3}.       (2)

The respective advance sources are F0 in Q4, G5 in Q5, F9 in Q6,
and G4 in Q7. No forward-point ownership is required for them.
All original central markers and paired-corner inner points remain
strict in their original owners.

**Theorem 1.** In this actual all-ordinary entrance, the four central
canonical angles cannot all be nonpositive, for any pattern of
forward-point membership.

We prove this using the following two continuous local obstructions:
three consecutive forward owners, and alternating forward ownership.
The other binary patterns contain two consecutive missing-forward
owners and are already excluded by the actual wall-center theorem.

Use the simultaneous quarter-turn

    R(x,y)=(4-y,x)

to cycle Q4,Q5,Q6,Q7 and Q9,Q10,Q11,Q8 in the indicated orders.
After translating (2,2) to the origin, R is (x,y)->(-y,x).

## 2. Forward-owned faces and clearance of the whole actual bar

Normalize a forward-owned nonpositive ordinary square to C=Q4 and
translate by (-2,-2). Write its canonical frame and faces as

    u=(c,-s), v=(s,c), c>=s>=0, c^2+s^2=1,
    U<u dot X<A=U+a,   V<v dot X<H=V+a.

Its strict points include

    P=(-1,-.26), G=(-1,-.4), T=(-.26,0),
    M=(-.35,-.35), Y=(-1,-.5).                       (3)

Its genuine foreign points include

    D0=(-1,0) in Q8, C0=(-1,-1) in Q0,
    N=(-.35,.35) in Q7.                             (4)

They force the following faces:

    U>=-c,       A>=a-c>0,       U<-c+.26s<0,
    V>=-c-s,     -.26s<H<=.35(c-s).                 (5)

Here are the complete exit comparisons. At D0, the upper-u,
lower-v and upper-v bands follow from P,G,T, respectively; their
increments are .26s>=0, .4c>0 and .74s>=0. Thus D0 is lower u.
In particular s=0 is impossible, since P then has the same u
projection as D0 and is strict.

At C0, the lower-u band follows from Y, the upper-u band from M,
and the upper-v band from G. The increments are .5s>=0,
.65(c-s)>=0 and .6c>0, so C0 is lower v. At N, the lower-u,
upper-u and lower-v bands follow from P,T,T; their increments are
.65c-.61s>=.04c>0, .09c+.35s>0 and .35c-.09s>=.26c>0.
Thus N is upper v. The remaining strict bounds in (5) are precisely
the strict P and T projections.

Suppose additionally that the next central owner Q5 owns its own
forward point I=(0,-.26). Then I is genuinely excluded from C.
Both of its lower bands follow from P, with increments c>0 and
s>=0, and its upper-v band follows from T with increment
.26(c-s)>=0. Hence

    A<=.26s,       1<a<=c+.26s.                     (6)

Put x=s/(1+c). The exact identity

    c+.26s-1=2x(.26-x)/(1+x^2)

gives

    0<x<13/50.                                     (7)

The actual far point F=(-.56,-1) belongs to Q9 by (2). Its lower-u
and upper-v bands in C follow from P, with increments
.44c+.74s>0 and .74c-.44s>0. If F were upper u, (5) would give
a<=.44c+s. But

    .44c+s-1=(1-x)(36x-14)/[25(1+x^2)]<0           (8)

on (7). Therefore F is lower v:

    V>=-c-.56s.                                    (9)

Let Z be C's lowest closure vertex. Its coordinates are

    Z=(cA+sV, -sA+cV).

Equations (5),(9) imply

    Z_x>=ac-1+.44s^2-cs>c-1+.44s^2-cs>-.56.       (10)

The final inequality has the exact positive identity

    c-.44+.44s^2-cs
      =(1-x)^2(1+x)(14-36x)/[25(1+x^2)^2]>0.

If Z_y<=-1, its upper-u face and (6) give

    cZ_x<=s(Z_y+.26)<=0.

Thus Z_x<=0. The segment from Z to the strict T then meets y=-1
at a point of (-.56,0] x {-1}. This entire segment is strict in
the one actual Q9 by (2). A closure point of C cannot lie in the
interior of a distinct square with disjoint open interiors: an open
neighborhood of that point would contain a point of C. This also
excludes Z_y=-1 and contact at the right endpoint. Consequently

    -sA+cV>-1.                                     (11)

Equations (5)--(11) use the next forward point only where it is
strict in Q5. They do not assume that a forward point omitted by
its indicated owner belongs anywhere else.

## 3. Three consecutive forward owners are impossible

Suppose Q4,Q5,Q6 all own their indicated forward points. Let C=Q4
and E=Q5 be their two actual squares in the centered coordinates.
Write

    C: u=(c,-s),v=(s,c), p in (0,pi/4],
    E: e=(d,-t),f=(t,d), q in (0,pi/4],
    k=cd+st=cos(q-p)>0,
    delta=ct-sd=sin(q-p).

Use L,K and J=L+a,D=K+a for E's lower and upper faces. Section 2
applies first to C with next owner E, and then to E in its own
quarter-turned chart with next owner Q6. Thus both half-angles
are less than 13/50. In particular

    c,d>2331/2669>.873,
    s,t<1300/2669<.488.                             (12)

The literal rotation of the lower-u origin floor and the whole-bar
clearance (11) gives

    K>=-d,      D>=a-d,      dJ+tD<1.               (13)

The last inequality is the strict rightmost-vertex clearance of E
from the actual Q10 bar {1} x [-.56,0], obtained by rotating
the proof of (11), not from the real container wall.

For later use, (13) implies

    L<t+1/d-a(1+t/d).                               (14)

Define the continuous scalar

    G(q)=(1-d)(1-t)/d=t+1/d-1-t/d.

It satisfies

    G'(q)=d-1/(1+t)<t.                              (15)

### 3.1. The exhaustive normal cone

Direct a separating normal n from C to E. Their strict markers
differ by (.7,0), so n_x>0. The strict C marker and E point
(.26,-1) also give

    .61n_x-.65n_y>0.

For either negative canonical frame, the positive transverse normal
has vertical component at least its horizontal component and fails
the second inequality. The other backwards normals have nonpositive
horizontal component. Hence the only possible actual face normals
are u and e, including all angle and tangent endpoints.

### 3.2. C's normal for both angle orders

If q<=p, delta<=0 and the exact lower E support is kL+delta D.
Using (13) and delta-kt/d=-s/d gives

    lower_E(u)=kJ+delta D-ak
      <k/d+s-a(k+s/d).

Since A>=a-c, separation would require a nonpositive value for

    a(1+k+s/d)-c-s-k/d.

Its coefficient of a is positive. At a=1, multiply by d and use
c<=d and k<=1 to obtain

    d(1-c)+(1-d)(s-k)
      >=(1-d)(d+s-1)>0.                            (16)

Here d<1 and s>=t>0, so d+s>=d+t>1. This excludes q<=p.

If q>=p, the exact lower support is kL+delta K. The same calculation
gives

    lower_E(u)<k/d+s-a(k+delta+s/d).

After replacing a by 1 in its positive coefficient and multiplying
the corresponding gap by d, the required scalar is

    F_C=d(1-c)+(1-d)(s-k)+d delta
       =d-Pc-Qs,
    P=d(2-d-t)>0,
    Q=d^2-(1-d)(1-t).                              (17)

Fix q and vary p on [0,q]. The exact identity

    Qd-Pt=d(d-t)>0

shows

    partial_p F_C=Ps-Qc
       <=c(Pt/d-Q)=-c(d-t)<0.

Its minimum is therefore at p=q, where

    F_C=(1-d)(d+t-1)>0.                            (18)

This also excludes q>=p and includes the common-angle endpoint.

### 3.3. E's normal when q>=p

The exact upper C support is kA-delta V. By (5), it is at least

    k(a-c)+delta[a-.35(c-s)].

Subtracting (14) and replacing a by 1 in its positive coefficient
1+t/d+k+delta gives a strict lower bound

    F_E=k(1-c)+delta[1-.35(c-s)]-G(q).              (19)

For fixed p its q-derivative is

    -delta(1-c)+k[1-.35(c-s)]-G'(q).

On the complete interval p<=q allowed by (12), we have
k>.873, delta<.488, 1-c<.127 and 1-.35(c-s)>=.65.
By (15), this derivative is strictly greater than

    -.488(.127)+.873(.65)-.488=.017474>0.           (20)

At q=p the value in (19) is

    (1-c)(c+s-1)/c>0.

Therefore E's normal cannot separate in this angle order.

### 3.4. E's normal when q<=p

Put h=sin(p-q)=-delta>=0. Here the exact upper C support is
kA+hH. The strict T projection gives H>-.26s. With (14), after
replacing a by 1 in its positive coefficient 1+t/d+k, the support
gap is strictly greater than

    F_E=k(1-c)-.26hs-G(q).                          (21)

For fixed q its p-derivative is

    .74ks-h(1-.74c)
      >=s(1.48c-1)>0,                              (22)

because k>=c, h<=s, 1-.74c>0, and c>.873. At p=q it has the
same positive endpoint value as (19). This excludes the last normal
and angle order. Thus three consecutive forward owners are
impossible. Every coefficient used to lower a to 1 was positive,
and (13) retained the actual whole-bar strictness.

## 4. Literal missing-neighbor profiles

We now treat alternating forward membership. Normalize it so that
C=Q4 owns T=G3, while its actual predecessor W=Q7 omits F5 and its
actual successor E=Q5 omits F4. Its opposite Q6 may be retained as
the forward owner in the alternating pattern; no point of Q6 beyond
its ordinary pair is needed below.

Lemma 1 of C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md applies to
each missing owner because (1),(2) supply both needed origins and
the actual far bar. In its own southwest chart a missing owner with
negative frame (b,-r),(r,b) has

    lower_u>=-b, upper_u<=r-.56b,
    lower_v>=-b-r, upper_v<=-.26r,
    r/(1+b)>7/18.                                 (23)

The corner, marker, own ordinary pair and halfpoint in this theorem
are all the literal quarter-turns of the actual data in Section 1.
Its missing forward point is an exclusion from that owner only.

For W=Q7, write its frame as (b,-r),(r,b), its angle magnitude as
phi, and its lower and upper faces as L_W,K_W,J_W,D_W. The
inverse-quarter-turn of (23) is exactly

    L_W>=-b-r, J_W<=-.26r,
    K_W>=.56b-r, D_W<=b.                           (24)

For E=Q5, use the frame and notation d,t,L,K,J,D from Section 3.
The forward-quarter-turn of (23) is exactly

    L>=.26t, J<=d+t,
    K>=-d, D<=t-.56d.                              (25)

Both phi and q exceed theta0=2 arctan(7/18), with endpoint

    cos theta0=275/373, sin theta0=252/373.

Consequently their cosine/sine pairs satisfy the exact uniform
bounds already proved in that missing-negative chapter:

    .7<b,d<.738, .675<r,t<.71,
    b+r,d+t>1.41, 0<=b-r,d-t<.062.                 (26)

The bounds below concern the one actual C between these two actual
missing neighbors. They are not independent replacement poses.

## 5. The missing predecessor leaves one support and a narrow C angle

Keep C's full table (5). Direct a separating normal from C toward W.
The strict markers give n_y>0. The strict pair P=(-1,-.26) in C
and (-.35,.35) in W gives

    .65n_x+.61n_y>0.

The two northwest normals (-c,s),(-b,r) fail this inequality, since
-.65c+.61s<=-.04c<0 and similarly for b,r. All downward normals
fail n_y>0. Thus the only possible actual directions are

    v=(s,c), supplied by C, and f_W=(r,b), supplied by W.

Put

    k=cb+sr>0, delta=cr-sb=sin(phi-p).

### 5.1. W's own normal is impossible in both angle orders

The exact upper C support on f_W is delta A+kH if delta>=0,
and delta U+kH if delta<=0. By A>0,U<0,H>-.26s from (5),
both alternatives are strictly greater than

    -.26ks>=-.26s>-.1846.

But its lower W support is K_W<=b-a<-.262 by (24),(26).
This excludes W's normal, including delta=0.

### 5.2. C's normal forces phi>p

If phi<=p, the exact lower W support on v is -delta L_W+kK_W.
Here -delta>=0 and L_W<=J_W-a<0. Also

    k>=cos(pi/4-phi)=(b+r)/sqrt(2)>.99,

using b+r>1.41 and sqrt(2)<1.42. Thus

    lower_W(v)<k(b-1)<-.99(.262)=-.25938.

This is smaller than H>-.1846. Therefore phi>p and delta>0.

In this remaining order, the exact lower W support is
-delta J_W+kK_W. Since J_W>=a-b-r and K_W<=b-a, separation
requires

    H<=-delta(a-b-r)+k(b-a)<c f(phi)-s g(phi),       (27)

where the exact expansion is

    f(phi)=1+br-b-r=(1-b)(1-r)
           =(b+r-1)^2/2,
    g(phi)=b^2-b+r.

Throughout theta0<phi<=pi/4,

    0<f<.086,      .48<g<=.5.                      (28)

For f, its displayed square is increasing in b+r, so its maximum
is 1.5-sqrt(2)<.086. For g,

    g'(phi)=b+r-2br>0,
    g(theta0)=67046/139129>12/25=.48,
    g(pi/4)=1/2.

These are continuous bounds on the full interval. Combining (27)
with the strict forward-point bound H>-.26s gives

    .22s<.086c,
    tan p<43/110<2/5.                              (29)

In particular c>.92 and s<.38.

### 5.3. The actual bottom origin and whole bar improve tan p to 1/4

Suppose p>=p1=arctan(1/4). Equations (27),(28) give

    H<.086c-.48s<=-.034c<0.                        (30)

The actual Q9 origin B0=(0,-1) is excluded from C. Its lower-u
band follows from P with increment c+.74s>0. Its upper-v band
follows from P with increment .74c-s>0 by (29). Its lower-v
band is strict because V=H-a<-1<=-c=v(B0). Hence it can exit
only through upper u:

    A<=s.                                          (31)

Use C's actual lowest closure vertex Z=(cA+sV,-sA+cV). The
origin and corner floors in (5) give

    Z_x>=ac-1-cs>c-1-cs>-.46>-.56,                 (32)

where c>.92 and cs<=s<.38. If Z_y<=-1, (31) gives
cZ_x<=s(Z_y+1)<=0. The segment from Z to T then meets the
strict actual bar [-.56,0] x {-1} in Q9. The same closure/interior
argument used for (11), including tangency and both endpoints,
gives the contradiction. Therefore Z_y>-1, and

    H>a-1/c+(s/c)A
       >=a(1+s/c)-1/c-s
       >h0(p):=-(1-c)(1-s)/c.                      (33)

This conclusion has been proved only in the hypothetical range
p>=p1 where its needed origin face (31) is genuine.

Compare it with (30). Define

    D(p)=h0(p)-.086c+.48s.

The exact derivative is

    D'(p)=1/(1+s)-.52c+.086s
          >50/69-13/25=353/1725>0                 (34)

on (29). At p=p1, c=4/sqrt(17),s=1/sqrt(17), and

    D(p1)=5/4-2557/[500sqrt(17)]>11/4100>0,         (35)

using sqrt(17)>41/10. Equations (34),(35) contradict (30),(33)
on the whole hypothetical interval p>=p1. We have therefore proved

    0<p<arctan(1/4).                               (36)

This conclusion used the actual missing predecessor, the actual
corner, the actual origin and whole bar, and no ownership of the
successor's omitted forward point.

## 6. The actual missing successor excludes both remaining normals

Retain the same C and the actual missing E of (25). Its angle q
exceeds theta0, while (36) gives p<arctan(1/4), so q>p and

    k=cd+st>0, delta=ct-sd>0.

The same strict marker/ordinary-point comparisons as in Section 3.1
leave only the genuine longitudinal normals u of C and e of E.

### 6.1. C's normal

The exact lower E support on u is kL+delta K. From (25),

    lower_E(u)<=k(d+t-a)+delta(t-.56d-a).

Together with A>=a-c, separation would require a nonpositive gap.
Replacing a by 1 in its positive coefficient 1+k+delta gives the
strict lower bound

    F_C=1-c+k(1-d-t)+delta(1-t+.56d)
       =1-Pc-Qs,
    P=2-d-t+.44dt,
    Q=1+d-t-.44d^2.                               (37)

By (26), dt<=.5 and d^2>=.5,

    P<.81,       Q<.842<.85.

The function .81 cos p+.85 sin p is increasing on
[0,arctan(1/4)]. Consequently

    F_C>1-.81c-.85s
       >=1-409/[100sqrt(17)]>1/410>0.              (38)

The last bound again uses sqrt(17)>41/10. Thus C's actual normal
cannot separate.

### 6.2. E's normal

Here the exact upper C support is kA-delta V. By (5), (25) and
V=H-a, its excess over lower_E(e)=L is at least

    a(1+k+delta)-d-t-kc-delta H.

After lowering a to 1 in its positive coefficient, the strict gap is
greater than

    F_E=1-d-t+k(1-c)+delta(1-H).                    (39)

Equations (27),(28) give H<.086. Also (26),(36) imply

    c>=4/sqrt(17)>.97,
    delta=c(t-d tan p)
       >.97[.675-.738/4]=.475785>19/40.

Since d+t<=sqrt(2)<1.42 and k(1-c)>=0, (39) is strictly greater
than the exact positive margin

    1-1.42+.914(19/40)=283/20000.                   (40)

E's normal is impossible as well. The two actual squares cannot
be disjoint, contradicting the alternating-forward entrance.

## 7. Completion of the actual four-sector cycle

Every forward membership is an ordinary dichotomy: the indicated
point is either strict in its indicated owner or omitted from it,
with face points counted as omitted. No other owner's membership
is inferred from the latter alternative.

If two consecutive owners omit their forward points, the actual
origins (1) allow Theorems 2 and 3 of
C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md to be applied to them.
For Q4,Q5, the first gives center(Q9)_x>1.8 and the quarter-turned
second gives center(Q9)_x<1.8. This is a contradiction for the
same actual Q9. Every other adjacent missing pair is its literal
simultaneous quarter-turn.

If at least three owners retain their forward points, there are
three consecutive retaining owners in the four-cycle. Section 3
excludes them, using the next forward point only in the named
strict retaining owner.

If at most one owner retains its forward point, there are two
consecutive missing owners, already excluded. With exactly two
retaining owners, either the two missing owners are consecutive,
or the memberships alternate. The first case has just been
excluded; Sections 4--6 exclude the second.

This exhausts every forward-membership pattern. All central zero
angles were already excluded by the literal face comparisons in
Section 2 for a retaining owner and by the missing-negative width
theorem for a missing owner. The proof retains every diagonal
endpoint, every equality of compared angles, every possible actual
face-normal source and every tangency. Thus Theorem 1 holds on
the full all-nonpositive ordinary sector.

The conclusion is an actual-square contradiction, not a statement
about auxiliary reassignments. Together with the already completed
nonordinary and wall-omission endings, it removes the whole
all-nonpositive subfamily of the remaining mixed-forward OOOO
obligation. Positive and mixed-sign forward patterns retain their
separate stated obligations.
