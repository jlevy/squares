# Two short corner gaps exclude an outward central square

All terminating decimals denote exact rational numbers. Every owned point is strictly inside the actual open square; an excluded point may lie on a face. No wall, center bound, upper side bound, or additional square is a premise of the theorem.

**Theorem 1.** Let 0<r,t<.4 and suppose

    (1−r)²+(1−t)²≤1.                                (1)

No open square Q of side a>1 can strictly own

    M=(.35,.35), A=(.4,1), B=(1,.4)

while excluding all three points

    F=(r,1), G=(1,t), K=(1,1).                       (2)

**Proof.** First use a nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1,

and let U,V be the lower face coordinates.

At K its lower u-band follows strictly from A. Its lower v-band follows strictly from B, and its upper v-band follows strictly from A, because

    u(K)−u(A)=.6c>0,
    v(K)−v(B)=.6c>0,
    v(A)−v(K)=.6s≥0.

Consequently K must exit through its upper u-face:

    U+a≤c+s.                                        (3)

At G, both upper bands follow strictly from B. Its lower u-band follows strictly from M: indeed

    u(G)−u(M)=.65c+(t−.35)s>0.

If t≥.35 this is immediate. If t≤.35, use s≤c to bound it below by (.30+t)c>0. Thus G can fail only its lower v-band, giving

    V≥−s+tc.                                        (4)

At F, its upper u-band and lower v-band follow strictly from A:

    u(A)−u(F)=(.4−r)c>0,
    v(F)−v(A)=(.4−r)s≥0.

If F failed its lower u-band, (3) would give opposed-face width

    a≤u(K)−u(F)=(1−r)c<1,

which is impossible. Hence F exits through its upper v-face:

    V+a≤c−rs.                                       (5)

Combining (4) and (5), and then applying (1), gives

    a≤(1−t)c+(1−r)s
      ≤sqrt((1−t)²+(1−r)²)≤1,

a contradiction.

For a nonpositive canonical angle, reflect Q and all six points simultaneously across x=y. This exchanges A with B, F with G, and r with t; M and K are fixed. It converts the frame to a nonnegative canonical frame after relabeling its two axes. All hypotheses, including (1), are invariant under this exchange, so the proof just given applies. The axial and diagonal endpoints are included, and all exterior contacts were weak. ∎

## Exact useful instances

The theorem applies whenever the two foreign gaps use any of the following pairs, or their exchange:

| r | t | (1−r)²+(1−t)² |
|---|---|---|
| .39 | .39 | .7442<1 |
| .26 | .39 | .9197<1 |
| .26 | .35 | .9701<1 |
| .30 | .30 | .98<1 |

In the original C1092 MMMM class, use the translation by (2,2), with r=t=.39. The strict marker of northeast Q6 is M+(2,2), and its outward auxiliary pair would be A+(2,2)=F7 and B+(2,2)=G9. The two foreign points F+(2,2)=(2.39,3) and G+(2,2)=(3,2.39) belong to the actual top and right wall owners by `C1092-WALL-SIGN-CHORD.md`. The excluded K+(2,2)=(3,3) belongs to the actual paired corner Q2. Thus Q6 cannot own both F7 and G9 in any original auxiliary alternative.

The asymmetric instances retain their individual actual exclusions and are available when only one wall supplies a longer strict chord. No whole segment between different owners is used in this argument.
