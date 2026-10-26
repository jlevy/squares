# C982: continuous geometry of the merged bottom owner

All decimals denote exact rationals. Owned points lie in the open square; excluded points may lie on its boundary. The original container and common side satisfy 1<a≤1001/1000. The first theorem below needs only a>1.

## 1. Two foreign points force the merged square's angle and a strict region

**Theorem 1.** Let Q be an open square of side a>1. In coordinates translated by (−2,−2), suppose Q owns

    B=(0,−1.086), M=(−.35,−.35),

and excludes

    J=(−.26,−1), R=(.35,−.35).

Then Q has a strictly negative canonical angle. Write its frame as

    u=(c,−s), v=(s,c), c≥s>0, c²+s²=1,

and its open bands as U<u·X<U+a, V<v·X<V+a. Then

    43/130 < s/c < 175/368,                              (1)
    U+a≤.35(c+s),       V≥−.26s−c.                     (2)

In particular, Q strictly owns

    Z=(.30,−.16), L=(−.55,.05), K=(.04,−.06).           (3)

If also a≤1001/1000, then neither (0,.26) nor (.26,0) belongs to Q.

### Proof: exclude every nonnegative angle

Use a nonnegative canonical frame u=(c,s), v=(−s,c), c≥s≥0. At J, the upper u band follows from B, because

    u(B)−u(J)=.26c−.086s≥.174c>0.

The upper v band follows from M, since v(M)−v(J)=.09s+.65c>0; and the lower v band follows from B, since v(J)−v(B)=.26s+.086c>0. Exclusion therefore forces U≥u(J).

At R, both lower bands are strict: the lower u band follows from M, and the lower v band follows from B, with difference .736c−.35s≥.386c>0. Its upper v band follows from M, since v(R)−v(M)=−.7s≤0. Hence exclusion forces U+a≤u(R). The two forced faces give

    a≤u(R)−u(J)=.61c+.65s≤sqrt(.7946)<1,

which contradicts a>1. This includes s=0 and s=c; strict membership of the comparison points handles equality in any projection comparison.

### Proof: the negative-angle faces

Now use u=(c,−s), v=(s,c), c≥s≥0. At J the lower u band follows from M, with increment .09c+.65s>0. Its upper u band follows from B, with difference .26c+.086s>0. Its upper v band follows from M, with difference .65c−.09s≥.56c>0. Thus J is excluded only through the lower v face:

    V≥v(J)=−.26s−c.

At R the lower u band follows from M, and the lower v band follows from B, whose difference is .35s+.736c>0. If R were excluded through the upper v face, the forced lower face at J would give

    a≤v(R)−v(J)=.61s+.65c≤sqrt(.7946)<1.

Consequently R is excluded through the upper u face, giving (2).

The strict lower v band and strict upper u band of the owned point B now imply respectively

    −1.086c>−.26s−c,
    1.086s<.35(c+s).

These rearrange to (1). In particular the angle is strictly negative; neither axial nor diagonal orientation survives.

### Proof: the three strict points

For Z=(.30,−.16), the lower u band follows from the upper face in (2), because

    u(R)−u(Z)=.05c+.19s<1<a.

Its upper u band follows from B: by (1),

    u(B)−u(Z)=.926s−.30c>0,

since .926·(43/130)−.30=409/65000>0. Its lower v band follows from B. For the upper v band, (2) gives

    v(Z)−V≤.56s+.84c.

The function (.84+.56τ)/sqrt(1+τ²) is increasing for 0≤τ≤175/368, because its derivative has the sign of .56−.84τ>0. Therefore

    .56s+.84c < 10178/(25sqrt(166049)) < 1,

where the final strict inequality is certified by

    625·166049−10178²=188941>0.

All four bands of Z are strict.

For L=(−.55,.05), its lower u band follows from (2), since

    u(R)−u(L)=.90c+.40s≤sqrt(.97)<1<a.

Its upper u band follows from M, since u(M)−u(L)=.20c+.40s>0. Its lower v band also follows from M, with difference .40c−.20s≥.20c>0. Finally,

    v(L)−V≤1.05c−.29s
       <(1.05−.29·3/10)c=.963c<1<a,

