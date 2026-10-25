# C1092 MMMP: the double-right branch forces a positive northwest angle

Every terminating decimal denotes an exact rational. All squares are the original actual open squares, with their common side a>1. Owned points are strict and separating supports may be tangent.

**Theorem.** In the original MMMP family, if actual Q10 owns G8, the northwest square Q7 has strictly positive canonical angle in the original chart. Thus both Q5 and Q7 have positive canonical angles in this branch, and Q5 has sine less than .21.

The southeast sign and sine assertions were proved in `C1092-MMMP-RIGHT-DOUBLE-SPAN.md` and `C1092-MMMP-DOUBLE-RIGHT-BOTTOM-ORIGIN.md`. We prove the remaining northwest assertion using the actual Q5,Q6,Q7 and their complete square supports.

## 1. Actual points and the nonpositive northwest supposition

Translate all squares by (−2,−2), and name

    W=Q7, N=Q6, E=Q5.

The completed northwest half-unit-square theorem gives

    O=(0,0), L=(−.26,0), P=(0,.26) strictly in W.

The actual southeast inward pair gives

    I=(0,−.26), D=(.26,0) strictly in E.

The northeast square N has the exact ordinary component131200 and the positive frame and full face table of `C1092-MMMP-NORTHEAST-TOP-CAP.md`.

Suppose W has a nonpositive canonical representative. Write

    u_W=(d,−r), v_W=(r,d), d≥r≥0, d²+r²=1,

and denote its upper faces by A,H. Its lower faces are A−a,H−a. Strict O implies

    A>0, H>0.                                      (1)

Section 3 of `C1092-MMMP-UPPER-STRICT-POINTS.md` applies to this actual W and its actual northeast neighbor. Its explicit point and face hypotheses hold throughout MMMP, without any southwest-label condition. It gives

    0≤r<.14, d>.99.                                (2)

The same complete pair analysis proves that the only possible W-to-N separator is N's longitudinal axis in this translated original chart. We state its exact transported inequality next.

## 2. The actual northeast neighbor puts W's upper v face below 25/33

Write N's positive original frame as

    u_N=(b,t), v_N=(−t,b), b≥t>0, b²+t²=1.

The top-origin cap gives t/(1+b)>1/4. Under the quarter-turn used in that chapter, its upper-v face becomes N's upper-u face in the present chart. Thus that full upper face is at most b+t, and its lower-u face is at most b+t−a.

Put

    alpha=bd−tr>0, k=br+td>0.

The full W support on u_N is alpha A+kH. The retained separator from the actual pair analysis therefore gives

    alpha A+kH≤b+t−a.                              (3)

This is also the direct rearrangement of equation (11) in Section 3 of the cited upper-strict-points chapter: its central upper faces are −(H−a),A after the quarter-turn. In particular no face coordinates of a separately translated copy of W are substituted.

By A>0, a>1 and k≥td,

    H<(b+t−1)/k≤(b+t−1)/(td)
      =[1−t/(1+b)]/d
      <(3/4)/(.99)=25/33.                         (4)

The identity in the middle follows from 1−b=t²/(1+b). The numerator b+t−1 is positive, as required when weakening its denominator. The strict positive alpha follows from (2) and b≥t, since d>r.

## 3. Every actual W–E separating direction contradicts the full supports

The earlier double-right results give E its strictly positive frame

    u_E=(c,s), v_E=(−s,c), c≥s>0, c²+s²=1,
    s<.21, c>.97.

Write U,V for its lower faces and h=V+a for its upper-v face. The actual strict inward points give

    U< u_E(I)=−.26s,
    h> v_E(D)=−.26s.                              (5)

Orient a separating normal from E toward W. The strict pairs D to L and I to P imply respectively

    n_x<0, n_y>0.

Among all face normals of these two actual squares, the only possible directions in this quadrant are v_E and −u_W. The axial endpoint r=0 may remove −u_W from the strict cone; retaining it can only enlarge the alternatives. Define

    j=sd+cr>0, k_0=cd−sr>0.

The uniform bounds above imply

    j<.21+.14=.35,
    k_0>(.97)(.99)−(.21)(.14)=.9309>.93.            (6)

In particular k_0>j. We check both sources using the full actual supports.

### 3.1. E's own transverse normal

The components of v_E in W's frame are −j,k_0. Hence its lower W support is

    lower_W(v_E)=−j A+k_0(H−a).

If this normal separated E from W, (5) would imply

    −.26s<h≤−j A+k_0(H−a)<k_0(H−a).

It follows from (6) that

    H>a−.26s/k_0>1−(.26)(.21)/(.93)
      =1459/1550>25/33.                           (7)

This contradicts (4). The two rational endpoints are strictly ordered since1459·33−25·1550=9397>0.

### 3.2. W's own negative longitudinal normal

The components of −u_W in E's frame are −k_0,j. Its full upper E support is therefore

    upper_E(−u_W)=−k_0 U+jh
       >.26s(k_0−j)>0,                            (8)

by (5),(6). But the lower W support in this direction is −A<0 by (1). Thus this normal cannot separate either.

Every possible actual face-normal source has failed. All separating inequalities were allowed to be weak, and the contradictions are strict because the named original anchors lie inside their actual owners and a>1. The nonpositive northwest representative is impossible. The remaining canonical sign of Q7 is strictly positive, proving the theorem.

## 4. Scope

This result excludes the entire nonpositive-Q7 part of the original double-right MMMP branch. It leaves the positive Q7 and positive Q5 configuration for its final contradiction. No conclusion about the nondouble right alternatives, or the final whole MMMP family, is asserted here.
