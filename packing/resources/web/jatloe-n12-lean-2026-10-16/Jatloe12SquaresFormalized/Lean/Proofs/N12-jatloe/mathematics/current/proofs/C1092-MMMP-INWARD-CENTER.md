# C1092 MMMP: two direct sectors for the northwest center point

All decimals are exact rationals. The proof retains the original actual square owners and weak exclusions. No orientation interval or numerical center history is used.

## 1. A strict-bar center lemma

**Theorem 1.** Let C be an open square of side a>1 with a nonnegative canonical frame

    u=(c,s), v=(−s,c), c≥s≥0, c²+s²=1.

Suppose C strictly owns

    M=(.35,.35), P=(0,.26), Q=(.26,0),

and excludes A=(.4,1), H=(.56,1), and the entire segment

    I={1}×[0,.39].

Then C strictly owns O=(0,0).

The whole segment is an actual exclusion premise; excluding its endpoints independently would not suffice.

**Proof.** Write U,V for the lower faces of C. If O were absent, its upper u-band follows from M and its two v-bands follow from P,Q. Therefore

    0≤U<u(P)=.26s.                                  (1)

In particular s>0. At A its lower u-band follows from M and its lower v-band from Q. Its upper u-band follows from (1), a>1, and

    u(A)=.4c+s≤1.4/sqrt(2)<1.

Consequently A exits upper v:

    V+a≤c−.4s.                                      (2)

Put z=s/(1+c), so 0<z≤sqrt(2)−1 and

    c+sz=1, −s+cz=−z.                               (3)

First suppose z≥.39. The point R=(1,.39) is strict in C. Its lower u-band follows from Q. Its upper u-band follows from c+.39s≤c+zs=1<a+U. Its upper v-band follows from P, since z≥.39 implies s/c≥.78/(1−.39²)>.13 and hence −s+.39c<.26c. For its lower v-band, (2) and a>1 give

    v(R)−V>1−.61c−.6s
              ≥1−sqrt(.61²+.6²)=1−sqrt(.7321)>0.

Thus R is strict in C, contrary to the exclusion of I.

It remains that 0<z≤.39. Consider Z=(1,z), which lies on I. By (3), its u-projection is exactly 1 and its v-projection is −z. Therefore its lower u-band follows from Q, its upper u-band from (1) and a>1, and its upper v-band from P. We show its lower v-band in two elementary regimes.

If s+.4c≥.6, then

    c−.4s+z−1=z(.6−s−.4c)≤0.

Equation (2) therefore gives V<c−.4s−1≤−z=v(Z), as required.

If s+.4c≤.6, use the other excluded point H. Its lower u-band follows from M and its lower v-band from Q. Its upper u-band follows from

    u(H)=.56c+s≤.6+.16c≤.76<1<a+U.

Thus H too exits upper v, giving V+a≤c−.56s. The function s+.56c increases over the canonical interval and is at least .56. Hence

    c−.56s+z−1=z(.44−s−.56c)<0.

Again V<−z, proving the last strict band. Thus Z is strict in C in either regime, contradicting the whole excluded segment I. Missing O is impossible. The original axis s=0 was already contradicted directly by (1), so every nonnegative canonical orientation is included. ∎

## 2. Application to the whole original MMMP entrance

**Corollary 2.** In the original MMMP sector, Q7 strictly owns (2,2) whenever either of the following holds:

1. Q7 has a nonpositive canonical angle in the original container chart.
2. Q7 owns G1=(1,2.4), with no angle assumption.

**Proof.** For the first assertion, apply Theorem 1 in the simultaneous chart

    (ξ,η)=(2−x,y−2).

Reflection changes the sign of the canonical angle, so the hypothesized original nonpositive angle becomes the nonnegative frame of Theorem 1. The required strict and excluded points have the following actual sources:

| Theorem datum | Original point | Actual source |
|---|---|---|
| M | (1.65,2.35) | Original marker in Q7 |
| P | F5=(2,2.26) | Q7 by `C1092-MMMP-CORE-OWNERS.md` |
| Q | G3=(1.74,2) | Q7 by the same core theorem |
| Excluded A | F3=(1.6,3) | Strict in Q11 by the core theorem |
| Excluded H | (1.44,3) | Strict in Q11 by `C1092-MMMP-WALL-TRANSFER.md` |
| Whole excluded I | {1}×[2,2.39] | Strict in the one actual Q8 by the wall-transfer theorem |

Every listed exclusion is therefore genuine for Q7. The target O is the original point (2,2), proving the first assertion.

