# ZH: 401 节点密度下界证明
# EN: A 401-node density lower-bound proof

## ZH: 定义与精确参数
## EN: Definition and exact parameters

ZH: s(40) 是四十个可任意旋转、内部两两不交的单位正方形装入正方形容器的最小边长，允许所有边界接触。以下参数均按精确有理数解释。
EN: s(40) is the minimum side of a square container holding forty arbitrarily rotated unit squares with pairwise disjoint interiors; all boundary contacts are allowed. Every parameter below is interpreted as an exact rational.

```text
N=40; L=67/10; K=[0,L]^2; B=9977/10000
M=3999/100; D=83/80000; theta_j=2 atan(jD), j=0,...,400
tau=10001/10000; X=335427/50000; q=L/X=335000/335427
h=514946944479/10^15; H=2818711359413/10^9
```

## ZH: 非负对称测度
## EN: The nonnegative symmetric measure

ZH: 原始输入的有限十进制坐标和分数权重按有理数读取。每个正权矩形 R 在容器的八个 D4 像上分别产生密度 w/(8 area(R))；重复像保留重数，重叠密度相加。
EN: Finite decimal coordinates and fractional weights in the source input are read as rationals. Each positive rectangle R contributes density w/(8 area(R)) on each of its eight D4 images; repeated images retain multiplicity and overlapping densities add.

ZH: 480 个正权代表产生 3840 个矩形项。旋转反射展开和顶点符号交换展开逐项核对，确认非负性、支撑包含于 K、D4 不变性及总质量 M=3999/100。所需积分为绝对连续面积测度 μ。
EN: The 480 positive representatives produce 3840 rectangle terms. A rotation-reflection expansion and a signed-permutation vertex expansion are reconciled term by term, establishing nonnegativity, support within K, D4 invariance and total mass M=3999/100. Their integral defines the absolutely continuous area measure μ.

ZH: 源件保持不变；验证时生成的节点输入仅保留正权项，并把角网声明设为 D=83/80000、节点数 401。删除零权项不改变测度；该派生输入的哈希和原件哈希分别记录。
EN: The source remains unchanged. The generated nodal input retains only positive-weight terms and declares D=83/80000 with 401 nodes. Removing zero-weight terms does not change the measure; the derived-input hash and source hash are recorded separately.

## ZH: 全部连续中心域的节点覆盖
## EN: Nodal coverage over every continuous center domain

ZH: 节点命题为：对每个 j=0,...,400，每个完全位于 K 内、方向为 theta_j 的 B 正方形均捕获至少 tau 的质量。令 c_j=(1−j²D²)/(1+j²D²)、s_j=2jD/(1+j²D²)，则合法中心域为 [B(c_j+s_j)/2,L−B(c_j+s_j)/2]^2。
EN: The nodal proposition is that, for every j=0,...,400, every side-B square of orientation theta_j fully contained in K captures mass at least tau. Put c_j=(1−j²D²)/(1+j²D²) and s_j=2jD/(1+j²D²); the legal center domain is [B(c_j+s_j)/2,L−B(c_j+s_j)/2]^2.

ZH: 容器中心的四分之一转动保持测度与正方形方向模 π/2，可将中心域缩到一个象限；不能以会改变方向符号的反射代替这一步。输入明确采用完整 B 正方形中心域，而不是较窄的单位父方块分箱中心域。
EN: Quarter-turns about the container center preserve the measure and square orientation modulo π/2, reducing centers to one quadrant; reflections that change the orientation's sign cannot replace this step. Admission explicitly uses the complete side-B center domain, not the narrower per-bin domain for unit parents.

ZH: 水平方向的矩形交长在支撑端点平移 ±B/2 时才改变斜率。相邻横纵断点组成的每个单元内，总捕获量为双线性函数，是四个顶点值的凸组合；包含域边界的完整事件扫描因此证明整个连续域。
EN: For the horizontal direction, rectangle overlap lengths change slope only at support endpoints shifted by ±B/2. Within every cell between consecutive horizontal and vertical breakpoints, capture is bilinear and is a convex combination of its four vertex values. A complete event sweep including domain boundaries therefore proves the continuous domain.

