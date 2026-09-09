                                                           Do Differentiable Simulators Give Better Policy Gradients?


                                                                    H.J. Terry Suh 1 Max Simchowitz 1 Kaiqing Zhang 1 Russ Tedrake 1


                                                                    Abstract
                                                Differentiable simulators promise faster computa-
arXiv:2202.00817v2 [cs.LG] 22 Aug 2022




                                                tion time for reinforcement learning by replacing
                                                zeroth-order gradient estimates of a stochastic
                                                objective with an estimate based on first-order
                                                gradients. However, it is yet unclear what fac-
                                                tors decide the performance of the two estimators
                                                on complex landscapes that involve long-horizon
                                                planning and control on physical systems, despite
                                                the crucial relevance of this question for the util-
                                                ity of differentiable simulators. We show that
                                                characteristics of certain physical systems, such         Figure 1. Examples of simple optimization problems on physical
                                                                                                          systems. Goal is to: A. maximize y position of the ball after
                                                as stiffness or discontinuities, may compromise
                                                                                                          dropping. B. maximize distance thrown, with a wall that results
                                                the efficacy of the first-order estimator, and ana-       in inelastic impact. C. maximize transferred angular momentum
                                                lyze this phenomenon through the lens of bias and         to the pivoting bar through collision. Second row: the original
                                                variance. We additionally propose an α-order gra-         objective and the stochastic objective after randomized smoothing.
                                                dient estimator, with α ∈ [0, 1], which correctly
                                                utilizes exact gradients to combine the efficiency        the question: given access to exact gradients of f , which
                                                of first-order estimates with the robustness of zero-     estimator should we prefer?
                                                order methods. We demonstrate the pitfalls of
                                                traditional estimators and the advantages of the          In stochastic optimization, the theoretical benefits of using
                                                α-order estimator on some numerical examples.             first-order estimates of ∇F over zeroth-order ones have
                                                                                                          mainly been understood through the lens of variance and
                                                                                                          convergence rates (Ghadimi & Lan, 2013; Mahamed et al.,
                                                                                                          2020): the first-order estimator often (not always) results
                                                                                                          in much less variance compared to the zeroth-order one,
                                         1. Introduction                                                  which leads to faster convergence rates to a local minima of
                                         Consider the problem of minimizing a stochastic objective,       general nonconvex smooth objective functions.
                                                                                                          However, the landscape of RL objectives that involve long-
                                                          min F (θ) = min Ew f (θ, w).                    horizon sequential decision making (e.g. policy optimiza-
                                                           θ              θ
                                                                                                          tion) is challenging to analyze, and convergence proper-
                                         At the heart of many algorithms for reinforcement learning       ties in these landscapes are relatively poorly understood,
                                         (RL) lies zeroth-order estimation of the gradient ∇F (Sut-       except for structured settings such as finite-state MDPs
                                         ton et al., 2000; Schulman et al., 2017). Yet, in domains that   (Agarwal et al., 2020; Zhang et al., 2020) or linear control
                                         deal with structured systems, such as linear control, phys-      (Fazel et al., 2019; Bhandari & Russo, 2020). In particu-
                                         ical simulation, or robotics, it is possible to obtain exact     lar, physical systems with contact, as we show in Figure 1,
                                         gradients of f , which can also be used to construct a first-    can display complex characteristics including nonlineari-
                                         order estimate of ∇F . The availability of both options begs     ties, non-smoothness, and discontinuities (van der Schaft &
                                            1                                                             Schumacher, 2000; Mason, 2001; Suh et al., 2021).
                                             Department of Electrical Engineering and Computer Science,
                                         Massachusetts Institute of Technology, Cambridge, USA. Corre-    Nevertheless, lessons from convergence rate analysis tell
                                         spondence to: H.J.Terry Suh <hjsuh@mit.edu>.                     us that there may be benefits to using the exact gradients
                                         Proceedings of the 39 th International Conference on Machine     even for these complex physical systems. Such ideas have
                                         Learning, Baltimore, Maryland, USA, PMLR 162, 2022. Copy-        been championed through the term “differentiable simula-
                                         right 2022 by the author(s).                                     tion”, where forward simulation of physics is programmed
                                  Do Differentiable Simulators Give Better Policy Gradients?

in a manner that is consistent with automatic differentia-        nearly/strictly discontinuous in the underlying landscape.
tion (Freeman et al., 2021; Hu et al., 2020; Tedrake, 2022;       These discontinuities are commonly caused by contact and
Werling et al., 2021; Geilinger et al., 2020; Howell et al.,      geometrical constraints. We provide minimal examples to
2022), or computation of analytic derivatives (Carpentier         highlight specific challenges in Figure 1. These are not mere
et al., 2019). These methods have shown promising results         pathologies, but abstractions of more complicated examples
in decreasing computation time compared to zeroth-order           that are rich with contact, such as robotic manipulation.
methods (Huang et al., 2021; Freeman et al., 2021; Gradu
                                                                  We show that the presence of such discontinuities causes the
et al., 2021; Du et al., 2020; de Avila Belbute-Peres et al.,
                                                                  first-order gradient estimator to be biased, while the zeroth-
2018; Mora et al., 2021).
                                                                  order one still remains unbiased under discontinuities. Fur-
Existing literature in differentiable simulation mainly fo-       thermore, we show that stiff continuous approximations of
cuses on the use of exact gradients for deterministic op-         discontinuities, even if asymptotically unbiased, can still
timization. However, (Suh et al., 2021; Le Lidec et al.,          suffer from what we call empirical bias under finite-sample
2021) show that using exact gradients for a deterministic         settings. This results in a bias-variance tradeoff between the
objective can lead to suboptimal behavior of certain sys-         biased first-order estimator and the often high-variance, yet
tems due to their landscapes. In these systems, stochasticity     unbiased zeroth-order estimator. Intriguingly, we find that
can be used to regularize the landscapes with randomized          the bias-variance tradeoff in this setting manifests itself not
smoothing (Duchi et al., 2015). We illustrate how the land-       through convergence rates, but through different local min-
scapes change upon injecting noise (Figure 1), and list some      ima. This shows that the two estimators may fundamentally
benefits of considering a surrogate stochastic objective.         operate on different landscapes implicitly.
                                                                  The presence of discontinuities need not indicate that we
   • Stochasticity smooths local minima. As noted in              need to commit ourselves to uniformly using one of the
     (Suh et al., 2021; Metz et al., 2021), stochasticity can     estimators. Many physical systems are hybrid by nature
     alleviate some of the high-frequency local minima that       (van der Schaft & Schumacher, 2000); they consist of
     deterministic gradients will be stuck on. For instance,      smooth regions that are separated by manifolds of non-
     the small discontinuity on the right side of Figure 1.B      smoothness or discontinuities. This suggests that we may be
     is filtered by Gaussian smoothing.                           able to utilize the first-order estimates far away from these
   • Stochasticity alleviates flat regions. In systems of         manifolds to obtain benefits of convergence rates, while
     Figure 1, the gradients in some of the regions can be        switching to zeroth-order ones in the vicinity of discontinu-
     completely flat. This stalls progress of gradient descent.   ities to obtain unbiased estimates.
     The stochastic objective, however, still has non-zero
                                                                  For this purpose, we further attempt to answer the question:
     gradient as some samples escape the flat regions and
                                                                  how can we then correctly utilize exact gradients of f for
     provide an informative direction of improvement.
                                                                  variance reduction when we know the objective is nearly
   • Stochasticity encodes robustness. In Figure 1.C, fol-        discontinuous? Previous works show that the two estima-
     lowing the gradient to increase the transferred momen-       tors can be combined by interpolating based on empirical
     tum causes the ball to miss the pivot and land in a          variance (Parmas et al., 2018; Metz et al., 2019; Mahamed
     high-cost region. In contrast, the stochastic objective      et al., 2020). However, we show that in the presence of near-
     has a local minimum within the safe region, as the           discontinuities, selecting based on empirical variance alone
     samples provide information about missing the pivot.         can lead to highly inaccurate estimates of ∇F , and propose
                                                                  a robustness constraint on the accuracy of the interpolated
Thus, our work attempts to compare two versions of gradient       estimate to remedy this effect.
estimators in the stochastic setting: the first-order estimator
and the zeroth-order one. This setting rules out the case         Contributions. We 1) shed light on some of the inherent
that zeroth-order estimates perform better simply because         problems of RL using differentiable simulators, and answer
of stochasticity, and sets equal footing for the two methods.     which gradient estimator can be more useful under different
                                                                  characteristics of underlying systems such as discontinu-
When f is continuous, these quantities both converge to           ities, stiffness, and chaos; and 2) present the α-order gra-
the same quantity (∇F ) in expectation. We first show that        dient estimator, a robust interpolation strategy between the
even with continuous f , the first-order gradient estimate can    two gradient estimators that utilizes exact gradients without
result in more variance than the zeroth-order one due to the      falling into the identified pitfalls of the previous methods.
stiffness of dynamics or due to compounding of gradients in
chaotic systems (Parmas et al., 2018; Metz et al., 2021).         We hope both contributions inspire algorithms for policy op-
                                                                  timization using differentiable simulators, as well as design
In addition, we show that the assumption of continuous f          guidelines for new and existing simulators.
can be violated in many relevant physical systems that are
                                         Do Differentiable Simulators Give Better Policy Gradients?

2. Preliminaries                                                        if there exist constants a, b such that, for all z ∈ Rd1 ,
                                                                        kψ(z)k ≤ a(1 + kzkb ). The following assumption ensures
Notation. We denote the expectation of a random vector
                                                                        these gradients are well-defined.
z as E[z], and its variance as Var[z] := E[kz − E[z]k2 ].
Expectations are defined in almost-sure sense, so that the              Assumption 2.2. We assume that the policy π is contin-
law of large numbers holds (see Appendix A.1 for details).              uously differentiable everywhere, and the dynamics φ, as
                                                                        well as the cost ch have polynomial growth.
Setting.      We study a discrete-time, finite-horizon,
continuous-state control problem with states x ∈ Rn , inputs            Even when the costs or dynamics are not differentiable, the
u ∈ Rm , transition function φ : Rn × Rm → Rn , and hori-               expected cost F (θ) is differentiable due to the smoothing
zon H ∈ N. Given a sequence of costs ch : Rn × Rm → R,                  w̄. ∇F (θ) is referred to as the policy gradient.
a family of policies πh : Rn × Rd → Rm parameter-
ized by θ ∈ Rd , and a sequence of injected noise terms                 Zeroth-order estimator. The policy gradient can be esti-
w1:H ∈ (Rm )H , we define the cost-to-go functions                      mated only using samples of the function values.
                                PH                                      Definition 2.3. Given a single zeroth-order estimate of
         Vh (xh , wh:H , θ) =       h0 =h ch (xh , uh ),
                                                   0    0                                   ˆ [0] Fi (θ), we define the zeroth-order
                                                                        the policy gradient ∇
s.t. xh0 +1 = φ(xh0 , uh0 ), uh0 = π(xh0 , θ) + wh0 , h0 ≥ h.           batched gradient (ZoBG) ∇  ¯ [0] F (θ) as the sample mean,

Our aim is to minimize the policy optimization objective                                                    H                     
                                                                         ˆ [0] Fi (θ) := 1 V1 (x1 , wi , θ)
                                                                                                            X
                                                                         ∇                2          1:H      Dθ π(xih , θ)| whi
        F (θ) := Ex1 ∼ρ E                V1 (x1 , w1:H , θ),    (1)                    σ
                                i.i.d.
                           wh ∼ p                                                                                h=1
                                                                                            PN   ˆ [0]
                                                                         ¯ [0] F (θ) := 1
                                                                         ∇              N    i=1 ∇ Fi (θ),
where ρ is a distribution over initial states x1 , and
w1 , . . . , wH are independent and identically distributed ac-         where xih is the state at time h of a trajectory induced by
cording to some distribution p. In the main text, we make                           i
                                                                        the noise w1:H  , i is the index of the sample trajectory, and
the following assumption on the distributions ρ and p:                  Dθ π is the Jacobian matrix ∂π/∂θ ∈ Rm×d .
Assumption 2.1. We assume that ρ has finite moments, and
that p = N (0, σ 2 In ) for some σ > 0.                                 The hat notation denotes a per-sample Monte-Carlo estimate,
                                                                        and bar-notation a sample mean. The ZoBG is also referred
Our rationale for Gaussian p is that we view w1:H as smooth-            to as the REINFORCE (Williams, 1992), score function, or
ing to regularize the optimization landscape (Duchi et al.,             the likelihood-ratio gradient.
2011; Berahas et al., 2019). To simplify the main text, we
                                                                        Baseline. In practice, a baseline term b is subtracted from
take x1 to be deterministic (ρ is a dirac-delta), with general                     i
                                                                        V1 (x1 , w1:H  , θ) for variance reduction. We use the zero-
ρ being addressed in the appendix. Setting w̄ = w1:H ,
                                                                        noise rollout as the baseline b = V1 (x1 , 01:H , θ) (Berahas
p̄ = N (0, σ 2 InH ), and f (θ, w̄) = V1 (x1 , w̄, θ), we can
                                                                        et al., 2019):
express F (θ) as a stochastic optimization problem,
                                                                                                            H
                                                                                                           X                 
                  F (θ) := Ew̄∼p̄ f (θ, w̄).                                  1              i                       i     | i
                                                                                   V1 (x1 , w1:H , θ) − b      Dθ π(xh , θ) wh .
                                                                              σ2
                                                                                                         h=1

Trajectory optimization. Our parametrization also in-
                                                                        First-order estimator. In differentiable simulators, the gra-
cludes open-loop trajectory optimization. Letting the pol-
                                                                        dients of the dynamics φ and costs ch are available almost
icy parameters be an open-loop sequence of inputs θ =
                                                                        surely (i.e., with probability one). Hence, one may com-
{θ h }H
      h=1 and having no feedback π(xh , θ) = θ h , we opti-             pute the exact gradient ∇θ V1 (x1 , w1:H , θ) by automatic
