#!/bin/sh
# zmx2 (6b7f0f79, built from retained bytes by devtools.replay_evand_zmx2 build, binary cba78a9e) on the published
# covers and on this review's mutated covers, one D4 root each: the root holding the pose where the exact evaluator
# found the mutant below one.  One thread, nice 10.  Usage: run_zmx2_controls.sh WORK
# Run run_all_final.sh with the same WORK first: it writes the mutated covers to WORK/mut.  Needs cargo and bc.
. "$(dirname -- "$0")/common.sh"
for m in n76_drop-heaviest-point n76_drop-heaviest-segment n76_scaled-999-1000 n95_drop-heaviest-point \
         n95_drop-heaviest-segment n95_scaled-249-250; do need mut/$m.txt run_all_final.sh; done
# The build is project tooling, run from packing/ as development.md runs devtools (not with -I, which drops cwd).
( cd -- "$PACKING" && "${UV:-uv}" run --frozen --all-extras --group dev python -m devtools.replay_evand_zmx2 build \
    --checker 6b7f0f79 --work "$WORK/zmx2" ) || exit 2
Z=zmx2/6b7f0f79/verify2/target/release/zmx2
mkdir -p outputs/zmx2
run() { # tag cover i j k
  echo "# zmx2 $(sha256sum $Z | cut -c1-16) cert $2 --d4 --threads 1 --xlo $3 --xhi $3 --ylo $4 --yhi $4 --bins $5-$5; cover sha256 $(sha256sum $2 | cut -d' ' -f1)" > outputs/zmx2/$1.log
  t0=$(date +%s.%N)
  nice -n 10 $Z cert $2 --d4 --threads 1 --xlo $3 --xhi $3 --ylo $4 --yhi $4 --bins $5-$5 >> outputs/zmx2/$1.log 2>&1
  echo "# exit $? wall $(echo "$(date +%s.%N) - $t0" | bc) s" >> outputs/zmx2/$1.log
  grep -E '^(ROOT|done|NOT|REGION|VERIFIED|INCOMPLETE|ERROR)' outputs/zmx2/$1.log | head -3 | sed "s/^/$1: /"
  grep -E '^UNCERT' outputs/zmx2/$1.log | head -1 | sed "s/^/$1: /"
}
run n76_published_x15y15u0 data/s76_cover_v5.txt 15 15 0
run n76_drop-heaviest-point_x15y15u0 mut/n76_drop-heaviest-point.txt 15 15 0
run n76_published_x5y35u0 data/s76_cover_v5.txt 5 35 0
run n76_drop-heaviest-segment_x5y35u0 mut/n76_drop-heaviest-segment.txt 5 35 0
run n76_published_x35y5u0 data/s76_cover_v5.txt 35 5 0
run n76_scaled-999-1000_x35y5u0 mut/n76_scaled-999-1000.txt 35 5 0
run n95_published_x15y15u0 data/s95_cover_v2.txt 15 15 0
run n95_drop-heaviest-point_x15y15u0 mut/n95_drop-heaviest-point.txt 15 15 0
run n95_published_x5y45u0 data/s95_cover_v2.txt 5 45 0
run n95_drop-heaviest-segment_x5y45u0 mut/n95_drop-heaviest-segment.txt 5 45 0
run n95_published_x35y25u0 data/s95_cover_v2.txt 35 25 0
run n95_scaled-249-250_x35y25u0 mut/n95_scaled-249-250.txt 35 25 0
