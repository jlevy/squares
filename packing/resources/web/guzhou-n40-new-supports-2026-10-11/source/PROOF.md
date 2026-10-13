# ZH: 新矩形支撑给出的严格下界
# EN: A strict lower bound from new rectangle supports

ZH: 允许四十个单位正方形独立平移、任意旋转、内部两两不交及所有边界接触。作者侧计算机辅助结论为下式；本版本的完整执行记录另见 results/verification.json。
EN: Forty unit squares may translate independently, rotate arbitrarily, have pairwise disjoint interiors and make all boundary contacts. The author-side computer-assisted conclusion is the following; results/verification.json separately records execution of this version.

```math
s(40)>\frac{3359}{500}=6.718.
```

## ZH: 1. 精确测度与证明目标
## EN: 1. Exact measure and proof obligation

```math
L=\frac{67}{10},\quad K=[0,L]^2,\quad B=\frac{3350}{3359},\quad
M=\frac{3999}{100},\quad \tau=\frac{4999}{5000}.
```

ZH: certificate/certified_candidate.json 的 SHA-256 为 984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2。它包含 685 个不同的正权 D4 矩形轨道，522 个来自原 2526 个候选，163 个位于原候选池之外。每个坐标及权重都按精确有理数解释。
EN: certificate/certified_candidate.json has SHA-256 984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2. It contains 685 distinct positive-weight D4 rectangle orbits, 522 inherited from the original 2526 candidates and 163 outside that pool. Every coordinate and weight is interpreted as an exact rational.

ZH: 对矩形 R_j 和权重 w_j，在八个 D4 像上分别放置密度 w_j/(8 area(R_j))，保留对称重数并累加重叠密度。两种展开逐项核对全部 5480 项，以及容纳、非负性、轨道身份和权重和 M。得到有限、有界、非负、D4 不变的面积密度 g，定义绝对连续测度 μ。
EN: For rectangle R_j and weight w_j, put density w_j/(8 area(R_j)) on each of its eight D4 images, preserving multiplicity and adding overlapping densities. Two expansions reconcile all 5480 terms, containment, nonnegativity, orbit identity and total weight M. This gives a finite, bounded, nonnegative D4-invariant area density g and an absolutely continuous measure μ.

ZH: 证明义务是每个完全位于 K 内的边长 B 正方形 P 都有 μ(P)≥τ。原密度的旧权重、旧 B 和旧角网元数据均不充当新覆盖证据；两个计算输入从新有理证书重新生成，逐项核对向外或向内舍入方向及固定哈希。
EN: The obligation is μ(P)≥τ for every side-B square P fully contained in K. Old weights, B and angular metadata from the original density are not new coverage evidence. Both computational inputs are regenerated from the new rational certificate and checked for outward or inward rounding and fixed hashes.

## ZH: 2. 全部连续姿态域
## EN: 2. The complete continuous pose domain

ZH: D4 不变性允许把单个方块积分问题的方向折到 [0,π/4]；再用容器中心的四分之一转动把中心移到东北闭象限，保持无标号正方形方向模 π/2。固定方向的中心归约不能用任意反射代替。这些变换只证明单方块收费，不假定分别变换后的四十个方块仍组成装填。
EN: D4 invariance folds an individual square's integral problem to orientations [0,π/4]. Quarter-turns about the container center then move its center into the closed northeast quadrant while preserving square orientation modulo π/2. Arbitrary reflections cannot replace this fixed-orientation center reduction. These transformations prove individual capture, without claiming the separately transformed forty squares remain a packing.

```math
t=\tan(\theta/2),\quad c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
E(t)=\frac L2-\frac B2(c+s),\quad
(x,y)=\left(\frac L2+uE(t),\frac L2+vE(t)\right),\quad (u,v)\in[0,1]^2.
```

