                                                                  Scalable Metropolis Monte Carlo for simulation of hard shapes

                                                                                  Joshua A. Andersona , M. Eric Irrgangb , Sharon C. Glotzera,b,∗
                                                              a Department of Chemical Engineering, University of Michigan, 2800 Plymouth Rd. Ann Arbor, MI 48109, USA
                                                         b Department of Materials Science and Engineering, University of Michigan, 2300 Hayward St. Ann Arbor, MI 48109,USA




                                                 Abstract
                                                    We design and implement HPMC, a scalable hard particle Monte Carlo simulation toolkit, and release it open source
                                                 as part of HOOMD-blue. HPMC runs in parallel on many CPUs and many GPUs using domain decomposition. We
arXiv:1509.04692v1 [cond-mat.soft] 15 Sep 2015




                                                 employ BVH trees instead of cell lists on the CPU for fast performance, especially with large particle size disparity, and
                                                 optimize inner loops with SIMD vector intrinsics on the CPU. Our GPU kernel proposes many trial moves in parallel on
                                                 a checkerboard and uses a block-level queue to redistribute work among threads and avoid divergence. HPMC supports
                                                 a wide variety of shape classes, including spheres / disks, unions of spheres, convex polygons, convex spheropolygons,
                                                 concave polygons, ellipsoids / ellipses, convex polyhedra, convex spheropolyhedra, spheres cut by planes, and concave
                                                 polyhedra. NVT and NPT ensembles can be run in 2D or 3D triclinic boxes. Additional integration schemes permit
                                                 Frenkel-Ladd free energy computations and implicit depletant simulations. In a benchmark system of a fluid of 4096
                                                 pentagons, HPMC performs 10 million sweeps in 10 minutes on 96 CPU cores on XSEDE Comet. The same simulation
                                                 would take 7.6 hours in serial. HPMC also scales to large system sizes, and the same benchmark with 16.8 million
                                                 particles runs in 1.4 hours on 2048 GPUs on OLCF Titan.
                                                 Keywords: Monte Carlo, hard particle, GPU
                                                 PACS: 02.70.Tt
                                                 PACS: 82.60.Qr


                                                 1. Introduction                                               most straightforward way to evolve the Markov chain, but
                                                                                                               it can achieve only a small fraction of the performance
                                                     CPU performance hit a performance brick wall in 2005 [1], available in a single compute node and does not scale
                                                 and serial execution performance has remained stagnant        to simulations with large numbers of particles. Efficient
                                                 since then. Whole socket CPU performance continues to         sampling algorithms can achieve orders of magnitude bet-
                                                 increase due to additional CPU cores and wider single in-     ter performance than Metropolis MC, such as the event
                                                 struction multiple data (SIMD) vector instruction widths.     chain algorithm for hard spheres [3] and general pair po-
                                                 Moore’s Law drives the increase in core counts, with 2-core   tentials [4]. However, it is not clear how event chain MC
                                                 CPUs available in 2005 increasing to 18-core CPUs in 2015.    can be extended to hard particles with shape, which is our
                                                 XSEDE [2] Comet is a modern commodity dual-socket             primary interest.
                                                 CPU cluster with 24 cores per node (12 cores per CPU).            Computational scientists need general purpose simula-
                                                 This is a typical configuration for current systems; future   tion tools that utilize parallel CPUs and GPUs effectively.
                                                 clusters will have more cores per node. However, CPUs         They need to run simulations of a few thousand particles
                                                 are not very power efficient. Graphics processing units       as fast as possible in order to answer research questions
                                                 (GPUs) have thousands of cores and can process hundreds       quickly, conduct high throughput screening studies, and
                                                 of thousands of concurrent lightweight threads. Given a       sample more states with a short turnaround time. Re-
                                                 fixed power budget, systems that use GPUs provide signif-     searchers also need scalable codes to complete large simu-
                                                 icantly higher performance than those with CPUs alone.        lations with millions of particles, which is intenable with
                                                 For example, the GPUs on OLCF Titan provide over 90%          a serial code. There are a number of possible routes to
                                                 of its performance. When Jaguar was upgraded to Titan         parallelizing Metropolis MC [5]: 1) execute many inde-
                                                 by adding GPUs, its total peak performance increased by       pendent runs in parallel to improve sampling, 2) evaluate
                                                 10x with only a 20% increase in power usage.                  energies in parallel for trial moves that are proposed in se-
                                                     Metropolis Monte Carlo (MC) simulations for off-lattice   rial, and 3) propose multiple trial moves in parallel. Exe-
                                                 particles are usually implemented in serial. This is the      cuting many independent serial runs is not helpful for large
                                                                                                               systems or those with long equilibration times. Two recent
                                                    ∗ Corresponding author                                     open source codes fall into the second category. CASSAN-
                                                      Email address: sglotzer@umich.edu (Sharon C. Glotzer)    DRA [6] uses OpenMP to run in parallel on the CPU and

                                                 Preprint submitted to Elsevier                                                                                  September 16, 2015
GOMC [7] uses CUDA to parallelize on NVIDIA GPUs.              import h o o m d s c r i p t a s hoomd
Both of these tools model atomistic systems with classical     from hoomd plugins import hpmc
potentials.
    A number of works use checkerboard techniques to pro-      # Read t h e i n i t i a l c o n d i t i o n .
pose trial moves in parallel in off-lattice systems with short hoomd . i n i t . r e a d x m l ( f i l e n a m e= ’ i n i t . xml ’ )
ranged interactions [8, 9, 10, 11, 12]. Heffelfinger intro-
duced the concept [8], but found it inefficient due to high    # MC i n t e g r a t i o n o f s q u a r e s
communication overhead. Ren [10] and O’Keeffe [11] im-         mc=hpmc . i n t e g r a t e . c o n v e x p o l y g o n ( s e e d =10 ,
proved efficiency with sequential moves in the domains.                                                        d =0.25 , a =0.3)
Sequential moves obey balance in serial implementations [13], s q u a r e =[( −0.5 , −0.5) , ( 0 . 5 , −0.5) ,
but the same argument does not apply to checkerboard                         ( 0 . 5 , 0 . 5 ) , ( −0.5 , 0 . 5 ) ] )
parallel moves. We showed in Ref. [12] that sequential         mc . shape param . s e t ( ’A ’ , v e r t i c e s=s q u a r e )
moves within active checkerboard domains lead to incor-
rect results, as does allowing particle displacements to       # Run t h e s i m u l a t i o n
cross from an active domain to an inactive one as al-          hoomd . run ( 1 0 e3 )
lowed in refs [8, 10, 11]. Uhlherr [9] implemented a two
color asymmetric striped decomposition, proposes com-
plex polymer conformation moves within the domains, and        Figure 1: Example HPMC job script. The syntax is pre-
correctly rejected moves that cross boundaries. Kamp-          liminary and may change as we reorganize components for
mann [14] combined event chain MC with the parallel            a final release.
checkerboard scheme in a rejection free manner by reflect-
ing trial moves off the domain walls.
                                                                   Python job scripts control HOOMD-blue execution.
    Previously, we developed a general algorithm for mas-
                                                               Users can activate HPMC integration with a few lines,
sively parallel Metropolis Monte Carlo, implemented it for
                                                               and can switch back and forth between MC and MD in
two-dimensional hard disks on the GPU [12], and used
                                                               the same job script. Figure 1 shows a job script that runs
it to confirm the existence of the hexatic phase in hard
                                                               a simulation of hard squares for ten thousand steps. A
