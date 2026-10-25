# Proposed Record Changes from the Stage 4 Review of T-241 and T-242

Drafts for the records lane, from the review of 24 October 2026
([review-2026-10-24-couzo-evand-n268-n304.md](../../../../../../docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md),
bead `think-vm3m`). The review writes none of them, and the ids are proposals.
The review names #763’s register entry “#763’s entry at 268”, as its brief asked.
That entry is on `main` as T-240 since PR #789 (`c30d944bb`), so the drafts below may
use its id.

## `packing/frontier/verifiers.yaml`

Register the checker, which decides.
`t241_t242_identity.py`, `t241_t242_credits.py`, `t241_t242_receipts.py`,
`t241_t242_sense.py` and the two shell scripts decide nothing and are kept unregistered,
as the measurement programs of the 23 October and 24 October reviews are.

```yaml
  - id: V-kaggle-268-304-review-check
    program: t241_t242_exact.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The 24 October review's standard-library exact checker of the three certificates
      T-241 and T-242 cite (Francisco Couzo's 304 at fa6237e, Evan Daniel's 268 and 304 at
      8a8879a), with a reader of its own that admits only integer and p/q literals and the
      stated row count, deciding each certificate in Fraction arithmetic by two methods:
      separating axes (every corner against the walls, and every pair whose centres lie
      within 2 of each other, chosen exactly, on the four edge normals; the rest disjoint
      by their circumscribed discs) and clipped areas (Sutherland-Hodgman: each square
      clipped to the box keeps area 1, each near pair's intersection has area 0), with a
      third pass of separating axes over every pair. It checks each file's SHA-256 against
      the packets' pins, its header side against the register's claim and the 12-place
      prints, and the register's stated margins; it decides nine hand-built packings and
      twelve controls per certificate: the side at far-wall contact (accepted), 1e-30 past
      it and at twice the clearance; the least-gap pair at contact (accepted) and 1e-30
      past it; a square moved 1e-3 toward its neighbour, enlarged past its pair and past
      its wall, duplicated, and moved past its near wall; every centre drawn in by the
      factor 1 - 1e-9; and a square turned by about 2e-9 radians.
    source:
      - packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_exact.py
    independence_record: docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md
    independence:
      read: [mathematics, certificate-format, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane of T-241 and T-242
            (c-review-t241-t242-math, think-vm3m), strongest sub-agent tier, maximum
            reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Couzo's commits fa6237e, 964ee2b and efef7d1 and Daniel's 8a8879a each carry a
          Co-Authored-By trailer naming Claude, and Daniel's CREDITS.md says the
          repository's work was produced by Claude (Anthropic) under human direction. The
          review's checker is Claude's too, written from a prompt of its own in a file that
          imports nothing from this repository or the sources, from the mathematics and the
          certificates' header lines. Its author never read Couzo's
          verify_bound_certificate.py, sqpack/verify.py, Daniel's verify_cert.py or
          verify_cert2.py, the maintained routes or sharp_controls.py. Before it decided,
          its author had read the register's and the packets' summaries of the producers'
          stated outputs (Daniel's JSON clearances, Couzo's pairs tested); it read those
          outputs themselves, and the packets' sharp-control receipts, after it decided.
          It shares the separating-axis method with the maintained routes and the sources'
          checkers; its clipped area is a second method.
    note: >-
      Written and run on 24 October 2026 by the review (SHA-256
      a4d32ac9d0e3b0dcca4a5886e12bf6ce8360c14470601fbb1572b35b427f5da9 as run); kept in the
      evand-kaggle-descents-2026-10-24 packet's review/review-2026-10-24/ with its README and
      receipt outputs/t241_t242_exact.json.
```

## `packing/frontier/evidence.yaml`

### The review’s checker, for T-241

