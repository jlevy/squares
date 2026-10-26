# C983 F4: the actual bottom bar gives a small southeast angle

All decimals are exact rationals. All strict points and whole strict segments keep their actual owners. Excluded points and segment contacts may be tangent. These are continuous lemmas for full open squares; no angle sampling is used.

## 1. A negative-angle theorem requiring only the nearer lower exclusion

**Theorem1.** Let E be an open square of side a>1 with canonical frame

    u=(c,−s), v=(s,c), c≥s≥0, c²+s²=1.

Suppose E strictly owns

    M=(.35,−.35), D=(.26,0), A=(1,−.26),

and excludes F=(0,−.26), K=(α,β), and the whole segment

    I=[.26,.8]×{−1}.

Assume either (α,β)=(.525,.125) or (α,β)=(.42,.16). Then, with U,V its lower face coordinates,

    U≥.26s, V≥.8s−c, V+a≤αs+βc,
    s/(1+c)<3/20.                                  (1)

In particular the theorem does not require an excluded point (0,−.5).

**Proof.** The parameter pairs satisfy

    .42≤α≤.525, .125≤β≤.16,
    α−.26≥β, α+3β=.9.                               (2)

At K, the lower u and v bands follow from D; the upper u band follows from A. The increments are

    (α−.26)c−βs≥0,
    (α−.26)s+βc>0,
    (1−α)c+(β+.26)s>0.

The possible zero in the first comparison still gives a strict band, because D is strict. Therefore K can leave only through the upper v face:

    V+a≤αs+βc.                                      (3)

Both upper bands of F follow from D. Its lower v band follows strictly from the opposite cap (3), since

    αs+(β+.26)c≤sqrt(.525²+.42²)<1<a.

Consequently F is lower u:

    U≥.26s.                                         (4)

Let B=(.26,−1),T=(.8,−1) be the endpoints of the same excluded segment I. At B its lower u band follows from D and its upper v band follows from M. An upper u exit, combined with (4), would give

    a≤.26c+.74s≤sqrt(.6152)<1.

Thus B is lower v, so

    V≥.26s−c.                                       (5)

At T its lower u and upper v bands follow from M, with increments .45c+.65s>0 and .65c−.45s≥.20c>0. Hence T is upper u or lower v. We prove that its upper u alternative is impossible by using the whole actual segment.

Suppose U+a≤.8c+s. Together with (4), this gives

    1<a≤.8c+.74s.

If the positive angle q satisfied tan q≤1/3, the increasing expression .8cos q+.74sin q would be at most

    3.14/sqrt(10)<1,

because3.14²=9.8596<10. Therefore q>atan(1/3).

Write A_E=U+a and H_E=V+a. The closed bottom vertex of E is

    Z=(cA_E+sV,−sA_E+cV).

Its abscissa is strictly between the bar endpoints. For its lower bound, (4),(5) give

    Z_x≥ac−.74cs+.26s²
       >c−.74cs≥1/sqrt(2)−.37>.26.                 (6)

For its upper bound, the supposed cap at T and (3) give

    Z_x≤.8+(α−.8)s²+s[(1+β)c−a]
       <.8+s[(1+β)c−(.8−α)s−1]<.8.                (7)

The final bracket is negative throughout q≥atan(1/3). Its angle-dependent part decreases strictly, and its value at atan(1/3) is

    [3(1+β)−(.8−α)]/sqrt(10)
       =(2.2+α+3β)/sqrt(10)=3.1/sqrt(10)<1.        (8)

Its ordinate is below the bar. Equations (3),(4) imply

    Z_y≤−a(c+s)+αcs+βc²−.26s².                     (9)

Set

    J(q)=c+s−1−αcs−βc²+.26s².

For atan(1/3)≤q≤π/4 this is strictly increasing, because

    J'(q)=(c−s)[1−α(c+s)]+2(β+.26)cs>0.

Indeed c−s≥0, α(c+s)≤.525sqrt(2)<1, and cs>0. At the lower endpoint, using (2),

    J=4/sqrt(10)−1−.3α−.9β+.026
     =4/sqrt(10)−1.244>0.                           (10)

The last exact comparison follows from16/10>(311/250)². Thus (9) gives Z_y<−1.

The strict point M has .26<M_x<.8 and M_y>−1. By (6),(7),(9), the segment from M to the closed vertex Z crosses I at a point before Z and with abscissa strictly between the endpoints. Every point of that segment before Z is strictly inside the open square: each defining strict linear band is interpolated between a strict interior value and a weak closure value. We have obtained an interior point on the excluded whole I, a contradiction. This argument includes a bar tangent to any edge or vertex as an allowed initial possibility.

Therefore T must be lower v:

    V≥.8s−c.                                        (11)

Combining (3),(11) yields

    1<a≤(1+β)c+(α−.8)s.                             (12)

This expression decreases strictly with q on the entire canonical interval, because 1+β>0 and α−.8<0. At half-angle3/20 its components are c=391/409,s=120/409. The two exact right-side values in (12) are

    3255/3272<1 for (α,β)=(.525,.125),
    10199/10225<1 for (α,β)=(.42,.16).