disks [15]. In this paper, we present a general purpose code
                                                               single “step” in HPMC is approximately ns sweeps, the
for MC simulations of hard shapes, HPMC. HPMC runs
                                                               approximation is due to the parallel domain decomposi-
NVT and NPT [16, 17] ensembles in 2D or 3D triclinic
                                                               tion. One sweep is defined as N trial moves, where N is
boxes. Additional integration schemes permit Frenkel-
                                                               the number of particles in the simulation box.
Ladd [16] free energy computations and implicit depletant
simulations [18]. It calculates pressure in NVT simulations
                                                               2.1. Metropolis Monte Carlo
by volume perturbation techniques [19, 17]. HPMC sup-
ports a wide variety of shape classes, including spheres /         Hard particle simulations have infinite potential energy
disks, unions of spheres, convex polygons, convex spheropoly-  when   any particles overlap and zero potential energy oth-
gons, concave polygons, ellipsoids / ellipses, convex poly-    erwise.   Metropolis Monte Carlo [25, 16] for hard particles
hedra, convex spheropolyhedra, spheres cut by planes, and      with  shape    consists of the following steps. Let ~ri and qi
concave polyhedra. It runs efficiently in serial, on many      be  the  position  and orientation of particle i.
CPU cores, on a single GPU, and on multiple GPUs. Re-             1. Select a particle i at random.
searchers have already used HPMC in studies of shape              2. Generate a small random trial move for that particle,
allophiles [20] and ellipsoids with depletants [21].                  resulting in a new trial configuration ~rtrial = ~ri + δ~r,
                                                                      qtrial = qi · δq.
2. Implementation                                                 3. Check for overlaps between the trial configuration
                                                                      and all other particles in the system.
    HPMC is an extension of HOOMD-blue [22, 23, 24] us-           4. Reject the trial move if there are overlaps, otherwise
ing the existing file formats, data structures, scripting en-         accept the move and set ~ri ← ~rtrial , ~qi ← ~qtrial .
gine, and communication algorithms. HOOMD-blue started
off as a molecular dynamics (MD) package, but its design           The last step is a simplification of the more general
is general enough to allow the addition of Monte Carlo         Metropolis    acceptance criterion [25] for hard particle sys-
moves with minimal modifications. HPMC is an Integra-          tems. It offers an important opportunity for optimization:
tor class inside HOOMD-blue that applies MC trial moves        Once the first overlap is found, no further checks need to
to the particles. The code is object-oriented and exten-       be made.
sible, and it is easy to add additional shape classes and          For new simulations, we follow a general rule of thumb
collective moves. Adding new types of local moves is not       and select the size of δ~r and δq so that an (estimated)
as easy, but can be accomplished by subclassing the inte-      optimal percentage of the trial moves are accepted. A
grator and re-implementing the main loop.                      simple way to measure efficiency for fluids is the diffusion
                                                               rate in wall clock time units. We check with this metric for
                                                                  2
several benchmark cases, and trial move sizes associated
with a 20% acceptance ratio are at or very close to peak                                    0
efficiency for the high density fluids we are interested in.
The rule of thumb is not always optimal, but it is useful                           1                   6
as researchers can trivially implement it. All benchmark
results reported in this work are initially tuned to 20%
acceptance, then the trial move size is fixed.                              2           5       7           10


2.2. Acceleration structures                                            3       4           8       9
    A naı̈ve implementation of hard particle MC would
check N − 1 particles for possible overlaps with each trial
configuration. The cost of a single sweep would be pro-
hibitively slow: O(N 2 ). Acceleration structures are data              Figure 2: A binary tree of axis aligned bounding boxes
structures that reduce the execution time by efficiently                (AABBs). Each node stores an AABB that contains all of
identifying a subset of the N particles that possibly over-             its children. Leaf nodes contain particles (2 each in this
lap with the trial configuration. Cell lists place particles            example). The tree adapts to density fluctuations and
in cells and have constant lookup time to find possible                 variable particle sizes. Nodes are stored in a simple array
overlaps: O(N ) sweep execution time. Bounding volume                   in memory, in the same order as a pre-order traversal.
hierarchies (BVH) build a binary tree of nodes that contain             Numbers in the boxes indicate the index of the node in
particles and have logarithmic lookup time: O(N log(N ))                the array. Bounding volumes are visualized on the right.
sweep execution time. HPMC uses cell lists on the GPU
and BVHs on the CPU.
    Cell lists are applicable on the CPU as well, but we                2.2.2. Bounding volume hierarchy
were able to optimize the BVH code to be faster in all test                  A bounding volume hierarchy (BVH) is a tree where
cases. The log(N ) factor is always small as the number                 each node represents the volume that bounds the particles
of particles per rank is never very large in domain decom-              inside it, as shown in Figure 2. The root node encom-
position parallel runs. HOOMD-blue can compute BVHs                     passes all N particles, its children each encompass disjoint
on the GPU and use them for MD simulations as well, the                 subsets of the particles, and so on recursively down to
focus of another publication [26]. In this work, we do not              the leaf nodes which contain particles but have no chil-
attempt to use BVHs on the GPU as they are most use-                    dren. We implement binary trees of axis-aligned bound-
ful in simulations with large particle size disparity where             ing boxes (AABB) as they have a good performance to
there is inherently very little parallelism for the GPU im-             efficiency trade-off. AABB trees are commonly used in
plementation to utilize.                                                raytracing [27, 28, 29, 30] and game physics engines. Ev-
                                                                        ery node in the BVH adapts to the size of the particles
2.2.1. Cell list                                                        it contains, unlike the cell list where every cell is sized by
    Let di be the diameter of the sphere that encloses par-             the largest particle in the entire system. This makes BVH
ticle i, centered on the position of the particle ~ri . Let             trees efficient even for large size ratios.
dmax = max({di }) be the largest diameter in the system.                     The cost to find particles that may overlap with with
A cell list [16] data structure splits the simulation box into          a trial configuration is O(log(N )). First, compute the
an n by m by k grid such that the shortest dimension of                 AABB of the trial configuration, Btrial centered on ~rtrial
a grid cell is greater than or equal to dmax . Each grid cell           and encompassing the circumsphere of the shape. Start
lists the particle indices that are inside that cell. A bucket          searching at the root node of the tree. At each node, check
sort efficiently assigns particles to cells, and a massively            the left and right children to see if their AABB overlaps
parallel bucket sort on the GPU is trivial to implement                 with Btrial . If a child does not overlap, skip it and all of
with atomic operations. With this data structure, the cost              its children. If it does overlap, recurse down and check its
to find possible overlapping particles is O(1). Given the               children. If this is a leaf node, check the trial configuration
position of a trial configuration ~rtrial , only its cell and the       for overlaps against all particles in the leaf. When a trial
neighboring cells ±1 in each direction need to be searched              move is accepted, update the tree so that future moves
(9 in 2D, 27 in 3D). HOOMD-blue already contains code                   will not miss possible overlaps. We update the tree with-
to generate cell lists for MD simulations.                              out changing its topology by expanding the AABB of the
    Cell lists perform well, provided that particle diameters           leaf and all of its parent nodes recursively in O(log(N ))