```yaml
  - id: E-couzo-n304-review-exact-feasibility
    claim: upper-bound
    scope:
      n_values: [304]
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Couzo n304 2026-10-23]'
    certificate: packing/resources/web/couzo-issue763-2026-10-23/source/certificates/best/n304.cert
    replay: >-
      From packing/ with the project interpreter (Python 3.14.7): python -I
      resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_exact.py
      --all-pairs --out OUT, as the 24 October review ran it (53.4 CPU seconds for all three
      certificates and their controls): accepted by both methods, the SHA-256 the pinned
      c8433dd7...231d, the header side equal to the claim's and rounded up at 12 places to
      17.926898903393; 1,170 pairs within 2 decided by both methods and all 46,056 by
      separating axes; every wall cleared by at least exactly 1/10^15 (two squares at the
      near walls, square 298 at the far), the least pair gap
      5787427125212248315636723446790347998647301071/70716860311549861524081902603115498615233747340000000000,
      about 8.1839e-11 (squares 67 and 68), equal to the packet's sharp-control receipt;
      all twelve controls as expected on both methods, and nine hand-built packings.
    replay_status: passed
    verifiers:
      - V-kaggle-268-304-review-check
    independence:
      coverage:
        extent: full
        unit: >-
          the certificate at n = 304 that T-241 cites, every wall and all 46,056 pairs by
          separating axes, and the 1,170 pairs within 2 by clipped area as well
        checked: 1
        of: 1
      read: [mathematics, certificate-format, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane of T-241 and T-242
            (c-review-t241-t242-math, think-vm3m), strongest sub-agent tier, maximum
            reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Couzo's commits fa6237e, 964ee2b and efef7d1 name Claude as co-author. The
          review's checker is Claude's too, from a prompt of its own, in a file that
          imports nothing from this repository or the source; its author read none of the
          source's checkers, sqpack/verify.py or the maintained routes (see
          V-kaggle-268-304-review-check).
    independence_record: docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md
    limitations: >-
      The review's own checker, with a reader of its own and no code of the packet's
      routes or the source's checkers; it shares CPython's Fraction and the separating-axis
      method with the maintained routes. It reads the certificate as counter-clockwise
      t = tan(theta/2), the sense of the verify_cert.py the header names; read the other
      way, 89 pairs overlap (t241_t242_sense.py). Finite feasibility only: no lower bound,
      optimum, local minimum, rigidity, novelty or human oversight.
    source_reviewed: '2026-10-24'
```

### The review’s checker, for T-242

```yaml
  - id: E-evand-kaggle-descents-review-exact-feasibility
    claim: upper-bound
    scope:
      n_values: [268, 304]
    assurance: verified
    method: exact-algebraic
    performed_by: repository
    relationship_to_generator: independent-implementation
    origin: replayed-here
    novelty: previously-published
    source_key: '[Daniel Kaggle descents 2026-10-24]'
    certificate: packing/resources/web/evand-kaggle-descents-2026-10-24/source/search/packer/candidates/
    replay: >-
      From packing/ with the project interpreter (Python 3.14.7): python -I
      resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_exact.py
      --all-pairs --out OUT, as the 24 October review ran it (53.4 CPU seconds for all three
      certificates and their controls): s268_lightning.cert and s304_pub.cert accepted by
      both methods, their SHA-256 the pinned c87da316...4a49 and 5dd7436a...6f21, their
      header sides equal to the claim's decimals and rounded up at 12 places to
      16.874361715870 and 17.926898900357; 1,018 and 1,170 pairs within 2 decided by both
      methods and all 35,778 and 46,056 by separating axes; every wall cleared by at least
      exactly 1/(2*10^20) (23 and 11 squares at the near walls; the far walls by
      250000000023039/(5*10^34) and 250000000030471/(5*10^34)); the least pair gaps about
      9.99999999999998886e-21 (squares 239 and 241) and 9.99999999999999487e-21 (57 and
      58), each equal to the packet's sharp-control receipt; all twelve controls per
      certificate as expected on both methods, and nine hand-built packings.
    replay_status: passed
    verifiers:
      - V-kaggle-268-304-review-check
    independence:
      coverage:
        extent: full
        unit: >-
          the two certificates T-242 cites, at n = 268 and 304, every wall and every pair by
          separating axes, and every pair within 2 by clipped area as well
        checked: 2
        of: 2
      read: [mathematics, certificate-format, producer-output]
      clean_room: true
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: >-
            the stage 4 mathematical review lane of T-241 and T-242
            (c-review-t241-t242-math, think-vm3m), strongest sub-agent tier, maximum
            reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Daniel's commit 8a8879a names Claude as co-author, and his CREDITS.md says the
          repository's work was produced by Claude (Anthropic) under human direction. The
          review's checker is Claude's too, from a prompt of its own, in a file that
          imports nothing from this repository or the source; its author read none of
          Daniel's verify_cert.py or verify_cert2.py or the maintained routes (see
          V-kaggle-268-304-review-check).
    independence_record: docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md
    limitations: >-
      The review's own checker, with a reader of its own and no code of the packet's
      routes or Daniel's checkers; it shares CPython's Fraction and the separating-axis
      method with the maintained routes. The margins, about 5e-21 and 1e-20, lie below the
      binary64 spacing of the coordinates, which exact arithmetic resolves; its controls
      1e-30 past contact are refused. Read clockwise, 99 and 92 pairs overlap. No KKT,
      flat-motion or second-order statement of the source is checked. Finite feasibility
      only: no lower bound, optimum, local minimum, rigidity, novelty or human oversight.
    source_reviewed: '2026-10-24'
```

### The reported entries and the records lane’s replays

Add to `E-couzo-n304-certificate-report` and
`E-evand-kaggle-descents-certificate-report`, and to the records lane’s replay entries
when it registers them:

