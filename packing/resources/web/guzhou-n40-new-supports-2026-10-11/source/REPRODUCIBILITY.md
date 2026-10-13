# ZH: 完整复验
# EN: Complete reproduction

ZH: 正下界需要 x86_64 Linux、Python 3.10+ 标准库、支持 C++17、IEEE binary64 和 __int128 的 GCC。两套完整对偶检查还需要 Boost 头文件，研究版本为 1.83。已有依赖时数学复验完全离线，无需 Rust、NumPy 或优化器。
EN: The positive bound needs x86_64 Linux, Python 3.10+ standard libraries and GCC supporting C++17, IEEE binary64 and __int128. Both complete dual checks also need Boost headers, version 1.83 in the research execution. Mathematical replay is offline once dependencies exist, without Rust, NumPy or an optimizer.

ZH: 内容检查核对精确输入、哈希、文档配对及既有执行记录，不执行新的连续覆盖。
EN: Content audit checks exact inputs, hashes, paired documents and existing execution records, without freshly executing continuous coverage.

```sh
python3 -B verifier/audit.py --check
```

ZH: 下列完整入口在新外部目录重新生成精确输入、编译两个冻结内核、执行轴向及全部 43 个连续角带，并完成有限几何、IEEE 模式、验收拒证与两套完整支撑族对偶检查。运行目录内保留每个进程的原始输出、错误输出和退出状态。
EN: The full entry below regenerates exact inputs in a fresh external directory, compiles both frozen kernels, executes the axis and all 43 continuous slabs, and completes finite geometry, IEEE modes, admission refusals and both complete support-family dual checks. Raw stdout, stderr and exit status of every process remain in the runtime directory.

```sh
RUNROOT="$(mktemp -d)"
python3 -B verifier/run.py --output "$RUNROOT/replay" --workers 4
python3 -B verifier/audit.py --package --runtime "$RUNROOT/replay" --output "$RUNROOT/public"
```

ZH: 每个角带限 30000000 个节点及 1800 秒；任何未决、超时、弱收费或缺失角带都会失败。故意错误的算术模式、编译模式和反例测试必须以指定非零退出码被拒绝，不把所有测试退出码强求为零。
EN: Every slab has limits of 30000000 nodes and 1800 seconds; unresolved boxes, timeout, weak capture or a missing slab fail. Intentionally invalid arithmetic modes, compiler modes and counterexample controls must be refused with specified nonzero exit codes; not every test subprocess is expected to exit zero.

ZH: 主几何证据为 verification.json、slabs.jsonl 和 axis.json；独立有限负结果为 obstruction.json。打包只复制源码、精确数据、必要收据与说明，不包含编译产物、缓存或搜索状态。公开包自身再次核查所有哈希及执行身份。
EN: Primary geometry evidence is verification.json, slabs.jsonl and axis.json; the separately checked finite negative result is obstruction.json. Packaging copies only source, exact data, necessary receipts and explanations, excluding binaries, caches and search states. The public archive is itself rechecked for every hash and execution identity.

ZH: 单独重跑有限对偶可使用以下命令。两个精确实现均枚举 388×2526 个系数。其成功不代替正下界的三维连续覆盖。
EN: The finite dual can be rerun separately using the command below. Both exact implementations enumerate 388×2526 coefficients. Their success does not replace 3D continuous coverage for the positive bound.

```sh
DUALROOT="$(mktemp -d)"
python3 -B obstruction/run.py --output "$DUALROOT/check"
```

ZH: 编译参数固定为 -O3 -std=c++17 -fno-fast-math -ffp-contract=off，断言保持启用。Python 优化、fast-math、FTZ/DAZ、非最近舍入和未审查注入环境均不得用于接受。
EN: Compilation fixes -O3 -std=c++17 -fno-fast-math -ffp-contract=off with assertions enabled. Python optimization, fast-math, FTZ/DAZ, non-nearest rounding and unreviewed injection environments cannot be admitted.
