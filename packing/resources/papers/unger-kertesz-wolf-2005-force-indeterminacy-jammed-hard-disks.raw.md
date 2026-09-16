                                                                             Force indeterminacy in the jammed state of hard disks
                                                                                                               Tamás Unger
                                                             Dept. of Theoretical Physics, Budapest University of Technology and Economics, H-1111 Budapest, Hungary and
                                                                              Institute of Physics, University Duisburg-Essen, D-47048, Duisburg, Germany

                                                                                                              János Kertész
                                                               Dept. of Theoretical Physics, Budapest University of Technology and Economics, H-1111 Budapest, Hungary
arXiv:cond-mat/0403089v3 [cond-mat.soft] 20 Jun 2005




                                                                                                             Dietrich E. Wolf
                                                                             Institute of Physics, University Duisburg-Essen, D-47048, Duisburg, Germany
                                                                                                       (Dated: November 9, 2018)
                                                                       Granular packings of hard discs are investigated by means of contact dynamics which is an appro-
                                                                    priate technique to explore the allowed force-realizations in the space of contact forces. Configura-
                                                                    tions are generated for given values of the friction coefficient, and then an ensemble of equilibrium
                                                                    forces is found for fixed contacts. We study the force fluctuations within this ensemble. In the
                                                                    limit of zero friction the fluctuations vanish in accordance with the isostaticity of the packing. The
                                                                    magnitude of the fluctuations has a non-monotonous friction dependence. The increase for small
                                                                    friction can be attributed to the opening of the angle of the Coulomb cone, while the decrease as
                                                                    friction increases is due to the reduction of connectivity of the contact-network, leading to local,
                                                                    independent clusters of indeterminacy. We discuss the relevance of indeterminacy to packings of
                                                                    deformable particles and to the mechanical response properties.


                                                          Jamming [1] has been in the focus of recent studies            change of the load can cause rearrangements of the parti-
                                                       because it occurs in a great variety of phenomena like            cles [15, 16]. The question arises whether a packing that
                                                       structural and spin glasses, colloidal systems, vehicular         exhibits many possible realizations of equilibrium forces
                                                       traffic and granular media. The characterization of the           becomes more robust against perturbations.
                                                       jammed state is therefore crucial and can perhaps be best            The results of this Letter provide nontrivial informa-
                                                       achieved in granular systems. Many intriguing proper-             tion also for packings of deformable particles: The actual
                                                       ties of granular packings originate from the microscopic          network of contact forces (which is uniquely determined
                                                       force transmission through a contact structure, where             by the elastic deformations) must be contained in the
                                                       non-linearity and disorder are known to be crucial. It            force-ensemble calculated for the same contact geometry
                                                       is an essential but not resolved question how the highly          assuming the particles (in their deformed shape) would
                                                       inhomogeneous force-network influences the macroscopic            be perfectly rigid. Moreover, for a finite system of suffi-
                                                       stress transmission in dense granular media.                      ciently rigid particles the contact geometry can be arbi-
                                                          Since the deformations of the grains are usually much          trarily close to the ideal one obtained for perfect rigidity.
                                                       smaller than their size, a very useful reference system for       Which of the solutions in the force ensemble is realized,
                                                       granular matter is that of rigid (undeformable) particles         depends e.g. on the elasticity of the individual grains.
                                                       [1, 2, 3, 4]. It is known that random packings of frictional      Here we address the question, how strong the restrictions
                                                       rigid disks or spheres exhibit a hyperstatic structure [5,        provided by the force ensemble are.
                                                       6, 7]: the number of the linear equilibrium equations of             Again another but closely related issue is that of hard
                                                       the grains, which relate the unknown contact forces to            particle simulations, where the dynamics is seemingly
                                                       the external load, is too small to determine the contact          ambiguous due to the indeterminacy of forces [13].
                                                       forces uniquely. Therefore many mechanically admissible              The above problems indicate the significance of the
                                                       force-networks are possible in the same packing geometry          force-ensemble, however very little is known about its
                                                       and for the same external load, which define an ensemble          properties. In this Letter some characteristics of the en-
                                                       of force-configurations.                                          semble are revealed, where emphasis is put on the influ-
                                                          This ensemble recently has received much attention             ence of friction.
                                                       [6, 8, 9, 10, 11, 12, 13, 14] due to the idea that some              In the recent literature [9, 10] it was suggested that
                                                       macroscopic properties of jammed granular systems can             all elements in the ensemble of admissible force config-
                                                       be derived based on an ensemble average over the admis-           urations are realized with equal probability. This mi-
                                                       sible force-states [8]. The determination of force distri-        crocanonical approach can be regarded as a restricted
                                                       bution in [9] or Green function in [10] are based on this         version [23] of the Edwards ensemble [1, 2, 3]. In the
                                                       approach.                                                         following we also address the validity of this assumption.
                                                          Another interesting aspect of the force-ensemble is re-           Let us consider n rigid, cohesionless disks. A configu-
                                                       lated to the behavior of the system under external per-           ration of the contact forces {Fi } (where i is the contact
                                                       turbations. Packing structures where contact forces are           index) is called admissible or a solution if two conditions
                                                       unique or strongly restricted appear to be fragile: slight        are fulfilled: the equilibrium and the Coulomb conditions.
                                                                                                                           2

