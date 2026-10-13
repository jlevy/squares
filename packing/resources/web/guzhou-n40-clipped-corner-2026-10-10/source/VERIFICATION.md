# ZH: 验证范围与证据
# EN: Verification scope and evidence

ZH: 命题为 s(40)>335427/50000。完整验证包含源密度身份、全部 401 个连续中心域、全局密度上界、连续角度转移和严格计数端点，不只检查显示小数。
EN: The claim is s(40)>335427/50000. Complete verification covers source-density identity, all 401 continuous center domains, a global density bound, continuous-angle transfer and the strict counting endpoint, not merely displayed decimals.

ZH: results/verification.json 中 PENDING_INDEPENDENT_REPLAY 表示尚无对应完整运行记录；CODE_DISTINCT_FULL 只有在新构建、全量节点、双算法有限界与拒证测试都成功后产生。results/nodes.jsonl 保留每个节点的结果，输入和代码身份绑定至该次运行。
EN: PENDING_INDEPENDENT_REPLAY in results/verification.json means a corresponding complete execution record is absent. CODE_DISTINCT_FULL is produced only after a fresh build, every node, dual-algorithm finite bounds and refusal tests succeed. results/nodes.jsonl retains each node's result, with input and code identities bound to that execution.

ZH: 原研究的非轴覆盖使用 Tokoharu 的 C++ 内核；公开完整复验使用 Joshua Levy 项目的独立 Rust 实现。两者共享矩形测度、角网覆盖、平移截面导数与中心盒分支定界等数学结构，因此属于代码不同而非完整数学方法不同。
EN: The research non-axis coverage uses Tokoharu's C++ kernel; the public complete replay uses the independently implemented Rust verifier from Joshua Levy's project. They share the rectangle measure, angular covering, translated-section derivatives and center-box branch and bound, so the distinction is in code, not wholly different mathematical methods.

ZH: 401 节点由固定原密度生成新的精确输入声明，不修改 Rust 内核。正权矩形、权重及八重对称质量保持不变；源 JSON 的 201 节点历史元数据不作为新网声明或新成功凭据。
EN: A new exact input declaration generates 401 nodes from the fixed original density without modifying the Rust kernel. Positive rectangles, weights and eightfold symmetric mass remain unchanged; the source JSON's historical 201-node metadata is neither the new net declaration nor evidence of new success.

ZH: 全局密度界分别以区间加法线段树和显式纵向前缀扫描计算，两次展开采用不同 D4 生成方式。坐标和计数使用精确有理数及无界整数；数值显示仅用于阅读。
EN: The global density bound is computed by a range-add segment tree and an explicit vertical-prefix scan, with different D4 generation methods for the two expansions. Coordinates and counting use exact rationals and unbounded integers; numerical displays are for reading only.

ZH: 反向测试包含错误输入、改变参数、伪造峰值、缺失或重复节点、错误方向网、错误中心域、弱阈值、未决状态及故障注入。人工合成的测试节点仅用于测试拒证逻辑，不属于实际覆盖证据。
EN: Negative tests include wrong inputs, changed parameters, false peaks, missing or duplicated nodes, a wrong net or center domain, weak thresholds, unresolved status and fault injection. Synthetic test nodes test refusal logic only and are not actual coverage evidence.

ZH: 哈希保证的是字节与记录之间的对应，而非数学真理。验证器源代码、所用几何引理、编译器及 IEEE binary64 行为仍属计算证明信任边界。本结果没有形式化证明助手认证，也不宣称人类专家同行评议。
EN: Hashes establish correspondence between bytes and records, not mathematical truth. Verifier source, geometric lemmas, compilers and IEEE binary64 behavior remain within the computational-proof trust boundary. The result has no formal-assistant certification and claims no human expert peer review.
