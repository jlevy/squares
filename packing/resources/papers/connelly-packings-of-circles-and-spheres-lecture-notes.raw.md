Packings of circles and spheres
         Lectures III and IV
     Session on Granular Matter
       Institut Henri Poincaré
                 R. Connelly
             Cornell University
          Department of mathematics




                                      1
What model is good for
     packings?




                         2
      What model is good for
           packings?
• There must be a container of some sort for
  the packing elements.




                                               3
      What model is good for
           packings?
• There must be a container of some sort for
  the packing elements.
• Is the packing jammed?




                                               4
      What model is good for
           packings?
• There must be a container of some sort for
  the packing elements.
• Is the packing jammed?
• If so, what criteria do you want for
  jamming?



                                               5
             Some containers
Put the packing in a box. Let the box shrink in size
  or let the packing elements grow in size until you
  are stuck.




                                                       6
      More possible containers
• A rectangular box
• A circle
• A torus




                                 7
            Jammed packings
When the packing is locally most dense, there is a
 rigid cluster that is jammed, but there could be
 “rattlers”, non-rigid pieces.




              The most dense packing of 7 congruent circles in a
              square. (Note the "rattler" in the upper right corner.)
              (Due to Shaer)



                                                                        8
             Random close packings
“Is Random Close Packing of Spheres Well
  Defined?” (Torquato, Truskett and Debenedetti 2000)
  Experimentally, if you pour ball bearings into a
  large container, shake, and calculate the density,
  you get about 0.636. But this depends on the
  method you use to “densify”. Other methods give
  0.642, 0.649, 0.68 … This paper suggests “order
  parameters”…
The following is joint work with A. Donev, F. Stillinger, and
  S. Torquato. See also my papers in:
http://www-iri.upc.es/people/ros/StructuralTopology/

                                                                9
                  Definitions
If P is a packing in a container C, call it locally
   maximally dense if every other packing of the
   same packing elements, sufficiently close to P in
   C has a packing density (=packing fraction) no
   larger than the density of P in C.
A packing P is (collectively) jammed in C if any
   other packing sufficiently close to P in C is the
   same as P. (I also say P is rigid in C.)

                                                       10
               Why jammed?
Theorem: If a packing P of circles (or spherical
  balls in 3-space) is locally maximally dense in a
  polygonal container C, then there is subset P0 of P
  that is collectively jammed in C.
Theorem (Danzer 1960): A packing P of circles (or
  spherical balls in 3-space) is collectively jammed
  in a polygonal container C, if and only if the
  underlying strut tensegrity framework is
  infinitesimally rigid.
                                                    11
                    Remarks
• If the packing P has no part that is collectively
  jammed, then the packing can be moved slightly
  and the container shrunk slightly to improve the
  overall density.
• Since a necessary condition for being jammed is
  infinitesimal rigidity, circle packings in polygons
  can be tested for being jammed with reasonably
  efficient linear programming (feasability)
  algorithms and the nearby improved packing
  calculated as well.
                                                        12
                       Proofs
Let the configuration p = (p1, p2, … pn) be the
   centers of the packing circles, including the pinned
   points on the boundary. If the associated strut
   framework G(p) is infinitesimally rigid, even for a
   subset of the packing centers, then there is no
   nearby configuration satisfying the packing
   constraints for that subset that increases density.
If G(p) is not infinitesimally rigid, let p¢= (p1¢, p2¢,
   … pn¢) be the (non-zero) infinitesimal flex of
   G(p). Then for each i define pi(t)= pi + t pi¢, 0 ≤ t .
                                                        13
           The crucial calculation
|pi(t)- pj(t)|2 = |pi- pj|2+2t(pi - pj)(pi¢ - pj¢)+t2|pi¢ - pj¢ |2.
So |pi(t)- pj(t)| ≥ |pi- pj| for each pair of disks that
  touch, and there is strict inequality unless pi¢ = pj¢.
  For example, the following shows this at work.




                                                                  14
            The crucial calculation
      |pi(t)- pj(t)|2 = |pi- pj|2+2t(pi - pj)(pi¢ - pj¢)+t2|pi¢ - pj¢ |2.
So |pi(t)- pj(t)| ≥ |pi- pj| for each pair of disks that touch, and
   there is strict inequality unless pi¢ = pj¢.
I call this motion, the canonical push. For example, the
   following shows this at work.




                                                                            15
                    Remarks