because s/c>43/130>3/10. Hence L is strictly owned.

For K=(.04,−.06), its lower u band follows from (2), since

    u(R)−u(K)=.31c+.29s≤sqrt(.1802)<1<a.

Its upper u band follows from B, since 1.026s−.04c>0 by (1). Its lower v band follows from B, and its upper v band follows from (2), since

    v(K)−V≤.30s+.94c≤sqrt(.9736)<1<a.

Thus K is strictly owned as well.

### Proof: the two optional auxiliary points are excluded

The interval (1) implies c>9/10 and s>3/10. Indeed 175/368<sqrt(19)/9 and 43/130>3/sqrt(91), as one sees by squaring positive quantities. The v-coordinate difference between (.26,0) and B is therefore

    1.086c+.26s>1.086·.9+.26·.3=1.0554>1.001≥a.

Two strict points of one side-a square cannot have a face-coordinate difference at least a. Thus (.26,0) is excluded. The v-coordinate difference between (0,.26) and B is 1.346c>1.2114>1.001≥a, so (0,.26) is excluded as well. No inference here treats a foreign point on a face as strictly separated. ∎

## 2. Exact C982 entrance and application

The retained entrance is `root_next/twenty_one_cases/C982-complete-exclusion.txt`, Sections 2–3, in the earlier completed source. Its original owner mask is

    (1,2,12,48,192,512,1024,2048,4096,8448,16384,32768).

The actual owner Q9 contains original markers (1.65,1.65) and (2,.914). The different owner Q0 strictly contains (1.74,1), and the different owner Q5 strictly contains the southeast marker (2.35,1.65). Thus translation by (−2,−2) supplies exactly B,M,J,R in Theorem 1. Its conclusions give

    (2.30,1.84), (1.45,2.05), (2.04,1.94) ∈ Q9.          (4)

The retained local label family for Q9 is

    {8208,73744,8240,73776}
      = {F4+G3, F4+G3+G6, F4+F5+G3, F4+F5+G3+G6}.

The final part of Theorem 1 excludes F5=(2,2.26) and G6=(2.26,2), so the actual label is 8208, owning precisely F4 and G3 among the twenty auxiliary points. This use of the original local ownership family does not claim to replace its finite entrance rule.

All original strict Q9 anchors and the three new points (4) belong to the same actual open convex square. Their entire convex hull is therefore strict in Q9 and excluded by every other square. This is the source of the whole-hull exclusions used below.

## 3. A whole segment and three points exclude the southeast marker

**Theorem 2 (one-segment, three-point obstruction).** No open square of side a>1 can own

    M=(.35,.65)

while excluding all three points

    P=(1,0), H=(1.086,0), R=(1.086,1)

and the entire closed segment

    S=[B,Z], B=(0,−.086), Z=(.30,.84).                   (5)

No container, upper side bound, auxiliary ownership or orientation premise is needed.

### 3.1. Coordinates and the two possible forms of separation

Translate M to the origin. In these coordinates the five foreign points are

    B=(−.35,−.736), Z=(−.05,.19),
    P=(.65,−.65), H=(.736,−.65), R=(.736,.35).            (6)

The segment has normal n=(.926,−.30), and its line is

    n·X=−d,       d=.1033.                              (7)

The owned origin lies strictly on the other side of this line.

For either canonical frame u=(c,±s), v=(∓s,c), with c≥s≥0 and c²+s²=1, write the square's bands

    U<u·X<U+a,       V<v·X<V+a.

Strict ownership of the origin means U<0<U+a and V<0<V+a.

The separating-axis theorem applied to a square and a segment allows a weak separator normal to a square side or to the segment. This also holds if the segment touches the square's boundary: only intersection with the open square is prohibited. It follows directly by applying the polygon separating-axis theorem to the segment as a degenerate convex polygon, or by first shrinking the square slightly and then taking the limit of disjoint positive-width rectangles about the segment.

