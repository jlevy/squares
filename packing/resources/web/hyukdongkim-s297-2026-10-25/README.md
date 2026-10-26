# Hyukdong Kim’s Exact Side at 297, Issue 804

Hyukdong Kim reported on
[jlevy/squares#804](https://github.com/jlevy/squares/issues/804), in a
[comment of 2026-10-25T12:23:57Z](https://github.com/jlevy/squares/issues/804#issuecomment-6397593690),
that the stationary side of T-174’s packing at 297 is the only real root $S^*$ of an
irreducible degree-21 integer polynomial $P_{297}$, which the comment prints, and that
$s(297) \le S^*$. That is 3.36e-90 below T-174’s rational certificate, the case’s house.
He attached an exact configuration at $S^*$ under CC0 1.0.

The attachment could not be downloaded from the importing session, because the session
proxy answers user-attachments URLs with 403. **Route A** builds an exact configuration at
$S^*$ from T-174’s own retained certificate, with this repository’s tools. Deciding that
configuration exactly is the next step, which exceeded this import’s CPU cap. **Route B**,
deciding the author’s file, waits until the file is reachable.

## Source and Credit

| Field | Value |
| --- | --- |
| Comments | [issuecomment-6397363927](https://github.com/jlevy/squares/issues/804#issuecomment-6397363927), 12:00:41Z, and [issuecomment-6397593690](https://github.com/jlevy/squares/issues/804#issuecomment-6397593690), 12:23:57Z, both by HyukdongKim on 25 October 2026. Neither had been edited when they were read at 15:46:55Z. Their text is in `acquisition/comments-804.json`. |
| Attachment | [`s297-exact-configuration.zip`](https://github.com/user-attachments/files/33925868/s297-exact-configuration.zip), SHA-256 `e08b5d0a64c5c68eed827ee7e323687929048a4cfea438bb77ef390bdd4147a7` as the comment states it, holding `n297.minpoly.json` (`e5c340b8af2ff75d01b9b414e32ef19d9c3d07ecce665c8fddad9c5952252826`). Not downloaded, not measured and not retained. |
| Bibliography key | **[Kim s297 2026-10-25]** |
| Human credit | Hyukdong Kim, for the exact side, after the packing’s finder and improvers as the case record credits them: Francisco Couzo, improved by Evan Daniel and PingYou Ltd (T-174) |
| AI assistance | The comment says Claude (Anthropic) did the computation, the construction and the checks at the author’s direction, and that he reviewed and reran them |
| Licence | CC0 1.0, stated in the comment for this bundle. The 12:00:41Z comment states the same for the two earlier bundles, whose packets belong to think-4rzl and think-9vai. |

## What the Comments Report

At 12:00:41Z the author answered the import’s acknowledgement. He gave CC0 for both earlier
bundles and agreed to the method credit. He gave an uncertified second-order note for 172
and 263. At 297 he reported a KKT side solved to 1,500 digits, 3.36e-90 below T-174, with
no integer relation found. At 12:23:57Z he withdrew that last statement as an LLL acceptance
error and made the claim above:

- every centre and half-angle tangent lies in $K = \mathbb{Q}(t)$, where $t$ is the
  half-angle tangent of the 44.74° band, $K$ of degree 21 and $f$ of height 300667;
- 19 free coordinates were pinned to the record’s binary64 values, and five near-45°
  squares with free angles were snapped to their classes;
- `verify_exact.py` at evand/square-packing `659ee62` printed VALID, with 1750 touching
  incidences proved as identities in K, and a checker of his own also passed, with
  controls refused.

## What Is Decided Here

`facts/s297-polynomial.json` keeps $P_{297}$ and the printed side, read from the
comment as text by `campaign/issue-intake/upper-bounds-issue804-297-20261025/review/side_297.py derive`.
That program’s `sides` command decides $P_{297}$ primitive and irreducible over Q, by
SymPy and by `sqpack.field`. It decides that $P_{297}$ has exactly one real root, which
the print names. It decides that root 3.359e-90 below T-174’s certificate and 6.624e-63
below issue 639’s degree-12 side (`exact-sides.json` in that directory).

### Route A

`route-a.sh` runs `devtools.build_field_configuration` on
`witnesses/known-best/n-297.yaml`, T-174’s rational certificate. Its authors read the
comments as text and none of the author’s code. The polynomial $P_{297}$ is used only to
compare, after the side has been found in its field. Each step writes a receipt in
`receipts/`:

1. `contacts.json` holds the contact graph. Every contact margin in the certificate is
   below 1e-91, and every strict one is above 1e-11. That gives 67 edges flush with a wall,
   490 edge-to-edge contacts, 295 corner-to-corner and 61 corner-to-edge: 1,208 equations
   in 607 unknowns, rank 590. There are twelve rotation classes: the axis, four band
   classes at ±44.74°, and seven near-45° classes.
2. `solve.json` holds the stationary point. The contacts leave 17 free directions, and
   along some of them the side moves at second order. The KKT system (1,815 by 1,197,
   rank 1,183) is solved by mixed-precision Gauss-Newton to 2,600 digits in 175
   CPU-seconds, with residual below 1e-2609. The 14 directions it leaves free, along which
   the side is constant, are pinned to small rationals. Tangents are pinned first, so the
   five free near-45° turns (squares 195, 231, 236, 249 and 254) are rational. Squares
   249 and 254 touch nothing.
3. `field.json` holds the field. The band tangent’s minimal polynomial has degree 21 and
   height 300667, as the comment describes. It was found by integer relation at 1,430
   digits and holds to 1e-2600. SymPy finds it irreducible. The other determined tangents,
   classes 5, 6 and 9, lie in $K$ with relations of 35, 35 and 32 digits. The refined
   side satisfies $P_{297}$ to a relative 1e-2613.
4. `build.json` and `facts/route-a-n297.json.gz` hold the exact configuration. With every
   rotation exact in $K$, the centres and the side are solved exactly in $K$ (89 seeds,
   711 constraints), and all 1,208 contact equations are identities in $K$.
   $P_{297}(S) = 0$ holds in $K$, so $S = S^*$ exactly. The configuration moves no
   coordinate of the 2,600-digit solve by more than 4e-2519.
5. The decision is not yet made. `route-a.sh decide` runs `sqpack.witness.exact_verify`
   over $K$, driven by `devtools.algebraic_witness_reports`’ jobs, on the positive and
   on the duplicate-square and outside-container controls, and writes `decide-*.json`.
   On 26 October 2026, on a shared four-core host, the positive ran 89.8 CPU-minutes and
   each control ran 48 without finishing. All three were stopped at the item’s 5
   CPU-hour cap, so no receipt was written. The decision is think-vv1q, priced at about
   2.5 CPU-hours a job.

Until step 5 runs, route A shows less than the bound. It shows exactly that every contact
of T-174’s packing holds as an identity in $K$ at a side equal to $S^*$. It shows
numerically, to 2,600 digits, that this configuration lies within 1e-14 of the
certificate, whose strict margins are at least 1e-11. It does not decide feasibility.

### Route B

Route B waits on the author’s attachment. Once the file is reachable, check its digest
against the comment. Then decide `n297.minpoly.json` on `exact_verify` through
`evand_minpoly_geometry`, and replay the retained `verify_exact.py` unchanged in a
separate directory under `python -I`, as T-193’s replay did. Under CC0 the files may be
kept.

## Files

| Path | What it is |
| --- | --- |
| `acquisition/comments-804.json` | The two comments, as the GitHub API returned them |
| `acquisition/sources.json` | The attachment’s address and the digests the comment states; nothing measured |
| `facts/s297-polynomial.json` | $P_{297}$, highest degree first, and the printed side |
| `facts/route-a-n297.json.gz` | Route A’s exact configuration, a centre-basis Witness/v2 over $K$ |
| `receipts/*.json` | Route A’s receipts, one a step |
| `route-a.sh` | The commands that wrote them, from `packing/` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
