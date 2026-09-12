                                                 RASP: Revisiting 3D Anamorphic Art for Shadow-Guided Packing of
                                                                        Irregular Objects

                                              Soumyaratna Debnath1 * Ashish Tiwari1 * Kaustubh Sadekar 2 Shanmuganathan Raman1
                                                      1
                                                        Indian Institute of Technology Gandhinagar 2 Portland State University
                                                    {debnathsoumyaratna, ashish.tiwari, shanmuga}@iitgn.ac.in, ksadekar@pdx.edu
arXiv:2504.02465v1 [cs.GR] 3 Apr 2025




                                        Figure 1. (a) An ensemble of arbitrary shapes casting the shadow of alphabets CVPR and numbers 2025, (b) a set of irregular objects
                                        packed inside a face-shaped container, (c) an assembly of parts of a vessel obtained through multi-view shadow guidance via RASP.

                                                                    Abstract                                1. Introduction

                                        Recent advancements in learning-based methods have                  For centuries, artists have used their expressions to redefine
                                        opened new avenues for exploring and interpreting art               the boundaries of visual art, demonstrating how art shapes
                                        forms, such as shadow art, origami, and sketch art, through         reality and influences human perception. Their work has
                                        computational models. One notable visual art form is 3D             also broadly impacted technology, design, and engineering.
                                        Anamorphic Art in which an ensemble of arbitrarily shaped           In this work, we explore using a unique visual art form,
                                        3D objects creates a realistic and meaningful expression            3D Anamorphic Art, to tackle challenges in irregular object
                                        when observed from a particular viewpoint and loses its co-         packing and extend this approach to part assembly.
                                        herence over the other viewpoints. In this work, we build on           Interestingly, we are not alone in using (and, in fact,
                                        insights from 3D Anamorphic Art to perform 3D object ar-            developing) artistic expressions to address applications in
                                        rangement. We introduce RASP, a differentiable-rendering-           computer vision. For example, DeepDream [24] uses GAN-
                                        based framework to arrange arbitrarily shaped 3D objects            based style transfer to apply the style of classical paintings,
                                        within a bounded volume via shadow (or silhouette)-guided           like those of Van Gogh or Picasso, to contemporary im-
                                        optimization with an aim of minimal inter-object spacing            ages. RePaint [34] leverages deep learning and 3D printing
                                        and near-maximal occupancy. Furthermore, we propose                 to replicate the colors and textures of paintings by optimiz-
                                        a novel SDF-based formulation to handle inter-object in-            ing ink layering. ScribGen [7] creates human-like scrib-
                                        tersection and container extrusion. We demonstrate that             bles and hand-strokes in different styles. Beyond images,
                                        RASP can be extended to part assembly alongside ob-                 researchers have expanded artistic techniques into 3D anal-
                                        ject packing considering 3D objects to be “parts” of an-            ysis and understanding, as in Shadow Art [23], which uses
                                        other 3D object. Finally, we present artistic illustrations of      shadows for 3D reconstruction, sketch-based 3D generation
                                        multi-view anamorphic art, achieving meaningful expres-             [32], expressive hand movements [8], and the design of knot
                                        sions from multiple viewpoints within a single ensemble.            configurations for realistic visual effects [9]. In this work,
                                                                                                            we draw upon insights from 3D Anamorphic Art to address
                                                                                                            an important problem of packing arbitrarily shaped objects
                                           * Equal Contribution | Project Page                              within a 3D bounding volume (or container). Packing has
                                                                  Figure 3. An example depicting the packed state of a cuboidal
Figure 2. Illustration of 3D Anamorphic Art (a, b): Portrait of   container and the associated silhouettes/shadows.
Nikola Tesla and Bedřich Smetana by Patrick Proško and Shadow
Art (c, d): Dirty White Trash and Wild Mood Swing by Tim Nobel
and Sue Webster.                                                  approach addresses the irregular object packing problem.
                                                                  However, if these elements are “parts” of another object al-
                                                                  together, it naturally extends to the part assembly problem.
numerous practical applications, spanning fields such as              A key challenge in existing packing methods is man-
combinatorial optimization [22, 33], computational geom-          aging overlaps or intersections among the elements to be
etry [12, 20], computer vision and graphics [2, 18, 31], ma-      packed. While some methods focus on simple geometries
chine learning [11, 46], robotics [35, 38, 44], and logistics     like cuboids [4, 43], spheres [21], cylinders [36], or ellip-
and manufacturing [47].                                           soids [13], or rely on assumptions of convexity or concavity
    3D Anamorphic Art. 3D Anamorphic Art involves ar-             in polyhedrons [19, 30, 37], often using simple heuristics
ranging objects in 3D space such that the arrangement ap-         [17, 27], others handle irregular shapes by employing vox-
pears coherent and meaningful only from the specific view-        elized representations [1, 6], which tend to be susceptible
point(s). In contrast, from any other view, it appears ran-       to approximation errors. This work introduces a signed-
dom. For example, artist Patrick Proško used this technique      distance field (SDF) approach to manage inter-object inter-
at the Illusion Art Museum Prague by arranging electrical         section and container extrusion.
appliances to form a portrait of Nikola Tesla [28] (Figure 2          Contributions. In this work, we introduce RASP –
(a)) and arranging musical instruments to create a likeness       Revisiting 3D Anamorphic art for Shadow-guided Packing
of the musician Bedřich Smetana [29] (Figure 2 (b)). This        of Irregular Objects. Given a set of arbitrarily shaped ob-
concept also extends to shadows cast by such arrangements         jects, a bounding volume (or container), and information
under particular camera-light configurations. For instance,       about the appearance of its projection/shadows from differ-
artists Tim Noble and Sue Webster created Dirty White             ent viewpoints in the packed state:
Trash [25] and Wild Mood Swings [26], where carefully             • We propose a differentiable rendering-based framework
arranged trash and wooden pieces cast shadows of people              to tackle irregular object packing by drawing inspira-
sitting beside each other (see Figure 2 (c, d)). Whether             tion from 3D Anamorphic Art. Our goal is to achieve
through perspective views from specific viewpoints or shad-          near-maximal occupancy and minimal inter-object spac-
ows created under particular camera-light configurations,            ing within a known bounding volume.
these projections reveal valuable insights about the arrange-     • We present a novel SDF-based approach to manage inter-
ment of objects in 3D space.                                         object intersections and object-container extrusions, en-
    Relation with Object Packing. Consider a cuboidal                hanced by an image-based loss function.
