                                                                 C. R. Mecanique 346 (2018) 247–262



                                                          Contents lists available at ScienceDirect


                                                   Comptes Rendus Mecanique
                                                                     www.sciencedirect.com


The legacy of Jean-Jacques Moreau in mechanics

The Contact Dynamics method: A nonsmooth story
La méthode de la dynamique des contacts, histoire d’une mécanique
non régulière
Frédéric Dubois a,b,∗ , Vincent Acary d , Michel Jean c
a
  LMGC, Univ. Montpellier, CNRS, Montpellier, France
b
  MIST, Univ. Montpellier, CNRS, IRSN, Montpellier, France
c
  Aix-Marseille Université, CNRS, Centrale Marseille, Marseille, France
d
  LJK, INRIA, Université de Grenoble Alpes, Grenoble, France



a r t i c l e           i n f o                           a b s t r a c t

Article history:                                          When velocity jumps are occurring, the dynamics is said to be nonsmooth. For instance, in
Received 20 May 2017                                      collections of contacting rigid bodies, jumps are caused by shocks and dry friction. Without
Accepted after revision 11 October 2017                   compliance at the interface, contact laws are not only non-differentiable in the usual sense
Available online 21 December 2017
                                                          but also multi-valued. Modeling contacting bodies is of interest in order to understand the
                                                          behavior of numerous mechanical systems such as ﬂexible multi-body systems, granular
Keywords:
Nonsmooth dynamics                                        materials or masonry. These granular materials behave puzzlingly either like a solid or a
Shock                                                     ﬂuid and a description in the frame of classical continuous mechanics would be welcome
Coulomb law                                               though far to be satisfactory nowadays. Jean-Jacques Moreau greatly contributed to convex
Contact Dynamics                                          analysis, functions of bounded variations, differential measure theory, sweeping process
Discrete element method                                   theory, deﬁnitive mathematical tools to deal with nonsmooth dynamics. He converted all
                                                          these underlying theoretical ideas into an original nonsmooth implicit numerical method
Mots-clés :                                               called Contact Dynamics (CD); a robust and eﬃcient method to simulate large collections
Dynamique non régulière
                                                          of bodies with frictional contacts and impacts. The CD method offers a very interesting
Chocs
                                                          complementary alternative to the family of smoothed explicit numerical methods, often
Loi de Coulomb
Dynamique des contacts                                    called Distinct Elements Method (DEM). In this paper developments and improvements of
Méthode par éléments discrets                             the CD method are presented together with a critical comparative review of advantages
                                                          and drawbacks of both approaches.
                                                           © 2017 Académie des sciences. Published by Elsevier Masson SAS. This is an open access
                                                                                                                  article under the CC BY-NC-ND license
                                                                                                   (http://creativecommons.org/licenses/by-nc-nd/4.0/).

                                                          r é s u m é

                                                          Lorsque des sauts de vitesse se produisent, la dynamique est dite non régulière. Par
                                                          exemple, dans les collections de solides supposés rigides rentrant en contact, les sauts
                                                          sont causés par les chocs et le frottement sec. L’absence de déformabilité fait que les
                                                          lois de contact sont, non seulement non différentiables au sens usuel, mais aussi multi-
                                                          valuées. Élaborer des modèles de solides en contact est un moyen de comprendre le
                                                          comportement de nombreux systèmes mécaniques tels que les systèmes multi-corps
                                                          ﬂexibles, les matériaux granulaires ou les maçonneries. Les matériaux granulaires se
                                                          comportent de manière étrange, soit comme des solides, soit comme des ﬂuides, et une



    * Corresponding author.
      E-mail addresses: frederic.dubois@umontpellier.fr (F. Dubois), vincent.acary@inria.fr (V. Acary), mjean.recherche@wanadoo.fr (M. Jean).

https://doi.org/10.1016/j.crme.2017.12.009
1631-0721/© 2017 Académie des sciences. Published by Elsevier Masson SAS. This is an open access article under the CC BY-NC-ND license
(http://creativecommons.org/licenses/by-nc-nd/4.0/).
248                                        F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262


                                           description dans le cadre de la mécanique classique des milieux continus, qui serait
                                           souhaitable, est loin d’être encore satisfaisante. Jean-Jacques Moreau a contribué, de façon
                                           fondamentale, à l’analyse convexe, à la théorie des fonctions à variations bornées et
                                           des mesures différentielles ainsi qu’au processus de raﬂe, outils mathématiques décisifs
                                           pour traiter la dynamique non régulière. Il a converti ces idées théoriques sous-jacentes en
                                           une méthode numérique originale appelée Contact Dynamics (CD), qui est une méthode
                                           non régulière implicite et aussi une méthode robuste et eﬃcace pour simuler de larges
                                           collections de solides avec du contact frottant et des impacts. Le méthode CD offre une
                                           alternative très intéressante à la famille de méthodes usuelles régularisées explicites,
                                           comme la méthode des éléments distincts (DEM). Dans cet article, des développements
                                           et des perfectionnements de la méthode CD sont présentés ainsi qu’une étude critique
                                           comparative des avantages et inconvénients des deux approches.
                                             © 2017 Académie des sciences. Published by Elsevier Masson SAS. This is an open access
                                                                                                   article under the CC BY-NC-ND license
                                                                                    (http://creativecommons.org/licenses/by-nc-nd/4.0/).




1. Introduction

    The generic label (DEM) Discrete Elements Methods, also called Distinct Elements Methods, refers to methods that, op-
positely to Finite Elements Methods (FEM) dedicated to the description of media in the frame of continuous mechanics,
consider a sample as an assembly of distinct bodies. Nowadays, such methods are widely used in the numerical modeling
of divided materials and structures. Natural applications concern the simulation of granular materials, suspensions, frac-
tured materials, masonries, rock mass, etc. in domains such as geophysics, mining, chemical engineering, civil engineering,
biomechanics, etc. DEM are also used for their capability to represent the various states of a collection of solids (gas, ﬂuid,
solid) and to represent some phase changes (solid to solids and vice versa) in the spirit of meshless methods [1] or particle
methods [2,3]. But such methods are also applied in multi-body systems such as mechanisms and robotics. Usually, in such
methods, one considers collections of rigid bodies, subject to interaction laws such as frictional contact laws that are steep
laws.
    A number of leading methods are derived from the pioneering work of Cundall [4] actually referred to the generic label
DEM. This work may be considered also as a modiﬁcation of the genuine Molecular Dynamics method as proposed by Allen
and Tidsley [5]. Since such methods are particularly pragmatic, steep frictional contact laws are modeled as nonlinear laws
using some regularization techniques, and explicit time integrators are used to cope with the nonlinear behavior. At the
end, such methodology leads to a set of uncoupled linear equations that can be solved straightforwardly. The name DEM
is commonly referring to those smoothed and explicit methods. The weaknesses of such methods come from their principle:
small time steps are mandatory due to explicit time integrators, the choice of relevant parameters may be tricky, since
they are used to manage several phenomena: contact condition, macroscopic mechanical response, dynamical properties,
etc. In particular, in order to ensure the stability of explicit schemes, it is necessary to introduce some damping, either
generated by the frictional contact laws, either as a numerical trick. There exist also several “conﬁdential” methods such as
Discontinuous Deformation Analysis (DDA) [6,7], or Discrete Fracture Network (DFN) [8]. For a small number of objects, the
classical Finite Element Method (FEM) can also manage contact problems [9].
    Jean-Jacques Moreau introduced the (CD) Contact Dynamics method during the year 1984. It is inspired by a formulation
of unilateral contact, shock laws, Coulomb friction, through Convex Analysis. The contacting laws are thus non differentiable
steep laws. They are managed with an implicit method using a Non-Linear Gauss–Seidel algorithm (NLGS) at each step.
These laws account roughly for the main features of contact and friction and are relevant in multi-bodies collections where
sophisticated laws cannot be exhibited for sure. The method uses large time steps, but each time step is time consuming.
So oppositely to the above smoothed and explicit DEM method, the CD method is a nonsmooth and implicit method. Note
that implicit methods enable to compute correctly equilibrium states, which is not always the case with explicit methods.
The method can also conserve, with a suitable choice of parameters, the total energy of the system in discrete time. In this
paper, we shall discuss the pros and cons of the CD method with respect to classical smoothed DEM.

2. Moreau contribution to Contact Dynamics genesis

    First, it is to be remembered that Jean-Jacques Moreau was earlier concerned with ﬂuid mechanics. He left an original
result concerning the helicity invariant in perfect ﬂuid dynamics (1961) [10].
    Jean-Jacques Moreau was introducing himself as involved in mechanics, claiming that he was using mathematics just
enough for his mechanical purpose. Actually he was the author of highly sophisticated concepts in mathematics mainly in
the ﬁeld of measure theory. He developed deﬁnitely the theory of locally bounded variation functions [11], the proper math-
ematical setting for the nonsmooth dynamics and the sweeping process theory [12–15]. After the works of the pioneers,
H. Minkowski and M.W. Fenchel, he set up Convex Analysis, a theory also developed at the same time by R.T. Rockafellar;
see for instance the numerous references in the famous book [16] to the results of Jean-Jacques Moreau. Convex Analysis
is the proper tool to deal with nonsmooth mechanics i.e. mechanics where the behavior laws are not differentiable in the
                                                      F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                249


usual sense [17–19]. Elastoplasticity mechanics is an example. Another example is the mechanics of frictional collisions
between rigid bodies, a problem where velocity jumps are expected. The ﬁrst-order sweeping process introduced by Jean-
Jacques Moreau, motivated by the quasi-static evolution of elastoplastic systems [20,21], seems to have provided one of the
ﬁrst occurrence of measure differential inclusions in the literature, with the work of M. Schatzman [22]. For the application
to nonsmooth dynamics, the second-order sweeping process is a fundamental tool for the mathematical analysis and the
design of numerical schemes. The formulation of the Signorini condition at the velocity level is crucial in the development
of the CD method. This condition may be viewed as the time derivative of the unilateral constraints. Firstly, it allows one
to get some very good dissipation properties ensuring stability. This lies in the fact that it reduces the index of the asso-
ciated switched differential algebraic equation. In other words, the unilateral constraints is written as a relation between
the velocity and the impulse. In this way, the mechanical power of the system is described in a consistent way. Secondly,
the second-order sweeping process is a direct extension of the Newton impact law, written for the ﬁrst time in a numerical
tractable way. Some authors call it the “Moreau impact law”, since it is really an outstanding contribution of Jean-Jacques
Moreau. For the numerical practice, it also ensures the Newton impact law to be satisﬁed in discrete time. Finally, another
major contribution of Jean-Jacques Moreau is the formulation of frictional impact laws in terms of Convex Analysis, with
equivalent formulations, for instance in terms of differential inclusions, pseudo-potentials of dissipation, and variational
inequalities.
    At the same time, other peoples contributed to the development of the method and its applications. An extension of the
CD method to deformable bodies has been proposed by M. Jean under the name of Nonsmooth Contact Dynamics (NSCD).
He proposed also a template of numerical architecture inspired by the idea of a mechanical scheme as two pairs of spaces
in duality (global variables space, local variables space), see the next section 3. The LMGC901 open-source software has
been developed around this skeleton by Frédéric Dubois et al. and enriched by all kinds of contacting rigid or deformable
objects with a variety of interaction laws.
    Currently the method is still developed by its precursors, but some relevant contributions are noticeable. The theory of
bi-potential has been proposed by Gery de Saxcé. It is in the spirit of Convex Analysis and uses the same kind of frictional
contact laws than the CD method. It comes out with a nice property, the reaction force appearing as the projection of a
linear combination of the reaction with the relative velocity onto Coulomb’s cone [23]. Another way of viewing this method
is that it may come out as a variational inequality over a cone and not a quasi-variational inequality. Glocker [24] has
proposed more sophisticated nonsmooth contact laws, also in the spirit of Convex Analysis, for evolutions where relative
velocities and accelerations have jumps. The results may be quite accurate for multi-bodies systems with few degrees
of freedoms. Brogliato and Acary [25–28] have proposed several improvements either concerning impact laws, enhanced
time-stepping schemes or the extension of the non-smooth framework to new application ﬁelds as electrical circuits. There
are also many methods and algorithms dedicated to quasi-static evolutions. We restrict the present paper to nonsmooth
dynamics.

3. Current appraisal

   We shortly give a hint of how the CD method works. Details may be found in the original papers by Jean-Jacques Moreau
[29–31], M. Jean [32], and in the books [33,34].

3.1. A robust framework

    As explained by Moreau contact problems in dynamics are non-smooth, due to 1/ kinematic unilateral constraints that
introduce nonsmoothness in space, 2/ collisions that are expected to induce velocity jumps, which lead to nonsmoothness
in time, 3/ multi-valued mappings between contact reactions and the contact velocities that introduce nonsmoothness in
the law. Following the spirit of the sweeping process, the dynamical problem is written as a measure differential inclusion;
it allows us to integrate and discretize non-smooth dynamical systems [35,36].

3.1.1. Dynamics of rigid bodies
    In the following the rigid-body motion is governed by a Newton–Euler system of non-smooth equations:
         
             M dv = Fext (t ) dt + dI
                                                                                                                           (1)
             J d = − × J + Mext (t ) dt + dM
where:

     • dv is the differential measure associated with velocity v, considered as a time function of Bounded Variations (BV) and
       d the differential measure of spin  expressed in a frame attached to the body,
     • dt is the Lebesgue measure,
     • M and J represent respectively the mass and the inertia matrices,


 1
      https://git-xen.lmgc.univ-montp2.fr/lmgc90/lmgc90_user.
250                                                            F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262




                                                                                  Fig. 1. Contact frame.


  • Fext (t ) and Mext (t ) are the force and torque resultants due to external loads,
  • dI and dM are the impulse and angular impulse measures due to contact.

Remark 1. From a practical point of view, one writes the Euler equation in a body-ﬁxed frame which makes J diagonal.
However, except in special cases (sphere, cube, etc.), when J and  are collinear, the Euler equation remains non-linear
and depends implicitly on the orientation of objects.

If f is a right continuous locally BV function, the measure of ]t b , t e ] by d f is given by
          
                    d f = f (t e ) − f (t b )                                                                                                  (2)
      ]t b ,t e ]