The first one requires force and torque balance at each          to avoid the effect of the straight plates, only the mid-
grain, while the Coulomb condition reads:                        dle part of the static configuration is considered for fur-
                                                                 ther investigation: this is a horizontal slice of height 28R
                     |(Fi )t | ≤ µ (Fi )n                 (1)    throughout the whole width in the bulk away from the
                                                                 plates. We retain the contact forces at the top and bot-
for the normal and tangential force at each contact, where       tom perimeter of the slice as fixed boundary forces, thus
µ is the friction coefficient. For µ > 0 no additional
                                                                 they provide the external load on the system. The plates
condition is needed to exclude tensile forces.                   and the disks outside the slice can be left away.
   Next we show that the solutions form a convex set.
                                                                    After that the exploration of the admissible force-
The space of contact forces F is defined (for fixed con-         solutions follows for this fixed arrangement of disks. We
tact network) as an Nc × d dimensional vector space,
                                                                 start with the force state that appeared at the jam-
where each point represents a force-configuration {Fi }.         ming and perturb all contact forces randomly [24], which
Nc is the number of contacts, and d the space dimen-
                                                                 leads out of equilibrium and violates the Coulomb con-
sion (i.e. each contact force component represents one           dition. This perturbed state serves as the input for the
degree of freedom). Let S be the subset of admissible
                                                                 Gauss-Seidel-like iterative solver of the contact dynam-
states in F under some fixed external forces. For a reg-         ics method. This iterative algorithm lets the forces relax
ular packing of disks S is known to be a convex polyhe-
                                                                 into a consistent state, providing a (possibly) new so-
dron [11] but it is easy to see that convexity is satisfied      lution [6, 18]. The perturbation and relaxation can be
in any case: shape of the particles, disorder, dimension-
                                                                 repeated many times always starting from the last solu-
ality or friction do not matter. Convexity means that
                                                                 tion (a kind of random walk in the force space); in that
if {Fi } and {Fi + ∆Fi } are solutions then {Fi + λ∆Fi }         way it is possible to sample points from S.
is a solution as well for 0 ≤ λ ≤ 1. First, the equi-
                                                                    Based on this collection of force solutions we can assess
librium condition holds: Both given force-configurations         the differences between admissible states and study the
provide equilibrium against the external load, thus their
                                                                 problem of force indeterminacy. The main feature of S
difference {∆Fi } corresponds to zero load and exerts no         that we found in these self-organized structures is that
total force or torque on the particles. Therefore it can be
                                                                 the admissible force-networks are rather similar: The
scaled freely (unrestricted λ) and added to an admissible        pattern of strong force lines changes little from one re-
state, that does not violate the linear equilibrium equa-
                                                                 alization to the other, showing that the contact-network
tions. Second, the Coulomb condition is satisfied simply         imposes strong restrictions on the force-configuration.
because for each contact i the d-dimensional Coulomb
                                                                    For each contact force Fi its variance (δFi )2 is calcu-
“cone” is a convex set and therefore must contain the            lated over the measured realizations. The ratio
component Fi + λ∆Fi , with 0 ≤ λ ≤ 1.
   The solution set S reflects basically the properties of                            η = hδF i/h|F|i                    (2)
