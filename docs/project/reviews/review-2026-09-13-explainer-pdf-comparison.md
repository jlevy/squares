# Preserved Explainer PDF Comparison: A Page-15 Baseline Shift

Date: 2026-09-13. Evidence: the first attempt of
[Certificate page run 34774787868](https://github.com/jlevy/squares/actions/runs/34774787868).
Tracked uncertainty: `think-ptit`.

The publication check correctly rejected two PDFs that differed in the vertical position
of one word.
Their mathematical text, glyphs, font programs and other page content match.
The saved pair does not establish its DOM, font-layout or browser cause, or explain
earlier intermittent comparisons.

## Source and Retained Pair

The pull-request run reports head `cadbf7e149b65215724daf813add78d80879d327`. Its
checkout was the GitHub merge commit `a62d695d80df3ebae58106a095ef68c882a573fa`; both
commits have Git tree `0233d5a96df43194d2a5be08296aad44969f8377`. The build ran on
Ubuntu 24.04, runner image `20260907.300.1`, and the PDFs identify their producer as
Skia/PDF m151.

The workflow first drew the publication artifact with `--update`, then compared that
stored file with one fresh draw using `--check-artifact`. This attempt therefore
compared two production PDFs.
No DOM trace was enabled.
The failed pair and its diagnostic were downloaded before any rerun from artifact
`explainer-pdf-check`, ID `10323137895`; the prepared HTML came from artifact
`prepared-page`, ID `10322424640`.

| File in `pdf-check-644lkxd1` | Role | Raw bytes | SHA-256 |
| --- | --- | --- | --- |
| [reference.pdf](../../../packing/benchmarks/math-startup/runs/ci-34774787868/reference.pdf) | Stored publication candidate | 843,157 | `ea8a21929c8e7fe9b4a401b22e521e4fae9351617d0fb317ee5144a70f17b70e` |
| [replay.pdf](../../../packing/benchmarks/math-startup/runs/ci-34774787868/replay.pdf) | First fresh comparison draw | 843,157 | `e76ca05a908f8beef6bbea6a6d6237c951b38ca1a0d480499d304b5ee78fea32` |

The retained
[diagnostic](../../../packing/benchmarks/math-startup/runs/ci-34774787868/report.txt) is
unchanged. The exact prepared HTML is retained as
[deterministic gzip](../../../packing/benchmarks/math-startup/runs/ci-34774787868/index.html.gz),
with compression timestamp zero.
The
[provenance record](../../../packing/benchmarks/math-startup/runs/ci-34774787868/provenance.json)
binds each file to its source artifact, byte count and SHA-256 digest.

Both PDFs contain one source receipt matching the exact downloaded prepared HTML’s
digest: `955ad1ec8e161c3db5a0cbd4ce4479db6663340d9903c8a0f9b7882384d4d0d1`. Both have 22
letter-sized pages and the same 18 embedded subset fonts.
The repository’s exporter reports `font_findings=[]` for each saved file.

## Difference Established by the Bytes

The normalized files have equal lengths.
Their first difference is at byte 524772, inside object 156’s compressed page-content
stream. Byte forensics found all 1,298 parsed indirect objects equal after the existing
creation/modification-date normalization except this page-15 stream; all embedded font
objects match.

The decoded streams have exactly one changed text matrix, using `/F8 16 Tf`, the
embedded PTSerif-Regular subset:

```text
stored: 1 0 0 -1 257.32813 12994.2188 Tm
fresh:  1 0 0 -1 257.32813 12994 Tm
```

The following glyph codes spell “tan”, with unchanged glyph advances.
This is the operator in `tan d ≤ D` on page 15, **The Contradiction Argument**.
Poppler’s extracted top coordinate changes from 200.692300 to 200.528205 points: a shift
of 0.164095 points.
The word’s horizontal bounds remain 282.990842 and 300.630379 points.

## Independent Text and Visual Checks

On macOS 26.5.2, Poppler 25.05.0 extracted byte-identical full-document layout text.
Its bounding-box output differs only in the two document dates and this word’s vertical
bounds. All 22 pages of each saved PDF were rasterized on the same host at 96 dpi:

- 21 corresponding pages are pixel-identical;
- page 15 differs in 142 pixels within a 24-by-13-pixel box around “tan”;
- a 300-dpi comparison of page 15 confines its 530 changed pixels to that same word.

Both complete page-15 images were visually inspected.
The proof text, displayed contradiction and following compactness paragraph are legible
in both. No missing or changed mathematical content was found in this pair.
Raster conversion and text extraction did not rerun Chromium or create a replacement
publication PDF.

## Disposition and Next Evidence

Keep the exact stored-artifact comparison unchanged.
A matching text extraction does not make unequal publication bytes reproducible, and
this observation does not justify normalizing text positions or compressed streams.
The final math-rendering guard and source-receipt check address separate publication
failures; this pair passed those guards and still differed.

The next diagnostic can retain per-draw DOM geometry, computed fonts, font-load state
and raw PDFs, alongside the ordinary uninstrumented comparison.
Such observation may force layout or change timing.
Agreement under tracing must not replace the ordinary gate, and a later passing rerun
must not erase this failed attempt’s evidence.
The retained artifacts were configured for seven days; download them before rerunning
because earlier-attempt artifacts may become unavailable, as described in the
[artifact-retention guidance](../../../development.md).

The upstream cause remains open under `think-ptit`. No code, normalization rule,
mathematical claim or scientific admission was changed by this forensic review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
