# Search code

Base: Evan Daniel's `search/` at evand/square-packing@659ee62 (MIT). Files used unchanged: `quadrant_lp.py`,
`qx2_tools.py`, `qx2_zm.py`, `qx2_germscan.py`, `mixed_cover.py`, `zeromargin.py`, `zm_mixed.py`; `zmx2` from
`verify2/`.

Our changes (diffs against 659ee62 in this folder):

- `qx2_exact.patch`
  - `germ_rows_exact` saves each of its 64 chunks to `$GERMCKPT`, so long runs can be resumed.
  - `project` streams cached chunks instead of loading them all.
  - New `project_fast` (`projectf`) for large tight sets: dedupe, QR row/column selection weighted by the float
    solution, exact solve with FLINT, exact check of every tight row.
- `qx2_lp.patch`
  - `$GERMCACHE`: the germ-limit rows are computed once and loaded from disk afterwards.

Drivers:

- `run_w4.sh`: the LP run (Mac). Environment: `NP` (workers), `EXTRA` (extra row file), `NRAND`, `NPOL`.
- `run_box11.sh`: the zmx2 oracle sweep of the 11 × 11 cover (Mac), 55 columns, resumable.
- `sweep_rows.py`: turns a sweep's uncertified boxes into LP rows (`zmx2_rows_itN.npz`).