Thus (12) forces s/(1+c)<3/20. The other face bounds in (1) are (3),(4),(11). The zero-angle possibility was retained; the theorem asserts the necessary interval without asserting that its zero endpoint is feasible in an application. ∎

## 2. Exact application to both remaining C983 F4 pairs

Use the complete actual reduction in `C983-F4-CENTRAL-REDUCTION.md`. The southeast Q5 strictly owns its marker,F8,G6. The excluded F4 belongs to merged Q7. The excluded whole segment is the translation of the actual strict Q9 bar [2.26,2.8]×{1}. For the point K, there are exactly two cases:

| Northeast Q6 | Strict point excluded from actual Q5 |
|---|---|
| 131200={F7,G7} | (2.525,2.125), the upper-square theorem with actual top origin, right bar and northeast corner |
| 131232={F5,F7,G7} | (2.42,2.16), the mixed-elbow theorem with the actual NW marker in Q7, top origin, right F9 and northeast corner |

Translate by (−2,−2) and apply Theorem1 to Q5 whenever it has a nonpositive canonical angle. All three strict anchors, both isolated exclusions and the whole foreign segment belong to the actual owners stated above. Consequently

    Q7 owns F4 and Q5 has nonpositive angle
       ⇒ s_Q5/(1+c_Q5)<3/20.                        (13)

This includes Q5=327936, whose G8 is owned. It does not use the missing C974 southwest-crosspoint premise. The parameter point K is strict in the actual northeast Q6, and the argument proving (11) uses the complete segment of the actual Q9.

## 3. The top-only pair locks the southeast sign when the merged angle is nonpositive

**Theorem2.** In a remaining F4 configuration with Q6=131200, if merged Q7 has a nonpositive canonical angle, then Q5 has a strictly negative canonical angle. Combined with Theorem1, its half-angle is in (0,3/20).

**Proof.** The central reduction supplies (3,2) strictly in actual Q10 through the top-only Q6 point (2.5,3) and the actual northeast corner transfer. Denote W=Q7,E=Q5 and translate by (−2,−2). Give W its nonpositive canonical frame

    u_W=(d,−r), v_W=(r,d), d≥r≥0.

The point O=(0,0) is strict in W by the explicit four-band comparison in Section8 of that reduction. Its strict F4 is F=(0,−.26), and its two strict original markers are P=(−.35,−.35),Q=(−.35,.35).

Suppose E had a nonnegative canonical frame u_E=(c,s),v_E=(−s,c),c≥s≥0. Write its lower faces as U_E,V_E, and H_E=V_E+a. At the foreign right origin R=(1,0), its lower u band follows from D=(.26,0), its lower v band follows from A=(1,−.26), and its upper v band follows from D. Therefore

    U_E+a≤c.                                        (14)

At F, the two upper bands follow from D and its lower v band follows from M=(.35,−.35). The last increment is .35s+.09c>0. Thus

    U_E≥−.26s,
    1<a≤c+.26s.                                     (15)

The half-angle identity in (15) forces

    0<s/(1+c)<13/50,
    s<1300/2669<1/2,
    c>2331/2669>4/5.                                (16)

In particular the axis and diagonal E endpoints are already impossible under this supposition.

Orient a separating unit normal n from W toward E. The two strict pairs P∈W,M∈E and Q∈W,M∈E give

    n_x>0, n_x>n_y.

Among actual edge normals, this leaves only u_W from W and u_E,−v_E from E. The other W normal v_W=(r,d) cannot satisfy n_x>n_y. We exhaust these three directions using the full square supports.

For n=u_E, (14) gives lower_E(n)=U_E<c−1≤0. But O is strict in W, so upper_W(n)>0. This contradicts separation.

For n=−v_E, strict D∈E gives lower_E(n)=−H_E<.26s. Strict F∈W gives upper_W(n)>.26c. Since c≥s, this also contradicts separation.

For n=u_W, put

    k=cd−sr>0, h=sd+cr>0.

The first strict sign follows from the sum of the W angle magnitude, at mostπ/4, and the E angle in (16), which is less thanπ/6. The full lower E-support is

    lower_E(u_W)=kU_E−hH_E.

By (14), U_E<c−1. Strict D gives H_E>−.26s. Thus

    lower_E(u_W)<k(c−1)+.26sh.

Strict F gives upper_W(u_W)>.26r. The exact difference of the displayed E upper bound and .26r is

    d(1−c)(.26−.74c)
      +r[s−.74cs−.26]<0.                            (17)

The first term is strictly negative by (16), since d>0 and c<1. The second coefficient is negative as well: (16) gives

    s(1−.74c)−.26
       <.5(1−.74·.8)−.26=−.056<0.

Therefore lower_E(u_W)<upper_W(u_W), the opposite of separation. Every actual normal has failed.

E consequently has no nonnegative canonical representative. Its remaining representative is strictly negative, and (13) puts its half-angle below3/20. The W axial and diagonal representatives were included throughout. No bottom crosspoint in W was needed. ∎

## 4. Scope

The first theorem gives full negative-frame face bounds and the small half-angle for either remaining northeast component, even when G8 belongs to Q5. The second theorem excludes an entire sign combination of the top-only central pair. The remaining allowed signs and full coupled-square configurations still require their final contradiction; these are reductions, not a claim that the whole C983 family has been excluded.