Recall that every function of bounded variations admits left and right limits: f − and f + . We choose         to identify the BV
function f as its right limit f + . Therefore, velocity and spin can be obtained such that v(t e ) = v(t b ) + ]t ,t ] dv and (t e ) =
                                                                               t                                             b e

(t b ) + ]tb ,te ] d. The position is computed using x(t e ) = x(t b ) + tbe v(t ) dt. The orientation is computed by integrating with
respect to the Lebesgue measure Ṙ = R        ˜ where      ˜ x =  × x.
   In the following, V = {v, } is the generalized velocity, q = {x, R} is the generalized coordinates,                   M̄ = diag(M, J) is the
generalized inertia matrix, F̄ext (t ) = {Fext (t ), Mext (t )}, F̄quad (t ) = {0, − × J} and Ī]tb ,te ] = { ]t ,t ] dI, ]t ,t ] dM} are respec-
                                                                                                                  b e         b e
tively external, quadratic and contact contributions. Finally, the system takes the form:

                                       te                     te
       M̄(V(t e ) − V(t b )) =               F̄ext (t ) dt +         F̄quad (t ) dt + Ī]tb ,te ]                                              (3)
                                       tb                      tb

For simplicity sake the symbol ¯ is omitted in the following. Note that the time derivative of q is not directly related to
the velocity V since Ṙ = R˜ . In the sequel, we shall write q̇ = T (q)V. The expression (3) is no more than a balance of
momentum over the time interval ]t b , t e ]. It is nonlinear due to contact and to Fquad (t ).

3.1.2. Dynamics of deformable bodies
    We mean by deformable bodies, bodies described in the frame of continuous mechanics. When numerical computation
is concerned, those bodies are discretized through some ﬁnite elements techniques, so that the degrees of freedom are
commonly the nodes coordinates. For instance, for a viscoelastic body within the small perturbations assumptions, the
linear governing dynamical equation is:

       M dv + Cv dt + Kx dt = Fext (t ) dt + dI                                                                                                (4)
where x is the coordinate with respect to a reference conﬁguration, C is the viscosity matrix, and K is the stiffness matrix.
In the case of large deformations or nonlinear behavior, one can use an updated Lagrange formulation nesting the linearized
previous approach in Newton–Raphson loops.

3.1.3. Contact kinematics
    Candidates to contact (shortly contacts) labeled α are selected. By candidates to contact is meant a pair of bodies
