# A three-square two-fifths slope squeeze

New mathematical simplification for task 04 / C1092. All terminating decimals in this chapter are exact rational numbers. This is a written continuous proof, not a numerical angle search or a Lean verification.

## 1. Statement and notation

Let E, N and R be three actual open squares of a common side a>1. Require E and N each to have interior disjoint from R. Each square is described by two orthonormal directions and two open face intervals of length a. All faces mentioned for one square are the faces of that same physical square.

**Southeast profile.** E has frame u=(c,s), v=(-s,c), with c>s>0, c²+s²=1 and 0<s/c<1/3. Write U,V for its lower faces, A=U+a,H=V+a for its upper faces, and z=s/(1+c). Require

    I=(0,-.26), D=(.26,0) strictly in E,
    H<=0,                         s A+c H>a(c+s)-1.             (E)

**Northeast profile.** N has positive frame u_N=(b,t), v_N=(-t,b), where b>=t>0, b²+t²=1 and

    1/4<tan(theta/2)<=1/3.

Writing U_N,V_N,A_N=U_N+a,H_N=V_N+a for its actual faces, require

    U_N>=.4t, V_N>=.4b-t, A_N<=b+t, H_N<=b,
    M=(.35,.35), F=(.4,1), P=(.47,.12) strictly in N.           (N)

**Right-wall profile.** R has arbitrary orientation and satisfies

    {1} x [-.26,.4] strictly in R,
    closure(R) subset {x<=2},                  center_y(R)>=0. (R)

Then these profiles are impossible.

In fact, E and the genuine right-wall profile force the magnitude of R's canonical slope to be **less than 2/5**. N and the same right-wall profile forbid every slope magnitude **at most 2/5**. The two conclusions concern the same R, not independently optimized copies of it.

The local theorem does not need a<=1.001, a choice concerning G8, E--N disjointness, any ordering of central centers, or a finite list of orientations.

## 2. Preliminary exact bounds and support convention

Write R's canonical frame as either (d,-r),(r,d) or (d,r),(-r,d), where d²+r²=1 and d>=r>=0. These two closed signs cover every square orientation after relabeling faces. At r=0 either representative may be used. Face relabeling does not move the square.

For a direction n with components k,h in a square's frame, its upper support is k times its upper face if k>=0, or its lower face if k<=0, plus the analogous h term. The lower support uses the opposite faces. Disjoint open squares have a weak separating support along a face normal of one of the two squares; this follows, for example, by separating the origin from their difference parallelogram sum. Thus all directed face sources are included below. A strict point in each square gives a strict projection ordering even when the separating supports touch.

Profile (E) and its strict points imply

    U<-.26s<0, H>-.26s, A>A0=[a(c+s)-1]/s>a-z>1-z,
    c>47/50=.94, 0<s<8/25=.32, z<16/97<1/6.                 (1)

Here A>A0 follows by H<=0. The exact identity

    A0=a-z+(a-1)c/s

proves the bound for A. Put eta=z(1-s). Since s(1-s) is increasing on [0,.32],

    eta<(.32)(.68)/1.94=272/2425<113/1000=.113.               (2)

The northeast interval gives

    4/5<=b<15/17, 8/17<t<=3/5, 8/15<t/b<=3/4.               (3)

## 3. E forces a small nonpositive right angle

Use the nonpositive frame u_R=(d,-r),v_R=(r,d), and let L,K be its lower faces. The right bar gives

    L<d-.4r,                       K<r-.26d.                (4)

Orient a separating normal from E to R. Strict D and the strict bar point (1,0) force its horizontal component to be positive. The complete possible sources are u_E, -v_E, u_R, v_R. A vertical source at r=0 is already excluded by the same strict-point test, but the following inequalities also allow it.

Set k=cd-sr>0 and h=sd+cr>0.

For -v_E, the displacement from I to the upper bar endpoint has projection s-.66c<0, so this source is impossible.

For u_R,

    upper_E(u_R)=kA-h(H-a)>k(1-z)+h
                 =d(c+z)+r(1-s)>d>L.

We used c+z-1=z(1-s)>0. This rules out u_R.