mize over sequence of inputs to be applied to the system.
                                                                        differentiation and average them to estimate ∇F (θ).
One-step optimization. We illustrate some key ideas in the              Definition 2.4. Given a single first-order gradient esti-
open-loop case where H = 1: π : Rd → Rm is the identity                      ˆ [1] Fi (θ), we define the first-order batched gradient
                                                                        mate ∇
function with w̄ = w ∈ Rm , d = m and c : Rm → R,                       (FoBG) as the sample mean:
    F (θ) = Ew∼p f (θ, w),        f (θ, w) = c(θ + w).          (2)                  ˆ [1] Fi (θ) := ∇θ V1 (x1 , wi , θ)
                                                                                     ∇                            1:H
                                                                                                        PN       ˆ [1] Fi (θ).
                                                                                     ¯ [1] F (θ) := 1
                                                                                     ∇              N    i=1 ∇
2.1. Gradient Estimators
In order to minimize F (θ), we consider iterative optimiza-             The FoBG is also referred to as the reparametrization gradi-
tion using stochastic estimators of its gradient ∇F (θ). We             ent (Kingma et al., 2015), or the pathwise derivative (Schul-
say a function ψ : Rd1 → Rd2 has polynomial growth                      man et al., 2015). Finally, we define the empirical variance.
                                   Do Differentiable Simulators Give Better Policy Gradients?

Definition 2.5 (Empirical variance). For k ∈ {0, 1}, we             whose stochastic objective becomes the error function
define the empirical variance by
                                                                              F (θ) = Ew [H(θ + w)] = erf(−θ; σ 2 ),
                      PN    ˆ [k] Fi (θ) − ∇
                                           ¯ [k] F (θ)k2 .
       σ̂k2 = N 1−1    i=1 k∇
                                                                                           R ∞ 1 −x2 /σ2
                                                                    where erf(t; σ 2 ) := t √2πσ     e        dx is the Gaussian
                                                                    tail integral. Defining the gradient of the Monte-Carlo
                                                                    objective H(θ + w) requires subtlety. It is common in
3. Pitfalls of First-order Estimates                                physics to define ∇θ H(θ + w) = δ(θ + w) as a dirac-
                                                                    delta function, where integration is interpreted so that the
What are the cases for which we would prefer to use the             fundamental theorem of calculus holds. This is irreconcil-
ZoBG over the FoBG in policy optimization using differen-           able with using expectation to define the integral, which
tiable simulators? Throughout this section, we analyze the          presupposes that the law of large numbers hold. Indeed,
performance of the two estimators through their bias and            since ∇θ H(θ + w) = 0 for all θ 6= −w, we have
variance properties, and find pathologies where using the           Ewi δ(θ + wi ) = 0. Hence, the FoBG is biased, because
first-order estimator blindly results in worse performance.         the gradient of the stochastic objective at any θ is non-zero:
                                                                                          1
                                                                    ∇θ erf(−θ; σ 2 ) = √2πσ   exp(−(θ − w)/2σ 2 ) 6= 0.
                                                                    It is worth noting that the empirical variance of the FoBG
3.1. Bias under discontinuities                                     estimator in this example is zero, since all the samples are
                                                                    identically zero. On the other hand, the ZoBG escapes this
