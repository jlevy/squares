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

`certificates/n211.json` calls the 211 certificate an exact optimum, seeded from Daniil
Ostashev’s issue-501 certificate and found by the author’s `hop` search (job 97342): the
author’s further refinement of the arrangement #583 and #586 certified.

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
every other report at 211, as `main` stood at `6964362b5`, each at its exact side.

| Report | Holder | Side | This certificate is below by |
| --- | --- | --- | --- |
| Case T-149, PR #574 (T-174) | Ostashev; PingYou Ltd | 14.9963367213363163 | 2.79e-3 |
| T-098 (#375) | Daniel | 14.9979607049673618 | 4.41e-3 |
| T-163 (Fang’s theorem inventory) | Fang | 14.99995 | 6.40e-3 |
| #575 (T-175) | Ostashev | 14.9936941865832463 | 1.45e-4 |
| #583 (T-181) | Couzo | 14.9935589141226373 | 9.29e-6 |
| #586 (T-182), #593 (T-183) | Couzo; Polkovskyi | 14.9935589139740060 | 9.29e-6 |

The certificate is the smallest at 211. A publication in a watched repository is a
report from its first commit, here 2026-10-14T17:45:39Z, after every report above, so
under the per-count rule
([stage 1](../../../campaign/result-import.md#several-reports-at-one-count)) it would be
recorded. No later report at 211 is smaller: the 4e4c8ce index restates the same bytes.

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

- **294 are recorded**: each is below every number every earlier member may be. At 263
  of them the earlier best is the grid; at 31 it is a report (Couzo’s #586 certificates
  at 339 and 378 to 382, Evan Daniel’s #596 at 370, Fang’s direct certificates and
  composites from 420 to 871, and Daniel’s tiling at 964), by 9.3e-6 to 3.0e-1.
- **2 are not recorded**: 812 and 930 are above Fang’s composite rows of `bef5c42`
  (2026-10-12), by 4.2e-3 and 1.3e-3.
- **All 296 are later superseded**: #607’s certificates (`43ac7d2`) are smaller at 16 of
  the counts and the `4e4c8ce` index at all 296. So each recorded row is recorded at
  `487b058` and then superseded, as the 14 October ledger recorded `4596670` at 375 before
  #584 and `93570ef` at 176 before PR #574.
- **A question for the owner.** At 42 recorded counts, from 408 to 974, the certificate is
  a rational witness 2.8e-11 to 5.7e-10 above Frits Göbel’s classical square or strip
  construction (with deletion), which the record holds at no count beyond 324; the
  author’s `58a7833` corrects these entries to Göbel’s closed forms. By the rule they are
  recorded against the beyond-horizon row or the grid; the owner may prefer to record them
  as Göbel’s.

[register-plan.yaml](register-plan.yaml) is the register plan: the entry, evidence,
source and bibliography `register-plan` prints for 211, then a drafted beyond-horizon part
with the 294 rows, the 18 current rows they supersede, and the source’s `claims_record`.
No record is edited here.

A replay of the 296 makes 456,922,338 pair decisions: 38 to 48 CPU-hours at the rate the
211 and 237 replays measured. It needs the bytes, from a checkout at the pin or a hosted
release, and is held (think-2d7f).

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificate is kept as
factual data and nothing of the source is relicensed.
The 211 certificate continues Daniil Ostashev’s arrangement, whose construction credit
the author’s metadata keeps, after the author’s own #583 and #586 certificates.
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
the script’s docstring.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