In both canonical signs, v(B)<0<v(Z). Thus the segment cannot be separated from the square along v. In the nonnegative sign u(B)<0, and in the negative sign u(Z)<0. Consequently the segment cannot lie beyond the square's upper u face. Finally, its line normal can separate only with the square on the origin's side of (7). The entire segment exclusion therefore yields at least one of exactly these alternatives:

    U≥max(u(B),u(Z)),                                    (8)

or

    lower_Q(n)≥−d.                                      (9)

All subsequent arguments use weak inequalities for the separating supports. In particular endpoint contact and face tangency are included.

We will also use the following elementary bound:

    c+.086s<1 whenever s/c≥1/5.                         (10)

Indeed (1+.086τ)/sqrt(1+τ²) decreases for τ≥1/5, since its derivative has the sign of .086−τ<0. At τ=1/5 it equals 2543/(500sqrt(26))<1, with exact squared margin

    500²·26−2543²=33151>0.

### 3.2. The square-face separation (8) is impossible

First take the nonnegative frame u=(c,s), v=(−s,c). Here

    u(Z)=−.05c+.19s,

so (8), together with U<0, forces s/c<5/19. The point H has positive u coordinate and negative v coordinate, so it can be excluded only through upper u or lower v. Upper u would give

    a≤u(H)−u(Z)=.786c−.84s<1,

using (8), a contradiction. Hence H is lower v: V≥v(H).

The point R has both coordinates positive because s/c<5/19<175/368. Thus R can be excluded only through upper u or upper v. The latter would give a≤v(R)−v(H)=c≤1. The former gives, again using (8),

    a≤u(R)−u(Z)=.786c+.16s≤sqrt(.643396)<1.

Both are impossible.

Next use the negative frame u=(c,−s), v=(s,c). From U≥u(B) and U<0 we get

    s/c<175/368<1/2.                                    (11)

Both coordinates of R are positive. Its exclusion through upper u would imply

    a≤u(R)−u(Z)=.786c−.16s<1,

so R must be upper v. The point H has positive u coordinate and negative v coordinate by (11). Lower v is impossible, because it would imply a≤v(R)−v(H)=c≤1. Thus H is upper u.

The point P has positive u coordinate and negative v coordinate. If it were upper u, (8) would give

    a≤u(P)−u(B)=c−.086s≤1.

Therefore P is lower v. When s/c≥1/5, this contradicts the upper-v face at R by (10): a≤v(R)−v(P)=c+.086s<1. When s/c≤1/5, the upper-u face at H and (8) instead give

    a≤u(H)−u(Z)=.786c+.84s≤.954c<1.

This excludes (8) in every sign and at the boundary s/c=1/5.

### 3.3. Segment-normal separation in the nonnegative sign

Use u=(c,s), v=(−s,c), and put

    α=.926c−.30s>0,       β=.30c+.926s>0.

Then n=αu−βv, so (9) says

    αU−β(V+a)≥−d.                                      (12)

As U<0<V+a, it follows that

    −αU<d,       β(V+a)<d.                              (13)

At H, only upper u or lower v can exclude. If H were upper u, then

    −αU≥α(a−u(H))>α(1−u(H)).

But c≥1/sqrt(2)>7/10 gives α≥.626c>.4382, and u(H)=.736c−.65s≤.736. Thus

    α(1−u(H))>.4382·.264=.1156848>d,

contradicting (13). Hence H is lower v.

At R, the lower u band is strict because u(R)>0. Lower v is impossible: if V≥v(R), then

    β(V+a)>β(1+v(R))>.21·.614=.12894>d,

where β≥.30c>.21 and v(R)=.35c−.736s≥−.386. Upper v is impossible because H is lower v and v(R)−v(H)=c≤1. Therefore R is upper u.

Substituting U≤u(R)−a and V≥v(H) into (12) yields

    a(α+β)≤αu(R)−βv(H)+d
      =.979836−.30s²+.926cs.                            (14)

However, for every c≥s≥0 on the unit circle,

    1.226c+.626s>.979836−.30s²+.926cs.                   (15)

Here is a continuous exact proof. Write c=cos θ, s=sin θ, 0≤θ≤π/4, and let F be the left side of (15) minus the right side. Put K=c+s and D=c−s. Direct differentiation gives

    F'(θ)=(1−K)(.30+.926D)−.30D²≤0.