the contact-network, therefore when studying S it is cru-
cial what kind of packing structure is considered. In            represents the ensemble fluctuation in S, thus it can be
real processes which lead to jamming, the microscopic            regarded as a measure of ambiguity of the forces. h·i
structure is not prescribed but develops spontaneously           means the average over all contacts. The force ambiguity
up to the point, where further rearrangements against            η has to be distinguished from the degree of indetermi-
outer driving forces are blocked. This self-organized tex-       nacy which refers to the dimension of the affine subspace
ture is an important feature of granular materials [15]          of force configurations solving the equilibrium conditions
which is disregarded in models using, e.g., regular ar-          (without the restrictions due to the Coulomb cones).
rangements [11, 12]. Therefore the packings studied be-             To investigate the effect of friction a new packing
low were constructed with discrete element simulations           is constructed for each value of µ before sampling the
where the particles obeying Newton’s dynamics build up           solutions. The force ambiguity η is plotted in Fig. 1
the contact-network in a compression process. In these           (full circles). Values of η around 10−7 reflect the ac-
jammed configurations we search for various solutions of         curacy level of our calculation and the corresponding
the contact forces and study the influence of friction on        force-configurations can be regarded as identical with
the properties of S.                                             this tolerance. In the zero friction limit the force am-
   A detailed description of our method of con-                  biguity disappears confirming isostaticity of frictionless
structing the packings and exploring admissible force-           packings [7, 19, 20]. For small µ the force ambiguity
configurations can be found in [6], here only a short            grows proportionally with friction, however for larger µ
review is given. With the help of the contact dynam-             it decreases again. The largest ambiguity of the forces
ics algorithm [17, 18] a 2D system of 200 rigid disks is         is found around µ ≈ 0.1. Despite the further opening of
compressed along the vertical axis between two horizon-          the Coulomb angle fluctuations are getting smaller, even
tal plates. Horizontally periodic boundary conditions are        fully determined states are found for strong friction.
applied, gravity is set to zero, disk radii are uniformly dis-      The behavior of η results from two competing effects:
tributed between R and 2R, the horizontal system width           first, increasing friction provides larger freedom locally
is 42R. We wait till the packing jams (relaxes into equi-        for the tangential forces, second, it also stabilizes the
librium) under the constant force of compression. Then,          system in a less dense state [21] causing lower connectiv-
                                                                                                                             3

            1


                                                        4
       0.01


         -4                                             3.5
   η




                                                              z
       10


         -6                                             3                       (a)                             (b)
       10


                                                        2.5       FIG. 2: (Color online) The difference between two admissible
         -8
       10
                -9    -7    -5        -3                          force-networks for (a) µ = 0.1 (b) µ = 0.5. Only normal force
            10       10    10        10    0.1     10
                                                                  differences are indicated with different colors depending on
                                 µ
                                                                  their sign.
FIG. 1: Force ambiguity η (full circles) and average coordi-
nation number z (open circles) as functions of the friction
coefficient µ. For comparison, squares connected by line show     indeterminacy-pattern is indeed a property of the pack-
the η values for a configuration of disks that was constructed    ing texture. Each of the two subgraphs shown in Fig. 2.b
without friction.                                                 is statically indeterminate, carries only one degree of free-
                                                                  dom and cannot be reduced further because the deletion
                                                                  of one particle or one contact would cancel the inter-
