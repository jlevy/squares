                                                  PHYSICAL REVIEW E 75, 051304 共2007兲


     Underconstrained jammed packings of nonspherical hard particles: Ellipses and ellipsoids

                   Aleksandar Donev,1,2 Robert Connelly,3 Frank H. Stillinger,4 and Salvatore Torquato1,2,4,5,*
            1
             Program in Applied and Computational Mathematics, Princeton University, Princeton New Jersey 08544, USA
                                 2
                                  PRISM, Princeton University, Princeton, New Jersey 08544, USA
                           3
                            Department of Mathematics, Cornell University, Ithaca, New York 14853, USA
                         4
                          Department of Chemistry, Princeton University, Princeton, New Jersey 08544, USA
                 5
                  Princeton Center for Theoretical Physics, Princeton University, Princeton, New Jersey 08544, USA
                                        共Received 16 August 2006; published 10 May 2007兲
                   Continuing on recent computational and experimental work on jammed packings of hard ellipsoids 关Donev
                et al., Science 303, 990 共2004兲兴 we consider jamming in packings of smooth strictly convex nonspherical hard
                particles. We explain why an isocounting conjecture, which states that for large disordered jammed packings
                the average contact number per particle is twice the number of degrees of freedom per particle 共Z̄ = 2d f 兲, does
                not apply to nonspherical particles. We develop first- and second-order conditions for jamming and demon-
                strate that packings of nonspherical particles can be jammed even though they are underconstrained 共hypocon-
                strained, Z̄ ⬍ 2d f 兲. We apply an algorithm using these conditions to computer-generated hypoconstrained ellip-
                soid and ellipse packings and demonstrate that our algorithm does produce jammed packings, even close to the
                sphere point. We also consider packings that are nearly jammed and draw connections to packings of deform-
                able 共but stiff兲 particles. Finally, we consider the jamming conditions for nearly spherical particles and explain
                quantitatively the behavior we observe in the vicinity of the sphere point.

                DOI: 10.1103/PhysRevE.75.051304                                PACS number共s兲: 45.70.⫺n, 05.20.⫺y, 61.20.⫺p


                        I. INTRODUCTION                                    that have been used for hard frictionless spheres would pro-
    Jamming in disordered hard-sphere packings has been                    duce the expectation Z̄ = 2d f , where d f is the number of de-
studied intensely in the last few years 关1–3兴, and recently                grees of freedom per particle 共d f = 2 for disks, d f = 3 for el-
packings of nonspherical particles have been investigated as               lipses, d f = 3 for spheres, d f = 5 for spheroids, and d f = 6 for
well 关4,5兴. Computer simulations and experiments performed                 general ellipsoids兲. Although it has already been noted in
for packings of hard ellipsoids in Ref. 关4兴 showed that asphe-             Ref. 关8兴 that the arguments for isostaticity only rigorously
ricity, as measured by the deviation of the aspect ratio ␣                 apply to perfectly spherical systems, this does not appear to
from unity, dramatically affects the properties of jammed                  be widely appreciated, and there appears to be a wide-spread
packings. In particular, it was observed that for frictionless             expectation that Z̄ ⬇ 2d f for large disordered jammed pack-
particles the packing fraction 共density兲 at jamming ␾J and                 ings of hard frictionless particles. We refer to this expecta-
the average coordination 共contact兲 number per particle Z̄ in-              tion as the isocounting conjecture, since it is based on the
crease sharply from the typical sphere values ␾J ⬇ 0.64 and                expectation that the total number of 共independent兲 con-
                                                                           straints equals the total number of degrees of freedom, that
Z̄ = 6 when moving away from the sphere point ␣ = 1. If one                is, that the packings are isoconstrained. We have referred to
views ␾J and Z̄ as functions of the particle shape, they have              this conjecture in the past as the isostatic conjecture 关4兴;
a cusp 共i.e., they are nondifferentiable兲 minimum at the                   however, here we give a more mathematically precise mean-
sphere point.                                                              ing to the term “isostatic,” as explained in Sec. IV.
    It has been argued in the granular materials literature that               Since d f increases discontinuously with the introduction
large disordered jammed packings of hard frictionless                      of rotational degrees of freedom as one makes the particles
spheres are isostatic 关6–8兴, meaning that the total number of              nonspherical, the isocounting conjecture would predict that Z̄
interparticle contacts 共constraints兲 equals the total number of            would have a jump at ␣ = 1. Such a discontinuity was not
degrees of freedom and that all of the constraints are 共lin-               observed in Ref. 关4兴; rather, it was observed that ellipsoid
early兲 independent. This property implies that the average
number of contacts per particle is equal to the number of                  packings are hypoconstrained, Z̄ ⬍ 2d f near the sphere point,
                                                                           and only become close to being isoconstrained for large as-
degrees of freedom per particle Z̄ = 2d in the limit as the                pect ratios 共but still remain hypoconstrained兲. These findings
number of particles gets large. This prediction has been veri-             support the theoretical predictions in Ref. 关8兴 that, in general,
fied computationally with very high accuracy 关2,3兴. Most of                systems of nonspherical particles would be hypoconstrained
the previous discussions of isostaticity have been restricted              and that the properties of packings should depend mildly on
to systems of spheres 关6,7兴, frictional systems 关9兴, or systems            the exact particle shape.
of deformable particles 关10兴. For a general hard frictionless                  The isocounting conjecture, as expressed by several of
particle shape, the obvious generalization of the arguments                our colleagues, appears to be based on several wrong as-
                                                                           sumptions arising because of the use of linearization in the
                                                                           treatment of the interparticle impenetrability constraints.
 *Electronic address: torquato@electron.princeton.edu                      Reference 关8兴 terms this linearization as the “approximation

1539-3755/2007/75共5兲/051304共32兲                                     051304-1                            ©2007 The American Physical Society
DONEV et al.                                                                               PHYSICAL REVIEW E 75, 051304 共2007兲

of small displacements” 共ASD兲. First, it has been stated that           共iv兲 Study the thermodynamics of packings that are nearly
a hypoconstrained packing cannot be rigid 共jammed兲 due to            jammed and draw connections to packings of deformable
the existence of floppy modes 关10兴, which are unjamming              共but stiff兲 particles.
motions 共mechanisms兲 derived within a linear theory of ri-              共v兲 Develop first-order expansions for nearly spherical
gidity. Additionally, various force-based arguments have             particles and explain quantitatively the behavior we observe
been given 关9兴 without realizing that forces themselves are          in the vicinity of the sphere point.
first-order Lagrange multipliers and do not necessarily exist
when one considers perfectly hard particles outside of the
linear 共first-order兲 approximation. Reference 关8兴 states that               A. Random jammed packings of hard ellipsoids
the ASD approximation is “indispensable if one wishes to                 The packing-generation algorithm we employ generalizes
deal with linear problems … In the case of granular systems,         the Lubachevsky-Stillinger 共LS兲 sphere-packing algorithm
it will also lead to a linearization of the problems, for the        关14兴 and is described in detail in Ref. 关15兴. The method is a
curvature of configuration spaces will be ignored.” The ob-          hard-particle molecular dynamics 共MD兲 algorithm for pro-
servation that terms of order higher than first need to be           ducing dense disordered packings. Initially, small particles
considered is emphasized in Ref. 关8兴: “When floppy modes             are randomly distributed and randomly oriented in a box
exist …, they appear as marginally unstable and one cannot           with periodic boundary conditions and without any overlap.
tell whether, to higher orders, they actually destabilize the        The particles are given velocities 共including angular veloci-
equilibrium configuration.” However, the mathematical                ties兲 and their motion followed as they collide elastically and
analysis extending beyond the ASD is not developed except            also expand uniformly. As the density approaches the jam-
for spheres 关8兴. If the curvature of the particles at the point of   ming density, the collision rate diverges. In the jamming
contact is included in a second-order approximation 共still for       limit, the particles touch to form the contact network of the
infinitesimally small displacements兲, then it can be seen that       packing, exerting compressive forces on each other but not
hypoconstrained packings of nonspherical hard packings can           being able to move despite thermal agitation 共shaking兲. If the
in fact be rigid, jammed, or stable 共these terms are defined in      rate of particle growth, or expansion rate ␥, is initially suffi-
Sec. IV兲. One does not need to consider particle deformabil-         ciently large to suppress crystallization, and small enough
ity, friction, large displacements, or stability under a specific    close to jamming to allow for local relaxation necessary for
applied load such as gravity, in order to see why packings of        true jamming, the final packings are disordered and represen-
nonspherical particles are generally hypoconstrained.                tative of the maximally random jammed 关16兴 共MRJ兲 state
Through the second-order mathematical analysis it will be-           关17兴 共corresponding to the least ordered among all jammed
come clear that preexisting 共internal兲 stresses inside the           packings兲.
packing are essential, as already realized in Ref. 关10兴. While           Note that the computational methodology presented in
this prestress is merely a mathematical tool for static pack-        Ref. 关2兴 applies to ellipsoids as well and we do not repeat the
ings of perfectly hard frictionless particles, for realistic sys-    details presented there. The ellipsoid packings produced by
tems particle deformability, history of preparation, and ap-         the algorithm do not show signs of local or global crystalli-
plied loads all bear a strong influence on the internal stresses     zation. The exact phase diagram for hard ellipsoids is not
in the packing and thus the mechanical properties of the sys-        known and, in particular, it is not known what the high-
tem.                                                                 density crystal phase is 关18兴; however, it is expected that
    In this paper, we generalize our previous theoretical and        nematic ordering is present at high densities. The produced
computational investigations of jamming in sphere packings           packings do not show 共global兲 nematic order to within sta-
关2,11兴 to packings of nonspherical particles and, in particular,     tistical accuracy 关4,19兴. A more detailed analysis of the local
packings of hard ellipsoids. We generalize the mathematical          共translational and orientational兲 correlations in truly jammed
theory of rigidity of tensegrity frameworks 关12,13兴 to pack-         ellipsoid packings has not been performed to our knowledge,
ings of nonspherical particles, and demonstrate rigorously           however, based on our experience with spheres we expect
that the computer-generated ellipsoid packings we studied in         our algorithm to supress crystallization under appropriate
Ref. 关4兴 are jammed even very close to the sphere point.             conditions 关2兴. Sphere packings have been observed to have
Armed with this theoretical understanding of jamming, we             a substantial fraction of rattling particles 共⬃2.5% 兲 关2兴, and
also obtain a quantitative understanding of the cusplike be-         such rattlers are also observed in packings of nearly spherical
havior of ␾J and Z̄ around the sphere point. Specifically, we        ellipsoids. However, the fraction of rattlers appear to rapidly
do the following.                                                    decrease as asphericity is increased, so that the majority of
    共i兲 Explain why the isocounting conjecture does not apply        ellipsoid packings we have generated do not have any rattlers
to nonspherical particles.                                           at all. For spheres, the packings produced with the MD al-
    共ii兲 Develop first- and second-order conditions for jam-         gorithm can be very close to the jamming point, so that the
ming, and demonstrate that packings of nonspherical par-             interparticle gaps are close to numerical precision 共⬃10−15兲
ticles can be jammed even though they are hypoconstrained.           关2兴. Similar precision can be achieved for ellipsoids, how-
    共iii兲 Design an algorithm that uses the jamming conditions       ever, this takes at least an order of magnitude more compu-
to test whether computer-generated hypoconstrained ellip-            tational effort 共or even two orders of magnitude for very
soid and ellipse packings are jammed, and demonstrate nu-            aspherical ellipsoids兲. Typically we have jammed the pack-
merically that our algorithm does produce jammed packings,           ings to a reduced pressure p ⬃ 106 − 109, which ensures that
even close to the sphere point.                                      the distance to jamming is on order of 10−9 − 10−6. To really

                                                               051304-2
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                                                         PHYSICAL REVIEW E 75, 051304 共2007兲

     0.74                                                                                      6



     0.72
                                                                                                                              0.9
                                                                                              5.5




                                                                           Contact number Z
                                                                                                                             0.89
      0.7
                                  α                                                                                          0.88




                                                                                                                Density φJ
φJ




                        1         2            3                                               5
                12
     0.68
                                                                                                                             0.87

                10                                                                                                                                                      −5
                                                     β=1 (oblate)                                                            0.86                                γ=10
                Z                                    β=1/4                                    4.5                                                                γ=10
                                                                                                                                                                        −4
     0.66           8                                β=1/2                                                                   0.85                                Theory
                                                     β=3/4
                                                     β=0 (prolate)                                                                  1           1.2              1.4         1.6
                    6                                                                                                                                        α
     0.64
            1               1.5         2            2.5             3                         4
                                                                                                    1    1.25                           1.5           1.75              2          2.25
                                  Aspect ratio α                                                                                        Aspect ratio α
    FIG. 1. 共Color online兲 Jamming density and average contact                 FIG. 2. 共Color online兲 Average contact number and jamming
number 共inset兲 for packings of N = 10 000 ellipsoids with ratios be-       density 共inset兲 for bi-dispersed packings of N = 1000 ellipses with
tween the semi-axes of 1 : ␣␤ : ␣ 共see Fig. 2 in Ref. 关4兴兲. The isocon-    ratios between the semi-axes of 1 : ␣, as produced by the MD algo-
strained contact numbers of 10 and 12 are shown as a reference.            rithm using two different expansion rates ␥ 共affecting the results
                                                                           only slightly兲. The isoconstrained contact number is 6. The results
                                                                           of the leading-order 共in ␣ − 1兲 theory presented in Sec. IX are shown
identify the exact contact network in the jamming limit re-                for comparison.
quires even higher pressures for larger packings due to exis-
tence of a multitude 共more specifically, a power-law diver-                                             B. Nontechnical summary of results
gence兲 of near contacts in disordered packings 关2兴. However,                   In this section, we provide a nontechnical summary our
with reasonable effort the average coordination number Z̄                  theoretical results and observations discussed in the main
can be identified within 1% even for systems of N = 105 el-                body of the paper. This summary is intended to give readers
lipsoids. Those packings for which we perform an exact                     an intuitive feeling for the mathematical formalism devel-
analysis of the contact network 共such as, for example, rigor-              oped in this work and demonstrate the physical meaning and
ously testing for jamming兲 have been prepared carefully and                relevance of our results. We will refer the interested reader to
are sufficiently close to the jamming point to exactly identify            appropriate sections to find additional details.
all of the true contacts.                                                      One aim of this paper is to explain the numerical results
    In Fig. 1 we show newer results than those in Ref. 关4兴 for             presented in Sec. I A. In particular, we will explain why
                                                                           jammed disordered packings of ellipsoids are strongly hypo-
the jamming density ␾J and contact number Z̄ of jammed
                                                                           constrained near the sphere point, and also why, even far
monodispersed packings of hard ellipsoids in three dimen-
                                                                           from the sphere point, ellipsoid packings are hypocon-
sions. The ellipsoid semiaxes have ratios a : b : c = 1 : ␣␤ : ␣
                                                                           strained rather than isoconstrained as are sphere packings.
where ␣ ⬎ 1 is the aspect ratio 共for general particle shapes, ␣            By a “jammed packing” we mean a packing in which any
is the ratio of the radius of the smallest circumscribed to the            motion of the particles, including collective combined trans-
largest inscribed sphere兲, and 0 艋 ␤ 艋 1 is the “oblateness” or            lational and rotational displacements, introduces overlap be-
skewness 共␤ = 0 corresponds to prolate and ␤ = 1 to an oblate              tween some particles. Under appropriate qualifications, a
spheroid兲. It is seen that the density rises as a linear function          jammed packing can also be defined as a rigid packing, that
of ␣ − 1 from its sphere value ␾J ⬇ 0.64, reaching densities as            is, a packing that can resolve any externally applied forces
high as ␾J ⬇ 0.74 for the self-dual ellipsoids with ␤ = 1 / 2.             through interparticle ones.
The jamming density eventually decreases again for higher                      Readers should observe that the terms “stable,” “rigid,”
aspect ratios, however, we do not investigate that region in               and “jammed” are defined differently by different authors.
this work. The contact number also shows a rapid rise with                 These different definitions are, however, mathematically
␣ − 1, and then plateaus at values somewhat below isocon-                  closely related. For example, Ref. 关8兴 defines a rigid packing
strained, Z̄ ⬇ 10 for spheroids, and Z̄ ⬇ 12 for nonspheroids.             as a packing which has no floppy modes, thus relying on
In Sec. IX we will need to revert to two dimensions 共ellipses兲             linearization of the impenetrability constraints. We prefer to
in order to make some analytical calculations possible. We                 use the term “jammed” for kinematic considerations, and not
therefore also generated jammed packings of ellipses, and                  involve linear approximations so that all definitions apply to
show the results in Fig. 2. Since monodispersed packings of                systems of nonspherical particles. Reference 关8兴 defines a
disks always crystallize and do not form disordered jammed                 stable packing as one which is a strict local potential energy
packings, we used a binary packing of particles with one                   minimum 共where the potential energy is, for example, grav-
third of the particles being 1.4 times larger than the remain-             ity兲. A precise definition of jamming based on stability is
ing two thirds. The ellipse packings show exactly the same                 developed mathematically in Ref. 关20兴. Since a packing can
qualitative behavior as ellipsoids.                                        be at a stable energy minimum without being jammed 共see,

                                                                     051304-3
DONEV et al.                                                                                PHYSICAL REVIEW E 75, 051304 共2007兲

for example, Fig. 13 in Ref. 关8兴兲, we use a more stringent
definition. We have chosen the more stringent definition be-
cause our focus is on locally maximally dense packings, that
is, packings where the density cannot be increased by con-
tinuously displacing the particles. Such packings are relevant
to understanding granular materials that have been vibrated
or shaken for long periods of time 关21,22兴, and also to un-
derstanding the inherent structures of glassy materials 关3,23兴.
They can be produced computationally with our molecular
dynamics algorithm and experimentally by shaking the pack-
ing container while adding more particles 关4,19兴. It is impor-
tant to point out that we do not wish to promote our defini-
tion of jamming as the “correct” one. It is equally “correct”
                                                                         FIG. 3. 共Color online兲 A jammed packing of hard disks 共yellow兲
to define a jammed packing as one stable under a particular
                                                                     is converted into a jammed packing of nonspherical particles by
applied load, and then study the particle rearrangements that
                                                                     converting the disks to polygons 共different colors兲, without chang-
result when the direction of the external applied forces             ing the contact network or contact forces. This preserves the jam-
change. In fact, realistic granular assemblies are not jammed        ming property, since the floppy modes composed of pure particle
according to our strict definitions, and particles typically re-     rotations are blocked by the flat contacts. Jamming would also be
arrange in response to external perturbations. In the limit of       preserved if the disks swell between the original shape and the
infinite compaction, however, the rearrangements will cease          polygonal shape, so that the curvature of the particle surfaces at the
and the assembly will become jammed. We focus here on                point of contact is sufficiently flat.
understanding this terminal idealized jammed state as an im-
portant first step in understanding more realistic systems. Ad-      tional overlap. That is, if we take into account orientational
ditionally, we are interested in the mathematics and physics         degrees of freedom, the disk packing would not be jammed.
of maximally dense disordered packings in their own right            It would possess floppy modes consisting of particles rotat-
关4兴.                                                                 ing around their own centroids. These floppy modes are how-
                                                                     ever trivial at the circle 共sphere兲 point in that they do not
1. Hypostatic packings of nonspherical particles can be jammed       actually change the packing configuration.
                                                                         Now imagine making the particles noncircular 共or non-
   As explained in Sec. IV, the isoconstrained property is
                                                                     spherical in three dimensions兲 and, in particular, making
usually justified in two steps. First, nondegeneracy is in-
                                                                     them polygons, so that the point contacts between the disks
voked to demonstrate the inequality Z̄ 艋 2d f , then, the con-       become 共extended兲 contacts between flat sides of the poly-
verse inequality Z̄ 艌 2d f is invoked to demonstrate the equal-      gons. The floppy modes still remain, in the sense that rota-
ity Z̄ = 2d f . The inequality Z̄ 艌 2d f is usually justified by     tions of the polygons, to first order, simply lead to the two
claiming that a packing cannot be jammed without having              tangent planes at the points of contact sliding along each
more contacts 共impenetrability constraints兲 than degrees of          other without leading to overlap. However, it is clear that this
freedom. A hypoconstrained packing necessarily has                   is only a first-order approximation. In reality, the polygons
“floppy” or zero modes, which are collective motions of the          cannot be rotated because such rotation leads to overlap in
particles that preserve the interparticle distances to first order   the extended region of contact around the point of contact.
in the magnitudes of the particle displacements. It is claimed       To calculate the amount of overlap, one must use second-
that such floppy modes are not blocked by the impenetrabil-          order terms, that is, consider not only the tangent planes at
ity constraints and therefore a hypoconstrained packing can-         the point of contact but also the curvature of the particles at
not be jammed. Alternatively, it is claimed that externally          the point of contact. Low curvature, that is, “flat” contacts,
applied forces that are in the direction of such floppy modes        block rotations of the particles. It should be evident that even
cannot be resisted 共sufficiently兲 by the interparticle forces        if the radius of curvature is not infinite, but exceeds a certain
and therefore the packing cannot be rigid. We will now ex-           threshold 关24兴, the floppy modes would in fact be blocked
plain, through an example, why these claims are wrong and,           and the packing would be jammed despite being hypocon-
in fact, why a hypoconstrained packing can be jammed/rigid           strained. In fact, the packing has exactly as many contacts as
if the curvature of the particles at the point of contact is         the original disk packing.
sufficiently flat in order to block the floppy modes.                    It is important to note that contact curvature cannot block
   Consider an isoconstrained jammed packing of hard cir-            purely translational particle displacements unless one of the
