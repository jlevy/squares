# ZH: 全部原始候选支撑在 6.72 的障碍
# EN: Obstruction at 6.72 for all original candidate supports

## ZH: 范围
## EN: Scope

ZH: 令 K=[0,67/10]²，对 certificate/original_density.json 的全部 2526 个矩形取 D4 对称的单位总质量均匀面积测度 σ_j，包括原来零权的 2046 项。任意非负组合 μ=Σw_jσ_j 都不能在 X≥168/25=6.72 形成统一逐方块收费的严格预算矛盾。
EN: On K=[0,67/10]², take the unit-total-mass D4-symmetrized uniform area measure σ_j for every one of the 2526 rectangles in certificate/original_density.json, including the 2046 originally zero-weight candidates. No nonnegative combination μ=Σw_jσ_j gives a strict uniform per-square charging contradiction at X≥168/25=6.72.

ZH: 这不是 s(40) 的上界或四十方块装填见证。新的矩形几何、非均匀密度、混合资源以及异质收费的占用规则均不在排除范围内。特别地，本结果不否定本版包含新增支撑的正下界。
EN: This is not an upper bound for s(40) or a witness packing of forty squares. New rectangle geometry, nonuniform density, mixed resources and occupancy rules for heterogeneous charging are outside the exclusion. In particular, it does not contradict this version's positive bound using new supports.

## ZH: 有限精确对偶
## EN: The finite exact dual

ZH: obstruction/certificate.json 给出 388 个合法有理姿态和正整数 m_i。取 B=335/336、t=tan(θ/2)，由 u,v∈[0,1] 及 E=L/2−B(c+s)/2 重建中心 (L/2+uE,L/2+vE)。检查器重新计算半正切方向和容纳。这些方块不需要相互不交，它们只用来抽取一个低收费姿态。
EN: obstruction/certificate.json gives 388 legal rational poses and positive integers m_i. With B=335/336 and t=tan(θ/2), u,v∈[0,1] and E=L/2−B(c+s)/2 reconstruct center (L/2+uE,L/2+vE). The checkers recompute half-tangent directions and containment. These squares need not be mutually disjoint; they select a low-capture pose only.

ZH: U=Σm_i=1000000000003。对全部 388×2526=980088 个系数 a_ij=σ_j(P_i)，精确计算交多边形面积，向上取整至 10^-12 后计算加权列和。最大列是原始索引 201，两套实现均给出：
EN: U=Σm_i=1000000000003. Every one of the 388×2526=980088 coefficients a_ij=σ_j(P_i) is computed by exact polygon intersection, rounded upward to 10^-12 and included in its weighted column sum. The maximizing column is original index 201; both implementations give:

```math
\sum_i\frac{m_i}{U}a_{ij}\le C=
\frac{24998348431654956215746}{1000000000003000000000000}<\frac1{40}.
```

ZH: 分母减去四十倍分子为 66062736801751370160>0，严格性只用整数比较。任取总质量 W=Σw_j>0，加权平均捕获至多 CW，故至少一个姿态收费不超过 CW<W/40，不可能同时有统一收费至少 τ 和 40τ>W。W=0 也显然无严格矛盾。
EN: The denominator minus forty times the numerator is 66062736801751370160>0, establishing strictness by integer comparison alone. For any total mass W=Σw_j>0, weighted average capture is at most CW, so some pose captures at most CW<W/40. Uniform capture at least τ cannot coexist with 40τ>W. W=0 plainly gives no strict contradiction either.

ZH: 更大 X 对应更小的边长 L/X。把每个测试方块同心缩小，仍合法，且非负密度捕获不增加。因此同一障碍适用于所有 X≥6.72。
EN: A larger X gives a smaller square side L/X. Concentric shrinking preserves legality and cannot increase capture under a nonnegative density. The same obstruction therefore extends to all X≥6.72.

## ZH: 实现与复验
## EN: Implementations and reproduction

ZH: obstruction/check.cpp 使用 Boost 任意精度有理数、反射后转动的 D4 展开及相对坐标裁剪。obstruction/check.py 使用 Python Fraction、交换及符号变换的展开和另一份半平面裁剪。两者均完整枚举全部系数并一致得到最大列、分子、分母和严格余量。
EN: obstruction/check.cpp uses Boost arbitrary-precision rationals, reflection-then-rotation D4 expansion and relative-coordinate clipping. obstruction/check.py uses Python Fraction, swaps/sign changes and a separate half-plane clipper. Both exhaust every coefficient and agree on maximizing column, numerator, denominator and strict slack.

ZH: 两种实现共享证书、原支撑和多边形面积的数学定义。LP 只产生对偶候选，不是证明。obstruction/run.py 从精确证书和源文件重新生成输入，运行两套程序及单姿态伪对偶反向测试；结果写入 results/obstruction.json。独立性仅属于本有限负结果，不推广至正下界的连续几何。
EN: The implementations share the certificate, original supports and mathematical definition of polygon area. An LP only proposes a dual candidate, not a proof. obstruction/run.py regenerates input from the exact certificate and source, runs both programs and a false one-pose dual control, and records results in results/obstruction.json. Independence belongs only to this finite negative result, not the continuous geometry of the positive bound.
