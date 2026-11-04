#!/bin/sh
# Regenerate the certificate from Hosono's published measure, check its hash, build
# jlevy/squares' sqverify-fast at a pinned commit and run it.
#   sh verify.sh [DIRECTIONS [THREADS]]   DIRECTIONS: all (default), a-b, or r1,r2,...
# Needs: git, curl, python3, sha256sum, rustup (the crate pins rustc 1.98.0).
set -eu
DIRS="${1:-all}"
THREADS="${2:-$(nproc)}"
HERE=$(cd "$(dirname "$0")" && pwd)
WORK="$HERE/_verify"
SQUARES_COMMIT=e6e8d57726db80cd0e6a1523166a96c5d36a3119
HOSONO_COMMIT=797bdf6e10eba5f9dccca9da06f8352e81ba9dde
HOSONO_SHA=64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a
CERT_JSON_SHA=b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c
mkdir -p "$WORK"
cd "$WORK"

curl -sSfL -o candidate.json \
  "https://raw.githubusercontent.com/wand125/square-packing-bounds/$HOSONO_COMMIT/certificates/mixed_n94_L995/candidate.json"
echo "$HOSONO_SHA  candidate.json" | sha256sum -c -
gzip -kf candidate.json
python3 "$HERE/tools/rescale.py" candidate.json.gz 1993/200 regenerated.json.gz 83/120000 599
echo "$CERT_JSON_SHA  -" > regenerated.sha
gzip -dc regenerated.json.gz | sha256sum -c regenerated.sha
gzip -dc "$HERE/certificate/n94_L9965.json.gz" | sha256sum -c regenerated.sha

if [ ! -d squares ]; then
  git clone --filter=blob:none --no-checkout https://github.com/jlevy/squares.git squares
  git -C squares sparse-checkout set packing/sqverify_fast
fi
git -C squares checkout -q "$SQUARES_COMMIT"
(cd squares/packing/sqverify_fast && cargo build --release)
squares/packing/sqverify_fast/target/release/sqverify-fast \
  --candidate "$HERE/certificate/n94_L9965.json.gz" --n 94 --directions "$DIRS" --threads "$THREADS" --confirm \
  > "sqverify-fast-$DIRS.jsonl"
tail -n 1 "sqverify-fast-$DIRS.jsonl"