ZH: L>B√2 保证 E>0，以上参数覆盖整个合法中心象限，中心域随角度同步变化。整数端点 1,500,10000,20000,…,410000,415000 除以 10^6 定义 43 个相接闭角带，覆盖 [10^-6,83/200]；末端满足 t²+2t−1>0，故超过 tan(π/8)。近零区间在第 6 节单独补足。
EN: L>B√2 ensures E>0, and the parameters cover the entire legal center quadrant while varying with angle. Integer endpoints 1,500,10000,20000,…,410000,415000 divided by 10^6 define 43 adjoining closed slabs covering [10^-6,83/200]. The last endpoint satisfies t²+2t−1>0 and exceeds tan(π/8). Section 6 separately covers the near-zero interval.

ZH: 每个角带验证 [0,1]² 与完整角带的笛卡尔积，不是一个方向样本。根盒为 [0,1]³；二分的子盒闭并集等于父盒。启发式只选择切分方向，只有所有叶盒通过严格下界且队列耗尽才接受。超时、节点预算耗尽和微小未决盒均导致拒绝。
EN: Every slab verifies the Cartesian product of [0,1]² with the entire angular interval, not a sampled orientation. The root is [0,1]³, and closed child boxes cover their parent. Heuristics choose only the split direction. Acceptance requires every leaf to pass the rigorous lower bound and the queue to be exhausted. Timeout, exhausted node budgets and tiny unresolved boxes are refusals.

## ZH: 3. 区间算术与整盒分类
## EN: 3. Interval arithmetic and whole-box classification

ZH: 基本 binary64 运算最近舍入后向所需方向移动一个相邻数，乘法取四个端点积的极值，除法分母不得含零。零、无穷和 NaN 单独处理；非有限验证输出被拒绝。平台为 x86_64 Linux，检查最近舍入、断言及非 FTZ/DAZ；编译固定 -O3 -std=c++17 -fno-fast-math -ffp-contract=off。
EN: Basic binary64 operations use round-to-nearest followed by one outward neighboring number. Multiplication takes extrema of four endpoint products, and divisors must exclude zero. Zero, infinities and NaNs are handled separately; nonfinite verification output is refused. The platform is x86_64 Linux, checking nearest rounding, assertions and absence of FTZ/DAZ, with fixed -O3 -std=c++17 -fno-fast-math -ffp-contract=off.

ZH: 在 0<t≤1/2 上 c 递减、s 递增；W=c+s 在 √2−1 前增加、之后减少。代码使用端点和唯一临界点外包 W；可能含临界点时采用平方严格大于 2 的有理上界 1414213562373096/10^15。E、中点位置及位置误差都由该外包计算。
EN: On 0<t≤1/2, c decreases and s increases, while W=c+s increases before √2−1 and decreases afterward. Endpoint values and the sole critical point enclose W. If the interval may contain the critical point, the rational upper bound 1414213562373096/10^15, whose square exceeds 2, is used. E, midpoint positions and positional errors all use this enclosure.

ZH: 每个矩形通过容器轴投影及旋转方块法向的区间投影分类。只有在整个三维姿态盒中完全包含才加入常数质量，只有整个盒中均外离才删除。传给子盒的缓存保持有效，因为其参数集合是父盒的子集。10^-10 的预筛选仅决定是否尝试严格投影，不是接受条件。
EN: Rectangle classification uses interval projections on container axes and square normals. Full mass enters the constant term only for containment throughout the entire 3D pose box; deletion requires exclusion throughout. Cached conclusions remain valid in child parameter subsets. The 10^-10 prescreen decides only whether to attempt rigorous projection, not acceptance.

## ZH: 4. 凹截面的中心积分下界
## EN: 4. Center-integral lower bounds from concave sections

