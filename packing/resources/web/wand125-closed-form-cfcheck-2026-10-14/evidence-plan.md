# Evidence-Update Plan: cfcheck on the Closed-Form Bound

This is the plan the records lane applies for bead think-3n1x (jlevy/squares#600). The
intake lane `wand125-cfcheck` wrote it on 14 October 2026 and changed no register.
It updates the closed-form lower bound that the
[9a28a84 register plan](../wand125-closed-form-2026-10-14/register-plan.md) registers as
`T-NNN`, with its reported evidence `E-wand125-closed-form-report`. Apply it in the same
change as that plan or after it.
Nothing here is on `main`. Every number comes from this packet’s [README](README.md) and
[`receipts/`](receipts/).

## The Claim Map

By [result-import.md](../../../campaign/result-import.md#stage-1-triage), new evidence
about a registered entry takes no new entry: the source retained at the revision that
holds it (this packet, at `746e2c5`), and an evidence update.

| Claim of the source | Register action |
| --- | --- |
| cfcheck, a Rust checker written from SPEC.md and the published bundles only, sharing no code with `replay4d`, `seam4d_core` or `validate_family.py` | A new verifier, `V-wand125-cfcheck`, with its `independence` record |
| cfcheck replayed intervals 1 and 34 completely, all eight records, and accepted all 3,138,681 leaves of 91,044 roots with no refusal | A new reported evidence entry, `E-wand125-closed-form-cfcheck-report`, cited by the closed-form entry. Its coverage is a sample of the certificate: 8 of 136 records |
| “The same leaf count as `replay4d` on these two intervals” | Stated in that entry; checked here: both receipts carry the published counts per kind and name only published input digests (`receipts/price.json`, `source_receipt_custody`) |
| The folder README no longer says that no independent checker exists | The closed-form entry’s `next_rung` and `composition`, which say it does, are rewritten (below) |
| The sample run here: premises in full on both intervals, 2,909 leaves accepted, three mutants refused | A new evidence entry, `E-wand125-closed-form-cfcheck-sample`, coverage a sample |
| The theorem, the intervals and the release | Unchanged at this pin: the folder’s other 25 files are byte-identical to the 9a28a84 packet’s |

## Evidence Entries

```yaml
- id: E-wand125-closed-form-cfcheck-report
  claim: lower-bound
  scope: {n_values: [<the 264 values of E-wand125-closed-form-report>]}
  assurance: reported
  reported_method: exact-algebraic
  performed_by: source-author
  relationship_to_generator: independent-implementation
  independence_record: packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/README.md
  independence:
    coverage: {extent: sample, unit: region records of the closed-form certificate, checked: 8, of: 136}
  origin: external
  novelty: previously-published
  source_key: '[wand125 cfcheck 2026-10-14]'
  certificate: packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/intervals.json.gz
  replay_status: not-attempted
  verifiers: [V-wand125-cfcheck]
  limitations: >-
    wand125/square-packing at 746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d (2026-10-14T10:38:27Z)
    adds problems/closed-form/indep-checker/, cfcheck, which its README says was written
    from SPEC.md and the published bundles only, shares no code with replay4d, seam4d_core
    or validate_family.py, which were not read, and was written with AI assistance (OpenAI
    Codex) and reviewed by the author. The source reports that it replayed intervals 1,
    (0, 1/50], and 34, (99/100, 1], completely, all four records of each: 91,044 roots and
    3,138,681 leaves accepted with no refusal, the published counts of every kind, in 242.02
    worker-hours of summed per-leaf time, with 24,226 roots of interval 1 resumed from
    checkpoints of earlier runs of the same checker that are not published. The other 32
    intervals were not checked with it. Of the record's counts, only the 33 at m^2 - 1, m^2 - 2
    and m^2 - 3 for m = 8 to 18 have a(N) attained on these intervals (interval 34, the cap
    k + 1), all proved already; none of the counts where a(N) is above the record is. Here
    the code was compared with the producer's: no file, line, comment, local crate or
    arithmetic kernel is shared, and the structure it shares traces to procedures SPEC.md
    states step by step. SPEC.md is the producer's description of its own checker's
    procedures, and the person who reviewed cfcheck wrote the producer's code, so it is an
    independent implementation of the producer's specification. The clean room is the
    source's statement, consistent with the code and not checkable here. A report, not a
    replay; a sample of the certificate.
  source_reviewed: '2026-10-14'

- id: E-wand125-closed-form-cfcheck-sample
  claim: lower-bound
  scope: {n_values: [<the 264 values of E-wand125-closed-form-report>]}
  assurance: verified
  method: exact-algebraic
  performed_by: repository
  relationship_to_generator: independent-implementation
  independence_record: packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/README.md
  independence:
    coverage: {extent: sample, unit: leaves of the closed-form certificate, checked: 2909, of: 187183108}
  origin: replayed-here
  novelty: previously-published
  source_key: '[wand125 cfcheck 2026-10-14]'
  certificate: packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/receipts/runs/interval-1-premises-and-kind-sample.json
  replay: >-
    Restore problems/closed-form/ in scratch from this packet and the 9a28a84 packet and
    match it to this packet's manifest; cargo fetch --locked, then cargo build --release
    --locked --offline in indep-checker/; unpack interval_0_0.02.tar.gz and
    interval_0.99_1.tar.gz of closed-form-v1, checked against ASSET.json and SHA256SUMS,
    under assets/ beside intervals.json; then run the three cfcheck commands that
    receipts/runs/*.json record, through replay/cfcheck_replay.py run. Each must exit 0
    with CFCHECK PARTIAL and no refusal; the three commands of receipts/controls/*.json,
    on the mutants replay/cfcheck_replay.py mutate writes, must each exit 1 with the
    refusal the receipt names.
  replay_status: passed
  verifiers: [V-wand125-cfcheck]
  limitations: >-
    Run here on 14 October 2026 from the retained cfcheck at 746e2c5, built with rustc
    1.97.0 (the source used 1.99.0), on four shared cores; its 42 tests passed. On intervals
    1 and 34 in full: every input digest, the structure of all four families, the region
    bounds, the product grid and 90-degree cover of the roots of all eight records, the
    bisection tiling of all 91,044 roots and the published counts, none refused. Leaf tests
    on a stated sample only: the first 200 leaves of each kind of interval 1's top.rec, the
    smallest record, and the first 25 (interval 1) and 20 (interval 34) leaves of each kind
    but B4U in each record, 2,909 distinct leaves of the 3,138,681, all accepted; 42.9
    CPU-minutes in all. A duplicated root, a leaf relabelled from CORE1:Tx to CORE and both
    families' masses scaled by 99/100, each re-sealed, were refused for the targeted reason.
    A complete replay of the two intervals is priced at 288 worker-hours by the source's own
    rates, about 320 to 650 CPU-hours here. A sample decides the leaves it checked and nothing
    about the others; it sets no rung.
  source_reviewed: '2026-10-14'
```

Both entries take the closed-form entry’s scope because both are about its certificate;
neither derives a rung at any count, since `devtools.check_results` counts no entry
whose coverage is a sample.
One alternative for the records lane: a report entry scoped to the 33 counts attained on
interval 34, with coverage full over the records those counts rest on.
It would derive nothing either, since it is a report and those counts are `proved` by
other routes, so this plan does not propose it.

## Verifier

Proposed for `packing/frontier/verifiers.yaml`, among the external programs.

```yaml
- id: V-wand125-cfcheck
  program: cfcheck (indep-checker), its coverage, family, region and interval commands
  author: wand125
  provenance: external
  language: [Rust]
  methods: [exact-algebraic]
  role: decides
  summary: >-
    Decides one interval of the closed-form certificate from SPEC.md: the input digests
    against SHA256SUMS and intervals.json; both families' structure (the wall period of
    mass 9/5, the reversal identities, the saving at both ends against the stored saving
    and the certified line, global against local agreement at k = 7, 8, 9, the right-side
    family); the region bounds; the product grid and 90-degree cover of each record's
    roots; the bisection tiling of every root; the published counts; and every leaf by its
    named exact test (EMPTY, CORE, B3D, EDGE, EX/EY, B3U, B3T, the nine CORE1 kinds, B4U),
    with no fallback between tests. Its coverage command checks that the 34 intervals
    partition (0, 1].
  source:
  - packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/square-packing/problems/closed-form/indep-checker/src
  - packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/square-packing/problems/closed-form/indep-checker/Cargo.toml
  - packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/square-packing/problems/closed-form/indep-checker/Cargo.lock
  versions:
  - revision: 746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d
    note: >-
      The commit that adds it. The source's production build used rustc 1.99.0; the
      build here used rustc 1.97.0 with the locked crates, and its release binary had
      SHA-256 c5a163d48d10155dbe6d319a8a8cae8cab3feb9278c6fb7116c2d0396e686484.
  independence_record: packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/README.md
  independence:
    read: [proof-text, specification, certificate-format, producer-output]
    clean_room: true
    shares: []
    written_by:
    - kind: person
      name: Hiroaki Hosono (wand125)
    - kind: ai
      system: Codex (OpenAI)
      setting: >-
        named by the checker's README, "written with AI assistance (OpenAI Codex),
        reviewed by the author"; role, tier and reasoning setting not stated
    - kind: ai
      system: Claude (Anthropic)
      setting: named co-author of the commit that adds it; its role is not stated
    overlaps_producer:
      extent: people
      separate_prompt: null
      separate_code: true
      note: >-
        The person who reviewed it, Hiroaki Hosono, wrote the producer's code, and issue
        #600 says the search, the certificates and both checkers were produced with Claude
        and Codex, so the authorship overlaps in the person and in both system families.
        clean_room is the source's statement ("which were not read"), which the code is
        consistent with and which cannot be checked here. The code shares no file, line,
        comment, local crate or arithmetic kernel with replay4d or seam4d_core
        (comparison/outputs/shared-code.json); its structural overlap, 8 to 23 times that of
        unrelated exact checkers, traces to procedures SPEC.md states step by step. SPEC.md
        is the producer's description of its own checker's procedures: cfcheck reads it as
        the specification and follows its names and constants, and reads the producer's
        published counts and five a(N) values of its README table as outputs to compare.
  note: >-
    Its relationship to the producer's code is independent-implementation. Its trust
    boundary is SPEC.md's procedures: an error in replay4d's code is one it can expose,
    and an error in a procedure SPEC.md prescribes is one it cannot. Not reviewed here
    for soundness; the mathematical review of 14 October 2026 read replay4d and SPEC.md,
    not cfcheck.
```

The registry exempts nothing here: the program is external, its relation is independent,
and the record carries the authorship fields that `devtools.verifier_registry` asks of a
new independent-implementation entry’s deciding program.
`clean_room: true` beside a `read` without `producer-code` is accepted.
If the records lane or the owner reads the producer’s review of the code as a reading of
`producer-code`, the record becomes `clean_room: false` with `producer-code` added to
`read`; the relation stays independent-implementation.

## What It Can Move, and What It Cannot

| Rung | Effect |
| --- | --- |
| `V` | None. The source’s run is a report, and the run here is a sample. The closed-form entry stays at `V0` until a complete replay passes here |
| `C1` | None. It comes from the mathematical review (think-tsox) when that is recorded as the entry’s `external_review` |
| `C3` | None. It needs one complete replay of every load-bearing part. A second route over 2 of 34 intervals is a sample, whether reported or replayed here, and sets no `C3` |
| The independence attribute | Beside the rung only: *sampled, 8 of 136 records, independently re-implemented by the source, from the producer’s specification*. A sample is never called confirmed |
| Case lanes | None at any count. The 156 counts where $a(N)$ is above the reported lower bound rest on intervals 2 to 33, which cfcheck has not checked |

What would move a rung later:

- **A complete replay of all 136 records by cfcheck here** would set `C3` at the level
  *independently re-implemented, clean-room as the source states it*, from the
  producer’s specification, by an authorship that overlaps the producer’s. That is a
  higher level than a complete `replay4d` replay, which is reproduced with the
  producer’s code. Priced at about 9,900 worker-hours (6,800 to 16,200) against
  `replay4d`’s 4,294, by the two checkers’ costs on intervals 1 and 34.
- **A complete replay of interval 34 alone** would complete the closed-form route at the
  33 counts $m^2 - j$ attained there: 156.2 worker-hours by the source’s rates.
  Those counts are `proved` by T-084, T-086 and T-064, so no rung would move.
  Each would gain a sentence naming the route.
- A replay here must not resume from the source’s checkpoints, which are not published.

## Prose of the Closed-Form Entry

Applied together with the 9a28a84 register plan’s entry:

- **`next_rung`.** Its last sentence, “An independently written checker of the leaf
  tests would be a second route beside the rung; the source says none exists”, becomes:
  “The source’s second checker, cfcheck, written from SPEC.md and sharing no code with
  replay4d (E-wand125-closed-form-cfcheck-report), has checked intervals 1 and 34 of the
  34; a complete replay of all 136 records by it would be a second route at a higher
  level, priced at about 9,900 worker-hours.”

- **`composition`.** After “A replay here would run the source’s replay4d unchanged, one
  implementation of one method”, add: “The source’s cfcheck is a second implementation
  of SPEC.md’s procedures, sharing none of replay4d’s code, run by the source on 8 of
  the 136 records and here on a sample of 2,909 leaves.”

- **`unfinished_confirmations`.** Beside the replay4d replay (C3, 4,294 CPU-hours), add:

  ```yaml
  - what: >-
      a complete replay of all 136 records by cfcheck built from the retained crate at
      746e2c5 with its locked dependencies, from no resumed checkpoint, with the three
      re-sealed mutants refused by the same build
    rung: C3
    link: think-3n1x
    estimated_cost:
      cpu_hours: 9900
      basis: >-
        The source's cfcheck receipts price intervals 1 and 34 at 288.45 worker-hours
        (242.02 recorded, 46.43 for resumed leaves at the source's per-kind rates), 2.31
        times replay4d's 124.65 CPU-hours on the same eight records; that ratio applied to
        replay4d's 4,294 CPU-hours for all 136 gives about 9,900, between 6,800 and 16,200 at
        the two intervals' own ratios. On this host the sampled leaves ran at 1.11 to 2.39
        times the source's rates.
      priced: '2026-10-14'
  ```

- **`evidence`.** Add `E-wand125-closed-form-cfcheck-report` and
  `E-wand125-closed-form-cfcheck-sample`.

- **T-084, T-086 and T-064.** The sentence the 9a28a84 plan adds, naming the closed-form
  route to $s(m^2 - j) = m$ for $m \ge 8$, may add that the source’s cfcheck has checked
  interval 34, which that route rests on.

## Bibliography and Coverage

Applied in this branch: `[wand125 cfcheck 2026-10-14]` in
`packing/resources/bibliography.yaml` and the Web Sources table of
`packing/resources/README.md`, `dated` by the pin.
`credit: wand125`, since neither README names a method it builds on.
`lineage: independent`, since neither cites this project.

```yaml
- id: wand125-closed-form-cfcheck-2026-10-14
  title: Independent checker cfcheck for the closed-form bound, intervals 1 and 34, issue 600
  role: source-repository
  url: https://github.com/wand125/square-packing/tree/746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d/problems/closed-form/indep-checker
  local: resources/web/wand125-closed-form-cfcheck-2026-10-14/
  source_key: '[wand125 cfcheck 2026-10-14]'
  scope: {n_values: [<the 264 values>]}
  reviewed: '2026-10-14'
  source_date: '2026-10-14'
  disposition: current-report
  replay_disposition: case-specific
  represented_by:
  - resources/web/wand125-closed-form-cfcheck-2026-10-14/README.md
  evidence:
  - E-wand125-closed-form-cfcheck-report
  - E-wand125-closed-form-cfcheck-sample
  notes: >-
    Revision 746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d, retrieved at 2026-10-14T11:34:13Z, the
    child of the 9a28a84 pin; it adds indep-checker/ and changes the folder README, and the
    folder's other 25 files are byte-identical. cfcheck, the source's second checker, written
    from SPEC.md and sharing no code with replay4d, accepted every leaf of intervals 1 and 34
    by the source's receipts (3,138,681 leaves); here its premise checks passed in full on both
    intervals and a sample of 2,909 leaves was accepted, with three re-sealed mutants refused.
```

## Validation, Priced

| Check | Status | Cost |
| --- | --- | --- |
| Custody of the two interval assets and `SHA256SUMS` against `ASSET.json`, the API digests and each archive’s `SHA256SUMS` | Done here | Seconds |
| Build from the retained copy, locked crates, and cfcheck’s 42 tests | Done here | 38 s build; 16.5 s wall and 28.8 CPU-s of tests |
| Code comparison with the producer, three baselines and a positive control | Done here | 6 s |
| Premises in full on intervals 1 and 34 | Done here, none refused | Within the runs below; the premises-only duplicate-root control on interval 1 took 14.6 CPU-s |
| Leaf tests on 2,909 leaves | Done here, all accepted | 42.9 CPU-minutes with the controls |
| Three re-sealed mutants | Done here, each refused for its reason | 29 CPU-s |
| A complete replay of intervals 1 and 34 | Not run: priced | 288.45 worker-hours by the source’s rates; about 320 to 650 CPU-hours here, 80 to 160 hours of wall on four dedicated cores. B4U is 61.1 of the source-rate hours, 111 single tasks of about 33 minutes |
| A complete replay of all 136 records by cfcheck | Not run: priced | About 9,900 worker-hours (6,800 to 16,200) |
| A soundness review of cfcheck against SPEC.md | Not run | Agent time at the strongest tier; about 6,300 lines of Rust |

No CPU-hour budget is set, so the replays wait in think-3n1x for the owner.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