```yaml
    external_review:
      state: informally-verified
      date: '2026-10-24'
      reviewed_by: >-
        AI agent (Claude), the stage 4 mathematical review lane of T-241 and T-242
        (c-review-t241-t242-math, think-vm3m), strongest sub-agent tier, maximum
        reasoning, prompted separately from the records lane
      note: >-
        docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md accepted the three
        certificates for finite feasibility, with no blocking finding; one major finding
        (M-1) and four minor ones are on the record's credit and assistance statements,
        not on the bounds. Its clean-room checker's runs are
        E-couzo-n304-review-exact-feasibility and
        E-evand-kaggle-descents-review-exact-feasibility, and its least gaps and wall
        clearances equal the packets' sharp-control receipts exactly.
```

The #763 review’s RF-4 finds that the maintained routes share the producer’s first
checker, `sqpack/verify.py`, and the `evand-cert` reader with Daniel’s checkers.
This review did not read the routes.
If RF-4 holds, the records lane’s replay entries for T-241 and T-242 are
`shared-components`, as the #763 review drafts for its own entry.

## `packing/frontier/results.yaml`

### Both entries

```yaml
    reviews:
      - path: docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md
        kind: adversarial
        reviewer: >-
          AI agent (Claude, strongest sub-agent tier, maximum reasoning), the stage 4
          review lane c-review-t241-t242-math of the 24 October intake, prompted separately
          from the records lane, with no shared context
        reviewer_kind: ai
        relation: project
        date: '2026-10-24'
        scope: >-
          Finite feasibility of the three certificates T-241 and T-242 cite, at 304 (Couzo,
          fa6237e) and at 268 and 304 (Daniel, 8a8879a): decided on a clean-room checker by
          separating axes and clipped areas, with twelve controls each (sharp at 1e-30 at a
          wall and a pair) and nine hand-built packings, held to the packets' sharp-control
          receipts exactly; custody against the sources' trees; the sides, their prints and
          the stated margins; identity and lineage measured pose by pose against #763's
          entry at 268, the houses T-174 and T-186, T-175, the manifest's parents and the
          sources' inputs; and the credit chains against the sources' own files.
        verdict: accepted
        covers: [T-241, T-242]
```

Add
`packing/resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_exact.json`
to each entry’s `controls`, and the new evidence entry to each entry’s `evidence`.

### T-241

- **`claim`, M-1.** Replace the paragraph from “The provenance that line defers to” to
  “Polkovskyi after Ostashev, Couzo and PingYou Ltd.”
  (lines 33732–33736) with: “The provenance that line defers to is the source’s witness
  manifest. Its 304 entry names no seed of the packing: its lineage is the notebook’s
  output alone, and its previous_source and previous_reference name Mykhailo
  Polkovskyi’s #593 certificate, T-186’s packing, as the record its catalogue held at
  304 before, as those fields do at every count (the 24 October stage 4 review, M-1). So
  the credit is Tymchishin’s packing, certified by Couzo; whether the notebook started
  from a recorded packing is asked of the author.”
- **`claim`, M-3.** After the construction-credit sentence, add: “The source’s own
  RECORD_PROVENANCE.md keeps Daniil Ostashev’s packing credit for Polkovskyi’s 70a033f
  update at 304.”
- **`claim` or `notes`, M-5.** “The source’s commits fa6237e, 964ee2b and efef7d1 carry
  Co-Authored-By trailers naming Claude.”
- **`notes`, M-1.** Replace “That fits the lineage the source’s manifest states, a
  re-closure of the house’s packing; with 54 squares beyond a tenth it is another
  arrangement, found from the house’s, not a refinement of it.”
  (lines 33807–33809) with “With 54 squares beyond a tenth it is another arrangement
  than the house’s; the 250 within a tenth are a resemblance, which states no lineage.”
- **`significance`:**

```yaml
    significance:
      score: 3
      rationale: >-
        A different arrangement at 304 from the house's, 2.53e-03 below T-186 and every
        report there: no symmetry pairs it one to one with T-186's packing by nearest
        centres, and the optimal assignment, best under the diagonal reflection, moves 54
        of 304 squares beyond a tenth and turns squares by up to 26.0 degrees, as T-175
        (1.38e-04 to 2.64e-03) and T-230 (1.86e-04) are (S3), far above T-226's 1.88e-05 at
        the low end of S3. The packing is Kirill Tymchishin's and Couzo certified it; whose
        arrangement it is changes the credit, not the score. No lower bound or optimum.
      scored: '2026-10-24'
      by: >-
        the 24 October stage 4 review
        (docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md), lane
        c-review-t241-t242-math, confirming the draft S3 of the stage 1 triage (think-6r5p)
        and the records lane of think-l49q
```

### T-242

