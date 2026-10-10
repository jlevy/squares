# Francisco Couzo: Twenty Reports Beyond the Case Corpus

This packet retains derived decimal facts for $n=327,332,335$–$342,364,369,372$–$379$
from
[Francisco Couzo’s pinned publication](https://github.com/franciscouzo/square-packing/tree/ffd900dfff6d2674ad995359208c2f0714915c82).
All twenty counts exceed this project’s $1$–$324$ case corpus.
The [acquisition record](acquisition/sources.json) and [numerical facts](facts/)
preserve every printed side, centre and angle as a string.

These are author reports, without geometry replay, native execution, exact certificates,
confirmed feasibility or optimality here.
The author’s comparison bounds for the expanded search are derived border-row or grid
references, not a survey of published best records.
The source does not state a feasibility tolerance or a checker for these decimal poses.
The eight in-horizon rational certificates in the
[separate issue451 packet](../couzo-exact-refinements-2026-10-08/README.md) have their
own inputs and receipts; none of their verification transfers to these twenty reports.

## Later Reports at n = 375 and 378

Read on 2026-10-09: the author’s next revision,
[2d32a6e](https://github.com/franciscouzo/square-packing/tree/2d32a6e96f55c5dc1a2dd0e3581098e7c0105252)
of 2026-10-08T22:12Z, reports smaller sides at $n=375$ (19.907024692022954, against
19.907052698737502 here) and $n=378$ (19.946861170999796, against 19.947426312032292
here). This packet is pinned at ffd900d and does not retain those two reports, so its
$n=375$ and $n=378$ facts are dated ffd900d reports rather than the author’s latest.
They remain valid dated reports.
Since 2026-10-09 the
[later packet pinned at 2d32a6e](../couzo-extended-updates-2026-10-08/README.md) keeps
those two reports, and the source register keeps this packet’s $n=375$ and $n=378$ rows
as dated rows it supersedes; their facts and this packet’s pins are unchanged.

## Source Custody and Retention

Three revisions are pinned: b10ad360f80ee82580e75330417e0171d1a9fb81,
74f7e8b3f8df9cd5c2277b54d3cd7fe00769a998 and ffd900dfff6d2674ad995359208c2f0714915c82.
Their complete nested Git trees bind paths, ordinary modes and blob identities.
The local acquisition checks all 73 named roles: three README contexts, forty current
TXT/SVG occurrences, the two earlier n378 occurrences and twenty-eight occurrences for
fourteen removed constructions.
It also checks the fixed parents and absence of the removed files in both later trees.
Author/message and size metadata are not authenticated by tree reconstruction.
The local ordinary check validates complete bytes and sizes for all selected roles; the
public derived packet reconstructs only the twenty current TXT identities.
The other source roles retain pinned identities without their raw bytes.

The complete ordinary preparation stays outside Git.
This packet contains numerical Witness/v2 facts and attributed metadata under the
[existing retention policy](../known-best-packings/README.md), with
`raw_asset_retained: false`. No redistribution permission or licence determination is
asserted.
Upstream text, SVGs, README prose and programs are not copied into this packet.

The maintained checker reconstructs each current TXT blob identity and complete byte
length from its retained numerical tokens and fixed source layout.
It refuses missing or extra inputs, altered roots or parents, malformed archives,
changed poses, symlinks, raw assets and unsupported verification claims.
Export writes the acquisition record in one fixed order whatever order the local
preparation used, and the checker refuses a record that differs from those bytes.
It validates the representation, not nonoverlap or containment.

Every side is the `.15f` rendering, and every coordinate token the `.17e` rendering, of a
binary64 value.
Export and the packet check both refuse any other encoding; all twenty sides and 21,312
coordinate tokens pass.
The Witness/v2 numerical method describes that checked compatible representation; the
author’s computation precision is unverified.

From `packing/`, the offline packet check is:

```bash
python -m devtools.couzo_extended_reports --check-packet
```

Use the project Python 3.14 interpreter.
The reported evidence atom and all twenty `beyond_horizon_claims` remain outside the
standing-case and result tables.
No result row, case, selected bound, witness-corpus entry or atlas entry is created.
The outside-corpus reader work remains owned by `think-1545`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
