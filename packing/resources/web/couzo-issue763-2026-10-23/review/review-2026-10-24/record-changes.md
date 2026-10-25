# Proposed Record Changes from the Stage 4 Review of #763 at 268 and 303

Drafts for the records lane’s PR B, from the review of 24 October 2026
([review-2026-10-24-couzo-n268-n303.md](../../../../../../docs/project/reviews/review-2026-10-24-couzo-n268-n303.md),
bead think-zjus). The review writes none of them.
The ids are proposals, and the #763 entry keeps the id `main` gives it, T-240 since #789
merged.

## `packing/frontier/verifiers.yaml`

Register the checker, which decides.
`agree.py`, `identity.py` and `sides.py` decide nothing and are kept unregistered, as
the 23 October review’s measurement programs are; records for them follow in case the
lane prefers to register them as premise checks.

```yaml
  - id: V-couzo-763-review-check
    program: check_certificates.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The 24 October review's standard-library exact checker of the two certificates the
      #763 entry cites, at 268 and 303, with a reader of its own that admits only integer
      and p/q literals and the stated row count, deciding each certificate on two routes
      in Fraction arithmetic: route A by the separating-axis test over every pair, with no
      distance filter, and every corner against the walls; route B by the exact area of
      each pair's clipped intersection (Sutherland-Hodgman) over the pairs whose centres
      lie within sqrt(2)(h_i + h_j), the rest disjoint by their circumscribed discs, and
      each square's support against the walls. It checks each file's digest against the
      source manifest, its header side against the claim and its 12-place print, and
      decides ten controls per certificate: a duplicated square, a square moved halfway to
      its neighbour, the closest pair closed to exact contact (accepted) and 1e-30 past
      it, that square enlarged by the pair's gap plus 1e-30, the square nearest a wall
      enlarged by its clearance plus 1e-30, the box at the packing's extent (accepted) and
      1e-30 below it, and two malformed texts.
    source:
      - packing/resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/check_certificates.py
    independence_record: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
    independence:
      read: [mathematics, certificate-format]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane of #763 at 268 and 303
            (c-review-t240-math, think-zjus), strongest sub-agent tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source's commit 964ee2b, which issue 763 names, and its parents fa6237e and
          efef7d1 end with "Co-Authored-By: Claude Opus 5.5"; efef7d1's message describes
          "Codex's reviewed intake", and the source's verify_bound_certificate.py is Evan
          Daniel's verifier "with modifications by Francisco Couzo with Codex". The
          review's checker is Claude's, written from a prompt of its own in a file that
          imports nothing from this repository or the source, from the mathematics and the
          certificates' format line ("unit squares, centre (x, y), rotation t =
          tan(theta/2)"). Its author never read the source's checkers, Daniel's checkers,
          sqpack/verify.py, check_rational_witness_independent, upper_bound_reports or
          evand_exact_certificates. Route A shares the separating-axis method with the
          maintained routes and with the source's checkers; route B's clipped area is a
          second method.
    note: >-
      Written and run on 24 October 2026 by the review (SHA-256 1870d726...e3a7 as run,
      twice, with identical receipts apart from CPU times); kept in the
      couzo-issue763-2026-10-23 packet's review/review-2026-10-24/ with its README and
      receipts out/check-certificates.json and out/second-run/.
```

Optional, if the lane registers the measurement programs.
Each would carry the same `independence` block as above with
`read: [mathematics, certificate-format,
producer-output]` for `agree.py`, which reads the maintained receipt, and
`read: [mathematics, certificate-format]` for the other two.

```yaml
  - id: V-couzo-763-review-agree
    program: agree.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Holds the 24 October review's checker to the packet's maintained replay receipt
      (receipts/exact-certification.json.xz): the side and every pose read by the
      maintained run, as exact rationals; the pairs both maintained routes tested; their
      least pair gaps and least wall clearances against the checker's route A, exactly;
      and the receipt's two controls refused by both routes. 24 of 24 equal.
    source:
      - packing/resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/agree.py
    independence_record: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
  - id: V-couzo-763-review-identity
    program: identity.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [numerical-f64]
    role: premises
    summary: >-
      Measures, in binary64, the identity of the #763 packings at 268 and 303 against
      their manifest parents, the houses T-174, T-230 and T-239, and Evan Daniel's
      8a8879a certificates: the least-cost assignment of squared centre distance over
      the 8 symmetries, squares moved beyond 0.1 and 1e-3, the largest move, turns,
      whether nearest centres pair one to one, the bottleneck and reversed tilts, with
      four alignment and cost variants. It decides no bound.
    source:
      - packing/resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/identity.py
    independence_record: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
  - id: V-couzo-763-review-sides
    program: sides.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Compares the #763 sides at 268 and 303 exactly with the comparators' stated sides
      (the houses, the manifest parents, Daniel's 8a8879a certificates, four side-only
      leaderboard values) and with every reported and verified bound at the later counts
      269 to 288 and 304 to 320; checks the record's decimals. It decides no geometry.
    source:
      - packing/resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/sides.py
    independence_record: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
```