The second assertion is exactly Corollary 2 of `INWARD-EXTENDED-ANCHOR-CENTER.md`, whose actual source table starts from the same original MMMP core and the original wall-center sign Y8≥2. It includes all canonical angles and retains its explicit G1 ownership premise. ∎

## 3. Exact face profile of any remaining missing center

The following additional reduction keeps the exact original labels visible.
It does not assert the impossibility of the remaining face profile.

**Proposition 3.** If the original MMMP square Q7 does not strictly own
(2,2), then its original canonical angle is strictly positive and its
exact original auxiliary label is 8224, namely precisely F5 and G3.
In the simultaneous chart

    (ξ,η)=(2−x,y−2),

write its negative frame as u=(c,−s), v=(s,c), with c≥s>0,
c²+s²=1, and lower faces U,V. It satisfies

    U≥−.35(c+s),       V≥0,
    U+a≤c−.4s,        V+a≤c+.4s.                    (4)

In particular its half-angle z=s/(1+c) obeys 0<z<.4.

**Proof.** Corollary 2 already shows that the original angle is strictly
positive and that G1 is excluded. If F4 were also owned by Q7, the
strict segment F4–F5 would contain (2,2); if G6 were owned, the strict
segment G3–G6 would contain it. Thus F4 and G6 are excluded as well.

In the displayed chart, the strict points are

    M=(.35,.35), P=(0,.26), Q=(.26,0),

and the excluded points used next are

    R=(1,.4), A=(.4,1), N=(−.35,.35).

Here R is the just-established absence of original G1; A is original
F3, strictly in the actual top square Q11; and N is the original
northeast marker, strictly in Q6. All are genuine exclusions from Q7.

The two u-bands of O=(0,0) are strict by P,Q, and its upper v-band
is strict by M. Thus missing O forces

    V≥0, V<v(Q)=.26s.                              (5)

For R, its lower u-band follows from Q since .74c−.4s>0, and its
lower v-band also follows from Q. Its upper v-band is strict because

    v(R)=s+.4c≤.7(c+s)≤.7sqrt(2)<1<a+V.

Consequently R exits upper u, giving the first upper-face bound in (4).

At A, its lower v-band is strict by M. A lower-u exit would combine
with R's upper-u exit to give

    a≤.6(c+s)≤.6sqrt(2)<1,

which is impossible. We also exclude an upper-u exit of A. Such an
exit, by strict ownership of M, would require

    .35(c−s)<.4c−s, hence s/c<1/13.                 (6)

The excluded N has both upper bands strict by M, so it exits lower u
or lower v. In the latter case, (5) would imply

    .35(c−s)<.26s, hence s/c>35/61,

contradicting (6). In the former case, an upper-u A and lower-u N
would give

    a≤u(A)−u(N)=.75c−.65s≤.75<1.

Thus neither u-face is an exit for A, and A must exit upper v:

    V+a≤c+.4s.                                    (7)

Now N cannot exit lower v, for that would combine with (7) to give

    a≤.65c+.75s≤sqrt(.65²+.75²)=sqrt(.985)<1.

It therefore exits lower u, proving the remaining lower bound in (4).
The bounds V≥0 and (7), together with a>1, imply c+.4s>1.
Since

    c+.4s−1=2z(.4−z)/(1+z²),

we obtain z<.4.

Finally Q7 cannot own F0 or G0. In the current chart these are
F0=(1,−.26) and G0=(1,−.4). Their respective u-projection
differences from the strict P are c+.52s and c+.66s. Simultaneous
ownership of either with P would make that difference less than a.
But (5) and (7) give a≤c+.4s, a contradiction since s>0.

For completeness, the exact-label inspection uses only the supplied
original single-cover lists. Requiring F5 while excluding the actual
foreign F1,F3,F7 (in Q8,Q11,Q6 respectively), and the proved absent
F0,F4, leaves exactly {F5}. Requiring G3 while excluding the actual
foreign G4,G7 (in Q11,Q6 respectively), and the proved absent
G0,G1,G6, leaves exactly {G3}. The combined label is
32+1024·8=8224. ∎

## 4. Remaining scope

This chapter reduces every possible missing center to the positive
original angle, exact label 8224, and face profile (4). The companion
`C1092-MMMP-FULL-INWARD-CENTER.md` then excludes that entire profile
using the full actual Q8 and Q11 supports. Thus the complete current
argument gives (2,2) strictly in Q7 throughout MMMP. The reduction here
remains a separate proved implication, and none of its actual-square
premises is replaced by independent point exclusions.