• The motion provided by the linear programming
  algorithm (LP) can be quite complicated, and it
  seems best to use it to clear up log jams, rather
  than ongoing “densification”.
• For example, the Lubachevsky-Stillinger
  algorithm of slow densification (bump-and-slow
  down) is more efficient in converging to a jammed
  state than LP.
• The (LP) motion does not continue forever. Some
  non-incident packing disks will get closer together
  and collide, sometimes quite soon.

                                                    16
                      Statics
When the packing is collectively jammed, it must be
 statically rigid, which means it must be able to
 resolve arbitrary loads. But such tensegrity
 frameworks are never statically determinant, since
 by the Roth-Whiteley Theorem, there is always a
 non-zero proper self stress. On the other hand, a
 physical system must resolve loads in some way…
 Later more about this. The final resolution of an
 external load is a function of the relative elasticity
 in the packing elements. Geometry, alone, cannot
 “resolve” this.
                                                     17
   The fundamental conundrum
Do numerical simulations make sense for large numbers of
  packing elements? For example, for monodispersed (i.e.
  congruent) disks in the plane, the following configuration
  often appears in some simulations, which is impossible.




                                                           18
          Infinite packings
How can infinite packings be “jammed”?




                                         19
          Infinite packings
How can infinite packings be “jammed”?
They can’t. We have to keep them from
 flying apart. Some ideas…




                                         20
           Infinite packings
How can infinite packings be “jammed”?
They can’t. We have to keep them from
   flying apart. Some ideas…
1. Insist that each packing element be fixed
   by its neighbors. (Locally jammed.)



                                               21
           Infinite packings
How can infinite packings be “jammed”?
They can’t. We have to keep them from
   flying apart. Some ideas…
1. Insist that each packing element be fixed
   by its neighbors. (Locally jammed.)
2. Pin all but a finite number. (Finite
   stability=collectively jammed)

                                               22
            Infinite packings
How can infinite packings be “jammed”?
They can’t. We have to keep them from flying apart.
   Some ideas…
1. Insist that each packing element be fixed by its
   neighbors. (Locally jammed.)
2. Pin all but a finite number. (Finite stability
   =collectively jammed)
3. Enforce periodicity. This amounts to putting the
   packing on a torus. (Periodic stability)

                                                 23
               Difficulties
The locally jammed property is very weak. K.
 Böröczky (1964) showed that there is a
 packing of congruent disks in the plane with
 0 density that is locally jammed. If you
 move 8 disks at a time, the packing falls
 apart.



                                            24
               Difficulties
The collectively jammed property is better,
 but as the number of packing elements that
 are allowed to move gets large, the packing
 can be very fragile. For example, the
 following square lattice packing in a square
 seems to be not collectively jammed ... (A.
 Bezdek, K. Bezdek, R. Connelly 1998)

                                            25
A near unjamming




                   26
A near unjamming




                   27
A near unjamming




                   28
A near unjamming




                   29
A near unjamming




                   30
A near unjamming




                   31
A near unjamming




                   32
A near unjamming




                   33
The size of the square




                         34
              Discrete rigidity
Theorem: Suppose that G(p) is a finite (tensegrity)
  framework, with pinned vertices, that is rigid in
  Ed. Then there is an e > 0 such that when |pi-qi| <
  e for all i, and the same member constraints hold
  for G(q), then p=q.
Even when the member constraints are relaxed by
  d > 0, say, then the configuration can jiggle about,
  but not too far.
The e for the square lattice packing in a square
  seems quite small.

                                                     35
Calculations for the square lattice
       packing in a square
Let s be the length of the side of the bounding
  square during the deformation shown. Then when
  the first pair of circles are rotated by q, then s is
  calculated as
               s = 4n cos q + 2 sin q + 2,
where the radius of the circles are 1, and there are
  n+1 circles on a side, hence (n+1)2 circles in all.
  So the square expands less than 1/(2n), and
  s < 4n +2, the side length of the square, for
  q > 2/n.
                                                      36
                The point
The e needed to insure rigidity converges to 0
 as n -> • for the square lattice packing. In
 other words, you have to decrease the
 tolerances to 0 as you release more and
 more of the packing elements and allow
 them to move.
A suggestion to address this problem …

                                             37
               Uniform stability
