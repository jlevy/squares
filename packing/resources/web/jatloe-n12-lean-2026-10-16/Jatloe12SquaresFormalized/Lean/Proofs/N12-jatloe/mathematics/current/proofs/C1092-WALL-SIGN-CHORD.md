# C1092: a wall-center sign forces a whole rational chord

Every terminating decimal denotes an exact rational. All ownership is strict interior membership in an actual open square. Excluded points and container contacts may be tangent.

## 1. A continuous strengthening of the forward-point theorem

**Theorem 1.** Let W be an open square of side a>1, with closure in x≥0. Suppose W strictly owns P=(.914,2), excludes N=(1.65,2.35), and its center ordinate satisfies Y_W≥2. Then W strictly contains the entire segment

    {1}×[2.22,2.39].                                  (1)

No other marker, auxiliary ownership, angle bound, or upper side bound is required. In particular, (1) contains the older side39 chord {1}×[2.22,2.37], but follows directly from three original physical premises.

**Proof.** Translate by (−1,−2), and put

    P=(−d,0), N=(b,h), A=(0,r),
    d=.086, b=.65, h=.35, .22≤r≤.39.

Write the center as (X,Y), so Y≥0, and the actual wall is x≥−1. Let c≥s≥0, c²+s²=1, be the absolute canonical components, and K=c+s. The wall gives

    X≥−1+aK/2.                                        (2)

The two elementary estimates used below are

    K≥1+(4/5)cs, c≥1−(3/5)s², c>7/10.                (3)

The first follows from K−1=2cs/(K+1) and K+1<5/2. The second has exact difference (1−c)(3c−2)/5≥0.

We first record the two uniform wall gaps

    1+cK−2c−2rs≥0,
    1+sK−2s−2rc>0.                                   (4)

They decrease with r, so it suffices to use r=.39. For arbitrary nonnegative c,s on the unit circle, write z=s/(1+c). Direct substitution gives

    1+c(c+s)−2c−.78s
      =z(100z³−89z²+11)/[25(1+z²)²],

    100z³−89z²+11
      =100(z−89/150)²(z+89/300)+37531/67500>0.         (5)

Thus the first gap is nonnegative, with equality only at s=0. Interchanging c and s proves the second; its corresponding z=c/(1+s) is strictly positive. This verifies (4) on the entire canonical interval without subdivision.

### 1.1. Positive canonical frame

Take u=(c,s), v=(−s,c), with lower faces U,V. Both lower bands of A follow strictly from P:

    u(A)−u(P)=dc+rs>0,
    v(A)−v(P)=rc−ds≥(r−d)c>0.

If A failed its upper u-band, then cX+sY≤rs−a/2. Together with (2) and Y≥0 this would give

    a(1+cK)≤2c+2rs,

contradicting the first gap in (4) and a>1.

Suppose instead A failed its upper v-band, so V+a≤rc. The lower u-band of N is strict by P. A lower v exit of N would imply the opposite-face width

    a≤v(A)−v(N)=.65s+(r−.35)c
      ≤.65s+.04c≤sqrt(.4241)<1,

which is impossible. N cannot exit through upper v either: that exit, together with strict U<u(P)=−dc, would give

    Y=s(U+a/2)+c(V+a/2)
      ≤.35c²−.736cs−(c−s)/2
       =c(.35c−1/2)+s(1/2−.736c)<0.                  (6)

Both bracketed coefficients are negative by c>7/10. Hence N is upper u, U+a≤.65c+.35s. Combining this cap with the supposed upper-v cap at A gives

    Y≤rc²+.35s²+.65cs−aK/2
      <−.11c²−.15s²+.25cs<0.                       (7)

The first strict inequality uses (3), a>1 and r≤.39. The final sign follows from

    .11c²+.15s²−.25cs
      =[(22c−25s)²+35s²]/4400>0.                    (8)

This contradicts Y≥0 and completes all four strict bands of A in the positive frame.

### 1.2. Negative canonical frame

Now take u=(c,−s), v=(s,c). A's lower v-band follows strictly from P. If its upper v-band failed, (2) and Y≥0 would imply

    a(1+sK)≤2s+2rc,

contrary to the second gap in (4).

Suppose A failed its upper u-band. If rs≥dc, the strict anchor P already gives that band, so assume rs<dc. Strict ownership of P gives sX+cY<−ds+a/2, and therefore

    c(cX−sY)=X−s(sX+cY)
      ≥−1+ac/2+ds².

The alleged upper-u failure also gives c(cX−sY)≤−rcs−ac/2. Consequently

    ac≤1−ds²−rcs.                                   (9)

At s=0 this contradicts a>1. At s>0, (3) and rs<dc give

    c+ds²+rcs−1≥s[rc−(.6−d)s]>0,

because

    r²−d(.6−d)≥(.22)²−.086·.514
      =1049/250000>0.                               (10)

Thus (9) is impossible, proving the upper u-band strictly.

Only a lower u exit remains. If U≥−rs, both lower bands of N are strict by P, with gaps

    (b+d)c−hs≥(.736−.35)c>0,
    (b+d)s+hc>0.

An upper u exit of N would imply

    a≤u(N)−u(A)=.65c+(r−.35)s
      ≤.65c+.04s≤sqrt(.4241)<1.

Hence N is upper v, V+a≤.65s+.35c. The center now satisfies

    Y=−s(U+a/2)+c(V+a/2)
      ≤rs²+.65cs+.35c²−aK/2
      <−.15c²−.11s²+.25cs<0,                       (11)

using the transpose of (8). This again contradicts Y≥0. Thus every A=(0,r) for .22≤r≤.39 is strictly inside W in either canonical sign, including axial and diagonal endpoints. The theorem follows. ∎

## 2. Exact whole-sector transports

Apply Theorem 1 using the five simultaneous wall, marker, foreign-marker and center-sign transformations listed in `C1092-WALL-SIGN-AUXILIARIES.md`. They give the following actual strict segments directly from the original C1092 entrance:

| Actual owner | Closed wall-center sign | Compulsory strict segment |
|---|---|---|
| Q8 | Y8≥2 | {1}×[2.22,2.39] |
| Q9 | X9≥2 | [2.22,2.39]×{1} |
| Q10 | Y10≥2 | {3}×[2.22,2.39] |
| Q11 | X11≥2 | [2.22,2.39]×{3} |
| Q11 | X11≤2 | [1.61,1.78]×{3} |

The MMMM sector uses the first four rows, and MMMP the first three and last. Each row uses only an original wall marker, an original excluded central marker, and the actual wall-center sign. Thus the entire older side39 chord input is now a conclusion of this single continuous theorem, with a slightly longer interval and no ownership-mask pass as a premise.
