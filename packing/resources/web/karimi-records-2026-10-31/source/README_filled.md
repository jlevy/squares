# Filled-end two-band L packings, n = 1182–9946 (Zenodo version V2.0)

Mohsen Karimi (ORCID 0009-0004-1055-8267), Independent Researcher, Zanjan, Iran.

## Contents
- `filled_records.csv` — 5134 rows, one per n: K, exact side (`side_exact`), decimal side, previous best side and its source, and the construction parameters (bV, tV, yV, bH, tH, yH; all exact rationals).
- `filled_ends.py` — exact construction (fractions only).
- `regenerate_filled.py` — rebuilds `certificates_filled/n<N>.cert` from each row (`python3 regenerate_filled.py` or `python3 regenerate_filled.py 9946`).
- `check_cert.py` — a small independent exact checker (`python3 check_cert.py file.cert --mutate`).

Certificate format: `n S` header, then one line `x y t` per unit square (centre, t = tan(θ/2)), the format of Mishapolk/square-packing-records.

## Construction and credit
- L-shaped frame (aligned grid plus two tilted bands): Sungjoon Ryu, doi:10.5281/zenodo.23278927, Theorem 1.3.
- Band ends filled with axis-parallel layers: Evan Daniel (evand/square-packing, certificates/k2-minus-c/, 18 October 2026); band and fill as written in Kevin Fang's note, doi:10.5281/zenodo.23624565, Sections 2–3.
- Independent width b, tilt t = tan(θ/2) and lift split of each band, and the per-n search: Mohsen Karimi.
- Code and computations were done with the assistance of Claude (Anthropic) under the author's direction; the search was run in MATLAB Online and reproduced in Python.

## Changes from Zenodo version V1.0 (doi:10.5281/zenodo.23681705, archive karimi_filled_end_v2.zip, 4571 rows)
- Finer search (band containers K = 35–100, finer tilt grid, 20 lift splits): 4536 sides lowered or added.
- Each row is now compared with both public indices: every row is strictly below the entry of franciscouzo/square-packing at commit 712c6a6 (certified_bounds.json) and of Mishapolk/square-packing-records at commit ab8e833, where an entry exists.
- 40 rows of V1.0 are removed because no construction here is below Couzo's index for them: 1240 1245 1246 1247 1375 1450 1451 2214 3484 3972 4625 4762 5185 5330 5477 5626 5777 5930 6085 6242 6401 6562 6725 6890 7057 7226 7397 7570 7745 7922 8101 8282 8465 8650 8837 9026 9217 9410 9605 9802.
- 603 values of n are new compared with V1.0.

## Rows
- 4841 rows improve the author's earlier records (Zenodo 10.5281/zenodo.23664800, v5).
- 293 rows are values of n not in v5 (previous best: 181 from Mishapolk ab8e833, 112 from Couzo 712c6a6).

## Verification
All 5134 certificates were rebuilt in exact rational arithmetic from the table and accepted by verify_bound_certificate.py of Mishapolk/square-packing-records (ab8e833): 5134 accepted, 0 rejected.