cular disks, as illustrated in Fig. 3. In reality, the disks would   particles is curved outward, i.e., is concave 共e.g., imagine a
be elastic 共soft兲 but stiff, and let us imagine the system is        dent in a table and a sphere resting in it, not being able to
under a uniform state of compression, so that the particles          slide translationally兲. If the particles shapes are convex, a
are exerting compressive forces on each other. If there are no       packing cannot have fewer contacts than there are transla-
additional external forces, the interparticle forces would be        tional degrees of freedom, that is, Z̄ 艌 2d. This explains why
in force equilibrium. The packing is translationally jammed,         hypersphere packings are indeed isoconstrained. It is only
and the disk centroids are immobile; however, the 共friction-         when considering rotational degrees of freedom that jammed
less兲 disks can freely rotate without introducing any addi-          packings can be hypoconstrained.

                                                               051304-4
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                     PHYSICAL REVIEW E 75, 051304 共2007兲

    Those that prefer to think about rigidity 共forces兲 would        necessarily denser than the corresponding sphere packings.
consider applying external forces and torques on the particles          The first point to note is that disordered isoconstrained
in the example from Fig. 3. The forces would clearly be             packings of nearly spherical ellipsoids are hard to construct.
resisted just as they were in the jammed disk packing. How-         In particular, achieving isocounting near the sphere point re-
ever, at first sight, it appears that torques would not be re-      quires such high contact numbers 关specifically, Z̄ = d共d + 1兲兴
sisted. In fact, it would seem that torques cannot be resisted      that translational ordering will be necessary. Translationally
by interparticle forces since, for each of the particles, the       maximally random jammed 共MRJ兲 sphere packings have Z̄
normal vectors at the points of contact all intersect at a single   = 2d, and even if one considers the observed multitude of
point 共the center of the hard disks兲 and therefore the net          near contacts 关2兴, they fall rather short of Z̄ = d共d + 1兲. It
torque is identically zero. This argument, however, neglects        seems intuitive that translational crystallization would be
an important physical consideration: the deformability of the       necessary in order to raise the contact number that much. In
particles. Namely, no matter how stiff the particles are, they      other words, in order to gain sufficiently many constraints,
will deform slightly under an applied load. In particular,          one would have to sacrifice translational disorder. Further-
upon application of torques, the particles will rotate and the      more, there is little reason to expect packings of nearly
normal vectors at the points of contact would change and no         spherical particles to be rotationally jammed. Near the jam-
longer intersect at a single point, and the packing will be able    ming point, it is expected that particles can rotate signifi-
to resist the applied torques. One may be concerned about           cantly even though they will be translationally trapped and
the amount of rotation necessary to resist the applied load. If     rattle inside small cages, until of course the actual jamming
the packing needs to deform significantly to resist applied         point is reached, at which point rotational jamming will also
loads, should it really be called rigid?                            come into play. Therefore, it is not surprising that near the
    To answer such concerns, one must calculate the particle        sphere point, the translational structure of the packings
displacements needed to resist the load. Such a calculation,        changes little.
carried out for deformable particles in Sec. VIII, points to the        Mathematically, jamming is analyzed by using a Taylor
importance of the preexisting 共i.e., internal兲 contact forces.      expansion of the interparticle distances in the particle dis-
This is easy to understand physically. If the packing is under      placements. At the first-order level, this expansion contains
a high state of compression, the interparticle forces would be      first-order terms coming from translations and from rotations
large and even a small change in the packing geometry 共de-          and involving the contact points and contact normals. The
formation兲 would resist large torques. If, on the other hand,       expansion also contains second-order terms from transla-
the internal forces 共stresses兲 are small, the particles would       tions, rotations, and combined motions, involving addition-
have to deform sufficiently to both induce sufficiently large       ally the contact curvatures. And of course, there are even
contact forces and to change the normal vectors sufficiently.       more complicated higher-order terms. One should be careful
This kind of stability, requiring sufficiently large internal       of such a Taylor expansion for two reasons. First, the expan-
stresses, is well known for engineering structures called           sion assumes that terms coming from translations and rota-
“tensegrities.” These structures are built from elastic cables      tions are of the same order. This is clearly not true for either
and struts, and are stabilized by stretching the cables so as to    the case of perfectly spherical particles, when rotational
induce internal stresses. Beautiful and intriguing structures       terms are identically zero, or for the case of rods or plates,
can be built that are rigid even though they appear not to be       where even a small rotation can cause very large overlap.
sufficiently braced 共as bridges or other structures would have      Second, the expansion assumes that various quantities re-
to be兲.                                                             lated to the particle and contact geometry 共for example, the
    While the above discussion focused on packings of mac-          contact curvature radii兲 are of similar order. This fails, for
roscopic elastic particles, similar arguments apply also to         example, for the case of planar 共flat兲 contacts, where even a
systems such as glasses. For such systems, floppy modes are         small rotation of the particles leads to significant overlap far
manifested as zero-frequency vibrational modes, that is, zero       from the point of contact. These subtle points arise only
eigenvectors of the dynamical matrix. The calculations in           when considering aspherical particles and should caution one
Sec. VIII show that for nonspherical particles, the dynamical       from blindly generalizing the mathematical formalism of
matrix contains a term proportional to the internal forces and      jamming developed and tested only within the context of
involving the contact curvatures. If the system is at a positive    sphere packings.
pressure, the forces will be nonzero and this term contributes          In Sec. IX, we will consider packings of nearly spherical
to the overall dynamical matrix. In fact, it is this term that      ellipsoids as a perturbation of jammed sphere packings in
makes the dynamical matrix positive definite, i.e., that elimi-     which the particles, following a slight change of the particle
nates zero-frequency modes despite the existence of floppy          shape away from perfect spherical symmetry, translate and
modes.                                                              rotate in order to reestablish contacts and jamming. While
                                                                    the necessary particles’ translations are small, the particle
     2. Translational versus rotational degrees of freedom
                                                                    rotations are large. In fact, rotational symmetry is broken,
    Having explained that hypoconstrained packings of non-          and particles must orient themselves correctly, so that con-
spherical particles can be jammed if the interparticle contacts     tacts can be reestablished, and also so that forces and torques
are sufficiently flat, we now try to understand why packings        become balanced. This symmetry breaking is the cause of the
of nearly spherical particles are hypoconstrained. The analy-       cusp like non analyticity of the density as a function of par-
sis will also demonstrate why packings of hard ellipsoids are       ticle shape 关4兴. We will see that the particle orientations in

                                                              051304-5
DONEV et al.                                                                                PHYSICAL REVIEW E 75, 051304 共2007兲

the final jammed packing of nearly spherical ellipsoids are         complexity we will often rely on the context for clarity. The
not random, but rather, they are determined by the structure        notation is similar to that used in Ref. 关15兴 and attempts to
of the initial sphere packing. Of course, as aspect ratio in-       unify two and three dimensions whenever possible. We refer
creases, rotations become more and more on equal footing            to reader to Ref. 关15兴 or Ref. 关25兴 for details on representing
with translations, and the packings become both truly trans-        particle orientations and rotations in both two and three di-
lationally and orientationally disordered.                          mensions.
    This picture of jamming in the vicinity of the sphere point         We will use matrix notation extensively, and denote vec-
also explains why the density rises sharply near the sphere         tors and matrices with bolded letters, and capitalize matrices
point for ellipsoids. Start with a jammed sphere packing and        in most cases. Infinite-dimensional or discrete quantities
apply an affine transformation to obtain an aligned 共nematic兲       such as sets or graphs will typically be denoted with script
packing with exactly the same density. This packing will not        letters. We will often capitalize the letter denoting a vector to
be rotationally jammed, and by displacing the particles one         denote a matrix obtained from that vector. Matrix multipli-
will be able to open up free volume between them and there-         cation is assumed whenever products of matrices or a matrix
fore increase the density. We will show that in fact the maxi-      and a vector appear. We prefer to use matrix notation when-
mal increase in the density is obtained for the choice of par-      ever possible and do not carefully try to distinguish between
ticle orientations that balances the torques on the particles in    scalars and matrices of one element. We denote the dot prod-
addition to the forces. Therefore, the jammed disordered el-        uct a · b with aTb, and the outer product a 丢 b with abT. We
lipsoid packings we obtain near the sphere point are the            denote a vector with all entries unity by e = 1, so that 兺iai
densest perturbation of the corresponding sphere packings.          = eTa. We consider matrices here in a more general linear
The added rotational degrees of freedom allow one to in-            operator sense, and they can be of order higher than 2 共i.e.,
crease the density beyond that of the aligned 共nematic兲 pack-       they do not necessarily have to be a rectangular two-
ing, which for ellipsoids has exactly the same density as the       dimensional array兲. We refer to differentials as gradients
sphere point.                                                       even if they are not necessarily differentials of scalar func-
    In conclusion, near the sphere point, there is a competi-       tions. Gradients of scalars are considered to be column vec-
tion between translational and rotational jamming and also          tors and gradients of vectors or matrices are matrices or ma-
between translational and rotational disorder. At the sphere        trices 共linear operators兲 of higher rank.
point ␣ = 1, and in this neighborhood, translational degrees of
freedom win. As one moves away from the sphere point,                                       A. Particle packings
however, translational and rotational degrees of freedom start
to play an equal role. For very large aspect ratios, ␣ Ⰷ 1, it is       A jammed particle packing has a contact network indicat-
expected that rotational degrees of freedom will dominate,          ing the touching pairs of particles 兵i , j其. We will sometimes
although we do not investigate that region here.                    talk about a particular particle i or a particular contact 兵i , j其
                                                                    ⬅ ij and we will usually let the context determine what spe-
                                                                    cific particle or contact is being referred to or, if deemed
                          C. Contents
                                                                    necessary, put subscripts such as i or ij to make it specific
   Before proceeding, we give an overview of our notation           what particle or contact is being referred to. The contact ji is
in Sec. II. In Sec. III, we discuss the nonoverlap conditions       physically the same undirected contact as ij, but the two
between convex hard particles. In Sec. IV, we define jam-           directed contacts are considered distinct.
ming and investigate the reasons for the failure of the iso-            There are two primary kinds of vectors x, particle vectors
counting conjecture for nonspherical particles. In Sec. V, we       X = 共xi兲 = 共x1 , . . . , xN兲, which are obtained by concatenating
develop the first- and second-order conditions for jamming          the vectors xi 共typically of size of the order of the space
in a system of nonspherical particles, and then design and          dimensionality d兲 corresponding to each of the N particles,
use a practical algorithm to test these conditions for ellipsoid    and contact vectors y = 共y ij兲 = 共y 1 , . . . , y M 兲, obtained by con-
packings in Sec. VI. In Sec. VII, we consider the thermody-         catenating the 共typically scalar兲 values y ij corresponding to
namical behavior of hypoconstrained packings that are close         each of the M contacts 共numbered in arbitrary order from 1
to, but not quite at, the jamming point. In Sec. VIII, we           to M兲. Note the capitalization of particle vectors, which we
discuss the connections between jammed packings of hard             will often do implicitly, to indicate that one can view X as a
particles and strict energy minima for systems of deformable        matrix where each row corresponds to a given particle. If a
particles. In Sec. IX, we focus on packings of nearly spheri-       contact vector agglomerates a vector quantity attached to
cal ellipsoids, and finally, offer conclusions in Sec. X.           each contact, for example, the common normal vector n at
   It is important to note that Secs. III, V, and VI are highly     the point of contact of two particles, it too would be capital-
technical, and may be either skipped or skimmed by readers          ized, e.g., N = 共nij兲.
not interested in the mathematical formalism of jamming.
Readers interested in specific examples of hypoconstrained                               1. Packing configuration
packings are referred to Sec. IV B 2 and the Appendix.
                                                                        A packing is a collection of N hard particles in Rd such
                                                                    that no two particles overlap. Each particle i has d f configu-
                        II. NOTATION
                                                                    rational degrees of freedom, for a total of N f = Nd f degrees of
  We have tried to develop a clear and consistent notation,         freedom. A packing Q = 共Q , ␾兲 is characterized by the con-
however, in order to avoid excessive indexing and notation          figuration Q = 共q1 , . . . , qN兲 苸 RN f , determining the positions

                                                              051304-6
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                       PHYSICAL REVIEW E 75, 051304 共2007兲

of the centroid and the orientations of each particle, and the                       a ⫻ b = Ab = − b ⫻ a = − Ba,                   共1兲
packing fraction 共density兲 ␾ determining the size of the par-
ticles. For spheres Q ⬅ R corresponds to only the positions          where



                                                                                              冤                            冥
of the centroids, and d f = d. For nonspherical particles with-                                    0     − az         ay
out any axes of symmetry there are an additional d共d − 1兲 / 2
rotational degrees of freedom, for a total of d f = d共d + 1兲 / 2                 A = 兩a兩⫻ =        az        0        − ax = − AT
degrees of freedom. In actual numerical codes particle orien-                                     − ay    ax           0
tation is represented using unit quaternions, which are redun-       is a skew-symmetric matrix which is characteristic of the
dant representations in the sense that they use d共d − 1兲 / 2 + 1     cross product and is derived from a vector. We will simply
coordinates to describe orientation. Here we will be focusing        capitalize the letter of a vector to denote the corresponding
on displacements of the particles ⌬Q from a reference                cross product matrix 共such as A above corresponding to a兲,
jammed configuration QJ, and therefore we will represent             or use 兩a兩⫻ when capitalization is not possible. In two dimen-
particle orientations as a rotational displacement from a ref-       sions, there are two “cross products.” The first one gives the
erence orientation ⌬␸. In two dimensions ⌬␸ = ⌬␸ simply              velocity of a point r in a system which rotates around the
denotes the angle of rotation in the plane, and in three di-         origin with an angular frequency ␻ 共which can also be con-
mensions the direction of ⌬␸ gives the axis of rotation and          sidered a scalar ␻兲,

                                                                                                         冋 册
its magnitude determines the angle of rotation. For simplic-
ity, we will sometimes be sloppy and not specifically sepa-                                              − ␻r y
rate centroid positions from orientations, and refer to qi as 共a                       v = ␻r =                       = ⍀r,        共2兲
                                                                                                          ␻rx
generalized兲 position; similarly, we will sometimes refer to
both forces and torques as 共generalized兲 forces.                     where

                        2. Rigidity matrix                                               ⍀=   冋    0 −␻
                                                                                                   ␻     0
                                                                                                                 册   = − ⍀T
    For the benefit of readers not interested in the mathemati-
cal formalism, we briefly introduce the concepts and notation        is a cross product matrix derived from ␻. The second kind of
developed in more detail in Sec. III. We denote the distance,        “cross product” gives the torque around the origin of a force
or gap, between a pair of hard particles i and j with ␨ij. When      f acting at a point 共arm兲 r,
considering all of the M contacts together, the gradient of the                 ␶ = f ⫻ r = − r ⫻ f = 关f xry − f yrx兴 = FLr,        共3兲
distance function ␨ = 共␨ij兲 with respect to the positions 共i.e.,
displacements兲 of the particles is the rigidity matrix A             where
= ⵱Q␨. This linear operator connects, to first order, the                                FL = 关− f y f x兴 = − 共FR兲T
change in the interparticle gaps to the particle displacements
⌬␨ = AT⌬Q. We denote the magnitudes of the compressive               is another cross product matrix derived from a vector 共the L
共positive兲 interparticle forces carried by the particle contacts     and R stand for left and right multiplication, respectively兲.
with f = 共f ij兲, f ij 艌 0, where it is assumed that the force vec-   Note that in three dimensions all of these coincide, FL = FR
tors are directed along the normal vectors at the point of           = F, and also  ⬅ ⫻, while in two dimensions they are re-
contact 共since the particles are frictionless兲. The total forces     lated via ab = Ab = −BRa.
and torques exerted on the particles B 共alternatively denoted
by ⌬B if thought of as force imbalance兲 are connected to the         III. NONOVERLAP CONSTRAINTS AND INTERPARTICLE
interparticle forces via a linear operator that can be shown to                          FORCES
be the conjugate 共transpose兲 of the rigidity matrix, B = Af.
    A subtle point that we will return to later is the role of the      In this section we will discuss hard-particle overlap po-
density ␾. Since we are interested in 共locally兲 maximally            tentials used to measure the distance between a pair of hard
dense disordered packings, we will sometimes consider the            particles. These potentials will be used to develop analytic
density as an additional kinematic degree of freedom. That           expansions of the nonoverlap conditions in the displacements
is, we will sometimes include the change in density ⌬␾ in            of the particles. This section is technical and may be skipped
the deformation ⌬Q. This effectively adds an additional row          or skimmed by readers not interested in the mathematical
to the rigidity matrix. One may similarly include additional         formalism of jamming. Interested readers can find additional
global degrees of freedom, such as boundary conditions, and          technical details on the material summarized in this section
add further rows to the rigidity matrix. This also adds gen-         in Chap. 2 of Ref. 关25兴.
eralized forces 共stresses兲 as the conjugate variables to those
additional kinematic degrees of freedom 关25兴.                                             A. Overlap potentials
                                                                        The nonoverlap condition between a pair of particles A
                                                                     and B can be thought of as an inequality between the posi-
                       B. Cross products
                                                                     tions and orientations of the particles. For this purpose, we
   In three dimensions, the cross product of two vectors is a        measure the distance between the two ellipsoids using the
linear combination of them that can be thought of as matrix-         overlap potential ␨共A , B兲 = ␨共qA , qB兲, whose sign not only
vector multiplication                                                gives us an overlap criterion,

                                                               051304-7
DONEV et al.                                                                              PHYSICAL REVIEW E 75, 051304 共2007兲


               ␨共A,B兲 ⬎ 0 if A and B are disjoint,

        ␨共A,B兲 = 0 if A and B are externally tangent,

           ␨共A,B兲 ⬍ 0 if A and B are overlapping,
but which is also at least twice continuously differentiable in
the positions and orientations of A and B. An additional re-
quirement is that ␨共A , B兲 be defined and easy to compute for
all positions and orientations of the particles.
   We define and compute the overlap conditions using a
procedure originally developed for ellipsoids by Perram and
Wertheim 关26兴. This procedure is easily generalized to any
convex particle shape given by the inequality ␨共r兲 艋 1, where
the shape function ␨ is strictly convex and defined through            FIG. 4. Illustration of the common scaling ␮ that brings two
                                                                   ellipses 共dark gray兲 into external tangency at the contact point rC.
                       ␨共r兲 = 关␮共r兲兴2 − 1,
where ␮ is the scaling factor by which the particle needs to                    1. Derivatives of the overlap potentials
be resized in order for the point r to lie on its surface. The        We will frequently need to consider derivatives of the
un-normalized normal vector to the surface at a given point        overlap function with respect to the 共generalized兲 positions
r, if the particle is rescaled so that it passes through it, is    of the particles, either first order,
n共r兲 = ⵱␨共r兲. Define also the displacement between the par-
ticle centroids rAB = rA − rB, and the unit vector joining the
two particle centroids with uAB = rAB / 储rAB储.
                                                                                          ⵱ qi␨ = ⵱ i␨ =   冉 冊
                                                                                                            ⳵␨
                                                                                                            ⳵qi
    The Perram and Wertheim 共PW兲 overlap potential is de-
fined through                                                      or second order

      ␨ = ␮2 − 1 = max min关␭␨A共rC兲 + 共1 − ␭兲␨B共rC兲兴.
                    0艋␭艋1 rC                                                          ⵱q2 q ␨ = ⵱2ij␨ =
                                                                                          i j
                                                                                                          冋 册⳵ 2␨
                                                                                                           ⳵ q i⳵ q j
                                                                                                                      .

For every multiplier ␭, the solution of the inner optimization
                                                                   To first order, the particles can be replaced by their 共parallel兲
over rC is unique due to the strict convexity of rC, and sat-
                                                                   tangent planes at the point of contact and the first order de-
isfies the gradient condition
                                                                   rivatives can be expressed in terms of quantities relating to
                   ␭nA共rC兲 = − 共1 − ␭兲nB共rC兲,                      the two tangent planes. To second order, the particles can be
                                                                   replaced by paraboloids that have the same tangent plane, as
which shows that the normal vectors are parallel 共with oppo-       well as the same principal curvature axes and the same radii
site directions兲. The solution of the outer optimization prob-     of curvatures as the two particles at the point of contact. It is
lem over ␭ is given through the condition                          therefore possible to derive general expressions for the de-
                                                                   rivatives in terms of quantities relating to the normal vectors
                      ␨ = ␨A共rC兲 = ␨B共rC兲,
                                                                   and surface curvatures of the particles at the point of contact.