Under standard regularity conditions, it is well-known that         problem and provides an unbiased estimate, since it always
both estimators are unbiased estimators of the true gradient        takes finite intervals that include the integral of the delta.
∇F (θ). However, care must be taken to define these con-
ditions precisely. Fortunately, the ZoBG is still unbiased
under mild assumptions.
Lemma 3.1. Under Assumption 2.1 and Assumption 2.2,
the ZoBG is an unbiased estimator of the stochastic objec-
tive.
                    ¯ [0] F (θ)] = ∇F (θ).
                  E[∇
                                                                    Figure 2. From left: heaviside objective f (θ, w) and stochastic
                                                                    objective F (θ), empirical values of the gradient estimates, and
In contrast, the FoBG requires strong continuity conditions         their empirical variance.
in order to satisfy the requirement for unbiasedness. How-
ever, under Lipschitz continuity, it is indeed unbiased.
                                                                    3.2. The “Empirical bias” phenomenon
Lemma 3.2. Under Assumption 2.1 and Assumption 2.2,
and if φ(·, ·) is locally Lipschitz and ch (·, ·) is continuously   One might argue that strict discontinuity is simply an artifact
differentiable, then ∇ ¯ [1] F (θ) is defined almost surely, and
                                                                    of modeling choice in simulators; indeed, many simulators
                                                                    approximate discontinuous dynamics as a limit of continu-
                    ¯ [1] F (θ)] = ∇F (θ).
                  E[∇                                               ous ones with growing Lipschitz constant (Geilinger et al.,
                                                                    2020; Elandt et al., 2019). In this section, we explain how
The proofs and more rigorous statements of both lemmas              this can lead to a phenomenon we call empirical bias, where
are provided in Appendix A. Notice that Lemma 3.1 permits           the FoBG appears to have low empirical variance, but is still
Vh to have discontinuities (via discontinuities of ch and φ),       highly inaccurate; i.e. it “looks” biased when a finite number
whereas Lemma 3.2 does not.                                         of samples are used. Through this phenomenon, we claim
                                                                    that performance degradation of first-order gradient esti-
                                                                    mates do not require strict discontinuity, but is also present
Bias of FoBG under discontinuities. The FoBG can fail               in continuous, yet stiff approximations of discontinuities. 1
when applied to discontinuous landscapes. We illustrate a           Definition 3.4 (Empirical bias). Let z be a vector-valued
simple case of biasedness through a counterexample.                 random variable with E[kzk] < ∞. We say z has (β, ∆, S)-
Example 3.3 (Heaviside). (Bangaru et al., 2021; Suh et al.,         empirical bias if there is a random event E such that Pr[E] ≥
2021) Consider the Heaviside function,                              1 − β, and kE[z | E] − E[z]k ≥ ∆, but kz − E[z | E]k ≤ S
                                       (                            almost surely on E.
                                         1 t≥0
     f (θ, w) = H(θ + w), H(t) =                  ,                    1
                                                                         We say that a continuous function f is stiff at x if the magni-
                                         0 t<0                      tude of the gradient k∇f (x)k is high.
                                      Do Differentiable Simulators Give Better Policy Gradients?

A paradigmatic example of empirical bias is a random scalar
z which takes the value 0 with probability 1 − β, and β1
with probability β. Setting E = {z = 0}, we see E[z] = 1,
E[z | E] = 0, and so z satisfies (β, 1, 0)-empirical bias.
Note that Var[z] = 1/β − 1; in fact, small-β empirical bias
implies large variance more generally.
Lemma 3.5. Suppose z has (β, ∆, S)-empirical bias. Then
          ∆2
Var[z] ≥ β0 , where ∆0 := max{0, (1 − β)∆ − βkE[z]k}.

Empirical bias naturally arises for discontinuities or stiff
continuous approximations. We give two examples of com-
mon discontinuities that arise in differentiable simulation,
that permit continuous approximations.
Example 3.6 (Coulomb friction). The Coulomb model of
friction is discontinuous in the relative tangential velocity
between two bodies. In many simulators (Geilinger et al.,               Figure 4. Top column: illustration of the physical system and the
2020; Castro et al., 2020), it is common to consider a contin-          relaxation of Coulomb friction. Bottom column: the values of
                                                                        estimators and their empirical variances depending on number of
uous approximation instead. We idealize such approxima-
                                                                        samples and slip tolerance. Values of FoBG are zero in low-sample
tions through a piecewise linear relaxation of the Heaviside
                                                                        regimes due to empirical bias. As ν → 0, the empirical variance
that is continuous, parametrized by the width of the middle             of FoBG goes to zero, which shows as empty in the log-scale.
linear region ν (which corresponds to slip tolerance).                  Expected variance, however, blows up as it scales with 1/ν.
                        (
                          2t/ν if |t| ≤ ν/2
              H̄ν (t) =                        .
                          H(t) else                                     create discontinuities. It is possible to make a continuous
In practice, lower values of ν lead to more realistic behavior          relaxation (Elandt et al., 2019) by considering smoother
in simulation (Tedrake, 2022), but this has adverse effects             geometry, depicted by the addition of the dome in Figure 3.
for empirical bias. Considering fν (θ, w) = H̄ν (θ + w),                While this makes FoBG no longer biased asymptotically,
we have Fν (θ) = Ew [H̄ν (θ + w)] := erf(ν/2 − θ; σ 2 ). In             the stiffness of the relaxation results in high empirical bias.
                            1
particular, setting cσ := √2πσ  , then at θ = ν/2, ∇Fν (θ) =
cσ , whereas, with probability at least cσ ν, ∇fν (θ, w) = 0.
Hence, the FoBG has (cσ ν, cσ , 0) empirical bias, and its              3.3. High variance first-order estimates
variance scales with 1/ν as ν → 0. The limiting ν = 0
case, corresponding to the Coulomb model, is the Heaviside              Even in the absence of empirical bias, we present other
from Example 3.3, where the limit of high empirical bias,               cases in which FoBG suffers simply due to high variance.
as well as variance, becomes biased in expectation (but,
                                                                        Scenario 1: Persistent stiffness. When the dynamics are
surprisingly, zero variance!). We empirically illustrate this
                                                                        stiff 2 , such as contact models with stiff spring approxima-
effect in Figure 4. We also note that more complicated
                                                                          2
models of friction (e.g. that incorporates the Stribeck effect              We say that a discrete-time dynamical system is stiff if the
(Stribeck, 1903)) would suffer similar problems.                        mapping function φ is stiff. Note that when φ contains forces from
Example 3.7. (Geometric Discontinuity). Discontinuity
also comes from surface normals. We show this in Fig-
ure 3, where balls that collide with a rectangular geometry




Figure 3. Left: More detailed example of ball hitting the wall in
Figure 1.B. Left: The green trajectories hit a rectangular wall,        Figure 5. The variance of the gradient of V1 , with running cost
displaying discontinuities. Right: the pink trajectories collide with   ch = kx2h − xg k2 , with respect to input trajectory as spring
the dome on top, and show continuous but stiff behavior.                constant k increases. Mass m and damping coefficient c are fixed.
                                     Do Differentiable Simulators Give Better Policy Gradients?

                                                                       4. α-order Gradient Estimator
                                                                       Previous examples give us insight on which landscapes are
                                                                       better fit for first-order estimates of policy gradient, and
                                                                       which are better fit for zeroth-order ones. As shown in
                                                                       Figure 7, even on a single policy optimization objective,
                                                                       it is best to adaptively switch between the first and zeroth-
                                                                       order estimators depending on the local characteristics of the
                                                                       landscape. In this section, we propose a strategy to achieve
                                                                       this adaptively, interpolating between the two estimators to
Figure 6. Variance of the gradient of the terminal cost kqH − q g k2
                                                                       reap the benefits of both approaches simultaneously.
with respect to the initial position q1 . As horizon grows through a
chaotic system, the ZoBG dominates the FoBG.                           Definition 4.1. Given α ∈ [0, 1], we define the alpha-order
                                                                       batched gradient (AoBG) as:

tions (Hunt & Crossley, 1975), the high norm of the gradient                 ¯ [α] F (θ) = α∇
                                                                             ∇              ¯ [1] F (θ) + (1 − α)∇
                                                                                                                 ¯ [0] F (θ).
can contribute to high variance of the FoBG.
Example 3.8. (Pushing with stiff contact). We demon-                   When interpolating, we use independent trajectories to gen-
strate this phenomenon through a simple 1D pushing exam-                     ¯ [1] F (θ) and ∇
                                                                       erate ∇               ¯ [0] F (θ) (see Appendix C.1). We
ple in Figure 5, where the ZoBG has lower variance than the            consider strategies for selecting α in a local fashion, as
FoBG as stiffness increases, until numerical semi-implicit             a function of the observed sample, as detailed below.
integration becomes unstable under a fixed timestep.
In practice, lowering the timestep can alleviate the issue at          4.1. A robust interpolation protocol
the cost of more computation time. Less stiff formulations of
contact dynamics (Stewart & Trinkle, 2000; Mirtich, 1996)              A potential approach might be to select α based on achieving
also addresses this problem effectively.                               minimum variance (Parmas et al., 2018; Metz et al., 2019),
Scenario 2: Chaos. As noted in (Metz et al., 2021), even               considering empirical variance as an estimate. However, in
if the gradient of the dynamics is small at every h, their             light of the empirical bias phenomenon detailed in Section 3
compounding product can cause k∇θ V1 k to be large if the              (or even actual bias in the presence of discontinuities), we
system is chaotic. Yet, in expectation, the gradient of the            see that the empirical variance is unreliable, and can lead
stochastic objective ∇F = ∇E[V1 ] can be benign and well-              to inaccurate estimates for our setting. For this reason, we
behaved (Lasota & Mackey, 1996).                                       consider an additional criterion of uniform accuracy:
Example 3.9. (Chaos of double pendulum). We demon-                     Definition 4.2 (Accuracy). α is (γ, δ)-accurate if the bound
strate this in Figure 6 for a classic chaotic system of the            on the error of AoBG is satisfied with probability δ:
double pendulum. As the horizon of the trajectory increases,
                                                                                        ¯ [α] F (θ) − ∇F (θ)k ≤ γ.
                                                                                       k∇                                        (3)
the variance of FoBG becomes higher than that of ZoBG.

                                                                       To remedy the limitations of considering empirical vari-
Comparison to ZoBG. Compared to the pitfalls of FoBG,                  ance in isolation, we propose an interpolation protocol that
the ZoBG variance can be bounded as follows.                           can satisfy an accuracy guarantee, while still attempting to
Lemma 3.10. If for all x and w̄, |V1 (x, w̄, θ)| ≤ BV and              minimize the variance.
kDθ π(x, θ)kop ≤ Bπ , then
                                                                                  min       α2 σ̂12 + (1 − α)2 σ̂02
                                                                                 α∈[0,1]
                                               2  2
      ¯ [0] F (θ)] =    1     ˆ [0] Fi (θ)] ≤ BV Bπ · Hn .                                                                       (4)
  Var[∇                   Var[∇                                                      s.t.    + α k∇¯ [1] F − ∇¯ [0] F k ≤ γ.
                        N                      N      σ2                                          |         {z         }
                                                                                                            B
We refer to Appendix B.2 for proof. Lemma 3.10 is intended             We explain the terms in Eq (4) below in detail.
to provide a qualitative understanding of the zeroth-order
variance: it scales with the horizon-dimension product Hn,             Objective. Since we interpolate the FoBG and ZoBG using
but not the scale of the derivatives. On the other hand, the           independent samples, α2 σ̂12 + (1 − α)2 σ̂02 is an unbiased
variance of FoBG does; when Hn                 ˆ [1]                                       ¯ [α] F (θ)]. Thus, our objective is to
                                                                       estimate of N · Var[∇
                                   σ 2  Var[∇ F (θ)] =
Var[∇θ V (x1 , w̄, θ)], the ZoBG has higher variance.                  choose α to minimize this variance.
spring-like components, k∇φk scales with the spring constant.          Constraint. Our constraint serves to enforce accuracy.
Thus, the presence of a stiff spring leads to a stiff system.          Since the FoBG is potentially biased, we use ZoBG as a
                                     Do Differentiable Simulators Give Better Policy Gradients?




Figure 7. First Column: Ball with wall example. In the third row, the triangle is the initial point, and red/blue/green stars are the optimum
achieved by FoBG, ZoBG, and AoBG respectively (blue and green stars overlap). Second column: Iteration vs. Cost plot of different
gradients. Right columns: Same plot repeated for the Momentum Transfer example. Standard deviation plotted 10 fold for visualization.


surrogate of ∇F (θ). For this purpose, we use  > 0 as a                    • In pathological cases where we are unbiased yet σ̂12 
confidence bound on k∇ ¯ [0] F (θ) − ∇F (θ)k from the ob-                     σ̂02 (e.g. stiffness and chaos), then α ≈ 0.
tained samples. When  is a valid confidence bound that                     • If there is a large difference between the ZoBG and the
holds with probability δ, we prove that our constraint in                     FoBG such that B  0, we expect strict/empirical bias
Eq (4) guarantees accuracy in Eq (3).                                         from discontinuities and tend towards using ZoBG.
Lemma 4.3 (Robustness). Suppose that  + αB ≤ γ with
probability δ. Then, α is (γ, δ)-accurate.

Proof. By repeated applications of the triangle inequality.             5. Landscape Analysis & Case Studies
See Appendix C.3 for a detailed proof.
                                                                        5.1. Landscape analysis on examples
Specifying the confidence  > 0. We select  > 0 based
on a Bernstein vector concentration bound (Appendix C.4),               Though we have characterized the bias-variance characteris-
which only requires a prior upper bound on the magnitude                tics of different gradients, their convergence properties in
of the value function V1 (·) and gradients Dθ π(·, θ).                  landscapes of physical systems remain to be investigated.
Asymptotic feasibility. Eq (4) is not feasible if  > γ,                We visualize the performance of fixed-step gradient descent
which would indicate that we simply do not have enough                  with the FoBG, ZoBG, and AoBG on examples of Figure 1.
samples to guarantee (γ, δ)-accuracy. In this case, we                  Ball with wall. On the system of Figure 1.B, the FoBG fails
choose to side on conservatism and fully use the ZoBG                   to make progress at the region of flatness, while the ZoBG
by setting α = 0. Asymptotically, as the number of samples              and AoBG successfully find the minima of the landscape
N → ∞, the confidence interval ε → 0, which implies that                (Figure 7). In addition, the interpolation scheme switches
Eq (4) will always be feasible.                                         to prioritizing ZoBG near discontinuities, while using more
Finally, we note that Eq (4) has a closed form solution,                information from FoBG far from discontinuities; as a result,
whose proof is provided in Appendix C.2.                                the variance of AoBG is lower than that of ZoBG.
                                                              σ̂ 2      Angular momentum transfer. Next, we show results for
Lemma 4.4. With γ = ∞, the optimal α is α∞ := σ̂2 +σ̂
                                                   0
                                                      2.
                                                1     0                 the momentum transfer system of Figure 1.C in Figure 7.
For finite γ ≥ , Eq (4) is                                             Running gradient descent results in both the ZoBG and
                   (                                                    AoBG converging to the robust local minima of the solution.
                     α∞     if α∞ B ≤ γ − ε                             However, the bias of FoBG forces it off the cliff and the
             αγ := γ−ε                              (5)
                       B    otherwise .                                 optimizer is unable to recover. Again, our interpolation
                                                                        scheme smoothly switches to prioritizing the ZoBG near
We give some qualitative characteristics of the solution:               the discontinuity, enabling it to stay within the safe region
                                                                        while maximizing the transferred momentum.
   • If we are within constraint and σ̂02  σ̂12 , as we can            Bias-variance leads to different minima. Through these
     expect from benign smooth systems, then α ≈ 1, and                 examples with discontinuities, we claim that the bias-
     we rely more on the FoBG.                                          variance characteristics of gradients in these landscapes not
                                    Do Differentiable Simulators Give Better Policy Gradients?




Figure 8. 1st column: trajectory optimization on pushing example with different contact models. AoBG and FoBG overlaps in soft
pushing example. 2nd column: trajectory optimization on friction contact, and policy optimization on the tennis example. 3rd / 4th
column: Visualization of policy performance for tennis. Black dots correspond to initial positions and colored dots correspond to final
position, while the shaded lines are visualizations of individual closed-loop trajectories across multiple initial conditions.


only lead to different convergence rates, but convergence             mal force sequence of the first block to minimize distance
to different minima. The same argument holds for nearly               between the second block and the goal position. Our results
discontinuous landscapes that display high empirical bias.            in Figure 8 show that for soft springs (k = 10), the FoBG
Both estimators are unbiased in expectation, and the high             outperforms the ZoBG, but stiffer springs (k = 1000) re-
variance of FoBG should manifest itself in worse conver-              sults in the ZoBG outperforming the FoBG. This confirms
gence rates. Yet, the high empirical bias in the finite-sample        our hypothesis that the stiffness of contact models has direct
regime leads to low empirical variance and different minima,          correlations with the variance of the estimators, which in
leading to performance that is indistinguishable from when            turn affects the convergence rate of optimization algorithms
the underlying landscape is truly discontinuous.                      that use such estimators.
Combined with the benefits of stochasticity in Section 1, we          In addition, we note that the interpolated gradient AoBG
believe that this might explain why zero-order methods in             is able to automatically choose between the two gradients
RL are solving problems for physical systems where deter-             that performs better by utilizing empirical variance as a
ministic (even stochastic) first order methods have struggled.        statistical measure of performance.
                                                                      Friction: Trajectory Optimization. We describe perfor-
                                                                      mance of gradients on the friction (Figure 4) environment.
5.2. Policy optimization case studies                                Although the FoBG initially converges faster in this envi-
To validate our results on policy optimization problems with         ronment, it is unaware of the discontinuity that occurs when
differentiable simulators, we compare the performance of             it slides off the box. As a result, the performance quickly
different gradients on time-stepping simulations written in          degrades after few iterations. On the other hand, the AoBG
torch (Paszke et al., 2019). For all of our examples, we             and ZoBG successfully optimize the trajectory, with AoBG
validate the correctness of the analytic gradients by compar-        showing slightly faster convergence.
ing the values of FoBG and ZoBG on a one-step cost.                  Tennis: Policy optimization. Next, we describe the per-
To empirically verify the various hypotheses made in this            formance of different gradients on a tennis environment
paper, we compare the performance of three gradient esti-            (similar to breakout), where the paddle needs to bounce
mators: the FoBG and ZoBG, which uniformly utilizes first            the ball to some desired target location. We use a linear
and zeroth-order gradients, and the AoBG, which utilizes             feedback policy with d = 21 parameters, and horizon of
our robust interpolation protocol.                                   H = 200. In order to correctly obtain analytic gradients,
                                                                     we use continuous event detection with the time of impact
Pushing: Trajectory optimization. We describe perfor-                formulation (Hu et al., 2020). The results of running policy
mance of gradients on the pushing (Figure 5) environment,            optimization is presented in Figure 8.
where contact is modeled using the penalty method (i.e. stiff
spring) with additional viscous damping on the velocities            While the ZoBG and the AoBG are successful in finding a
of the system. We use horizon of H = 200 to find the opti-           policy that bounces the balls through different initial condi-
                                  Do Differentiable Simulators Give Better Policy Gradients?

tions, the FoBG suffers from the discontinuities of geometry,     also has the effect of smoothing the induced value function,
and still misses many of the balls. Furthermore, the AoBG         though the resulting landscape will be different from the
still converges slightly faster than the ZoBG by utilizing        landscaped induced by appending noise to the policy output.
first-order information.
                                                                  However, even when φ can be analytically smoothed, Monte-
                                                                  Carlo sampling is still required for optimization across ini-
                                                                  tial conditions ρ. For such settings, the findings of Sec-
6. Discussion                                                     tion 3.2 is still highly relevant, as the performance of FoBG
                                                                  still suffers from the stiffness of the smoothed approxima-
In this section, we elaborate and discuss on some of the          tion of φ. However, as many smoothing methods provide
ramifications of our work.                                        access to parameters that control the strength of smooth-
                                                                  ing, algorithms may be able to take a curriculum-learning
Impact on Computation Time. The convergence rate of               approach where dynamics become more realistic, and less
gradient descent in stochastic optimization scales directly       smooth, as more iterations are taken for policy search.
with the variance of the estimator (Ghadimi & Lan, 2013).
For smooth and well-behaved landscapes, FoBG often con-
verges faster since Var[∇ ¯ [1] F ] < Var[∇
                                          ¯ [0] F ]. However,
                                                                  7. Conclusion
when there are discontinuities or near-discontinuities in the
landscape, this promise no longer holds since gradient de-        Do differentiable simulators give better policy gradients?
scent using FoBG might not converge due to bias. Indeed,          We have shown that the answer depends intricately on the
Example 3.6 tells us that bias due to discontinuities can be      underlying characteristics of the physical systems. While
interpreted as infinite variance. Under this interpretation,      Lipschitz continuous systems with reasonably bounded gra-
the convergence rate of gradient descent is ill-defined.          dients may enjoy fast convergence given by the low variance
                                                                  of first-order estimators, using the gradients of differentiable
In practice; however, the computation cost of obtaining the
                                                                  simulators may hurt for problems that involve nearly/strictly
gradient must be taken into consideration as well. Given
                                                                  discontinuous landscapes, stiff dynamics, or chaotic sys-
the same number of samples N , the computation of FoBG
                                                                  tems. Moreover, due to the empirical bias phenomenon,
is more costly than the ZoBG, as FoBG requires automatic
                                                                  bias of first-order estimators in nearly/strictly discontinuous
differentiation through the computation graph while ZoBG
                                                                  landscapes cannot be diagnosed from empirical variance
simply requires evaluation. Thus, the benefits of conver-
                                                                  alone. We believe that many challenging tasks that both
gence rates using the FoBG must justify the additional cost
                                                                  RL and differentiable simulators try to address necessarily
of computing them.
                                                                  involve dealing with physical systems with such characteris-
Implicit time-stepping. In our work, we have mainly ad-           tics, such as those that are rich with contact.
dressed two classes of simulation methods for contact. The
                                                                  These limitations of using differentiable simulators for plan-
first uses the penalty method (Geilinger et al., 2020; Tedrake,
                                                                  ning and control need to be addressed from both the design
2022), which approximates contact via stiff springs, and the
                                                                  of simulator and algorithms: from the simulator side, we
second uses event detection (Hu et al., 2020), which explic-
                                                                  have shown that certain modeling decisions such as stiffness
itly computes time-of-impact for automatic differentiation.
                                                                  of contact dynamics can have significant underlying conse-
In addition to the ones covered, we note a third class of         quences in the performance of policy optimization that uses
simulators that rely on optimization-based implicit time-         gradients from these simulators. From the algorithm side,
stepping (Todorov et al., 2012; Coumans & Bai, 2016–2021;         we have shown we can automate the procedure of deciding
Macklin et al., 2014; Pang, 2021; Howell et al., 2022), which     which one to use online via interpolation.
can be made differentiable by sensitivity analysis (Boyd &
Vandenberghe, 2004). These simulators suffer less from
stiffness by considering more long-term behavior across
each timestep; however, geometrical discontinuities can still     Acknowledgements
remain problematic. We leave detailed empirical study using
these simulators to future work.
                                                                  This work was funded by Amazon PO 2D-06310236,
Analytic Smoothing. Randomized smoothing relies on                Lincoln Laboratory/Air Force Contract No. FA8702-
smoothing out the policy objective via the process of noise       15-D-0001, Defense Science & Technology Agency
injection and sampling. However, one can also resort to           No.DST00OECI20300823, NSF Award EFMA-1830901,
analytic smoothing, which finds analytically smooth approx-       and the Ocado Group. We would also like to thank the
imation of the underlying dynamics φ (Huang et al., 2021;         anonymous ICML reviewers for their valuable feedback on
Howell et al., 2022). Modifying and smoothing φ directly          the manuscript.
                                  Do Differentiable Simulators Give Better Policy Gradients?

References                                                       Du, T., Li, Y., Xu, J., Spielberg, A., Wu, K., Rus, D., and
                                                                   Matusik, W. D3{pg}: Deep differentiable deterministic
Agarwal, A., Kakade, S. M., Lee, J. D., and Mahajan, G.            policy gradients, 2020. URL https://openreview.
  On the theory of policy gradient methods: Optimality,            net/forum?id=rkxZCJrtwS.
  approximation, and distribution shift, 2020.
                                                                 Duchi, J., Bartlett, P., and Wainwright, M. Randomized
Bangaru, S. P., Michel, J., Mu, K., Bernstein, G., Li, T.-         smoothing for stochastic optimization. SIAM Journal on
  M., and Ragan-Kelley, J. Systematically differentiating         Optimization, 22, 03 2011. doi: 10.1137/110831659.
  parametric discontinuities. ACM Trans. Graph., 40(4),
  July 2021. ISSN 0730-0301. doi: 10.1145/3450626.               Duchi, J., Jordan, M., Wainwright, M., and Wibisono, A.
  3459775.                                                         Optimal rates for zero-order convex optimization: The
                                                                   power of two function evaluations. IEEE Transactions
Berahas, A. S., Cao, L., Choromanski, K., and Scheinberg,          on Information Theory, 61, 12 2015. doi: 10.1109/TIT.
  K. A theoretical and empirical comparison of gradient            2015.2409256.
  approximations in derivative-free optimization. arXiv:
  Optimization and Control, 2019.                                Elandt, R., Drumwright, E., Sherman, M., and Ruina, A.
                                                                   A pressure field model for fast, robust approximation of
Bhandari, J. and Russo, D. Global optimality guarantees for        net contact force and moment between nominally rigid
  policy gradient methods, 2020.                                   objects. IROS, pp. 8238–8245, 2019.

Boyd, S. and Vandenberghe, L. Convex optimization. Cam-          Ern, A. and Guermond, J.-L. Theory and practice of finite
  bridge university press, 2004.                                   elements, volume 159. Springer Science & Business
                                                                   Media, 2013.
Carpentier, J., Saurel, G., Buondonno, G., Mirabel, J., Lami-
  raux, F., Stasse, O., and Mansard, N. The pinocchio            Fazel, M., Ge, R., Kakade, S. M., and Mesbahi, M. Global
  c++ library : A fast and flexible implementation of rigid        convergence of policy gradient methods for the linear
  body dynamics algorithms and their analytical deriva-            quadratic regulator, 2019.
  tives. In 2019 IEEE/SICE International Symposium
  on System Integration (SII), pp. 614–619, 2019. doi:           Freeman, C. D., Frey, E., Raichuk, A., Girgin, S., Mor-
  10.1109/SII.2019.8700380.                                        datch, I., and Bachem, O. Brax - a differentiable
                                                                   physics engine for large scale rigid body simulation. In
Castro, A. M., Qu, A., Kuppuswamy, N., Alspach, A., and            Thirty-fifth Conference on Neural Information Process-
  Sherman, M. A transition-aware method for the sim-               ing Systems Datasets and Benchmarks Track (Round 1),
  ulation of compliant contact with regularized friction.          2021. URL https://openreview.net/forum?
  IEEE Robotics and Automation Letters, 5(2):1859–1866,            id=VdvDlnnjzIN.
  Apr 2020. ISSN 2377-3774. doi: 10.1109/lra.2020.
  2969933. URL http://dx.doi.org/10.1109/                        Geilinger, M., Hahn, D., Zehnder, J., Bächer, M.,
  LRA.2020.2969933.                                                Thomaszewski, B., and Coros, S. Add: Analytically
                                                                   differentiable dynamics for multi-body systems with fric-
Çinlar, E. Probability and stochastics, volume 261. Springer,     tional contact, 2020.
   2011.
                                                                 Ghadimi, S. and Lan, G. Stochastic first- and zeroth-order
Coumans, E. and Bai, Y. Pybullet, a python module for              methods for nonconvex stochastic programming. SIAM
  physics simulation for games, robotics and machine learn-       Journal on Optimization, 23(4):2341–2368, 2013. doi:
  ing. http://pybullet.org, 2016–2021.                            10.1137/120880811. URL https://doi.org/10.
                                                                  1137/120880811.
de Avila Belbute-Peres, F., Smith, K., Allen, K., Tenen-
  baum, J., and Kolter, J. Z. End-to-end differentiable   Gradu, P., Hallman, J., Suo, D., Yu, A., Agarwal, N., Ghai,
  physics for learning and control.       In Bengio, S.,    U., Singh, K., Zhang, C., Majumdar, A., and Hazan, E.
  Wallach, H., Larochelle, H., Grauman, K., Cesa-           Deluca – a differentiable control library: Environments,
  Bianchi, N., and Garnett, R. (eds.), Advances in Neural   methods, and benchmarking, 2021.
  Information Processing Systems, volume 31. Curran As-
  sociates, Inc., 2018. URL https://proceedings. Howell, T. A., Cleac’h, S. L., Kolter, J. Z., Schwager, M.,
  neurips.cc/paper/2018/file/                               and Manchester, Z. Dojo: A differentiable simulator for
  842424a1d0595b76ec4fa03c46e8d755-Paper.                   robotics, 2022. URL https://arxiv.org/abs/
  pdf.                                                      2203.00806.
                                 Do Differentiable Simulators Give Better Policy Gradients?

Hu, Y., Anderson, L., Li, T.-M., Sun, Q., Carr, N., Ragan-      Metz, L., Maheswaranathan, N., Nixon, J., Freeman, D., and
  Kelley, J., and Durand, F. Difftaichi: Differentiable pro-     Sohl-Dickstein, J. Understanding and correcting patholo-
  gramming for physical simulation. ICLR, 2020.                  gies in the training of learned optimizers. In Chaudhuri, K.
                                                                 and Salakhutdinov, R. (eds.), Proceedings of the 36th In-
Huang, Z., Hu, Y., Du, T., Zhou, S., Su, H., Tenenbaum,          ternational Conference on Machine Learning, volume 97
 J. B., and Gan, C. Plasticinelab: A soft-body ma-               of Proceedings of Machine Learning Research, pp. 4556–
  nipulation benchmark with differentiable physics. In           4565. PMLR, 09–15 Jun 2019.
 International Conference on Learning Representations,
  2021. URL https://openreview.net/forum?                       Metz, L., Freeman, C. D., Schoenholz, S. S., and Kachman,
  id=xCcdBRQEDW.                                                 T. Gradients are not all you need, 2021.
Hunt, K. H. and Crossley, F. R. E. Coefficient of Resti-
                                                                Mirtich, B. V. Impulse-Based Dynamic Simulation of Rigid
  tution Interpreted as Damping in Vibroimpact. Journal
                                                                 Body Systems. PhD thesis, 1996. AAI9723116.
  of Applied Mechanics, 42(2):440–445, 06 1975. ISSN
  0021-8936. doi: 10.1115/1.3423596. URL https:
                                                                Mora, M. A. Z., Peychev, M., Ha, S., Vechev, M., and
 //doi.org/10.1115/1.3423596.
                                                                 Coros, S. Pods: Policy optimization via differentiable
Kakade, S. M. On the sample complexity of reinforcement          simulation. In Meila, M. and Zhang, T. (eds.), Pro-
  learning. University of London, University College Lon-        ceedings of the 38th International Conference on Ma-
  don (United Kingdom), 2003.                                    chine Learning, volume 139 of Proceedings of Machine
                                                                 Learning Research, pp. 7805–7817. PMLR, 18–24 Jul
Kingma, D. P., Salimans, T., and Welling, M. Variational         2021. URL https://proceedings.mlr.press/
  dropout and the local reparameterization trick. In Cortes,     v139/mora21a.html.
  C., Lawrence, N., Lee, D., Sugiyama, M., and Garnett,
  R. (eds.), Advances in Neural Information Processing          Pang, T. A convex quasistatic time-stepping scheme for rigid
  Systems, volume 28. Curran Associates, Inc., 2015.              multibody systems with contact and friction. 2021 IEEE
                                                                  International Conference on Robotics and Automation
Lasota, A. and Mackey, M. C. Chaos, Fractals, and Noise:
                                                                  (ICRA), pp. 6614–6620, 2021.
  Stochastic Aspects of Dynamics. Cambridge university
  press, 1996.
                                                                Parmas, P., Rasmussen, C. E., Peters, J., and Doya, K.
Le Lidec, Q., Montaut, L., Schmid, C., Laptev, I.,                PIPPS: Flexible model-based policy search robust to the
  and Carpentier, J. Leveraging Randomized Smooth-                curse of chaos. In Dy, J. and Krause, A. (eds.), Proceed-
  ing for Optimal Control of Nonsmooth Dynamical                  ings of the 35th International Conference on Machine
  Systems.    working paper or preprint, December                 Learning, volume 80 of Proceedings of Machine Learn-
  2021. URL https://hal.archives-ouvertes.                        ing Research, pp. 4065–4074. PMLR, 10–15 Jul 2018.
  fr/hal-03480419.
                                                                Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J.,
Macklin, M., Müller, M., Chentanez, N., and Kim,                 Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga,
 T.-Y.     Unified particle physics for real-time ap-             L., Desmaison, A., Kopf, A., Yang, E., DeVito, Z., Rai-
 plications.   ACM Trans. Graph., 33(4), jul 2014.                son, M., Tejani, A., Chilamkurthy, S., Steiner, B., Fang,
 ISSN 0730-0301. doi: 10.1145/2601097.2601152.                    L., Bai, J., and Chintala, S. Pytorch: An imperative
 URL https://doi-org.libproxy.mit.edu/                            style, high-performance deep learning library. In Wal-
 10.1145/2601097.2601152.                                         lach, H., Larochelle, H., Beygelzimer, A., d’Alché Buc,
                                                                  F., Fox, E., and Garnett, R. (eds.), Advances in Neural In-
Mahamed, S., Rosca, M., Figurnov, M., and Mnih, A. Monte
                                                                  formation Processing Systems 32, pp. 8024–8035. Curran
 carlo gradient estimation in machine learning. In Dy,
                                                                  Associates, Inc., 2019.
 J. and Krause, A. (eds.), Journal of Machine Learning
 Research, volume 21, pp. 1–63, 4 2020.                         Rudin, W. et al. Principles of mathematical analysis, vol-
Mason, M. T. Mechanics of Robotic Manipulation. The MIT           ume 3. McGraw-hill New York, 1964.
 Press, 06 2001. ISBN 9780262256629. doi: 10.7551/
 mitpress/4527.001.0001. URL https://doi.org/                   Schulman, J., Heess, N., Weber, T., and Abbeel, P. Gra-
 10.7551/mitpress/4527.001.0001.                                  dient estimation using stochastic computation graphs.
                                                                  In Cortes, C., Lawrence, N., Lee, D., Sugiyama, M.,
Maurer, A. and Pontil, M. Empirical bernstein bounds              and Garnett, R. (eds.), Advances in Neural Information
 and sample variance penalization. arXiv preprint                 Processing Systems, volume 28. Curran Associates, Inc.,
 arXiv:0907.3740, 2009.                                           2015.
                                  Do Differentiable Simulators Give Better Policy Gradients?

Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and
  Klimov, O. Proximal policy optimization algorithms,
  2017.
Stein, E. M. and Shakarchi, R. Real analysis. Princeton
  University Press, 2009.
Stewart, D. and Trinkle, J. J. An implicit time-stepping
  scheme for rigid body dynamics with coulomb friction.
  volume 1, pp. 162–169, 01 2000. doi: 10.1109/ROBOT.
  2000.844054.
Stribeck, R. Die wesentlichen Eigenschaften der Gleit-
  und Rollenlager. Mitteilungen über Forschungsarbeiten
  auf dem Gebiete des Ingenieurwesens, insbesondere aus
  den Laboratorien der technischen Hochschulen. Julius
  Springer, 1903.
Suh, H. J. T., Pang, T., and Tedrake, R. Bundled gradients
  through contact via randomized smoothing. arXiv pre-
  print, 2021.
Sutton, R., Mcallester, D., Singh, S., and Mansour, Y. Policy
  gradient methods for reinforcement learning with func-
  tion approximation. Adv. Neural Inf. Process. Syst, 12,
  02 2000.
Tedrake, R. Drake: A planning, control, and analysis
  toolbox for nonlinear dynamical systems, 2022. URL
  http://drake.mit.edu.
Todorov, E., Erez, T., and Tassa, Y. Mujoco: A physics
  engine for model-based control. In IROS, pp. 5026–5033,
  2012. doi: 10.1109/IROS.2012.6386109.
Tropp, J. A. An introduction to matrix concentration
  inequalities. Foundations and Trends® in Machine
  Learning, 8(1-2):1–230, 2015. ISSN 1935-8237. doi:
  10.1561/2200000048. URL http://dx.doi.org/
  10.1561/2200000048.
van der Schaft, A. and Schumacher, H. An Introduction to
  Hybrid Dynamical Systems. Springer Publishing Com-
  pany, Incorporated, 1st edition, 2000. ISBN 978-1-4471-
  3916-4.
Wasserman, L. All of statistics: a concise course in statisti-
 cal inference, volume 26. Springer, 2004.
Werling, K., Omens, D., Lee, J., Exarchos, I., and Liu,
 C. K. Fast and feature-complete differentiable physics
 for articulated rigid bodies with contact, 2021.
Williams, R. J. Simple statistical gradient-following algo-
 rithms for connectionist reinforcement learning. Machine
 Learning, 3, 05 1992.
Zhang, K., Koppel, A., Zhu, H., and Başar, T. Global con-
  vergence of policy gradient methods to (almost) locally
  optimal policies, 2020.
                              Do Differentiable Simulators Give Better Policy Gradients?


                               Supplementary Materials for
                “Do Differentiable Simulators Give Better Policy Gradients”



A. Formal Expected Gradient Computations

This section establishes rigorous unbiasedness guarantees for the ZoBG (under general conditions) and of the
FoBG (under more restrictive conditions). Specifically, Corollary A.12 provides a rigorous version of the ZoBG
guarantee, Lemma 3.1, which is a special case of Proposition A.11 which holds for general, possibly non-
Gaussian noise distributions. The FoBG estimator is addressed in Proposition A.15, which provides the rigorous
statement of Lemma 3.2. We present a lengthy preliminaries section, Appendix A.1, to formalize the results that
follow. We then follow with formal statements of the results, Appendix A.2, and defer proofs to Appendix A.3.
The preliminaries below are requisites only for the results and proofs within this section, and are not needed in
future appendices.


A.1. Preliminaries

Throughout, k · k denotes the Euclidean norm of vectors. We begin by specifying our sense of expectations
and derivatives, and then turn to other, less-standard preliminaries. To rigorously describe expectations of
non-continuous functions and of derivatives of non-smooth functions, we start with some preliminaries from
measure theory.


Lebesgue measurability.     For a background on measure theory, we direct the reader to (Stein & Shakarchi,
2009). Here, we recall a few definitions. We define the set of Lebesgue measurable sets L (RD ) as the collection
                                                                                  0
of subset Z ⊂ RD for which the Lebesgue measure is well-defined. We let B(RD ) ⊂ L (RD ) be the collection
                                 0                                      0
of Borel measurable sets on RD . We say a mapping Φ : RD → RD is Lebesgue measurable if for all Z 0 ∈
       0
B(RD ), Φ−1 (Z 0 ) ∈ L (RD ). We say it is Borel measurable if, more strongly, it holds that Φ−1 (Z 0 ) ∈ B(RD ).
The composition of Borel measurable functions are Borel measurable, but the same is not true more generally
for Lebesgue measurable functions. Throughout, all functions are assumed Borel measurable unless otherwise
specified, so their compositions are also Borel measurable.
More generally, given a Lebesgue measurable set Z ⊂ RD , we define L (Z) as the set {Z ∩ Z̃ : Z̃ ∈ L (RR )},
                                                                                                               d

                                 0                                                             0
and say a function Φ : Z → RD is Lebesgue mearuable on its domain if for all Z 0 ∈ B(RD ), Φ−1 (Z 0 ) ∈
L (RD ).


Lebesgue complete distribution.    We consider probability distributions D on RD which assign probability to all
Lebesgue measurable sets Z ⊂ RD : i.e., Prz∼D [z ∈ Z] is well defined. Note that these distribution do not need
to have density with respect to the Lebesgue measure: indeed, continuous, discrete, and mixture of continuous
and discrete distributions all can be defined to assign probabilities to all Lebesgue-measurable sets.
We say Z ⊂ RD is D-null if Prz∼D [z ∈ Z] = 0. We assume without loss of generality that D is complete, so
that given a D-null Lebesgue measurable set Z , Prz∼D [z ∈ Z 0 ] is well defined and equal to zero for all Z 0 ⊂ Z .
We call distributions which are complete and assign probability to all Lebesgue sets Lebesgue complete. We
shall assume without comment that all distributions are Lebesgue complete.
                                Do Differentiable Simulators Give Better Policy Gradients?

Almost-everywhere functions and expectation.  Given a Lebesgue complete distribution D on RD , we define
                                                0
expectation of a Lebesgue measurable Φ : RD → RD in the standard way.      We say a function Φ is defined
D-almost-surely if there exists a Lebesgue-measurable set Z ⊂ RD such that Φ is a Lebesgue measurable as
                  0
mapping Z → RD , and Z c = RD \ Z is D-null. Given such a function Φ, we define its expectation
                                                                 (
                                                                   Φ(z) z ∈ Z
                     Ez∼D [Φ(z)] := Ez∼D [Φ̃(z)], where Φ̃(z) =                                        (6)
                                                                   0      otherwise.

One can verify that Φ̃(z) is Lebesgue measurable. Note that this definition is independent of the choice of Z : if
Z 0 is another set witnessing the almost-sure definition of Φ, then the induced map Φ̃0 defined by applying Eq (6)
with Z 0 is also Lebesgue measurable, Φ̃0 = Φ̃ D-almost surely, so that the integrals coincide.
Example A.1 (Heaviside, revisited). With definition in Eq (6), we see that the derivative of the example in
Example 3.3 is 0 almost surely under w ∼ p; that is, the event on which the derivative of the Heaviside is both
undefined has probability zero when w ∼ p, and outside this event, its derivative is identically zero.
Stated simply, we ignore values of Φ defined outside the probability-one set Z . This definition has numerous
advantages. For one, it satisfies the law of large numbers. That is,

                                                       i.i.d.     PN
  • If Ez∼D kΦ̃(z)k < ∞, then for z(1) , . . . , z(N ) ∼ D, N1       i=1 Φ(z
                                                                               (i) ) converges to E[Φ(z)] in probability.


  • If Ez∼D kΦ̃(z)k2 < ∞, this convergence holds almost surely.

For further discussion, we direct the readers to a standard reference on probability theory (e.g. (Çinlar, 2011)).


Multivariable derivative.  We provide conditions under which the multivariable function F (θ) : Rd → R is
differentiable. Formally, we say that a function Φ : Rd1 → Rd1 is differentiable at a point z ∈ Rd if there exists
a linear map DΦ(z) ∈ Rd2 ×d1 such that

                                            Φ(h + z) − Φ(z)
                                    lim                     − DΦ(z) · h = 0.
                                   khk→0         khk

The limit is defined in the sense of limkhk→0 (·) = limt→0 supkhk≤t (·). Existence of a multivariable derivative
slightly stronger that Φ(·) having directional derivatives, and in particular, stronger than the existence of a
gradient (see (Rudin et al., 1964, Chapter 9) for reference).


Finite moments and polynomial growth.         To ensure all expectations are defined, we consider distributions for
which all moments are finite.
Definition A.2. We say that a (Lebesgue complete) distribution ρ over a random variable z has finite moments
if Ez∼ρ kzka < ∞ for all a > 0.

The class of function which have finite expectations under distributions with finite moments are functions which
have polynomial growth, in the following sense.
Definition A.3. We say that a function ψ : Rd1 → Rd2 has polynomial growth if there exists constants a, b > 0
such that kψ(x)k ≤ a(1 + kzkb ) for all z ∈ Rd . We say that a matrix (or tensor) valued function has polynomial
growth if the vector-valued function corresponding to flattening its entries into a vector has polynomial growth
(for matrices, this means kψ(z)kF ≤ a(1 + kzkb )).

The following lemma is clear.
                              Do Differentiable Simulators Give Better Policy Gradients?

Lemma A.4. Suppose ρ is a distribution over variables x which has finite moments, and suppose g(x) has
polynomial growth. Then E[g(x)] is well defined.

A second useful (and straightforward to check) fact is that polynomial growth is preserved under marginalization.

Lemma A.5. Suppose ρ is a distribution over variables x which has finite moments, and suppose g(z, x) has
polynomial growth in its argument (z, x). Then z 7→ E[g(z, x)] is well defined and has polynomial growth in z.


Lipschitz functions.  To establish the unbiasedness of the FoBG for non-smooth functions, we invoke the Lip-
                                                                    0
schitz continuity assumption. We say a function Φ : RD → RD is locally-Lipschitz if, for every z ∈ RD ,
there is a neighborhood a neighborhood U of z such that there exists an L > 0 such that for all z0 , z00 ∈ U ,
kΦ(z0 ) − Φ(z00 )k ≤ Lkz0 − z00 k. Locally Lipschitz functions are continuous, and thus Borel measurable.
Lemma A.6 (Rademacher’s Theorem). Every locally Lipschitz function ψ : RD → R is differentiable on a set
of Z ⊂ RD such that Z c = RD \ Z has Lebesgue measure zero.

The above result is standard (see, e.g. Ern & Guermond (2013, Chapter 2)).
To ensure convergence of integrals, we consider functions where the Lipschitz constant grows polynomially in
the radius of the domain.
Definition A.7 (Polynomially Lipschitz). We say that

  • A function ψ(z) : Rd1 → Rd2 is polynomially-Lipschitz if there are constants a, b > 0 such that for all radii
    R ≥ 1 and all z, z0 ∈ Rd1 such that kzk, kz0 k ≤ R, kψ(z) − ψ(z0 )k ≤ aRb .

  • We say a function ψ(z; x) : Rd1 × Rn → Rd2 is parametrized-polynomially-Lipschitz if for all radii R ≥ 1
    and all z, z0 ∈ Rd1 and x ∈ Rn such that kzk, kz0 k, kxk ≤ R, kψ(z; x) − ψ(z0 ; x)k ≤ aRb .

One can check that polynomially Lipschitz functions are locally Lipschitz.


A.2. Formal results

We now state our formal results. Throughout, our smoothing noise w has distribution p which has the following
form.
Assumption A.8. The distribution p admits a density p(w) = eα−ψ(w) , where

(a) ψ(w) ≥ akwk − b for some constants a > 0 and b ∈ R.

(b) ψ is twice differentiable everywhere, and ∇2 ψ(w) has polynomial growth.
Example A.9 (Gaussian distribution). The cannonical example is the Gaussian distribution w ∼ N (0, σ 2 In ),
                                 2
                                                  kwk2
where p(w) = √2πσ 1
                       exp( −kwk
                             2σ 2 ). Here, ψ(w) = 2σ 2 , which has polynomial growth and, being quadratic, is
twice differentiable. In addition,
                                                    w
                                       ∇ψ(w) =         ,   E[∇ψ(w)] = 0.                                      (7)
                                                    σ2

Zeroth-order unbiasedness.     We now stipulate highly general conditions under which the zeroth-order estimator
is unbiased. In the interest of generality, we allow time-varying policies and costs.
                               Do Differentiable Simulators Give Better Policy Gradients?

Definition A.10. We say that a tuple (ρ, p, φ, c1:H ; π1:H ) is a benign planning problem if (a) ρ has finite mo-
ments (b) p satisfies Assumption A.8, (c) the dynamics φ(·, ·) and costs ch (·, ·) have polynomial growth (for all
h ∈ H ), and (d), for each x ∈ Rn and h ∈ [H], u 7→ πh (x, u) is twice-differentiable in u and its second-order
derivative has polynomial growth in x. In addition, we assume φ, c1:H , π1:H are all Borel measurable.

We consider the resulting stochastic optimization objective.

                             F (θ) = Ex1 ∼ρ,w1:H ∼pH [V1 (xh , w1:H , θ)]
                                    s.t. xh+1 = φ(xh , uh ), uh = π(xh , θ) + wh .

Note that we define the expectation jointly over Ex1 ∼ρ,w1:H ∼pH , so as not to assume Fubini’s theorem holds
(even though, under our assumptions, it does). Our first result is a rigorous statement of the unbiasedness of the
zeroth-order estimator.
Proposition A.11. Suppose that (ρ, p, φ, c1:H ; π1:H ) is a benign planning problem. Then, the objective F (θ)
defined in Eq (1) is differentiable, and
                                              "H                                             #
                                               X
                   ∇θ F (θ) = Ex1 ∼ρ,w1:H ∼pH      (Dθ πh (xh , θ))| ψ(wh )Vh (xh , wh:H , θ) .
                                                  h=1

If, in addition Ew∼p [∇ψ(w)] = 0, we also have
                                                                     H
                                            "                                                 #
                                                                     X
                                                                                       |
                   ∇θ F (θ) = Ex1 ∼ρ,w1:H ∼pH     V1 (xh , w1:H , θ)   (Dθ πh (xh , θ)) ψ(wh ) .
                                                                     h=1


Eq (7) yields the following corollary for Gaussian distributions, which recovers Lemma 3.1 in the main text.
Corollary A.12. In the special case where p = N (0, σ 2 I), we have
                                                                   H
                                              "                                         #
                              1                                   X
                                                                                     |
                 ∇θ F (θ) = 2 Ex1 ∼ρ,w1:H ∼pH V1 (xh , w1:H , θ)     (Dθ πh (xh , θ)) wh .
                             σ
                                                                        h=1


First-order unbiasedness under Lipschitzness.  Next, we turn to the formal result under Lipschitzness. We
consider objectives which have the following additional assumptions:
Definition A.13. We say that a tuple (ρ, p, φ, c1:H ; π1:H ) is a benign Lipschitz planning problem if it is a
benign planning problem, and in addition, (a) ch and πh are everywhere-differentiable and their derivatives
have polynomial growth, and (b) φ is polynomially Lipschitz.

In addition, we require one more technical condition which ensures measurability of the set on which the
analytic gradients are defined.
Definition A.14. We say that the distribution ρ is decomposable if there exists a Lebesgue-measurable function
µ : Rn → R≥0 andRa countable setP    of atoms a1 , a2 , . . . , with weights ν1 , ν2 , . . . such that, for any X ⊂ Rn ,
Prx1 ∼ρ [x1 ∈ X ] = X µ(x1 )dx1 + i≥1 ai νi .

More general conditions can be established, but we adopt the above for simplicity. We assume that the distri-
bution over initial state x1 ∼ ρ satisfies decomposability, which in particular encompasses the deterministic
distribution over initial states considered in the body of the paper. The following lemma formalizes Lemma 3.2.

Proposition A.15. Suppose that (ρ, p, φ, c1:H ; π1:H ) is a benign Lipschitz planning problem. If ρ is decompos-
able, then
                                Do Differentiable Simulators Give Better Policy Gradients?

(a) For each θ , there exists a set Lebesgue-measurable set Z                          ⊂      Rn+mH such that
    Prx1 ∼ρ,w1:H ∼pH [(x1 , w1:H ) ∈ Z] = 1 and θ 7→ V1 (x1 , w1:H , θ) is differentiable for all (x1 , w1:H ) ∈ Z .

(b) ∇θ F (θ) = Ex1 ∼ρ,w1:H ∼pH [∇V1 (x1 , w1:H , θ)], where expectations are taken in the sense of Eq (6).

If ρ is not necessarilly decomposable, but for given θ                     ∈ RD , the set {(x1 , w1:H )                   :
V1 (x1 , w1:H , θ) is differentiable} is Lebesgue measureable, then points (a) and (b) still hold.
Example A.16 (Piecewise linear). As an example, piecewise linear, or piecewise-polynomial dynamics statisfy
the conditions of the above proposition.


A.2.1. Separable functions

A key step in establishing the unbiasedness of the zeroth-order estimator for policy optimization is the special
case of separable functions. We begin by stating guarantees for simple functions which the noise enters in the
following separable fashion.
Definition A.17 (Benign separability). We say that a function f (θ, w) has benign separability if there exists an
everywhere differentiable function gin (θ) and a Lebesgue measurable function gout (·) with polynomial growth
such that

                                            f (θ, w) = gout (gin (θ) + w).

A slightly more general version of the above definition is as follows.
Definition A.18. We say that a x-parameterized function function f (θ, w; x) has parametrized benign separa-
bility if there exists Lebesgue-measure functions gout (·; ·) and gin (·; ·) such that gin (·; ·) is differentiable for all
x, and

                                        f (θ, w; x) = gout (gin (θ; x) + w; x),

where (a) (z, x) 7→ gout (z; x) has polynomial growth, (b) for each θ , the mapping x 7→ Dθ gin (θ; x) has
polynomial growth, (z, x) 7→ gout (z; x) has polynomial growth, and (c) for some 0 > 0, there is a function
g̃(x) with polynomial growth such that such that for all ∆ : k∆k ≤ ,

                           kgin (θ; x) − gin (θ + ∆; x) − Dgin (θ; x) · ∆k ≤ k∆k2 g̃(x).                               (8)

We note that Eq (8) is satisfied when gin (θ; x) has a second derivative by having polynomial growth.
The following gives an expression for the derivative of separable functions. Note that we do not require gout (·)
to be differentiable, and depend only on the derivatives of ψ(w) = log p(w)+ const. from the density p, as well
as the derivative of gin (θ). The following statement establishes the well-known (Williams, 1992) computation
at our level of generality.
Proposition A.19. Suppose that p satisfies Assumption A.8. Then, if f (θ, w) is benign separable, then the
expectation F (θ) = Ew∼p [f (θ, w)] is well defined, differentiable, and has

                                   ∇F (θ) = Ew∼p [Dgin (θ)| ∇ψ(w) · f (θ, w)].

More generally, if ρ has finite moments and f (θ, w; x) has benign parametrized separability, then F (θ) =
Ex∼ρ,w∼p [f (θ, w; x)] satisfies

                                ∇F (θ) = Ex∼ρ,w∼p [Dgin (θ)| ∇ψ(w) · f (θ, w; x)].
                              Do Differentiable Simulators Give Better Policy Gradients?

A.3. Proofs

A.3.1. Proof of Proposition A.19

Lemma A.20. Let p be the distribution of w satisfying Assumption A.8 (and, by abuse of notation, its density
with respect to the Lebesgue measure). Then, the following statements are true

(a) The distribution p has finite moments. In particular, for any function g(·) : Rm → Rd with polynomial
    growth, Ew∼p [kg(w)k] < ∞. This only requires Assumption A.8 part (a).

(b) ∇ψ(w) has polynomial growth, and E[∇ψ(w)] = 0.

(c) For any B > 0, there exists a function with polynomial growth such that g̃(·), for all ∆ : k∆k ≤ B ,

                         |p(w) − p(w + ∆) − p(w)h−∇ψ(w), ∆i| ≤ k∆k2 p(w) · g̃(w).


(d) Let g(·, ·) : Rm × Rn → R have polynomial growth. Then x 7→ Ew ∇ψ(w) · g(w, x) is well defined and
    polynomial growth in x.


Proof. Since p(w) decays exponentially in w, p has finite moments. Thus, part (a) follows from Lemma A.4.
Part (b) follows from the fundamental theorem of calculus:
                                   Z 1
                k∇ψ(w)k =                ∇2 ψ(tw) · wdt ≤ k∇ψ(0)k + kwk max k∇2 ψ(tw)kop ,
                                    0                                          t∈[0,1]


the upper bound on which has polynomial growth since k∇2 ψ(tw)kop does.
To prove part (c), we have that since p(w) = eα−ψ(w) for ψ differentiable

                                                 ∇2 p(w) = p(w) · ∇ψ(w)∇ψ(w)| − ∇2 ψ(w) .
                                                                                       
              ∇p(w) = −p(w) · ∇ψ(w),
                                                                 |        {z           }
                                                                                  :=M (w)


Note that, by part (b) and the map that ∇2 ψ(w) has polynomial growth, M (w) has polynomial growth. There-
fore, for any bound B > 0, the function g̃(w) := supk∆k≤B M (w + ∆) has polynomial growth. Finally, by the
intermediate value theorem and for any ∆ : k∆k ≤ B ,

          |p(w) − p(w + ∆) − p(w)h∇ψ(w), ∆i| = |p(w) − p(w + ∆) − h∇p(w), ∆i|
                                                       ≤ k∆k2 p(w)M (w + t∆),              for some t ∈ [0, 1]
                                                               2
                                                       ≤ k∆k p(w)g̃(w),

as needed.
Part (d) is a consequence of part (b) and Lemma A.5.


Proof of Proposition A.19. Consider the non-parametric case. Since gout (·) has polynomial growth, one can
verify that w 7→ f (θ, w) has polynomial growth. Hence the expectation F (θ) is well-defined by Lemma A.20,
                               Do Differentiable Simulators Give Better Policy Gradients?

part (a). We now prove that F (θ) is differentiable. Fix a θ , and let kθ 0 − θk ≤ .
                              Z
                         0
                                  f (θ, w) − f (θ 0 , w) p(w)dw
                                                        
             F (θ) − F (θ ) =
                              Z
                                  gout (gin (θ) + w) − gout (gin (θ 0 ) + w) p(w)dw
                                                                             
                            =
                              Z                                  Z
                            = gout (gin (θ) + w)p(w)dw − gout (gin (θ 0 ) + w) p(w)dw
                                       | {z }                              |    {z      }
                                            w1                                  w2
                              Z                                      Z
                            = gout (w1 )p(w1 − gin (θ))dw1 − gout (w2 )p(w2 − gin (θ 0 ))dw2
                              Z
                                  p(w − gin (θ)) − p(w − gin (θ 0 )) · gout (w)dw
                                                                        
                            =
                              Z
                                  p(w) − p(w + gin (θ) − gin (θ 0 )) · gout (w + gin (θ))dw
                                                                        
                            =
                              Z
                                  p(w) − p(w + gin (θ) − gin (θ 0 )) · f (θ, w)dw
                                                                        
                            =

                                         p(w) − p(w + gin (θ) − gin (θ 0 ))
                                                                                       
                            = Ew∼p                                              · f (θ, w) .
                                                        p(w)
Setting ∆ = gin (θ) − gin (θ 0 ), Lemma A.20 implies that the remainder term enjoyes the following property.
           R(w) := p(w) − p(w + ∆) − p(w)h−∇ψ(w), ∆i satisifies |R(w)| ≤ k∆k2 g̃(w)p(w),
where g̃(w) has polynomial growth, and thus g̃(w) · f (θ, w) integrable under p. Thus, there exists a constant
Cw > 0 such that
                       F (θ) − F (θ 0 ) − Ew∼p [h−∇ψ(w), ∆if (θ, w)] ≤ Cw k∆k2 ,
                                       

where the integral on the right hand side exists because ψ(w) and f (θ, w) have polynomial growth. Simplying
and dividing by kθ − θ 0 k and substituting again∆ = gin (θ) − gin (θ 0 ),
            F (θ) − F (θ 0 ) − gin (θ 0 ) − gin (θ), Ew [∇ψ(w) · f (θ, w)]             kgin (θ 0 ) − gin (θ)k2
                                                                                ≤ Cw                           .        (9)
                                         kθ − θ 0 k                                          kθ − θ 0 k

The result now follows from taking kθ − θ 0 k → 0 and using differentiability of gout (·) concludes.


Parametrized case.  Now consider the parametrized case, and define F (θ; x) = Ew∼p f (θ, w; x). Then the
analogue of Eq (10) holds pointwise for each x:
 F (θ; x) − F (θ 0 ; x) − gin (θ 0 ; x) − gin (θ; x), Ew [∇ψ(w; x) · f (θ, w; x)]            kgin (θ 0 ; x) − gin (θ; x)k2
                                                                                      ≤ Cw                                 .
                                       kθ − θ 0 k                                                       kθ − θ 0 k
                                                                                                                       (10)
Using Eq (8), the triangle inequality and Cauchy Schwartz, we obtain, for some integrable function g̃ with
polynomial growth,
             F (θ; x) − F (θ 0 ; x) − Dgin (θ; x)(θ 0 − θ), Ew [∇ψ(w; x) · f (θ, w; x)]
                                               kθ − θ 0 k
                                                                             kgout (θ 0 ; x) − gout (θ; x)k2
                  ≤ g̃(x) · kθ − θ 0 k · Ew k∇ψ(w) · f (θ, w; x)k + Cw                                       .
                                                                                         kθ − θ 0 k
                                    Do Differentiable Simulators Give Better Policy Gradients?

Applying Eq (8) again, we can bound
                                                                                                                              2
     kgout (θ 0 ; x) − gout (θ; x)k2 =     gout (θ 0 ; x) − gout (θ; x) − kθ − θ 0 k∇θ gout (θ; x) + kθ − θ 0 k∇θ gout (θ; x)
                                                                                                  

                                                                                                                                   2
                                    = 2kθ − θ 0 k2 k∇θ gout (θ; x)k2 + 2 gout (θ 0 ; x) − gout (θ; x) − kθ − θ 0 k∇θ gout (θ; x)
                                    ≤ 2kθ − θ 0 k2 k∇θ gout (θ; x)k2 + 2g̃(x)2 kθ − θ 0 k4 .

Thus,

          F (θ; x) − F (θ 0 ; x) − hDgin (θ; x)(θ 0 − θ), Ew [∇ψ(w; x) · f (θ, w; x)]i
                                             kθ − θ 0 k
              ≤ g̃(x) · kθ − θ 0 k · kEw∼p )∇ψ(w) · f (θ, w; x)k + 2Cw kθ − θ 0 kk∇θ gout (θ; x)k2 + 2Cw g̃(x)2 kθ − θ 0 k3 .

 To conclude, observe that, by assumption, g̃(x), x 7→ ∇θ gout (θ; x), and (by Lemma A.20 part (d)) x 7→
Ew∼p [∇w ψ(w) · f (θ, w; x)] all have polynomial growth. Thus, the fact that ρ has finite moments ensures that
all terms have expectations under x ∼ ρ, and thus,

        Ex∼ρ [F (θ; x) − F (θ 0 ; x)] − Ex∼ρ [hDgin (θ; x)(θ 0 − θ), Ew [∇ψ(w; x) · f (θ, w; x)]i]
                                                kθ − θ 0 k
                   F (θ; x) − F (θ 0 ; x) − hDgin (θ; x)(θ 0 − θ), Ew [∇ψ(w; x) · f (θ, w; x)]i
         ≤ Ex∼ρ
                                                      kθ − θ 0 k
         ≤ Ex∼ρ g̃(x) · kθ − θ 0 k · kEw∼p ∇ψ(w) · f (θ, w; x)k + 2Cw kθ − θ 0 kk∇θ gout (θ; x)k2 + 2Cw g̃(x)2 kθ − θ 0 k3 .
                                                                                                                         


Again, since all expectations are finite, the all terms on the last line above tend to zero as kθ − θ 0 k → 0, so that

                              ∇θ F (θ) = ∇θ (Ex∼ρ [F (θ; x)])
                                       = Ex∼ρ [Dgin (θ; x)| Ew∼p [∇w ψ(w) · f (θ, w; x)]]
                                       = Ex∼ρ,w∼p [∇θ Dgin (θ; x)| ∇w ψ(w) · f (θ, w; x)]

where in the last step, measurability and polynomial-growth conditions allow the application of Fubini’s theo-
rem.


A.3.2. Proof of Proposition A.11

We prove a slightly different proof from that of the standard REINFORCE lemma to accommodate the fact that
the state space is continuous, but the distribution over states may not have a density with respect to the Lebesgue
measure. Instead, we adopt an approach based on the performance difference lemma (Kakade, 2003, Lemma
5.2.1).
To begin, define the expected cost to go function and expected costs

                                             V̄h (xh , θ) = Ew         i.i.d.
                                                                        ∼ p
                                                                                V (xh , wh:H , θ)                                        (a)
                                                                 h:H
                                    +
                                   Vh,θ (θ 0 , wh ; xh ) = V̄h+1 (φ(xh , πh (xh , θ 0 ) + wt ), θ)                                     (b.1)
                                            +
                                          V̄h,θ (θ 0 ; xh ) = Ewh ∼p Vh+ (θ 0 , wh ; xh , θ).                                          (b.2)
                                         ch (θ, wh ; xh ) = ch (xh , πh (xh , θ) + wt ),                                               (c.1)
                                              c̄h (θ; xh ) = Ewh ∼p ch (θ, wh ; xh )                                                   (c.2)

which describe (a) the expected cost-to-go under xh , θ , and (b) the expected cost-to-go from the next stage h
after starting in state xh , acting according to θ 0 in stage h, and subsequently acting according to θ , and (c)
                                    Do Differentiable Simulators Give Better Policy Gradients?

expected cost in state xh under policy θ and. By the well known performance-difference lemma, we have

 F (θ) − F (θ 0 )                                                                                                            (11)
 = Ex1 ∼ρ V̄1 (x1 , θ) − V̄1 (x1 , θ 0 )
                                       

      H
      X                                            +                                
  =         Eθ;h [ c̄h (θ; xh ) − c̄h (θ 0 ; xh ) + V̄h,θ              +
                                                          (θ; xh ) − V̄h,θ (θ 0 ; xh ) ]
      h=1
      XH
  =         Eθ;h Ewh ∼p [ch (θ, wh ; xh ) − ch (θ 0 , wh hxh )] + Exh ∼θ;h Ewh ∼p [Vh,θ
                                                                                    +                    +
                                                                                        (θ, wh ; xh ) − Vh,θ (θ 0 , wh ; xh )]
      h=1
    H
    X
  =   (Fh,θ;c (θ) − Fh,θ;c (θ 0 )) + (Fh,θ;V (θ) − Fh,θ;c (θ 0 ))                                                            (12)
      h=1

where Eθ,h denotes expectations over xh under the dynamics

                                   x1 ∼ ρ,      xt+1 = φ(xt , ut ),      ut = π(xt , θ) + wt ,

and where we define

       Fh,θ;c (θ 0 ) := Exh ∼θ;h Ewh ∼p ch (θ 0 , wh ; xh )],     Fh,θ;V (θ 0 ) := Exh ∼θ;h Ewh ∼p Vh,θ
                                                                                                    +
                                                                                                        (θ 0 , wh | xh )].

Hence, if the functions Fh,θ;c (θ 0 ) and Fh,θ;c (θ 0 ) are differentiable at θ 0 = θ for h = 1, 2, . . . , H , Eq (12)
implies
                                               H
                                               X
                                                      ∇θ0 Fh,θ;c (θ 0 ) + ∇θ0 Fh,θ;V (θ 0 )
                                                                                              
                                 ∇θ F (θ) =                                                       θ 0 =θ
                                                                                                           .                 (13)
                                               h=1

We establish differentiability and compute the derivatives by appealing to Proposition A.19. First, we establish
a couple of useful claims.
Claim A.21. The marginal distribution over xh under Eh;θ has all moments.

Proof. Observe that the polynomial growth conditions on the dynamics map φ(·, ·) imply that as a function,
xh = xh (x1 , w1:h−1 ), xh has polynomial growth in xh (x1 , w1:h−1 ). Thus, since the distributions over x1 and
w1:h−1 have all moments, so does the distribution over xh .
Claim A.22. The function θ 7→ ch (θ, wh ; xh ) = ch (xh , π(xh ; θ) + wt ) satisfies benign parametrized separa-
bility.

Proof. Take gout (·; xh ) = ch (xh , ·) and gin = π(xh , θ). Since ch (·, ·) has polynomial growth, the requisite
growth condition on gout (·, ·) holds. The polynomial growth in x of the second-order differentials of θ 7→
πh (x, θ) implies that the first order differential of θ 7→ πh (x, θ) has polynomial growth in x, and that gin also
satisfies Eq (8) by Taylor’s theorem. Hence, gout , gin satisfy the requisite conditions.
                               +
Claim A.23. The function θ 7→ Vh,θ 0
                                     (θ, wh ; xh ) = V̄h+1 (φ(xh , πh (xh , θ 0 ) + wt ), θ 0 ) satisfies benign
parametrized separability.

Proof. Take gout (u; xh ) = V̄h+1 (φ(xh , u), θ 0 ) and gin = πh (xh , θ). As shown in Claim A.22, gin satisifes
the requisite conditions for benign parametrized separability. To conclude, it suffices to show that (u, xh ) 7→
V̄h+1 (φ(xh , u), θ 0 ) has polynomial growth. By Lemma A.5, it suffices to show that

                                      (u, xh , wh+1:H ) 7→ Vh+1 (φ(xh , u), wh+1:H θ 0 )
                                  Do Differentiable Simulators Give Better Policy Gradients?

has polynomial growth. This holds since we have
                                            H
                                            X
      Vh+1 (φ(xh , u), wh+1:H , θ 0 ) =           ci (xi , πh (xi , θ 0 ) + wi ,   s.t. xi+1 = φ(xi , πh (xi , θ 0 )) + wi .
                                          i=h+1

Just as in the proof of Claim A.21, xi , i > 1 have polynomial growth when viewed as functions of wh+1:H ,
xh and u (since the dynamics φ) have polynomial growth. Since ci also have polynomial growth, we conclude
Vh+1 (φ(xh , u), wh+1:H , θ 0 ) must as well.

The above three claims allow us to invoke Proposition A.19, so that

               ∇θ0 Fh,θ;c (θ 0 ) = Exh ∼θ;h Ewh ∼p Dθ0 πh (xh , θ 0 )| ∇ψ(wh )ch (θ 0 , wh ; xh )]
                                                                                                  
                                                  h                                                     i
              ∇θ0 Fh,θ;V (θ 0 ) = Exh ∼θ;h Ewh ∼p Dθ0 πh (xh , θ 0 )| ∇ψ(wh ) · Vh,θ
                                                                                  +
                                                                                        (θ 0 , wh | xh ) .

Therefore, from Eq (13), we conclude
                    H
                    X                    h                                                                i
       ∇θ F (θ) =         Exh ∼θ;h Ewh ∼p Dθ0 πh (xh , θ)| ∇ψ(wh ) ch (θ 0 , wh ; xh ) + Vh,θ
                                                                                          +
                                                                                              (θ, wh | xh ) ] .
                    h=1

                                                                                                         +
Thus, the various polynomial growth conditions imply we can use Fubini’s theorem (and the definition of Vh,θ )
, so that the above is equal to
                      H
                      X
        ∇θ F (θ) =          Ex1 ∼ρ Ew1:H ∼pH [Dθ πh (xh , θ)| ∇ψ(wh ) (ch (xh , uh ) + Vh+1 (xh , wh+1:H , θ))]]
                      h=1
                      XH
                  =         Ex1 ∼ρ Ew1:H ∼pH [Dθ πh (xh , θ)| ∇ψ(wh ) · Vh (xh , wh:H , θ)]]
                      h=1
                                         "H                                                         #
                                          X
                                                                |
                  = Ex1 ∼ρ Ew1:H ∼pH             Dθ πh (xh , θ) ∇ψ(wh ) · Vh (xh , wh:H , θ) .
                                           h=1