## `packing/frontier/evidence.yaml`

### The review’s own checker

```yaml
  - id: E-couzo-763-review-exact-feasibility
    claim: upper-bound
    scope:
      n_values: [268, 303]
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Couzo issue 763 2026-10-23]'
    certificate: packing/resources/web/couzo-issue763-2026-10-23/source/certificates/best/
    replay: >-
      From packing/ with the project interpreter (Python 3.14.7) on a shared four-core
      host: python -I
      resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/check_certificates.py
      --out OUT, as the 24 October review ran it twice (34.6 and 34.4 CPU seconds, identical
      receipts apart from CPU times): both certificates accepted on both routes, their
      SHA-256 equal to the manifest's (e9833bf2...e07e and 39a150f4...791a), their header
      sides equal to the claim's and rounded up at 12 places to 16.874361715874 and
      17.906978233799; route A decided all 35,778 and 45,753 pairs, route B the 668 and 701
      within the discs; none touching, every wall cleared by at least 1/10^15 (squares 3
      and 4), the least pair gaps about 2.0963e-13 (squares 101 and 223) and 2.0718e-13
      (46 and 58); every one of the ten controls per certificate as expected on both
      routes. agree.py found 24 of 24 shared numbers equal with both maintained routes'
      receipt.
    replay_status: passed
    verifiers:
      - V-couzo-763-review-check
    independence:
      coverage:
        extent: full
        unit: >-
          the two certificates the #763 entry cites, at n = 268 and 303, every wall and
          every pair on route A, and every pair within the discs on route B
        checked: 2
        of: 2
      read: [mathematics, certificate-format]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane of #763 at 268 and 303
            (c-review-t240-math, think-zjus), strongest sub-agent tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source's commits 964ee2b, fa6237e and efef7d1 name Claude as co-author, and
          its second checker is Evan Daniel's verifier modified with Codex. The review's
          checker is Claude's too, written from a prompt of its own in a file that imports
          nothing from this repository or the source, from the mathematics and the
          certificates' format line; its author read none of the source's, Daniel's or
          the maintained routes' code. Before writing it, its author had read T-239's
          register entry, which says that replay met sharp controls at exact contact and
          refused them 1e-30 past it, and the controls here take that form.
    independence_record: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
    limitations: >-
      The review's own checker, with a reader of its own and no code of the packet's
      routes, the source or Daniel's checkers; it shares CPython's Fraction with the
      maintained routes, and route A the separating-axis method with them and with the
      source's checkers. The packet's two gross controls were decided by the maintained
      routes, not by this checker; its own controls are its ten per certificate. Finite
      feasibility only: no lower bound, optimum, local minimum, rigidity, novelty or human
      oversight.
    source_reviewed: '2026-10-24'
```

### The records lane’s replay

When PR B registers the maintained replay of `receipts/exact-certification.json.xz`, its
relationship is `shared-components` (RF-4), as `E-couzo-670-exact-feasibility`’s is for
the same source:

```yaml
    relationship_to_generator: shared-components
    shared_components:
      - >-
        sqpack.verify's unit-shape and separating-axis predicates (verify_packing, which
        sqpack.witness.exact_verify calls), the jlevy/squares checker the source's manifest
        names as its first checker, at 37e6757, byte-identical to main (SHA-256
        56bc5b9f...7337)
      - >-
        the certificate parser and half-angle map of devtools.evand_exact_certificates (the
        evand-cert adapter, acquisition/report.json), through which both maintained routes
        read each certificate, transcribed from Evan Daniel's checkers, from whose
        verify_cert.py the source's verify_bound_certificate.py derives
      - CPython's fractions.Fraction arithmetic
    external_review:
      state: informally-verified
      date: '2026-10-24'
      reviewed_by: >-
        AI agent (Claude), the stage 4 mathematical review lane of #763 at 268 and 303
        (c-review-t240-math, think-zjus), strongest sub-agent tier, maximum reasoning,
        prompted separately from the records lane
      note: >-
        docs/project/reviews/review-2026-10-24-couzo-n268-n303.md accepted both
        certificates for finite feasibility, with no blocking or major finding (RF-1 to
        RF-4, RF-7 and RF-8 minor; RF-5, RF-6 and RF-9 to RF-12 notes). Its clean-room
        checker's run is E-couzo-763-review-exact-feasibility, and its agree.py found the
        maintained receipt's sides, poses, pairs tested, least pair gaps and least wall
        clearances equal to the checker's (24 of 24).
```