close enough according to some criteria so that the reaction between those bodies (vanishing or not) has to be computed.
For any candidates to contact α between bodies i and j, one deﬁnes: the gap g α = D (qi , q j ) (the signed distance from
                                              F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                                 251


body i to body j) and the local frame {A, t, n, s}; see Fig. 1. For the sake of simplicity, the contact locus is considered as
punctual. It is the case when strictly convex boundary are meeting. Knowing the nearest points C and A, it follows that
D (qi , q j ) = (xC − xA ) · n. In the case of meshed objects, one has to consider contact elements composed of a node versus a
face of the antagonist discretized boundaries. There are more sophisticated contact elements.
    For a given contact α , obvious kinematic relations allow one to express the relative velocity V α at contact as a function
of the generalized velocities Vi j of contacting bodies i and j:

      V α = Hα , (qi , q j )Vi j                                                                                                   (5)

where Vi j = [Vi , , V j , ] . Obviously, D (·) and Hα , (·) depend on the positions qi and q j of bodies i and j, which are
not known a priori since they are solutions to the problem. Thus computing more accurately Hα , (qi , q j ) is a nonlinear
problem.
   Using duality considerations (equality of power expressed in terms of global or local variables),

        q, V ← Equations of motion →             I

       H ↓                                    ↑H                                                                                   (6)

        g, V        ← Interaction laws →        I
the local contact impulse may be mapped into a generalized impulse:

      Ii j = Hα (qi , q j )I α                                                                                                      (7)

where Hα , (qi , q j ) is the transpose of Hα (qi , q j ) and Ii j = [Ii , , I j , ] . Another important relation relates the normal
component of the relative velocity to the gap,

       ġ α = VNα                                                                                                                   (8)
which means that at the contact α the time derivative of the gap is the normal component of the relative velocity.

3.1.4. Frictional contact laws
    We present here two basic nonsmooth laws that are used in the kernel of the CD method. Other more sophisticated
frictional contact laws may be derived from these seed laws as mentioned later on (section 4.1). Consider for a moment
that the reaction exerted between two contacting bodies at the contact α is a force Rα and V α is the relative velocity.
Rα has components on the local frame RαT , Rαs (the components of the friction force) and RαN . The relative velocity V α
has for components VTα , Vsα (the components of the sliding velocity) and VNα . Actually the relative velocity involved in these laws
is the right velocity V +α , i.e. the velocity just after the considered instant of contact (where a possible velocity discontinuity
occurs, for instance caused by a shock). In order to simplify the writing, we consider the two-dimensional case (we disregard
the s-components, and we omit the symbol α ). The signed distance between the bodies is g (the gap).
    The inelastic shock law reads as,

      if g > 0 then RN = 0                                                                                                          (9)
      if g ⩽ 0 then VN ⩾ 0 RN ⩾ 0 VN RN = 0                                                                                        (10)
The last relation, a complementary relation, implies that, when bodies are touching each other, the right component of the
velocity is separating the bodies (since there is no adhesion), but if the normal component of the reaction is positive (some
pressure is exerted), the normal component of the relative velocity vanishes, which means that the contacting bodies keep
sticking or sliding on each other. Jean-Jacques Moreau has proven that these laws ensures impenetrability between bodies;
see Jean-Jacques Moreau viability lemma [35,37,36].
    The Coulomb law reads as,

      |Rt | ⩽ μRn ∀S such as |S| ⩽ μRn then V t · (S − Rt ) ⩾ 0                                                                    (11)
where μ ⩾ 0 is the friction coeﬃcient.
    Both laws may be written in several equivalent manners in terms of Convex Analysis, for instance using the sub-
differential of the indicatrix function of a proper convex set. The graphs of these laws are shown in Fig. 2. Those are
graphs of multi mappings. Those laws being positively homogeneous, one is inclined to admit that they are still relevant
when Rα is an impulse I α instead of a force. Sometimes, this may be a strong modeling assumption.
    In the case of deformable bodies, a restitution shock law may be irrelevant. Nevertheless, when a deformable body is
numerically modeled, for instance using a ﬁnite element method, the conﬁguration is described by node coordinates acting
as materials points yielding a ﬁnite-dimensional mechanical system. The inelastic shock law is usually adopted. Coulomb’s
law is also relevant for ﬂexible systems.
252                                                F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262




                                                      Fig. 2. Inelastic shock and Coulomb graphs.


3.1.5. Discrete formulation of the dynamical equation
    The time evolution is managed using an arbitrary time step tn+1 = tn + h of length h. Doing so, contact events are all
captured and solved simultaneously during a time step. Integration of velocity (and external forces) during a time step is
performed using a θ -scheme:

                        
                        t n +1

      qn+1 = qn +                T (q)V(τ )dτ = qn + hT (qn+θ )Vn+θ                                                            (12)
                        tn

where qn+θ = θ qn+1 + (1 − θ)qn and Vn+θ = θ Vn+1 + (1 − θ)Vn . In practice, we also perform the integration of the rotation
with an objective algorithm (see, for example, [38]).
   Concerning granular materials, the time step and the spin are usually small,              which makes the quadratic forces small
or negligible. Therefore, this term is either omitted or explicitly integrated ]t ,t ] Fquad (τ )dτ = hFquad (qm , Vn ) with qm =
                                                                                        n n +1
qn + h(1 − γ )Vn , γ ∈ [0, 1]. However, in some situations with large time steps or high spin, it is more relevant to use an
                                                 tn+1
implicit generalized mid-point rule such as t          Fquad (τ ) dτ = hFquad (qn+θ , Vn+θ ).
                                                  n
   The mapping Hα (qi , q j ) is approximated as Hα (qm,i , qm, j ). This is done using an explicit contact frame built with qm , so
that local variables (gap, relative velocity, impulse) are expressed in this frame. When large displacements over a time step
are observed, an implicit choice of the local frame is sometimes required. The formula (8) is discretized in a similar way:

                        
                        t n +1

      gαn +1   = gα +
                 n            V nα (t ) dt = gnα + h(θV αN,n+1 + (1 − θ)V αN,n )                                               (13)
                        tn

Using the mappings between local and global variables (H and H ) and the equation (3), the discrete form of the dynamical
equation comes out as,

      V = V free + W I where: W = H (qm ) M−1 H(qm )                                                                          (14)
where V α represents now the relative velocity at the end of the time step playing the role of the right relative velocity and I α
is the impulse over the time step. The term V free accounts for all known data as given external forces. The matrix W is called
the Delassus matrix. In other contexts and for rigid bodies, it is also called the mass matrix reduced to local variables.

Remark 2. In (6), H may be viewed as an incidence matrix of the graph of all contacts. In other words, it possesses a
non-null block H α , (qi , q j ) if a contact exists between bodies i and j. By construction, for a large collection of bodies, the
matrix H is sparse. Therefore, since M−1 is block diagonal (each block corresponding to a body), the matrix W is also
block sparse and is not assembled in practice.

     In the case of deformable bodies, one shows that using a θ -scheme (or any implicit time integration scheme) leads to
the same numerical dynamical equation than for rigid bodies. Only the mass matrix is modiﬁed to obtain Mθ = M + θ hC +
θ 2 h 2 K.

3.1.6. Discrete formulation of the frictional contact law
    The standard CD discrete frictional contact laws is a discrete formulation of (10), (11), and writes:

      if a contact is forecasted then VNα ⩾ 0 INα ⩾ 0 VNα INα = 0
      |I T | ⩽ μIN ∀S such as |S| ⩽ μIN , then V T · (S − I T ) ⩾ 0
Both laws are summarized as

      law(V α , I α ) = 0                                                                                                      (15)
                                               F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                             253


Remark 3. The proposition “if a contact is forecasted” means that at the considered candidates to contact α , bodies are
suﬃciently close (even more so bodies are numerically interpenetrating each other) according to some approximate explicit
calculation of the gap, so that the inelastic shock law be processed. For instance, we can choose g (qm ) ⩽ 0 for activating the
law. Otherwise, the reaction is null.

   Some laws, such as restitution shock laws [35], adhesive laws with damage [39], viscoelastic contact laws involving the
gap, may be considered as well. The kinematic (8) and its discrete form (13) allows us to write the frictional contact law
under the form law(V α , I α ) = 0 and to keep V α , I α as the main unknowns.

