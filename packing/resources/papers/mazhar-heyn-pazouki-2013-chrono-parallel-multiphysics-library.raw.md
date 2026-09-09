Mech. Sci., 4, 49–64, 2013
www.mech-sci.net/4/49/2013/                                                                                    Mechanical
doi:10.5194/ms-4-49-2013
© Author(s) 2013. CC Attribution 3.0 License.                                                                  Sciences
                                                                                                                     Open Access




           Chrono: a parallel multi-physics library for rigid-body,
                     flexible-body, and fluid dynamics
       H. Mazhar1 , T. Heyn1 , A. Pazouki1 , D. Melanz1 , A. Seidl1 , A. Bartholomew1 , A. Tasora2 , and D. Negrut1
           1
               Simulation Based Engineering Lab, Department of Mechanical Engineering, University of Wisconsin,
                                                    Madison, WI, 53706, USA
               2
                 Department of Industrial Engineering, University of Parma, V.G.Usberti 181/A, 43100, Parma, Italy

                                     Correspondence to: D. Negrut (negrut@engr.wisc.edu)
                        Received: 16 November 2012 – Accepted: 26 January 2013 – Published: 12 February 2013

        Abstract. The last decade witnessed a manifest shift in the microprocessor industry towards chip designs that
        promote parallel computing. Until recently the privilege of a select group of large research centers, Teraflop
        computing is becoming a commodity owing to inexpensive GPU cards and multi to many-core x86 processors.
        This paradigm shift towards large scale parallel computing has been leveraged in Chrono, a freely available
        C++ multi-physics simulation package. Chrono is made up of a collection of loosely coupled components
        that facilitate different aspects of multi-physics modeling, simulation, and visualization. This contribution pro-
        vides an overview of Chrono::Engine, Chrono::Flex, Chrono::Fluid, and Chrono::Render, which are modules
        that can capitalize on the processing power of hundreds of parallel processors. Problems that can be tackled
        in Chrono include but are not limited to granular material dynamics, tangled large flexible structures with
        self contact, particulate flows, and tracked vehicle mobility. The paper presents an overview of each of these
        modules and illustrates through several examples the potential of this multi-physics library.


1   Introduction                                                    tinue to double every two years for the current decade. This
                                                                    will translate into immediate access to commodity chips that
                                                                    host multiple compute cores. Given the stagnation in proces-
Over the last decade there has been a manifest trend in the         sor operating frequency, an ever growing gap between CPU
hardware industry to increase flop rates by increasing the          speed and memory speed, and the waning of instruction level
number of cores available on a processor. To a very large           parallelism gains, it becomes apparent that the only way we
extent, the tide that propelled sequential computing for sev-       can continue to enjoy reduced simulation times or ability to
eral decades is subsiding. The frequency at which cores are         rely on refined models is to fall back on parallel comput-
operated today has at best plateaued; in many cases, it went        ing. There are two major directions in which parallel com-
down in an attempt to tame power dissipation and overheat-          puting has evolved. The x86 architecture has defined a so-
ing. Instruction level parallelism advances that ensured re-        lution that evolved as a steady and predictable process in
spectable gains through pipelining and out of order execu-          which the number of cores on a chip increased over time:
tion have largely fulfilled their potential. The bright spot in     AMD produces today 16 core chips, while Intel has 12 core
this evolving hardware landscape has been the growing im-           processors. Leveraging these chips requires a low entry point
petus behind parallel computing hardware. If anything has           that calls for programming against relatively mature libraries
held steady over the last four decades, it has been the pace at     such as OpenMP, MPI, pthreads, cilk, TBB, etc. At mem-
which transistors are packed per unit area in computer chips.       ory bandwidths of 75 GB s−1 and flop rates of 0.3 TFlop s−1 ,
This trend allows today chip designs that draw on 22 nm fea-        this has traditionally represented the conservative choice for
ture length. Intel’s road map calls for 14 nm technology in         entering the parallel computing arena. With the release of
2014, 10 nm in 2016, 7 nm in 2018, and 5 nm in 2020. In             CUDA 1.0 in 2006, NVIDIA offered a second alternative
other words, the number of transistors per unit area will con-

Published by Copernicus Publications.
50                H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics

to leveraging parallel computing by programming the ubiq-          such systems also include mechanisms composed of rigid
uitous video cards available on millions of desktops world-        bodies and mechanical joints. These challenges require an ef-
wide. This path to parallel computing is less conventional as      ficient and robust simulation tool, which has been developed
it requires one to get familiar with the hardware layout and       in the Chrono simulation package. Chrono::Engine was ini-
memory hierarchy associated with GPUs. Today, an Nvidia            tially developed leveraging the Differential Variational In-
GPU has close to seven billion transistors. Priced at about        equality (DVI) formulation as an efficient method to deal
$6000, an Nvidia Kepler K20x delivers a memory bandwidth           with problems that encompass many frictional contacts – a
of 250 GB s−1 and 1.3 TFlop s−1 by virtue of using more than       typical bottleneck for other types of formulations (Anitescu
2800 Scalar Processors. It is used side by side with a regular     and Tasora, 2010; Tasora and Anitescu, 2010). This approach
CPU processor, which means that heterogeneous computing,           enforces non-penetration between rigid bodies through con-
on the CPU and GPU, can lead to substantial speed gains. In        straints, leading to a cone-constrained quadratic optimiza-
this framework, the GPU plays the role of an accelerator by        tion problem which must be solved at each time step (Ne-
boosting the floating point performance of the CPU. A sim-         grut et al., 2012). Chrono::Engine has since been extended
ilar setup is offered now by Intel; i.e., CPU plus accelerator,    to support the Discrete Element Method (DEM) formula-
owing to its recent release of the Knights Corner architec-        tion for handling the frictional contacts present in granu-
ture. A Knights Corner chip has about 60 cores, can deliver        lar dynamics problems (Cundall, 1971; Cundall and Strack,
up to 320 GB s−1 and 1 TFlop s−1 , and uses the x86 instruc-       1979). This formulation computes contact forces by penaliz-
tion set architecture, which translates into an easier adoption    ing small interpenetrations of colliding rigid bodies. Various
path provided one is familiar with OpenMP or MPI.                  contact force models can be used depending on the applica-
   It becomes apparent that in the immediate future, any in-       tion (Mindlin and Deresiewicz, 1953; Kruggel-Emden et al.,
crease in simulation speed or model complexity in Compu-           2007).
tational Science will be fueled by parallel computing. This           The remainder of this section describes the features of
paper outlines an ongoing effort in the area of computational      Chrono::Engine, starting with the structure of the code. Next,
mutlibody dynamics that is motivated by this belief. It starts     several sub-sections describe the use of GPU computing in
with a description of a core simulation engine that aims at        the collision detection task, the use of MPI for distributed so-
simulation of many-body dynamics problems with friction            lution of large systems, and validation work which has been
and contact. Chrono::Engine handles both rigid and flexible        done to assess the accuracy of the simulation tool.
bodies and draws on MPI and/or GPU computing. It then
discusses Chrono::Fluid, a GPU parallel simulation tool that       2.1   Code structure of Chrono::Engine
aims at fluid-solid interaction problems, which is singled out
as an application area that has been largely ignored until re-     The core of Chrono::Engine is built around the concept of
cently due to an excessive computational burden incurred by        middleware, namely a layer of classes and functions that can
the simulation of systems of practical relevance. Finally, the     be used by third-party developers to create complex mechan-
papers outlines a rendering pipeline that is used for postpro-     ical simulation software with little effort (Tasora et al., 2007).
cessing of big data. Chrono::Render is capable of using 320        Because of this, graphical user interfaces and end-user tools
cores and is built around Pixar’s RenderMan. All these com-        are not the main focus of the Chrono::Engine core project; it
ponents combine to produce Chrono, a multi-physics simu-           is assumed that programs with graphical interfaces are built
lation environment that is designed to take advantage of com-      on top of such middleware, or should be considered as addi-
modity parallel computing made available by many-core and          tional, or optional, modules.
GPU architectures.                                                    Given the complexity of the project, approaching half
                                                                   a million lines of code, the software is organized in
                                                                   classes and namespaces as recommended by the Object
2    Chrono::Engine                                                Oriented Programming paradigm, targeting modularity, en-
                                                                   capsulation, reusability and polymorphism. The libraries of
The Chrono::Engine software is a general-purpose simulator         Chrono::Engine are thread safe, fully re-entrant, and include
for three dimensional multi-body problems (Tasora and An-          more than six hundred C++ classes. Objects from these
itescu, 2011). Specifically, the code is designed to support the   classes can be instantiated and used to define models and
simulation of very large systems such as those encountered in      simulations that run in third party software, for instance ve-
granular dynamics, where the number of interacting elements        hicle simulators, CAD tools, virtual reality applications, or
can be in the millions. Target applications include tracked        robot simulators.
vehicles operating on granular terrain (Heyn, 2009) or the            Chrono::Engine is completely platform-independent,
Mars Rover operating on discrete granular soil. In these ap-       hence libraries are available for Windows, Linux and Mac
plications, it is desirable to model the granular terrain as a     OSx, for both 32 bit and 64 bit versions. Moreover, we fol-
collection of many thousands or millions of discrete bodies        lowed a modular approach, splitting the libraries in mod-
interacting through contact, impact, and friction. Note that       ules that can be dynamically loaded only if necessary, thus

Mech. Sci., 4, 49–64, 2013                                                                         www.mech-sci.net/4/49/2013/
H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics                  51

minimizing issues of dependency from other libraries and          tures, CAD models), with multiple paths from pre-processing
reducing memory footprint. For instance, we developed li-         to post-processing. To this end, we also provide a C# add-in
braries for MATLAB interoperability, for real-time visualiza-     for a parametric 3-D CAD package (SolidWorks) that can
tion through OpenGL, for interfacing with post-processing         be used to export models into Chrono::Engine without pro-
tools, etc. (see Fig. 1).                                         gramming efforts (see Fig. 4).
   Classes and objects have been tested and profiled for
fast execution, in order to achieve real-time performance
when possible. Modern programming techniques have been            2.2     Collision detection in Chrono::Engine
adopted, like metaprogramming, class templating, class fac-
                                                                  This section describes the collision detection algorithm de-
tories, memory leak trackers and persistent-transient data
                                                                  signed and implemented for the Chrono::Engine package.
mapping. C++ operator overloading has been used to provide
                                                                  Recall that problems of interest are focused on granular dy-
a compact algebra to manage quaternions, static and moving
                                                                  namics, such as sand flowing inside an hourglass, a rover
coordinate systems, and OS-agnostic classes are used for log-
                                                                  running over sandy terrain, an excavator/frontloader dig-
ging, streaming/checkpointing and exception handling.
                                                                  ging/loading granular material, etc. In this context, the col-
   We embraced an intense object-oriented approach, there-
                                                                  lision detection task is performed on a rather small collec-
fore most C++ objects that define parts of the multi-
                                                                  tion of rigid and/or deformable bodies of complex geome-
body model are inherited from a base class called
                                                                  try (hourglass wall, wheel, track shoe, excavator blade, dip-
ChPhysicsItem, which defines the essential interfaces for
                                                                  per), and a very large number of bodies (millions to billions)
all items that have some degrees of freedom. For example,
                                                                  that make up the granular material. On this scale, the colli-
specialized classes that inherit the ChPhysicsItem are the
                                                                  sion detection task, particularly when dealing with the gran-
ChBody class, which is used for 3-D rigid bodies as shown
                                                                  ular material, fits perfectly the Single Instruction Multiple
in Fig. 2, ChShaft, which is used for 1-D concentrated pa-
                                                                  Data (SIMD) computation paradigm. Specifically, the same
rameter models of power trains, ChLinkLockRevolute that
                                                                  sequence of instructions needs to be applied to every indi-
is a joint between rigid bodies, and so on. A set of more than
                                                                  vidual body and/or contact in the granular material. There-
thirty mechanical constraints are part of this class hierarchy.
                                                                  fore, a collision detection algorithm capable of leveraging
Furthermore, the architecture is open to further definition of
                                                                  the SIMD computational power of commodity Graphics Pro-
new specialized classes for user-customized parts and joints.
                                                                  cessing Units (GPUs) was developed and implemented to re-
An object of ChSystem class stores a list of all moving parts
                                                                  move collision detection as the bottleneck in large granular
