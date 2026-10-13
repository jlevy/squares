# ZH: 全部连续姿态的密度下界证明
# EN: A density lower bound over all continuous poses

ZH: 日期：2026-10-10。命题允许四十个单位正方形独立平移、任意旋转、边界接触，内部两两不交。
EN: Date: 2026-10-10. The statement permits independent translations, arbitrary rotations and boundary contacts of forty unit squares with pairwise disjoint interiors.

```math
s(40)>\frac{1340000}{199529}=6.715815746082023\ldots
```

ZH: 验证级别为作者侧 CERTIFIED：下述归约、整个有限分支运算、精确输入和计数均已完成。新连续角度内核尚无外部独立复验或形式化证明；既有 6.70854 的外部审查不覆盖本命题。
EN: The status is author-side CERTIFIED: the reduction, entire finite branch computation, exact input and counting have completed. The new continuous-angle kernel has no external independent replay or formal proof; external review of the earlier 6.70854 bound does not cover this claim.

## ZH: 1. 冻结测度与精确命题
## EN: 1. Frozen measure and exact proposition

```math
L=\frac{67}{10},\quad K=[0,L]^2,\quad B=\frac{199529}{200000},\quad M=\frac{3999}{100},\quad \tau=\frac{4999}{5000}.
```

ZH: 测度仍是 wand125 的 rect_n40_L67；未移动支撑，也未重新优化权重。每个正权代表矩形 R 的权重 w 在八个 D4 像上产生密度 w/(8 area(R))，保留对称重数，重叠密度相加。
EN: The measure remains wand125’s rect_n40_L67: supports are not moved and weights are not reoptimized. A positive rectangle R of weight w contributes density w/(8 area(R)) on each of its eight D4 images, retaining symmetric multiplicities and adding overlapping densities.

ZH: 480 个正权代表给出 3840 项非负矩形密度。源文件中的有限十进制与分数字符串均按精确有理数读取；独立的两种 D4 展开逐项核对支撑、重数和质量，得到绝对连续测度 μ(K)=M。
EN: The 480 positive representatives give 3840 nonnegative rectangle-density terms. Finite decimals and fractional strings in the source are read as exact rationals; two independently implemented D4 expansions reconcile supports, multiplicities and mass term by term, giving an absolutely continuous measure with μ(K)=M.

ZH: 需要证明的覆盖命题不是一组采样：每个完全包含于 K 的 B 正方形，无论中心或方向，均满足 μ(P)≥τ。源文件内旧 B 和旧角网元数据不充当新覆盖证据。
EN: The coverage proposition is not a sampling statement: every side-B square fully contained in K, at every center and orientation, satisfies μ(P)≥τ. Old B and angular-net metadata in the source do not count as evidence of new coverage.

ZH: 冻结密度 SHA-256 为 71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0；verifier/exact.py 从原始 JSON 自动重建姿态输入和轴向整数输入，核对每个支撑、密度、重数与舍入方向。两份输入的 SHA-256 与研究冻结输入相同；历史状态字段不参与验收。
EN: The frozen-density SHA-256 is 71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0. verifier/exact.py regenerates the pose and integer-axis inputs from the source JSON, checking each support, density, multiplicity and rounding direction. Both input SHA-256 values match the frozen research inputs; historical status fields do not determine acceptance.

## ZH: 2. 对称性与连续参数域
## EN: 2. Symmetry and the continuous parameter domain

ZH: 对每个单独的积分问题，D4 不变性和正方形方向模 π/2 可把方向折到 [0,π/4]。随后以容器中心的四分之一转动把中心移到东北闭象限，仍保持同一无标号方块方向。固定方向的中心归约不能以任意反射作理由。
EN: For each individual integral problem, D4 invariance and square orientation modulo π/2 fold the direction into [0,π/4]. A subsequent quarter-turn about the container center places the center in the closed northeast quadrant while preserving the unlabeled square’s orientation. Arbitrary reflections cannot justify the fixed-orientation center reduction.

ZH: 这些变换只用于证明逐方块收费下界；不声称分别变换后的四十个方块仍组成装填。最终求和始终针对原始的内部不交方块。
EN: These transformations prove the per-square charge bound only; the individually transformed forty squares are not claimed to remain a packing. The final sum always concerns the original interior-disjoint squares.