An infinite packing of circles in the plane is uniformly stable
  if there is an e > 0 such that the only finite rearrangement
  of the disks as a packing, where each center is displaced
  less than e, is the identity. (This is related to a different, but
  similar, definition of L. Fejes Toth.)




                                                                 38
                   Examples
1. The square lattice packing (or the cubic lattice
   packing in higher dimensions) is NOT uniformly
   stable.
2. The triangular lattice packing in the plane IS
   uniformly stable, even with the removal of one
   packing element. (I. Bárány and N.P. Dolbilin (1988)
    as well as A. Bezdek, K. Bezdek, R.C. (1998))
3. Most of the candidates for the most dense
   packings of congruent spheres in higher
   dimensions are uniformly stable. (A. Bezdek, K.
    Bezdek, R. Connelly 1998)
Another suggestion for this problem:
                                                     39
    How do you handle infinite
           packings?
• Only allow a finite number of packings to
  move. . . . or
• Consider periodic packings with a fixed
  lattice defining the periodicity . . . or
• Consider periodic packings with a variable
  lattice as well as a variable configuration,
  but such that the density is locally maximal.


                                              40
          Periodic Packings
A packing is periodic with lattice L if for
  every packing element X, l + X is a
  packing element for every l in L. Regard
  this as a packing of a finite number of
  packing elements in the torus R2/L. So such
  a packing can be regarded as stable if there
  is no perturbation of the configuration
  except trivial perturbations.
                                            41
    The problem with fixing the
     lattice defining the torus




The packing (with only 2 disks) defined on a torus, whose
  fundamental region is the small yellow square, is jammed.
The packing (with 8 disks) defined on a torus, whose
  fundamental region is the larger square, is NOT jammed.

                                                          42
        Counting in Coverings
Let k be the order of the covering, so there are
  exactly kn disks in the covering and ke contacts. If
  there are the minimal number of contacts e = 2n-1
  in the original rigid configuration, there will be
            ke = k(2n-1) = 2kn-k < 2kn-1
 contacts in the cover, and so the cover will NOT be
  rigid.


                                                    43
            Strictly Jammed
So we define a packing on a (flat) torus to be
  strictly jammed if there is no non-trivial
  infinitesimal motion of the packing, as well
  as the lattice defining the torus, subject to
  the condition that the total area of the torus
  does not increase during the infinitesimal
  motion.

                                               44
   Counting for Strictly Jammed
             Packings
• Variables:
   – Coordinates: 2n       - Lattice vectors: 2 + 2 = 4
• Constraints:
   – Packing contacts: e   - Area constraint: 1
• Trivial motions:
   – Translatons: 2        - Rotations: 1
The final count is then
             e +1 ≥ 2n + 4 - 3 + 1 or e ≥ 2n +1.
So the packing covers have a chance to be strictly jammed,
  although it is not guaranteed. The number of constraints in
  a cover is more than is needed for stability.
                                                           45
  The Crystallization Conjecture
If a periodic packing is strictly jammed, what
   does it look like?
Conjecture: The only strictly jammed
   periodic packing in the plane is the
   triangular lattice packing, possibly with
   some disks missing.


                                                 46
   The Crystallization Conjecture
If a periodic packing is strictly jammed, what
   does it look like?
Conjecture: The only strictly jammed
   periodic packing in the plane is the
   triangular lattice packing, possibly with
   some disks missing.
Sadly this is false.


                                                 47
Start with this tiling




                         48
The construction of the pentagon
          in the tiling
                          b
                                  1
              1



             120                  120

                      3       3
         1                              1



                  a       1       a

               2a + b + 60 = 360


                                            49
 Split it apart and add some
“bracing triangles” as well as
some connecting rhombuses.




                                 50
 Split it apart and add some
“bracing triangles” as well as
some connecting rhombuses.




                                 51
This what the packing looks like.




                                52
Another possible example of a
  strictly jammed packing




                                53
    Low density strictly jammed
            packings
Conjecture: The density of a strictly jammed
 periodic packing is greater than (3/4)p/√12, the
 density of the Kagome packing.




                                                    54
“In fact, in a flat two-dimensional space it is
believed that only the triangular lattice
configuration … is stable in the alter case.” (Einar L.
Hinrichsen, Jens Feder, and Torstein Jossnag, Random
packing of disks in two-dimensions, Phys. Rev. A, Vol 41,
No. 8, 15 April 1990, p.4200.)




                                                            55
56
57