bounding volume (or container), as depicted in Figure 3.          • We demonstrate that RASP can also be applied to part
When fully packed, this cuboid would appear as a rectangle           assembly without the need for explicit 3D ground truth
or square upon being viewed orthographically along any of            supervision. Additionally, we illustrate compelling visual
its faces. Similarly, it would cast rectangular or square shad-      effects that cater to multi-view anamorphic art.
ows under the same viewing configuration. Ideally, gaps           • To the best of our knowledge, this is the first approach to
between the objects would appear as holes in the shadow              address packing (and part assembly) using only shadows
from at least one perspective. By considering these shad-            or projections, guided by the principles of differentiable
ows (technically binary images or silhouettes of the packed          rendering.
state) as target projections, we aim to arrange arbitrarily           Through this work, we push the boundaries of 3D
shaped elements within a bounding volume, thereby tack-           anamorphic art to address an important research ques-
ling the packing problem.                                         tion: can shadows be used to automatically find an opti-
    Interestingly, this approach also allows for bounding vol-    mal arrangement of arbitrarily shaped 3D objects within
umes of arbitrary shapes, where the target projections are        a bounded volume? While our framework aims to provide
simply the volume’s appearance from multiple viewpoints.          practical solutions, it does not always yield an optimal ar-
If the elements to be arranged are whole 3D objects, this         rangement due to the NP-hard nature of the packing prob-
Figure 4. The proposed differentiable rendering-based pipeline for RASP. We use Adam optimizer with a learning rate of 1e − 2 to 1e − 4
over 1000 iterations. Packing the Kitchen dataset (106 objects, 80000 grid points) takes nearly 17 minutes, and reassembly for each object
in the Fantastic Breaks dataset (2 parts, 80000 grid points) takes under 3 minutes.


lem [10]. Nonetheless, this work introduces a new perspec-              ing irregular objects is to handle object collision detection
tive on solving the 3D packing and arrangement problem                  or intersection/overlap avoidance. Several different geo-
using shadows as a guiding mechanism.                                   metric representations of objects (say, objects tightly bound
                                                                        by a sphere or cuboid [45]) have been assumed by differ-
2. Related Works                                                        ent methods for collision detection and packing optimiza-
                                                                        tion. Romanova et al. [1] pose the packing problem as
Object packing has been addressed using heuristic-based,                a nonlinear optimization problem and propose quasi-phi
model-based, learning-based, or policy-based (online) ob-               functions for simple concave polyhedrons to describe non-
ject packing. Several methods have assumed simple object                overlapping and distance constraints. However, obtaining
geometries, such as cuboids [4, 43], spheres [21], cylinders            a local optimum takes longer, even with free translations
[36], or ellipsoids [13], or leverage convexity and/or con-             and rotations. A few works [2, 45] learned to decompose
cavity in polyhedrons [19, 30, 37]. This section primarily              the object into multiple small parts to perform packing to
discusses the methods dealing with irregular object pack-               reduce the supporting materials, build time, and assembly
ing.                                                                    costs of 3D printing. While [2] used voxel-based represen-
    Heuristic-based Methods. Several previous attempts                  tation, [45] used level sets to represent the object parts.
at object packing were primarily based on heuristic strate-                 Moreover, Zhao et al. [47] and Zhuang et al. [48] divide
gies. One method proposed by Wang et al. [40] sequen-                   the objects into convex shapes for efficient collision detec-
tially places objects employing the Deepest Bottom Left                 tion in physical simulation and pack the objects either using
Fill (DBLF) heuristic strategy. However, it is shown to                 shaking of the container as per the dynamic principle or re-
create holes, leading to empty spaces. Later, Wang and                  inforcement learning in an online manner, respectively. Our
Hauser [39] addressed this limitation by reducing unfilled              work does not focus on online packing. Cui et al. [5] per-
gaps through height-map minimization, which in itself ig-               formed efficient collision metric computation in the spectral
nores the difference between positions at the same level.               domain using voxel representation and Fast Fourier Trans-
HAPE3D [19], another heuristic-based algorithm, deploys                 form (FFT) for discrete placement search. They deploy a
the principle of the minimum total potential energy for                 greedy strategy to sort objects by volume from largest to
irregular polyhedrons. Even after allowing free transla-                smallest and then pack sequentially to minimize the dis-
tions and rotations, it fails to achieve high packing density.          tance between the new and already placed objects at each
Lamas et al. [15] voxelized irregular objects and used meta-            placement.
heuristic algorithms to optimize voxel representation that is               The closest to our setting is the work by Ma et al. [20]
limited due to memory constraints. Heuristic-based meth-                that optimizes the orientation and position of the objects
ods generally apply well to objects with only a few facets              from their initial placement. However, their approach is
and struggle to achieve a high packing density while deal-              multi-stage, involving combinatorial optimization that in-
ing with complex irregular objects.                                     cludes object swapping, enlargement, and replacement to
    Learning-Based Methods. The key challenge for pack-                 reduce the gaps between the objects. Furthermore, they
