# Amund Kristiansen’s s(303) Certificate

[Issue #755](https://github.com/jlevy/squares/issues/755), opened 2026-10-23T11:12:48Z
by amundsk, asks to register an exact rational packing of 303 unit squares, credited to
Amund Kristiansen, in the gist
[amundsk/78f9f0e7b4669f2f509a281845081768](https://gist.github.com/amundsk/78f9f0e7b4669f2f509a281845081768/511f56bf6e6afb4eb22f12d31371c2a2fe7b4767).
The packet pins the revision the issue names, `511f56bf6e6afb4eb22f12d31371c2a2fe7b4767`
(tree `801bf40a0d0e79692ae6bdd5811201e0fb99504a`, committed 2026-10-23T11:12:11Z), 37
seconds before the issue. It is the gist’s only revision: the GitHub API lists no other
version, the head was the pin when it was read at 16:11Z on 23 October, and the gist had
no comments.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 303 | `223872029093440709529093216833/12500000000000000000000000000` | 17.909762327476 | 17.9097623274752568 |

The side is exactly 17.90976232747525676232745734664.
The certificate, `s303_amund.cert`, gives 303 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in Evan Daniel’s
format, the format of #728’s certificate.
The issue says it is a dilation certificate made with Daniel’s
`search/packer/dilate_cert.py` (evand/square-packing at `7982d7a`): the binary64 packing
in `s303_amund.input.txt` (side 17.909762327457347) has its centres and box scaled by
$1 + 10^{-12}$, its coordinates rounded to rationals and each angle rounded to a rational
half-angle tangent, so every square is exactly unit.
The claim rests on `s303_amund.cert`.

## What the Issue Reports

- **Credit name.** “Amund Kristiansen (GitHub @amundsk)”. The gist’s README says the
  same: “(Amund Kristiansen, 2026-10-23)”.
- **Claim.** One upper bound, $s(303) \le 17.909762327476$, the certificate’s exact side
  rounded up at 12 places, $9.89 \times 10^{-6}$ below the register’s 17.909772217275
  (Evan Daniel, #728). The issue compared it with the case record at 303 on `main` and
  with the open issues and pull requests that mention 303 (#375, #470, #573, #593, #719,
  PR #574).
- **The long decimal.** The issue also prints the side as “17.909762327475256427…”.
  That is the binary64 value nearest the side, $3.35 \times 10^{-16}$ below it, not its
  decimal expansion; the record quotes the exact side or its 12-place ceiling.
- **Digests.** It prints the SHA-256 of the certificate and of its binary64 input; both
  are the digests of the pinned files.
- **Checks.** The author reports that Daniel’s two exact checkers at `7982d7a` accept it:
  `verify_cert.py` (separating axes), with least wall clearance $8.2 \times 10^{-13}$ and
  least pair separation $1.2 \times 10^{-12}$ over 724 close pairs, and `verify_cert2.py`
  (polygon intersection). A third check, “a local packing workbench’s rational certifier
  on the float packing”, is unpublished. No source program ran here.
  The author’s answer of 24 October says the $8.2 \times 10^{-13}$ is the least wall
  clearance of an earlier, unsubmitted certificate (side 17.909763172478), and that
  `verify_cert.py` prints $6.020 \times 10^{-13}$ on this file.
- **What the checkers share.** The issue says the two public checkers share an author and
  the certificate format, and that the certificate was made with the same author’s
  `dilate_cert.py`.
- **Not done.** No exact KKT solve and no local-optimality or rigidity analysis; the float
  packing is a converged polish, not an exact stationary point.
- **Method and lineage.** A new packing found from Daniel’s registered packing (#728,
  `W-known-best-n303`), not a refinement of it. Each round relaxed 2,048 perturbed
  variants of the register packing in a float32 GPU batch through a box slightly below
  the record side, polished the best 64 in binary64 with Daniel’s `fq` quench (augmented
  Lagrangian and SLP), and repeated from the current best. Matched one to one by an
  optimal assignment on centres, the largest move is 0.547, 12 squares move more than 0.1
  and 31 more than 0.01, and it has 96 tilted squares against 91.
- **AI assistance.** “Yes. The search, the certificate and this report were done by
  Claude (Anthropic), working in Claude Code at my direction, using Evan Daniel’s
  open-source engine and checkers.”

[acquisition/issue.json](acquisition/issue.json) keeps the issue as read at 16:20Z on 23
October: never edited, no comments, and the `intake` label added at 16:06:30Z.

## Source Custody

The gist states no licence. The author dedicated its three files to the public domain
under CC0 1.0 on 24 October 2026, in a
[comment on #755](https://github.com/jlevy/squares/issues/755#issuecomment-6388401978),
and asked that the certificate and its input be kept, so the packet retains all three
under [source/](source/), bound to their Git blobs at the pin.
[acquisition/answer.json](acquisition/answer.json) keeps the comment as read at 21:03Z on
24 October, never edited. Until then the packet kept no upstream byte, under the
derived-only form of the [existing retention policy](../known-best-packings/README.md),
and the derived fact of 23 October stays as written, since its receipts are bound to it.

`devtools.acquire_source` wrote the custody record from a blobless clone of the gist
checked out at the pin, from [acquisition/declaration.json](acquisition/declaration.json);
[acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
It was first written on 23 October and written again at the same pin at 20:56Z on 24
October to retain the files, with the digests unchanged; the record keeps the first
retrieval time, which the derived fact names.
Its scope is the gist’s three files, 57,364 bytes, each retained and bound to its Git
blob at the pin:

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `s303_amund.cert` | `748da9ad9ed08571d98c263199d06ee2509e1da7` | 41954 | `9ec01059b35cc983cb28a1bb33bd215a2717228f7efd182e1724de6b22dc511b` |
| `s303_amund.input.txt` | `509560c4f053f977cdeeecde1615be7ff25fdeae` | 14340 | `19fc5d171a26bf8d4a925c0457fa367b12127e8bd581d91c6dcd573108e4bba4` |
| `README.md` | `30d5c0966e6fcba93c56f4dbeaf22f8c9c39c271` | 1070 | `870ead517ba491b00830ece0f357fbced9efa395310c9ecb20c5bb6833fa0c58` |

The checkers and the dilation producer the issue names are Daniel’s, at `7982d7a`, the
commit the [#728 packet](../evand-n303-2026-10-22/README.md) read as the head of
evand/square-packing on 22 October; that packet and the
[n229 packet](../evand-n229-dilation-2026-10-17/README.md) pin `verify_cert.py`,
`verify_cert2.py` and `dilate_cert.py` by digest. They were not run.

## Derived Fact

`devtools.upper_bound_reports` read the certificate from the checkout, after
`acquire_source` showed that the checkout yields this packet’s record, so the bytes have
the digests the manifest pins. It wrote it as an exact rational `center-basis`
Witness/v2, [facts/n-303.yaml.gz](facts/n-303.yaml.gz), naming the certificate’s SHA-256
as `revision_sha256`, from the declaration in
[acquisition/report.json](acquisition/report.json). Offline, the fact must rebuild
itself from the certificate it states. Since the certificate is retained as well, the
importer also holds the fact to `source/s303_amund.cert` whenever it admits it, with no
checkout; `derive --check` against a checkout compares it with the certificate again.
The row keeps its fact, since the receipts below are bound to it.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as #728’s did: `sqpack`’s exact witness verifier and
the independent rational corner checker (`devtools.check_rational_witness_independent`),
each deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle
conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
Every wall is cleared by at least
`60200000000010299100000000000060300000000010299/10^59` ($6.020 \times 10^{-13}$) and
every pair by at least `60250000000010249/(5 * 10^28)` ($1.2050 \times 10^{-12}$), on
both routes, as a $10^{-12}$ dilation gives.
The 3 jobs made 274,518 pair decisions, 45,753 a route a job, in 28.73 route CPU seconds
and 67.37 job wall seconds, summed; the longest job took 27.16 seconds.
`certify --workers 2` took 46 seconds of wall time on 23 October 2026, under `nice` on a
four-core host shared with other lanes at a load average of about 15, and
`check --replay` decided the receipt again in 46 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

**Sharp controls.** The receipt’s two controls are gross, so
[replay/sharp_controls.py](replay/sharp_controls.py) runs the kernel’s two sharp controls
on the derived fact (`SHARP_CONTROLS`, `run_sharp`), at exact contact and $10^{-30}$ past
it: the side lowered by its least far-wall clearance, and the tightest pair closed along
the face normal that separates it. Both routes accept both at contact with the margin
exactly 0 and refuse both past it at exactly $-10^{-30}$, in 39 CPU seconds;
[replay/sharp-controls.json](replay/sharp-controls.json) keeps the verdicts.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and no source program ran here. The adapter that
reads the format transcribes the line filter and corner construction of Daniel’s
checkers, as RF-1 of the
[#728 review](../../../../docs/project/reviews/review-2026-10-22-daniel-728.md) records.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `c1115c095` (23 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet:

| Report at 303 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-230` (#728), the case ceiling and house best packing | Evan Daniel, found from Daniil Ostashev’s packing | $9.8898 \times 10^{-6}$ |
| `T-186`, `T-174` (PR #574), `T-162` (#562), #593 | Mykhailo Polkovskyi, after PingYou Ltd, of Daniil Ostashev’s packing; PingYou Ltd; Ostashev; Polkovskyi | $1.9596 \times 10^{-4}$ |
| `T-146`, `T-136` (#481), #573 | Evan Daniel’s regularization of Nate Chaoweeraprasit’s packing; Chaoweeraprasit; Polkovskyi | $3.30 \times 10^{-3}$ |
| `T-134` (#476), #488 | Francisco Couzo | $7.68 \times 10^{-3}$, $7.60 \times 10^{-3}$ |
| `T-138` (#470), `T-113` (#401) | Mykhailo Polkovskyi; Nate Chaoweeraprasit | $1.06 \times 10^{-2}$ |
| `T-098` (#375), `T-092`, `T-056` | Evan Daniel; Francisco Couzo | $1.46 \times 10^{-2}$ |

The margin below the case ceiling is exactly the difference `claims.json` records,
`9889799071009889799071/10^27` = $0.000009889799071009889799071$.

## Report Order

When read at 16:11Z on 23 October 2026, #755 was the only report below T-230 at 303.
The open issues that mention 303 were #375, #470, #573 and #593, each registered or read
and above T-230, and none had a comment since #728. Of the issues and pull requests
opened since #728, #732’s rows start at 328, and the open records pull requests added no
claim at 303. Of the watched repositories, evand/square-packing’s head was still
`7982d7a`, and Mishapolk/square-packing-records’ five commits since #728 concerned 328 to
10,000. With one report open at the count, no report-order ledger was needed.

Two later reports reach 303, and each is its own pull request’s to import:

- **Mykhailo Polkovskyi’s commit**
  [`Mishapolk/square-packing-records@7e82c64`](https://github.com/Mishapolk/square-packing-records/commit/7e82c6408937c9a6fe2e11054ed716bba67922f0),
  committed at 21:42:16Z on 23 October. The header side of its
  `certificates/0000-0999/n303.cert` is $1.81 \times 10^{-11}$ below T-230 and
  $9.89 \times 10^{-6}$ above this certificate.
- **Francisco Couzo’s #763**, opened at 23:35:51Z on 23 October. Its bound index,
  `upper_bounds.json` at `franciscouzo/square-packing@964ee2b`, holds 303 at
  17.906978233799 rounded up, $2.784 \times 10^{-3}$ below this certificate.

Neither changes this import. #755’s report of 11:12:48Z comes first in report order, and
the house rule adopts a smaller packing only once its certificate is validated.

## Pose by Pose

[measure/identity.py](measure/identity.py) measures the packing against the five
certificates the record holds at 303 that are nearest it, with the #728 packet’s identity
program loaded unchanged, and writes [measure/identity.json](measure/identity.json).
A measurement, which decides nothing:

- **T-230, Daniel’s packing.** Nearest centres pair it one to one with T-230’s packing
  under the identity, with the largest displacement 0.547. The best assignment moves 12
  squares beyond a tenth, 31 beyond $10^{-2}$ and 72 beyond $10^{-3}$, and turns one by
  up to 17.85 degrees; 37 squares move by less than $10^{-6}$. These are the issue’s
  figures.
- **The tilts.** This packing has 96 squares tilted by 1.93 to 26.14 degrees, all one
  way, where T-230’s has 91, at 22.83 to 26.12 degrees, all the same way. Under the
  assignment all 91 of T-230’s tilted squares pair, within a tenth, with squares tilted
  the same way, and 5 of this packing’s tilted squares pair with squares T-230’s packing
  has upright or near upright.
- **The others.** Against T-186’s, T-174’s and T-162’s packings of Ostashev’s two-band
  design no symmetry pairs it one to one, the assignment moves 68 to 70 squares beyond a
  tenth, and 44 of the tilted squares pair with squares tilted the other way, as #728’s
  packing does. Against T-146’s it moves 120 beyond a tenth.

The record keeps the word refinement for a pairing in which no square moves beyond a
tenth, and 12 squares move further here. So it is another arrangement of T-230’s
packing, found from it, not a refinement, as the issue says and RF-4 of the
[stage 4 review](#stage-4-review) words it: 291 of 303 squares lie within a tenth of
T-230’s, and five more squares are tilted. That it was found from T-230’s packing is the
source’s account, which the measurement supports: it is far nearer T-230’s packing than
any other the record holds.

**The dilation.** Given `--checkout`, the program also reads the binary64 input, held to
the digest the manifest pins (retained since 24 October as `source/s303_amund.input.txt`,
so a checkout of the packet’s own `source/` serves), and finds that the input side times $1 + \delta$, with
$\delta$ the double nearest $10^{-12}$, rounded up at 30 places is the certificate’s
side; every centre lies within $4.9 \times 10^{-31}$ of the dilated input, and every
angle within $5.7 \times 10^{-14}$ degrees of the input’s, as the issue says.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The issue claims no local optimality, KKT condition or rigidity, and none was examined.
Novelty, local or global optimality and rigidity are not established.

## Credit

The issue and the gist’s README credit Amund Kristiansen (GitHub @amundsk).
The issue says the search started from Evan Daniel’s registered packing at 303 (#728,
whose own search started from Daniil Ostashev’s packing), naming the record’s witness
`W-known-best-n303`, and used Daniel’s `fq` quench, `dilate_cert.py` and checkers.
The bibliography credit therefore reads `Kristiansen after Daniel, Ostashev, Levy`,
keeping T-230’s chain through its intermediate author
([attribution.md](../../../../attribution.md#credit-text-and-lineage)).
The search, the certificate and the report were done by Claude (Anthropic) in Claude Code
at the author’s direction, as the issue discloses.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source amundsk-n303-2026-10-23 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-n303-2026-10-23 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-n303-2026-10-23 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports amundsk-n303-2026-10-23 check --replay
uv run --frozen --all-extras --group dev python resources/web/amundsk-n303-2026-10-23/replay/sharp_controls.py --out resources/web/amundsk-n303-2026-10-23/replay/sharp-controls.json
uv run --frozen --all-extras --group dev python resources/web/amundsk-n303-2026-10-23/measure/identity.py --checkout GIST_CHECKOUT --out resources/web/amundsk-n303-2026-10-23/measure/identity.json
```

`check` admits the receipt structurally against the derived fact; only `--replay` decides
the geometry again. `derive --checkout GIST_CHECKOUT --check` compares the fact with the
certificate in a checkout at the pin, and `certify --jobs-dir SCRATCH --workers 2` writes
a new receipt from a fresh job directory.

## Stage 4 Review

The [review of 23 October 2026](../../../../docs/project/reviews/review-2026-10-23-amundsk-n303.md)
accepted the certificate for finite feasibility, with nine findings, none blocking.
Its programs and outputs are kept in
[review/review-2026-10-23/](review/review-2026-10-23/README.md), equal to the digests
its `outputs/program-digests.sha256` records.

- **Its own checker.** `review_t238_check.py` decides the certificate on two exact routes
  that share only a reader of its own: integers alone (route Z) and `Fraction` with exact
  edge and vertex tests (route E). Both accept it, and agree with both maintained routes,
  this packet’s receipt and its derived fact at 116 shared numbers. Its author read
  neither maintained route nor Daniel’s checkers before it decided, so it is a clean-room
  re-implementation (`E-amundsk-755-n303-review-exact-feasibility`).
- **Controls.** 21 mutants, at exact contact and $10^{-30}$ past it at three walls and
  five pairs, and gross ones, are accepted and refused as expected by all four deciders.
- **RF-1, the wall clearance.** The issue’s least wall clearance, $8.2 \times 10^{-13}$,
  is not this file’s: by its code at `7982d7a` (read, not run), `verify_cert.py` gives
  $6.020 \times 10^{-13}$ on it, at square 3 and the top wall, as measured here. Its pair
  figure and its 724 close pairs are this file’s. (Answered 24 October: an earlier,
  unsubmitted certificate’s.)
- **RF-2, the long decimal.** “17.909762327475256427…” is the binary64 print of the
  side, not the side; the record quotes the exact side or its ceiling.
- **RF-3, the method.** `dilate_cert.py`’s formulas reproduce the side and all 606 centre
  coordinates from the input, and each tangent to within one unit in the last place of
  the platform’s `tan`; the factor is $1 + \mathrm{fl}(10^{-12})$. (Answered 24 October:
  made on macOS 26 arm64 with Python 3.14.6, so with Apple’s libm.)
- **RF-4, identity.** Another arrangement of T-230’s packing, found from it, not a
  refinement of it: one to one with it, 12 squares beyond a tenth, five newly tilted and
  47 of about 860 contacts changed.
- **RF-5, significance.** S2, at T-188’s scale and kind, replacing the draft S3.
- **RF-6.** Not rigid: five squares touch nothing and keep at least
  $4.67 \times 10^{-3}$; no local-minimum claim follows.
- **RF-7.** The maintained replay shares the adapter’s two transcribed expressions with
  Daniel’s checkers, so it is `shared-components`, as T-230’s is
  (`E-amundsk-755-n303-exact-feasibility`).
- **RF-8 and RF-9.** Custody as recorded above, and the review’s programs retained and
  registered (`V-amundsk-755-review-check`, `V-amundsk-755-review-controls`). (RF-8
  answered 24 October: CC0 1.0; the files are now retained.)

The review is a dated record and stays as written. Its three Questions for the Author are
answered by the author’s comment of 24 October, which the record reads in T-239’s notes
and here: the first confirms RF-1 as the correction it made and gives its cause, the
second confirms RF-3’s reading that the tangents differ by platform libm, and the third
is yes, by retention under CC0. None was held open.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-303.yaml.gz` | receipt | `015a685fb0ca8561d2ef9aaa211575aee8aad6d8` | `7465269ff93b702c88735e9204256a708664a7c64fefe3219ae13183d11ae986` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