```math
t=\tan(\theta/2),\quad c(t)=\frac{1-t^2}{1+t^2},\quad s(t)=\frac{2t}{1+t^2},\quad W(t)=c(t)+s(t).
```

```math
E(t)=\frac L2-\frac B2W(t),\qquad x=\frac L2+uE(t),\quad y=\frac L2+vE(t),\qquad (u,v)\in[0,1]^2.
```

ZH: E(t)>0，因为 L>B√2。每个合法中心在四分之一归约后都由上述参数给出。验证盒包含 u、v 和 t 三个维度；改变角度时中心域随 E(t) 同步变化，而不是继续使用某一个节点的中心范围。
EN: E(t)>0 because L>B√2. Every legal center after quadrant reduction has this parameterization. Verification boxes have three dimensions, u, v and t; the center domain changes with E(t) as the angle varies instead of retaining one node’s center range.

## ZH: 3. 角度全覆盖的划分
## EN: 3. Decomposition covering every angle

```math
\epsilon=10^{-6},\qquad T=83/200,\qquad T^2+2T-1>0.
```

ZH: 最后的不等式精确保证 T>√2−1=tan(π/8)，因此覆盖到 T 足以覆盖 π/4。区间 [ε,T] 被下列整数端点除以 10^6 后划成 43 个连续闭角带；相邻角带端点相接。
EN: The final exact inequality gives T>√2−1=tan(π/8), so coverage through T reaches π/4. Dividing the following integer endpoints by 10^6 partitions [ε,T] into 43 closed angular slabs with matching adjacent endpoints.

```text
1, 500, 10000, 20000, ..., 410000, 415000
```

ZH: 每个角带的整个 [0,1]² 中心参数域与该角带的乘积都已完成分支定界。[0,ε] 不通过插值推断，而由第 8 节的完整轴向证书和几何包含补足。
EN: The product of every slab with the entire normalized center domain [0,1]² has completed branch and bound. The interval [0,ε] is not inferred by interpolation; Section 8 supplies it using complete axial certification and geometric containment.

## ZH: 4. 算术与方向范围不变量
## EN: 4. Arithmetic and direction-range invariants

ZH: 所有基本区间加减乘除先按 IEEE binary64 的最近舍入求值，再向所需方向移动一个相邻浮点数。乘法取四个端点积的极值；除法仅用于不含零的分母。输入十进制和十六进制浮点串经逐项精确审计，确实向外包住源有理数。
EN: Each basic interval addition, subtraction, multiplication or division first uses IEEE binary64 round-to-nearest, then moves one representable neighbor outward. Multiplication takes extrema of four endpoint products; division uses denominators excluding zero. Exact row-wise auditing verifies that decimal and hexadecimal input float strings enclose the source rationals outward.

ZH: 位步进依赖 IEEE 有符号编码顺序，单独处理零、无穷和 NaN；近邻方向由符号确定。正式平台为 x86_64 Linux，断言、最近舍入及非 FTZ/DAZ 模式均检查；编译禁止 fast-math、FMA contraction 和 NDEBUG。有限输出检查拒绝非有限值。
EN: Bit stepping uses the sign-ordered IEEE encoding, handles zero, infinity and NaN separately, and chooses the neighbor direction by sign. The certified platform is x86_64 Linux; assertions, round-to-nearest and absence of FTZ/DAZ are checked. Builds forbid fast-math, FMA contraction and NDEBUG. Nonfinite verification outputs are refused.

ZH: 在 0<t≤1/2 上，c 递减而 s 递增，用角带端点的有理表达式外包范围。W(t) 在 √2−1 前增加、之后减少，因此直接用 W 的端点及唯一临界点包围旋转宽度，避免独立 c 与 s 区间相加造成过宽。
EN: On 0<t≤1/2, c decreases and s increases, so rational expressions at slab endpoints enclose their ranges. W(t) increases before √2−1 and decreases afterward. Its endpoint values and sole critical point therefore enclose rotational extent directly, avoiding the excess width from independently summing c and s intervals.

ZH: 若区间可能包含临界点，采用有理上界 1414213562373096/10^15，其平方严格大于 2；临界点是否可能在区间内由向外区间比较判断。E(t)、中点位置和位置半宽全部使用这个有效 W 外包。
EN: If the interval may contain the critical point, the upper bound 1414213562373096/10^15 is used; its square is strictly above 2. Outward interval comparisons decide whether the critical point may occur. E(t), midpoint locations and positional half-widths all use this valid W enclosure.

