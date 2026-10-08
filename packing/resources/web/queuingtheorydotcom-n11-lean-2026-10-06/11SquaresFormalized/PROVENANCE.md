# Source provenance

## Verified integration into 11SquaresFormalized

This update is based on 11SquaresFormalized main commit
`b237948fa44eb8876ed87eeb21329ab5577c833c` and preserves that repository's history.
It imports the exact Lean source trees, pinned dependency configuration,
numerical inventories, and verification tools from 11SquaresEvolving commit
`1bf942a7af1ea330e95489d8997deebd4227ca71`, whose completed run is documented in
[VERIFICATION_20261006.md](docs/VERIFICATION_20261006.md). Only documentation,
portable evidence, and manual workflow configuration are adapted for this
repository. T03 and the public optimality statements are unchanged from the
previous main branch.

The proof uses Lean's kernel and native compiler for the approved numerical
certificates. The previous source export's unfinished-status statements below
are historical and are superseded by the successful full replay and final audit.
Development histories from the separate source export are not added as ancestors.
Third-party notices and attributions remain in place.

## Earlier source export history

This repository contains a standalone source snapshot of an eleven-square packing formalization and its proposed simplifications. It starts a new Git history with a generic project identity, rather than importing development commits or personal metadata.

The initial source snapshot corresponded to checkpoint `34e6b03536469379445bc7f87119cbb06d118f77`, following the recovered simplification checkpoint `dac90e2f02d4afe8482096e13b9dcf546d871fde` and earlier integration base `c82cff63e48b2d3f2da60cb998bbab48e557c012`.

The selective-native update copies the Lean source tree from checkpoint
`7d688b83e4087743df699b9dffaa8a5b9ac34194`, based on the later certificate-data
checkpoint `e5200e0ef5b75c9f3d4d59d59a6d410bb00554dd`. These are provenance
identifiers; development commits are deliberately not imported as ancestors.
The update is committed on this repository's existing history and retains its
runner configuration, diagnostic/checkpoint packaging, and license notices.

The formalization incorporates the published certificate checker and results from [wand125/n11-optimality-lean](https://github.com/wand125/n11-optimality-lean), including the source identified by upstream revision `a8b51d3e0682beb1bf911048bdc8e7fa62329124`. Existing third-party source credits are retained. Dependency repositories and exact revisions are listed in `lake-manifest.json`; dependency sources and build caches are not copied into this repository.

The initial selective-native copy matched that checkpoint byte-for-byte. A
subsequent compatibility fix removes unnecessary `noncomputable` modifiers from
119 finite data definitions in eleven baseline field modules. Their types and
bodies are unchanged; `verification/native-data-compatibility.json` records both
the original and executable hashes. Selected numerical certificate proofs use
`native_decide`; ordinary geometry, checker soundness, and assembly proofs retain
their proof terms. The final
theorem therefore inherits trust in Lean's compiler from the numerical checks.
Other publication adaptations concern documentation and the runner's explicit
trust reporting and compiler diagnostics. Source preservation does not establish
correctness of the assembled theorem; its full production replay remains outstanding.

Third-party notices accompany the export in `integrations/wand125/LICENSE`, `integrations/wand125/UPSTREAM-LICENSE.txt`, and `integrations/wand125/EVAND-LICENSE.txt`. These retain the published MIT notices; this document does not assign a new license to other project material.
