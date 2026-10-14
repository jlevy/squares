# Grade-C local-minimality certificates: 233 VALID runs

From the release `exact-data-2026-10-12` of https://github.com/evand/square-packing (`gradec.py` at commits 0d0146e
and e493eea).  Theorem C and its proof: `tasks/exact-minpoly/grade-C.md`.  Checker: `search/exact/gradec.py` (exact
in the number field K, signs by interval arithmetic).

Scope: the 250 best-known configurations with field degree <= 4.  231 VALID at once; n = 230 and 261 VALID with
`GRADEC_DROPZERO=1`, which drops 24 rows forced to zero force; 17 timed out at the 30-minute cap.  (233 = 231 + 2.)

| path | contents |
|---|---|
| `certs/n-N.contacts.json` | the contact rows used (input) |
| `certs/n-N.gradec.json` | the certificate: rows, dropped rows, load-bearing squares, rank L0, dim F, moving squares, dim W, lambda_min, margin, Hessian minors, `valid` |
| `logs/n-N.log`, `logs/n-N.dropzero.log` | run logs (including the 17 timeouts and the dropzero reruns) |
| `logs/_status.txt`, `logs/_dropzero_status.txt` | `n exit CODE` (0 = done, 124 = timeout) |

## Replay

The exact forms `n-N.minpoly.json` are committed in the repo as `search/exact/minpoly/data/n-N.minpoly.json.gz`.
Put the unzipped form next to its `n-N.contacts.json`, then from `search/exact/`:

    PYTHONPATH=. ./env.sh python3 gradec.py DIR/n-N                       # writes DIR/n-N.gradec.json
    GRADEC_DROPZERO=1 PYTHONPATH=. ./env.sh python3 gradec.py DIR/n-230   # likewise n-261

Compare `valid` and the reported constants with the shipped `n-N.gradec.json`.  The 10-11 batch took up to 30 min per
count (`gradec_runs/run.sh`, 8 in parallel).
