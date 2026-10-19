# Packing 229 unit squares in a square

An exact rational certificate proves a feasible enclosing side of **15.650174756949**, improving the [website-listed packing](https://jlevy.github.io/squares/cases/229.html) of side 15.65685424949238, checked on 17 October 2026.

| Unit squares | Website-listed side | Certified decimal upper bound |
| ---: | ---: | ---: |
| 229 | 15.65685424949238 | **15.650174756949** |

![Before and after](figures/n229_before_after.png)

Orange marks changed near-contact adjacencies at a distance threshold of 0.001 unit, after a documented noncanonical matching of squares. It is a descriptive comparison, independent of the exact feasibility proof. The diagrams use the actual packing coordinates.

## Files

- [Coordinates](n229_record.json), [SVG](n229_record.svg), and [PNG](n229_record.png).
- [Exact rational witness](n229_exact.json) and [equivalent text certificate](n229_record.cert).
- [Proof and audit report](n229_proof.pdf), covering all three results from this campaign.
- [Self-contained proof package](n229_proof_package.zip).
- `figures/`: side-by-side PNG/SVG and matching metadata.
- `records.json`: numerical-source provenance and exact-witness SHA-256.
- `SHA256SUMS`: hashes of all files in this folder except itself.
- `audit/`: dated audit receipts, covering all three packings (227, 229 and 260).

The JSON with centers and angles is a convenient floating-point illustration. The exact rational JSON is authoritative. The decimal upper bound rounds its exact side upward to 12 decimal places. The field `validators_passed: 2` in `records.json` counts the two separating-axis checks; the audit added the third (polygon clipping).

## Reproduce verification

Python 3.10 or later; standard library only:

```bash
python3 -B verify_all.py
```

All three exact algorithms check square count, unit geometry, walls and every pair, allowing boundary contact. Two implement separating-axis projection with different geometry code. The third computes convex polygon intersections using rational clipping and exact area. All were implemented within the same AI-assisted campaign and share Python Fraction and rational witness inputs. Outside independent review is not claimed.

To regenerate the figures, install NumPy, SciPy and CairoSVG and follow [VISUALIZATION_METHOD.md](VISUALIZATION_METHOD.md). Rendering is optional for proof replay. Regenerated figures will have different file hashes.

## Credit and scope

The numerical search, rational certificate construction, checking and visualization were performed with OpenAI Codex agents under the direction of Joost de Winter (JoostdeWinter). The comparison packing is credited on the linked Squares Project case page. The comparison used the jlevy/squares catalogue at commit `804eff369193b698d497a9c06847059eb9de0470`.

These are feasible upper bounds, without a proof of optimality or exhaustive worldwide novelty. The 227-, 229- and 260-square improvements belong to one related construction family (Young-corner/slipped-ribbon); the 229-square packing descends from the 260-square packing.
