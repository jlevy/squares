#!/bin/bash
# w = 4 family LP (corner module R = 4, wall band w = 4), lines only, germ-limit rows, tilt margin kappa = 0.02, th0 = 3 deg.
# Resumable: the germ-row setup saves each of its 64 pieces to fam/ckpt/ (34 already done in the cloud);
# after setup the rows are cached in runs/germ_R4w4_p01.npz.  Ctrl-C and re-run at any time.
# Usage:  cd ~/PycharmProjects/square-packing/sq/fam && bash run_w4.sh
cd "$(dirname "$0")"
PY="$HOME/miniforge3/bin/python3"; [ -x "$PY" ] || PY=$(command -v python3)
echo "python: $PY"
"$PY" -c "import numpy, scipy, highspy" 2>/dev/null || "$PY" -m pip install numpy scipy highspy || exit 1
NP=${NP:-4}   # 4 workers: leaves cores and memory for the s(44) jobs still running
mkdir -p ../runs
TAG=${TAG:-w4k02g2}; KAPPA=${KAPPA:-0.02}; TH0=${TH0:-3}   # e.g. TAG=w4k05 KAPPA=0.05 TH0=0.5
WARM=../runs/qx2_$TAG/sol.npz; [ -f "$WARM" ] || WARM=../runs/qx2_w4k02g2/sol.npz; [ -f "$WARM" ] || WARM=warm_w4p1Li.npz
[ -n "${EXTRA:-}" ] && WARM="$WARM,$EXTRA"   # extra constraint rows, e.g. EXTRA=../box11/zmx2_rows_it1.npz
echo "warm: $WARM"
GERMCKPT="$PWD/ckpt" GERMCACHE="$PWD/../runs/germ_R4w4_p01.npz" caffeinate -i "$PY" qx2_lp.py lp --R 4 --w 4 \
  --hc 0.1 --hp 0.1 --hca 0 --hpa 0 --no-points --kappa $KAPPA --th0 $TH0 --germs --nproc "$NP" --rounds 40 \
  --nrand ${NRAND:-200000} --npol ${NPOL:-500} --solver ipm --crossover off --warm "$WARM" --tag $TAG 2>&1 | tee -a ../runs/$TAG.out
echo "run_w4 finished"
