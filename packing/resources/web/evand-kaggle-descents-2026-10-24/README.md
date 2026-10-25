# Evan Daniel’s Exact Descents of Public Kaggle Packings at 8a8879a

This packet retains the certificates Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/8a8879a2972c32cbd2d906049228cc9f0762b02a/search/packer/candidates)
adds at `8a8879a2972c32cbd2d906049228cc9f0762b02a` (authored 2026-10-24T04:38:50Z,
committed 04:49:33Z), which GitHub’s activity log records pushed at 2026-10-24T04:53:53Z.
No issue reports them. A certificate published in a watched repository is a report from
its publication (the owner, 14 October 2026), so the record takes two of the three:

- **268, recorded as T-242:** `s268_lightning.cert`,
  $s(268) \le 8437180857934672912242411148233/(5 \times 10^{29}) =
  16.874361715869345824484822296466$, 4.48e-12 below T-240 (#763) and 4.45e-3 below
  T-174, the case’s house.
- **304, recorded as T-242:** `s304_pub.cert`,
  $s(304) \le 1792689890035674158972360842897/10^{29} = 17.92689890035674158972360842897$,
  3.04e-9 below T-241, Francisco Couzo’s certificate of the same packing at `fa6237e`
  ([packet](../couzo-n304-2026-10-23/README.md)), and 2.53e-3 below T-186, the house.
- **303, not recorded:** `s303_cdeotte.cert`,
  $s(303) \le 17907238274538241192624181047171/10^{30}$, 2.60e-4 above T-240’s 303, which
  #763 reported first. It is retained as credit evidence only ([303](#303)).

T-242 registers 268 and 304, with T-241 before it at 304, at `V3`/`C3` since the
[stage 4 review of 24 October](#stage-4-review). Both are the smallest validated sides at
their counts, so the cases adopt them under the house rule: 304 in the pull request that
maps the review, and 268 in the next one, since the adoption of #763’s entry (T-240)
already moves 268 in the pass of 25 October and one day’s archive holds one prior state a
count.

The source was read on 24 October 2026 from a blobless clone whose head stood at
`659ee62e4a9d39542a1146e8b011cc3ab6407ede`, which leaves every retained file unchanged.

## What the Author Claims

The commit message, in full apart from its trailer:

> Candidates s(268), s(303), s(304): certificates for three posts beyond the register
>
> s268_lightning: Vladislav Lavrentev’s (Kaggle lightningv08) public packing, exact descent
> (shrink-only) to 16.8743617159, the side a Kaggle per-puzzle side-only claim lists; the
> first public packing at that side. s303_cdeotte: Chris Deotte’s public Kaggle packing,
> exact descent to 17.9072382745. s304_pub: the public Kaggle packing at 17.9268989004
> (finder unknown; earliest public copy: kozykappa’s notebook). Posting approved by Evan in
> chat 10-23 (304 on behalf, 268 first public; 303 cdeotte’s).

Each certificate’s JSON report (`sNNN_*.json`) states its `S_cert`, which is the
certificate’s header side; `cert_valid` true at 80 digits; least wall and pair
clearances of `5e-21` and about `1e-20`; `S_input`, the binary64 side of the packing it
descends from (16.87436171586941 at 268, 17.926898901941495 at 304); and `S_exact`, the
side of a Newton-converged KKT point. From those two sides, `S_cert` exceeds `S_exact` by
about 1.7e-19 at 268 and 1.8e-19 at 304, a relative padding of 1e-20 (computed here; the
JSON states the sides, not the gap). At 268 it also reports 19 free squares and a second-order analysis with
127 exact flat motions (`dim_null`). The `_vs_prior.json` files compare each descent with
the source store’s prior best at the count and call each a “distinct minimum”.

The source’s next commit, `659ee62`, records in `Completed.md`: “certified the public
Kaggle packings (8a8879a2; 268 and 303 by exact descent of lightningv08’s / cdeotte’s
packings) but did not post: franciscouzo’s open #763 already held all three”, and in
`TODO.md`: “the packing first appears in lightningv08’s CUDA Packing Search output,
kirilltym’s input”.

These statements are the author’s. No source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 27 files of 657,988 bytes: 19 retained under
[source/](source/) (478,041 bytes) and 8 pinned by digest.

| Count | Retained under `source/search/packer/candidates/` | SHA-256 of the certificate |
| ---: | --- | --- |
| 268 | `s268_lightning.cert`, `.json`, `.input.txt`, `.predescent.txt`, `.exact.txt`, `_prior.json`, `_vs_prior.json`, and the regularized display view `_regularized.cert` and `.json` | `c87da316589dd384…` |
| 303 | `s303_cdeotte.cert` and `.json` | `6cf9cc95a48f957d…` |
| 304 | `s304_pub.cert`, `.json`, `.input.txt`, `.exact.txt`, `_prior.json`, `_vs_prior.json` | `5dd7436a0f658d36…` |

The licence and `CREDITS.md` are retained beside them.
Pinned by digest: the other six files at 303, and the two exact checkers the
certificates name, `search/exact/verify_cert.py` and `verify_cert2.py`, against the
identical copies the [n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 0.5 MB, and `check_added_blobs` passed before the first commit, so it
is kept in Git.

## Report Order

The [ledger of 24 October for this import](../../../campaign/issue-intake/upper-bounds-evand-20261024/README.md)
walks the two publications in the order of the pushes that made them public, as the
record dates a commit a later push published (`8a8879a` by its push at 04:53:53Z,
`fa6237e` by the push at 23:38:42Z on 23 October), against the starts frozen at `main`
`2ec489d1`:

- **268:** T-240 (#763, 23 October 23:35:51Z), pending adoption, then this commit:
  recorded, 4.48e-12 below. The two sides print differently at 12 places
  (16.874361715874 and 16.874361715870), so the restatement ruling does not reach it.
- **303:** T-240, then this commit: not recorded, 2.60e-4 above.
- **304:** T-186, the house; Couzo’s `fa6237e` (T-241, pushed 23 October 23:38:42Z,
  committed at 18:59:39Z), recorded 2.53e-3 below; then this commit, recorded 3.04e-9
  below that. Dating either by its commit instead changes no verdict, since nothing else
  reached 304 between them.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `2ec489d1` on 24 October
2026):

| n | Case house | Below the house by | Nearest report | Relation |
| ---: | --- | --- | --- | --- |
| 268 | T-174 | 4.45e-03 | T-240 (#763) | below by 4.48e-12 |
| 303 | T-239 | 2.52e-03 | T-240 (#763) | above by 2.60e-04 |
| 304 | T-186 | 2.53e-03 | T-241 (`fa6237e`) | below by 3.04e-09 |

Every other report at each count is further above.

## Pose by Pose

[measure/identity.py](measure/identity.py) measures each certificate against the packings
its credit names, with the measures of the
[20 October packet](../evand-regularized-2026-10-20/measure/identity.py) loaded
unchanged, and writes [measure/identity.json](measure/identity.json). A measurement for
credit; it decides nothing.

- **268.** The certificate is the source’s input, Lavrentev’s packing, descended: no
  square moves beyond 1e-3 (largest 1.41e-4). Against T-240 it is one arrangement and
  another placement. Nearest centres pair the two one to one under the mirror
  $x \mapsto s - x$, with none beyond 0.1 but 135 squares beyond 1e-3 and 165 beyond 1e-9
  (largest 7.08e-2, largest turn 1.36°). It is not T-240’s packing re-solved; the stage 4
  review of T-240 of 24 October (think-zjus, its RF-6) measured the same, a sibling
  placement, Lavrentev’s and not #763’s. Against #763’s Kaggle parent (Kirill
  Tymchishin’s EDA+Seam LP v4 packing, `certificates/parents/85dbd707…` in the
  [issue-763 packet](../couzo-issue763-2026-10-23/README.md)) it pairs under the identity,
  none beyond 0.1 (largest 2.49e-2). The source’s `s268_lightning.predescent.txt` is that
  parent to 2.47e-10. The regularized display view pairs with the certificate only by an
  optimal assignment (9 squares beyond 0.1), and is not registered here.
- **304.** Nearest centres pair the certificate with T-241’s packing under the identity,
  none beyond 1e-3 and 73 beyond 1e-6 (largest 4.60e-4, largest turn 0.019°). The
  source’s binary64 input is T-241’s packing to 2.05e-9. So the certificate is T-241’s
  packing descended, which T-242 lists as a regularization of T-241. Against T-186 no
  symmetry pairs it one to one by nearest centres; the optimal assignment, best under the
  diagonal reflection, keeps 250 of 304 squares within 0.1 and moves 54 beyond it (largest
  1.13), as for T-241: another arrangement, and a resemblance that states no lineage.
- **303.** Against T-240’s 303, one to one under the anti-diagonal reflection, 4
  squares beyond 0.1 (largest 0.238), 71 beyond 1e-3.

## Exact Replay

`devtools.upper_bound_reports certify` decided the three certificates and their
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 9 jobs, 765,522 pair decisions, 118.9 route CPU seconds, the longest
job 15.69 seconds ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
Each certificate clears every wall by exactly 5e-21 and every pair by at least
9.99e-21.

Those margins are below the binary64 spacing of the coordinates, so the gross controls
cannot tell an exact route from one that rounds.
[receipts/sharp_controls.py](receipts/sharp_controls.py) takes each registered
certificate to exact contact and 1e-30 past it: the side lowered by the least far-wall
clearance, the least-gap pair closed by its gap, and every square moved toward the nearer
near wall by its least clearance. Both routes accepted all three at contact with margin 0
and refused all three past it with margin −1e-30, at 268
([sharp-controls-n268.json](receipts/sharp-controls-n268.json)) and 304
([sharp-controls-n304.json](receipts/sharp-controls-n304.json)). The same program ran on
T-241’s certificate (its [packet](../couzo-n304-2026-10-23/README.md)).

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method. The source’s checkers were not run.

## 303

`s303_cdeotte.cert` certifies Chris Deotte’s public Kaggle packing at
17.907238274538241…, 2.52e-3 below T-239, the house, but 2.60e-4 above #763’s 303
(T-240), which reached this repository first. A later, weaker report is not recorded,
and nothing here is a key reason to record it. It bears on #763’s credit at 303: the
stage 4 review of T-240 found #763’s Kaggle parent one to one with it, two squares
beyond 0.1. That question goes to the authors.

## What Is Not Established

A finite packing certifies an upper bound and nothing more.
No KKT, local-minimum, rigidity or optimality statement is replayed: the source’s
`S_exact`, free squares and second-order report are its own. No arrangement identity
beyond the measurements above is decided. Whether Lavrentev’s packing at 268 was public
before #763, and who found the packing at 304, are the authors’ to say.

## Credit and Licence

- **268:** Vladislav Lavrentev’s public Kaggle packing (lightningv08), as the source
  credits it, descended exactly by Evan Daniel.
  #763 (T-240) credits its own 268 to Couzo after Kirill Tymchishin’s notebook packing,
  another placement of the same arrangement. The source’s `TODO.md` says the packing
  first appears in Lavrentev’s output and is Tymchishin’s input.
- **304:** the packing T-241 certifies. The source says its finder is unknown and its
  earliest public copy is kozykappa’s notebook. Couzo’s index credits it to Kirill
  Tymchishin’s Kaggle notebook “CPU Alternating Reclosure” v3. His manifest’s
  `previous_source` there names Mykhailo Polkovskyi’s packing, T-186’s, as the record his
  catalogue held at 304 before, not as the notebook’s seed, so no source states a link
  before Tymchishin (M-1 of the [stage 4 review](#stage-4-review);
  [T-241’s packet](../couzo-n304-2026-10-23/README.md)). A regularization leaves the
  packing with its finder through the result that holds it, so the line names T-241’s
  credit, Tymchishin. Evan Daniel descended it exactly.
- **Licence and assistance:** MIT, copyright (c) 2026 Evan Daniel ([LICENSE](source/LICENSE)).
  [CREDITS.md](source/CREDITS.md) says the repository’s work was “Produced by Claude
  (Anthropic) in a single session under human direction”, and the commit carries a
  Co-Authored-By trailer naming Claude.

The bibliography key is **[Daniel Kaggle descents 2026-10-24]**, credited *Daniel after
Lavrentev, Tymchishin*: Lavrentev at 268 and Tymchishin at 304, through T-241. Its lineage
is `independent`, and it names no Levy link (M-4). The manifest that names this project’s
`sqpack/verify.py` as a first checker is Couzo’s, which certified Couzo’s file, and
Daniel’s descent started from the public binary64 packing instead. For these descents
Daniel’s source names nothing of this project’s but the comparison its
`s268_lightning_prior.json` and `s304_pub_prior.json` draw from the register and pending
issues (#375, #476, #501, #575, #593, #624), which is context and not the basis, and its
`CREDITS.md` lists the Squares Project as parallel work.

## Stage 4 Review

The [review of 24 October 2026](../../../../docs/project/reviews/review-2026-10-24-couzo-evand-n268-n304.md)
of T-241 and T-242 accepted both of these certificates and T-241’s for finite feasibility,
with one major finding (M-1), four minor and four notes, none blocking. Its programs and
outputs are kept here in [review/review-2026-10-24/](review/review-2026-10-24/README.md),
equal to the digests its `outputs/program-digests.sha256` records.

- **Its own checker.** `t241_t242_exact.py` decides each certificate in `Fraction` by
  separating axes over every pair and by the exact clipped area of every pair whose
  centres lie within 2, with twelve controls each, sharp at $10^{-30}$, and nine
  hand-built packings, all as expected. Its least pair gaps and least wall clearances
  equal [sharp-controls-n268.json](receipts/sharp-controls-n268.json) and
  [sharp-controls-n304.json](receipts/sharp-controls-n304.json) fraction for fraction.
  Its author read neither maintained route nor any checker of Daniel’s or Couzo’s, so it
  is a clean-room re-implementation (`E-evand-kaggle-descents-review-exact-feasibility`,
  `V-kaggle-268-304-review-check`).
- **The maintained replay** reads the certificates through the `evand-cert` reader, whose
  line filter and corner construction are transcribed from Daniel’s `verify_cert.py` and
  `verify_cert2.py`, the checkers the certificates name, as the #763 review’s RF-4 found,
  so it is `shared-components` (`E-evand-kaggle-descents-exact-feasibility`), and T-242’s
  independent re-implementation rests on the review’s checker.
- **M-1, M-2, M-4 and N-1** are fixed above and in the register: the credit at 304, the
  print the rationale names, the key’s lineage and Levy link, and the descent’s input at
  268. S2 is confirmed at both counts. The questions D1 and D2 are below. Of Couzo’s, the
  reply of 25 October on #763 asks C1 as its question 7 and covers C3 and C4 in its
  questions 1 and 6; C2 is to be asked in the next #763 reply.

## Questions for the Author

Drafted in think-l49q for Evan Daniel, and in think-hx0e’s notes after the stage 4 review
(its D1 and D2). None is posted: Daniel opened no issue, so the questions are held in
think-hx0e until the coordinator decides where they go.

1. Do you claim the 268 and 304 certificates at `8a8879a` as bounds, credited “Daniel
   after Lavrentev” at 268 and as your descent of the packing Couzo credits to Tymchishin
   at 304?
2. Is “finder unknown” at 304 the missing finder field your `TODO.md` notes for Kaggle
   imports? Do you know who first published that packing, and which notebook versions and
   dates hold Lavrentev’s 268 (lightningv08), Deotte’s 303 and kozykappa’s 304?
3. `s268_lightning.predescent.txt` is #763’s Kaggle parent at 268, Tymchishin’s EDA+Seam
   LP v4 packing, to 2.47e-10 (measured here), while `s268_lightning.input.txt` is
   Lavrentev’s placement. What is the predescent file, and did any step of the descent use
   it? The stage 4 review answers half of this (N-1): `s268_lightning.json` gives
   `S_input` 16.87436171586941, the side of `.input.txt`, and the certificate is that file
   moved by at most 1.41e-4 and 2.49e-2 from the predescent file. So the descent started
   from Lavrentev’s placement, as the credit “Daniel after Lavrentev” has it.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-kaggle-descents-2026-10-24 --checkout CHECKOUT
python -m devtools.acquire_source evand-kaggle-descents-2026-10-24 --check
python -m devtools.upper_bound_reports evand-kaggle-descents-2026-10-24 check-claims --write
python -m devtools.upper_bound_reports evand-kaggle-descents-2026-10-24 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-kaggle-descents-2026-10-24 check --replay
python resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp_controls.py --packet evand-kaggle-descents-2026-10-24 --n 268 --out resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp-controls-n268.json
python resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp_controls.py --packet evand-kaggle-descents-2026-10-24 --n 304 --out resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp-controls-n304.json
python resources/web/evand-kaggle-descents-2026-10-24/measure/identity.py --out resources/web/evand-kaggle-descents-2026-10-24/measure/identity.json
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s268_lightning_vs_prior.json.gz` | upstream | `25cbc273d960517034c762f4116aee8a478dcdd7` | `6299e402a29f9a74e07a19b5b804fdcf43da6554492f63462a7704e5102dfe42` |
| `source/search/packer/candidates/s304_pub_vs_prior.json.gz` | upstream | `7621dc27d6c8ee093f027e7eb48feb6f686bc0c0` | `91c2b66a175a06eff6cd56bf2d5e3d0c449070d8a10e1b0e80507f9bb9baaaaf` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
