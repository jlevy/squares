# ZH: 四十个单位正方形的严格下界
# EN: A strict lower bound for forty unit squares

ZH: 对允许独立平移、任意旋转、边界接触且内部两两不交的四十个单位正方形，计算机辅助证明给出以下严格下界。
EN: For forty unit squares with independent translations, arbitrary rotations, boundary contacts and pairwise disjoint interiors, the computer-assisted proof gives the following strict lower bound.

```math
s(40)>\frac{335427}{50000}=6.70854.
```

ZH: 证明使用 wand125 的固定矩形密度、401 个有理半正切节点、连续中心域覆盖及一个全局密度上界；不依赖装填接触图、刚性或搜索失败。较简洁的完整内核论证另给出 s(40)>6.70848908。
EN: The proof uses wand125's fixed rectangle density, 401 rational half-tangent nodes, continuous-center coverage and one global density bound; it does not rely on packing contact graphs, rigidity or failed searches. A simpler full-core argument also gives s(40)>6.70848908.

ZH: 数学论证见 [证明](PROOF.md)，完整执行步骤见 [复现说明](REPRODUCIBILITY.md)，证据范围见 [验证说明](VERIFICATION.md)，署名和许可见 [来源](SOURCES.md)。
EN: See [proof](PROOF.md) for the mathematics, [reproduction](REPRODUCIBILITY.md) for complete execution, [verification](VERIFICATION.md) for evidence boundaries and [sources](SOURCES.md) for credit and licensing.

ZH: [运行记录](results/verification.json) 是本版本的验证状态来源。完整运行必须重新检查全部 401 个连续中心域，且通过双算法密度上界、精确转移和拒证测试；内容哈希检查不能代替这些计算。
EN: The [execution record](results/verification.json) is the verification-status source for this version. A complete run must freshly check all 401 continuous center domains and pass dual-algorithm density bounds, exact transfer and refusal tests; content hashes do not replace these calculations.

ZH: 连续节点验证采用 squares 项目的独立 Rust 实现；CODE_DISTINCT_FULL 表示不同实现共享部分数学结构，不表示完整方法独立、形式化证明或人类专家同行评议。现有密度与验证器不属于本项目的原创贡献，也不作当前最佳或首次发表的声明。
EN: Continuous nodes are checked by the squares project's independently implemented Rust verifier. CODE_DISTINCT_FULL means distinct implementations with some shared mathematical structure, not complete method independence, formal proof or human expert peer review. The existing density and verifier are not original contributions of this project, and no current-best or publication-priority claim is made.
