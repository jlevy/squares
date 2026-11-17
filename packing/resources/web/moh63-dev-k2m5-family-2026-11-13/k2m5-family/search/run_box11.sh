#!/bin/bash
# Oracle sweep (zmx2 exact boxes; uncertified boxes become new LP rows) of the k^2 - 5 family's 11 x 11 box cover with zmx2 (E. Daniel's checker), native macOS.
# 55 columns of root boxes (the D4 region), one job per column; finished columns are skipped on re-run,
# so you can stop (Ctrl-C) and re-run at any time.   Usage:  cd ~/PycharmProjects/square-packing/sq/box11 && bash run_box11.sh
cd "$(dirname "$0")"
Z=../verify2/target/release/zmx2
B=sol_exact_box11.txt
DEPTH=${DEPTH:-24}; NODECAP=${NODECAP:-2000000}   # oracle settings; final certification uses the exact Python checker
NP=${NP:-$(sysctl -n hw.perflevel0.physicalcpu 2>/dev/null || echo 6)}
mkdir -p logs
[ -f logs/d4.ok ] || { $Z d4 $B | tail -1 | tee logs/d4.txt; grep -q invariant logs/d4.txt && touch logs/d4.ok; }
[ -f logs/cert0.ok ] || { $Z cert0 $B --d4 > logs/cert0.txt 2>&1; tail -2 logs/cert0.txt; grep -q "^VERIFIED" logs/cert0.txt && touch logs/cert0.ok; }
one(){ i=$1; t=col$(printf %02d $i); [ -f logs/$t.done ] && return
  $Z cert $B --d4 --first-order --threads 1 --depth $DEPTH --node-cap $NODECAP --xlo $i --xhi $i --log logs/$t.log > logs/$t.out 2>&1 && touch logs/$t.done
  echo "$(date +%T) $t: $(grep -iE 'uncert' logs/$t.out | tail -1)" >> logs/progress.txt; }
export -f one; export Z B DEPTH NODECAP
echo "start $(date), $NP jobs" >> logs/progress.txt
caffeinate -i bash -c 'seq 0 54 | xargs -P '"$NP"' -I{} bash -c "one {}"'
echo "all columns done $(date)" >> logs/progress.txt; echo "all columns done"