Figure 5. (a) Target shadow a duck-shaped container, optimized arrangement with mesh intersections. Mesh enclosed within (b) sphere and
(c) cube where the intersection region doesn’t include object meshes. (d) SDF of two non-intersecting and intersecting objects (intersecting
points are marked in red), and SDF transformation within the container.


also minimize the height of a container to obtain an opti-               based 3D packing and part assembly.
mal one through binary search. Due to repeated processing,
the method is heavily time-consuming. In contrast, given
                                                                         3.2. Proposed Approach
a set of irregular objects, ours is a single-stage end-to-end            The flow of the proposed methodology has been outlined
optimization pipeline that performs packing only via 2D                  in Figure 4. Consider a set of N arbitrarily shaped objects
shadow guidance without any intense calculation within the               S = {O1 , O2 , . . . , ON } such that each Oi is represented
3D bounding volume. While Ma et al. [20] have the infor-                 as a triangular mesh, an arbitrarily shaped bounding con-
mation about the object set and process only one object at               tainer C located inside the camera viewing volume V, and
a time, sequentially determining the initial placement, our              shadow projection configuration X = {Xk = (Ik , Pk )|k =
proposed method considers a set of objects at a time.                    1, 2, . . . , K}. Here, {Ik }K
                                                                                                      k=1 are the target images under
                                                                         the camera configuration {Pk }K   k=1 . Essentially, the cam-
3. Method                                                                era configuration Pk = (Rk , tk ) corresponds to the cam-
                                                                         era extrinsic parameters associated with image Ik . With S,
3.1. Overview
                                                                         C, and X as input to the differentiable renderer R, the ob-
The key idea of our work is to arrange a set S of arbi-                  jective here is to learn the optimal arrangement of objects
trarily shaped 3D objects within an arbitrarily shaped con-              in set S inside the container C placed within the viewing
tainer C such that the resulting arrangement casts K differ-             volume V such that the resulting images {Ibk }K   k=1 rendered
ent shadows (projections) when viewed from K different di-               under camera configurations {Pk }K    k=1 are close to the cor-
rections using a differentiable rendering-based optimization             responding target images {Ik }K  k=1 . From  the shadow’s  per-
pipeline. Interestingly, the problem has two interpretations             spective, the target images are silhouettes, and we assume
depending on how we consider the set S.                                  that the light (to cast the shadows) will be co-located with
   (a) 3D Packing problem: when S contains arbitrarily                   the camera. Finding the arrangement of objects is equiv-
shaped 3D objects and C is the bounding container within                 alent to finding the rigid transformation, i.e., rotation and
the viewing volume.                                                      translation {Ri , ti }N
                                                                                               i=1 of each object Oi in set S. We use
   (b) Part Assembly problem: when S contains “parts” of                 quaternions for obtaining rotations - (a) to avoid gimble
a 3D object (O) where this object O itself is treated as the             lock through other representations like axis-angle rotation
container C.                                                             or rotation composition of rotation along x − y − z axes, (b)
   In the case of packing, we might not always have a                    for smooth interpolation, and (c) to learn a smaller number
ground truth or a unique solution, i.e., objects can be ar-              of parameters compared to the rotation matrices. Specif-
ranged in multiple optimal ways to maximize occupancy                    ically, we obtain the angle of rotations across each of the
and minimize spaces. However, we have a ground truth                     coordinate axes and convert them to quaternion representa-
shape in a part assembly whose parts can be assembled only               tion for optimization.
in one way. We demonstrate how this is implemented in
                                                                         3.2.1. Objective Function
Section 4. Overall, we propose a differentiable-rendering-
based framework that naturally caters to both these require-             We propose a combined loss function consisting of an SDF-
ments, in addition to generating multi-view anamorphic art.              based intersection loss, an image-based loss, and an object-
Inspired by computational visual arts, some of the recent                container extrusion loss, as per Equation 1.
works based on shadow art [8, 9, 23] have demonstrated the                                  \centering \mathcal {L}_{total} = \mathcal {L}_{sil} + \mathcal {L}_{is} + \lambda \mathcal {L}_{ext} \label {ref:total_loss}    (1)
potential of 3D shape understanding, analysis, and recon-
struction through shadows. In this work, we take the first               Here, we set λ = 0.001
step towards leveraging the benefit of differentiable render-               Image-based (Silhouette) Loss. A straightforward ap-
ing and principles of visual arts [42] to propose shadow-                proach is to optimize each object’s rotation and translation
Figure 6. Visualization of 3D Object packing into a cuboidal container using RASP over four different object categories from [47]. Each
instance is labeled with the number of objects packed in the container and the packing density.




Figure 7. Qualitative comparison of object packing with RASP
and Zhao et al. [47] for same set and same number of objects.
Best viewed in PDF with zoom.                                                                                                                             Figure 8. (Top) Loss curves for packed configuration in Figure 6
                                                                                                                                                          (solid line) & Figure 10 (dashed line). (Bottom) Effect of different
                                                                                                                                                          loss terms on the packing. Best viewed in pdf with zoom.
