                                                  January 21, 2021 13:20 WSPC/INSTRUCTION FILE                       paper-1.8
arXiv:0803.3566v2 [physics.comp-ph] 18 Apr 2011




                                                             Generation of homogeneous granular packings: Contact dynamics
                                                             simulations at constant pressure using fully periodic boundaries



                                                                                                M. Reza Shaebani

                                                                   Institute for Advanced Studies in Basic Sciences, Zanjan 45195-1159, Iran


                                                          Department of Theoretical Physics, Budapest University of Technology and Economics, H-1111
                                                                                                Budapest, Hungary

                                                           Department of Theoretical Physics, University of Duisburg-Essen, 47048 Duisburg, Germany
                                                                                        shaebani@comphys.uni-duisburg.de


                                                                                                   Tamás Unger
                                                          Department of Theoretical Physics, Budapest University of Technology and Economics, H-1111
                                                                                                Budapest, Hungary


                                                             HAS-BME Condensed Matter Research Group, Budapest University of Technology and
                                                                                                    Economics


                                                                                                  János Kertész

                                                          Department of Theoretical Physics, Budapest University of Technology and Economics, H-1111
                                                                                                Budapest, Hungary


                                                             HAS-BME Condensed Matter Research Group, Budapest University of Technology and
                                                                                                    Economics



                                                             The contact dynamics method (CD) is an efficient simulation technique of dense granular
                                                             media where unilateral and frictional contact problems for a large number of rigid bodies
                                                             have to be solved. In this paper we present a modified version of the contact dynamics to
                                                             generate homogeneous random packings of rigid grains. CD simulations are performed
                                                             at constant external pressure, which allows the variation of the size of a periodically
                                                             repeated cell. We follow the concept of the Andersen dynamics and show how it can be
                                                             applied within the framework of the contact dynamics method. The main challenge here
                                                             is to handle the interparticle interactions properly, which are based on constraint forces
                                                             in CD. We implement the proposed algorithm, perform test simulations and investigate
                                                             the properties of the final packings.

                                                             Keywords: Granular material; Nonsmooth contact dynamics; Homogeneous compaction;
                                                             Jamming; Random granular packing; Constant pressure.

                                                             PACS Nos.: 45.70.-n, 45.70.Cc, 02.70.-c, 45.10.-b


                                                                                                         1
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                  paper-1.8




        2


        1. Introduction
        Computer simulation methods have been widely employed in recent years to study
        the behavior of granular materials. Among the numerical techniques, discrete ele-
        ment methods, including soft particle molecular dynamics (MD) 1,2 , event-driven
        (ED) 3,4 and contact dynamics (CD) 5,6,7,8 , constitute an important class where
        the material is simulated on the level of particles. In such algorithms the trajectory
        of each particle is calculated as a result of interaction with other particles, confining
        boundaries and external fields. The differences between the discrete element meth-
        ods stem from the way how interactions between the particles are treated, which
        leads also to different ranges of applicability.
             In low density granular systems, where interactions are mainly binary collisions,
        the event-driven method is an efficient technique. The particles are modeled as
        perfectly rigid and the contact duration is supposed to be zero. The handling of
        dense granular systems, where the frequency of collisions is large or long-lasting
        contacts appear, becomes problematic in ED simulations 9,10 .
             In case of dense granular media the approach of soft particle molecular dynamics
        is more favorable and widely used. In MD, the time step is usually fixed and the
        original undeformed shapes of the particles may overlap during the dynamics. These
        overlaps are interpreted as elastic deformations which generate repulsive restoring
        forces between the particles. Based on this interaction, which is defined in the form
        of a visco-elastic force law, the stiffness of the particles can be controlled. When the
        stiffness is increased MD simulations become slower since the time step has to be
        chosen small enough so that the velocities and positions vary as smooth functions
        of time.
             The contact dynamics method considers the grains as perfectly rigid. Therefore
        no overlaps between the particles are expected and they interact with each other
        only at contact points. The contact forces in CD do not stem from visco-elastic
        force laws but are calculated in terms of constraint conditions (for more details see
        Sec. 2). This method has shown its efficiency in the simulation of dense frictional
        systems of hard particles.
             Packings of hard particles interacting with repulsive contact forces are exten-
        sively used as models of various complex many-body systems, e.g. dense granu-
        lar materials 11 , glasses 12 , liquids 13 and other random media 14 . Jamming in
        hard-particle packings of granular materials has been the subject of considerable
        interest recently 15,16. Furthermore hard-particle packings, and especially hard-
        sphere packings, have inspired mathematicians and been the source of numerous
        challenging theoretical problems 17 , from which many are still open.
             Real systems in the laboratory and in nature contain far too large number of
        particles to model the whole system in computer simulations. Due to the limited
        computer capacity the simulations are often restricted to test a small mesoscopic
        part of a large system. Typically, the studies are focused to a local homogeneous
        small piece of the material inside the bulk far from the border of the system. There-
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                     paper-1.8




                                                                                              3


        fore simulation methods are required that are able to generate and handle packings
        of hard particles without side effects of confining walls.
            The usual simulation methods of dense systems involve confining boxes where
        the material is compactified by moving pistons or gravity. However, the properties
        of the material differ in the vicinity of walls and corners of the confining cell from
        those in the bulk far from the walls. The application of walls in computer simulations
        leads to inhomogeneous systems due to undesired side effects (e.g. layering effect).
        Moreover, the structure of the packings becomes strongly anisotropic in these cases
        due to the orientation of walls and special direction of the compaction. For studies
        where such anisotropy is unwanted other type of compaction methods are needed.
            In this paper, we present a compaction method where boundary effects are
        avoided due to exclusion of side walls. This simulation method is based on the
        contact dynamics algorithm where we applied the concept of the Andersen dynamics
        18 , which enables us to produce homogeneous granular packings of hard particles
        with desired internal pressure. The compaction method involves variable volume of
        the simulation cell with periodic boundary conditions in all directions.
            This paper is organized as follows. First we present some basic features of CD
        method in Section 2. Then, Section 3 describes the equations of motion for a system
        of particles with variable volume. In Section 4 we present a modified version of CD
        with coupling to constant external pressure. In Section 5 we report the results of
        some test simulations. Section 6 concludes the paper.


        2. Non smooth contact dynamics
        Contact dynamics (CD), developed by M. Jean and J. J. Moreau 6,7,8 , is a discrete
        element method in the sense that the time evolution of the system is treated on
        the level of individual particles. Once the total force F~i and torque T~i acting on the
        particle i is known, the problem is reduced to the integration of Newton’s equations
        of motion which can be solved by numerical methods. Here we use the implicit first
        order Euler scheme:
                                                          1 ~
                                 ~vi (t + ∆t) = ~vi (t) +    Fi (t + ∆t)∆t                   (1)
                                                          mi

                                 ~ri (t + ∆t) = ~ri (t) + ~vi (t + ∆t)∆t ,                  (2)
        which gives the change in the position ~ri and velocity ~vi of the center of mass of
        the particle with mass mi after the time step ∆t. ∆t is chosen so that the relative
        displacement of adjacent particles during one time step is small compared to the
        particle size and to the radius of curvature of the contacting surfaces. Corresponding
        equations are used also for the rotational degrees of freedom, describing the time
        evolution of the orientation and the angular velocity ~ωi caused by the new total
        torque T~i (t + ∆t) acting on the particle i.
            The interesting part of the CD method is how the interaction between the par-
        ticles are handled. For simplicity we assume that the particles are noncohesive and
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                     paper-1.8




        4


        dry, we exclude electrostatic and magnetic forces between them and consider only
        interactions via contact forces. The particles are regarded as perfectly rigid and the
        contact forces are calculated in terms of constraint conditions. Such constraints are
        the impenetrability and the no-slip condition, i.e. the contact force has to prevent
        the overlapping of the particles and the sliding of the contact surfaces. This latter
        condition is valid only below the Coulomb limit of static friction, which states that
        the tangential component of a contact force R~ can not exceed the normal component
        times the friction coefficient µ:
                                                ~ t ≤ µRn .
                                                R                                               (3)

        If the friction is not strong enough to ensure the no-slip condition the contact will be
        sliding and the tangential component of the contact force is given by the expression
                                                           rel
                                           ~ t = −µRn ~vt ,
                                           R                                                    (4)
                                                      ~vtrel
        where ~vtrel stands for the tangential component of the relative velocity between the
        contacting surfaces. In the CD method the constraint conditions are imposed on the
        new configuration at time t + ∆t, i.e., the unknown contact forces are calculated in
        a way that the constraints conditions are fulfilled in the new configuration 8 . This
        is the reason why an implicit time stepping is used.
            In order to let the system evolve one step from time t to t + ∆t one has to
        determine the total force and torque acting on each particle which may consist of
        external forces (like gravity) and contact forces from neighboring particles. Let us
        suppose that all the unknown contact forces are already determined except for one
        force between a pair of particles already in contact or with a small gap between
        them. Here we explain briefly how the constraint conditions help to determine the
        interaction between these two particles. A detailed description of the method can
        be found in 8 .
            The algorithm starts with the assumption that the contact force we are searching
        for is zero and checks whether this leads to an overlap of the undeformed shapes of
        the two particles after one time step ∆t. This is done based on the time stepping
        [Eq. (1)]: The external forces and other contact forces provide Fi (t + ∆t) and Ti (t +
        ∆t) for both particles thus the new relative velocity of the contacting surfaces ~v rel,free
        can be calculated. Here we use the term contacting surfaces for simplicity thought
        the two particles are not necessarily in contact. There might be a positive gap g
        between them, which is the length of the shortest line connecting the surfaces of
        the two particles (Fig. 1). We will refer to the relative velocity of the endpoints
        of the line as the relative velocity of the contact and denote the direction of the
        line by the unit vector ~n. In the limit of a real contact g is zero and ~n becomes
        the contact normal. Negative gap has the meaning of an overlap. The superscript
        free in ~v rel,free denotes that the relative velocity has been calculated assuming no
        interaction between the two particles. We use the sign convention that negative
        normal velocity (~n · ~v rel < 0) means approaching particles.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                           paper-1.8




                                                                                            5




                                          n



                                              g




                           Fig. 1.   Two rigid particles before a possible contact.


           The new value of the gap (after one time step) is estimated by the algorithm
        based on the current gap g and the new relative velocity ~v rel,free according to the
        implicit time stepping. If the new gap is positive:
                                           g + ~v rel,free · ~n∆t > 0                     (5)
        then the zero contact force (no interaction) is accepted because no contact is formed
        between the two particles. However, if the estimated new gap is negative then a
        contact force has to be applied in order to avoid the violation of the constraint
        conditions. Generally, one expects the following relation between the unknown new
        contact force R~ and the unknown new relative velocity ~v rel :

                                      ~ = −1 M(~v rel,free − ~v rel ),
                                      R                                                    (6)
                                           ∆t
        where M is the mass matrix that describes the inertia of the contact, i.e. M−1 R     ~
        is the relative acceleration of the contacting surfaces due to the contact force R. ~
        The mass matrix M depends on the shape, mass and moment of inertia of the two
        particles. On one hand, the interpenetration of the two rigid particles has to be
        avoided, which gives the following constraint for the normal component of ~v rel :
                                              g + ~v rel · ~n∆t = 0.                      (7)
        On the other hand, the tangential component of ~v rel has to be zero in order to
        ensure the no-slip condition
                                                   ~vtrel = 0.                            (8)
        The required contact force that fulfills Eqs. (7) and (8) then reads

                                    R~ = −1 M( g ~n + ~v rel,free ).                     (9)
                                          ∆t     ∆t
        This contact force is acceptable only if it fulfills the Coulomb condition [Eq. (3)].
        Otherwise we can not exploit the non-slip contact assumption. In this case, ~vtrel is
        not zero, the contact slides and the contact force has to be recalculated. Eqs. (6)
        and (7) then provide

                                 R~ = −1 M( g ~n − ~vtrel + ~v rel,free ),              (10)
                                       ∆t     ∆t
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                   paper-1.8




        6


        where the number of unknowns (components of R       ~ and ~v rel ) exceeds the number
                                                                    t
        of equations. In order to determine the contact force R ~ one has to solve Eq. (10)
        together with Eq. (4).
            It is recommended to use g pos = max(g, 0) instead of g in Eqs. (9) and (10).
        The gap size g should always be non-negative and using g pos apparently makes no
        difference 7 . However, due to the inaccuracy of the calculations small overlaps can
        be created between neighboring particles. If g instead of g pos is used then these
        overlaps are eliminated in the next time step by imposing larger repulsive contact
        forces to satisfy Eq. (7), which pumps kinetic energy into the system. Using g pos
        instead of g eliminates this artifact on the cost that an already existing overlap is
        not removed (which then serves to check the inaccuracies of the simulation 19 ), only
        its further growth is prevented. Regarding the above mentioned points, we rewrite
        the equations (9) and (10) as
                                                pos
                                 ~ = −1 M( g ~n + ~v rel,free )
                                 R                                  and                    (11)
                                     ∆t     ∆t

                                                pos
                                 ~ = −1 M( g ~n − ~v rel + ~v rel,free ).
                                 R                                                         (12)
                                                    t
                                     ∆t     ∆t
            A flowchart of the single contact force calculation is given in Fig. 2. So far we
        have explained only how the CD algorithm determines a single existing or incipient
        contact, based on the assumption that all the surrounding contact forces are known.
        However, in a dense granular media, many particles contact simultaneously and form
        a contact network. In this case, a contact force cannot be evaluated locally, since it
        depends on the adjacent contact forces which are also unknown. To find a globally
        consistent force network at each time step, an iterative scheme is applied in CD.
            At each iteration step, all contacts are chosen one by one and the force at
        the contact is updated according to the scheme shown in Fig. 2. The update is
        sequential, i.e., the freshly updated contact force is stored immediately as the current
        force and then a new contact is chosen for the next update.
            After one iteration step, constraint conditions are not necessarily fulfilled for
        each contact. In order to find a global solution the iteration process has to be
        repeated several times until the resulting force network converges. The convergence
        of the iteration process is smooth, i.e., the precision of the solution increases with
        the number of iterations NI . Higher NI provides more precise solution but also
        requires more computational effort. The CD method can be used with a constant
        number of iterations in subsequent time steps 19,8 or with a convergence criterion
        that prescribes a given precision to the force calculation 6,7,8 . In this latter case,
        the number of iterations NI varies from time step to time step.
            After the new force network is determined with a prescribed precision, the system
        evolves at the end of the time step according to the time-stepping scheme described
        at the beginning of this section. It is important to note that choosing small NI
        and/or large time step causes systematic errors of the force calculation which lead
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                                   paper-1.8




                                                                                                         7




                                 r              r              Yes
                             g + v rel , free ⋅ n ∆t > 0                    o
                                                                         contact

                                    o
                             Evaluation
                              r          of
                             R via Eq. (11)


                                  r                        o                               r
                                                               Sliding       Evaluation of R via
                                 |R t |≤ µRn                   contact        Eqs. (12) and (4)

                                 Yes
                                  Sticking
                                  contact




             Fig. 2.   The flowchart of the force calculation of a single contact in contact dynamics.


         to a spurious soft particle behavior 19 in spite of the original assumption of perfect
         rigidity.
             To conclude this section, we present briefly the scheme of the solver.
     
       t := t + ∆t (time step)
      Evaluating the gap g for all contacts
     
      N := N + 1 (iteration)
      I        I
       k := k + 1 (contact index)
     
           Evaluating ~vkrel,free then R
                                       ~ k (according to the flowchart in Fig. 2)
     
     
     
      Convergence test for contact forces
       Time-stepping for velocities and positions of all particles (using Eqs. (1) and (2))


         3. The equations of motion at constant external pressure
         In the simulation of granular materials, it is often desirable to investigate systems
         which are not surrounded by walls and to apply periodic boundary conditions in
         all directions. It is a nice feature of periodic boundary conditions that they make
         points of the space equivalent, the boundary effects are eliminated. That way the
         bulk properties of the material can be studied more easily. However, the application
         of an external pressure becomes problematic since the total volume is fixed and the
         system cannot be compressed by pistons or moving walls.
             In order to overcome this problem, but at the same time keep the advantageous
         periodic boundaries, Andersen 18 proposed a method for molecular dynamics sim-
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                      paper-1.8




        8


         ulations. Here, we recall his method briefly as its basic ideas will be used later on
         in this paper.
               According to the Andersen method the boundaries are still periodically con-
         nected in all directions and no walls are present, but the volume of the system is
         a dynamical variable which evolves in time driven by constant external pressure.
         When a system of N atoms is compressed or expanded it is done in an isotropic
         and homogeneous way: The distances between the atoms are rescaled by the same
         factor regardless of the relative or absolute positions.
               Let us give the equations of motion of a system with particle positions
        ~r1 , ~r2 , ..., ~rN in a D-dimensional cubic volume V (D = 2, 3 and each component
         of ~ri is between 0 and V 1/D ):
                                  d~ri (t)   p~i (t)  1        d ln V (t)
                                           =         + ~ri (t)            ,                (13)
                                     dt        mi     D            dt

                                  d~
                                   pi (t)            1        d ln V (t)
                                          = F~i (t) − ~pi (t)            ,                 (14)
                                    dt               D            dt

                                 Mv d2 V (t)
                                              = Pin (t) − Pext = ∆P (t).                    (15)
                                      dt2
        Eq. (13) describes the change in the position ~ri . The first term on the right is the
        usual one, the momentum ~    pi divided by the mass of the ith particle. The last term
        is the extension by the Andersen method that rescales the position according to the
        relative volume change.
            Eq. (14) provides the time evolution of the momentum due to two terms. The
        first one is the usual total force F~i acting on the ith particle which originates from
        the interaction with other particles and/or from external fields. The additional
        term leads to further acceleration of the particle if the volume is changing. E.g.,
        if the system is compressed the kinetic energy of the particles is increased due to
        the work done by the compression. The energy input is achieved by rescaling all
        particle momenta regardless of their positions. This is in contrast to usual pistons
        where the energy enters at the boundary.
            Eq. (15) can be interpreted as Newton’s second law that governs the change of
        the volume. It describes the time evolution of an imaginary piston which has the
        inertia parameter Mv and is driven by the generalized force ∆P (t) = Pin (t) − Pext .
        This latter is the pressure difference between the constant external pressure Pext and
        the internal pressure of the system Pin (t). The pressure difference ∆P (t) drives the
        system towards the external pressure, the sensitivity of the system to this driving
        force is controlled by the inertia parameter Mv .
            In the limit of infinite inertia Mv → ∞ together with the initial condition
        dV (t0 )/dt = 0 the volume of the system remains constant and Eqs. (13) and (14)
        correspond to the usual Newtonian dynamics of the particles.
            In order to get more insight into the Andersen dynamics let us consider a simple
        example of a system of non-interacting particles with all F~i (t) = 0. Initially, the
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                      paper-1.8




                                                                                            9


        velocities and the volume velocity dV (t0 )/dt are set to zero. Because the internal
        pressure Pin is zero the system with finite inertia Mv and under external pressure
        Pext > 0 will start contracting according to Eq. (15). The acceleration of the par-
        ticles [Eq. (14)] remains zero during the time evolution; One might say that the
        particles are standing there all the time. However, the distances between them are
        decreasing because of the contraction of the “world” around them. This is caused
        by the second term on the right hand side of Eq. (13) while the first term remains
        zero.
            This suggests the picture of an imaginary background membrane that contracts
        or dilates homogeneously together with the volume and carries the particles along.
        The velocity of this background at position ~ri is given by λ(t)~ri where λ is the
        dilation rate defined by the rate of the relative change in the system size L:

                                              L̇(t)   1 d ln V (t)
                                     λ(t) ≡         =                                    (16)
                                              L(t)    D     dt
        and D is the dimension of the system. Then the right hand side of Eq. (13) can
        be interpreted as the sum of two velocities: the second one is the velocity of the
        background at the position of the particle and the first one is the intrinsic velocity
        of the particle measured compared to the background. The sum of these two forces
        gives the changing rate of the absolute position ~ri . In the rest of the paper the
        velocity ~vi will refer always to the intrinsic velocity. We rewrite Eq. (13) in the
        following form
                                      d~ri (t)
                                               = ~vi (t) + λ(t)~ri (t).                  (17)
                                         dt
            Next we turn to the modelling of granular systems. Our goal is to achieve static
        granular packings that are compressed from a loose gas-like state. Here again it is
        advantageous to exclude confining walls and in order to apply pressure and achieve
        contraction of the volume we will use the concept of the Andersen method. However,
        the equations of motion will be slightly changed in order to make them suit better
        to our goals.
            In granular materials the interactions between the particles are dissipative. When
        the material is poured into a container or is compressed by a piston the particles
        gain kinetic energy due to the work done by gravity or the piston. All this energy has
        to be dissipated (turned into heat) by the interactions between the particles before
        the material can settle into a static dense packing of the particles. This relaxation
        process requires a massive computational effort when large packings are modeled in
        computer simulations. One encounters the same problem if the Andersen dynamics
        is applied straight to granular systems. The role of the second term on the right
        hand side of Eq.(14) is to conserve the total energy of the system by taking into
        account the energy gain of the particles due to compaction. The relaxation time
        can be reduced if this term is omitted, because then the total amount of energy
        pumped into the system is reduced. In this case the particles are accelerated only
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                     paper-1.8




        10


        by the forces F~i but they receive no additional energy due to the decreasing volume.
        Thus the following equation will be applied for granular compaction here

                                          d~vi (t)   1 ~
                                                   =    Fi (t)                            (18)
                                             dt      mi

        which results in a more effective relaxation rather than Eq. (14). This change is ad-
        vantageous also from the point of view of momentum conservation. If the system is
        compactified by using Eq. (14) from an initial condition where the total momentum
        of the particles is non-zero, then this momentum will be increased inverse propor-
        tionally to the size of the system L. Thus the total momentum e.g. due to initial
        random fluctuations is magnified which can lead to non-negligible overall rigid body
        motion of the final static packing. This is in contrast to Eq. (18) which provides
        momentum conservation in the absence of external fields.
            We note that neglecting the term in Eq. (14) leads to an artificial dynamics in the
        sense that the energy corresponding to the work of the compaction is not delivered
        to the particles. However, our main goal here is to produce a static configuration
        of grains and contact forces that can be used for further studies, thus we are not
        interested in that part of the dynamics, where compaction rate is significant and
        the neglected term makes a difference.
            Concerning the equation that describes the time evolution of the system size
        we find it more convenient to control λ instead of dV /dt. This is actually not an
        important change and leads to very similar dynamics. Our third equation reads

                                              dλ(t)
                                         Mλ         = ∆P (t).                             (19)
                                               dt

            The equations of motion (17), (18) and (19) describe an effective compaction
        dynamics for granular systems, they are able to provide static packings under the
        desired pressure Pext and if they are restricted to the limit of Mλ → ∞ we receive
        back the classical Newtonian dynamics.
            We note that the force scale in our systems of rigid particles is determined by
        the the external pressure as there is no intrinsic force scale. Taking larger value
        of Pext leads in principle to the same compaction dynamics (apart from rescaling
        time, velocities and forces). Consequently, the same final packing-configuration is
        expected, independently of the external pressure. Of course, the value of Pext does
        matter if an intrinsic force scale is present, e.g. when cohesion between the particles
        is incorporated. In such cases the final packing will strongly depend on the applied
        external pressure.
            In order to close the equations we need to define interactions between the par-
        ticles. The interparticle forces provide F~i in Eq. (18) and they are also needed to
        evaluate the inner pressure Pin .
            The stress tensor σαβ is not a priori spherical in granular materials. The average
        σαβ of the system is determined by the interparticle forces 20 and the particle
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                       paper-1.8




                                                                                             11


        velocities as
                                            Nc              N
                                        1 X                X
                              σαβ =       (    Fk,α lk,β +     mi vi,α vi,β ),             (20)
                                        V                  i=1
                                           k=1

        where N and Nc denote the number of particles and the number of contacts, re-
        spectively. If two contacting particles at contact k are labelled by 1 and 2, then F~k
        is the force exerted on particle 2 by particle 1, and the vector ~lk is pointing from
        the center of mass of particle 1 to that of particle 2 where periodic boundary condi-
        tions and nearest image neighbors are taken into account. Thus lk is the minimum
        distance between particles 1 and 2:
                                  lk = |~lk | = min|~r2 − ~r1 + V 1/3~a|,                  (21)
        where ~a is an integer-component translation vector. The inner pressure is then given
        by the trace of the stress tensor divided by the dimension of the system
                                              Nc              N
                                          1 X
                                                 F~k · ~lk +
                                                             X
                                Pin =       [                    mi~vi · ~vi ],            (22)
                                         DV                  i=1
                                              k=1

        which has the meaning of an average normal stress.
            The implementation of the above method in computer simulations is straight-
        forward if the interparticle forces are functions of the positions and velocities of the
        particles, e.g., in soft particle MD simulations. The implementation is less trivial for
        the case of the contact dynamics method where interparticle forces are constraint
        forces. We devote the next section to this problem.


        4. Contact dynamics with coupling to a constant external pressure
        In this section we present a modified version of the contact dynamics algorithm
        which enables us to perform CD simulations at constant external pressure. Accord-
        ing to Sec. 3 let us suppose that the system is subjected to a constant external
        pressure Pext and its time evolution is given by Eqs. (17), (18) and (19).
           Here we will follow the description of the CD method given in Sec. 2 and discuss
        the required modifications. Once the force calculation process is completed, the
        implicit Euler integration can proceed one time step further. Now the time stepping
        has to involve also the equations of motion of the system size. By discretizing the
        Eqs. (16) and (19) in the same implicit manner as for the particles [Eqs. (1) and (2)]
        we obtain the new values of the system size L and the dilation rate λ:
                                                          ∆P (t + ∆t)
                                 λ(t + ∆t) = λ(t) +                   ∆t,                  (23)
                                                             Mλ

                                 L(t + ∆t) = L(t)[1 + λ(t + ∆t)∆t]                         (24)
        where the “velocity” λ(t) and the “position” L(t) are updated by the new “force”
        ∆P (t + ∆t) and by the new “velocity” λ(t + ∆t), respectively.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                       paper-1.8




        12


            The discretized equations governing the translational degrees of freedom of the
        particles [Eqs. (1) and (2)] are rewritten according to Eqs. (17) and (18) in the
        following form:
                                                         1 ~
                              ~vi (t + ∆t) = ~vi (t) +      Fi (t + ∆t)∆t   and                   (25)
                                                         mi

                          ~ri (t + ∆t) = ~ri (t)[1 + λ(t + ∆t)∆t] + ~vi (t + ∆t)∆t.               (26)

         The time stepping for the rotational degrees of freedom remains unchanged because
         the dilation (contraction) of the system has no direct effect on the rotation of the
         particles.
               In the CD method, as we explained in Sec. 2 the particles are perfectly rigid and
         are interacting with constraint forces, i.e. those forces are chosen between contacting
         particles that are needed to fulfill the constraint conditions. E.g. the contact force
         has to prevent the interpenetration of the contacting surfaces.
               If a constant external pressure is used then the calculation of the constraint
         forces has to be reconsidered because the relative velocity of the contacting surfaces
         is influenced by the variable volume. When the system is dilating or contracting,
         particles gain additional relative velocities compared to each other. For a pair of
         particles, this velocity is λ~l where ~l is the vector connecting the two centers of mass.
         The same change appears in the relative velocity of the contacting surfaces as the
         size of the particles is kept fixed. If this change led to interpenetration then it has to
         be compensated by a larger contact force. It may also happen that existing contacts
         open up due to expansion of the system resulting in zero interaction force for those
         pair of particles.
               In the calculation of a single contact force, the relative velocity λ~l (i.e. the
         contribution of the changing system size) has to be added to ~v rel,free . The new
         relative velocity of the contact assuming no interaction between the two particles
        ~v rel,free is calculated here in the same way as in Sec. 2, i.e., based on the intrinsic
         velocities of the particles. Thus the effect of the dilation/contraction of the system
         is not taken into account in ~v rel,free . Therefore one has to replace ~v rel,free with
         (~v rel,free + λ~l) in all equations of Sec. 2 in order to impose the constraint conditions
         properly. Let us first suppose that the system has infinite inertia (Mλ = ∞) thus the
         dilation rate λ is constant. In this case the modified equations of the force update
         (containing already the term ~v rel,free + λ~l) provide the right constraint forces at the
         end of the iteration process. These forces will alter the relative velocity (~v rel,free +λ~l)
         in such a way that the prescribed constrain conditions will be fulfilled in the new
         configuration at t + ∆t.
               More consideration is needed if finite inertia Mλ is used and the dilation rate λ
         is time-dependent. The problem is that in order to calculate the proper contact force
         one has to know the new dilation rate. The new dilation rate, however, depends on
         the new value of the inner pressure [Eq. (23)] which, in turn, depends on the new
         value of the contact forces. This problem can be solved by incorporating λ and Pin
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                       paper-1.8




                                                                                            13


        into the iteration process. Instead of using the old values λ(t) and Pin (t) during the
        iteration, we always use the expected values λ∗ and Pin   ∗
                                                                    . These represent our best
        guess for the new dilation rate λ(t + ∆t) and for the new inner pressure Pin (t + ∆t).
        Pin
          ∗
            is defined based on the current values of the contact forces F~k∗ during the force
        iteration. Whenever a contact force is updated we recalculate the expected inner
        pressure Pin∗
                      . With the help of the current contact forces F~k∗ we can determine the
        total forces acting on the particles and then, following Eq. (25) we obtain also the
        expected new velocities of the particles ~vi∗ . The expected inner pressure, according
        to Eq. (22), then reads:
                                            Nc               N
                                        1 X
                                               F~k∗ · ~lk +
                                                            X
                               Pin
                                 ∗
                                   =      [                     mi~vi∗ · ~vi∗ ].          (27)
                                       DV                   i=1
                                            k=1

        Of course, there is no need to recalculate all the terms in Eq. (27) in order to update
        Pin
          ∗
            . When the force at a single contact is changed it affects only three terms: one
        due to the force itself and two due to the velocities of the contacting particles. In
        order to save computational time, only the differences in these three terms have to
        be taken into account when Pin  ∗
                                          is updated. Following Eq. (23), we obtain also the
        corresponding value of the expected dilation rate:
                                                   Pin
                                                     ∗
                                                       − Pext
                                       λ∗ = λ(t) +            ∆t                          (28)
                                                       Mλ
        This way, λ∗ and Pin ∗
                               are updated many times between two consecutive time steps
        (in fact they are updated NI Nc times) but in turn λ∗ and Pin  ∗
                                                                         are always consistent
        with the current system of the contact forces. At the end of the iteration process
        Pin
          ∗
             and λ∗ provide not just an approximation of the new inner pressure and new
        dilation rate but they are equal to Pin (t + ∆t) and λ(t + ∆t), respectively.
            To complete the algorithm, we list here also the equations that are used for the
        force calculation of a single contact. The inequality (5) is replaced by
                                    g + (~v rel,free + λ∗ ~l) · ~n∆t > 0,                 (29)
        i.e. there is no interaction between the two particles if the inequality is satisfied.
        Otherwise we need a contact force. The force, previously given by Eq. (11), that is
        required by a sticking contact is
                                                  pos
                                 ~ = −1 M( g ~n + λ∗ ~l + ~v rel,free ).
                                 R                                                        (30)
                                     ∆t     ∆t
                                                                                  ~ in Eq. (30)
        This force again has to be recalculated according to a sliding contact if R
        violates the Coulomb condition:
                                            pos
                               ~ = −1 M( g ~n − ~vtrel + λ∗ ~l + ~v rel,free ),
                               R                                                           (31)
                                    ∆t      ∆t
        which replaces the original equation (12).
            Except the above changes, the CD algorithm remains the same. In each time step
        the same iteration process is applied in order to reach convergence of the contact
        forces. After the iteration process we apply Eqs. (23)-(26) to complete the time step.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                         paper-1.8




         14


              The scheme of the solver for the modified version of CD can be presented as
     
       t = t + ∆t (time step)
      Evaluating the gap g for all contacts
     
         NI = NI + 1 (iteration)
     
      
       k = k + 1 (contact index)
     
        Evaluating ~v rel,free
     
                     k
        Evaluating R
                     ~ k (using Eqs. (30) and (31))
       Evaluating P ∗ (Eq. (27)) then λ∗ (Eq.( 28))
                        in
      Convergence test for contact forces
     
     
      Time-stepping for the dilation rate and the system size (using Eqs. (23) and (24))
       Time-stepping for velocities and positions of all particles (using Eqs. (25) and (26))

         In the next section we will present some simulations with the above method. We
         will test the algorithm and analyze the properties of the resulting packings.
             As an alternative to this fully implicit method we considered another possibility
         to discretize the Eqs. (16)-(19) in the spirit of the contact dynamics and, at the same
         time, impose the constraint conditions on the new configuration. The main difference
         is that the new value of the inner pressure Pin (t + ∆t) is determined based on the
         old velocities ~vi (t) and not on the new ones ~vi (t + ∆t), while the contribution of the
         forces are taken into account in the same way, i.e. the new contact forces F~k (t + ∆t)
         are used in Eq. (22). Therefore this version of the method is only partially implicit,
         however, the constraint conditions and the force calculation [Eqs. (29)-(31)] can be
         applied in the same way. Only, the expected values λ∗ and Pin        ∗
                                                                                has to be changed
         consistently with the new pressure Pin (t + ∆t):
                                            Nc               N
                                        1 X
                                               F~k∗ · ~lk +
                                                            X
                               Pin
                                 ∗
                                   =      [                     mi~vi (t) · ~vi (t)]          (32)
                                       DV                   i=1
                                            k=1

         and then this modified Pin ∗
                                      is used to determine the expected dilation rate λ∗ with
         the help of Eq. (28). Again here, Pin  ∗
                                                  and λ∗ are calculated anew after each force
         update during the iteration process and their last values equal the new pressure
         Pin (t + ∆t) and the new dilation rate λ(t + ∆t).
             We implemented and tested this second version of the method and found that the
         constraint conditions are handled here also with the same level of accuracy. Although
         the second method is perhaps less transparent than the fully implicit version, for
         practical applications it seems to be more useful. First, the second version of the
         method is easier to implement into a program code, second, it turned out to be
         faster by 25% in our test simulations. The improvement of the computational speed
         originates from the smaller number of the operations. One does not have to handle
         the expected particle velocities ~vi∗ and the recalculation of Pin
                                                                          ∗
                                                                             is more simple as
                                          ~
         the change of a contact force Fk affects only one term in the Eq. (32). We note
                                            ∗

         that here the distinction “partially implicit” and “fully implicit” refers only to the
         difference, whether the velocities are or are not included in the iteration process.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                       paper-1.8




                                                                                                      15


        5. Numerical results
        We perform numerical simulations using the CD algorithm with the fully implicit
        constant pressure scheme of section 4. This algorithm has been used to study me-
        chanical properties of granular packings in response to local perturbations 21,22 .
        Here, the main goal is to show that the algorithm works indeed in practical applica-
        tions and to test the method from several aspects; We investigate how the simulation
        parameters influence the required CPU time and the accuracy of the simulation.
        Such parameters are the external pressure Pext , the inertia parameter Mλ and the
        computational parameters, like the number of iterations per time step NI and the
        length of the time step ∆t. We also analyze the properties of the resulting packings.
            Here, we report only simulations of two-dimensional systems of disks, where the
        behavior is very similar to that we found for spherical particles in three-dimensional
        systems. Length parameters, the time and the two-dimensional mass density of the
        particles are measured in arbitrary units of l0 , t0 and ρ0 , respectively. The samples
        are polydisperse and the disk radii are distributed uniformly between 0.8 and 1.2,
        thus the average grain radius is 1. The material of the grains has unit density and
        the masses of the disks are proportional to their areas. In this section we have one
        reference system that contains 100 disks. The interparticle friction coefficient is set
        to 0.5. The value of other parameters are: NI = 100, ∆t = 0.01, Pext = 1 (this
        latter is expressed in units of ρ0 l02 /t02 ) and the inertia Mλ = 100 (in units of ρ0 l02 ).
        Throughout this section, we either use these reference parameters or the modified
        values will be given explicitly. Usually, we will vary only one parameter to check its
        effect while other parameters are kept fixed at their reference values.




        Fig. 3. Schematic picture of a two dimensional granular system controlled by a constant external
        pressure: (a) the initial gas state, and (b) the final homogeneous packing. The dashed lines mark
        periodic boundaries.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                                                paper-1.8




        16



                                                           14
                0                                                                                     35
                                                           12
             -0.02                                         10
                                                                                                      30




                                                    Pin/Pext
                                                               8
             -0.04




                                                                                                  L
        λ




                                                               6
                                                                                                      25
             -0.06                                             4
                                                               2
             -0.08                                                                                    20
                                                               0
                     0   1000 2000 3000 4000 5000                  0   1000 2000 3000 4000 5000            0   1000 2000 3000 4000 5000
                              Time Step                                     Time Step                               Time Step


        Fig. 4. Typical time evolution of the dilation rate λ (left) the inner pressure Pin (middle) and
        the system size L (right) during the compression of a 2D polydisperse sample. The data shown
        here were recorded in the reference system specified in the text.


            In each simulation, we start with a dilute sample of nonoverlapping rigid disks
        randomly distributed in a two dimensional square-shaped cell [Fig. 3(a)]. No confin-
        ing walls are used according to the boundary conditions specified in Sec. 4. Gravity
        and the initial dilation rate are set to zero. Due to imposing a constant external
        pressure the dilute system starts shrinking. As the size of the cell decreases, particles
        collide, dissipate energy and after a while a contact force network is formed between
        touching particles in order to avoid interpenetrations. The contact forces build up
        the inner pressure Pin which inhibits further contraction of the system. Finally, a
        static configuration is reached in which Pin equals Pext and mechanical equilibrium
        is provided for each particle [Fig. 3(b)]. Technically, we finish the simulation when
        the system is close enough to the equilibrium state: We apply a convergence thresh-
        old for the mean velocity vmean and mean acceleration amean of the particles (which
        are measured in units l0 /t0 and l0 /t02 , respectively). Only if both vmean and amean
        become smaller than the threshold 10−10 we regard the system as relaxed and stop
        the simulation.
            The typical time evolution can be seen in Fig. 4 where we show the compaction
        process in the case of the reference system. Fig. 4(left) implies that the magnitude
        of λ grows linearly in the beginning when the inner pressure is close to zero. The
        negative value of the dilation rate indicates contraction which becomes slower after
        the particles build up the inner pressure [Fig. 4(middle)]. The fluctuations in Pin
        are due to collisions of the particles. In the final stage of the compression λ goes to
        zero, Pin converges to the external pressure and the size of the system reaches its
        final value [Fig. 4(right)].
            Next we investigate how the required CPU time of the simulation is affected
        by the various parameters. All simulations are performed with a processor Intel(R)
        Core(TM)2 CPU T7200 @ 2.00GHz and the CPU time is measured in seconds.
        Figure 5 reveals that the variation of Pext , ∆t, NI and Mλ have direct influence
        on the required CPU time. The final packing is achieved with less computational
        expenses if larger Pext , larger ∆t or smaller NI is used. The role of system inertia
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                                            paper-1.8




                                                                                                                                17


                           104
          CPU Time (sec)




                           103

                           102

                           101

                            1
                                     10-2      1       102   10-4     10-2      1 101      102      103 10-2   1    102   104
                                              Pext                     ∆t                   NI                     Mλ


                                                 Fig. 5.     CPU time versus the simulation parameters.


        Mλ is more complicated. Mλ reflects the sensitivity of the system to the pressure
        difference Pin − Pext . If the level of the sensitivity is too small or too large, the
        simulation becomes inefficient. It is advantageous to choose the inertia Mλ near
        to its optimal value which depends on the specific system (e.g. on the number and
        mass of the particles) 23 .
            Regarding the efficiency of the computer simulation, not only the computational
        expenses play an important role but the accuracy of the simulation is also essential.
        Here we use the overlaps of the particles as a measure of the inaccuracy of the sim-
        ulation (see Sec. 2). In an ideal case there would be no overlaps between perfectly
        rigid particles. Fig. 6 shows the mean overlaps measured in the final packings. It
        can be seen for the parameters Pext , ∆t and NI that the reduction of the compu-
        tational expenses at the same time leads also to the reduction of the accuracy of
        the simulation. In Fig. 7(left) we plot the CPU time versus the mean overlap for
        these three parameters. The data points collapse approximately on the same master
        curve which tells us that the computational expenses are determined basically by
        the desired accuracy; smaller errors require more computations. The efficiency of
        the simulation is approximately independent of the parameters Pext , ∆t and NI .
        The situation is, however, different for the inertia of the system Mλ . First, it has
        relatively small effect on the accuracy of the simulation (Fig. 6). Variation of Mλ
        by 7 orders of magnitude could hardly change the mean overlap of the particles.


                                 1

                             -2
                           10
          Mean Overlap




                           10-4

                           10-6

                           10-8
                                      10-2     1       102   10-4     10-2      1 101      102      103 10-2   1    102   104
                                              Pext                     ∆t                   NI                     Mλ


                                             Fig. 6.    Mean overlap in terms of the simulation parameters.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                                                                                          paper-1.8




        18


                                            104                                                                              104



                                            103                                                                                                           Mλ
                                                                           Pext
                           CPU Time (sec)




                                                                                                            CPU Time (sec)
                                                                           NI                                                103
                                                                           ∆t
                                            102

                                                                                                                             102
                                            101



                                             1                                                                               101
                                             10-8    10-7   10-6    10-5 10-4 10-3       10-2   10-1    1                      10-6           2x10-6            5x10-6       10-5
                                                                     Mean Overlap                                                                   Mean Overlap


        Fig. 7. CPU time in terms of the mean overlap. The different curves are obtained by the variation
        of different parameters according to Figs. 5 and 6. These parameters are the external pressure Pext ,
        the number of iterations per time step NI , the length of the time step ∆t (left) and the inertia
        of the system Mλ (right). The open circle on the right indicates the most efficient simulation we
        could achieve by controlling the inertia Mλ .


        Second, Mλ affects strongly the efficiency of the simulation which is shown clearly
        by Fig. 7(right). If Mλ is varied then larger computational expense is not neces-
        sarily accompanied with smaller errors. In fact, in the whole range of Mλ studied
        here, the fastest simulation turned out to be the most accurate one [open circle in
        Fig. 7(right)].
            Next we turn to the question whether the parameters of the simulation used
        in the compaction process influence the physical properties of the final packing.
        There are many ways to characterize static packings of disks. Here we test only one
        quantity, the frequently used volume fraction. The volume fraction gives the ratio
        between the total volume (total area in 2D) of grains and the volume (area) of the
        system. Fig. 8 shows the volume fraction of the same packings that were studied
        already in Fig. 6. It can be seen that the volume fraction remains approximately
        unchanged under the variation of the four parameters Pext , NI , ∆t and Mλ . This
        is except for one data point for large time step ∆t, where the simulation is very
        inaccurate. The corresponding mean overlap (Fig. 6) is comparable to the typical



                                   0.9
         Volume Fraction




                                   0.8


                                   0.7


                                                    10-2      1         102       10-4           10-2       1 101                       102         103 10-2    1     102   104
                                                             Pext                                 ∆t                                     NI                          Mλ


                                                               Fig. 8.     Volume fraction versus the simulation parameters.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                              paper-1.8




                                                                                                                                               19


                             90

                     120                  60
                                    140
                                   130
                                   120


               150                              30


                                                                                                                                          17

                                                          Nc(x,y)
                                                                                                                                          16
         180                                          0   30
                                                          25                                                                              15
                                                          20
                                                          15                                                                              14
                                                                                                                                     60
                                                          10                                                                    50
               210                              330
                                                           5                                                               40
                                                           0                                                          30
                                                               0
                                                                                                                 20
                                                                                                                                 y
                                                                    10
                                                                         20
                                                                                  30                        10
                     240                  300                                              40
                                                                              x                 50
                                                                                                     60 0
                             270




        Fig. 9. (left) The angular distribution of the contacts. The number of contacts is plotted in terms
        of the direction of their normal vectors. (right) Spatial distribution of the contacts. The system
        contains N = 1000 disks in both figures.


        size of the particles which is the reason why the volume fraction appears to be much
        larger.
            Finally, we investigate the inner structure of the resulting random packings.
        For that, we study larger samples with N = 1000 particles, otherwise, the default
        parameters are used during the compaction. To suppress random fluctuations, we
        produce 5 different systems and all quantities reported hereafter represent average
        values over these systems. In Fig. 9(left) we study the angular distribution of the
        contact normals and find that it is very close to uniform. However, there is a small
        but definite deviation (around 3%): the density of the contact normals are slightly
        larger parallel to the periodic boundaries. In this sense the packing is not completely
        isotropic. Although the effect is very small, the orientation of the boundaries can
        be observed also in such local quantities like the direction of the contacts.
            In connection to the question of the isotropy we checked also the global stress
        tensor σ. In the original frame σ reads
                                                                                 
                                                    1.00909 −0.01334
                                           σ=                                          .                                                  (33)
                                                    −0.01332 0.99091

        This stress is isotropic with good approximation. The diagonal entries are close to 1
        which equals Pext while the off-diagonal elements are approximately zero. Compared
        to the unit matrix, the elements deviate around 1% of Pext .
            The final packings are expected to be homogeneous as all points of the space
        are handled equivalently by the compaction method. Apart from random fluctua-
        tions we do not observe any inhomogeneity in our test systems. As an example, we
        show the spatial distribution of the contacts in Fig. 9(right), where the density is
        approximately constant.
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                   paper-1.8




        20


        6. Concluding remarks
        In this work we have proposed and tested a simulation method to produce homoge-
        neous random packings in the absence of confining walls. We combined the contact
        dynamics algorithm with a modified version of the Andersen method to perform
        constant pressure simulations of granular systems. Our main concern was to discuss
        how constraint conditions can be applied to determine the interaction between the
        particles in an Andersen-type of dynamics. We have presented the results of some
        numerical tests and discussed the effect of the main parameters on the efficiency of
        the simulations and on the physical properties of the final packings.
            We restricted our study to the simple case where we allow only spherical strain
        of the system in order to achieve the desired pressure. However, the method can
        be generalized to apply other type of constraints to the stress tensor and, conse-
        quently, to allow more general strain deformations where shape as well as size of
        the simulation cell can be varied 24,25 .

        Acknowledgements
        We acknowledge support by grants No. OTKA T049403, No. OTKA PD073172 and
        by the Bolyai Janos Scholarship of the Hungarian Academy of Sciences.

        References
         1. P. A. Cundall and O. D. L. Strack, Géotechnique 29, 47 (1979).
         2. L. E. Silbert et al., Phys. Rev. E 65, 031304 (2002).
         3. D. C. Rapaport, J. Comp. Phys. 34, 184 (1980).
         4. O. R. Walton and R. L. Braun, Journal of Rheology 30, 949 (1986).
         5. M. Jean and J. J. Moreau, Unilaterality and dry friction in the dynamics of rigid body
            collections – Proc. of Contact Mechanics Intern. Symposium, ed. A. Curnier (Presses
            Polytechniques et Universitaires Romandes, 1992), p. 31.
         6. J. J. Moreau, Eur. J. Mech. A-Solids 13, 93 (1994).
         7. M. Jean, Comput. Methods Appl. Mech. Engrg. 177, 235 (1999).
         8. L. Brendel, T. Unger and D. E. Wolf, The Physics of Granular Media (Wiley-VCH,
            Weinheim, 2004), p. 325.
         9. P. K. Haff, J. Fluid Mech. 134, 401 (1983).
        10. S. McNamara and W. R. Young, Phys. Rev. E 50, R28-R31 (1994).
        11. A. Mehta, Granular Matter (Springer-Verlag, New York, 1994).
        12. R. Zallen, The Physics of Amorphous Solids (Wiley, New York, 1983).
        13. J. P. Hansen and I. R. McDonald, Theory of Simple Liquids (Academic Press, New
            York, 1986).
        14. S. Torquato, Random Heterogeneous Materials (Springer-Verlag, New York, 2002).
        15. A. J. Liu and S. R. Nagel, Nature 396, 21 (1998).
        16. G. Combe and J. N. Roux, Phys. Rev. Lett. 85, 3628 (2000).
        17. T. Aste and D. Weaire, The Pursuit of Perfect Packing (IOP Publishing, New York,
            2000).
        18. H. C. Andersen, J. Chem. Phys. 72, 2384 (1980).
        19. T. Unger et al., Phys. Rev. E 65, 061305 (2002).
        20. J. Christoffersen, M. M. Mehrabadi and S. Nemat-Nasser, J. Appl. Mech. 48, 339
            (1981).
January 21, 2021 13:20 WSPC/INSTRUCTION FILE                paper-1.8




                                                                                           21


        21. M. R. Shaebani, T. Unger and J. Kertész, Phys. Rev. E 76, 030301(R) (2007).
        22. M. R. Shaebani, T. Unger and J. Kertész, Phys. Rev. E 78, 011308 (2008).
        23. A. Kolb and B. Dunweg, J. Chem. Phys. 111, 4453 (1999).
        24. M. Parrinello and A. Rahman, Phys. Rev. Lett. 45, 1196 (1980).
        25. M. P. Allen and D. J. Tildesley, Computer Simulation of Liquids (Oxford University
            Press, New York, 1996).
