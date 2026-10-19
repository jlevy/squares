# ZH: 完整复验
# EN: Complete reproduction

ZH: 所需环境为 x86_64 Linux、Python 3.10 或以上的标准库，以及支持 __int128 和 IEEE binary64 的 GCC C++17 编译器。Windows 可使用已有 WSL；无需 Rust、NumPy、求解器或联网获取数学输入。
EN: Requirements are x86_64 Linux, the Python 3.10+ standard library and a GCC C++17 compiler supporting __int128 and IEEE binary64. Windows may use existing WSL; Rust, NumPy, solvers and network acquisition of mathematical inputs are unnecessary.

ZH: 下列检查核对全部文件哈希、配对双语文档、精确输入与已有运行记录，不新执行连续姿态覆盖。
EN: The following audit checks every file hash, paired bilingual documents, exact inputs and retained execution records, without freshly executing continuous-pose coverage.

```sh
python3 -B verifier/audit.py --check
```

ZH: 完整运行要求此前不存在的外部目录；源码及原始证据不覆盖。下列命令重新构建和测试两个冻结内核，执行 43 个完整连续角带、完整轴向证明及精确计数，再生成已复跑归档。
EN: A complete run requires a new external directory and does not overwrite source or original evidence. These commands rebuild and test both frozen kernels, execute 43 complete continuous slabs, the complete axis proof and exact counting, then produce a replayed archive.

```sh
RUNROOT="$(mktemp -d)"
python3 -B verifier/run.py --output "$RUNROOT/replay" --workers 4
python3 -B verifier/audit.py --package --runtime "$RUNROOT/replay" --output "$RUNROOT/public"
```

ZH: 连续内核固定编译参数为 -O3 -std=c++17 -fno-fast-math -ffp-contract=off，纯整数轴向程序为 -O2 -std=c++17。不得使用 Python 优化模式、NDEBUG、fast-math、FMA contraction、FTZ/DAZ 或非最近舍入；危险环境模式受测试覆盖。
EN: The continuous kernel uses -O3 -std=c++17 -fno-fast-math -ffp-contract=off, and the integer-only axis program uses -O2 -std=c++17. Python optimized mode, NDEBUG, fast-math, FMA contraction, FTZ/DAZ and non-nearest rounding are forbidden; unsafe environment modes are covered by tests.

ZH: 两份大体积文本输入由原始密度重建并核对固定 SHA-256，不重复装入源码。verification.json、slabs.jsonl、axis.json 保留全部数学验收信息；逐带原始数值 stdout、参数、退出码及身份包括在 slabs.jsonl。
EN: Both larger text inputs are regenerated from the original density and checked against fixed SHA-256 values rather than duplicated in the source. verification.json, slabs.jsonl and axis.json retain mathematical acceptance evidence; slabs.jsonl includes each slab’s original numerical stdout, arguments, exit status and identities.

ZH: 额外构建日志和编译产物仅在运行目录保留。任何超时、未决盒、缺失角带、错误输入或不足下界都阻断通过；重复执行同一内核不提升独立性等级。
EN: Additional build logs and binaries remain in the runtime directory only. Timeouts, unresolved boxes, missing slabs, wrong inputs or insufficient lower bounds prevent acceptance; reexecuting the same kernel does not raise its independence level.

ZH: GitHub Actions 配置使用相同完整入口。只有成功完成的新运行才能生成正式归档；仅检查已有哈希不是全量验证。
EN: The GitHub Actions configuration uses the same complete entry point. Only a successful fresh execution can generate the final archive; checking retained hashes is not full verification.