di are comparable and there are only a few particles per                steps.
cell. Efficiency drops precipitously with disparate particle                 The main simulation loop performs trial moves, and
sizes. The cell size is set by the largest diameter, so the             the next innermost loop finds possible overlaps. Recursive
smaller particles are able to fill in gaps leading to hundreds          function calls have high overhead, and an explicit stack is
of particles per cell. At large enough diameter ratios this             almost as expensive. Neither performs well in the inner
degrades to O(N 2 ) sweep time.                                         loop. We use a stack-free iterative scheme to perform the

                                                                    3
search, and implement AABB overlap tests using stream-                cumsphere, the particle can rotate without changing its
ing SIMD extensions (SSE) vector intrinsics. We store the             AABB and this reduces the time needed to update the
nodes in an array in pre-order and include an additional              tree on an accepted trial move at the cost of a slightly
skip count for each node. With this structure, the recur-             lower quality tree.
sive algorithm becomes a simple for loop iteration over
nodes in memory order [29]. When a node and all of its                2.3. Overlap checks
children need to be skipped, add the pre-computed skip                    HPMC supports many different classes of shapes. It
value to the loop index. Iterating over nodes in memory               calls the shape overlap check from the innermost loop and
order is cache-friendly on the CPU and gives good perfor-             executes it billions of times per second in a typical simu-
mance even with large N .                                             lation run, so heavily optimized shape overlap checks are
    Unlike cell lists, AABB trees do not directly encode              needed for good overall performance. We write each shape
periodic boundary information. When a particle is near                overlap check ourselves and do not use existing libraries
a boundary, or in a small simulation box where particles              that would require costly data conversions and function
may interact with themselves, HPMC translates each trial              call overhead at every check, and which lack GPU support.
configuration ~rtrial by all necessary periodic images and            There is a single MC integration loop that is templated on
checks each image against the tree separately. Most of                the shape class to enable the best performance and to make
these checks terminate the search at the root node, so                code maintenance easy. Only that single class needs to be
there is little performance penalty. There are no periodic            modified when fixing bugs or adding additional features to
boundaries in a single domain of a fully decomposed par-              the main loop. By template instantiation, the compiler is
allel simulation, so only one tree search is needed in the            able to inline every overlap check call, we can arrange the
most common use-case.                                                 data in the best format for the computation, and we can
    Particles migrate to and from domains, and it would               choose the best overlap detection algorithm for each shape
be impossible to maintain a balanced tree with constant               class. Users only need to write an overlap check to add a
additions and removals. So at the start of each step, we de-          new shape class.
stroy the old AABB tree and build a new one from scratch.                 There are a number of methods to determine if two
There are many tree build algorithms, including top-down              shapes overlap. Some methods are specific for a single
and bottom up approaches. There are different heuristics              class of shapes, while other are more general. When there
for determining node splits [28], and methods to optimize             are multiple algorithms to choose from, we test them and
trees after they are built [30]. Low quality trees are fast           select the one with the best performance. For spheres and
to build but take longer to traverse in the search phase.             disks, overlap detection is trivial. For unions of spheres, all
High quality trees cost more execution time to construct,             spheres in one shape are exhaustively checked against all
but are faster to traverse.                                           those in the other. We use the separating planes method [31]
    We choose the median cut algorithm [27] as it is sim-             for convex polygons on the CPU, but XenoCollide [32]
ple to implement and offers good tree quality and very fast           is faster on the GPU. XenoCollide is a general algorithm
build times. It proceeds as follows: For each particle, con-          that can detect overlaps between any two convex shapes.
struct the AABB that bounds the particle’s circumsphere.              HPMC uses XenoCollide for convex polygons, spheropoly-
Partition that list recursively. At each level of recursion,          gons, convex polyhedra, convex spheropolyhedra, and spheres
merge the current sublist of AABBs into one large AABB.               cut by planes. To detect overlaps between two concave
Split that AABB at the median of its longest axis. Parti-             polygons, HPMC checks all pairs of edges and all vertices.
tion the particles in the sublist so that particle centers less       If no edges intersect and no vertex from one shape is in-
than or equal to the split are on the left side of the array          side the other, then the shapes do not overlap. We use a
and particle centers greater than the split are on the right.         matrix method [33, 34, 21] to detect overlaps of ellipsoids
Terminate recursion and generate a leaf node when the                 and ellipses.
number of particles in the sublist is less than or equal to               It would be expensive in both memory and compute
the maximum node capacity (we use 12, which we found                  to keep all particle geometry (e.g. polyhedron vertices)
empirically). If recursion is not terminated, generate a              in world coordinates. HPMC efficiently represents each
new internal node with the merged AABB and place it at                particle with a position ~ri and an orientation quaternion qi .
the end of the array. This build algorithm puts the nodes             Together, these describe how to rotate and then translate
in pre-order to be searched with the stack-free iterative             from the frame of the particle to the world frame. The user
scheme.                                                               specifies the shape geometry in particle local coordinates
    The entire recursion partitions a single array of AABBs           once for each type of particle.
and requires no memory allocations or extra copies of data.               When performing an overlap check between particles A
A naı̈ve implementation with memory allocations and data              and B, HPMC works in a local coordinate system centered
copies takes many times longer to execute. Tighter AABBs              on particle A. The application of this local coordinate
are possible for shaped particles, but are much more ex-              system optimization depends on the shape overlap check
pensive to compute as they need to be updated every time              algorithm. For example, a support function is evaluated
the particle rotates. With an AABB that bounds the cir-
                                                                  4
at every iteration of XenoCollide. The support function
for the Minkowski difference B − A is

           Sworld
            B−A (~n) = Sworld
                        B     (~n) − Sworld
                                      A     (−~n) .       (1)
            world       world
Replacing SA      and SB      with operations on the par-
ticle support functions in their local coordinate systems
gives [32]

   SB−A (~n) = RSB (R−1~n) + (~rB − ~rA ) − SA (−~n)      (2)

where R is the rotation matrix that takes B into the co-
ordinate system of A. SB−A is in the coordinate system
of particle A, but this is irrelevant for the overlap calcula-
tion. On the GPU, we replace R with an operation that
                                            ∗
rotates vectors by the quaternion q = qA      qB because it is
faster. The quaternion rotation uses more floating point
operations, but requires fewer registers.                            Figure 3: Domain decomposition scheme. The outer box
    Single precision particle coordinates are not accurate in        is the triclinic simulation box, which is split into 4 do-
large simulation boxes (without cell-local coordinate sys-           mains. On the right and bottom edge of each domain is a
tems [12]), so in HPMC we use double precision particle              gray inactive area, one particle diameter wide. Particles in
coordinates. In mixed precision mode, we compute the dis-            the inactive region are colored lighter and are not selected
placement between particles ~rAB = min image(~rB −~rA ) in           for trial moves. Any trial configuration that ends in the
double precision, then we cast ~rAB to single precision and          inactive region must be rejected (top left domain in this
compute the overlap check in single precision. Within the            example). On the GPU, individual domains are further
local coordinate system of particle A, single precision is ac-       subdivided with a checkerboard grid.
curate for self-assembly simulations, though densest pack-
ing calculations may require full double precision. HPMC
supports both full double precision and mixed precision              part of a production simulation run. We used oprofile
modes as a compile time option. Full single precision                to run a line level execution profile of a typical polyhe-
builds do not even pass simple validation tests.                     dra simulation in the final version of the code. About 40
    All benchmark and validation studies in this work use            percent of the runtime is spent in the vectorized support
mixed precision.                                                     function, 10 percent in XenoCollide iteration logic, 40 per-
                                                                     cent in AABB tree searches and the remaining 10 percent