ZH: 固定真实角度，以可表示的浮点端点选择一个内矩形，使它在所有可能的盒中点平移下都位于源矩形的相对坐标范围内。令竖端点为 b₀,e₀，横坐标 ξ，h=B/2，则有符号竖截面为：
EN: At a fixed true angle, choose a rectangle with representable endpoints contained in the source rectangle's relative-coordinate range for all possible box-midpoint translations. For vertical endpoints b₀,e₀, abscissa ξ and h=B/2, the signed vertical section is:

```math
f(\xi)=\min\left(e_0,\frac{h-c\xi}{s},\frac{h+s\xi}{c}\right)-
\max\left(b_0,\frac{-h-c\xi}{s},\frac{-h+s\xi}{c}\right).
```

ZH: 仿射函数的下包络减上包络是凹函数，所以 f 的图像不低于端点连线。实际截长为 max(0,f)。用区间下端点代替两个端点值，所得梯形积分仍是下界；与零取最大后依然是下界，逐段相加即可。
EN: A lower envelope of affine functions minus an upper envelope is concave, so f lies above its endpoint chords. Actual section length is max(0,f). Replacing chord endpoints by interval lower bounds gives a lower trapezoidal integral; taking its maximum with zero preserves the lower bound, and segments may be summed.

ZH: 浮点启发式仅提出区间内有序积分结点，不要求结点恰为真实事件；漏事件、重复结点或负梯形只损失精度。整个 c,s 区间参与端点公式，保证下界对所有真实角度成立，不需要角导数或角度采样。相减后再除法的表达式保持数学语义并减小依赖损失。
EN: Floating heuristics merely propose ordered quadrature knots within the interval, without requiring exact geometric events. Missing events, duplicate knots or negative trapezoids only reduce sharpness. Endpoint formulas use the entire c,s intervals, giving a bound for every true angle without angular derivatives or sampling. Subtracting before division preserves semantics and reduces dependency loss.

## ZH: 5. 从中点积分覆盖整个中心盒
## EN: 5. Extending midpoint capture to the entire center box

ZH: 对每个固定真实角度，平移捕获函数 F 的 x 导数由密度乘以方块在矩形左边的竖截长减右边截长给出，y 类似。区间 min、max、正部和有理方向公式包住整个姿态盒的导数。密度有界，F 沿平移直线绝对连续，因此几乎处处的导数界足够。
EN: At each fixed true angle, the x derivative of translated capture F is the density times the difference between square-section lengths at the rectangle's left and right edges; y is analogous. Interval min, max, positive parts and rational direction formulas enclose derivatives over the pose box. Bounded density makes F absolutely continuous along translation lines, so almost-everywhere bounds suffice.

```math
F(x,y,\theta)\ge f_0-d_xG_x-d_yG_y.
```

ZH: f₀ 是适用于整段角度的中点积分下界，Gx,Gy 是整个姿态盒的导数绝对上界；dx,dy 包住真实中心与同一角度下盒中点的距离 du E(t)、dv E(t)。加回常数项后，只在向下舍入下界达到 τ 的向上表示时关闭盒。
EN: Here f₀ bounds midpoint capture throughout the angular interval, Gx,Gy bound absolute derivatives throughout the pose box, and dx,dy enclose distances du E(t),dv E(t) from the true center to the same-angle box midpoint. After restoring constant mass, a box closes only when its downward-rounded bound reaches an upward representation of τ.

ZH: 研究完整运行每次检查 60,500,889 个节点、30,250,466 个叶盒和 13,812,428 次角度二分，43 个角带均成功。最小返回下界为 9005397816695287/9007199254740992>τ。发布复验逐项绑定源码、输入、二进制、完整角带集合、原始输出和退出码，不信任孤立成功标志。
EN: Each complete research run checks 60,500,889 nodes, 30,250,466 leaves and 13,812,428 angle bisections, with all 43 slabs succeeding. The least returned bound is 9005397816695287/9007199254740992>τ. Publication replay binds source, input, binary, complete slab sets, raw output and exit codes individually rather than trusting an isolated success flag.

## ZH: 6. 完整近轴补丁
## EN: 6. The complete near-axis patch

