#!/bin/sh
# A214 -- the per-run measurement: the same page twice, kernel OFF then ON (isolated cert/results, --no-fig).
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
export A213_INTCORE=1
A214_CKERNEL=0 python code/profrun214.py off k5_11_interior_Y0202 --wall 900 --pads zero > logs/run_off.log 2>&1
A214_CKERNEL=1 python code/profrun214.py on  k5_11_interior_Y0202 --wall 900 --pads zero > logs/run_on.log 2>&1
echo RUNS214_DONE
