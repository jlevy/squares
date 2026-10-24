#!/bin/sh
# de Winter's packing of 211 squares as Evan Daniel's exact certificate. The file carries no
# licence, so it is fetched (and its Lean data generated) locally and not committed.
set -e
cd "$(dirname "$0")/.."
mkdir -p certs/fetched
curl -sSf -o certs/fetched/n-211.cert \
  https://raw.githubusercontent.com/evand/square-packing/29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d/search/exact/batch/certs/n-211.cert
echo "ca491d50bb17c976f82edc0ef0accf1316aeac692c9e26bba49921f46ad942ef  certs/fetched/n-211.cert" | shasum -a 256 -c -
python3 scripts/gen_cert.py certs/fetched/n-211.cert N211 --W 15
