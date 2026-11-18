# Blind Stage 4 Review of jlevy/squares#1031: Programs and Receipts

Lane r1031-1118 of the intake pass of 17 and 18 November 2026 (bead `think-r3tn`). This
packet holds the programs a blind stage 4 mathematical review wrote for Joost de Winter’s
claim $s(299) \le 17.793636991744$, their controls plan, the frozen digest lists and the
receipts. The review itself is `docs/project/reviews/review-2026-11-18-de-winter-1031.md`.

The source is read as data at
[JoostdeWinter/square-packing `497eb478`](https://github.com/JoostdeWinter/square-packing/tree/497eb478b790175ea8690671b66785b70c97f9f2/n299),
folder `n299/`: `n299_exact.json` (form J, a centre and a unit edge direction per square)
and `n299_witness.yaml` (form C, a Witness/v2 corners file). None of the source’s programs
ran, and its `verify_exact.py` and `check_area.py` were not opened before the findings
were frozen.

## Programs

Every program is this lane’s own, imports nothing from this repository or the source, and
runs under the project interpreter (CPython 3.14.7, gmpy2 2.3.1, PyYAML 6.0.3) as
`python -I -B`, at `nice -n 19`.

| Program | Reads | Decides |
| --- | --- | --- |
| `rv1031_reader.py` | (a module) forms J, C and P, strictly, into exact rationals | nothing by itself |
| `rv1031_axes.py` | (a module) method A: separating axes on poses, `fractions.Fraction` | pair margins and wall clearances |
| `rv1031_clip.py` | (a module) method B: exact Sutherland–Hodgman clipping on corners, `gmpy2.mpq` | pair classes and areas, wall terms, area inside |
| `rv1031_decide.py` | (a module) whole-packing decisions by both methods and their comparison | nothing by itself |
| `rv1031_check.py` | forms J and C | the certificate, directly and crossed, and the claim |
| `rv1031_contract.py` | any one form, and optionally its twin | the contraction margin, exactly |
| `rv1031_controls.py` | forms J and C, `controls-plan.json` | nothing: runs the controls plan |
| `rv1031_selftest.py` | synthetic data only | nothing: holds the methods to hand-derived values and to seven broken copies |
| `rv1031_synth.py` | nothing | nothing: writes the synthetic certificates the controls were tried on |

`programs/issue-1031.json` is the issue as the REST API returned it at 07:36:09Z on 18
November (the body only was read). `programs/controls-plan.json` states every control and
its outcome as a rule over the certificate’s exact facts, the priors, and the run plan
with its pricing.

## Freeze Protocol

1. The programs and the controls plan were committed and pushed, with their SHA-256 in
   `frozen/checker-frozen-digests.txt`, before any program of this lane read the
   certificate or any packing of the record. Before that freeze they ran only on synthetic
   data.
2. Then they ran, in the order of the plan.
3. The findings were frozen in `frozen/findings-frozen-digests.txt` before the doc-map
   entry, the synopsis map or the pull request.

Verify a freeze from this directory:

```bash
cd packing/resources/web/de-winter-1031-review-2026-11-18
sha256sum -c frozen/checker-frozen-digests.txt
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
