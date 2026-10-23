# Francisco Couzo’s Verified-Bounds Index at 487b058

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d/certificates)
at `487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d` (tree
`f8f9ee10413e40c8c5d4f8cb1b411b7d9e11a802`, committed 2026-10-14T17:45:39Z, “Land
verified bounds through n=1024”) publishes, with no issue, a tighter exact certificate at
211 and 296 certificates beyond the case corpus.
It follows `b85dee2`, the pin of [#586](https://github.com/jlevy/squares/issues/586),
and precedes `43ac7d2`, the pin of [#607](https://github.com/jlevy/squares/issues/607).
Against `b85dee2` it adds 290 certificates (370 and 403 to 991), changes seven (211,
339, 378, 379, 380, 381 and 382), deletes 22 and rewrites the author’s index
`upper_bounds.json`, which #607 compares against.

| n | Exact side of the certificate | Rounded up at 16 places | Printed by | Requested |
| --- | --- | --- | --- | --- |
| 211 | `7496774813149710519467765230441/500000000000000000000000000000` | 14.9935496262994211 | the certificates README: 14.993549626300 | no issue |

`certificates/n211.json` calls the 211 certificate an exact optimum, found by the
author’s `hop` search (job 97342) from his own 211 and seeded from Daniil Ostashev’s
certificate, which it links to issue 501 but whose side it states, 14.99369418658324…,
is that of Ostashev’s #575 certificate (T-175): the author’s further refinement of the
arrangement #583 and #586 certified (T-181, T-182).

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone with a sparse checkout
at the pin, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
599 files, 34,106,389 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
`certificates/n211.cert` (35,784 bytes) is retained as factual data under the owner
decision of 2026-10-09 ([Retained Factual Data](../known-best-packings/README.md)).
The 296 certificates beyond the corpus total 33,074,931 bytes, bulk data under
[`OR-18`](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob):
each is pinned by its SHA-256 and compared from its exact header side in
[review/](review/), not retained.
Their metadata, the two READMEs, the index and n211’s decimal packing and drawing are
pinned by digest only. No prose or program is copied.

## The Certificate at 211

[acquisition/claims.json](acquisition/claims.json) compares it with the case record and
every other report at 211, as `main` stood at `22a67ce4a`, after #614 adopted T-182 as
the house at 211, each at its exact side.
The record first read `c4c690a3e`, with T-149 as the house, and every relation is the
same at both.

| Report | Holder | Side | This certificate is below by |
| --- | --- | --- | --- |
| Case T-182 (#586); #593, not registered at 211 | Ostashev, improved by Couzo; Polkovskyi | 14.9935589139740060 | 9.29e-6 |
| #501 (T-149), PR #574 (T-174) | Ostashev; PingYou Ltd | 14.9963367213363163 | 2.79e-3 |
| T-057 | de Winter | 14.9979607049677150015 (printed) | 4.41e-3 |
| T-098 (#375) | Daniel | 14.9979607049673618 | 4.41e-3 |
| T-163 (Fang’s theorem inventory) | Fang | 14.99995 | 6.40e-3 |
| #575 (T-175) | Ostashev | 14.9936941865832463 | 1.45e-4 |
| #583 (T-181) | Couzo | 14.9935589141226373 | 9.29e-6 |

[review/compare_lineage-output.txt](review/compare_lineage-output.txt) measures the 211
against #586’s, #583’s, #575’s and #501’s packings with
`mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py`: it lies nearest
#586’s (T-182), with 139 of 211 squares within $10^{-3}$ under a reflection of the box
and none further than 0.354, and T-188 lists it as a regularization of T-182.

The certificate is the smallest at 211. A publication in a watched repository is a
report from its first commit, here 2026-10-14T17:45:39Z, after every report above, so
under the per-count rule
([stage 1](../../../campaign/result-import.md#several-reports-at-one-count)) it is
recorded, as T-188. No later report at 211 is smaller: the 4e4c8ce index restates the same
bytes.

The maintained two-route kernel decided it by `devtools.upper_bound_reports certify
--workers 1`, from 03:24:21Z to 03:25:34Z on 15 October on a four-core machine shared
with other lanes: the positive passes `sqpack`’s exact witness verifier and the
independent rational corner checker, and both refuse the duplicate-square and
outside-container controls. Both find the same least wall clearance, exactly
`1/200000000000000000000` ($5 \times 10^{-21}$), and the same least pair gap, just under
$10^{-20}$. The three jobs made 132,930 pair decisions in 50.2 route CPU seconds and 69.0
job wall seconds, summed. A fresh `check --replay` decided all three again, equal to the
retained rows apart from timing, in 70 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes are two implementations of one method; the third exact route,
`devtools.check_half_angle_area`, is a separate review lane. No source program ran here.

## Beyond the Corpus

[review/compare_beyond_horizon.py](review/compare_beyond_horizon.py) reads each of the
296 certificates from a checkout at the pin, holds it to the manifest’s digest and to the
side `certificates/README.md` prints (rounded up at 12 places), and compares its exact
header side with every member that stood at the count when `487b058` was committed:
every beyond-horizon row of `frontier/source-coverage.yaml` (exactly where its packet
states the side), every exact side beyond 324 in a packet claim record, Kevin Fang’s
theorem inventory and composite table, the 14 October ledger’s steps, Evan Daniel’s
tiling at 964, and the grid. It writes
[review/beyond-horizon-comparison.json](review/beyond-horizon-comparison.json) and, for
the recorded counts, the claims record a beyond-horizon row reads,
[review/beyond-horizon-claims.json](review/beyond-horizon-claims.json).

- **252 are recorded**: each is below every number every earlier member may be, and
  below Göbel’s classical construction at its count. At 222 of them the earlier best is
  the grid; at 30 it is a report (Couzo’s #586 certificates at 339 and 378 to 382, Evan
  Daniel’s #596 at 370, and Fang’s direct certificates and composites from 420 to 871),
  by 9.3e-6 to 2.4e-2.
- **42 are `undecided-goebel`**: below every earlier member, but each a rational witness
  2.8e-11 to 5.7e-10 above Frits Göbel’s classical square or strip construction at its
  count (408 to 974; [review/goebel-beyond-horizon.md](review/goebel-beyond-horizon.md)),
  which the record holds at no count beyond 324. The author’s `58a7833` corrects these
  entries to the closed forms. Whether Göbel’s constructions count as earlier reports, and
  so as the baseline beyond 324, is the owner’s question; until then these rows are
  neither recorded nor in the claims record.
- **2 are not recorded**: 812 and 930 are above Fang’s composite rows of `bef5c42`
  (2026-10-12), by 4.2e-3 and 1.3e-3.
- **All 296 are later superseded**: #607’s certificates (`43ac7d2`) are smaller at 16 of
  the counts and the `4e4c8ce` index at all 296. So each recorded row is recorded at
  `487b058` and then superseded, as the 14 October ledger recorded `4596670` at 375 before
  #584 and `93570ef` at 176 before PR #574.

[review/goebel-beyond-horizon.md](review/goebel-beyond-horizon.md) states how Göbel’s side
is computed, exactly, from the archived Kingbird family pages, and compares four sets of
rows with it: these, #607’s, the 4e4c8ce index’s and the record’s current beyond-horizon
rows on `main`.

[register-plan.yaml](register-plan.yaml) is the register plan: the entry, evidence,
source and bibliography `register-plan` prints for 211, then a drafted beyond-horizon part
with the 252 rows, the 18 current rows they supersede, the 42 `undecided-goebel` rows,
the owner’s question and the source’s `claims_record`.
The records lane of 15 October applied it: T-188 records the 211 side, and the source
register holds the 252 rows, the 18 it supersedes and, at 14 of the counts, #607’s rows
that supersede these (T-189). The 42 `undecided-goebel` rows are not recorded until the
owner answers #613, and the two not recorded stay so.

A replay of the 296 makes 456,922,338 pair decisions: 38 to 48 CPU-hours at the rate the
211 and 237 replays measured. It needs the bytes, which are held only in the author’s
repository at the pin until a hosted release keeps them, and is held (think-2d7f).
The `4e4c8ce` index’s exact sides, in
[review/goebel-beyond-horizon.json](review/goebel-beyond-horizon.json), are smaller than
all 238 of the 252 recorded rows that are still current, by $3.79 \times 10^{-12}$ (381)
to $2.38 \times 10^{-2}$ (749); T-188’s notes and the source register say so until that
index is recorded (think-yfoo).
It now is: the [history walk of Couzo’s watched publications](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md)
records the index’s certificates (couzo-index-2026-10-15), and 199 of the 252 rows name it
as the report that beat them first, 64 of them current before that walk.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificate is kept as
factual data and nothing of the source is relicensed.
The 211 certificate continues Daniil Ostashev’s arrangement of #575 (T-175), whose
construction credit the author’s metadata keeps, after the author’s own #583 and #586
certificates (T-181, T-182).
Evan Daniel’s optimizer, contact solver and verifier and this repository’s exact verifier
were used. The pinned files state nothing about AI assistance; the author’s issues of 13
and 14 October state that OpenAI Codex assisted search and verification orchestration,
that earlier search work used Claude Code, and that the author directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-verified-bounds-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-verified-bounds-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-verified-bounds-2026-10-14 check --replay
```

The beyond-horizon comparison reruns from a checkout at the pin, with the commands in
the script’s docstring. The lineage measurement reruns from the retained packets:

```sh
uv run --frozen --all-extras --group dev python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py couzo-verified-bounds-2026-10-14 211 couzo-certificates-2026-10-13 couzo-issue583-2026-10-13 dostashev-merged-bands-2026-10-13 dostashev-records-2026-10-11
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
