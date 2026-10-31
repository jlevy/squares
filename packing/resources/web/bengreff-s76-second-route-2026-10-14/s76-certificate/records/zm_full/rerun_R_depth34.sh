export PATH=~/mm/envs/sq/bin:$PATH
cd ~/s76repo_test/work/upstream/s12/search
python3 -u zm_mixed.py cert /home/greff/s76/s76_cover_v5.txt --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 34 --nproc 1 --cx-lo 27/20 --cx-hi 7/5 --cy-lo 13/10 --cy-hi 27/20 --u-lo 1/4 --u-hi 9/32 --resume /home/greff/s76/zmm_R34.jsonl > /home/greff/s76/zmm_R34.log 2>&1
echo "EXIT $?" >> /home/greff/s76/zmm_R34.log