## ZH: 5. 整盒内外分类与缓存
## EN: 5. Whole-box containment, exclusion and caching

ZH: 每个矩形项先通过容器轴投影，必要时再通过旋转方块两条法向的区间投影分类。只有在整个三维姿态盒中都完全包含，才把其完整质量下界移入常数项；只有整个盒都外离，才丢弃为零。接触边界的零面积不影响分类。
EN: Each rectangle is classified first by container-axis projections, then when needed by interval projections on the square’s two normals. Its full mass lower bound enters the constant term only if containment holds for the whole three-dimensional pose box; it is dropped as zero only if exclusion holds throughout. Area-zero boundary contacts do not affect these classifications.

ZH: 代码中的 10^-10 比较只筛选值得进行区间证明的候选，绝不作为接受或排除判据。常数项与活动矩形传给子盒后仍有效，因为子盒的参数集合包含于父盒；这给出缓存的归纳不变量。
EN: The code’s 10^-10 comparisons merely screen candidates worth attempting with interval proofs; they never decide acceptance or exclusion. Constants and active rectangles remain valid in child boxes because their parameter sets lie within the parent, giving the cache induction invariant.

## ZH: 6. 凹截面给出的中心积分下界
## EN: 6. A center-integral lower bound from concave sections

ZH: 固定真实角度，对某个矩形项，先选择一个浮点端点组成的内矩形，使它在全部可能中点平移下仍包含于该源矩形的相对坐标表示。令其竖向端点为 b₀,e₀，横坐标为 ξ，h=B/2。
EN: At a fixed true angle, choose a rectangle with representable endpoints lying inside the source rectangle in relative coordinates for every possible midpoint translation. Write its vertical endpoints as b₀,e₀, its horizontal coordinate as ξ, and h=B/2.

```math
f(\xi)=\min\left(e_0,\frac{h-c\xi}{s},\frac{h+s\xi}{c}\right)-\max\left(b_0,\frac{-h-c\xi}{s},\frac{-h+s\xi}{c}\right).
```

ZH: f 是仿射函数下包络减去上包络，因此为凹函数。实际截长为 max(0,f)。任意两个横坐标之间的 f 图像不低于端点连线；使用向外区间算出的端点下界，其连线仍在真实图像之下。
EN: f is a lower envelope of affine functions minus an upper envelope, hence concave. The actual section length is max(0,f). Between any two abscissae, f lies above the line through its endpoint values; replacing those endpoints by interval-certified lower bounds leaves the line below the true graph.

ZH: 因此每个小段的积分至少为 max(0,梯形积分下界)，相加后仍是该项交面积的下界。中间结点由浮点启发式提出，但仅其排序和区间内位置参与定义；不要求它们是真实几何事件。即使漏掉事件、提出重复结点或某段给出负值，也只损失精度，不产生高估。
EN: The integral on each small segment is at least max(0, the lower trapezoidal integral), and summing remains a lower bound on intersection area. Floating heuristics propose intermediate knots, but only their sorted positions inside the interval matter; they need not be actual geometric events. Missing events, duplicate knots or negative segment values lose sharpness, not soundness.

ZH: 角度仍在区间中变化时，截面端点公式被整个 c,s 区间外包。这证明下界对所有角度都成立，无需对角度采样，也不需要角导数。相关分子先相减再除以 s 或 c，保持同一数学表达式而显著减小近零方向的区间损失。
EN: When the angle varies over an interval, the endpoint section formulas are enclosed over the entire c,s ranges. The bound therefore holds at every angle, without angular sampling or an angle derivative. Subtracting correlated numerators before division by s or c preserves the expression while greatly reducing interval loss near zero.

## ZH: 7. 从中心积分到整个中心盒
## EN: 7. From the center integral to the entire center box

ZH: 记活动矩形的捕获量为 F(x,y,θ)。关于 x 的导数为各矩形密度乘以方块在矩形左边的竖截长减去右边竖截长之和；y 方向同理。矩形截长用同一正部、min/max 和有理方向表达式向外包住整个姿态盒。
EN: Let F(x,y,θ) be capture from active rectangles. Its x derivative is the sum of each density times the square’s vertical section at the rectangle’s left edge minus that at its right edge; the y derivative is analogous. Positive parts, min/max and rational direction expressions enclose these section lengths across the whole pose box.

