# Francisco Couzo: Later Reports at n = 375 and 378

This packet retains derived decimal facts for $n=375$ and $n=378$ from
[Francisco Couzo’s publication pinned at 2d32a6e](https://github.com/franciscouzo/square-packing/tree/2d32a6e96f55c5dc1a2dd0e3581098e7c0105252)
(tree `1e98bf6`, committed 2026-10-08T22:12:27Z, parent `ffd900d`). Both counts exceed
this project’s $1$–$324$ case corpus.
The [acquisition record](acquisition/sources.json) and [numerical facts](facts/)
preserve every printed side, centre and angle as a string.

| $n$ | Side at 2d32a6e | Side at ffd900d | Below it by |
| ---: | --- | --- | ---: |
| 375 | 19.907024692022954 | 19.907052698737502 | $2.80 \times 10^{-5}$ |
| 378 | 19.946861170999796 | 19.947426312032292 | $5.65 \times 10^{-4}$ |

The commit message says the two counts “improved by the continuing search” and names
Claude as a co-author, disclosing AI assistance.
The source README compares each side with a derived border-row or grid reference, not a
survey of published best records.
These are author reports, without geometry replay, native execution, exact certificates,
confirmed feasibility or optimality here.
The source states no feasibility tolerance or checker for these decimal poses.

## The Earlier Reports

The [ffd900d packet](../couzo-extended-reports-2026-10-08/README.md) keeps the earlier
reports at both counts, unchanged and still pinned: a later revision is a new packet.
In the source register, `beyond_horizon_claims` in
[`source-coverage.yaml`](../../../frontier/source-coverage.yaml), its two rows stay as
dated history, with `disposition: superseded` and `superseded_by` naming this source,
and this packet’s two rows are the current ones.
`devtools.check_source_coverage` holds every row to its source’s reparsed claim byte for
byte, and requires each later side to be strictly smaller than the one it supersedes by
exact comparison of the printed decimals, from a source dated no earlier.
Smaller decimals are a comparison of reports, not of verified geometry.

## Source Custody and Retention

The pinned tree has no licence file, and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md) this packet keeps no
upstream byte: no decimal pose, SVG, README or program.
No redistribution permission or licence determination is asserted.

The acquisition record keeps the commit, its parent and all 136 leaves of the pinned
tree, with `raw_asset_retained: false`. Each case records its source file’s identity:

| $n$ | File | Git blob | Bytes | SHA-256 |
| ---: | --- | --- | ---: | --- |
| 375 | `n375.txt` | `96f21d6cc851d453a1f8da202667f33f29304cb6` | 27,240 | `cdcb176cec3fff245aa05705322c9cee3fefaac71ddf1072d6ec6d9374f9d103` |
| 378 | `n378.txt` | `4179d7d494138075487af04722df01a57a8ee6c0` | 27,316 | `dbd3cc98ab671dc96be094c3e99e3d3ac0388973be1a45a4bf40cf8eb18339bc` |

The tree and both blob identities are the ones the
[follow-up packet](../couzo-followup-refinements-2026-10-08/README.md) recorded at the
same commit before this import, which kept only identities and printed sides.
The two reports hold 753 poses in 54,556 bytes.
Every side is the `.15f` rendering, and every coordinate token the `.17e` rendering, of a
binary64 value, as in the earlier packet; the author’s computation precision is
unverified.

`acquire` read a local object store fetched at the pinned commit, never a checkout, and
ran no author program.
It holds the tree to the follow-up packet’s record and to its pinned root, and each input
to its blob identity and length, before parsing it with the existing `parse_couzo`
header parser.
The offline packet check rebuilds each source text from the retained facts and runs the
same export on it; every retained file must be what the export writes, byte for byte.
It validates the representation, not nonoverlap or containment.

From `packing/`, with the project Python 3.14 interpreter:

```bash
python -m devtools.couzo_extended_updates check-packet
```

No result row, case, selected bound, witness-corpus entry or atlas entry is created.
The outside-corpus reader work remains owned by `think-1545`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