and performs the simulation.
                                                                  dynamics simulations.
   Each ChPhysicsItem-inheriting class can encapsulate a
                                                                     The parallel collision detection algorithm is separated into
variable number of ChLcpVariable objects and/or a vari-
                                                                  two phases, broadphase, and narrowphase. The broadphase
able number of ChLcpConstraint objects, that are fed to
                                                                  algorithm quickly determines a list of potential contact pairs
the solver for Cone Complementarity Problems (CCP) at
                                                                  while the narrowphase algorithm determines actual contact
each time step of the DVI integration; this helps the devel-
                                                                  information. A brief outline of the parallel collision detection
opment of black-box CCP solvers that are independent from
                                                                  algorithm is presented below, for more details see (Mazhar
the data structures of the physical layer. Also, these data
                                                                  et al., 2011; Pazouki et al., 2012, 2010).
structures represent the sparse data for the model descrip-
tion, which is completely matrix- and vector-free for the sake
of a small memory footprint and fast linear algebra. Specifi-     2.2.1    Broad-Phase algorithm
cally, tthe system matrices for mass, Jacobians, etc. are never
explicitly assembled. The objects of most of the above men-       The Broad-Phase algorithm is used to compute whether two
tioned classes are managed by smart (shared) pointers with        bodies might be in contact at a given time. The purpose of
automatic deletion.                                               the broad-phase algorithm is not to find actual contact infor-
   This relieves the programmer from the burden of taking         mation, but rather to determine if a contact could potentially
care of object’s lifetime, given that the relationships between   occur based on the Axis Aligned Bounding Boxes of the bod-
objects can be quite complex as illustrated in Fig. 3. A large    ies involved.
portion of the C++ classes are available also as Python mod-         An Axis Aligned Bounding Box (AABB) is a special case
ules; this enables the use of most simulation features in a       of a bounding box that is always aligned to the global refer-
scripted environment. Since novice users are more comfort-        ence frame, simplifying collision detection as the bounding
able with Python than with C++, the Python interface proved       box cannot rotate. Because of this, the volume enclosed by
to be optimal for teaching purposes. The Python interface         the bounding box will always be equal to or greater than the
was produced using the SWIG utility, a process that auto-         volume of the shape it encloses. AABB generation is simple
matically generates the code for the Python wrapper.              and can be easily paralellized on a per object basis. See Fig. 5
   The software architecture has been designed to accommo-        for an example of AABB computation for a cylinder in 3-D
date an expandable system for handling assets (meshes, tex-       space.

www.mech-sci.net/4/49/2013/                                                                        Mech. Sci., 4, 49–64, 2013
            Mazhar et al.: Chrono: A Parallel Multi-Physics Library for Rigid-Body, Flexi
52                H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics


                     Examples of use       Example C++ program 'A'          Example C++ program 'B'      Example Python program




                      Chrono libraries
                                                 unit_MPI             unit_GPU           unit_MATLAB           unit_POSTPROCESS




                           Chrono Engine                                                          unit_OPENGL        unit_PYTHON
                                                    unit_CASCADE            unit_IRRLICHT




                                                                     CUDA                     Irrlicht
                      External             MPICH2                                                                  Python v3
                      dependencies
                                                                               MATLAB
                                                       OpenCASCADE                                    OpenGL




                                                                        Operating System



Figure 1. UML graph of dependencies between module libraries.
             Figure 1: UML graph of dependencies between module libraries.                                                          Figure 2: Cla



            tion through OpenGL, for interfacing with post-processing                                                              tthe system m
            tools, etc. (see Figure 1).                                                                                            plicitly assem
                                                                                                                                   tioned classes
            Classes and objects have been tested and profiled for fast ex-                                                         automatic dele
            ecution, in order to achieve real-time performance when pos-
            sible. Modern programming techniques have been adopted,                                                     This relieves t
            like metaprogramming, class templating, class factories,                                                    of object’s life
            memory leak trackers and persistent-transient data mapping.                                                 jects can be qu
            C++ operator overloading has been used to provide a com-                                                    tion of the C+
            pact algebra to manage quaternions, static and moving coor-                                                 this enables th
Figure 2. Class ineritance diagram for objects of ChBody type.
            dinate systems, and OS-agnostic classes are used for logging,                                               environment.
            streaming/checkpointing and exception                     handling.                                         Python than w
2.2.2 Spatial Subdivision algorithm                            2.2.3 Narrow-Phase algorithm
                                                                                                                        timal for teach
             We embraced an intense object-oriented
A high-level overview of the GPU-based collision detection
                                                                                 approach, therefore
                                                                    Once potential contacts have been determined duced   from the using t
is as follows.most    C++ objects that define parts of the multi-body model
               The collision detection  process starts by identi-   broad-phase    collision detection stage, the Narrow-Phase al-
fying the intersections between AABBs and bins (see Fig. 6
                                                                                                                        generates
                                                                    gorithm needs to process each possible contact and determine
                                                                                                                                     the c
             are    inherited         from      a    base
for a visual representation of a bin). The AABB-bin pairs are  class    called      ChPhysicsItem,
                                                                    if it actually occurs. To this end an algorithm capable of de-
subsequentlywhich
               sorted bydefines       the essential interfaces
                          bin id. Next,  each bin’s  starting in-   terminingforcontacts
                                                                                   all items
                                                                                           betweenthat
                                                                                                    convexhave          The
                                                                                                            geometries was     software a
                                                                                                                            imple-
dex is determined so that the bins’ AABBs can be traversed          mented on the GPU. This algorithm, called “XenoCollide”
sequentially.some      degrees
               All AABBs     touchingof   freedom.
                                        a bin               For example,
                                              are subsequently                     specialized
                                                                    (Snethen, 2007),
                                                                                                                        an expandable
                                                                                                      classesPortal Refinement
                                                                                       is based upon Minkowski
checked against each other for collisions.
             that inherit the ChPhysicsItem are                     (MPR) (Snethen, 2008).
                                                                          the ChBody class, which                       CAD models)
             is used for 3D rigid bodies as shown in Fig.2, ChShaft,                                                    post-processin
Mech. Sci., 4, 49–64, 2013                                                                          www.mech-sci.net/4/49/2013/
             which is used for 1D concentrated parameter models of                                                      a parametric 3
             power trains, ChLinkLockRevolute that is a joint between                                                   to export mode
4 H. Mazhar et al.: Chrono:
               Mazhar       a parallel
                        et al.: Chrono multi-physics library for rigid-body,
                                        : A Parallel Multi-Physics           flexible-body,
                                                                       Library              and fluid
                                                                                for Rigid-Body,       dynamics and Fluid Dynamics
                                                                                                 Flexible-Body,           53




  Figure 3. Collaboration graph between
                            Figure      classes: example
                                   3: Collaboration      forbetween
                                                     graph          and ChSystem.
                                                             ChBody classes: example for ChBody and ChSystem.


  2.3 Using MPI for distributed Chrono                                      unit which must always be kept together. Therefore, if any
ular  material, fits perfectly the Single Instruction Multiple
                                                                            body in a chain of constrained bodies is contained in a given
Data (SIMD) computation paradigm. Specifically, the same
  Chrono ofhasinstructions
               been furtherneeds
                             extended   to allow  thetouse  of CPU          sub-domain, all bodies in the chain are considered by that
sequence                           to be   applied       every   indi-                            Chrono::Engine add-in .bmp
  parallelism for certain problems. To  efficiently simulate   large        sub-domain and used to correctly solvetexturesthe constraint     equa-
                                                                                                                                     Photoshop, Paint, ..

vidual body and/or contact in the granular material. There-                 tions.
                                                                                                                                      Mesh refinement,
                                                                                                                                      UV texturing, etc.
  systems,
fore,       a domain
      a collision      decomposition
                    detection          approach
                               algorithm   capablehasofbeen  devel-
                                                          leveraging                                               .py           .obj
  oped to allow the use of many-core compute clusters. In this                                                     scene file    meshes
the SIMD computational power of commodity Graphics Pro-
  approach, we divide the simulation domain into a number of                2.3.1       Sub-division and set-up
cessing Units (GPUs) was developed and implemented to re-
  sub-domains in a lattice structure. Each sub-domain manages
move   collision detection as the bottleneck in large granular              A pre-processing Co-simulation  stepUNIT_PyParser
                                                                                                                   is used to C++discretize the simulation
  the simulation of all bodies contained therein. Note that bod-                                                                        program

dynamics                                                                    domain into a specified                   number ofPython       sub-domains, set up the
  ies may simulations.
                                                                                                                                  or
                                                                                                     TCP socket
            span the boundary between adjacent sub-domains.                                                      Chrono::Engine            program

                                                                            communication
                                                                                    SPICE, etc. ..        conduits        between processes, and initialize
                                                                                                                 core library


TheIn this  case,collision
       parallel   the body detection
                              is considered   shared and
                                           algorithm       its dynamics
                                                       is separated  into                                       UNIT_PostProcessing UNIT_Irrlicht
                                                                            the sub-domains as appropriate. The sub-division is based
   may be influenced by the participating sub-domains. The im-
two phases, broadphase, and narrowphase. The broadphase                     on a cubic lattice with support for arbitrary sized divisions.
   plementation leverages the MPI standard (Gropp et al., 1999)
algorithm quickly determines a list of potential contact pairs              The sub-domain   .dat         boundaries .pov are aligned with the global carte-
   to implement the necessary communication and synchroniza-                                 raw output              PovRay 3D
while     the narrowphase algorithm determines actual contact               sian coordinate system, and              renderingtheir locations            are user-specified.
                                                                                                                                               Realtime 3D

   tion between sub-domains.                                                                                         scripts                   view

information.     A brief   outlinetheofsimulation
                                        the parallelofcollision detection   Separate MPI processes are mapped to each sub-domain.
      This approach     enables                        large systems  in
algorithm     is First,
                 presented     below,   forpower
                                             more of
                                                   details   seecomput-
                                                                 (Mazhar    Note that at this time, the sub-division is static and does not
   two ways.            it relies   on the             parallel
et ing
    al., since
         2011;one
                Pazouki     et al.,core
                                    2012,                                   change during             the simulation. Therefore, the user should be
                     computer           can2010).
                                             be assigned to each MPI                    Octave, NumPy, ..
                                                                            careful to set up the discretization to maintain the best possi-
   process (and therefore to each sub-domain). These processes
                                                                            ble load balancing.
   can execute in parallel, constrained only by the required com-                                                   .bmp
                                                                               In terms of communication,           animation      each sub-domain in the grid
   munication
2.2.1           and synchronization.
         Broad-Phase      Algorithm Second, it allows access to                                                     frames
                                                                            can communicate with all other sub-domains. These commu-
                                                                                         plots
   the larger memory pool available on distributed memory ar-
                                                                            nication pathways are set up and initialized during the pre-
   chitectures. Whereas a single node or GPU card may have
The   Broad-Phase algorithm is used to compute whether two                  processing step Figure      and persist
                                                                                                                 4: Network  throughoutof asset   theworkflows.
                                                                                                                                                         simulation.
   about 6 GB of memory, a distributed memory cluster may
bodies   might   be in of
                        contact at memory,
                                   a given time.     Thethe
                                                          purpose              Note that this implementation relies heavily on inheri-
   have on   the order    1 TB of             enabling       simula-of
thetion
     broad-phase    algorithm  is not to find actual contact infor-         tance and the class-based structure of Chrono. For exam-
        of vastly larger problems.
mation,                                                                     ple, ChSystem is extended to ChSystemMPI by including
      Notebut  rather
            that      to determine
                  the domain        if a contact
                              decomposition       could potentially
                                               approach    currently
occur                                                                       the code to perform communication and synchronize the sub-
   usesbased   on theelement
        the discrete   Axis Aligned
                              methodBounding
                                       to resolve Boxes
                                                  frictionofand
                                                             thecon-
                                                                 bod-
iestact
     involved.                                                              domains.
        forces between elements in the system. The approach
   also supports constraints between bodies in the simulation
AnbyAxis    AlignedanBounding
       considering     assembly ofBox   (AABB) rigid
                                    constrained    is a special
                                                        bodies ascase
                                                                   a
of a bounding box that is always aligned to the global refer-                  volume of the shape it encloses. AABB generation is sim-
ence frame, simplifying collision detection as the bounding                    ple and can be easily paralellized on a per object basis. See
  www.mech-sci.net/4/49/2013/
