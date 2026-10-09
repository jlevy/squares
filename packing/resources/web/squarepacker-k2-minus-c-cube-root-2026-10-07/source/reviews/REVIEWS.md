# Reviews and tests of this preprint (all by AI systems)

The paper has not been peer reviewed, and no human has reviewed it. Everything below was done with AI systems (Claude, Anthropic) and computer programs. All reviewers are AI systems of the same family and may share blind spots.

## Reviews of the argument

1. **First blank-slate review (of a first draft of the argument).** The reviewer read the draft, the cited statements of [Q] and [R], and, where the draft relies on their generality, the proofs; in particular the proof of [R, Lemma 4.13] (that it holds for an arbitrary measurable set Y and function β) and the proofs of [Q, Theorems 6.9 and 8.3]. Result: no critical or major issue; 12 minor ones. Among them:
   - a missing hypothesis (E* < 1 − ν₀);
   - a sketched final deduction, now written out as Proposition 6.1;
   - slightly low values of the asymptotic constant;
   - an exact count (k − 6) where the draft had (k − 8).

   All 12 were addressed.
2. **Second blank-slate review (of the corrected draft).** Same scope, with an independent recomputation of the explicit cases in exact rational interval arithmetic (now `code/check_table_exact.py`). Result: no critical or major issue; 6 minor ones, all addressed:
   - citations;
   - the ceiling case of Lemma 4.1;
   - the measurability of the shadow;
   - wording.

   It also noted that one case of Table 1 (case 6) satisfies its condition (iv) with a small slack (34934.224 against 34934.664). The check is rigorous in all programs.
3. **Third blank-slate review (of a draft of this text).** The reviewer checked every cited statement number against the sources and recomputed Table 1 and the numbers quoted in the text with an independent program (now `code/check_table_exact2.py`). Result: no critical or major issue; 12 minor ones, all addressed:
   - notation clashes;
   - the explicit justification of choosing the threshold θ from W;
   - the status of the literature on s(k²−1) and s(k²−2);
   - wording of the remarks;
   - completeness of the abstract.

4. **Fourth blank-slate review (of the version of this text prepared for release).** It was made in a separate session, by a lead reviewer and five independent agents with separate scopes:
   - [Q] Sections 3–4;
   - [Q] Sections 5–8;
   - the citations of [R] and the main inequality;
   - the constants and Table 1;
   - an adversarial reading of the whole text.

   The agents did not see each other's conclusions. The review:
   - checked 49 citations of [Q] against [Q]'s numbering by script and found no mismatch;
   - compared the quotations of [R] with [R] letter by letter;
   - checked that [Q] Theorems 6.9, 7.1, 8.3 and Proposition 5.10 apply to the master flow with a very small threshold;
   - recomputed Table 1, every constant and the numbers in the text with several new implementations (interval and exact rational arithmetic).

   Result: no critical or major issue; 10 minor ones, all addressed:
   - one displayed number rounded in the wrong direction (34934.22, now 34934.23; the condition it supports holds with slack 0.44);
   - a missing hypothesis k ≥ 2 in the abstract;
   - an undefined symbol (S for S_K);
   - an explicit statement that the analytic variant uses A₁₃ and A′₁₃ throughout;
   - incomplete citations (Lemma 4.7(a)–(c) of [Q]; Lemma 3.8, Lemma 3.17(f), Definitions 3.32 and 6.6, Remarks 2.2 and 6.13 of [Q]; Lemma 3.1(a) of [R]);
   - a shortened quotation of [Q, Remark 6.13];
   - "a set of squares of 𝒫" in Lemma 4.3;
   - the caveat that the upper bound O(k^{3/5}) rests on preprints that have not yet been refereed;
   - notation shared with [Q] that has a different meaning here.

   It also pointed out small margins: cases 4 and 8 of Table 1 hold with relative margin about 0.5%, and condition (iv) of case 6 with relative margin 1.3·10⁻⁵. These margins assume the constants of [Q] and [R] as stated.

## Programs

- `code/check_table_iv.py`: mpmath interval arithmetic.
- `code/check_table_exact.py` and `code/check_table_exact2.py`: exact rational arithmetic. They were written by the second and the third reviewer, from the statements and independently of the first program and of each other.

All three confirm the eight cases of Table 1. The table entries are rounded outwards.

## Numerical test on scaled analogues

**What was tested.** The lemmas of Sections 3–5 and Theorem 5.1, on scaled analogues of the construction:
- k = 14 and 16;
- inclinations 0.01–0.34 instead of at most 1.5·10⁻⁶;
- δ ∈ {1/20, 1/10}.

The constants of [Q] and [R] were replaced by values measured on the same packing.

**How.** 2,560 closed packings in 11 families, each verified exactly in rational arithmetic. The flow was traced exactly in rational arithmetic, giving:
- 893,085 path pieces;
- 1.49 million entry candidates;
- 311,040 line samples.

The tracer was cross-checked against an independent exact point tracer and against an earlier floating-point tracer.

**Result.** No counterexample, and every negative control (removing one hypothesis or one term) made the corresponding check fail. A notable detail is that in the top-ramp case of Lemma 4.1 the term 1 − cos a is really needed for large a. In the paper, the hypothesis a ≤ 2·10⁻⁴ covers it.

**Limitations.** Such a test cannot check the constants of [Q] and [R], and at this scale several inequalities have structural slack. The final step of Theorem 5.1 was exercised in only 12 of the packings.

## Corrections made along the way

- A consequence stated in an early draft ("W ≥ 2 for k ≥ 10⁸, i.e. s(k²−1) = k") was withdrawn because it is not new: s(k²−1) = s(k²−2) = k is known for all k (see [R, Section 1]).
- Some entries of Table 1 were first rounded in the unsafe direction: two upper bounds, and the lower bounds 0.665 and 0.6664. They were corrected before the third review, which confirmed that all entries are rounded outwards.

## What a human review should look at first

- Lemma 3.1 of the paper: the use of [R, Lemma 4.13] for the union of the height intervals of one path.
- [R, Lemma 4.13], and for Theorem 1.1 the computer-assisted [R, Lemma 4.10].
- [Q, Sections 3–8]: the flow, the height identity, the shadow inequality (Theorem 6.9) and the termination bounds (Proposition 5.10, Theorems 7.1 and 8.3).
