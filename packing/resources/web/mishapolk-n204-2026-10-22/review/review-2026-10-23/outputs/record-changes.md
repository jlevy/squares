# Proposed Record Changes: Stage 4 Review of T-231 (`n204.cert`, #719)

For the records lane (`c-lane-719-records-1023`, `think-h01y`) and the coordinator
(`coord-intake-1023`). The review lane (`c-review-t231-math`, `think-tetq`) writes none
of these. Identifiers follow the records branch at `15ecb0a68`: source key
`[Mishapolk n204 2026-10-22]`, packet `mishapolk-n204-2026-10-22`, report evidence
`E-mishapolk-n204-certificate-report`. Where the branch has not yet named a replay
entry, this file calls it `E-mishapolk-n204-exact-feasibility`; rename to match.

## Files to Land

Copy these from the review lane’s output directory to the same repository paths:

- `docs/project/reviews/review-2026-10-23-mishapolk-n204.md`, the review.
- `packing/resources/web/mishapolk-n204-2026-10-22/review/review-2026-10-23/`, holding:
  - `README.md`;
  - `programs/`: `review_t231_check.py`, `sharp_controls_t231.py`,
    `maintained_routes_t231.py`, `agree_t231.py`, `margins_t231.py`, `identity_t231.py`
    and `lineage_t231.py`;
  - `outputs/`: every receipt, `second-run/`, `regularizer-rerun/` (about 128 KB, the
    rerun’s receipt, report, input, solve certificate and records, and regularized
    certificate) and `program-digests.sha256`.

Then map the review in `docs/project/document-map.yaml`:

```yaml
- {path: docs/project/reviews/review-2026-10-23-mishapolk-n204.md, role: review, authority: record, lifecycle: retained}
```

Link the packet README to `review/review-2026-10-23/README.md` once the review is
mapped.

## `evidence.yaml`

**The report entry**, `E-mishapolk-n204-certificate-report`, gains:

```yaml
external_review:
  state: informally-verified
  date: '2026-10-23'
  reviewed_by: 'AI agent (Claude), the stage 4 mathematical review lane of T-231 (c-review-t231-math,
    think-tetq), strong sub-agent tier, maximum reasoning, prompted separately from the records lane
    (c-lane-719-records-1023)'
  note: docs/project/reviews/review-2026-10-23-mishapolk-n204.md accepted certificates/n204.cert at
    12fc4667 for finite feasibility only, with seven non-blocking findings (RF-1 to RF-7); the replay is
    E-mishapolk-n204-exact-feasibility, and the review checker's run is
    E-mishapolk-n204-review-exact-feasibility.
```

**The records lane’s replay entry** (`E-mishapolk-n204-exact-feasibility`) needs three
things:

- `relationship_to_generator: shared-components`, with `shared_components` naming
  `sqpack.verify`’s predicates (the issue names `sqpack/verify.py` among the author’s
  checkers), the `evand-cert` reader, the half-angle map and `Fraction`, as T-229’s
  `E-mishapolk-719-exact-feasibility` does.
- In `limitations`, after its own sharp-controls receipt: “This review’s sixteen mutants
  (outputs/sharp-controls.json in review/review-2026-10-23/) were refused or accepted as
  required by both maintained routes: walls at the top-and-right, left and bottom, and
  pairs tilted-tilted, tilted-aligned and aligned-aligned, at exact contact and 1e-30
  past it.”
- This review as `external_review`, or the report entry’s note citing it, whichever the
  checker reads.

**A new entry for this review’s checker:**