ity of the contact-network (open circles in Fig. 1), which        nal indeterminacy. We call such subgraphs elementary
reduces force ambiguity. One can separate the two effects         clusters. They can be regarded as geometric units of in-
by fixing the configuration and letting the Coulomb an-           determinacy.
gle alone influence η: We generated one packing without              If the connectivity is high the formation of elemen-
friction but switched on friction before sampling force-          tary clusters is more probable, which suggest the follow-
configurations. The results obtained this way (squares in         ing picture: For small friction many overlapping elemen-
Fig. 1) provide monotonously increasing fluctuations, as          tary clusters are formed so that two admissible solutions
expected. Compared to the original data (full circles) de-        generically differ throughout the system (Fig. 2.a). As
viations appear only on the right side of the figure, where       Nc is reduced the density of the elementary clusters ρ
the changes in the connectivity become important, while           decreases and the indeterminacy gets localized into small
the behavior on the left side is governed by the first ef-        separated domains. Around µ = 1 the density ρ becomes
fect. For small µ the average coordination number of the          so small that only a few elementary clusters are present
configuration is essentially the same as in the friction-         due to the finite system size. This explains the strong
less case, where from isostaticity Nc ≈ 2n follows. This          scattering of the data for η in Fig. 1.
gives us the degree of indeterminacy: 2Nc − 3n ≈ Nc /2,              The spatial localization raises the question of a per-
since there are two unknown force components per con-             colation transition. In case of small ρ the separated
tact and three equations per disk due to force and torque         domains carry force-fluctuations independently of each
balance. Thus we conclude that for tiny friction there is         other, therefore we think that η becomes a well defined
a small but high-dimensional set of force-solutions in the        intensive quantity for large systems. However if the inde-
2Nc dimensional force-space, and its size goes to zero            terminacy percolates through the system the overlapping
with vanishing friction. Similarly for spheres in three di-       elementary clusters provide fluctuating boundary forces
mensions one obtains an Nc -dimensional solution set S            for each other, thus the indeterminacy of forces is en-
within a 3Nc -dimensional force space F .                         hanced with growing system size. Simulations up to 500
   For large µ the dimension of S is strongly reduced due         particles show this size dependence, but it is not clear
to the decreasing number of contacts. In our small system         what happens in the thermodynamic limit.
we found that dim(S) can reach even zero, allowing only              Finally we investigate the dynamically created force-
one single force-configuration. This case corresponds to          configuration {Fi,0 }, which is determined by the con-
the marginal rigidity state found in experiments [22].            struction history. Our findings indicate that this state
   The regression of the degrees of freedom occurs in             is more “central” than typical points in the solution set:
an interesting way: the indeterminacy gets localized in           We generate 20 initial configurations with µ = 0.01 and
space into small subgraphs of the contact-network, which          sample for each of them 100 points randomly in S. Their
are surrounded by determined forces, i.e. a relatively            (vectorial) average is regarded as the center of S. Then
large ambiguity is present but only in a small part of            we measure the Euclidean distances ℓ of the sampled
the system (Fig. 2.b). The pattern of the fluctuation-            points from the center. The histogram of the distances in
bearing contacts can be visualized by plotting the dif-           units of their average ℓ̄ is shown in Fig. 3 together with
ference between any two admissible force-configurations.          the histogram of the distances ℓ0 of the initial, dynam-
We found the same subgraphs as in Fig. 2.b also for               ically generated 20 points from the centers of the cor-
other arrangements of boundary forces, showing that this          responding sets S. The two histograms clearly indicate
                                                                                                                                                 4

                                         3                                          suggest the following physical picture: A contact with
                                                                                    large mobilization of friction (Ft /µFn ≈ 1) is less stable
                                        2.5                                         against perturbations. Near the end of the relaxation
                                                                                    process small collisions “shake” the already established
                                         2                                          contacts reducing the possibility that the contact remains
                      P (ℓ0 ) , P (ℓ)




                                                                                    on the verge of sliding. However, the system comes to
                                        1.5                                         rest finally by the marginal fulfillment of the Coulomb
                                                                                    criterion at some contacts.
                                         1
                                                                                       Our results show a significant difference between dis-
                                        0.5
                                                                                    tributions of the solutions sampled by the random walks
                                                                                    plus relaxation and of those relaxed physically. The uni-
