# Evan Daniel’s s(154) Certificate

[Issue #552](https://github.com/jlevy/squares/issues/552) reports an exact rational
packing of 154 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/597e660c9a078a552991ab893cda3ab693cb5ac8/search/packer/candidates).
The packet pins the commit the issue names,
`597e660c9a078a552991ab893cda3ab693cb5ac8` (tree
`a52316fa7075147cb9e486d8d7063caa643683ec`, committed 2026-10-12T13:58:36Z), which adds
the six n = 154 files and the packer log’s submission entry.
The branch head when the sources were retrieved, `31523f8` (13:59:32Z), adds one line to
the packer log and nothing else.
The issue was filed at 2026-10-12T13:59:25Z, and the sources were retrieved at
2026-10-12T14:38Z.

| n | Exact side of the certificate | The issue prints | Rounded up at 16 places |
| --- | --- | --- | --- |
| 154 | `12922566401934059503377267965457/1000000000000000000000000000000` | `12922566401934059503377267965457 / 10^30` | 12.9225664019340596 |

The certificate, `tt_n154.cert`, gives 154 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side. It uses the format
of issues #375, #399, #465 and #489.
Its side is the 80-digit KKT point $S^\ast$ of `tt_n154.exact.txt` scaled by
$1 + 10^{-20}$ about the origin corner, rounded up at 30 places, as the issue says.
The commit also holds a regularized drawing of the same packing,
`tt_n154_regularized.cert`, at the same side.
The issue says the claim rests on `tt_n154.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
13 files, 313,527 bytes.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/tt_n154.cert` | `854d41a1ccef74826c4bf5e28444926117b7fb9d` | 24700 | `06985d5fd506a29d534b8b8c60d872139921205070794f1681f843733e5610df` |
| `search/packer/candidates/tt_n154_regularized.cert` | `d69a06840b022f34a7b5a6704207296a635af7da` | 23863 | `02ad1b81a1a68f7bd9232c1aa6bcfbb264f89f843e50b4dbc0d78c892aaa6612` |

Beside the two certificates the packet retains the KKT point (`tt_n154.exact.txt`), the
binary64 packing it was solved from (`tt_n154.input.txt`), the solver’s report
(`tt_n154.json`) and the regularizer’s report (`tt_n154_regularized.json`), with
`LICENSE`, `CREDITS.md` and `search/exact/README.md`: 9 files and 137,477 bytes.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest only. They are byte-identical to the copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run. The packer’s working log, `search/packer/PACKER.md` (166,630 bytes), and the
time-travel test’s report script, `search/packer/timetravel.py`, are pinned by digest
only.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the issue-399, issue-465 and issue-489 imports
did. The two routes are `sqpack`’s exact witness verifier and the independent rational
corner checker. Each decides every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion.
The count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

The positive passes both routes, and both routes refuse both controls, each on the
overlap or the wall it was built to break.
The two routes find the same least wall clearance, exactly `1/200000000000000000000`
($5 \times 10^{-21}$), and the same least pair gap, just under $10^{-20}$, as the issue
states.
The 3 jobs made 70,686 pair decisions in 40.97 route CPU seconds and 80.68 job wall
seconds, summed; the longest job took 29.49 seconds.
`certify --workers 1` took 91 seconds of wall time, with other lanes holding the
four-core machine at a load average of about 13 to 17.
A fresh `check --replay` decided all 3 jobs again, equal to the retained rows apart from
timing, in 75 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method.
The third exact route, `devtools.check_half_angle_area decide-imports`, has no roster
line for this import yet. Run once from scratch with the line added in that process
alone, it accepts the certificate and reaches the required outcome on all six of its
controls. It finds the same least wall clearance and a least Euclidean distance between
squares of $1.00 \times 10^{-20}$, holds the retained bytes to the pin, and reports no
disagreement, in 41 seconds.
The regularized drawing was decided the same way, outside any receipt: the positive
passes all three routes with the same clearances, and every control is refused.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record as it stood when the issue was read: local branch `layer6` at `92649a2eb`, which
carries the 2026-10-11 adoption layer and the records to `T-155` as that branch numbered
them; its `T-153` to `T-155` are `T-157` to `T-159` since the merge with main, where
`T-153` to `T-156` name other results.
`check-claims` rebuilds the case ceiling and every other side from its own retained
packet:

| Report at 154 | Holder | Exact side | This certificate is below it by |
| --- | --- | --- | --- |
| `T-136`, the case ceiling on `layer6` | Nate Chaoweeraprasit (itsnaka), SQUISH | 12.9230702023011407… | $5.04 \times 10^{-4}$ |
| `T-127` (#438), the case ceiling on `main` (`4a4910524`) | itsnaka, improved by Siddharth Gupta | 12.9265622458523469… | $4.00 \times 10^{-3}$ |
| #470 | Mishapolk | 12.926562245853 | $4.00 \times 10^{-3}$ |
| `T-115` (#401) | Nate Chaoweeraprasit | 12.9265622458535389… | $4.00 \times 10^{-3}$ |
| `T-113` (#401) | Nate Chaoweeraprasit | 12.9282936576777576… | $5.73 \times 10^{-3}$ |
| `T-098` (#375) | Francisco Couzo, improved by Evan Daniel | 12.9316637211668470… | $9.10 \times 10^{-3}$ |
| `T-056` | Francisco Couzo | prints 12.931663721169976 | $9.10 \times 10^{-3}$ |

The certificate is below every report the record holds or has pending at 154.
No other open issue reports a packing of 154 squares, and no report of the 2026-10-11
stack layers (`T-147` to `T-152`, and `T-157` to `T-159`) is at 154.

## Lineage

The issue says the packing came from a test of the author’s size-chaining explorer, the
quality-diversity basin explorer of #465 and #489, restarted from the register of 5
October. Its comment of 14:13 UTC traces the run round by round and says the packing
descends from Francisco Couzo’s 5 October packing of 155 squares with one square removed,
after 17 productive rounds at n = 154.
The chain never saw SQUISH’s packing.
The tracing script the comment names, `search/packer/chain_lineage.py`, is not in the
tree at the pin or at `31523f8`.

Measured here with the third route’s own credit tools, `arrangement_gap` and
`patch_lineage`, called from scratch:

- **T-136.** No symmetry of the box matches the two packings one to one by nearest
  centre. Under the best placement `patch_lineage` finds, 32 of T-136’s squares land
  within $10^{-9}$ of a square of this packing, and one of them to the digit. This is
  another arrangement than T-136’s, not a refinement of it.
- **Couzo’s 154 and 155** (T-098’s exact optima of the 5 October packings). The 154 does
  not match this packing one to one either. Blocks of upright squares reappear to the
  digit from both: 43 squares of the 155 under one translation, and 45 of the 154.
  That measurement cannot tell the two starts apart.
  The source’s own matching distances, 0.319 per square from T-136’s packing and 0.396
  from the 5 October packing, are its statements and were not replayed.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that $S^\ast$ is a KKT point with positive multipliers on its
load-bearing contacts, the smallest $1.5 \times 10^{-4}$. It states that the reduced
Hessian is positive semidefinite modulo 45 exact flat motions, and that a first-order
MILP finds the packing jammed in all 98 corner-to-corner branches; it has 8 rattlers.
Those are numerical evidence, as the source says, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.

The regularized drawing has the same exact side.
Square by square it keeps 112 of the 154 poses and moves 42, the largest by 0.135; every
moved square is a rattler or one of the solver report’s flat squares, and only the 8
rattlers turn. The regularizer’s report lists no angle changes.
It is the source’s display view and is not a separate claim.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`. Its commits disclose Claude (Anthropic) as co-author, and the issue states
that the search code, the run and the request were done with Claude (Claude Code), which
Evan Daniel directed and reviewed.
The issue asks that the start be credited to Francisco Couzo’s packings, and its comment
narrows that to his 5 October packing of 155 squares.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n154-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-2026-10-12 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-2026-10-12 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