2.4. SIMD vectorization                                              in trial moves and AABB tree generation.
     The polygon, spheropolygon, polyhedron, and spheropoly-
hedron overlap checks evaluate the support function many     2.5. Parallelization
times in the innermost loop of XenoCollide. The support          Even with fast BVH trees and SIMD vector optimiza-
function loops over all vertices in the shape, dots them     tions, a serial CPU simulation still only uses a fraction of
with ~n, and returns the vertex that gives the maximum       the capabilities of a single compute node. We implement
dot product. In our initial implementation, this code used   parallel computations that utilize the full capabilities of
over 80% of the CPU time (determined by line level pro-      multi-core CPUs and clusters of CPU nodes to provide
filing with oprofile). We improve performance of this        faster time to solution and to enable larger scale simula-
loop with SIMD vector instruction intrinsics. The first      tions across many nodes. In hard particle MC, there are
loop computes the dot products for all vertices, w vertices  typically only a few dozen possible overlaps with each trial
per iteration with SIMD parallelism, and just stores the     configuration. This is not large enough to parallelize over
result to avoid branch mispredication penalties around the   a whole node and cannot scale to large simulations. The
floating point operations. A second w width SIMD loop        only path to achieving fast, scalable simulations for MC
starts and each iteration uses masks and the BSF assem-      with short range particle interactions is to perform many
bly instruction to find the index of the maximum element.    trial moves in parallel [5].
We implement these loops in SSE (w = 4) and AVX (ad-             To do this, we need to be able to efficiently generate
vanced vector extensions) (w = 8). SIMD vectorization        many parallel random number streams. As we have be-
boosts performance of the support function evaluation by     fore [35, 12], we use a hash based RNG, Saru [36]. Each
a factor of 2-3 over a serial implementation with manually   time a trial move is generated, we hash together the parti-
unrolled loops, achieving near peak floating point through-  cle index, time step, user seed, and MPI rank to initialize
put in a microbenchmark. While the vectorized support        an independent RNG stream. We then use that stream to
function now executes several times faster, it is only one

                                                                 5
generate as many random numbers as needed for the trial                   4. Generate a small random trial move for particle i,
move.                                                                        resulting in a new trial configuration ~rtrial = ~ri + δ~r,
                                                                             qtrial = qi · δq. Reject the trial move if ~rtrial is in an
2.5.1. Domain decomposition                                                  inactive region.
     To scale beyond a single compute node, we employ a                   5. Check for overlaps between the trial configuration
domain decomposition strategy using MPI with one rank                        and all other particles in the system, using the AABB
per CPU core, or one rank per GPU. We implement HPMC                         tree.
as an extension of HOOMD-blue, a parallel MD code that                    6. Reject the trial move if there are overlaps, otherwise
already has the necessary decomposition and communi-                         accept the move and set ~ri ← ~rtrial , ~qi ← ~qtrial . Also,
cations routines [23]. Each rank covers a portion of the                     update the AABB tree with the new position of par-
simulation box and owns all of the particles in that re-                     ticle i which may or may not require expanding its
gion. The communications routines copy particle data                         leaf node and all parents up to the root.
from neighboring ranks in a ghost layer around each do-                   7. Repeat stages 2–6 ns times.
main, and migrate particles from one domain to another
                                                                          8. Choose a random displacement vector and translate
as they move.
                                                                             all particles by this vector.
     We base HPMC domain decomposition on our previous
method for massive parallelism [12]. However, we do not                   9. Migrate particles to new domains and communicate
use a 2d color checkerboard grid to scale across domains.                    ghost particles.
Updating only 21d of the system at a time is unnecessary                    Stages 1–9 implement one step, and typical MC sim-
with low thread counts, and would require ghost commu-                  ulation runs continue for tens of millions of steps. The
nication after every fractional system update. Instead, we              amount of useful work done by a step is proportional to
modify the checkerboard scheme to have only two regions                 the number of trial moves attempted and simulation effort
(active and inactive) and make the active region as large               is usually measured in sweeps (N trial moves). When run-
as possible, see Figure 3. The inactive region has width                ning on a single rank, one step executes ns sweeps. The
dmax , and it is placed along the bottom, right, and back               ratio of active to inactive particles decreases as the num-
faces of each domain.                                                   ber of parallel domains increases, so the number of sweeps
     In this layout, all inactive particles are in the neighbor-        in a step varies depending on the run configuration. Users
ing domain’s ghost layer, or separated from the neighbor-               need to be aware of this behavior so that they can config-
ing domain’s active particles by an inactive region. There              ure their run protocols properly.
is no need to communicate ghost layer updates because
these particles do not move during substeps. Communi-                   2.5.2. GPU kernel
cation between ranks only occurs at the end of the step,                    For multi-GPU simulations, we use the same domain
when we apply a single random displacement to all par-                  decomposition strategy as on the CPU but assign each ac-
ticles and call the migration routine. The user sets ns ,               tive domain to a single GPU. On the GPU, we run a kernel
the number of substeps to perform per step, giving them                 that implements the checkerboard update scheme, similar
control of the computation to communication ratio.                      to the one we previously implemented [12] but with a few
     In our previous work [12], we showed that shuffling the            differences. In HPMC, user configuration choices can lead
order of particles selected for trial moves achieves detailed           to hundreds of particles in a cell, so we keep particle posi-
balance within the checkerboard scheme. We proposed                     tions in global memory and each kernel call only proposes
full shuffling of all 0–4 particle indices within a cell, as for-       one trial move per cell. For disk simulations, this is slower
ward and reverse permutations occur with equal probabil-                than our specialized implementation [12], but it is not a
ity. Full shuffling causes cache thrashing in a general CPU             bottleneck for complex shaped particles where the over-
domain decomposition implementation, where individual                   lap check costs dominate and accessing global memory is
domains might have thousands of particles. In HPMC,                     almost free in comparison.
we choose randomly to loop through particles either in                      To assign threads to cells, we pre-compute arrays that
forward or reverse index order. Both orders are cache                   list the active cells for each color of the checkerboard.
friendly, and this selection preserves the essential element            Then we launch 1D indexed kernels that read their cell
required for detailed balance: that forward and reverse                 from this array so that a single kernel may work for all
sequences occur with equal probability. With this slight                use-cases. Most research relevant simulations are dense
modification, this scheme obeys detailed balance following              enough that the fraction of empty cells is small, though
the same arguments as in ref. [12].                                     these could be removed from the list with an additional
     Putting all of these elements together, HPMC with do-              overhead per step. This structure makes one trial move
main decomposition on the CPU has the following stages.                 for each cell that has a non-zero number of particles in it.
    1. Generate the AABB tree.                                          To approach parity between a step on the GPU and a step
    2. Choose forward or reverse index order randomly.                  on the CPU, HPMC uses particle density and the number
    3. Loop through all particles i in the chosen order, skip-          of cells to estimate how many times to run the kernel so
       ping those where ~ri is in an inactive region.                   that one GPU step is approximately ns sweeps.
                                                                    6
        (a)

                                                                                                   Initialization
                                                                                                   Trial move
                                                                                                   Circumsphere check
                                                                                                   Overlap check
                                                                                                   Overlap divergence
                                                                                                   Early exit divergence
        Thread




                                                                                              Time (0.5 ms total)
        (b)