ZH: 非水平方向使用区间分支定界。捕获函数 F 的平移导数由矩形相对两边上的截长之差给出；若中心值下界为 f、盒半宽为 dx,dy、导数绝对值上界为 Gx,Gy，则整个盒有 F≥f−dx Gx−dy Gy。面积密度有界，沿平移线绝对连续，故几乎处处的导数界足够。
EN: Nonhorizontal directions use interval branch and bound. Translation derivatives of capture F are differences of section lengths on opposite rectangle edges. A center lower bound f, box half-widths dx,dy and derivative bounds Gx,Gy give F≥f−dx Gx−dy Gy throughout the box. Bounded area density gives absolute continuity along translation lines, so almost-everywhere derivative bounds suffice.

ZH: 原 C++ 路线用区间核验的内接多边形给出中心面积下界；本版 Rust 路线用凹截面函数下方的梯形并独立构造仿射边长外包。子盒闭并集覆盖父盒；只有所有盒均达到 tau 后才接受。资源用尽、非有限数值或未决盒均不是成功。
EN: The original C++ route bounds center area by interval-certified inscribed polygons. This version's Rust route uses trapezoids below concave section functions and independently constructed affine edge enclosures. Closed child boxes cover their parent; acceptance requires every box to reach tau. Resource exhaustion, nonfinite values and unresolved boxes are not success.

