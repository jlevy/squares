# Evan Daniel: Three Packings of 126 Reconstructed from a Picture

No issue asked for this import.
The intake pass of 10 October 2026 read
[evand/square-packing](https://github.com/evand/square-packing/tree/268af529546176a25224ea3b2c7d29cef8d9e911/search/trio126)
past `ed01e0d` and found `search/trio126/`, added by
`268af529546176a25224ea3b2c7d29cef8d9e911` (tree
`2679e86744bae0c4a6f1096b0c9413d63896c02d`, committed 2026-10-09T05:43:37Z). The
directory holds exact certificates of three packings of 126 unit squares that Evan
Daniel reconstructed from one picture and polished to exact local minima.
Its README says “No claim here: register status not checked”.
No later commit touches the directory; the repository’s head was `799be37` when the
source was retrieved at 2026-10-10T13:50Z.

| Certificate | Packing, as the source names it | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- | --- |
| `n126_xu.cert` | Ryan Xu’s, a 45° lattice diamond | `11742640687119285146522492579501/10^30` | 11.7426406871192852 |
| `n126_ph14.cert` | SQUISH phase 14, a diagonal staircase band | `11763736443985669176333330330349/10^30` | 11.7637364439856692 |
| `n126_ph10.cert` | SQUISH phase 10, a lattice block near 30° | `11773303606603240442283309232987/10^30` | 11.7733036066032405 |

Each side is written in its certificate as a fraction over $10^{30}$, and each is a
terminating decimal of 30 places.

## Every Claim the Commit Makes

- **The three certificates.** Each states $s(126) \le S$ at the side above, in Evan
  Daniel’s text format: `n S`, then a rational centre $(x, y)$ in $[0, S]^2$ and a
  rational $t = \tan(\theta/2)$ per square.
- **Exact local minima.** The README gives the exact side of each polished packing as
  `exactsolve` finds it: $15/2 + 3\sqrt2 = 11.742640687119285\ldots$ for Ryan Xu’s,
  $11.763736443985669\ldots$ and $11.773303606603240\ldots$ for the two SQUISH packings.
  It says each is a local minimum of $S$, strict modulo exact flat motions and jammed in
  every corner-corner branch.
  The `.exact.txt` files hold those points at 70 digits; they are numerical evidence,
  not a certificate of either statement.
- **Fidelity to the picture.** Each side agrees with the one printed under its panel to
  all six printed decimals (11.742641, 11.763736 and 11.773304), and a reconstruction
  may differ from the original in rattlers.
  The picture, `126.jpg`, is not in the repository.
- **Checkers.** The README runs `verify_cert.py` and the independent
  polygon-intersection `verify_cert2.py` on each certificate, and `SHA256SUMS` lists the
  three certificates’ digests.
  The digests match the retained bytes.

The same commit adds split-rigidity notes to `search/TILINGS.md`, including the 2×2
split of the phase-14 packing, a packing of 504 at 23.5275, above the grid’s 23 and not
a local minimum. That file is outside this packet and asks for nothing at a count of the
case corpus.

## Retained Here

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

The scope is 17 files.
The 15 retained are the whole of `search/trio126/` (the README, `SHA256SUMS`, and for
each packing its certificate, its binary64 `fq` output `.txt` and its 70-digit
`exactsolve` point `.exact.txt`), the licence, `CREDITS.md`, the certificate-format
README `search/exact/README.md`, and `search/packer/img2packing.py`, the tool that
turned the picture into starting poses.
The two checkers `search/exact/verify_cert.py` and `verify_cert2.py` are pinned by
digest only: they are byte-identical to the copies
[the issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, which
the custody check compares.
No source program was run.

## Exact Replay

Only `n126_xu.cert` is replayed, the one certificate below the case ceiling.
It enters geometry decisions through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
A positive job, a duplicate-square control and an outside-container control each ran in
their own child process.

The positive passes both routes, and both routes refuse both controls, each on the
overlap or the wall it was built to break.
Both routes find the least wall clearance exactly $5 \times 10^{-21}$ and the least pair
gap $9.99999999999999 \times 10^{-21}$, consistent with a touching packing dilated by
$1 + 10^{-20}$: the certificate’s side exceeds $15/2 + 3\sqrt2$ by
$1.1743 \times 10^{-19}$, about $10^{-20}$ of the side.
The three jobs made 47,250 pair decisions in 11.48 route CPU seconds and 26.27 job wall
seconds, summed; the longest job took 10.76 seconds, and the two-worker run 17.4 seconds
of wall time.
Other lanes held the machine at a load average of 9 to 12 on four cores, so
the walls overstate the work and the route CPU seconds do not.
`check --replay` decided the receipt again in 17.3 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the `n126_xu` certificate
against the record as it stood on `main` at `af17208c0` (10 October 2026), and
`devtools.upper_bound_reports` rebuilds it with the case ceiling read from Ryan Xu’s own
packet. The [declaration](acquisition/report.json) reads one certificate per count, so
the two SQUISH reconstructions are compared below from their stated sides and are not in
that record.

- **`n126_xu`.** The case’s reported and verified ceilings are both Ryan Xu’s
  certificate side `14678300859014678300859/1250000000000000000000`
  (11.7426406872117427, T-125, `E-ryxu-432-rational-feasibility`). The certificate is
  below it by exactly `92457494164707420499/10^30` ($9.25 \times 10^{-11}$), the
  smallest side the record would hold at 126. It is a precision refinement of the same
  arrangement as the source describes it; this import has not compared the two
  certificates pose by pose.
- **`n126_ph14` and `n126_ph10`.** Both are above the case ceiling, by
  $2.11 \times 10^{-2}$ and $3.07 \times 10^{-2}$. Phase 14’s side is below every SQUISH
  side the record holds at 126, and neither the record nor `itsnaka/squish-certs` at
  `d45669b` holds a SQUISH release that states it: that repository’s `n126` folders are
  the two releases T-113 and T-115 hold.
  Phase 10’s is $4.00 \times 10^{-12}$ below the side of the SQUISH update’s certificate
  (`3196078786847066046655612475207/271468306062659398105946914816`,
  11.7733036066072403, T-115), which is superseded at 126.
- **The record’s other entries at 126.** T-098 (11.774735132387832842560264587322, Evan
  Daniel’s exact optimum of Joost de Winter’s packing), T-113 (SQUISH,
  11.7735852916961071) and T-115 hold larger sides, each superseded at 126 by T-125.
  T-127 does not hold 126. T-083 holds the verified lower bound 11.2354552767. No
  pending report names 126.
- **$15/2 + 3\sqrt2$.** The record holds no closed form at 126: the case’s exact form is
  Ryan Xu’s rational side, with algebraic degree 1, and his own records file prints
  11.7426406872. The closed form is the side of a local minimum of one packing, an upper
  bound and not a value of $s(126)$, and no retained certificate decides a packing at
  that side: `n126_xu.cert` certifies its rational side, $1.17 \times 10^{-19}$ above
  it.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The local-minimum statements, the closed form $15/2 + 3\sqrt2$, and the agreement with
the picture are the source’s; no KKT point, interval enclosure or comparison with the
picture has been replayed here, and the replay above has not been reviewed.
The two SQUISH certificates were read but not replayed, since neither is below the case.

## Credit and Licence

The source names the packings as other people’s: Ryan Xu’s, and two of Nate
Chaoweeraprasit’s SQUISH packings, phases 14 and 10. Evan Daniel reconstructed them from
the picture with `img2packing.py`, polished them with his `fq` quench and solved them
with `exactsolve`. Everything retained is under the MIT licence, copyright 2026 Evan
Daniel (`LICENSE`), with attribution in `CREDITS.md`. The commit names Claude Opus 5.5
as co-author, and `CREDITS.md` says the repository’s work was produced by Claude under
human direction.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-trio126-2026-10-09 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-trio126-2026-10-09 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-trio126-2026-10-09 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-trio126-2026-10-09 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
