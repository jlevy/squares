           Packing of 11 unit squares in a square with minimum size
                            Walter Trump, 2023-02-27, last update 2023-03-05
Abstract
We claim that the densest known packing of 11 unit squares in a square is still the one found in 1979. It cannot
be improved by computer programs as long as the same geometrical arrangement of the unit squares is used.

The packing was first published correctly (but with an unprecise drawing) in a book of Martin Gardner. [1]

   The following drawing of the packing was sent to Martin Gardner 1979 by Walter Trump.
    As shown on page 2, a slight improvement is not possible because the packing is rigid.




          Important:        The vertices D11 and C9 lay on edges of the large square.
                            The vertices C2 , D3 , A6 , B5 and C4 lay on edges of unit squares.
          (It can be proved that the distance of the vertices D11 and D6 is exactly 1.)
           is the smallest angle between an edge of an inner square (7, 8, 9, 10, 11)
          and an edge of the large square.
          k = 3 + s is the length of an edge of the large square.
           and k are constants given by two equations, as shown on page 2.
                                                         -2-

Implicit equation for the tilt angle , sent to Martin Gardner in 1979.




This equation has only one solution  with 0°    90°.

with         ( )          ( )             ( )             [ (             )                                ]

(In 2007 I could replace s and t by c:
the largest real solutions is    ( ). )
Precise solution:            40.18193729032971646523034236806062154252265849634355838751445324...°
Sent to Gardner 1979:        40.18193730°      (relative error < 2.5  1010)
The calculation was done with the programmable RPN pocket calculator Hewlett-Packard 67.




                                                                      Pictures from 2023, my HP 67 still works.

The length k  s(11) of the sides of the large square can be calculated easily:
Precise result              3.877083590022814177307897060100962706376455668463162560763968342...
Sent to Gardner 1979:       3.8770835903        (I should have deleted the last digit. 11 digits are too much for HP 67.)
 The accuracy of k is only limited by the available computer hard- and software.
The packing sent to Martin Gardner is exactly defined by the fact that certain vertices of the unit squares
lay on edges of other unit squares or edges of the large square.
The geometrical object is absolutely rigid, no unit square can be rotated or translated. 
                              It is impossible to slightly improve this packing.
                         Any improved packing would have to have an essentially
                          different geometrical arrangement of the unit squares.


In his square packing publication 1998 Erich Friedman wrote s(11)  3.8772 [2]. It was my fault for not
realizing this and proposing to refine it to s(11) < 3.8771. Gensane and Ryckelynck [5] thought s(11) >
3.8771 and assumed 2004 that their program could slightly improve the packing from 1979. But this is
not possible as shown above. Since version 4 (Nov 8, 2005) of his article "Packing Unit Squares in Squares:
A Survey and New Results" Erich Friedman writes s(11) < 3.8771.[3] [4]
In an email from February 2023 Thierry Gensane confirmed that their program could not improve the
packing from 1979.
                                                                                  Walter Trump, ms(at)trump.de
Find more details and letters from Martin Gardner in
www.trump.de/square-packing/
                                                       -3-


References
[1]   Gardner, Martin (1992) "Fractal Music, Hypercards and more". New York: W. H. Freeman
      pp. 299, 300

[2]   Friedman, Erich (1998), "Packing unit squares in squares: a survey and new results", version 1,
      Electronic Journal of Combinatorics, Dynamic Survey 7
      p. 7

[3]   Friedman, Erich (2005), "Packing unit squares in squares: a survey and new results", version 4,
      Electronic Journal of Combinatorics, Dynamic Survey 7
      Figure 6

[4]   Friedman, Erich (2009), "Packing unit squares in squares: a survey and new results", version 5,
      Electronic Journal of Combinatorics, Dynamic Survey 7
      Figure 6

[5]   Gensane, Thierry; Ryckelynck, Philippe (2005), "Improved dense packings of congruent squares in a
      square", Discrete & Computational Geometry, doi:10.1007/s00454-004-1129-z
      pp. 106, 107