ZH: Rust 区间内核及其测试保持源版本不变，底层算术和数值误差守卫的证明见 [固定版本的可靠性说明](https://github.com/jlevy/squares/blob/ef79288a498b5469e6b944f7b150d83aeeab5f94/packing/sqverify_fast/SOUNDNESS.md)。完整运行逐一核对 401 个节点、精确角网、中心域、阈值和输入身份，不从历史日志或部分节点推断全量覆盖。
EN: The Rust interval kernel and tests remain unchanged from the source revision; proofs of its arithmetic and numerical-error guards are in the [pinned soundness account](https://github.com/jlevy/squares/blob/ef79288a498b5469e6b944f7b150d83aeeab5f94/packing/sqverify_fast/SOUNDNESS.md). Complete execution checks all 401 nodes, the exact net, center domain, threshold and input identity, without inferring full coverage from historical logs or a subset.

## ZH: 不削角的直接结论
## EN: A direct result without clipping

ZH: 由 D4 不变性可逐个父方块将积分问题的方向折到 [0,π/4]，无需各自变换后的方块仍组成装填。末节点 400D=83/200>√2−1，角网覆盖 π/4。相邻角间隔的一半满足 tan((theta_(j+1)−theta_j)/2)=D/(1+j(j+1)D²)≤D。
EN: D4 invariance folds each parent's integral problem separately into [0,π/4], without requiring individually transformed parents to remain a packing. The final tangent 400D=83/200 exceeds √2−1, so the net reaches π/4. Half an adjacent angular gap satisfies tan((theta_(j+1)−theta_j)/2)=D/(1+j(j+1)D²)≤D.

ZH: 最近节点的角误差不超过 atan D，因此边长 gamma=B(1+D)/sqrt(1+D²) 的父方块包含一个合法同心节点 B 正方形，捕获至少 tau。40tau−M=7/500>0，缩放并排除端点得到以下较弱但无需密度峰值的结论。
EN: The nearest-node error is at most atan D. A parent of side gamma=B(1+D)/sqrt(1+D²) therefore contains a legal concentric nodal B square and captures at least tau. Since 40tau−M=7/500>0, scaling and endpoint exclusion give the following weaker result without a density-peak estimate.

```math
s(40)>\frac{67000\sqrt{6400006889}}{798988091}>6.70848908.
```

## ZH: 精确全局密度上界
## EN: An exact global density upper bound

ZH: 每项密度 rho 向上取整到 ceil(10^9 rho)/10^9，矩形坐标不取整。在全部精确坐标确定的开二维单元上，一种线段树扫描和另一种显式纵向前缀扫描分别求出最大整数叠加高度，并核对一致。
EN: Round each density rho upward to ceil(10^9 rho)/10^9 without rounding rectangle coordinates. Over all open two-dimensional cells defined by the exact coordinates, a segment-tree sweep and a separate explicit vertical-prefix scan compute and reconcile the maximum integer overlap height.

ZH: 同一横坐标的所有进入和离开事件处理完毕后才对下一开条带取最大值；纵向叶单元也为相邻事件间的开区间。Python 使用无界整数。结果为 g≤H=2818711359413/10^9 几乎处处，事件边界线的面积为零，不影响积分上界。
EN: All entering and leaving events at one abscissa are processed before taking the maximum in the next open slab; vertical leaf cells are open intervals between adjacent events. Python uses unbounded integers. The result is g≤H=2818711359413/10^9 almost everywhere; area-zero event boundaries do not affect integral bounds.

## ZH: 合法参考方块与削角损失
## EN: Legal reference squares and clipped-corner loss

ZH: 令 delta0=2 atan h。精确核算 B(cos delta0+sin delta0)≤q。对夹在相邻节点间的父方向 alpha，若上节点误差不超过 delta0，选完全包含于父方块内的同心 B 正方形。
EN: Set delta0=2 atan h. Exact arithmetic checks B(cos delta0+sin delta0)≤q. For a parent orientation alpha between adjacent nodes, select the concentric side-B square wholly inside the parent whenever the upper-node error is at most delta0.

ZH: 否则选下节点，其误差小于 beta=2 atan b，其中 b=(D−h)/(1+Dh)。该参考方块仍在 K 内，因为下节点角度不超过 alpha≤π/4 且 B≤q，使其轴向包围宽度不超过父方块。略超过 π/4 的上节点不妨碍第一分支的相对角度包含论证。
EN: Otherwise select the lower node, whose error is less than beta=2 atan b, where b=(D−h)/(1+Dh). This reference still lies in K: the lower-node angle does not exceed alpha≤π/4 and B≤q, so its axis-aligned extent is at most the parent's. An upper node slightly beyond π/4 does not affect the first branch's relative-angle containment argument.

ZH: 对 0≤delta≤beta≤π/4，设 c=cos delta、s=sin delta、e=max(0,B(c+s)−q)。参考方块在父方块外的部分为四个内部不交的直角三角形，各腿为 e/(2c)、e/(2s)，总面积为 e²/(2cs)，delta=0 时为零。q≥B 保证这些角不重叠。
EN: For 0≤delta≤beta≤π/4, put c=cos delta, s=sin delta and e=max(0,B(c+s)−q). The reference outside its parent consists of four interior-disjoint right triangles with legs e/(2c), e/(2s), and total area e²/(2cs), zero at delta=0. The condition q≥B prevents overlap among the corners.

ZH: 令 a=q/B≥1、z=cos delta+sin delta。在正损失区，归一化面积为 (z−a)²/(z²−1)，对 z 的导数为 2(z−a)(az−1)/(z²−1)²≥0。故 beta 端点的面积 A 控制全部角误差；端点正弦余弦均由有理半正切精确求出。
EN: Put a=q/B≥1 and z=cos delta+sin delta. On the positive-loss range, normalized area is (z−a)²/(z²−1), whose derivative in z is 2(z−a)(az−1)/(z²−1)²≥0. The endpoint area A at beta therefore bounds every angular error; endpoint sine and cosine are calculated exactly from rational half-tangents.

## ZH: 计数矛盾与严格端点
## EN: Counting contradiction and the strict endpoint

ZH: 节点参考捕获至少 tau，丢失质量至多 HA，因此每个实际 q 父方块捕获至少 chi=tau−HA。求和对象是实际父方块，而不是可能重叠的参考方块。精确有理数检查给出以下矛盾。
EN: The nodal reference captures at least tau and loses at most HA, so every actual side-q parent captures at least chi=tau−HA. The sum is over actual parents, not potentially overlapping references. Exact rational checks give the following contradiction.

```math
\chi\ge\frac{99979}{100000},\qquad
40\frac{99979}{100000}-\frac{3999}{100}=\frac1{625}>0.
```

ZH: 面积测度对方块边界赋零质量，故四十个内部不交的父方块总积分至多 M。矛盾排除了 K 内的 q 方块装填，也即排除了边长恰为 X 的单位方块装填。
EN: The area measure assigns zero mass to square boundaries, so forty interior-disjoint parents have total integral at most M. The contradiction excludes side-q packings in K, equivalently unit-square packings at side exactly X.

ZH: 7×7 网格提供有限可行上界。把边长、中心与方向限制在对应紧域，顶点包含条件闭；两方块内部不交可由有限个非严格分离轴不等式集合的并表达，也为闭条件。可行集紧，最小边长可达。因此端点排除确实给出 s(40)>X，而不仅是 s(40)≥X。
EN: A 7×7 grid gives a finite feasible upper bound. Restrict sides, centers and orientations to the corresponding compact domains. Vertex containment is closed, and interior disjointness is a finite union of non-strict separating-axis inequality sets, also closed. The feasible set is compact and the minimum side is attained. Endpoint exclusion thus gives s(40)>X, not merely s(40)≥X.
