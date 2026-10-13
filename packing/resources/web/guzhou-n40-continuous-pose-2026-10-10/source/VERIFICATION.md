# ZH: 验证范围
# EN: Verification scope

ZH: 数学结论为 s(40)>1340000/199529。作者侧证明状态是 CERTIFIED，新内核的公开独立审查仍未完成；完整重复运行的标签是 REPLAYED_SAME_KERNEL。
EN: The mathematical claim is s(40)>1340000/199529. The author-side proof status is CERTIFIED, external independent review of the new kernel remains incomplete, and a complete repeated execution is labeled REPLAYED_SAME_KERNEL.

ZH: 连续内核与研究冻结代码的 SHA-256 为 da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c；轴向内核为 f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d。仅公开执行和验收包装另行组织。
EN: The continuous kernel retains the research source SHA-256 da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c; the axis kernel is f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d. Only public execution and admission wrappers are reorganized.

ZH: 43 个闭角带完整覆盖半正切 [10^-6,83/200]；每带均覆盖全部合法中心。边长 997643/1000000 的完整轴向证书通过严格包含覆盖 [0,10^-6]。不允许将几个方向的成功替代角带穷尽。
EN: The 43 closed slabs completely cover half-tangents [10^-6,83/200], each over all legal centers. The complete axis certificate at side 997643/1000000 covers [0,10^-6] by strict containment. Success at selected directions cannot substitute for slab exhaustion.

ZH: 研究基准为 61,860,927 个姿态节点、30,930,485 个叶盒、14,096,668 次角度二分，以及 4,897,369 个轴向事件顶点。实际新运行统计由结果记录给出，而非硬编码为成功。
EN: The research baseline contains 61,860,927 pose nodes, 30,930,485 leaves, 14,096,668 angular bisections and 4,897,369 axial event vertices. Actual fresh-run counts are recorded rather than hardcoded as acceptance.

ZH: 7 组输入与验收测试包括 29 个错误收据变体；160 组独立有理数多边形测试比较 4,014 个姿态及 3,568 项面积。两个 IEEE 近邻方向在 1,000,008 个输入上逐位对照。还有错误舍入、FTZ、危险编译、低预算和合成正反例控制。
EN: Seven input/admission groups include 29 invalid receipt variants. The 160 independent rational-polygon cases compare 4,014 poses and 3,568 areas; both IEEE-neighbor directions are compared bitwise at 1,000,008 inputs. Controls also cover wrong rounding, FTZ, unsafe compilation, insufficient budgets and synthetic positive/negative cases.

ZH: 有限测试只能发现某些错误，不能代替全域数学证明。可信基础包括所列几何引理、区间核、输入与验收代码、编译器、C++/Python 运行时及 IEEE 硬件语义。
EN: Finite tests can expose certain defects but do not replace the global mathematical proof. The trust base includes the stated geometric lemmas, interval kernels, input/admission code, compiler, C++/Python runtimes and IEEE hardware semantics.

ZH: 新内核继承 Tokoharu 的平移导数结构并借鉴 Squares Project 的凹截面方法。不同来源代码的全域复验、方法独立验证、人类专家审查和形式化认证均不作已完成声明。
EN: The new kernel derives translation-derivative structure from Tokoharu and draws on the Squares Project’s concave-section method. Full distinct-code replay, method-independent verification, human expert review and formal certification are not claimed as completed.

ZH: 此前 Issue #485 中 wand125 对 e5abeb4d 和 6.70854 的肯定审查保持其原始范围，不自动扩展为新命题的审查。V/C/S 登记评级由维护者决定。
EN: wand125’s positive Issue #485 review of e5abeb4d and 6.70854 retains its original scope and does not automatically review the new claim. Maintainers determine register V/C/S ratings.