- **`claim`, M-1.** In lines 33860–33865, drop “after Mykhailo Polkovskyi’s packing,
  T-186’s, and T-186’s recorded chain (Ostashev, Couzo, PingYou Ltd), as T-241 records”.
- **`notes`, N-1.** “The source’s s268_lightning.json gives S_input 16.87436171586941,
  the side of s268_lightning.input.txt, Lavrentev’s placement, which the certificate is
  to 1.41e-4; s268_lightning.predescent.txt, Tymchishin’s v4 packing to 2.47e-10, is
  2.49e-2 from it, and what it is is asked of the author.”
- **`significance`, M-2:**

```yaml
    significance:
      score: 2
      rationale: >-
        Smaller finite construction sides at 268 and 304, 4.48e-12 and 3.04e-09 below the
        reports before them. At 304 it is the solved side of the packing T-241 certifies,
        one to one with it and no square beyond 4.60e-4, as T-225 and T-231 are (S2); of
        its 3.04e-09 margin, 1.45e-09 is the height of T-241's side above the binary64
        packing Daniel started from and 1.58e-09 his descent. At 268 it descends Vladislav
        Lavrentev's placement of the arrangement #763's entry refines, one to one with that
        entry under the mirror x to S - x and none beyond a tenth, and moves the 12-place
        print of that entry (16.874361715874, pending adoption) to 16.874361715870: below
        T-239's case (S2, 12 squares beyond a tenth) and above padding alone (S1, T-174,
        T-186). A citable detail that moves no theorem; no lower bound or optimum.
      scored: '2026-10-24'
      by: >-
        the 24 October stage 4 review
        (docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md), lane
        c-review-t241-t242-math, confirming the draft S2 of the stage 1 triage (think-6r5p)
        and the records lane of think-l49q
```

### At the exit, both entries

- **Confirmation:** “confirmed, independently re-implemented”: the 24 October review
  decided the certificates on a clean-room checker of its own, by a Claude agent, a
  system family both producers also used.
  The maintained replay is the records lane’s, `shared-components` if the #763 review’s
  RF-4 holds here.
- **`next_rung`:** adopt 268 (after #763’s entry is adopted, PR #794) and 304 in one
  change (`think-hx0e`), regularizing each new house with both strong generators; the
  house credit at 268 is *Daniel after Lavrentev* and at 304 follows T-241’s packing as
  credited after M-1; the authors’ questions C1 to C4 and D1 and D2; a second
  adversarial review by a distinct reviewer and human oversight for rung 4.

## `packing/resources/bibliography.yaml`

- **`[Couzo n304 2026-10-23]`, M-1, M-3, M-5:** `credit: Couzo after Tymchishin, Levy`,
  with Levy for the manifest’s first checker, `sqpack/verify.py`, as `[Couzo issue 763
  2026-10-23]` has it; `short_credit` the same.
  In the note, replace “The source’s manifest gives the notebook’s previous source and
  seed as Mykhailo Polkovskyi’s 70a033f certificate (#593), T-186’s packing, which this
  record measures as Daniil Ostashev’s T-175 packing re-solved, so the chain after
  Polkovskyi is T-186’s as recorded.”
  with “The source’s manifest names Mykhailo Polkovskyi’s 70a033f certificate (#593),
  T-186’s packing, as the record its catalogue held at 304 before, not as the notebook’s
  seed.” Add the commits’ Claude co-author trailers, and the source’s own
  `RECORD_PROVENANCE.md` beside the declined construction credit.
- **`[Daniel Kaggle descents 2026-10-24]`, M-1, M-4:** `credit: Daniel after Lavrentev,
  Tymchishin`, with Levy only where Daniel’s source supports it for these descents.
  The key’s stated reason, T-241’s chain, no longer does.
  The same holds for `lineage: builds-on-project`; Daniel’s earlier keys hold it on
  grounds this review did not check.
  In the note, replace “after Mykhailo Polkovskyi’s packing, T-186’s, whose recorded
  chain the line carries” and the “Levy enters through 304, T-241’s chain” sentence
  accordingly.

## The packets’ READMEs

- **`couzo-n304-2026-10-23/README.md`:** M-1 at lines 49–63 (the provenance paragraph),
  109–112 (“That fits the lineage the manifest states”), 128–135 and 140–144 (the credit
  and the key), and question 1 at lines 150–156, which becomes the review’s C1; M-3 at
  lines 62–63; M-5 in Credit and Licence.
- **`evand-kaggle-descents-2026-10-24/README.md`:** M-1 at lines 190–198 and 204–208;
  N-1 beside question 3 (lines 222–225).

## The Document Map and the Replies

Map the review in `docs/project/document-map.yaml` as a non-superseded `review`, which
the `reviews` items above need.
The replies to the authors (C1 to C4, D1 and D2) are drafted in the import’s answer bead
and posted at stage 7 on the owner’s word.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