This completes the first part of the proof. Next, we simplify in the special case where Ew∼p [∇ψ(w)] = 0.
Observe that the last line of the above display is equal to
                                    "H                                                #
                                      X
                  Ex1 ∼ρ Ew1:H ∼pH        Dθ πh (xh , θ)| ∇ψ(wh ) · V1 (x1 , w1:H , θ)
                                         h=1
                                                  "H                                     h−1
                                                                                                           !#
                                                   X                                     X
                                                                          |
                            − Ex1 ∼ρ Ew1:H ∼pH           Dθ πh (xh , θ) ∇ψ(wh ) ·              ci (xi , ui )       ,
                                                   h=1                                   i=1
                              |                                     {z                                         }
                                                                    (b)


where in the last line, we use that V1 (x1 , w1:H , θ) = h−1
                                                        P
                                                          i=1 ci (xi , ui ) = Vh (xh , w1:H , θ). It suffices to show
term (b) is zero. This follows since, for each i < h, we have

                  Ex1 ∼ρ Ew1:H ∼pH [Dθ πh (xh , θ)| ∇ψ(wh )ci (xi , ui )]
                       = Ex1 ∼ρ Ew1:h−1 ∼ph−1 [Dθ πh (xh , θ)| ci (xi , ui )] · Ewh ∼p [∇ψ(wh )] = 0.

