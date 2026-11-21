# De Winter’s Issue 997 Follow-Up at n = 90

[Joost de Winter’s comment of 21 November 2026](https://github.com/jlevy/squares/issues/997#issuecomment-7058975230)
submits an exact rational candidate at upward ceiling 9.994038766583. Both maintained
routes accept it, both gross controls are refused, and all eleven maintained sharp
controls meet their exact predictions.
Registration, review and adoption remain separate from this custody packet.

## Source and Attribution

The source is
[GitHub issue attachment 35205206](https://github.com/user-attachments/files/35205206/n90-rational.zip).
Its measured size is 39,377 bytes and SHA-256 is
c04a0a60ca91f15922f6077c878c50b654e759ee659c14d43096cadaae574afa. The author supplies no
checksum in the comment.
[acquisition/sources.json](acquisition/sources.json) binds the four retained factual
archive members to their raw sizes and digests.
The archive’s producer programs and prose are not retained in this packet or executed.

De Winter supplies this rational enclosure and names GPT6.2 Astra as his AI tool.
The comment’s source map names Sargis Khachatryan and jazivxt via the Nevska
compilation. Those source-map and Kaggle-score statements remain author reports here.
The predecessor T-304 is credited to de Winter after jazivxt.
The author explicitly submitted the source in this comment; the packet records that
submission and the retained-factual-data policy as its custody basis.
No specific licence is stated for these attachment members, and nothing is relicensed.

## Reversible Reading Copy

The comment defines each candidate row as exact centre coordinates and signed
counterclockwise half-angle tangent in the lower-left box.
The original candidate envelope is refused by the existing readers.
[The refusals](receipts/raw-original-adapter-refusals.json) are retained separately.

[normalize_candidate.py](normalize_candidate.py) verifies the raw acquisition digest,
preserves all exact scalar strings and row order, renames side to s_exact and places all
remaining original metadata under provenance.
The supported pingyou-json parser reads the resulting
[derived copy](derived/candidate-reading-copy.json).
[acquisition/normalization.json](acquisition/normalization.json) binds both files and
records exact reconstruction of the parsed original, including metadata and order.
The original input uses the maintained ono-json reader directly.

Run the normalizer with the project interpreter from packing and PYTHONPATH=.:src.
[acquisition/recipe.json](acquisition/recipe.json) gives the source, reader, profile and
artifact names. The original candidate SHA-256 is
3a8e8913d0b87ac0b68c3fc4ac24d6ad042074c9696a2cdbfae3682b2e0b96c7. The decoded source
SHA-256 is 5f58ac1e3f082df767237ae430180d64a09a7332b3d0b00015503cfa3c9e2099.

## Exact Comparisons and Feasibility

[The maintained first-contact comparison](receipts/contraction-T304-vs-followup.json)
puts the candidate below contracted T-304 by about 8.794239e-12. Its gain from T-304 is
2.698158e-11, or 1.4835 times T-304’s 1.818734e-11 margin.
The exact within-margin decision is false; both routes accept T-304 and its contraction.
This passes Option D’s comparison with T-304. The final input-to-candidate contraction
is only about 8.994039e-73 and within that input’s margin.
The candidate’s own contraction margin is exactly zero.

[The comparison with the earlier held solve](receipts/held-row3-comparison.json)
puts this candidate about 9.99404 × 10⁻²⁰ below the rational side certified by Evan
Daniel’s driver on 16 November. Both sides beat T-304 at first contact. The candidate
rounds to the driver’s 65-significant-digit display of the limiting side. That
display gives no certified root interval. The earlier held witness coordinates are
absent, so the comparison establishes rational side ordering only.

[Identity](receipts/identity-vs-T304.json) pairs all squares one to one under symmetry
0: largest move 0.0304373, with 17 beyond 1e-9, five beyond 1e-3 and two beyond 1e-2;
none moves beyond 0.1. The largest turn is 0.09344 degrees.
All 40 tilted squares pair with the same tilt sign.

[The eleven sharp controls](receipts/sharp-controls.json) all meet their exact
predictions. Their run took 77.03 seconds in one process under an observe-only guard.
The native gross-control rerun took 17.99 seconds; worker and guard exited zero.
[summary.json](receipts/summary.json) retains the measured comparisons and observer
summaries. Raw guard journals stay in dedicated external scratch.

## External Native Diagnostic

The maintained repository writer refused an external scratch output path.
[The refusal](receipts/writer-boundary-refusal.json) and its original stderr remain
intact. The coordinator separately authorized the lossless
[external diagnostic export](receipts/external-diagnostic-native-jobs.json.gz).
Its outer format explicitly identifies it as external diagnostics.
The receipt_payload field contains the three jobs that passed in-memory validation.
It is not a published native repository receipt.
The repository writer’s checks and kernel.REPO were unchanged.

The repository receipt is [exact-certification.json.xz](receipts/exact-certification.json.xz).
The maintained reader admitted all three validated jobs before its ordinary writer
saved them within the repository. The external wrapper remains a separate record.
The [independent review](../../../../docs/project/reviews/review-2026-11-21-de-winter-997-n90-rational-followup.md) also accepted finite feasibility.

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `receipts/external-diagnostic-native-jobs.json.gz` | receipt | `72fa49cbdfa833d234041c405be711bf9cb09ac8` | `fff243fdc1b47d8968ea04343a60af457161015108d62c4ebc93334c2dcd02da` |

## Original Gzip Files

| Stored file | Origin | Git blob of stored bytes | SHA-256 of stored bytes |
| --- | --- | --- | --- |
| `source/90/candidate.json.gz` | upstream | `a348275c6786bf75c1b8d684a90846de2b9163f1` | `3a8e8913d0b87ac0b68c3fc4ac24d6ad042074c9696a2cdbfae3682b2e0b96c7` |
| `source/90/input.json.gz` | upstream | `f66f68b048284b97c23bde6a768ef3f3c5f6bcc3` | `c519aa1822709897d541e7b83efdb027054ad636059bfb340acdb3e9c4a5fb9b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