```yaml
- id: E-mishapolk-n204-review-exact-feasibility
  claim: upper-bound
  scope:
    n_values:
    - 204
  assurance: verified
  method: exact-algebraic
  performed_by: repository
  relationship_to_generator: independent-implementation
  origin: replayed-here
  novelty: previously-published
  source_key: '[Mishapolk n204 2026-10-22]'
  certificate: packing/resources/web/mishapolk-n204-2026-10-22/source/certificates/n204.cert
  replay: 'From the packet''s review/review-2026-10-23/, with any CPython 3.12 or later: python -I
    programs/review_t231_check.py --route Z CERT and --route C CERT, one process a route, as the 23
    October review ran them (0.25 s and 6.8 s): accepted on both routes, every wall cleared by at least
    exactly 1/(2*10^20) (left and bottom) and 500000000068827/10^35 (right and top), and every one of the
    20,706 pairs separated, none touching, the least gap 9.99999999999998720936e-21 (squares 63 and 84,
    numbered from 0) and equal to that pair''s exact Euclidean distance; the two routes'' per-pair gaps
    and per-square wall clearances equal. agree_t231.py found the side, all 204 poses, the pair count,
    the least clearance and the least gap equal to both maintained routes'' and the records lane''s receipt
    (63 of 63 checks). Its sharp controls (sharp_controls_t231.py) accepted exact contact and refused 1e-30
    past it on both of its routes and both maintained routes.'
  replay_status: passed
  verifiers:
  - V-mishapolk-n204-review-check
  - V-mishapolk-n204-review-controls
  independence:
    coverage:
      extent: full
      unit: the certificate at n = 204 that T-231 cites, every wall and every pair, on each of the
        checker's two routes
      checked: 1
      of: 1
    read:
    - mathematics
    - certificate-format
    - specification
    clean_room: true
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the stage 4 mathematical review lane of T-231 (c-review-t231-math, think-tetq), strong
        sub-agent tier, maximum reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: >-
        The author discloses Gemini assistance. The certificate's determined rows equal Evan
        Daniel's exact solver's output for T-229's arrangement (the review's RF-1), and that
        solver's author says it was written with Claude. The issue names this repository's
        sqpack/verify.py, whose first revisions are Claude-authored commits, among the author's
        checkers. The review's checker is Claude's too. It was written from a prompt of its own in a
        file that imports nothing from this repository or the source, from the certificate's format
        line, the mathematics and the #728 review's account of its checker (specification). It
        decided the certificate before its author read any maintained or source code, and has not
        changed since. Its author never read sqpack/verify.py, sqpack/witness.py or
        check_rational_witness_independent. Afterwards the author read the source's
        check_packing.py, which cannot read this certificate, and the module statement of the
        vendored exactsolve.py.
  independence_record: docs/project/reviews/review-2026-10-23-mishapolk-n204.md
  limitations: >-
    The review's own checker, with a reader of its own and no code of the packet's routes or the
    source's; route C shares CPython's Fraction with the maintained routes, and route Z uses
    integers alone. Its author read the #728 review's account of its checker before writing it.
    The gross controls and the sharp mutants were decided by this checker and the maintained
    routes alike (outputs/sharp-controls.json). Finite feasibility only.
  source_reviewed: '2026-10-23'
```

## `verifiers.yaml`

```yaml
- id: V-mishapolk-n204-review-check
  program: review_t231_check.py
  author: Squares Project (Levy)
  provenance: first-party
  language:
  - Python
  methods:
  - exact-algebraic
  role: decides
  summary: 'The 23 October review''s standard-library exact checker of the certificate T-231 cites, with
    a strict reader of its own, deciding it on two routes that share only the reader: route Z in integers
    alone (a Pythagorean triple per row, containment by half-extents and every pair by four separating-axis
    inequalities cleared of denominators, never loading fractions), and route C in Fraction (unit edges,
    right angles, orientation and corner mean, corner containment, every pair by the exact area one square''s
    closed half-planes clip from the other and again by corner projections, and the exact squared distance
    of every pair whose centres lie within 2). Its --self-test runs 13 hand-built cases, 12 malformed texts
    and 1,500 random pairs.'
  source:
  - packing/resources/web/mishapolk-n204-2026-10-22/review/review-2026-10-23/programs/review_t231_check.py
  sha256: 2c8053b16a28c42b1f6bac5f921aa66a00cd782c99bd8c7ccd383febe9128dd6
  independence_record: docs/project/reviews/review-2026-10-23-mishapolk-n204.md
  independence:
    read:
    - mathematics
    - certificate-format
    - specification
    clean_room: true
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the stage 4 mathematical review lane of T-231 (c-review-t231-math, think-tetq), strong
        sub-agent tier, maximum reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: As E-mishapolk-n204-review-exact-feasibility's.
  note: Written and run on 23 October 2026 by the review; kept in the mishapolk-n204-2026-10-22 packet's
    review/review-2026-10-23/ with its README and receipts (RF-7).
- id: V-mishapolk-n204-review-controls
  program: sharp_controls_t231.py, maintained_routes_t231.py
  author: Squares Project (Levy)
  provenance: first-party
  language:
  - Python
  methods:
  - exact-algebraic
  role: premises
  summary: 'The 23 October review''s controls of the certificate T-231 cites. sharp_controls_t231.py builds
    sixteen mutants (the side lowered by the least top-or-right clearance, every square moved by the least
    left and by the least bottom clearance, and the least-gap pairs between two tilted, a tilted and an
    aligned, and two aligned squares closed along their edge normal, each at exact contact and 1e-30 past
    it; a duplicated square; a square moved outside; a row dropped; a decimal literal) and decides each
    by the review''s checker and by both maintained routes through the evand-cert adapter.
    maintained_routes_t231.py runs the kernel''s positive and two gross jobs one per process, as certify''s
    child does, with validate_job, and the kernel''s run_sharp at contact and past it. They add the mutants
    and the expectations; the routes decide.'
  source:
  - packing/resources/web/mishapolk-n204-2026-10-22/review/review-2026-10-23/programs/sharp_controls_t231.py
  - packing/resources/web/mishapolk-n204-2026-10-22/review/review-2026-10-23/programs/maintained_routes_t231.py
  sha256:
    sharp_controls_t231.py: 4d00610020f83050ec65f5bb6cd2a1bf49585e060c5267e0fd37807a5faf3093
    maintained_routes_t231.py: 8e992d49664b9f6e77342769b2cb82bf5369187af14616b83b43313424c35470
  independence_record: docs/project/reviews/review-2026-10-23-mishapolk-n204.md
  note: Written and run on 23 October 2026 by the review (c-review-t231-math); they import
    devtools.upper_bound_reports, devtools.evand_arrangement_reports and devtools.evand_exact_certificates
    to reach the maintained routes, and the review's checker. Kept with their receipts
    (outputs/sharp-controls.json, outputs/maintained-*.json).
```

