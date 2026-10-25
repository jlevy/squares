# Mohsen Karimi’s Two-Strip Packings at 1184 to 3775, Zenodo V1.0

[Issue #799](https://github.com/jlevy/squares/issues/799), opened 2026-10-24T19:49:24Z by
mohsensbu-jpg, reports 683 upper bounds at $n = 1184$ to $3775$, credited to Mohsen Karimi
(ORCID 0009-0004-1055-8267). They are published as Zenodo record
[10.5281/zenodo.23624433](https://doi.org/10.5281/zenodo.23624433), version V1.0.
Each row of its `records.csv` states an exact side $S < K = \lceil\sqrt n\,\rceil$ and the
seven parameters of one packing. A box of side $S$ holds two strips of unit squares tilted
by small angles with rational $\tan(a/2)$: $m_H$ rows on the bottom wall and $m_V$ rows
standing on the right wall. The rest of the box is a $(K - m_V) \times (K - m_H)$
axis-parallel grid. The record holds no certificate file.

The construction is Sungjoon Ryu’s L-shaped packing (his Theorem 1.3) with the two
strips’ widths, angles and phases chosen independently. The maintained checker
[`devtools.two_strip_checker`](../../../devtools/two_strip_checker.py) decides every row
exactly from its parameters, as the owner’s D2 answer asks of a construction with no
certificate file (think-f2io).

**No row is recorded here.** The rows wait for the walk above 1024, which R1 of
[the plan for rows above 1024](../../../../docs/project/specs/active/plan-2026-10-24-rows-above-1024.md)
creates (think-llit). That walk decides report order at each count, and the rows land in
a records slice of their own. Bead `think-5dc3` holds the import and the reply, and
`think-clgp` the checker.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | Zenodo record 23624433, [10.5281/zenodo.23624433](https://doi.org/10.5281/zenodo.23624433), *Two-strip square packings: improved upper bounds for s(n), n = 1184–3775*, by Mohsen Karimi (independent researcher, Zanjan, Iran) |
| Version | V1.0, created 2026-10-24T19:32:47Z, the first version of concept `10.5281/zenodo.23624432` |
| Files | `karimi_two_strip_records_v1_lite.zip`, 13,329 bytes, MD5 `14499cbc797c5775c8a3887cc61bc9c6` as the record states, SHA-256 `0d4f89b0b9353af405139cbb249831edd4f480cece86e219431ac924546978c5`; `issue_text-1.md`, 1,619 bytes, MD5 `4d27a831ecf09e359d8190676b034ae7`, SHA-256 `0ea2844e4fcaef4819799417149ce77590d4568e5de3c979615e742dd8d7ff1e` |
| The issue’s attachment | The zip attached to #799’s comment of 20:08:23Z is the same file byte for byte, by its SHA-256 (the stage 1 triage, think-5dc3) |
| Licence | The record states CC BY 4.0. The deposit’s README says “License: data CC BY 4.0; code MIT” |
| Retrieved | 2026-10-25T04:24:16Z, by `devtools.capture_web_source zenodo`; the stage 1 triage read the same bytes at 2026-10-24T20:27Z |
| Retained here | 4 files, 59,957 bytes: the archive’s three members (58,338 bytes) and `issue_text-1.md` |
| Dated by | The issue, 2026-10-24T19:49:24Z: the time the claims reached this repository (think-5dc3, O5) |

The same text was opened as Mishapolk/square-packing-records#1 at 19:44:35Z, five minutes
before #799, with no commit to that repository.

**A later version is not this packet.** Version 2,
[10.5281/zenodo.23628190](https://doi.org/10.5281/zenodo.23628190), was created at
2026-10-24T22:32:58Z and reported on #799 at 22:34:47Z: 2,824 rows at $n = 1184$ to
$9944$. A comment at 22:09:22Z cites a theorem preprint by the author,
[10.5281/zenodo.23627827](https://doi.org/10.5281/zenodo.23627827). Neither is retained
here, and neither has been triaged.

## Credit and AI Assistance, as the Source States Them

The deposit’s README names the construction “Karimi two-strip construction” and says “The
idea and the cost–benefit design are due to Mohsen Karimi”.
Its credits read: “Construction idea, strip cost–benefit analysis and research
direction: Mohsen Karimi. Code and computations were written with the assistance of
Claude (Anthropic), an AI model, under the author’s direction. Verifier: M. Polkovskyi
(Mishapolk).” The issue says the same of the code.

The README cites neither Ryu’s Theorem 1.3, nor Evan Daniel’s Lean variants of it
(evand/square-packing `aa12b98`, 18 October), nor Kevin Fang’s #797. The record credits
every row to Mohsen Karimi, as the source states. It describes the construction as a
two-strip (L-shaped) packing after Ryu’s Theorem 1.3, and holds the eponym until the
author answers the acknowledgement’s question (think-5dc3, O4).

## What Is Retained

- **[`zenodo/`](zenodo/)**, written by
  `python -m devtools.capture_web_source zenodo 23624433 --extract README.md --extract records.csv --extract regenerate.py`.
  It holds the record and its file listing as Zenodo served them
  (`zenodo-23624433.json`, `zenodo-23624433-files.json`), the archive’s member list
  (`zenodo-23624433.sha256`), the capture’s receipt with each file’s stated and computed
  digests (`zenodo-23624433-receipt.json`), and the three members under
  [`zenodo-23624433/`](zenodo/zenodo-23624433/):
  - `records.csv`, 52,333 bytes, the 683 rows: `n`, `new_side_exact` (the side as
    `p/q`), `new_side` (the same side as a decimal of ten places), `previous_best_side`
    (the author’s comparison), and `K`, `mH`, `tH`, `phH`, `mV`, `tV`, `phV`;
  - `README.md`, 2,626 bytes, the deposit’s description, credit and licence;
  - `regenerate.py`, 3,379 bytes, the author’s builder, kept as text. It was read and
    never run here. `two_strip_checker.write_out`, written from the README and the issue,
    is the record’s own builder.
- **`zenodo-23624433/issue_text-1.md`**, the record’s second file. The capture checks it
  by its MD5 and does not write it, so it was fetched alone and held to the receipt’s
  SHA-256.
- **[`acquisition/issue-799.json`](acquisition/issue-799.json)**, the issue with its four
  comments, read with `gh issue view` on 25 October 2026.
- **Not retained:** the archive itself, which the DOI serves and the MD5 and SHA-256 above
  pin (OR-18). Also not retained are the 683 certificates written out from the
  parameters, 56,229,853 bytes in all (the largest 127,079): they are derived, `write_out`
  writes them again byte for byte, and the decisions receipt pins each by its SHA-256 and
  size.

The source is a Zenodo deposit, not a Git repository. `devtools.acquire_source`, which
binds each file to its Git blob at an upstream commit, therefore does not apply. The
capture held each download to the MD5 Zenodo states, and the digests above are the stage
1 triage’s. From then on Git keeps the bytes (OR-16). Before any row is read,
`two_strip_checker.custody` checks only that the packet keeps exactly the files the
capture names.

The checker reads `records.csv` as untrusted data (`parse_records`). The header must be
the eleven columns exactly, and each row eleven fields. Each literal is matched whole,
with at most 30 digits in any part (the longest here has 12). $K$ must be at most 1,000
and equal $\lceil\sqrt n\,\rceil$, and each count may appear once. Every refusal is a
`CustodyError`.

## What the Rows Claim

683 counts from 1184 to 3775, with $K$ from 35 to 62 and $K = \lceil\sqrt n\,\rceil$ at
every row. Each side is a terminating decimal of at most ten places, below $K$, and the
decimal column equals the exact one at every row. The phases are 0, 1/4, 1/2 and 3/4.
The issue’s six-place prints round to nearest, so they are not upper bounds (at 2342 the
print is 48.900000 and the side 48.90000012); the record reads the exact sides from
`records.csv`.

The README says each row is below the bounds of Mishapolk/square-packing-records at
`7e82c64` and franciscouzo/square-packing on 24 October, and that “In 85 cases the
previous best was the trivial grid.” The walk above 1024 decides how each row stands
against every earlier report. The stage 1 triage found all 683 below every earlier
report it read and below Göbel’s construction (think-5dc3).

## What Was Checked Here

Two receipts under [`receipts/`](receipts/), each written by
[`devtools.two_strip_checker`](../../../devtools/two_strip_checker.py). Everything in it is
exact, in integers and fractions.

- **[`two-strip-decisions.json`](receipts/two-strip-decisions.json)**, `decide-all` (7.4
  CPU-seconds). Every row is decided by the checker’s lemma: no two squares of a strip
  overlap, the three regions are disjoint inside $[0, S]^2$ by the two fit inequalities,
  and the count is at most the capacity. The capacity equals $n$ at 403 rows and exceeds
  it by at most 19. The least slack in the fit inequalities is $1.13 \cdot 10^{-8}$ for
  the bottom strip and $1.36 \cdot 10^{-8}$ for the right one. Each row carries seven
  controls, and all 4,781 are refused:
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
  is a genuine two-strip packing by the same lemma, whose capacity falls only because
  the row’s parameters were locally better. The grid one larger and both strips deeper
  are refused while the slacks are below 1 and below each strip’s $c$ (about 0.98);
  the largest here is 0.025. The receipt records each written-out certificate’s
  SHA-256 and size, and records no row of the coverage register.
- **[`replay-sample.json`](receipts/replay-sample.json)**, `replay-sample` (49 seconds
  wall at two workers; 8.4 CPU-seconds of positives and 64.9 of controls). It is the
  cross-check. At 1184, 1193, 1813, 2363 and 3775 the written-out certificate is decided
  on both exact routes of `devtools.couzo_678_replay`, `sqpack`’s predicates and the
  independent checker, over every wall and every pair whose centres are closer than
  $\sqrt 2$ (2,850, 2,754, 4,228, 5,436 and 8,688 pairs). All five pass, and every one of
  the six controls of each is refused by both routes, 30 of 30. The certificates are the
  ones whose digests the decisions receipt states.

The checker also decides Ryu’s own packings: at his Theorem 1.3 parameters (equal bands
at Lemma 4.2’s angle) its capacity is at least his count $N(k, b)$ for every
$2 \le b < k \le 40$. That is checked in `tests/test_two_strip_checker.py`.

From `packing/`, with the project interpreter:

```sh
python -m devtools.two_strip_checker decide-all
python -m devtools.two_strip_checker replay-sample --workers 2
python -m devtools.two_strip_checker check [--digests] [--replay]
```

`tests/test_two_strip_checker.py` runs the controls at every row, the refusals, the
agreement with Ryu’s packings and with both routes on small written-out packings, and
the receipts’ check in the pull-request tier. The replay of 1184 and every count’s
digest are in the slow lane.

## Limitations

- **No row is recorded.** Report order, the comparison with earlier reports at each
  count and the coverage rows are the walk’s and the records slice’s.
- **The packings checked are this record’s write-out**, built from the parameters by
  `write_out`. They are not the author’s files, which the record never received.
- **No source program ran.** `regenerate.py` is retained as text only.
- **Version 2 and the theorem preprint** are not retained or triaged here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
