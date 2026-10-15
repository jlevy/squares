# Evan Daniel’s s(146) Certificate

[Issue #606](https://github.com/jlevy/squares/issues/606) reports an exact rational
packing of 146 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/e006ce6230f2240457b083199755a3a5d287692c/search/packer/candidates).
The packet pins the commit the issue names,
`e006ce6230f2240457b083199755a3a5d287692c` (tree
`544367ecc88089d90c74bc963a891ba29fd2965f`, committed 2026-10-14T21:50:35Z), which adds
the seven n = 146 files.
The issue was filed at 2026-10-14T21:51:24Z, 49 seconds later. When it was read at
22:30Z it had no comments, and its last update was the owner’s `intake` label at 22:27Z.
The sources were retrieved at 2026-10-14T22:32Z, when the branch head was `0f37f49`; its
two commits after the pin add log lines to `Completed.md`, `search/packer/PACKER.md` and
`search/packer/pk/pending.yaml` and nothing else.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 146 | `12583782190151860342292508597077/1000000000000000000000000000000` | 12.583782190152 | 12.5837821901518604 |

The certificate, `tt2_n146.cert`, gives 146 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #375, #489, #552, #584 and #596.
Its side is the 80-digit KKT point $S^\ast$ of `tt2_n146.exact.txt` scaled by
$1 + 10^{-20}$ about the origin corner, rounded up at 30 places, as the issue says; a test
holds that.
The commit also holds a regularized drawing of the same packing at the same side,
`tt2_n146_regularized.cert` (five angle groups), and the source’s comparison with issue
#505’s packing, `tt2_n146_vs505.json`. The claim rests on `tt2_n146.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
13 files, 422,987 bytes.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/tt2_n146.cert` | `76db96fac15d188b932268e380910e110ffa6da4` | 22916 | `ec6e75ec1f7299d1107c2fabf1683c43907625f5c5b953c791c04e56944fa271` |
| `search/packer/candidates/tt2_n146_regularized.cert` | `3ce34303f57cc84948eda60cdb133778dcb0bcad` | 21189 | `3b19e89db20ac403046e74bba8daded4a97f17501a4d03c7d8a7b3dde1befc0d` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 packing it was
solved from (`tt2_n146.input.txt`), the solver’s report (`tt2_n146.json`), the
regularizer’s report and the comparison with #505, with `LICENSE`, `CREDITS.md` and
`search/exact/README.md`: 10 files and 125,811 bytes.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest only. They are byte-identical to the copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run. The packer’s working log, `search/packer/PACKER.md` (290,674 bytes), is pinned by
digest only.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the issue-552 import did: `sqpack`’s exact
witness verifier and the independent rational corner checker, each deciding every wall
and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

The positive passes both routes, and both routes refuse both controls, each on the
overlap or the wall it was built to break.
The two routes find the same least wall clearance, exactly `1/200000000000000000000`
($5 \times 10^{-21}$), and the same least pair gap, just under $10^{-20}$.
The 3 jobs made 63,510 pair decisions in 21.14 route CPU seconds and 21.33 job wall
seconds, summed; the longest job took 7.24 seconds.
`certify --workers 1` took 24 seconds of wall time, 22:39:53Z to 22:40:17Z, at a load
average of about 1.5 on four cores.
A fresh `check --replay` decided all 3 jobs again, equal to the retained rows apart from
timing, in 23 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and the third exact route
(`devtools.check_half_angle_area`) has not read this certificate.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `9b32da04d` (14 October 2026, after #602 registered T-161 to T-184), and
`check-claims` rebuilds it, each side from its own retained packet:

| Report at 146 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-150`, the case ceiling | Ryan Xu, improved by Robert Barnett (#505) | $1.38 \times 10^{-8}$ |
| `T-174` (PR #574), pending adoption | PingYou Ltd | $1.38 \times 10^{-8}$ |
| `T-168` (#566), pending adoption | PingYou Ltd | $1.38 \times 10^{-8}$ |
| #593, not recorded at 146 | Mykhailo Polkovskyi | $1.38 \times 10^{-8}$ |
| `T-146` (no issue) | Evan Daniel | $8.73 \times 10^{-8}$ |
| `T-125` (#432) | Ryan Xu | $8.74 \times 10^{-8}$ |
| `T-101` (#375) | the Kingbird catalogue, verified by Evan Daniel’s exact ceiling | $1.71 \times 10^{-2}$ |

The certificate is below every report the record holds or has pending at 146.
The issue compares it with Barnett’s 12.583782203951. PingYou Ltd’s two refinements of
that packing, `T-168` and `T-174`, are $2.12 \times 10^{-13}$ below it and print the same
at 12 places, so the issue’s margin of $1.38 \times 10^{-8}$ holds against them too.
No other open issue states a bound at 146, and no watched repository published one after
the 14 October ledger read its reports: BuddenPing’s head `318ab94` re-indexes #566’s
certificate, Mishapolk’s `70a033f` does not touch 146, and Couzo’s `487b058` and
`43ac7d2` hold nothing at 146.

**In report order** (the owner’s rule of 14 October), #606 is the latest report at 146,
at 2026-10-14T21:51:24Z, and is decidably below the standing side, so the rule records it.

## Lineage

The issue says the packing came from a time-travel test of the author’s chain search,
started from the public packings of 10 October: two random large perturbations of Ryan
Xu’s #432 packing and a re-polish reached 12.5837821905, and one exact descent step, a
MILP direction and a re-polish, reached the certified minimum.
It asks that Ryan Xu’s #432 packing be credited as the start and Robert Barnett’s #505 as
the record it improves, and calls the result a different local minimum from #505’s.
Its own matching, an optimal assignment over the box’s symmetries on the regularized
views, finds the two agree to about $10^{-7}$ except a cluster of 10 squares tilted near
42°, which move by up to 0.056.

Measured here by
[`compare_lineage.py`](../mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py),
a greedy nearest-centre matching of the raw certificates under the box’s 8 symmetries
([review/compare_lineage-output.txt](review/compare_lineage-output.txt)): against #505’s
certificate (T-150), 63 of the 146 centres lie within $10^{-6}$, 89 within $10^{-3}$ and
137 within 0.1, the largest distance 0.453; PingYou Ltd’s refinements (T-168, T-174)
give the same counts within two squares.
The two packings share most of their squares and differ in one region, which agrees with
the source’s word that this is another local minimum and not a refinement of #505’s.
The measurement decides nothing; the identity stays the source’s claim.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that $S^\ast$ is a local minimum of $S$, strict modulo 59 exact flat
motions, with 69 corner-to-corner contacts, no corner-to-corner MILP descent, 13 rattlers
and contact equations 74 at the walls and 556 between squares.
It finds no closed form: elimination leaves irreducible factors of degree 15 to 32.
Those are numerical evidence at 80 digits, as the source says, not interval proofs, and
were not replayed here.
Novelty, local or global optimality and rigidity are not established.

The regularized drawing has the same exact side and moves 139 of the 146 poses, turning
45. It is the source’s display view and is not a separate claim; it was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`. The pinned commit names Claude Opus 5.5 as co-author, and the issue states:
“The search, the checks and this request were done with Claude (Claude Code). Evan Daniel
directed and reviewed the work.”
The issue asks for the credit name “Evan Daniel (GitHub @evand)”, and asks that Ryan Xu’s
#432 packing be credited as the start and Robert Barnett’s #505 as the record it
improves.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n146-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n146-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n146-2026-10-14 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n146-2026-10-14 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.
[register-plan.yaml](register-plan.yaml) keeps that output as it printed on 14 October
at `main` `9b32da04d`, for the records pull request that registers the result: one
register entry over n = 146, with no `regularizations`, since by the source’s word and
the measurement above this is a new packing and not a refinement.
The records pull request of 15 October registers it as `T-187`, at V0/C0, pending an
independent review of the replay and adoption at 146.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