Here, we used that wh is independent of x1 , w1:h−1 , and the assumption that Ewh ∼p [∇ψ(wh )] = 0.
                                Do Differentiable Simulators Give Better Policy Gradients?

A.3.3. Proof of Proposition A.15

First, we establish almost-everywhere differentiability. Let φ̃h denote the transitions under noise w and policy
θ , defined as

                                         φ̃h (x, w, θ) = φ(x, πh (x, θ) + w).

Set Φh to be their composition

                 Φh (x1 , w1:h−1 , θ) = φ̃h−1 (·, wh , θ) ◦ φ̃h−2 (·, wh−1 , θ) ◦ · · · ◦ φ̃1 (x1 , w1 , θ).

Notice that xh = Φh (x1 , w1:h−1 , θ), where xh is generated according to the dynamics xi+1 = φ(xi , πi (xi , θ) +
wi ). We now establish two key claims.
Claim A.24. Fix (x1 , w1:H , θ). If θ 0 7→ Φh (x1 , w1:h−1 , θ 0 ) for all is differentiable at θ 0 = θ for all h ∈ [H],
then θ 0 7→ V1 (x1 , w1:H , θ 0 ) is differentiable at θ 0 = θ .

Proof. Defining c̃h (x, θ; w) = ch (x, πh (x, θ) + w), we have
                                                      H
                                                      X
                               V1 (x1 , w1:H , θ) =         c̃h (Φh (x1 , w1:h−1 , θ), θ; wh ).
                                                      h=1

