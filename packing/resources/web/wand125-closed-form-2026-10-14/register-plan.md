# Register Plan: wand125’s Closed-Form Lower Bound

This is the plan the records lane applies at stage 3 of the
[result import process](../../../campaign/result-import.md#stage-3-record), for bead
think-tsox. The intake lane `wand125-cf` wrote it on 14 October 2026 and changed no
register. Nothing here is on `main`, and the `T-NNN` is taken by the records lane in the
commit that registers the result.
Every number comes from the receipts of this packet:
[`evaluation/outputs/bounds.json`](evaluation/outputs/bounds.json), with one row per
count in [`evaluation/outputs/counts.tsv`](evaluation/outputs/counts.tsv), and
[`receipts/`](receipts/).

## The Claim Map

| Claim of the source | Register action |
| --- | --- |
| **Theorem**: for every non-square $N \ge 49$ with $k = \lfloor\sqrt N\rfloor$, $s(N) \ge a(N)$, the closed form of SPEC.md §1.1 on 34 intervals | One `lower-bound` entry stating the theorem. Its `scope` is the 264 non-square counts 50 to 323 that this record holds. |
| Above the case’s reported lower bound at 156 counts | The reported lane at 155 of them. At $n = 125$ the earlier report T-144, which is pending adoption, is stronger (see below). |
| Above the case’s verified lower bound at 189 counts | No change until stage 4. These are the counts the verified lane would take once the theorem is confirmed. |
| $s(m^2 - 1) = s(m^2 - 2) = s(m^2 - 3) = m$ for $m \ge 8$ | No new entry and no change of scope. These are consequences that T-084, T-086 and T-064 already register, at the verified lane, so the older claims each gain a sentence naming the newer route. |
| $a(N) > F(N)$, Nagamochi’s capped formula, at every non-square $N \ge 49$ but $m^2 - 1$ and $m^2 - 2$, where both are $m$ | Stated in the entry’s claim. If the theorem is confirmed, it re-establishes T-007’s values for $N \ge 49$ without Lemma 1 (T-085), and is stronger everywhere else. |
| $a(N) > K(N)$, Karakuş’s Corollary 6.2 (T-083), except at $m^2 - 1$ | Stated in the claim. T-083 holds the verified lane at 187 of the 189 counts. |
| The site’s count of $N \le 3600$ against its own choice of known bounds | Beyond the case corpus. It stays in the packet. |

No count’s upper bound is below $a(n)$ (the possible-error check), and no open case is
settled: the 33 counts where $a(n)$ meets the verified upper bound are the $m^2 - j$
values above, already `proved`.

## Who Holds Each Value Now

- **Reported lane, the 156 counts above it**: Nagamochi’s closed form (T-007) at 149;
  Green’s DS7 Theorem 9 by monotonicity at 125, 148, 173, 261 and 294; wand125’s linear
  certificate of 2 October (T-080) by monotonicity at 104 and 105.
- **Reported lane, the 75 counts below it**: wand125’s own measure certificates and
  exact covers at 40 counts, 50–59, 65–77, 82–95 and 101–103. Evan Daniel’s
  $s(m^2 - 4) = m$ (T-081, V0/C1) holds 96, 117, 140, 165, 192, 221, 252, 285 and 320.
  Daniel’s cover holds 60. Green’s DS7 values hold the first counts of each block from
  122, 25 in all.
- **Verified lane, the 189 counts above it**: Karakuş’s strip bound (T-083) at 187, and
  T-080 by monotonicity at 104 and 105.
- **Verified lane, the 42 counts below it**: wand125’s and Daniel’s replayed measure
  certificates and covers, 50 to 103.
- **The 33 equal counts**: $m^2 - 1$ is Karakuş’s (T-084); $m^2 - 2$ is chelokot’s Lean
  proof (T-086); $m^2 - 3$ is Daniel’s Valid7 (T-064), or at 61 and 78 the $n = 60$ and
  $n = 77$ covers by monotonicity.

**The one earlier, stronger report.** T-144 (wand125, 10 October, V0/C0) reports
$s(n) \ge 563/50 = 11.26$ at 122 to 126, with the case lanes left unchanged, so it is
pending adoption. $a(125) = 11.2545798369\ldots$ is below 11.26, so at $n = 125$ this
import is not the strongest report, and by the 14 October ledger’s rule its reported
lane should not take $a(125)$. $a(126) = 11.3133238509\ldots$ is above 11.26, so the
closed form is the strongest report at 126. This lane checked no other pending report;
the coordinator’s per-count ledger decides between reports in order.

## Bibliography

Applied in this branch: `[wand125 closed form 2026-10-14]` in
`packing/resources/bibliography.yaml` and the Web Sources table of
`packing/resources/README.md`. `dated` is the pin’s date.
`credit: wand125`, since the folder names no method it builds on.
`lineage: independent`, since the folder neither credits this project nor builds on it:
it cites jlevy/squares#295 only for the public discussion of Nagamochi’s gap.
That reading is the records lane’s or the owner’s to confirm.

## Coverage Entry

```yaml
- id: wand125-closed-form-2026-10-14
  title: Closed-form lower bound for every non-square N >= 49, no issue
  role: source-repository
  url: https://github.com/wand125/square-packing/tree/9a28a84bd55dc124bfa2919bb6c4fb504dda3149/problems/closed-form
  local: resources/web/wand125-closed-form-2026-10-14/
  source_key: '[wand125 closed form 2026-10-14]'
  scope: {n_values: [<the 264 values of the entry's scope>]}
  reviewed: '2026-10-14'
  source_date: '2026-10-13'
  disposition: current-report
  replay_disposition: case-specific
  represented_by:
  - resources/web/wand125-closed-form-2026-10-14/README.md
  evidence:
  - E-wand125-closed-form-report
  notes: >-
    Revision 9a28a84bd55dc124bfa2919bb6c4fb504dda3149, retrieved at 2026-10-14T09:29:10Z;
    problems/closed-form is unchanged since eb0fd19 of 13 October. A theorem for every
    non-square N >= 49 from a C4-symmetric segment measure on 34 intervals of the fractional
    part; above the reported lower bound at 156 counts and the verified one at 189. The
    source's structure check passed here on all 68 families and an exact evaluation here
    agrees with the source's a(N) at every count to 3600; the 136 records (4,294 CPU-hours
    by the source) are not replayed. The release is pinned by digest and not retained.
```

The source date is the commit that first holds the certificate, eb0fd19, at
2026-10-13T09:36:19Z. The release was published 17 seconds earlier.

## Evidence Entry

```yaml
- id: E-wand125-closed-form-report
  claim: lower-bound
  scope: {n_values: [<the 264 values>]}
  assurance: reported
  reported_method: exact-algebraic
  performed_by: source-author
  relationship_to_generator: same-implementation
  origin: external
  novelty: previously-published
  source_key: '[wand125 closed form 2026-10-14]'
  certificate: packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/intervals.json.gz
  replay_status: not-attempted
  verifiers: [V-wand125-replay4d]
  limitations: >-
    wand125/square-packing problems/closed-form (closed-form-v1), on no issue, reports
    s(N) >= a(N) for every non-square N >= 49: on each of 34 intervals of delta a family
    of line segments defines, for every k >= 7, a C4-symmetric measure on [0, k + delta]^2
    of total mass (k + delta)^2 - 4 S(delta) with mass at least 1 on every closed unit
    square, checked in four local regions by 187,183,108 exact leaf tests in 136 records.
    The source reports every record replayed and accepted by replay4d (Rust, exact rational
    and real-algebraic arithmetic; 4,294 CPU-hours over 269 runs on two machines), the
    published build replaying intervals 1 and 34 again (124.65 CPU-hours), and all 68
    families passing structure/validate_family.py. replay4d shares its core, seam4d_core,
    with the source's search tools, so the source's replay is not independent of its
    producer. Here: complete custody of the 35 release assets (815,734,366 bytes) against
    ASSET.json, the release API digests and SHA256SUMS; the source's structure check run
    unchanged on all 68 families, ALL STRUCTURE OK, with its results equal to the source's
    receipt, whose validate_family digest (fdd61866...) is not the published script's
    (22e55f17...), and two mutations refused; and an exact evaluation of a(n) at every
    count, which decides only what the theorem implies. No record was replayed here.
  source_reviewed: '2026-10-14'
```

## Verifiers

Proposed for `packing/frontier/verifiers.yaml`. Only the first is named by the evidence
entry above; the other two belong to the evidence entries for the structure run and the
evaluation, if the records lane registers those runs as evidence, as the packet’s
receipts would support.

```yaml
- id: V-wand125-replay4d
  program: replay4d, with seam4d_core, driven by checker/replay_all.py
  author: wand125
  provenance: external
  language: [Rust, Python]
  methods: [exact-algebraic]
  role: decides
  summary: >-
    Decides one region record of the closed-form certificate: that its roots are exactly
    the product grid of the region, its leaves tile each root by midpoint bisection, and
    each leaf passes its named exact test (EMPTY, CORE, B3D, EDGE, EX/EY, B3U, B3T, the nine
    CORE1 kinds, B4U) against the family.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/replay4d/src/main.rs
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/seam4d_core/src/lib.rs
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/seam4d_core/src/replay.rs
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/seam4d_core/src/b3d.rs
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/seam4d_core/src/fast.rs
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/replay_all.py
  versions:
  - {sha256: 92002e0e8924d96f0e5962eabb8fce6e4de67a2f350ca66d4889abee0762c193, note: "replay4d's printed source hash of the published crates; the source's full replay ran 306ad4b5..., which differs in comments only, as the source says"}
  note: >-
    Not built or run here. The source says seam4d_core is the code its search tools use to
    evaluate leaves, so a replay with it is the producer's own code re-run.
- id: V-wand125-closed-form-structure
  program: structure/validate_family.py, run by structure/structure_all.py
  author: wand125
  provenance: external
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Checks each family's format and nonnegativity, the wall profile on the 1/5 grid with
    mass 9/5 per period, the corner separation, the saving at both ends against the
    certified line and delta/2, the total mass and C4 invariance for k = 7, 8, 9, agreement
    with the local model on [0, 24/5]^2, the reduction of k >= 10 by wall shifts, the
    right-side family, and the region bounds.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/structure/validate_family.py
  - packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/structure/structure_all.py
  versions:
  - {sha256: 22e55f17f29a0568f7def24f358d9ad15912c503b0c0af6b1104911543f21786, note: validate_family.py as published and as run here}
  - sha256: 7e32c71d6e9bf65954a34739705543b34db827558589ebc7aec5d9c878044943
    path: packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/structure/structure_all.py
    note: structure_all.py
  note: >-
    Run here unchanged on 14 October 2026 (receipts/structure-check/). The source's receipt
    names validate_family.py at fdd61866..., which is not the published file.
- id: V-closed-form-evaluation
  program: closed_form_bounds.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Decides, from the retained intervals.json, what the closed-form theorem implies at
    each count 49 to 324 by two routes, the closed form and the theorem's inequality, and
    compares the value exactly with every case bound.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/evaluation/closed_form_bounds.py
  versions:
  - {sha256: 1a430c0925d5abb20a0782f95aaff443d6b7bb77750b416a8a67f10a8df1e251}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/evaluation/README.md
  independence:
    read: [mathematics, proof-text, producer-code]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the intake lane wand125-cf of the 14 October intake, tbd-moderate tier
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: >-
        The source's commit names Claude Opus 5.5 as co-author. Written by a Claude agent
        in a file of its own that imports none of the source; its authors had read
        a_of_n.py, README.md and SPEC.md first.
  note: It decides nothing about the measure certificate.
```

## The Register Entry

```yaml
- id: T-NNN
  kind: lower-bound
  registered: '2026-10-14'
  headline: "Closed-form lower bound `s(N) ≥ a(N)` for every non-square `N ≥ 49`; `50 ≤ n ≤ 323` are the cases held here, reported"
  claim: >-
    For every non-square integer N >= 49, with k = floor(sqrt(N)), wand125 reports
    s(N) >= a(N) = k + sup{delta in (0, 1] : (k + delta)^2 - 4 S*(delta) < N}, where
    S*(delta) is the largest of 34 certified savings alpha_i delta + beta_i, exact
    rationals, over the intervals of delta that contain it. In closed form a(N) is the
    largest of min(2 alpha_i + sqrt(4 alpha_i^2 + N + 4 beta_i - 4 alpha_i k), k + d1_i)
    over the intervals whose root exceeds k + d0_i: one square root on each interval.

    The certificate is a measure on the container of side k + delta: Lebesgue measure in
    the middle and, for each interval, a family of line segments along the walls and in the
    corners, C4-symmetric, with total mass (k + delta)^2 - 4 S(delta) for every k >= 7 and
    mass at least 1 on every closed unit square. The source checks the last by 187,183,108
    exact leaf tests in 136 records of four local regions, every one replayed by its Rust
    checker replay4d (4,294 CPU-hours), and the structure of all 68 families by an exact
    Python check.

    At the counts held here it is above the reported lower bound at 156 counts, n = 104 to
    116, 125 to 139, 148 to 164, 173 to 191, 201 to 220, 230 to 251, 261 to 284 and 294 to
    319, mostly Nagamochi's closed form, and above the verified lower bound, Karakus's
    strip bound, at 189: s(104) >= 10.288527854902856…, s(230) >= 15.212985634623918…,
    s(319) >= 17.950279622148055…. It is above no upper bound. It exceeds Nagamochi's
    capped formula at every other non-square N >= 49 than m^2 - 1 and m^2 - 2, without
    Nagamochi's Lemma 1 (T-085), and because S*(1) > 3/4 it gives
    s(m^2 - 1) = s(m^2 - 2) = s(m^2 - 3) = m for m >= 8, values this record already holds
    (T-084, T-086, T-064).

    Here the source's structure check passed on all 68 families from the release, and an
    exact evaluation written here derives a(n) at every count from the retained intervals
    by two routes; both agree with the source's own a(N) at every count to 3600. No
    record has been replayed here, so the bound stands as reported.

    wand125, [square-packing](https://github.com/wand125/square-packing/tree/9a28a84bd55dc124bfa2919bb6c4fb504dda3149/problems/closed-form),
    13 October 2026. The commit that adds it names Claude Opus 5.5 as co-author.
  scope: {n_values: [<the 264 values>]}
  verification: V0
  confirmation: C0
  significance:
    score: 4
    rationale: >-
      Scored as a claim: a bound family for every non-square N >= 49, by one new measure
      construction, that raises the reported lower bound at 156 of the counts held here
      and would raise the verified one at 189, and re-proves Nagamochi's values at
      N >= 49 without his Lemma 1. S4 by the anchor "a reusable technique, bound family,
      or resolved disputed value". The score is the theorem's, not ours.
    scored: '2026-10-14'
    by: the wand125-cf intake lane (think-tsox; draft)
  novelty: previously-published
  attribution:
    source_keys: ['[wand125 closed form 2026-10-14]']
    published: '2026-10-13'
  composition: >-
    One reported certificate on its reported entry. The theorem rests on the measure
    principle (SPEC.md 1.2), the total-mass identity (1.3), the reduction of every square
    to four local regions for k >= 7 (2.2, 2.3), the structure of each family, every leaf
    of every record, the coverage of (0, 1] by the intervals, and the chord of the affine
    saving on each interval. The value at each count is derived from the intervals by
    V-closed-form-evaluation, exactly. A replay here would run the source's replay4d
    unchanged, one implementation of one method.
  evidence:
  - E-wand125-closed-form-report
  artifacts:
  - packing/resources/web/wand125-closed-form-2026-10-14/README.md
  - packing/resources/web/wand125-closed-form-2026-10-14/receipts/release-custody.json
  - packing/resources/web/wand125-closed-form-2026-10-14/receipts/structure-check/run.json
  - packing/resources/web/wand125-closed-form-2026-10-14/evaluation/closed_form_bounds.py
  - packing/resources/web/wand125-closed-form-2026-10-14/evaluation/outputs/bounds.json
  next_rung: >-
    C1 needs the mathematical review that reads the proof (SPEC.md, the structure check
    and replay4d's trust boundary), which starts at intake in its own lane. C3 needs a
    complete replay of all 136 records by replay4d from the retained crates, built with
    the locked Cargo.lock, with the structure check, two mutated records refused, and that
    review; the source prices it at 4,294 CPU-hours. An independently written checker of
    the leaf tests would be a second route beside the rung; the source says none exists.
  unfinished_confirmations:
  - what: >-
      the mathematical review of SPEC.md, the families' structure check and replay4d's
      trust boundary, recorded under docs/project/reviews/
    rung: C1
    link: think-tsox
  - what: >-
      a complete replay of all 136 records (187,183,108 leaves) by replay4d built from the
      retained crates with the locked dependencies, through replay_all.py, with the
      structure check and two mutated records refused by the same build
    rung: C3
    link: think-tsox
    estimated_cost:
      cpu_hours: 4294
      basis: >-
        The source's own complete replay, receipts/replay.json: 4,294.08 CPU-hours summed
        from replay4d's cpu_seconds over 269 runs on two Ubuntu 24.04.5 machines (rustc
        1.86.0). Not calibrated here: the smallest records take 0.27 to 0.32 CPU-hours by
        the source, so a calibration on two of them, plus the build of GMP from source,
        is about one CPU-hour.
      priced: '2026-10-14'
  notes: >-
    V0 because the cited entry is the source's public claim: assurance reported, replay
    not attempted. C0 because no review of it is on file yet.
```

## Case-Record Changes

**Reported lane, 155 counts**: 104–116, 126–139, 148–164, 173–191, 201–220, 230–251,
261–284 and 294–319, leaving 125 to T-144 as above.
Each takes the row of `counts.tsv` for its count, in this shape (at $n = 104$):

```yaml
reported_lower_bound:
  value: '10.288527854902'
  exact_form: <a(n) rounded down at 30 places, as p/10^30, or the exact root of evaluation/outputs/exact-forms.json>
  kind: counting
  proved_by: [wand125]
  proved_year: 2026
  source_key: '[wand125 closed form 2026-10-14]'
  note: >-
    wand125's closed-form bound (13 October 2026): s(N) >= a(N) for every non-square
    N >= 49, from a measure of line segments on 34 intervals of the fractional part,
    replayed by the source's replay4d and not yet here. At n = 104, k = 10 and interval
    6, [1/5, 19/50], gives a(104) = 10.2885278549028…. The commit names Claude Opus 5.5
    as co-author.
  scope: Unrestricted unit-square packing with independent rotations and disjoint interiors.
  evidence: [E-wand125-closed-form-report]
```

`value` is $a(n)$ rounded down at 12 places, which the theorem implies, as the source
says of its own rounded-down prints.
The exact root runs to about a thousand characters.
This lane recommends the 30-place rational for `exact_form`, which is exact, short and
within $10^{-30}$ below $a(n)$, with the note naming the interval.
The records lane chooses.
Two other routes exist: leaving the lanes unchanged with per-count values in the claim,
as T-144 did, or leaving `exact_form` null, as the Nagamochi rows do.

**Verified lane**: no change until stage 4. The 189 counts it would take are listed in
the summary of `bounds.json`.

**Prose and other entries**:

- Each case record that cites the key owes the sentence on AI assistance.
  The commit names Claude Opus 5.5 as co-author (`devtools.state_ai_assistance`).
- T-084, T-086 and T-064 each gain a sentence naming the closed form’s route to their
  values for $m \ge 8$.
- T-007’s and T-083’s notes may say that, if the theorem is confirmed, it implies their
  values at $N \ge 49$ (T-007’s at $m^2 - 1$ and $m^2 - 2$ only as equality) and exceeds
  them elsewhere.

## Validation, Priced

| Check | Status | Cost |
| --- | --- | --- |
| Custody of the 35 release assets against ASSET.json, the release API digests and SHA256SUMS | Done here | 43 s download, under 1 s to hash |
| The source’s structure check on all 68 families, with two mutations | Done here: ALL STRUCTURE OK, mutations refused | 68 s wall, 44 CPU-s |
| An independent exact evaluation of $a(N)$ against the case records, with four controls | Done here | 19.5 s wall, 17.9 CPU-s |
| The source’s `a_of_n.py`, 49 to 3600, as a cross-check | Done here: identical at 3,498 counts | 5.5 s |
| A complete replay of the 136 records by replay4d | Not run: priced, and held by the owner’s 40 CPU-hour cap (think-wu73) | 4,294 CPU-hours by the source’s receipt, about 5,250 here by the calibration below. That is about 1,310 hours of wall on four dedicated cores, or about 82 hours on 64. It also needs 18 GB unpacked, network access to crates.io for the locked crates, and GMP built from source. |
| A calibration replay of the two smallest records, with the build | Done after the intake (think-au7j): both `REPLAY OK`, three controls refused or accepted as expected; ratio to the source 1.223 | 0.75 CPU-hours, plus the toolchain download; the complete replay is about 5,250 CPU-hours here |
| A mathematical review of SPEC.md, the structure check and replay4d’s trust boundary | Not run: runs in its own lane | Agent time at the strongest tier. The reading list in the packet README is about 6,200 lines |
| An independently written checker of the leaf tests | Not planned: a W7 slice | Its engineering, plus a run likely of the same order as the source’s replay |

The owner’s cap of 14 October holds anything above 40 CPU-hours, so the complete replay
waits in think-wu73 for the owner.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