Thus F is at least its diagonal value

    F(π/4)=.926sqrt(2)−1.292836
       >.926·1.4−1.292836=.003564>0.

Since α+β=1.226c+.626s, (14) and (15) imply a<1. This contradiction excludes (9) in the whole nonnegative sector, including zero angle and the diagonal.

### 3.4. Segment-normal separation in the negative sign

Now use u=(c,−s), v=(s,c), and put

    α=.926c+.30s>0,       γ=.926s−.30c.

The point R has both frame coordinates positive. In either sign of γ, (9) and ownership of the origin imply −αU≤d. If R were excluded through upper u, then

    −αU≥α(a−u(R))>α(1−u(R))
       >.6482·.264=.1711248>d,

because α≥.926c>.6482 and u(R)=.736c−.35s≤.736. Therefore R is necessarily upper v.

**First subcase: γ≥0.** Here s/c≥150/463>1/5, and (9) reads

    αU+γV≥−d.                                          (16)

The point P can only be upper u or lower v. Lower v would contradict the upper-v face at R, by a≤c+.086s<1 from (10). Hence P is upper u. Substituting U≤u(P)−a and V≤v(R)−a into (16) gives

    a(α+γ)≤αu(P)+γv(R)+d
      =.6002+.379636s²+.9002cs.                         (17)

But the following inequality holds on the entire canonical quarter circle:

    .626c+1.226s>.6002+.379636s²+.9002cs.                (18)

To prove it, write K=c+s. Since

    K−1=2cs/(K+1)≥(4/5)cs,

the left side minus the right side in (18) is at least

    .0258+s(.60−.3994c−.379636s)>0.

Indeed .3994c+.379636s<.40(c+s)≤.40sqrt(2)<.60. Since α+γ=.626c+1.226s, (17) and (18) contradict a>1. This includes γ=0.

**Second subcase: γ<0.** Put β=−γ>0, so (9) is

    αU−β(V+a)≥−d,       −αU<d.                        (19)

Now s/c<150/463<1/3. The point H has positive u coordinate and negative v coordinate. Its exclusion through lower v is impossible, since R is upper v and v(R)−v(H)=c≤1. Thus H is upper u.

If s/c≤1/5, then u(H)=.736c+.65s≤.866 and α≥.926c≥.926/sqrt(1.04)>.90. Consequently

    −αU≥α(a−u(H))>.90·.134=.1206>d,

contradicting (19).

If s/c≥1/5, the lower-v alternative for P is again impossible by (10), so P is upper u. The bound s/c<1/3 gives u(P)=.65(c+s)<13/15 and c>3/sqrt(10)>.9. Thus α>.8334, and

    −αU≥α(a−u(P))>.8334·(2/15)=.11112>d,

again contradicting (19).

This handles every negative angle, including all intermediate equality thresholds. Alternatives (8) and (9) have both been excluded, so the alleged square does not exist. ∎

## 4. Complete continuous exclusion of the original C982 family

**Theorem 3.** The entire retained original family C982 is impossible.

By Theorem 1 and its exact application in Section 2, the actual merged owner Q9 strictly owns both (2,.914) and (2.30,1.84). Their entire closed segment is therefore strictly inside Q9 and excluded from Q5.

The actual southeast central owner Q5 owns (2.35,1.65). The actual paired southeast corner Q2 owns (3,1) and (3.086,1), and the different right-wall owner Q10 owns (3.086,2). Translate these five points and the segment by (−2,−1). They become exactly M,P,H,R and S in Theorem 2, with each foreign point and the whole segment supplied by its named actual owner. The theorem excludes Q5, a contradiction.

This proof covers every original auxiliary alternative at once. Beyond the retained original hull/ownership entrance, it uses no central label, angle-cell state, center enclosure, directed pair update, four-chord propagation, or terminal margin. The optional-label conclusion in Theorem 1 is a valid reusable strengthening, but is unnecessary for the final contradiction. The continuous ending requires only a>1; the upper side bound is used solely in that optional-label strengthening.
