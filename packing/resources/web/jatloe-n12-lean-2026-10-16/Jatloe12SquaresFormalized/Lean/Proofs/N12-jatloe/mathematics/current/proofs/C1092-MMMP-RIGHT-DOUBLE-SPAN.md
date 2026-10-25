# C1092 MMMP: a right wall reaching downward must span both directions

All decimals are exact rational numbers. Every owner is an actual original open square of common side 1<a≤1.001. Owned points are strict; all exclusions and separating supports may be equality.

**Theorem.** In the original MMMP sector, if Q10 strictly owns G8=(3,1.6), then it also strictly owns G9=(3,2.4). More precisely, in this branch

    Q10 has exactly label787200={F8,F9,G8,G9},
    {3}×[1.6,2.4] is strictly in Q10,
    Q5 strictly owns F4,G6 and has a strictly positive canonical angle,
    Q6 has exactly label131200={F7,G7}.

The conclusion is a further exact branch reduction. It does not assert that this remaining double-span arrangement exists or is already excluded.

## 1. The actual owner consequences before the support argument

The MMMP core and right-inner exclusion give F9 strictly in Q10 and G6 excluded from Q10. The unconditional theorem `C1092-MMMP-BOTTOM-ORDINARY-PAIR.md` gives F6,G5 strictly in Q9. Also F7 is strictly in Q6.

Require F9,G8 in the original Q10 component list, and remove components meeting the actual foreign F6,F7,G6. The only two components left are

    262912={F8,F9,G8},
    787200={F8,F9,G8,G9}.                              (1)

In particular F8 belongs strictly to Q10. The southeast Q5's original F-covering row {F4,F6,F8} therefore forces F4; its original G-covering row {G5,G6,G8} forces G6. Thus

    F4,G6 strictly in Q5.                              (2)

The completed northwest-center theorem gives (2,2) strictly in Q7, so it is excluded from Q5. Corollary 3 of `C1092-MMMP-SOUTHEAST-CENTER-REDUCTION.md`, applied with (2) and the actual Q10-owned G8, shows that Q5 has a strictly positive original canonical angle. The nonpositive original angle has already been excluded by the actual bottom/right wall supports in that theorem.

## 2. An omitted G9 supplies exactly the opposite-center wide-wall theorem

Suppose G9 were excluded from Q10. Work simultaneously in the reflected chart

    (xi,eta)=(x−2,2−y).

The actual C=Q5 has a strictly negative canonical frame u=(c,−s),v=(s,c), c≥s>0, with lower faces U,V. Its strict inward anchors and its genuine exclusions have the following sources:

| Local datum | Original point | Actual source |
|---|---|---|
| Strict M=(.35,.35) | Southeast marker | Q5 |
| Strict P=(0,.26), Q=(.26,0) | F4,G6 | Q5 by (2) |
| Excluded O=(0,0) | (2,2) | Actual Q7 |
| Excluded R=(1,.4) | G8=(3,1.6) | Actual Q10 |
| Excluded A=(.4,1) | F6=(2.4,1) | Actual Q9 |
| Excluded N=(−.35,.35) | Southwest marker | Actual Q4 |

The face proof in Proposition 3 of `C1092-MMMP-INWARD-CENTER.md`, used only up to its label-free face conclusion, gives

    U≥−.35(c+s), V≥0,
    U+a≤c−.4s, V+a≤c+.4s,
    0<z=s/(1+c)<.4.                                  (3)

For clarity, its starting missing-O exit is lower v; R is upper u; A is upper v; and the excluded marker N is lower u. The two alternative opposite-face widths are bounded by .6sqrt(2) and sqrt(.985), both less than one. These deductions use precisely the strict/excluded points in the table.

Now apply Theorem 2 of `MIXED-WALL-HALFANGLE-CROSSING.md` to C and the same actual W=Q10. Its complete actual input table is

| Wide-wall premise | Original actual source |
|---|---|
| S=(1.086,0) strict | Original right marker (3.086,2) in Q10 |
| T=(1,−.39) strict | Direct wall-sign endpoint (3,2.39) in Q10 |
| B=(1,.4) strict | G8 in Q10, this theorem's branch premise |
| E=(1,−.4) excluded | G9, the present supposed absence from Q10 |
| M=(.35,.35) excluded | Southeast marker, strict in actual Q5 |
| Real wall xi≤2 | Original right wall x≤4 |
| Center ordinate at most zero | Original MMMP sign Y10≥2 |

All its conditions, including the common side cap, are therefore literal original or proved facts. That continuous two-square theorem gives

    (z,1) strictly in the same actual C.                (4)

## 3. The actual bottom square excludes the downstream support

Transpose the whole chart by (X,Y)=(eta,xi). The same actual C now has positive frame (c,s),(−s,c), lower faces L=V,H=U, and satisfies

    L≥0, H≥−.35(c+s), 0<z<.4.

It owns the interchanged P,Q and Z=(1,z). It also strictly owns E_C=(.35,.65): its lower longitudinal band follows from M, its lower transverse band follows from P since .39c−.35s>0, and its upper bands follow from

    .35c+.65s≤sqrt(.545)<1<a+L,
    v(E_C)−H≤c≤1<a.

In this transposed chart the actual bottom Q9 strictly owns

    (1.086,0), (1,.4),

coming from its original marker (2,.914) and the already proved F6=(2.4,1). Its genuine original bottom wall y≥0 becomes X≤2. Thus Lemma 2 of `C1092-MMMP-FULL-INWARD-CENTER.md` applies exactly to this actual C and Q9. It uses neither a center sign nor a backward auxiliary exclusion on Q9. Its complete full-square support proof excludes the pair, contradicting their disjoint interiors.

The supposed absence of G9 was therefore impossible. Hence G9 is strict in Q10. The two alternatives in (1) reduce to exactly787200, and convexity joins its strict G8,G9 into the whole stated vertical bar.

Finally Q6 already owns F7,G7 and excludes G6 by `UNIT-SPAN-BETWEEN-TWO-BARS.md`. Its last optional G9 is now strictly in Q10. The exact remaining core labels {131200,196736,655488} therefore reduce to131200. This proves all the conclusions. ∎

The proof explicitly retains the opposite center sign of the actual right wall after reflection. It is the proved mixed-wall crossing theorem, rather than the earlier crossing theorem with the other center sign, that supplies (4). No absent auxiliary has been assigned a new owner.