parameters based on image rendering loss, such as mean
squared error, as per Equation 2.
                                                                                                                                                          essary gaps.
                                                                                                                                                             Intersection Loss. To overcome these challenges, we
           \mathcal {L}_{sil} = \frac {1}{MNK}\sum _{k=1}^{K} \sum _{i=1}^{MN} ||I_{k}(i) - \widehat {I_{k}}(i)||_{2}^{2} \label {eq:image_loss}    (2)
                                                                                                                                                          propose an SDF-based approach to handle both object-
                                                                                                                                                          object intersections and object-container extrusion. The
Here, M N is the total number of pixels in the image. As                                                                                                  signed distance field (SDF) provides the shortest distance
shown in Figure 5 (a), the projection of the arrangement                                                                                                  from a point to the surface, with a negative sign indicating
may appear feasible (apart from a few gaps where more ob-                                                                                                 the point is inside and a positive sign indicating it is out-
jects could fit), but in 3D, objects can still intersect within a                                                                                         side the object. Specifically, we pre-compute the SDF of
duck-shaped container.                                                                                                                                    each mesh (using [41]) at fixed query points within the con-
   Therefore, the loss functions should penalize mesh in-                                                                                                 tainer C (a few milliseconds on GPU) and deform the SDFs
tersections. However, handling mesh intersections is com-                                                                                                 with every update of the learned rotation and translation pa-
plex; some methods [14] detect intersections by evaluating                                                                                                rameters. Rather than recalculating the SDF for each rigid
each triangular face of one mesh against others, which is                                                                                                 transformation, we warp the previous SDF using a linear
computationally costly and impractical for large numbers                                                                                                  transformation to match the new configuration, as shown in
of meshes. To simplify intersection computation, some                                                                                                     Figure 5 (d). The degree of intersection, thus, can be deter-
approaches enclose objects within unit spheres or cubes,                                                                                                  mined by identifying points where more than one object has
finding intersections among these simpler bounding shapes                                                                                                 a negative SDF value, as marked in red in Figure 5 (d).
[45]. Although faster, this approach often fails with asym-                                                                                                  Let the SDF of the object Oi at a point p after a rigid
metrically shaped objects, as intersections between bound-                                                                                                transformation (updated rotation and translation) has been
ing spheres or cubes may not correspond to intersections                                                                                                  applied to Oi be denoted by SeOi (p). One could simply
among the actual object meshes, as shown in Figure 5 (b,                                                                                                  consider the amount of intersection to be proportional to the
c). This can lead to excessive penalization of intersections,                                                                                             number of objects under intersection at any point within the
causing the network to push objects apart and create unnec-                                                                                               container, i.e., Dis (p) = {i ∈ {1, 2, ...N }|SeOi (p) < 0} .
Figure 9. Illustration of packing of 24 cubes, each of dimensions
                                                                                                                                                                                     Figure 10. Illustration of packing arbitrarily shaped objects into
1 × 1 × 1 cubic units, into a container of dimensions 6 × 6 × 6
                                                                                                                                                                                     arbitrarily shaped containers. The initial containers, the set of ob-
cubic units, with varying silhouette widths to simulate physically
                                                                                                                                                                                     ject shapes to be packed, and the final packed configuration are
correct packing for N < Nmax .
                                                                                                                                                                                     shown in the figure.

However, we observed that considering the SDF value in-
stead of just the count provides smoother guidance to re-                                                                                                                            4. Experiments
solve the intersections. Therefore, we define the degree of                                                                                                                          In this section, we showcase the results obtained through
intersection Dis (p) as the sum of the (negative of) SDFs of                                                                                                                         the RASP framework for irregular object packing drawing
the objects that contain point p within them at every opti-                                                                                                                          parallels with 3D Anamorphic art. Furthermore, we extend
mization step, such that,                                                                                                                                                            RASP to applications like part assembly and creating artis-
                                                                                                                                                                                     tic illustrations.
               \centering D_{is}(\mathbf {p}) = \sum _{\{\forall O_{i} | \widetilde {S}_{O_{i}}(\mathbf {p}) < 0\}} - \widetilde {S}_{O_{i}}(\mathbf {p})                      (3)
                                                                                                                                                                                     4.1. Irregular Object Packing
                                                                                                                                                                                     For 3D object packing, we demonstrate the results majorly
   Here, Dis (p) > 1 indicates that there is an intersection                                                                                                                         on the objects from the IR-BPP dataset [47], which contains
of at least two objects at the point, and Dis (p) = 0 repre-                                                                                                                         objects from four categories: General, Kitchen, ABC, and
sents that the point p is not inside any object. Considering                                                                                                                         Block Out. A few other illustrations also include objects
the set of query points Cp inside the container C, the inter-                                                                                                                        from the VOLMAP dataset [3] and SilNet dataset [49].
section loss is defined as per Equation 4.                                                                                                                                              Following the existing literature of 3D object packing,
                                                                                                                                                                                     we define the packing efficiency/density (ρ), as per Equa-
                                                   \centering \mathcal {L}_{is} = \sum _{\mathbf {p} \in \mathcal {C}_{p}} D_{is}(\mathbf {p}) \label {eq:inter_loss}          (4)   tion 6.
                                                                                                                                                                                                                 \centering \rho = \sum _{O_{i}\in \mathcal {C}}\frac {|O_{i}|}{|\mathcal {C}|} \label {eq:6}    (6)
   Container Extrusion Loss. Let Vi be the set of vertices