### The reported entry

Add to `E-couzo-763-certificate-report`:

```yaml
    external_review:
      state: informally-verified
      date: '2026-10-24'
      reviewed_by: >-
        AI agent (Claude), the stage 4 mathematical review lane of #763 at 268 and 303
        (c-review-t240-math, think-zjus), strongest sub-agent tier, maximum reasoning,
        prompted separately from the records lane
      note: >-
        docs/project/reviews/review-2026-10-24-couzo-n268-n303.md accepted the two
        certificates the #763 entry cites, at 268 and 303, for finite feasibility only, with
        no blocking or major finding; the replay it held to its own checker is the records
        lane's, and its own checker's run is E-couzo-763-review-exact-feasibility.
```

## `packing/frontier/results.yaml`, the #763 entry

```yaml
    reviews:
      - path: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md
        kind: adversarial
        reviewer: >-
          AI agent (Claude, strongest sub-agent tier, maximum reasoning), the stage 4
          review lane c-review-t240-math of the 24 October intake, prompted separately from
          the records lane, with no shared context
        reviewer_kind: ai
        relation: project
        date: '2026-10-24'
        scope: >-
          Finite feasibility of the two certificates issue 763 names in the corpus, at 268
          and 303: decided on a clean-room checker of two exact routes with ten controls each
          (sharp at 1e-30 at a pair, a wall and the box), held to both maintained routes'
          receipt at 24 shared numbers; the sides, their prints, the margins and the later
          counts; and identity and lineage measured pose by pose against the manifest's
          parents, the houses T-174, T-230 and T-239, and Evan Daniel's later certificates;
          the credit chain against the source's own files.
        verdict: accepted
        covers: [T-240]
    significance:
      score: 3
      rationale: >-
        New arrangements at 268 and 303 relative to the record, 4.45e-03 and 2.78e-03 below
        the houses T-174 and T-239, one to one with neither under any symmetry, with 118 and
        133 squares beyond a tenth of them, as T-162's 2.02e-03 to 1.42e-02 (S3) are, and
        far above T-230's 1.86e-04 (S3). Each refines the Kaggle notebook packing its search
        started from, with none beyond a tenth of Tymchishin's v4 at 268 and three of
        Couzo's push packing at 303, so the arrangements come from the notebooks and the
        sides from the refinements, as the credit records. No lower bound or optimum.
      scored: '2026-10-24'
      by: >-
        the 24 October stage 4 review
        (docs/project/reviews/review-2026-10-24-couzo-n268-n303.md), lane
        c-review-t240-math, confirming the draft S3 of the stage 1 triage (think-cnn7) and
        the records lane of think-ptkk
```

For the `claim`, `notes` and `next_rung`, rewritten together at the exit:

- **Confirmation:** “confirmed, independently re-implemented”: the 24 October review
  decided both certificates on a clean-room checker of its own, by a Claude agent, a
  system family the producer also used; the maintained replay shares the producer’s
  first checker, `sqpack/verify.py`, and the `evand-cert` reader (RF-4).
- **Lineage, measured:** at 268 one to one with Tymchishin’s v4 parent under (x, y) ↦ (s
  − x, y), none beyond 0.1, largest 5.91e-2; at 303 one to one with Couzo’s push parent,
  three beyond 0.1 (squares 230, 264 and 289), largest 0.309. Against the houses one to
  one under no symmetry: 118 beyond 0.1 of T-174’s, 125 of T-230’s and 133 of T-239’s
  (118 to 119, 123 to 125 and 131 to 134 across the variants).
- **Daniel’s later 268:** one arrangement with #763’s and a different placement,
  Lavrentev’s, re-solved: none beyond 0.1, 135 beyond 1e-3, largest 7.08e-2, the mirror
  image. This replaces “measured by the stage 4 review” (RF-3, RF-6).
- **`previous_source`:** the top-level one is the parent; the previous record is the
  parent’s own (RF-2).
- **AI assistance:** the commits’ Claude co-author trailers and `efef7d1`’s “Codex’s
  reviewed intake” (RF-1).
- **`next_rung`:** adopt 303 now with its regularization; decide Daniel’s 268
  (think-l49q) before adopting 268; the author’s six questions; a second adversarial
  review by a distinct reviewer and human oversight for rung 4.

## The packet README

RF-1 (lines 88 to 91), RF-2 (lines 252 and 253) and RF-3 (question 8, lines 278 to 283),
as the review states them.
The question to the author can be replaced by the review’s question 1.

## `docs/project/document-map.yaml`

```yaml
  - {path: docs/project/reviews/review-2026-10-24-couzo-n268-n303.md, role: review, authority: record, lifecycle: retained}
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
