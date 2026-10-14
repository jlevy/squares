#!/bin/sh
# Download the two pieces of the n = 15 base case that are not redistributed here, from pinned
# commits, and check their SHA-256. De Winter's repository has no licence, so neither his file nor
# Daniel's exact certificate of the same packing is copied into this repository.
#
#   sh third_party/fetch_unlicensed.sh [outdir]      # default: third_party/unlicensed (git-ignored)
#
# Then, for example:
#   python3 verify.py third_party/unlicensed/n-211.cert --strict
#   python3 tools/glue.py --rect rectangles/r17x16_n0257/r17x16_n0257.cert \
#       --second third_party/unlicensed/n-211.cert --out n031_from_211.cert    # 932 = 31^2 - 31 + 2
set -eu
here=$(cd "$(dirname "$0")" && pwd)
out=${1:-"$here/unlicensed"}
mkdir -p "$out"

if command -v sha256sum >/dev/null 2>&1; then sha() { sha256sum "$1" | cut -d' ' -f1; }
else sha() { shasum -a 256 "$1" | cut -d' ' -f1; }; fi

fetch() {  # url file expected-sha256
  curl -fsSL -o "$out/$2" "$1"
  got=$(sha "$out/$2")
  if [ "$got" = "$3" ]; then echo "OK        $2  $got"
  else echo "MISMATCH  $2  got $got, expected $3" >&2; exit 1; fi
}

# Joost de Winter, 211 unit squares in side 14.99796..., commit 702df9bb (no licence)
fetch https://raw.githubusercontent.com/JoostdeWinter/square-packing-211/702df9bb3b1e7fe13279a61a1fa89722aa2d496a/n211__record.json \
  n211__record.json 94b206475442caade4892a393251c9d464341b3327e58c6ef21076fea3dad372
# Evan Daniel's exact certificate of de Winter's packing, commit 29d0cee
fetch https://raw.githubusercontent.com/evand/square-packing/29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d/search/exact/batch/certs/n-211.cert \
  n-211.cert ca491d50bb17c976f82edc0ef0accf1316aeac692c9e26bba49921f46ad942ef
echo "saved in $out"
