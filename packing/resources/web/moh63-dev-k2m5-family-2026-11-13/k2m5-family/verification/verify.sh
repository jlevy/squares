#!/bin/bash
# Re-check the k >= 10 part of s(k^2 - 5) = k from this release.
#
#   bash verification/verify.sh            (fast, a few minutes): exact bookkeeping, locality on built boards,
#                                          and exact audits of every recorded run
#   bash verification/verify.sh --full     also re-runs the computations from scratch (needs git, Rust/cargo,
#                                          python3 with numpy; the zmx2 sweep takes hours, the tight-tile jobs
#                                          several CPU-days; every step is resumable)
#
# The checkers zmx2 (Rust) and qx2_zm.py (Python) are Evan Daniel's, used unmodified from
# evand/square-packing@659ee62, except a one-line patch that makes zmx2 print *all* uncertified boxes when
# ZMX2_PRINT_ALL is set (verification/zmx2_print_all.patch; output only).
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd); CERT=$ROOT/certificate/sol_exact_box11.txt
PIN=659ee62e4a9d39542a1146e8b011cc3ab6407ede
sha() { sha256sum "$@" 2>/dev/null || shasum -a 256 "$@"; }

echo "== 0. certificate hashes"
(cd certificate && (sha256sum -c SHA256SUMS 2>/dev/null || shasum -a 256 -c SHA256SUMS))

echo "== 1. exact bookkeeping: total = 121 - 4D, D > 5/4, D4 invariance"
python3 verification/sanity_k2m5.py certificate/sol_exact_box11.txt certificate/sol_exact.json certificate/sol_exact_family.txt

echo "== 2. locality on the built boards k = 10, 12, 13, 20 (exact; Lemma 7 of the paper is the general proof)"
python3 verification/locality_check.py certificate/sol_exact_box11.txt verification/boards/box10.txt \
  verification/boards/box12.txt verification/boards/box13.txt verification/boards/box20.txt | tail -1

echo "== 3. audit of the recorded zmx2 sweep (theta = 0 and first-order D4 sweep, 12,100 roots)"
[ -d tight_tile/cov ] || (cd tight_tile && tar xJf cov.tar.xz)
python3 verification/audit_zmx2.py verification/logs/zmx2_box11 tight_tile/cov

echo "== 4. root 9632: zmx2 and qx2_zm.py together leave nothing uncertified"
(cd verification/r9632 && python3 check_9632.py dump.out zm.out zm_unc.txt)

echo "== 5. Tight-Tile Lemma: every job and chart certified; every leftover zmx2 box covered"
(cd tight_tile && python3 summarize_tt.py out | tail -1 && python3 cov_check.py cov | grep -v "outside:")

[ "${1:-}" = "--full" ] || { echo "fast checks done"; exit 0; }

echo "== 6. (full) checkers at the pin"
mkdir -p build
[ -d build/square-packing ] || git clone -q https://github.com/evand/square-packing build/square-packing
git -C build/square-packing checkout -q $PIN
(cd build/square-packing && git apply "$ROOT/verification/zmx2_print_all.patch" 2>/dev/null || true)
(cd build/square-packing/verify2 && cargo build -q --release)
Z=$ROOT/build/square-packing/verify2/target/release/zmx2
echo "== 7. (full) zmx2 sweep: cert0, then the first-order D4 sweep column by column (resumable)"
mkdir -p build/zmx2
$Z cert0 "$CERT" --d4 > build/zmx2/cert0.txt 2>&1; tail -1 build/zmx2/cert0.txt
for i in $(seq 0 54); do t=build/zmx2/col$(printf %02d $i)
  [ -f $t.done ] || { $Z cert "$CERT" --d4 --first-order --threads 1 --depth 40 --node-cap 20000000 \
      --xlo $i --xhi $i --log $t.log > $t.out 2>&1 && touch $t.done; }
done
python3 verification/audit_zmx2.py build/zmx2 tight_tile/cov
echo "== 8. (full) tight-tile jobs (see tight_tile/README.md; several CPU-days), then the coverage check"
(cd tight_tile && NP=${NP:-8} bash run_all2.sh && bash run_u2000.sh && python3 cov_check.py cov | tail -1)
