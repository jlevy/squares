# 复验说明 / Reproduction

快速模式只读取冻结证书和完整 Node 账本；包含模式另行重算资源闭包、预算和角度严格包含。两种 full 模式分别重新计算全部 15721 行。 / Quick mode reads the frozen certificate and complete Node ledger; containment mode additionally recomputes resource closure, budget and strict angular containment. Each full mode freshly recomputes all 15721 rows.

所有命令从仓库根目录运行，输出写入尚不存在的包外目录；不允许 Python -O。 / Run all commands from the repository root with a nonexistent output directory outside the package; Python -O is rejected.

```bash
python -X utf8 -B -S certificates/R052/verify.py --output .replay-runs/r052-records
python -X utf8 -B -S certificates/R052/verify.py --containment --output .replay-runs/r052-containment
python -m pip install -r certificates/R052/requirements-full.txt
python -X utf8 -B certificates/R052/verify.py --python-full --jobs 4 --output .replay-runs/r052-python
python -X utf8 -B -S certificates/R052/verify.py --bigint-full --jobs 4 --output .replay-runs/r052-bigint
```

记录和包含仅需 Python 标准库；Python 全扫使用 requirements-full.txt 锁定的 NumPy、Numba、llvmlite，测试环境为 Python 3.12；BigInt 全扫需要 Node.js 24 或更新版本。 / Records and containment use only the Python standard library; the Python full scan uses the NumPy, Numba and llvmlite versions pinned in requirements-full.txt, tested with Python 3.12; the BigInt full scan requires Node.js 24 or newer.

BigInt 模式从固定 R038 提交下载单个原源，再执行两阶段确定性字节编辑；原源、中间结果和最终检查器均绑定 SHA-256。离线时可通过 --source 指定该精确 R038 原源文件。重建文件只写到本次输出目录。 / BigInt mode downloads one source file from the pinned R038 commit and applies two deterministic byte-edit stages, binding the original, intermediate and final checker by SHA-256. For offline use, pass that exact R038 source with --source. Reconstruction writes only to the current output directory.

候选原字节 SHA-256 为 d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825；最终 Node 检查器 SHA-256 为 82fad041d66bc7a0f14d9dfe9b9282d8562d50fc4844649d2e684414a7ba24b1。 / The original candidate SHA-256 is d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825; the final Node checker SHA-256 is 82fad041d66bc7a0f14d9dfe9b9282d8562d50fc4844649d2e684414a7ba24b1.

原主计算由 13017 个直接最终区间和 2704 个保守继承下界组成，独立 Node 已新算全部 15721 行；这些继承记录不用于填补独立扫描的范围。公开 Python full 入口则重新计算每一行，不依赖私有继承历史。 / The original primary computation comprises 13017 directly computed final intervals and 2704 conservative inherited lower bounds; independent Node freshly computed all 15721 rows, so inherited records fill no gap in that scan. The public Python full entry recomputes every row without private inheritance history.

默认记录 PASS 不是一次新中心扫描。隔离发布验证的真实执行范围见仓库 verification/R052.json；CI 是否通过以对应提交的 GitHub Actions 状态为准。 / A default records PASS is not a fresh centre scan. Actual isolated publication-validation scope is recorded in verification/R052.json at repository level; CI success is determined by GitHub Actions for the corresponding commit.

裸 Node 检查器不自行阻止小数行界或绑定自身代码，本公开入口只构造整数分块，并在前后检查代码、候选及逐行账本；请使用 verify.py 进行接受判定。 / The bare Node checker does not itself reject fractional row bounds or bind its own source; this public entry constructs only integer chunks and checks the code, candidate and per-row ledger before and after execution. Use verify.py for acceptance decisions.
