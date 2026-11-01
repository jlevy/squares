# Mohsen Karimi’s Record Sets at ad8b094

This packet retains
[mohsensbu-jpg/square_packing_records_karimi](https://github.com/mohsensbu-jpg/square_packing_records_karimi/tree/ad8b094be0785ed47fd90f5b965bc84c077d5bb1)
at `ad8b094be0785ed47fd90f5b965bc84c077d5bb1` (committed 2026-10-31T11:40:48Z, “Copies of
Zenodo deposits, unchanged”), the repository’s only commit. Mohsen Karimi (ORCID
0009-0004-1055-8267) made it after this repository’s acknowledgements said zenodo.org
was unreachable from its environment, and named it on
[#836](https://github.com/jlevy/squares/issues/836#issuecomment-6542916041) at
11:43:02Z and [#847](https://github.com/jlevy/squares/issues/847#issuecomment-6542921495)
at 11:43:36Z as unchanged copies of three Zenodo records:

| Zenodo record | Version | Reported by | Kept here as |
| --- | --- | --- | --- |
| [10.5281/zenodo.23664800](https://doi.org/10.5281/zenodo.23664800) | two-strip v5.0, 2026-10-26 | #836 | `source/karimi_two_strip_records_v3_lite.zip` |
| [10.5281/zenodo.23819397](https://doi.org/10.5281/zenodo.23819397) | filled-end V2.0, 2026-10-30 | #847 | `source/filled_records.csv`, `filled_ends.py`, `regenerate_filled.py`, `check_cert.py`, `README_filled.md` |
| [10.5281/zenodo.23681705](https://doi.org/10.5281/zenodo.23681705) | filled-end V1.0, 2026-10-27 | #836’s comment of 27 October | `source/karimi_filled_end_v2.zip` |

zenodo.org was still refused by the session’s network policy when the packet was
written, so no Zenodo listing was read. The rows are above 1024, where the record keeps
upper bounds as dated rows of its coverage register, decided in report order by
think-llit’s walk above 1024, which does not exist yet. So this packet records no row and
no register entry; it retains the sources and the stage 4 checks that rest on them: two
samples, the full replay of v5 on both routes, and W9’s decisions of every filled-end
row.

## Custody

`devtools.acquire_source` wrote the packet from the declaration in `acquisition/`, from a
full clone at the pin; every file is bound to its Git blob at `ad8b094`, and
`acquisition/upstream-subtree.sha256` lists all seven. The scope is the whole tree:
990,199 bytes, all retained. The receipts add 2,780,357 bytes: 420,373 for
`two-strip-decisions-v5.json.gz`, 28,464 for the two samples, and 2,331,520 for the full
replay of v5, 66 receipts of at most 169 lines each and their summary. So the packet is
about 3.8 MB in a checkout; OR-18 admits it, and `check_added_blobs` passes. The
decisions receipt, 5,339 lines and 2,128,349 bytes, is stored as deterministic gzip, as
`devtools.retained_data` keeps a retained file of more than 1,000 lines
([Compressed Files](#compressed-files)); every other two-strip receipt is under that
threshold.

W9’s receipts (below) add 1,352,523 bytes stored: its two decisions receipts, each over
1,000 lines, are stored the same way, 722,184 bytes for V2.0’s and 615,884 for V1.0’s,
and the replay sample is 14,455 bytes, plain. The stage 4 review’s programs and receipts
under `review/` add 604,175 bytes in 14 files, so the packet is about 5.8 MB.

Each digest the author stated holds:

| File | SHA-256 as stated | Where it was stated |
| --- | --- | --- |
| `karimi_two_strip_records_v3_lite.zip` | `9c70c4d8…6325` | #836’s body |
| its member `records.csv` | `7e78c15d…e941` | #836’s body |
| `filled_records.csv` (V2.0) | `1cbfecf8…48f5` | #847’s body |
| `karimi_filled_end_v2.zip` (V1.0) | `f1684581…7cfa97` | #836’s comment of 27 October |
| its member `filled_records.csv` | `f047c44b…0b56` | #836’s comment of 27 October |

These were checked once, when the packet was written. From then on Git keeps the bytes
and `acquire_source --check` holds every retained file to the manifest (OR-16), so no
program here compares a digest when it runs. Review A1 of #853 asked that a file with no
stated digest be checked against Zenodo’s per-file listing, or a digest the author
states, before any checker reads it. Zenodo’s listing was unreachable, so:

- V2.0’s `filled_ends.py`, `regenerate_filled.py` and `check_cert.py` state no digest
  of their own, but each is byte-identical to the member of the same name in the V1.0
  archive, whose SHA-256 the author stated on 27 October, before this copy existed
  (`filled_ends.py`: `91ac0758…9210`). That binds them to the V1.0 programs he
  published; that they are also V2.0’s files rests on his statement that `ad8b094`
  holds unchanged copies, as `README_filled.md`’s does. No decision rests on it: the
  routes decide, and the builder only writes the certificates out.
- The v5 archive’s `regenerate.py` is versions 1 and 2’s byte for byte (`67c861dc…a04f`,
  retained by `karimi-two-strip-2026-10-24`).
- V2.0’s `README_filled.md` and the v5 archive’s `README.md` have no stated digest and no
  copy to compare with. They are pinned by the commit alone, and no checker reads them;
  their credit statements are read as the author’s words.

## What the Sets Claim, and What the Data Say

Every count the issues state holds in the data:

- **v5.0 (#836):** 5,308 rows at n = 1182 to 9944, in the two-strip format of #799 with
  the author’s `below_all_reported` column after the eleven (51 rows `no`, 5,257 `yes`).
  Against version 2 (#799): 2,484 counts new, 1,434 lower, 1,390 identical in side and
  parameters, none higher.
- **V2.0 (#847):** 5,134 rows at n = 1182 to 9946, each an exact side and the parameters
  K, bV, tV, yV, bH, tH, yH. Against v5: 4,841 rows lower and none not lower, 293 counts
  new; 467 v5 rows have no V2.0 row, and the two sets cover 5,601 counts.
- **V1.0:** 4,571 rows at 1184 to 9946: 4,261 lower than v5 and 310 at counts v5 lacks.
  V2.0 drops 40 of its counts, the 40 #847 lists. Where both state a count, V2.0 equals
  V1.0 at 598 and is lower at 3,933.

Whether a row is below every earlier report at its count, and whether V1.0 counts as an
earlier report at all (Q-847a on think-r94q, the owner’s; the author is “content with
whatever the project’s owner decides”), are the walk’s and the owner’s, not this packet’s.

## Decided Here

**v5, every row** (`receipts/two-strip-decisions-v5.json`, stored as `.gz`):
`devtools.two_strip_checker`
reads the retained archive’s `records.csv` through version 5’s own column set and
decides all 5,308 rows exactly from their parameters, each row’s seven controls refused
(212.9 CPU-seconds with the digests of every written-out certificate, which are not
kept). Least fit slack: 1.0e-8 in both strips. The author’s flag is
counted and decides nothing.

**v5, a sample on both routes** (`receipts/replay-sample-v5.json`): at 1182, 1253, 6089,
9912 and 9944, the first count, the first lowered, a new one in the middle, the last
lowered and the largest, the written-out certificate passes both maintained exact routes
of `devtools.couzo_678_replay`, and both refuse all six of its controls. Near 9944 a
count costs 14.7 CPU-seconds for the positive and 120 for the controls.

**v5, every row on both routes** (`receipts/replay-v5/k035.json` to `k100.json`, one
receipt per K, and their summary `receipts/replay-v5.json`; think-gw1s):
`two_strip_checker replay-all` writes out the certificates of all 5,308 rows, and both
maintained exact routes pass every one. Each certificate is the one the decisions
receipt names, by its SHA-256. At one count per K, 66 in all, chosen by the checker’s
rule (the least fit slack, then the smallest count), both routes refuse all six
controls: 396 of 396 by each. The routes decided 31,499,439 squares and 71,808,283
candidate pairs, 70,690,393 of them touching. The least wall clearance and the least
pair gap are both 0, since squares touch the walls and each other, which the closed
contract allows. The run took 47,031.4 CPU-seconds, 13.1 CPU-hours (12.1 for the
positives, 0.9 for the controls), on two workers. K = 35 ran from 17:08:39Z and the
rest from 17:09:33Z on 31 October; the receipts were written from 17:08:54Z to
23:54:32Z. It ran from the working tree that `b0fe65eae` committed at 17:26:15Z, and
its deciding code (`write_out`, `route_row`, the receipt it writes and
`couzo_678_replay`’s routes) is unchanged at the head. Review A of #863 changed only
how the receipts are read back, resumed and stopped, and the stricter read-back accepts
all 66 as written. Six controls at every count would have cost about eight times the
positives, over the compute cap. This decides that each written-out packing is a
packing; which rows the record takes is still the walk’s.

**V2.0, a sample on both routes** (`receipts/filled-end-replay-sample.json`):
`devtools.filled_end_sample` writes out the rows at 1182, 2505, 4990, 7500 and 9946 with
the author’s own `build`, from the retained `filled_ends.py`, and checks that each has
the row’s exact side and n squares. Each certificate passes both maintained exact
routes, and both refuse all six of its controls. The builder is the author’s, so this
reproduces his construction; the decision is first-party, and his `check_cert.py` did
not run. It decides those five certificates, 5 of 5,134 rows, and nothing about the
rest. In the committed receipt, 9946 costs 16.5 CPU-seconds for the positive and 124.1
for the controls. Its `check` writes the five out again with the retained builder, about
0.4 CPU-seconds, and holds each to the size, side and SHA-256 the receipt names. The
builder is third-party code that runs in the quick tests and in CI; it was read whole
first: it imports only `math`, `sys` and `fractions`, its module level defines and does
nothing else, and its one writer, `write_cert`, is never called.

## W9: The Filled-End Checker

`devtools.filled_end_checker` (think-fuwd) decides a filled-end row exactly from its
parameters, by a lemma its module docstring states and proves and
[research-2026-11-01-filled-end-lemma.md](../../../../docs/project/research/research-2026-11-01-filled-end-lemma.md)
writes out. Each band’s rows and its two ends’ layers are interior-disjoint inside the
band; the grid and the two placed bands are disjoint inside $[0, S]^2$ when both fit
inequalities hold; and every count up to the capacity is packed. It was written from
`filled_ends.py` read as data and shares no code with it.

**The stage 4 review accepted the lemma** on 1 November, with no defect
([review-2026-11-01-filled-end-lemma.md](../../../../docs/project/reviews/review-2026-11-01-filled-end-lemma.md)).
A separately prompted lane wrote its own exact geometry, sharing no code with the checker
or the author, and verified every row of both deposits with it: 30,445,623 squares
placed in V2.0 and 27,149,538 in V1.0, no pair overlapping and no wall crossed. Its
programs and receipts are under
[`review/filled-end-lemma-2026-11-01/`](review/filled-end-lemma-2026-11-01/README.md).
Its gaps and notes, F1 to F7, are carried into the checker, the write-up and the
receipts below. So under D2 (think-f2io) each decided row is a row once the walk records
it, and the decisions still record none.

**The decimal side is no bound** (the review’s F2). The ingest holds the author’s decimal
`side` within one unit of its last place of `side_exact`, as a consistency check only.
He rounded to nearest, so it is below `side_exact` at 2,514 of V2.0’s 5,134 rows and
2,204 of V1.0’s 4,571, by up to 0.502 units of its twelfth place (0.504 in V1.0). The V
fit binds at every row, so a square of that side does not hold the construction there.
Each decisions receipt counts this under `author_columns.side`. The walk records a row at
`side_exact`, or at a decimal rounded up from it, never at `side`.

**V2.0, every row** (`receipts/filled-end-decisions-v2.json.gz`): all 5,134 rows decided
by the lemma, none refused. Each row’s eighteen controls are refused, each by the check
it names, which `check` derives again. Seven were added after the review found that
seven of the lemma’s eleven hypotheses had no per-row control (F3):

- the H band one square narrower (the H fit);
- a negative tilt;
- a lift 10^-15 below zero;
- a layer of -1 squares;
- an H band K wide;
- K = 1;
- an H band left shorter than its depth.

The layer controls make one change for every level of a band end and one for the level
after it, 85,174 in all (21,764, 23,228, 19,458 and 20,724 for the four ends), each
refused. 4,851 rows are filled to the capacity and none has a surplus above 7. The least
slacks: the V fit 0 at every row, since $S = K - b_V + W_V$ exactly; the H fit
$1.5 \times 10^{-8}$ (9517); a layer $1.4 \times 10^{-6}$ (5265). 284.2 CPU-seconds,
with the SHA-256 and size of every written-out certificate, which are not kept.

**V1.0, every row, apart** (`receipts/filled-end-decisions-v1.json.gz`): all 4,571 rows
decided, none refused, every control refused by its own check (76,268 layer changes);
246.0 CPU-seconds. It is decided and labelled apart because whether V1.0 counts as a
report at all is the owner’s question Q-847a (think-r94q). The receipt says only that the
lemma decides each of its packings, and `check` holds its note, which names Q-847a, to
the checker’s on every pull request.

The review’s `fe_all_rows.py` compared 16 fields of these receipts as they stood at
`7db2baa55`, with eleven controls, and holds a row to eleven refused. The receipts now
carry eighteen, so that program reads the receipts at that commit; every other field it
compared is unchanged.

**The cross-checks.** At five V2.0 counts nearest the lemma’s edges, 1188 (a lift of
zero), 5265 (the least layer slack), 7439 and 8524 (the least H and V lift room) and 9517
(the least H fit slack), the certificate `write_out` writes passes both maintained exact
routes, and both refuse its six controls (`receipts/filled-end-checker-replay-sample.json`;
430.9 CPU-seconds on two workers, 49.5 of them for the positives and 381.2 for the
controls). And at the five counts of the author-built sample above, `write_out` writes
the author’s certificates byte for byte, which `check` holds by their SHA-256s without
running his code. A row the lemma refuses is no row: `check` names it, and no route
decides it in the lemma’s place. No row of either deposit is refused.

They decide that each stated packing is a packing; which rows the record takes,
and in what order, is still the walk’s (think-llit), after the owner’s D4 and Q-847a.
think-qczx’s full validation on both routes waits for those.

These programs are not yet registered in `frontier/verifiers.yaml` and no evidence entry
cites their receipts: the rows they serve are not recorded until the walk above 1024
records them (R5 for v5 with #799’s, a later slice for the filled-end sets). For v5 the
full replay is the stage 4 evidence those rows will cite, whichever of them the walk
records.

## Credit and Licence

The rows are Mohsen Karimi’s. As his READMEs state it, the two-strip packing is an
instance of Sungjoon Ryu’s L-shaped packing (doi:10.5281/zenodo.23278927, Theorem 1.3)
with independent widths, angles and phases, found independently; the filled-end packing
adds axis-parallel layers in the band ends, Evan Daniel’s idea (evand/square-packing,
`certificates/k2-minus-c/`), written as in Kevin Fang’s note
(doi:10.5281/zenodo.23624565, Sections 2–3). Claude assistance is disclosed in both.

V2.0 and V1.0 are under CC BY 4.0 for every file, the code also under MIT, as the author
states it on #847; v5 is under CC BY 4.0 for its data and MIT for its code, as its
README states:

- **v5:** its README states “License: data CC BY 4.0; code MIT.”
- **V2.0 and V1.0:** `README_filled.md` states no licence, so it was asked. The author
  answered on
  [#847](https://github.com/jlevy/squares/issues/847#issuecomment-6546015739) at
  16:22:49Z on 31 October: both records are published under CC BY 4.0, which covers all
  their files, data and code, and the code files may also be used under the MIT licence,
  as with v5.

The repository has no licence file, and Zenodo’s licence metadata was unreachable from
this environment, so the licence rests on the author’s statements. The files were
retained before his answer, under the owner’s presumption of permission for a submitted
source (think-cnn7). The answer settles the follow-up on think-nu37.

For citation, the same comment names his preprint
[doi:10.20944/preprints202610.2669.v1](https://doi.org/10.20944/preprints202610.2669.v1)
as describing the two-strip records. It is pinned by its DOI alone: doi.org was
unreachable from this environment, so neither its title nor its text was read.
`bibliography.yaml` keeps only the keys a record cites, and no row cites these sets until
the walk above 1024 records them, so the preprint enters it with those rows. Fetching it
and reading its metadata before then is think-rf6h’s.

## Compressed Files

Version 5’s decisions receipt is stored as gzip with no file name or timestamp in the
header (think-rsqv); it decompresses to the receipt as written on 31 October.
`two_strip_checker` reads and writes it through `devtools.retained_data`, so `check`
takes the plain path and `decide-all` writes the gzip again.
A rerun records new timings, so the receipt is not pinned by digest: Git keeps its
bytes (OR-16), and `acquire_source --check` asks that it is listed, carries no name or
timestamp, and decompresses.

W9’s two decisions receipts are stored the same way, through
`filled_end_checker`, which reads and writes them by `devtools.retained_data`, and are
listed here on the same terms.

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `receipts/two-strip-decisions-v5.json.gz` | receipt |  |  |
| `receipts/filled-end-decisions-v1.json.gz` | receipt |  |  |
| `receipts/filled-end-decisions-v2.json.gz` | receipt |  |  |

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source karimi-records-2026-10-31 --check
python -m devtools.two_strip_checker check            # every deposit, v5 included
python -m devtools.two_strip_checker replay-sample --version 5 --workers 2
python -m devtools.two_strip_checker replay-all --version 5 --workers 2   # resumes by K
python -m devtools.filled_end_sample check [--replay]
python -m devtools.filled_end_sample replay --workers 2
python -m devtools.filled_end_checker check [--digests] [--replay]
python -m devtools.filled_end_checker decide-all [--version 2] [--version 1]
python -m devtools.filled_end_checker replay-sample --workers 2
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