Match the registry’s actual field names: digest fields, and one entry or two for the two
controls files. The four other programs (`agree_t231.py`, `margins_t231.py`,
`identity_t231.py` and `lineage_t231.py`) decide nothing and are not registered; their
README says so.

## `results.yaml`, T-231

**`reviews`:**

```yaml
- path: docs/project/reviews/review-2026-10-23-mishapolk-n204.md
  kind: adversarial
  reviewer: 'AI agent (Claude, strong sub-agent tier, maximum reasoning), the stage 4 mathematical review
    lane of T-231 (c-review-t231-math), prompted separately from the records lane (c-lane-719-records-1023)'
  reviewer_kind: ai
  relation: project
  date: '2026-10-23'
  scope: 'Finite feasibility of the certificate T-231 cites (certificates/n204.cert at 12fc4667): a
    clean-room checker written for the review deciding it on an integer route and a Fraction route with
    exact clipping area and Euclidean distance, both maintained routes run as certify''s child runs them,
    sixteen sharp, gross and reader controls through all four deciders, the side''s margins in report order
    and against every bound through 224, each route''s trust boundary, the identity measured pose by pose
    against T-229, T-225, T-223, T-228, T-226 and T-186, and the certificate compared row by row with Evan
    Daniel''s exact solver''s output for T-229''s witness.'
  verdict: accepted
  covers:
  - T-231
```

**`significance`** (replacing the draft):

```yaml
significance:
  score: 2
  rationale: The solved side of T-229's packing at 204, at Evan Daniel's exact solver's padding of
    1e-20, 1.48e-11 below T-229, which certifies the same point padded by 1e-12 (T-229 is this certificate
    dilated by 1 + 1.000055e-12 to within 2.9e-15). That is T-225's case, the solved exact side of a packing
    already reported 1.76e-11 to 1.39e-9 below its certificate, S2. The step is padding alone, but eight
    orders above the padding the record scores S1 (T-170, T-174, T-186, at most 1.8e-19), and it moves
    the case's 12-place print (14.808642830528 to 14.808642830514), as at T-229's 105 (S2). A citable detail
    that moves no theorem; no lower bound, optimum or local minimum.
  scored: '2026-10-23'
  by: the 23 October stage 4 review (docs/project/reviews/review-2026-10-23-mishapolk-n204.md), lane
    c-review-t231-math, confirming or replacing the records lane's draft
```

If the records lane’s draft was S2, write “confirming the draft S2 of the records lane
(`think-h01y`)”; if S1, “changing the draft S1”. Read as a padding change by kind alone,
S1 is the alternative, and the owner may prefer it.
The review keeps S2 by scale and by T-225’s precedent.

**Claim, `notes` and method**, rewritten together:

- The method, as measured (RF-1): “the exact solved side of T-229’s packing, whose
  determined rows equal Evan Daniel’s exact solver’s (`exactsolve.py`, MIT) row for row,
  at that solver’s padding of 1e-20; T-229 is the same point padded by 1e-12”. Cite
  `review/review-2026-10-23/outputs/lineage.json`, and keep that wording until the
  author answers Question 1.
- The packing’s credit is T-229’s: Couzo’s arrangement as Daniel and Polkovskyi refined
  it. The certificate is Polkovskyi’s, dated by `1851c2c` (2026-10-22T05:29:48Z), and
  claimed on #719 at 2026-10-22T20:15:57Z.