Since both ch (·, ·) and πh (·, ·) are everywhere differentiable (jointly in their arguments), (x, θ) 7→
c̃h (x, θ; w) is everywhere differentiable. Thus, under the assumptions of the claim, the composition θ 0 7→
c̃h (Φh (x1 , w1:h−1 , θ 0 ), θ 0 ; wh ) is differentiable at θ 0 = θ .

The next claim provides a sufficient condition for Claim A.24 to hold.
                                            0
Claim A.25. Fix (x1 , w1:H , θ). Then if w1:h−1                                                  0
                                                   7→ Φh (x1 , w1:h−1 , θ) is differentiable at w1:h−1 = w1:h−1 for
                   0                      0                        0
all h ∈ [H], then θ 7→ Φh (x1 , w1:h−1 , θ ) is differentiable at θ = θ for all h ∈ [H].

Proof. Fix x1 , w1:h−1 . Let δ ∈ Rd denote perturbations of θ . It suffices to show that, for each h = 1, 2, . . . , H ,
the mapping Ψh (δ) := Φh (x1 , w1:h−1 , θ + δ) is differenitable if δ . By induction, it is straightforward to verify
the identity

                       Ψh (δ) := Φh (x1 , w1:h−1 , θ + δ) = Φh (x1 , w1:h−1 + w̃1:h (δ)), θ)                       (14)