For v_R, upper_E(v_R)=hA+kH>h(1-z)-.26sk. Subtracting the upper bound for K in (4), the gap is greater than

    d[.26+s(1-z-.26c)] + r[c(1-z)+.26s²-1].                 (5)

Its first coefficient exceeds .26. Its second is greater than

    (.94)(5/6)-1=-13/60.

Therefore (5) exceeds (.26-13/60)d=(13/300)d>0. This source also fails.

Only u_E remains. Its lower R support, using the same lower faces (4), satisfies

    lower_R(u_E)=kL+hK
      <c-.66cdr-s(.26d²-.4r²).

Since upper_E(u_E)=A>1-z, weak separation would require

    .66cdr+s(.26d²-.4r²)<c-1+z=eta<.113.                    (6)

Suppose r/d>=2/5. On [2/5,1], the function v/(1+v²) is increasing, so dr>=10/29. Also .26d²-.4r²=.26-.66r²>=-.07. The left side of (6) is strictly greater than

    (.66)(.94)(10/29)-(.07)(.32) > .113.                    (7)

Contradiction. Hence r/d<2/5 in the nonpositive sign.

## 4. E forces a small nonnegative right angle

Now use u_R=(d,r),v_R=(-r,d). Let L,K be the lower faces and J=K+a. The strict bar gives

    L<d-.26r,                        J>-r+.4d.              (8)

Strict D and (1,0) again force a rightward separator. The only sources are u_E,-v_E,u_R,-v_R. The source -v_E fails as before.

For -v_R=(r,-d), put alpha=cd+sr and delta=cr-sd. In the E frame, its components are delta,-alpha. Because A>0,U<0,V=H-a<=-a, its full upper support is at least a alpha, regardless of the sign of delta. Canonical angles give alpha>=1/sqrt(2). On the other hand the **actual** right wall and center give

    lower_R(-v_R)<=2r-a[1+r(d+r)]/2
                    <=2r-1/2-r²
                    <=sqrt(2)-1<1/sqrt(2).

This eliminates -v_R, with no upper estimate using the wrong sign of center_y(R).

Let q be E's positive angle and rho R's nonnegative angle. If rho<=q, then r/d<=s/c<1/3<2/5, already the desired conclusion. For rho>=q set alpha=cd+sr>0 and delta=cr-sd>=0.

### 4.1. R's own positive normal

The coupled floor is retained rather than replaced by independent face bounds:

    upper_E(u_R)=alpha A+delta H
       =(d/c)A+(delta/c)(sA+cH)>alpha A0>alpha(1-z).

Combining this with (8), separation along u_R would require

    -d P0+r Q0<0,
    P0=z(c+s),                      Q0=.26+s(1-z)>0.        (9)

We prove P0/Q0<2/5 over the whole E angle interval. After multiplication by 1+c,

    (1+c)(2Q0-5P0)=f(s)=.52(1+c)+2s-3cs-7s²,
    c=sqrt(1-s²),                  0<=s<=1/sqrt(10).        (10)

Throughout this interval c>=.9 and s²<=.1. Direct differentiation gives

    f'(s)=-.52s/c+2-3c+3s²/c-14s
           <=-.7+1/3=-11/30<0.

At the upper endpoint,

    f(1/sqrt(10))=(89-27sqrt(10))/(25sqrt(10))>0,
    since 89²=7921>7290=10(27²).

Thus 2Q0-5P0>0 everywhere. Inequality (9) forces r/d<P0/Q0<2/5.

### 4.2. E's own positive normal

The components of u_E in the R frame are alpha,-delta. Therefore

    lower_R(u_E)=alpha L-delta J
       <c-.66cdr+s(.4d²-.26r²).

Separation requires

    loss=.66cdr-s(.4d²-.26r²)<eta<.113.                     (11)

For fixed E and 0<=rho<=pi/4,

    d(loss)/d(rho)=.66c(d²-r²)+1.32sdr>0.

If r/d>=2/5, its minimum is at d=5/sqrt(29),r=2/sqrt(29). Consequently

    loss> [6.6(.94)-8.96(.32)]/29
          =4171/36250 >113/1000.                            (12)

This contradicts (11). Every source has been accounted for, proving r/d<2/5 in this sign as well.

## 5. N forbids the small nonpositive right angles