which means that when the particles are rescaled by a com-             The first-order derivatives can easily be expressed in
mon scaling factor ␮ = 1 + ⌬␮ = 冑1 + ␨ they are in external        terms of the position of the contact point rC and the 共normal-
tangency, sharing a common normal direction n = nA / 储nA储          ized and outwardly directed兲 contact normal vector n. For
共i.e., normalized to unit length and directed from A to B兲, and    this purpose, it is easier to measure the distance between two
sharing a contact point rC. When focusing on one particle we       particles in near contact via the Euclidian interparticle gap h
can measure rC with respect to the centroid of the particle, or    giving the 共minimal兲 surface-to-surface distance between the
otherwise specifically denote rAC = rC − rA and rBC = rC − rB.     particles along the normal vector. Moving one of the par-
This is illustrated for ellipses in Fig. 4. If the particles are   ticles by ⌬q = 共⌬r , ⌬␸兲 displaces the contact point by ⌬rC
touching then ␮ = 1 and the procedure described above gives        = ⌬r + ⌬␸rC and therefore changes the gap by ⌬h =
us the geometric contact point and therefore the common            −nT⌬rC = −nT⌬r − 共rC ⫻ n兲T⌬␸, giving the gradient


                                                                                                     冋 册
normal vector. In the case of spheres of radius O the PW
overlap potential simply becomes                                                                        n
                                                                                          ⵱ qh = −          .
                                           2
                                                                                                     rC ⫻ n
               共rA − rB兲T共rA − rB兲        lAB
       ␨AB =                       −1=            − 1,      共4兲    The relation between the 共small兲 Euclidian gap h and the
                   共OA + OB兲 2
                                       共OA + OB兲2
                                                                   共small兲 gap as measured by the PW overlap potential ␨ can
which avoids the use of square roots in calculating the dis-       be seen by observing that scaling an ellipsoid by a factor ␮
tance between the centers of A and B, lAB, and is easily           displaces the contact point by ⌬rC = ⌬␮rC. Therefore, the
manipulated analytically.                                          scaling factor needed to close the interparticle gap is

                                                             051304-8
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                                    PHYSICAL REVIEW E 75, 051304 共2007兲


                     ␨       h         h                                         torque exerted on a given particle i by the contacts with its
               ␮⬇      ⬇          T = T   ,                                      neighbors N共i兲 is
                     2 共rBC − rAC兲 n rABn
giving the gradient
= 2共⵱qh兲 / 共rAB
             T
                n兲,
                           of       the        overlap        potential   ⵱ q␨            ⌬bi = −    兺
                                                                                                    j苸N共i兲
                                                                                                           冋
                                                                                                           f ij ij
                                                                                                                    n
                                                                                                                   ij
                                                                                                               共r ⫻ nij兲
                                                                                                               iC
                                                                                                                           册
                                                                                                                         = 兺 f ij共⵱ihij兲


               ⵱A/B␨ = ⫿     T
                            rAB
                                2
                                n
                                     冋            n
                                         r共A/B兲C ⫻ n
                                                          册   .
                                                                                 or, considering all particles together,
                                                                                                            ⌬B = AEf.
For spheres the cross product is identically zero and rotations                  The fact that the matrix 共linear operator兲 connecting force
can be eliminated from consideration.                                            imbalances to contact forces is the transpose of the rigidity
   The second-order derivatives are not as easily evaluated                      matrix is well-known and can also be derived by considering
for a general particle shape. In two dimensions, or in three                     the work done by the contact forces to displace the particles
dimensions when the principal radii of curvatures at the point
of contact are equal, one can replace the particle around the                     W = ⌬bT⌬Q = 共Ãf兲T⌬Q = fT共ÃT⌬Q兲 = fT⌬h = fT共AET⌬Q兲,
point of contact with a sphere of the appropriate position and
radius. However, when the radii of curvatures are different                      showing that Ã = AET. In this work we will use forces f that
this is not as easy to do. We will give explicit expressions for                 are a rescaled version of the physical forces fE, f ij = 共rTijnij兲
the second-order derivatives of ␨ for ellipsoids in Sec.                         f Eij / 2, so that Af = AEfE. This scaling is more natural for our
VI A 2. Related first- and second-order geometric derivatives                    choice of overlap potential, and does not affect any of the
have been derived for general particle shapes 共i.e., using the                   results.
normal vectors and curvature tensors of the particles at the                            In static packings that are under an applied load B, the
point of contact兲 in the granular materials literature in more                   force/torque equilibrium condition
general contexts 关20,27兴; here we specialize to the case of
hard frictionless ellipsoids.                                                                           Af = − B and f 艌 0
                                                                                 must be satisfied. The actual magnitudes of the forces are
                     B. The rigidity matrix                                      determined by external loads 共for example, the applied pres-
   When considering all of the M contacts together, the gra-                     sure for a system of deformable particles兲, history of the
dient of the overlap potential ␨ = 共␨ij兲 is the important rigidity               packing preparation, etc. However, the relation between the
matrix                                                                           forces at different contacts is determined by the packing ge-
                                                                                 ometry, or more specifically, by A. Typically forces are res-
                           A = ⵱ Q␨ .                                            caled to a mean value of unity eTf = M, and it has been ob-
                                                                                 served that the distribution of rescaled contact forces has
This 关N f ⫻ M兴 matrix connects, to first order, the change in
                                                                                 some universal features, for example, there is an exponential
the interparticle gaps to the particle displacements ⌬␨                          tail of contacts carrying a large force, and also a large num-
= AT⌬Q. It may sometimes be more convenient to work with                         ber of contacts supporting nearly zero force 关2,28兴. We will
surface-to-surface interparticle gaps ⌬h = AET⌬Q 共the sub-                       see later that these force chains, or internal stresses, are an
script E stands for Euclidian兲, especially if second-order                       essential ingredient of jamming for hard particles.
terms are not considered 关11兴. The rigidity matrix is sparse
and has two blocks of d f nonzero entries in the column cor-
responding to the particle contact 兵i , j其, namely, ⵱i␨ij in the                           IV. THE ISOCOUNTING CONJECTURE
block row corresponding to particle i and ⵱ j␨ij in the block
                                                                                    In the granular materials literature special attention is of-
row corresponding to particle j 共unless one of these particles
                                                                                 ten paid to so-called isostatic packings. There are several
is frozen兲. Represented schematically:
                                                                                 different definitions of isostaticity, and most of the discus-
                                         兵i, j其                                  sions in the literature are specifically applied to mechanical
                                                                                 structures composed of elastic bars, to packings of hard
                                           ↓




                                    冤冥
                                                                                 spheres, or to packings of frictional particles. In this section
                                           ⯗                                     we summarize several relevant definitions of and arguments
                      A = i→          ⵱i␨ij           .                          for isostaticity and generalize them to nonspherical particles.
                                           ⯗                                        We define a packing to be “isoconstrained” if the number
                          j→                                                     of constraints 共contacts兲 is equal to the total number of de-
                                      ⵱ j␨ij                                     grees of freedom
                                           ⯗
                                                                                                           Nc = N f + 1,
                                                                                 where for jammed packings one should count the density ␾
                     C. Interparticle forces
                                                                                 as a single degree of freedom, in addition to the degrees of
   Hard particles in contact can exert a compressive 共posi-                      freedom due to the particles and boundary N f , as discussed
tive兲 contact force f = fn, f 艌 0, directed along the normal                     further in Sec. IV A 1 and IV A 2. Packings with fewer con-
vector 共for frictionless particles兲. The total excess force and                  tacts than isoconstrained are called “hypoconstrained” and

                                                                           051304-9
DONEV et al.                                                                             PHYSICAL REVIEW E 75, 051304 共2007兲

packings with more contacts than isoconstrained are “hyper-            Perturbation. A packing is stable if the structure of the
constrained.” The isocounting conjecture states that large          packing changes smoothly for small perturbations of the
jammed disordered packings of hard particles are isocon-            packing.
strained. Defining what precisely is meant by a disordered             We will consider each of these approaches separately. It
packing is difficult in itself 关16,29兴. Intuitively, in a disor-    will shortly become clear that all of them are closely related,
dered packing there is only the minimal degree of correla-          and under certain mild conditions they are actually equiva-
tions between particles, as necessitated by the constraints of      lent. We will use the term jamming as an umbrella term, and
impenetrability and jamming. Therefore, it is expected that in      later give our preferred definition of jamming, which is
a certain sense disordered packings are “generic” 关30,31兴,          based on the kinematic perspective. We note that it is impor-
and that “special” configurations with geometric degenera-          tant to precisely specify the boundary conditions applied re-
cies will not appear. Note that for large systems the majority      gardless of the view used in considering jamming; different
of the degrees of freedom come from the particles them-             boundary conditions lead to different jamming categories,
selves, N f ⬇ Nd f , and the majority of constraints come from      specifically local, collective, or strict jamming 关11,37兴. Here,
contacts shared between two particles, Nc ⬇ M = NZ̄ / 2, giv-       we will sometimes use local jamming in simple examples but
ing the isocounting property                                        mostly focus on collective jamming; all collective particle
                                                                    motions are blocked by the impenetrability constraints sub-
                            Z̄ = 2d f .                      共5兲    ject to periodic boundary conditions with fixed lattice vec-
                                                                    tors. In order to eliminate trivial uniform translations of the
Equation 共5兲 has been verified to very high accuracy for            systems, we can freeze the centroid of one of the particles, to
jammed hard-sphere packings 关2兴. However, disordered                obtain a total of
packings of hard ellipsoids are always hypoconstrained and
thus contradict the isocounting conjecture 关4兴.                                              N f = Nd f − d
   The notion of an isoconstrained packing is very closely
                                                                    internal degrees of freedom. The exact boundary conditions
related to the concept of an isostatic packing, which consid-
                                                                    affect the counting of constraints and degrees of freedom,
ers the 共linear兲 independence of the constraints in addition to
                                                                    however, the correction is not extensive in N and therefore is
their number. An isostatic packing is defined as a packing
                                                                    negligible for large system when considering per-particle
that has an invertible 共and thus square兲 rigidity matrix. This
definition has not been formally stated in the literature, and it   quantities such as Z̄.
is the obvious generalization of the definition commonly                An important point to note is that the above definitions of
used for systems of spheres. One can include the density as         jamming treat all degrees of freedom identically, in particu-
an additional degree of freedom when forming the rigidity           lar, translational motion 共forces兲 is treated on the same foot-
matrix, or exclude it, depending on the definition of jamming       ing as rotational motion 共torques兲. This is not necessarily the
that is adopted, as discussed in the next section. This choice      most appropriate definition, as is easily seen by considering
changes the counting arguments by 1. This definition of the         the case of spheres, which can rotate in place freely even
term isostatic implicitly relies on the linearization of the im-    though they are 共translationally兲 jammed. This distinction be-
penetrability constraints. We try to make our definitions in-       tween translations and rotations will become important in
dependent of the order of approximation used in some par-           Sec. VII when considering packings that are nearly, but not
ticular expansion. Therefore, we use the simple definition of       quite jammed. It should also be mentioned that jammed ran-
“isoconstrained” based on counting, and qualify it with             dom particle packings produced experimentally or in simu-
“jammed” or “rigid.”                                                lations typically contain a small population of rattlers, i.e.,
   In this section we attempt to deconstruct previous discus-       particles trapped in a cage of jammed neighbors but free to
sions of isostaticity and jamming in hard-particle packings,        move within the cage. For present purposes we shall assume
and we hope that through our discussions it will become             that these have been removed before considering the 共possi-
clear why previous “proofs” of the isocounting conjecture do        bly兲 jammed remainder. This idea of excluding rattlers can
not apply to nonspherical particles, or to put it the other way     be further extended to rattling clusters of particles, i.e.,
around, what makes disordered sphere packings isocon-               groups of particles that can be displaced collectively even
strained.                                                           though the remainder of the packing is jammed. In fact, we
                                                                    will consider any packing which has a jammed subpacking
               A. Jamming, rigidity, and stability
                                                                    共called a “backbone”兲 to be jammed.

   An essential initial step is defining more precisely what is
                                                                                           1. Kinematic view
meant by a stable, rigid, or jammed packing. All of these
terms have been used in the literature, and in fact we equate           The kinematic perspective considers a packing jammed if
each of them with a particular perspective on jamming.              it is not possible to continuously displace the particles in a
   Kinematic. A packing is jammed if none of the particles          nontrivial way without introducing overlap. We have focused
can be displaced in a nontrivial way without introducing            on this perspective in our work, see Refs. 关11,32兴. That is,
overlap between some particles.                                     the impenetrability conditions preclude any motion of the
   Static. A packing is rigid if it can resolve any externally      particles. Here trivial motions are those that do not change
applied forces through interparticle ones, without changing         the distances between any two particles, such as global trans-
the packing configuration.                                          lations when periodic boundary conditions are used. We can

                                                              051304-10
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                      PHYSICAL REVIEW E 75, 051304 共2007兲

assume that such trivial motions have been eliminated via          geometry of the packing, i.e., the rigidity matrix A, changes
some artificial constraint, such as fixing the centroid of one     when an external load is applied on the packing. Physically,
particle externally when using periodic boundary conditions.       forces arise only through deformation, and this deformation,
   Mathematically, for any continuous motion ⌬Q共t兲 there           however small, together with the preexisting forces in the
exists a T ⬎ 0 such that at least one of the impenetrability       packing, may need to be taken into account. Forces are in
constraints between a touching pairs of particles                  essence Lagrange multipliers associated with the impenetra-
                                                                   bility constraints in Eq. 共6兲; the very existence of such
                      ␨关QJ + ⌬Q共t兲兴 艌 0                     共6兲    Lagrange multipliers may require a change in the packing
                                                                   configuration.
is violated for all 0 ⬍ t ⬍ T. A motion ⌬Q共t兲 such that for all        The above formulation also neglects the existence of
0 ⬍ t ⬍ T none of the constraints are violated is an unjam-        small interparticle gaps, which cannot be neglected when
ming motion. One can in fact restrict attention to analytic        analyzing the response of packings to applied loads, espe-
paths ⌬Q共t兲, and also show that a jammed packing is in a           cially for granular materials 关8,11兴. While mathematically we
sense isolated in configuration space, since the only way to       talk about ideal jammed packings, where geometric contacts
get to a different packing is via a discontinuous displacement     are perfect, in reality one should really analyze packings that
储⌬Q 储 ⬎ 0 关12兴.                                                    are almost jammed, i.e., where the contacts are almost
    A similar definition of jamming was used by Alexander in       closed. This is more appropriate for granular materials,
Ref. 关10兴. He considers a packing to be geometrically rigid if     where there is typically some room for the particles to move
it cannot be “deformed continuously by rotating and trans-         freely. Alternatively, one should analyze packings where all
lating the constituent grains without deforming any of them        the contacts are indeed closed, however, the system is under
and without breaking the contacts between any two grains.”         some form of global compression. This is appropriate for
This definition implies that a packing in which particles can      glassy systems under a uniform external pressure. When in-
be moved so as to break contacts 共for example, imagine a           terparticle gaps are present, particles must displace slightly
pebble resting on other pebbles in gravity, and moving it          to close the gaps so that they can exert positive contact
upward away from the floor兲 is jammed. Later in the paper          forces on one another and resist the applied load. The set of
Alexander talks about adding constraints to block motions          contacts 兵i , j其 that are closed 共i.e., have a positive force f ij兲 is
that break contacts. We in fact have in a certain sense a          the set of active contacts. Different applied loads will be
choice in the matter, determining whether we work with in-         supported by different active contact networks, and for suf-
equality or equality constraints. We choose to work with in-       ficiently small interparticle gaps finding the active set re-
equality constraints, since this is the natural choice for fric-   quires solving a linear program, as discussed in Sec. V D 1.
tionless hard particles; there is no cohesion between the          When there is a global external compression 共pressure兲 in the
particles maintaining contacts. In effect, when counting de-       system that keeps all contacts closed, one has one more ad-
grees of freedom for packings, we count the density ␾ 共i.e.,       ditional force-equilibrium equation in Eq. 共7兲 that has the
the possible collective rescaling of the particle shapes neces-    pressure p on the right hand side. Mathematically, the pres-
sary to maintain contacts兲 as a single degree of freedom, as       sure is the conjugate 共dual兲 variable of the density 共viewed as
discussed further in Sec. IV A 2.                                  a degree of freedom兲 关25兴.
                                                                       Various counting arguments related to force equilibrium
                         2. Static view                            constraints, starting with the seminal work of Maxwell, have
                                                                   appeared in the engineering literature on mechanical struc-
   The static perspective considers a packing rigid if it can      tures 关33兴. There are, however, some important differences
resolve any applied forces through interparticle ones. This is     between elastic structures and packings of hard particles.
sometimes referred to as “static rigidity,” to be contrasted       Most significantly, the non-negativity of the contact forces is
with “kinematic rigidity” as defined in the previous section.      an added condition, and it effectively adds +1 to the number
For hard particles, there is no scale for the forces, and so the   of contacts needed to ensure static rigidity, i.e., adds a single
actual magnitude of the forces does not matter, only the rela-     degree of freedom in various counting arguments. For clas-
tive magnitudes and the directions. The particles do not de-       sical structures of elastic bars, an isostatic framework is such
form, but can exert an arbitrary positive contact force.           that it has exactly as many bars, i.e., unknown internal bar
   Mathematically, we consider the existence of a solution to      forces, as there are force-equilibrium equations M = N f . That
the force-equilibrium equations                                    is, the rigidity matrix is square and the solution to the force-
                  Af = − B,    where f 艌 0,                 共7兲    equilibrium equations is f = −A−1B. Finding the internal
                                                                   forces therefore does not require knowing anything about the
for all resolvable external loads B. The space of resolvable       specific elastic properties of the bars: the structure is stati-
loads is determined by the boundary conditions: certain            cally determinate 关34兴. Reference 关8兴 defines “isostatic struc-
forces such as pulling on the walls of a container cannot be       tures” as “such that all problems are isostatic, whatever the
resolved by any packing and need to be excluded. This is           choice of the load. More precisely, one requires all loads
similar to the definition used in Ref. 关7兴: A packing is me-       orthogonal to the overall rigid body degrees of freedom to be
chanically stable “if there is a nonzero measure set of exter-     supportable with a unique determination of internal forces.”
nal forces which can be balanced by interbead ones.” The               On the other hand, a jammed isoconstrained packing, as
problem with this definition of rigidity and in particular Eq.     we have defined it, has M = N f + 1 contacts, and the additional
共7兲 is that it does not take into account the fact that the        one contact is needed in order to ensure that any applied load

                                                             051304-11
DONEV et al.                                                                             PHYSICAL REVIEW E 75, 051304 共2007兲

can be resolved by non-negative interparticle forces in the        we look for solutions of the coupled system of equations of
active contact network. Assuming the existence of 共infinitesi-     preserving contacts and maintaining force equilibrium:
mally兲 small but positive interparticle gaps, under certain
mild non-degeneracy conditions, it can be demonstrated that                        关A共Q + ⌬Q兲兴共f + ⌬f兲 = − ␧⌬B,
if one applies a specific load only N f of the contacts will
actually be active, and one contact will be broken and will                          ␨共Q + ⌬Q兲 − ⌬␨␮ = − ␧⌬␨
carry no force. Different contacts will be broken for different
loads, however, once it is known which contact is broken                                      eT⌬f = 0,                          共8兲
共see Sec. V D 1兲 the active contact network is isostatic in the    where ␧ ⬎ 0 is a small number and we have assumed f ⬎ 0.
classical structural mechanics sense and the forces can be         Note that in Ref. 关20兴, ⌬f are called the “basic statical un-
                    −1
determined, f = −Aactive B, without resorting to constitutive      knowns” and ⌬Q are called the “basic kinematical un-
elastic equations for the contacts. The additional contact ap-     knowns.”
pears because of our choice of definition of jamming; if one          Similarly to the external forces, the space of resolvable
considers stability under a single external load, then all the     gap perturbations is determined by the boundary conditions:
contacts will be active, M = N f . This difference has some        global expansions will lead to gaps that cannot all be closed
subtle effects that may lead to confusion when comparing to        unless the particles grow by a certain scaling factor ␮ = 1
previous results in the literature. For example, as we will see    + ⌬␮. It is therefore convenient to include ⌬␨␮ ⬇ 2⌬␮ as an
in Sec. V, ideal jammed packings posseses a nontrivial inter-      additional variable. An added constraint is that the normal-
nal stress, or self-stress f ⬎ 0, Af = 0. In elastic structures    ization eTf = M be maintained. It is important to note that we
such an internal stress is associated with overconstrained         explicitly account for the dependence of the rigidity matrix
共sub兲structures, and such stresses do not appear in unloaded       on the configuration in the force-balance equation. Notice
granular piles. The fact that we observe only a single self-       that when we combine perturbations of the geometry and
stress for packings means that upon removal of any contact         forces together, the total number of variables is M + N f , and
from the packing there will no longer be self-stresses left,       the total number of constraints is also M + N f 共here we in-
i.e., the system will no longer be overconstrained.                clude the global particle rescaling ⌬␨␮ as a degree of free-
    Note that a positive internal 共self兲 stress does appear in     dom兲. Therefore there are no underdetermined 共linear兲 sys-