- The side is printed as the exact fraction or its ceiling (14.808642830514 at 12
  places, 14.8086428305130872 at 16), and no source print (RF-2).
- Cite `12fc4667` and the digest, never the head’s path (RF-3).
- For feasibility, cite the records lane’s replay and this review, not the triage’s
  unretained run (RF-6).
- No local-minimum, KKT or rigidity claim beyond “not rigid”: 21 free squares keep
  clearances of $5.774 \times 10^{-9}$ to $1.25 \times 10^{-2}$ (RF-5).
- Confirmation wording: *confirmed, independently re-implemented* (this review’s
  clean-room checker), with the maintained replay re-implemented, sharing the producer’s
  components. Note the system-family overlap as above.

**Identity:** basis `measured`, measured in
`review/review-2026-10-23/outputs/identity.json` and `lineage.json`. One to one with
T-229 under the identity and in the same row order, largest move $2.02 \times 10^{-11}$,
which is a uniform dilation by $1 + 10^{-12}$ to within $2.9 \times 10^{-15}$. One to
one with T-223 under the identity and with T-225 under a half turn, as T-229 is.

## The Case Record, `n-204.md`, and the House

- Once T-231 stands at `V3`/`C3` with this review mapped as its accepted review, the
  house rule adopts it at 204 from T-229, regularized in the same pull request (the
  regularization run at T-231’s side).
  T-229 stays retained as history.
- A section for the certificate.
  Suggested lead: “Mykhailo Polkovskyi’s certificate of T-229’s packing at its solved
  side, published beside `n-204.cert` in `1851c2c` and claimed on #719 …”, with this
  review’s confirmation sentence and RF-1’s method sentence.
- The rigidity block (`n-204.md` lines 64–78) describes an earlier witness.
  Revisit it at the adoption: T-231 is not rigid by its free squares (RF-5).

## T-229, Beside This Change

- Add to T-229’s notes that its certificate is T-231’s point dilated by
  $1 + 1.000055 \times 10^{-12}$ (rounded to within $2.9 \times 10^{-15}$), which is why
  its margins at 204 are about $5 \times 10^{-13}$ and $10^{-12}$.
- The triage bead’s note of 23 October (`think-xyhn`, 04:05Z) plans to drop Evan
  Daniel’s regularization (T-225) from T-229’s lineage at 204, on the author’s answer
  that the solve started from #678. RF-1 does not oppose that.
  The solver it measures is a method credit, not a packing antecedent: the record can
  drop T-225 as an antecedent while naming Daniel’s exact solver as the measured method
  of both 204 files, pending the author’s answer.

## The Adoption README of 23 October

`packing/cases/regularized_drawings/think-4h23-2026-10-23/README.md`, lines 81–82
(RF-4). Change “the view reproduces his own publication” to “the run reproduces his
side”, and add: “the solved view is the display regularization at that side; the solve’s
own certificate shares 119 rows with his file byte for byte, and differs only at the
solver’s free squares and frozen flat variables (review of 23 October, RF-1)”.

## The Rung Each Piece of Evidence Supports

| Evidence | Supports | Relation | Coverage |
| --- | --- | --- | --- |
| `E-mishapolk-n204-certificate-report`, with this review as `external_review` | the reported bound; `C1` by the read | not applicable | full |
| `E-mishapolk-n204-exact-feasibility` (records lane’s replay) | `V3`/`C3` (exact-algebraic, certificate, `check --replay`, passing, controls refused) | `shared-components` | full |
| `E-mishapolk-n204-review-exact-feasibility` (this review’s checker) | `V3`/`C3` on its own | `independent-implementation`, `clean_room: true` | full |
| this review in `reviews` (adversarial, accepted) | status `reviewed`; one of the two adversarial reviews `V4`/`C4` would need |  |  |
| `outputs/sharp-controls.json`, `maintained-sharp.json` | the replay entries’ limitations (sharp controls) | premises | the ten sharp mutants and the kernel’s two |
| `identity.json`, `lineage.json`, `margins.json`, `agree.json` | no rung; cited by the case record and the entry’s notes | decide nothing |  |

The result: `V3`/`C3`, *confirmed, independently re-implemented*. `V4`/`C4` is not
reached: it needs a second accepted adversarial review by a distinct reviewer, and a
retained human oversight record.

## The Reply to the Author (Stage 7, on the Owner’s Word)

Draft points for the answer bead: the bound is accepted, with its margins.
Then the findings: the two 204 files are one point at two paddings; the side and
determined rows are Evan Daniel’s exact solver’s (Question 1); the licence and custody
of a file his tree no longer holds (Question 2); and which file came first (Question 3).
Then S2, and the adoption by the house rule.
