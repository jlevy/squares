#!/bin/bash
# Coverage input: complete list of zmx2's uncertified boxes in the 75 tight-tile roots of the k05-5 box cover
# (same settings as the box11_k5 sweep; ZMX2_PRINT_ALL prints every box).  Output: cov/r<id>.out
# Usage:  cd ~/PycharmProjects/square-packing/sq/ttbox && nohup bash run_cov.sh > cov.out 2>&1 &
cd "$(dirname "$0")"
Z=../build/square-packing/verify2/target/release/zmx2  # built with verification/zmx2_print_all.patch; B=../certificate/sol_exact_box11.txt; NP=${NP:-6}
mkdir -p cov
IDS="10000 10180 10220 10400 10440 10620 10660 10840 10880 11060 11100 11280 11320 11500 11540 11720 11760 11940 11980 3360 3400 3436 3440 3464 3468 3472 3476 3480 3484 3488 3492 3496 3500 3504 3508 3512 3516 5376 5560 5596 5668 5672 5676 5680 5684 5688 5692 5696 5700 5704 5708 5712 5716 7576 7580 7760 7796 7800 7836 7840 7868 7872 7876 7980 8420 8640 8680 9080 9300 9340 9520 9560 9740 9780 9960"
echo "start $(date)"
for id in $IDS; do echo $id; done | xargs -P "$NP" -n 1 sh -c 'id=$0; c=$((id/220)); r=$(((id%220)/4)); b=$((id%4)); f=cov/r$id.out
  [ -f "$f" ] && grep -q "^done in" "$f" && exit 0
  ZMX2_PRINT_ALL=1 '"$Z"' cert '"$B"' --d4 --first-order --threads 1 --depth 40 --node-cap 20000000 --uncert-cap 100000000 --xlo $c --xhi $c --ylo $r --yhi $r --bins $b-$b > "$f" 2>&1
  echo "$(date +%T) r$id $(grep -c ^UNCERT $f) boxes"'
echo "cov done $(date)"
