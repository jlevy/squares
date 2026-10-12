# ZH: 验证范围
# EN: Verification scope

ZH: 本版本的主结论为 s(40)>3359/500。连续及轴向 C++ 源码与已公开的 1340000/199529 版本逐字节相同；支撑和权重已经改变，所有新输入及全部连续覆盖必须从头重新验证。
EN: The primary claim is s(40)>3359/500. Continuous and axial C++ sources are byte-identical to the published 1340000/199529 version. Supports and weights have changed, so every new input and all continuous coverage must be verified anew.

ZH: 正证明分为非负有理密度、D4 对称归约、随角度变化的合法中心域、全盒包含或排除缓存、凹截面下界、平移导数界、43 个角带的有限穷尽、完整近轴补丁以及严格计数与端点。每部分的完整论证见 PROOF.md。
EN: The positive proof comprises nonnegative rational density, D4 symmetry, angle-dependent legal centers, whole-box containment/exclusion caching, concave-section lower bounds, translation-derivative bounds, finite exhaustion of 43 slabs, a complete near-axis patch, and strict counting with the endpoint. PROOF.md gives the complete argument for each part.

ZH: 研究阶段两次完整运行各有 60,500,889 个节点、30,250,466 个叶盒和 13,812,428 次角度二分，轴向均枚举 10,843,849 个顶点，非计时输出一致。发布版本另从公开源码完整复跑；实际编译器、代码、输入、二进制和耗时记录在 results 中。
EN: Two complete research executions each have 60,500,889 nodes, 30,250,466 leaves and 13,812,428 angle bisections, with 10,843,849 axial vertices and matching nontiming outputs. The publication version is additionally replayed completely from its public source; actual compiler, code, input, binary and timing identities are recorded in results.

ZH: REPLAYED_SAME_KERNEL 表示实际重建并执行同一几何内核，不是另一套完整独立实现。精确有限多边形对照和八组验收测试仅检测错误，不能把有限测试成功当成整个连续域的证明。
EN: REPLAYED_SAME_KERNEL means actual rebuilding and execution of the same geometry kernel, not another complete independent implementation. Exact finite-polygon comparisons and eight admission-test groups detect errors only; passing finite tests is not proof over the continuous domain.

ZH: 支撑族负结果由 Python Fraction 和 C++ Boost 任意精度有理数的两套完整程序重新计算。二者的 D4 展开与裁剪实现不同，但共享源矩形、对偶姿态及多边形面积的数学定义。其代码独立性只适用于有限负结果。
EN: The support-family negative result is recomputed by complete Python Fraction and C++ Boost arbitrary-precision rational programs. Their D4 expansion and clipping implementations differ, while sharing source rectangles, dual poses and the definition of polygon area. Code independence applies only to this finite negative result.

ZH: 输入、参数、阈值、完整角带集合、进程退出及生成物哈希分别核验；故意伪造或删减证据会被拒绝。哈希只绑定身份，不证明数学正确；编译器、运行时、IEEE 硬件和明确的几何引理仍属于信任基础。
EN: Input, parameters, thresholds, complete slab sets, process exits and output hashes are checked separately; deliberately forged or incomplete evidence is refused. Hashes bind identity, not mathematical truth. Compilers, runtimes, IEEE hardware and the explicit geometric lemmas remain within the trust base.

ZH: 6.718 尚无外部独立几何审查、完整方法独立验证或形式化证明。旧版 6.70854 的 wand125 审查保留其原范围。这里的状态不是 jlevy/squares 已授予的 V/C/S 评级，也不表示维护者已接受或最优性已证明。
EN: The 6.718 result has no external independent geometry review, full method-distinct verification or formal proof. wand125's review of 6.70854 retains its original scope. These statuses are not V/C/S ratings assigned by jlevy/squares and do not mean maintainer acceptance or proved optimality.