glasses under a uniform external pressure 关28兴, and in those       tems as found in counting arguments that consider geometry
systems indeed all N f + 1 contacts are active and participate     and forces separately, as is typically done in the literature.
in the resolution of applied loads. The magnitude of the in-
ternal stresses is determined by the external pressure. For                                 B. Isocounting
high pressures, depending on the stiffness of the packing             In this section we will attempt to deconstruct previous
elements, additional active contacts may form as particles         arguments in justification of an isocounting conjecture,
deform and one would have to consider the constitutive elas-       mostly in the context of sphere packings, and try to identify
tic equations for the contacts in order to determine the inter-    the problems when the same arguments are applied to non-
particle forces.                                                   spherical particles. The isocounting conjecture 共property兲 is
                      3. Perturbation view                         usually justified in two steps. First, an inequality Z̄ 艋 2d f is
   The perturbation perspective considers a packing to be          demonstrated, then, the converse inequality Z̄ 艌 2d f is in-
stable if the structure of the packing changes smoothly for        voked to demonstrate the equality Z̄ = 2d f . We will demon-
small perturbations of the packing. In particular, the structure   strate that it is the second of these steps that fails for non-
of the packing includes the positions of the particles and the     spherical particles, however, first we recall some typical
contact force network. Perturbations to be considered should       justifications for the inequality Z̄ 艋 2d f . The observation that
include changes in the grain internal geometry 共deforma-           the inequality Z̄ 艌 2d f does not generally apply to nonspheri-
tion兲, strain, and stress 共external forces due to shaking, vi-     cal particles is already made by Roux in Ref. 关8兴, as we point
bration, or a macroscopic load兲. In great generality we can        out below. Roux also discusses the applicability of the con-
restrict our perturbations to small perturbations of the dis-
                                                                   verse inequality Z̄ 艋 2d f in significant detail; here we present
tances between contacting particles combined with small
                                                                   our own summary for completeness.
perturbations of the applied forces. Such a perspective on
                                                                      It is important to note that the arguments supporting the
jamming was recently presented in Ref. 关20兴. In this work,
however, only perturbations of the applied forces were con-        inequality Z̄ 艌 2d f given below apply only to cohesionless
sidered. However, it is realized in Ref. 关20兴 that deformations    particles, that is, particles for which only compressive inter-
of the boundary conditions can easily be incorporated with-        particle contact forces are allowed. In fact, stable packings of
out changing the stability conditions. In fact, arbitrary exter-   adhesive 共frictionless兲 particles stability can be hypocon-
nal perturbations of the geometry of the contacts can be con-      strained 关8兴, further reinforcing our criticism of a generally
sidered in addition to the applied load perturbations without      applicable isocounting conjecture.
any significant complication.                                                           1. Why Z̄ Ï 2df applies
   Mathematically, we consider the sensitivity of the con-
figuration and force chains to all perturbations of the inter-        A packing with Z̄ ⬎ 2d f is overconstrained, and in a cer-
particle gaps ⌬␨ and applied forces ⌬B away from zero, i.e.,       tain sense geometrically degenerate and thus not “random.”

                                                             051304-12
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                        PHYSICAL REVIEW E 75, 051304 共2007兲

It can be argued that such a packing is not stable against
small perturbations of the packing geometry, since all con-
tacts cannot be maintained closed without deforming some
of the particles. For example, Tkachenko and Witten 关7兴 con-
sider hard-sphere packings with a small polydispersity, so
that particles have slightly different sizes, to conclude that
“the creation of a contact network with coordination number
higher than 2d occurs with probability zero in an ensemble
of spheres with a continuous distribution of diameters.”
Moukarzel 关6,35兴 considers how the actual stiffness modulus
of deformable particles affects the interparticle forces and
concludes that making the particles very stiff will eventually
lead to negative forces and thus breaking of contacts, until
the remaining contact network has Z̄ 艋 2d f 关36兴: “The contact
network of a granular packing becomes isostatic when the
stiffness is so large that the typical self-stress … would be           FIG. 5. 共Color online兲 A mobile ellipse 共green兲 jammed between
much larger than the typical load-induced stress … granular         three fixed ellipses 共yellow兲. All ellipses are of the same size and
packings will only fail to be isostatic if the applied compres-     have an aspect ratio ␣ = 2. This packing was produced by a
sive forces are strong enough to close interparticle gaps es-       Lubachevsky-Stillinger–type algorithm, where the three particles
tablishing redundant contacts.” A similar argument is made          were kept fixed by giving them infinite mass and no initial veloci-
by Sir Edwards in Ref. 关9兴 for frictional grains: “if z ⬎ 4 then    ties. The normal vectors at the points of contact intersect at a com-
there is a solution with no force on z − 4 contacts, and there is   mon point I, as is necessary to achieve torque balance. For the
no reason why other solutions would have validity.”                 corresponding disk example, shown in Fig. 7, the number of force
    These arguments apply also to nonspherical particles,           balance constraints is two, while the number of unknown forces is
however, it is important to point out that they specifically        three. For the ellipse case the number of unknown forces is the
only apply to truly hard-particle packings or to packings           same, while the number of force balance constraints is two, and the
of deformable particles in the limit of zero applied pressure       number of torque constraints is one, giving a total of three equilib-
共f → 0兲. In real physical systems particles will have a finite      rium constraints. However, due to the geometric degeneracy, there
                                                                    are only two independent equations of mechanical equilibrium; the
stiffness and the applied forces will be non-negligible, and
                                                                    torques are always balanced. In the notation described in Sec.
such packings will have more contacts than the idealized
                                                                    V A 2, for the ellipse example above Nstresses = Nfloppy = 1, while for
hard-particle construction.                                         the corresponding disk case, Nstresses = 1 but Nfloppy = 0.

                 2. Why Z̄ Ð 2df does not apply                     shows that the argument in Ref. 关6兴, namely, that the mini-
    The converse inequality, stating that a minimum of M            mum number of contacts needed for a packing of N spheres
                                                                    in d dimensions to be rigid is dN, cannot be generalized to
= N f + 1 contacts is necessary for jamming 共rigidity兲, does not
                                                                    nonspherical particles by simply replacing d with d f . Claims
apply to nonspherical particles. We can demonstrate this viv-
                                                                    that the number of constraints must be larger than the num-
idly with a simple example of an ellipse jammed between
                                                                    ber of degrees of freedom have been made numerous times
three other stationary 共fixed兲 ellipses, as shown in Fig. 5.
                                                                    within the kinematic perspective on jamming, for example,
This example was also given in Ref. 关37兴, however, a de-
                                                                    in Ref. 关9兴. Our careful analysis of the conditions for jam-
tailed explanation was not provided.
                                                                    ming in the next section will elucidate why this is correct for
    Jamming a disk requires at least three touching disks; the
                                                                    spheres but not necessarily correct for nonspherical particles,
additional rotational degree of freedom of the ellipse would
                                                                    and under what conditions a hypoconstrained packing can be
seem to indicate that four touching ellipses would be needed
                                                                    jammed.
in order to jam an ellipse. However, this is not true: if the
                                                                        The example in Fig. 5 is a geometrically degenerate con-
normal contact vectors intersect at a single point, three el-
                                                                    figuration which would usually be dismissed as a
lipses can trap another ellipse, as shown in Fig. 5. We will
                                                                    probability-zero configuration. However, we will explain in
shortly develop tools that can be used to demonstrate rigor-
                                                                    later sections why such apparently nongeneric 共degenerate兲
ously that this example is indeed jammed. Another simple
                                                                    configurations must appear for sufficiently small aspect ra-
example demonstrating that Z̄ 艌 2d f does not apply is the          tios for a variety of realistic packing protocols. In Ref. 关33兴
rectangular lattice of ellipses, which is collectively jammed       geometrically peculiar examples such as this one are pre-
even though Z̄ = 4, the minimum necessary even for discs.           sented, however, they are considered to be in unstable equi-
This example is discussed in the Appendix, where we also            librium, i.e., stable only under special types of loading. This
demonstrate that, in fact, any isostatic packing of spheres can     type of argument, made within the static perspective on jam-
be converted into a jammed packing of nonspherical par-             ming 关see Eq. 共7兲兴, is given in the context of granular mate-
ticles.                                                             rials in Ref. 关7兴: “The number of equilibrium equations Nd
    The above example shows that the claim of Ref. 关10兴 that        should not exceed the number of force variables Nc; other-
“One requires 4共=3 + 1兲 contacts to fix the DOF 关degrees of         wise these forces would be overdetermined.” The example in
freedom兴 … of an ellipse in the plane” is wrong. Similarly, it      Fig. 5 demonstrates why this argument cannot be applied to

                                                              051304-13
DONEV et al.                                                                                 PHYSICAL REVIEW E 75, 051304 共2007兲

nonspherical grains. Since the normal vectors at the points of            A packing is first-order jammed if and only if there are no
contact intersect at a point, a torque around that point cannot        共nontrivial兲 first order flexes. A packing is first-order flexible
be resolved by any set of normal forces between the par-               if there exists a strict first-order flex. Some packings are
ticles. Yet the packing is jammed, and if built in the labora-         neither first-order jammed nor first-order flexible; one must
tory it will resist the torque by slight deformations of the           consider higher-order terms to access whether such packings
particles, so that the normal vectors no longer intersect in           are jammed, and if they are not, to identify an unjamming
one point and the contact forces can resist the applied torque.        motion. We will consider the second-order terms later; in this
The connection between the geometry of the contact net-                section we develop conditions and algorithms to verify first-
work, i.e., A, and the packing configuration Q, as well as the         order jamming and identify first-order flexes if they exist.
pre-existing stresses 共forces兲 in the packing, must be taken           The algorithms are closely based on work in Ref. 关11兴.
into account when considering the response of hypocon-
                                                                                              1. Strict self-stresses
strained packings to external perturbations. This important
observation was also recently pointed out independently in                Let us first focus on a single contact 兵i , j其, and ask
Ref. 关20兴, and we elaborate on it in the next section.                 whether one can find a first-order flex that is strict on that
                                                                       contact, i.e.,

               V. CONDITIONS FOR JAMMING                                         ␨˙ ij = 共ATQ̇兲ij = 共ATQ̇兲Teij = 共Aeij兲TQ̇ ⬎ 0,
    In this section we develop first- and second-order condi-          where eij denotes a vector that has all zero entries other than
tions for jamming, using a kinematic approach. Statics                 the unit entry corresponding to contact 兵i , j其. If it exists, such
共forces兲 will emerge through the use of duality theory. The            a flex can be found by solving the linear program 共LP兲
discussion here is an adaptation of the theory of first-order,
prestress, and second-order rigidity developed for tensegri-                                     max共Aeij兲TQ̇
                                                                                                   ˙
ties in Ref. 关12兴. This section is technical and may be                                            Q

skipped or skimmed by readers not interested in the math-
ematical formalism of jamming. In Sec. VIII the rigorous                                           ATQ̇ 艌 0.                         共10兲
hard-particle results are explained more simply by consider-
ing the conditions for local 共stable兲 energy minima in soft-           If this LP has optimal objective value of zero, then there is
particle systems.                                                      no first-order flex that is strict on the contact in question.
    We consider an analytic motion of the particles                    Otherwise, the LP is unbounded, with an infinite optimal
                                                                       objective value. The dual LP of Eq. 共10兲 is a feasibility prob-
                                      t2                               lem
                   ⌬Q共t兲 = Q̇t + Q̈      + O共t3兲,
                                      2
                                                                                                 A共f̃ + eij兲 = 0
where Q̇ are the velocities, and Q̈ are the accelerations. Ex-
panding the distances between touching particles to second-                                            f̃ 艌 0,                       共11兲
order, and taking into account that ␨共QJ兲 = 0, gives
                                                                       where the contact forces f̃ are the Lagrange multipliers cor-
                                       t2          t2
         ␨共t兲 ⬇ A Q̇t + 关Q̇ HQ̇ + A Q̈兴 = ␨˙ t + ␨¨ ,
                   T         T          T
                                                                共9兲    responding to the impenetrability constraints ATQ̇ 艌 0. If the
                                       2           2                   dual LP 共11兲 is feasible, then the primal LP 共10兲 is bounded.
where the Hessian H = ⵱2Q␨ = ⵱QA can be thought of as a                If we identify f = f̃ + eij 艌 0, f̃ ij 艌 1, we are naturally led to
higher-rank symmetric matrix.                                          consider the existence of nontrivial solutions to the force-
                                                                       equilibrium equations

                       A. First-order terms                                                   Af = 0 and f 艌 0.                      共12兲
                                                                          A set of non-negative contact forces f ⫽ 0 that are in equi-
   Velocities Q̇ ⫽ 0 for which ␨˙ = ATQ̇ 艌 0 represent a first-
                                                                       librium as given by Eq. 共12兲 is called a “self-stress”关38兴. In
order flex 共using the terminology of Ref. 关12兴兲. If we can find
                                                                       Ref. 关12兴 these are called “proper self-stresses,” as opposed
an unjamming motion Q̇ such that ␨˙ ⬎ 0 共note the strict in-           to self-stresses which are not required to be non-negative.
equality兲, then the packing is first-order flexible, and there         Self-stresses can be scaled by an arbitrary positive factor, so
exists a T ⬎ 0 such that none of the impenetrability condi-            we will often add a normalization constraint that the average
tions 关see Eq. 共6兲兴 are violated for 0 艋 t ⬍ T. We call such a Q̇      force be unity, eTf = M. A self-stress that is strictly positive on
a strict first-order flex. If, on the other hand, for at least one     a given contact is strict on that contact. A self-stress f ⬎ 0 is
constraint ␨˙ ⬍ 0 for every Q̇, then the packing is jammed,            a strict-self stress. The existence of a 共strict兲 self-stress can
since every nontrivial movement of the particles violates              be tested by solving the linear program
some impenetrability condition for all 0 ⬍ t ⬍ T for some T
                                                                                                       max ␧,
⬎ 0. We call such a packing “first-order jammed.” Finally, a                                            f,␧
Q̇ such that ␨˙ = 0 is a null first-order flex, often referred to as
zero or floppy mode in the physics literature.                                                         Af = 0,

                                                                 051304-14
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                         PHYSICAL REVIEW E 75, 051304 共2007兲


                             f 艌 ␧e,                                  stress and a rigidity matrix of full-rank is 共first-order兲
                                                                      jammed. We will later show that this sufficient condition for
                             e Tf = M                         共13兲    jamming is also necessary for sphere packings, that is,
                                                                      jammed sphere packings are never hypoconstrained.
and seeing whether the optimal value is negative 共no self-               However, we will see that jammed ellipsoid packings may
stress exists兲, positive 共a strict self-stress exists兲, or zero 共a    be hypoconstrained, M ⬍ N f + 1. Such a hypoconstrained
self-stress exists兲. What we showed above using linear dual-          packing always has floppy modes,
ity is that if there is a self stress that is strict on a given
contact, there is no flex strict on that contact. In particular,                 Nfloppy = N f + Nstresses − M 艌 N f + 1 − M .
this means that packings that have a strict self-stress can only      Every floppy mode can be expressed as a linear combination
have null first-order flexes.                                         of a set of Nfloppy basis vectors, i.e.,
    We can also show that there is a first-order flex that is
strict on all contacts that do not carry a force in any self-                                Q̇ = Vx for some x,                   共16兲
stress 共i.e., no self-stress is strict on them兲. To this end, we
                                                                                                                                  T
look for a first-order flex that is strict on a given subset of the   where the matrix V is a basis for the null-space of A . To
contacts, as denoted by the positions of the unit entries in the      determine whether any of the null first-order flexes can be
vector ẽ                                                             extended into a true unjamming motion, we need to consider
                                                                      second-order terms, which we do next.
                             max ␧,
                              ˙ ,␧
                              Q                                                            B. Second-order terms

                                                                         Consider a given null first-order flex ATQ̇ = 0. We want to
                           ATQ̇ 艌 ␧ẽ.                        共14兲
                                                                      look for accelerations Q̈ that make the second-order term in
The dual program is the feasibility problem                           the expansion 共9兲 non-negative, i.e.,
                             Af = 0,                                                          ATQ̈ 艌 − Q̇THQ̇.                     共17兲

                             ẽTf = 1,                                If we cannot find such a Q̈ for any first-order flex, then the
                                                                      packing is second-order jammed. If we find a Q̈ such that all
                              f 艌 0,                          共15兲    inequalities in Eq. 共17兲 are strict, than we call the unjamming
which is infeasible if there is no self-stress that is positive on    motion 共Q̇ , Q̈兲 a strict second-order flex, and the packing is
at least on the contacts under consideration, since ẽTf ⬅ 0.         second-order flexible, since there exists a T ⬎ 0 such that
Therefore the primal problem 共13兲 is unbounded, that is, one          none of the impenetrability conditions 关see Eq. 共6兲兴 are vio-
can find a self-stress that is strict 共since ␧ → ⬁兲 on the given      lated for 0 艋 t ⬍ T. If for all first-order flexes Q̇ at least one
set of contacts. This shows that packings that do not have a          of the inequalities in Eq, 共17兲 has to be an equality, then we
self-stress are first-order flexible. In other words, the exis-       need to consider even third-or higher-order terms, however,
tence of force chains in a packing is a necessary criterion for       we will see that for sphere and ellipsoid packings this is not
jamming.                                                              necessary.
   In summary, if a packing has no self-stress, it is not
                                                                                             1. The stress matrix
jammed, and one can easily find a strict first-order flex by
solving a linear program 关11兴. The analysis is simplified if             In order to find a strict second-order flex, we need to solve
the packing has a strict self-stress, since in that case all first-   the LP
order flexes are null, i.e., they are solutions of a linear system
                                                                                                    max ␧
of equalities ATQ̇ = 0. This is the case of practical importance                                     ¨ ,␧
                                                                                                     Q
to jammed packings, so we will focus on it henceforth.

                         2. Floppy modes
                                                                                           ATQ̈ 艌 ␧e − Q̇THQ̇,                     共18兲
                                                                      the dual of which is
   The linear system ATQ̇ = 0 has Nfloppy = N f − r solutions,
where r = M − Nstresses is the rank of the rigidity matrix, and
                                                                                              min 共Q̇THQ̇兲Tf,
Nstresses is the number of 共not necessarily proper兲 self-stresses                               f
共more precisely, the dimensionality of the solution space of
Af = 0兲. We know that Nstresses 艌 1 for a jammed packing. If                                        Af = 0,
the packing is not hypoconstrained, or more precisely, if the
number of contacts is sufficiently large
                                                                                                    eTf = 1,
                  M = N f + Nstresses 艌 N f + 1,
                                                                                                    f 艌 0,                         共19兲
then there are no nontrivial null first-order flexes 共floppy
modes兲, Nfloppy = 0. Therefore, a packing that has a strict self-     where the common optimal objective function is

                                                                051304-15
DONEV et al.                                                                                  PHYSICAL REVIEW E 75, 051304 共2007兲


            ␧* = 共Q̇THQ̇兲Tf = Q̇T共Hf兲Q̇ = Q̇THQ̇,                     space of floppy modes, and this general case of a second-
                                                                      order jammed packing is difficult to test for algorithmically.
where H = Hf is a form of reduced Hessian that incorporates           In our study of disordered sphere and ellipsoid packings, we
information about the contact force and the curvature of the          will see that in practice the jammed packings only have one
touching particles. The 关N f ⫻ N f 兴 matrix H plays an essential      strict self-stress. In this case, testing for jamming reduces to
role in the theory of jamming for hypoconstrained ellipsoid           calculating the smallest eigenvalue of HV. We will discuss
packing and we will refer to it as the stress matrix following        actual numerical algorithms designed for ellipsoid packings
Ref. 关12兴.                                                            in subsequent sections, but first we explain what makes
    The stress-matrix has a special block structure, where all        sphere packings special.
of the blocks are of size 关d f ⫻ d f 兴, and both the block-rows
and the block-columns correspond to particles. The block                            2. The stress matrix for hard spheres
entry corresponding to the pair of particles 共i , j兲 is nonzero if
                                                                         For hard spheres it is easy to write down the explicit form
and only if there is a contact between them. Written explic-          for Hij since the overlap function is given explicitly by Eq.
itly, the stress matrix is a force-weighted sum of contribu-          共4兲 and its second-order derivatives are trivial,
tions from all the contacts
                                                                                                                              2Id
                             H = 兺 f ijHij ,                                 ⵱2iiFij = ⵱2jjFij = − ⵱2ijFij = − ⵱2jiFij =               ,
                                     兵i,j其
                                                                                                                           共Oi + O j兲2

where the contribution from a given contact 兵i , j其 is                where Id is the 关d ⫻ d兴 identity matrix. This implies that Hij
                                                                      is a positive-definite matrix, since
                             i        ¯        j,
                                                                                      ṘTHijṘ = 共ṙi − ṙ j兲T共ṙi − ṙ j兲 艌 0.
                             ↓         ¯        ↓,
                                                                      Therefore, any first-order flex in fact represents a true unjam-
                                                                      ming motion, since Q̇THQ̇ 艌 0 and we can trivially use Q̈

                       冤                               冥
                  i→       ⵱2ii␨ij    ¯      ⵱2ji␨ij
                                                                      = 0 in Eqs. 共18兲. In other words, a sphere packing is jammed
           Hij = ]           ]                ]           .   共20兲   if and only if it is first-order jammed, and therefore it cannot
                  j→       ⵱2ij␨ij    ¯      ⵱2jj␨ij                  be hypoconstrained. To test for jamming in hard-sphere
                                                                      packings we need only focus on the velocities of the sphere
    If Q̇THQ̇ ⬍ 0 then ␧* ⬍ 0 and therefore the first-order flex      centroids and associated linear programs in Sec. V A. This
