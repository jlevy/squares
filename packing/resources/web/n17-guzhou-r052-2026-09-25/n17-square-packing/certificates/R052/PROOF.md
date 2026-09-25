# R052 证明 / R052 proof

定义 s(17) 为容纳十七个单位正方形的最小正方形边长，允许旋转和边界接触，但内部两两不交。 / Define s(17) as the minimum side of a square containing seventeen unit squares, allowing rotation and boundary contact but requiring pairwise disjoint interiors.

原字节证书保留历史生成 provenance 和旧分支哈希，这些备注不是最终几何状态的断言；证明以当前 entries、资源及精确复验为准。 / The original-byte certificate retains historical generation provenance and earlier branch hashes; these notes do not assert the final geometric state, which is established by current entries, resources and exact replay.

## 缩放、资源与预算 / Scaling, resources and budget

假设端点 231001/50000 可装填；按 A=230650/231001 缩放后，十七个边长 A 的父方形位于边长 L=4613/1000 的容器中。 / Suppose packing is possible at 231001/50000; scaling by A=230650/231001 yields seventeen parent squares of side A in a container of side L=4613/1000.

证书列出 2354 个 D4 点轨道，按每个轨道的字典序展开为 18585 个互异点；514 个三点中至少两点的阈值轨道和 54 个通用阈值轨道共生成 4504 个物理组，其中六个通用轨道具有正权五点中至少三点的收费。组索引引用完整点表，包括零权点。 / The certificate lists 2354 D4 point orbits expanded in lexicographic order within each orbit into 18585 distinct points; 514 two-of-three and 54 generic threshold orbits yield 4504 physical groups, with six positive three-of-five generic orbits. Group indices refer to the complete point table, including zero-weight points.

点权与组权均为非负整数。一个内核包含点时收取点权，包含某 m 点组至少 k 个点时收取组权。两两不交内核至多使用一个点一次、激活同一组 floor(m/k) 次，因此总收费至多为精确预算 16990246659579。 / Point and group weights are nonnegative integers. A core is charged a point weight when it contains the point and a group weight when it contains at least k points of an m-point group. Disjoint cores use a point at most once and activate a group at most floor(m/k) times, giving the exact total budget 16990246659579.

## 全角度严格内含 / Strict containment over every angle

以半角参数 u=tan(θ/2) 表示方向，c(u)=(1−u²)/(1+u²)、s(u)=2u/(1+u²)。资源具有完整 D4 对称性，所以任意单个父方形的收费可在对称变换下归约到 θ∈[0,π/4]，无需同时旋转整个装填。 / Write orientations using u=tan(θ/2), with c(u)=(1−u²)/(1+u²) and s(u)=2u/(1+u²). Complete D4 resource symmetry reduces the charge of each individual parent to θ∈[0,π/4] without requiring a common rotation of the whole packing.

15721 个连续区间 [a,b] 无空隙覆盖 0 至 207107/500000；末端满足 u²+2u−1=309449/250000000000>0，故覆盖 tan(π/8)。每行 [a,b,t,B] 给出同中心、方向 t、边长 B 的闭内核。 / The 15721 contiguous intervals [a,b] cover 0 through 207107/500000 without gaps; the last endpoint satisfies u²+2u−1=309449/250000000000>0 and therefore covers tan(π/8). Each row [a,b,t,B] specifies a concentric closed core of orientation t and side B.

独立有理检查核对全部 62884 条端点轴向投影不等式，最小严格余量为 4613/9240040000000000000。对核心与父方向之差 δ，其范围满足 |δ|≤π/4，投影因子 cosδ+|sinδ| 随 |δ| 单调增加，因此端点检查推出整个区间的严格内含。 / Independent rational checks establish all 62884 endpoint axial-projection inequalities, with minimum strict margin 4613/9240040000000000000. The core-to-parent angle difference satisfies |δ|≤π/4, where cosδ+|sinδ| increases with |δ|, so endpoint checks imply strict containment throughout each interval.