PSfrag replacements
                                         0
                                                                                    formity of the (unbiased) random walk based sampling
                                              0   0.5         1         1.5   2     cannot be proved due to the high dimensionality of the
                                                        ℓ0 /ℓ̄ , ℓ/ℓ̄               problem, however, the distance distribution of the points
                                                                                    should be rather robust just because of this high dimen-
                  FIG. 3: Histograms of the distributions of normalized dis-        sionality. Therefore we consider the observed discrepancy
                  tances of dynamically generated (full circles) and randomly       though not as a proof but as a strong indication of the
                  sampled (open circles) points in the sets S for µ = 0.01. The
                                                                                    violation of the microcanonical assumption for the phys-
                  inset shows a two dimensional cross section of a high dimen-
                  sional solution set. The dynamically constructed force state is
                                                                                    ically realized solutions.
                  marked by the arrow. The white area belongs to S, while out-         It is expected that the ambiguity of forces for a given
                  side S the gray scale indicates the violation of the Coulomb      geometry has implications for the mechanical behavior.
                  condition (darker means smaller violation).
                                                                                    We regard the following preliminary result as an indica-
                                                                                    tion of such an effect. For a horizontal layer of hard disks
                                                                                    settled under gravity we applied a point-force downwards
                  that the initial points are closer to the center on aver-         on the free surface, just strong enough to cause local rear-
                  age than the randomly sampled ones. Assuming that the
                                                                                    rangement. We measured the depth of the rearrangement
                  distribution of the random sampling of S is close to a uni-       zone and obtained non-monotonous dependence on µ: It
                  form one, we conclude that the force configurations of the
                                                                                    is larger for small and large friction coefficients, and has a
                  dynamically generated jammed states are not uniformly
                                                                                    minimum at µ ≈ 0.1, right where η reaches its maximum.
                  distributed in the set S.
                     That the original force configuration is “closer to the          This research was partially supported by DFG grant
                  center” is not in contradiction to the fact that we always        SFB 445, BMBF/OM grant HUN 02/011, OTKA
                  find it at the edge of two dimensional cross sections of the      T035028, and the Center for Applied Mathematics and
                  high dimensional solution set S (see inset of Fig. 3). We         Computational Physics of the BUTE.




                   [1] H. A. Makse, J. Brujic, and S. F. Edwards, in The                 of Jyväskylä, Finland, 2004), CD.
                       Physics of Granular Media (Wiley-VCH, 2004), p. 45.          [14] S. McNamara and H. Herrmann, Phys. Rev. E 70, 061303
                   [2] S. F. Edwards and R. B. S. Oakeshott, Physica A 157,              (2004).
                       1080 (1989).                                                 [15] M. E. Cates, J. P. Wittmer, J. P. Bouchaud, and
                   [3] A. Mehta and S. F. Edwards, Physica A 157, 1091                   P. Claudin, Phys. Rev. Lett. 81, 1841 (1998).
                       (1989).                                                      [16] G. Combe and J. N. Roux, Phys. Rev. Lett. 85, 3628
                   [4] F. Radjai, M. Jean, J. Moreau, and S. Roux, Phys. Rev.            (2000).
                       Lett. 77, 274 (1996).                                        [17] M. Jean, Comput. Methods Appl. Mech. Engrg. 177, 235
                   [5] L. E. Silbert, D. Ertas, G. S. Grest, T. C. Halsey, and           (1999).
                       D. Levine, Phys. Rev. E 65, 031304 (2002).                   [18] T. Unger and J. Kertész, in Modeling of Complex Systems
                   [6] T. Unger and J. Kertész, Int. J. of Mod. Phys. B 17,             (AIP, Melville, 2003), p. 116, cond-mat/0211696.
                       5623 (2003).                                                 [19] C. F. Moukarzel, Phys. Rev. Lett. 81, 1634 (1998).
                   [7] J. N. Roux, Phys. Rev. E 61, 6802 (2000).                    [20] A. V. Tkachenko and T. A. Witten, Phys. Rev. E 60,
                   [8] J. P. Bouchaud, in Slow Relaxations and Nonequilibrium            687 (1999).
                       Dynamics in Condensed Matter (Springer, 2003), p. 131.       [21] D. Kadau, G. Bartels, L. Brendel, and D. E. Wolf, Phase
                   [9] J. H. Snoeijer, T. J. H. Vlugt, M. van Hecke, and W. van          Trans. 76, 315 (2003), cond-mat/0206572.
                       Saarloos, Phys. Rev. Lett. 92, 054302 (2004).                [22] R. Blumenfeld, S. F. Edwards, and R. C. Ball (2001),
                  [10] S. Ostojic and D. Panja (2004), cond-mat/0403321.                 cond-mat/0105348.
                  [11] T. Elperin and A. Vikhansky, Physica A 260, 201 (1998).      [23] In Edwards’ thermodynamic theory the ensemble average
                  [12] E. Clement, C. Eloy, J. Rajchenbach, and J. Duran, in             is taken over force- and also over packing-configurations.
                       Stochastic Dynamics (Springer, Berlin, 1998), p. 261.        [24] We add random tangential and normal components to
                  [13] J. J. Moreau, in Proc. of the 4th ECCOMAS (University             the contact forces, which are chosen uniformly from
                                                              5

[−hFn i, hFn i], where hFn i is the average normal force in
the system.
