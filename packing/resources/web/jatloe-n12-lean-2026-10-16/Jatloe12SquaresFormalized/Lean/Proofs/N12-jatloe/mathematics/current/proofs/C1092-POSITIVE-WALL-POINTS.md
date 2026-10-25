# C1092: every positive central owns the corner-transfer point, and every wall point follows

All terminating decimals denote exact rationals. Owned points are strictly inside their named actual open square. Excluded points and separating supports may be tangent. The actual squares have one common side a>1, disjoint interiors, and their original container walls. No upper bound on a, coordinate enclosure, or initial boundary-angle bound is used below.

## 1. Exact scope and the completed positive entrance

Retain the last C1092 MPPM auxiliary assignment

    (0,0,0,0,9217,32848,590336,16424,2050,4100,262400,131200).

Let R(x,y)=(4−y,x). In the chart R⁻ⁱ, the actual local owners are

    C_i=Q_(4+i), K_i=Q_i,
    (B₀,B₁,B₂,B₃)=(Q₉,Q₁₀,Q₁₁,Q₈),

with all indices interpreted cyclically. Suppose the four central canonical angles are strictly positive. The unconditional D-exclusion theorem in `C1092-POSITIVE-D-TRANSFER.md` and Theorem 1 of `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md` then apply directly to these actual owners. In each local chart they give

    0<tan(p_C/2)<1/5,
    |tan(β_B/2)|<1/3,
    L''=(107/75,1) strictly in B,
    X=(1.5,2) strictly in C,
    center(C)_x<1.5<center(C)_y.                       (1)

In particular, no ownership of P=(2,1) was assumed in deriving any of (1).

**Theorem 1.** Under these actual hypotheses, every local central C strictly owns H=(1,1.5), and every local boundary B strictly owns P=(2,1). Consequently every negative boundary canonical angle satisfies

    |tan(β_B/2)|<1/8.                                  (2)

Together with (1), this gives the full asymmetric angle domain

    0<tan(p_C/2)<1/5,
    −1/8<tan(β_B/2)<1/3.                              (3)

All these statements are conclusions from the original last assignment and the strictly positive central signs.

## 2. A missing H has only one possible face

Write u=(c,s), v=(−s,c), with c≥s>0 and c²+s²=1, for the actual C. Let U,V be its lower face values. Its original strict points include

    M=(1.65,1.65), U₀=(1,1.74),
    L₀=(1,1.6), T=(1.74,2).

The original preceding central marker N=(1.65,2.35) belongs to a distinct actual square, so N is outside C.

Suppose H were outside C. Its upper u-band is strict by comparison with M, since

    u(M)−u(H)=.65c+.15s>0.

Its upper v-band is strict by comparison with L₀, since

    v(L₀)−v(H)=.1c>0.

Thus H can exit only through a lower face. If it exits through lower v, then strict M implies

    V≥v(H), V<v(M),
    .15c−.65s>0, hence s/c<3/13.                     (4)

Both lower bands of N are strict, using U₀ and M respectively. Its upper u-band is also strict: under (4),

    u(N)−u(T)=−.09c+.35s
      <c(−.09+.35·3/13)<0.

Therefore N must exit through upper v. The opposite v-faces at H and N would give

    a≤v(N)−v(H)=.85c−.65s≤.85<1,

which is impossible. A missing H is consequently forced through lower u:

    U≥u(H)=c+1.5s.                                    (5)

This elementary face statement holds over the full positive canonical interval; it does not require a small-angle hypothesis.

## 3. The next actual crosspoint makes that face impossible

The bootstrap established X=(1.5,2) strictly in every central square before P was known. The next actual central therefore strictly owns the transported point

    E'=R(X)=(2,1.5)

in the current chart. It is genuinely foreign to C. Section 7 of the bootstrap proves its forced upper-u exit,

    U+a≤u(E')=2c+1.5s.                               (6)

For clarity, that exit follows from strict M and T, the already proved exclusion of D=(1,2), and the central bound in (1). E' has its lower u and upper v bands strict; a lower-v exit opposing D would imply a≤.5c+s≤11/13<1. Thus (6) retains every possible exit and includes boundary tangency.

If H were missing, (5) and (6) would now give

    a≤u(E')−u(H)=c≤1,

again impossible. Hence H belongs strictly to every C. The conclusion is strict because every point outside the open square, including its boundary, was covered by the contradiction.

## 4. The actual corners transfer all four wall points

Every local paired corner K strictly owns (1,.914) and (1,1), has its closure in the actual local first quadrant, and is distinct from C. The just-proved strict ownership of H by C makes H outside K. The actual boundary B strictly owns (2,.914) and (1.6,1), and its closure lies above the actual bottom wall.

These are precisely the hypotheses of Theorem 7 of `C1092-DIRECT-WALL-POINT.md`, with

    b=.914=457/500, ell=1.6=8/5.

That all-angle theorem applies to the actual common-side pair K,B and proves P=(2,1) strictly in B. No angle information about K or B is required for this transfer.

The full owner ledger is:

| Chart i | Actual central C | Actual corner K | Actual boundary B | Strict H in original coordinates | Strict P in original coordinates |
|---|---|---|---|---|---|
| 0 | Q4 | Q0 | Q9 | (1,1.5) | (2,1) |
| 1 | Q5 | Q1 | Q10 | (2.5,1) | (3,2) |
| 2 | Q6 | Q2 | Q11 | (3,2.5) | (2,3) |
| 3 | Q7 | Q3 | Q8 | (1.5,3) | (1,2) |

All rows are transported by the same quarter-turn R, including the squares and real walls. No exclusion is supplied by a hypothetical owner.

Now that each actual B strictly owns P, Theorem 2 of `C1092-POSITIVE-QUADRANT-BOOTSTRAP.md` gives (2) for every negative boundary angle. Combining it with the positive branch of (1) proves (3), completing Theorem 1. ∎

## 5. What remains after this entrance

Every sign pattern containing a nonpositive central angle is already impossible by `C1092-DIRECT-NEGATIVE-CYCLE.md` and `C1092-DIRECT-MIXED-CYCLE.md`. The present theorem supplies all four strict H and P points in the only remaining sign pattern. Thus there is no remaining missing-wall-point branch of the actual last assignment.

The next task for that assignment is a final contradiction in the all-positive regime, using the proved center quadrants, points, and angle domain (3). The twelve wall remainder signs already hold on exactly this wider domain by Theorem 2 of `C1092-WALL-REMAINDERS.md`. Their actual separating-normal sources and unequal-angle transport must still be justified in a final cyclic inequality. The earlier positive-cycle theorem's smaller central cutoff 7/64 is not inferred here.

This chapter closes the positive point-transfer and quadrant entrance. It does not assert that the whole C1092 simplification program, or the earlier reduction to the last auxiliary assignment, has been completed.
