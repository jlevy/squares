# Mohsen Karimi’s Two-Strip Packings at 1184 to 9944, Zenodo Versions 1 and 2

[Issue #799](https://github.com/jlevy/squares/issues/799), opened 2026-10-24T19:49:24Z by
mohsensbu-jpg, reports 683 upper bounds at $n = 1184$ to $3775$, credited to Mohsen Karimi
(ORCID 0009-0004-1055-8267). They are published as Zenodo record
[10.5281/zenodo.23624433](https://doi.org/10.5281/zenodo.23624433), version V1.0.
The author’s comment of 22:34:47Z that day reports version 2,
[10.5281/zenodo.23628190](https://doi.org/10.5281/zenodo.23628190): 2,824 rows at
$n = 1184$ to $9944$.

Each row of a version’s `records.csv` states an exact side $S < K = \lceil\sqrt n\,\rceil$
and the seven parameters of one packing. A box of side $S$ holds two strips of unit squares
tilted by small angles with rational $\tan(a/2)$: $m_H$ rows on the bottom wall and $m_V$
rows standing on the right wall. The rest of the box is a $(K - m_V) \times (K - m_H)$
axis-parallel grid. Neither version holds a certificate file.

The construction is Sungjoon Ryu’s L-shaped packing (his Theorem 1.3) with the two
strips’ widths, angles and phases chosen independently. The maintained checker
[`devtools.two_strip_checker`](../../../devtools/two_strip_checker.py) decides every row
of both versions exactly from its parameters, as the owner’s D2 answer asks of a
construction with no certificate file (think-f2io).

**No row is recorded here.** The rows wait for the walk above 1024, which R1 of
[the plan for rows above 1024](../../../../docs/project/specs/active/plan-2026-10-24-rows-above-1024.md)
creates (think-llit). That walk decides report order at each count, and the rows land in
a records slice of their own, R5. Bead `think-5dc3` holds the import and the reply,
`think-clgp` the checker, and `think-z2mj` the second triage, of the later comments.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | Zenodo concept `10.5281/zenodo.23624432`, *Two-strip square packings: improved upper bounds for s(n)*, by Mohsen Karimi (independent researcher, Zanjan, Iran). It lists three versions ([`acquisition/zenodo-23624432-versions.json`](acquisition/zenodo-23624432-versions.json)) |
| Version 1 | Record 23624433, V1.0, created 2026-10-24T19:32:47Z: `karimi_two_strip_records_v1_lite.zip`, 13,329 bytes, MD5 `14499cbc797c5775c8a3887cc61bc9c6` as the record states, SHA-256 `0d4f89b0b9353af405139cbb249831edd4f480cece86e219431ac924546978c5`; and `issue_text-1.md`, 1,619 bytes, MD5 `4d27a831ecf09e359d8190676b034ae7`, SHA-256 `0ea2844e4fcaef4819799417149ce77590d4568e5de3c979615e742dd8d7ff1e` |
| Version 2 | Record 23628190, created 2026-10-24T22:32:58Z, the last version: `karimi_two_strip_records_v2_lite-1.zip`, 36,756 bytes, MD5 `cba95c0c8a7cdb98719c88dbff63389b`, SHA-256 `1b072b5398fc1add55a07fba8292b7aa9a053e8b083dd4485e2cb78bfff53108` |
| The middle version | Record 23628081, created 22:29:35Z, carries version 2’s title over version 1’s zip, byte for byte. It holds no row and is pinned only by the listing |
| The issue’s attachment | The zip attached to #799’s comment of 20:08:23Z is version 1’s, byte for byte, by its SHA-256 (the stage 1 triage, think-5dc3) |
| Licence | Each record states CC BY 4.0. Each deposit’s README says “License: data CC BY 4.0; code MIT” |
| Retrieved | Version 1 at 2026-10-25T04:24:16Z and version 2 at 04:31:17Z, by `devtools.capture_web_source zenodo`. The stage 1 triages read the same bytes at 2026-10-24T20:27Z and from 05:20Z on 25 October |
| Retained here | 6 files, 274,154 bytes: version 1’s three archive members and `issue_text-1.md` (59,957 bytes), and version 2’s `README.md` and `records.csv` (215,201 bytes) |
| Dated by | Version 1 by the issue, 2026-10-24T19:49:24Z, and version 2 by the comment of 22:34:47Z: the times the claims reached this repository (think-5dc3, O5) |

The same texts were posted at Mishapolk/square-packing-records#1, opened at 19:44:35Z,
five minutes before #799, with no commit to that repository.

**The preprint is pinned, not retained.** The author’s comments of 22:09:22Z and
04:51:33Z cite his note *Packing unit squares in a square of side just below an integer:
a two-strip construction with O(√K) deficit*. Version V1.0 is
[10.5281/zenodo.23627827](https://doi.org/10.5281/zenodo.23627827) (`karimi_near_integer.pdf`,
224,724 bytes, MD5 `3f51d3e5a5b9c2a7aa81ffeef5626901`, SHA-256
`abb4f0b83c45711a6c9b6061e000d3437fa98eed8126b21e00986f455e700a4a`). Version V2.0 is
[10.5281/zenodo.23633300](https://doi.org/10.5281/zenodo.23633300)
(`karimi_near_integer_v2.pdf`, 236,034 bytes, MD5 `e1b201e4b5260983d69d7e02fdb23196`,
SHA-256 `d9685b57275f26dcd077d3b8e5a1f2265035eb715c105c573ab1d36fc3820fbe`). Both are under
CC BY 4.0, and the concept is `10.5281/zenodo.23627826`. The capture writes each record and
its receipt with those digests, and no PDF. Its Theorem 1 takes no row of the record’s
asymptotic table, since Ryu’s, Daniel’s and Fang’s reported bounds are smaller at every
K. #799’s requests entry notes it with its one new statement, the side window
$[K - 1/K, K)$.

## Credit and AI Assistance, as the Source States Them

The deposit’s README names the construction “Karimi two-strip construction” and says “The
idea and the cost–benefit design are due to Mohsen Karimi”.
Its credits read: “Construction idea, strip cost–benefit analysis and research
direction: Mohsen Karimi. Code and computations were written with the assistance of
Claude (Anthropic), an AI model, under the author’s direction. Verifier: M. Polkovskyi
(Mishapolk).” The issue says the same of the code. Version 2’s README adds: “Part of the
search was run by the author in MATLAB Online.”

Neither README cites Ryu’s Theorem 1.3, Evan Daniel’s Lean variants of it
(evand/square-packing `aa12b98`, 18 October) or Kevin Fang’s #797. The record credits
every row to Mohsen Karimi, as the source states. It describes the construction as a
two-strip (L-shaped) packing after Ryu’s Theorem 1.3, and holds the eponym until the
author answers the acknowledgement’s question (think-5dc3, O4).

## What Is Retained

- **[`zenodo/`](zenodo/)**, written by `python -m devtools.capture_web_source zenodo` for
  each record. For each it holds the record and its file listing as Zenodo served them, the
  capture’s receipt with each file’s stated and computed digests and, for an archive, its
  member list (`zenodo-RECORD.sha256`).
  - **Version 1**, with `--extract README.md --extract records.csv --extract
    regenerate.py`, under [`zenodo-23624433/`](zenodo/zenodo-23624433/):
    - `records.csv`, 52,333 bytes, the 683 rows: `n`, `new_side_exact` (the side as
      `p/q`), `new_side` (the same side as a decimal of ten places),
      `previous_best_side` (the author’s comparison), and `K`, `mH`, `tH`, `phH`, `mV`,
      `tV`, `phV`;
    - `README.md`, 2,626 bytes, the deposit’s description, credit and licence;
    - `regenerate.py`, 3,379 bytes, the author’s builder, kept as text. It was read and
      never run here. `two_strip_checker.write_out`, written from the README and the
      issue, is the record’s own builder;
    - `issue_text-1.md`, the record’s second file. The capture checks it by its MD5 and
      does not write it, so it was fetched alone and held to the receipt’s SHA-256.
  - **Version 2**, with `--extract README.md --extract records.csv`, under
    [`zenodo-23628190/`](zenodo/zenodo-23628190/): `records.csv`, 212,304 bytes, the
    2,824 rows in the same eleven columns, and `README.md`, 2,897 bytes. Its
    `regenerate.py` is version 1’s, byte for byte, as the member list shows, so it is not
    kept twice.
  - **The preprint’s two records**, 23627827 and 23633300, with no file extracted.
- **[`acquisition/`](acquisition/)**: the issue with its five comments, read with
  `gh issue view` on 25 October 2026 (`issue-799.json`), and each concept’s version
  listing as Zenodo served it.
- **Not retained:** the archives and the preprint’s PDFs, which the DOIs serve and the
  digests above pin (OR-18). Also not retained are the written-out certificates: 683 for
  version 1 (56,229,853 bytes, the largest 127,079) and 2,824 for version 2 (527,961,559
  bytes, the largest 336,743). They are derived, `write_out` writes them again byte for
  byte, and the decisions receipts pin each by its SHA-256 and size.

The source is a Zenodo deposit, not a Git repository. `devtools.acquire_source`, which
binds each file to its Git blob at an upstream commit, therefore does not apply. The
capture held each download to the MD5 Zenodo states, and the digests above are the stage
1 triages’. From then on Git keeps the bytes (OR-16). Before any row is read,
`two_strip_checker.custody` checks only that the packet keeps exactly the files each
capture names.

The checker reads each `records.csv` as untrusted data (`parse_records`). The header must
be the eleven columns exactly, and each row eleven fields. Each literal is matched whole,
with at most 30 digits in any part (the longest in either version has 12). $K$ must be at
most 1,000 and equal $\lceil\sqrt n\,\rceil$, and each count may appear once. Every
refusal is a `CustodyError`.

## What the Rows Claim

**Version 1:** 683 counts from 1184 to 3775, with $K$ from 35 to 62. **Version 2:** 2,824
counts from 1184 to 9944, with $K$ from 35 to 100. In both, $K = \lceil\sqrt n\,\rceil$ at
every row, each side is a terminating decimal of at most ten places below $K$, and the
decimal column equals the exact one. The phases are 0, 1/4, 1/2 and 3/4. The issue’s
six-place prints round to nearest, so they are not upper bounds (at 2342 the print is
48.900000 and the side 48.90000012); the record reads the exact sides from `records.csv`.

At version 1’s 683 counts, version 2 states the same side and parameters at 682. At 2459
it states a side $4 \cdot 10^{-8}$ lower (49.98253277 against 49.98253281) with the same
parameters. Its other 2,141 rows, at 3776 to 9944, are at counts version 1 does not
reach.

Each README says its rows are below the bounds of Mishapolk/square-packing-records at
`7e82c64` and franciscouzo/square-packing on 24 October. Version 1’s says “In 85 cases the
previous best was the trivial grid”, and version 2’s says 867. The walk above 1024
decides how each row stands against every earlier report. The stage 1 triages found
version 1’s 683 rows and version 2’s 2,141 new rows below every earlier report they read
and below Göbel’s construction (think-5dc3, think-z2mj). Version 2 ties version 1 at 682
counts, where the earlier report keeps the row, and refines it at 2459.

## What Was Checked Here

Three receipts under [`receipts/`](receipts/), each written by
[`devtools.two_strip_checker`](../../../devtools/two_strip_checker.py). Everything in it is
exact, in integers and fractions.

- **[`two-strip-decisions.json`](receipts/two-strip-decisions.json)** (version 1) and
  **[`two-strip-decisions-v2.json`](receipts/two-strip-decisions-v2.json)** (version 2),
  `decide-all` (7.4 and 67.0 CPU-seconds, most of it writing out the certificates for
  their digests). Every row is decided by the checker’s lemma: no two squares of a strip
  overlap, the three regions are disjoint inside $[0, S]^2$ by the two fit inequalities,
  and the count is at most the capacity.
  - In version 1, the capacity equals $n$ at 403 rows and exceeds it by at most 19. In
    version 2, it equals $n$ at 1,366 rows and exceeds it by at most 42.
  - In both, the least slack in the fit inequalities is $1.13 \cdot 10^{-8}$ for the
    bottom strip and $1.36 \cdot 10^{-8}$ for the right one.
  - Each row carries seven controls, and all are refused, 4,781 in version 1 and 19,768
    in version 2:
    - one square above the capacity;
    - the side $10^{-15}$ below the binding fit inequality;
    - both strips one row deeper around the same grid ($K$, $m_H$ and $m_V$ each one
      more) at the capacity;
    - no tilt;
    - a right angle;
    - the grid one column and row larger;
    - an unknown kind.

  A side $10^{-12}$ lower is no control here, since every side sits at least
  $1.13 \cdot 10^{-8}$ above its fit. Nor is the bottom strip one row deeper alone: that
  is a genuine two-strip packing by the same lemma, whose capacity falls only because the
  row’s parameters were locally better. The grid one larger and both strips deeper are
  refused while the slacks are below 1 and below each strip’s $c$ (about 0.98); the
  largest slack in version 1 is 0.025. Each receipt records each written-out
  certificate’s SHA-256 and size, and records no row of the coverage register.
- **[`replay-sample.json`](receipts/replay-sample.json)**, `replay-sample` (49 seconds
  wall at two workers; 8.4 CPU-seconds of positives and 64.9 of controls). It is the
  cross-check. At 1184, 1193, 1813, 2363 and 3775 the written-out certificate is decided
  on both exact routes of `devtools.couzo_678_replay`, `sqpack`’s predicates and the
  independent checker, over every wall and every pair whose centres are closer than
  $\sqrt 2$ (2,850, 2,754, 4,228, 5,436 and 8,688 pairs). All five pass, and every one of
  the six controls of each is refused by both routes, 30 of 30. The certificates are the
  ones whose digests version 1’s decisions receipt states. Version 2 states the same row
  at all five counts.

The checker also decides Ryu’s own packings: at his Theorem 1.3 parameters (equal bands
at Lemma 4.2’s angle) its capacity is at least his count $N(k, b)$ for every
$2 \le b < k \le 40$. That is checked in `tests/test_two_strip_checker.py`.

From `packing/`, with the project interpreter:

```sh
python -m devtools.two_strip_checker decide-all [--version 1] [--version 2]
python -m devtools.two_strip_checker replay-sample --workers 2
python -m devtools.two_strip_checker check [--digests] [--replay]
```

`tests/test_two_strip_checker.py` runs these checks in the pull-request tier:
- the controls at every row of version 1;
- the refusals, the ingest’s included;
- the agreement with Ryu’s packings and with both routes on small written-out packings;
- the receipts’ check, both versions’ decisions included.

The replay of 1184 and every count’s digest are in the slow lane.

## Limitations

- **No row is recorded.** Report order, the comparison with earlier reports at each
  count and the coverage rows are the walk’s and the records slice’s, R5.
- **The packings checked are this record’s write-out**, built from the parameters by
  `write_out`. They are not the author’s files, which the record never received.
- **The routes have decided five counts, all at or below 3775.** Version 2 reaches 9944,
  where R5 is to measure one count on both routes before replaying the rest.
- **No source program ran.** `regenerate.py` is retained as text only.
- **The preprint is pinned, not read here.** The second triage read Theorem 1 and checked
  its steps by hand, which is not a review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