of the triangular mesh corresponding to the object Oi and                                                                                                                            Here, |Oi | and |C| are the volume of the ith object and con-
SC be the SDF of the container C. We define the container                                                                                                                            tainer volume, respectively.
extrusion loss as per Equation 5                                                                                                                                                        Figure 6, compares the packing density of irregular 3D
                                                                                                                                                                                     objects from different categories into a typical cuboidal con-
                                                                                                                                                                                     tainer. Interestingly, RASP does not require any regularity
                  \centering \mathcal {L}_{ext} = \sum _{i=1}^{N} \sum _{\mathbf {v} \in V_{i}} \text {max}(-\epsilon , S_{\mathcal {C}}(\mathbf {v})) \label {eq:ext_loss}    (5)
                                                                                                                                                                                     in object shapes and can handle arbitrary shapes of different
                                                                                                                                                                                     sizes, achieving reasonably good packing configurations.
Here, ϵ, the distance between a vertex and the container’s                                                                                                                              Deciding the number of objects that can be maximally
boundary, creates a “buffer zone” around the container                                                                                                                               packed within a container is crucial for optimal packing. To
boundary to control when the extrusion loss begins to be                                                                                                                             start with, we decide the initial number of objects as Ninit
active. While a higher value of ϵ hinders the movement                                                                                                                               based on the average volume of the objects and the con-
of objects inside the container, a very small value leads                                                                                                                            tainer volume, such that Ninit = |O||C|  avg
                                                                                                                                                                                                                                  . Consider Nmax
to portions of objects suddenly extruding out of the con-                                                                                                                            as an unknown upper bound, i.e., the maximum a physical
tainer boundary, leading to an unstable optimization. We                                                                                                                             container can accommodate. If Ninit < Nmax , we draw an-
find ϵ = 0.01 to be a reasonable value that avoids penal-                                                                                                                            other set of Nk objects from the pool (if available) and again
izing objects that are slightly inside the container but still                                                                                                                       optimize the arrangement with Ninit + Nk based on the tar-
close to the boundary. We observed that in some cases, sil-                                                                                                                          get silhouettes of projection. In case this exceeds Nmax , the
houette loss was just enough to contain the objects with the                                                                                                                         remaining objects either start extruding out of the container
container, especially for simple shapes. However, for more                                                                                                                           or intersecting heavily within the container depending on
irregular shapes with asymmetric and skewed spread, extru-                                                                                                                           the predominance of Lis or Lext , respectively. All the re-
sion loss proved to be helpful.                                                                                                                                                      sults correspond to N = Nmax objects that can maximally
Figure 11. Extending RASP to perform part reassembly of broken objects. The figure showcases the target silhouettes and broken parts
reassembled using RASP.

fit inside the container with no intersection, a condition es-       alter the object dimensions. However, since their imple-
sential for real-world applicability. Moreover, the objects          mentation is unavailable online, we choose to quantitatively
are randomly initialized within the container before opti-           compare the average packing efficiency across different ob-
mization. We discuss the effect of different initialization          jects. Although different from ours, we also compared our
strategies in the supplementary.                                     average packing efficiency of a physically inspired rein-
    Due to silhouette or shadow-guided optimization, the re-         forcement learning-based online packing method by Zhao
sulting arrangement can sometimes be physically inaccu-              et al. [47] over their dataset to establish the efficacy of our
rate. As shown in Figure 9, when the number of objects               optimization-based methods learning solely from 2D image
N is less than the maximum capacity Nmax , the arrange-              guidance. Zhao et al. [47] look at only one or a few ob-
ment often floats within the container rather than settling at       jects at a time, and packing efficiency is dependent on the
the bottom. While such effects are inherent to this type of          sequence in which the objects arrive. Moreover, the ob-
optimization-based framework, we demonstrate that merely             ject placement is guided by the dynamics and constraints of
adjusting the width of the silhouettes would effectively con-        physics. In contrast, RASP - an offline method, takes a more
strain the objects to rest at the bottom of the container in         global standpoint by optimizing all N ≤ Nmax objects at a
Figure 9 progressively.                                              time. Overall, RASP obtains an average of 45% occupancy
    Arbitrarily Shaped Container. Owing to its design to             over the four different categories of the IR-BPP dataset [47]
derive insights from the projected silhouettes, RASP can             which is better than Ma et al. [20] (34%) and drops below
also accommodate arbitrarily shaped containers, as shown             that of Zhao et al. [47] (51.9%) evaluated over the objects
in Figure 1 (b) and Figure 10. Similar to multi-view shape           from online packing dataset. Moreover, Ma et al. [20] bears
optimization, the target shadows are essentially the silhou-         an average optimization time of 40.55 minutes while RASP
ettes of the container from 5 different views. Figure 10 de-         achieves the same in ∼ 15 minutes.
picts the packing on donut-shaped and squirrel-shaped con-              For a qualitative comparison over samples from IR-BPP
tainers.                                                             dataset, we adapt [47] to align closest to our setting. Specif-
    Effect of loss terms. Figure 8 (top) shows the conver-           ically, we generate 100 random sequences of the same set
gence of each of the loss terms for illustrations in Figure          (and same number) of objects from each IR-BPP dataset
6 and Figure 10. The intersection density for all the re-            category (as in Figure 6) and report the best configuration
sults is zero, offering a multi-view consistent, intersection-       to compare with RASP in Figure. 7. Due to implementation
free/non-overlapping configuration. Figure 8 (bottom) also           constraints of [47], we could not assign different colors to
illustrates the impact of different loss terms in addition to        objects or obtain multiple views of the packed arrangement
observations in Figure 5 for Lsil vs Lsil + Lin . Overall,           of [47], and hence, we compared only the top view. RASP
we find that extrusion term Lext acts as a regularizer, pre-         performs similar to or slightly better than the physics-aware
venting objects from drifting too far apart to avoid inter-          method for the same object set.
sections. While the intersection remains zero without Lext ,
its inclusion improves the rendered silhouette by reducing           4.2. 3D Part Assembly
Lsil . Notably, objects are positioned closer together when          Part assembly using RASP also shares similarities with
Lext is applied.                                                     multi-view geometry optimization. However, instead of op-
    Comparison with existing methods. Out of several rel-            timizing a single shape, RASP learns the rigid transforma-