ZH: 有界面积密度使捕获量沿平移直线绝对连续，故几乎处处的导数界足以积分。对每个固定 θ，真实中心距离该 θ 对应盒中点的横纵差分别不超过 du E(θ)、dv E(θ)。
EN: Bounded area density makes capture absolutely continuous along translation lines, so almost-everywhere derivative bounds suffice for integration. At every fixed θ, horizontal and vertical distances to that θ’s box midpoint are at most du E(θ) and dv E(θ).

```math
F(x,y,\theta)\ge f_0-d_xG_x-d_yG_y.
```

ZH: 其中 f₀ 为第 6 节的全角度中心积分下界，Gx,Gy 为整个盒中的导数绝对值上界，dx,dy 为位置差上界。将缓存常数质量加回后，只有向下舍入的总下界达到 τ 的向上表示，才能关闭一个盒。
EN: Here f₀ is the all-angle center-integral lower bound from Section 6, Gx,Gy bound derivative magnitudes throughout the box, and dx,dy bound positional differences. After adding cached constant mass, a box closes only when its downward-rounded bound reaches an upward representation of τ.

ZH: 未关闭的盒只沿一个归一化坐标二分；两子盒闭并集恰为父盒。分割选择属于启发式，不参与接受。坐标在停止阈值前均为可精确表示的二进有理数，最小半宽低于 2^-40 或资源预算耗尽均非零退出，不是接受。
EN: An unclosed box bisects one normalized coordinate; the closed children cover exactly the parent. Choosing the split is heuristic and does not decide acceptance. Coordinates remain exactly representable dyadics before the stopping threshold. A half-width below 2^-40 or exhausted resource budget causes nonzero exit, not acceptance.

ZH: 每个根盒从 [0,1]³ 开始；只有队列耗尽才记录 verified。43 次执行全部退出 0，累计 61,860,927 个节点、30,930,485 个叶盒，其中 14,096,668 次角度二分。每角带均核对 nodes=2 leaves−1、参数、输入/源码/程序身份及原始输出。
EN: Every root starts at [0,1]³, and verified is emitted only on queue exhaustion. All 43 executions exited 0, totaling 61,860,927 nodes and 30,930,485 leaves, with 14,096,668 angle bisections. Every slab checks nodes=2 leaves−1, parameters, input/source/binary identities and raw output.

## ZH: 8. 近水平域的精确补丁
## EN: 8. The exact near-axis patch

```math
A=\frac{997643}{1000000},\qquad 0\le t\le\epsilon=10^{-6}.
```

ZH: 对水平 A 正方形，支撑端点向内取整到 10^-9 网格，密度向下取整到 10^-9；得到逐点不大于原密度的非负测度。独立核查了全部整数行、向内/向下方向和四分之一转动对称。
EN: For horizontal side-A squares, supports are rounded inward to a 10^-9 grid and densities downward to 10^-9, yielding a nonnegative measure pointwise dominated by the original. Every integer row, rounding direction and quarter-turn symmetry is independently checked.

ZH: 捕获量在支撑端点平移 ±A/2 得到的全部横纵断点之间双线性，因此每个单元的最小值在顶点。整数 hinge 展开和二维前缀和枚举全部 2213²=4,897,369 个断点对，并在最小值位置直接求和核对。
EN: Capture is bilinear between all horizontal and vertical breakpoints obtained by shifting support endpoints by ±A/2, so every cell minimum is at a vertex. Integer hinge expansions and two-dimensional prefix sums enumerate all 2213²=4,897,369 breakpoint pairs, with a direct-sum check at the minimizer.

ZH: 所有有符号 128 位累加量和求值都受输入计算出的绝对值上界控制，最大评估上界为 384178892657373682994447839008000000，严格小于 2^125；阈值比较先计算所需整数质量，避免乘法溢出。
EN: Input-derived absolute bounds control every signed-128-bit accumulation and evaluation. The evaluation bound is 384178892657373682994447839008000000, strictly below 2^125. Threshold comparisons first compute the required integer mass to avoid overflow.

