#!/bin/sh
# Regenerate every certificate data file (deterministic). N211 comes from scripts/fetch_211.sh.
set -e
cd "$(dirname "$0")/.."
G="python3 scripts/gen_cert.py"
$G certs/daniel/n-110.cert M110 --W 11
$G certs/daniel/n-132.cert M132 --W 12
$G certs/daniel/n-156.cert M156 --W 13
$G certs/daniel/n-182.cert M182 --W 14
$G certs/daniel/n-241.cert N241 --W 16
$G certs/daniel/n-273.cert N273 --W 17
$G certs/ours/n0308.cert N308 --W 18
$G certs/ours/n0343.cert N343 --W 19
$G certs/ours/n0381.cert N381 --W 20
$G certs/ours/n0421.cert N421 --W 21
$G certs/ours/n0463.cert N463 --W 22
$G certs/ours/n0507.cert N507 --W 23
$G certs/ours/n0553.cert N553 --W 24
$G certs/ours/n0601.cert N601 --W 25
$G certs/ours/n0651.cert N651 --W 26
$G certs/ours/r17x16_n0257.cert R257 --W 17 --H 16
$G certs/ours/r22x21_n0443.cert R443 --W 22 --H 21
