# Record Changes Drafted by the Stage 4 Review of Theorem A (#797)

Drafts for the records lane, from the review of 25 October 2026
([docs/project/reviews/review-2026-10-25-fang-theorem-a.md](../../../../../../docs/project/reviews/review-2026-10-25-fang-theorem-a.md)).
Nothing here is applied: a records lane applies, adjusts or declines each item and
commits it. The paths are repository-relative, and the YAML is written to the schemas at
PR #801’s head `a3e826606`.

## 1. `packing/frontier/verifiers.yaml`: the Three Deciding Programs

`fang_a_squeeze_conditions.py` and `fang_a_case_bounds.py` decide nothing about the
theorem and are not registered; the README says so.

```yaml
  - id: V-fang-797-review-identities
    program: fang_a_identities.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      Decides symbolically, with sympy's simplification of rational functions to zero,
      every identity and polynomial inequality Kevin Fang's Theorem A note (v0.2) uses for
      every b, k and t: the band geometry (R1)-(R3) and (E1)-(E3), the closeness
      conditions at t0 = 1/b with 2b(b^2+1) delta_b = (b-1)(b^2-2b-1), the floor pairing
      of Lemma 2 (also on an exact rational grid with its ties), Lemma 3 as the polynomial
      identity bL - C_lower - RHS(2) = F(bc - 2 tau), the values at t0, H(1/b) = B(k), the
      final 6b^4 - b^3 - 2b^2 - b > 0, and the sharpness remark's expansion; 46 checks,
      and four mutated identities refused.
    source:
      - packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/programs/fang_a_identities.py
    independence_record: >-
      packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/README.md
    independence:
      read: [mathematics, proof-text, earlier-review]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane c-review-797-math of the #797 import
            (think-qmqq) for the intake pass coord-intake-1024, tbd-strong-max tier,
            maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The note's acknowledgement says its construction code, checkers and
          certificates were written and run with Claude (Anthropic), directed and
          reviewed by Kevin Fang. Written by a Claude agent from a prompt of its own, in a
          file that imports nothing from the source or this repository.
      note: >-
        Written from the note's text (main.tex, SHA-256 f6f26d7b...1152). Its authors
        never opened the source's lband.py, windowed_check.py, regenerate.sh or
        certificates. Before writing they had read the packet README and the register row,
        which summarise the maintained fang_theorem_a.py's results, and knew the stage 1
        triage had found no gap (earlier-review); they read that module, its receipts and
        the triage's notes only after the review's findings were written.
    note: >-
      Written and run on 25 October 2026 by the stage 4 review of Kevin Fang's Theorem A;
      kept in the packet's review/review-2026-10-25/ with its README and receipts, whose
      outputs/program-digests.sha256 records the SHA-256 that ran
      (4fc91df0eae975160014929bccbe318f198f2d33114c4e578dfd6ae03322e2c3, unchanged since it
      decided).

  - id: V-fang-797-review-construction
    program: fang_a_review.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      Builds Kevin Fang's Theorem A construction (Ryu's L with both band ends filled by
      axis-parallel rows, odd b with |b - sqrt(2k)| <= 1) from the note in exact
      rationals and decides, at a close rational t for each (k, b), conditions (a)-(d),
      S < k, identity (1), Lemma 2 at all four ends, Lemma 3 for both bands, w < H(t) and
      w, H(t) and B(k) below 4 sqrt(2k) + 2; the one-sided limit count as t -> 1/b+ by
      exact power series; Lemmas 2 and 3 and (E2) at sampled close t, lifts and lengths;
      every square of chosen packings by exact separating axes, with mutants refused; the
      ties k = 2m^2; and the sharpness remark.
    source:
      - packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/programs/fang_a_review.py
    independence_record: >-
      packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/README.md
    independence:
      read: [mathematics, proof-text, earlier-review]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane c-review-797-math of the #797 import
            (think-qmqq) for the intake pass coord-intake-1024, tbd-strong-max tier,
            maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The note's acknowledgement says its construction code, checkers and
          certificates were written and run with Claude (Anthropic), directed and
          reviewed by Kevin Fang. Written by a Claude agent from a prompt of its own, in a
          file that imports nothing from the source or this repository.
      note: >-
        As V-fang-797-review-identities: written from the note's Sections 2 to 5, never
        reading the source's programs or certificates; the packet README's summary of the
        maintained module's results was read first, the module itself only after the
        findings.
    note: >-
      Written and run on 25 October 2026 by the stage 4 review of Kevin Fang's Theorem A;
      kept in the packet's review/review-2026-10-25/ with its README and receipts. SHA-256
      that ran: 6b0e079306dad85d239e46aa5bfdebcfffbbd9506800172febc71c5dc8c721bf,
      unchanged since it decided.

  - id: V-fang-797-review-comparisons
    program: fang_a_comparisons.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic, numerical-multiprecision]
    role: decides
    summary: >-
      Decides in integers, one k at a time with the tail lemmas it prints, the
      comparisons of Fang's Theorem A note (Section 7 and the abstract) with Evan Daniel's
      4 ceil(sqrt(2k-7)) - 1, Ryu's Theorems 1.3 (at its best b), 1.4, 1.2 and 1.6 and
      T-163, and the register's count of k at which Theorem A is strictly the least
      statement in [42, 702000]. Daniel's k^{2/5} bound and Ryu's Theorem 1.2, which have
      real constants, are evaluated in mpmath at 50 digits, refused within 1e-30 of an
      integer, and exactly at perfect fifth powers.
    source:
      - packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/programs/fang_a_comparisons.py
    independence_record: >-
      packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/README.md
    independence:
      read: [mathematics, proof-text, earlier-review]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane c-review-797-math of the #797 import
            (think-qmqq) for the intake pass coord-intake-1024, tbd-strong-max tier,
            maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The note's acknowledgement says its construction code, checkers and
          certificates were written and run with Claude (Anthropic). Written by a Claude
          agent from a prompt of its own, in a file that imports nothing from the source
          or this repository.
      note: >-
        Written from the note and the statements of the register's rows and Ryu's
        preprint v1.1. Revised once, after the review's findings and after its authors
        read the maintained fang_theorem_a.py and its receipts, to report the first k at
        which Daniel's k^{2/5} bound is smaller and its margin at 10^6 (digest before
        ea73666051b2163de9a3f6127bb9ff69d715e5548cb1222363ec31ed182ccdaf); the revision
        changed no decision and copies nothing of that module. The source's programs were
        never read.
    note: >-
      Written and run on 25 October 2026 by the stage 4 review of Kevin Fang's Theorem A;
      kept in the packet's review/review-2026-10-25/. SHA-256 that ran for the retained
      receipt: 0e3a7d566a568f2c09d73892f877f5ea2f63b1e38b838a53a48e507a1e786031.
```

