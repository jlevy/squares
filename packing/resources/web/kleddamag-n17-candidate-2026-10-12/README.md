# Overbeck: A Candidate Proof That s(17) = L, 12 October 2026

[Issue #557](https://github.com/jlevy/squares/issues/557) tracks Marc Leonard Overbeck’s
verification edition of a candidate proof that John Bidwell’s 1998 packing of seventeen
unit squares is optimal: $s(17) = L = 4.67553009360455095163\ldots$. The issue’s title
says n = 18; the source is n = 17. The edition is
[Kleddamag/the-seventeenth-square-candidate](https://github.com/Kleddamag/the-seventeenth-square-candidate/tree/653b9589d0f8a152f01adc56b1d48ba53d49abc3)
at `653b9589d0f8a152f01adc56b1d48ba53d49abc3` (tree
`502e27fba825790bf99bf42ae297b38adfe1646b`, committed 2026-10-12T14:40:59Z, the
repository’s only commit), with the 12 assets of its release
[`large-files-v1`](https://github.com/Kleddamag/the-seventeenth-square-candidate/releases/tag/large-files-v1)
(4,785,719,080 bytes).
Both were retrieved at 2026-10-12T16:47Z.

This packet is the stage 2 retention of the import.
Nothing in it is a register entry, and nothing in it confirms the claim: the source’s
status is a candidate proof, `check.py` recomputes no certificate, and the sampled
checks in [receipts-here/](#sampled-checks-run-here) recompute a sample, not the whole.
The read of the argument is a separate review, recorded with the register entry, T-153.

## Source and Credit

| Field | Value |
| --- | --- |
| Author | Marc Leonard Overbeck (GitHub Kleddamag, ORCID 0009-0008-8607-8197), as `README.md` and `CITATION.cff` name him |
| Version | Version 1 (candidate), 2026-10-12 (`CHANGELOG.md`) |
| Status, as the source states it | “Candidate proof, not an established theorem”: the claim holds if the 210 obligations of `OBLIGATIONS.json` hold, 15 of them mathematical premises (`STATEMENT_STATUS.md`) |
| Outside review | Guzhou0806 (N17 project) read the 15 premises in an earlier state and ran a checker of his own on two of the 13 trees (JQ and JPG15p_v5); his report is not in the edition |
| Human credit | `CREDITS.md`: Bidwell for the packing; Gensane and Ryckelynck; David Ellsworth for the degree-18 polynomial; this project (Joshua Levy) for the charge method, the exact certification of L, the local recipe and the plan to follow the n = 11 proof shape; Manasseh Ahmed’s 11SquaresOptimal for that proof shape; Mira-acc for the 4.613 frame; Guzhou0806 for the angle catalogue, parent-side reduction and first exact JavaScript checker; Muhammad Maaz for the semidefinite leaves |
| AI assistance | `README.md` and `CREDITS.md`: the mathematics, engines, certificates, checkers, reviews and text were produced by AI systems under his direction, Codex (OpenAI) and Claude (Anthropic), which are named and are not authors; within the project no human has read the mathematics |
| Announcement | Overbeck as [@kleddamag](https://x.com/kleddamag/status/2109658579678761429) (display name “Marc Leonard Overbeck”, account 1496776810767519746), 2026-10-12T14:52:55Z: “A proof candidate for 17 squares: the 1998 packing cannot be beaten. s(17) = 4.67553009…”, “Built with @OpenAI Codex and @AnthropicAI Claude. Thanks to @ojoshe, @_Mira___Mira_, @guzhou0806 and @ManassehA06, whose work this builds on.”, linking the edition. The owner supplied the address on 13 October; retained as [`receipts/announcement/tweet-2109658579678761429.json`](receipts/announcement/tweet-2109658579678761429.json), the post as X’s syndication endpoint returned it at 2026-10-13T19:11Z |
| Licence | `README.md`, Licence: “No licence for reuse is granted yet. You may download the files and run the checks to verify the result.” |
| Bibliography key | **[Overbeck n17 candidate 2026]** |

`THIRD_PARTY.md` lists copies of this repository’s files inside the edition: the exp-237
root certificate (rewritten in another layout), the exp-238 endpoint certificate, the
H-256 sheet and `devtools/check_n17_endpoint_feasibility.py`, at commit
`ef79288a498b5469e6b944f7b150d83aeeab5f94`.

## Source Custody

No licence permits reuse, so the packet keeps no upstream byte, as the
[Deleeuw packet](../ebdeleeuw-n70-refinement-2026-10-10/README.md) and the SQUISH
packets do. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote [acquisition/sources.json](acquisition/sources.json) and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) from the
declaration in [acquisition/declaration.json](acquisition/declaration.json) and a clone
checked out at the pin.
The manifest pins 49 files, each bound to its Git blob at the pin: the 28 top-level
files, `OBLIGATIONS.json`, `CLASS_ROW_LEMMA.md`, the public runbook and its runner, the
capture checkers’ sources and manifests, and the tree checkers, their specification and
acceptance script. The declared `source/` directory is empty by design.

Three digests pin the edition as a whole, and each equals the value the source
publishes:

| What | SHA-256 | Published where |
| --- | --- | --- |
| `MANIFEST.sha256`, the SHA-256 of every other tracked file (7,118) | `9ecfa0db00fc9afaf98c6df8eeee920df8cb1e4737c88521ac3c64366ec7689e` | release notes of `large-files-v1` |
| `check.py` | `c17240b5189821c9244b1e5568e7d6b73c3c4de0fae741ec4206f9852d86a7cb` | release notes, and its line in `MANIFEST.sha256` |
| `LARGE_FILES.tsv`, the 12 release assets | `9a01cac28d3377a2ce900b92a99688890d6831d62e767c08d07da0daa12f28cb` | `check.py`’s fixed hashes |

The 12 release assets are not in the Git tree.
[acquisition/large-files.json](acquisition/large-files.json) gives each one’s path, size
and SHA-256. Each was fetched with the author’s `fetch_large.py` through
`gh release download`, then hashed again here, and each equals its `LARGE_FILES.tsv` row
and the digest GitHub reports for the asset.
Eleven are tree certificates (`JG`, `JPA_v5`, `JPG15m_v5`, `JPG17m_v5`, `JPG17p_v5`,
`JPG3m_v5`, `JPG3p_v5`, `JPW13`, `JPWS_v4`, `G20S`, `HW`; the other two trees, `JQ` and
`JPG15p_v5`, are in the tree), and one is the larger-leaf `RESULT.json`.

`upper-packing-certificate.json`, the rational seed of side $4675530093604551/10^{15}$,
is byte-identical to the file
[the 21 September packet](../n17-kleddamag-certified-bound-2026-09-21/README.md)
retains, and `acquire_source` compares the two.

## The Statement, as Derived Facts

[facts/statement.json](facts/statement.json) keeps what the record needs of
`STATEMENT.md`, `OBLIGATIONS.json`, the capture plan and the tree records, each with the
SHA-256 of the file it was read from.
The polynomials are parsed by the packet’s own parser, with no evaluation of upstream
text.

- $t_0$ and $b_0$, 60-place decimals; the isolating rectangle of half-width $10^{-12}$
  about them.
- $F(t,b) = t-3t^2-t^3-t^4+(1-t-t^4+t^5)b+(-3t+t^2-t^3-t^4)b^2$ and
  $G(t,b) = -2t^3-2t^4+(-1+3t-4t^2+t^4+t^5)b+(4-2t-2t^2+2t^3-2t^4)b^2+(-1-5t+4t^2+t^4+t^5)b^3+(2t+2t^2)b^4$,
  as coefficient lists.
- $L = (6+4t_*)/(1+2t_*-t_*^2)$, with $4.67553009360455095163 < L <
  4.67553009360455095164$.
- The claim: a packing of seventeen unit squares exists at side $L$, and a packing at
  side $S$ implies $L \le S$. Uniqueness is not claimed.
- 210 obligations: 15 mathematical premises, 50 base capture or physical-transfer rows,
  1 slab statement, 49 strict budgets, 84 branch implications and 11 local roots.
  The premises are `ALGEBRAIC_ENDPOINT`, `UPPER`, `ENDPOINT`, `CHARGE_SEMANTICS`,
  `FRAME_ASSIGNMENT`, `C7_C8_TRANSFER`, `WALL_PARTITION`, `ROOT_ADMISSION`,
  `SELECTOR_LOGIC`, `LOCAL_CHECKER_SOUNDNESS`, `LOCAL_CERTIFICATE_IMPORT`,
  `G20S_PHYSICAL`, `WALL_CONTRADICTION`, `KEY_W_ELIMINATION` and
  `COARSE_LOOSE_CAPACITY`.
- Five steps: the upper bound (68 wall and 136 pair conditions, exact); capture at side
  at most $C = 4675531/10^6$ by 98 weighted counting certificates (94 of 18,000 rows and
  4 of 9,000, 1,728,000 rows and 1,152 slices per checker), leaving 11 cases; admission
  of each case into one of 11 root regions; 13 tree certificates, by which ten regions
  hold no packing below $L$ and the eleventh only packings in a tube around the known
  one; and rigidity in the tube, 17 exact rounds and a contraction of ratio
  $159201934153319/200000000000000 < 1$.

## Against the Record

[receipts/statement-comparison.json](receipts/statement-comparison.json) decides, in
exact rational arithmetic under Python 3.14.7 with this repository’s own n17 tools, that
the statement’s $L$ is the side the record already certifies:

- $F$ and $G$ equal, coefficient for coefficient, the two chart polynomials of H-255 as
  `devtools.check_n17_root_certificate` derives them and as the exp-237 certificate
  freezes them.
- $t_0$, $b_0$ and the radius $10^{-12}$ equal the exp-237 box exactly, so the
  statement’s rectangle is the certified box, and exp-237’s contraction (norm below
  $6.6 \times
  10^{-11}$) proves its unique root there: $(t_*, b_*)$ is the H-255 root.
- The side map is the one exp-245 uses.
  The tight inclusion of $t_*$ gives
  $L \in [4.67553009360455095163409910549\ldots, 4.67553009360455095163412343546\ldots]$,
  width $2.4 \times 10^{-23}$, inside the statement’s 20-place enclosure, and it holds
  exp-245’s enclosure of the catalogue polynomial’s root,
  $4.675530093604550951634111270483146648767\ldots$ to width $10^{-40}$.
- $L$ is strictly below n-017’s verified upper bound, the ceiling
  $23377650468022754758171074269267527/5\times10^{33}$ that `E-n017-certified-endpoint`
  holds, by $1.0358 \times 10^{-22}$, and the catalogue’s printed 4.67553009360455 is
  $9.5 \times 10^{-16}$ below $L$.
- $L$ exceeds the case’s reported and verified lower bound, Guzhou0806’s R071
  $18641771/4000000$, by $0.0150873436\ldots$.

## The Author’s Check, Run Here

`check.py` was read in full, with the runner it uses and the scripts outside the runner
(`check_equivalence.py`, `check_comparison_records.py`, `own_endpoint_enclosure.py`);
the 31 runbook scripts and their local imports were scanned for process, network and
file-mutation calls and found none outside the runner’s guard.
It ran once on 12 October 2026 from a scratch directory outside this repository, under
CPython 3.12.3 in an isolated venv with SymPy 1.14.0, Node.js v22.22.0, on a shared
4-core Linux x86_64 container: a platform the source never tested.

```text
CHECK RESULT: PASS (levels 0-2; 7118 files, 22013 pins, 41 checks); sha256 of MANIFEST.sha256: 9ecfa0db00fc9afaf98c6df8eeee920df8cb1e4737c88521ac3c64366ec7689e
```

Exit code 0, 809.7 s of wall and 793 CPU-seconds with its children; 58 lines PASS and
none other but INFO; all 31 public checks PASS, `endpoint_upper` in 296.5 s and
`provenance` in 268.7 s. The MANIFEST digest it prints equals the release notes’.
[receipts/check-py/](receipts/check-py/) keeps its output, the equivalence and
comparison-records outputs, and [run.json](receipts/check-py/run.json), which summarizes
the 31 runner receipts with the SHA-256 of each.

What the PASS establishes is what `CHECK.md` says: the files, large files and pins have
their digests; the 31 cheap public checks give their recorded outcomes on the files they
recorded reading (the exact upper bound, the tight enclosure of $L$, the case logic, the
finite rigidity rounds and the contraction); `provenance` re-decides every stored row of
the 98 capture statements from the numbers recorded in it, in both checkers, which
agree; and the stored outputs of the second and third executions of the 13 trees say
PASS and ACCEPTED and name these certificates.
It recomputes no capture row and no tree, reads no mathematics, and cannot show that a
stored execution ran what its record says.

## The Recomputations Not Run

[receipts/recomputation-price.json](receipts/recomputation-price.json) prices, from the
author’s own records, the two full recomputations `check.py` leaves out:

| Recomputation | Author’s record | CPU-hours |
| --- | --- | --- |
| 98 capture statements, both checkers, 1,728,000 rows each | `cpu_seconds_rows` of the 1,152 selected slices, Linux x86_64 runners, four workers per checker | 1,273 Python + 1,074 Node = **2,347** (600.8 slice-hours of wall) |
| 13 tree certificates, both tree checkers and the post-check | the `time` line of each stored second-execution output, the author’s macOS arm64 build machine | 6.05 Python + 1.38 Node = **7.4** |

`JPA_v5` is the largest tree: 2.32 and 0.49 CPU-hours, and its Node run peaked at 7.0 GB
resident. The Python capture checker took 2.5 CPU-seconds per row at the median slice.
A slice of 1,500 rows is about 1.1 Python and 0.9 Node CPU-hours.

## Sampled Checks Run Here

Lane K3 of the import ran four sets of checks on 12 October 2026 and kept JSON receipts
only, with commands, input digests, verdict lines, derived numbers and times, in
[receipts-here/](receipts-here/).
Every one agrees with the source.

| Receipt | What ran | Outcome |
| --- | --- | --- |
| [upper-bound.json](receipts-here/upper-bound.json) | The record’s two exact routes on the source’s rational seed; the record’s H-255 and H-256 checkers on it; K3’s own root isolation, a Krawczyk test and a Sturm count; the author’s `own_endpoint_enclosure.py` and its control | The seed packs at $4675530093604551/10^{15}$, $4.84 \times 10^{-17}$ above $L$; exactly one root in the stated box; $L$ inside the 20-place interval, a root of the degree-18 polynomial, $1.04 \times 10^{-22}$ below the record’s ceiling |
| [capture-sample.json](receipts-here/capture-sample.json) | The author’s `recompute_slice.py`, both capture checkers, on 34 rows of 21 statements covering every root | All 28 calls `EQUAL` to the stored rows |
| [capture-independent.json](receipts-here/capture-independent.json) | K3’s own exact row checker, written from `CLASS_ROW_LEMMA.md`, `PROOF.md` section 3 and `RESTRICTED_CHECKER.md`, on 34 rows of 6 statements | Every per-level minimum equal to both stored rows; a raised-$\Gamma$ control fails |
| [trees.json](receipts-here/trees.json) | Both v3.0 tree checkers and `h_report30.py` on JQ, JPG17m_v5 and JPG15p_v5 | `PASS`, `RESULT: ACCEPTED`, reports equal to the stored ones; the ten other trees not run |

K3’s own programs, `k3_capture_row.py` with `compare_independent.py`, and
`k3_root_isolation.py`, are retained in [receipts-here/programs/](receipts-here/programs/)
with the SHA-256 the receipts give.

## Programs

[receipts/programs/](receipts/programs/) holds the scratch programs that made these
receipts, each reading the edition as data and run with `-I` from outside it:
`verify_large.py` and `write_large_record.py` (the release assets), `run_check.sh` and
`summarize_check_run.py` (the `check.py` run), `compare_statement.py` and
`derive_facts.py` (the comparison and the facts, Python 3.14 with this repository’s
`devtools`), and `price_recomputation.py` (the prices).

[review-2/programs/](review-2/programs/) holds the eighteen programs the
[second adversarial review](../../../../docs/project/reviews/review-2026-10-13-overbeck-n17-candidate-second.md)
wrote and ran on 13 October 2026, kept as run, each reading the edition’s files as data
from a checkout of the pin. Among them are `geom.py` (the exact-root layout and its
Krawczyk boxes), `cmp_file.py` (that layout against the edition’s rational packing
file), `identities.py` (the 52 base-gap identities in the ideal of `F` and `G`),
`audit.py` (the 152 separating options), `rows.py` with `check_rows.py` (the
independent row builder against the five stored stopped models), `replay.py` (the
duality bounds and the contraction ratio), `stops.py`, `budgets.py`, `admission.py` and
`profiles.py`. [review-2/run.sh](review-2/run.sh) runs them all in the order of the
review’s checks table and prints each command before its output. `cmp_file.py` takes
only the certificate path and imports its sibling `geom.py` from its own directory;
[review-2/RESULTS.txt](review-2/RESULTS.txt) is its complete output on a checkout of the
pin before that argument restriction, under Python 3.14.7, SymPy 1.14.0 and mpmath
1.3.0, with the checkout’s path
written `CLONE` and the review’s `G/` folder written `G`. The review’s “Checks Run
Here” section summarizes it. Four of them are registered since 14 October 2026, each in
[`verifiers.yaml`](../../../frontier/verifiers.yaml) with its structured independence
record: `geom.py` (`V-overbeck-review2-krawczyk-root`), `audit.py` with `identities.py`
(`V-overbeck-review2-groebner-identities`), `rows.py` with `check_rows.py`
(`V-overbeck-review2-row-builder`) and `replay.py` (`V-overbeck-review2-duality-bounds`),
and `E-n017-overbeck-gate-review2` records what they decide: the normalized 52-row gate
of `G20S_PHYSICAL`, re-derived with P096’s stop cuts taken as premises. n-017’s case record cites it and T-153 does not, since
it is not the complete replay T-153’s rungs wait on. The other twelve decide nothing on
the register’s behalf: no evidence entry cites them.

`stops_eps.py`’s output at core radius $501/100000$ is not what the review’s check 8
says of it. It compares $b$ and $b + z$ with the root-scale cuts $-17/50000$ and
$3/125$, not with P096’s $-213/25000$ and $49/2000$, which is why it prints two `False`
lines; and its `z <=` line adds $17/50000$ to the bound on $b + z$, which holds only
where $b \ge -17/50000$, so the $0.024774$ it prints is not a bound at that radius.
`stops_cuts.py`, added on 13 October after
[review A of #577](https://github.com/jlevy/squares/pull/577#pullrequestreview-5499709484),
bounds $z$ by the bound on $b + z$ minus the bound on $b$ at the same radius and
compares each radius with its own cuts: all six hold, at $501/100000$ with margins of
$7.6 \times 10^{-6}$ and more. The review’s
[status addendum](../../../../docs/project/reviews/review-2026-10-13-overbeck-n17-candidate-second.md#status-addendum-2026-10-13)
records the correction.

[review-3/](review-3/README.md) holds the programs of the
[third review](../../../../docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md),
the mathematical-correctness lane of 13 and 14 October 2026, with the two logs it kept:
its own root isolation, the upper construction at side $L$ with every contact proved by
ideal membership, 192 literal checks plus one case-partition check, the admission of the eleven
roots, the hand-overs, random tests of the specification’s lemmas and of the
parallel-pair rows, and a checker of its own that decides the one-node tree `JQ`. Its
README says what each program read and decides, the one line changed at retention, and
the evidence entries that record them.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source kleddamag-n17-candidate-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.acquire_source kleddamag-n17-candidate-2026-10-12 --checkout CLONE
.venv/bin/python3 -I resources/web/kleddamag-n17-candidate-2026-10-12/receipts/programs/compare_statement.py .. CLONE OUT.json
bash resources/web/kleddamag-n17-candidate-2026-10-12/review-2/run.sh CLONE > RESULTS.txt
```

`--check` re-derives the record from this packet alone; `--checkout` needs a clone at
the pin and refuses one that does not yield this record and manifest.
The comparison needs the clone for `STATEMENT.md` and the seed, and nothing else.
`run.sh` needs the clone without the release’s large files, writes `audit.json` to a
temporary directory, and takes about 15 seconds; its output should equal
[review-2/RESULTS.txt](review-2/RESULTS.txt).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