evant works on 3D object packing (as described in Section            tions of different parts of a single shape to obtain a 3D con-
2), the work by Ma et al. [20] is the closest to our opti-           sistent arrangement across all the views. For demonstrating
mization setup (not guided by shadows) whose setup is dif-           part assembly, we used the Fantastic Breaks dataset [16]
ferent from RASP since it involves swapping, replacement             that consists of paired 3D scans of real-world broken ob-
with new objects, and object enlargement - which we be-              jects and their complete counterparts. Figure 11 demon-
lieve is not practical in a real-world setup where we cannot         strates some qualitative results on reassembling broken ob-
Figure 12. (a) & (b) use objects from the Kitchen dataset to generate 2-view and 3-view 3D anamorphic art. (c) Multi-view pixelated
portraits generated using RASP with artistic texture applied. (d) RASP recreates the famous cover page of the book Gödel, Escher, Bach
by Douglas Hofstadter. The 3D and dynamic visualization of these and more related results are provided in the supplementary.

jects. Notably, it does so solely via silhouette guidance             rendered images highlights the creative potential of RASP.
without the need for any explicit 3D ground truth super-              In Figure 12 (d) we recreate the famous artistic cover page
vision.                                                               of the Book by Douglas Hofstadter featuring blocks casting
                                                                      shadows of the first letters of artists – Gödel, Escher, and
4.3. Multi-view Anamorphic Art                                        Bach. Overall, RASP is a versatile optimization pipeline
We also leverage RASP to reinterpret and construct differ-            stressing on the fact that shadows do provide limited yet
ent forms of multi-view anamorphic art. Thus far, we have             useful cues for 3D understanding and artistic exploration.
seen that silhouettes or shadows do provide important cues
for 3D arrangement. However, these binary images alone                5. Conclusion
cannot create interesting artistic illustrations. Therefore, we
also seek guidance from colored or textured images. Take,             We introduce RASP, a differentiable rendering-based opti-
for example, the portrait of Nikola Tesla shown in Figure 2           mization framework for irregular 3D object packing, part
(a). One approach would be to search for suitable objects             assembly, and recreating artistic illustrations, taking guid-
and apply heuristic methods to arrange them in a way that             ance from images, whether in the form of binary silhouettes,
recreates the portrait’s appearance. Alternatively, one could         textured RGB images, or simple portrait sketches. The cur-
collect and randomly arrange objects (like those in Figure            rent offline strategy does not account for physical dynam-
2 (c)) within the outline of the silhouette, then paint the           ics, such as the influence of gravity on object placement.
arrangement to revive the essence of the portrait. Follow-            Additionally, RASP struggles with multi-part (more than 2
ing the latter approach, RASP uses a two-stage optimiza-              or 3 parts) part assembly, particularly symmetrical and/or
tion procedure, where first, it arranges the discrete objects         identical parts. An interesting potential extension of this
in a 3D space through silhouette matching across a set of             work would be to incorporate physics-based guidance for
views and later performs rendering-based texture optimiza-            the packing to be more physically consistent. We believe
tion (integrated as an add-on) over the finalized arrangement         that there are plenty of untapped capabilities in shadows
to match the target textures. Figure 12 (a) illustrates how           that drive 3D understanding, and RASP presents a few of
this strategy allows RASP to recreate multi-view portraits            them. We anticipate that this work would attract researchers
of Nikola Tesla and Marie Curie across two non-orthogonal             from different domains to use shadows or silhouettes for ap-
views that are 120◦ apart using objects from the Kitchen              plications like partitioning and reconfiguration of complex
dataset. Furthermore, it also generates consistent ensem-             3D objects into simpler forms, multi-part part assembly, dy-
bles that are meaningful across three non-orthogonal views,           namic visual arts, CAD design, and handling non-rigid de-
as shown in Figure 12 (b), giving a visually plausible ap-            formations.
pearance of Pokémon, Wall-e, and Minion. In figure 12 (c)            Acknowledgments.          This work is supported by the
we obtain 3D arrangements using binary images and then                Prime Minister Research Fellowship (PMRF) grant and the
apply artistic textures to create unique 3D illustrations. The        Jibaben Patel Chair in Artificial Intelligence. We also thank
resemblance of the textured arrangement and the associated            Prajwal Singh, IIT Gandhinagar, for his valuable inputs.
References                                                          [16] Nikolas Lamb, Cameron Palmer, Benjamin Molloy, Sean
                                                                         Banerjee, and Natasha Kholgade Banerjee. Fantastic breaks:
 [1] Thomas Byholm, Martti Toivakka, and Jan Westerholm.                 A dataset of paired 3d scans of real-world broken ob-
     Effective packing of 3-dimensional voxel-based arbitrar-            jects and their complete counterparts. In Proceedings of
     ily shaped particles. Powder Technology, 196(2):139–146,            the IEEE/CVF Conference on Computer Vision and Pattern
     2009. 2                                                             Recognition, pages 4681–4691, 2023. 7
 [2] Xuelin Chen, Hao Zhang, Jinjie Lin, Ruizhen Hu, Lin Lu,        [17] Max Limper, Nicholas Vining, and Alla Sheffer. Box cutter:
     Qi-Xing Huang, Bedrich Benes, Daniel Cohen-Or, Baoquan              atlas refinement for efficient packing via void elimination.
     Chen, et al. Dapper: decompose-and-pack for 3d printing.            ACM Trans. Graph., 37(4):153, 2018. 2
     ACM Trans. Graph., 34(6):213–1, 2015. 2, 3
                                                                    [18] Hao-Yu Liu, Xiao-Ming Fu, Chunyang Ye, Shuangming
 [3] Gianmarco Cherchi and Marco Livesu. VOLMAP: A large                 Chai, and Ligang Liu. Atlas refinement with bounded pack-
     scale benchmark for volume mappings to simple base do-              ing efficiency. ACM Transactions on Graphics (TOG), 38
     mains. Computer Graphics Forum, 42(5), 2023. 6                      (4):1–13, 2019. 2
 [4] Teodor Gabriel Crainic, Guido Perboli, Roberto Tadei, et al.   [19] Xiao Liu, Jia-min Liu, An-xi Cao, and Zhuang-le Yao.
     Recent advances in multi-dimensional packing problems.              Hape3d—a new constructive algorithm for the 3d irregular
     New technologies-trends, innovations and research, 1:91–            packing problem. Frontiers of Information Technology &
     110, 2012. 2, 3                                                     Electronic Engineering, 16(5):380–390, 2015. 2, 3
 [5] Qiaodong Cui, Victor Rong, Desai Chen, and Wojciech Ma-        [20] Yuexin Ma, Zhonggui Chen, Wenchao Hu, and Wenping
     tusik. Dense, interlocking-free and scalable spectral pack-         Wang. Packing irregular objects in 3d space via hybrid opti-
     ing of generic 3d objects. ACM Trans. Graph., 42(4):141–1,          mization. In Computer graphics forum, pages 49–59. Wiley
     2023. 3                                                             Online Library, 2018. 2, 3, 4, 7
 [6] ACJ De Korte and HJH Brouwers. Random packing of digi-         [21] Alan L Mackay. A dense non-crystallographic packing
     tized particles. Powder technology, 233:319–324, 2013. 2            of equal spheres. Acta Crystallographica, 15(9):916–918,
 [7] Soumyaratna Debnath, Ashish Tiwari, and Shanmuganathan              1962. 2, 3
     Raman. Scribgen: Generating scribble art via metaheuristics.   [22] Silvano Martello, David Pisinger, and Daniele Vigo. The
     SIGGRAPH Asia Art Paper, 2024. 1                                    three-dimensional bin packing problem. Operations re-
 [8] Aalok Gangopadhyay, Prajwal Singh, Ashish Tiwari, and               search, 48(2):256–267, 2000. 2
     Shanmuganathan Raman. Hand shadow art: A differentiable        [23] Niloy J Mitra and Mark Pauly. Shadow art. ACM Transac-
     rendering perspective. Pacific Graphics, the Eurographics           tions on Graphics, 28(5):156–1, 2009. 1, 4
     Association, 2023. 1, 4                                        [24] Alexander Mordvintsev, Christopher Olah, and Mike Tyka.
 [9] Aalok Gangopadhyay, Paras Gupta, Tarun Sharma, Prajwal              Inceptionism: Going deeper into neural networks. Google
     Singh, and Shanmuganathan Raman. Search me knot, render             research blog, 20(14):5, 2015. 1
     me knot: Embedding search and differentiable rendering of      [25] Tim Nobel and Sue Webster. Dirty white trash (with gulls),
     knots in 3d. In Computer Graphics Forum, page e15138.               1998. https://www.artworksforchange.org/
     Wiley Online Library, 2024. 1, 4                                    portfolio/tim-noble-and-sue-webster/. 2