Q̇ cannot be extended into a second-order flex. We say that           important conclusion was demonstrated using a simple cal-
                                                                      culation in Ref. 关11兴.
the stress matrix blocks the flex Q̇. If, on the other hand,
                                                                          For general particle shapes, however, Hij may be indefi-
Q̇THQ̇ ⬎ 0, then ␧* ⬎ 0 and by solving the LP 共18兲 we can             nite for some contacts, and testing for jamming may require
find an unjamming motion, i.e., the packing is second-order           considering second-order terms. If one considers general
flexible. Therefore, finding an unjamming motion at the               convex particle shapes but freezes the orientations of the
second-order level essentially consists of looking for a null         particles, the packing will behave similar to a hard-sphere
first-order flex 共floppy mode兲 Q̇, ATQ̇ = 0, that is also a posi-     packing. In particular, a jammed packing of nonspherical
tive curvature vector for the stress matrix.                          particles must have at least as many contacts as the corre-
    Recalling that every floppy mode can be expressed as Q̇           sponding isoconstrained packing of spheres would, that is
= Vx 关see Eq. 共16兲兴, we see that
                                                                                                     Z̄ 艌 2d
                Q̇THQ̇ = xT共VTHV兲x = xTHVx.
                                                                      for any large jammed packing of convex hard particles.
If the matrix HV is negative definite, than the packing is
second-order jammed. In Ref. 关12兴 such packings are called
                                                                                            C. Testing for jamming
prestress stable, since the self-stress f rigidifies the packing
共i.e., blocks all of the floppy modes兲. If HV is indefinite, than        We now summarize the theoretical conditions for jam-
the packing is second-order flexible since any of the positive-       ming developed in this section in the form of a procedure for
curvature directions can be converted into a strict self-stress       testing whether a given packing of nonspherical particles is
by solving the LP 共18兲.                                               jammed. We assume that the contact network of the packing
    If a packing has more than one 共proper兲 self-stress, than it      is known and available as input. For spherical particles, as
is not clear which one to use in the stress-matrix. One can try       already discussed, second-order terms never need to be con-
to find a self-stress that provides for jamming 共prestress sta-       sidered, and testing for jamming can be done by solving one
bility兲 by looking for a solution to Eq. 共13兲 such that HV            or two linear programs, as discussed in detail in Ref. 关11兴. In
Ɐ 0 共i.e., HV is negative-semidefinite兲. This is known as             the formulation below, we avoid solving linear programs un-
semidefinite programming 共SDP兲, and is a powerful gener-              less necessary, but rather use basic linear algebra tools when-
alization of linear programming that has received lots of at-         ever possible.
tention recently 关39兴. It is, however, possible that different           共1兲 Find a basis F for the null-space of the rigidity matrix
self-stresses are needed to block different portions of the           A, i.e., find Nstresses linearly independent solutions to the lin-

                                                                051304-16
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                                 PHYSICAL REVIEW E 75, 051304 共2007兲

ear system of equations Af= 0, normalized to mean of unity.                  The addition of arbitrary multiples of the self-stress to f
This can be done, for example, by looking for zero eigenval-             is, however, a product of the mathematical idealization of the
ues and the associated eigenvectors of the matrix ATA. If 共a兲            packing. In fact, each specific applied load in an isocon-
Nstresses = 0, 共b兲 Nstresses = 1 but the unique self-stress is not       strained packing with M = N f + 1 contacts will be supported
non-negative, or 共c兲 Nstresses ⬎ 1 but the linear feasibility pro-       by a well-defined f. The self-stress is only physical if all
gram 共13兲 is infeasible, then declare the packing not jammed             N f + 1 contacts are active, which requires that the packing
共first-order flexible兲, optionally identify an unjamming mo-             already be compressed by some pre-existing applied load.
tion by solving the linear feasibility program ATQ̇ 艌 e, and             Otherwise, the density will be slightly smaller than the jam-
terminate the procedure. Otherwise, if the identified self-              ming density and upon application of an external load one of
stress f is not strict, declare the test inconclusive and termi-         the contacts will break and only N f of the contacts will be
nate.                                                                    active. In general, finding the active set of contacts requires
    共2兲 If Nfloppy = N f + Nstresses − M = 0, then declare the packing   solving the linear program 关11兴
共first-order兲 jammed and terminate the procedure. Otherwise,                                 min eTf for virtual work
find a basis V for the null-space of AT, i.e., Nfloppy linearly                                  f
independent solutions to the linear system of equations
AT⌬Q = 0. Compute the stress matrix H using the                                       such that Af = − B for equilibrium
previously-identified strict self-stress f, and compute its pro-
jection HV on the space of null first-order flexes.
                                                                                             f 艌 0 for repulsion only.              共21兲
    共3兲 Compute the smallest eigenvalue ␭min and associated
eigenvector xmin of the matrix HV. If ␭min ⬍ 0, declare the              At the solution, modulo degenerate situations, only N f of the
packing 共second-order兲 jammed and terminate the procedure.               forces will be positive, the remaining ones will be zero.
If ␭min ⬎ 0 and Nstresses = 1 declare the packing not jammed                For jammed hypoconstrained ellipsoid packings, such as
共second-order flexible兲, optionally compute an unjamming                 the one in Fig. 5, supporting some loads may require a small
motion by solving the LP 共18兲 with Q̇ = Vxmin, and terminate             deformation of the packing, such as a slight rotation of the
the procedure. Otherwise, declare the test inconclusive and              mobile ellipse in the example in Fig. 5. After this small de-
terminate.                                                               formation, the normal vectors at the points of contact will
    We will discuss the actual numerical implementation of               change slightly and the interparticle forces f can support the
this algorithm later, and see that in practice we do not need to         applied force B. The larger the magnitude of the forces is,
solve linear programs to test for jamming in hypoconstrained             the smaller the deformation needed to support the load is.
ellipsoid packings. Essentially, the packings we encounter in            Therefore every jammed packing can support any applied
our work with disordered packings of hard ellipsoids always              force in a certain generalized sense. Another way to look at
have a single strict self-stress and a negative-definite HV. The         this is to observe that, if the interparticle forces are much
rectangular lattice of ellipses offers a different kind of ex-           larger than the applied ones, the applied load will act as a
ample, namely, one with simple regular geometry but mul-                 small perturbation to the packing and the static view be-
tiple self-stresses, and we analyze this example theoretically           comes equivalent to the perturbation view 共with ⌬␨ = 0兲. We
in the Appendix.                                                         consider the perturbation view next and show how the stress
                                                                         matrix appears in the response of the packing to perturba-
                                                                         tions.
              D. Outside the kinematic perspective
                                                                                                     2. Perturbation view
   It is worthwhile to briefly consider the connections be-
tween the jamming criteria developed above using the kine-                  In the perturbation view we consider how the configura-
matic approach to jamming, and the static and perturbation               tion and the contact forces respond to perturbations consist-
approaches.                                                              ing of small changes of the contact geometry and small ap-
                                                                         plied forces. Counting geometric and force constraints
                           1. Static view                                separately, as done in the literature, is incorrect when f ⬎ 0:
                                                                         There is coupling between the particle positions and the in-
   We have already seen that forces appear naturally as                  terparticle forces as represented by the Hessian H = Hf.
Lagrange multipliers corresponding to impenetrability con-                  With this in mind, we can expand Eq. 共8兲 to first order in
straints, in the form of a strict self-stress f ⬎ 0. In the static       兵储⌬Q储 , 储⌬f储其, to get the linear system of equations
view, we ask whether a packing can support a given applied


                                                                                     冤                        冥冤 冥 冤 冥
external force B by a set of non-negative interparticle forces.                          A −H            0     ⌬f       ⌬B
The key observation is that we can add an arbitrary positive                             0   AT        − 2e    ⌬Q = − ␧ ⌬␨ .        共22兲
multiple of a self-stress to any set of interparticle forces that
                                                                                         e   0           0     ⌬␮        0
support B in order to make them non-negative, without af-
fecting force balance. Therefore, if the rigidity matrix A is of         It can be demonstrated that if the reduced Hessian HV is
full rank, as it has to be for jammed sphere packings, any               definite, this system will have a solution for any ⌬B and ⌬␨.
共supportable兲 load B can be balanced with non-negative in-               Furthermore, if HV is negative-definite the response to per-
terparticle forces, and kinematic and static rigidity become             turbations will be stable, in the sense that applied forces will
equivalent 关40兴.                                                         do a positive work in order to perturb the packing. This is

                                                                   051304-17
DONEV et al.                                                                               PHYSICAL REVIEW E 75, 051304 共2007兲

explained in greater detail in Ref. 关20兴, where the conditions                   rC = rA + 共1 − ␭兲XA−1n = rB − ␭XB−1n,                 共26兲
储⌬Q储 = O共储⌬B储兲 and ⌬BT⌬Q ⬍ 0 are stated in a more general
setting, and then a linearization of the response of the pack-     where
ing to perturbations is considered 共recall that in Ref. 关20兴
⌬␨ ⬅ 0兲.                                                                                          n = Y−1rAB                           共27兲
   Equation 共22兲 can be used to find the jamming point start-      is the un-normalized common normal vector at the point of
ing with a packing that is nearly jammed, i.e., a packing that     contact.
has nonzero interparticle gaps ␧⌬␨ and a self-stress that has          In principle the overlap potential is a function of the nor-
a small imbalance ␧⌬B = Af. This works well for small pack-        malized quaternions describing the particle orientations, and
ings, however, for large disordered packings, the force chains     derivatives of ␨ need to be projected onto the unit quaternion
are very sensitive to small changes in the geometry and the        sphere. This projection can be avoided if we do not do a
linearization of the perturbation response is not a good ap-       traditional Taylor series in the quaternions, namely, an addi-
proximation even for packings very close to the jamming            tive perturbation ⌬q, but rather consider a multiplicative per-
point. Additionally, we note that to first order in ␧, the solu-   turbation to the quaternions in the form of a small rotation
tion to Eq. 共22兲 has ⌬␮ / ␧ = fT⌬␨ / 2M = fETh / 2M, which can     from the current configuration ⌬␸.
be used to quickly estimate the jamming gap of a nearly
jammed packing from just the interparticle gaps ⌬␨ = ␨ and                               1. First-order derivatives
the interparticle forces, without knowing the actual jamming
point 关2兴.                                                            The gradient of the overlap potential, which enters in the
                                                                   columns of the rigidity matrix, can be shown to be
    VI. NUMERICALLY TESTING FOR JAMMING IN
     HYPOCONSTRAINED ELLIPSOID PACKINGS

   In this section we will apply the criteria for jamming and
                                                                           ⵱ B␨ = − ⵱ A␨ =   冋 册
                                                                                             ⵱ rB␨
                                                                                             ⵱ ␸B␨
                                                                                                        = 2␭共1 − ␭兲    冋      n
                                                                                                                           rBC ⫻ n
                                                                                                                                   册
                                                                                                                                   ,

the algorithm to test for jamming from Sec. V C to our com-        as we derived in Sec. III A 1 for a general convex particle
putationally generated hypoconstrained packings of ellip-          shape by using the normalized normal vector n̂ = n / 储n储 关note
soids. This section is technical and may be skipped or             that ␨ = ␭共1 − ␭兲rAB
                                                                                     T
                                                                                        n − 1 = 0兴. Additionally, it is useful to know
skimmed by readers not interested in the mathematical for-         the derivatives of ␭,
malism of jamming. The numerical results show that the
packings are indeed second-order jammed, even very close                                                   2
                                                                                             ⵱ rB␭ = −           ñ,
to the sphere point. Before discussing the numerical details                                              f ␭␭
of the algorithm, we need to calculate the first and second-
order derivatives of the overlap potential for ellipsoids.         where

                                                                                                 rT Y−1rAC
               A. Overlap potentials for ellipsoids                                      f ␭␭ = 2 BC       ⬍ 0,
                                                                                                  ␭共1 − ␭兲
   Numerical algorithms for calculating the PW overlap po-
tential ␨ = ␮2 − 1 for ellipsoids are presented in the second
part of Ref. 关15兴. Here we review the essential notation and               ñ = ␭nB + 共1 − ␭兲nA = ␭Y−1rAC + 共1 − ␭兲Y−1rBC
give the first and second-order derivatives of the overlap po-
                                                                   and
tential, necessary to build the rigidity and stress matrices for
a given packing.                                                                              2
   An ellipsoid is a smooth convex body consisting of all                        ⵱ ␸B␭ = −          关MBnA − ␭共rBC ⫻ n兲兴,
                                                                                             f ␭␭
points r that satisfy the quadratic inequality
                    共r − r0兲TX共r − r0兲 艋 1,                共23兲    where

where r0 is the position of the center 共centroid兲, and X is a                             MB = ␭NLXB−1 + RCB
                                                                                                          L
                                                                                                             .
characteristic ellipsoid matrix describing the shape and ori-
entation of the ellipsoid
                                                                                        2. Second-order derivatives
                                T
                         X = Q O Q, −2
                                                           共24兲       The explicit expressions for the Hessian of the overlap
where Q is the rotational matrix describing the orientation of     potential are
the ellipsoid, and O is a diagonal matrix containing the major
semi-axes of the ellipsoid along the diagonal. Consider two                                                     4
                                                                                 ⵱r2 ␨ = 2␭共1 − ␭兲Y−1 −             共ññT兲 Ɑ 0,
ellipsoids A and B and denote                                                      B                           f ␭␭

                    Y = ␭XB−1 + 共1 − ␭兲XA−1 ,              共25兲
                                                                              ⵱␸2 r ␨ = 2␭共1 − ␭兲MBY−1 + 2关共⵱␸B␭兲ñT兴
                                                                                  B B
where ␭ is defined in Sec. III. The contact point rC of the two
ellipsoids is                                                      and finally

                                                             051304-18
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                           PHYSICAL REVIEW E 75, 051304 共2007兲


     ⵱␸2 ␨ = − f ␭␭关共⵱␸B␭兲共⵱␸B␭兲T兴                                        ing in collisions as well as average the total transfer of col-


                           再冋                                   册
        B
                                                                          lisional momentum between them in order to obtain the
                                 1                                        共positive兲 contact forces 关2兴.
             + 2␭共1 − ␭兲           共rBCnT + nrBC
                                              T
                                                 兲 − 共rBC
                                                       T
                                                          n兲I
                                 2                                            Once the contact network is identified, we want to look

             + ␭NLXB−1NR + MBY−1MBT .          冎                          for null vectors of the rigidity matrix. This can be done using
                                                                          specialized algorithms that ensure accurate answers 关42兴,
                                                                          however, we have found it sufficient in practice to simply
                                                                          calculate the few smallest eigenvalues of the semi-definite
The derivatives with respect to the position and orientation
                                                                          matrix ATA. We used MATLAB’s sparse linear algebra tools to
of particle A can be obtained by simply exchanging the roles
                                                                          perform the eigenvalue calculation 共internally MATLAB uses
of particles A and B, however, there are also mixed deriva-
                                                                          the ARPACK library, which implements the implicitly re-
tives involving motion of both particles
                                                                          started Arnoldi method兲. We consistently found that the
                       ⵱␸2 r ␨ = − ⵱␸2 r ␨                                smallest eigenvalue is about 3 − 6 orders of magnitude
                           B A           B B
                                                                          smaller than the second-smallest eigenvalue, indicating that
                                                                          there is a near linear-dependency among the columns of A in
                       ⵱␸2 r ␨ = − ⵱␸2 r ␨                                the form of a self-stress. The self-stress, which is simply the
                           A B           A A
                                                                          eigenvector corresponding to the near-zero eigenvalue, was
                                           1                              always strictly positive; in our experience, disordered pack-
         ⵱␸2 ␸ ␨ = − ⵱␸2 ␨ + 共⵱␸2 r ␨兲RAB
                                       R
                                          − 兩⵱␸B␨兩⫻ .                     ings of ellipsoids have a unique strict self-stress f. This
            B A         B        B B       2
                                                                          means that there are Nfloppy = N f + 1 − M solutions to AT⌬Q
The stress-matrix is built from these blocks as given in Eq.              = 0, N f − M of which are exact, and one which is approximate
共20兲, where each of the four blocks ⵱␣␤ 2
                                          ␨ 共␣ and ␤ denote               共corresponding to the approximate self-stress兲. This can be
either A or B兲 involves both translations and rotations,                  seen, for example, by calculating the eigenvalues of AAT,

                 ⵱␣␤
                  2
                     ␨=    冋    ⵱r2 ␨
                                   ␣

                               ⵱r2 ␸ ␨
                                  ␣ ␤
                                         ⵱␸2 r ␨
                                            ␣ ␤

                                          ⵱r2 ␨
                                               ␤
                                                   册   .
                                                                          since N f − M will be zero to numerical precision, one will be
                                                                          very small, and the remaining ones will be orders of magni-
                                                                          tude larger.
                                                                              Verification of second-order jamming. Once a strict self-
                                                                          stress is known, second-order jamming or flexibility can be
                                                                          determined by examining the smallest eigenvalue of HV,
              B. Numerically testing for jamming                          which requires finding a basis for the linear space of floppy
    The numerical implementation of the algorithm given in                modes. However, it is computationally demanding to find a
Sec. V C poses several challenges. The most important issue               basis for the null-space of AT due to the large number of
is that that algorithm was designed for ideal packings, that is,          floppy modes, and since sparsity is difficult to incorporate in
it was assumed that the true contact network of the packing               nullspace codes. There are algorithms to find sparse basis for
is known. Packings produced by the MD algorithm, although                 this null-space 关42兴, however, we have chosen a different
very close to jamming 共i.e., very high pressures兲, are not                approach.
ideal. In particular, it is not trivial to identify which pairs of            Namely, we calculate the smallest eigenvalues of
particles truly touch at the jamming point. Disordered pack-                                     Hk = kAAT − H,
ings have a multitude of near contacts that play an important
role in the rigidity of the packing away from the jamming                 which as we saw in Sec. VIII B is the Hessian of the poten-
point 关41兴, and these near contacts can participate in the                tial energy for a system of deformable ellipsoids where the
backbone 共force-carrying network兲 even very close to the                  stiffness coefficients are all k. For very large k 共we use k
jamming point. Additionally, not including a contact in the               = 106兲, any positive eigenvalue of AAT is strongly amplified
contact network can lead to the identification of spurious                and not affected by H, and therefore only the floppy modes
unjamming motions, which are actually blocked by the con-                 can lead to small eigenvalues of Hk, depending on how they
tact that was omitted in error.                                           are affected by H. We have found that MATLAB’s eigs func-
    For hard spheres, the algorithms can use linear program-              tion is not able to converge the smallest eigenvalues of Hk
ming to handle the inclusion of false contacts 关11兴. For ellip-           for large stiffnesses k, however, the convergence is quick if
soids, we look at the smallest eigenvalues of ATA, i.e., the              one asks for the eigenvalues closest to zero or even closest to
least-square solution to Af = 0. The solution will be positive            −1. This typically reveals any negative eigenvalues of Hk
if we have identified the true contact network, f ⬎ 0, but the            and the corresponding floppy modes.
inclusion of false contacts will lead to small negative forces                It is also possible to perform a rigorous numerical test for
on those false contacts. The problem comes about because                  positive-definiteness of Hk using properly rounded IEEE ma-
the calculation of the self-stress by just looking at the rigidity        chine arithmetic and MATLAB’s 共sparse兲 Cholesky decompo-
matrix does not take into account the actual proximity to                 sition of a numerically reconditioned Hk 关43兴. We have used
contact between the particles. One way to identify the true               the code described in Ref. 关43兴 to show that indeed for our
contact network of the packing is to perform a long molecu-               packings Hk Ɑ 0 and therefore the packings are second-order
lar dynamics run at a fixed density at the highest pressure               jammed. For spheroids, that is, ellipsoids that have an axes
reached, and record the list of particle neighbors participat-            of symmetry, there will be trivial floppy modes correspond-

                                                                    051304-19
DONEV et al.                                                                              PHYSICAL REVIEW E 75, 051304 共2007兲

ing to rotations of the particles around their own centroid.
These can be removed most easily by penalizing any com-
ponent of the particle rotations ⌬␸ that is parallel to the axis
of symmetry. For example, one can add to every diagonal
block of Hk corresponding to the rotation of an ellipsoid with
axes of symmetry u a penalization term of the form kuuT.
    We have not performed a detailed investigation of a very           FIG. 6. 共Color online兲 The feasible region around a jamming
wide range of samples since our goal here was to simply            point 共black circle兲 for two curved constraints in two dimensions
demonstrate that under appropriate conditions the packings         共black circles兲. The region of the plane forbidden by one of the
we generate using the modified Lubachevsky-Stillinger algo-        constraints is colored red and colored blue for the other constraint.
rithm are indeed jammed, even though they are very hypo-           The region forbidden by both constraints is purple. The distance
constrained near the sphere point. In this work we have given      from the jamming point to the constraints is approximately ␦ and
the fundamentals of the mathematics of jamming in these            chosen small. Four cases are shown, going from left to right. 共a兲
packings. A deeper understanding of the mechanical and dy-         Both constraints are concave and the region is not bounded. Moving
namical properties of nearly jammed hypoconstrained ellip-         along the vertical direction unjams the system 共this is typical of
soid packings is a subject for future work.                        hard spheres兲. 共b兲 Both constraints are convex and the yellow re-
                                                                   gion is closed, even though it is very elongated along the vertical
                                                                   direction 共of order 冑␦兲. This is an example of pre-stress stability
            VII. NEARLY JAMMED PACKINGS                            共second-order jamming兲. 共c兲 One of the constraints is convex, but
                                                                   not enough to block the unjamming motion in the vertical direction.
    So far we have considered ideal jammed packings, where         The motion has to curve to avoid the convex constraint, i.e., a
