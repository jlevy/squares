# Reproducing the checks

Both checks run on a stock Ubuntu 24.04 machine (x86_64). Times above are for 10 threads.

## First system (sqverify-fast --continuous v4)

```
tar xzf check1/src/sqverify_continuous_v4.tgz
cd sqverify_continuous/sqverify_fast && cargo build --release && cd -
BIN=sqverify_continuous/sqverify_fast/target/release/sqverify-fast
$BIN --candidate candidate.json --n 28 --continuous --core 499/500 --tau 1 --threads 10 --max-nodes 200000000 > run.jsonl
tail -1 run.jsonl          # "status":"VERIFIED", "claim":"s(28) > 1149/200", input_sha256 a2e47a39e310c695fafeb8d1c744f930a561b3be7d71bbdb359e362eaebacb8d
$BIN --candidate control/candidate-mass0985.json --n 28 --continuous --core 499/500 --tau 1 --threads 10 \
     --max-nodes 200000000 > control.jsonl
tail -1 control.jsonl      # "status":"REFUSED"
```

The build prints the source SHA-256 in every summary (`build.source_sha256` = 619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5).

## Second system (contpose_check3 v1.2)

```
mkdir c3 && cp -r check2/src/* c3/ && mkdir c3/inputs && cp candidate.json control/candidate-mass0985.json c3/inputs/
cd c3
python3 check.py --candidate inputs/candidate.json --n 28 --core 499/500 --tau 1 --workers 10 \
        --node-budget 4000000000 --timeout 172800 --label main
python3 check.py --candidate inputs/candidate-mass0985.json --n 28 --core 499/500 --tau 1 --workers 10 \
        --node-budget 4000000000 --timeout 14400 --label control
```

`check.py` compiles the kernels in `kernel/` with the system C++ compiler on first use, reads only files inside its folder,
and writes `runs/<label>/receipt.json`: `status` VERIFIED with 43/43 slabs for the main run (`manifest.json` and the derived
inputs must match `check2/manifest.json`), REFUSED for the control. Python 3.12, g++ 13.