Figure 4: Traces of warp execution from a benchmark run of truncated octahedra. Timing data is captured with the
clock64() function for just a single warp on the device. Colors indicate time spent in different parts of the execution.
Panel (a) shows the register queue implementation and (b) shows the block queue. In panel (b), the later trial move and
early exit condition rectangles indicate synchronization with other warps in the block.


2.5.3. Block queues                                                  must be rejected. The remaining 20 percent must check all
     For complex shaped particles, such as polyhedra with            potential overlaps before accepting the move. The critical
many vertices, overlap checks take a majority of the ker-            path for the entire warp to complete is determined by only
nel run time. They are compute limited, so GPUs have                 20% of the threads so divergence is still a problem.
the potential to execute these checks with very high per-                We attempt to use a global queue to work around this.
formance, but divergence is a problem. Current GPUs                  The first kernel generates trial moves, performs circum-
execute warps of 32 threads in lockstep. Threads within a            sphere checks, and inserts the needed full overlap checks
warp can take different branches, but all threads in a warp          into a global queue. Then a second kernel processes the
execute the instructions on both sides of the branch and             queue and runs all of the overlap checks with no diver-
inactive threads are masked out. A direct translation of             gence due to circumsphere checks or early exit conditions.
the MPMC checkerboard algorithm [12] loops over parti-               A third kernel applies the accepted moves. Overall, this
cles in nearby cells, checks for circumspheres that overlap          method performs no better than the register queue kernel.
with the trial configuration, and calls the full overlap check       It was able to compute many more overlap checks per sec-
if the circumspheres overlap. In a typical simulation, there         ond, but it also had to perform many more overlap checks
might be 100 particles in the cells around the location of a         because it is not able to take advantage of the early exit
trial configuration, but only five of those pass the circum-         condition.
sphere test. With such low hit probabilities, that branch                Our fastest, and final, implementation uses the idea of
is likely to diverge every time, leading to a large reduction        a work queue for the expensive overlap checks, but does
in performance.                                                      so at a block level rather than at the global level. One or
     We improve on this by changing the structure of the             more threads in a group run for each cell in the active set.
loop to make a register queue. Threads loop over poten-              They generate the trial move and then loop through the
tial neighbors, only checking the circumsphere overlap in-           particles in the nearby cells in a strided fashion. For exam-
side the loop. When a thread finds a potential overlap, it           ple, with a group size of 4, thread 0 checks nearby particles
breaks out of the loop. Then the full overlap check is per-          0, 4, 8, . . . and thread 1 checks 1, 5, 9, . . . . In this phase,
formed outside the loop after the threads have converged.            threads only check for circumsphere overlaps. When a
This modification causes the overlap checks to run as con-           particle passes the circumsphere test, the thread adds the
verged as possible. Figure 4(a) shows a trace from a warp            particle index and group id to a queue in shared memory.
using the register queue. The next problem is immediately            The maximum queue size is the number of threads in the
obvious in this figure: 80 percent of the threads end early          block. Once the queue is full, the loop over nearby parti-
when they find their first overlap and know that the move            cles exits and all threads in the block enter the next phase.

                                                                 7
Here, each thread performs the overlap check in the queue           benefits greatly from the BVH tree, though the size ratio is
entry matching its thread index, which may be for a trial           not large enough to demonstrate the full capabilities of the
move generated by a different thread. If the particles over-        tree to efficiently simulate huge size disparities. We leave
lap, the thread atomically increments an overlap counter            those benchmarks for other papers on methods to model
for the appropriate group. Then the first phase starts pop-         systems with large colliods and small depletants [18] and
ulating the queue again, except that threads with already           MD methods using BVH trees [26].
discovered overlaps do not add any work to the queue.                   For all three benchmarks, we explore strong scaling
These two phases repeat until there are no more nearby              performance in two regimes. The first case is N = 4096,
particles to check for any thread in the block, then ac-            a system size representative of what researchers have used
cepted trial moves are handled.                                     in previous studies with serial MC implementations. Such
    Figure 4(b) shows a trace from a warp using the block           systems are too small to run efficiently on the GPU, but
queue. The overlap check phase of the kernel runtime is             parallel CPU simulations offer tremendous speedups over
kept dense and non-divergent until the last pass of the non-        serial ones. We run this case on XSEDE Comet, a recent
full queue. There is still divergence within the iterative          addition to the XSEDE ecosystem. Comet has dual-socket
XenoCollide overlap checks themselves. We implemented               nodes with Intel Xeon E5-2680v3 CPUs — a total of 24
XenoCollide as a single loop to avoid divergence as much            cores per node. Figure 5(a–b) shows the performance of
as possible, but some particle configurations require more          the three benchmarks at N = 4096 on Comet. Both the
iterations than others. We tried a variety of ways to re-           pentagon and dodecahedron benchmarks scale out to 96
move overlap checks that exit in the first iteration from the       CPU cores, only 43 particles per domain. At this point, it
queue, but adding that cost on top of every circumsphere            takes 10 minutes to run 10 million sweeps in the pentagon
check slowed performance overall.                                   benchmark, and 45 minutes in the dodecahedron bench-
    With the block queue implementation, any number of              mark. Contrast that with serial simulations that would
threads can be run per active cell so long as the total             take 7.6 and 21.8 hours, respectively. Due to the size dis-
block size is a multiple of the warp size. This allows many         parity, the binary benchmark does not decompose over
threads to execute per cell, which is critical to obtain high       24 cores. Past that point, the inactive region covers the
performance on modern GPUs. HOOMD-blue autotunes                    whole domain. Still, we reduce a serial runtime of 32.9
kernel launch parameters to find the fastest performing             hours down to 2.45 to complete 10 million sweeps.
values [23]. We autotune over all valid combinations of                 The second regime we benchmark is large systems of
the group size and block size to find the fastest perform-          N = 224 (16.8 million) particles. Running such a large sys-
ing configuration. In cases where there are a large number          tem is inconceivable with a serial simulation code, where
of particles in nearby cells, the autotuner will pick a large       it would take more than a month to complete 10 million
group size (i.e. 8 or 32) to have many threads available to         sweeps and years to equilibrate a system. Large systems
process the overlap checks. In cases where there are only           easily fill the GPU, so we run these benchmarks on OLCF
a few particles in nearby cells, it chooses 1 or 2. We test         Titan, which has 1 NVIDIA Tesla K20X GPU per node.
a variety of benchmark cases and always find the block              Figure 5(c–d) shows the results. The pentagon benchmark
queue outperforms the register queue; performance bene-             scales out to 2048 GPUs (8192 particles/GPU), where it
fits range from 20 to 80 percent.                                   takes 1.4 hours to complete 10 million sweeps. The dodec-
                                                                    ahedron benchmark scales out to 4096 GPUs (4096 par-
3. Performance                                                      ticles/GPU), where it takes 10.36 hours to complete 10
                                                                    million sweeps. As on the CPU, domain size limits the
    We benchmark HPMC performance on a few reference                scaling of the binary benchmark, this time to 1024 GPUs
