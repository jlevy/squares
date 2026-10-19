# Mishapolk: Seventy-Three Certificates at 46f638c, n = 51 to 308

[Issue #593](https://github.com/jlevy/squares/issues/593), opened 2026-10-14T01:40Z,
reports 73 upper bounds for $n$ from 51 to 308, each an exact rational certificate in
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/46f638ce0537beeb1bad24242c6a3d357eecd9ee/certificates)
at `46f638ce0537beeb1bad24242c6a3d357eecd9ee` (tree
`a3d2236c9b2c67d111d21ff9448b855436ed59f6`, committed 2026-10-14T01:24:10Z), the
revision the issue pins.
The source was retrieved at 2026-10-14T07:09Z. `main` had moved to
`ec87dc69b2094d4c0f692c1b810aec23b1b3b409`, whose six commits add and edit only
`ISSUE_REGISTRATION.md`, the issue’s draft.
The issue had no comments and had not been renamed when it was read at 07:10Z.

The issue’s claim is that all 73 bounds “beat or tie all standing records in the
official catalogue and all open issues/PRs (#500, #501, #503, #504, #505, #506, #552)”.
**Measured against the record at `main` `b8c930338` and every open report of 14 October,
that holds at one count, 237.** At 40 counts the certificate’s exact side equals the
case’s, at 16 it is above the case, and at 17 it is below the case, where at 16 of them
another open report is smaller or states the same side.
[Against the Record](#against-the-record) has the table.

## What the Issue Reports

- **Credit name.** “Mishapolk (Mykhailo Polkovskyi)” at the top, and “Credit: Mishapolk
  (Mikhail Polk)” under Lineage and credit.
  The packet records both spellings and asks which the record should use.
- **Sides.** The table prints each side at 16 places, labelled “Certified Side S (16
  dec)”. Those prints are the sides’ binary64 values, the `side_float` field of the
  release’s `certificates/census.json`; they neither equal nor round up the exact sides,
  and the importer refuses all 73 at them.
  The census states each exact `side_fraction`, and every certificate’s header equals
  it, so each is admitted there (`printed_in` in
  [acquisition/report.json](acquisition/report.json)).
- **Digests.** All 73 SHA-256 digests the issue lists are the digests of the pinned
  files, and the census lists the same 73.
- **Checks.** Evan Daniel’s `verify_cert.py` and `verify_cert2.py`, and this
  repository’s `sqpack/verify.py`, run from the author’s own copies under
  `tools/competitors/` and `tools/jlevy_squares/`, accept all 73 with zero tolerance,
  219 runs in 43.9 seconds.
  None of those copies is in the pinned tree.
- **Not claimed.** No global optimality, local rigidity or KKT second-order optimality.
- **Lineage.** Each row names a “Lineage / Baseline Holder”, 50 of them in the form “X
  (conquered via …)”, 27 of those “via exact dual-verified optimum”; the closing
  paragraph credits Erich Friedman, Joshua Levy, Evan Daniel, Ryan Xu, Nate
  Chaoweeraprasit, Robert Barnett, Francisco Couzo, Daniil Ostashev, David Ellsworth,
  Kevin Fang “and other contributors”.
- **AI assistance.** “Gemini 3.8 assisted with solver scripting, precision checks, and
  formatting.”

## What the Release Holds

`certificates/` holds the 73 certificates `n<n>.cert`; `census.json`, the exact side,
binary64 side, baseline, delta, digest and lineage of each; the 19 certificates
`square-<n>.cert` of [issue #573](https://github.com/jlevy/squares/issues/573), the same
Git blobs as at `336bdf5`, which the
[#573 packet](../mishapolk-exact-certificates-2026-10-12/README.md) derives; and the
decimal poses and drawings `square-<n>.txt` and `.svg` of issues #470 and #573. The root
holds `LEGAL_VICTORIES.jsonl`, which restates the census with a tier and a timestamp per
count, the README, and a copy of David Ellsworth’s `check_packing.py`.

The certificates entered the history in five groups, each dated by the first commit that
holds its bytes:

| First commit (UTC) | Counts |
| --- | --- |
| `336bdf5`, 2026-10-12T23:52:23Z, as #573’s `square-<n>.cert` | 103, 153, 207, 258 |
| `8bb41af`, 2026-10-13T15:51:54Z | 129, 131, 154, 155, 156, 175, 176, 204, 211, 232, 237, 238, 239, 241, 263, 264, 271, 302, 303, 304 |
| `3d13a87`, 2026-10-13T16:39:57Z | 84, 86, 105 |
| 34 commits of one count each, 2026-10-13T21:26:08Z to 21:38:21Z | 51, 68, 70, 88, 102, 106, 110, 123, 126, 130, 132, 152, 172, 177, 179, 180, 182, 199, 206, 208, 210, 228, 240, 259, 266, 268, 269, 273, 292, 295, 297, 301, 307, 308 |
| `46f638c`, 2026-10-14T01:24:10Z, the pin | 108, 127, 146, 181, 209, 236, 261, 267, 270, 272, 305, 306 |

The pin’s commit message is “Absorb latest pending issue/PR submissions: update 12
certificates (…) to absolute tightest bounds”.
**Thirteen of the 73 files are, byte for byte, certificates this repository already
retains from other authors:** Evan Daniel’s regularized lists
([T-146](../evand-regularized-2026-10-10/README.md)) at 70, 102, 123, 269, 292 and 295,
and Francisco Couzo’s certificates at 105, 108, 127, 209, 267, 305 and 306
([T-128](../couzo-exact-refinements-2026-10-08/README.md),
[#476](../couzo-exact-certificates-2026-10-09/README.md),
[#488](../couzo-certificates-2026-10-10/README.md) and
[#506](../couzo-certificates-2026-10-11/README.md)). The manifests of those packets and
of this one record the same SHA-256 for each.
27 of the 73 files carry Evan Daniel’s regularized-view header (`search/regularize`) and
42 the header of his exact-certificate writer, which Couzo’s certificates also carry.

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for Mishapolk’s
[#470 packet](../mishapolk-decimal-poses-2026-10-09/README.md), this packet keeps no
upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
All 191 files of the declared scope, 5,901,361 bytes, are pinned only; the declared
`source/` directory is empty by design.
They include the README (SHA-256
`d1b8a7da7c0e61e38ce558bedc54ca0429bdce7ef9bf1778890852b8e13c6378`), the census
(`ada395897cd0818c8aa626390732b3721ee521f25d68ffb6ffacebfa9a032abc`) and
`LEGAL_VICTORIES.jsonl`
(`f8d1b8ac4fa4b44720d227425dc1f2184872118c6f3ba36f1abd296420c4657d`).

## Derived Facts

`devtools.upper_bound_reports` read 72 certificates from the checkout at the pin, after
`devtools.acquire_source` showed that the checkout yields this packet’s acquisition
record and manifest, so the bytes it read have the digests the manifest records.
It wrote each as an exact rational `center-basis` Witness/v2 under `facts/`, naming the
certificate’s SHA-256 as `revision_sha256`. The facts are this repository’s derivation;
offline each must rebuild itself from the certificate it states.

**$n = 51$ is held out of the declaration.** Its case ceiling is Ryan Xu’s
$(16 + 5\sqrt{2})/3$ (T-125’s radical certificate,
`E-ryxu-432-radical-n51-feasibility`), and the importer’s houses state rational sides
only. The certificate (`certificates/n51.cert`, SHA-256
`e066f65fa4c8a426f3ce34987389332e0aeeb94578b28aa0512a9e32af2e4c9d`) states
$S = 7690355937288491748079718099723/10^{30}$, so $3S - 16 = 7.0710678118654752442391…$
and $(3S - 16)^2 - 50 \approx 3.26 \times 10^{-18} > 0$: $S$ is above
$(16 + 5\sqrt{2})/3$, by about $7.69 \times 10^{-20}$, which is the radical side dilated
by $1 + 10^{-20}$. It is pinned by digest, not derived and not replayed.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each of the 72 certificates
against the record at `main` `b8c930338` (14 October 2026), and `check-claims` rebuilds
it: each case ceiling from its holder’s own packet, each register entry at the count
from its own packet or, where it has none, from the bound its claim states, and each
open report from the side it prints.
The open reports are PingYou Ltd’s (#503 and #504 refinements, #564, #566 to #569,
posted by BuddenPing), PR #574 (PingYou Ltd’s cumulative refinements: at each count the
latest of its exact 153 and 302 claims, its algebraic claims and its numerical claims,
read at head `4c319c2`), Francisco Couzo’s #561, #583 and #586, Daniil Ostashev’s #562
and #575 (with 304, added on 13 October), and #573 at 209 and 270, where its
certificates differ from these.
#570 restates #583’s 154; #582, #584, #594 and #596, and open PRs #585, #587 and #591,
state no side at these counts.
A printed side is compared as the numbers its rounding allows, so a print equal to this
certificate’s at its places is undecided.

| Relation to the case’s exact ceiling | Counts |
| --- | --- |
| Equal (40) | 70, 84, 86, 88, 102, 105, 106, 108, 110, 123, 126, 127, 130, 132, 152, 172, 177, 179, 180, 182, 199, 206, 208, 209, 210, 228, 240, 263, 266, 267, 268, 269, 273, 292, 295, 297, 301, 305, 306, 308 |
| Above (15, and 51 by hand) | 68, 103, 131, 146, 155, 181, 236, 238, 239, 258, 259, 261, 270, 272, 307 |
| Below (17) | 129, 153, 154, 156, 175, 176, 204, 207, 211, 232, 237, 241, 264, 271, 302, 303, 304 |

Above the case, the margins are $9.9 \times 10^{-31}$ at 155; $1.0 \times 10^{-21}$ at
146, 181, 261, 270 and 272, all five among the twelve the pin’s commit says it absorbed;
about $10^{-19}$ at 68, 131, 238, 239, 259 and 307; $3.3 \times 10^{-16}$ at 236;
$4.4 \times 10^{-14}$ at 103 and $3.4 \times 10^{-12}$ at 258, where the case holds Evan
Daniel’s regularization (T-146) of Mishapolk’s own #470 packing.

Of the 17 counts below the case:

- **237: the smallest known side.** $2.45 \times 10^{-4}$ below the case (T-140, Couzo’s
  refinement of SQUISH) and $2.43 \times 10^{-4}$ below Couzo’s #561 and PR #574, which
  agree with each other at the places #561 prints.
- **211 and 241: the same exact side as Couzo’s.** Couzo’s #586 prints 14.993558913975
  and 15.987117095151, and its certificates at `b85dee2` (committed
  2026-10-13T17:30:53Z, read from a clone and not retained) state exactly
  `7496779456987003085666602828823/500000000000000000000000000000` and
  `15987117095150238758321758129189/1000000000000000000000000000000`, the sides here;
  the two files differ, and their poses differ as sets.
  Mishapolk’s first commit of both is `8bb41af`, 2026-10-13T15:51:54Z. Couzo’s #583 and
  #586 credit both arrangements to Daniil Ostashev’s #575, whose sides are
  $1.35 \times 10^{-4}$ and $1.72 \times 10^{-5}$ above.
- **Smaller elsewhere, by a certificate guard:** PR #574 by about $10^{-19}$ at 129,
  175, 176, 204, 232, 264 and 303, and Ostashev’s #562 and #575, posted
  2026-10-12T19:10Z and 2026-10-13T00:42Z (304 at 04:13Z), by less than $10^{-30}$ at
  129, 176, 204, 303 and 304: the same sides as Ostashev’s to 30 places, which Mishapolk
  first committed in `8bb41af` at 15:51Z on 13 October.
- **Smaller elsewhere, by a different packing:** Couzo’s #583 at 302 by
  $2.62 \times 10^{-4}$; Couzo’s #586 at 154 by $1.29 \times 10^{-3}$.
- **Smaller elsewhere, by a refinement:** PR #574 at 153 by $1.57 \times 10^{-14}$ and
  at 207 by $2.42 \times 10^{-12}$. Here the certificate is below the case (T-148,
  T-147) by $2.56 \times 10^{-12}$ and $1.49 \times 10^{-9}$, and below PingYou’s #504
  and #503 refinements by $2.55 \times 10^{-12}$ and $5.56 \times 10^{-13}$.
- **156 and 271:** Couzo’s #561 prints the same side at 12 places, which leaves the two
  undecided, and PR #574 is smaller by about $10^{-19}$.

The full table, smallest first among the other reports:

| n | Side, rounded up at 16 places | Against the case ceiling (holder) | Smaller or tied reports | Smallest |
| --- | --- | --- | --- | --- |
| 68 | 8.7987952372182840 | above by $8.80 \times 10^{-20}$ (Francisco Couzo, improved by Seth Rehwaldt, T-118) | PR #574 (PingYou) smaller by $8.80 \times 10^{-20}$; T-098 (#375) equal | undecided: case: Francisco Couzo, improved by Seth Rehwaldt, PR #574 (PingYou) |
| 70 | 8.8809603715555796 | equal (ry-xu, improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $8.88 \times 10^{-20}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 84 | 9.6979347990149214 | equal (ry-xu, improved by Francisco Couzo, T-130) | PR #574 (PingYou) smaller by $9.70 \times 10^{-20}$ | PR #574 (PingYou) |
| 86 | 9.8205354074967423 | equal (ry-xu, improved by Francisco Couzo, T-130) | PR #574 (PingYou) smaller by $9.82 \times 10^{-20}$ | PR #574 (PingYou) |
| 88 | 9.8824510304812469 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, T-127) | PR #574 (PingYou) smaller by $9.88 \times 10^{-20}$ | PR #574 (PingYou) |
| 102 | 10.6058286964315784 | equal (ry-xu, improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.06 \times 10^{-19}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 103 | 10.6792320473613500 | above by $4.36 \times 10^{-14}$ (ry-xu, improved by Mishapolk, Evan Daniel, T-146) | PR #574 (PingYou) smaller by $4.36 \times 10^{-14}$; this file is #573’s certificate, byte for byte | PR #574 (PingYou) |
| 105 | 10.7893037837481589 | equal (ry-xu, improved by Francisco Couzo, T-130) | #568 (PingYou) smaller by $1.08 \times 10^{-19}$; PR #574 (PingYou) smaller by $1.08 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | undecided: #568 (PingYou), PR #574 (PingYou) |
| 106 | 10.8229080441328476 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | T-121 (#419) smaller by $1.08 \times 10^{-19}$; PR #574 (PingYou) smaller by $1.08 \times 10^{-19}$ | undecided: PR #574 (PingYou), T-121 (#419) |
| 108 | 10.9048210123203565 | equal (ry-xu, improved by Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $1.09 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 110 | 10.9967833966315917 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.10 \times 10^{-19}$ | PR #574 (PingYou) |
| 123 | 11.5913781454976982 | equal (ry-xu, improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.16 \times 10^{-19}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 126 | 11.7426406871192852 | equal (ry-xu, improved by Evan Daniel, T-139) | PR #574 (PingYou) smaller by $1.17 \times 10^{-19}$ | PR #574 (PingYou) |
| 127 | 11.8108787875891799 | equal (ry-xu, improved by Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $1.18 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 129 | 11.8700138504044644 | below by $2.02 \times 10^{-3}$ (ry-xu, improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.18 \times 10^{-19}$; #562 (Ostashev) smaller by $3.61 \times 10^{-31}$ | PR #574 (PingYou) |
| 130 | 11.9044830325157865 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, T-127) | PR #574 (PingYou) smaller by $1.19 \times 10^{-19}$ | PR #574 (PingYou) |
| 131 | 11.9496595880358604 | above by $1.19 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), T-136) | PR #574 (PingYou) smaller by $1.19 \times 10^{-19}$ | PR #574 (PingYou) |
| 132 | 11.9856801988458089 | equal (Evan Daniel, T-141) | PR #574 (PingYou) smaller by $1.20 \times 10^{-19}$ | PR #574 (PingYou) |
| 146 | 12.5837822039510463 | above by $1.00 \times 10^{-21}$ (ry-xu, improved by Robert Barnett, T-150) | PR #574 (PingYou) smaller by $2.12 \times 10^{-13}$; #566 (PingYou) smaller by $2.12 \times 10^{-13}$ | undecided: #566 (PingYou), PR #574 (PingYou) |
| 152 | 12.8307188009766100 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | T-122 (#419) smaller by $1.28 \times 10^{-19}$; PR #574 (PingYou) smaller by $1.28 \times 10^{-19}$ | undecided: PR #574 (PingYou), T-122 (#419) |
| 153 | 12.8700138504044800 | below by $2.56 \times 10^{-12}$ (PingYou Ltd, T-148) | PR #574 (PingYou) smaller by $1.57 \times 10^{-14}$; this file is #573’s certificate, byte for byte | PR #574 (PingYou) |
| 154 | 12.9224998146423975 | below by $5.70 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), T-136) | #586 (Couzo) smaller by $1.29 \times 10^{-3}$ | #586 (Couzo) |
| 155 | 12.9524254069584562 | above by $9.92 \times 10^{-31}$ (Daniil Ostashev, T-149) | PR #574 (PingYou) smaller by $1.30 \times 10^{-19}$ | PR #574 (PingYou) |
| 156 | 12.9791658538342765 | below by $6.76 \times 10^{-6}$ (Daniil Ostashev, T-149) | PR #574 (PingYou) smaller by $1.30 \times 10^{-19}$; #561 (Couzo) undecided, printed side within $7.24 \times 10^{-13}$ | undecided: #561 (Couzo), PR #574 (PingYou) |
| 172 | 13.6189889568993985 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.36 \times 10^{-19}$ | PR #574 (PingYou) |
| 175 | 13.7641743174865967 | below by $2.95 \times 10^{-3}$ (ry-xu, improved by Francisco Couzo, T-140) | PR #574 (PingYou) smaller by $1.38 \times 10^{-19}$ | PR #574 (PingYou) |
| 176 | 13.7958723184364073 | below by $1.70 \times 10^{-2}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.38 \times 10^{-19}$; #575 (Ostashev) smaller by $9.23 \times 10^{-31}$ | PR #574 (PingYou) |
| 177 | 13.8229797341694487 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | T-123 (#419) smaller by $1.38 \times 10^{-19}$; PR #574 (PingYou) smaller by $1.38 \times 10^{-19}$ | undecided: PR #574 (PingYou), T-123 (#419) |
| 179 | 13.8837954905108985 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, T-127) | PR #574 (PingYou) smaller by $1.39 \times 10^{-19}$ | PR #574 (PingYou) |
| 180 | 13.9169935224778325 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $1.39 \times 10^{-19}$ | PR #574 (PingYou) |
| 181 | 13.9508195310229241 | above by $1.00 \times 10^{-21}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.00 \times 10^{-21}$ | PR #574 (PingYou) |
| 182 | 13.9740907131214391 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.40 \times 10^{-19}$ | PR #574 (PingYou) |
| 199 | 14.6175721735928069 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, T-127) | PR #574 (PingYou) smaller by $1.46 \times 10^{-19}$ | PR #574 (PingYou) |
| 204 | 14.8086632343869566 | below by $1.42 \times 10^{-2}$ (the Kingbird catalogue, verified by Evan Daniel’s exact ceiling, T-101) | PR #574 (PingYou) smaller by $1.46 \times 10^{-19}$; #562 (Ostashev) smaller by $3.52 \times 10^{-32}$ | PR #574 (PingYou) |
| 206 | 14.8601586633919033 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.49 \times 10^{-19}$ | PR #574 (PingYou) |
| 207 | 14.8809603715580000 | below by $1.49 \times 10^{-9}$ (PingYou Ltd, T-147) | PR #574 (PingYou) smaller by $2.42 \times 10^{-12}$; this file is #573’s certificate, byte for byte | PR #574 (PingYou) |
| 208 | 14.9245187720293559 | equal (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, T-127) | PR #574 (PingYou) smaller by $1.49 \times 10^{-19}$ | PR #574 (PingYou) |
| 209 | 14.9462232264464511 | equal (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-140) | PR #574 (PingYou) smaller by $1.49 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 210 | 14.9730011165876258 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.50 \times 10^{-19}$ | PR #574 (PingYou) |
| 211 | 14.9935589139740062 | below by $2.78 \times 10^{-3}$ (Daniil Ostashev, T-149) | #586 (Couzo) undecided, printed side within $9.94 \times 10^{-13}$ | undecided: this certificate, #586 (Couzo) |
| 228 | 15.6046014757296743 | equal (Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $1.56 \times 10^{-19}$ | PR #574 (PingYou) |
| 232 | 15.7641743174865967 | below by $3.25 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), T-136) | PR #574 (PingYou) smaller by $1.58 \times 10^{-19}$ | PR #574 (PingYou) |
| 236 | 15.8639557471592678 | above by $3.29 \times 10^{-16}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $3.29 \times 10^{-16}$; T-136 (#481) smaller by $1.00 \times 10^{-21}$ | PR #574 (PingYou) |
| 237 | 15.9027050578663668 | below by $2.45 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-140) | none | this certificate |
| 238 | 15.9241067853214947 | above by $1.59 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.59 \times 10^{-19}$ | PR #574 (PingYou) |
| 239 | 15.9484433273005000 | above by $1.59 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.59 \times 10^{-19}$ | PR #574 (PingYou) |
| 240 | 15.9696853375307804 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.60 \times 10^{-19}$ | PR #574 (PingYou) |
| 241 | 15.9871170951502388 | below by $1.02 \times 10^{-3}$ (Francisco Couzo, improved by Evan Daniel, T-098) | #586 (Couzo) undecided, printed side within $7.61 \times 10^{-13}$ | undecided: this certificate, #586 (Couzo) |
| 258 | 16.5634480021371700 | above by $3.38 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Mishapolk, Evan Daniel, T-146) | PR #574 (PingYou) smaller by $3.38 \times 10^{-12}$; this file is #573’s certificate, byte for byte | PR #574 (PingYou) |
| 259 | 16.5913781454976982 | above by $1.66 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), T-136) | PR #574 (PingYou) smaller by $1.66 \times 10^{-19}$ | PR #574 (PingYou) |
| 261 | 16.6787798753432078 | above by $1.00 \times 10^{-21}$ (ry-xu, improved by Robert Barnett, T-150) | PR #574 (PingYou) smaller by $2.98 \times 10^{-13}$; #567 (PingYou) smaller by $2.98 \times 10^{-13}$ | PR #574 (PingYou) |
| 263 | 16.7331660078993790 | equal (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.67 \times 10^{-19}$ | PR #574 (PingYou) |
| 264 | 16.7747351323878329 | below by $3.44 \times 10^{-3}$ (the Kingbird catalogue, verified by Evan Daniel’s exact ceiling, T-101) | PR #574 (PingYou) smaller by $1.68 \times 10^{-19}$ | PR #574 (PingYou) |
| 266 | 16.8230287507564760 | equal (Evan Daniel, T-119) | PR #574 (PingYou) smaller by $1.68 \times 10^{-19}$ | PR #574 (PingYou) |
| 267 | 16.8388152699482623 | equal (ry-xu, improved by Francisco Couzo, T-134) | PR #574 (PingYou) smaller by $1.68 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 268 | 16.8788148210067648 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.69 \times 10^{-19}$ | PR #574 (PingYou) |
| 269 | 16.9015135821891322 | equal (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.69 \times 10^{-19}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 270 | 16.9281969933290166 | above by $1.00 \times 10^{-21}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.00 \times 10^{-21}$ | PR #574 (PingYou) |
| 271 | 16.9489923564512057 | below by $1.24 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.69 \times 10^{-19}$; #561 (Couzo) undecided, printed side within $7.94 \times 10^{-13}$ | undecided: #561 (Couzo), PR #574 (PingYou) |
| 272 | 16.9655864748376712 | above by $1.00 \times 10^{-21}$ (Nate Chaoweeraprasit (itsnaka), T-151) | #569 (PingYou) smaller by $5.26 \times 10^{-16}$; PR #574 (PingYou) smaller by $5.26 \times 10^{-16}$ | undecided: #569 (PingYou), PR #574 (PingYou) |
| 273 | 16.9839259626504044 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.70 \times 10^{-19}$ | PR #574 (PingYou) |
| 292 | 17.5913781454976982 | equal (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.76 \times 10^{-19}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 295 | 17.7042327907360304 | equal (ry-xu, improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.77 \times 10^{-19}$; this file is T-146’s certificate, byte for byte | PR #574 (PingYou) |
| 297 | 17.7404172875438019 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.77 \times 10^{-19}$ | PR #574 (PingYou) |
| 301 | 17.8466671928434898 | equal (Francisco Couzo, improved by Evan Daniel, T-098) | PR #574 (PingYou) smaller by $1.78 \times 10^{-19}$ | PR #574 (PingYou) |
| 302 | 17.8702753825550597 | below by $1.75 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | #583 (Couzo) smaller by $2.62 \times 10^{-4}$; PR #574 (PingYou) smaller by $1.79 \times 10^{-19}$ | #583 (Couzo) |
| 303 | 17.9099582910699080 | below by $3.11 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.79 \times 10^{-19}$; #562 (Ostashev) smaller by $2.64 \times 10^{-31}$ | PR #574 (PingYou) |
| 304 | 17.9294277580751750 | below by $1.38 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-152) | #575 (Ostashev) smaller by $8.85 \times 10^{-31}$ | #575 (Ostashev) |
| 305 | 17.9504664821377123 | equal (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-152) | PR #574 (PingYou) smaller by $1.80 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 306 | 17.9634337174914258 | equal (Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $1.80 \times 10^{-19}$; this file is Couzo’s certificate, byte for byte | PR #574 (PingYou) |
| 307 | 17.9808627840546911 | above by $1.80 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), T-136) | PR #574 (PingYou) smaller by $1.80 \times 10^{-19}$ | PR #574 (PingYou) |
| 308 | 17.9982698795262559 | equal (Kevin Fang, improved by Evan Daniel, T-141) | PR #574 (PingYou) smaller by $1.80 \times 10^{-19}$ | PR #574 (PingYou) |

## Exact Replay of Three Counts

Only the facts enter geometry decisions, through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. The replay covers the counts where no report is decidably smaller: 237,
and 211 and 241, which tie Couzo’s certificates.
Each ran a positive job, a duplicate-square control and an outside-container control,
each in its own child process, on one worker.

All three positives pass both routes, and both routes refuse all six controls, each on
the overlap or the wall it was built to break.
In each positive the two routes find the same least wall clearance, exactly
$1/(2 \times 10^{20})$, and the same least pair gap, $1.00 \times 10^{-20}$, which is
what an exact contact point dilated by $1 + 10^{-20}$ leaves.
The nine jobs made 474,246 pair decisions in 176.28 route CPU seconds and 227.80 job
wall seconds, summed; the longest job took 33.87 seconds.
The one-worker `certify` took 4 minutes 47 seconds of wall time, 07:29:54Z to 07:34:41Z,
at a load average of 7 to 9 on four cores.
A fresh serial `check --replay` decided all nine jobs again, equal to the retained rows
apart from timing, in 4 minutes 33 seconds, 07:40:01Z to 07:44:34Z.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the source’s code.
The third exact route (`devtools.check_half_angle_area`) has not read these
certificates.

## What Was Not Replayed

The other 69 declared certificates were not replayed, and 51 was not derived.
The kernel jobs measured here and for the pricing run of this lane (2.1 seconds a job at
51, 23 at 146, 52 at 270 and 65 at 308, at a load of 15) put the 69 at 75 to 125 minutes
of one-worker wall for `certify` and as much again for `check --replay`, no job near the
kernel’s 600-second limit.
The 14 below the case and not replayed (129, 153, 154, 156, 175, 176, 204, 207, 232,
264, 271, 302, 303 and 304) are 17 to 28 minutes of that.
At the 40 counts where the side equals the case’s, a replay would decide again a side
the record already holds.

## What Is Not Established

The replay establishes that the three dilated packings at 211, 237 and 241 are packings,
at the exact sides their certificates state.
It establishes nothing about the 69 certificates not replayed, about 51, or about
optimality, rigidity or KKT conditions, which the source does not claim.
The source’s own checks are the author’s reports; no source program ran here.
Apart from 211 and 241, read against Couzo’s `b85dee2` files, this packet compares sides
only. It has not compared poses, so where a side equals or nearly equals an earlier
report’s it makes no finding of copying or of independent rediscovery; the thirteen
byte-identical files are a fact of the manifests, not a finding about how they were
made.

## Credit

The issue credits the release to Mishapolk, under two spellings of the author’s name,
and names a lineage for every count: earlier finders “conquered” through optimizations
it attributes to methods (“exact dual-verified optimum”, “Ostashev composition optimum”,
“V-band continuous relaxation”, “cut-out optimum from s(302)”). At 129, 176, 303 and
304, where the sides are within $10^{-30}$ of Daniil Ostashev’s earlier #562 and #575,
the lineage names Ryan Xu, SQUISH and Couzo and not Ostashev, while it names the methods
those issues describe: a cut-out of the s(302) house at 129, a V-band merge at 176 and
compositions at 303 and 304. At 204 it names “Ostashev composition optimum”.
At 237, the one count where the release holds the smallest side, the lineage column
names Couzo’s #561. The issue discloses Gemini 3.8 assistance with solver scripting,
precision checks and formatting.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source mishapolk-records-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-records-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-records-2026-10-14 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-records-2026-10-14 derive --checkout CHECKOUT --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-records-2026-10-14 register-plan
```

`CHECKOUT` is a clone of the source at the pin.
`check-claims` and `check --replay` run offline from the facts; `derive --check` refuses
a checkout that does not yield this packet’s record and manifest, and compares each fact
it derives with the retained one.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-068.yaml.gz` | receipt | `e228236d6cf5c5307b01239a5777a51156c3702f` | `9d769cfc44dcb8b621e28e320c949b6f096b43bf068ce10149d1d15d689c86d0` |
| `facts/n-070.yaml.gz` | receipt | `d8c2d1ac994e0a748682e77a2217d548eb72cf84` | `3045d3371b5257f3d48a449223d1b76bd66bebdf9b23586c68fd66aa81ea13f9` |
| `facts/n-084.yaml.gz` | receipt | `07117f9256965924c67edc63f5e878a4da04bc3c` | `4db415acff1e3175d95e8cf476aed4e46ced7cc0a93eaf7d3845135ff6e79226` |
| `facts/n-086.yaml.gz` | receipt | `254625fe0f35da267e8e8cc5ebe07537a257e899` | `2a7e9d4c9a91a79f7fe6e03601a26b132df741b23ccaa518727040826c162ffe` |
| `facts/n-088.yaml.gz` | receipt | `a3c7956df83bc5f836d4d175996fae813f5df128` | `ec6ae6c787dad7f4d141bac610a12b72bbad60882a9ce4115d8cbc64ef854e26` |
| `facts/n-102.yaml.gz` | receipt | `cab9aa5097bf5d7c3c1ca90291dd12b99f0e5da5` | `5a98371db70f076005c9fd38631ddd0f551e7f211a69b54d3ca371f9d84ce0e2` |
| `facts/n-103.yaml.gz` | receipt | `99bcfe670aef61cf42b1ab444dd2f55c98cce828` | `9e84bcb3db036cb09e5cd999d6671d3feaf4ab89cd59efcd8753cee1c09c5317` |
| `facts/n-105.yaml.gz` | receipt | `c98bd30a86b506bdd193d19123e4e88e4ba3416e` | `6a3f445bad39af1d26d948ac908ba0c2a51b0cce8247c1801748cc5c3704b28d` |
| `facts/n-106.yaml.gz` | receipt | `0bd345beb11a608f71073d4e5a012807a96bb1b4` | `ec70cc07767cda7e94af8e913ab20bcb30b938e720d2d1dcb4e7e4cbd00771b4` |
| `facts/n-108.yaml.gz` | receipt | `34266f10e966982f0495979b801a1f879de04437` | `511c28a39ddc4ba2e89d464872c5f13a5ff4c197bedeb696eeed616b4e71a3c8` |
| `facts/n-110.yaml.gz` | receipt | `70ae3dd8e866ba9a9d028374543e551790a8bc04` | `147af45e8201011ae8bd39faac52d215de70d8cf01617d0747c309732552080d` |
| `facts/n-123.yaml.gz` | receipt | `f4cd25e8dfc1bfdc9dd00f9e0d6c0381577d63c5` | `cb32bcbb24981d61bc7a05115e076f88d3cbe7ca1edd694f10c64239e6500278` |
| `facts/n-126.yaml.gz` | receipt | `2b3f5a0ea05ad0578bf8ce544e71e4694801740c` | `0e8f638857e2daf36ef554476abb3ed24eea1da4ba387ce7bf449deec79b0f8e` |
| `facts/n-127.yaml.gz` | receipt | `c1553634c70646dfcdbe8e9c863ccafea4507661` | `93a83fbdf4787c99f57be920d73e71e63e50131c7f1d448314486b019001c96d` |
| `facts/n-129.yaml.gz` | receipt | `39084f0816d0f935683c45004e8a1ad9629cee60` | `11a856741a56b564d694f5aadb4529d11145fc337ff63ff98c5821551fc03ca1` |
| `facts/n-130.yaml.gz` | receipt | `0ba9c9abf56e33b58e1fd3432bc8419833656a87` | `8edaf310dcb331b928e7c7c73f70892c324653dc1f7db3352cc6940eb2fd261e` |
| `facts/n-131.yaml.gz` | receipt | `d3bde57da3e5f7f0ffd9d28c035c795f3c542b47` | `1811f2f9acda0c92b057ae5cb7710cd8fce51ea079d9cf7f38e2ce8fd6562e05` |
| `facts/n-132.yaml.gz` | receipt | `0cfa325ba74037a54944a7df63dfbd27a017612b` | `a93b107da82c90e7a6a0a492defb53d808c78a31d5d85a176e52ac22e73e590d` |
| `facts/n-146.yaml.gz` | receipt | `b68191103610e36ffa0747aec355135f0d6391d6` | `aece951ba8307bdd2f5023eb97c5f9d6af0c5ec4a85cec1e3f282cfcd5edd439` |
| `facts/n-152.yaml.gz` | receipt | `d52c4ed5a6f0b2e8adbd1c326a032f3c1ea757a7` | `d3e3ebc2aca47ca40389daa4e7bd4fe3628d48d51e591f25f4759562f882bb08` |
| `facts/n-153.yaml.gz` | receipt | `a366d6686f832f9d4bbbdcd1679ce977aa50d102` | `429a8040f9552ad7fbf40bf83b3d0e81f72e328e54ac43d73485a75369bb5956` |
| `facts/n-154.yaml.gz` | receipt | `4e7ca75bb1d6a5c04efe598f929faf067bd80d20` | `7ead6ae892e360e27e4c0d88db58fe981d64e9c2b3040f313d19b4dcea0a2533` |
| `facts/n-155.yaml.gz` | receipt | `3793fccd3047fba714a5b4dad8709b08686d4321` | `44a608b13ab88e5fcc14ec25b370afac619525af9eee1ff6eaff6a9677c47fe5` |
| `facts/n-156.yaml.gz` | receipt | `ac34993044328243aa0f08f8eebb6bdeaceb9c60` | `6c7112acc38edabe13d2e974cc3eb4e8b3f2f24d1aa7a0b2d5c7f1aa4e5e3cc6` |
| `facts/n-172.yaml.gz` | receipt | `0911d29fa376450526011465843258c0224a3b16` | `cdfa26954e57473e673b2a66aa3f98c947a13caaecd679ecf2968dc6be0fdcf4` |
| `facts/n-175.yaml.gz` | receipt | `25d536f1fb66d68ce9e7c4e6ff829612cfce2083` | `29bc02997661de800760e139cac17366e42ac8b488c7099beb8677a96e365b20` |
| `facts/n-176.yaml.gz` | receipt | `3bce2b367f390a51459551de390acddf7b81ab95` | `2c62e604f9aa6d14faba119de3cc148c166e2019a35221b19b6bcbd4d79c15bb` |
| `facts/n-177.yaml.gz` | receipt | `10b52de6f9e880b848076c2cef32b69643c9552f` | `9bed08e4c35741d2b0e0794b89b333820745ae6794b8cf74ab8f1df048fb13ae` |
| `facts/n-179.yaml.gz` | receipt | `d790a52a5996acc322df50c18ddc2c7e57eb7ce0` | `9afe4bf817aaaa3fa40ac8c220f1553894cda5fb9787e84a8aabc0c5317b150e` |
| `facts/n-180.yaml.gz` | receipt | `4f9ed755faa8040e85f7add6a64a14cbdf2f3d17` | `2d77f4e2e2cfe0c074dcce84bef5518a53d85a2ad17e44a9ca848b9a16cd946b` |
| `facts/n-181.yaml.gz` | receipt | `cbd0f3a6b018a1788fade329c191935fc9c7b08b` | `28bb29851d4f9a986aa480d487be512e18ff32cbe58d64642a34eb9e0ac30b05` |
| `facts/n-182.yaml.gz` | receipt | `76996a736bd8d515db88cbcf9ee3e8102ca1ffe1` | `4ba75f7bc884cd846167cea98ac75e3b91442bf050837f8b3808f56d7d9b5a85` |
| `facts/n-199.yaml.gz` | receipt | `448923deeb4ca6ee1bc69fdf93c3e8f634fffe17` | `f431d8c4162c726cd42065d6ba6905ce8103cec9b25a141fa5f47dfb0629f4ba` |
| `facts/n-204.yaml.gz` | receipt | `8845c91154bde6847f29e001fd976e3254934608` | `ba64fb7d1f5bee8da03c511deed876169ca4d0e160054c2329837c1d2ccb3147` |
| `facts/n-206.yaml.gz` | receipt | `8b51dff2bcf41f453a0c3d642e21e014612a51ad` | `fa30e7c2979cccc5366e5c068c0d536b038437bf6c592a3eabc3c24801066cc7` |
| `facts/n-207.yaml.gz` | receipt | `be47c04182debcd2f9da5abbfdb0a320b114dd74` | `eca36bf68e398fcfa74f5eb6136992922700a51802bce6c8e39263f71e5527f8` |
| `facts/n-208.yaml.gz` | receipt | `95b7f1f9d53a7292aa4ceab91aad6ab4fe5da513` | `9406dcbcd3026bad751d5626f26c4d7e508a7d93e3361a3a47c0c82f4641d727` |
| `facts/n-209.yaml.gz` | receipt | `72cf5f0eb74837fac2856c6e9680f624343f11cb` | `7fe3b384421a9345829915faf8ecfe43b73aaaa2af289d83b930fc9ee92ccc82` |
| `facts/n-210.yaml.gz` | receipt | `36a0814977c1091d80ae14f01d227f8413aa7266` | `8e0387a138678bb434b575ba0d8346319a1880a8d7f9cfb5bb269acdf19de23b` |
| `facts/n-211.yaml.gz` | receipt | `a10c748e1be5c7a1929871f41904b04d6952c410` | `de5bb29a7d1b0ba6e70898f0935a88f7dd164bf0490e096bf5f1c3466baa5ace` |
| `facts/n-228.yaml.gz` | receipt | `077adbfbf4b73f114a384ff370c7ff9998918cef` | `4e569a3242fe9dac5c3d7a0c0b6bf683d3779dc56e8ad3286ea12787f4d7f3ab` |
| `facts/n-232.yaml.gz` | receipt | `78cb949dced1762ec6c9ea3166dc97780df6e780` | `a21ebaebcd64b4ade9878790c5fa54f7ebda8f4d8aabaa3bdf45554481a0cbd0` |
| `facts/n-236.yaml.gz` | receipt | `993bc11440a80fd2ee49f9cf2ef355fec6a1d994` | `e1a685c7cbf01149861442153e53c0f042b82b4bb98844b16f6011deb890e33e` |
| `facts/n-237.yaml.gz` | receipt | `dd893655b28dfcb79eb7cf8ceb671b8a3d8c29e6` | `81b497b9c460e2f33cfb6c7af43814673c397f4a9e7b58f0c22a0372da869816` |
| `facts/n-238.yaml.gz` | receipt | `bda3ecd98e2e492084198a16d6aa11a461130fc9` | `99adcf7d63b456bbb04a458fec17d146e0dde2d5d4afe310b7c5cc250cbedc28` |
| `facts/n-239.yaml.gz` | receipt | `2b10f10fcc0a600c725e21b3b477ef045630e044` | `a6094080c8fc28e63c60e793accdc1ab234adf75c0d067877d07c5bad7a0fa2b` |
| `facts/n-240.yaml.gz` | receipt | `4df3aa0bf892e96fdc696917c788e66dcb3c08b6` | `9cff399ade92e690c145fcea677f9588d9bb2ded464862051b133184cf2862b3` |
| `facts/n-241.yaml.gz` | receipt | `4164c7bfd6f5913c5d18399c9844740259da0f90` | `7d8e9174dcb103dc0a832b5c4b9f031eeecd2e7b3b091732710e98b5445c0e0e` |
| `facts/n-258.yaml.gz` | receipt | `cc55757ba78af3a791851b6d69f3127225d8e119` | `34808de995f941d31dc735b7169b6af0e40a137449cc91ca4f1d491fee3cb8a8` |
| `facts/n-259.yaml.gz` | receipt | `02e1a3c420fabaa8eea20a018582c76c5f244f97` | `98b5372f254ea5af7e086cda00e320d53260dbab8696c2c48544d5e3daaa4341` |
| `facts/n-261.yaml.gz` | receipt | `4fa20c75f0c53cf31bd7a411f4cfdf7e0aa3eb44` | `6bd5021db186b2552bab1db6ecae46a70479e5d7b331b3c498c9403f9e124a9e` |
| `facts/n-263.yaml.gz` | receipt | `d61cfb6197a1f3743d222fe7ce8a1354816d4389` | `aa7bc3d6ce4c78879274702e2256c3878dc6e1545b9c9cb8c1a9d6143c7b9a61` |
| `facts/n-264.yaml.gz` | receipt | `09b8c7b6ca811f8c2ed75e9dfab13cbfa8ea8dd6` | `543ac6c59ae80c5da8294766c848b9c47c39a106d040062ceb2c22f294d871bd` |
| `facts/n-266.yaml.gz` | receipt | `0d72500a115fe0ca135f095ff452eefe79663a19` | `639108f2969596214e7144701ec82cf700c7f676709bb8b2e76090aa992bb351` |
| `facts/n-267.yaml.gz` | receipt | `fb062c855e1dbaa07a4e2426a4f85e1f5f1cd6ce` | `0012fddb3aa9693df10122ce1d588693c72893e1f8eb536a03727f4568c7d0a6` |
| `facts/n-268.yaml.gz` | receipt | `4d52604f512642884de70698f355754b9a3b4c4a` | `4ef6013316599d6291d596095a6316978784f42615389c0f2bf6c839ec422d57` |
| `facts/n-269.yaml.gz` | receipt | `25f069509a5dadccc15c27f9ec898bc6db4169b7` | `acac8cb97a8fb7a08bb109e019b831a686330db65e44baec61820e84c7450305` |
| `facts/n-270.yaml.gz` | receipt | `d0535013ebcf3f832992d114b7f9f3ae94eb0208` | `b88d4c3093461ab435886ff2a128723d5e0fbd4521f7725177720774feb0f601` |
| `facts/n-271.yaml.gz` | receipt | `eeca6bede517f6d513ea7d5d9c2b4949fa5e1f7b` | `8e0c31f287ad6e5772424ab2490db7dd921cb7ae601f295c8d9b85e6839f558e` |
| `facts/n-272.yaml.gz` | receipt | `6503897b871a4bbe9f5efecd4f4b3f8fe4cf3e7e` | `832efa30c3bf60c653144ceb12290ec5a26699e4855ce33a8f58ac5775fe4a9e` |
| `facts/n-273.yaml.gz` | receipt | `c52b7766680640528159db082968a9781925e832` | `c51e98d4a30481a6a1fa69041153052f0887ab8b49f4fe99bda281e2363595c2` |
| `facts/n-292.yaml.gz` | receipt | `501471077cec8809c9f58b335525d65a04c34f56` | `c1882a9457ec5b03430b392843482b131eb1b2b5835979c2f86d6db3b3fed40d` |
| `facts/n-295.yaml.gz` | receipt | `2548135edaf2632006ca3f7a6b6c49dd0f70e5c3` | `e4a10e65af68f6e9e97732976392e1a979c8015f0fe3e440fbc537e3117aaf98` |
| `facts/n-297.yaml.gz` | receipt | `7ec7c3dfb815e429ff4a75abe749d13f4e9aa85e` | `969afb4e0d3d936a7be828e4bf96a4515ebe8513574b8fb5ec06204113342314` |
| `facts/n-301.yaml.gz` | receipt | `70c2c61e2f27c02e34ecd2c520d113801800acd5` | `6fb4dc9c14241f93530f8acd48ef59b77ee1e522e20f06ff3123baa611469f90` |
| `facts/n-302.yaml.gz` | receipt | `f00fc5dcc6a716bd0e0525ceb346f0a9365d669a` | `01da6c547809833f0e491d0ff4b87c78c6ea45b3ad519c2277ff478d8aefaf54` |
| `facts/n-303.yaml.gz` | receipt | `6f547a1a395253ada1aeca8c212afb371abee24d` | `0626be5b141573bf03d73d23feaa66478f98ef07dfbf6c36a2ca72ba943dd0df` |
| `facts/n-304.yaml.gz` | receipt | `933ed1a75e20d4490190f0b745c5a212d71207da` | `c31f7daa05bf871c22f8580c064ee17cea916651feb0c95913271a9fbae0b214` |
| `facts/n-305.yaml.gz` | receipt | `bf2cca17e3a50b681704a5afed76ddfa2562b18f` | `7a39ec72a35f5c15cc1e5e1297cc180c7ed627a962d48f56d12f268f2f4e897b` |
| `facts/n-306.yaml.gz` | receipt | `21b7ca6033a893abeb4e0936b32047232a9e58f1` | `620a5537fd3c36bf1afa3bf09df5d7596fff31be75f993464bd318b200361d74` |
| `facts/n-307.yaml.gz` | receipt | `f4f43e7cb395255bfca00cacebbc0f397932ee57` | `c351eca2fdbb778839d2bf667b07b19f640e68be171e73818a0510f78fa2e031` |
| `facts/n-308.yaml.gz` | receipt | `d29e87040edce00f7e58f95b4b6176f5cb1f5baa` | `f1603163017f4e8c47e5300414aac1dd766799a8a2ea8737bdf977574bde8431` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