3.1.7. Solving the standard CD system
    The system to be solved is

      V = V free + W I
      ∀α law(V α , I α ) = 0
The adopted formulation has allowed us to exhibit V α , the relative velocity at the end of the time step, and I α , the impulse over
the time step, as main unknowns. The above system is solved using a NLGS method, performing loops (of iterate k) on the
list of all α candidates to contact:
                                       α β I β,k+1 + 
       V α ,k+1 = V αfree +    β<α W                     β>α W
                                                                  α β I β,k + W αα I α ,k+1
                                                                                                                                (16)
       law(V α ,k+1 , I α ,k+1 ) = 0
A particular feature of the CD method is that for a single contact α , assuming provisional values of the local variables
of neighboring candidates to contact (β = α ), the relative velocity and impulse are found straightforwardly, discussing the
intersections of hyperplanes [40].
   The loops are processed as follows:

(1) consider a contact α between two contacting bodies. Assume provisional values of the reactions on these bodies from
    neighboring contacts; those reactions are considered as external forces;
(2) the local-solver gives provisional values of the reaction at the contact α ;
(3) all reactions are updated;
(4) the next contact in the list is processed;
(5) the list of contacts is run over and over until some convergence criteria is satisﬁed.

The convergence criteria uses distances to Signorini–Coulomb graphs. It happens that some laws, such as restitution shock
laws, adhesive laws, viscoelastic contact laws, may be implemented using changes of variables, i.e. the new variables satisfy
Signorini–Coulomb’s laws. It is done by introducing two supplementary steps in the above loop, a change of variables and
the reverse change.

3.2. Some applications

   The CD method has been applied to investigate mechanical systems such as granular materials (rheology [41,42], tribol-
ogy [43,44], industrial process [45,46]), masonry structures [47,48] or rock masses, under quasi-statics or dynamics loads,
natural hazards (earthquake [49], landslide[50]), etc. More recently it was used to model robotics or multibody systems [51,
52]. Jean-Jacques Moreau, himself made 3D investigations into some controversial questions, such as segregation in shaken
granular materials, pression under a heap of granular materials, shear bands in a 3-dimensional oedometric test, and also
buildings made of blocks submitted to ground subsidence or earthquakes, some of these investigations were only privately
published. One can say that a kind of maturity has been reached since the CD method is able to manage objects of any
shape with various mechanical behavior and to take into account interaction laws as complex as necessary. Some examples
are listed below:

  • shape of objects may be described with simple convex primitives (disk, polygon, sphere, polyhedron, etc), compound
    of simple primitives or general triangulated surface convex or not. Contact detection has to be performed for any
    combination of primitives;
  • bulk behavior of objects may be rigid as well as deformable (small or large transformation, using ﬂoating frame of
    reference) by means of the ﬁnite element method;
  • a large set of interaction laws is available, e.g., frictional contact, cohesion (capillarity, damage, brittle fracture, etc.),
    wire, rod, etc.;
  • multiple physics couplings (thermal effects, electrical conductivity, ﬂuid dynamics, ﬂow in porous media etc) are pro-
    gressively taken into account. Physics couplings can be performed at different scales through upscaling/downscaling
    methods.
254                                           F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262




                                     Fig. 3. Packing of a sample made of circles and shape of the grains.




                           Fig. 4. Positions at rest of a collapsed column of grains. Inﬂuence of the objects’ shape.




    A ﬁrst illustration concerns the collapse of a column of grains in a box (see Fig. 3) with a rough foundation. First a
random granulometry of circles is generated. Then, using a geometrical circle packing algorithm, the position of the circles
is computed. Finally, each circle is replaced by a disk, a pentagon (convex polygon), a star (non-convex polygon), or a ﬂake
(compound of rectangles and disks). Objects are considered as rigid. The coeﬃcient of friction between objects is μ = 0.7.
    The positions at rest of samples made of disks, pentagons, stars or ﬂakes are drawn in Fig. 4. Even with a quite high fric-
tion, the sample made of disks behaves like a ﬂuid. Replacing disks by pentagons introduces some torque transmission and
leads to arching and alignment phenomena. Replacing disks by non-convex stars introduces almost the same mechanisms
than before, but it increases also the shear strength. Replacing disks by ﬂakes introduces new bending phenomena due to
tangle.
    The second example concerns the cross section of a retaining wall, 1.5 m high, located in Largentière, France [53]. Fig. 5a
displays the equilibrium conﬁguration and the network of reaction forces arch-buttering the pressure of the ground exerted
on the right-hand side of the wall (reactions are displayed as bold rectangles oriented in the direction of the forces, and
the thicker the stronger). A 5-cm ground subsidence has been simulated as shown in Fig. 5b. The wall moves to a ﬁnal
equilibrium conﬁguration (see Fig. 5c) with “a belly like” facing and typical open joints. The two bond stones contribute to
this precarious equilibrium. When such bond stones are missing, the wall collapses in those circumstances.
                                                  F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                                      255




            Fig. 5. Retaining wall: (a) equilibrium conﬁguration, (b) ultimate ground subsidence, (c) equilibrium after ground subsidence.


4. Smoothed or nonsmooth methods: advantages and drawbacks

4.1. Interaction laws and numerical schemes

   We have already quoted the family of DEM (Distinct Elements Methods). We come back shortly to the advantages and
drawbacks of these methods, since some ideas may be commented from the point of view of both the DEM and the CD
methods.

Choice of unknown variables. In DEM methods, the main unknowns are the positions and the reaction forces at the end of the
time step, while in the CD method, the main unknowns are the relative velocities at the end of the time step and the impulse
reaction over the time step. As we said before, this choice is motivated by the fact that impacts have to be consistently
integrated.

Standard (explicit) schemes for ordinary differential equations requires smooth laws rather than nonsmooth laws require implicit
integration. The DEM uses smoothed explicit schemes, while CD uses nonsmooth implicit schemes. Explicit schemes are
easy to implement and some of them are very sophisticated and up to provide a high accuracy. To be able to write explicit
schemes, the frictional contact laws must be expressed as standard (single-valued) mappings and must be differentiable
enough according to the order of the scheme (reaction force versus gap for unilateral constraints, and friction force versus
sliding velocity for the frictional laws). Those mappings are steep and yield stiff differential equations that are known to
be diﬃcult to integrate, especially for conserving stability and energy. For stability, it is necessary to use small time steps
and some physical or numerical viscosity must be introduced. Furthermore, the fulﬁllment of the dissipation/conservation
properties in discrete time is very diﬃcult to ensure with explicit schemes and highly nonlinear contact models. Symplectic
and geometric integration schemes [54] are not easy to design with switched nonlinear components. By the way, note that
most of the compliant models are of limited differentiability, which prevents the use of higher-order schemes. In practice,
people might use these schemes, but they have to face numerical instability and spurious oscillations. Thus conservative
models are out of reach.
    In the CD method the frictional contact laws are expressed as multi-mapping (shock laws and Coulomb law). The CD
method is purely implicit for the nonsmooth terms. Though the choice of the local frames is usually done explicitly without
loss of accuracy, the main unknowns, relative velocities and impulses, are computed within an implicit integration scheme.
The reactions found at the end of a time step are those satisfying the dynamics, the shock law, and Coulomb’s law during
the time step. It can use large time steps, but each step needs a large number of NLGS iterations. They are many choices,
but the larger the step, the more the number of iterations at each time step. In the CD method, the smooth nonlinearity
(stiffness/damping, etc.) at contact is removed. This avoids stiff systems and we can ensure that the scheme respects some
very important energetic conditions. Stability is then induced by these properties [55]. Note that these conservation and
stability results are not available with a treatment of the contact condition at the position level.

Smooth elastic models or nonsmooth rigid models. It is the place to get rid of a controversial discussion: it is said that shock
laws and Coulomb’s law are not physical because they disregard local deformability; on the other side, it is said that, since
256                                         F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262


