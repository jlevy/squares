# C983 F5-only: exclusion of the pure lower right-wall component

All owned points retain their actual open-square owners, exclusions allow tangency, and the original common side satisfies a>1. The entrance is the audited owner reduction `C983-F5-CENTRAL-REDUCTION.md` together with the merged-center theorem `C983-F5-MERGED-CENTER.md`.

**Theorem.** In merged label8224, the actual right-wall square cannot have component

    Q10=262400={F8,G8}.                            (1)

**Proof.** The direct single-owner reduction in Section 4 of `C983-F5-CENTRAL-REDUCTION.md` shows that (1) leaves

    Q5=65552={F4,G6}
    or Q5=66064={F4,F9,G6}.                       (2)

Thus F4,G6 and the southeast marker all belong strictly to this one actual Q5.

Apply the ordinary two-wall center theorem, reproduced with its full continuous proof in Section A of `C981-RETAINED-CONTINUOUS-LEMMAS.md`, after reflecting its entire configuration in y=2. Its actual squares are A=Q5, R=Q10 and T=Q9. The complete literal source table is:

| Ordinary theorem datum | Reflected original C983 datum |
|---|---|
| A owns P=(2,2.26) | F4=(2,1.74), owned by Q5 in both alternatives (2) |
| A owns Q=(2.26,2) | G6=(2.26,2), owned by Q5 |
| A owns M=(2.35,2.35) | The southeast marker (2.35,1.65) in Q5 |
| A excludes G=(2.35,1.65) | The northeast marker (2.35,2.35) strictly in actual Q6 |
| A excludes B=(1.65,2.35) | The southwest marker (1.65,1.65) strictly in merged Q7 |
| R owns N_R=(3.086,2) | The original right-wall marker in Q10 |
| R owns H_R=(3,2.4) | G8=(3,1.6), owned by Q10 in (1) |
| R excludes (3,1.74) | F9=(3,2.26), omitted by the exact Q10 component (1) |
| T owns N_T=(2,3.086) | The original bottom-wall marker (2,.914) in Q9 |
| T owns H_T=(2.4,3) | F6=(2.4,1), owned by every original Q9 component |
| T excludes (1.74,3) | G2=(1.74,1), strictly in actual singleton Q0 |
| R's genuine wall x≤4 | The original right container wall |
| T's genuine wall y≤4 | The reflection of the original bottom container wall y≥0 |

All three named squares have the same physical side a>1, and A has disjoint interior from each of the two actual wall squares. The source theorem does not require a side upper bound or any favorable orientation. It allows an auxiliary exclusion without a distinct owner, as used for F9 in the right-wall component.

Its strict conclusion is therefore

    (2,2) ∈ Q5.                                  (3)

But the universal merged-center theorem gives

    (2,2) ∈ Q7 strictly.                          (4)

The two actual squares Q5 and Q7 are distinct and have disjoint interiors. Equations (3),(4) contradict this. Hence (1) is impossible. ∎

The remaining necessary right-wall alternatives in label8224 are consequently

    524800={F9,G9},
    262912={F8,F9,G8},
    525056={F8,F9,G9},
    787200={F8,F9,G8,G9}.

All four now own F9. In particular every remaining actual Q6 owns F7 and omits F9; its only necessary components are 131200={F7,G7}, 524416={F7,G9} and 655488={F7,G7,G9}, with the latter two possible only when Q10=262912. This final observation is the direct restriction of the original single-owner lists already displayed in the central reduction. It is not a separate jointly enumerated catalogue.
