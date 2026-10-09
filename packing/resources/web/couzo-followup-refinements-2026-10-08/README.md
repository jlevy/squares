# Francisco Couzo: Five Follow-Up Exact Rational Refinements

A [comment on pull request #460](https://github.com/jlevy/squares/pull/460#issuecomment-6070798890)
reports smaller exact rational certificates at $n=84,86,105,175,270$, published in
[the pinned source](https://github.com/franciscouzo/square-packing/tree/2d32a6e96f55c5dc1a2dd0e3581098e7c0105252)
(commit `2d32a6e`, tree `1e98bf6`, committed 2026-10-08T22:12:27Z, parent `ffd900d`).
This packet keeps those five certificates as derived exact facts.

The author starts from Ryan Xu’s #432 packings at 84, 86, 105 and 175 and from Evan
Daniel’s #399 packing at 270. Couzo’s basin hopping refined 84, 86, 105 and 270; David
Ellsworth’s refine_packing followed by Evan Daniel’s fq refined 175. Evan Daniel’s exact
contact solver wrote the certificates. The commit credits Claude under Couzo’s
direction. These are source attributions, not independent priority findings.

The author reports that all five pass Evan Daniel’s `verify_cert.py` and a copy of this
repository’s `sqpack` verifier, lie within about $10^{-19}$ of a KKT point and admit no
first-order descent. Those statements are author claims here; no author program runs.

## Source Custody and Retention

The repository has no licence file, and its README states no reuse terms.
`certificates/README.md` names the MIT-licensed solver that wrote the certificates, which
does not license this bundle. Under the
[existing retention policy](../known-best-packings/README.md) this packet therefore keeps
no upstream byte: no certificate, decimal pose, SVG, README or program.
No redistribution permission or licence determination is asserted.

[`acquisition/sources.json`](acquisition/sources.json) records the commit, its parent and
all 136 leaves of the pinned tree, with `raw_asset_retained: false`. Each of the five
[facts](facts/) is an exact rational `center-basis` Witness/v2 converted from the
certificate’s centres and half-angle parameters. It is the deciding witness of the
maintained exact route.

From `packing/`, with the project interpreter, the offline packet check is:

```bash
python -m devtools.couzo_followup_reports check-packet
```

It rebuilds the pinned tree root from its leaves, recovers every half-angle exactly from
the facts and rebuilds each certificate’s exact text and Git blob identity.
It also confirms that the seven other certificates at this commit, $n=108$, 127, 131,
155, 180, 228 and 306, and their decimal poses are byte-identical to the
[issue #451 originals](../couzo-exact-refinements-2026-10-08/README.md).
The earlier $n=105$ certificate in that packet is unchanged and remains valid; the new one
is smaller.

The decimal poses `n84.txt` to `n270.txt` are source context, held by identity with
their printed sides quoted. Only the five rational certificates enter geometry
decisions. The same commit also changes the outside-horizon `n375.txt` and `n378.txt`;
this packet records their identities and printed sides only, and their claims stay with
the [outside-horizon packet](../couzo-extended-reports-2026-10-09/README.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
