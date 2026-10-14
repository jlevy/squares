#!/usr/bin/env bash
# Run the author's check.py (read in full first) once, from outside the clone, under the isolated
# scratch interpreter (CPython 3.12.3, SymPy 1.14.0), with -I and a minimal environment.
# Output: k1/check-run/{stdout.txt,stderr.txt,rc.txt,time.txt,env.txt}
here="$(cd "$(dirname "$0")" && pwd)"
out="$here/check-run"
mkdir -p "$out"
cd "$here" || exit 2
{
  echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "uname=$(uname -srm)"
  echo "nproc=$(nproc)"
  echo "python=$("$here/venv/bin/python" -I -c 'import sys; print(sys.version.split()[0])')"
  echo "sympy=$("$here/venv/bin/python" -I -c 'import sympy; print(sympy.__version__)')"
  echo "node=$(/opt/node22/bin/node --version)"
} > "$out/env.txt"
TIMEFORMAT='real_s=%R user_s=%U sys_s=%S'
{ time /usr/bin/env -i PATH="/opt/node22/bin:/usr/bin:/bin" HOME="$HOME" LANG=C.UTF-8 \
  "$here/venv/bin/python" -I "$here/../src/repo/check.py" > "$out/stdout.txt" 2> "$out/stderr.txt" ; } 2> "$out/time.txt"
rc=$?
echo "$rc" > "$out/rc.txt"
echo "exit=$rc $(cat "$out/time.txt")"
tail -1 "$out/stdout.txt"