box  cannot rotate. Because of this, the volume enclosed by                                                Mech.computation
                                                                               Fig. 5 for an example of AABB       Sci., 4, 49–64,
                                                                                                                               for 2013
                                                                                                                                   a cylinder
the bounding box will always be equal to or greater than the                   in 3D space.
 n graph between classes: example for ChBody and ChSystem.
          54                H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics

 uction Multiple
fically, the same
d to every indi-                                                       Chrono::Engine add-in               .bmp
                                                                                                                         Photoshop, Paint, ..
                                                                                                           textures
material. There-                                                                                                          Mesh refinement,
                                                                                                                          UV texturing, etc.

 e of leveraging                                                            .py                .obj
                                                                            scene file         meshes
 y Graphics Pro-
plemented to re-
n large granular                             Co-simulation             UNIT_PyParser            C++ program
                                                                                                or
                                                          TCP socket
                                                                       Chrono::Engine           Python program
                                                                       core library
                                    SPICE, etc. ..
                                                                       UNIT_PostProcessing UNIT_Irrlicht
  separated into
The broadphase
                                                                                         Mazhar et al.: Chrono: A Parallel Multi-Physics Library for
ial contact pairs                            .dat                          .pov                                                                 Maximum Point
                                             raw output                    PovRay 3D
s actual contact                                                           rendering
                                                                           scripts
                                                                                                        Realtime 3D
                                                                                                        view

 lision detection