## 2. The Evidence That Raises the Row

**Where the row’s assurance lives.** The deficiency rows of
`packing/frontier/asymptotic-waste-bounds.yaml` carry no evidence ids and no `reviews`
field, and the schema gives them none.
Ryu’s rows record their review and the checks done here in `note` and `corollary`, and
the Theorem A row (PR #801) says “The mathematical review of the note is pending
(think-4tj5)”. What raises the row is therefore its text.

### 2a. The row: replace the last two sentences of `note`, and fix `constant`

In the Theorem A row’s `note`, replace “The mathematical review of the note is pending
(think-4tj5). Not refereed; …” with:

```yaml
      The proof was re-derived in the stage 4 review of 25 October 2026,
      docs/project/reviews/review-2026-10-25-fang-theorem-a.md (accepted with findings,
      none blocking or major; Claude, strongest tier, maximum reasoning, prompted
      separately from the records lane): every identity and inequality of Sections 2 to 5
      decided symbolically, and the construction independently re-implemented clean-room
      from the note in exact rationals, deciding the bound with Lemmas 2 and 3 at every
      k from 6 to 250,000 at both odd widths, every square at 46 packings to k = 101, the
      ties k = 2m^2 to m = 1000 and the sharpness remark for odd b to 2001 (programs and
      receipts in the 24 October packet's review/review-2026-10-25/). Its two minor
      findings, the Section 6 squeeze example and the last sentence of Section 7, are
      the author's. Not refereed; the source states Claude assistance and two blind
      language-model reviews of the proof, which it says are not an external mathematical
      review. It settles no count n <= 324, so it is not in the result register.
```

In its `constant`, “each below 2bL/(b^2+1) + b + 2 - kappa_b, kappa_b = …, as t -> 1/b
(Lemma 2)” cites the band estimate by the record’s number.
The retained PDF prints it as Lemma 3, so either cite “Lemma 3” or say once that the
record numbers the lemmas from 1. Each band term is below the right side of (2) at $t$,
whose limit as $t \to 1/b$ is that value.
The same renaming applies to the packet README’s “Lemmas 1 and 2” and “Lemma 2 with
equation 1”. The `constant` text is held by `deficiency_family.py`’s `Statement`, so the
module changes with it.

In its `complementary_case`, “which a sampled integer check here finds not smaller at
702,000 and smaller at 748,000” can read “which is not smaller at any k below 735,988
and smaller at every k from 736,595 (decided one k at a time in the 25 October review’s
receipts)”.

### 2b. `packing/frontier/evidence.yaml`, if the record wants the run as an entry

`evidence.yaml` scopes every entry by count.
The counts at which the review’s run laid out every square are those of $k = 6$ to 18
(at both widths at $k = 8$ and 18): 26, 38, 50, 52, 66, 84, 105, 126, 151, 176, 205,
236, 268, 300 and 302. At every one of them both the reported and the verified upper
bound already lie below that $k$, by at least 0.12 (`outputs/case-bounds.json`), so no
case record would cite the entry.
`devtools.check_certificate_citations` would then need a deferral naming what cites it,
or a rule for theorem-level evidence.
That is the decision the triage also left open (“they have no `n_values` scope a case
record would cite”). The entry, if wanted:

```yaml
  - id: E-fang-theorem-a-review-construction-exact
    claim: upper-bound
    scope: {n_values: [26, 38, 50, 52, 66, 84, 105, 126, 151, 176, 205, 236, 268, 300, 302]}
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Fang Theorem A 2026-10-24]'
    replay: >-
      From any directory with the project interpreter (CPython 3.14.7) on a shared
      four-core host, under nice, on 25 October 2026: python3 -I
      packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/programs/fang_a_review.py
      geometry, which builds Kevin Fang's Theorem A construction from the note in exact
      rationals at k = 6 to 40, 50, 59, 72, 98 and 101, both odd widths at a tie, and
      decides every square inside [0, S]^2 with S < k, unit, pairwise disjoint interiors
      by exact separating axes over every pair whose centres are closer than sqrt 2, and
      the count equal to the note's formula: 46 packings valid, 49 of 49 mutants refused
      (outputs/geometry.json). The same program's construction subcommand decided the
      bound with Lemmas 2 and 3 at every k from 6 to 250,000 (outputs/construction.json,
      outputs/construction-extension.json).
    replay_status: passed
    verifiers:
      - V-fang-797-review-construction
    independence:
      coverage:
        extent: full
        unit: >-
          the construction's packings at the counts n <= 324 it reaches, k = 6 to 18 at
          each odd width, every square and every pair within sqrt 2 of centres decided
        checked: 15
        of: 15
    independence_record: >-
      packing/resources/web/fang-theorem-a-2026-10-24/review/review-2026-10-25/README.md
    external_review:
      state: informally-verified
      date: '2026-10-25'
      reviewed_by: >-
        AI agent (Claude), the stage 4 mathematical review lane of the #797 import
        (c-review-797-math, think-qmqq), strongest sub-agent tier, maximum reasoning,
        prompted separately from the records lane
      note: >-
        docs/project/reviews/review-2026-10-25-fang-theorem-a.md accepted Theorem A for
        every k >= 6 with findings, none blocking or major (M-1, M-2 minor; N-1 to N-12
        notes); this entry is its own program's run.
    limitations: >-
      Finite feasibility of the construction at fifteen counts, which every case record
      already bounds more tightly: no case bound moves. It is the review's own program,
      written from the note by a Claude agent, a system family the source also used; the
      theorem for every k >= 6 rests on the proof as the review re-derived it, not on this
      run. The 36 certificates the source ships are not this entry's: the maintained
      replay decides them.
    source_reviewed: '2026-10-25'
```

## 3. `docs/project/document-map.yaml`

```yaml
  - {path: docs/project/reviews/review-2026-10-25-fang-theorem-a.md, role: review, authority: record, lifecycle: retained}
```

## 4. Elsewhere

- **`packing/cases/asymptotic/fang_theorem_a.py`.** In `comparisons`, `tail_100` reads
  `4 * 200 - 7 + 2 * isqrt(200 * 193) >= 28 * 28`. At $k = 100$ the square of
  $\sqrt{2k} + \sqrt{2k-7}$ is $4k - 7 + 2\sqrt{2k(2k-7)}$, so the first term should be
  `4 * 100 - 7`. The corrected check holds ($393 + 392 = 785 \ge 784$), so the receipt’s
  conclusion stands, but as written it passes whatever the premise is.
  A test would hold it.
- **The answer bead.** M-1, M-2 and the six questions of the review go to the author on
  the owner’s word at stage 7.
- **Significance.** The draft S2 is kept (the review’s Significance).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