local deformability laws are hardly known or measurable, shock laws and Coulomb law account satisfactorily for the main
features of frictional contact laws (unilateral behavior and sliding threshold). This controversial discussion is irrelevant. The
choice is a matter of modeling and of numerical facilities. In any numerical method, the choice of the numerical parameters
must be appropriate so as to ensure a correct modeling. For instance, in the DEM, the local stiffness of the contacting bodies
is considered so as to ensure a moderate interpenetration. This stiffness is thus quite large, which consequently leads to use
quite small time steps in order to secure the stability of explicit numerical schemes. When the local physics is restricted
only to elasticity, waves propagate, which in many applications, in soil mechanics for instance, is of no interest. Looking
for steady states with DEM methods, the local physics should be augmented with viscosity contents, of questionable values.
Anyway, any damping from physical considerations or any numerical trick may do, if properly scaled. Quasi-static and equi-
librium conditions are really diﬃcult to reach with compliant models. The compliant methods often calls for “cosmological
damping”. Although these methods claim a more accurate mechanical modeling, such numerical tricks are not acceptable.
Finally, with a nonlinear compliant model with damping, it is very diﬃcult to get nearly plastic impacts. In other works,
low values of the coeﬃcient of restitution are not reachable. Except for bi-stiffness models and ideal elasto-plastic models,
that are, by the way nonsmooth, it is impossible to get large dissipation rates with smooth compliant contact models (see
[56], for instance).

Velocity level constraints implies interpenetration, but corrections are possible. A possible drawback of the CD method, with re-
spect to the idea of a fully implicit formulation, is the fact that the gap between the contacting bodies needs to be evaluated
explicitly to activate the constraints at the velocity level (see Remark 3). This could be done implicitly, but numerical ex-
periments show that it is not worthwhile. A similar drawback comes from the way the unilateral constraints are modeled.
It is said that when a contact is occurring, the normal component of the relative velocity must be positive after the impact.
This formulation introduced by Jean-Jacques Moreau [57] ensures that the gap remains positive in a continuous time evo-
lution. Nevertheless, in a time stepping integration scheme, this formulation provides approximate gaps and may generate
interpenetrations, sometimes self-restoring. There exist at least three methods to circumvent this issue.

  • Some “viscoelastic device” may be introduced between contacting bodies, device governed by an inelastic shock law and
    Coulomb law, after a convenient change of variables [32–34]. This amounts to introducing some additional terms in the
    Delassus matrix improving the conditioning. The same CD method is thus used to perform numerical computations,
    with large time steps and a number of iterations at each time step less than usual. The oscillator composed of two
    contacting bodies linked by the viscoelastic device is “critical” in the sense that the stiffness and viscosity values are
    such that the free oscillations are damped. In fact, the relevant parameter is the period of oscillations, which is currently
    chosen equal to the time step. The proposed device should be considered as a regularizing artifact rather than a real
    model of the local viscoelasticity as in the DEM. It prevents waves propagation and interpenetrations are self restoring.
    In differential algebraic equations, a usual tool to stabilize the constraints is to introduce a critical harmonic oscillator
    (the “device”) in the joints. This technique is known as the Baumgarte stabilization. This device may be viewed as a
    nontrivial extension of the Baumgarte stabilization technique to unilateral constraints.
  • Another possible solution in the case of inelastic shock law is to impose the satisfaction of the position and velocity
    constraints over two steps, as is has been developed in [32].
  • Finally, a solution to cope with interpenetration is to use a velocity formulation of the non-interpenetration law, but
    introducing an additional constraint at the position level to recover a null value of the gap as proposed by Acary [28]
    or Brüls et al. [52]. This latter method is an adaptation of the well-know Gear–Gupta–Leimkühler technique for the
    stabilization of differential algebraic equations.

Indeterminacy and slow convergence of the NLGS method. Another drawback of the CD method is the slow convergence of
the NLGS algorithm. Actually, the NLGS solver is not to blame and it may be improved as mentioned hereafter. The slow
convergence comes from indeterminacy (plurality of solutions). By indeterminacy we mean, for instance in the case of
a sample at equilibrium, that there is not a unique set of reactions achieving the equilibrium, since there are kinematic
constraints. To ﬁgure out roughly the situation, we may propose the following analogy: when bodies are linked together
by springs, the system has a single equilibrium state (let us say that the system is isostatic). It is the case of the DEM.
It is not the case of the CD method where there are rigid connections between bodies (the system is hyperstatic); it is
a case of global indeterminacy. When two polygonal objects meet, a side of a polygon set onto a side of the other, the
situation is handled choosing two contact loci where “nodal” reactions are exerted. This localization process generates
indeterminacy; it is a case of local indeterminacy. From a mathematical point of view, when indeterminacy occurs, the
mapping H has a kernel that is not reduced to {0}. It is the set of self-equilibrated reactions. For example, for rigid contacts
dim(ker H) ∼ d.o. f .contacts − d.o. f objects . It happens that the algorithm has diﬃculty to select an element in the kernel and
it has no reason to do it, except that the initializing conditions may incline the algorithm to select some value. Concerning
local indeterminacy, one can introduce some ad hoc relationship between contacts to reduce the kinematic constraints [58].
Introducing the viscoelastic device mentioned above theoretically annihilates the indeterminacy, and thus improves the
convergence. Other attempt may be found in [59,60].
    When interested in macroscopic data as the resultant of reactions forces on a wall, the algorithm gives reliable values.
In fact, a distribution of contact forces is selected by the algorithm [61] and it appears that the network of weak reactions
                                             F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                          257


forces is sensitive to the way the algorithm proceeds, while the network of strong reactions forces is rather steady. The
effect of indeterminacy is more acute in monodisperse collections, we mean samples of grains with almost the same radius.
It is also the case in monuments made of blocks, for instance a wall built with the same blocks. The solution yielded by
the algorithm, though mechanically true, may look strange, for instance being quite asymmetric. Scrambling, i.e. changing
at random the order of the contacts in the NLGS iterations improves the look of the selected solution. Using a Jacobi solver
also helps. An eﬃcient solution is to use the viscoelastic device described above. It allows us to select a sensible solution
and it reduces the number of iterations.
    However, the NLGS procedure has also drawbacks. Some of them are related to the internal operation of the method, and
particularly the way information propagates. It may be improved using a relaxation procedure. In some situations, the NLGS
procedure can be replaced by a faster solver [62,63]. Otherwise, parallel computing can help to obtain some reasonable
computation time [64,65].

4.2. Bulk behavior: ﬂoating frame of reference

    For several reasons detailed hereafter, using deformable-bodies instead of rigid ones may offer numerical and modeling
advantages. As previously explained, indeterminacy may slow down the convergence rate of NLGS procedure. Increasing the
number of degrees of freedom of bodies makes H a full-rank matrix. Concerning the shock law, using a Newton restitution
law is questionable [66,67], it is able to mimic effects of wave propagation and dissipation, but only for binary contacts.
Using deformable bodies should overcome partly this issue. In any case, managing multiple impacts remains an open prob-
lem [68,69]. Regarding mechanical analysis, fracture mechanics, upscaling techniques, etc., the computation of a stress or a
deformation ﬁeld in a discrete material is of main interest. The so-called Weber tensor is an approximation of the Cauchy
stress tensor on a gauge [70] for a quasi-static deformation,

                  1  α
                    nc
      < σ >=         l ⊗ Rα                                                                                                (17)
                  V
                   α =1
where V is the volume of the gauge, nc the number of contacts in the gauge, R are the reactions between contacting
bodies, and l are the branch vectors between the center of the gauge and the contact points. There exists several attempts
revisiting this formula [71–73]. However, using such formula on a unique body is questionable due to indeterminacy. In
such situation, using deformable-body models gives naturally access to a stress ﬁeld. Finally, it may be necessary to intro-
duce some structural effects in bodies to catch phenomena such as compression or ﬂexion, waves, etc., where once again
rigid-body models are too rough.
    Modeling collections of deformable-bodies or mixture of deformable bodies and rigid bodies was already done with
CD/NLGS [32,47,74,75,46]. However, due to kinematic non-linearities, such approaches are really CPU time consuming, except
in very particular cases, since bodies are subject to large rotations whatever the deformation.
    The main idea to overcome this issue is to consider the body motion as the sum of a rigid-body motion and a
deformable-body motion relatively to the rigid-body motion. This deformable-body motion is supposed to be suﬃciently
small such that the center of inertia of the body remain the same (small perturbations).
    The present work is inspired by ideas developed in Fraeijs de Veubeke [76], Shabana [77], Acary [47], Felippa [78] or
