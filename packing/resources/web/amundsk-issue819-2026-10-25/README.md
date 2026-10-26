# Amund Kristiansen’s Certificate at 344

[Issue #819](https://github.com/jlevy/squares/issues/819), opened 2026-10-25T19:05:14Z
by amundsk, reports one upper bound beyond the case corpus, credited to Amund
Kristiansen, in the gist
[amundsk/18ada41ec384b6ff2c96f58b7ce7d1a6](https://gist.github.com/amundsk/18ada41ec384b6ff2c96f58b7ce7d1a6/f916f69f0ae570935991440712a08ad930469da3).
The packet pins the revision the issue names, `f916f69f0ae570935991440712a08ad930469da3`
(tree `17d88948244316f1b4623d5d7b2ff91bd0d087c5`, committed 2026-10-25T19:04:50Z), 24
seconds before the issue.
It is the gist’s only revision and was its head when read at 02:35Z on 26 October; the
issue had no comments.

The certificate, `s344_amund.cert`, gives 344 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in Evan Daniel’s
format, the format of #798’s certificates.
The issue says it is a dilation certificate made with Daniel’s
`search/packer/dilate_cert.py` at evand/square-packing `7982d7a`, on macOS arm64 with
Python 3.14.6, from the binary64 packing beside it, `s344_amund.input.txt`: centres and
box scaled by $1 + 10^{-12}$, coordinates rounded to rationals and each angle rounded to a
rational half-angle tangent, so every square is exactly unit.

| n | The issue prints, rounded up | Exact side rounded up at 16 places | Disposition |
| ---: | --- | --- | --- |
| 344 | 18.992567544845 | 18.9925675448442776 | row |

The exact side is the certificate’s header,
$9496283772422138783772412642309/500000000000000000000000000000$, which the issue prints
as S′; [acquisition/claims.json](acquisition/claims.json) keeps it.

## What the Issue Reports

- **Credit name.** “Amund Kristiansen (GitHub @amundsk)”. The gist’s README says the
  same: “(Amund Kristiansen, 2026-10-25)”.
- **Claim.** One upper bound, the certificate’s exact side rounded up at 12 places,
  $1.60 \times 10^{-4}$ below Francisco Couzo’s `certificates/best/n344.cert` at
  `1c17153`, 18.992727809347, which the issue says is the same as `964ee2b`’s (#763).
  It compared Couzo’s index at `1c17153` and the register’s other sources at 344 (Kevin
  Fang’s two-wedge certificates, Daniel’s record hunt 3, Couzo’s certificates of 11
  October), all higher, and found no request since #798 at 344.
- **Digests.** It prints the SHA-256 of the certificate (`4e2c6880…6e21`) and of the
  binary64 input (`32cd4883…33e5`); both are the digests of the pinned files, each
  downloaded into an empty directory and checked on 26 October.
- **Checks.** The author reports that Daniel’s two exact checkers at `7982d7a`,
  `verify_cert.py` (separating axes) and `verify_cert2.py` (polygon intersection), accept
  the certificate, with least wall clearance $6.054 \times 10^{-13}$, least pair separation
  $1.215 \times 10^{-12}$ and 794 close pairs, re-checked on the file downloaded from the
  gist, and that no full line of 19 upright squares occurs. The issue says the two
  checkers share an author and the certificate format, which also made the certificate.
  No source program ran here.
- **Not done.** No exact KKT solve, rigidity or local-optimality analysis; only the upper
  bound is claimed.
- **Method and lineage.** A new packing of another lineage than Couzo’s: the register’s
  307 record design (Nate Chaoweeraprasit (itsnaka) / PingYou Ltd, PR #574; a 6+6
  two-band family-A packing) stretched one K-step, by one upright column and one band
  square in each bottom-band row and one upright row and one band square in each left-band
  column, keeping deficit 17; started from 307 minima of that design and polished in
  float32 GPU batches of kicked variants with Daniel’s `fq` quench in 64-bit.
  Matched one to one with Couzo’s 344 by an optimal assignment over the eight symmetries,
  the issue counts a largest move of 0.993, 67 squares beyond 0.1 and 122 beyond 0.01, and
  114 tilted squares against 125.
- **AI assistance.** “Yes. As at #755 and #798: the search, the certificate and this
  report were done by Claude (Anthropic), working in Claude Code at my direction, using
  Evan Daniel’s open-source engine and checkers.”

[acquisition/issue.json](acquisition/issue.json) keeps the issue as read at 02:33Z on 26
October: never edited and no comments.

## Source Custody

The gist’s README and the issue both dedicate the certificate, the input packing and the
README to the public domain under CC0 1.0, so the packet retains all 3 files.

`devtools.acquire_source` wrote the packet from a blobless clone of the gist checked out
at the pin, from [acquisition/declaration.json](acquisition/declaration.json);
[acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Its scope is the gist’s 3 files, 72,754 bytes, each retained under [source/](source/)
and bound to its Git blob at the pin: the certificate (53,584 bytes), the binary64 input
(18,333 bytes) and the README (837 bytes).
No file is stored compressed.

The tools the issue names are Daniel’s, at `7982d7a`, which the
[#728 packet](../evand-n303-2026-10-22/README.md) read; that packet and the
[n229 packet](../evand-n229-dilation-2026-10-17/README.md) pin `verify_cert.py`,
`verify_cert2.py` and `dilate_cert.py` by digest. They were not run.

## Report Order

The [ledger of 26 October for issue 819](../../../campaign/issue-intake/upper-bounds-issue819-20261026/README.md)
walks the count from a start frozen at `main` `5c50803d6` (#807’s merge): the row of
`couzo-964ee2b-2026-10-23`, 18.992727809347, with Göbel’s construction beside it.
Nothing reached 344 between `964ee2b`’s push and the issue.
franciscouzo/square-packing’s head is still `1c17153`, whose
`certificates/best/n344.cert` is `964ee2b`’s byte for byte (SHA-256 `40c0540a…deb9`, the
digest the [#763 packet](../couzo-issue763-2026-10-23/README.md) records), and
evand/square-packing at `d99925d`, Mishapolk/square-packing-records at `7e82c64` and
TheSnakeFang/squarepack-certs at `db1ed62` are unchanged since their last reads.
No issue or pull request from #798 to #821 states a bound at 344.

- **One row.** The certificate is below every earlier report at 344: by
  $1.6026 \times 10^{-4}$ below the side of Couzo’s certificate, exactly, and by
  $0.1998$ below Göbel’s construction (the Göbel square of 349, less 5 of its squares).
  It supersedes `couzo-964ee2b-2026-10-23`’s row there.
- **No restatement.** The margin is far above one unit in the 12th place.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `5c50803d6` (26 October 2026): the grid, Göbel’s construction
(`devtools.goebel_construction`) and the count’s current beyond-horizon row at its print.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the requested count, the record `check_source_coverage` reads the row against.
`check-claims` rebuilds both.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as #798’s did: `sqpack`’s exact witness verifier and
the independent rational corner checker (`devtools.check_rational_witness_independent`),
each deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle
conversion.
It ran a positive job, a duplicate-square control and an outside-container control, each
in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
Both routes find the clearances the issue prints: every wall by at least
$6.054 \times 10^{-13}$ and every pair by at least $1.215 \times 10^{-12}$, as a
$10^{-12}$ dilation gives.
The 3 jobs made 353,976 pair decisions in 102.72 route CPU seconds and 107.71 job wall
seconds, summed; the longest job took 36.9 seconds.
`certify --workers 2` took 74 seconds of wall time on 26 October 2026, under `nice` on a
four-core host shared with other lanes at a load average of about 4, and
`check --replay` decided the receipt again in 105 seconds on one process.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

**Sharp controls.** The receipt’s controls are gross, so `sharp-controls`
(`devtools.upper_bound_sharp_controls`) takes the certificate to exact contact and
$10^{-30}$ past it on both routes: the side lowered by its least far-wall clearance, the
tightest pair closed along the face normal that separates it, every square moved toward
its near wall, one square of a tight pair and the square nearest a wall enlarged, and a
duplicated square. All 11 controls come out on both routes as the module’s rules require:
at contact a moved square or side is accepted with the decisive margin exactly 0 and an
enlarged square is refused for its shape alone, past contact every one is refused by the
margin the rules set, and the duplicate is refused.
They took 386 CPU seconds, 476 seconds of wall time on one process, and
`sharp-controls --check` decided them again in 416 seconds.
[receipts/sharp-controls.json](receipts/sharp-controls.json) keeps the verdicts.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and no source program ran here.

## Pose by Pose

[measure/identity-n344.json](measure/identity-n344.json), written by
`devtools.measure_identity`, measures the packing against `964ee2b`’s at the count, the
packing the issue compares it with. A measurement, which decides nothing:

- **No pairing by nearest centres.** No symmetry of the box matches the two packings
  square for square.
- **The optimal assignment.** Best under symmetry 5 of the box’s eight, the largest move
  is 0.993, as the issue says, but 82 squares move beyond 0.1 and 137 beyond $10^{-2}$,
  where the issue counts 67 and 122. The issue does not say how it aligned the two boxes,
  and either count makes the packing another arrangement, not a refinement.
- **Tilts.** 114 squares are tilted beyond a degree against 125 in Couzo’s packing, the
  issue’s figures; 24 tilted squares pair with tilts of the opposite sign, 90 with upright
  squares, and no tilt angle is shared within $10^{-4}$ degrees.

The issue’s account of the lineage, the 307 design stretched one step, is the author’s
statement; nothing here measures it, since the 307 packing has another count.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The issue claims no local optimality, KKT condition or rigidity, and none was examined.
Novelty, local or global optimality and rigidity are not established.

## Credit

The issue and the gist’s README credit Amund Kristiansen (GitHub @amundsk).
The issue says the search stretched the register’s 307 record design, Nate
Chaoweeraprasit’s (itsnaka) with PingYou Ltd’s certificate (PR #574), and used Evan
Daniel’s `fq` quench, `dilate_cert.py` and checkers.
The bibliography credit therefore reads
`Kristiansen after Chaoweeraprasit, PingYou Ltd, Daniel, Levy`, keeping the project link
([attribution.md](../../../../attribution.md#credit-text-and-lineage)).
Per-row credit beyond the horizon stays the owner’s open question from #686.
The search, the certificate and the report were done by Claude (Anthropic) in Claude Code
at the author’s direction, as the issue discloses.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source amundsk-issue819-2026-10-25 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue819-2026-10-25 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue819-2026-10-25 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue819-2026-10-25 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-issue819-2026-10-25 sharp-controls --check
uv run --frozen --all-extras --group dev python -m devtools.intake_ledger check campaign/issue-intake/upper-bounds-issue819-20261026
```

`check` admits the receipt structurally; only `--replay` decides the geometry again, and
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job directory.
`measure/identity-n344.json` is written by `devtools.measure_identity` and names its
inputs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
