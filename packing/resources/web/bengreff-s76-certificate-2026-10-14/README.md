# Benjamin Greff’s Certificate for s(76) = 9, Pinned 2026-10-14

This packet pins the whole of
[bengreff/s76-certificate](https://github.com/bengreff/s76-certificate) at its head of 14
October 2026, for one registration request:
[jlevy/squares#594](https://github.com/jlevy/squares/issues/594), opened by Benjamin
Greff (`bengreff`) at 2026-10-14T02:06:46Z, which reports $s(76) = 9$, the case $k = 9$
of the $k^2 - 5$ series. The upper half is the $9 \times 9$ grid; the new claim is the
lower bound $s(76) \ge 9$, by a mixed cover in Evan Daniel’s format decided by two of
Daniel’s checkers. When it was retrieved the record held $s(76)$ open at
$1793/200 = 8.965$ (wand125, [`n-076.md`](../../../frontier/n-076.md)).

Its proposed Frontier key is **[bengreff s76 certificate 2026-10-14]**. The claim below
is stated as the source states it. What was checked here at retention, and the replay
the triage ran, are in [Checks Made Here](#checks-made-here); none of it is a review,
and nothing here registers the result.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/bengreff/s76-certificate> |
| Revision | `1cb924fa2fb7e8e30d8ddeb9b5e0dfcfae4f9f1f`, branch `main`, tree `b7c5ee885d529b258078afeb8687c68923269440`: the revision #594 names, and the head of `main` when retrieved and again at 05:53Z |
| Committed | 2026-10-14T02:05:47Z, 21:05:47 on 13 October by the author’s clock (`-05:00`) |
| History | Four commits by Benjamin Greff, all on 14 October (UTC). The first, `7c7832759f46f43686daf6f1191b6a25709e0022` at 01:57:08Z, adds the cover, the run records, the Lean wrapper and `verify.sh`; `git diff --stat 7c78327 1cb924f` touches only `LICENSE`, `README.md`, `SHA256SUMS`, `records/toolchain.txt` and `verify.sh` |
| Licence | MIT, “Copyright (c) 2026 Benjamin Greff” (`LICENSE`) |
| Retrieved | 2026-10-14T04:45Z: a shallow clone of `main` at the pinned commit, its history then fetched to the root |
| Pinned subtree | The whole tree: 151 files, 914,432 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | All 151 files, byte-identical at their upstream paths under [`s76-certificate/`](s76-certificate/). The three upstream `.gz` files are kept as published ([Original Gzip Files](#original-gzip-files)) |
| Source checksums | The tree’s own `SHA256SUMS` lists the other 150 files, and `sha256sum -c SHA256SUMS` passes on the retained copy |

Evan Daniel’s checkers are not in the tree. The source’s `verify.sh` fetches them from
evand/square-packing at `b91d70b6ed314624c1434b628a9c7bf9a132c743` and checks their
digests; this repository already retains all four pinned files byte for byte:
`s12/verify2/src/bin/zmx2.rs` (`6b7f0f79…`), `s12/search/zm_mixed.py` (`ee3e2915…`) and
`s12/search/mixed_cover.py` (`bb89de15…`) in the
[September 28 evand packet](../evand-square-packing-2026-09-28/README.md), and
`s12/search/zeromargin.py` (`640fe453…`) with `verify2/Cargo.toml`, `Cargo.lock` and
`src/main.rs` in the [September 26 packet](../evand-square-packing-2026-09-26/README.md).
The Lean wrapper builds on Daniel’s `Sqpack` at evand/square-packing `1718a58`, which no
packet here retains.

## Credit and AI Assistance, as the Source States Them

The README’s Credits section names Evan Daniel (evand/square-packing, MIT) for “the
weighted-cover method at margin zero, the mixed format, the checkers `zmx2`,
`zm_mixed.py` and `zeromargin.py`, and the Lean library”, and wand125
(wand125/square-packing, MIT) for “the s(59) = 8 cover reused for the corners, the
band-insertion construction, and the pinned toolchain”. It ends: “**Benjamin Greff**
directed the work. The search, LP and verification pipeline were built and run with
Claude (Anthropic) as an AI assistant.”

The issue adds, under “AI assistance”: “Yes, extensively. I chose the problem and the
standard of proof, and directed the work. Claude (Anthropic), working as an agent in
Claude Code, built and ran the LP search, the export, the verification script, the
coverage checks, the Lean wrapper and the replay, and drafted this write-up.” It says
there has been no review outside the author’s project.

Neither the tree nor the issue credits this project; the issue cites
[`n-076.md`](../../../frontier/n-076.md) for the standing bound.

## What Is Retained

Everything at the pinned revision, under [`s76-certificate/`](s76-certificate/):

- **`cover/s76_cover_v5.txt.gz`**, the certificate: unpacked, 996,130 bytes with SHA-256
  `b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2`, the digest the
  issue and the README state.
- **`records/`**: the `zmx2` sweep’s per-root log (`zmx2/zmx2_v5.log.gz`) and summary
  (`zmx2_v5.out`), the four roots it leaves (`zmx2/failing_roots.txt`), the 64
  `zm_mixed.py` sub-root records with their jobs list and log tails (`zm_mixed/`), and the
  toolchain of the source’s clean replay (`toolchain.txt`).
- **`tools/`**: `check_total.py` and `check_coverage.py`, the author’s two
  standard-library scripts for the total and for the tiling of the pieces.
- **`lean/`**: `S76Lower.lean`, the generated data `S76T_Pts.lean.gz`, its generator
  `mk_s76_lean.py` and `build_summary.txt`.
- **`verify.sh`**, `README.md`, `LICENSE` and `SHA256SUMS`.
- **`construction/`**: the LP search code, which the source calls research code not
  needed to check the proof.

Nothing is pinned by digest alone.
[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
[`acquisition/sources.json`](acquisition/sources.json) records the pin. From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  bengreff-s76-certificate-2026-10-14 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claim, as the Source States It

| Claim | Certificate | Total | Checks the source reports |
| --- | --- | --- | --- |
| $s(76) \ge 9$, so $s(76) = 9$ with the grid | 41,633 weighted points and 9,744 axis-parallel segments of $[0,9]^2$ in Daniel’s `mixed 1` format, coordinates $X/8000$, weights $w/(4 \cdot 10^8)$, exactly D4-invariant | $3788361049/50000000 = 75.76722098 < 76$ | `zmx2 cert --d4` over 8,100 roots, 4 roots left with 18 uncertified boxes; `zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24` on the 64 sub-roots of those 4, none uncertified; `check_coverage.py` for the tiling |

The argument is the README’s: the measure is a point-and-segment mass on $[0,9]^2$ with
total below 76, such that every closed unit square in $[0,9]^2$, at any position and
angle, captures mass at least one, boundary included. A packing of 76 unit squares at a
side below 9, scaled up to side 9, would hold 76 pairwise disjoint closed unit squares
capturing mass at least 76. By the exact D4 invariance the covering statement needs only
centres in $[0, 9/2]^2$ and $u = \tan(\theta/2) \in [0, 1/2]$. Its two checkers split
that region: `zmx2`, in outward-rounded binary64, decides 8,096 of its 8,100 root cells
of $1/10 \times 1/10 \times 1/8$, and `zm_mixed.py`, in exact rationals, decides the 64
cells of $1/20 \times 1/20 \times 1/32$ that tile the other four. No cell rests on both.

`lean/S76Lower.lean` proves `theorem s76_eq_9 (hcov : S76Cover) : minSide 76 = 9` on
Daniel’s `Sqpack` at `1718a58` (Lean v4.33.1), with axioms `propext`, `Classical.choice`
and `Quot.sound`, built in 15 min 21 s by `build_summary.txt`. The data facts are
kernel-checked (`pts_nodup`, `pts_d4`, `segs_d4`, `wsum_lt`); `S76Cover`, the covering
statement on the D4 region, is a hypothesis, not proved in Lean.

The issue also reports a second pass in progress, `zm_mixed.py` alone over all 129,600
D4 roots, 42,000 done with none uncertified when it was written, whose records are not
at this revision. It names $s(95) = 10$ and $s(116) = 11$ as the author’s next targets.

## Checks Made Here

These were made on 14 October 2026 for the import’s triage, on a shared four-core
x86-64 Linux container, with Python 3.14.7 and rustc 1.97.0. Each checker run below has
its receipt under [`receipts/`](receipts/), written by `devtools.replay_receipt`.
The comparisons and premise checks were made by triage diagnostics that are not yet
repository tools; the import’s bead records them, and registering case 76 in
`devtools.replay_evand_zmx2` and `devtools.audit_evand_mixed_covers` is the tooling
slice it owes.

- **Data facts.** The repository’s `devtools.audit_evand_mixed_covers.audit_cover`
  recomputes the cover’s total, counts and exact D4 invariance, entry by entry and as a
  measure, with no point on a loaded line:
  [`receipts/n76_cover_audit.json`](receipts/n76_cover_audit.json). The segments lie on
  the lines $x, y \in \{0, 1, \dots, 9\}$ with lengths $1/500$ (2,104), $1/50$ (5,976)
  and $1/16$ (1,664). Sixteen of them lie on the container’s walls, with mass
  $1/(4 \cdot 10^8)$ each.
- **The Lean data.** Every point and segment of `S76T_Pts.lean` matches the cover file
  as `mk_s76_lean.py` says it aggregates them, the total is the same, and `S76Cover` is
  stated over centres in $[0, 9/2]^2$ and $u \in [0, 1/2]$. The Lean was not built.
- **The corners.** The cover’s corner $[0, 5/2)^2$ is wand125’s $s(59) = 8$ cover’s,
  1,140 points and 452 segments with identical masses, as the source credits; that cover
  is retained in the
  [October 1 wand125 packet](../wand125-point-and-mixed-2026-10-01/README.md).
- **The `zmx2` sweep.** `zmx2` built from the retained `6b7f0f79` source
  ([`receipts/n76_zmx2_build.log`](receipts/n76_zmx2_build.log)) ran `cert --d4` over
  all 8,100 roots ([`receipts/n76_zmx2_d4.log`](receipts/n76_zmx2_d4.log), root log
  `n76_zmx2_d4_roots.log.gz`): 147 s wall and 239 CPU-s, 14,672,104 boxes and 18
  uncertified in the same four roots. Every root’s census and all 18 uncertified boxes
  equal the source’s `zmx2_v5.log` line for line.
- **The `zm_mixed.py` sub-roots.** The retained checker files, digests checked, ran the
  64 jobs of `jobs.txt` with the flags `verify.sh` uses, three at a time
  ([`receipts/n76_zm_mixed/`](receipts/n76_zm_mixed/)): each prints
  `VERIFIED-D4 (PARTIAL)`, 4,950 boxes in all, maximum depth 15, none uncertified, 1,168
  CPU-s. Every record equals the source’s apart from the input path and CPU time. Read
  with exact fractions, the 64 cells are distinct cells of the $1/20$ grid and tile the
  four failing roots exactly, and the author’s `check_coverage.py` accepts the replay’s
  own logs.
- **Controls.** The `drop-heaviest-point` and `drop-heaviest-segment` mutations of
  `devtools.replay_evand_zmx2.mutate` are refused by `zmx2` at one root each
  ([`receipts/controls/`](receipts/controls/)), and `zm_mixed.py pose` finds a pose
  where each captures less than one, exactly ($0.99736$ and $0.89682$), where the
  published cover captures $1.00993$ and $1.00726$. No `zm_mixed.py` sweep of a
  mutation was run: refusal at depth 24 is not affordable.
- **The wall segments.** No closed unit square in $[0,9]^2$ needs mass on the container’s
  walls: a square flush with a wall is the limit of squares moved off it, each capturing
  at least one, and in the limit that mass lies off the wall. None of the five other
  covers in Daniel’s format that this repository retains ($s(21)$, $s(45)$, $s(59)$,
  $s(60)$, $s(77)$) has a wall segment, so `zmx2 cert --d4` was run again on the cover
  without them
  ([`receipts/controls/n76_control_nowall_zmx2_d4.log`](receipts/controls/n76_control_nowall_zmx2_d4.log)):
  all 8,100 roots have the census of the published cover’s replay, box for box, and the
  same 18 boxes are left. No `zmx2` decision depends on them.

[`receipts/n76_triage_checks.log`](receipts/n76_triage_checks.log) re-runs every
comparison above from this packet’s retained bytes and receipts, by
[`receipts/programs/triage_checks.sh`](receipts/programs/triage_checks.sh); the programs
it calls, and the scripts that made the checker receipts, are in
[`receipts/programs/`](receipts/programs/). The run scripts name the scratch paths they
ran in, which the receipts repeat.

## Limitations

- **One implementation per cell.** Each cell of the D4 region is decided by one of
  Daniel’s checkers, run here from the bytes the source pins; no checker of this
  repository decides a mixed cover, so this is a reproduction with the producer’s code,
  not a second implementation.
- **`zm_mixed.py` has not confirmed a result here before.** Its partial-region options
  and the composite of its records with a `zmx2` root set are new to this record, and are
  the review’s to read.
- **The Lean is unbuilt and its library unretained.** `Sqpack` at `1718a58` is not in
  any packet, and `S76Cover` is a hypothesis.
- **The full `zm_mixed.py` pass is not at this revision**, and neither is a `zmx2 --full`
  sweep.

## Original Gzip Files

The three upstream files whose own names end in `.gz` are retained as published, never
recompressed. The table binds their compressed bytes: the Git blob and SHA-256 of each
stored file, which are its blob at the pinned commit and the digest the source’s
`SHA256SUMS` lists.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `s76-certificate/cover/s76_cover_v5.txt.gz` | upstream | `cfc1c97c8d991f4561830d68010a9465df6f1b79` | `d6a1c6bb6b63ab71740984c7f48f3e51c757d89444b16125c05bffe9b9ce4416` |
| `s76-certificate/lean/S76T_Pts.lean.gz` | upstream | `fb7f5dbd4d8b7377a7a727c5eead76a2a34f624f` | `f6c3f30ec2641417fb4f9455bf8a384fd96c4cd13e3633bc8a74612e8c32e045` |
| `s76-certificate/records/zmx2/zmx2_v5.log.gz` | upstream | `2632c2dfb1068d921c6857aae361b6d7ea9196cd` | `9794cf5b0dd21411363d95b5dbf9f453a16220c5ceb935dd12025177d5eb3ad9` |

## Compressed Files

Two receipts of more than 1,000 lines, the `zmx2` root logs of the replay and of the
wall control, are stored as deterministic gzip made by `gzip -9n`, with no file name or
timestamp in the header. The table gives the Git blob and SHA-256 of the decompressed
bytes, and `python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/n76_zmx2_d4_roots.log.gz` | receipt | `821e9db8a5d76b742fa65438b5ac77a2a2b0e12c` | `e3c878e0b6d07ef238655931e72873d23e6123f0a6c8304a60cc1590d51cf6f4` |
| `receipts/controls/n76_control_nowall_zmx2_d4_roots.log.gz` | receipt | `1af58c240def4590216145a2d412ffb32c5a736d` | `12f4a5488a1b2b1f726f968307c6dac4223b54187ad54e073d19db1973a6cc76` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
