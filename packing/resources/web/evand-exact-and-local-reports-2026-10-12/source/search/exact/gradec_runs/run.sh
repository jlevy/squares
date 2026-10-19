#!/usr/bin/env bash
# Grade-C batch (10-11): from search/exact,  xargs -P 8 -n 1 gradec_runs/run.sh < LIST   (LIST: one n per line;
# the 10-11 run used the 250 records of field degree <= 4).  Logs gradec_runs/n-N.log (gitignored), status lines
# "n exit CODE" in gradec_runs/_status.txt; certificates minpoly/solve/n-N.gradec.json (gitignored).
# Records with zero-force rows (230, 261): rerun with GRADEC_DROPZERO=1.
n=$1
PYTHONPATH=. timeout ${GRADEC_TIMEOUT:-1800} python3 gradec.py minpoly/solve/n-$n > gradec_runs/n-$n.log 2>&1
echo "$n exit $?" >> gradec_runs/_status.txt