systems that researchers have previously studied. Our first         (16384 particles/GPU).
benchmark is a system of 2D regular pentagons in a high                 The strong scaling limit is the fastest possible simu-
density fluid at a packing fraction of 0.676 in NVT. This           lation one can achieve, though it uses compute resources
is a single state point in a previous study by Schilling,           inefficiently. Given a fixed compute time budget, one can
Frenkel et al. [37]. Our second benchmark is a system               get more simulations completed with fewer MPI ranks at
of 3D dodecahedra in a high density fluid at a packing              the cost of longer wait times to finish each run. Efficiency
fraction of 0.5 in NVT. This is representative of monodis-          depends primarily on the number of particles per CPU
perse self-assembly simulations of polyhedra [38]. Binary           core (or per GPU). HPMC obtains a reasonable efficiency
systems have a much larger phase space to explore (com-             of 60–70% with 85 particles per CPU core for the pentagon
position, size ratio), so such studies are computationally          benchmark and 170 for the dodecahedron benchmark. The
expensive and can benefit greatly from optimized, paral-            same efficiency is reached at 65536 pentagons/GPU and
lel simulation codes. Khadilkar and Escobedo [39] studied           131072 dodecahedra/GPU, though Titan’s usage policies
a binary mixture of tetrahedra and octahedra with equal             strongly encourage runs much closer to the strong scaling
edge lengths that could tile space (volume ratio 1 : 4). We         limit. These are representative of 2D and 3D simulations
use this system for our third benchmark, in the solid at            of single particle type systems in general, so researchers
a packing fraction of 0.6 in NVT. The binary benchmark              can use these as rules of thumb. For systems with parti-
                                                                8
                 (a) Comet performance (N = 4096)                                      (b) Scaling on Comet

                      Hours to run 10e6 sweeps                          102
             P    Pentagon Dodecahedron Binary
             1          7.56           21.78       32.94
             2          3.58           11.33       17.40
             4          1.91            6.52        9.48




                                                            Speedup
             8          1.06            3.72        5.86                 10
            16          0.55            1.96        3.28
            24          0.39            1.37        2.45
            48          0.23            0.88           -                                        N=4096 - Pentagon
            96          0.17            0.75           -                                        N=4096 - Dodecahedron
                                                                                                N=4096 - Binary
           192          0.19               -           -                                        Ideal scaling
                                                                          1
           384          0.26               -           -
                                                                              1                 10               102
                                                                                             P - CPU cores

                  (c) Titan performance (N=224 )                                        (d) Scaling on Titan

                       Hours to run 10e6 sweeps                         103
             P     Pentagon Dodecahedron Binary
             8        102.03           492.83      901.73
            16         51.25           252.48      482.17
            32         26.04           131.01      294.12
                                                              Speedup




            64         13.82            73.42      173.80               102
           128          7.47            44.61      114.48
           256          4.68            26.32       72.52
           512          2.83            16.64       47.45                                        N=224 - Pentagon
          1024          1.83            17.13       32.42                                        N=224 - Dodecahedron
                                                                                                 N=224 - Binary
          2048          1.42            12.40           -                10                      Ideal scaling
          4096          1.46            10.36           -
                                                                                  10            102               103
                                                                                                P - GPUs

Figure 5: Performance is reported in hours to complete 10e6 sweeps. Scaling plots are performance values renormalized
to performance on the smallest P run. Simulations are run on CPUs on XSEDE Comet (Intel Xeon E5-2680v3) with
N = 4096 and GPUS on OLCF Titan (NVIDIA Tesla K20X) with N = 224 .


cle size disparity, we advise users to run their own short               CPU socket and 38.9 million per GPU socket, for a socket
scaling benchmarks for their systems to determine an ap-                 to socket speedup of 3.1. At reasonable efficiency on the
propriate selection. Efficiency as a function of N/P varies              dodecahedron benchmark, HPMC performs 4.45 million
greatly with size ratio and composition parameters.                      trial moves per second per CPU socket and 8.16 million
    GPU speedup over the CPU is not a focus of this work;                per GPU socket, for a socket to socket speedup of 1.8.
we instead present what types of simulations the CPU and
GPU hardware architectures are well-suited for and how
                                                                         4. Validation testing
well HPMC performs those benchmarks. However, some
readers may still be interested in relative speedup. It is                   We rigorously test HPMC for validity at three levels.
difficult to make a GPU/CPU comparison at scale and it                   At the lowest level, we perform unit tests on the AABB
is not fair to compare several year old K20X GPU to the                  tree, move generation code, and shape classes. We test
brand new Haswell CPUs on Comet. However, these are                      that AABBs are generated properly, and that queries on
the systems currently available to researchers at scale —                the resulting trees find all possible overlapping particles.
Comet has K80s, but limits users to no more than 16 GPUs                 We verify that trial moves are generated from the proper
at a time. One way to compare is to pick points at the                   uniform distribution and that the particle update order is
60–70% efficiency level and compare trial moves per sec-                 correctly randomized. For each shape class, we place many
ond. At reasonable efficiency on the pentagon benchmark,                 test configurations and validate that overlapping and non-
HPMC performs 12.5 million trial moves per second per                    overlapping configurations are correctly detected. This is

                                                                  9
essential to ensure the quality of the overlap check algo-                                                           Truncated
                                                                                   Mode       Disk        Sphere
rithms as there are many corner cases to account for. The                                                            octahedron
shape overlap unit tests contain many configurations cap-                        Serial     9.1707(4)    9.3135(4)   13.8975(17)
tured from simulation runs that we identified were overlap-               24 CPU cores      9.1709(2)    9.3136(2)   13.8972(11)
ping by independent methods. Low level unit tests cover                         1 GPU       9.1708(2)    9.3134(2)   13.8970(7)
14 classes with over 1400 different checks.                                    4 GPUs       9.1710(3)    9.3134(2)   13.8970(6)
    MC integrators cannot be checked with low level unit
tests because their stochastic nature makes it impossible               Table 1: Pressures obtained during NVT validation test
to define what a correct output is given an input. Instead,             runs, in reduced units. In 2D, P ∗ = βP σ 2 , where σ is
we validate the integrators with system level tests which               the diameter of the disk. In 3D, P ∗ = βP v0 , where the
are python job scripts that perform simulation runs. Sys-               reference volume v0 is the single particle volume for the
tem tests verify different operating modes of the integra-              respective shape. The numbers in parentheses are two
tor and ensure that documented interfaces for controlling               standard errors of the mean in the last given digit(s).
those modes work. Additionally, we run short simulations
and check for any overlaps in the generated configurations.
Most bugs in the integrator implementation result in ac-                as 2 standard errors of the mean from the independent
cepted moves that have overlapping particles.                           runs. We perform the set of runs in serial, on 24 CPU
    We run unit and system level tests on every commit                  cores in parallel with domain decomposition, on a single
to the repository with a Jenkins continuous integration                 GPU with checkerboard parallelism, and on 4 GPUs with
server. Jenkins runs these tests on the CPU and on 4                    both checkerboard and domain decomposition. Tests are
different generations of GPU, in both mixed and double                  performed on the XSEDE Comet and University of Michi-
precision, and with and without MPI for a total of 20 build             gan Flux systems.
configurations. It e-mails developers when a commit fails                   To sample the pressure in NVT runs, we build a his-
any of the tests.                                                       togram of scale factors s that cause two neighboring parti-
    Unit and system level tests are designed to run quickly             cles to overlap and extrapolate the probability of overlap at
