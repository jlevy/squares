# Archived: Kingbird squares-in-squares Göbel squares

**Source:**
https://kingbird.myphotos.cc/packing/squares_in_squares__Göbel_squares.html  
**Archived:** 2026-09-07  
**Method:** `curl` plus Pandoc; the original HTML is preserved alongside this file. The
path is fetched percent-encoded, as `squares_in_squares__G%C3%B6bel_squares.html`.  
**SHA-256 of HTML:**
`d041c144dd0cbfee78ea0540c212520866476228a7918cd9058ce4606ca7ea4e`

This is an author-maintained descriptive catalogue page. It states the Göbel square
family in closed form — `n = 2(a+1)a + b²` unit squares inside a square of side
`a + 1 + (b/2)√2`, for `a, b` positive integers with `a − 1 < (b/2)√2 < a + 1` — and
renders its members. A closed-form construction gives an upper bound, not a proof of
optimality; the page marks several of these members “Not optimal.”

* * *

Squares in Squares  
Göbel squares  
SVG, high-precision, and categorized list by
<a href="https://github.com/Davidebyzero"
style="text-decoration:none">David Ellsworth</a>  
based on <a
href="https://web.archive.org/web/20230530194618/https://erich-friedman.github.io/packing/squinsqu/"
style="text-decoration:none">original</a> compiled by
<a href="https://erich-friedman.github.io/"
style="text-decoration:none">Erich Friedman</a>

This is a list of Göbel square packings, shown alongside their
alternative packings or rearrangements. For the main list, see [Squares
in Squares](squares_in_squares.html) or [Squares in Squares: Triangular
Table View](squares_in_squares__triangular_table.html).

Where the word "alternative" is used, this designates an alternative
packing, which is enclosed within the same-sized bounding square as
another packing, but cannot be reached by continuously translating
and/or rotating the squares in that packing. When the packing can be
reached by such continuous transformations, the word "rearrangement" is
used.

For more information on each packing, view its SVG's source code. In
browsers that don't provide an easy way to do this, you can prepend the
URL with "`view-source:`" (without the quotes).

Generalizing from Frits Göbel's findings, if \$a,b \in \mathbb{Z}^+\$
satisfy \$a\\-\\1 \lt {1\over 2}b\sqrt 2 \lt a\\+\\1\$, then \$n =
2(a\\+\\1)a\\+\\b^2\$ unit squares can be packed inside a square of side
\$s = a\\+\\1\\+\\{1\over 2}b\sqrt 2\$. This is accomplished by placing
a \$b\\×\\b\$ square of squares at a \$45°\$ angle in the center,
surrounded by four "staircases" each having \$a\$ steps. This is better
than a trivial packing iff \$s \lt \bigl\lceil \sqrt{n} \bigr\rceil\$.

David Ellsworth found that the arrangement in which all four corner
squares of the \$b\\×\\b\$ square are unrotated is attainable iff \$0 \\
\le \\ {1\over 2}b\sqrt 2 - a \\ \le \\ 2\sqrt 2-2\$, and is an
alternative packing iff \$4 - b + (a - {5\over 4})\sqrt 2 - {1\over
2}\sqrt 5 \lt 0\$, which is the case for \$s(28)\$, \$s(1544)\$,
\$s(4009)\$, \$s(9465)\$, \$s(14716)\$, \$s(32149)\$, \$s(41340)\$,
\$s(56308)\$, \$s(68285)\$, \$s(101956)\$, etc.

Zoom:

0.25×

 

1/3×

 

0.5×

 

2/3×

 

3/4×

 

1×

 

1.5×

 

2×

 

SVG Edit Mode: OFF

------------------------------------------------------------------------

<div class="wrapper">

