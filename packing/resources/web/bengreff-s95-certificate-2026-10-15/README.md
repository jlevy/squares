# Benjamin Greff’s Certificate for s(95) = 10, Pinned 2026-10-15

This packet pins the whole of
[bengreff/s95-certificate](https://github.com/bengreff/s95-certificate) at its head of 15
October 2026, for one registration request:
[jlevy/squares#610](https://github.com/jlevy/squares/issues/610), opened by Benjamin
Greff (`bengreff`) at 2026-10-15T01:16:36Z, which reports $s(95) = 10$, the case
$k = 10$ of the $k^2 - 5$ series. The upper half is the $10 \times 10$ grid; the new
claim is the lower bound $s(95) \ge 10$, by a mixed cover in Evan Daniel’s format decided
by two of Daniel’s checkers. When it was retrieved the record held $s(95)$ open at
$1993/200 = 9.965$ (wand125, [`n-095.md`](../../../frontier/n-095.md)).

It is the author’s second case by this pipeline, one size up from $s(76) = 9$
([#594](https://github.com/jlevy/squares/issues/594), T-184, retained in the
[14 October packet](../bengreff-s76-certificate-2026-10-14/README.md)), and this packet
follows that one’s import step for step.

Its proposed Frontier key is **[bengreff s95 certificate 2026-10-15]**. The claim below
is stated as the source states it. What was checked here at retention is in
[Checks Made Here](#checks-made-here); none of it is a review, and nothing here registers
the result. The register entries the records lane would apply are drafted in
[`register-plan.yaml`](register-plan.yaml); the records lane of 15 October applied them,
registering the result as T-191 at V0/C0 and adding T-081’s sentence on 96. The case
record at 95 is unchanged until a review.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/bengreff/s95-certificate> |
| Revision | `dd7297d06adc664268c65005369b895e4ded7547`, branch `main`, tree `53bf09b90398e46842dd7a758a60390d66acf1ca`: the revision #610 names, and the head of `main` when retrieved |
| Committed | 2026-10-15T01:16:20Z, 20:16:20 on 14 October by the author’s clock (`-05:00`) |
| History | Two commits by Benjamin Greff, both on 15 October (UTC), each with a `Co-Authored-By: Claude Opus 5.5` trailer. The first, `06da947115f20158779dcf041adcee35d8d8bbb2` at 01:10:26Z, adds the cover, the run records, the Lean wrapper and `verify.sh`; the second touches only `README.md` (the clean-replay time) and `SHA256SUMS` |
| Licence | MIT, “Copyright (c) 2026 Benjamin Greff” (`LICENSE`) |
| Retrieved | 2026-10-15T01:29Z: a full clone of `main` |
| Pinned subtree | The whole tree: 635 files, 1,871,783 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | All 635 files, byte-identical at their upstream paths under [`s95-certificate/`](s95-certificate/). The three upstream `.gz` files are kept as published ([Original Gzip Files](#original-gzip-files)) |
| Source checksums | The tree’s own `SHA256SUMS` lists the other 634 files, and `sha256sum -c SHA256SUMS` passes on the retained copy |

Evan Daniel’s checkers are not in the tree. The source’s `verify.sh` fetches them from
evand/square-packing at `b91d70b6ed314624c1434b628a9c7bf9a132c743` and checks their
digests, the same four as for $s(76)$; this repository already retains all four byte for
byte: `s12/verify2/src/bin/zmx2.rs` (`6b7f0f79…`), `s12/search/zm_mixed.py`
(`ee3e2915…`) and `s12/search/mixed_cover.py` (`bb89de15…`) in the
[September 28 evand packet](../evand-square-packing-2026-09-28/README.md), and
`s12/search/zeromargin.py` (`640fe453…`) with `verify2/Cargo.toml`, `Cargo.lock` and
`src/main.rs` in the [September 26 packet](../evand-square-packing-2026-09-26/README.md).
The Lean wrapper builds on Daniel’s `Sqpack` at evand/square-packing `1718a58`, which no
packet here retains.

## Credit and AI Assistance, as the Source States Them

The README’s Credits section names Evan Daniel (evand/square-packing, MIT) for “the
weighted-cover method at margin zero, the mixed format, the checkers `zmx2`,
`zm_mixed.py` and `zeromargin.py`, and the Lean library”, and wand125
(wand125/square-packing, MIT) for “the s(59) = 8 cover reused for the corners, and the
band-insertion construction”. It ends: “**Benjamin Greff** directed the work. The
search, LP and verification pipeline were built and run with Claude (Anthropic) as an AI
assistant.”

The issue’s “Lineage and credit” names the same two, says the corners $[0, 2.5)^2$ and
their images are wand125’s $s(59) = 8$ cover unchanged with a band of width 2 inserted at
$x = 4$ and $y = 4$, and claims as the author’s own the cross
$\{x \text{ or } y \in [2.5, 7.5]\}$, re-optimised by LP with #594’s settings except a
row margin of 0.006. Under “AI assistance” it says: “Yes, extensively. I chose the problem
and the standard of proof, and directed the work. Claude (Anthropic), working as an agent
in Claude Code, built and ran the LP search, the GPU solver, the export, the verification
script, the coverage checks, the Lean wrapper and the replay, and drafted this
write-up.” Both commits carry a `Co-Authored-By: Claude Opus 5.5` trailer. The issue
says there has been no review outside the author’s project.

Neither the tree nor the issue credits this project; the issue cites
[`n-095.md`](../../../frontier/n-095.md) for the standing bound.

## What Is Retained

Everything at the pinned revision, under [`s95-certificate/`](s95-certificate/):

- **`cover/s95_cover_v2.txt.gz`**, the certificate: unpacked, 1,160,654 bytes with
  SHA-256 `8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c`, the digest
  the issue and the README state.
- **`records/`**: the `zmx2` sweep’s per-root log (`zmx2/zmx2_s95_v2.log.gz`) and summary
  (`zmx2_s95_v2.out`), the 19 roots it leaves (`zmx2/failing_roots.txt`), the 304
  `zm_mixed.py` sub-root records with their jobs list and log tails (`zm_mixed/`), and the
  toolchain of the source’s runs (`toolchain.txt`).
- **`tools/`**: `check_total.py` and `check_coverage.py`, the author’s two
  standard-library scripts for the total and for the tiling of the pieces, the #594
  scripts with the side as a parameter; and `check_full.py`, for the records of a full
  `zm_mixed.py` pass, which this revision does not hold.
- **`lean/`**: `S95Lower.lean`, the generated data `S95T_Pts.lean.gz`, its generator
  `mk_lean.py` and `build_summary.txt`.
- **`verify.sh`**, `README.md`, `LICENSE` and `SHA256SUMS`.
- **`construction/`**: the LP search code, the GPU interior-point solver, the export, the
  excluded points and the two coincidence finders, which the source calls research code
  not needed to check the proof.

Nothing is pinned by digest alone.
[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
[`acquisition/sources.json`](acquisition/sources.json) records the pin. From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  bengreff-s95-certificate-2026-10-15 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## The Claim, as the Source States It

| Claim | Certificate | Total | Checks the source reports |
| --- | --- | --- | --- |
| $s(95) \ge 10$, so $s(95) = 10$ with the grid | 48,352 weighted points and 11,438 axis-parallel segments of $[0,10]^2$ in Daniel’s `mixed 1` format, coordinates $X/8000$, weights $w/(4 \cdot 10^8)$, exactly D4-invariant | $3791753447/40000000 = 94.793836175 < 95$ | `zmx2 cert --d4` over 10,000 roots, 15,065,314 boxes, 19 roots left with 8,263 uncertified boxes, none capped (309 CPU-s); `zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24` on the 304 sub-roots of those 19, 9,614 boxes, maximum depth 13, none uncertified (2,771 CPU-s); `check_coverage.py` for the tiling |

The argument is #594’s at side 10: the measure is a point-and-segment mass on
$[0,10]^2$ with total below 95, such that every closed unit square in $[0,10]^2$, at any
position and angle, captures mass at least one, boundary included. A packing of 95 unit
squares at a side below 10, scaled up to side 10, would hold 95 pairwise disjoint closed
unit squares capturing mass at least 95. By the exact D4 invariance the covering
statement needs only centres in $[0, 5]^2$ and $u = \tan(\theta/2) \in [0, 1/2]$. Its two
checkers split that region: `zmx2`, in outward-rounded binary64, decides 9,981 of its
10,000 root cells of $1/10 \times 1/10 \times 1/8$, and `zm_mixed.py`, in exact
rationals, decides the 304 cells of $1/20 \times 1/20 \times 1/32$ that tile the other
19\. No cell rests on both.

`lean/S95Lower.lean` proves `theorem s95_eq_10 (hcov : S95Cover) : minSide 95 = 10` on
Daniel’s `Sqpack` at `1718a58` (Lean v4.33.1), with axioms `propext`, `Classical.choice`
and `Quot.sound`, built in 20 min 35 s with a peak of 25 GB by `build_summary.txt`. The
data facts are kernel-checked (`pts_nodup`, `pts_d4`, `segs_d4`, `wsum_lt`); `S95Cover`,
the covering statement on the D4 region, is a hypothesis, not proved in Lean.

The issue says no full `zm_mixed.py` pass over all 160,000 D4 roots has been run (for
$s(76)$ it took 181 CPU-hours), and offers to run one. It names $s(116) = 11$ as the
author’s next target. It also gives two notes for others: a second kind of exact
coincidence, at $\theta = \arctan(1/5)$, which `zm_mixed.py` cannot close at any depth
and which the construction removed by excluding the atoms within $6 \cdot 10^{-4}$ of
those edges; and a mixed-precision GPU interior-point solver for the LP, with the warning
that CuPy’s sparse product returns wrong results without warning on this $A^T D A$.

## Checks Made Here

These were made on 15 October 2026 for the import’s triage, on a shared four-core x86-64
Linux container with other lanes’ processes running, with Python 3.14.7 and rustc
1.97.0, one checker process at a time and one thread or worker each. Each checker run
below has its receipt under [`receipts/`](receipts/), written by
`devtools.replay_receipt`. The comparisons and premise checks were made by triage
diagnostics in [`receipts/programs/`](receipts/programs/), #594’s with the count and side
as arguments; registering cases 76 and 95 in `devtools.replay_evand_zmx2` and
`devtools.audit_evand_mixed_covers` is the tooling slice both imports owe.

- **Data facts.** The repository’s `devtools.audit_evand_mixed_covers.audit_cover`
  recomputes the cover’s total, counts and exact D4 invariance, entry by entry and as a
  measure, with no point on a loaded line, in 0.6 s:
  [`receipts/n95_cover_audit.json`](receipts/n95_cover_audit.json). `zmx2 d4` agrees
  ([`receipts/n95_zmx2_d4_invariance.log`](receipts/n95_zmx2_d4_invariance.log)), and so
  does the author’s `check_total.py`, read and then run with `-I` from scratch. The
  segments lie on the lines $x, y \in \{0, 1, \dots, 10\}$ with lengths $1/500$ (3,222),
  $1/50$ (5,976) and $1/16$ (2,240).
- **The wall segments.** 404 segments lie on the container’s walls, 101 per wall, each
  of length $1/500$ and mass $1/(4 \cdot 10^8)$, centred on the $1/20$-lattice points
  from $5/2$ to $15/2$: $101/10^8$ in all. They are the pattern the author explained on
  #594 for that cover’s sixteen, an LP candidate for every lattice point on an integer
  line rounded up to one unit, here at every such point of the cross.
- **The Lean data.** Every point and segment of `S95T_Pts.lean` matches the cover file
  as `mk_lean.py` says it aggregates them, the total is the same, the data facts carry
  this cover’s constants, and `S95Cover` is stated over centres in $[0, 5]^2$ and
  $u \in [0, 1/2]$. The Lean was not built. Its doc comment calls the hypothesis
  `S76Cover`, a name left in `mk_lean.py`’s template; the definition is `S95Cover`.
- **The corners.** The cover’s corner $[0, 5/2)^2$ is wand125’s $s(59) = 8$ cover’s,
  1,140 points and 452 segments with identical masses, as the source credits; that cover
  is retained in the
  [October 1 wand125 packet](../wand125-point-and-mixed-2026-10-01/README.md).
- **The `zmx2` sweep.** `zmx2` built from the retained `6b7f0f79` source
  ([`receipts/n95_zmx2_build.log`](receipts/n95_zmx2_build.log), binary `cba78a9e…`, the
  one #594’s triage built) ran `cert --d4` over all 10,000 roots on one thread
  ([`receipts/n95_zmx2_d4.log`](receipts/n95_zmx2_d4.log), root log
  `n95_zmx2_d4_roots.log.gz`): 305 s wall and 293 CPU-s, 15,065,314 boxes and 8,263
  uncertified in the same 19 roots, none capped. Every root’s census and all 111
  uncertified boxes the log lists equal the source’s `zmx2_s95_v2.log` line for line. One
  root, centres $[3/2, 8/5] \times [47/10, 24/5]$ and $u \in [0, 1/8]$, holds 8,192 of
  the 8,263.
- **The `zm_mixed.py` sub-roots.** The retained checker files, digests checked, ran all
  304 jobs of `jobs.txt` with the flags `verify.sh` uses, one at a time
  ([`receipts/n95_zm_mixed/`](receipts/n95_zm_mixed/)). They ran in two parts. First, a
  sample of 14 priced the rest (`jobs_sample.txt`, chosen by `zm_sample.py` as the four
  costliest by the source’s records, every 38th job, and two cells at the centre in the
  $u$ bin of $\arctan(1/5)$): 254 CPU-s in 6 min 45 s wall. Then the other 290
  (`jobs_rest.txt`), from 02:01Z to 03:03Z, 62 minutes of wall on a host whose load
  reached 12 on four cores. Each prints `VERIFIED-D4 (PARTIAL)`: 9,614 boxes in all,
  maximum depth 13, none uncertified, 2,327 CPU-s by the checker’s own count (ratio
  0.840 to the source’s 2,771.3) and 3,278 CPU-s by the receipts, interpreter start-up
  and cover parsing included. Every record equals the source’s apart from the input
  path and CPU time.
- **The `zm_mixed.py` records, the source’s and the replay’s.** Read with exact
  fractions, each set of 304 records names the pinned checker and cover digests and the
  certificate-mode D4 settings, and is 304 distinct cells of the $1/20$ grid that tile
  the 19 failing roots exactly, none uncertified. The author’s `check_coverage.py`, read
  and then run with `-I` from scratch, accepts the source’s two records, and accepts the
  replay’s own `zmx2` log with the replay’s own `zm_mixed.py` records: the composite
  over the whole D4 region, reproduced here with the producer’s code.
- **Controls.** The `drop-heaviest-point` and `drop-heaviest-segment` mutations of
  `devtools.replay_evand_zmx2.mutate` are refused by `zmx2` at one root each
  ([`receipts/controls/`](receipts/controls/)), 235 and 234 boxes uncertified, where the
  published cover certifies those roots. `zm_mixed.py pose` finds a pose where each
  captures less than one, exactly ($0.99736$ and $0.84619$), where the published cover
  captures $1.00993$ and $1.01200$. The heaviest point is the corner atom of #594’s
  control; the heaviest segment lies on the centre line $y = 5$, $x \in [15/16, 1]$. No
  `zm_mixed.py` sweep of a mutation was run: refusal at depth 24 is not affordable.
- **The wall control.** No closed unit square in $[0,10]^2$ needs mass on the
  container’s walls: a square flush with a wall is the limit of squares moved off it,
  each capturing at least one, and in the limit that mass lies off the wall. `zmx2 cert
  --d4` was run again on the cover without its 404 wall segments
  ([`receipts/controls/n95_control_nowall_zmx2_d4.log`](receipts/controls/n95_control_nowall_zmx2_d4.log)):
  all 10,000 roots have the census of the published cover’s replay, box for box, and the
  same 19 roots and 111 listed boxes are left, in 293 s wall and 290 CPU-s. No `zmx2`
  decision depends on them.

[`receipts/n95_triage_checks.log`](receipts/n95_triage_checks.log) re-runs every
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
  and the composite of its records with a `zmx2` root set are new to the record since
  #594, and are the review’s to read.
- **The Lean is unbuilt and its library unretained.** `Sqpack` at `1718a58` is not in
  any packet, the source’s build needed 25 GB of memory, more than this host has, and
  `S95Cover` is a hypothesis. The build is held in bead think-ojr9.
- **The full `zm_mixed.py` pass is not at this revision**, about 190 CPU-hours here and
  held over the per-item cap (think-zn7s). Neither is a `zmx2 --full` sweep: about 6
  CPU-hours with its follow-up, priced in think-eucc and not run, since #594’s rungs
  did not ask for it. It is the route that does not rest on the D4 reduction, which
  T-066’s replay of $s(59)$ also ran.

## Original Gzip Files

The three upstream files whose own names end in `.gz` are retained as published, never
recompressed. The table binds their compressed bytes: the Git blob and SHA-256 of each
stored file, which are its blob at the pinned commit and the digest the source’s
`SHA256SUMS` lists.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `s95-certificate/cover/s95_cover_v2.txt.gz` | upstream | `3a6c45dcb84cac653dbad4f5ac805a749f133ae9` | `1f2a0361832e628be9b52fdfc88fd6d4f31c58d53e7584631e8caf310e973394` |
| `s95-certificate/lean/S95T_Pts.lean.gz` | upstream | `ac2cceea3aa798c1c849750f5e35e6ee6bca4985` | `2016456436cefa51ac7347002ced6bda9ff384310a0dea0cee5d4137cad7fafc` |
| `s95-certificate/records/zmx2/zmx2_s95_v2.log.gz` | upstream | `9d08457472a7ba789f28c77af2db401d53dce904` | `9c683c4f3070b89ba48468955f7eacd9daee21d2148b08d29188e37850c386a8` |

## Compressed Files

Two receipts of more than 1,000 lines, the `zmx2` root logs of the replay and of the
wall control, are stored as deterministic gzip made by `gzip -9n`, with no file name or
timestamp in the header. The table gives the Git blob and SHA-256 of the decompressed
bytes, and `python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/n95_zmx2_d4_roots.log.gz` | receipt | `0a8b50fa0de1f1ea8d2d42aded8bc0f5c428e471` | `fc3bb14daca8c06e521a81d75414236019cb48129f5b88c3645cc82c7d5a7b00` |
| `receipts/controls/n95_control_nowall_zmx2_d4_roots.log.gz` | receipt | `29ca18acb314218f00ef7ae2923dd9206bd49ffb` | `6d65cd860b55bee6e622825c21c2b4411fb72c4fde648101263e960e8c7007ad` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
