#!/bin/bash
# A243 -- one descent worker, restarted every --max-classes runs (memory hygiene).  Resumable: the verdict table is
# the skip test.  `touch attempts/A243-climb-17-19/logs/STOP` stops it after the current class.
#   bash worker243.sh N W [descend243 flags...]
cd "$(dirname "$0")" || exit 1
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
N=$1; W=$2; shift 2
while true; do
  python descend243.py $N --worker $W --of 2 "$@"
  rc=$?
  [ $rc -eq 3 ] && continue
  echo "$(date +%H:%M:%S) worker243 n=$N w=$W exit rc=$rc"
  break
done