Koziara [79].
    Motion can be described through:

  • The rigid-body motion of the center of inertia (M c ) which is deﬁned by: generalized coordinates q R = {xc , Rc } , where
    xc is the position and Rc is the orientation matrix of the body and generalized velocity v R = {vc , c } , where vc is the
                                                                         ˜ c.
    translation velocity and c the angular velocity. Note that Ṙc = Rc 
  • A deformable-body displacement/velocity relatively to the rigid-body motion.

   The velocity ﬁeld v splits into a rigid-body velocity vR and a deformable-body one vD as:

      v(x) = vc + c × (x − xc ) +vD (x)                                                                                   (18)
                         
                         vR (x)

Velocity ﬁeld decomposition is based on two mappings:

  • A distribution mapping G which interpolates the rigid-body motion at each point knowing the generalized rigid-body
    velocity: vR (x) = G (x, v R ).
  • A projection mapping L which extracts the generalized rigid-body velocity from any velocity ﬁeld.
    L (G (•)) is identity on the image of G mapping, noted VR .

Operators are chosen to split the velocity vector space V into a direct sum of vector spaces related to pure deformable-body
velocities VD and rigid-body velocities VR . By duality, the forces space F splits into two supplementary spaces FR and FD .
258                                                                 F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262


         V = VR ⊕ VD            <, >         F = FR ⊕ FD
            L ↓↑ G                             G  ↓↑ L                                                                                                     (19)
               VR               <.>                FR
A possible way to build G and L operators is:

        G (x, v R ) = vR (x) = vc + c × (x − xc )                                                                                                           (20)
                                               
                          vc = m−1  ρ v d
         L (v) =                                                                                                                                            (21)
                      c = J−1  ρ (x − xc ) × v d
where:

  • ρ is the density of the solid,
  • m =  ρ (x) d is the total mass; M = m I.
  • J =  (x − xc ) · (x − xc )I − (x − xc ) ⊗ (x − xc )ρ (x)d is the inertia.

      A smooth motion of the body is governed by the momentum conservation law:

        ρ (x, t )v̇(x, t ) = div(σ (x, t )) + ρ (x, t )f v (t ), ∀x ∈ (t )                                                                                  (22)

where f v is the body forces, v̇ the acceleration and σ the stress tensor. Surface forces T are imposed on                                        f , which normal
is N (T = σ · N). Velocities are imposed on v .
   Considering the velocity form introduced in (18), the acceleration v̇ takes the following expression:

                   ˙ c × (x − xc ) + c × (c × (x − xc )) + c × vD + v̇D
        v̇ = v̇c +                                                                                                                                          (23)

