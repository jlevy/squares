# ZH: 四十个正方形的严格下界 6.718
# EN: A strict lower bound of 6.718 for forty squares

```math
s(40)>\frac{3359}{500}=6.718.
```

ZH: 允许单位正方形独立平移、任意旋转及所有边界接触，要求内部两两不交。证明使用 685 个正权 D4 矩形轨道；522 个来自 wand125 原候选池，163 个是池外的新几何，全部权重重新认证。
EN: Unit squares may translate independently, rotate arbitrarily and have any boundary contacts, with pairwise disjoint interiors. The proof uses 685 positive D4 rectangle orbits: 522 from wand125's original pool and 163 new geometries outside it, with all weights certified anew.

ZH: 精确总质量为 3999/100；每个合法边长 3350/3359 的方块捕获至少 4999/5000。43 个完整三维角带加精确近轴补丁覆盖全部姿态，计数矛盾余量为 1/500。这不是姿态采样，也不是可行装填。
EN: Total mass is exactly 3999/100, and every legal side-3350/3359 square captures at least 4999/5000. Forty-three complete 3D slabs and an exact near-axis patch cover all poses, with counting contradiction margin 1/500. This is neither pose sampling nor a feasible packing.

ZH: [证明](PROOF.md)给出连续几何与严格端点；[复现](REPRODUCIBILITY.md)给出完整执行入口；[验证范围](VERIFICATION.md)区分同内核复跑与独立验证；[来源](SOURCES.md)保留署名及许可。
EN: [Proof](PROOF.md) gives the continuous geometry and strict endpoint; [reproduction](REPRODUCIBILITY.md) provides complete execution; [verification scope](VERIFICATION.md) distinguishes same-kernel replay from independent verification; [sources](SOURCES.md) retains credit and licensing.

ZH: 另有独立的[证书族障碍](OBSTRUCTION.md)：原文件全部 2526 个均匀矩形轨道不能在 X≥6.72 形成统一收费矛盾，两套完整精确程序检查相同有限对偶。它不是 s(40) 的上界或 6.72 的下界证明。
EN: A separate [certificate-family obstruction](OBSTRUCTION.md) excludes uniform charging at X≥6.72 using all 2526 original uniform rectangle orbits, with two complete exact programs checking the same finite dual. It is not an upper bound for s(40) or a lower-bound proof at 6.72.

ZH: 正下界为作者侧计算机辅助证明；实际运行状态见 results/verification.json。REPLAYED_SAME_KERNEL 不代表完整代码独立或形式化验证。wand125 对旧版 6.70854 的审查不覆盖本密度或连续内核；不作最优性或发表优先权声明。
EN: The positive bound is an author-side computer-assisted proof; actual execution status is in results/verification.json. REPLAYED_SAME_KERNEL does not mean full code-distinct or formal verification. wand125's review of the earlier 6.70854 result does not cover this density or continuous kernel; no optimality or publication-priority claim is made.
