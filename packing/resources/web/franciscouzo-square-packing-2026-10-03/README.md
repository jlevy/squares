# Francisco Couzo’s `square-packing` at 3 October 2026, Retrieved 2026-10-05

This packet records the revision of
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing) that
follows the one the [27 September packet](../franciscouzo-square-packing-2026-09-27/README.md)
retains. Its one commit, “new records”, lowers the packings for seven of the 49 counts,
`n = 208, 209, 228, 263, 272, 303` and `306`, and leaves the other 42 byte for byte.
Each new side is below the one it replaces and below the Kingbird catalogue as this
record last captured it, on 30 September 2026.
Its Frontier key is **[franciscouzo square-packing 2026-10-03]**, and the result is
registered as T-092. No issue asked for it: the intake sweep of 5 October reported the
commit past the earlier packet’s pin (bead `think-ipbg`).

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `6042c56b43b64c09fe5a32c64879e698f399beaf`, tree `bb542bf7fc3ad77123b1658eb6a9ad99c8780c9b`, authored and committed 2026-10-03T12:33:31Z |
| Follows | `f3c5a529c255b546db18605702b8da298132309f`, retained in [`../franciscouzo-square-packing-2026-09-27/`](../franciscouzo-square-packing-2026-09-27/README.md); this is the only commit between the two |
| Changes | `n208`, `n209`, `n228`, `n263`, `n272`, `n303` and `n306`, each `.txt` and `.svg`, and their rows of the README table; the README also pictures `n = 208` and no longer pictures `n = 305` |
| Author | Francisco Couzo, read from the commit metadata: the repository still has no LICENSE and its README names no author |
| Credit | The README names no prior work beyond the catalogue it compares against, so nothing is credited after the author. The repository states no AI assistance; its author said on [jlevy/squares#227](https://github.com/jlevy/squares/issues/227) that he found the 102 and 103 packings “with the help of Claude” |
| Licence | None published |
| Retrieved | 2026-10-05, a full clone |
| Retained here | Derived facts and metadata only: [`facts/`](facts/), one Witness/v2 witness for each of the seven changed counts with the source’s centres and angles carried verbatim, and [`acquisition/sources.json`](acquisition/sources.json), which pins all 99 upstream files at this revision by SHA-256 and records each of the seven counts’ commit history with every side it has printed |
| Not retained | The packing files, their SVG renderings and the README, under the derived-only form of the [known-best retention policy](../known-best-packings/README.md), as in the earlier packet: no raw asset is kept (`raw_asset_retained: false`) |

The acquisition record names the earlier packet under `supersedes`, and keeps facts only
where the printed side changed since that pin; the 42 unchanged counts stay with the
earlier packet. `python -m devtools.upper_bound_packets acquire --source
franciscouzo-square-packing-2026-10-03 --clone PATH` writes both from a clone at the pin.

## Certified Here

`python -m devtools.upper_bound_packets certify --source
franciscouzo-square-packing-2026-10-03` runs the procedure the earlier packet’s
[Certified Here](../franciscouzo-square-packing-2026-09-27/README.md#certified-here)
describes on the seven new poses: each is promoted to an exact rational packing
(`robust-rational`, 36 digits, side increase at most `1e-9`), and every pair and wall is
decided over `ℚ` by the promotion’s exact separating-axis test and again by
`devtools.check_rational_witness_independent`, which shares no code with it.
All seven promoted at centre dilation 1, so each certificate is the author’s packing, and
each certificate’s side differs from the printed side by less than `1.8e-15` either way.
The certificates are under
[`packing/witnesses/franciscouzo-2026-10-03/`](../../../witnesses/franciscouzo-2026-10-03/)
as deterministic gzip; [`receipts/certification.json`](receipts/certification.json)
records each one’s digests, exact side, pair count, both verdicts and walls.

The verified upper bound a case carries is the larger of the printed side and the
certified side rounded up at the printed fifteen decimals.
That is the printed side at `n = 228, 272` and `303`, and one unit of the fifteenth
decimal above it at `n = 208, 209` and `263`, which `bounds_agree_at_declared_precision`
accepts as the same bound.
At **`n = 306`** the rounded-up certificate sits 2 units above the printed side, so that
case record carries the certified value, a `replay-failure` conflict and a `mathematics`
blocker, and the printed side itself is not certified. The certified value there,
`17.963438139777141`, is still below the earlier packet’s `17.963449907261179`.

Two negative controls on the `n = 208` certificate, its side cut by `1e-15` and square 2
moved right by `1e-6`, are refused by both checkers:
[`receipts/negative-controls.json`](receipts/negative-controls.json).
Square 2 is the first whose move makes an overlap, with square 51.

The certification took 264 s of wall time on four workers on 5 October 2026.
Replay, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_packets \
  check --replay --source franciscouzo-square-packing-2026-10-03 --workers 4
```

## Interval Route

`python -m devtools.upper_bound_intervals certify --source
franciscouzo-square-packing-2026-10-03` decides each printed pose again, as the earlier
packet’s [Interval Route](../franciscouzo-square-packing-2026-09-27/README.md#interval-route)
describes: decimal fixed-point intervals of 40 digits rounded outward, with each angle’s
cosine and sine enclosed, and the facts rebuilt into each upstream file and matched to the
size and SHA-256 the acquisition took from the clone.

- **Pairs.** 228,845 of the 232,869 pairs are separated by bounding circles, decided
  exactly on the printed centres, and the other 4,024 by the separating-axis test over
  the four edge normals. None needed more than 40 digits, and none touches. The least
  gap is `1.99e-13`, at `n = 306`.
- **The verified value** equals the exact route’s at every count, and the exact
  certificate’s side lies within `2.3e-40` of the enclosure of the pose’s extent.
- **The printed side fits the printed pose** at `n = 228, 272` and `303`. At the other
  four the pose’s own extent exceeds the printed side by `2.9e-16` to `1.76e-15`: one
  unit of the fifteenth decimal at `n = 208, 209` and `263`, and 2 units at `n = 306`,
  exactly where the exact certificate rounds up.
- **As placed in the source’s own frame,** the poses at `n = 272` and `303` lie inside
  `[0, s]²` for the printed `s`; the other five cross a wall by up to `1.76e-15`, so each
  bound is the translated pose’s, as in the exact route.

Three controls on `n = 208` are refused: a side `1e-15` below the extent, square 2 moved
right by `1e-6` (one overlap, with square 51), and the angles read as degrees (82
overlaps). The receipts are
[`receipts/interval-certification.json`](receipts/interval-certification.json) and
[`receipts/interval-negative-controls.json`](receipts/interval-negative-controls.json).
The replay takes about a second, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_intervals \
  check --source franciscouzo-square-packing-2026-10-03
```

## The Seven Counts

Generated by
`uv run --frozen --all-extras --group dev python -m devtools.upper_bound_packets table --source franciscouzo-square-packing-2026-10-03`.
“Side it replaces” and “Verified before” are the earlier packet’s printed side and the
verified value it gave (T-056).
The Kingbird column is the retained capture of 30 September 2026; the live page was not
read, because `kingbird.myphotos.cc` was unreachable from the session that retained this
packet. It was read later on 5 October, at 22:39Z, and served the same bytes as that
capture (SHA-256 `b99c3265…`), so the column is the live page’s too.

| n | Side printed | Authored (UTC) | Certified side | Verified here | Side it replaces | Verified before | Lower by | Kingbird, 2026-09-30 | Casson, 2026-09-23 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 208 | `14.926534459703511` | 2026-10-03 12:33 | `14.92653445970351144714…` | `14.926534459703512` (+1 unit) | `14.937018796984567` | `14.937018796984568` | `1.048e-2` | `14.93776656277905` | `14.93761283595916289` |
| 209 | `14.953939011860642` | 2026-10-03 12:33 | `14.95393901186064228780…` | `14.953939011860643` (+1 unit) | `14.955041639430016` | `14.955041639430017` | `1.103e-3` | `14.95861500087481` | `14.95856148981292932` |
| 228 | `15.604602454552252` | 2026-10-03 12:33 | `15.60460245455225174639…` | `15.604602454552252` | `15.604638007678682` | `15.604638007678683` | `3.555e-5` | `15.60902282132495` | `15.60895620815939289` |
| 263 | `16.742270262031791` | 2026-10-03 12:33 | `16.74227026203179158598…` | `16.742270262031792` (+1 unit) | `16.742280159187313` | `16.742280159187314` | `9.897e-6` | `16.74264068711928` | — |
| 272 | `16.968165867864400` | 2026-10-03 12:33 | `16.96816586786439978569…` | `16.968165867864400` | `16.968279785326896` | `16.968279785326897` | `1.139e-4` | `16.96971602419903` | `16.96944950195848989` |
| 303 | `17.924341009860250` | 2026-10-03 12:33 | `17.92434100986024845032…` | `17.924341009860250` | `17.924349265547932` | `17.924349265547932` | `8.256e-6` | `17.93125509556197` | `17.93105636462953001` |
| 306 | `17.963438139777139` | 2026-10-03 12:33 | `17.96343813977714075435…` | `17.963438139777141` (+2 units) | `17.963449907261179` | `17.963449907261179` | `1.177e-5` | `17.96913960675661` | `17.96846609160515484` |

## Parallel Results

Griffin Casson’s packings of 23 September, in
[`../casson-square-packing-2026-09-23/`](../casson-square-packing-2026-09-23/README.md),
cover six of the seven counts, all but `n = 263`; each is larger than Couzo’s new side, as
it was larger than his earlier one.
Couzo publishes nothing at `n = 69, 83` or `87`, the three counts whose catalogue sides
wait on their own intake.

## Review

The import’s review lane read this packet, its certificates and records, and the tooling
changes on 5 October 2026, with no blocking defect:
[review-2026-10-05-couzo-6042c56.md](../../../../docs/project/reviews/review-2026-10-05-couzo-6042c56.md).
It ran both replays and the controls again, decided all seven packings a third way with
its own code, and checked this packet against a fresh clone of the source at the pin.

## Not Done Here

- `n = 306` needs a pose refined beyond the source’s binary64 digits, or
  higher-precision coordinates from the source, before its printed side certifies.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