<div class="container">

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">5.<br />
<a href="square-5.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 2 + { 1\over 2}\sqrt 2 =
\Nn{2.70710678118654}$<br />
<a href="squares_in_squares__rigid.html">Rigid.</a><br />
Proved by Frits Göbel<br />
in early 1979.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">28.<br />
<a href="square-28_r1.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-28_r1b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-28.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 3 + 2 \sqrt 2 = \Nn{5.82842712474619}$<br />
Found by Frits Göbel<br />
in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = 3 + 2 \sqrt 2 = \Nn{5.82842712474619}$<br />
<a href="squares_in_squares__rigid.html">Semi-rigid</a> alternative with
minimal rotated squares found by David Ellsworth<br />
in June 2023.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s =
{}^{6}🔒 = \Nn{5.82444461667405}$</span> <span
class="frames">$s^6-24s^5+212s^4-812s^3+1025s^2+882s-1615=0$</span>
</span><br />
<a href="squares_in_squares__rigid.html">Rigid.</a><br />
Found by David Ellsworth<br />
in December 2025, using his modified version of Thomas Schadt's
simulated annealing program, starting from randomness.<br />
Beats the Göbel square.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">40.<br />
<a href="square-40.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 4 + 2 \sqrt 2 = \Nn{6.82842712474619}$<br />
<a href="squares_in_squares__rigid.html">Rigid.</a><br />
Found by Frits Göbel<br />
in early 1979.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">65.<br />
<a href="square-65.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-65b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 5 + { 5\over 2}\sqrt 2 =
\Nn{8.53553390593273}$<br />
Found by Frits Göbel<br />
in early 1979.</td>
<td></td>
<td class="desc">$s = 5 + { 5\over 2}\sqrt 2 =
\Nn{8.53553390593273}$<br />
Rearrangement with minimal rotated squares found by David
Ellsworth<br />
in June 2023.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">89.<br />
<a href="square-89.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-89b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 5 + { 7\over 2}\sqrt 2 =
\Nn{9.94974746830583}$<br />
Found by Evert Stenlund in 1980,<br />
by extending a pattern found<br />
by Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 5 + { 7\over 2}\sqrt 2 =
\Nn{9.94974746830583}$<br />
Rearrangement with minimal rotated squares found by David
Ellsworth<br />
in June 2023.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">109.<br />
<a href="square-109.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 6 + { 7\over 2}\sqrt 2 =
\Nn{10.94974746830583}$<br />
Extends a pattern found<br />
by Frits Göbel in early 1979.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">124.<br />
<a href="square-124.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-124b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 6 + 4 \sqrt 2 = \Nn{11.65685424949238}$</td>
<td></td>
<td class="desc">$s = 6 + 4 \sqrt 2 = \Nn{11.65685424949238}$<br />
Rearrangement with minimal rotated squares.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">148.<br />
<a href="square-148.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 7 + 4 \sqrt 2 = \Nn{12.65685424949238}$</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">233.<br />
<a href="square-233.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-233b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 8 + {11\over 2}\sqrt 2 =
\Nn{15.77817459305202}$</td>
<td></td>
<td class="desc">$s = 8 + {11\over 2}\sqrt 2 =
\Nn{15.77817459305202}$<br />
<a href="square-233b.html">Rearrangement</a> with minimal rotated
squares found by David Ellsworth<br />
in November 2024.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">265.<br />
<a href="square-265.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-265b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 9 + {11\over 2}\sqrt 2 =
\Nn{16.77817459305202}$</td>
<td></td>
<td class="desc">$s = 9 + {11\over 2}\sqrt 2 =
\Nn{16.77817459305202}$<br />
Rearrangement with minimal rotated squares found by David
Ellsworth<br />
in November 2024.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">376.<br />
<a href="square-376.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 10 + {14\over 2}\sqrt 2 =
\Nn{19.89949493661166}$</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">416.<br />
<a href="square-416.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 11 + {14\over 2}\sqrt 2 =
\Nn{20.89949493661166}$</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">445.<br />
<a href="square-445.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-445c.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 11 + {15\over 2}\sqrt 2 =
\Nn{21.60660171779821}$</td>
<td></td>
<td class="desc">$s = 11 + {15\over 2}\sqrt 2 =
\Nn{21.60660171779821}$<br />
Rearrangement with minimal rotated squares found by David
Ellsworth<br />
in November 2024.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1544.<br />
<a href="square-1544.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1544b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 20 + 14\sqrt 2 = \Nn{39.79898987322333}$</td>
<td></td>
<td class="desc">$s = 20 + 14\sqrt 2 = \Nn{39.79898987322333}$<br />
Alternative with minimal rotated squares found by David Ellsworth<br />
in November 2024.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1624.<br />
<a href="square-1624.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 21 + 14 \sqrt 2 = \Nn{40.79898987322333}$</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1765.<br />
<a href="square-1765_r0.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1765.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 22 + {29\over 2}\sqrt 2 =
\Nn{42.50609665440987}$<br />
Not optimal.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s = 🔒 =
\Nn{42.48797851186022}$</span> <span
class="frames">$2s^4-212s^3+8129s^2-148140s+1362276=0$</span>
</span><br />
Found by Károly Hajba<br />
in November 2024.<br />
Improved by David Ellsworth<br />
in November 2024.<br />
Beats the Göbel square.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">4009.<br />
<a href="square-4009_r0.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-4009_r0b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 32 + {45\over 2}\sqrt 2 =
\Nn{63.81980515339463}$<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = 32 + {45\over 2}\sqrt 2 =
\Nn{63.81980515339463}$<br />
Alternative with minimal rotated squares found by David Ellsworth<br />
in November 2024.</td>
<td></td>
<td class="desc">$s &lt; 63.78564927$<br />
Beats the Göbel square.<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">9465.<br />
<a href="square-9465_r0.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-9465_r0c.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 49 + {69\over 2}\sqrt 2 =
\Nn{97.79036790187177}$<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = 49 + {69\over 2}\sqrt 2 =
\Nn{97.79036790187177}$<br />
Alternative with minimal rotated squares found by David Ellsworth<br />
in November 2024.</td>
<td></td>
<td class="desc">$s &lt; 97.70584$<br />
Beats the Göbel square.<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

</div>

</div>

------------------------------------------------------------------------

For more details, see Erich Friedman's paper on the subject: [Packing
Unit Squares in Squares: A Survey and New
Results](https://erich-friedman.github.io/papers/squares/squares.html)
(or [David Ellsworth's edit](squares.html)).