particles are exactly in contact. Computer-generated pack-         nonzero acceleration is needed to unjam the system 共second-order
ings however always have a packing fraction ␾ slightly             flexible兲. 共d兲 Only one of the constraints is convex, but enough to
lower than the jamming packing fraction ␾J, and the par-           close the yellow region 共second-order jammed兲. If the radii of cur-
ticles can rattle 共move continuously兲 to a certain degree if       vatures R1 and R2 are very close in magnitude, this region can
agitated thermally or by shaking 关2兴. We can imagine that we       become a very elongated bananalike shape.
started with the ideal jammed packing and scaled the particle
sizes by a factor ␮ = 1 − ␦ ⬍ 1, so that the packing fraction is   if the sum of the radii of curvatures of the two constraints at
lowered to ␾ = ␾J共1 − ␦兲d. We call ␦ the jamming gap or dis-       the jamming point R1 + R2 is positive, there is no unjamming
tance to jamming.                                                  motion. On the other hand, if it is negative then there is an
    It can be shown that if ␦ is sufficiently small the rattling   unjamming motion in the vertical 共floppy兲 direction. This is
of the particles does not destroy the jamming property, in the     equivalent to looking at the smallest eigenvalue of the stress
sense that the configuration point Q = QJ + ⌬Q remains             matrix in higher dimensions.
trapped in a small jamming neighborhood or jamming basin               The jamming basin J⌬Q共␦兲 for a given jamming gap ␦ is
J⌬Q 傺 RN f around QJ, which can be shown rather generally
                                                                   the local solution to the relaxed impenetrability equations
using arguments similar to those in Ref. 关13兴 for tensegrities.
In the limit ␦ → 0 the set of accessible configurations J⌬Q
→ 兵QJ其, and in fact this is the definition of jamming used by                       ␨共⌬Q兲 艌 − ␨␦ = 1 −     冉 冊
                                                                                                             1 2
                                                                                                            1−␦
                                                                                                                 .
Salsburg and Wood in Ref. 关44兴. Rewritten to use our termi-
nology, this definition is: “A configuration is stable if for      One way to determine J⌬Q共␦兲 for a wide range of ␦’s is to
some range of densities slightly smaller than ␾J, the configu-     consider the function of the particle displacements
ration states accessible from QJ lie in the neighborhood of                        ˜␦共⌬Q兲 = 冑1 + min关␨共⌬Q兲兴 − 1,
QJ. More formally, if for any small ⑀ ⬎ 0 there exists a ␦                                                                         共28兲
⬎ 0 such that all points Q accessible from QJ satisfy 储Q           that is, to calculate by how much the particles need to be
− QJ储 ⬍ ⑀ provided ␾ 艌 ␾J共1 − ␦兲d.” We call this the trapping      shrunk to make a given particle displacement ⌬Q feasible
view of jamming, most natural one when considering the             共preserving nonoverlapping兲. The contours 共level-sets兲 of the
thermodynamics of nearly jammed hard-particle systems              function ˜␦共⌬Q兲 denote the boundaries of J⌬Q共␦兲, that is,
关45兴. Note that the trapping definition of jamming is in fact
equivalent to our kinematic definition of jamming 关13兴.            J⌬Q共␦兲 = 兵⌬Q 兩 ˜␦共⌬Q兲 艋 ␦其.
    To illustrate the influence of the constraint curvature on                     A. First-order jammed packings
jamming, we show in Fig. 6 four different cases with two
constraints in two dimensions. In all cases a self-stress exists       As a simple but illustrative example, we will consider a
since the normals of the two constraints are both horizontal.      single mobile disk jammed between three other stationary
If both constraint surfaces are concave 共have negative or out-     disks, as shown in Fig. 7, an analog of the ellipse example
ward curvature兲, as constraints always are for hard-spheres,       from Fig. 5. This packing is first-order jammed, and the fig-
two constraints cannot close a bounded region J⌬Q around           ure also shows a color plot of the function ˜␦共⌬Q兲 along with
the jamming point. One needs at least three constraints and        its contours. It is seen that for small ␦ the jamming basin
in that case J⌬Q will be a curved triangle. If however at least    J⌬Q is a closed curved triangle.
one of the constraints is convex 共has positive curvature兲, two         These observations are readily generalized to higher di-
constraints can bound a closed jamming basin. Specifically,        mensions. For sufficiently small ␦, the jamming basin ap-

                                                             051304-20
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                         PHYSICAL REVIEW E 75, 051304 共2007兲




   FIG. 7. 共Color online兲 共Top兲 An example of a mobile disk jammed between three fixed disks. This is analogous to the ellipse packing
shown in Fig. 5. 共Bottom兲 A color plot of the function ˜␦共⌬Q兲 for this disk packing along with its contours 共level sets兲.

proaches a convex jamming polytope 共a closed polyhedron              the volume of J⌬Q 共and thus the free energy兲 in the jamming
in arbitrary dimension兲 P⌬Q. For spheres all constraint sur-         limit. If we consider the simple two-constraint example in
faces are concave and therefore P⌬Q 債 J⌬Q 关44,46兴. The               Fig. 6, we find that the area A of the feasible region scales
jamming polytope is determined from the linearized impen-            as ␦3/2 instead of ␦2,

                                                                                                      冑
etrability equations
                                                                                                 16        R1R2 3/2
                     AT⌬Q 艌 − ␨␦ ⬇ − 2␦ ,                    共29兲                          A=                     ␦ .
                                                                                                 3        R1 + R2
and we can see that its volume, which determines the 共non-
equilibrium兲 free-energy, scales as ␦N f . This leads to the free-   An obvious generalization of this result to higher dimensions
volume divergence of the pressure in the jamming limit               can be obtained by assuming that the jamming basin J⌬Q has
                                                                     extent 冑␦ along all Nfloppy ⬇ N f − M directions corresponding
                          PV     df                                  to floppy modes, where as it has extent ␦ along all other
                     p=      ⬇         ,                     共30兲
                          NkT 1 − ␾/␾J                               perpendicular directions. The volume would then scale as
                                                                                                                  ¯
which has been verified numerically for disordered isocon-                   兩J⌬Q兩 ⬃ ␦ M ␦共N f −M兲/2 = ␦N共d f /2+Z/4兲 = ␦Nd f 共1+s兲/2 ,
strained hard sphere packings 关2兴.
                                                                     where we quantify the hypostaticity of the packing by s
              B. Second-order jammed packings                        = Z̄ / 2d f . The corresponding scaling of the pressure in the
                                                                     jamming limit is
    The ellipse analog from Fig. 5 has three degrees of free-
dom, two translational and one orientational. If we fix the                                     PV    d f 共1 + s兲/2
orientation of the 共mobile兲 ellipse, that is, we take a planar                            p=        ⬇               .
                                                                                                NkT    1 − ␾/␾J
cut through ˜␦共⌬Q兲, the situation is identical to that for the
disk example above: For small ␦ the jamming basins J⌬Q are               However, as ␦ becomes very small, the jamming region
closed curved triangles. However, the range of accessible            becomes so elongated along the space of floppy modes that
orientations is rather large, on the order of 冑␦, since even for     the time-scales for rattling along the elongated directions
a small ␦ the ellipse can rotate significantly. This is a conse-     becomes much larger than the time for rattling in the perpen-
quence of the rotation of the ellipse being a floppy mode, and       dicular directions. This manifests itself as a remarkably large
only being blocked by second-order effects as given by the           and regular oscillation of the “instantaneous” pressure 共as
curvature of the impenetrability constraints. In a certain           measured over time intervals of tens of collisions per par-
sense, the packing is trapped to a greater extent in the sub-        ticle兲 during molecular-dynamics runs at a fixed ␦, as illus-
space of configuration space perpendicular to the space of           trated in Fig. 9. The oscillations are more dramatic the
floppy modes than it is in the space of floppy modes. This is        smaller ␦ is, and can span six or more orders of magnitudes
illustrated in Fig. 8.                                               of changes in the instantaneous pressure. The period of
                                                                     oscillation, as measured in numbers of collisions per particle,
                                                                     is dramatically affected by the moment of inertia of the el-
 C. Pressure scaling for hypostatic jammed ellipsoid packings
                                                                     lipsoids I, most naturally measured in units of mO2, where m
   The observations in Fig. 8 are readily generalized to             is the particle mass and O is the 共say smallest兲 ellipsoid
higher dimensions, however, it is no longer easy to determine        semiaxis.

                                                               051304-21
DONEV et al.                                                                                                        PHYSICAL REVIEW E 75, 051304 共2007兲




    FIG. 8. 共Color online兲 共Left兲 A plot of the function ˜␦共⌬Q兲 for the packing from Fig. 5. The horizontal axes correspond to the translational
degrees of freedom and the vertical to the rotational degree of freedom 共the rotation angle of the major axes兲. The ⌬Q = 0 cut is also shown
共horizontal colored plane兲, to be compared to the right part of Fig. 7. We also show the jamming basin J⌬Q共␦ = 0.0035兲 共dark blue region兲,
illustrating that this region is shaped like a banana, elongated along the direction of the floppy mode. 共Right兲 Several contours 共isosurfaces兲
of ˜␦共⌬Q兲, bounding the banana-shaped regions J⌬Q共␦兲.

   We do not understand the full details of these pressure                                                                       dfs
oscillations, however, it is clear that dynamics near the jam-                                                           p⬇            .
                                                                                                                              1 − ␾/␾J
ming point for the hypoconstrained ellipsoid packings is not
ergodic on small time scales. In particular, as a packing is
compressed during the course of the packing algorithm, the                           In Fig. 10 we show C = p共1 − ␾ / ␾J兲 as a function of the jam-
time scale of the compression may be shorter than the time                           ming gap for compressions of systems of ellipses of different
scale of exploring the full jamming basin. Over shorter time                         aspect ratios close to unity. The compression started with a
scales the packing can only explore the directions perpen-                           dense liquid and the particles were grown slowly at an ex-
dicular to the floppy modes, and in this case we expect that                         pansion rate ␥ = 10−5 to a high pressure 共jamming兲 p = 109.
the pressure would scale as                                                          The figure shows for each aspect ratio the lower bound CL
                                                                                     = d f s = 3s and the upper bound CU = d f 共1 + s兲 / 2 = 1.5共1 + s兲,
                                                                                     where s was calculated by counting the almost perfect con-
    1012


                                                                                                   2.8

                                                                                                   2.7

    1011                                                                                           2.6

                                                                                                   2.5
                                                                                     C=p(1−φ/φJ)
p




                                                                                                   2.4

    1010                                                                                           2.3
                                                            −12
                                                   I=1, δ=10
                                                                                                   2.2                                             α=1
                                                                                                                                                   α=1.01
                                                                  −12
                                                   I=0.01, δ=10
                                                   I=1, δ=10
                                                            −11
                                                                                                   2.1                                             α=1.025
                                                   I=0.01, δ=10
                                                                  −11
                                                                                                                                                   α=1.05
    109                                            I=1, δ=10
                                                            −10                                     2                                              α=1.075
                                                   I=0.01, δ=10
                                                                  −10
                                                                                                   1.9                                             α=1.1
           0            2000                       4000                 6000
                        Number of collisions (100s per particle)                                   1.8
                                                                                                    0.000001   0.00001        0.0001       0.001             0.01
    FIG. 9. 共Color online兲 The “instantaneous” reduced pressure for                                                             1−φ/φJ
a jammed hypoconstrained packing of three-dimensional ellipsoids
with semi-axes ratio 1.025−1: 1: 1.025, at different 共estimated兲 dis-                    FIG. 10. 共Color online兲 The pressure scaling coefficient C
tances from the jamming point ␦. Molecular dynamics runs using a                     = p共1 − ␾ / ␾J兲 as systems of hard ellipses are compressed from a
natural moment of inertia of the particles as well as ones using a                   dense liquid to the jamming point. The value of C is not constant;
much smaller moment of inertia are shown. The pressure oscilla-                      however, it seems to remain between the bounds CL 共shown with a
tions are sustained for very long periods of time, however, it is not                dashed line in the same color as C兲 and CU 共shown with a solid
clear whether they eventually dissipate.                                             line兲.

                                                                               051304-22
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                     PHYSICAL REVIEW E 75, 051304 共2007兲

tacts at the highest pressure 关2兴. As expected from the argu-                                     d 2E
ments above, we see that very close to the jamming point                                     k=        艌0
                                                                                                  d␨2
C ⬇ CL, however, further away from jamming C ⬇ CU. For
packings that are not hypoconstrained CL = CU = d f , and for
disks CU = CL = 2.                                                 becomes very large and positive. This indicates a physical
                                                                   interpretation of the hard-particle interaction potential: It is
VIII. ENERGY MINIMA IN SYSTEMS OF DEFORMABLE                       the limit of taking an infinite stiffness coefficient while the
                  PARTICLES                                        force between particles is kept at some non-negative value,
                                                                   which can be tuned as desired by infinitesimal changes in the
    In this section we consider the connections between jam-       distance between the particles 共but note that the forces in
ming in hard particle packings and stable 共local兲 energy           different contacts are correlated since the motion of particles
minima 共inherent structures 关23兴兲 for systems of deformable        affects all of them simultaneously兲.
共soft兲 particles. This has a twofold purpose. Firstly, in physi-
cal systems particles are always deformable, and therefore it
is important to establish that the hard-particle conditions for      A. Stable energy minima correspond to jammed packings
jamming we established in Sec. V are relevant to systems of
deformable particles. We expect that if the particles are suf-         Assume that we have a packing of hard particles and that
ficiently stiff, to be made more quantitative shortly, the be-     we can find a set of interparticle interaction potentials Uij for
havior of the soft-particle system will approach that of the       the geometric contacts such that the configuration is a stable
corresponding hard-particle packing. Secondly, considering         energy minimum. This means that any motion of the par-
the conditions for the existence of a stable energy minimum        ticles leads to increasing the energy U, i.e., to overlap of
will enable us to derive in a simpler fashion and better un-       some pair of particles. Therefore, the packing of hard par-
derstand the jamming conditions from the previous section.         ticles is jammed. This gives a simple way to prove that a
    We consider systems with short-ranged continuous inter-        given packing is jammed: Find a set of interparticle poten-
particle potentials that are a monotonically decreasing func-      tials that makes the configuration a stable energy minimum
tion E of the overlap between particles                            关12,13兴. We examine the conditions for a stable energy mini-
                                                                   mum when the interaction potentials are twice differentiable
                           Uij = E关␨共qi,q j兲兴.             共31兲    next.
                                                                       The converse is also true, in the sense that arbitrarily near
That is, we assume that the elastic behavior of the particles is   a jammed packing there is an energy minimum for a suffi-
such that the interaction energy only depends on the distance      ciently “hard” interaction potential 共in some cases the poten-
between the particles as measured by the overlap potential ␨.      tial energy U may have to be discontinuous at the origin
An example of such an elastic potential is an inverse power        关12兴兲. We demonstrate this in the examples from Figs. 7 and
law                                                                8 for a power-law interaction potential with increasing expo-
                                                                   nent ␯ in Figs. 11 and 12, respectively. It is clear that in the
                           E共␨兲 = 共1 + ␨兲−␯ ,              共32兲    limit p → ⬁, the contours of the interaction potential become
                                                                   those of ˜␦共⌬Q兲 and are thus closed near the origin, i.e., the
which in the limit ␯ → ⬁ approaches a hard-particle interac-
                                                                   energy has a minimum. The higher the exponent p is, how-
tion


                                再                 冎
                                                                   ever, the more anharmonic the interaction potential becomes
                                    0 if ␨ ⬎ 0,                    and the contours are no longer ellipsoidal near the energy
                   E H共 ␨ 兲 =                                      minimum.
                                    ⬁ if ␨ ⬍ 0.                        It should be emphasized that the energy minima in soft-
                                                                   particle systems have a variable degree of overlap between
For sufficiently large power exponents ␯ the interaction is        neighboring particles and therefore do not correspond to
localized around particles in contact and the overall energy       hard-particle packings. In particular, at large pressures or ap-
                                                                   plied forces the deformability of the particles becomes im-
     U = 兺 Uij → max Uij = 1 + min ␨ij −␯ = 共1 + ˜␦2兲−␯
          ij          ij             共    ij      兲                portant and the energy minima no longer have the geometric
                                                                   structure of packings. However, in the limit of no externally
                                                                   applied forces, i.e., f → 0, the only interacting particles are
is dominated by the most overlapping pair of particles 关see        those that barely overlap, i.e., that are nearly touching.
Eq. 共28兲 for the definition of ˜␦兴. Additionally, as ␯ grows the   Therefore energy minima for purely repulsive interaction po-
interparticle potential becomes stiff in the sense that small      tentials and a finite cutoff correspond to jammed packings of
changes in the distance between the particles cause large          hard particles in the limit of zero external pressure 共alterna-
changes of the interparticle force                                 tively, one can keep the applied forces constant and make the
                                                                   grains infinitely stiff 关6兴兲. Therefore, the packings of soft
                             f=−
                                     dE
                                        艌0                         particles studied in Ref. 关3兴 very slightly above the “jamming
                                     d␨                            threshold” ␾c are closely related to collectively jammed ideal
                                                                   packings of spheres of diameter D = ␴ 共polydispersity is
and the stiffness coefficient                                      trivial to incorporate兲 关47兴.

                                                             051304-23
DONEV et al.                                                                                  PHYSICAL REVIEW E 75, 051304 共2007兲




  FIG. 11. 共Color online兲 The total interaction energy U共⌬Q兲 for the example in Fig. 7 when the disks are deformable and interact via a
power-law potential. We show U as a color plot with overlaid contours for power exponents ␯ = 12, 25, and 100 共going from left to right兲.
Compare the ␯ = 100 case to the contours of ˜␦共⌬Q兲 in Fig. 7.

              B. Hessian eigenvalues and jamming                       where K = ⵱␨2⑀ = Diag兵kij其 is an 关M ⫻ M兴 diagonal matrix
   It is well known that for smooth interactions a given con-          with the stiffness coefficients along the diagonal, and H
figuration is a stable energy minimum if the gradient of the           = ⵱QA = ⵱2Q␨ is the Hessian of the overlap constraints. Note
energy is zero and the Hessian is positive definite, and the           that more careful notation with derivatives of vectors and
converse is also true if positive definite is replaced with posi-      matrices can be developed and should in principle be em-
tive semidefinite. This has been used as a criterion for jam-          ployed in calculations to avoid confusions about the order of
ming in systems of deformable particles 关3,47兴.                        matrix multiplications and transpositions 关48兴.
   The gradient of U = 兺ijUij is                                          The Hessian

             dE                                                                             HU = ⵱2QU = AKAT − H
   ⵱ QU = 兺       共⵱Q␨ij兲 = 共⵱Q␨兲共⵱␨E兲 = A共⵱␨E兲 = − Af.
          ij d␨ij                                                      consists of two terms, the stiffness matrix HK = AKAT, and
                                                                       the stress matrix H that we already encountered in the
The first-order necessary condition for a stable energy mini-          second-order expansion of the impenetrability constraints.
mum is therefore exactly the force/torque balance condition            The importance of not neglecting the stress matrix is also
                                                                       noted independently in Ref. 关20兴, where also expressions are
                       Af = 0 and f 艌 0,                               given for this matrix for certain types of contact geometry.
as we derived using linear programming and duality theory                 The second-order sufficient condition for a strict energy
for hard-particle packings. The Hessian is                             minimum is

             ⵱2QU = 关⵱Q共⵱␨E兲兴AT + 共⵱2Q␨兲共⵱␨E兲                                                       HU Ɑ 0.

                   = 关A共⵱␨2E兲兴AT + 共⵱QA兲共⵱␨E兲                          Since K ⬎ 0, the stiffness matrix HC is positive-semidefinite:
                                                                       For any vector ⌬Q that is not a floppy mode, ⌬QTHK⌬Q
                   = AKAT − Hf = AKAT − H,                             ⬎ 0, while ⌬QTHK⌬Q = 0 if ⌬Q is a floppy mode 共i.e.,




   FIG. 12. 共Color online兲 The contours 共isosurfaces兲 of the total interaction energy U共⌬Q兲 for the example in Fig. 8 when the ellipses are
deformable and interact via a power-law potential. Going from left to right, we show ␯ = 12 and 25, as well as the hard ellipsoid ˜␦共⌬Q兲,
corresponding to the limit ␯ → ⬁.

                                                                051304-24
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                      PHYSICAL REVIEW E 75, 051304 共2007兲

