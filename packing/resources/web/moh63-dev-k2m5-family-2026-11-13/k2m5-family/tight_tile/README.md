# Tight-Tile checker (`ttbox`)

Proves the Tight-Tile Lemma (paper §6, report `paper/tight_tile_report.pdf`) for the board
`../certificate/sol_exact_box11.txt`. Python 3, standard library + `scipy` (the LP only proposes weights; they are
re-verified exactly).

| file | role |
|---|---|
| `ttpoly.py` | exact polynomials (`Fraction`) and outward-rounded float intervals |
| `ttbox.py` | constraints, charts (line, strip, corner, wedge-corner, ray zones), the cell certificate, the cell loop |
| `ttarea.py` | the Lebesgue term (limit value and derivative bound) |
| `run_tt.py` | one job: every chart of one base line or strip, with automatic corner/wedge/ray zones |
| `make_jobs.py`, `run_all2.sh` | the 308 jobs at u₀ = 1/4000 → `out/` |
| `run_u2000.sh` | the 15 jobs at u₀ = 1/2000 → `out_u2000/` |
| `out_fix/`, `out_u2000_fix/` | reruns of three jobs with the corner zones (they override exactly the charts they report) |
| `run_cov.sh`, `cov.tar.xz` | zmx2 dumps of all uncertified boxes in the 75 tight-tile roots |
| `cov_check.py` | strict job check + exact coverage check → `COVERAGE-OK` |
| `summarize_tt.py` | job summary |
| `ctl_rise.py`, `ctl_rise.txt` | the "same limit values, smaller growth" control |

Re-run one job: `python3 run_tt.py ../certificate/sol_exact_box11.txt 3.5 -1 line 3.5`
(env `U0=1/2000` for the larger tilt range; `SKIP=C_u,...` runs a subset and ends `PARTIAL-...`).