```math
\mu(Q_A)\ge\frac{249950896232809301864786207}{250000000000000000000000000}=0.999803584931237207459144828>\tau.
```

ZH: 在这个近零区间中 W(t) 递增，且下列包含余量严格为正。故每个旋转 B 正方形都包含一个同心水平 A 正方形；它也在 K 内，非负测度的单调性给出所需收费。
EN: W(t) increases on this near-zero interval, and the following containment margin is strictly positive. Every rotated side-B square therefore contains a concentric horizontal side-A square, itself in K; monotonicity of the nonnegative measure supplies the required capture.

```math
B-AW(\epsilon)=\frac{589499411}{125000000000125000}>0.
```

## ZH: 9. 精确计数与严格端点
## EN: 9. Exact counting and the strict endpoint

ZH: 第 3–8 节证明整个合法 B 姿态域的统一收费至少 τ。四十个内部不交的 B 正方形，其边界面积为零，故捕获总质量至多 M；但下面给出严格相反的不等式。
EN: Sections 3–8 prove uniform capture at least τ across the entire legal side-B pose domain. Forty interior-disjoint side-B squares have area-zero boundaries and hence total capture at most M, contradicting the following strict inequality.

```math
40\tau-M=40\frac{4999}{5000}-\frac{3999}{100}=\frac1{500}>0.
```

ZH: 若单位正方形能装入边长 X=L/B 的容器，整体缩放 B 倍将得到 K 中的四十个 B 正方形，矛盾。因此边长恰为 X 也被排除。
EN: If unit squares packed into a container of side X=L/B, scaling the whole packing by B would give forty side-B squares in K, a contradiction. The endpoint X itself is therefore excluded.

ZH: 7×7 网格给出有限可行上界。把中心、方向、容器边长限制在相应紧域后，包含条件闭；内部不交由有限个连续非严格分离轴不等式集合的并表达，同样闭。因此可行集紧，最小边长可达，端点排除给出严格 s(40)>X。
EN: A 7×7 grid gives a finite feasible upper bound. Restrict centers, orientations and container side to the corresponding compact domains. Containment is closed, and interior disjointness is a finite union of continuous non-strict separating-axis inequality sets, also closed. The feasible set is compact and the minimum is attained, so endpoint exclusion gives strict s(40)>X.

## ZH: 10. 信任边界与复验状态
## EN: 10. Trust boundary and reproduction status

ZH: 连续姿态覆盖由新 C++ 内核完成；平移导数来自 Tokoharu，凹截面下界受到 Squares Project Rust 实现启发，轴向采用本项目的独立整数算法。它不是全新独立来源的第二套完整验证器。
EN: Continuous-pose coverage uses the new C++ kernel. Translation derivatives derive from Tokoharu, concave-section bounds are informed by the Squares Project Rust implementation, and the axis uses this project’s independently implemented integer algorithm. It is not a wholly independently sourced second complete verifier.

ZH: 在最终 B 上另有 160 组有限精确多边形对照，涉及 4014 个姿态与 3568 项面积比较；另有 1,000,008 个 IEEE 输入的双向近邻对照、合成正反控制，以及包含 29 个错误收据变体的 7 组输入与验收测试。它们检测实现错误，但不替代上文的连续归约和整个队列的实际穷尽。
EN: At the final B, 160 finite exact-polygon cases compare 4014 poses and 3568 areas, alongside two-neighbor comparisons at 1,000,008 IEEE inputs, synthetic positive/negative controls, and seven input/admission test groups including 29 invalid receipt variants. These detect implementation errors but do not replace the continuous reduction or actual exhaustion of every queue.

ZH: 哈希只绑定内容身份，不构成数学证明。可信基础仍包括明确的几何引理、区间内核、C++/Python 运行时、编译器和 IEEE 硬件语义。verifier/audit.py --check 核对内容与已有收据，不重新执行三维覆盖；verifier/run.py 在全新外部目录重新编译、测试并执行轴向与全部角带。
EN: Hashes bind content identity; they are not mathematical proofs. The trust base remains the stated geometric lemmas, interval kernel, C++/Python runtimes, compiler and IEEE hardware semantics. verifier/audit.py --check audits contents and existing receipts without rerunning 3D coverage; verifier/run.py freshly compiles, tests and executes the axis and every slab in a new external directory.