AT⌬Q = 0兲. Therefore, for any direction of particle motion          inside each spring f needs to be f⌬x = F. If the system is not
that is not a floppy mode, one can make the stiffness coeffi-       prestressed, then the potential energy is quartic around the
cients large enough to make ⌬QTHK⌬Q ⬎ 0, regardless of              origin, ⌬U = 21 k⌬l2 ⬇ 21 k⌬x4, and the applied force causes a
the value of ⌬QTH⌬Q. Floppy modes, however, correspond              very large deformation of the structure ⌬x = 共F / k兲1/3. The
to negative curvature directions of the Hessian HU if they are      structure is stable 共i.e., corresponds to a jammed packing兲,
positive-curvature directions of the stress matrix,                 however, its response to perturbations is not harmonic. If,
⌬QTH⌬Q ⬎ 0. Therefore, the energy minimum is strict if              however, there is an initial force f in the springs, then the
and only if the stress matrix is negative-definite on the space     potential energy is quadratic around the origin ⌬U ⬇ f⌬l
of floppy modes. This is exactly the same result as the             = f⌬x2 and the deformation is linear in the applied force
second-order condition for jamming we derived in Sec. V             ⌬x = F / f. If f ⬍ 0, then the system is unstable and will
using duality theory.                                               buckle, and if f ⬎ 0 the system is stable and its response to
    For deformable particles, the stiffness coefficients are fi-    perturbations is harmonic. This is exactly the form of stabil-
nite. Therefore, for sufficiently large interparticle forces, the   ity that hypoconstrained ellipsoid packings have.
stress matrix may affect the eigenspectrum of the Hessian               It is instructive to compare the simple example in Fig. 13
HU and therefore the stability of potential energy minima.          with the example given in Fig. 5. In the latter there is also a
For cohesionless 共f ⬎ 0兲 spheres, as we derived earlier, H          single floppy mode. Let the small displacement of the central
Ɑ 0 and therefore interparticle forces may only destabilize         mobile particle along this floppy mode, due to an applied
packings: This is the well known result that increasing the         torque ␶, be ⌬q. This involves both a small rotation and a
interparticle forces leads to buckling modes in sphere pack-        small displacement of the centroid, and causes a quadratic
ings 关10兴. Jamming in systems of soft spheres is therefore          change in the contact distances ⌬l ⬃ ⌬q2. If the packing is
considered in the limit of f → 0, i.e., the point when particles    prestressed by a slight compression 共or expansion of the cen-
first start interacting 关3,41兴. For ellipsoids however, the         tral ellipse兲, so that the contact forces are a positive multiple
forces can, and in practice they do, provide stability against      of the self-stress, f = ␭fself, ␭ ⬎ 0, then the potential energy is
negative or zero-frequency vibrational modes. The magni-            quadratic, ⌬U = fT⌬l ⬃ ␭⌬q2. The deformation needed to re-
tude of the forces becomes important, and will determine the        sist the applied torque is determined from ␶ = fT⌬N = ␭⌬q
shape of the density of states 共DOS兲 spectrum 关41兴 for small        共fself
                                                                      T
                                                                           ⵱qN兲, i.e., ⌬q ⬃ ␶ / ␭. Here ⵱qN denotes the sensitivity
vibrational frequencies. To quote from Ref. 关10兴, “ The basic       of the normal vectors N 共represented in a suitable matrix
claim … is that one cannot understand the mechanical prop-          form兲 at the points of contact with respect to the position of
erties of amorphous materials if one does not explicitly take       the mobile ellipse. The response of the system is therefore
into account the direct effect of stresses.”                        strongly dependent upon the magnitude of the pre-stress ␭,
    The density of states 共vibrational modes兲 in packings of        just as the response in the example in Fig. 13 is dependent
soft spheres has been the subject of recent interest                upon f.
关41,49,50兴. In particular, a Boson peak of low-frequency
modes has been identified and attributed to the marginal ri-
gidity 共isostaticity兲 of the packings 关49兴. The effect of pre-        IX. PACKINGS OF NEARLY SPHERICAL ELLIPSOIDS
stresses 共pressure兲 on the density of vibrational modes has            In this section we will consider nearly spherical ellip-
also been studied 关50兴. Such studies should be carried out          soids, that is, ellipsoids with aspect ratio ␣ close to unity. In
also for packings of soft ellipsoids. In this case additional       particular, we try to understand why these packings are hy-
low-frequency modes will appear due to the floppy modes,            poconstrained and to quantitatively explain the sharp rise in
especially at low pressures and for nearly spherical ellip-         the density and contact numbers of disordered packings as
soids. These floppy modes will affect the mechanical re-            asphericity is introduced. We propose that the packings of
sponse of the system, and there will be a subtle interplay          nearly spherical ellipsoids should be looked at as continuous
between the low-frequency modes due to the marginal rigid-          perturbations of jammed disordered sphere packings, and es-
ity and those that appear because of the floppy modes inher-        tablish the leading order terms in the expansion around the
ent to hypoconstrained systems.                                     sphere point.

             C. An example of pre-stress stability                              A. Rotational and translational degrees
                                                                                       of freedom are not equal
    Figure 13 shows a very simple example in which pre-
stressing, i.e., pre-existing forces, stabilize a structure. Al-        One might at first sight expect a discontinuous change in
though the example is not a packing, it illustrates well some       the contact number, and therefore the structure, as aspheric-
of the essential features. First, the geometry of the system is     ity is introduced. After all, the number of degrees of freedom
degenerate, since the two springs are exactly parallel. This        jumps suddenly from d f = d to 共for nonspheroids兲 d f = d共d
degeneracy insures that a self-stress exists, since one can         + 1兲 / 2 ⬎ d. However, such an expectation is not reasonable.
stretch/compress both springs by an identical amount and            First, the number of degrees of freedom is d f = d共d + 1兲 / 2
still maintain force balance.                                       even for spheres, since spheres can rotate too. This rotation
    Observe that geometrically the change in the position of        does not affect the non-overlap conditions and therefore is
the joint ⌬x causes a quadratic change in the length of each        not coupled to translational degrees of freedom. If the ellip-
spring ⌬l ⬇ ⌬x2. To balance an applied force F, the force           soids are nearly spherical, particle rotation is only mildly

                                                              051304-25
DONEV et al.                                                                                   PHYSICAL REVIEW E 75, 051304 共2007兲

                                                                         between translational and rotational jamming. For example,
                                                                         the ellipsoid packing produced by simply stretching the crys-
                                                                         tal packing of spheres along a certain axis by a scaling factor
                                                                         of ␣ is translationally but not rotationally 共strictly 关11兴兲
                                                                         jammed. This is because by changing the axis along which
                                                                         the stretch is performed one gets a whole family of ellipsoid
                                                                         packings with exactly the same density. Therefore, it is pos-
                                                                         sible to shear the packing by changing the lattice vectors
                                                                         used in the periodic boundary conditions, without changing
                                                                         the density, as illustrated in Fig. 14 in two dimensions.
    FIG. 13. 共Color online兲 An example of a pre-stress stable sys-           Isostatic packings are translationally ordered. As we al-
tem. Two elastic springs of stiffness k and length l are connected via   ready demonstrated, in order for a hypoconstrained packing
a joint that can move in the horizontal direction under the influence    of ellipsoids to be jammed, the packing geometry must be
of an external force F.                                                  degenerate. The existence of a self-stress f requires that the
                                                                         orientations of particles be chosen so that the torques are
coupled to particle translations and rotation only affects the           balanced in addition to the forces on the centroids. This leads
non-overlap conditions very close to the jamming point. This             to a loss of “randomness” in a certain sense, since the num-
is seen, for example, through a violation of the equipartition           ber of jammed configurations is reduced greatly by the fact
theorem in nonequilibrium MD simulations of hard ellip-                  that geometrically “special” 共not generic兲 configurations are
soids, depending on the moment of inertia of the particles               needed to balance the torques.
and the time scale of the system evolution. We therefore                     However, it is also important to point out that disordered
expect that thermodynamically and kinetically, at least at the           isoconstrained packings of nearly spherical ellipsoids are
level of translations, systems of nearly spherical ellipsoids            hard to construct. In particular, achieving isocounting near
will behave identically to systems of spheres until the inter-           the sphere point requires translational ordering. In two di-
particle gaps become comparable to the difference between                mensions, the average number of contacts per particle
the semiaxes. It is therefore not really surprising that the             needed is Z̄ = 6, however, the maximal kissing number near
properties of the jammed packings such as ␾J or Z̄ change                the sphere point is also Zmax = 6. Therefore the only possibil-
continuously with ␣.                                                     ity is that every particle have exactly Z = 6 contacts. This
    What is somewhat surprising, however, is that ␾J and Z̄              inevitably leads to translational ordering on a triangular lat-
are not differentiable functions of particle shape. In particu-          tice. In other words, the only isoconstrained packing of el-
lar, starting with a unit sphere and changing a given semiaxes           lipses in the limit ␣ → 1 is the hard disk triangular crystal.
by +⑀ Ⰶ 1 increases the density linearly in ⑀, and changing it           Similarly, in three dimensions, Z̄ = Zmax = 12 for nonsphe-
by −⑀ also increases the density by the same amount, ⌬␾J                 roids, and therefore every particle must have exactly Z = 12
⬃ 兩⑀兩. As we will show through our calculations, this nondif-            neighbors. While it not rigorously known what are the sphere
ferentiability is a consequence of the breaking of rotational            packings with all particles having twelve neighbors, it is
symmetry at the sphere point. The particle orientations them-            likely that only stacking variants of the fcc/hcp lattice
selves are not differentiable functions of particle shape and            achieve that property. For spheroids, the isoconstrained num-
change discontinuously as the sphere point is crossed.                   ber of contacts is Z̄ = 10 and the results in Fig. 1 indicate that
    Finally, there is little reason to expect packings of nearly         this value is nearly reached for sufficiently large aspect ra-
spherical particles to be rotationally jammed. After all,                tios. For nonspheroids, however, we only observe a maxi-
sphere packings are never rotationally jammed, since the                 mum of 11.4 contacts per particle, consistent with the fact
spheres can rotate in place arbitrarily. Similarly, near the             that achieving the isoconstrained value requires more trans-
jamming point, it is expected that particles can rotate signifi-         lational ordering.
cantly even though they will be translationally trapped and
rattle inside small cages, until of course the actual jamming
point is reached, at which point rotational jamming will also                        B. Two near spheres (nearly) touching
come into play. It is therefore not surprising that near the
sphere point, the parameters inside the packing-generation                   In what follows we will need first-order approximations
protocol, such as the moment of inertia of the particles and             of the impenetrability constraints between two nearly spheri-
the expansion rate of the particles, can significantly affect the        cal ellipsoids. Assume there are two spheres A and B of
final results. In particular, using fast particle expansion or too       radius OA/B touching. Transform the spheres into ellipsoids
large of a moment of inertia leads to packings that are clearly          with semiaxes OI + ⌬O, and orientation described by the ro-
not rotationally jammed, since the torques are not balanced,             tation matrix Q, and denote ⑀O = O−1⌬O. Finally, define the
however, they are translationally jammed and have balanced               matrix
centroid forces. We do not have a full understanding of the                                        T = QT⑀OQ,
dynamics of our packing-generation algorithm, even near the
jamming point.                                                           which in the case of turning a disk into an ellipse with semi-
    In this paper we will focus on packings that are also ro-            axes O and O共1 − ⑀兲, i.e., aspect ratio ␣ = 1 + ⑀, ⑀ Ⰶ 1, be-
tationally jammed. In general one may need to distinguish                comes

                                                                  051304-26
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                               PHYSICAL REVIEW E 75, 051304 共2007兲

                                                                                                         d

                                                                               ␾J/␾SJ = 共1 + ⌬␮兲d    兿
                                                                                                     k=1
                                                                                                         共1 + ⑀O
                                                                                                               i 兲 ⬇ 1 + d⌬␮ + e ⑀O .
                                                                                                                                T



                                                                         Keeping all ellipsoids aligned produces an affine deforma-
                                                                         tion of the sphere packing that has the same jamming den-
                                                                         sity, but is not 共first-order兲 jammed. Therefore, the true jam-
                                                                         ming density must be higher ␾J 艌 ␾SJ . This explains why the
    FIG. 14. The triangular packing of ellipses is not rotationally      jamming density increases with aspect ratio near the sphere
jammed since one can shear the packing continuously without in-          point. The added rotational degrees of freedom allow one to
troducing overlap or changing the density. The figure shows a se-        increase the density beyond that of the aligned 共nematic兲
quence of snapshots as this shearing motion proceeds. The packing
                                                                         packing, which for ellipsoids has exactly the same density as
is, however, 共strictly 关11兴兲 translationally jammed.
                                                                         the sphere point.


               冋                                   册
                                                                             Can we find a set of orientations for the ellipsoids so that
                      sin2 ␾       − sin ␾ cos ␾                         the resulting packing is jammed? The first condition for jam-
        T=−⑀                                           = − ⑀T␾ ,
                   − sin ␾ cos ␾      cos2 ␾                             ming is that there exist a self-stress that balances both forces
                                                                         and torques on each particle. Just from the force-balance
where ␪ is the angle of orientation of the ellipse. It can be            condition, one can already determine the interparticle forces
shown that to first order in ⑀ the new distance between the              f. These will change little as one makes the particles slightly
ellipsoids is                                                            aspherical, because the normal vectors barely change. There-
                                                                         fore, the self-stress is already known a priori, without regard
                          ⌬␨ = 2uAB
                                 T
                                    SuAB ,                               to the choice of particle orientations. The orientations must
                                                                         be chosen so that the torques are also balanced. As shown
where
                                                                         above, to first order in asphericity ⑀, the torque balance con-
                          OA           OB                                dition for particle i is
                   S=           TA +         TB .
                        OA + OB      OA + OB                                         兺 f ij共Tiuij兲 ⫻ uij = 兺j f ijUijTiuij = 0.
                                                                                   j苸N共i兲
                                                                                                                                        共33兲
   The torque exerted by the contact force f = fn on a given
particle, to first order in asphericity ⑀, comes about because           This gives for each particle a set of possible orientations,
the normal vector no longer passes through the centroid of               given the contact network of the isoconstrained sphere pack-
the particle 共as it does for spheres兲. One can ignore the small          ing. The torque balance condition 共33兲 is in fact the first-
changes in the magnitude of the normal force or the change               order optimality condition for maximizing the jamming den-
in the contact point rC, and only consider the change in the             sity, as expected. It is worth pointing out that for a random
normal vector                                                            assignment of orientations to ellipses the expected change in
                                                                         density is identically zero; in order to get an increase in the
               n ⬇ Xu ⬇ 共I − 2T兲u = u − 2Tu,                             density one must use orientations correlated with the trans-
                                                                         lational degrees of freedom.
giving a torque
                                                                             Ellipses. In two dimensions, for a particular contact with
                     ␶ = rC ⫻ f ⬇ 2of共Tu兲 ⫻ u.                           u = 具cos ␪ , sin ␪典 we have the simple expressions
                                                                                                uT␾u = sin2共␾ − ␪兲,
        C. Maintaining jamming near the sphere point
                                                                                                             1
    Assume now that we have a collectively jammed isocon-                                   u ⫻ 共T␾u兲 =        sin关2共␾ − ␪兲兴.
strained sphere packing with density ␾SJ and that we want to                                                 2
make the disks slightly ellipsoidal by shrinking them along a            Considering 2␾ as the variable, one easily finds the solution
given set of axes, while still preserving jamming. Keeping               to Eq. 共33兲

                                                                                               冉                                冊
orientations fixed, one can expand each near sphere by a
scaling factor ⌬␮ and displace each centroid by ⌬r, so that                      2␾ = arctan ± 兺 f i sin 2␪i, ± 兺 f i cos 2␪i .         共34兲
all particles that were initially in contact are still in contact.                                   i                   i
Note that because the matrix S is proportional to ⑀, so will             If we calculate the second derivative for the density increase
⌬␮ and ⌬R. In other words, the change in the density will be             we find that
linear in asphericity. However, the value of the slope depends
on the choice of orientations of the ellipsoids. Referring back
to Sec. V D 2 we see that to first order in ⑀, ⌬␮ is
                                                                                          d2
                                                                                               冋                     册
                                                                                             兺 f i sin2共␾ − ␪i兲 = ± 1,
                                                                                         d␾2 i
        1 T     1                    1
 ⌬␮ =     f ⌬␨ = 兺 f ijuTijSijuij =    兺 兺 f ijuTijTiuij ,               and therefore in order to maximize the jamming density we
        M       M 兵i,j其             2M i j苸N共i兲                          need to choose the minus signs in Eq. 共34兲. Once we find the
                                                                         unique orientation of each ellipse that ensures torque bal-
giving a new jamming density                                             ance, we can calculate the jamming density

                                                                   051304-27
DONEV et al.                                                                                                    PHYSICAL REVIEW E 75, 051304 共2007兲


                         ␾J/␾SJ ⬇ 1 + s␾⑀ ,
                                                                                  0.875
                                                           共35兲
                                                                                                     MD algorithm
where                                                                                                Free orientations
                                                                                   0.87              Frozen orientations

                            兺 f ij共uTijTi␾uij兲
                        兺i j苸N共i兲
                                                                                                     Theory




                                                                   Estimated φJ
               s␾ = 2                            − 1.                             0.865

                                 兺 f ij
                             兺i j苸N共i兲                                                                                                   0.9
                                                                                                                                    0.89
                                                                                   0.86
                                                                                                                                    0.88
    We have calculated the slope s␾ for disordered binary disk                                                                                                 Frozen random
packings 共with ␾SJ ⬇ 0.84兲 numerically, and find a value s␾
                                                                                                                                    0.87
                                                                                  0.855                                             0.86
⬇ 0.454. We compare this theoretical value with numerical
                                                                                                                                    0.85
calculations in Fig. 15. The first comparison is directly to the
                                                                                                                                    0.84
packing fractions obtained using the Lubachevsky-Stillinger                        0.85                                                        1      1.2     1.4     1.6

algorithm, which do not have anything to do with perturbing                               1   1.01      1.02     1.03      1.04   1.05         1.06    1.07   1.08    1.09     1.1

a sphere packing. Although the simulation jamming densities                                                                Aspect ratio α
are not linear over a wide range of aspect ratios, near ␣ = 1
                                                                        FIG. 15. 共Color online兲 The estimated jamming density near the
they are and the slope is close to the theoretically predicted       disk point for binary packings of hard ellipses, as obtained from the
s␾. We also compare to results obtained by perturbing a              LS packing algorithm, from perturbing the disk packing using
jammed disk packing using MD. Specifically, we start with a          constant-pressure MD, and from the first-order perturbation theory.
jammed disk packing at a relatively high pressure 共p                 The inset shows some of the data over a larger range of aspect ratio
= 1000兲 and assign an orientation according to Eq. 共34兲 to           and also shows the packing densities obtained when the ellipses
every disk, and then we start growing the large semiaxes             have infinite moment of inertia in the LS algorithm.
slowly while performing a form of constant pressure MD.
The density changes automatically to keep the pressure con-
stant, and from the instantaneous density we estimate the            共large兲 jammed ellipse packings with Z̄ = 4, the absolute
jamming density using Eq. 共30兲. In Fig. 15 we show how the           minimum contact number possible for a jammed packing.
共estimated兲 jamming density changes with aspect ratio. If we             Finally, we note that in three dimensions the torque bal-
freeze the orientations 共i.e., use an infinite moment of iner-       ance equations 共33兲 involve quaternions and are quartic, and
tia兲, we obtain results that follow the theoretical slope pre-       it does not seem an analytical solution is possible as it is in
diction closely. Very good agreement with the results from           two dimensions. We however expect that the calculations
the LS algorithm is obtained over a wide range of ␣ if we            performed here in d = 2 can be generalized to higher dimen-
start with the correct orientations and then allow the ellipse       sions as well. One interesting question to answer theoreti-
orientations to change dynamically. For comparison, in the           cally in d = 3 is whether the middle axes 共␤兲 affects the slope
inset we show that the packing density actually decreases if         of the density s␾ or whether only the ratio of the largest to
we use the LS algorithm and freeze orientations at their ini-        the smallest semiaxes 共␣兲, matters. In Ref. 关4兴 we proposed
tial 共random兲 values, demonstrating that balancing the               that the rapid increase in packing fraction could be attributed
torques and 共maximally兲 increasing the density requires a            to the need to increase the contact numbers, since forming
particular value for the particle orientations.                      more contacts requires a denser packing of the particles. This
    For ellipses, there are unique orientations that guarantee       is supported by the observation that the maximal packing
the existence of self-stresses near a given isoconstrained           density is achieved for the most aspherical shape 共␤ = 1 / 2兲.
jammed disk packing. Do these orientations actually lead to          However, numerical results very close to the sphere point are
jammed packings, that is, are the second-order conditions for        consistent with a slope s␾ independent of ␤. The arguments
jamming also satisfied? If one starts with a jammed disk             of this section indicate that the density rise is independent of
packing and transforms the disks into ellipses of aspect ratio       the rise of the coordination number, at least near the sphere
sufficiently close to unity, the packing will remain transla-        point.
tionally jammed 关13兴. Subsequent increase in the size of the
particles must eventually lead to a packing of maximal den-
                                                                                              D. Contact number near the sphere point
