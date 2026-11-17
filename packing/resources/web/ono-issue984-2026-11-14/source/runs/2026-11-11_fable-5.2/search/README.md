# search/ — code written during this run

All files were written by the agent inside this run directory. Nothing here judges a result:
only the frozen top-level `verify.py` does (via `make_cert.py`, which calls the frozen `certify.py`).

## Core

| file | purpose |
|---|---|
| `sqgeom.py` | numba kernel: separating-axis overlap depth, penalty energy and gradient, validity check |
| `opt.py` | `penalty_min` (L-BFGS on S + mu*E) and `polish` (exact-constraint SLP with a trust-region schedule) |
| `make_cert.py` | float packing -> frozen `certify.py` -> frozen `verify.py --compare`; copies VALID certificates to `../certificates/` and logs the attempt |
| `indep_check.py` | independent exact re-check of a certificate (rational polygon clipping; shares no code with the verifier). A rule-7 step, not a judge |
| `render.py` | PNG pictures for inspection |

## Phase 1 and 2

| file | purpose |
|---|---|
| `build_records.py` | builds `../records.json` from the two downloaded catalogues (digit-for-digit copy, lower value wins). Incomplete on its own: run `add_kaggle_source.py` afterwards |
| `targets_table.py` | softness indicators per n (position in band, age of record, neighbour-trend residual) |
| `closure.py` | table-consistency checks: delete-a-square, add-an-L, clean strip removal |
| `gsearch.py` | from-scratch global search (random start, penalty continuation, polish, basin hopping); reads no published coordinates |
| `sa.py` | simulated annealing at fixed side with soft overlaps (failed at n = 29, see REPORT) |

## Phase 3

| file | purpose |
|---|---|
| `witness_io.py` | loads the published record packings (Squares Project witnesses) as floats |
| `attack.py` | drivers: `delone`, `unl`, `sweep` (un-L and L-insertion transfers), `hop` (basin hopping; `SQ_MOVES=poly` adds band-shape moves) |
| `blockseed.py`, `latseed.py` | structured seed generators (tilted block / rotated-lattice region + corner-anchored grids); abandoned |
| `splice.py` | periodic splice inside one band family |
| `diagper.py` | **diagonal-period closure**: remove or insert (p, p) periods of a diagonal band, repair, polish. Sources: record n, `cert:`, `npz:` or `json:` files, or a directory. Produced the two packings first reported as candidates (n = 147, n = 228; both claims withdrawn, see REPORT) |
| `diagcuts.py` | all cut positions for one (source, p, m) diagonal reduction |
| `crossper.py` | cross-cut closure: remove a vertical and a horizontal strip of width p, close up, repair, polish |
| `bigclosure.py` | exact clean-strip surgery on third-party certificate files |
| `refine_near.py` | basin hopping from the closure passes' near misses |
| `ext_table_check.py` | compares a directory of third-party packings with `records.json` (is our table stale anywhere?) |
| `recheck_sources.py` | rule-7 helper: re-reads the public sources for one n and searches the tracker |

## Bookkeeping

| file | purpose |
|---|---|
| `merge_attempts.py` | appends the pods' attempt lines to `../attempts.jsonl` exactly once |
| `log_stopped_hops.py`, `log_stopped_pass.py` | attempt lines for runs that were stopped before they logged themselves (reconstructed from their logs) |
| `annotate_attempts.py` | marks 7-decimal progress values that coincide with a record as rounding, not improvements |
| `summarize_attempts.py`, `report_table.py`, `pass_table.py`, `near_misses.py` | tables for the report |

## Post-run correction

| file | purpose |
|---|---|
| `add_kaggle_source.py` | adds the Kaggle per-puzzle leaderboard (best side per n, side only) to `../records.json` as a third source; where a team's side is lower, it becomes `upper`. This is what showed that the two "candidates" were not improvements |
| `kaggle_check_table.py` | writes `../evidence/kaggle_per_puzzle_check.md`, the comparison of that table with the two catalogues |

## Follow-up after the run (2026-11-14, human-steered; see `../FOLLOWUP.md`)

| file | purpose |
|---|---|
| `fu_pinwheel.py` | tilted blocks (Ryu/Fang band geometry) plus an exact refill of the upright squares: maximum independent set over the four corner-anchored grids, HiGHS MILP; optional tolerance for small dips |
| `fu_scan.py`, `fu_refine.py` | random scan and hill climbing (with tapered rows) over two-block layouts |
| `fu_subwindow.py` | corner-anchored sub-window closure over the public packings |
| `fu_refill_public.py` | exact refill around the tilted cores of public packings near the grid crossover |
| `fu_core.py` | edits of a parent's tilted core (slide, insert or remove a bar, lengthen or shorten a bar) with exact refill |
| `fu_softseed.py` | one more square from a tolerant refill, then penalty repair and exact polish |

| `fu_strict_check.py` | exact check under the stricter convention (positive wall margins, strictly separated pairs) and export to the text format `n S` / `x y t`. Not a judge |
| `fu_registration.py` | writes the strict variants and the draft registration requests under `../evidence/registration/` (drafts only) |

All follow-up searches are negative; none of these scripts produced a new certificate.

Remote orchestration (no secrets): `../work/remote/rp.sh`, `rpcp.sh`, `sync_one.sh`, `sync_loop.sh`,
`guard.sh` (see RUN.md).

## Reproduce the calibration (no published coordinates are read by `gsearch.py`)

```
python3 search/gsearch.py 11 --time 60  --procs 8 --target 3.8770836
python3 search/gsearch.py 17 --time 420 --procs 6 --target 4.6755310
python3 search/gsearch.py 18 --time 420 --procs 5 --target 4.8228766
python3 search/gsearch.py 19 --time 420 --procs 5 --target 4.8856190
python3 search/make_cert.py work/calib/n17_seed1000.json --den "10**15"
```
