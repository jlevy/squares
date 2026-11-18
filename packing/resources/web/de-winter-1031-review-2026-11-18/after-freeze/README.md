# After the Findings’ Freeze

What lane r1031-1118 did after it froze its findings (digest list written at 08:27:44Z,
pushed at 08:27:59Z) on 18 November 2026, including its answers to review A of #1036.
None of it is in either frozen digest list, and none of it changes a finding; the review’s
section After the Freeze reports it.

| File | What it is |
| --- | --- |
| `rv1031_compare.py` | compares this lane’s `out/contraction-t325.json` with the record’s own receipt for T-325, written by `devtools.contraction_margin` in the import of #1009 (`packing/resources/web/mishapolk-issue1009-2026-11-16/measure/contraction-n299-own.json`), which this lane read and did not run; decides nothing |
| `compare-t325-contraction.json` | its receipt: the same side, factor, contracted side, margin and binding pair (71, 140) |
| `rv1031_generic.py` | in answer to review A’s A2 on #1036: scores the subject against T-325, T-248, T-101 and itself under every symmetry and the strongest translations of each kind, turned and upright squares counted apart; decides nothing |
| `generic.json` | its receipt, run at 08:55Z: T-325’s best motion lines up 210 squares (53 turned, 157 upright), an unrelated house (T-101) 162 (161 upright), a unit shift of the packing’s own grid 155; the review’s After the Freeze states what follows |
| `author-files-sha256.txt` | the SHA-256 of the source’s `verify_exact.py`, `check_area.py` and `README.md` at the pin and `REGISTRATION.md` at `3293038d`, fetched at 08:28:50Z and read as data, not run; all four as the source’s `SHA256SUMS` lists them |

Rerun the comparison from the repository root:

```bash
R=packing/resources/web/de-winter-1031-review-2026-11-18
packing/.venv/bin/python3 -I -B $R/after-freeze/rv1031_compare.py --ours $R/out/contraction-t325.json \
  --record packing/resources/web/mishapolk-issue1009-2026-11-16/measure/contraction-n299-own.json \
  --out $R/after-freeze/compare-t325-contraction.json
```

and the measure of A2, with the certificate's form J in `$SRC`:

```bash
W=packing/resources/web
packing/.venv/bin/python3 -I -B $R/after-freeze/rv1031_generic.py --subject json:$SRC/n299_exact.json \
  --ref "T-325=witness:$W/mishapolk-issue1009-2026-11-16/source/witnesses/2026-11-16/n-299.yaml" \
  --ref "T-248=cert:$W/evand-n299-2026-10-26/source/search/packer/candidates/s299-1025.cert" \
  --ref "T-101=cert:$W/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-299.cert" \
  --self --out $R/after-freeze/generic.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