sity. It is not however a priori obvious whether this packing
is rotationally and translationally jammed or has some kind             In our perturbation approach to ellipsoid packings near
of peculiar unjamming motions that preserve the density,             the sphere point, we assumed that the contact network re-
such as the ones shown in Fig. 14. For small disk packings,          mains that of the disk packing even as the aspect ratio moves
we have found the perturbed ellipse packings to be second-           away from unity. However, as the aspect ratio increases and
order jammed sufficiently close to the sphere point. For             the packing structure is perturbed more and more, some new
larger systems, even for very small asphericities, it is diffi-      contacts between nearby particles will inevitably close, and
cult numerically to perturb a given disk packing into an el-         some of the old contacts may break. In Fig. 16 we show a
lipse packing without leading to new contacts or breaking of         system that the linear perturbation prediction produces at ␣
old ones, as discussed shortly. An analytical investigation          = 1.025. While the original contacts in the jammed disk pack-
may be able to prove that the perturbed packings are actually        ing are maintained relatively well, we see that many new
second-order jammed, and therefore prove that there exist            overlaps form that were not contacts in the disk packing.

                                                             051304-28
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                        PHYSICAL REVIEW E 75, 051304 共2007兲


This means that the contact number will increase from Z̄
= 4 as asphericity is introduced.
   These observations suggest a way to calculate the leading
order term of Z̄共␣兲 − 2d: We simply count the overlaps intro-
duced by orienting and displacing the centroids of the ellip-
soids according to the linear perturbation theory. It is well-
known that jammed disordered sphere packings have an
unusual multitude of nearly-touching particles, as manifested
by a power-law divergence in the pair correlation function
near contact of the form g2共r兲 ⬃ 共r − D兲−0.4 共once rattlers are
removed兲 关2兴. For binary disks in two dimensions the exact
exponent has not been calculated, but it appears close to a
half 关51兴. These near contacts will close to form true contacts
and cause the rapid increase in Z̄共␣兲, and we expect that the
growth will be of the form

                    Z̄共␣兲 − 2d ⬇ Z␣冑␣ − 1.                   共36兲
A more rigorous analysis is difficult since we do not really
have an understanding of the geometry of the near contacts.              FIG. 16. Overlaps introduced at ␣ = 1.025 by the naive linear
We have numerically estimated the coefficient Z␣ and plotted         perturbation theory, which only takes into account the original con-
the prediction of Eq. 共36兲 in Fig. 2. It is seen that the predic-    tact network of the disk packing 共black lines兲. We see many over-
tion matches the actual simulation results well sufficiently         laps forming between particles that were nearly touching when ␣
close to the sphere point.                                           = 1.

                                                                     packing that has the minimal number of contacts needed for
                      X. CONCLUSIONS
                                                                     jamming, satisfied only the inequality Z̄ 艌 2d, since at least
    In this paper we presented in detail the mathematical            2d contacts per particle are needed to block particle transla-
theory of jamming for packings of nonspherical particles and         tions. Particle rotations, however, and combined rotation/
tried to understand the properties of jammed packings of             translation motions, can be blocked by the curvature of the
nonspherical particles of aspect ratio close to unity, focusing      particle surfaces at the point of contact. In essence, if the
on hard ellipses and ellipsoids. In this section we summarize        radii of curvatures at the point of contact are sufficiently
our findings and also point to directions for future investiga-      large, i.e., the particle contact is sufficiently “flat,” rotation of
tion.                                                                the particles is blocked. This can be visualized by consider-
    Mathematically, understanding jamming in hard-particle           ing the limit of infinite radii of curvatures, when have a
packings is equivalent to understanding the behavior of large        contact between two flat surfaces. Such contacts, in a certain
systems of nonlinear inequalities as given by the impenetra-         sense, count as several “contact points” and block several
bility conditions. These inequalities can be written explicitly      degrees of freedom.
by introducing a continuously differentiable overlap potential          In Sec. V, we generalized the mathematics of first and
whose sign determines whether two particles overlap. In Sec.         second-order rigidity for tensegrity frameworks developed in
III we generalized the overlap potential proposed by Perram          Ref. 关12兴 to packings of nonspherical particles. We proved
and Wertheim for hard ellipsoids to arbitrary smooth strictly        that in order for a packing to be jammed there must exist a
convex particle shapes and determined its first order deriva-        set of 共nonzero兲 non-negative interparticle forces that are in
tives.                                                               equilibrium, i.e., the packing must have a self-stress. Further-
    In Sec. IV, we discussed the conjecture that large disor-        more, we considered second-order terms for hypoconstrained
dered jammed packings of hard particles are isoconstrained,          packings that do have a self-stress but also have floppy
i.e., that they have an equal number of constraints and de-          modes, that is, particle motions that preserve interparticle
                                                                     distances to first order. The second-order analysis showed
grees of freedom, Z̄ = 2d f . It is not possible to make this
                                                                     that jammed packings of strictly convex particles cannot
conjecture into a theorem since the term “disordered” is
                                                                     have less than 2d contacts per particle. We found that floppy
highly nontrivial to define 关17兴. However, arguments have
                                                                     modes involving particle rotations can be blocked 共rigidified兲
been made in the literature in support of isocounting. We
                                                                     by the stressmatrix, which includes second-order information
showed that this conjecture can be supported with reasonable
                                                                     about the particle surfaces at the point of contact. We pro-
arguments only for spheres, where particle rotations are not
                                                                     posed that this is exactly the type of jamming found in dis-
considered. In particular, while it is expected that Z̄ 艋 2d f for   ordered ellipsoid packings near the sphere point, and in Sec.
“random” packings, the converse inequality Z̄ 艌 2d f only ap-        VI we presented a numerical algorithm for testing hypocon-
plies to spheres. Packings of nonspherical particles can be          strained ellipsoid packings for jamming and applied it to
jammed and have less than 2d f contacts per particle, i.e., be       some computer-generated samples. We demonstrated that the
hypoconstrained. A minimally rigid ellipsoid packing, i.e., a        packings are indeed jammed even very close to the sphere

                                                               051304-29
DONEV et al.                                                                                PHYSICAL REVIEW E 75, 051304 共2007兲

point, where they have close to 2d contacts per particle.             relatively close to unity, the perturbation changes the prop-
   In Sec. VII we considered the thermodynamics of pack-              erties of the system such as density and contact number in a
ings that are close to, but not exactly at, the jamming point,        sharp fashion, making sphere packings a quantitatively unre-
so that particles have some room to rattle 共free volume兲. We          liable reference point for packings of more realistic particle
found that for hypoconstrained packings the jamming basin             shapes. Furthermore, even qualitative understanding of jam-
J⌬Q, which is localized around the jamming point in con-              ming and mechanical rigidity for packings of nonspherical
figuration space, is very elongated along the space of floppy         particles requires consideration of phenomena that simply do
modes. For isostatic or hyperstatic packings, as jammed               not have a sphere equivalent.
sphere packings always are, the jamming basin approaches a                Future work should consider the mathematics of jamming
polytope in the jamming limit, whereas for hypoconstrained            for packings of hard particles that are convex, but not nec-
packings it approaches a 共hyper兲 banana. The latter leads to          essarily smooth or strictly convex. In particular, particles
very large oscillations of the instantaneous pressure near the        with sharp corners and/or flat edges are of interest, such as,
jamming point and a violation of the asymptotic free-volume           for example, tetrahedra 关52兴, cylinders and cubes. We also
equation of state 共pressure scaling兲.                                 believe that understanding jamming in frictional hard-
   Real packings are always made from deformable 共albeit              particle packings, even for the case of spheres, requires a
very stiff兲 particles, i.e., particles that interact via some elas-   more thorough mathematical foundation. It is also important
tic interaction potential. The analog of a jammed hard-               to consider packings of soft ellipsoids and in particular de-
particle packing for deformable particles are strict energy           velop algorithms to generate them computationally and to
minima 共inherent structures兲, i.e., structures where any mo-          study their mechanical properties and vibrational spectra. In-
tion of the particles costs energy 共quadratic in the displace-        vestigations of the thermodynamics of very dense ellipsoid
ments兲. In Sec. VIII we analyzed the first- and second-order          systems also demand further attention.
conditions for a strict energy minimum for twice-
differentiable interaction potentials. We found that the first-
                                                                                           ACKNOWLEDGMENTS
order condition is exactly the requirement for the existence
of a selfstress, and that the second-order condition is exactly          A.D. and S.T. were supported in part by the National Sci-
the condition that the stress-matrix blocks the floppy modes.         ence Foundation under Grant No. DMS-0312067. R.C. was
This deep analogy between jamming in hard-particle pack-              supported in part by the National Science Foundation under
ings and energy minima in soft-particle packings is not un-           Grant No. DMS-0510625. We thank Paul Chaikin for many
expected since a “soft” potential can approximate the singu-          inspiring discussions of ellipsoid packings.
lar hard-particle potential arbitrarily closely. As the potential
becomes stiffer, the energy minimum will become highly
                                                                              APPENDIX: THE RECTANGULAR LATTICE
anharmonic and its shape will closely resemble that of the
                                                                                          OF ELLIPSES
jamming basin J⌬Q 共even at very small temperatures兲.
   Finally, in Sec. IX we developed a first-order perturbation            In this appendix we consider a simple example of a
theory for packings of nearly spherical ellipsoids, expanding         jammed hypoconstrained packing of ellipses having Z̄ = 4,
around the sphere point. The theory is based on the idea that         the minimum necessary for jamming even for disks. Namely,
packings of ellipsoids with aspect ratio ␣ = 1 + ⑀ near unity         the rectangular lattice of ellipses, i.e., the stretched version of
have the same contact network as a nearby isostatic packing           the square lattice of disks, is collectively jammed, and in
of hard spheres. In order for the ellipsoid packing to also be        particular, it is second-order jammed. More specifically,
jammed, the orientations of the ellipsoids must be chosen so          freezing all but a finite subset of the particles, the remaining
as to balance the torques on each particle. These orientations        packing is second-order jammed. An illustration is provided
also maximize the jamming density, increasing it beyond that          in Fig. 17. At first glance, it appears that one can rotate any
of the disk packing, and we analytically calculated the linear        of the ellipses arbitrarily without introducing overlap. How-
slope of the density increase with ⑀ for binary ellipse pack-         ever, this is only true up to first order, and at the second-
ings. The calculated coefficient is in good agreement with            order level the “flat” contacts between the ellipses, that is,
numerical results. The perturbation of the sphere packing             the contacts whose normals are along the small ellipse semi-
also leads to a rapid increase in the average particle coordi-        axes, block this rotation through the curvature of the par-
nation Z̄, which we attributed to the closing of the multitude        ticles at the point of contact.
of near contacts present in disordered disk packings. The                 The set of first-order flexes, i.e., particle motions which
predicted Z̄ ⬃ 冑⑀ is also in good agreement with numerical            preserve contact distances to first order, can easily be con-
observations.                                                         structed in this example due to the simple geometry. Namely,
   The observed peculiar behavior of packings of nonspheri-           a basis vector for this set is a single ellipse rotating around
cal particles near the sphere point is a consequence of the           its centroid, giving the total number of first-order flexes N f
breaking of rotational symmetry. Near the sphere point the            = N 关25兴. The basis formed by these first-order flexes is not
coupling between particle positions and orientations is weak          orthogonal. However, its advantage is that it is easier to cal-
and translations dominate the behavior of the system. In this         culate the stress matrix, or more specifically, the matrix HV;
sense sphere packings are a good model system, and particle           we only need to consider ellipsoid rotations without consid-
shapes close to spherical can be treated as a continuous per-         ering translations. The same observation applies whenever
turbation of sphere packings. However, even for aspect ratios         one takes a jammed sphere packing and makes the particles

                                                                051304-30
UNDERCONSTRAINED JAMMED PACKINGS OF…                                                            PHYSICAL REVIEW E 75, 051304 共2007兲

nonspherical but does not change the normal vectors at the
point of contact. This can be done, for example, by simply
taking a jammed sphere packing and swelling the particles to
be nonspherical, without changing the geometry or connec-
tivity of the contact network. If the particles swell enough to
make all of the contacts sufficiently flat, the new packing
will be jammed, since all of the first-order flexes consist of
particle rotations only and are blocked by the flat curvature
of the contacts.
    The fact that “flat” 共the contacts among vertical neighbors
in Fig. 17兲 contacts block rotations can easily be seen ana-                 FIG. 17. The rectangular lattice of ellipses 共i.e., affinely
lytically by considering the case of one ellipse jammed                  stretched square lattice of hard disks兲 with “hard-wall” boundary
among four fixed ellipses 共two horizontally, two vertically兲.            conditions created by freezing the ellipses on the boundary. This
Specifically, any self-stress for which the contact force in the         packing is jammed, since the curvature of the flat contacts blocks
“flat” contacts is larger than the force in the “curved” con-            the rotations 共including collective ones兲 of the ellipses.
tacts, f flat ⬎ f curv, makes the mobile ellipse jammed, more
specifically, prestress rigid 关25兴. The same result can be
shown to apply to the square lattice of ellipses for an arbi-            that the hard-ellipse equivalent is jammed and can resist any
trary number of ellipses. If the ellipses are not hard but rather        finite external forces, including a compression along the
deformable, the packing would not support a compression                  curved contacts. The anharmonicity of the hard-sphere po-
along the curved contacts, but it would along the flat con-              tential becomes essential in this example, since the packing
tacts. This is a very intuitive result: If one takes a smooth            can choose the correct internal 共self-兲 stresses 共forces兲
ellipsoid and presses it against a table with its most curved            needed to provide mechanical rigidity. In 共realistic兲 systems
tip, it will buckle and the only stable configuration is one             of deformable particles, the internal stresses are fixed and
where the flat tip presses against the table. Note, however,             determined by the state of compression.




 关1兴 H. A. Makse, J. Brujic, and S. F. Edwards, The Physics of           关18兴 A. Donev, F. H. Stillinger, P. M. Chaikin, and S. Torquato,
     Granular Media 共Wiley, New York, 2004兲, Chap. Statistical                Phys. Rev. Lett. 92, 255506 共2004兲.
     Mechanics of Jammed Matter, pp. 45-86.                              关19兴 W. Man, A. Donev, F. H. Stillinger, M. T. Sullivan, W. B.
 关2兴 A. Donev, S. Torquato, and F. H. Stillinger, Phys. Rev. E 71,            Russel, D. Heeger, S. Inati, S. Torquato, and P. M. Chaikin,
     011105 共2005兲.                                                           Phys. Rev. Lett. 94, 198001 共2005兲.
 关3兴 C. S. O’Hern, L. E. Silbert, A. J. Liu, and S. R. Nagel, Phys.      关20兴 K. Bagi, Granular Matter 9, 109 共2006兲.
     Rev. E 68, 011306 共2003兲.                                           关21兴 E. R. Nowak, J. B. Knight, E. Ben-Naim, H. M. Jaeger, and S.
 关4兴 A. Donev, I. Cisse, D. Sachs, E. A. Variano, F. H. Stillinger, R.        R. Nagel, Phys. Rev. E 57, 1971 共1998兲.
     Connelly, S. Torquato, and P. M. Chaikin, Science 303, 990          关22兴 J. B. Knight, C. G. Fandrich, C. N. Lau, H. M. Jaeger, and S.
     共2004兲.                                                                  R. Nagel, Phys. Rev. E 51, 3957 共1995兲.
 关5兴 S. R. Williams and A. P. Philipse, Phys. Rev. E 67, 051301          关23兴 F. H. Stillinger and T. A. Weber, J. Chem. Phys. 83, 4767
     共2003兲.                                                                  共1985兲.
 关6兴 C. F. Moukarzel, Phys. Rev. Lett. 81, 1634 共1998兲.                  关24兴 This threshold is larger than the radius of the 共original兲 hard
 关7兴 A. V. Tkachenko and T. A. Witten, Phys. Rev. E 60, 687                   disks and dependent upon the exact geometry of the packing.
     共1999兲.                                                             关25兴 A. Donev, Ph.D. thesis, Princeton University, Princeton, NJ,
 关8兴 J. N. Roux, Phys. Rev. E 61, 6802 共2000兲.                                2006
 关9兴 S. F. Edwards, Physica A 249, 226 共1998兲.                           关26兴 J. W. Perram and M. S. Wertheim, J. Comput. Phys. 58, 409
关10兴 S. Alexander, Phys. Rep. 296, 65 共1998兲.                                 共1985兲.
关11兴 A. Donev, S. Torquato, F. H. Stillinger, and R. Connelly, J.        关27兴 M. R. Kuhn and C. S. Chang, Int. J. Solids Struct. 43, 6026
     Comput. Phys. 197, 139 共2004兲.                                           共2007兲.
关12兴 R. Connelly and W. Whiteley, SIAM J. Discrete Math. 9, 453          关28兴 C. S. O’Hern, S. A. Langer, A. J. Liu, and S. R. Nagel, Phys.
     共1996兲.                                                                  Rev. Lett. 86, 111 共2001兲.
关13兴 R. Connelly, Invent. Math. 66, 11 共1982兲.                           关29兴 T. M. Truskett, S. Torquato, and P. G. Debenedetti, Phys. Rev.
关14兴 B. D. Lubachevsky and F. H. Stillinger, J. Stat. Phys. 60, 561           E 62, 993 共2000兲.
     共1990兲.                                                             关30兴 The mathematically formal meaning of the term “generic” is
关15兴 A. Donev, S. Torquato, and F. H. Stillinger, J. Comput. Phys.            used in rigidity theory for configurations of points 关31兴. How-
      202, 737 共2005兲.                                                        ever, that rigorous meaning of the term almost never applies to
关16兴 For spheres, such jammed disordered packings have tradition-             packings of monodispersed particles. We use the term “ge-
     ally been referred to as random close packing 共RCP兲.                     neric” merely to mean “not special,” i.e., typical.
关17兴 S. Torquato, T. M. Truskett, and P. G. Debenedetti, Phys. Rev.      关31兴 Rigidity Theory and Applications, edited by M. F. Thorpe and
     Lett. 84, 2064 共2000兲.                                                   P. M. Duxbury, Fundamental Materials Research 共Kluwer/

                                                                  051304-31
DONEV et al.                                                                                    PHYSICAL REVIEW E 75, 051304 共2007兲

     Plenum, Dordrecht, 1999兲.                                           关39兴 M. Todd, Acta Numerica 10, 515 共2001兲.
关32兴 S. Torquato and F. H. Stillinger, J. Phys. Chem. B 105, 11849       关40兴 R. Connelly, Struct. Topology 14, 43 共1988兲.
     共2001兲; S. Torquato, A. Donev, and F. H. Stillinger, Int. J.        关41兴 M. Wyart, Ann. Phys. 共Paris兲 30, 1 共2005兲.
     Solids Struct. 40, 7143 共2003兲.                                     关42兴 C. Gotsman and S. Toledo, SIAM J. Matrix Anal. Appl. 共to be
关33兴 C. H. Norris and J. B. Wilbur, Elementary Structural Analysis            published兲.
     共McGraw-Hill, New York, 1960兲.                                      关43兴 S. M. Rump, Numer. Math. 43, 001 共2003兲.
关34兴 A hyperconstrained packing is statically underdetermined,           关44兴 Z. W. Salsburg and W. W. Wood, J. Chem. Phys. 37, 798
     since there are multiple ways to resolve almost any applied              共1962兲.
     load. In this case constitutive 共elastic兲 laws need to be invoked   关45兴 A. Donev, F. H. Stillinger, and S. Torquato, J. Comput. Phys.
     to determine the forces. A hypoconstrained packing, on the               共to be published兲.
     other hand, is statically overdetermined, and as such is consid-    关46兴 F. H. Stillinger and Z. W. Salsburg, J. Stat. Phys. 1, 179
     ered unstable in the classical literature on mechanical struc-           共1969兲.
     tures 关33兴.                                                         关47兴 A. Donev, S. Torquato, F. H. Stillinger, and R. Connelly, Phys.
关35兴 C. F. Moukarzel, Granular Matter 3, 41 共2001兲.                           Rev. E 70, 043301 共2004兲.
关36兴 Specifically, a packing of stiff particles will have only as many   关48兴 H. Lütkepohl, Handbook of Matrices 共Wiley, New York,
     contacts closed as there are degrees of freedom, M 艋 N f . The           1997兲.
     additional single degree of freedom due to the density ␾ does       关49兴 L. E. Silbert, A. J. Liu, and S. R. Nagel, Phys. Rev. Lett. 95,
     not count unless the packing is compressed to close the addi-            098301 共2005兲.
     tional one contact that is discussed in Sec. IV A 2. Closing        关50兴 M. Wyart, L. E. Stilbert, S. R. Nagel, and T. A. Witten, Phys.
     more than M = N f + 1 contacts will require further compression          Rev. E 72, 051306 共2006兲.
     and significantly larger deformation of the particles.              关51兴 There is some ambiguity in defining the pair-correlation func-
关37兴 P. M. Chaikin, A. Donev, W. Man, F. H. Stillinger, and S.                tion for bi-dispersed packings, leading to ambiguity in the ex-
     Torquato, Ind. Eng. Chem. Res. 45, 6960 共2006兲.                          ponent.
关38兴 Note that in our notation a self-stress has dimensions of force,    关52兴 J. H. Conway and S. Torquato, Proc. Natl. Acad. Sci. U.S.A.
     rather than force per unit area as in the engineering literature.         103, 10612 共2006兲.




                                                                  051304-32