[10] Juris Hartmanis. Computers and intractability: a guide to      [26] Tim Nobel and Sue Webster.             Wild mood swings,
     the theory of np-completeness (michael r. garey and david s.        2009. http : / / www . timnobleandsuewebster .
     johnson). Siam Review, 24(1):90, 1982. 3                            com/wild_mood_swings_2009-10.html. 2
[11] Haoyuan Hu, Xiaodong Zhang, Xiaowei Yan, Longfei Wang,         [27] Tobias Nöll and Didier Strieker. Efficient packing of arbi-
     and Yinghui Xu. Solving a new 3d bin packing problem                trary shaped charts for automatic texture atlas generation. In
     with deep reinforcement learning method. arXiv preprint             Computer Graphics Forum, pages 1309–1317. Wiley Online
     arXiv:1708.05930, 2017. 2                                           Library, 2011. 2
[12] Ruizhen Hu, Juzhan Xu, Bin Chen, Minglun Gong, Hao             [28] Patrick Proško. Nikola tesla, 2015. https://www.
     Zhang, and Hui Huang. Tap-net: transport-and-pack us-               prosko.cz/anamorphosis/nikola-tesla. 2
     ing reinforcement learning. ACM Transactions on Graphics       [29] Patrick Proško. Bedrich semtana, 2019. https://www.
     (TOG), 39(6):1–15, 2020. 2                                          prosko.cz/anamorphosis/bedrich-smetana. 2
[13] Josef Kallrath. Packing ellipsoids into volume-minimizing      [30] Tatiana Romanova, Julia Bennell, Yuriy Stoyan, and Alek-
     rectangular boxes. Journal of Global Optimization, 67:151–          sandr Pankratov. Packing of concave polyhedra with contin-
     185, 2017. 2, 3                                                     uous rotations using nonlinear optimisation. European Jour-
