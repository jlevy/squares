# ZH: 四十个正方形的连续姿态严格下界
# EN: A continuous-pose strict lower bound for forty squares

ZH: 允许独立平移、任意旋转和所有边界接触，要求方块内部两两不交。计算机辅助证明给出以下精确严格下界。
EN: Independent translations, arbitrary rotations and all boundary contacts are permitted, with pairwise disjoint square interiors. The computer-assisted proof gives the following exact strict lower bound.

```math
s(40)>\frac{1340000}{199529}=6.715815746082023\ldots
```

ZH: 使用 wand125 的固定矩形密度，直接覆盖边长 199529/200000 方块的连续中心和方向域。总质量为 3999/100，每方块捕获至少 4999/5000，计数矛盾余量为 1/500。
EN: Using wand125’s fixed rectangle density, verification directly covers the continuous center and orientation domain for squares of side 199529/200000. Total mass is 3999/100, each square captures at least 4999/5000, and the counting-contradiction margin is 1/500.

ZH: 完整数学见 [证明](PROOF.md)，操作步骤见 [复现](REPRODUCIBILITY.md)，验证边界见 [证据说明](VERIFICATION.md)，方法归属见 [来源](SOURCES.md)。
EN: See [proof](PROOF.md) for the mathematics, [reproduction](REPRODUCIBILITY.md) for commands, [verification](VERIFICATION.md) for evidence boundaries and [sources](SOURCES.md) for attribution.

ZH: [结果记录](results/verification.json) 区分作者认证与实际复跑。REPLAYED_SAME_KERNEL 只表示新构建和同一内核完整运行，不代表代码独立、方法独立或形式化认证。
EN: The [result record](results/verification.json) distinguishes author certification from actual replay. REPLAYED_SAME_KERNEL means a fresh build and complete execution of the same kernel, not code independence, method independence or formal certification.

ZH: 新连续姿态内核仍待外部独立审查。wand125 对此前 6.70854 的审查不覆盖本次新内核或更强数值。本结果不是装填见证、最优性证明或优先权声明。
EN: The new continuous-pose kernel still awaits external independent review. wand125’s review of the earlier 6.70854 result does not cover this new kernel or stronger value. This is not a packing witness, optimality proof or priority claim.

