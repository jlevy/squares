# Exact forms for the current records (2026-10-15)

The 10-07 table (`../EXACT_FORMS.md`) covers the register as of 10-06.  Since then the records have moved
(SQUISH, Xu, Mishapolk, Couzo, Ostashev, ours).  On 10-15, of the 324 current records (`pk.py frontier`,
register + pending), **249** had an exact form for that same packing; 55 n had never been solved and at 20 n
the exact form is for a superseded packing.  This directory runs the 10-07 pipeline unchanged on the current
records of those 75 n.

**Result: 23 new exact forms, all VALID** (`verify_exact.py`, independent replay below), so **272 / 324** current
records now have one.  12 are n that were open on 10-07 (88, 123, 126, 172, 199, 207, 259, 263, 292, 297, 301,
302: the newer packings there have simpler contact graphs than the old ones that timed out), 11 replace an exact
form of a superseded packing (51, 70, 102, 153, 175, 204, 232, 258, 266, 267, 295).  Degrees 2 to 41; three are
quadratic: s(51) ≤ (16 + 5√2)/3, s(126) ≤ 15/2 + 3√2, s(295) ≤ 22(1 + √2)/3.  Table: `RESULTS.md`
(`results.json`).

Integer-shift families (same polynomial up to x → x + k): 70 / 207, 175 / 232, 123 / 259 / 292, 153 / 302.

## Files
| file | what |
|---|---|
| `run.py N[:REF] ...` | per n: `pk.py get best:N` → `exactsolve.py` (→ `slp2.py` polish → `exactsolve.py` if the first does not certify, as in `search/regularize/refresh.py`) → `minpoly.py` → `verify_exact.py` (last two via `../env.sh`).  Outputs `runs/exact-cur/<tag>/` (gitignored), `status.jsonl` |
| `data/n-N.minpoly.json.gz` | the 23 exact forms (same format as `../minpoly/data/`) |
| `verify_data.sh` | replays `verify_exact.py` (stdlib only) on `data/`: **23 / 23 VALID**, 4 min on 8 processes; `data/verify.txt` |
| `crosscheck.py` | independent of `minpoly.py`'s algebra: exactsolve's 64-digit Newton S lies in p's isolating interval (23 / 23, relative residual ≤ 2e-59); `mpmath.findpoly` from those digits returns p at 51, 102, 126, 295 and nothing elsewhere (too few digits for its search), never a different polynomial.  `crosscheck.json` |
| `table.py` | `RESULTS.md`, `results.json` (credit = the frontier's "best known by"; "pending" = an open register issue) |

Run (10-15): `python3 run.py <75 n> --procs 12`, `--tmo 900`, `--mem 12G`, ~1 h wall.

**Register (jlevy/squares main 4e8c898, synced 10-15).**  Every S* equals the register's reported value (to
1e-14; 207 to 2.4e-12, a 12-digit rounding there).  The register already has s(51) = (16+5√2)/3 (Ryan Xu, #432):
ours agrees.  For the other 22 it records a rational (a certified side, `algebraic_degree: 1`) or nothing.
Input packings: the store's best, which at 153 and 207 is a Mishapolk / Couzo copy tying the register witness
(PingYou).  Re-run on the register witnesses (`run.py 153:291578 207:291579`): the same p at both; 153 VALID; 207
NOT VERIFIED on pair (73, 74) ("no separating line proved"; that witness's own exact point, not investigated), so
207's committed form is from the copy (store id 1044231).

Published cross-checks: none for these packings.  Ellsworth's page (fetched 10-06,
`tasks/exact-minpoly/results/kingbird_crosscheck.json`) predates them; at these n it has the older packings.

## Still open (52), by failure
| # | n | failure | what it needs |
|---|---|---|---|
| 22 | 110, 127, 130, 131, 156, 181, 182, 208, 210, 211, 239, 240, 241, 270, 272, 273, 303, 304, 305, 306, 307, 308 | `minpoly.py` killed at 12 GB (15–31 tilted angle classes; 304 got to 3 consistency factors of degree 19, 19, 15 and died in msolve) | block-triangular elimination (rigid clusters in order), or homotopy for 304 |
| 18 | 29, 68, 71, 103, 105, 108, 132, 154, 155, 176, 180, 206, 209, 228, 237, 238, 264, 271 | timeout 900 s (mostly msolve on 5–10 consistency factors) | homotopy (`../homotopy/`, as s(29)); count paths first (mixed volume) and skip anything far above ~1000 |
| 7 | 83, 84, 86, 146, 179, 235, 236 | msolve: system not zero-dimensional | force balance in more than one free direction |
| 3 | 129, 268, 269 | Lagrange determinant identically 0 | flat rotation: pin the flat angle class (as 53, 106, 129, 177 on 10-07) |
| 1 | 55 | msolve error | multiplier formulation (task README) |
| 1 | 261 | exactsolve + polish did not certify | re-solve the record |

s(29) itself has its polynomial (degree 7213, `../homotopy/N29.md`) but no `verify_exact` exact form; it is
counted as open here.  Paused 10-15 (Evan) after this batch.