[14] Tero Karras. Maximizing parallelism in the construc-                nal of Operational Research, 268(1):37–53, 2018. 2, 3
     tion of bvhs, octrees, and k-d trees. In Proceedings of        [31] Daniel Saakes, Thomas Cambazard, Jun Mitani, and Takeo
     the Fourth ACM SIGGRAPH/Eurographics Conference on                  Igarashi. Paccam: material capture and interactive 2d pack-
     High-Performance Graphics, pages 33–37, 2012. 5                     ing for efficient material usage on cnc cutting machines. In
[15] Carlos Lamas-Fernandez, Julia A Bennell, and Antonio                Proceedings of the 26th annual ACM symposium on User in-
     Martinez-Sykora. Voxel-based solution approaches to the             terface software and technology, pages 441–446, 2013. 2
     three-dimensional irregular packing problem. Operations        [32] Kaustubh Sadekar, Ashish Tiwari, and Shanmuganathan Ra-
     Research, 71(4):1298–1317, 2023. 3                                  man. Shadow art revisited: a differentiable rendering based
     approach. In Proceedings of the IEEE/CVF Winter Con-            [46] Hang Zhao, Yang Yu, and Kai Xu. Learning efficient online
     ference on Applications of Computer Vision, pages 29–37,             3d bin packing on packing configuration trees. In Interna-
     2022. 1                                                              tional conference on learning representations, 2021. 2
[33] Steven S Seiden. On the online bin packing problem. Journal     [47] Hang Zhao, Zherong Pan, Yang Yu, and Kai Xu. Learning
     of the ACM (JACM), 49(5):640–671, 2002. 2                            physically realizable skills for online packing of general 3d
[34] Liang Shi, Vahid Babaei, Changil Kim, Michael Fos-                   shapes. ACM Transactions on Graphics, 42(5):1–21, 2023.
     hey, Yuanming Hu, Pitchaya Sitthi-Amorn, Szymon                      2, 3, 5, 6, 7
     Rusinkiewicz, and Wojciech Matusik. Deep multispectral          [48] Qiubing Zhuang, Zhonggui Chen, Keyu He, Juan Cao, and
     painting reproduction via multi-layer, custom-ink printing.          Wenping Wang. Dynamics simulation-based packing of ir-
     ACM Transactions on Graphics, 2018. 1                                regular 3d objects. Computers & Graphics, 123:103996,
[35] Rahul Shome, Wei N Tang, Changkyu Song, Chaitanya Mi-                2024. 3
     tash, Hristiyan Kourtev, Jingjin Yu, Abdeslam Boularias, and    [49] AP Zisserman and O Wiles. Silnet: Single-and multi-view
     Kostas E Bekris. Towards robust product packing with a min-          reconstruction by learning from silhouettes. In British Ma-
     imalistic end-effector. In 2019 International Conference on          chine Vision Conference. British Machine Vision Associa-
     Robotics and Automation (ICRA), pages 9007–9013. IEEE,               tion and Society for Pattern Recognition, 2017. 6
     2019. 2
[36] Yu Stoyan and A Chugay. Packing cylinders and rectangu-
     lar parallelepipeds with distances between them into a given
     region. European Journal of Operational Research, 197(2):
     446–455, 2009. 2, 3
[37] YG Stoyan, NI Gil, G Scheithauer, A Pankratov, and I Mag-
     dalina. Packing of convex polytopes into a parallelepiped.
     Optimization, 54(2):215–235, 2005. 2, 3
[38] Fan Wang and Kris Hauser. Robot packing with known
     items and nondeterministic arrival order. IEEE Transactions
     on Automation Science and Engineering, 18(4):1901–1915,
     2020. 2
[39] Fan Wang and Kris Hauser. Dense robotic packing of irregu-
     lar and novel 3d objects. IEEE Transactions on Robotics, 38
     (2):1160–1173, 2021. 3
[40] Lei Wang, Songshan Guo, Shi Chen, Wenbin Zhu, and An-
     drew Lim. Two natural heuristics for 3d packing with practi-
     cal loading constraints. In PRICAI 2010: Trends in Artificial
     Intelligence: 11th Pacific Rim International Conference on
     Artificial Intelligence, Daegu, Korea, August 30–September
     2, 2010. Proceedings 11, pages 256–267. Springer, 2010. 3
[41] Peng-Shuai Wang, Yang Liu, and Xin Tong. Dual octree
     graph networks for learning adaptive volumetric shape rep-
     resentations. ACM Transactions on Graphics (SIGGRAPH),
     41(4), 2022. 5
[42] Kang Wu, Xiao-Ming Fu, Renjie Chen, and Ligang Liu.
     Survey on computational 3d visual optical art design. Vi-
     sual Computing for Industry, Biomedicine, and Art, 5(1):31,
     2022. 4
[43] Hiroyuki Yamazaki, Keishi Sakanushi, Shigetoshi Nakatake,
     and Yoji Kajitani. The 3d-packing by meta data structure and
     packing heuristics. IEICE transactions on fundamentals of
     electronics, communications and computer sciences, 83(4):
     639–645, 2000. 2, 3
[44] Zifei Yang, Shuo Yang, Shuai Song, Wei Zhang, Ran Song,
     Jiyu Cheng, and Yibin Li. Packerbot: Variable-sized product
     packing with heuristic deep reinforcement learning. In 2021
     IEEE/RSJ International Conference on Intelligent Robots
     and Systems (IROS), pages 5002–5008. IEEE, 2021. 2
[45] Miaojun Yao, Zhili Chen, Linjie Luo, Rui Wang, and
     Huamin Wang. Level-set-based partitioning and packing
     optimization of a printable model. ACM Transactions on
     Graphics (TOG), 34(6):1–11, 2015. 3, 5