Assume 0<=r/d<=2/5 and use the nonpositive frame of Section 3. Strict M in N and (1,.35) in R force a separator from N to R to point rightward. The complete sources are u_N,-v_N,u_R,v_R.

The projection of the displacement from strict F to the lower bar endpoint is .6b-1.26t<-.072b<0 in direction u_N. In direction v_R it is .6r-1.26d<0. Both upward sources are impossible.

For u_R put alpha=bd-tr>0,beta=td+br>0. Profile (N) implies A_N>=a+.4t and V_N<=b-a. Thus

    upper_N(u_R)=alpha A_N-beta V_N>d C+r D,
    C=b+t-.6bt,                       D=b-t-1+.6t².         (13)

On interval (3), C increases with theta since C'=(b-t)[1-.6(b+t)]>0, while D decreases. Therefore

    C-1>30/289>1/10,               D+.4>=-23/125.

Subtracting L<d-.4r in (4), the support gap is strictly greater than

    d[1/10-(2/5)(23/125)]=(33/1250)d>0.                     (14)

For -v_N=(t,-b), use the genuine center/wall in (R). Direct support evaluation gives

    lower_R(-v_N)<=2t-a[(2t+b)d+br]/2.

Put w=r/(1+d). Then w<=r/(2d)<=1/5, and

    (2t+b)d+br-(2t+b)=r[b-(2t+b)w]>=0,

because (2t+b)<=2.5b on (3). Hence

    lower_R(-v_N)<t-b/2<=1-b<a-b<=upper_N(-v_N).

Here t+b/2<=1: it increases over (3) and equals one at (b,t)=(4/5,3/5). The strict inequality is supplied by a>1, including r=0. No remaining source separates N from R.

## 6. N forbids the small nonnegative right angles

Use the nonnegative right frame. Again u_N is excluded by strict F and the lower bar endpoint. The remaining sources are u_R,-v_R,-v_N.

For u_R put k=bd+tr>0 and h=td-br>0; the latter follows from r/d<=2/5<8/15<t/b. The same actual N faces give

    upper_N(u_R)=kA_N-hV_N
       >d C+r[1+t-b-.6t²]>d,

where C>1 as above and the bracket is positive. But L<d by the strict bar point (1,0). This source fails.

For -v_R, use strict P and the upper bar endpoint. Their displacement has projection

    .53r-.28d<=(.53(.4)-.28)d=-.068d<0.

It remains -v_N. Its upper N support is -V_N>=a-b. The same actual center and wall yield

    lower_R(-v_N)<=2t-a[(2t+b)d+(2t-b)r]/2.

Since a>1 and the bracket is positive, separation requires

    F(theta,rho)=1-b-2t+[(2t+b)d+(2t-b)r]/2<0.               (15)

Set P1=1-d/2+r/2 and Q1=2-d-r. Both are positive. Then F=1-bP1-tQ1, and

    Q1-(3/4)P1=(10-5d-11r)/8>=3/40>0,
    partial_theta F=tP1-bQ1<0.

We used d<=1,r<=2/5 and (3). Thus F decreases with theta on the full interval, so

    F(theta,rho)>=F(theta0,rho)=d+r/5-1
       =r[1/5-r/(1+d)]>=0,
    theta0=2 atan(1/3).

The last inequality follows from r/(1+d)<=r/(2d)<=1/5. This contradicts (15), including the aligned case r=0 and the endpoint theta=theta0.

Sections 3--4 force a right slope below 2/5, whereas Sections 5--6 exclude every right slope at most 2/5. This proves the theorem. ∎

## 7. What was simplified

The common local theorem covers both possible truth values of strict G8 ownership in E. The original MMMP proofs used two separate right-angle endings in the G8-omitted branch and another ending in the G8-owned branch. The common profile above replaces those three terminals; the short separate **entrance** lemmas for the two G8 alternatives must still be proved and retained.

The complete actual-owner entrance ledger and its application to the handoff's precise omission target are in `MMMP-ACTUAL-ENTRANCE.md`. In particular, no conclusion is obtained by asserting the three-square profile without that entrance. The right wall and center are essential hypotheses and cannot be deleted to obtain a point-only relaxation.