In the following, a virtual velocity ﬁeld is considered such that δ v(x) ∈ δ V 0 , with:

        δ V 0 = {δ v(x) = δ vc + δ c × (x − xc ) + δ vD (x), ∀x ∈ (t ) and homogeneous for ﬁxed d.o.f.                                                     (24)

Starting from (22), the principle of virtual power is derived and one recovers a set of three coupled equations:

  • Newton’s equation:
                        
             mv̇c +             ρ (x)v̇D d
                       (t )
                                                                                                                                                           (25)
                       =            ρ (x)f v (t ) d +                 T(x, t ) d
                           (t )                                (t )

  • Euler’s equation:
                                         
              ˙ +  × J +
             J                                ρ (x)(x − xc ) × v̇D (x, t )d
                                       (t )
                                                                                                                                                           (26)
                       =           ρ (x)(x − xc ) × f v (t ) d +                      (x − xc ) × T(x, t ) d
                        (t )                                                   (t )

  • Deformable-part equation:
                                                          
                     ρ (x)v̇D · δ vD d +  ×                       ρ (x)vD (x, t ) · δ vD d
             (t )                                       (t )
                                                                                                                
                                                   =−               σ (x, t ) : ∇δ vD (x, t ) d(x, t ) +               ρ (x)f v (t ) · δ vD d              (27)
                                                        (t )                                                   (t )
                                                       
                                                   +            T(x, t ) · δ vD d
                                                       f (t )
                                                   F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                                             259




       Fig. 6. Bi-axial test, Von Mises stress evolution: (a) hydrostatic compression conﬁguration, (b) vertical compression conﬁguration ε = 4%.


Introducing quantities expressed in the ﬂoating frame: x the position,  the spin vector (c = Rc  ) and vD the de-
formable velocity, one obtains:
      ⎧                                                           
      ⎪
      ⎪mv̇c + Rc (t ) ρ (x )v̇D d = (t ) ρ (x)f v (t ) d + (t ) T(x, t ) d
      ⎪
      ⎪
      ⎪
      ⎪                           
      ⎪    ˙  +  × J  +
        J                                         
      ⎪
      ⎪
      ⎨                             (t ) ρ (x )x × v̇D d =
                                        
                                                                  
      ⎪              (t ) ρ (x )x × Rc f v (t )d + (t ) x × Rc T(x, t ) d                                                                         (28)
      ⎪
      ⎪                                                                  
      ⎪
      ⎪                                                                     
      ⎪
      ⎪
      ⎪  (t ) ρ (x )v̇D · δ vD d + 2 × (t ) ρ (x )vD · δ vD d + (t ) σ : ∇δ vD d =
      ⎪
      ⎩                                         
                                                                            
                     (t ) ρ (x)Rc f v (t ) · δ vD d + (t ) Rc T(x, t ) · δ vD d

In the ﬂoating reference frame, the stiffness matrix is constant. W = (M + h2 θ 2 K )−1 and is computed once for all. One
only have to rotate forces and velocities from the global to the ﬂoating frame. Omitting the deformable-body contribution,
one recovers the classical Newton–Euler formulation. We refer to [80] for additional discussions on this model.

4.3. Example

    Here are presented the results of a bi-axial test (2D) made of 500 deformable disks computed with the ﬂoating frame of
reference method. For the sake of clarity, we have only presented a 2D example, even if the method works also in 3D.
    A set of radii is generated picking randomly in {0.1 m, 0.15 m, 0.2 m}. Each grain is meshed using triangles with the same
reference size (0.025 m). It implies that the boundaries of the grains are no more smooth curves but poly-lines. The me-
chanical parameters are the following: density ρ = 2500 kg/m3 , Young modulus E = 50 GPa and Poisson coeﬃcient ν = 0.3.
First, a hydrostatic pressure of 0.1 MPa is applied through a driven force prescribed on the top and right walls (Fig. 6a).
Then a vertical deformation is applied imposing a velocity on the top wall while the horizontal pressure is maintained to
0.1 MPa (Fig. 6b). The left and down walls are clamped.
    One obtains the stress ﬁeld in the grains; in Fig. 6, the Von Mises stress norm is drawn after the hydrostatic compression
phase (6a) and at the end of the following vertical compression phase (6b). The intensity of the stress is clearly related to
the contact forces. The vertical stress–strain curve is depicted in Fig. 7a. It is compared to the curve obtained with rigid
disks, with rigid meshed objects (omitting the vD contribution) and taking a high value of the Young modulus (E = 1e14 Pa).
Obviously, one observes that the rigid models are not able to catch the elastic part of the behavior. In Fig. 7b, one observes
that, for a given tolerance of the NLGS method, using deformable bodies the contact solver needs less iterations to converge.


5. Conclusion

    Several years ago, Jean-Jacques Moreau built a bridge between theoretical tools of convex analysis and applications thanks
to the CD method. His original works, introducing a rigorous and robust framework, open the way for scientists to tackle
a huge set of problems. Such works are still in progress. The CD method has demonstrated to be a relevant framework for
the numerical treatment of frictional contact problems (including several behaviors such as cohesive or viscoelastic laws),
but also ad hoc laws (bilateral constraint, wire, spring, etc.). Due to its implicit formulation, contact laws are simultaneously
taken into account with dynamics equations. Obviously, set-valued conditions can be managed in an exact form, i.e. without
introducing any regularization. Furthermore, the CD method enjoys very good stability properties due to its implicit time
260                                                   F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262




                          Fig. 7. Bi-axial test: (a) stress–strain curve, (b) NLGS iterations evolution during the compression phase.


integration scheme. However, the uniqueness of the reactions is not guaranteed though the uniqueness of velocities and
displacements is often observed. Since the contact law does not depend on the body shape, managing any shape is a generic
feature of the CD method, which is an advantage considering force laws used in DEM. Several variants of the method were
developed to take into account deformability or to manage parallel computing. Since deformability is taken into account by
body internal degrees of freedom in the CD method, rather than at the contact level in DEM, the roles played by bulk and
contact behaviors can be analyzed. Latest works are related to multiple physics couplings.

Acknowledgements

   We acknowledge P. Alart, L. Daridon, A. Lozovskiy, Y. Monerie, R. Mozul, S. Pagano, F. Radjai, M. Renouf, and P. Taforel for
interesting and motivating discussions on the topics addressed in this paper.

References

 [1] N. Sukumar, B. Moran, T. Belytschko, The natural element method in solid mechanics, Int. J. Numer. Methods Eng. 43 (5) (1998) 839–887.
 [2] L.D. Libersky, A. Petschek, Smooth Particle Hydrodynamics with Strength of Materials, Lecture Notes in Physics, vol. 395, 1990, pp. 248–257.
 [3] L.D. Libersky, A.G. Petschek, T.C. Carney, J.R. Hipp, F.a. Allahdadi, High strain Lagrangian hydrodynamics, 1993.
 [4] P.A. Cundall, O.D.L. Strack, A discrete numerical model for granular assemblies, Géotechnique 29 (1) (1979) 47–65.
 [5] M.P. Allen, D.J. Tildesley, Computer Simulation of Liquids, Oxford University Press, 1987.
 [6] G. Shi, Discontinuous deformation analysis: a new numerical model for the statics and dynamics, Eng. Comput. 9 (1992) 157–168.
 [7] L. Jing, Formulation of discontinuous deformation analysis (DDA) – an implicit discrete element model for block systems, Eng. Geol. 49 (1998) 371–381.
 [8] D. Elmo, S. Rogers, D. Stead, E. Eberhardt, Discrete fracture network approach to characterise rock mass fragmentation and implications for geome-
     chanical upscaling, Min. Technol. 123 (3) (2014) 149–161.
 [9] P. Wriggers, Computational Contact Mechanics, second edition, Springer Verlag, 2006.
[10] J.-J. Moreau, Constantes d’un îlot tourbillonnaire en ﬂuide parfait barotrope, C. R. hebd. Séances Acad. Sci. Paris 252 (1961) 2810–2812.
[11] J.-J. Moreau, Bounded variation in time, in: J.J. Moreau, P.D. Panagiotopoulos, G. Strang (Eds.), Topics in Nonsmooth Mechanics, Birkhäuser, Basel,
     Switzerland, 1988, pp. 1–74.
[12] J.-J. Moreau, Raﬂe par un convexe variable (première partie), exposé no 15, in: Séminaire d’analyse convexe, University of Montpellier, France, 1971,
     p. 43.
[13] J.-J. Moreau, Raﬂe par un convexe variable (deuxième partie) exposé no 3, in: Séminaire d’analyse convexe, University of Montpellier, France, 1972,
     36 p.
[14] J.-J. Moreau, Sur l’évolution d’un système élasto–viscoplastique, C. R. hebd. Séances Acad. Sci. Paris 274 (A–B) (1971) 118–121.
[15] J.-J. Moreau, Evolution problem associated with a moving convex set in a Hilbert space, J. Differ. Equ. 26 (1977) 347–374.
[16] R.T. Rockafellar, Convex Analysis, Princeton University Press, Princeton, NJ, USA, 1970.
[17] J.-J. Moreau, Fonctionnelles convexes, in: Séminaire Jean-Leray, 1966, pp. 1–108.
[18] J.-J. Moreau, Problème d’évolution associé à un convexe mobile d’un espace hilbertien, C. R. hebd. Séances Acad. Sci. Paris 276 (1973) 791–794.
[19] J.-J. Moreau, Sur les mesures différentielles de fonctions vectorielles et certains problèmes d’évolution, C. R. hebd. Séances Acad. Sci. Paris 282 (1976)
     837–840.
[20] J.-J. Moreau, On unilateral constraints, friction and plasticity, in: New Variational Techniques in Mathematical Physics, Edizioni Cremonese, Roma, 1974,
     pp. 175–322.
[21] J.-J. Moreau, Application of convex analysis to the treatment of elastoplastic systems, in: Applications of Methods of Functional Analysis to Problems
     in Mechanics, in: Lecture Notes in Mathematics, vol. 503, Springer, Berlin, Heidelberg, 1976.
[22] M. Schatzman, Un problème hyperbolique du 2e ordre avec contrainte unilatérale : la corde vibrante avec obstacle ponctuel, J. Differ. Equ. 36 (2) (1980)
     295–334.
[23] G. De Saxce, Z.Q. Feng, New inequality and functional for contact with friction: the implicit standard material approach, Mech. Struct. Mach. 19 (3)
     (1991) 301–325.
                                                        F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262                                                   261


[24] C. Glocker, Set-Valued Force Laws: Dynamics of Non-Smooth Systems, Lecture Notes in Applied and Computational Mechanics, vol. 1, Springer Verlag,
     2001.
[25] B. Brogliato, A. Daniilidis, C. Lemaréchal, V. Acary, On the equivalence between complementarity systems, projected systems and differential inclusions,
     Syst. Control Lett. 55 (2006) 45–51.
[26] V. Acary, B. Brogliato, Numerical Methods for Nonsmooth Dynamics. Applications in Mechanics and Electronics, Springer Verlag, 2009.
[27] V. Acary, Higher order event capturing time-stepping schemes for nonsmooth multibody systems with unilateral constraints and impacts, Appl. Numer.
     Math. 62 (10) (2012) 1259–1275.
[28] V. Acary, Projected event-capturing time-stepping schemes for nonsmooth mechanical systems with unilateral contact and Coulomb’s friction, Comput.
     Methods Appl. Mech. Eng. 256 (2013) 224–250.
[29] M. Jean, J.-J. Moreau, Dynamics in the presence of unilateral contacts and dry friction: a numerical approach, in: G. Del Piero, F. Maceri (Eds.), Unilateral
     Problems in Structural Analysis-2, in: CISM Courses and Lectures, vol. 304, 1987, pp. 151–196.
[30] M. Jean, J.-J. Moreau, Unilaterality and dry friction in the dynamics of rigid body collections, in: Proceedings of Contact Mechanics International
     Symposium, 1992, pp. 31–48.
[31] J.-J. Moreau, Modélisation et simulation de matériaux granulaires, in: B. Mohammadi (Ed.), Actes du 35e Congrès national d’analyse numérique, 2–6
     June 2003.
[32] M. Jean, The non-smooth contact dynamics method, Comput. Methods Appl. Mech. Eng. 177 (3–4) (1999) 235–257.
[33] B. Cambou, M. Jean, F. Radjai, Micromechanics of Granular Materials, Iste, Wiley, London, UK, 2009.
[34] F. Radjai, F. Dubois, Discrete Numerical Modeling of Granular Materials, Wiley, ISTE, 2010.
[35] J.-J. Moreau, Unilateral contact and dry friction in ﬁnite freedom dynamics, in: J.-J. Moreau, P.D. Panagiotopoulos (Eds.), Nonsmooth Mechanics and
     Applications, in: CISM Courses and Lectures, vol. 302, Springer Verlag, Wien, New York, 1988, pp. 1–82.
[36] J.-J. Moreau, Numerical aspects of the sweeping process, Comput. Methods Appl. Mech. Eng. 7825 (177) (1999) 329–349.
[37] J.-J. Moreau, Some numerical methods in multibody dynamics: application to granular materials, Eur. J. Mech. A, Solids (4 suppl.) (1994) 93–114.
[38] T.J.R. Hughes, J. Winget, Finite rotation effects in numerical integration of rate constitutive equations arising in large-deformation analysis, Int. J. Numer.
     Methods Eng. 15 (12) (1980) 1862–1867.
[39] M. Jean, V. Acary, Y. Monerie, Non smooth contact dynamics approach of cohesive materials, Philos. Trans. R. Soc. Lond. Ser. A, Math. Phys. Eng. Sci.
     359 (1789) (2001) 2497–2518.
[40] F. Jourdan, P. Alart, M. Jean, A Gauss–Seidel like algorithm to solve frictional contact problems, Comput. Methods Appl. Mech. Eng. 155 (1) (1998)
     31–47.
[41] É. Azéma, F. Radjai, R. Peyroux, G. Saussine, Force transmission in a packing of pentagonal particles, Phys. Rev. E 76 (1) (2007) 011301.
[42] É. Azéma, F. Radjai, F. Dubois, Packings of irregular polyhedral particles: strength, structure, and effects of angularity, Phys. Rev. E 87 (6) (2013) 062203.
[43] M. Renouf, F. Massi, N. Fillot, A. Saulot, Numerical tribology of a dry contact, Tribol. Int. 44 (7) (2011) 834–844.
[44] M. Renouf, H.-P. Cao, V.-H. Nhu, Multiphysical modeling of third-body rheology, Tribol. Int. 44 (4) (2011) 417–425.
[45] G. Saussine, C. Cholet, P-É. Gautier, F. Dubois, C. Bohatier, J.-J. Moreau, Modelling ballast behaviour under dynamic loading. Part 1: A 2D polygonal
     discrete element method approach, Comput. Methods Appl. Mech. Eng. 195 (19–22) (apr 2006) 2841–2859.
[46] P. Taforel, M. Renouf, F. Dubois, C. Voivret, Finite element-discrete element coupling strategies for the modelling of ballast-soil interaction, Int. J.
     Railway Technol. 4 (2) (2015) 73–95.
[47] V. Acary, Contribution à la modélisation mécanique et numérique des édiﬁces maçonnés, PhD thesis, Université Aix-Marseille 2, 2001.
[48] P. Taforel, Apport de la méthode des éléments discrets à la modélisation des maçonneries en contexte sismique: vers une nouvelle approche de la
     vulnérabilité sismique, PhD thesis, Université Montpellier-2, 2013.
[49] A. Raﬁee, M. Vinches, C. Bohatier, Modelling and analysis of the nîmes arena and the arles aqueduct subjected to a seismic loading, using the non-
     smooth contact dynamics method, Eng. Struct. 30 (12) (2008) 3457–3467.
[50] A. Taboada, H. Ginouvez, M. Renouf, P. Azemard, Landsliding generated by thermomechanical interactions between rock columns and wedging blocks:
     study case from the Larzac Plateau (Southern France), in: EPJ Web of Conferences, vol. 140, EDP Sciences, 2017, p. 14012.
[51] C. Duriez, F. Dubois, A. Kheddar, C. Andriot, Realistic haptic rendering of interacting deformable objects in virtual environments, IEEE Trans. Vis.
     Comput. Graph. 12 (2006) 36–47.
[52] O. Brüls, V. Acary, A. Cardona, Simultaneous enforcement of constraints at position and velocity levels in the nonsmooth generalized-alpha scheme,
     Comput. Methods Appl. Mech. Eng. 281 (nov 2014) 131–161.
[53] M. Bagnéris, M. Jean, Constructions en pierres sèches : la vision du mécanicien, in: Pierre sèche: théorie et pratique d’un système de construction
     traditionnel, Eyroles, 2017, chapter 6, isbn 2212673515, 9782212673517.
[54] E. Hairer, Ch. Lubich, G. Wanner, Geometric Numerical Integration. Structure-Preserving Algorithms for Ordinary Differential Equations, second edition,
     Springer, 2006.
[55] V. Acary, Energy conservation and dissipation properties of time-integration methods for nonsmooth elastodynamics with contact, Z. Angew. Math.
     Mech. (Zeitschrift für Angewandte Mathematik und Mechanik) 96 (5) (2016) 585–603.
[56] N.S. Nguyen, B. Brogliato, Multiple Impacts in Dissipative Granular Chains, Lecture Notes in Applied and Computational Mechanics, vol. 72, Springer
     Verlag, 2014, XXII, 234 p., 109 illus.
[57] J.-J. Moreau, Facing the plurality of solutions in nonsmooth mechanics, in: C.C. Baniotopoulos (Ed.), Nonsmooth/Nonconvex Mechanics with Applications
     in Engineering. International Conference in Memoriam of P.D. Panagiotopoulos, vol. 2006, Ziti, Perea, Thessaloniki, 2006, pp. 3–12.
[58] R. Perales, Modélisation du comportement mécanique par éléments discrets des ouvrages maçonnés tridimensionnels. Contribution à la déﬁnition
     d’éléments de contacts surfaciques, PhD thesis, Université de Montpellier-2, France, 2007.
[59] P. Alart, How to overcome indetermination and interpenetration in granular systems via nonsmooth contact dynamics. An exploratory investigation,
     Comput. Methods Appl. Mech. Eng. 270 (2014) 37–56.
[60] P. Alart, M. Renouf, On inconsistency in frictional granular systems, Comput. Part. Mech. (2017) 1–14, https://doi.org/10.1007/s40571-017-0160-9.
[61] F. Radjai, V. Richefeu, Contact dynamics as a nonsmooth discrete element method, Mech. Mater. 41 (6) (2009) 715–728.
[62] M. Renouf, Optimisation numérique et calcul parallèle pour l’étude de milieux divisés bi- et tri-dimensionnels, PhD thesis, Université Montpellier-2,
     France, 2004.
[63] M. Renouf, P. Alart, Conjugate gradient type algorithms for frictional multi-contact problems: applications to granular materials, Comput. Methods
     Appl. Mech. Eng. 194 (18–20) (2005) 2019–2041.
[64] M. Renouf, F. Dubois, P. Alart, A parallel version of the non smooth contact dynamics algorithm applied to the simulation of granular media, J. Comput.
     Appl. Math. 168 (1–2) (jul 2004) 375–382.
[65] V. Visseq, A. Martin, D. Dureisseix, F. Dubois, P. Alart, Distributed nonsmooth contact domain decomposition (NSCDD): algorithmic structure and
     scalability, in: 21th Domain Decomposition International Conference, 2014, pp. 627–636.
[66] C. Glocker, On frictionless impact models in rigid-body systems, Philos. Trans. R. Soc. Ser. A, Math. Phys. Eng. Sci. 359 (2001) 2385–2404.
[67] M. Payr, C. Glocker, C. Bösch, Experimental treatment of multiple – contact – collisions, in: ENOC-2005 Conference, August, 2005, pp. 7–12.
[68] M. Frémond, Rigid bodies collisions, Phys. Lett. A 204 (1) (1995) 33–41.
262                                                  F. Dubois et al. / C. R. Mecanique 346 (2018) 247–262


[69] H. Zhang, B. Brogliato, Multiple impacts with friction in the rocking block, in: Euromech 2011, vol. 2, 2011, pp. 6–7.
[70] J. Weber, Recherches concernant les contraintes intergranulaires dans les milieux pulvérulents, Bull. Liaison Ponts Chauss. 20 (1966) 3–20.
[71] J. Fortin, O. Millet, G. de Saxcé, Construction of an averaged stress tensor for a granular medium, Eur. J. Mech. A, Solids 22 (4) (2003) 567–582.
[72] B. Chetouane, F. Dubois, M. Vinches, C. Bohatier, NSCD discrete element method for modelling masonry structures, Int. J. Numer. Methods Eng. 64 (1)
     (2005) 65–94.
[73] J.-J. Moreau, The stress tensor in granular media and in other mechanical collections, in: B. Cambou, M. Jean, F. Radjai (Eds.), Micromechanics of
     Granular Material, Iste, Wiley, 2009, pp. 51–100.
[74] H.-P. Cao, M. Renouf, F. Dubois, Impact of interaction laws and particle modeling in discrete element simulations, in: AIP Conference Proceedings, 2009,
     pp. 1–4.
[75] H.-P. Cao, M. Renouf, F. Dubois, Y. Berthier, Coupling continuous and discontinuous descriptions to model ﬁrst body deformation in third body ﬂows,
     J. Tribol. 133 (4) (2011) 041601.
[76] B. Fraeijs de Veubeke, The dynamics of ﬂexible bodies, Int. J. Eng. Sci. 14 (3) (1976) 895–913.
[77] A.A. Shabana, R. Schwertassek, Equivalence of the ﬂoating frame of reference approach and ﬁnite element formulations, Int. J. Non-Linear Mech. 33 (3)
     (1998) 417–432.
[78] C.A. Felippa, B. Haugen, A uniﬁed formulation of small-strain corotational ﬁnite elements: I. Theory, Comput. Methods Appl. Mech. Eng. 194 (21–24)
     (jun 2005) 2285–2335.
[79] T. Koziara, L. Kaczmarczyk, B. Nenad, Multibody contact dynamics with corotational ﬁnite elements and rough background mesh, in: International
     Conference on Particle-Based Methods – Fundamentals and Applications, PARTICLES 2011, 2011, pp. 1–12.
[80] A. Lozovskiy, F. Dubois, The method of a ﬂoating frame of reference for non-smooth contact dynamics, Eur. J. Mech. A, Solids 58 (2016) 89–101.
