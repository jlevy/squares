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
no register entry; it retains the sources and the stage 4 samples that rest on them.

## Custody

`devtools.acquire_source` wrote the packet from the declaration in `acquisition/`, from a
full clone at the pin; every file is bound to its Git blob at `ad8b094`, and
`acquisition/upstream-subtree.sha256` lists all seven. The scope is the whole tree:
990,199 bytes, all retained. The three receipts add 2,156,813 bytes, 2,128,349 of them
`two-strip-decisions-v5.json`, so the packet is about 3.16 MB in a checkout; OR-18 admits
it, and `check_added_blobs` passes.

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

**v5, every row** (`receipts/two-strip-decisions-v5.json`): `devtools.two_strip_checker`
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

No program here decides a V2.0 row from its parameters: that is W9’s (think-fuwd), and
the full validation is think-qczx’s.

These programs are not yet registered in `frontier/verifiers.yaml` and no evidence entry
cites their receipts: the rows they serve are not recorded until the walk above 1024
records them (R5 for v5 with #799’s, a later slice for the filled-end sets).

## Credit and Licence

The rows are Mohsen Karimi’s. As his READMEs state it, the two-strip packing is an
instance of Sungjoon Ryu’s L-shaped packing (doi:10.5281/zenodo.23278927, Theorem 1.3)
with independent widths, angles and phases, found independently; the filled-end packing
adds axis-parallel layers in the band ends, Evan Daniel’s idea (evand/square-packing,
`certificates/k2-minus-c/`), written as in Kevin Fang’s note
(doi:10.5281/zenodo.23624565, Sections 2–3). Claude assistance is disclosed in both.

Every file is under CC BY 4.0, and the code also under MIT, as the author states it:

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
the walk above 1024 records them, so the preprint enters it with those rows.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source karimi-records-2026-10-31 --check
python -m devtools.two_strip_checker check            # every deposit, v5 included
python -m devtools.two_strip_checker replay-sample --version 5 --workers 2
python -m devtools.filled_end_sample check [--replay]
python -m devtools.filled_end_sample replay --workers 2
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