where we have defined the noise term w̃1:h−1 (δ) so as to transition from policy θ to policy θ + δ :

                                     w̃i (δ) = πi (Ψi (δ), θ + δ) − πi (Ψi (δ), θ).                                (15)
                                               0
We now argue by induction on little h that if w1:i−1 7→ Φh (x1 , w1:i−1 , θ) for all i ≤ H , then Ψi (δ) is differen-
tiable at δ = 0 for all i ≤ h.
For h = 1, both maps are the constant map Φ1 (·, ·, x1 ) = x1 , so the result holds trivially. Now suppose the
inductive hypothesis holds at some h ≥ 1. Then, since each πi (·, ·) is everywhere differentiable in its arguments,
and since Ψi (δ) is differentiable at δ = 0 for all i ≤ h by inductive hypothesis, w̃i (δ) defined in Eq (15) is
differentiable at δ = 0 for each i ≤ h. Hence, w̃1:h (δ) is differentiable at δ = 0. Now, by assumption
  0
w1:h                   0 , θ) is differentiable at w0
      7→ Φh+1 (x1 , w1:h                            1:h = w1:h . Therefore, at δ = 0, Ψh (δ) is given by the
composition of two maps which are differentiable, and hence is differentiable.

Define the set Wh (x1 ) as the set of w1:H ∈ RmH such that the map w1:H 7→ Φh (x1 , w1:h−1 , θ) is differentiable
(for simplicity, we augmented the T map to be a function of all noises w1:H ). Synthesizing Claims A.24 and A.25,
we see that if w1:H ∈ W̄(x1 ) := H                        0                    0                        0
                                      h=1 Wh (x1 ), then θ 7→ V1 (x1 , w1:H , θ ) is differentiable at θ = θ .
                                     Do Differentiable Simulators Give Better Policy Gradients?

Furthermore, define Zh as the set of (x1 , w1:H ) ∈ Rd+mH such that (x1 , w1:H ) 7→ Φh (x1 , w1:h−1 , θ) is
differentiable. Here, we’ve just added x1 as a nuissance variable, so Claims A.24 and A.25 also imply that, on
Z̄ := H           0                   0                        0
      T
        h=1 h , θ 7→ V1 (x1 , w1:H , θ ) is differentiable at θ = θ .
             Z
We invoke Rademacher’s theorem. Since w1:H 7→ Φh (x1 , w1:h−1 , θ) is given by the composition of locally
Lipschitz maps (note that differentiable maps are locally Lipschitz), Lemma A.6 implies that RmH \ Wh (x1 )
has Lebesgue measure zero for each h, so that RmH \ W̄(x1 ) has Lebesgue measure zero by a union bound for
each fixed x1 . Similarly, Rd+mH \ Z̄ has measure zero.


Proof under decomposability.           Assume ρ is decomposable with atoms a1 , a2 , . . . . Define the set
                                                         \
                                               Z := Z̄ ∩ {ai } × W̄(ai ).
                                                                i≥1

The set Z is Lebesgue measurable because it is the intersection of Lebesgue measurable sets. Moroever,
by the above discussion, θ 7→ V1 (x1 , w1:H , θ) is differentiable everywhere on Z . Lastly, one can ver-
ify by decomposability and the fact that Z̄ and W are the complement of Lebesgue measure-zero sets that
Prx1 ∼ρ,w1:H ∼ρH [(x1 , w1:H ) ∈ Z] = 1. This proves part (a).
To prove part (b), one can use the polynomial Lipschitz conditions to verify that ∇θ V1 (x1 , w1:H , θ), has poly-
nomial growth wherever defined. Hence, its expectation (in the sense of Eq (6)) is well-defined. To prove part
(b), one can verify that, via polynomial-Lipschitzness of the dynamics, policies and costs that the quotients
satisfy
                             V1 (x1 , w1:H , θ) − V1 (x1 , w1:H , θ + δ)
                                                                         ≤ poly(kx1 k, kw1:H k).
                                                 kδk
Hence, the quotients are uniformly integrable, and one can apply the dominate convergence theorem to show
that, for any sequence δ n → 0
                                                                                                           
               F (θ + δ n ) − F (θ)                          V1 (x1 , w1:H , θ) − V1 (x1 , w1:H , θ + δ n )
          lim                       = Ex1 ∼ρ,w1:H ∼p H   lim                                                  .
         n→∞         kδ n k                             n→∞                      kδ n k
By considering δ n = tn v for a direction v ∈ Rd and a sequence tn → 0, one can equate directional derivatives
                                 h∇θ F (θ), vi = Ex1 ∼ρ,w1:H ∼pH [h∇θ V1 (x1 , w1:H , θ), vi].
This proves that3
                                       ∇θ F (θ) = Ex1 ∼ρ,w1:H ∼pH [∇θ V1 (x1 , w1:H , θ)].


Proof under measurability assumption.             Consider the set
                         Z0 := {(x1 , w1:H ) s.t. θ 0 7→ V1 (x1 , w1:H , θ 0 ) is differentiable at θ}
and define its slices
                          Z0 (x1 ) := {w1:H s.t. θ 0 7→ V1 (x1 , w1:H , θ 0 ) is differentiable at θ}.
If we assume that Z0 is Lebesgue measurable, then by Fubini’s theorem,
                                  Pr       [(x1 , w1:H ) ∈ Z0 ] = Ex∼ρ           Pr      [w1:H ∈ Z0 (x1 )].
                            x∼ρ,w1:H ∼pH                                      w1:H ∼pH
   3
     Note that , ∇θ F (θ) is differentiable by Proposition A.11, so we do not make the mistake of using existence of partial derivatives to
imply differentiability.
                                  Do Differentiable Simulators Give Better Policy Gradients?

Notice that, for any given x1 , the above proof under decomposability shows that Z0 (x1 ) ⊇ W̄(x1 ), and thus
the complement of Z0 (x1 ) in RmH has Lebesgue measure zero. Hence Prw1:H ∼pH [w1:H ∈ Z0 (x1 )] = 1, so
that Prx∼ρ,w1:H ∼pH [(x1 , w1:H ) ∈ Z0 ] = 0. This proves part (a). Part (b) follows by the same dominated
convergence argument.




B. Additional Proofs from Section 3

B.1. Proof of Lemma 3.5

Recall that empirical bias means there exists an event E such that kE[z | E] − E[z]k ≥ ∆, and Pr[E] ≥ 1 − β .
Since the target lower bound increases as β decreases, we may assume that Pr[E] = 1 − β with equality (since
choosing a small β so that equality holds gives a larger variance lower bound). We begin


                    ∆ ≤ kE[z | E] − E[z]k
                       = k(1 − β)−1 E[zI{E}] − E[z]k
                       ≤ k(1 − β)−1 E[zI{E}] + (1 − β)−1 E[z]k − kE[z]k · |1 − (1 − β)−1 |
                       ≤ (1 − β)−1 kE[zI{E c }]k − kE[z]k · |1 − (1 − β)−1 |.


Rearranging, we have


                                 kE[zI{E c }]k ≥ ∆0 := max{0, (1 − β)∆ − βkE[z]k}.


And thus, since Pr[E c ] = β ,


                                                                      ∆0
                                                    kE[z | E c ]k ≥      .
                                                                      β


Therefore,


                                             E[kzk2 ] ≥ E[kzk2 I{E c }]
                                                      = Pr[E c ] · E[kzk2 | E c ]
                                                      ≥ Pr[E c ] · kE[z | E c ]k2
                                                             ∆20   ∆20
                                                      ≥β·        =     .
                                                             β2    β
                                          Do Differentiable Simulators Give Better Policy Gradients?

B.2. Proof of Lemma 3.10
                    ˆ [0] estimator with a single sample, and drop the superscript i. We accommodate the general
Let’s consider that ∇
case with x1 ∼ ρ. Since Var[z] ≤ E[kzk2 ] for any random vector z, we have
          "                          "H                     ##                                     H                     2
              1               i
                                      X                > i                1               i
                                                                                                   X         i      > i
    Var          V1 (x 1 , w̄   , θ)    ∇ θ π(x h , θ)  w h    ≤ E   i
                                                                   w̄ ,x1    V1 (x 1 , w̄   , θ) ·   D θ π(x h , θ)  w h
              σ2                                                          σ2
                                  h=1                                                             h=1                   2
                                                                                  H                         2
                                                               B2                 X
                                                              ≤ V4 Ew̄i ,x1             Dθ π(xh , θ)> whi
                                                                σ
                                                                                  h=1                       2
                                                                                                                                   
                                                                              H     H D
                                                               B2             X    X                                                E
                                                              = V4 Ew̄i ,x1             Dθ π(xh1 , θ)> whi 1 , Dθ π(xh2 , θ)> whi 2 
                                                                σ
                                                                             h1 =1 h1 =1

                                                                      H H
                                                                  BV2 X X         hD                                          Ei
                                                              =     4
                                                                          Ew̄i ,x1 Dθ π(xh1 , θ)> whi 1 , Dθ π(xh2 , θ)> whi 2 .
                                                                  σ
                                                                      h1 =1 h1 =1



We claim that Ew̄i ,x1 Dθ π(xh1 , θ)> whi 1 , Dθ π(xh2 , θ)> whi 2 = 0 unless h1 = h2 . Suppose h1 6= h2 . Since
                                                                 
inner products are symmetric, we may assume without loss of genearlity that h1 < h2 . Then, xh2 , xh1 and
wh1 are all functions of x1 and w1:h2 −1 ,whereas w2 is independent of these. Hence, since E[w2 ] = 0, the cross
term vanishes. Thus, we are left with
          "                     "H                     ##       H
         1               i
                                 X                > i       BV2 X             hD
                                                                                               > i                   > i
                                                                                                                          Ei
     Var    V1 (x 1 , w̄   , θ)    ∇ θ π(x h , θ)  w h    ≤       E w̄ i ,x     D θ π(x h , θ)  w h , D θ π(x h , θ)  w h
         σ4                                                 σ4              1
                                    h=1                                h=1
                                                                        H
                                                                B2 X         h                         i
                                                               ≤ V4  Ew̄i ,x1 kDθ π(xh , θ)kop kwhi k2
                                                                 σ
                                                                       h=1
                                                                              H
                                                                B2 B 2 X         h       i B2 B 2           HnBV2 Bπ2
                                                               ≤ V 4π    Ew̄i ,x1 kwhi k2 = V 4 π · Hnσ 2 =           ,
                                                                  σ                          σ                σ2
                                                                             h=1

as needed.


C. Interpolation

C.1. Bias and variance of the interpolated estimator

Here we describe the bias and variance of the interpolated estimator. The first is a straightforward consequence
of linearity of expectation and the expectation computations in Eq (4).
Lemma C.1 (Interpolated bias). Assuming the costs and dynamics satisfies the conditions of Lemma 3.1 (for-
mally, Corollary A.12), then for all α ∈ [0, 1],
                                                                                  
                               ¯ [α] F (θ)] − ∇F (θ) = α E[∇
                             E[∇                             ¯ [1] F (θ)] − ∇F (θ) .

If in addition, the costs and dynamics satisfy the conditions of Lemma 3.2 (formally, Proposition A.15), then
E[∇ ¯ [α] F (θ)] = ∇F (θ).
Lemma C.2 (Interpolated variance). Assume that ∇    ¯ [1] F (θ) and ∇
                                                                    ¯ [0] F (θ) are constructed using two indepen-
dent sets of N trajectories. Then We have that
                                   ¯ [α] F (θ)] = α2 Var[∇
                               Var[∇                     ¯ [1] F (θ)] + (1 − α)2 Var[∇
                                                                                     ¯ [0] F (θ)]
                                                        α2                            2
                                                               ˆ [0] Fi (θ)] + (1 − α) Var[∇
                                                                                           ˆ [1] Fi (θ)].
                                                    =      Var[∇
                                                        N                         N
                              Do Differentiable Simulators Give Better Policy Gradients?

Proof. Let X = ∇  ¯ [1] F (θ) and Y = ∇
                                      ¯ [1] F (θ). Since the ZoBG and FoBG are assumed to use independent
trajectories, X and Y are independent, and thus

   Var[αX + (1 − α)Y ] = E[kα(X − E[X]) + (1 − α)(Y − E[Y ])k2 ]
                          = α2 EkX − E[X]k2 + (1 − α)2 EkY − E[Y ]k2 + α E[hX − E[X], Y − E[Y ]i]
                                                                         |         {z           }
                                                                                             =0
                               2                     2
                          = α Var[X] + (1 − α) Var[Y ],

                                                                                              ¯ [1] F (θ) and
which establishes the first equality. The second equality follows from decompsing each of X = ∇
Y =∇ ¯ [1] F (θ) as the empirical mean of N i.i.d random variables.


The following lemma justifies using α2 σ̂12 + (1 − α)2 σ̂22 as a proxy for the variance:
                                                           

Lemma C.3 (Empirical variance). For k = 0, 1, we have

                                               1                ¯ [k] ].
                                                 E[σ̂k2 ] = Var[∇
                                               N

Thus,

                                                                          ¯ [α] ].
                                   E[ α2 σ̂12 + (1 − α)2 σ̂22 ] = N · Var[∇
                                                             



Proof. The first part of the lemma follows from a standard unbiasedness computation for a sample variance
(see, e.g. Wasserman (2004, Theorem 3.17) for the scalar case). The second part of the lemma follows from
Lemma C.2.



C.2. Closed-form for interpolation
                                                                   2
Recall Lemma 4.4: With γ = ∞, the optimal α is α∞ := σ2σ+σ
                                                         0
                                                           2 . For finite γ ≥ , Eq (4) is
                                                               1       0


                                               (
                                                α∞       if α∞ B ≤ γ − ε
                                       αγ :=     γ−ε                                                       (16)
                                                  B      otherwise .


Proof. Intuitively, the objective is convex with a linear constraint, so meets its optimality either at the un-
constrained minimum or at the constraint surface. This is implied by complementary slackness of the KKT
conditions, since an optimal α∗ satisfies:

                                        2α∗ σ̂12 + 2(1 − α∗ )σ̂02 + λB = 0
                                                     λ( − γ + α∗ B) = 0,

where the first line is stationarity of the Lagrangian and the second line is complementary slackness. Clearly,
either λ = 0 and the minimum is met at the inverse-weighted solution of the variances, or the constraint is zero
and we have α∗ = (γ − )/B .
                                Do Differentiable Simulators Give Better Policy Gradients?

C.3. Proof of Lemma 4.3

We give a more detailed proof of Lemma 4.3 here.
           ¯ [α] F (θ) − ∇F (θ)k
          k∇
           = kα∇  ¯ [1] F (θ) + (1 − α)∇
                                       ¯ [0] F (θ) − ∇F (θ)k
          = kα∇¯ [1] F (θ) + (1 − α)∇ ¯ [0] F (θ) − α∇F (θ) − (1 − α)∇F (θ)k
          ≤ (1 − α)k∇  ¯ [0] F (θ) − ∇F (θ)k + αk∇  ¯ [1] F (θ) − ∇F (θ)k
                                                                                                         
          ≤ (1 − α)k∇  ¯ [0] F (θ) − ∇F (θ)k + α k∇   ¯ [1] F (θ) − ∇
                                                                    ¯ [0] F (θ)k + k∇
                                                                                    ¯ [0] F (θ) − ∇F (θ)k

          ≤ k∇¯ [0] F (θ) − ∇F (θ)k + αk∇      ¯ [1] F (θ) − ∇
                                                             ¯ [0] F (θ)k
          ≤  + αk∇   ¯ [1] F (θ) − ∇
                                    ¯ [0] F (θ)k
          ≤ γ.


C.4. Empirical Bernstein confidence

Here describe our confidence estimate based on the ZoBG. Recall that that ZoBG is
                      N                                  N
                                                                                "H                #
     ¯ F (θ) =
       [0]         1 X
                         ˆ Fi (θ), where ∇
                           [0]                 ˆ Fi (θ)
                                                 [0]
                                                        X
                                                                 i    i
                                                                                 X
                                                                                               >
     ∇                   ∇                                 V1 (x1 , w1:H , θ) ·    Dθ π(xh , θ) wh .
                  N
                       i=1                                        i=1                        i=1

Our estimate is based on the matrix Bernstein inequality due (see, e.g. (Tropp, 2015)) specified below.
Lemma C.4 (Matrix Bernstein inequality). Let X1 , . . . , XN be N i.i.d random d-dimensional random vectors
with kX1 − E[X1 ]k ≤ R almost surely, and E[kX1 k2 ] ≤ σ 2 . Then,
                                  N
                           "                          #
                                                                            −N t2 /2
                                                                                     
                              1 X
                        Pr           Xi − E[X] ≥ t ≤ (d + 1) exp
                              N                                            σ 2 + Rt/3
                                     i=1

Hence, with probability, for any δ > 0,
                                            s                         
                              N                  2   d+1
                           1 X                 2σ log δ    2R     d + 1
                  Pr            Xi − E[X] ≥             +    log        ≤ 1 − δ.
                          N                        N       3N       δ
                               i=1


As stated, Lemma C.4 does not apply to our setting because (a) the variance of each Xi := ∇   ˆ [0] Fi (θ) is
unknown, and (b) Xi are not uniformly bounded (due to the Gaussian noise whi being unbounded.) We address
point (a) by replacing Var[Xi ] with the following empirical upper bound
                                                 X
                                         σ̄02 :=     ˆ [0] Fi (θ)k2 ≥ σ̂02 .
                                                    k∇
                                                     i

To address point (b), we take R to be some educated guess on the problem using the gradient samples from the
system (e.g. R = maxi k∇  ˆ [0] Fi (θ) − ∇
                                         ¯ [0] F (θ)k). In practice, since the confidence bound  directly scales with
R, and the user needs to set some threshold term γ on  + αB , a guess on the scale of R is already decided
by the user threshold γ . Thus, rather than viewing R as a rigorous absolute bound on the max deviation that
we have to compute, we interpret it as a hyperparameter balancing how much we should be cautious against an
extreme deviation outside the events covered by the variance term. We find that this approach, while not entirely
rigorous, performs well in simulation. The following remark sketches how a rigorous confidence interval could
be derived.
                             Do Differentiable Simulators Give Better Policy Gradients?

Remark C.5. For a statistically rigorous confidence interval, one would have to (a) control the error introduced
by using an empirical estimate of the variance, and (b) control the non-boundedness of the Xi vectors. The first
point could be addressed by generalizing the empirical Bernstein inequality (Maurer & Pontil, 2009) (which
slightly inflates the confidence intervals to accomodate fluctuations in empirical variance) to vector-valued
random variables. Point (b) can be handled by a truncation argument, leveraging the light-tails of Gaussian
vectors. Nevertheless, we find that our naive approach which substitutes in the empirical variance for the true
variance and our choice of R has good performance in simulation, so we do not pursue more complicated
machinery. In fact, we conjecture that a more rigorous concentration bound may be overly conservative and
worse in experiments.