and automatically to detect bugs in the implementation.                 s = 0. This is a generalization of the g(r) based technique
They are not sufficient to verify that HPMC correctly sam-              we previously used for hard disks [12, 15], see those refer-
ples the ensemble of states available to the system. Such               ences for full details on how to sample and extrapolate the
tests take much longer to run and we do so by hand. We                  histogram without introducing any systematic errors. We
test three separate systems to validate HPMC in NVT:                    use a more general volume perturbation technique [19, 17]
disks, spheres, and truncated octahedra. We run each sys-               to extend this method to particles with shape.
tem in multiple compute configurations, sample the pres-                    Table 1 shows the results of these tests. For each shape,
sure to high precision, and ensure that all simulations pro-            all run configurations give the same pressure within error
duce the same result. For hard disks, we have three inde-               and verify that HPMC performs correct simulations in all
pendent data points to compare to from event chain MC,                  parallel modes. Additionally, HPMC’s hard disk results
event driven MD, and our previous GPU checkerboard im-                  match, within error, the previous pressures obtained with
plementation [15]. No such high precision data exists to                three simulation methods [15], where P ∗ = 9.1707(2) for
validate hard spheres and truncated octahedra, so we in-                this state point.
stead verify that serial and all parallel builds agree. From
our previous work, and from tests that introduce issues in              5. Conclusions
HPMC, we know that this validation technique is sensitive
enough to detect when there are subtle problems - such as                   We presented HPMC, a parallel simulation engine for
looping through particles in sequence instead of randomly               hard particle Monte Carlo simulations we developed as an
choosing the forward or reverse order.                                  extension to HOOMD-blue. HPMC executes in parallel
    Specifically, we run: 65536 hard disks at a packing frac-           on many CPU cores and many GPUs, and we optimized
tion of 0.698 (fluid), 131072 hard spheres at a packing                 HPMC to run as fast as possible on both architectures. On
fraction of 0.60 (solid), and 16000 truncated octahedra at              the CPU, we used efficient bounding volume hierarchies to
a packing fraction of 0.7 (solid). We initialize the hard               search for possible overlaps, and SIMD vector intrinsics in
disks randomly and allow them to equilibrate, while we                  the innermost loop to take full advantage of modern pro-
place the two solid systems on the known self-assembled                 cessors. On the GPU, we performed trial moves in parallel
FCC and BCC lattices. We prepare a number of indepen-                   on a checkerboard with many threads per cell, and imple-
dent equilibrated initial configurations and run as many                mented a block level queue to limit performance degrada-
sampling runs, 30 for disks, and 8 for the other shapes.                tion due to divergence.
We ran each parallel disk simulation for 60 million sweeps                  Our implementation is general and works for any shape,
(only 24 million in serial), spheres for at least 8 million, and        given an implementation of an overlap check. Users can
truncated octahedra for up to 80 million sweeps, all after              easily add new shapes to the code without needing to
suitable equilibration periods. Estimated error is reported             write GPU kernels. HPMC ships with overlap checks for
                                                                   10
many classes of shapes, including spheres / disks, unions              [4] M. Michel, S. C. Kapfer, W. Krauth, Generalized event-chain
of spheres, convex polygons, convex spheropolygons, con-                   Monte Carlo: Constructing rejection-free global-balance al-
                                                                           gorithms from infinitesimal steps, The Journal of Chemical
cave polygons, ellipsoids / ellipses, convex polyhedra, con-               Physics 140 (5) (2014) 054116. doi:10.1063/1.4863991.
vex spheropolyhedra, spheres cut by planes, and concave                [5] G. S. Heffelfinger, Parallel atomistic simulations, Computer
polyhedra.                                                                 Physics Communications 128 (1-2) (2000) 219–237. doi:10.
    Completing 10 million sweeps of a system of 4096 pen-                  1016/S0010-4655(00)00050-3.
                                                                       [6] J. K. Shah, E. J. Maginn, A general and efficient Monte
tagons required 7.6 hours in serial. HPMC achieved the                     Carlo method for sampling intramolecular degrees of freedom of
same in 10 minutes when running in parallel on 96 cores.                   branched and cyclic molecules, The Journal of Chemical Physics
GPUs allow efficient runs with tens of millions of particles.              135 (13) (2011) 134121. doi:10.1063/1.3644939.
On 2048 GPUs, HPMC ran 10 million sweeps of a system                   [7] J. Mick, E. Hailat, V. Russo, K. Rushaidat, L. Schwiebert,
                                                                           J. Potoff, GPU-accelerated Gibbs ensemble Monte Carlo simula-
of 16.8 million pentagons in 1.4 hours.                                    tions of Lennard-Jonesium, Computer Physics Communications
    HPMC is available open-source in HOOMD-blue, start-                    184 (12) (2013) 2662–2669. doi:10.1016/j.cpc.2013.06.020.
ing with version 2.0.                                                  [8] G. S. Heffelfinger, M. E. Lewitt, A comparison between
                                                                           two massively parallel algorithms for Monte Carlo com-
                                                                           puter simulation: An investigation in the grand canoni-
Acknowledgments                                                            cal ensemble, Journal of Computational Chemistry 17 (2)
                                                                           (1996) 250–265. doi:10.1002/(SICI)1096-987X(19960130)17:
                                                                           2<250::AID-JCC11>3.0.CO;2-N.
    HPMC is a group effort. We acknowledge the following               [9] A. Uhlherr, S. J. Leak, N. E. Adam, P. E. Nyberg, M. Doxas-
group members for contributions to various parts of the                    takis, V. G. Mavrantzas, D. N. Theodorou, Large scale atomistic
code, Khalid Ahmed, Michael Engel, Jens Glaser, Eric S.                    polymer simulations using Monte Carlo methods for parallel
Harper, and Benjamin A. Schultz.                                           vector processors, Computer Physics Communications 144 (1)
                                                                           (2002) 1–22. doi:10.1016/S0010-4655(01)00464-7.
    Parts of this work were supported by the DOD/ASD(R&E) [10] R. Ren, G. Orkoulas, Parallel Markov chain Monte Carlo sim-
under Award No. N00244-09-1-0062 (initial design and im-                   ulations, The Journal of Chemical Physics 126 (21) (2007)
plementation) and the National Science Foundation, Divi-                   211102. doi:10.1063/1.2743003.
sion of Materials Research Award # DMR 1409620 (BVH                   [11] C. J. O’Keeffe, G. Orkoulas, Parallel canonical Monte Carlo
                                                                           simulations through sequential updating of particles, The Jour-
tree implementation and GPU kernel optimizations). Soft-                   nal of Chemical Physics 130 (13) (2009) 134109. doi:10.1063/
ware was validated and benchmarked on the Extreme Sci-                     1.3097528.
ence and Engineering Discovery Environment (XSEDE),                   [12] J. A. Anderson, E. Jankowski, T. L. Grubb, M. Engel, S. C.
which is supported by National Science Foundation grant                    Glotzer, Massively parallel Monte Carlo for many-particle sim-
                                                                           ulations on GPUs, Journal of Computational Physics 254 (1)
number ACI-1053575, on resources of the Oak Ridge Lead-                    (2013) 27–38. doi:10.1016/j.jcp.2013.07.023.
ership Computing Facility at the Oak Ridge National Lab-              [13] V. I. Manousiouthakis, M. W. Deem, Strict detailed balance is
oratory, which is supported by the Office of Science of                    unnecessary in Monte Carlo simulation, The Journal of Chem-
                                                                           ical Physics 110 (6) (1999) 2753. doi:10.1063/1.477973.
the U.S. Department of Energy under Contract No. DE-                  [14] T. A. Kampmann, H. Boltz, J. Kierfeld, Parallelized event chain
AC05-00OR22725, and was also supported through com-                        algorithm for dense hard sphere and polymer systems, Journal
putational resources and services provided by Advanced                     of Computational Physics 281 (2015) 864–875. doi:10.1016/j.
Research Computing Technology Services at the Univer-                      jcp.2014.10.059.
                                                                      [15] M. Engel, J. A. Anderson, S. C. Glotzer, M. Isobe, E. P.
