# ZH: 完整复验
# EN: Complete reproduction

ZH: 数学输入与验证源码随仓库提供。环境要求为 Linux、Python 3.11 或更高及 Rust 1.98.0；依赖版本和校验值由 Cargo.lock 固定。Windows 可使用 Linux 子系统。无需 NumPy、商业求解器或原研究目录。
EN: Mathematical inputs and verifier sources are included. Requirements are Linux, Python 3.11 or later and Rust 1.98.0; Cargo.lock pins dependency versions and checksums. Windows can use a Linux subsystem. NumPy, commercial solvers and the original research directory are unnecessary.

ZH: 内容检查核对全部 SHA-256、双语文档配对、文件集合、精确密度和有限转移；它不是 401 个连续中心域的新运行。
EN: Content checks cover every SHA-256, bilingual document pairing, the file set, exact density and finite transfer; they are not a fresh run over the 401 continuous center domains.

```sh
python3 -B verifier/release.py --check
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

ZH: 完整复验使用一个位于源码目录之外的新运行目录。首次准备工具链与固定依赖需要联网；prepare.py 按锁文件核对每个依赖归档的 SHA-256。其后的构建与数学验证使用离线模式。
EN: Complete reproduction uses a fresh run directory outside the source tree. Initial toolchain and pinned-dependency preparation require networking; prepare.py checks every dependency archive's SHA-256 against the lockfile. Subsequent builds and mathematical verification run offline.

```sh
rustup toolchain install 1.98.0 --profile minimal
RUNTIME=$(mktemp -d)
python3 -B verifier/prepare.py --runtime "$RUNTIME"
RUSTUP_TOOLCHAIN=1.98.0 python3 -B verifier/run.py --runtime "$RUNTIME" --workers 4
```

ZH: 执行包括 Python 拒证测试、Rust 单元与对抗测试、全新 release 构建、401 个节点的完整连续覆盖、两种全局密度扫描以及精确计数。缺失节点、错误角网、错误中心域、低阈值、注入故障或非零退出均使运行失败。
EN: Execution includes Python refusal tests, Rust unit and adversarial tests, a fresh release build, complete continuous coverage at 401 nodes, two global-density sweeps and exact counting. Missing nodes, an incorrect net or center domain, a weak threshold, fault injection or a nonzero exit fail the run.

ZH: 最终记录写入运行目录的 replay/verification.json，节点原始记录写入 replay/nodes/，汇总节点写入 replay/nodes.jsonl，各阶段标准输出、错误输出及退出码也保留。源码、输入和二进制身份分别记录，并检查执行前后源码未变。
EN: The final record is written to replay/verification.json in the run directory, raw node records to replay/nodes/, and combined nodes to replay/nodes.jsonl; stage stdout, stderr and exit codes are also retained. Source, input and binary identities are recorded separately, and source immutability during execution is checked.

ZH: 下列命令从已完成的运行生成最小公开归档，并再次核对归档中的执行身份、数学组合、文档和哈希。源码仓库不会被生成物覆盖。
EN: The following command creates a minimal public archive from a completed run and rechecks its execution identities, mathematical composition, documents and hashes. Generated outputs do not overwrite the source repository.

```sh
OUTPUT=$(mktemp -d)
python3 -B verifier/release.py --package --runtime "$RUNTIME" --out "$OUTPUT"
```

ZH: 自动化运行采用同一入口，不把仅有内容检查或历史成功标志当作完整复验。使用新的运行目录可保证没有继承旧构建产物；未经审查的编译包装器、额外 Rust 编译参数及 Python 优化模式被拒绝。
EN: Automation uses the same entry point and does not treat content checks or historical success flags as a complete replay. A fresh run directory prevents inherited build outputs; unreviewed compiler wrappers, extra Rust flags and Python optimized mode are refused.