ils see (Mazhar
                                         Octave, NumPy, ..




                                                                          .bmp
                                                                          animation
                                                                          frames
                                          plots
                                                                                                                 Minimum Point
          Figure 4. Network of asset workflows.                                                Figure 5: Example of AABB generation for 3D cylinder.
ute whether two                                        Figure 4: Network of asset workflows.
 The purpose of                                                                                                                                         Bin
al contact infor-
ould potentially
oxes of the bod-


s a special case
 he global refer-         volume of the shape it encloses. AABB generation is sim-
as the bounding           ple and can be easily paralellized on a per              object basis. See
                                                                               3-Dimensional Grid
me enclosed     byExample ofFig.
         Figure 5.           AABB5generation
                                   for anforexample
                                             3-D cylinder. of AABB computation for a cylinder
                                                                 Figure 6. Example of 3-D space divided into bins.
greater than the          in 3D space.                             Figure 6: Example of 3D space divided into bins.
          2.3.2   Simulation and communication
                                                                       rank to each sub-domain so that A is mapped to MPI rank
          Each sub-domain is now represented by a ChSystemMPI ob-      0, B → 1, C → www.mech-sci.net
                                                                                       2, and D → 3. Each sub-domain maintains
          ject and an associated MPI process. For example, assume2.2.2
                                                                    a  atSpatial
                                                                          all times Subdivision      Algorithm
                                                                                    m + 1 lists of objects. The first list contains all
          simulation is discretized into a set S of m sub-domains. In  objects which are even partially contained in the associated
          this case, let S = {A, B,C, D} and m = 4, and map an MPI     sub-domain. These are the objects which must be considered
                                                                                         A high-level overview of the GPU-based collision detection
                                                                                         is as follows. The collision detection process starts by identi-
          Mech. Sci., 4, 49–64, 2013                                                                                   www.mech-sci.net/4/49/2013/
                                                                                         fying the intersections between AABBs and bins (see Fig. 6
                                                                                         for a visual representation of a bin). The AABB-bin pairs are
                                                                                         subsequently sorted by bin id. Next, each bin’s starting in-
which should contain the same objects as BA . Further, list             state identically, but due to the potential for round-off error
BB is not used but is created for the sake of generality. All           we synchronize the state from the master sub-domain (where
lists are maintained in order sorted by object ID number (see           the center-of-mass is located) to all others. The final stage
   H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body,
Fig.7).                                                                        flexible-body,
                                                                        is to process    the mand+ 1 fluid
                                                                                                      listsdynamics
                                                                                                            in each sub-domain, as  55 objects
                                                                        may enter or leave a given sub-domain or be shared between
                                                                        At  this point,
                                                                        a different   seteach   sub-domain Xnecessitating
                                                                                          of sub-domains,        has the true net force of the
                                                                                                                               updates
                                                                     on contents
                                                                         each body    in its list
                                                                                   of the lists.  XO . Each   sub-domain   can advance
                                                                              the state of its bodies in time by one time step by computing
                                                                              the new accelerations, velocities, and positions of all objects
                                                                              in the sub-domain given their mass/inertia properties and the
                                                                                 2.3.3 Example Simulation
                                                                              set of applied forces. We perform an end-of-step communi-
                                                                              cation to synchronize object states among sub-domains. All
                                                                                 In this example
                                                                              sub-domains     which we    simulate
                                                                                                      share   a givena body
                                                                                                                         Marsshould
                                                                                                                                 Rover compute
                                                                                                                                         type wheeled
                                                                                                                                                    its ve-
                                                                                 hicle  operating    on  granular    terrain.   The   vehicle
                                                                              new state identically, but due to the potential for round-off    is  composed
                                                                                 of we
                                                                              error  a chassis    and six
                                                                                         synchronize    the wheels
                                                                                                             state from connected
                                                                                                                           the mastervia   revolute joints.
                                                                                                                                         sub-domain
                                                                                 The wheels
                                                                              (where             are driven iswith
                                                                                       the center-of-mass              a constant
                                                                                                                  located)             angularThe
                                                                                                                              to all others.     velocity
                                                                                                                                                    fi-    of
                                                                              nalπstage  is to process
                                                                                    rad/sec.             the m + terrain
                                                                                                The granular       1 lists iniseach  sub-domain,
                                                                                                                                composed            as
                                                                                                                                              of 2,016,000
                                                                              objects  may enter
                                                                                 spherical          or leave
                                                                                              particles.   The a given   sub-domain
                                                                                                                  simulation            or be shared
                                                                                                                                  is divided  into 64 sub-
                                                                              between
                                                                                 domainsa different
                                                                                             and usesset of sub-domains,
                                                                                                         a time    step of 10 necessitating
                                                                                                                                 −5          updates
                                                                                                                                     sec. This    small time
                                                                              of step
                                                                                 the contents   of the lists.
                                                                                      is necessary due to the use of the DEM approach to com-
                                                                                 pute contact forces - a stiff force model is used to achieve
                                                                                smallExample
                                                                              2.3.3   normal simulation
                                                                                             interpenetration, requiring a small step size to
                                                                                 maintain stability. A snapshot from the simulation can be
                                                                              In this example we simulate a Mars Rover type wheeled
                                                                                 seen in Fig.8. In the figure, note that the wheels of the rover
                                                                              vehicle operating on granular terrain. The vehicle is com-
                                                                                 are checkered
                                                                              posed   of a chassisblue  andandsix white.
                                                                                                                   wheels This   signifies
                                                                                                                            connected    via that  the master
                                                                                                                                               revolute
                                                                              joints. The wheels are driven with a constant angular velocityand the
                                                                                 copy   of  the  rover    assembly    is in the blue  sub-domain
                                                                              of rover
                                                                                  π rad sspans
                                                                                         −1
                                                                                            . Theinto    adjacent
                                                                                                     granular       sub-domains.
                                                                                                                terrain  is composedInofFig.2 016 8,000
                                                                                                                                                     the rover
                                                                                 has  settled    into   the  granular    terrain and   is
                                                                              spherical particles. The simulation is divided into 64 sub-  starting   to move
                                                                                 forward.      The arear                  −5
                                                                              domains    and uses       timewheels
                                                                                                              step of displace
                                                                                                                       10 s. Thismoresmallgranular
                                                                                                                                             time stepmaterial
                                                                                 than the front
                                                                              is necessary    due towheels
                                                                                                       the usebecause
                                                                                                                of the DEMthe center  of mass
                                                                                                                               approach           of the rover
                                                                                                                                          to compute
Figure
   Figure7: 7.(TOP)
               (Top) Sample 2-D2D simulation   domainwith
                                   simulation domain   withfour
                                                              foursub-
                                                                     sub-     contact  forces
                                                                                 is closer   to –thea stiff
                                                                                                      rear force
                                                                                                            of themodel    is used to achieve small
                                                                                                                    vehicle.
   domains
domains     andseven
          and    sevenobjects.
                       objects. (BOTTOM)
                                (Bottom) Corresponding objectobject
                                            Corresponding     lists for
                                                                     lists    normal interpenetration, requiring a small step size to main-
foreach
    eachsub-domain.
          sub-domain.                                                         tain stability. A snapshot from the simulation can be seen in
                                                                              Fig.
                                                                                 2.48. InValidation
                                                                                           the figure,and  noteDemonstration
                                                                                                                 that the wheelsofofTechnology
                                                                                                                                       the rover are
The   sub-domains                                                             checkered blue and white. This signifies that the master copy
   when    computing are nowforces,
                      contact  ready for
                                      for example.
                                          time-stepping.
                                                     The next Each    sub-
                                                                 m lists
                                                                              of the rover assembly is in the blue sub-domain and the rover
domain        performs
   containXbodies  whichcollision
                          are shareddetection  among
                                       with other         all objects in
                                                   sub-domains.                  This section describes a validation effort in which experi-
                                                                              spans into adjacent sub-domains. In Fig. 8, the rover has set-
list XInO our
          andexample,
               computesub-domain      B maintains
                         the associated    collisiontheforces
                                                         lists Bbased
                                                                 O , BA ,on      mental results were compared to simulation results obtained
                                                                              tled into the granular terrain and is starting to move forward.
theBBDEM
      , BC , force
              and BDmodel.
                     . BO is Then,
                              the listsub-domain
                                       of all objectsX that   intersectthe
                                                         computes             Thefrom     wheels ::Engine.
                                                                                    rearChrono       displace moreTo this   end, amaterial
                                                                                                                        granular    test rigthanwas the
                                                                                                                                                     designed
 (touch) sub-domain B, while BA is the list of objects which
                                                                              front wheels because the center of mass of the rover is closer
 are in sub-domain A and B. Note that sub-domain A has a list
Mech.   Sci. should contain the same objects as BA . Further, list            to the rear of the vehicle.                               www.mech-sci.net
 AB which
 BB is not used but is created for the sake of generality. All
 lists are maintained in order sorted by object ID number (see                2.4     Validation and demonstration of technology
 Fig. 7).
                                                                              This section describes a validation effort in which experi-
    The sub-domains are now ready for time-stepping. Each
                                                                              mental results were compared to simulation results obtained
 sub-domain X performs collision detection among all objects
                                                                              from Chrono::Engine. To this end, a test rig was designed
 in list XO and computes the associated collision forces based
                                                                              and fabricated to measure the rate at which granular material
 on the DEM force model. Then, sub-domain X computes the
                                                                              flowed out of a slit due to gravity. Chrono::Engine was used
 net force on each object in list XO , taking into account the
                                                                              to set up a corresponding simulation to match the experimen-
 contact forces, gravitational forces, and applied forces.
                                                                              tal results. For more detail, see Melanz et al. (2010).
    Next, mid-step communication occurs. Sub-domain X
 should send to each sub-domain Y the net force on each body
 in list XY . Similarly, X should receive from each Y the net                 2.4.1    Experimental model
 force on each body in list XY . Finally, X should compute the
                                                                              The experimental set-up consisted of a fixed base, a mov-
 total force on each body in list XO . Note that X may receive
                                                                              able wall (angled at 45◦ ), a translational stage, a linear ac-
 force contributions for a given body from any or all of the
                                                                              tuator, and a scale (see schematic in Fig. 9). The linear ac-
 other sub-domains in the system.
                                                                              tuator was capable of quickly opening a precise gap, out of
                                                                              which the granular material would flow due to gravity. The

  www.mech-sci.net/4/49/2013/                                                                                      Mech. Sci., 4, 49–64, 2013
Mazhar et al.: Chrono: A Parallel Multi-Physics Library for Rigid-Body, Flexible-Body, and Fluid Dynamic

                56                    H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics

                                                                                                2.4.2    Simulation model
                                                                                                Chrono::Engine was used to build a model representing the
                                                                                    experimental set up described above. In the model, the trough
                                                                                    was represented by four rectangular boxes of finite dimen-
                                                                                    sions. The motion of the box representing the angled side was
                                                                                    captured from the data sheet of the translational stage. The
                                                                                    granular material was modeled as perfect, identical spheres
                                                                                    with the same mass and coefficient of friction.
                                                                                        The load cell measured the outflow through the gap. In the
                                                                                    simulation, the scale was modeled by counting the number
                                                                                    of spheres below a certain height. The number of spheres
                                                                                    multiplied by the mass and gravity yielded the weight which
                                                                                    was compared with experimental results. A plane was used
                                                                                    to contain the spheres after they had been counted.
                                                                                        In order to save computational time, the simulation was
                                                                                    split into two parts: one representing the process of filling
                                                                                    the trough and the other the opening and measuring process.
                                                                                    In this way, the trough was filled with randomly positioned
                                                                                    spheres which were allowed to settle. Once the kinetic en-
                                                                                    ergy of the system was below 0.001 Joules and had reached
              Figure 8. Snapshot of Mars Rover simulation with 2 016 000 terrain
  gure 8: Snapshot          of Mars    Rover    simulation      with   2,016,000
              particles using 64 sub-domains. Bodies are colored by sub-domain,        relatively Figure
                                                                                    ater-                     9: Schematic
                                                                                                  constant value,                  of z-position
                                                                                                                     the x-, y- , and   validation    experiment.
                                                                                                                                                  of each
  in particleswithusing    64 sub-domains.
                   shared bodies                    Bodies are
                                  (those which span sub-domain      colored
                                                                boundaries)         sphere
                                                                            col-by sub-      was  and
                                                                                                  saved  translational
                                                                                                          to a file.        stage     moved     the left   angled sid
              oredshared
                   white. bodies (those which span sub-domain bound-                    The  same    initial conditions   from   the  settling simulation
                                                                                                  opening a precise gap from which the particles
 omain,
 brary for with
           Rigid-Body,   Flexible-Body, and Fluid Dynamics                     7
                                                                                    were used to perform all of the necessary simulations. At
  ies) colored white.                                                                             flow rate was measured by the scale. Schematic n
                                                                                    the beginning of each simulation the position data set of the
                                                                                    spheres was loaded into the model and the spheres were cre-
                                                                                    ated at the same positions they appeared in the filling process.
                                                                                    The motion was applied to the translating side to achieve the
 nd fabricated to measure the rate at which granular material                       desired gapmultiplied            by thebegan
                                                                                                   size, and the material      mass      and gravity yielded t
                                                                                                                                     to flow.
 owed out of a slit due to gravity. Chrono::Engine was used                             The       was compared with experimental
                                                                                              simulations    setup   consisted    of  39  000 rigid bodyresults. A
                                                                                    spheres with a radius of 2.5 × 10−4 m and a mass of 1.631 ×
   set up a corresponding simulation to match the experimen-                                      to contain the spheres after they had been co
                                                                                    10−7 kg. The following parameters were set for this simula-
  l results. For more detail, see (Melanz et al., 2010).                            tion. A time step of 10−4 s with 500 CCP iterations, and a
                                                                                    tolerance ofIn 10−7order
                                                                                                          for thetomaximum
                                                                                                                     save computational
                                                                                                                              velocity correction.time,
                                                                                                                                                     Sim- the sim
                                                                                    ulations were into     two run
                                                                                                      generally    parts:
                                                                                                                      for 8 s.one
                                                                                                                              SI unitsrepresenting
                                                                                                                                         were used for allthe proce
                                                                                    parameters.
                                                                                                                     trough and the other the opening and me
  4.1       Experimental Model
                                                                                                                     In thisused
                                                                                                        2.4.3 Procedure         way,     the trough
                                                                                                                                    to select  the frictionwas      filled with rand
                                                                                                                                                              coefficient
                                                                                                                     spheres which were allowed to settle. Onc
                                                                                                        The friction coefficient of a certain material is not a con-
 he experimental set-up consisted of a fixed base, a movable
                Figure
                 Figure 9.      ◦
                           9:Schematic
                               Schematic   ofof
                                              validation
                                                 validation experiment.
                                                               experiment. A linear    actuator
                                                                                Aalinear         and
                                                                                            actuator
                                                                                                        stant value.ergy
                                                                                                                      It canof   the system
                                                                                                                              depend   on variouswas         below 0.001
                                                                                                                                                      environmental      influ- Joules
   ,000 (angled
  all   ter-          at   45
                translational
                 and translational
                                  ),  a   translational
                                 stage stage
                                        moved    the left
                                               moved    theangled
                                                                    stage,
                                                             left angled
                                                                                      linear
                                                                            fixeda amount,
                                                                    side a side               open-
                                                                                     fixed amount,
                                                                                                  actuator,
                                                                                                        ences such as   humidity, surface
                                                                                                                     a relatively      constant       value, thetc.x-,
                                                                                                                                            quality, temperature           They- , and z
    by sub-
 nd    a
 n bound- scale ing (see
                     a precise
                 opening    a schematic
                                  gap
                              precise  from
                                        gap   which
                                              from  in   Fig.
                                                       the
                                                     which    the  9).
                                                             particles
                                                                  particles The
                                                                        flowed.    The
                                                                               flowed. linear
                                                                                         mass
                                                                                          The      actuator
                                                                                                flow
                                                                                               mass     friction coefficient of glass  was an  unknown      in the validation
                rate
                 flowwas   measured     by thebyscale.   Schematic     not tonotscale.                  process andsphere
                                                                                                                       needed towas    saved to before
                                                                                                                                   be determined      a file.further obser-
  as capable         ofratequickly
                             was measured
                                           opening the scale.
                                                             a Schematic
                                                                precise            to scale.
                                                                                gap,      out of which  vations could be done. To achieve this, one experiment at a
  e granular material would flow due to gravity. The scale                                              gap size of The
                                                                                                                     1.5 mmsame      initial conditions
                                                                                                                              was performed                       from the settling
                                                                                                                                                and multiple simulations
                scale   recorded
                 multiplied           the  mass     of  collected
                                                       gravity yielded
                                     the mass and granular
                                by collected                          granular     material
                                                                              the weight       as
                                                                                             which a    with  the same   setup  and  different  friction
                                                                                                                     used to perform all of the necessary coefficients    were simula
  corded the
 material           massofof
                function         time.  The    granular     material
                                                                         material
                                                                        consisted       of
                                                                                           as  a function
                                                                                           approx-
 was used        was compared with experimental results. A plane was used                               performed.   The  simulation   results were    compared     to the ex-
     time.
  erimen-
               The
                imately
                 to     granular
                    contain 40 000
                               the        material
                                      uniform
                                     spheres      glass
                                                after  they consisted
                                                           disruptor
                                                               had  been beads   of
                                                                                  with
                                                                           counted.    approximately
                                                                                          diameter      perimental   ginning
                                                                                                                    test results of
                                                                                                                                 to   each
                                                                                                                                    determinesimulation
                                                                                                                                                which    frictionthe   position
                                                                                                                                                                   coefficient      data s
 0,000
  .             of 500 microns.
             uniform order
                 In1.5
                            glass
                             to 2save
                                        Experiments were
                                       disruptor           beads   performed        for gap sizesof 500
                                                                        with diameter                                was
                                                                                                        resulted in the bestloaded
                                                                                                                             match, see   Fig.the
                                                                                                                                       into         model
                                                                                                                                               10. It           and thethatspheres w
                                                                                                                                                       was determined
                of       mm,       mm,computational
                                         2.5 mm, and 3time,    mm.the At simulation       was split
                                                                          least 5 experiments           µ = 0.15 most closely matched the experimental results. This
  icrons. Experiments
                 into performed
                were    two parts: for   were
                                        one          performed
                                               representing
                                            each    gap  size. the process for gap          sizes
                                                                                    of filling   the of 1.5          same positions they appeared in the filling p
                                                                                                        value was used for all subsequent simulations.
                 trough     and    the  other    the  opening
  m, 2 mm, 2.5 mm, and 3 mm. At least 5 experiments were           and    measuring        process.                  tion was applied to the translating side to ac
                 In this way, the trough was filled with randomly positioned
 erformed spheresfor each    which gapweresize.
                                              allowed to settle. Once the kinetic en-                                gap size, and the material began to flow.
 movable     ergy of the system was below 0.001 Joules and had reached
 actuator,   a relatively constant value, the x-, y- , and z-position of each                                 The simulations setup consisted of 39,000 ri
 actuator   Mech.
             sphere Sci., 4, 49–64,   2013                                                                                 www.mech-sci.net/4/49/2013/
  4.2
                     was saved
  f which Simulation Model
                                to a file.                                                                    with a radius of 2.5 × 10−4 m and a mass of
 he scale    The same initial conditions from the settling simulation were                                    The following parameters were set for thi
 function    used to perform all of the necessary simulations. At the be-                                                              −4
        8     H. Mazhar  Mazhar     et al.: Chrono    : A Parallel    Multi-Physics      Library    for Rigid-Body,    Flexible-Body, and Fluid Dy
        8     Mazhar et et al.:Chrono
                        al.:
                         Mazhar Chrono: :aAparallel
                                    et al.: Parallel
                                            Chrono  multi-physics library
                                                      :Multi-Physics
                                                        A Parallel        for rigid-body,
                                                                          Library
                                                                      Multi-Physics       flexible-body,
                                                                                     for Library
                                                                                         Rigid-Body,     and fluid dynamics
                                                                                                         Flexible-Body,
                                                                                                   for Rigid-Body,                     57 Fluid
                                                                                                                           and Fluid Dynamics
                                                                                                                      Flexible-Body,  and       Dyn




                                                                                                                      Figure 12: Weight vs time for a gap size of 2.5 mm.
                                                                                                    Figure
                                                                                                  Figure 12.12: Weight
                                                                                                             Weight       vs
                                                                                                                    vs. time
                                                                                                                 Figure       time
                                                                                                                           12for    forsize
                                                                                                                                 a gap
                                                                                                                               : Weight  avs
                                                                                                                                           gap   size
                                                                                                                                            oftime
                                                                                                                                               2.5 mm.ofa2.5
                                                                                                                                                    for   gapmm.
                                                                                                                                                              size of 2.5 mm.



                                    Figure 10: Selection of µ
                Figure     Selection
                       10. 10
                  Figure                    of: µSelection of µ
                                     of µ. 10
                              : Selection
                                 Figure




                                                                                                  Figure          Figure
                                                                                                         13. Weight          13
                                                                                                                    vs. timevs   : Weight
                                                                                                                             fortime         vs   time   for a gap size of 2 mm.
                                                                                                     Figure       Figure
                                                                                                             13: Weight     13   : aWeight
                                                                                                                                    gapfor
                                                                                                                                        sizeavs
                                                                                                                                             of 2time
                                                                                                                                              gap  mm.
                                                                                                                                                    sizeforofa2gap
                                                                                                                                                                mm.size of 2 mm.

                                                                                                  ally, Chrono::Flex leverages the GPU to accelerate solution
                                                                                                     3 Chrono::Flex
                                                                                             of large3problems.
                                                                                          3 Chrono::Flex Chrono::Flex
           Figure 11. Weight
              Figure         vs. timevsfortime
                      11: Weight            a gapfor
                                                  sizea of
                                                        gap3 mm.
                                                              size of 3 mm.
              Figurevs
  Figure 11: Weight   11time
                         : Weight
                              for a vs
                                     gaptimesizefor
                                                  of a3 gap
                                                         mm.size of 3 mm.
                                                                                                  3.1 Element
                                                                                                           The Chrono   types ::Flex software is a general-purpose sim
                                                                                                                     Chrono
                                                                                          The Chrono       The::Flex software      ::Flexissoftware          is a general-purpose
                                                                                                                                                a general-purpose           simulator sim
              2.4.4 Results                                                                       Chrono   for
                                                                                                            ::Flexthree      dimensional
                                                                                                                      includes      two    elementflexible
                                                                                                                                                      types    multi-body
                                                                                                                                                              implemented       problems an
                                                                                                                                                                               us-          an
                                                                                                           for three dimensional
                                                                                          for three dimensional                flexible multi-bodyflexible multi-body
                                                                                                                                                               problems and     problems
                                                                                                                                                                                    pro-
                                                                                                  ing the vides
                                                                                                                      aa2001;
                                                                                                                          suite     of Coordinate
                                                                                                                                        flexible bodybody     support.(ANCF)
                                                                                                                                                                          The features
                                                                                                                                                                                  features in
       tion   coefficient     ofof   glass    was     an                                                     Absolute        Nodal                      Formulation
              Theglass
                    weightwas
              coefficient
        tion of
oefficient                      ofthe  collected
                                     glass
                                    an        wasgranular
                                         unknown      aninunknown
                                                                material
                                                           unknown
                                                             the
                                                                           inplotted
                                                                           is
                                                                          in
                                                                   validation   the  validation
                                                                                the validation
                                                                                       ver-        a suitevides
                                                                                          vides(Berzeri                   suite
                                                                                                              ofal.,flexible
                                                                                                             et
                                                                                                                                   of
                                                                                                                                  body
                                                                                                                                von
                                                                                                                                        flexible
                                                                                                                                             support. 2002).
                                                                                                                                      Dombrowski,          Thesupport.
                                                                                                                                                                 features
                                                                                                                                                                  The
                                                                                                                                                                          Theincluded inc
                                                                                                                                                                      gradient-
       process     and     needed
                              variousto                                                                    in this
                                                                                                                this module
                                                                                                                         module are   are multiple
                                                                                                                                              multiple element
                                                                                                                                                           element types,
                                                                                                                                                                      types, the the ability
                                                                                                                                                                                      ability t
                                       to be     determined        beforeFig.   further
              sus time    for           gap sizes    in Fig. 11 through           14 usingobser-           in
s andprocess
          needed   and
                    to be  needed
                               determined   be   determined
                                                  before in        before
                                                             further     obser- further   in
                                                                                          obser-    module
                                                                                             thisdeficient    beam       multiple
                                                                                                                  are element        andelement        types, the ability
                                                                                                                                            the gradient-deficient    plate ele-to con-
       vationsthe  friction
                  could      becoefficient
                                  done.      determined
                                            To   achieve         Fig.  10.  For   each
                                                                             experiment
                                                                      one experiment
                                                              this, one                 ex-       a arenect
                                                                                              at these     nect      these      elements         with     a  variety   of   bilateral    cons
s could vations   couldTothe
           be periment,
               done.         beachieve
                                  done.from
                                 result     To
                                            this,achieve
                                                the one       this,
                                                           experiment
                                                     simulation    in Chrono      a
                                                                              at ::Engine,nectat ament       lements thesewith
                                                                                                              described         elements
                                                                                                                              below.   a variety                            bilateral const
                                                                                                                                                            variety ofconstraints,
                                                                                                                                                withofa bilateral
       gap   size   of  1.5    mm     was    performed         and   multiple      simulations             multiple solvers,
                                                                                                           multiple          solvers, and contact   contact with with friction.
                                                                                                                                                                        friction. Additio
                                                                                                                                                                                       Additi
        gap mm
ze of 1.5    size
              shown ofby
                   was   1.5themmsolidwas
                           performed         performed
                                       line,and    multiple
                                              is overlaid   onand
                                                                top  multiple
                                                                 simulations
                                                                     of the standard      multiple solvers,
                                                                                   simulations
                                                                                        de-                              and contactand        with friction.         Additionally,
       with   the                                                                                          Chrono          ::Flex leverages
                                                                                                                                       leverages        the GPU
                                                                                                                                                              GPU to to accelerate
                                                                                                                                                                          accelerate solu
he same        the same
              viation
        withsetup   same
                     andof thesetup
                               setup
                             different
                                        and
                                  experimental
                                        and    different      friction
                                                   runs,coefficients
                                               different
                                            friction       shown   by the
                                                              friction    coefficients
                                                                              dashed line.
                                                                          coefficients
                                                                            were
                                                                                            were3.1.1::Flex
                                                                                          Chrono
                                                                                            were           Chrono
                                                                                                           Gradient-deficient
                                                                                                                  leverages::Flex    thebeam GPU     tothe
                                                                                                                                                 elements accelerate     solution ofsolut
       performed.
              Note that  Thethe simulation
                                  simulated resultresults    were compared
                                                        lies within   compared       to the    ex-problems.large      problems.
med. performed.
        The simulation   The     simulation
                                results    wereresults
                                                    compared were   toa the
                                                                         single standard
                                                                               ex- to the largeex-         large problems.
                                                                                                  This implementation           uses gradient deficient ANCF beam ele-
              deviation
       perimental      testof results
                               the experimental
                                          to          data. which friction coefficient
                                              determine
        perimental      test   results    to  determine
 ntal test results to determine which friction coefficient    which     friction    coefficient   ments   to  model      slender    beams, examples of which are shown
       resulted
        resulted   in  the   best
                   in the best      match,
                                     match,     see   Fig.   10.  It  was    determined       thatin Fig.  15.    These      are  two    node elements with one position
 d in the  best match,        see Fig.     10. see    Fig.determined
                                                 It was      10. It was determined
                                                                              that           that
       µµ = 0.15   most      closely     matched       the   experimental         results.   This vector   3.1
                                                                                                           and    onlyElement
                                                                                                                           one        Types
                                                                                                                                 gradient     vector used as nodal coordi-
 5 most=closely
              3 Chrono::Flex
            0.15    most
                      matchedclosely thematched
                                           experimentalthe experimental
                                                                results. Thisresults.3.1     ThisElement
                                                                                                  nates.
                                                                                                           3.1 Types
                                                                                                          Each
                                                                                                                      Element Types
                                                                                                                   node     thus   has    6  coordinates:    three components
       value
        value   was
                was   used
                      used     for
                               for   all  subsequent
                                     all software
                                          subsequent        simulations.
was used    for
              TheallChrono
                      subsequent::Flex    simulations.is a simulations.
                                                             general-purpose simula-              of the global position vector of the node and three compo-
                                                                                                           Chrono
                                                                                                         ofChrono          ::Flex
                                                                                                                           ::Flex     includes
                                                                                                                                      includes        two
                                                                                                                                                     two    element
                                                                                                                                                            element     types
                                                                                                                                                                   Thistypes      implemen
                                                                                                                                                                         formu-implement
              tor for three dimensional flexible multi-body problems and                  Chrono      ::Flex
                                                                                                  nents      the includes
                                                                                                                  position         two
                                                                                                                                vector     element
                                                                                                                                          gradient   at the node.
                                                                                                                                                         types   implemented         us-
              provides a suite of flexible body support. The features in-                         lation   ing the
                                                                                                          displays
                                                                                                           ing      thenoAbsolute
                                                                                                                            Absolute
                                                                                                                             shear locking    Nodal
                                                                                                                                                 problems
                                                                                                                                              Nodal       Coordinate
                                                                                                                                                              for thin and
                                                                                                                                                         Coordinate       Formulation
                                                                                                                                                                             stiff
                                                                                                                                                                          Formulation        (A
                                                                                          ing the      Absolute           Nodal       Coordinate          Formulation         (ANCF) (A
              cluded in this module are multiple element types, the abil-                         beams andBerzeri
                                                                                                                 is
                                                                                                           Berzeri         et al.
                                                                                                                     computationally
                                                                                                                          et von    (2001);
                                                                                                                              al. (2001);        von
                                                                                                                                              more      Dombrowski
                                                                                                                                                    efficient
                                                                                                                                                von Dombrowski compared    (2002).
                                                                                                                                                                           to  the
                                                                                                                                                                          (2002).      The  gr
                                                                                                                                                                                      The gra
              ity to connect these elements with a variety of bilateral con-
                                                                                          Berzeri     et al.  (2001);
                                                                                                  originaldeficient
                                                                                                             ANCF duebeam
                                                                                                                                     Dombrowski
                                                                                                                               to the element
                                                                                                                                         reduced number    (2002).   The
                                                                                                                                                               of nodal     gradient-
                                                                                                                                                                         coordi-
                                                                                                           deficient         beam                     and    the  gradient-deficient       pla
       2.4.4     Results
        2.4.4straints,
  Results         Resultsmultiple solvers, and contact with friction. Addition-           deficient
                                                                                                  natesbeam
                                                                                                         (Gerstmayrelement         andelement
                                                                                                                           and Shabana,    the2006). and    the gradient-deficient
                                                                                                                                                 gradient-deficient         plate ele- pla
                                                                                                                                                        The gradient deficient
                                                                                                           ment are
                                                                                                           ment       are described
                                                                                                                             described below.  below.
                                                                                          ment are described               below.
                www.mech-sci.net/4/49/2013/                                                                                               Mech. Sci., 4, 49–64, 2013
      The weight    of
                    of the  collected granular  material is
                                                          is plotted ver-
eight The
       of theweight    thegranular
               collected    collected granular
                                    material    material
                                             is plotted ver-plotted ver-    3.1.1 Gradient-Deficient
                                                                                   Gradient-Deficient Beam
                                                                                                      Beam Elements
      sus  time for various  gap sizes in Fig. 11 through  Fig. 14
                                                                143.1.1
                                                                   using Gradient-Deficient
                                                                            3.1.1           Beam Elements Elements
 e for sus timegap
       various  for various
                    sizes in gap
                             Fig.sizes in Fig. Fig.
                                  11 through   11 through  Fig.
                                                    14 using       using
      the friction coefficient determined in Fig. 10. For each ex-
58                      H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics




                                                                       Figure 16. Two models with friction and contact using
                                                                       Chrono::Flex plate elements: a cloth hanging on a sphere and a
                                                                       closed contour shaped like a tire.


Figure 14. Weight vs. time for a gap size of 1.5 mm. This was the
test case that was used for calibration.




                                                                       Figure 17. The equations of motion for Chrono::Flex.



                                                                       in a plane perpendicular to the axis of revolute joint. There
                                                                       are also additional constraints due to the element connectiv-
                                                                       ity in each beam. The element connectivity can be modeled
                                                                       as a fixed joint between the nodes. Here the common node
Figure 15. Two models with friction and contact using
                                                                       between two elements is treated as two different nodes at-
Chrono::Flex beam elements: a ball sitting on grass-like beams and
                                                                       tached to each other through the fixed joint. This fixed joint
a ball hitting a net.
                                                                       requires all the nodal coordinates of the two nodes be identi-
                                                                       cal. The generalized coordinates of the system change in time
ANCF beam element does not describe a rotation of the beam             under the effect of applied forces such that these constraint
about its own axis so the torsional effects cannot be modeled.         equations are satisfied at all times. The time evolution of the
                                                                       system is governed by the Lagrange multiplier form of the
                                                                       constrained equations of motion.
3.1.2    Gradient-deficient plate elements
Much like beams, numerical difficulties are encountered in             3.3   Solvers
the fully parameterized plate element when the system has
very thin and stiff components (Dufva and Shabana, 2005).              The equations shown in Fig. 17 form a system of index-3 Dif-
The high frequencies that are induced along the thin direction         ferential Algebraic Equations (DAEs). Although several low
of the element require an extremely small time step, resulting         order numerical integration schemes have been effectively
in longer simulation times. In the case where the aspect ratio         used to solve index-3 DAEs, Chrono::Flex utilizes the New-
(length divided by thickness) of the element is high, plane            mark integration scheme (Hussein et al., 2008). Originally
stress assumptions can be made that allow a reduced-order              used in the structural dynamics community for the numeri-
element to be accurate. Specifically, Kirchhoff’s plate theory,        cal integration of a linear set of second order ODEs, it was
which does not account for shear deformation, is used and              adapted for the discretization of DAEs. This implicit solver
results in an element with 36 degrees of freedom, or nodal             was proved to have convergence of order 1 or 2, depending
coordinates, are shown in Fig. 16.                                     on the choice of parameters γ and β.
                                                                          At each time step, the numerical solution commences by
                                                                       solving the nonlinear set of equations shown in Fig. 18. The
3.2     Kinematic constraints
                                                                       numerical solution of the nonlinear algebraic system falls
Several types of mechanical joints are modeled in                      back on a Newton-type iterative algorithm that requires the
Chrono::Flex. A spherical joint (Shabana, 2005) between                computation of its sensitivity matrix. Advancing the numer-
two nodes of any two bodies will require the position vec-             ical solution in time draws on three loops: the outer-most
tor of each node to be identical. A revolute joint will have           loop marches forward in time, while at each time step the
two additional constraints to the spherical joint constraints.         second loop solves the algebraic discretization problem in
In this case, the gradient vectors of the two nodes will remain        Fig. 18. Each iteration in this second loop launches a third

Mech. Sci., 4, 49–64, 2013                                                                              www.mech-sci.net/4/49/2013/
                                                                    dva             pb   pa           (µa + µb )rab .∇a Wab 
CUDA. Chrono::Flex was validated in Khude et al. (2011)                 = − mb ( 2 + 2 )∇a Wab −                             vab  + fa
                                                                     dt               ρa   ρb             ρ̄2ab (rab
                                                                                                                  2
                                                                                                                     + εh̄2ab )
as well as in (Melanz, 2012) against the commercial code                      b
ADAMS (MSC.Software, 2012), and the nonlinear finite el-                                                                           (2)
H. Mazhar  et al.: Chrono: a parallel multi-physics
ement analysis code ABAQUS (ABAQUS, 2004).          library for rigid-body, flexible-body, and fluid dynamics                     59
                                                                    which are solved in conjunction with

                                                                          the fluid flow using SPH are expressed as
                                                                                                              dx/dt = v                                (3)
                                                                          dρa         X mb
                                                                                = ρa             (va − vb ) .∇a Wab                                   (1)
                                                                          todtupdate theb
                                                                                             ρfluid
                                                                                               b     properties. In Eqs. (1) to (3), ρ, v, and p
                                                                          are local fluid density, velocity, and pressure, respectively, m
                                                                          is the representative fluid mass assigned to the SPH marker,
                                                                          dva
                                                                          W is= a kernel function which smooths out the local fluid
                                                                           dt
                                                                          properties
                                                                             X  pwithin          a resolution length l = κh, andrab is the
                                                                                           b     pa two fluid (µ    a +µb )rabdenoted
                                                                                                                               .∇a Wab by a and b.
                                                                                mb ( 2 + 2 )∇a Wab − markers
                                                                          distance
                                                                          −           between                                           vab + fa (2)
                                                                                        ρ        ρ                 ρ̄  2 (r 2 +εh̄2 )
                                                                                     
Figure 18
Figure   18.: The discretized equations of
                                        of motion
                                           motion for
                                                  for Chrono::Flex
                                                      Chrono::Flex        Fluid
                                                                              b flow evolution
                                                                                          a       b     equations,abdefinedab    byab Eqs. (1) to (3),
(fully implicit).                                                         are solved explicitly, where pressure is related to density via
                                                                          which are solved in conjunction with
                                                                          an appropriate state equation to maintain the compressibility
                                                                          below= 1%.
                                                                          dx/dt     v        To increase the accuracy and stability of (3)             the
loop whose role is that of producing a vector of correc-                  simulation, an XSPH modification (Monaghan, 1989) and
 4 Chrono::Fluid
tions  for the acceleration and Lagrange multipliers. The cor-            Shephard
                                                                          to update the  filtering    (Dalrymple
                                                                                            fluid properties.          and(1)Rogers,
                                                                                                                 In Eqs.        to (3), ρ,2006)
                                                                                                                                           v, and pwere
                                                                                                                                                      are
rections are computed using the BiCGStab iterative solver                 applied.
                                                                          local fluid density, velocity, and pressure, respectively, m is
(Yang   and Brent,
 The Chrono          2002),
                ::Fluid       which also
                          component        provides
                                        aims           for a matrix-
                                               at leveraging    GPU       the representative fluid mass assigned to the SPH marker, W
free  solution.   A serial   solver  was  implemented
 computing to efficiently simulate fluid dynamics          using and
                                                                   the
                                                                          is a kernel function which smooths out the local fluid proper-
Armadillo    Matrix   Algebra     Library (Sanderson,     2010)   and
 fluid-solid interaction problems. Fluid-Solid Interaction                ties within a resolution length l = κh, and rab is the distance
a(FSI)
   GPUcovers
         parallel  solverrange
                           was ofimplemented     using
                                                    fromCUSP
                                                           blood(Bell     4.1 FSItwo   withfluid
                                                                                               Smoothed
                a wide              applications,                 and     between                    markersParticle
                                                                                                                denoted  Hydrodynamics:
                                                                                                                            by a and b. Fluid   A Quick
                                                                                                                                                    flow
and   Garland,  2012),  a  linear  algebra  library
 polymer flow to tanker trucks and ships. Simulation built on top   of
                                                               of the            Overview
                                                                          evolution equations, defined by Eqs. (1) to (3), are solved
CUDA.     Chrono::Flex was validated in Khude et al. (2011)
 FSI problem requires two components: Fluid and Solid                     explicitly, where pressure is related to density via an appro-
as   well as in Melanz
 simulations.              (2012)
                  Simulation        against
                                of the  Solidthephase,
                                                  commercial
                                                         either code
                                                                 rigid    A proper
                                                                          priate  statechoice
                                                                                          equation of fluid-solid
                                                                                                        to maintaincoupling        should satisfy
                                                                                                                       the compressibility        belowthe
ADAMS
 or flexible, in an HPC fashion, is described in finite
            (MSC.Software,     2012),  and  the nonlinear           el-
                                                             previous     no-slip   and    impenetrability      conditions     on   the  surface   of  the
                                                                          1 %. To increase the accuracy and stability of the simulation,
ement   analysis  code  ABAQUS       (ABAQUS,      2004).
 sections. To leverage the existing solid phase simulation,               solid  obstacles.        By attaching     Boundary
                                                                          an  XSPH     modification        (Monaghan,      1989)Condition
                                                                                                                                    and Shephard Enforc-
                                                                                                                                                      fil-
the fluid flow simulation should satisfy some conditions,                 ing  (BCE)      markers     on    the surface
                                                                          tering (Dalrymple and Rogers, 2006) were applied.of the   solid  objects,    the
4   Chrono::Fluid
introduced by the aforementioned target problems. First, the              local relative velocity, i.e. at the markers location, of the two
fluid flow may experience large domain deformation due                    phases will be zero (Fig. 19). The position and velocity of the
                                                                          4.1 FSI with Smoothed Particle Hydrodynamics:
The  Chrono
to the  motion ::Fluid component
                  of the            aims Second,
                          solid phase.    at leveraging  GPUphases
                                                    the two     com-      BCE amarkers         are updated according the motion of the solid
                                                                                    quick overview
puting
should tobeefficiently
             coupled viasimulate  fluid dynamics
                           an accurate    algorithm.and   fluid-solid
                                                        Third,  target    phase, which results in the propagation of the solid motion
interaction
problems may  problems.   Fluid-Solid
                   experience           Interaction
                                free surface         (FSI)
                                                as well  as covers
                                                             internala    A   proper
                                                                          to the  fluidchoice
                                                                                          domain.  of On    the othercoupling
                                                                                                       fluid-solid     hand, theshould      satisfy
                                                                                                                                     interaction      the
                                                                                                                                                   forces
flow. range
wide          of the
       Finally,   applications, from blood
                      whole simulation         and be
                                          should   polymer
                                                      capable flow  to
                                                                 of an    no-slip
                                                                          on the BCEand impenetrability
                                                                                           markers are used     conditions
                                                                                                                  to calculate on the total
                                                                                                                                        surface       the
                                                                                                                                                   of and
                                                                                                                                               force
tanker  trucks and ships.
HPC implementation           Simulation
                         to maintain   the of  the FSI problem
                                            scalability            re-
                                                        of the code.      solid
                                                                          torqueobstacles.
                                                                                   exerted by    Bythe
                                                                                                     attaching
                                                                                                         fluid onBoundary      Condition Enforcing
                                                                                                                  the solid object.
quires two components: Fluid and Solid simulations. Simu-                 (BCE) markers on the surface of the solid objects, the lo-
lation of the Solid phase, either rigid or flexible, in an HPC            cal relative velocity, i.e., at the markers location, of the two
Mech. Sci.
fashion,  is described in previous sections. To leverage the ex-                                                                  www.mech-sci.net
                                                                          phases will be zero (see Fig. 19). The position and veloc-
isting solid phase simulation, the fluid flow simulation should           ity of the BCE markers are updated according the motion of
satisfy some conditions, introduced by the aforementioned                 the solid phase, which results in the propagation of the solid
target problems. First, the fluid flow may experience large               motion to the fluid domain. On the other hand, the interac-
domain deformation due to the motion of the solid phase.                  tion forces on the BCE markers are used to calculate the total
Second, the two phases should be coupled via an accurate al-              force and torque exerted by the fluid on the solid object.
gorithm. Third, target problems may experience free surface
as well as internal flow. Finally, the whole simulation should
                                                                          4.1.1     FSI with Smoothed Particle Hydrodynamics:
be capable of an HPC implementation to maintain the scala-
                                                                                    proximity computation
bility of the code.
   Fluid flow can be simulated in either an Eulerian or a La-             The overall simulation of the FSI framework is performed in
grangian framework. Provided that the interfacial forces are              parallel, where each thread handles the force calculation of
captured thoroughly, the Lagrangian framework is capable of               a fluid or BCE marker first, and a rigid body later. Next, the
tracking the domain deformation introduced by the motion                  parallel threads perform the kinematics update of the fluid
of the solid phase at almost no extra cost. Smoothed Particle             markers, rigid bodies, and BCE markers, respectively. An
Hydrodynamics (SPH) (Lucy, 1977; Gingold and Monaghan,                    essential part of the force calculation stage is the proximity
1977; Monaghan, 2005), its modifications (Monaghan, 1989;                 computation, which will be explained briefly herein.
Dilts, 1999), and variations (Koshizuka et al., 1998) have                   Proximity computation used in our work leverages the
been widely used for the simulation of the fluid domain in                algorithm provided in CUDA SDK (NVIDIA Corporation,
a Lagrangian framework. The main evolution equations of                   2012), where the computation domain is divided into bins

www.mech-sci.net/4/49/2013/                                                                                         Mech. Sci., 4, 49–64, 2013
60                  H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics




                                                                        12                Mazhar et al.: Chrono: A Parallel Multi-Physics Librar

                                                                        5.1    On the Choice of RenderMan                                          render
                                                                                                                                                   Figure
                                                                        Using RenderMan for rendering is motivated by the scope of
                                                                        arbitrary data sets and the potentially immense scene com-
                                                                        plexity that results from big data; REYES, the underlying
                                                                        architecture for RenderMan is ideally suited for this task.
                                                                        REYES works by dividing each surface in the scene into a
                                                                        grid of micropolygons and shades at the grid vertices (Cook
                                                                        Figure   21. Chrono
                                                                        et al., 1987)       ::Render22).
                                                                                      (see Figure    architecture.


Figure 19. Coupling of the fluid and solid phases. BCE and fluid
markers are represented by black and white circles, respectively.

                                                                                                                                                   The X
                                                                                                                                                   salient
                                                                                                                                                   in Figu
                                                                                                                                                   line fr
                                                                                                                                                   Rende



                                                                        Figure 22. An overview
                                                                                Figure         of the REYES
                                                                                       22: An overview  of thePipeline.
                                                                                                               REYES Pipeline.

                                                                        This results
                                                                        particles,  doesinnot
                                                                                           tractable   rendering
                                                                                               affect the           for time.
                                                                                                           simulation    complex  scenes the
                                                                                                                              Therefore,   be-
                                                                        cause:  (a)   only  a small   portion   of the  scene needs
                                                                        simulation of a highly dense suspension is possible. Figure   to be in
Figure 20. Simulation of rigid bodies inside a fluid flow: rigid el-    memory     at any  given  time;  (b)  grid-based   computation   leads
                                                                        20 shows the result of the simulation of the flow of suspen-
lipsoids with their BCE markers are shown in the left image while       to optimal    memory
the fluid’s velocity contours and rigid ellipsoids at the mid-section
                                                                        sion including    1500 access     patterns;
                                                                                                  particles  through(c)   non-visible
                                                                                                                       a channel.      objects
                                                                                                                                   A similar
                                                                        need  not  be  loaded   into  memory;     (d) fully-rendered
                                                                        scenario with 13 000 particles in suspension was simulated     objects
of the channel are shown in the right image.                            canChrono
                                                                            be removed
                                                                        in          ::Fluid.from memory; and (e) objects are tessellated
                                                                        according to size on the screen; less complex geometry is
                                                                        dynamically loaded whenever possible.
whose sizes are the same as the resolution length of the SPH            5     Chrono::Render
kernel function. A hash value is assigned to each marker                REYES is perfectly suited for parallel processing since it
based on its location with respect to the bins. Markers are             Chrono   ::Renderwith
                                                                        scales linearly      is a the
                                                                                                   software
                                                                                                       numberpackage    that Considering
                                                                                                                of cores.    enables simple,that
                                                                                                                                                   Figure
sorted based on their hash value. The sorted properties are             streamlined,    and   fast  visualization   of  arbitrary
                                                                        REYES needs only a handful of relevant scene elements      data usingat
                                                                                                                                                   ment sh
stored in independent arrays to improve the memory access               Pixar’s
                                                                        a time, RenderMan
                                                                                  this data can (Pixar,  1988, 1989,
                                                                                                    be parsed           2000, 2005). Specif-
                                                                                                                 into low-memory       buckets
and cache coherency. To compute the forces on a marker, the             ically, Chrono   ::Render    contains a  hybrid
                                                                        and distributed amongst cores for parallel       of processing
                                                                                                                              rendering;bina-
                                                                                                                                           thus
lists of the possible interacting markers inside its bin and all        ries and Python
                                                                        REYES’             scripting modulesand
                                                                                    low memory-footprint         thatefficient
                                                                                                                       seek to concurrent
                                                                                                                                abstract awayre-   Althou
26 neighbor bins are called. The hash values of the bins are            the complexities
                                                                        source   usage for of
                                                                                            therendering
                                                                                                 complex with
                                                                                                           scenesRenderMan.     Additionally,
                                                                                                                    makes it a great  renderer     is ofte
used to access the relevant segments of the sorted data.                Chrono   ::Render is targeted for
                                                                        for a distributed-computing          providing rendering as an au-
                                                                                                          platform.                                not ha
                                                                        tomated post-processing step in a remote simulation pipeline,              genera
                                                                        hence it is controlled via a succinct XML specification for                able si
4.2   Validation and demonstration of technology                        “gluing”   together rendering     with arbitrary  processes. As seen
                                                                        5.2 Accessibility       of High-Quality    Graphics                        genera
The aforementioned FSI simulation engine was used to val-               in Fig. 21, Chrono::Render combines simulation data, XML                   runtim
idate the lateral migration of cylindrical particles in plane           describing
                                                                        Although REYEShow tocan usemanage
                                                                                                      the data,
                                                                                                             theand
                                                                                                                  issueoptional
                                                                                                                        of sceneuser-defined
                                                                                                                                  complexity,      dering
Poiseuille flow, spherical particles in pipe flow, and parti-           Python   scripts  into  a complex,   visually-rich
                                                                        leveraging this power is difficult without computer  scene to begraph-
                                                                                                                                          ren-     ing fo
cle distribution in Poiseuille flow of suspension (Pazouki and          dered   by RenderMan.
                                                                        ics expertise. The guiding principle of Chrono::Render                     ing of
Negrut, 2012,?). Due to the scalability of Chrono::Fluid in             is to make high-quality rendering available to researchers,                for defi
both fluid and solid phases, increasing the number of rigid             most of whom don’t have the background or bandwidth to                     modul
bodies, which translates into decreasing the number of fluid            spend time learning how to use complex graphics applica-                   gramm
                                                                        tions or make sense of REYES’ intricacies. Consequently,                   Chron
                                                                        Chrono::Render encapsulates into the XML specification                     classes
Mech. Sci., 4, 49–64, 2013                                                                           www.mech-sci.net/4/49/2013/
                                                                        the complicated steps needed to make interesting visual ef-                ing use
                                                                        fects, such as multipass rendering. The user must only in-                 ure 25
                                                                        stance the correct XML components to achieve high-quality                  scripts
 ing
ask.             Figure 23.
 oa
 e of
ook         H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics                              61

om-
ying          Figure 23: Chrono::Render execution workflow.
ask.
to a The XML specification allows for the concise expression of
 ook salient features and scene objects. For example, the snippet
     in Figure 24 illustrates the XML file that translates a single
          line from a comma-separated value (CSV) data file into a
          RenderMan sphere using two shaders.
            Figure 23. Chrono::Render execution workflow.

                                  Figure 23: Chrono::Render execution workflow.
                                                                                     source usage for the complex scenes makes it a great renderer
                                                                                     for a distributed-computing platform.

 be-                                                                                 5.2    Accessibility of high-quality graphics
e in             The XML specification allows for        the concise expression of
                                                 Although REYES can manage the issue of scene complex-
 ads
ects             salient features and scene objects.      For this
                                                 ity, leveraging example,
                                                                      power is difficultthe   snippet
                                                                                         without computer graph-
                                                 ics expertise. The guiding principle of Chrono::Render is to
ects             in Figure 24 illustrates the XMLmakefile     that rendering
                                                         high-quality   translates           a researchers,
                                                                                  available to   single most
 ted                                             of whom do not have the background or bandwidth to
y is             line from a comma-separated value
                                                 spend time (CSV)
                                                              learning how data          file graphics
                                                                             to use complex      into applica-
                                                                                                         a
                                                 tions or make sense of REYES’ intricacies. Consequently,
                 RenderMan sphere using two shaders.
                                                 Chrono::Render encapsulates into the XML specification the
                                                                                         complicated steps needed to make interesting visual effects,
e it        Figure 24. Simple XML for a sphere with a Surface and Displace-
                                                                                         such as multipass rendering. The user must only instance the
 hat        ment shader.
          Figure 24: Simple XML for a sphere with a Surface and Displace-                correct XML components to achieve high-quality renders.
s at      ment shader.                                                                   The program flow of Chrono::Render is shown in Fig. 23.
kets        5.1 On the choice of RenderMan                                                  The XML specification allows for the concise expression
                                                                                         of salient features and scene objects. For example, the snip-
hus         Using RenderMan for rendering is motivated by the scope of                   pet in Fig. 24 illustrates the XML file that translates a single
 re-      Although
            arbitrary datasimple,     thethe
                               sets and    render     is visually
                                              potentially    immense  rich.
                                                                         sceneThis
                                                                                com-description
                                                                                         line from a comma-separated value (CSV) data file into a
erer      isplexity
              often that    resultsto
                        enough        from   big data;most
                                         visualize        REYES,     the underlying
                                                                 generic    data, but itRenderMan
                                                                                            can-       sphere using two shaders.
            architecture     for  RenderMan      is ideally    suited  for
          not handle all arbitrary visualizations, so in order to maintain this task.       Although   simple, the render is visually rich. This descrip-
   be-      REYES works by dividing each surface in the scene into a
          generality       we make use
            grid of micropolygons        and of   Python
                                              shades    at thescripts    and wrappers
                                                                grid vertices  (Cook
                                                                                         tion is often enough to visualize most generic data, but it can-
                                                                                          to en-
                                                                                         not  handle all arbitrary visualizations, so in order to maintain
          able    simplified       procedural       RenderMan Interface Bytestream
e in        et al., 1987) (see Fig.
          generation.
               This resultsAny
                                        22).
                                     XML rendering
                               in tractable   elementfor    can    be scripted
                                                                complex
                                                                                         generality we make use of Python scripts and wrappers to en-
                                                                                   such that
                                                                          scenes be-           at
                                                                                         able simplified   procedural RenderMan Interface Bytestream
eads        cause:    (a) only   a small  portion    of  the  scene
          runtime, the script output will be piped into the same ren-needs
            memory at any given time; (b) grid-based computation leads
                                                                             to be in    generation.   Any  XML element can be scripted such that at
                                                                                         runtime, the script output will be piped into the same ren-
  ity,    dering     context. This makes it possible to perform process-
 ects
 ph-
            to optimal memory access patterns; (c) non-visible objects
          ing
            need fornotspecialized
                         be loaded intodata     as well
                                           memory;            as modularize
                                                        (d) fully-rendered
                                                                                         dering context. This makes it possible to perform process-
                                                                                    the render-
                                                                              objects    ing for specialized data as well as modularize the render-
 ects
  der     ing
            canof bespecific
                     removed fromeffects.    Obviously
                                        memory;                this adds
                                                   and (e) objects          more complexity
                                                                      are tessellated    ing of specific effects. Obviously this adds more complexity
ers,        according     to  size  on  the  screen;   less  complex
          for defining the scene, but Chrono::Render provides Python    geometry    is   for defining the scene, but Chrono::Render provides Python
ated
h to        dynamically loaded whenever possible.
          modules with methods and classes intended to ease this pro-                    modules with methods and classes intended to ease this pro-
               REYES is perfectly suited for parallel processing since it                gramming as much as possible. Additionally, most of the
 yca-is   gramming
            scales linearly as with
                                much   theas  possible.
                                           number     of cores. Additionally,
                                                                   Considering thatmost of   the ::Render Python modules wrap C++ functions and
                                                                                         Chrono
 tly,       REYES ::Render
          Chrono        needs only Python
                                      a handfulmodules
                                                   of relevantwrapscene C++     functions
                                                                         elements  at        and with the purpose of exploiting speed while still mak-
                                                                                         classes
 ion        a  time,   this  data   can  be  parsed    into  low-memory
          classes with the purpose of exploiting speed while still mak-       buckets    ing  use of the syntactical/type-free simplicity of Python. Fig-
  ef-       and    distributed   amongst     cores  for   parallel  rendering;
          ing use of the syntactical/type-free simplicity of Python. Fig-        thus    ure  25 gives an example of combining XML with Python
            REYES’ low memory-footprint and efficient concurrent re-                     scripts to achieve a more complicated render.
ce it ure 25 gives an example of combining XML with Python
  in-
 lity scripts to achieve a more complicated render.
 that       www.mech-sci.net/4/49/2013/                                                                                  Mech. Sci., 4, 49–64, 2013
                 Figure 24: Simple XML for a sphere with a Surface and Displace-
 s at            ment shader.                                       www.mech-sci.net
62                H.Mazhar
                    Mazhar etet
                             al.:al.: Chrono
                                  Chrono:        :A
                                          a parallel   Parallel library
                                                     multi-physics Multi-Physics
                                                                        for rigid-body, Library     forandRigid-Body,
                                                                                        flexible-body,     fluid dynamics Flexible


                                                                                                                       of arbitrary sim
                                                                                                                       ponents. These
                                                                                                                       age high-perform
                                                                                                                       sible. Chrono:
                                                                                                                       a domain-decom
                                                                                                                       Chrono::Flex, a
                                                                                                                       lelism to further
                                                                                                                       While these com
                                                                                                                       ties on their own
                                                                                                                       various Chrono


                                                                                                                       6.1      Chrono A
Figure 25. General purpose rendering with Chrono::Render. The Rover body contains multiple shape descriptions of which are generated
from a Python script. Figure     25:with
                      Data is tagged General     purpose
                                         a name which         rendering
                                                      can be later be accessedwith
                                                                               using Chrono    ::Render.
                                                                                     some of Chrono ::Render’sThe
                                                                                                              Python functionality.
                  Rover body contains multiple shape descriptions of which are gen-
                  erated from a Python script. Data isnally,  tagged     with  a name    which   can
                                                                                                            Major releases o
5.3 Other capabilities                                            Chrono    ::Render provides high-quality visualization
                  be later be accessed using some of Chrono of arbitrary::Render’s   Python
                                                                          simulation data fromfunc-
                                                                                                            from the Chron
                                                                                                the other Chrono com-
Beyond interpreting parameters and data into RenderMan                                                      info.    Chrono in
                  tionality.                                ponents. These components have been designed       to lever-
calls, Chrono::Render provides tools for bootstrapping ren-
                                                                     age high-performance computing hardware whenever                pos-
                                                                                                                            sbel.wisc.edu/ch
dering projects. Chrono::Render can: (a) construct direc-
                                                                     sible. Chrono::Engine supports CPU parallelism through
tory structures for localizing and managing scene resources;                                                                build     status for v
                                                                     a domain-decomposition approach, while Chrono             ::Engine,
(b) automate distribution of rendering across a multi-node
                                                                     Chrono::Flex, and Chrono::Fluid all support GPU paral-
network; (c) convert5.3common  Other
                                 graphics Capabilities
                                            file formats into Ren-
                                                                     lelism to further improve simulation performance.
derMan file formats such as Wavefront Objs and Mtls to Ren-
                                                                        While these components provide useful simulation capa-
derMan RIBs and Shaders; (d) generate XML for automati-
                                                                     bilities on their own, ongoing work seeks to further       integrate
                                                                                                                            Acknowledgme
                     Beyond
cally adding parameters             interpreting
                           to the scene   description forparameters
                                                          describ-
                                                                     theand
                                                                         variousdata
                                                                                  Chrono into    RenderMan
                                                                                            components.
ing advanced visual effects such as subsurface scattering,
ambient occlusion, calls,           etc.; (e)::Render
                               Chrono
                      reflections,                          provides tools for bootstrapping ren-
                                               mesh point-clouds,
particularly useful dering                                           Chrono availability
                                 projects.
                     for particle-based            Chronoand
                                           fluid simulations;  ::Render    can: (a) construct direc-                        Financial support
(f) dump the generated RenderMan calls to disk for reuse.            Major   releases of scene
                                                                                          the Chrono  ::Engine software are available
                     tory    structures        for   localizing
   Chrono:Render is currently available for free download
                                                                   and  managing                    resources;              by the National Sc
                                                                     from the Chrono::Engine website at http://chronoengine.
as a pre-built binary(b)forautomate
                             Linux. Members  distribution       of rendering
                                                   of the Wiscon-    info. Chronoacross        a multi-node
                                                                                     in its entirety can be downloaded from search     Office W91
                                                                                                                                   http://
sin Applied Computing Center can use this capability re-
                     network; (c) convert common graphics file formats into Ren-
motely as a service by leveraging 320 AMD cores on which
                                                                     sbel.wisc.edu/chrono.    The  latter site also displays the  nightly
                                                                                                                            was provided in pa
                                                                     build status for various platforms and unit testing results.
                     derMan        file
Chrono::Render is currently deployed.    formats       such   as Wavefront       Objs    and    Mtls    to   Ren-           PRIN grant 2007Z
                   derMan RIBs and Shaders; (d) generate XML for automati-                                           soring our researc
                                                               Acknowledgements. Financial support for the Wisconsin
6    Conclusions and future work
                   cally adding parameters to the scene                 description
                                                               authors was                 forby describ-
                                                                             provided in part    the National Scienceputing.
                                                                                                                      Foundation
                                                               Award 0840442 and Army Research Office W911NF-12-1-0395.
                   ing advanced
The Chrono simulation                  visual effects
                          package is composed             such Financial
                                                  of a col-     as subsurface         scattering, am-
                                                                         support for A.Tasora was provided in part by the Italian
lection of components designed to perform multi-physics
                   bient occlusion, reflections, etc.;Ministry
simulations leveraging emerging high-performance comput-
                                                                 (e) mesh        point-clouds,
                                                                         of Education   under the PRINpar-
                                                                                                         grant 2007Z7K4ZB. We
                                                               thank NVIDIA and AMD for sponsoring our research programs in
                   ticularly
ing hardware. Chrono   ::Engine useful
                                 provides for  particle-based
                                          support  for rigid        fluid
                                                               the area      simulations;
                                                                        of high-performance       and ( f )
                                                                                              computing.             References
body dynamics, focusing   on large granular dynamics  prob-
                   dump the generated RenderMan calls to disk for reuse.
lems, Chrono::Flex enables simulation of flexible beam     Edited by: A. Müller    ABAQUS: User
and plate elements interacting through contact and bilat-  Reviewed by: two anonymous referees
                    Chrono
eral constraints, while         :Render is currently available for free download as
                          Chrono:Fluid allows the simula-                              Sorensen, Inc.,
tion of fluid flows andpre-built      binary problems.
                        fluid-solid interaction for Linux.
                                                       Fi-   Members of the Wiscon- Anitescu, M. and
                  sin Applied Computing Center can use this capability re-             complementarit
Mech. Sci., 4, 49–64, 2013                                         www.mech-sci.net/4/49/2013/
                                                                                       tional Optimiza
                  motely as a service by leveraging 320 AMD cores on which
                  Chrono::Render is currently deployed.                                s10589-008-92
                                                                                    Bell, N. and Gar
H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics                              63

References                                                              Lucy, L.: A numerical approach to the testing of the fission hypoth-
                                                                           esis, Astron. J., 82, 1013–1024, 1977.
ABAQUS: User Manual – Version 6.5, Hibbitt, Karlsson and                Mazhar, H., Heyn, T., and Negrut, D.: A scalable parallel method
  Sorensen, Inc., Pawtucket, RI, 2004.                                     for large collision detection problems, Multibody Syst. Dyn., 26,
Anitescu, M. and Tasora, A.: An iterative approach for cone com-           37–55, doi:10.1007/s11044-011-9246-y, 2011.
  plementarity problems for nonsmooth dynamics, Comput. Op-             Melanz, D.: On the Validation and Applications of a Parallel Flex-
  tim. Appl., 47, 207–235, doi:10.1007/s10589-008-9223-4, 2010.            ible Multi-body Dynamics Implementation, M.S. thesis, Univer-
Bell, N. and Garland, M.: CUSP: Generic Parallel Algorithms                sity of Wisconsin-Madison, 2012.
  for Sparse Matrix and Graph Computations, http://cusp-library.        Melanz, D., Tupy, M., Smith, B., Turner, K., and Negrut, D.: On the
  googlecode.com, version 0.3.0, 2012.                                     Validation of a Differential Variational Inequality Approach for
Berzeri, M., Campanelli, M., and Shabana, A. A.: Definition of the         the Dynamics of Granular Material-DETC2010-28804, in: Pro-
  Elastic Forces in the Finite-Element Absolute Nodal Coordinate           ceedings to the 30th Computers and Information in Engineer-
  Formulation and the Floating Frame of Reference Formulation,             ing Conference, edited by: Fukuda, S. and Michopoulos, J. G.,
  Multibody Syst. Dyn., 5, 21–54, 2001.                                    ASME International Design Engineering Technical Conferences
Cook, R. L., Carpenter, L., and Catmull, E.: The Reyes Image               (IDETC) and Computers and Information in Engineering Con-
  Rendering Architecture, SIGGRAPH 1987 Proceedings, 95–102,               ference (CIE), 2010.
  1987.                                                                 Mindlin, R. and Deresiewicz, H.: Elastic spheres in contact under
Cundall, P.: A computer model for simulating progressive large-            varying oblique forces, J. Appl. Mech., 20, 327–344, 1953.
  scale movements in block rock mechanics, in: Proceedings of the       Monaghan, J.: On the problem of penetration in particle methods, J.
  International Symposium on Rock Mechanics, Nancy, France,                Comput. Phys., 82, 1–15, 1989.
  1971.                                                                 Monaghan, J.: Smoothed particle hydrodynamics, Rep. Prog. Phys.,
Cundall, P. and Strack, O.: A discrete element model for granular          68, 1703–1759, 2005.
  assemblies, Geotechnique, 29, 47–65, 1979.                            MSC.Software: ADAMS: Automatic Dynamic Analysis of Me-
Dalrymple, R. and Rogers, B.: Numerical modeling of water waves            chanical Systems, Ann Arbor, Michigan, 2012.
  with the SPH method, Coast. Eng., 53, 141–147, 2006.                  Negrut, D., Tasora, A., Mazhar, H., Heyn, T., and Hahn, P.: Leverag-
Dilts, G.: Moving-least-squares-particle hydrodynamics I. Consis-          ing parallel computing in multibody dynamics, Multibody Syst.
  tency and stability, Int. J. Numer. Meth. Eng., 44, 1115–1155,           Dyn., 27, 95–117, doi:10.1007/s11044-011-9262-y, 2012.
  1999.                                                                 NVIDIA Corporation: NVIDIA CUDA Developer Zone, available
Dufva, K. and Shabana, A.: Analysis of thin plate structures using         at: https://developer.nvidia.com/cuda-downloads, 2012.
  the absolute nodal coordinate formulation, P. I. Mech. Eng. K-J.      Pazouki, A. and Negrut, D.: Direct simulation of lateral migra-
  Mul., 219, 345–355, 2005.                                                tion of bouyant particles in channel flow using GPU computing,
Gerstmayr, J. and Shabana, A.: Analysis of thin beams and cables           in: Computers and Information in Engineering, CIE32, ASME,
  using the absolute nodal co-ordinate formulation, Nonlinear Dy-          Chicago, IL, USA, 2012a.
  nam., 45, 109–130, 2006.                                              Pazouki, A. and Negrut, D.: A numerical study of the effect of
Gingold, R. and Monaghan, J.: Smoothed particle hydrodynamics-             rigid body rotation, size, skewness, mutual distance, and colli-
  theory and application to non-spherical stars, Mon. Not. R. As-          sion on the radial distribution of suspensions in pipe flow, in re-
  tron. Soc., 181, 375–389, 1977.                                          view, 2013.
Gropp, W., Lusk, E., and Skjellum, A.: Using MPI: Portable Paral-       Pazouki, A., Mazhar, H., and Negrut, D.: Parallel Ellipsoid
  lel Programming with the Message-Passing Interface, 2nd Edn.,            Collision Detection with Application in Contact Dynamics-
  MIT Press, 1999.                                                         DETC2010-29073, in: Proceedings to the 30th Computers and
Heyn, T.: Simulation of Tracked Vehicles on Granular Terrain               Information in Engineering Conference, edited by: Fukuda, S.
  Leveraging GPUComputing, M.S. thesis, Department of Me-                  and Michopoulos, J. G., ASME International Design Engineer-
  chanical Engineering, University of Wisconsin-Madison, http:             ing Technical Conferences (IDETC) and Computers and Infor-
  //sbel.wisc.edu/documents/TobyHeynThesis final.pdf, 2009.                mation in Engineering Conference (CIE), 2010.
Hussein, B., Negrut, D., and Shabana, A.: Implicit and explicit inte-   Pazouki, A., Mazhar, H., and Negrut, D.: Parallel colli-
  gration in the solution of the absolute nodal coordinate differen-       sion detection of ellipsoids with applications in large scale
  tial/algebraic equations, Nonlinear Dynam., 54, 283–296, 2008.           multibody dynamics, Math. Comput. Simulat., 82, 879–894,
Khude, N., Melanz, D., Stanciulescu, I., and Negrut, D.: A Paral-          doi:10.1016/j.matcom.2011.11.005, 2012.
  lel GPU Implementation of the Absolute Nodal Coordinate For-          Pixar: The RenderMan Interface, Technical specification, Pixar,
  mulation With a Frictional/Contact Model for the Simulation of           1988, 1989, 2000, 2005.
  Large Flexible Body Systems, ASME Conference on Multibody             Sanderson, C.: Armadillo: An open source C++ linear algebra li-
  Systemss and Nonlinear Dynamics, 2011.                                   brary for fast prototyping and computationally intensive experi-
Koshizuka, S., Nobe, A., and Oka, Y.: Numerical analysis of break-         ments, Tech. rep., Technical report, NICTA, 2010.
  ing waves using the moving particle semi-implicit method, Int. J.     Shabana, A. A.: Dynamics of Multibody Systems, Cambridge Uni-
  Numer. Meth. Fl., 26, 751–769, 1998.                                     versity Press, 3rd Edn., 2005.
Kruggel-Emden, H., Simsek, E., Rickelt, S., Wirtz, S., and Scherer,     Snethen, G.: XenoCollide Website, http://www.xenocollide.com,
  V.: Review and extension of normal force models for the discrete         2007.
  element method, Powder Technol., 171, 157–173, 2007.                  Snethen, G.: XenoCollide: Complex Collision Made Simple, in:
                                                                           Game Programming Gems 7, edited by: Jacobs, S., Charles River



www.mech-sci.net/4/49/2013/                                                                                  Mech. Sci., 4, 49–64, 2013
64                 H. Mazhar et al.: Chrono: a parallel multi-physics library for rigid-body, flexible-body, and fluid dynamics

  Media, 165–178, 2008.                                              von Dombrowski, S.: Analysis of Large Flexible Body Deformation
Tasora, A. and Anitescu, M.: A convex complementarity approach         in Multibody Systems Using Absolute Coordinates, Multibody
  for simulating large granular flows, J. Comput. Nonlin. Dyn., 5,     Syst. Dyn., 8, 409–432, doi:10.1023/A:1021158911536, 2002.
  1–10, doi:10.1115/1.4001371, 2010.                                 Yang, L. and Brent, R.: The improved BiCGStab method for large
Tasora, A. and Anitescu, M.: A matrix-free cone comple-                and sparse unsymmetric linear systems on parallel distributed
  mentarity approach for solving large-scale, nonsmooth, rigid         memory architectures, in: Algorithms and Architectures for Par-
  body dynamics, Comput. Method. Appl. M., 200, 439–453,               allel Processing, 2002. Proceedings. Fifth International Confer-
  doi:10.1016/j.cma.2010.06.030, 2011.                                 ence on, IEEE, 324–328, 2002.
Tasora, A., Righettini, P., and Silvestri, M.: Architecture of the
  Chrono::Engine physics simulation middleware, in: Proceedings
  of ECCOMAS 2007 Multibody Conference, 2007.




Mech. Sci., 4, 49–64, 2013                                                                           www.mech-sci.net/4/49/2013/
