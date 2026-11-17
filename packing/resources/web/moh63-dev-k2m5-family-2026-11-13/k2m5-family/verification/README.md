# Verification

`bash verify.sh` (fast) or `bash verify.sh --full`; see the top-level README. Contents:

| file | what |
|---|---|
| `sanity_k2m5.py` | exact bookkeeping: well-formed board, total = 121 − 4D, D > 5/4, D4 invariance |
| `locality_check.py`, `boards/` | exact window check of the locality lemma on μ_k, k = 10, 12, 13, 20 (built from the family) |
| `audit_zmx2.py`, `logs/zmx2_box11/` | exact audit of the recorded zmx2 sweep (cert0 + first-order D4 sweep, 12,100 roots) |
| `r9632/` | root 9632: zmx2 dump, qx2_zm.py run on the cropped cover, and `check_9632.py` |
| `controls/` | checker controls: zmx2 and qx2_zm.py on scaled covers, the tight-tile "smaller growth" control, a one-weight mutation for the locality check |
| `stress_family.py` | float stress test (not part of the proof) |
| `zmx2_print_all.patch` | the one-line output patch used for the coverage dumps |
