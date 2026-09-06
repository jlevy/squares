                                                                                                                                        SIAM J. DISCRETE MATH.                                 () 1996 Society for Industrial and Applied Mathematics
                                                                                                                                        Vol. 9, No. 3, pp. 453-491, August 1996                                                                  008




                                                                                                                                           SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY FOR
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                      TENSEGRITY FRAMEWORKS*
                                                                                                                                                                 ROBERT CONNELLY AND WALTER WHITELEY$

                                                                                                                                             Abstract. This paper defines two concepts of rigidity for tensegrity frameworks (frameworks
                                                                                                                                        with cables, bars, and struts): prestress stability and second-order rigidity. We demonstrate a hier-
                                                                                                                                        archy of rigidity--first-order rigidity implies prestress stability implies second-order rigidity implies
                                                                                                                                        rigiditymfor any framework. Examples show that none of these implications are reversible, even for
                                                                                                                                        bar frameworks. Other examples illustrate how these results can be used to create rigid tensegrity
                                                                                                                                        frameworks.
                                                                                                                                              This paper also develops a duality for second-order rigidity, leading to a test which combines
                                                                                                                                        information on the self stresses and the first-order flexes of a framework to detect second-order rigidity.
                                                                                                                                        Using this test, the following conjecture of Roth is proven: a plane tensegrity framework, in which
                                                                                                                                        the vertices and bars form a strictly convex polygon with additional cables across the interior, is rigid
                                                                                                                                        if and only if it is first-order rigid.

                                                                                                                                                Key words, tensegrity frameworks, rigid and flexible frameworks, stability of frameworks,
                                                                                                                                        static stress, first-order motion, second-order motion

                                                                                                                                                AMS subject classifications. Primary, 52C25; Secondary, 70B15, 70C20

                                                                                                                                             1. Introduction. A fundamental problem in geometry is to determine when
                                                                                                                                        selected distance constraints, on a finite number of points, fix these points up to
                                                                                                                                        congruence, at least for small perturbations. We rephrase this as a problem in the
                                                                                                                                        rigidity of frameworks. From this point of view, we do the following:
                                                                                                                                               (i) provide methods for recognizing when a given framework is rigid;
                                                                                                                                              (ii) find ways of generating rigid frameworks;
                                                                                                                                             (iii) explore the relationship among these methods;
                                                                                                                                             (iv) solve a conjecture of Roth, in [29], concerning the rigidity of a specific class
                                                                                                                                        of frameworks in the plane.
                                                                                                                                             Many of the concepts here are inspired by techniques used in structural engineer-
                                                                                                                                        ing, such as the principle of least work and energy, but our treatment is independent
                                                                                                                                        of any such concepts. Broadly speaking our objective in this paper is to investigate
                                                                                                                                        the geometric properties of configurations of points in Euclidean space. However, our
                                                                                                                                        results clarify and justify mathematically some of the techniques used by structural
                                                                                                                                        engineers to analyze certain tensegrity structures. (See [5, 27, 28] for example.) Our
                                                                                                                                        techniques extend those of [21] and are related to the questions posed by Tarnai [31].
                                                                                                                                        A summary of these results, for engineers, was presented in [13].
                                                                                                                                             1.1. Terminology. A tensegrity framework is an ordered finite collection of
                                                                                                                                        points in Euclidean space, called a configuration, with certain pairs of these points,

                                                                                                                                                *Received by the editors April 13, 1992; accepted for publication (in revised form) October 10,
                                                                                                                                        1995.
                                                                                                                                                Department of Mathematics, Cornell University, Ithaca, NY, 14853-7901 (connelly@math. cor-
                                                                                                                                        nell.edu). The work of this author was supported in part by National Science Foundation grant MCS-
                                                                                                                                        790251, Distinguished Visitorship, Centre de Recherches Mathematiques, Universit de Montreal, and
                                                                                                                                        the Humboldt research award program.
                                                                                                                                                :Departmentof Mathematics and Statistics, York University, 4700 Keele Street, North York,
                                                                                                                                        Ontario M3J-1P3, Canada (whiteley@mathstat.yorku.ca). The work of this author was supported in
                                                                                                                                        part by grants from Fonds pour la Formation de Chercheurs et l’Aide k la Recherche (Quebec) and
                                                                                                                                        Natural Sciences and Engineering Research Council of Canada.
                                                                                                                                                                                            453
                                                                                                                                        454                              R. CONNELLY AND W. WHITELEY

                                                                                                                                        called cables, constrained not to get further apart; certain pairs, called struts, con-
                                                                                                                                        strained not to get closer together; and certain pairs, called bars, constrained to stay
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        the same distance apart. Together, struts, cables, and bars are called members. If
                                                                                                                                        each continuous motion of the points satisfying all the constraints is the restriction of
                                                                                                                                        a rigid motion of the ambient Euclidean space, then we say the tensegrity framework
                                                                                                                                        is rigid. See [9] and [29].
                                                                                                                                              For the recognition problem (i) there has been much work done using the concept
                                                                                                                                        of first-order rigidity. A tensegrity framework is first-order rigid (or infinitesimally
                                                                                                                                        rigid) if the only smooth motion of the vertices, such that the first derivative of each
                                                                                                                                        member length is consistent with the constraints, has its derivative at time zero equal
                                                                                                                                        to that of the restriction of a congruent motion of Euclidean space. See 2.2 for more
                                                                                                                                        details. An equivalent dual concept says that a tensegrity framework is statically rigid
                                                                                                                                        if every equilibrium load can be resolved. See [10] or [29] for more details and a precise
                                                                                                                                        definition. Our working definition will be that of first-order rigidity as above.
                                                                                                                                              A stress in a tensegrity framework is an assignment of a scalar to each member.
                                                                                                                                        It is called a self stress if the vector sum of the scalar times the corresponding member
                                                                                                                                        vector is zero at each vertex. It is called proper if the cable stresses are nonnegative
                                                                                                                                        and the strut stresses are nonpositive (with no condition on the bars). It is called
                                                                                                                                        strict if the stress in each cable and strut is nonzero.
                                                                                                                                             1.2. First-order duality. The interplay between first-order motions and self
                                                                                                                                        stresses yields a test for first-order rigidity. Every first-order rigid tensegrity framework
                                                                                                                                        has a strict proper self stress, by a result of Roth and Whiteley [29]. We state the first-
                                                                                                                                        order stress test as follows: There is a first-order flex of a framework which strictly
                                                                                                                                        changes the length of a strut or cable if and only if every proper self stress is zero on
                                                                                                                                        the given member.


                                                                                                                                                                                                                       cable



                                                                                                                                                                                                                       bar




                                                                                                                                                                                   S                              c
                                                                                                                                                                                                                        strut

                                                                                                                                              FIG. 1. Two first-order rigid tensegrity frameworks (a, b) where cables and struts are reversed.

                                                                                                                                        In addition, if a first-order rigid bar framework has any nonzero self stress at all, one
                                                                                                                                        can change these members to cables or struts following the sign of the self stress to get
                                                                                                                                        another statically rigid tensegrity framework. In the spirit of (ii), this is a first-order
                                                                                                                                        method for generating examples of statically rigid tensegrity frameworks. See [29]
                                                                                                                                        and [35] for examples. Note that any first-order rigid tensegrity framework can have
                                                                                                                                        its cables and struts reversed to struts and cables, respectively, and it will remain
                                                                                                                                        first-order rigid. Figure 1 shows a pair of frameworks which are infinitesimally rigid
                                                                                                                                        in the plane.
                                                                                                                                              1.3. Prestress stability and second-order rigidity. In .this paper, we define
                                                                                                                                        two other classes of frameworks, those that are prestress stable and those that are
                                                                                                                                        second-order rigid. We call a tensegrity framework prestress stable if it has a proper
                                                                                                                                        strict self stress such that a certain energy function, defined in terms of the stress and
                                                                                                                                        defined for all configurations, has a local minimum at the given configuration, and this
                                                                                                                                                         SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                    455

                                                                                                                                        minimum is a strict local minimum up to congruence of the whole framework. (See
                                                                                                                                        3.3 for the precise formula for this energy function.)
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                              Prestress stability is a concept we have borrowed from structural engineering.
                                                                                                                                        The "principle of least work" is the motivation behind the definition of our energy
                                                                                                                                        functions. If a certain configuration of a framework corresponds to a local minimum
                                                                                                                                        (modulo rigid motions) of an energy function, which is the sum of the energies of all
                                                                                                                                        the members, then it is clear that the framework is rigid. When the usual second
                                                                                                                                        derivative test detects such a minimum, this corresponds to prestress stability. Pel-
                                                                                                                                        legrino and Calladine [28] describe certain matrix rank conditions that are necessary
                                                                                                                                        but not sufficient for prestress stability. However, their condition essentially ignores
                                                                                                                                        the basic positive definite conditions. See [5] for an improved version, though. For
                                                                                                                                        engineering calculations, the stress-strain relation in each member is given, and this
                                                                                                                                        information determines the corresponding energy function. On the other hand, for
                                                                                                                                        the simpler mathematical recognition problem (i), one is free to choose the member
                                                                                                                                        energy functions at will.
                                                                                                                                              A tensegrity framework is second-order rigid if every smooth motion of the ver-
                                                                                                                                        tices, which does not violate any member constraint in the first and second derivative,
                                                                                                                                        has its first derivative trivial; i.e., its first derivative is the derivative of a one parameter
                                                                                                                                        family of congruent motions.




                                                                                                                                                  Nonrigid
                                                                                                                                                 Figure 3a


                                                                                                                                                               i!Ii                                                    J)i   Figure 16d




                                                                                                                                             FIG. 2. A diagram of the hierarchy of "rigidity" (numbers refer to illustrative examples).

                                                                                                                                             A series of basic results shows that for any tensegrity framework, first-order rigid-
                                                                                                                                        ity (i.e., infinitesimal rigidity) implies prestress stability, which implies second-order
                                                                                                                                        rigidity, which implies rigidity, and none of these implications can be reversed. See
                                                                                                                                        Figure 2, where the figure numbers refer to examples seen later in this paper that lie
                                                                                                                                        only in that region of the diagram. This extends the second-order rigidity results of [6]
                                                                                                                                        for bar frameworks and places prestress stability between first-order and second-order
                                                                                                                                        rigidity.
                                                                                                                                             1.4. The second-order stress test. Information about a framework, or a
                                                                                                                                        class of frameworks, may come in various forms, and it can be useful to relate these
                                                                                                                                        different forms for the situation at hand. For example, to test the first-order rigidity
                                                                                                                                        of a tensegrity framework we may use both the self stresses and the first-order flexes,
                                                                                                                                        as in the first-order stress test.
                                                                                                                                             We extend this first-order duality to the second-order situation. Regard any stress
                                                                                                                                        as the constant coefficients of a quadratic form on the space of all configurations as well
                                                                                                                                        as the space of first-order flexes. This is a "homogeneous" energy function. Suppose
                                                                                                                                        we have a fixed first-order flex of a given framework, and we wish to know when that
                                                                                                                                        first-order flex extends to some second-order flex. Our second-order stress test states
                                                                                                                                        the following: A second-order flez exists if and only if for every proper self stress of
                                                                                                                                        the framework the quadratic form it defines is nonpositive when evaluated at the given
                                                                                                                                        456                             R. CONNELLY AND W. WHITELEY

                                                                                                                                        first-order flez. Thus information about proper self stresses of a framework, as well
                                                                                                                                        as first-order flexes, can provide information about second-order rigidity. The proof
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        amounts to observing that the (inequality and equality) constraints of second-order
                                                                                                                                        rigidity and our dual stress condition is a special case of the "Farkas alternative" (as
                                                                                                                                        used in linear programming duality).
                                                                                                                                             It is also possible to sharpen the second-order stress test to provide necessary
                                                                                                                                        and sufficient conditions to detect when the second-order inequalities are strict. This
                                                                                                                                        sharpening is a generalization of the first-order stress test. The sharpened second-
                                                                                                                                        order stress test can be helpful not only in detecting second-order rigidity but also
                                                                                                                                        quite often in detecting when there is an actual continuous flex that has the cable and
                                                                                                                                        strut conditions slacken at the second-order.
                                                                                                                                             1.5. Roth’s conjecture. As an application of these methods we verify a con-
                                                                                                                                        jecture of Roth about polygons in the plane in [29]. In their Lectures on Lost Mathe-
                                                                                                                                        matics [18, 19], Griinbaum and Shepard conjectured that if one has a framework G(p)
                                                                                                                                        in the plane with the points as the vertices of a convex polygon, bars on the edges, and
                                                                                                                                        cables inside connecting certain pairs of the vertices (Figure 3a, c) in such a way that
                                                                                                                                        the framework is rigid in the plane (Figure la), then reversing the cables and bars to
                                                                                                                                        get ((p) (Figure lb) preserves rigidity. (They also observed that starting with cables
                                                                                                                                        on the outside and bars inside does not necessarily preserve rigidity (Figure 3b, a).)
                                                                                                                                             If Griinbaum and Shephard’s polygonal frameworks are rigid because they are
                                                                                                                                        infinitesimally rigid, then it follows that the reversed framework is also infinitesimally
                                                                                                                                        rigid and therefore rigid. Roth’s conjecture was that all rigid convex polygons with
                                                                                                                                        cables on the inside were indeed infinitesimally rigid. For example, Figure 3c shows a
                                                                                                                                        regular octagon with bars on the edges and fourteen cables on the inside. It is easy to
                                                                                                                                        check that this framework is not infinitesimally rigid. Thus Roth’s conjecture implies
                                                                                                                                        that this framework is not rigid since if it were rigid, it would be infinitesimally rigid.
                                                                                                                                        The reader is invited to find the motion of the vertices in the plane directly. (See
                                                                                                                                        Remark 6.2.1.)




                                                                                                                                            FIG. 3. Framework (b) is rigid, but framework (a), where cables and struts are reversed, is not.
                                                                                                                                        Framework (c) is not first-order rigid and is not rigid, illustrating Roth’s conjecture.


                                                                                                                                             Meanwhile, Connelly [7] showed that any proper self stress coming from one
                                                                                                                                        of Griinbaum and Shepard’s polygonal frameworks G(p) had an associated negative
                                                                                                                                        semidefinite quadratic form with nullity three. Equivalently the reversed framework
                                                                                                                                        ((p) had a positive semidefinite quadratic form with nullity three. Then it is easy
                                                                                                                                        to show that (p) is rigid by showing that (globally) there is no other noncongruent
                                                                                                                                        configuration satisfying the bar and cable constraints. This global type of rigidity
                                                                                                                                        is somewhat different from infinitesimal rigidity. Neither infinitesimal rigidity nor
                                                                                                                                        global rigidity implies the other. However, the energy functions used to prove the
                                                                                                                                        global rigidity also imply prestress stability. Thus Griinbaum’s conjecture was proved
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                              45?

                                                                                                                                        and generalized in one direction, but Roth’s conjecture, a generalization in another
                                                                                                                                        direction, was not proved.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                              1.6. The proof of Roth’s conjecture. The idea behind our proof of Roth’s
                                                                                                                                        conjecture is the following. We observe that the conditions for a strict second-order
                                                                                                                                        flex, in the second-order stress test, are satisfied by any one of Griinbaum and Shep-
                                                                                                                                        ard’s frameworks G(p), since any proper self stress defines a negative semidefinite
                                                                                                                                        quadratic form which is negative definite on any space of nontrivial first-order flexes.
                                                                                                                                        Thus if there is any nontrivial first-order flex, it will extend to a strict second-order flex
                                                                                                                                        which in turn implies that there will be a nontrivial continuous flex of the framework.
                                                                                                                                        Thus (the contrapositive of) Roth’s conjecture is verified: if G(p) is not infinitesimally
                                                                                                                                        rigid, then G(p) is not rigid. In particular, if any one of Griinbaum and Shepard’s
                                                                                                                                        frameworks G(p) is rigid, the reversed framework (p) is both infinitesimally rigid
                                                                                                                                        and globally rigid.
                                                                                                                                              In an appendix we summarize a series of "replacement principles" which describe
                                                                                                                                        when and how one can switch between bars and cables or struts and preserve the
                                                                                                                                        various levels of rigidity or flexibility.
                                                                                                                                             2. Review of tensegrity frameworks.             Throughout this paper the word
                                                                                                                                        tensegrity is used to describe any framework with cables--each cable determines a
                                                                                                                                        maximum distance between two points, struts--each strut determines a minimum dis-
                                                                                                                                        tance between two points, and bars--each bar determines a fixed distance between
                                                                                                                                        two points. Statically, cables can only apply tension and struts can only apply com-
                                                                                                                                        pression. We partition the edges of our graph into three disjoint classes        E_ for
                                                                                                                                        cables, E0 for bars, and E+ for struts, creating a signed graph G (V; E_,Eo, E+).
                                                                                                                                        In our figures, cables are indicated by dashed lines, struts by double thin lines, and
                                                                                                                                        bars by single thick lines (see Figure 1). General references for this chapter are [8, 9,

                                                                                                                                             2.1. Rigidity.
                                                                                                                                             DEFINITION 2.1.1. A tensegrity framework in d-space G(p) is a signed graph
                                                                                                                                        (V; E_, E0, E+), and an assignment p E IRdv such that each pi IRd corresponds
                                                                                                                                        to a vertex of G, where p     (pl,...,pv) is a configuration. The members in E_
                                                                                                                                        are cables, the members in Eo are bars, and the members in E+ are struts. A bar
                                                                                                                                        framework is a tensegrity framework with no cables or struts; i.e., E Eo.
                                                                                                                                             DEFINITION 2.1.2. A tensegrity fumework G(p) dominates the tensegrity frame-
                                                                                                                                        work G(q), written G(p) _> G(q), if

                                                                                                                                                              ]Pi   Pjl -> Iqi           when     { i, j } E_
                                                                                                                                                              IPi   PJl Iqi              when     { i, j} Eo,
                                                                                                                                                              IPi   PJl -< Iqi           when     { i, j} e E+
                                                                                                                                             A tensegrity framework G(p) is rigid in ]Rd if any of the following three equivalent
                                                                                                                                        conditions holds [9] or [29]"
                                                                                                                                             (a) there is an > 0 such that if G(p) >_ G(q) and IP-ql < then p is
                                                                                                                                        congruent to q; or
                                                                                                                                             (b) for every continuous path, or continuous flex, p(t) e IRd, p(0) p, such
                                                                                                                                        that G(p) _> G(p(t)) for all 0 <_ t <_ 1, then p is congruent to p(t) for all 0 <_ t <_ 1;
                                                                                                                                        or
                                                                                                                                             (c) for every analytic path, or analytic flex, p(t) E IRd, p(0) p, such that
                                                                                                                                        G(p) _>_ G(p(t)) for all 0 <_ t <_ 1, then p is congruent to p(t) for all 0 <_ t <_ 1.
                                                                                                                                        458                             R. CO NNELLY AND W. WHITELEY

                                                                                                                                            2.2. First-order rigidity.


                                                                                                                                                                                          -
                                                                                                                                            DEFINITION 2.2.1. A first-order flex, or an infinitesimal flex, of a tensegrity
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        framework G(p) is an assignment p’ V IRn, p’(vi)                     p,
                                                                                                                                                                                                    such that for each edge
                                                                                                                                        {i, j} e E (Figure 4),
                                                                                                                                                           (pj    p) (p        p) _< 0        for cables {i, j} E E_,
                                                                                                                                                           (p     pi) (p       p) 0           for bars {i, j } E E0,
                                                                                                                                                           (pj    pi) (p       p) _> 0        for struts {i, j} E+.
                                                                                                                                        The dot product of two vectors X, Y is indicated by XY or X. Y.




                                                                                                                                                             cable                     bar                     strut
                                                                                                                                                 FIG. 4. Some first-order motions (velocities) permitted by cables, bars, and struts.

                                                                                                                                             DEFINITION 2.2.2. A first-order flex p’ of a tensegrity framework G(p) is trivial
                                                                                                                                        if there is a skew symmetric matrix S and a vector t such that p Sp + t for all
                                                                                                                                        vertices i.
                                                                                                                                             DEFINITION 2.2.3. A tensegrity framework G(p) is first-order rigid (or infinites-
                                                                                                                                        imally rigid) if every first-order flex is trivial and first-order flexible otherwise.
                                                                                                                                              Let


                                                                                                                                                                                              p;
                                                                                                                                        be regarded as a column vector in Ia, where each p                 IRa,       1,..., v. Then R(p)
                                                                                                                                        is the e-by-dv matrix defined by



                                                                                                                                                                     R(p)p*         (pj    p)       (P; p)

                                                                                                                                        See [9] or [29]. R(p) is called the rigidity matrix for the framework G(p). Notice that
                                                                                                                                        a first-order flex of a bar framework is a solution to the linear equations

                                                                                                                                                                                   n(p)p*          0.

                                                                                                                                             Remark 2.2.1. A basic theorem of the subject says that first-order rigidity for a
                                                                                                                                        tensegrity framework implies rigidity for the framework. (See [9, 29].)
                                                                                                                                             DEFINITION 2.2.4. A first-order flex p is an equilibrium flex if p. q 0 for all
                                                                                                                                        trivial first-order flexes q.
                                                                                                                                             Physically, a first-order flex is a velocity vector field associated with the configu-
                                                                                                                                        ration, and it turns out that an equilibrium flex is a vector field such that the linear
                                                                                                                                        and angular momentum is preserved (Figure 5).
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                   459
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                               a                                                  b
                                                                                                                                              FIG. 5. The cable (Pl, P2) in example (a) is unstressed because it can be shortened, while the
                                                                                                                                        strut (P3, P4) in (b) is unstressed because it can be lengthened.

                                                                                                                                             2.3. Stresses.
                                                                                                                                             DEFINITION 2.3.1. A stress w on a tensegrity framework G(p) is an assignment
                                                                                                                                        of scalars wj    ozj to the edges of G, where       (... ,wj,...) E IRe, and e is the
                                                                                                                                        number of edges of G.
                                                                                                                                             A stress w on a tensegrity framework is a self stress if the following equilibrium
                                                                                                                                        condition holds at each vertex i"

                                                                                                                                                                             EJ (pj p) O,
                                                                                                                                                                                  oij


                                                                                                                                        where the sum is taken over all j with {i, j} E E.
                                                                                                                                             A self stress w is called a proper self stress if (a) j _> 0 for cables {i, j} E_
                                                                                                                                        and (b) j <_ 0 for struts {i, j} E+.
                                                                                                                                        There is no condition for a bar.
                                                                                                                                             A proper self stress is strict if the inequalities in (a) and (b) are strict.
                                                                                                                                             With this notation a self stress w is a solution to the linear equations wR(p) 0,
                                                                                                                                        and w is a proper self stress if each of the wj corresponding to cables and struts have
                                                                                                                                        the proper sign. The following is shown in [35].
                                                                                                                                             THEOREM 2.3.2 (first-order stress test). Let G(p) be a tensegrity framework,
                                                                                                                                        where {i, j} is a fixed cable or strut. There is a first-order flex p’ for G(p) such that

                                                                                                                                                                           (pi- p). (p- p})           : 0,
                                                                                                                                        which means that a cable {p, pj} is shortened or a strut {p, pj} is lengthened, to
                                                                                                                                        first-order, if and only if for every proper self stress w for G(p) has ozj O.
                                                                                                                                             It is helpful to change the presentation of a stress. Let w (..., wj,...) IR
                                                                                                                                        be a stress for G(p). Define a v-by-v symmetric matrix, the reduced stress matrix
                                                                                                                                        by se{ting the (i, j) entry to be

                                                                                                                                                                        ij      { EkWk
                                                                                                                                                                                  -wj        if
                                                                                                                                                                                             if        =j
                                                                                                                                                                                                         j,


                                                                                                                                        Denoting by pk the kth coordinate of p             ]ad, k       1,..., d, the expression



                                                                                                                                                                          k=l
                                                                                                                                                                                                      Pvk
                                                                                                                                        460                                 R. CONNELLY AND W. WHITELEY

                                                                                                                                        is a quadratic form on the vd-dimensional space of coordinates of all points of the
                                                                                                                                        configuration. Reordering the coordinates by the order of the points yields
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                                               IPl
                                                                                                                                        where )T represents the transpose operation. This defines the stress matrix which
                                                                                                                                        is, up to permutation of the coordinates of p, just k "copies" of f. It is easy to check
                                                                                                                                                                                                                                   ,
                                                                                                                                        that if p, q E IRvd, w E IRe, then

                                                                                                                                        (1)                   wR(p)q- pTfq            E Wi (pi- pj). (qi- q).
                                                                                                                                                                                       ij

                                                                                                                                        Thus Ft is just the matrix of a bilinear form in the coordinates of p and q, and it turns
                                                                                                                                        out that w is a self stress if pT 0.
                                                                                                                                              3. Prestress stability.
                                                                                                                                             3.1. The energy principle. If a cable is stretched, the energy in the cable
                                                                                                                                        increases. Similarly, if a strut is shortened, or a bar is changed in length, the energy
                                                                                                                                        increases. We put these together in the following energy function"

                                                                                                                                        (2)                                 H*(q)   E fJ (IqJ q12),
                                                                                                                                                                                     j

                                                                                                                                        where
                                                                                                                                                      for each cable {i, j},          is strictly monotone increasing,
                                                                                                                                                      for each strut {i, j},          is strictly monotone decreasing,
                                                                                                                                                      for each bar {i, j}, fij        has a strict minimum at ]pj pi] 2.
                                                                                                                                        See Figure 6.

                                                                                                                                                f.j




                                                                                                                                                          Lij     Iqi.qjl               Lij      Iqi-qj                  Lij     Iqi-qjl
                                                                                                                                                cable                         bar                              strut
                                                                                                                                             FIG. 6. At the given configuration, the energy function is increasing on cables, a local minimum
                                                                                                                                        on bars, and decreasing on struts.

                                                                                                                                             We have the following Theorem 3.1.1.
                                                                                                                                             THEOREM 3.1.1 (energy principle). If such an H* has a local minimum at p
                                                                                                                                        which is strict up to congruence in some neighborhood of p in IRdv, then the framework
                                                                                                                                        G(p) is rigid.
                                                                                                                                             Proof. Any nearby q with G(q) _< G(p) will have fi. ([ q[2)
                                                                                                                                        for all members. Since this makes H*(q) _< H*(p), we conclude that q is congruent
                                                                                                                                        to p. This makes G(p) rigid, by Definition 2.1.2(a) of rigidity.
                                                                                                                                                        SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                        461

                                                                                                                                             Remark 3.1.1. It turns out that any rigid tensegrity framework G(p) will have
                                                                                                                                        "some" energy functions that make H* a minimum at p, but they would only satisfy
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        certain "relaxed" conditions (2). Later it will be necessary to use conditions (2) as
                                                                                                                                        they stand.
                                                                                                                                             3.2. Stiffness matrix, stress matrix decomposition. We apply the energy
                                                                                                                                        principle for functions H*(p) which have their minimum by the second derivative
                                                                                                                                        test. Let equation (2) define an energy function, where each fij is twice continuously
                                                                                                                                        differentiable and chosen so that the first derivative fj (IPj- Pil 2)      ij for each
                                                                                                                                        member, wij     :  0 are scalars for all cables and struts, and the second derivative
                                                                                                                                        f" (IPJ Pil 2) cij > 0 for all members. Note that (3) insures that is a strict and
                                                                                                                                        proper stress. We suppose that p is a fixed particular configuration.
                                                                                                                                             To find a local minimum, the first step is to find a critical point. Note that p
                                                                                                                                        is a critical point for H* if and only if the directional derivative at p is zero for all
                                                                                                                                        directions p*. Hence, we compute the directional derivative of this energy function in
                                                                                                                                        the direction p* starting from p.
                                                                                                                                             Let p(t) p + tp*. So Dt(p(t)) p*, where Dt represents differentiation with
                                                                                                                                        respect to t. We compute the derivative of H*(p(t)) with respect to t,

                                                                                                                                                      Dt(H*(p(t)))     E fi(Ipj(t)12) [2(pj (t) pi(t)) (p; p’)].
                                                                                                                                                                          ij

                                                                                                                                        The directional derivative is then the above function evaluated at t- 0.

                                                                                                                                                   Dt(H*(p(t)))[t=             Efij(Ipj
                                                                                                                                                                               ij
                                                                                                                                                                                          pil 2) [2(pj   pi)   (p; p)].

                                                                                                                                        Since fij(IPj-   PI )    a;ij, using (1) we have


                                                                                                                                                   Dt(H*(p(t)))      [t:o 2 E wij(pj Pi) (P P) 2wR(p)p*.
                                                                                                                                                                                    ij


                                                                                                                                             By the above calculation p is a critical point for H* if and only if 2wR(p)p* 0
                                                                                                                                        for all p* if and only if wR(p) 0 if and only if w is a self stress for G(p).
                                                                                                                                             If w is a self stress on G(p), we use the second derivative test to check whether
                                                                                                                                        H* has a strict minimum at p, up to congruences. For each direction p* we calculate
                                                                                                                                        the second derivative along the path p(t) and then evaluate when t 0 and p(0) p.

                                                                                                                                                      Dt [H*(p(t))] t=O




                                                                                                                                        The constant cij is often called the stiffness coefficient for the member {i, j} and in
                                                                                                                                        physics it is normally a function of the Young modulus of the material forming the
                                                                                                                                        member, the rest length of the member, and the cross-sectional area of the member.
                                                                                                                                        462                            R. CONNELLY AND W. WHITELEY

                                                                                                                                             The rigid congruences of p form a submanifold in the space of all configurations,
                                                                                                                                        and it is clear that H* is constant on this set. Thus when p* is a trivial infinitesimal
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        flex of G(p) it is easy to see that both the first and second derivative of H* along a
                                                                                                                                        path in the direction of p* are zero. (This can also be seen by a direct calculation.)
                                                                                                                                        We conclude with Proposition 3.2.1.
                                                                                                                                             PROPOSITION 3.2.1. The energy function H* has a strict local minimum, up to
                                                                                                                                        congruence, if the quadratic form

                                                                                                                                                H(p*)   E 2wij (p; p’) (p; p’) + E 4cj[(pj pi) (p; p’)]2
                                                                                                                                                         ij                                 ij


                                                                                                                                        regarded as a function of the coordinates of p*, satisfies H(p*) >_ 0 for all p*, and
                                                                                                                                        H(p*)      0 if and only if p* is a trivial infinitesimal flex of G(p). In other words H
                                                                                                                                        is positive definite on any complement of the trivial infinitesimal flexes.
                                                                                                                                             Note that each fj for each cable and strut is a monotone function with nonzero
                                                                                                                                        derivative. For that reason we know that the self stress is strict and proper. In other
                                                                                                                                        words the self stress w is nonzero with the correct sign on each cable and strut.
                                                                                                                                             What we have done is calculate the Hessian H as a quadratic form for the function
                                                                                                                                        H*. Note, however, that H itself is not the sum of energy functionals of the members
                                                                                                                                        of G. Thus the energy principle does not apply directly to H but applies only because
                                                                                                                                        H* is locally approximated by H.
                                                                                                                                             We now rewrite the formula for H in terms of the rigidity matrix. Let C denote
                                                                                                                                        the dv-by-dv diagonal matrix with entries cj, where its rows and columns correspond
                                                                                                                                        to the members of G. If {i, j} is a member of G, then the corresponding diagonal
                                                                                                                                        entry is cj.
                                                                                                                                                                   2R(p*)p* / 4(p*)Tn(p)TCR(p)p*
                                                                                                                                                                   H
                                                                                                                                                                   2(p*)Ttp* / 4(p*)TR(p)TCR(p)p*
                                                                                                                                                                   (p*)T[2 / 4R(p)TCR(p)]p *.
                                                                                                                                        In structural engineering, the matrix R(p)TCR(p) is called the stiffness matrix of
                                                                                                                                        the framework, t is the geometric stiffness matrix or the stress matrix, and 2[ +
                                                                                                                                        2R(p)TCR(p)] is the tangential stiffness matrix. The matrix R(p)TCR(p) is clearly
                                                                                                                                        positive semidefinite with the first-order flexes in its kernel. If the framework is in-
                                                                                                                                        finitesimally rigid, then t      0 can be used in the above. The interesting cases for
                                                                                                                                        us occur when there are some nontrivial infinitesimal flexes and some nonzero self
                                                                                                                                        stresses.
                                                                                                                                             Remark 3.2.1. The condition of Proposition 3.2.1 is a particular kind of stability
                                                                                                                                        which corresponds to the engineer’s concept of first-order stiffness [30]. If we take
                                                                                                                                        gradients of this energy function, we find that if the force at the ith joint is F, then
                                                                                                                                        this set of forces is resolved, at first-order, by a displacement p* of the joints, where

                                                                                                                                              Fi- AH          2   E wij(p; p)+ 4 E [(pj Pi) (P; P’)] (Pj P).
                                                                                                                                                                                      cij



                                                                                                                                        Regarding the forces as one column vector F         (FT,..., FT) T, we get
                                                                                                                                                                       F   [2a + 4R(p)TCR(p)]p *.
                                                                                                                                        All equilibrium loads are resolved if and only if the matrix [2t + 4R(p)TCR(p)] is
                                                                                                                                        invertible when restricted to the orthogonM complement of the trivial motions. In this
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                         463

                                                                                                                                        case, the deformation p* resolves the load [2t) + 4R(p)TCR(p)]p *. This is a feasible
                                                                                                                                        physical response of the structure, corresponding to positive work by the force, if and
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        only if p* is in the same direction as F or p*. F >_ 0, with equality only if F 0. This
                                                                                                                                        is a restatement of the fact that H is positive definite on a complement of the trivial
                                                                                                                                        motions.
                                                                                                                                             If H is only positive semidefinite on a complement of the trivial infinitesimal
                                                                                                                                        motions, then there is a direction p* for which there is no change in the energy up to
                                                                                                                                        the second derivative. It may turn out that there will still be third- or higher-order
                                                                                                                                        effects of a real energy which produce rigidity. However, if H is indefinite there is a
                                                                                                                                        direction p* in which the energy strictly decreases.
                                                                                                                                             Remark 3.2.2. Looking at this discussion in terms of the physics we can also
                                                                                                                                        understand the rule of the energy functions. If H strictly decreases in the direction
                                                                                                                                        p*, then any smooth energy function H* with the equilibrium stresses coij as the first
                                                                                                                                        derivatives and the cij as the second derivatives for each member will have a local
                                                                                                                                        maximum at p along the line p / tp*. If released with this energy in the direction
                                                                                                                                        of p*, the framework will continue to move while seeking a smaller overall energy.
                                                                                                                                        It is also possible to interpret the behavior of the framework in terms of Lagrange
                                                                                                                                        multipliers.
                                                                                                                                             3.3. Definition of prestress stability. Recall that if Q is a quadratic form
                                                                                                                                        on a finite-dimensional vector space, then there is a symmetric matrix A such that
                                                                                                                                        Q(p) pTAp, where p is a vector written as coordinates with respect to some basis
                                                                                                                                        of the vector space. If Q(p) _> 0 for all vectors p, then Q (or A) is called positive
                                                                                                                                        semidefinite. The zero set of Q is the set of vectors p such that Q(p) 0. If Q is
                                                                                                                                        positive semidefinite and the zero set consists of just the zero vector, then Q is called
                                                                                                                                        positive definite.
                                                                                                                                             DEFINITION 3.3.1. We say a tensegrity framework G(p) is prestress stable if
                                                                                                                                        there is a proper self stress w and nonnegative scalars cij (where {i, j} is a member of
                                                                                                                                        G) such that the energy function regarded as quadratic form in the coordinates of p*

                                                                                                                                                                    wij(p   p)2 +        cij   [(pi pj). (p   p)]2
                                                                                                                                                               ij                   ij


                                                                                                                                        is positive semidefinite, cij   0 when coij 0 and {i, j} is a cable or strut, and only the
                                                                                                                                        trivial infinitesimal flexes of p are in the kernel of H. In this case we say w stabilizes
                                                                                                                                        G(p). The cij are called the stiffness coefficients as in 3.2. We have dropped the
                                                                                                                                        constants 2 and 4 that appeared in 3.2 for simplicity.
                                                                                                                                             Remark 3.3.1. If, for some member {i, j}, H has wiy 0 but cij > 0, then for
                                                                                                                                        the energy principle to apply, the member must be a bar. Imagine a single cable,
                                                                                                                                        which has no nonzero self stress. It is certainly not rigid, but it would be prestress
                                                                                                                                        stable with the zero self stress if we did not insist that cij     0 when wij     0. This
                                                                                                                                        is why the definition insists that each cable or strut which appears with a zero stress
                                                                                                                                        does not appear in the formula at all.
                                                                                                                                             Thus if any G(p) is prestress stable, stabilized at w, then we might as well change
                                                                                                                                        G(p) to have struts only for those members where wij < 0 and cables only for those
                                                                                                                                        members where wij > 0, deleting any cables or struts with a zero stress.
                                                                                                                                             Note also that if we regard unstressed members as not being in G, then increasing
                                                                                                                                        any cj keeps H positive definite (if it already was) and so we may assume they are all
                                                                                                                                        equal to each other, assuming that we are only interested in recognizing the rigidity
                                                                                                                                        of the framework. Thus if co stabilizes G(p) with all cables and struts stressed, with
                                                                                                                                        464                           R. CONNELLY AND W. WHITELEY

                                                                                                                                        stiffness coefficients cij, then axcj} stabilizes G(p) with all the stiffness coefficients
                                                                                                                                        equal to one.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                              PROPOSITION 3.3.2. If a tensegrity framework G(p) is prestress stable for a self
                                                                                                                                        stress w, then G(p) is rigid.
                                                                                                                                              Proof. The positive definite property of H guarantees a strict local minimum
                                                                                                                                        modulo trivial first-order flexes of p. Since v2ij 0 for all the cables and struts of G
                                                                                                                                        that appear in H*, we have the strictly monotone property of their energy functions,
                                                                                                                                        near p. Thus the energy principle applies to show G(p) is rigid.
                                                                                                                                              Remark 3.3.2. We will. see, by Theorem 4.4.1, that if G(p) is prestress sta-
                                                                                                                                        ble, then G(p) is second-order rigid and, by Theorem 4.3.1, G(p) is rigid. However,
                                                                                                                                        the present proof is much simpler since it is a direct application of the energy prin-
                                                                                                                                        ciple.
                                                                                                                                              PROPOSITION 3.3.3. If a tensegrity framework G(p) is first-order rigid, then it
                                                                                                                                        is prestress stable.
                                                                                                                                              Proof. The underlying bar framework G(p) is certainly first-order rigid; thus
                                                                                                                                        R(p)TR(p) has only the trivial infinitesimal flexes in its kernel. In other words
                                                                                                                                        R(p)TR(p) is positive definite on the equilibrium infinitesimal motions perpendic-
                                                                                                                                        ular to the trivial infinitesimal motions in IRd. By [29] there is a proper self stress
                                                                                                                                        w which is nonzero on each cable and strut. By choosing w sufficiently small, then
                                                                                                                                        t2 + R(p)TR(p) also will be positive definite on the equilibrium infinitesimal flexes
                                                                                                                                        restricted to the compact unit sphere. Thus G(p) is prestress stable.           I:]
                                                                                                                                              Often it is convenient to assume that a proper stress o for G(p) is strict; i.e.,
                                                                                                                                        wij     0 for every cable or strut. If we are willing to consider subframeworks of G(p),
                                                                                                                                        we need only consider strict self stresses for prestress stability.
                                                                                                                                              Remark 3.3.3. Pellegrino and Calladine [28] use a different analysis of the rigid-
                                                                                                                                        ifying effect of a prestress. (See also [4].) Given a framework G(p) with a self stress w
                                                                                                                                        and a set of generators p,...,    p   for a complementary space of nontrivial first-order
                                                                                                                                        flexes, they add k new rows to the rigidity matrix wR(pl),OzR(p2),... ,wR(p). If
                                                                                                                                        this extended matrix R*(p w) has rank vd a(d+l)       2     they say that the prestress
                                                                                                                                        "stiffens" the framework, modulo the positive definiteness of an unspecified matrix.
                                                                                                                                              If R*(p, w) does not have rank vd-d(d + 1)/2 (assuming the vertices span IRa),
                                                                                                                                        then there is a nontrivial first-order flex p’       apj satisfying wR(p)p’          0 for all
                                                                                                                                        i    1,..., k. Thus wR(p’)p’ 0 and G(p) is certainly not prestress stable for this
                                                                                                                                        self stress w. In fact, it is easy to see that their condition for stiffening is equivalent
                                                                                                                                        to requiring that the rank of a2f + R(p)TR(p) be vd d(d+l)          2   for all sufficiently
                                                                                                                                        small a (assuming that the affine span of p is at least (d- 1)-dimensional). The
                                                                                                                                        matrix that they have in mind, which must be positive definite, must be equivalent
                                                                                                                                        to t2 + R(p)TR(p) restricted to some space complementary to the space of trivial
                                                                                                                                        first-order flexes. If no positive definiteness is required, many mechanisms, such as
                                                                                                                                        collinear parallelograms, would be declared "stiff."
                                                                                                                                              On the other hand, if there is a one-dimensional space of equilibrium first-order
                                                                                                                                        flexes, then we will see that prestress stability, the rank of R*(p) dv d(d+l)      2     and
                                                                                                                                        second-order rigidity will all coincide. It is interesting that in the paper [28], most
                                                                                                                                        examples have a one-dimensional space of equilibrium flexes. See [5] for corrections, as
                                                                                                                                        well as [22-26] for a discussion of the problem of how to do the second-order analysis.
                                                                                                                                              3.4. Interpretation in terms of the stress matrix and quadratic forms.
                                                                                                                                        We now present some simple facts about quadratic forms that we will find useful later.
                                                                                                                                             LEMMA 3.4.1. Let Q1 and Q2 be two quadratic forms on a finite-dimensional
                                                                                                                                        real (inner product) vector space. Suppose that Q2 is positive semidefinite with zero
                                                                                                                                                      SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                            465

                                                                                                                                        set K, and Q1 is positive definite on K. Then there is a positive real number a such
                                                                                                                                        that QI + aQ2 is positive definite.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                             Proof. Let X denote the compact set (a sphere) of unit vectors in the inner
                                                                                                                                        product space.
                                                                                                                                                                            X={plp’p=l }.
                                                                                                                                        Recall that the zero set of Q2 is

                                                                                                                                                                         K={plQz(p)-0}.
                                                                                                                                        Let K N X C N c X be an open neighborhood of K in X such that

                                                                                                                                                                     Q (p) > o       for all     p    N.

                                                                                                                                        Such an open set N exists since K 7)X is compact, Q is positive on K \ {0} D K N X,
                                                                                                                                        and thus Q restricted to K U X must have a positive minimum rn. Then take
                                                                                                                                                               m
                                                                                                                                        N {p E XIQ(p) > }.           For similar reasons there are real constants Cl, c such
                                                                                                                                        that
                                                                                                                                                                   Ql(p)>cl for all pEX,
                                                                                                                                                              e(p)_>>0 orl pX\N.
                                                                                                                                        Then we define             We calculate for p        N 7)X,

                                                                                                                                                                     Q (p) + cQz(p) > Q (p) > o.
                                                                                                                                        For p   X\N,

                                                                                                                                                         Q1 (p) + cQ:(p)     Q (p) +       ICzlQ
                                                                                                                                                                                           82
                                                                                                                                                                                                 (p) > c + Icl > o,

                                                                                                                                        Thus Q1 + oQ2 is positive on all of X, and hence it is positive definite.     [:]
                                                                                                                                             Remark 3.4.1. Note that Q1 is allowed to be an indeterminate term on the
                                                                                                                                        whole vector space. It is only required to be positive definite on K. Note also, for
                                                                                                                                        any quadratic form given by a symmetric matrix A,..where Q(p)         pTAp, certainly
                                                                                                                                        the kernel of A is contained in the zero set of Q. If Ap 0, then Q(p) pTAp O.
                                                                                                                                        However, the converse is not true unless A is positive semidefinite. In particular the
                                                                                                                                        converse is true when A R(p)TCR(p), the stiffness matrix. Then

                                                                                                                                                      (P*)TR(p)TCR(p)P*          E [(p p’). (pj pi)]
                                                                                                                                                                                 j
                                                                                                                                                                                     cij


                                                                                                                                        and the kernel of A, assuming all the Cij > 0, is the same as the zero set of its quadratic
                                                                                                                                        form. It is also clear from the above that the kernel of A is precisely the space of all
                                                                                                                                        first-order flexes of the corresponding bar framework.
                                                                                                                                             For any tensegrity framework G(p) we recall that G(p) is the corresponding bar
                                                                                                                                        framework with all members converted to bars. We denote

                                                                                                                                          =I((p))={p’eIRvd (Pi-Pj)’(P-P)-O, {i,j}                              amemberof G}.

                                                                                                                                        In other words    is the space of first-order flexes of (p), a linear subspace of IRyd.
                                                                                                                                        Recall also that Tp is the space of trivial first-order flexes at p. (So Tp I.) Note
                                                                                                                                        466                           R. CONNELLY AND W. WHITELEY

                                                                                                                                        that if G(p) has a strict proper self stress, then the first-order stress test implies that
                                                                                                                                        I-I.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                           We now give a way of checking the prestress stability of a tensegrity framework
                                                                                                                                        which is useful for calculations later. Recall a stress o: is strict if it is nonzero on every
                                                                                                                                        cable and strut.
                                                                                                                                             PROPOSITION 3.4.2. A tensegrity framework G(p) is prestress stable for the
                                                                                                                                        strict proper self stress v if and only if the associated stress matrix ft is positive
                                                                                                                                        definite on any subspace K c I complementary to Tp.
                                                                                                                                             Proof. Assume that [ + R(p)TCR(p)] is positive semidefinite with only Tp as
                                                                                                                                        the kernel, where C is a diagonal matrix with positive stiffness coefficients. Let p E I.
                                                                                                                                        Then R(p)p’--0 and so

                                                                                                                                                                0 _< (p,)T [ + R(p)TCR(p)]p,- (p,)Tp,,

                                                                                                                                        with equality if and only if p E Tp..Thus on K, 2 is positive definite.
                                                                                                                                             Before proving the converse we remark that if p is any trivial first-order ilex at
                                                                                                                                        p, then by Definition 2.2.2 there is a d-by-d (skew symmetric) matrix S and a vector
                                                                                                                                        t IRd such that     p   Spi + t,      1,...,v. Thus


                                                                                                                                                   Ewij(P-P})               Ewi(SP-                      SEwJ(P--PJ) _0.
                                                                                                                                                                                                            J



                                                                                                                                            Now suppose t2 is positive definite on K. Let pt IRvd be arbitrary. Write
                                                                                                                                        pt   PT+PK +PE, where PT Tp, PK K, and pe E E, the (orthogonal)
                                                                                                                                        complement of I in IRyd. Since t2pT 0 R(p)pT, we have

                                                                                                                                        (4)   (p,)T [ + R(p)TCR(p)]p,- (PK + p)T [ + R(p)TCR(p)](pK + p).

                                                                                                                                        By Remark 3.4.1, the kernel of R(p)TCR(p) is I Tp + K. Now apply Lemma 3.4.1
                                                                                                                                        to the inner product space K + E, where Q1 is the quadratic form corresponding to
                                                                                                                                        gt, and Q2 is the quadratic form corresponding to R(p)TCR(p). The kernel of Q2 is
                                                                                                                                        precisely K, and we have assumed that Q1 is positive definite on K. Thus by possibly
                                                                                                                                        multiplying C by a positive constant we can assume that Ft + R(p)TCR(p) is positive
                                                                                                                                        definite on K + E. By (4), this implies that t2 + R(p)TCR(p) is positive semidefinite
                                                                                                                                        with kernel Tp, and G(p) is prestress stable.
                                                                                                                                             3.5. Examples of prestress stable frameworks. The following are examples
                                                                                                                                        of tensegrity frameworks that are prestress stable, but not first-order rigid. Thus the
                                                                                                                                        converse of Proposition 3.3.3 is false.
                                                                                                                                             In Figure 7a there is a self stress such that the outside members have a positive
                                                                                                                                        self stress. A nontrivial first-order flex is given so that one can apply Proposition
                                                                                                                                        3.4.2. Figure (Tb) is stable by a result in [7] concerning spider webs. In Figure 7b it
                                                                                                                                        is the inside members we can choose to be positive. In both of these examples there
                                                                                                                                        is a strict proper self stress such that the indicated first-order flex is nonzero only
                                                                                                                                        on vertices of members that have a positive self stress, and the given first-order flex
                                                                                                                                        generates a complementary space to the trivial flexes in the space of all first-order
                                                                                                                                                        SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                     467
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                              a                                   b
                                                                                                                                             FIG. 7. Examples of prestress stable bar frameworks that are not first-order rigid. (Nontrivial
                                                                                                                                        first-order motions are indicated).




                                                                                                                                                             \\ y IiI                                      \----I
                                                                                                                                                               \\ il I
                                                                                                                                                                   \\,//                              b
                                                                                                                                             FIG. 8. Corresponding examples of prestress stable tensegrity frameworks, where the bars have
                                                                                                                                        been replaced by cables and struts following the stabilizing self stress.

                                                                                                                                        flexes. Hence the stress matrix on this space is positive definite and the framework is
                                                                                                                                        prestress stable.
                                                                                                                                             Following Remark 3.3.1, we can change appropriate members to be cables or
                                                                                                                                        struts and preserve prestress stability, as in Figure 8.
                                                                                                                                              Can a framework be rigid but not prestress stable? Consider the next two exam-
                                                                                                                                        ples. Note that any first-order rigid bar framework with no self stress at all must have
                                                                                                                                        0 as its stabilizing self stress. But the example in Figure 9a has a self stress on part of
                                                                                                                                        the framework, and the bar can have no stress other than 0. It still is prestress stable.
                                                                                                                                              However, the example of Figure 9b is not prestress stable, because the short
                                                                                                                                        horizontal cable and the horizontal strut are unstressed and the framework becomes
                                                                                                                                        nonrigid upon their removal. Nevertheless the framework is clearly still rigid. In fact,
                                                                                                                                        built with all bars, it is prestress stable.




                                                                                                                                                                                              b
                                                                                                                                              FIG. 9. Example (a) is first-order rigid, and thus prestress stable. Example (b) is rigid but not
                                                                                                                                        prestress stable.

                                                                                                                                             Suppose we fix (or pin) certain vertices. For our purposes this can be accomplished
                                                                                                                                        by adding some first-order framework that contains these vertices and none of the other
                                                                                                                                        original vertices. If the original framework has only cables with a proper self stress
                                                                                                                                        (where the equilibrium condition only holds at the vertices that are not fixed), then
                                                                                                                                        we say that the framework is a spider web. There is a discussion of this in [9] and [36]
                                                                                                                                        as well as [7]. It is clear that .spider webs are prestress stable. See Figure 10.
                                                                                                                                        468                           R. CONNELLY AND W. WHITELEY
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                        FIG. 10. This example is a spider web and thus prestress stable.




                                                                                                                                                a                                           b
                                                                                                                                                       FIG. 11. Two prestress stable tensegrity frameworks in three-space.

                                                                                                                                              In three-space there are many examples of prestress stable but not necessarily
                                                                                                                                        infinitesimally rigid tensegrity frameworks, such as in Figure 11.
                                                                                                                                              Figure 11a is a regular cube with its main diagonals as struts and its edges as
                                                                                                                                        cables. Examples such as in 11b can be obtained by taking any convex polyhedron
                                                                                                                                        with a triangular face (in this case a cube with its near upper corner truncated),
                                                                                                                                        choosing a point p0 close to that face, and joining p0 to all the other vertices of the
                                                                                                                                        polyhedron with struts and making all the edges of the polyhedron cables except the
                                                                                                                                        triangle which is composed of struts. Again it turns out that there is a strict proper
                                                                                                                                        self stress w, and t is positive semidefinite with only the affine motions in the kernel.
                                                                                                                                        This example is closely related to three-dimensional spider webs. (See [36].)
                                                                                                                                              Another three-dimensional example can be obtained by taking a tetrahedron and
                                                                                                                                        putting struts on each of the six edges and some prestressed spider web on the inside
                                                                                                                                        of each triangular face, as in Figure 12.
                                                                                                                                              Each face is prestress stable even in IRa so the sum of the energy functions is
                                                                                                                                        positive semidefinite with only the first-order flexes that are trivial on each face in the
                                                                                                                                        kernel. But since the tetrahedron itself is first-order rigid, flexes which are trivial on
                                                                                                                                        each face are trivial on the whole framework. The framework is prestress stable.
                                                                                                                                             3.6. Roths conjecture. Suppose G(p) has its points as the vertices of a
                                                                                                                                        convex polygon in the plane. If the exterior edges of G are cables, and all of the other
                                                                                                                                        members are struts, say, then we call it a cable-strut polygon or a c-s polygon.
                                                                                                                                             It follows from [7] that any c-s polygon that has a proper self stress w =fi 0 has Ft
                                                                                                                                        as positive semidefinite with only the affine motions in the kernel. It turns out that
                                                                                                                                        the affine motions are never a first-order flex of such a framework [36]. Thus such an
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                     469
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                              FIa. 12. A prestress stable tetrahedvn with cables in the faces and struts on the edges.




                                                                                                                                                                        FIG. 13. A cable-strut (c-s) polygon.

                                                                                                                                        w also stabilizes G(p), and thus G(p) is prestress rigid. Note that such a c-s polygon
                                                                                                                                        need not be first-order rigid. In the case of Figure 13, the six vertices lie on an ellipse,
                                                                                                                                        and by a classical result (see [3] and [34]), the framework has a strict proper self stress
                                                                                                                                        and a nontrivial first-order flex. So this framework is prestress stable, but it is not
                                                                                                                                        first-order rigid.
                                                                                                                                             On the other hand Roth conjectured that any rigid b-c polygon (bars on the
                                                                                                                                        outside, cables inside) was first-order rigid. In 6.2 we show that this is true. In Figure
                                                                                                                                        14 we show three examples of nonrigid b-c hexagons with first-order flex indicated.




                                                                                                                                              a                                  b                          c
                                                                                                                                            FIG. 14. Examples of bar-cable (b-c) polygons, with nontrivial first-order motions indicated.

                                                                                                                                              For the three frameworks in Figure 14, the six vertices of each configuration form
                                                                                                                                        a regular hexagon. For the first two cases, there are certain other configurations for
                                                                                                                                        the same tensegrity graph (but still a convex b-c polygon) such that the framework
                                                                                                                                        is rigid. This is not true for the last case, though. The reader is invited to find the
                                                                                                                                        continuous nontrivial flex of each of these frameworks. But see 6.2 for a proof that
                                                                                                                                        the flex exists.
                                                                                                                                              Following [29] we see that there are many cabling schemes that guarantee first-
                                                                                                                                        order rigidity, as in Figure 15.
                                                                                                                                        470                             R. CONNELLY AND W. WHITELEY
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                         a        Cauchy Polygon           b     Griinbaum polygon          C generalized Grtinbaum polygon
                                                                                                                                                              FIG. 15. Examples of first-order rigid bar-cable polygons.

                                                                                                                                             Consider a b-c hexagon with four cables. One can see that either it contains one
                                                                                                                                        of the examples of Figure 15 and thus is always first-order rigid, or it is contained in
                                                                                                                                        one of the examples of Figure 14 and thus, at least for some convex configurations, it
                                                                                                                                        is not rigid.
                                                                                                                                              4. Second-order rigidity for tensegrity frameworks.
                                                                                                                                             4.1. The definition of second-order rigidity.             Our definition of second-
                                                                                                                                        order rigidity for tensegrity frameworks comes from differentiating the equation
                                                                                                                                        Ipj(t) pi(t)l 2
                                                                                                                                        rigidity for bar
                                                                                                                                                              Litwice. This generalizes the previous definition of second-order
                                                                                                                                                         frameworks   in [7].
                                                                                                                                             DEFINITION 4.1.1. A second-order flex (p’, p") for a tensegrity framework G(p)
                                                                                                                                        is a solution to the following constraints, where p and p" are configurations in IRa
                                                                                                                                        (each regarded as an associated pair of vectors p and p’ to each point pi).
                                                                                                                                              (a) For {i,j} a bar, (pi-pj).(p-p}) 0 and Ip-p12+(pi-pj).(pT-py) 0.
                                                                                                                                              (b) For {i,j} a cable, either (pi- pj). (p- p}) < 0 or (pi- pj). (p- p}) 0
                                                                                                                                        and   IP   Pj + (P- Pj)" (P’- Pj) < 0.
                                                                                                                                              (c) For {i,j} a strut, either (pi pj). (p- p}) > 0 or (pi- pj). (p- p) 0
                                                                                                                                        and ]p- pj] + (p pj). (p’- py) >_ 0.
                                                                                                                                             A tensegrity framework is second-order rigid if all second-order flexes (p,
                                                                                                                                        have p as a trivial first-order flex. Otherwise G(p) is second-order flexible.
                                                                                                                                             Figure 16 shows second-order flexes of some tensegrity frameworks (double arrows
                                                                                                                                        for p", single arrow for p). The flex in Figure 16a is nontrivial for p. The flex in
                                                                                                                                        Figure 16b is trivial for p, but (p, p") is not the first and second derivative of a rigid
                                                                                                                                        motion of p. The flex in Figure 16c is the derivative of a rigid motion of p. Figure
                                                                                                                                        16d shows a nontrivial second-order flex in a framework which is still rigid.




                                                                                                                                              a
                                                                                                                                             FIG. 16. Examples of bar frameworks with first-order (single arrows) and second-order (double
                                                                                                                                        arrows) motions indicated.

                                                                                                                                              Since the second-order extension p is the solution of an inhomogeneous system of
                                                                                                                                                        SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                  471

                                                                                                                                        equations and inequalities, we can add any solution q of the corresponding homoge-
                                                                                                                                        neous system to p.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                            PROPOSITION 4.1.2. If (p, p’) is a second-order flex of a tensegrity framework
                                                                                                                                        G(p) and q’ is any first-order flex of G(p/, then (p’, p"+ q’) is a second-order flex
                                                                                                                                        of G(p).
                                                                                                                                             Proof. Assume that for each cable {i, j} (respectively, each bar, strut) with
                                                                                                                                        (pi    pj). (p  p.) O,
                                                                                                                                              (pi- pi). (p- p) + (pi- p). (p- p) _< 0 (respectively,                        O, _> O)
                                                                                                                                        and
                                                                                                                                                            (pi    p). (q    q) <_ 0 (respectively,             O, _> 0).
                                                                                                                                        Therefore by adding these inequalities we obtain

                                                                                                                                        (p- pj).(p-pj)+(p pj).,[(p +qi)-(py+qj)] <_0 (respectively, --0, >_0).
                                                                                                                                        These are the inequalities required for Definition 4.1.1.  E]
                                                                                                                                            If we add a multiple of p itself to any second-order extension p we can make
                                                                                                                                        the second-order extension also satisfy the second-order inequalities even for those
                                                                                                                                        members with (p- pj). (p- p) 0.
                                                                                                                                              4.2. Trivial higher-order motions. In the following p(t)       (p(t),...), 0 _<
                                                                                                                                        t _< 1 will be an analytic path in the configuration space, so p(t) IRd,     1,..., v.
                                                                                                                                        Following [6] we say that p(t) is a trivial flex if
                                                                                                                                                         p(t)     T(t)p(0)   (T(t)p (0), T(t)p2(0),..., T(t)p(0)),




                                                                                                                                                                                        _-
                                                                                                                                        where T(O) I, T(t) is a rigid motion of IR d, and T(t) is an analytic function of t. In
                                                                                                                                        particular, this means that we can write T(t)pi A(t)pi + b(t),         1,..., v, w.here
                                                                                                                                        A(t) is an orthogonal matrix, b(t) E IRd, and all the coordinates are real analytic
                                                                                                                                        functions of t.
                                                                                                                                             We next say that p, p",..., p(k), each p(J) E IRd for j 1,..., k, is a k-trivial
                                                                                                                                        flex of p if there is a trivial flex p(t) such that

                                                                                                                                                                  Dtp(t) t=0 p(J)           for j -1 2          k.

                                                                                                                                        Recall that     Drepresents the jth derivative with respect to t.
                                                                                                                                             It is easy to check that if p,..., p(k) is a k-trivial flex of any framework G(p) in
                                                                                                                                        IRd, then the analogue of equations (a) in Definition 4.1.1 holds for j 1,..., k, since
                                                                                                                                        clearly edge lengths are preserved up to any order k.
                                                                                                                                             in fact we will give a fairly explicit description of k-trivial flexes. Although this
                                                                                                                                        description is long, it seems important to be precise, given the long history of confusion
                                                                                                                                        in this area.
                                                                                                                                              We already know that 1-trivial flexes p are given by
                                                                                                                                                                        p    Spi + b’                1     v

                                                                                                                                        where S -S T is a d-by-d skew symmetric matrix and b’ IRd. See [6] or [9]. In fact
                                                                                                                                        every orthogonal matrix A sufficiently close to the identity matrix I can be written as

                                                                                                                                                                   A    eS   l+S
                                                                                                                                                                                        1
                                                                                                                                                                                            $2   +   -.   $3 +...,
                                                                                                                                        472                             R. CONNELLY AND W. WHITELEY

                                                                                                                                        where S is a skew symmetric matrix, and the above infinite series converges. It is well
                                                                                                                                        known that the exponential map

                                                                                                                                                                                              -
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                                         S        eS

                                                                                                                                        takes the tangent space of the Lie group to orthogonal matrices, which is the Lie
                                                                                                                                        algebra of the Lie group, into the Lie group itself. This exponential map is a local
                                                                                                                                        analytic diffeomorphism near I, the identity. Thus any analytic path A(t) with A(0)
                                                                                                                                        I pulls back to a path S(t) in the Lie algebra, which is itself analytic. Thus

                                                                                                                                                                                    A(t)          eS(t).

                                                                                                                                        On the other hand since e           I and thus S(0)                0 we can write

                                                                                                                                                                                         t2              t3
                                                                                                                                                                     s(t)        tSl +            +
                                                                                                                                        where each $1, $2,... is skew symmetric. Thus

                                                                                                                                                              t2            t3                                     t2         t3        2
                                                                                                                                                   I + tl +
                                                                                                                                          A(t)                -2 + --_3 +...
                                                                                                                                        Rearranging terms, which is possible since we have an absolutely convergent power
                                                                                                                                        series, we get
                                                                                                                                                                   t2                     t3             3     3
                                                                                                                                        (5       A(t)   I + tS1 + (Se + S) +                      ( Ss + -SS + -SS + $3 +
                                                                                                                                        Thus each of the matrix coefficients of       gives a parametric description of the jth
                                                                                                                                        derivative of A(t), and thus a description of a k-trivial flex of p. In particular p, p"

                                                                                                                                         ,
                                                                                                                                        is a 2-trivial flex of p if and only if there are skew symmetric matrices S, S and
                                                                                                                                        b b" ]ad such that
                                                                                                                                                                             p’     Sp + (b’,..., b’),
                                                                                                                                                                        p"= (S + $12)p + (b",..., b").
                                                                                                                                            Later it will be convenient to be able to "cancel" initial parts of a kth order flex,
                                                                                                                                        with a k-trivial flex. Thus we state the following. See [6].
                                                                                                                                            PROPOSITION 4.2.1. Let p(t), p(0) p, be an analytic path in configuration
                                                                                                                                        space such that
                                                                                                                                                                 p(J) Dtj         [p(T)],[t:0,
                                                                                                                                                                                         j 0, 1,..., k

                                                                                                                                        is k-trivial. Then there is a rigid motion T(t) of IRd, analytic in t, such that T(O)                   I
                                                                                                                                        and
                                                                                                                                                               Dt[T(t)p(t)] t=0 =0                       for j=l             k.

                                                                                                                                              Proof. We proceed by induction on k. For k                          0, there is nothing to prove. So
                                                                                                                                        we assume
                                                                                                                                                                   D{[p(t)] t=o              0      if        j   1,...,k,
                                                                                                                                        and we wish to find T(t) such that the (k / 1)st derivative is 0 as well, assuming that
                                                                                                                                        the first k + 1 derivatives are k-trivial.
                                                                                                                                                      SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                            473

                                                                                                                                             We restrict to the space spanned by pl, p2,..., pv. By adding a translation we
                                                                                                                                        have, using (5),
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                     b(J) 0, j 1,..., k + 1,
                                                                                                                                                                        Sy-O, j-1,...,k.
                                                                                                                                        Note then that Dt+lp(t)lt=o       k+lP. Define T(t) by
                                                                                                                                                                      _tk+l                 tk+l
                                                                                                                                                                     e r) S+l
                                                                                                                                                                                           (k + 1)! Sk+l +
                                                                                                                                                             ()                      I-

                                                                                                                                        We then observe, for all j     1, 2,...,

                                                                                                                                        (6)

                                                                                                                                        But
                                                                                                                                                                                    -S+
                                                                                                                                        Thus

                                                                                                                                                DJt[T(t)p(t)]t=o     { Sk+lP  0
                                                                                                                                                                                   Sk+lp    0,        for j=k+l
                                                                                                                                                                                                     for j=l,...,k   }   -0.     E]


                                                                                                                                              Remark 4.2.1. There are several ways of handling the problem of "normalizing"
                                                                                                                                        the first few derivatives. One way is the above technique; another way is to use "tie
                                                                                                                                        downs" as in [33] and discussed in [9]; a third way is to use the method described by
                                                                                                                                        [20]. (See also [9].) This normalizing is a nuisance but it is convenient to have for the
                                                                                                                                        argument used to show that second-order rigidity implies rigidity.
                                                                                                                                             The following is an immediate consequence of the definition of k-trivial and the
                                                                                                                                        formula (5).
                                                                                                                                             LEMMA 4.2.2. Let pt,...,p() be such that pt p"                     p(k-1) 0. Then
                                                                                                                                        p(k) is a l-trivial flex at p if and only if p, p’,..., p(k) is k-trivial at p.
                                                                                                                                             It is also useful to have the following.
                                                                                                                                             LEMMA 4.2.3. Let p(t) be any analytic path in configuration space such that
                                                                                                                                        p’= Dtp(t)lt=o,... p() Dtp(t)lt=o Let T(t) be any rigid motion of lRd, analytic
                                                                                                                                        in t; T(O)      I. Then Dt[T(t)p(t)]lt=o,...,Dt[T(t)p(t)]lt=o is k-trivial at p if and
                                                                                                                                        only if pt,..., p(k) is k-trivial at p.
                                                                                                                                              Proof. Since T(t) is invertible it is enough to show that if p,..., p() is k-trivial,
                                                                                                                                        then Dt[T(t)p(t)]lt=o,... ,Dt[T(t)p(t)]lt=o is k-trivial. But then p(e)_
                                                                                                                                        for g- 1,..., k for some rigid notion T(t) of IRd, analytic in t, T(0) I. But then
                                                                                                                                        clearly for t- 1,..., k,

                                                                                                                                                               Dt [T(t)p(t)] [t:o Dt [T(t)(t)p(t)] t:o’
                                                                                                                                        by expanding both sides by the product rule (6). But T(t)T(t) is again a rigid analytic
                                                                                                                                        motion of ]ad and we are done.      FI
                                                                                                                                             4.3. Second-order rigidity implies rigidity. We have generalized the notion
                                                                                                                                        of second-order flex (see [6] for bar frameworks) to general tensegrity frameworks. In
                                                                                                                                        the next theorem we will show that a nontrivial analytic flex of a tensegrity framework
                                                                                                                                        474                          R. CONNELLY AND W. WHITELEY

                                                                                                                                        gives rise to a second-order flex (p, p’) whose first-order part p is nontrivial. The
                                                                                                                                        natural idea is to take the first and second derivatives of the analytic flex evaluated
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        at the starting point. Unfortunately, this may not work because the first derivative of
                                                                                                                                        the analytic flex may be trivial, and we may have to wait for some higher derivative
                                                                                                                                        to be nontrivial. For cables and struts we use the principle that the first nonvanishing
                                                                                                                                        derivative of the member length squared has the correct sign.
                                                                                                                                             THEOREM 4.3.1. If a tensegrity framework G(p) is second-order rigid, then it
                                                                                                                                        is rigid.
                                                                                                                                              Proof. Assume G(p) is not rigid. Then we will show that G(p) is not second-order
                                                                                                                                        rigid by finding a second-order flex (q, q’) such that q is not l-trivial at p.
                                                                                                                                             Since G(p) is not rigid we know that G(p) has a nonrigid analytic flex p(t) by
                                                                                                                                        Definition 2.1.2 (c). (See [6] or [9].) Define, for g- 1, 2,...,
                                                                                                                                                                            p()       DTP(t)lt=o.
                                                                                                                                            Suppose for all k 1, 2,..., p,..., p(k) is k-trivial. Then for any {i, j}, not just
                                                                                                                                        those members of G, for all k 1, 2,...,
                                                                                                                                                                      Dt [[p(t)       pj(t)l=]
                                                                                                                                                                                                 it=0 -0
                                                                                                                                        which implies that lp(t) pj(t)l is constant in t, which implies that p(t) is rigid
                                                                                                                                        nMytic flex, contradicting the choice of p(t). Thus for some k 1, p,..., p(k) is not
                                                                                                                                        k-trivial.
                                                                                                                                             Now let k be the smallest positive integer such that p,..., p() is not k-trivial,
                                                                                                                                        fixing k. (If k 1, life is especially easy.) Applying Proposition 4.2.1, we can alter
                                                                                                                                        p(t) so that not only is p’,..., p(k-) (k- 1)-trivial, but p’         p(k-) 0. (If
                                                                                                                                        k 1 we do nothing.) Note that by Lemma 4.2.3, 0 p,..., p() is still not k-triviM.
                                                                                                                                             We observe that for any {i, j},
                                                                                                                                                                                  k




                                                                                                                                                                             2(pi- pj)" (p}) pa)).
                                                                                                                                        Hence p() is a first-order flex for G(p). By Lemma 4.2.2, p(a) is not l-trivial. Now
                                                                                                                                        we define
                                                                                                                                                                                  q     p().
                                                                                                                                             We now proceed to find q’. We still must pay attention to conditions analogous
                                                                                                                                        to first-order conditions. Recall that E0 is the set of bars of G, E_ is the set of cables
                                                                                                                                        of G, and E+ is the set of struts of G. For every n k, k + 1,..., 2k 1, define

                                                                                                                                         E={{i,j}EoUE_UE+ (pi-pj).(pe)-p))=O for=l,...,n-1}
                                                                                                                                        Note that when m       1,..., n, and {i, j}     E, or when {i, j} is a bar,
                                                                                                                                              Dp[Ip(t)     p(t)l ] t--O                (pe pe). (,
                                                                                                                                                                          =2(pi                   _()
                                                                                                                                                                                      P) "tP(m) -Pj
                                                                                                                                                                                                              ’
                                                                                                                                                                          --0 if {i,j}eEo
                                                                                                                                                                          -0 if m=l,2,...,n-1 and {i,j}E
                                                                                                                                                                          < 0 if m n and {i, j} En E-
                                                                                                                                                                          >0 if m=n and {i,j}EE+
                                                                                                                                                      SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                 475

                                                                                                                                        since either p(e)    0 or p(m-e) 0 if t 1,..., m- 1 _< 2k- 1. (Note that only cables




                                                                                                                                                                                                                  -
                                                                                                                                        or struts are in any En.) In other words, for just those members in E, p(’) acts as
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        a strict first-order flex of G(p).
                                                                                                                                             We will next find a sequence of real numbers 1 > > 2 >>          0 and define
                                                                                                                                                          r       p() + p(+) + p(+) +... + _p(-),
                                                                                                                                        where > + means that + is chosen suciently small such that later inequal-
                                                                                                                                        it)es will remain satisfied. We see that r’ is also a (nontrivial) first-order flex of G(p).
                                                                                                                                        In fact we require that for {i, j} a member of G,

                                                                                                                                        (7)       (pi-p)-(r-r})
                                                                                                                                                                         {     <0 if
                                                                                                                                                                                           {i,j}(E...E_)E_}
                                                                                                                                                                               >0 if {i,j}(EU
                                                                                                                                                                                0 otherwise
                                                                                                                                        To see that this is possible we proceed by induction. Define tbr n
                                                                                                                                                                                                                UE-I)E+

                                                                                                                                                                                                                   k, k + 1,..., 2k + 1,
                                                                                                                                                                  r(n)       p(k) + ep(k+) +... + e_kp(),
                                                                                                                                        where r’(k)    p(k). We require that for {i,j} a member of G,

                                                                                                                                        (8)      (pi-pj).(r(n)-r}(n))
                                                                                                                                                                                {        <0 if
                                                                                                                                                                                                 {i,j}e(EkU...UE)E_}
                                                                                                                                                                                         >0 if {i,j}e(EkU...UE)E+
                                                                                                                                                                                          0 otherwise
                                                                                                                                        But this is true for n k, and if e+l > 0 is chosen small enough we can satisfy (8)
                                                                                                                                        for n + 1, assuming it is true for n.
                                                                                                                                             In other words for every cable and strut of G, either r is strict or r and p,...,
                                                                                                                                        p(2k-) act as if {i, j} were a bar for the first-order conditions.
                                                                                                                                             We now choose a large real number B > 0 and define
                                                                                                                                                                                2
                                                                                                                                                                               q"=
                                                                                                                                                                                         ()p() + Br’.
                                                                                                                                        Recalling that q’ p(k), we claim tha.t (q’, q") is a second-order flex of G(p) for B
                                                                                                                                        large enough. For {i, j} E U.-. U E_ we calculate
                                                                                                                                              (P- Pj)" (q’-q.)+ Iq- qj]2

                                                                                                                                                          ()
                                                                                                                                                              2
                                                                                                                                                                  (,     ,).   ,    ()
                                                                                                                                                                                           .
                                                                                                                                                                                           _()
                                                                                                                                                                                                   + (, ,). (r r}) + ,U

                                                                                                                                                      {>0 if {i,j}
                                                                                                                                                       <0 if {i,j}     E+
                                                                                                                                                                             E-
                                                                                                                                                                            (Ek U
                                                                                                                                                                            (Ek
                                                                                                                                                                                                 U E2k-1)
                                                                                                                                                                                                 U Ek_)     }
                                                                                                                                        if B is chosen large enough by (7).
                                                                                                                                            For {i,j} a member of G but {i,j} E                  ...
                                                                                                                                                                                  Ek_, then (pi- py). (r- r})                          0
                                                                                                                                        and (pi- pj)" (pe) pe)) 0 for e 1,..., 2h 1. Then


                                                                                                                                                                       t=0
                                                                                                                                                                                    2k


                                                                                                                                                                                  g=0
                                                                                                                                                                                               p
                                                                                                                                                                                                  _()
                                                                                                                                                                               =2(pi-pj).[pi(k) -Pj
                                                                                                                                                                                                        ). (p

                                                                                                                                                                                                                   -
                                                                                                                                                                                                      )+(k)l p}) -Pj()
                                                                                                                                                                                 ()[(p- p). (.- w.)+ q;-
                                                                                                                                                                                 0 if {i,j}E_(EkU...UEk_I)
                                                                                                                                                                                 -0 if {i,j}Eo (EkU’"UEk-)
                                                                                                                                                                                 k0 if {i,j}E+(EkU...UEk_).
                                                                                                                                        476                               R. CONNELLY AND W. WHITELEY

                                                                                                                                            Thus in either case the second-order conditions are satisfied, (q’, q’) is a second-
                                                                                                                                        order flex of G(p), and q is not 1-trivial.    D
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                             Remark 4.3.1. The general outline for the above proof is the same as in [6],
                                                                                                                                        except that the cables and struts can cause complications. Differentiating the edge
                                                                                                                                        length condition allows us to detect any cable or strut, but its occurrence causes an
                                                                                                                                        appropriate sign somewhere from the level k to 2k. The intermediate levels from k + 1
                                                                                                                                        to 2k- 1 must be introduced into the (q, q’) carefully.
                                                                                                                                             4.4. Prestress stability and second-order rigidity. We observe that pre-
                                                                                                                                        stress stability is stronger than second-order rigidity.
                                                                                                                                             THEOREM 4.4.1. If a tensegrity framework G(p) is prestress stable, then it is
                                                                                                                                        second-order rigid.
                                                                                                                                             Proof. Let co be the prestress that stabilizes G(p). Then from the comments
                                                                                                                                        following the definition of prestress stability, co also stabilizes that subframework of
                                                                                                                                        G(p) consisting of the same bars and all cables and struts with wij O. Thus, without
                                                                                                                                        any loss of generality, we can assume that co is strict. For example, wij 0 on all the
                                                                                                                                        cables and struts of G.
                                                                                                                                             Suppose (p’, p’) is a second-order flex of G(p), where p’ is not a trivial first-
                                                                                                                                        order flex. We wish to find a contradiction. By the first-order stress test we see that
                                                                                                                                        (p- pj). (p- pj) 0 for all members of (because wj # 0 on all cables and
                                                                                                                                        struts). Thus, by the second-order condition,
                                                                                                                                                                                                           {i,j}= cable
                                                                                                                                                     IP- pj 12 + (p             pj)" (p’- pj)            0 {i,j}  bar
                                                                                                                                                                                                       _>0 {i,j}= strut

                                                                                                                                        for all members {i, j) of G. In any case, since co is proper for all members {i, j} of G,

                                                                                                                                                             COij   IPi     pj [2
                                                                                                                                                                                    ._ (pi- pj). (pi- pj) <
                                                                                                                                                                                       COij                      0.

                                                                                                                                        But since p is a nontrivial first-order flex of G(p) and since co is a stabilizing self
                                                                                                                                        stress for G(p),

                                                                                                                                                            wR(p’)p’-            Eij
                                                                                                                                                                                       wij    p- pl -(p,)Tp, > 0
                                                                                                                                        by Proposition 3.4.2. Recalling that coR(p)               0,
                                                                                                                                                 0 < coR(p’)p’            coR(p’)p’ + coR(p)p"
                                                                                                                                                                          Eij
                                                                                                                                                                              wij (p   pj )2 + coij (Pi    Pj)" (P’   Py) _< 0,
                                                                                                                                        a contradiction. Thus G(p) is second-order rigid.
                                                                                                                                             Remark 4.4.1. It turns out that there are tensegrity frameworks that are not
                                                                                                                                        prestress stable for any prestress yet are still second-order rigid. For instance, the
                                                                                                                                        example of Figure 9b has this property. The two "tetrahedral" blocks are prestress
                                                                                                                                        stable. Therefore, all second-order flexes are trivial on these blocks. Any such second-
                                                                                                                                        order flex must extend to a rotation about the common point 0. However, this violates
                                                                                                                                        either the strut or the cable condition on the unstressed connecting members at first-
                                                                                                                                        order.
                                                                                                                                             However, in 5.3 we will see that if the space of first-order flexes or the space
                                                                                                                                        of proper self stresses is one-dimensional, then second-order rigidity and prestress
                                                                                                                                                      SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                            477

                                                                                                                                        stability are the same. This will also help us to find examples of bar frameworks
                                                                                                                                        which are second-order rigid but not prestress stable in 5.3.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                            5. The stress test.
                                                                                                                                             5.1. Duality from linear algebra. We now formulate some well-known prin-
                                                                                                                                        ciples of duality in linear algebra which we will later interpret as a "stress" test for
                                                                                                                                        second-order rigidity. These duality principles are a special case of the duality princi-
                                                                                                                                        ples used in linear programming.
                                                                                                                                             In the following, let A be a d-by-e real matrix, where we write A in block form

                                                                                                                                                                               A=     [AoA+]’
                                                                                                                                        where Ao and A+ are some designated subsets of the rows of A. In our applications
                                                                                                                                        A will correspond to the rigidity matrix, A0 will correspond to the rows indexed by
                                                                                                                                        the bars of G, and A+ will correspond to the rows indexed by the struts and cables of
                                                                                                                                        G, with the strut rows multiplied by -1. However, for the general statements in this
                                                                                                                                        section we will not need any special properties of A.
                                                                                                                                             We can now restate the first-order stress test in this somewhat more general
                                                                                                                                        context. We use the notation [X l,X2,...] < 0 for vectors to mean xi < 0 for all
                                                                                                                                        i= 1,2,
                                                                                                                                            PROPOSITION 5.1.1.       There is a column vector x E IRd such that

                                                                                                                                                                                 Aox =0,
                                                                                                                                                                                 A+x < 0,
                                                                                                                                        if and only if for all row vectors y E IRe, y       [y0, y+], such that
                                                                                                                                                                           y0A0 + y+A+          0,

                                                                                                                                                                                 y+ _> O;
                                                                                                                                        then y+ 0.
                                                                                                                                             This is a special case of the duality principle for homogeneous linear equalities,
                                                                                                                                        for instance, as found in [32, Thin. 6]. Note that the "only if" implication is easy, since
                                                                                                                                        if Aox 0, A+x < 0, y0A0 +y+A+ 0, y+ >_ 0, then 0 yoA0x + y+A+x _< 0. If
                                                                                                                                        y+     0 this gives a strict inequality and thus a contradiction. The other implication
                                                                                                                                        implicitly or explicitly uses the principle of "hyperplane separation." See, for example,
                                                                                                                                        [17, p. 10].
                                                                                                                                             An important point is the strictness of the inequalities. However, in the following
                                                                                                                                        we instead concentrate on the duality principle itself, putting aside the strictness
                                                                                                                                        properties for the moment.
                                                                                                                                            Let
                                                                                                                                                                            b=   [bob+] IR
                                                                                                                                        be a column vector.
                                                                                                                                             PROPOSITION 5.1.2.      There is a column vector x        IRd such that
                                                                                                                                                                                A0x   bo,
                                                                                                                                                                               A+x _< b+,
                                                                                                                                        478                         R. CONNELLY AND W. WHITELEY

                                                                                                                                        if and only if for all row vectors y E IRe, y   [y0, y+], such that
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                          y0A0 + y+A+      0,
                                                                                                                                                                              y+ _>0;

                                                                                                                                        then yob0 + y+b+ _> 0.
                                                                                                                                             Note that again the "only if" implication is easy since if Aox bo, A+x _< b+,
                                                                                                                                        y0Ao + y+A+ 0, and y+ _> 0 then 0 yoA0x + y+A+x _< yobo + y+b+, and again
                                                                                                                                        the "if" implication follows from the hyperplane separation principle.
                                                                                                                                             In the terminology of linear programming this proposition is an asymmetric form
                                                                                                                                        of duality in the special case when the primal problem has the constant 0 objective
                                                                                                                                        function. See [15] for instance for a discussion of various such forms of the Parkas
                                                                                                                                        alternative as well as a proof.
                                                                                                                                             We now sharpen this proposition to obtain an equivalent dual reformulation to
                                                                                                                                        determine when we get strict inequality. We fix A and b.
                                                                                                                                             PROPOSITION 5.1.3. There is a column vector x IRd such that
                                                                                                                                                                               Aox bo,
                                                                                                                                                                              A+x < b+,
                                                                                                                                        if and only if for all row vectors y IRe, y     [yo, y+], such that
                                                                                                                                                                          y0Ao + y+A+       0,
                                                                                                                                                                              y+ >_ 0;

                                                                                                                                        then yobo + y+b+ _> 0 with equality if and only if y+ 0.
                                                                                                                                              Proof. Again, the only if implication follows easily. A0x bo, A+x < b+,
                                                                                                                                        y0Ao + y+A+ 0, y+ _> 0 imply that 0 yoA0x / y+A+x _< yobo / y+b+ and we
                                                                                                                                        have strict inequality, and a contradiction, if and only if y+ :fi 0.
                                                                                                                                              To show the converse we use the two previous propositions. Assume that the
                                                                                                                                        condition on the y vector holds. By Proposition 5.1.2 we know that there is an
                                                                                                                                        x     IRd such that A0x b0, A+x _< b+. If all of the b+ inequalities are strict
                                                                                                                                        we are done. If not, throw out those strict inequalities from A to get the condition
                                                                                                                                        Aox bo, A+x b+. Similarly, we can throw out the corresponding set of variables
                                                                                                                                        in the y vector. Now it is still true that if y0A0 / y+A+ 0, then yoAox / y+A+x
                                                                                                                                        yob0 + y+b+ 0. Thus Proposition 5.1.1 applies, and there is a (small) x .IR e
                                                                                                                                        such that Aox        0, A+x < 0. ThenAo(x+x) bo, A+(x+x) < b+. Ifx
                                                                                                                                        is snall enough then x / x still satisfies those inequalities that were thrown out as
                                                                                                                                        well.
                                                                                                                                             5.2. Interpretation as the stress test. We now specialize the results of
                                                                                                                                        5.1 to the case of the rigidity matrix. Let G(p) be a tensegrity framework in ]Rd,
                                                                                                                                        and let R(p) be its d-by-e rigidity matrix. Let R0(p) denote those rows (regarded
                                                                                                                                        as a smaller matrix) corresponding to the bars of G. Let R+(p) denote the matrix
                                                                                                                                        obtained from those rows of R(p) corresponding to cables and struts of G, with the
                                                                                                                                        rows corresponding to struts multiplied by -1.
                                                                                                                                             Suppose w is a proper stress for G(p), so wR(p) 0. We then have a correspond-
                                                                                                                                        ing [w0, w+], where 0 corresponds to the stresses on the bars and w+ to the stresses
                                                                                                                                        on the cables and struts, but with the opposite sign for struts only. Thus    being
                                                                                                                                        proper translates into w+ _> 0, and being a self stress means w0R(p) + w+R+(p) 0.
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                          479

                                                                                                                                             In this terminology p is a first-order flex if
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                                Ro(p)p’ 0,
                                                                                                                                                                                n+(p)p’ _< 0,
                                                                                                                                        and p, p" is a second-order flex if in addition

                                                                                                                                                                        no(p’)p’ + no(p)p" 0,
                                                                                                                                                                        R+ (p’)p’ + R+ (p)p" <_ 0,
                                                                                                                                        where an inequality need only hold when the corresponding inequality, in the first-
                                                                                                                                        order system, is an equality. Recall that p" (or p’) is strict for {i, j} a cable or strut
                                                                                                                                        if the corresponding inequality is strict.
                                                                                                                                             We now have our strict second-order duality result.
                                                                                                                                              COROLLAaY 5.2.1 (the second-order stress test). A first-order flex p’ of G(p)
                                                                                                                                        extends to a second-order flex (p, p") if and only if for all proper self stresses w for
                                                                                                                                        G(p), with stress matrix ft,
                                                                                                                                                                              (p,)Tfp, _< 0.
                                                                                                                                        Furthermore, p" can be chosen to be strict, on each cable and strut {i, j} where p is
                                                                                                                                        not strict, if and only if for all proper self stresses co, pftp 0 implies wj O, for
                                                                                                                                        each such { i, j }
                                                                                                                                             Proof. We apply Proposition 5.1.3, where
                                                                                                                                                                                   p=x

                                                                                                                                                                Ro(p)     Ao,              Ro (p’) p’     bo,
                                                                                                                                                               R+(p)      A+,             -R+(p’)p’       b+,
                                                                                                                                                                          w0=Y0,       w+=Y+.
                                                                                                                                        We may assmne, without loss of generality, that R(p)p          0, since any cable or strut
                                                                                                                                        where p is strict can be disregarded as a cable or strut for the second-order conditions.
                                                                                                                                            The second-order conditions translate into the hypothesis of Proposition 5.1.2,
                                                                                                                                        and the conclusion translates into the condition that w is a proper self stress. Then

                                                                                                                                            0 _< yobo + y+b+      -woRo(p’)p’- w+R+(p’)p’               -wR(p’)p’
                                                                                                                                        is the condition desired. The strictness follows from Proposition 5.1.3.  [:1
                                                                                                                                             We can simplify matters even further when G consists only of bars. This is our
                                                                                                                                        second-order duality result for bar frameworks.
                                                                                                                                             COROLLARY 5.2.2 (second-order stress test for bars). A first-order flex p of a
                                                                                                                                        bar framework G(p) extends to a second-order flex if and only if for all self stresses w
                                                                                                                                        for G(p), with stress matrix f,
                                                                                                                                                                                (p,)Tp,     O.

                                                                                                                                            Remark 5.2.1. In the appendix, we show that we can always replace a framework
                                                                                                                                        (with a strict proper self stress) by an equivalent bar framework and use this to check
                                                                                                                                        second-order rigidity. However, it seems simpler to use Corollary 5.2.1 directly, rather
                                                                                                                                        than introduce so many extraneous members.
                                                                                                                                        480                           R. CONNELLY AND W. WHITELEY

                                                                                                                                             5.3. Second-order rigidity and prestress stability. When does second-
                                                                                                                                        order rigidity imply prestress stability? We begin with cases when the set of self
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        stresses or the set of equilibrium first-order flexes is one-dimensional, the natural first
                                                                                                                                        cases to consider.




                                                                                                                                                                                                  _
                                                                                                                                             Note that for a fixed tensegrity framework G(p), the proper self stress and first-
                                                                                                                                        order flexes each form a cone with the origin as the cone point.
                                                                                                                                             PROPOSITION 5.3.1. If a tensegrity framework G(p) is second-order rigid with
                                                                                                                                        either a one-dimensional cone of equilibrium first-order flexes or a one-dimensional
                                                                                                                                        cone of proper self stresses, then G(p) is prestress stable.
                                                                                                                                             Proof. Suppose p is any nontrivial equilibrium first-order flex of G(p) generating
                                                                                                                                        the one-dimensionM cone of all equilibrium first-order flexes. If for all proper self
                                                                                                                                        stresses with stress matrix t we have
                                                                                                                                                                        t(p’)Tgtp ’- (tp’)Tgttp 0
                                                                                                                                        for all first-order flexes tp’ of G(p) (t a real scalar), then by Corollary 5.2.1 p’ extends
                                                                                                                                        to a second-order flex (p’, p") of G(p), which contradicts G(p) being second-order
                                                                                                                                        rigid. Thus for some proper self stress w, (p’)Ttp’ > 0, w stabilizes G(p) (by Propo-
                                                                                                                                        sition 3.4.2) and G(p) is prestress stable.
                                                                                                                                              Suppose w is a proper nonzero self stress in the one-dimensional cone of proper
                                                                                                                                        self stresses. Suppose there is a nontrivial first-order flex p such that (p}Tfp _< 0.
                                                                                                                                        If --w is not a proper stress, then tw, t _> 0, are the only proper self stresses for G(p).
                                                                                                                                        Then by Corollary 5.2.1 again G(p) would not be second-order rigid, contradicting
                                                                                                                                        the hypothesis. Therefore either (p)Tgtp > 0 for all nontrivial first-order flexes p or
                                                                                                                                        -w is a proper self stress. If -w is a proper self stress, then (p)Tp 0 and again
                                                                                                                                        p’ would extend to a second-order flex. Thus (p’)T(:i:)p’ > 0 and +/-w stabilizes
                                                                                                                                        G(p).
                                                                                                                                              We have already seen an example of tensegrity framework in the plane, Figure
                                                                                                                                        9b, which is easily seen to be second-order rigid, directly from the definition, but is
                                                                                                                                        not prestress stable for any proper self stress. Here we present another example, but
                                                                                                                                        one which is a bar framework in three-space. It also serves as an example of how to
                                                                                                                                        calculate using the stress test.
                                                                                                                                             If we have any bar framework G(p), let
                                                                                                                                                                             p’(1),..., p’(n)
                                                                                                                                        denote a basis for a space of nontrivial first-order flexes of G(p). Let
                                                                                                                                                                          f(1),..., t(m)
                                                                                                                                        denote a basis for the space of self stresses of G(p). If G(p) is prestress stable,
                                                                                                                                        some linear combination of the stress matrices must be positive definite on the space
                                                                                                                                        generated by the first-order flexes p’(1),..., p’(n). From Corollary 5.2.2, the second-
                                                                                                                                        order stress test for bar frameworks, G(p) is not second-order rigid if and only if all
                                                                                                                                        of the stress mtrices have a common nonzero vector on which they evaluate to be 0
                                                                                                                                        in this same space generated by p’(1),..., p’(n). When n 2, both of these criteria
                                                                                                                                        can be checked with certain easily calculated expressions.

                                                                                                                                             Example 5.3.1. We define a specific example in three-space. Let G(p) be the
                                                                                                                                        following bar framework in three-space with the following seven vertices:
                                                                                                                                                         Pl    (0, 0, 0),     p4     (1, 0, 0),       P7   (1, 0, 0),
                                                                                                                                                         P2    (0, 1, 0),     P5     (1, 1, 0),
                                                                                                                                                         P3    (0, 0, 1),     P6     (0, 1, 0),
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                   481

                                                                                                                                        and the following bars:
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                         {1, 2}, {1, 3}, {1,4}, {1, 6}, {1, 7},
                                                                                                                                                                         {,a}, {,}, {, },
                                                                                                                                                                         {3, 4}, {3, 5},
                                                                                                                                                                         {4,5},{4,6},
                                                                                                                                                                         {,}, {,7},
                                                                                                                                                                         {6, 7}.
                                                                                                                                        See Figure 17a, where although p. p6 and p4 p7 we have separated them slightly
                                                                                                                                        so that the framework can be more easily understood.

                                                                                                                                                               P3




                                                                                                                                              a                 P                              b
                                                                                                                                             FIG. 17. A bar framework (a) in 3-space that is second-order rigid but not prestress stable. A
                                                                                                                                        portion of the planar base is shown in (b).


                                                                                                                                            Note that this framework is made of the framework of Figure 17b and its sym-
                                                                                                                                        metric copy, with appropriate identifications. Then pa is added along the z-axis.
                                                                                                                                            We consider those first-order flexes p’(k), where (k)             p
                                                                                                                                                                                                             (k)       p
                                                                                                                                                                                                                       (k) 0,   p
                                                                                                                                        which clearly determines a complement of the space of trivial flexes, since (pl, p., pa)
                                                                                                                                        determines a bar triangle. Since (pl, p2, pT) and (p2, ps, p) are bar triangles in the
                                                                                                                                        same plane, sharing a common bar pl, p, any first-order flex p’ must have

                                                                                                                                                                             (Pl    Ps)" (Pl       P)    O.

                                                                                                                                        In other words, {1, 5} is an "implied bar." Thus the first-order rigid tetrahedron
                                                                                                                                        (pl,p.,pa,p) is implied and p 0. Similarly p 0, from the implied tetrahedron
                                                                                                                                        (pl, p3, p5, p4). See [9]. So the following first-order flexes are a basis for a comple-
                                                                                                                                        mentary space:
                                                                                                                                                                    p(1)      { (0,0,1)
                                                                                                                                                                                (0, 0) 0,
                                                                                                                                                                                                    if
                                                                                                                                                                                                         i-6}
                                                                                                                                                                                                    otherwise

                                                                                                                                                                    p(2)           (0,0,1)
                                                                                                                                                                                   (0, 0, 0)
                                                                                                                                                                                                    if i=7
                                                                                                                                                                                                            }
                                                                                                                                                                                                    otherwise
                                                                                                                                             We can also find two independent stresses for G(p):


                                                                                                                                                     wij (1)
                                                                                                                                                                     1
                                                                                                                                                                    -1
                                                                                                                                                                     0
                                                                                                                                                                                if {i, j}
                                                                                                                                                                                if {i,j}
                                                                                                                                                                                otherwise
                                                                                                                                                                                               {2, 7}, {5, 6},
                                                                                                                                                                                               {2,5},{6,7},
                                                                                                                                                                                                                  or
                                                                                                                                                                                                                  or
                                                                                                                                                                                                                       {1,6}}
                                                                                                                                                                                                                       {2, 1}
                                                                                                                                        482                              R. CONNELLY AND W. WHITELEY


                                                                                                                                                    coy(2)          -1        if {i,j)            {1, 4}, {6, 7),   or   {4, 5)
                                                                                                                                                                                                                                  /
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                     0        otherwise
                                                                                                                                        These are easy to see by looking at Figure 17b. Notice that e 15 3v- 6 and that
                                                                                                                                        the space of first-order nontrivial (equilibrium) flexes must be of dimension 2, so the
                                                                                                                                        dimension of the space of self stresses is 2 as well. Thus co(l) and w(2) generate all
                                                                                                                                        the self stresses.
                                                                                                                                             We next calculate the stress matrices (I), Ft(2) corresponding to w(1), w(2),
                                                                                                                                        relative to the vectors pt(1), pt(2). Note that for a- 1,2, b- 1,2, k 1,2,

                                                                                                                                               p’(a)Tt(k)p’(b)           tab(k)     E wj(k)(p(a) p.(a)). (p(b) p}(b)).
                                                                                                                                                                                     j

                                                                                                                                        Then
                                                                                                                                                                          E w6{(1) -w67(1)
                                                                                                                                                             t(1)
                                                                                                                                                                           -w76(1) E w{(1)
                                                                                                                                                                                                       1 +1]    1
                                                                                                                                                                                                               +1    0




                                                                                                                                                                           -w6 (3)        E (2)  wi            +1

                                                                                                                                        To see if any linear combination of these is positive definite, we calculate, for any real


                                                                                                                                                det[Al/(1) + A2(2)]           det          AI
                                                                                                                                                                                       )1 -1t-

                                                                                                                                        which is a negative definite quadratic form itself, since (-1) 2 -4(-1)(-1) -3 < 0.
                                                                                                                                        Thus for each choice of (A1,A2)         (0,0), det[Alt(1)+ A2(2)] < 0, which implies
                                                                                                                                        that none of the forms A1(1)+ A2t(2) are positive definite, and thus no stress
                                                                                                                                        Alw(1) + A2w(2) can serve as a stable prestress.
                                                                                                                                             On the other hand recall that the second-order stress test for bar frameworks,
                                                                                                                                        Corollary 5.2.2, says that a first-order flex p will extend to a second-order flex if and
                                                                                                                                        only if p is in the zero set of all the proper self stresses (regarded as quadratic forms)
                                                                                                                                        of G(p). If some pl does extend, then so does pl plus any trivial first-order flex, and
                                                                                                                                        so we can assume that p’ is in the space spanned by p’(1) and p’(2). Thus G(p) will
                                                                                                                                        be second-order rigid if and only if t(1) and Ft(2) (and thus all )lt(1)+ A2t(2)) have
                                                                                                                                        a common zero. The zeros of (i) (as a quadratic form) are scalar multiples of

                                                                                                                                                                              (0, 1)        or     (2,-1).
                                                                                                                                        For (2) we get
                                                                                                                                                                              (1,0)         or     (-1,2).
                                                                                                                                             None of the above four vectors are scalar multiples of any of the others, so G(p)
                                                                                                                                        is second-order rigid but not prestress stable.
                                                                                                                                             Remark 5.3.1. If the dimension of the space of nontrivial (equilibrium) first-order
                                                                                                                                        flexes I is two, then it is easy to determine when the framework is prestress stable.
                                                                                                                                        Calculate a basis of stress matrices restricted to I. Choosing an orthonormal basis for
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                483

                                                                                                                                        I, we see that there are at most three such distinct stress matrices (even if the space of
                                                                                                                                        self stresses is higher-dimensional), since they correspond to symmetric 2 2 matrices.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        If there are just two such matrices, one can perform an analysis similar to Example
                                                                                                                                        5.3.1. If there are three such stress matrices, independent over I, there always is a
                                                                                                                                        stabilizing self stress.
                                                                                                                                              Also for Example 5.3.1 it is possible to vary the points by a small amount, keeping
                                                                                                                                        all the points except p3 in a plane, and obtain many other examples of second-order
                                                                                                                                        rigid but not prestress stable bar frameworks in three-space.            [I
                                                                                                                                              Note that the underlying graph of the example above is a triangulated sphere.
                                                                                                                                        Figure 18a shows a realization of this graph as a triangulated convex surface. By
                                                                                                                                        [6], this realization is also second-order rigid. In fact it is prestress stable as well. All
                                                                                                                                        members adjacent to p6 and p7 have a positive stress in the stabilizing self stress. This
                                                                                                                                        brings up the question: are all triangulations of a convex polyhedron in three-space,
                                                                                                                                        with edges as bars, prestress stable? In [6] it is only shown that such frameworks are
                                                                                                                                        second-order rigid. The answer is yes and will be shown elsewhere.

                                                                                                                                                                P3




                                                                                                                                              P2


                                                                                                                                                                                        P4


                                                                                                                                                                 Pl
                                                                                                                                               a                                                     b
                                                                                                                                            FIG. 18. Example (a), with the same graph as Figure 17a, is prestress stable in three-space.
                                                                                                                                        Example (b) is second-order rigid in the plane but not prestress stable.

                                                                                                                                             In the plane, it turns out that if we take the bipartite graph K3,3 with its six
                                                                                                                                        points on the line and { i, 2, 3}, {4, 5, 6} as the partition (Figure 18b), then this frame-
                                                                                                                                        work K3,3(p) is second-order rigid but not prestress stable. We omit this nontrivial
                                                                                                                                        calculation. It also turns out that K3,3(p) is a mechanism in R3.
                                                                                                                                             In [26], as well as in [27, p. 50], there is another example of a second-order rigid
                                                                                                                                        but not prestress stable bar framework in the plane. The calculation for that example
                                                                                                                                        turns out to be quite simple.
                                                                                                                                             5.4. Applications in b-c polygons. Here we apply the second-order stress
                                                                                                                                        test to a special class of frameworks G(p): the b-c polygons of 3.5. That is, G(p) is
                                                                                                                                        a convex polygon in the plane with bars as edges and only cables on the inside.
                                                                                                                                             PROPOSITION 5.4.1. Let p be any nontrivial first-order flex of G(p), a b-c
                                                                                                                                        polygon in the plane. Then p’ extends to a strict second-order flex (p’, p") of G(p).
                                                                                                                                             Proof. Let f be any stress matrix coming from a proper self stress w of G(p).
                                                                                                                                        Since p is nontrivial it is easy to check that p is not an affine image of p. By [7]

                                                                                                                                                                                (p,)Tp, < 0,
                                                                                                                                        since for the reversed polygon (with struts on the inside) the corresponding matrix
                                                                                                                                        (-f) is positive semidefinite. Thus by Corollary 5.2.1, p extends to a strict second-
                                                                                                                                        order flex (p, p").           [:]
                                                                                                                                        484                          R. CONNELLY AND W. WHITELEY

                                                                                                                                             Remark 5.4.1. We will use this result in the next section to prove Roth’s conjec-
                                                                                                                                        ture about b-c polygons. It is interesting (although painful) to calculate ptt directly
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        for the pt as indicated in Figure 14.
                                                                                                                                             Note, however, with this result alone we can prove a weak form of Roth’s conjec-
                                                                                                                                        ture. Namely, if p is a nontrivial first-order flex of a strut-cable polygon (the outside
                                                                                                                                        edges are struts), then an argument similar to the one above can be used to find a
                                                                                                                                        strict second-order flex (p’ p") as well. Then p(t) p + tp’ + t2p" is a flex at G(p)
                                                                                                                                        as required.
                                                                                                                                             The only problem left in the stronger form of Roth’s conjecture is to find a way
                                                                                                                                        of handling the bars. We will treat this in 6.
                                                                                                                                             5.5. Interpretation for triangulated spheres. For any triangulated sphere
                                                                                                                                        G(p) in IR3, there is a natural correspondence between first-order flexes p’ of G(p)
                                                                                                                                        (modulo trivial first-order flexes) and self stresses w of G(p). In fact for each edge
                                                                                                                                        {i,j} there is a dihedral angle 0ij, which itself "varies" and thus there is a Oj defined
                                                                                                                                        as. the derivative of 0ij. Then

                                                                                                                                                                          0j
                                                                                                                                                                                     {i, j} and edge at G

                                                                                                                                        serves as a self stress for G(p). Conversely, given a self stress it is possible to define a
                                                                                                                                        first-order flex p’ with Oj as above. See [16] or [14] for a discussion of this.
                                                                                                                                             Thus using Corollary 5.2.1 we can state the dual condition for a second-order flex.
                                                                                                                                             COROLLARY 5.5.1. A first-order flex p of a triangulated sphere G(p) in IR3
                                                                                                                                        extends to a second-order flex if and only if for every      0   (coming from a possibly
                                                                                                                                        different first-order flex) we have



                                                                                                                                              5.6. Interpretation in terms of packings.          For the rigidity of packings as in
                                                                                                                                        [11] or [12] we see that the associated framework has certain vertices pinned and all
                                                                                                                                        the members are struts. For any proper self stress w, wj <_ 0 for all {i, j} struts, and
                                                                                                                                        thus such a G(p) has for all p, a first-order flex,

                                                                                                                                                                   (p,)Tp,      E wj(p- pj)2 _< 0,
                                                                                                                                                                                 j

                                                                                                                                        since we can take p to be 0 on the pinned vertices. In fact, we get strict inequality
                                                                                                                                        assuming G is connected and p’ 0. Thus there is a strict second-order flex (p, p’),
                                                                                                                                        and it is easy to see that such a G(p) is rigid if and only if it is first-order rigid. This
                                                                                                                                        was observed directly in [11].
                                                                                                                                              6. Extending second-order flexes.
                                                                                                                                              6.1. The general result. Some second-order flexes extend to continuous flexes
                                                                                                                                        of the framework. For example, if a second-order flex shortens all cables and lengthens
                                                                                                                                        all struts and there are no bars, then it is clear that we can complete these first two
                                                                                                                                        derivatives to a real analytic path. We describe a less restrictive situation where we
                                                                                                                                        can still extend the second-order flex. This result is an extension of and motivated by
                                                                                                                                        some of the results in [1, 2]. A bar framework G(p) is called independent if the only
                                                                                                                                        self stress for G(p) is the zero self stress.
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                       485

                                                                                                                                            PROPOSITION 6.1.1. Let G(p) be any independent bar framework with a second-
                                                                                                                                        order flex (p’, p") in IRd. Then there is an analytic flex p(t) of G(p) with
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                                  p(0)      p,

                                                                                                                                                                          Dt[p(t)]lt:o p’,
                                                                                                                                                                          D2t [p(t)][t=o p,,.
                                                                                                                                               Proof. Let


                                                                                                                                        be the set of all configurations equivalent to p. By [1] or [29], since G(p) is inde-
                                                                                                                                        pendent, Ma(p) is a smooth analytic manifold of dimension at least d(d + 1)/2 in a
                                                                                                                                        neighborhood of p (when the dimension of the affine span of p is at least d- 1), and
                                                                                                                                        we may naturally identify the tangent space Tp of Ma(p) at p with the first-order
                                                                                                                                        flexes of G(p).
                                                                                                                                             Let h Tp + Ma(p) be a smooth analytic map such that the following hold:
                                                                                                                                              (a) On a neighborhood of p in Tp, h is a real analytic diffeomorphism onto a
                                                                                                                                        neighborhood of p in Me(p).
                                                                                                                                              (b) Identifying the tangent space of Tp with itself, h(p) p and dhp(p’) p’
                                                                                                                                        for all p’ E Tp, where dhp is the differential of h at p.
                                                                                                                                             For instance, the exponential map has these properties.
                                                                                                                                             Let q(t) p + tp’ + 5t2q be a smooth analytic path in Tp where we see that
                                                                                                                                        q(0) p. Dt[q(t)]lt=o p’ and Dt2[q(t)]
                                                                                                                                        Then define p(t)
                                                                                                                                                                                   It=Q     q", which will be determined later.
                                                                                                                                                              h(q(t)), which is a smooth analytic flex of G(p) with p(0) p.
                                                                                                                                        Also

                                                                                                                                        (9)                   Drip(t)]    Dt[h(q(t))]      dhq(t)(Dt[q(t)])
                                                                                                                                        and
                                                                                                                                                                     Dt[p(t)]]t=o dhp(p’) p’,
                                                                                                                                        by condition (b). Since p(t) E Ma(p), p(t) is an analytic flex of G(p) and thus the
                                                                                                                                        second derivatives of the squares of the edge lengths are zero. Restating this in terms
                                                                                                                                        of the matrix R(p) we get

                                                                                                                                                             R(Dt[p(t)])Dt[p(t)] + R(p(t))D2t [p(t)]      O.
                                                                                                                                        Evaluating when t    O, we get
                                                                                                                                                                         R(p’)p’ + R(p)r"        0,
                                                                                                                                        where r"- Dt[p(t)]lt=0
                                                                                                                                              We must choose q such that r          p" the preassigned vector. Recalling that
                                                                                                                                        (p,, p,,) is a second-order flex of G(p) we see that for any q",

                                                                                                                                                             n(p’)p’ + R(p)p"     0       R(p’)p’ + R(p)r".
                                                                                                                                        So
                                                                                                                                        (10)                              R(p) (p"- r")=0.
                                                                                                                                        486                                R. CO NNELLY AND W. WHITELEY

                                                                                                                                        Differentiating (9) again we obtain
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                                                Dt[p(t)]        Dt[dhq(t)]Dt[q(t)] + dhq(t)Dt [q(t)].
                                                                                                                                        Applying the chain rule to each entry of the matrix dhq(t), we see that Dt[dhq(t)]lt=o
                                                                                                                                        depends only on p and not on q". Let s" be the value of the second derivative of p(t)
                                                                                                                                        (that is r") when q" 0, evaluated when t 0. In other words
                                                                                                                                                                            s-     Dt[dhq(t)]Dt[q(t)]lt:o
                                                                                                                                        is independent of the choice of q". We must then solve the linear equation

                                                                                                                                                                           p"      s" + dhp q"      s" + q"

                                                                                                                                        for q". Recall that dhp is the identity map by condition (b). By (10), (p’, s") is a
                                                                                                                                        second-order flex of G(p) and p"-s" is a first-order flex of R(p) and thus is in Tp.
                                                                                                                                        Thus we can define q" p"-s". Then p(t) as defined is the desired flex.               [:]
                                                                                                                                             Remark 6.1.1. One way of looking at the above proof is to think of adding some
                                                                                                                                        curvature via q" to the curve q(t) to cancel the curvature in M(p) in order to achieve
                                                                                                                                        the given second derivative p".
                                                                                                                                             For our purposes we do not need p(t) to be real analytic. It only needs to be
                                                                                                                                        twice differentiable. In the spirit of Definition 2.1.2 (c) we stated things in this more
                                                                                                                                        general form.
                                                                                                                                             It seems natural that there also should be a generalization of this result involving
                                                                                                                                        any number of derivatives.
                                                                                                                                              6.2. Roth’s conjecture.              We can now prove Roth’s conjecture in its full gen-
                                                                                                                                        erality.
                                                                                                                                              PROPOSITION 6.2.1. A convex b-c polygon in the plane is rigid if and only if it
                                                                                                                                        is first-order rigid.
                                                                                                                                             Proof. Let p’ be any nontrivial first-order flex of a b-c polygon G(p). If G(p) has
                                                                                                                                        no nonzero proper self stress, then by the first-order stress test, we can choose p such
                                                                                                                                        that (pi- pj). (p- pj) < 0 for all cables {i,j}. If c is any proper nonzero self stress
                                                                                                                                        for G(p), then, by [7], the associated stress matrix ft is negative semidefinite with
                                                                                                                                        only the affine motions in the kernel. It is easy to check, due to the convex nature of
                                                                                                                                                                                               :
                                                                                                                                        the polygon and the cabling, that (p’)TFtp’ 0. Thus (p’)Ttp’ < 0. Thus by the
                                                                                                                                        second-order stress test, Corollary 5.2.1, p extends to a second-order flex (p, p") that
                                                                                                                                        is strict on all cables. But the subframework G0(p) of G(p) consisting of just the bars
                                                                                                                                        is just a convex polygon and so is independent. Thus Proposition 6.1.1 applies to show
                                                                                                                                        that there is a flex p(t) of G(p) such that Dt[p(t)]t=o p’ and D[p(t)][=o
                                                                                                                                        But since (p’, p") is strict on all cables, p(t) is a nontrivial continuous flex of G(p) as
                                                                                                                                        well. Thus G(p) is not rigid, and the result is proved.
                                                                                                                                              COROLLARY 6.2.2. If a convex b-c polygon in the plane with v vertices has less
                                                                                                                                        than v- 2 cables, then it is not rigid.
                                                                                                                                              Proof. At least v- 2 cables are needed to make the tensegrity framework infinites-
                                                                                                                                        imally rigid.
                                                                                                                                              Remark 6.2.1. When one is attempting to show directly that a particular convex
                                                                                                                                        b-c polygon is not rigid in the plane, one might be tempted to force some of the
                                                                                                                                        stressed cables to be bars in order to decrease the "degrees of freedom" and simplify
                                                                                                                                        the calculation. For example, the framework G(p) of Figure 19 is not rigid. It is
                                                                                                                                                           SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                     487
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                            FI(. 19.   A flexible framework in the plane (a), with the corresponding first-order flex (b).

                                                                                                                                        obtained by forcing two of the cables of Figure 14a to be bars. (If the horizontal cable
                                                                                                                                        is changed to a strut (or bar), then the framework becomes rigid.)
                                                                                                                                             The subframework G0(p), consisting of just the bars, is independent: G(p) has a
                                                                                                                                        first-order flex, and from first-order considerations, as in [I], (0(p) has a continuous
                                                                                                                                        flex. The length of the horizontal cable cannot increase under this flex (by [7]), and
                                                                                                                                        the other cable lengths decrease strictly in their first derivative. Thus we obtain a
                                                                                                                                        continuous flex of G(p).
                                                                                                                                             However, one must be careful in deciding which of the cables to force to be bars.
                                                                                                                                        For example, consider the framework of Figure 20a.

                                                                                                                                                             P8
                                                                                                                                                                                                                   /
                                                                                                                                                 P7                                     P2                     /

                                                                                                                                                                                                       /

                                                                                                                                                                                        P3

                                                                                                                                                             P                  P4
                                                                                                                                                       a                                          b
                                                                                                                                                           FIG. 20. Framework (a) is rigid because subframework (b) is rigid.

                                                                                                                                             We have changed three of the stressed cables of Figure 3c to bars, and we consider
                                                                                                                                        only {I,6}, {4, 7}, and {3,8} from the rest of the cables of Figure 3c. There is a
                                                                                                                                        proper stress w involving only members among the pairs of the first six vertices, since
                                                                                                                                        pl,..., P6 lie on a circle. See Figure 20b for this c-b subframework, which is rigid by

                                                                                                                                            Considering pl,p3,p4, and p6 as a pinned rigid subset, then the vertices
                                                                                                                                        p,p3,p4,p6,pT,p8 determine an infinitesimally rigid framework. So the whole frame-
                                                                                                                                        work G(p) in Figure 20a is rigid.
                                                                                                                                             On the other hand, in G(p), the subframework determined by just the bars is
                                                                                                                                        independent, as with our proof of Roth’s conjecture. Also, all the proper self stresses
                                                                                                                                        of Figures 3c are proper self stresses of G(p) as well, and there is a nontrivial first-
                                                                                                                                        order flex p of Figure 3c that is a nontrivial first-order flex of G(p). Why can’t we
                                                                                                                                        then conclude, as we did with our proof of Roth’s conjecture, that G(p) is flexible by
                                                                                                                                        488                          R. CONNELLY AND W. WHITELEY

                                                                                                                                        extending p’ to s strict second-order flex (p’, p") of G(p) (using the strict second-order
                                                                                                                                        stress test, Corollary 5.2.1)? The reason we cannot apply the second-order stress test
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                        is because we must consider all proper self stresses of G(p), not just those coming
                                                                                                                                        from Figure 3c. In fact, G(p) has more self stresses to consider due to the added
                                                                                                                                        bars. When the added stresses are considered, it turns out that G(p) is even prestress
                                                                                                                                        stable.
                                                                                                                                             The moral of the story is that if one wants to add interior bars, as in Figure 19,
                                                                                                                                        and keep the framework flexible, then one must not only be careful that the added bars
                                                                                                                                        keep the bar subframework independent and do not destroy the infinitesimal flexes,
                                                                                                                                        but also be sure that the new bars do not introduce any new proper self stresses to
                                                                                                                                        the whole framework.
                                                                                                                                              A. Appendix on replacement principles.
                                                                                                                                             A.1. From bar frameworks to cables and struts. Recall from 2.3 that if a
                                                                                                                                        bar framework is infinitesimally rigid, with a nonzero self stress, we can replace some
                                                                                                                                        of the bars with cables and struts, following the signs of the self stress. (See [29].)
                                                                                                                                             Similarly, from 3.4, if a bar framework is prestress stable with a nontrivial self
                                                                                                                                        stress w, then we are able to replace some of the bars with cables or struts, following
                                                                                                                                        the signs of this self stress
                                                                                                                                             For a second-order rigid bar framework, we have no such replacement principle.
                                                                                                                                        If the framework is not prestress stable, we must check the signs of all stresses used
                                                                                                                                        to block the cone of first-order flexes. If these all agree on a specific sign, then the
                                                                                                                                        corresponding bar can be replaced, while preserving second-order rigidity.
                                                                                                                                             For a framework which is rigid, by some other test, we know of no generM re-
                                                                                                                                        placement principle. In the following, we show how to replace cables and struts with
                                                                                                                                        bars.
                                                                                                                                             A.2. Equivalent bar frameworks for prestress stability. Given a tenseg-
                                                                                                                                        rity framework with cables and struts, we can always replace all members with bars.
                                                                                                                                        This replacement will, of course, preserve any rigidity in the framework. In fact it
                                                                                                                                        may increase the rigidity, turning a nonrigid framework into a rigid framework, a
                                                                                                                                        second-order rigid framework into a prestress stable framework, or a prestress stable
                                                                                                                                        framework into a first-order rigid framework. We would like a more delicate replace-




                                                                                                                                                 -
                                                                                                                                        ment principle which leaves the rigidity, prestress stability, or second-order rigidity
                                                                                                                                        unchanged.
                                                                                                                                              We associate a special bar framework with a tensegrity framework, which does
                                                                                                                                        not depend on fixing a self stress. Suppose some framework G(p) has a cable {i,j}
                                                                                                                                        with p pj. We can then replace the cable by two bars {i,k} and {k,j} and place
                                                                                                                                        pk on the open line segment between pi and pj to get a framework as in Figure 21a.
                                                                                                                                              Similarly, a strut {i, j} can be replaced by two brs {i, k} nd {k, j}, but now we
                                                                                                                                        insist that pa be on the line through pi and pj but outside the closed line segment
                                                                                                                                        between pi and pj as in Figure 21b.
                                                                                                                                              We call the above processes splitting a cable and splitting a strut, respectively. It
                                                                                                                                        is clear that such splittings do not change the rigidity of a framework in IRd for d >_ 2,
                                                                                                                                        but any such splitting creates a framework that is not first-order rigid. In fact we can
                                                                                                                                        split all the cables and struts of G(p) to create what we shall call an equivalent bar
                                                                                                                                                                            rigid       o. y         is r g d.
                                                                                                                                              We next look at the relation between splitting members and prestress stability.
                                                                                                                                        Suppose w is a proper self stress for the tensegrity framework G(p), and {i, j} is
                                                                                                                                                            SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                              489
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                              FIG. 21. Replacing a cable (a) and a strut (b) with "equivalent" pairs of bars preserving pre-
                                                                                                                                        stress stability.

                                                                                                                                        cable or strut for G. Suppose G(p) is split along {i, j} at pk. Define

                                                                                                                                                                               dik     02ij
                                                                                                                                                                                              IP
                                                                                                                                                                           wi ]pi      phi
                                                                                                                                                                 &JR             IPj    Pil        if   wij < 0

                                                                                                                                        and &, Wm for {g, m} {i, k} and {g, m} =fi {j, k}, where py is between pi and
                                                                                                                                        pa when wij < 0. It is easy to check that & defined above is a self stress for ((17)), the
                                                                                                                                        split framework.
                                                                                                                                              PROPOSITION A.2.1. Let G(p) be any tensegrity framework with a proper strict
                                                                                                                                        self stress w. Let ()) be the framework split along any cable or strut. Then w
                                                                                                                                        stabilizes G(p) if and only if & stabilizes ()).


                                                                                                                                                                   .
                                                                                                                                              Proof. By Proposition 3.4.2 we need only consider a space of first-order flexes pl
                                                                                                                                        of G(p) that are complementary to the trivial first-order flexes and then evaluate them
                                                                                                                                        on the form determined by

                                                                                                                                                                 =       A similar statement holds for (15). By the first-order
                                                                                                                                        stress test since wiy 0 we know that (pi p). (p pj) 0. By adding a trivial
                                                                                                                                        first-order flex to pl we may consider some space of first-order flexes of G(p) that has
                                                                                                                                        p pjl 0. Similarly for (15) we may consider only those first-order flexes t5’ that
                                                                                                                                        are the direct sum of p/ on the vertices of G(p) and p which is perpendicular to
                                                                                                                                        pi    pj, where k is the splitting vertex.
                                                                                                                                             We evaluate ( at 15/"



                                                                                                                                                                            E IP Pml + Wik]Pl + Wjc]PI :
                                                                                                                                                                                              2         2


                                                                                                                                                                         --(p’)Tap’"
                                                                                                                                        It is easy to check (even for struts) that wi + w > 0. Thus is positive definite
                                                                                                                                        on its complementary space of nontrivial first-order flexes if and only if t is positive
                                                                                                                                        definite on its corresponding space.
                                                                                                                                             COROLLARY A.2.2. Let G(p) be any tensegrity framework and ()) the equiv-
                                                                                                                                        alent bar framework obtained by splitting all the cables and struts of nonzero length.
                                                                                                                                        490                            R. CONNELLY AND W. WHITELEY

                                                                                                                                        Then G(p) is prestress stable with a strict proper self stress if and only if ()) is
                                                                                                                                        prestress .stable.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                             Thus, if we wish, we can "reduce" the problem of when a framework is prestress
                                                                                                                                        stable to the case when all the members are bars.
                                                                                                                                             A.3. Equivalent bar frameworks for second-order rigidity. If we have
                                                                                                                                        a tensegrity framework with no strict proper self stress, such as in Figure 9b, then
                                                                                                                                        replacing this with the equivalent pair of bars can destroy second-order rigidity (but
                                                                                                                                        not rigidity). For example, a second-order flex is indicated on Figure 22.




                                                                                                                                              FIG. 22. A second-order flexible (but rigid) bar framework equivalent to a second-order rigid
                                                                                                                                        tensegrity framework.

                                                                                                                                             If we restrict ourselves to tensegrity frameworks in which all cables and struts
                                                                                                                                        have nonzero coefficients in some self stress, then we can switch to the equivalent bar
                                                                                                                                        framework to check second-order rigidity. (Recall that for a tensegrity framework a
                                                                                                                                        proper self stress is strict if wij 0 for every cable or strut.) We omit the proof, which
                                                                                                                                        is not difficult. See 5.2 and the second-order stress test.
                                                                                                                                             PROPOSITION A.3.1. A tensegrity framework with a strict proper self stress is
                                                                                                                                        second-order rigid if and only if the equivalent bar framework is second-order rigid.
                                                                                                                                             Acknowledgments. This work was provoked by the stimulating exchanges at
                                                                                                                                        the workshops on tensegrity frameworks and rigidity of triangulated surfaces held at
                                                                                                                                        the Universit de Montreal during February 1987. We thank all of the participants,
                                                                                                                                        with particular thanks to Tibor Tarnai, Zsolt Gaspar, Tim Havel, and Ben Roth. We
                                                                                                                                        also thank Gerard Laman for several corrections to an earlier draft.


                                                                                                                                                                                  REFERENCES
                                                                                                                                          [1] L. ASIMOW AND B. ROTH, The rigidity of graphs, Trans. Amer. Math. Soc., 245 (1978),
                                                                                                                                                 pp. 279-289.
                                                                                                                                          [2] ,        The rigidity of graphs II, J. Math. Anal. Appl., 68 (1979), pp. 171-190.
                                                                                                                                          [3] E. BOLKER AND B. ROTH, When is a bipartite graph a rigid framework? Pacific J. Math., 90
                                                                                                                                                  (1980), pp. 27-44.
                                                                                                                                          [4] C. R. CALLADINE, Buckminister Fuller’s "tensegrity" structures and Clerk Maxwell’s rules for
                                                                                                                                                  the construction of stiff frames, Internat. J. Solids Structures, 14 (1978), pp. 161-172.
                                                                                                                                          [5] C. a. CALLADINE AND S. PELLEGRINO, First-order infinitesimal mechanisms, Internat. J.
                                                                                                                                                  Solids Structures, 27 (1991), pp. 505-515.
                                                                                                                                          [6] R. CONNELLY, The rigidity of certain cables frameworks and the second-order rigidity of arbi-
                                                                                                                                                  trarily triangulated convex surfaces, Adv. Math., 37 (1980), pp. 272-299.
                                                                                                                                          [7] ,        Rigidity and energy, Invent. Math., 66 (1982), pp. 11-33.
                                                                                                                                                       SECOND-ORDER RIGIDITY AND PRESTRESS STABILITY                                       491

                                                                                                                                         [8] R. CONNELLY, Basic concepts of rigidity, in The Geometry of Rigid Structures, H. Crapo and
                                                                                                                                                 W. Whiteley, eds., manuscript.
Downloaded 01/01/13 to 150.135.135.70. Redistribution subject to SIAM license or copyright; see http://www.siam.org/journals/ojsa.php




                                                                                                                                         [9]          Basic concepts of infinitesimal rigidity, in The Geometry of Rigid Structures, H. Crapo
                                                                                                                                                 and W. Whiteley, eds., manuscript.
                                                                                                                                        [10]          Basic concepts of static rigidity, in The Geometry of Rigid Structures, H. Crapo and
                                                                                                                                                 W. Whiteley, eds., manuscript.
                                                                                                                                        [11]   .,     Rigid circle and sphere packings Part I: Finite packings, Structural Topology, 14 (1988),
                                                                                                                                                 pp. 43-60.
                                                                                                                                        [12]   .,     Rigid circle and sphere packings Part II: Infinite packings with finite motion, Structural
                                                                                                                                                 Topology, 16 (1991), pp. 57-76.
                                                                                                                                        [13] R. CONNELLY AND W. WHITELEY, The stability of tensegrity frameworks, J. Space Structures,
                                                                                                                                                 7 (1992), pp. 153-163.
                                                                                                                                        [14] H. CRAPO AND W. WHITELEY, Stresses in frameworks and motions of panel structures: A
                                                                                                                                                 projective geometry introduction, Structural Topology, 6 (1982), pp. 42-82.
                                                                                                                                        [15] J. FRANKLIN, Methods of Mathematical Economics, Springer-Verlag, New York, 1980.
                                                                                                                                        [16] H. GLiJCK, Almost all simply connected surfaces are rigid, in Geometric Topology, Lecture
                                                                                                                                                 Notes in Math 438, Springer-Verlag, Berlin, New York, 1975, pp. 225-239.
                                                                                                                                        [17] B. GRONBAUM, Convex Polytopes, Interscience, New York, 1967.
                                                                                                                                        [18] B. GRiJNBAUM AND G. C. SHEPARD, Lectures on Lost Mathematics, Mimeographed notes, Uni-
                                                                                                                                                 versity of Washington, Seattle, 1975.
                                                                                                                                        [19]   ,      Lectures on Lost Mathematics, Mimeographed notes, University of Washington, Seattle,
                                                                                                                                                 (reissued for the special section on rigidity at the 760th meeting of the A.M.S.), 1978
                                                                                                                                        [20] N. H. KUIPEa, Spheres polyhedriques flexible dans E 3, d’dpres Robert Connelly, Seminaire
                                                                                                                                                 Bourbaki, 541 (1978), pp. 1-22.
                                                                                                                                        [21] E. KTTER, ber die MSglichkeit, n Punkte in der Ebene oder im Raume dutch weniger als
                                                                                                                                                 2n- 3 oder 3n- 6 Stiibe yon ganz unveriinderlicher Liinge universchieblich miteinander
                                                                                                                                                 zu verbinden, Festschrift Heinrich Miiller-Breslau, 1912, pp. 61-80.
                                                                                                                                        [22] E. N. KUZNETSOV, Underconstrained structural systems, Internat. J. Solids Structures, 24
                                                                                                                                                 (1988), pp. 153-163.
                                                                                                                                        [23]   ,      On immobile kinematic chains and a fallacious matrix analysis, J. Appl. Mech., Brief
                                                                                                                                                 Notes, 56 (1989), pp. 222-224.
                                                                                                                                        [24]   ,      Letter to the editor, Internat. J. Solids Structures, 27 (1991), pp. 517-519.
                                                                                                                                        [25]   ,      Systems with infinitesimal mobility: Part I-Matrix analysis and first-order mobility,
                                                                                                                                                 J. Appl. Mech., 58 (1991), pp. 513-519.
                                                                                                                                        [26]   ,      Systems with infinitesimal mobility: Part II-Compound and higher-order infinitesimal
                                                                                                                                                 mechanisms, J. Appl. Mech., 58 (1991), pp. 520-526.
                                                                                                                                        [27]   ,       Underconstrained Structural Systems, Springer-Verlag, Berlin, New York, 1991.
                                                                                                                                        [28] S. PELLEGRINO AND C. R. CALLADINE, Matrix analysis of statically and kinematically indeter-
                                                                                                                                                 minate frameworks, Internat. J. Solids Structures, 32 (1986), pp. 409-428.
                                                                                                                                        [29] B. ROTH AND W. WmTELEY, Tensegrity frameworks, Trans. Amer. Math. Soc., 265 (1981),
                                                                                                                                                 419-446.
                                                                                                                                        [30] J. SZABO AND L. KOLL.a, Structural Design of Cable-Suspended Roofs, Akademiai Kiado,
                                                                                                                                                 Budapest, 1984.
                                                                                                                                        [31] T. TARNAI, Problems concerning spherical polyhedra and structural rigidity, Structural Topol-
                                                                                                                                                 ogy, 4 (1980), pp. 61-66.
                                                                                                                                        [32] A. W. TUCKER, Dual systems of homogeneous linear relations, in Linear Inequalities and Re-
                                                                                                                                                 lated Systems H. W. Kuhn and A. W. Tucker, eds., Annals of Math Studies 38, 1956,
                                                                                                                                                 pp. 3-18.
                                                                                                                                        [33] N. WroTE AND W. WHITELEY, The algebraic geometry of stresses in frameworks, SIAM J. Alg.
                                                                                                                                                 Disc. Meth., 8 (1983), pp. 1-32.
                                                                                                                                        [34] W. WHITELEY, Infinitesimal motions of a bipartite framework, Pacific J. Math., 110 (1984),
                                                                                                                                                 pp. 233-255.
                                                                                                                                        [35]   ,      Tensegrity frameworks, in The Geometry of Rigid Structures, H. Crapo and W. White-
                                                                                                                                                 ley, eds., manuscript.
                                                                                                                                        [36]   ,       Second-order rigidity and global rigidity, in The Geometry of Rigid Structures, H.
                                                                                                                                                 Crapo and W. Whiteley, eds., manuscript.