sity of Michigan, Ann Arbor.                                               Bernard, W. Krauth, Hard-disk equation of state: First-order
    The Glotzer Group at the University of Michigan is                     liquid-hexatic transition in two dimensions with three simula-
an NVIDA GPU Research Center. Hardware support by                          tion methods, Physical Review E 87 (4) (2013) 042134. doi:
NVIDIA Corp. is gratefully acknowledged.                                   10.1103/PhysRevE.87.042134.
                                                                      [16] D. Frenkel, B. Smit, Understanding molecular simulation from
                                                                           algorithms to applications, 2nd Edition, Academic Press, San
                                                                           Diego, 2002.
6. Bibliography                                                       [17] P. E. Brumby, A. J. Haslam, E. de Miguel, G. Jackson, Sub-
                                                                           tleties in the calculation of the pressure and pressure ten-
References                                                                 sor of anisotropic particles from volume-perturbation methods
                                                                           and the apparent asymmetry of the compressive and expan-
 [1] K. Asanovic, R. Bodik, B. C. Catanzaro, J. J. Gebis, P. Hus-          sive contributions, Molecular Physics 109 (1) (2011) 169–189.
     bands, K. Keutzer, D. A. Patterson, W. L. Plishker, J. Shalf,         doi:10.1080/00268976.2010.530301.
     S. W. Williams, K. A. Yelick, The landscape of parallel com-     [18] J. Glaser, A. Karas, S. Glotzer, Implicit depletion, preprint
     puting research: a view from berkeley, Tech. Rep. UCB/EECS-           V (June) (2015) 1–5.
     2006-183, EECS Department, University of California, Berkeley    [19] R. Eppenga, D. Frenkel, Monte Carlo study of the isotropic
     (Dec. 2006).                                                          and nematic phases of infinitely thin hard platelets, Molec-
 [2] J. Towns, T. Cockerill, M. Dahan, I. Foster, K. Gaither,              ular Physics 52 (6) (1984) 1303–1334.             doi:10.1080/
     A. Grimshaw, V. Hazlewood, S. Lathrop, D. Lifka, G. D. Peter-         00268978400101951.
     son, R. Roskies, J. R. Scott, N. Wilkens-Diehr, XSEDE: Accel-    [20] E. S. Harper, R. Marson, J. A. Anderson, G. van Anders, S. C.
     erating scientific discovery, Computing in Science & Engineering      Glotzer, Shape allophiles improve entropic assembly, Soft Mat-
     16 (5) (2014) 62–74. doi:10.1109/MCSE.2014.80.                        terdoi:10.1039/C5SM01351H.
 [3] E. P. Bernard, W. Krauth, D. B. Wilson, Event-chain Monte        [21] L. C. Hsiao, B. A. Schultz, J. Glaser, M. Engel, M. E. Szakasits,
     Carlo algorithms for hard-sphere systems, Physical Review E           S. C. Glotzer, M. J. Solomon, Metastable orientational order of
     80 (5) (2009) 056704. doi:10.1103/PhysRevE.80.056704.                 colloidal discoids, preprint.
                                                                      [22] J. A. Anderson, C. D. Lorenz, A. Travesset, General purpose


                                                                    11
     molecular dynamics simulations fully implemented on graphics
     processing units, Journal of Computational Physics 227 (10)
     (2008) 5342–5359. doi:10.1016/j.jcp.2008.01.047.
[23] J. Glaser, T. D. Nguyen, J. A. Anderson, P. Lui, F. Spiga, J. A.
     Millan, D. C. Morse, S. C. Glotzer, Strong scaling of general-
     purpose molecular dynamics simulations on GPUs, Computer
     Physics Communications 192 (2015) 97–107. doi:10.1016/j.
     cpc.2015.02.028.
[24] HOOMD-blue, http://codeblue.umich.edu/hoomd-blue (2015).
[25] N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth, A. H.
     Teller, E. Teller, Equation of state calculations by fast comput-
     ing machines, Journal of Chemical Physics 21 (6) (1953) 1087.
     doi:10.1063/1.1699114.
[26] M. P. Howard, J. A. Anderson, A. Nikoubashman, S. C. Glotzer,
     A. Z. Panagiotopoulos, Efficient neighbor list calculation for
     molecular simulation of colloidal systems using graphics pro-
     cessing units, preprint.
[27] J. Goldsmith, J. Salmon, Automatic creation of object hierar-
     chies for ray tracing, IEEE Computer Graphics and Applica-
     tions 7 (5) (1987) 14–20. doi:10.1109/MCG.1987.276983.
[28] J. D. MacDonald, K. S. Booth, Heuristics for ray tracing using
     space subdivision, The Visual Computer 6 (3) (1990) 153–166.
     doi:10.1007/BF01911006.
[29] B. Smits, Efficiency issues for ray tracing, Journal of Graph-
     ics Tools 3 (2) (1998) 1–14. doi:10.1080/10867651.1998.
     10487488.
[30] T. Karras, T. Aila, Fast parallel construction of high-quality
     bounding volume hierarchies, in: Proceedings of the 5th High-
     Performance Graphics Conference on - HPG ’13, ACM Press,
     New York, New York, USA, 2013, p. 89. doi:10.1145/2492045.
     2492055.
[31] S. Gottschalk, Separating axis theorem, Tech. rep., TR96-024,
     Dept. of Computer Science, UNC Chapel Hill (1996).
[32] S. Jacobs, Game programming gems 7, Charles River Media/-
     Course Technology, Boston, MA, 2008.
[33] W. Wang, J. Wang, M.-S. Kim, An algebraic condition for the
     separation of two ellipsoids, Computer Aided Geometric Design
     18 (6) (2001) 531–539. doi:10.1016/S0167-8396(01)00049-8.
[34] S. Alfano, M. L. Greer, Determining if two solid ellipsoids inter-
     sect, Journal of Guidance, Control, and Dynamics 26 (1) (2003)
     106–110. doi:10.2514/2.5020.
[35] C. L. Phillips, J. A. Anderson, S. C. Glotzer, Pseudo-random
     number generation for Brownian Dynamics and Dissipative Par-
     ticle Dynamics simulations on GPU devices, Journal of Com-
     putational Physics 230 (19) (2011) 7191–7201. doi:10.1016/j.
     jcp.2011.05.021.
[36] Y. Afshar, F. Schmid, A. Pishevar, S. Worley, Exploiting seed-
     ing of random number generators for efficient domain decom-
     position parallelization of dissipative particle dynamics, Com-
     puter Physics Communications 184 (4) (2013) 1119–1128. doi:
     10.1016/j.cpc.2012.12.003.
[37] T. Schilling, S. Pronk, B. Mulder, D. Frenkel, Monte Carlo
     study of hard pentagons, Physical Review E 71 (3) (2005)
     036138. doi:10.1103/PhysRevE.71.036138.
[38] P. F. Damasceno, M. Engel, S. C. Glotzer, Predictive
     self-assembly of polyhedra into complex structures, Science
     337 (6093) (2012) 453–457. doi:10.1126/science.1220869.
[39] M. R. Khadilkar, F. A. Escobedo, Self-assembly of binary space-
     tessellating compounds, Journal of Chemical Physics 137 (19)
     (2012) 194907. doi:10.1063/1.4765699.




                                                                          12