```math
\epsilon=10^{-6},\quad A=\frac{249329659}{250000000},\quad
B-A\frac{1+2\epsilon-\epsilon^2}{1+\epsilon^2}
=\frac{424025836324581}{839750000000839750000000}>0.
```

ZH: 在 [0,ε] 上 c+s 递增，上式证明每个旋转 B 方块都包含一个同心水平 A 方块，它仍在 K 内。水平测度由支撑向内、密度向下取整到 10^-9 的整数数据给出，逐项检查其受原测度支配和四分之一转动对称。
EN: Since c+s increases on [0,ε], the inequality proves that every rotated side-B square contains a concentric horizontal side-A square, still inside K. Horizontal certification uses integer data with supports rounded inward and densities downward to 10^-9, checking term by term domination by the original measure and quarter-turn symmetry.

ZH: 所有支撑边平移 ±A/2 给出完整横纵断点；捕获量在每个乘积单元内双线性，最小值在顶点。整数 hinge 展开与二维前缀和枚举 3293²=10,843,849 个顶点，求得的极小点另以直接整数求和核对。输入推导的中间量绝对界保证无有符号 128 位溢出，评估上界为 627444222088298915573283512797161984<2^125。
EN: All support edges shifted by ±A/2 give the complete horizontal and vertical breakpoints. Capture is bilinear in each product cell and attains a minimum at a vertex. Integer hinge expansions and 2D prefix sums enumerate 3293²=10,843,849 vertices, with independent direct integer summation at the minimizer. Input-derived absolute bounds prevent signed-128-bit overflow; the evaluation bound is 627444222088298915573283512797161984<2^125.

```math
\mu(Q_A)\ge\frac{1001486431423867090847280653}{10^{27}}>\tau.
```

ZH: 几何包含和非负测度单调性把这个完整水平下界转移到整个 [0,ε]，补齐第 2–5 节的覆盖，不依赖插值。
EN: Geometric containment and monotonicity of the nonnegative measure transfer this complete horizontal bound to all of [0,ε], completing Sections 2–5 without interpolation.

## ZH: 7. 计数与严格端点
## EN: 7. Counting and the strict endpoint

ZH: 因此每个合法 B 方块均捕获至少 τ。面积测度对边界赋零质量，四十个内部不交方块的总捕获至多 M，但有以下精确矛盾：
EN: Every legal side-B square thus captures at least τ. Boundaries have zero area measure, so forty interior-disjoint squares capture total mass at most M, contradicting:

```math
40\tau-M=40\frac{4999}{5000}-\frac{3999}{100}=\frac1{500}>0.
```

ZH: 若单位方块装入边长恰为 X=L/B=3359/500 的容器，缩放 B 倍给出上述不可能装填，所以端点也被排除。有限网格给出可行上界；对应紧参数域中顶点容纳条件闭，内部不交由有限个连续非严格分离轴不等式集合的并表达，亦闭。最小边长可达，故得到严格 >，不只是 ≥。
EN: A unit-square packing at side exactly X=L/B=3359/500 scales by B into the impossible packing, excluding the endpoint. A finite grid gives a feasible upper bound. In the corresponding compact parameter domain, vertex containment is closed and interior disjointness is a finite union of continuous non-strict separating-axis inequality sets, also closed. The minimum is attained, giving strict > rather than only ≥.

ZH: 本证明不使用 Göbel 装填的刚性、接触图唯一性、搜索失败或未经验证的优化成功标志。全量复跑仍使用同一内核，不是另一套独立全局证明；有限对偶障碍的独立性仅属于 OBSTRUCTION.md 的不同结论。
EN: This proof uses no rigidity of Göbel's packing, contact-graph uniqueness, failed search or unverified optimizer success flag. Full replay still uses the same kernel, not another independent global proof. Independence of the finite dual obstruction applies only to the separate conclusion in OBSTRUCTION.md.