令 r=A·min(c(a)+s(a),c(b)+s(b))/2，则包含全部合法父中心的方盒为 [r,L−r]²。由于 c+s 在区间内没有内部极小值，这个盒包含本区间内全部合法父中心。 / Set r=A·min(c(a)+s(a),c(b)+s(b))/2; the enclosing parent-centre box is [r,L−r]². Since c+s has no interior minimum on the interval, this box contains every legal parent centre in that interval.

## 精确中心扫描及边界 / Exact centre scan and boundaries

在核心坐标系中，一个点被闭核包含的条件成为中心的轴向闭矩形；捕获某个点子集对应矩形交。k-of-m 指示函数等于从 j=k 到 m 的各 j 元子集指标之和，系数为 (−1)^(j−k)·C(j−1,k−1)。 / In core coordinates, containing a point is an axis-aligned closed rectangle condition on the centre; capturing a subset corresponds to rectangle intersection. The k-of-m indicator is the sum over j-element subsets for j=k through m with coefficient (−1)^(j−k)·C(j−1,k−1).

Python 实现通过整数旋转坐标、矩形事件与凸合法域的精确投影扫描开放事件胞元；Node 实现使用独立有理/BigInt 几何和解析条带极值。两个实现的坐标与交点比较不依赖浮点舍入。 / The Python implementation scans open event cells using integer rotated coordinates, rectangle events and exact projections of the convex legal domain; Node uses separate rational/BigInt geometry and analytic strip extrema. Neither implementation relies on floating-point rounding for coordinate or intersection comparisons.

Node 未合并的绝对系数质量为 26783030323131<2^50，段树中有效整数加减与比较保持精确；大坐标使用原始 JSON 整数 token 无损读取。Python 的相应整数扫线在 int64 安全界内。LP 仅用于发现候选，不是证明步骤。 / Node's unmerged absolute coefficient mass is 26783030323131<2^50, keeping effective integer tree additions, subtractions and comparisons exact; large coordinates are read losslessly from original JSON integer tokens. The corresponding Python integer sweep is within its int64 bound. LP is used only to discover candidates, not as a proof step.

有限站点中，任何不在边界中心闭核内的点，在充分小邻域仍在核外；因此附近中心捕获集是边界捕获集的子集。非负单调收费使边界收费不低于逼近它的非事件内部值。合法凸中心域有非空内部，边界可由此类点逼近，故退化矩形和事件边界不能隐藏更小收费。 / With finitely many sites, a point outside the closed core at a boundary centre stays outside in a sufficiently small neighbourhood; nearby capture sets are therefore subsets of the boundary capture set. Nonnegative monotone charges make boundary charges no smaller than approaching nonevent interior values. The convex legal-centre domain has nonempty interior and such points approach its boundary, so degenerate rectangles and event boundaries cannot conceal a smaller charge.

完整独立账本覆盖行 0 至 15720，每行恰一次；最低收费为 999426274093，仅第 15555 与 15556 行达到。123 个原始分块及逐行账本随包提供；完整复演必须覆盖全部行。 / The complete independent ledger covers rows 0 through 15720 exactly once; its minimum is 999426274093, attained only by rows 15555 and 15556. All 123 original blocks and the per-row ledger are included; full replay must cover every row.

## 严格矛盾与端点 / Strict contradiction and endpoint

闭内核严格位于父方形开内部，故十七个闭内核两两不交，包括边界。其总收费至少 17×999426274093，比总预算多 2，矛盾；端点及全部更小容器均不可装填。 / Closed cores lie strictly inside parent interiors, so the seventeen closed cores are pairwise disjoint, including their boundaries. Their total charge is at least 17×999426274093, exceeding the total budget by 2, a contradiction; the endpoint and every smaller container are infeasible.

最小装填边长可达到：取可行边长趋向下确界的有界序列，中心与方向处于紧集，收敛子列保留容器包含关系；若极限中两方形内部相交，正余量会使充分靠后的两方形也相交，矛盾。因此端点被排除推出严格结论 s(17)>4.62002。 / The minimum feasible side is attained: take a bounded sequence of feasible sides approaching its infimum, with centres and orientations in a compact set. A convergent subsequence preserves containment; any interior overlap in the limit would have positive slack and persist in sufficiently late packings, a contradiction. Excluding the endpoint therefore yields the strict conclusion s(17)>4.62002.
