# Archived: Kingbird squares-in-squares Göbel strips

**Source:**
https://kingbird.myphotos.cc/packing/squares_in_squares__Göbel_strips.html  
**Archived:** 2026-09-07  
**Method:** `curl` plus Pandoc; the original HTML is preserved alongside this file. The
path is fetched percent-encoded, as `squares_in_squares__G%C3%B6bel_strips.html`.  
**SHA-256 of HTML:**
`94840551cd3f250a3658db8c99c66193bb562e765a1bb32cbef884313d43cf35`

This is an author-maintained descriptive catalogue page. It states the Göbel strip
family in closed form — `n = (a+1)a + 2 + b` unit squares, with `b = 1 + ⌊(a−1)√2⌋`,
inside a square of side `a + 1 + (1/2)√2` — and renders its members. A closed-form
construction gives an upper bound, not a proof of optimality; the page marks several of
these members “Not optimal.”

Five entries in the retained HTML sit inside comment blocks and are therefore not
rendered by the page: `n = 687`, `1460`, `2937`, `2938` and `3047`. Pandoc drops
unrendered markup, so they are absent from this transcription and present in the `.html`
beside it. The largest rendered entry here is `n = 2135`.

* * *

Squares in Squares  
Göbel strips  
SVG, high-precision, and categorized list by
<a href="https://github.com/Davidebyzero"
style="text-decoration:none">David Ellsworth</a>  
based on <a
href="https://web.archive.org/web/20230530194618/https://erich-friedman.github.io/packing/squinsqu/"
style="text-decoration:none">original</a> compiled by
<a href="https://erich-friedman.github.io/"
style="text-decoration:none">Erich Friedman</a>

This is a list of Göbel strip packings, shown alongside their
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

Generalizing from Frits Göbel's findings, with \$a \in \mathbb{Z}^+\$
and \$b=1\\+\\\lfloor{(a\\-\\1)\sqrt 2}\rfloor\$, a Göbel strip consists
of \$n = (a\\+\\1)a\\+\\2\\+\\b\$ unit squares packed inside a square of
side \$s = a\\+\\1\\+\\{1\over 2}\sqrt 2\$. This is accomplished by
placing a 1-width strip of \$b\$ squares at a \$45°\$ angle in the
center, flanked by two unrotated squares at the corners, and sandwiched
by two unrotated "staircases" each having \$a\$ steps. This yields the
best known packing for all \$a\\\lt\\44\$ except for \$a\\=\\3\$.

Most Göbel strips also have a "simplified" alternative packing or
rearrangement in which the \$45°\$ strip can contain \$b\\+\\2\$
squares, without any unrotated squares flanking it at the corners. If
\$(3+2\lfloor{(a-1)\sqrt 2}\rfloor)\sqrt 2-4a \> 0\$, then this is not
possible at all, and it can contain no more than \$b\$ squares.
Otherwise, if \$(3+\lfloor{(a-1)\sqrt 2}\rfloor)\sqrt 2-2a-2 \> 0\$,
then the strip can only contain \$b\\+\\1\$ squares, and needs to be
flanked at one corner by an unrotated square.

David W. Cantrell found in 2005 that there are alternative packings with
minimal rotated squares for \$s(27)\$ and later, filling them out up to
\$s(84)\$. David Ellsworth noticed that the \$s(52)\$ with minimal
rotated squares is rigid (which coincides with its Göbel strip
counterpart have very little space to slide), and later found that the
pattern of rigid packings continues for every \$a ≡ 1\\\mod\\5\$.

David Ellsworth found in 2024 that whereas the general formula for the
number of minimal rotated squares (i.e. number of copies of \$s(5)\$ in
the packing) is \$\lfloor{(2a+3)/5}\rfloor\$, the number of rotated
squares needed to match the efficiency of the Göbel strip is
\$\lfloor{(a-1)\sqrt 2}\rfloor+2-a\$. Up to and including \$s(331)\$,
these two formulae agree with each other (because \$\sqrt 2\\-\\1
\approx 0.4\$), but at \$s(369)\$, they differ for the first time.
Following that point there are only \$26\$ more minimal rotated square
packings for which they agree (out of \$53\$), the last one being
\$s(5213)\$. This includes all of the rigid ones, which is not a
coincidence – they have the least wasted space. But since Göbel strips
are inoptimal starting at \$s(2043)\$ or possibly earlier, there are
actually only at most \$9\$ alternative packings with minimal rotated
squares for Göbel strips that may be optimal that are lost due to the
divergence between the two formulae: \$s(369)\$, \$s(586)\$, \$s(853)\$,
\$s(974)\$, \$s(1170)\$, \$s(1311)\$, \$s(1537)\$, \$s(1698)\$, and
\$s(1954)\$.

Starting at \$s(18)\$, there is another type of Göbel strip, in which
the strip is \$b+1\$ squares long, and is touched by the two unrotated
squares in the corners, not the two "staircases" as the others are.
These have \$n = (a\\+\\1)a\\+\\3\\+\\b\$ and \$s =
2\\+\\(b\\+\\1){1\over 2}\sqrt 2\$, and have a chance at being optimal
when \$\\s-{1\over 2}\sqrt 2\\\$ is small. For example, with \$a=13\$,
\$n=202\$ and \$\\s-{1\over 2}\sqrt 2\\ \approx 0.02081528\$ which is
indeed small.

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
Rigid.<br />
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
<td class="box">10.<br />
<a href="square-10.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-10s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-10b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 3 + {1\over 2}\sqrt 2 =
\Nn{3.70710678118654}$<br />
Found by Frits Göbel<br />
in early 1979.</td>
<td></td>
<td class="desc">$s = 3 + {1\over 2}\sqrt 2 =
\Nn{3.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 3 + {1\over 2}\sqrt 2 =
\Nn{3.70710678118654}$<br />
Alternative with minimal rotated squares.<br />
Adds an "L" to $s(5)$.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">17.<br />
<a href="square-17_r1a.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-17_r1s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-17_r1.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-17_r2.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-17.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 4 + {1\over 2}\sqrt 2 =
\Nn{4.70710678118654}$<br />
Found by Frits Göbel in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = 4 + {1\over 2}\sqrt 2 =
\Nn{4.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 4 + {1\over 2}\sqrt 2 =
\Nn{4.70710678118654}$<br />
Alternative with minimal rotated squares.<br />
Adds two "L"s to $s(5)$.</td>
<td></td>
<td class="desc">$s = {7\over 3} + {5\over 3}\sqrt 2 =
\Nn{4.69035593728849}$<br />
Found by Pertti Hämäläinen<br />
in 1980.<br />
Beats the Göbel strip.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s =
{}^{18}🔒 = \Nn{4.67553009360455}$</span> <span
class="frames">$4775s^{18}-190430s^{17}+3501307s^{16}-39318012s^{15}+300416928s^{14}-1640654808s^{13}+6502333062s^{12}-18310153596s^{11}+32970034584s^{10}-18522084588s^9-93528282146s^8+350268230564s^7-662986732745s^6+808819596154s^5-660388959899s^4+358189195800s^3-126167814419s^2+26662976550s-2631254953=0$</span>
</span><br />
Improved by John Bidwell<br />
in 1998.<br />
Beats the Göbel strip.</td>
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
<td class="box">(18.)<br />
<a href="square-18_r1.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-18_r1r.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-18.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 2 + 2 \sqrt 2 = \Nn{4.82842712474619}$<br />
Found by Frits Göbel<br />
in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = 2 + 2 \sqrt 2 = \Nn{4.82842712474619}$<br />
<a href="squares_in_squares__rigid.html">Rigid</a> alternative found by
David Ellsworth in December 2024.<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = {7\over 2} + {1\over 2}\sqrt 7 =
\Nn{4.82287565553229}$<br />
Found by Pertti Hämäläinen<br />
in 1980.<br />
Beats the Göbel strip.</td>
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
<td class="box">27.<br />
<a href="square-27.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-27s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-27b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 5 + {1\over 2}\sqrt 2 =
\Nn{5.70710678118654}$<br />
Found by Frits Göbel<br />
in early 1979.</td>
<td></td>
<td class="desc">$s = 5 + {1\over 2}\sqrt 2 =
\Nn{5.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 5 + {1\over 2}\sqrt 2 =
\Nn{5.70710678118654}$<br />
Alternative with minimal rotated squares found by David W.
Cantrell<br />
in 2005.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">38.<br />
<a href="square-38.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-38s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-38b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-38c.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 6 + {1\over 2}\sqrt 2 =
\Nn{6.70710678118654}$<br />
Found by Frits Göbel<br />
in early 1979.</td>
<td></td>
<td class="desc">$s = 6 + {1\over 2}\sqrt 2 =
\Nn{6.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 6 + {1\over 2}\sqrt 2 =
\Nn{6.70710678118654}$<br />
Mirror-symmetric alternative with minimal rotated squares found by<br />
David W. Cantrell in 2005.</td>
<td></td>
<td class="desc">$s = 6 + {1\over 2}\sqrt 2 =
\Nn{6.70710678118654}$<br />
Rotationally symmetric rearrangement of alternative with minimal rotated
squares by David Ellsworth in December 2024.</td>
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
<td class="box">52.<br />
<a href="square-52.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-52b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 7 + {1\over 2}\sqrt 2 =
\Nn{7.70710678118654}$<br />
Found by Frits Göbel<br />
in early 1979.</td>
<td></td>
<td class="desc">$s = 7 + {1\over 2}\sqrt 2 =
\Nn{7.70710678118654}$<br />
Rigid alternative with minimal rotated squares found by David W.
Cantrell<br />
in 2005.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">67.<br />
<a href="square-67.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-67s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-67b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-67c.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 8 + {1\over 2}\sqrt 2 =
\Nn{8.70710678118654}$<br />
Found by Evert Stenlund<br />
in early 1980, extending the $s(52)$<br />
found by Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 8 + {1\over 2}\sqrt 2 =
\Nn{8.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 8 + {1\over 2}\sqrt 2 =
\Nn{8.70710678118654}$<br />
Alternative constructed by adding an "L" to the $s(52)$ found by
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 8 + {1\over 2}\sqrt 2 =
\Nn{8.70710678118654}$<br />
Alternative with minimal rotated squares found by David W.
Cantrell<br />
in June 2023.</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">84.<br />
<a href="square-84.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-84s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-84b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-84c.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-84d.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 9 + {1\over 2}\sqrt 2 =
\Nn{9.70710678118654}$<br />
Found by Evert Stenlund<br />
in early 1980, extending the $s(52)$<br />
found by Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 9 + {1\over 2}\sqrt 2 =
\Nn{9.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 9 + {1\over 2}\sqrt 2 =
\Nn{9.70710678118654}$<br />
Rearrangement. Can also be constructed by adding an "L" to the $s(67)$
that extends the $s(52)$ found by Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 9 + {1\over 2}\sqrt 2 =
\Nn{9.70710678118654}$<br />
Alternative constructed by adding two "L"s to the $s(52)$ found by
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 9 + {1\over 2}\sqrt 2 =
\Nn{9.70710678118654}$<br />
Alternative with minimal rotated squares found by David W.
Cantrell<br />
in 2005.</td>
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
<td class="box">(85.)<br />
<a href="square-85_r1.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-85b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-85c.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 2 + {11\over 2}\sqrt 2 =
\Nn{9.77817459305202}$<br />
Found by Evert Stenlund<br />
in early 1980.<br />
Extends the $s(18)$ found by<br />
Frits Göbel in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc">$s = {11\over 2} + 3 \sqrt 2 =
\Nn{9.74264068711928}$<br />
Found by Erich Friedman<br />
in 1997.<br />
Beats the Göbel strip.</td>
<td></td>
<td class="desc">$s = {11\over 2} + 3 \sqrt 2 =
\Nn{9.74264068711928}$<br />
Alternative with minimal rotated squares.</td>
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
<td class="box">104.<br />
<a href="square-104.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-104s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-104b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 10 + {1\over 2}\sqrt 2 =
\Nn{10.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 10 + {1\over 2}\sqrt 2 =
\Nn{10.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 10 + {1\over 2}\sqrt 2 =
\Nn{10.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">125.<br />
<a href="square-125.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-125s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-125b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 11 + {1\over 2}\sqrt 2 =
\Nn{11.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 11 + {1\over 2}\sqrt 2 =
\Nn{11.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 11 + {1\over 2}\sqrt 2 =
\Nn{11.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">149.<br />
<a href="square-149.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-149s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-149b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 12 + {1\over 2}\sqrt 2 =
\Nn{12.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 12 + {1\over 2}\sqrt 2 =
\Nn{12.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 12 + {1\over 2}\sqrt 2 =
\Nn{12.70710678118654}$<br />
Rigid alternative with minimal rotated squares found by David Ellsworth
in November 2024, based on the rigid $s(52)$ found by David W. Cantrell
in 2005.</td>
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
<td class="box">174.<br />
<a href="square-174.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-174s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-174b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 13 + {1\over 2}\sqrt 2 =
\Nn{13.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 13 + {1\over 2}\sqrt 2 =
\Nn{13.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 13 + {1\over 2}\sqrt 2 =
\Nn{13.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" data-cellspacing="0" data-border="0">
<colgroup>
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
<col style="width: 11%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">201.<br />
<a href="square-201.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-201s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-201b.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-201d.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-201c.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 14 + {1\over 2}\sqrt 2 =
\Nn{14.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 14 + {1\over 2}\sqrt 2 =
\Nn{14.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 14 + {1\over 2}\sqrt 2 =
\Nn{14.70710678118654}$<br />
Mirror-symmetric alternative with minimal rotated squares arranged by
David Ellsworth in December 2024, based on the technique found by David
W. Cantrell in 2005.</td>
<td></td>
<td class="desc">$s = 14 + {1\over 2}\sqrt 2 =
\Nn{14.70710678118654}$<br />
Rotationally symmetric alternative with minimal rotated squares arranged
by David W. Cantrell in December 2024.</td>
<td></td>
<td class="desc">$s = 14 + {1\over 2}\sqrt 2 =
\Nn{14.70710678118654}$<br />
Alternative combining the $s(52)$ rigid alternative with minimal rotated
squares found by David W. Cantrell in 2005, and the $s(51)$ found by
Károly Hajba<br />
in July 2009.</td>
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
<td class="box">(202.)<br />
<a href="square-202_r1.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-202_r2.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-202.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = {21\over 2} + 3 \sqrt 2 =
\Nn{14.74264068711928}$<br />
Found by David Ellsworth in November 2024, by extending the $s(85)$
found by Erich Friedman in 1997.<br />
Didn't set a record.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s =
{}^{8}🔒 = \Nn{14.73657855744445}$</span> <span
class="frames">$776s^4-(33320+336\sqrt{2})s^3+(528568+7752\sqrt{2})s^2-(3662244+43296\sqrt{2})s+9301325-28968\sqrt{2}=0$</span>
<span
class="frames">$6208s^8-533120s^7+19900352s^6-421620160s^5+5543230416s^4-46288934864s^3+239607688384s^2-702396496296s+891886272841=0$</span>
</span><br />
Improved by David Ellsworth in November 2024, by adapting the technique
from the $s(37)$ found by<br />
David W. Cantrell in September 2002.<br />
Didn't set a record.</td>
<td></td>
<td class="desc">$s = 2 + 9 \sqrt 2 = \Nn{14.72792206135785}$<br />
Extends the $s(18)$ found by<br />
Frits Göbel in early 1979.</td>
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
<td class="box">231.<br />
<a href="square-231.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-231s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-231b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 15 + {1\over 2}\sqrt 2 =
\Nn{15.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 15 + {1\over 2}\sqrt 2 =
\Nn{15.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 15 + {1\over 2}\sqrt 2 =
\Nn{15.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">262.<br />
<a href="square-262.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-262s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-262b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 16 + {1\over 2}\sqrt 2 =
\Nn{16.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 16 + {1\over 2}\sqrt 2 =
\Nn{16.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 16 + {1\over 2}\sqrt 2 =
\Nn{16.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">296.<br />
<a href="square-296.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-296s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-296b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 17 + {1\over 2}\sqrt 2 =
\Nn{17.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 17 + {1\over 2}\sqrt 2 =
\Nn{17.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 17 + {1\over 2}\sqrt 2 =
\Nn{17.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">331.<br />
<a href="square-331.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-331s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-331b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 18 + {1\over 2}\sqrt 2 =
\Nn{18.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 18 + {1\over 2}\sqrt 2 =
\Nn{18.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 18 + {1\over 2}\sqrt 2 =
\Nn{18.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">369.<br />
<a href="square-369.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">368.<br />
<a href="square-369_no_min_rot.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 19 + {1\over 2}\sqrt 2 =
\Nn{19.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 19 + {1\over 2}\sqrt 2 =
\Nn{19.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.</td>
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
<td class="box">408.<br />
<a href="square-408.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-408s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-408b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 20 + {1\over 2}\sqrt 2 =
\Nn{20.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 20 + {1\over 2}\sqrt 2 =
\Nn{20.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 20 + {1\over 2}\sqrt 2 =
\Nn{20.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">449.<br />
<a href="square-449.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-449s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-449b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 21 + {1\over 2}\sqrt 2 =
\Nn{21.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 21 + {1\over 2}\sqrt 2 =
\Nn{21.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 21 + {1\over 2}\sqrt 2 =
\Nn{21.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">493.<br />
<a href="square-493.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-493s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-493b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 22 + {1\over 2}\sqrt 2 =
\Nn{22.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 22 + {1\over 2}\sqrt 2 =
\Nn{22.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 22 + {1\over 2}\sqrt 2 =
\Nn{22.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">538.<br />
<a href="square-538.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-538s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-538b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 23 + {1\over 2}\sqrt 2 =
\Nn{23.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 23 + {1\over 2}\sqrt 2 =
\Nn{23.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 23 + {1\over 2}\sqrt 2 =
\Nn{23.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">586.<br />
<a href="square-586.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-586s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">585.<br />
<a href="square-586_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 24 + {1\over 2}\sqrt 2 =
\Nn{24.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 24 + {1\over 2}\sqrt 2 =
\Nn{24.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 24 + {1\over 2}\sqrt 2 =
\Nn{24.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">635.<br />
<a href="square-635.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-635s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-635b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 25 + {1\over 2}\sqrt 2 =
\Nn{25.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 25 + {1\over 2}\sqrt 2 =
\Nn{25.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 25 + {1\over 2}\sqrt 2 =
\Nn{25.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">686.<br />
<a href="square-686.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-686s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-686b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 26 + {1\over 2}\sqrt 2 =
\Nn{26.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 26 + {1\over 2}\sqrt 2 =
\Nn{26.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 26 + {1\over 2}\sqrt 2 =
\Nn{26.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">740.<br />
<a href="square-740.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-740s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-740b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 27 + {1\over 2}\sqrt 2 =
\Nn{27.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 27 + {1\over 2}\sqrt 2 =
\Nn{27.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 27 + {1\over 2}\sqrt 2 =
\Nn{27.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">795.<br />
<a href="square-795.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-795s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-795b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 28 + {1\over 2}\sqrt 2 =
\Nn{28.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 28 + {1\over 2}\sqrt 2 =
\Nn{28.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 28 + {1\over 2}\sqrt 2 =
\Nn{28.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">853.<br />
<a href="square-853.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-853s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">852.<br />
<a href="square-853_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 29 + {1\over 2}\sqrt 2 =
\Nn{29.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 29 + {1\over 2}\sqrt 2 =
\Nn{29.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 29 + {1\over 2}\sqrt 2 =
\Nn{29.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">912.<br />
<a href="square-912.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-912s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-912b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 30 + {1\over 2}\sqrt 2 =
\Nn{30.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 30 + {1\over 2}\sqrt 2 =
\Nn{30.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 30 + {1\over 2}\sqrt 2 =
\Nn{30.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">974.<br />
<a href="square-974.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">973.<br />
<a href="square-974_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 31 + {1\over 2}\sqrt 2 =
\Nn{31.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 31 + {1\over 2}\sqrt 2 =
\Nn{31.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">1037.<br />
<a href="square-1037.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1037s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1037b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 32 + {1\over 2}\sqrt 2 =
\Nn{32.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 32 + {1\over 2}\sqrt 2 =
\Nn{32.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 32 + {1\over 2}\sqrt 2 =
\Nn{32.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">1102.<br />
<a href="square-1102.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1102s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1102b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 33 + {1\over 2}\sqrt 2 =
\Nn{33.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 33 + {1\over 2}\sqrt 2 =
\Nn{33.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 33 + {1\over 2}\sqrt 2 =
\Nn{33.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1170.<br />
<a href="square-1170.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1170s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">1169.<br />
<a href="square-1170_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 34 + {1\over 2}\sqrt 2 =
\Nn{34.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 34 + {1\over 2}\sqrt 2 =
\Nn{34.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 34 + {1\over 2}\sqrt 2 =
\Nn{34.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">1239.<br />
<a href="square-1239.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1239s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1239b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 35 + {1\over 2}\sqrt 2 =
\Nn{35.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 35 + {1\over 2}\sqrt 2 =
\Nn{35.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 35 + {1\over 2}\sqrt 2 =
\Nn{35.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">1311.<br />
<a href="square-1311.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">1310.<br />
<a href="square-1311_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 36 + {1\over 2}\sqrt 2 =
\Nn{36.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 36 + {1\over 2}\sqrt 2 =
\Nn{36.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">1384.<br />
<a href="square-1384.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1384s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1384b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 37 + {1\over 2}\sqrt 2 =
\Nn{37.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 37 + {1\over 2}\sqrt 2 =
\Nn{37.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 37 + {1\over 2}\sqrt 2 =
\Nn{37.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">1459.<br />
<a href="square-1459.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1459s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1459b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 38 + {1\over 2}\sqrt 2 =
\Nn{38.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 38 + {1\over 2}\sqrt 2 =
\Nn{38.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 38 + {1\over 2}\sqrt 2 =
\Nn{38.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1537.<br />
<a href="square-1537.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1537s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">1536.<br />
<a href="square-1537_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 39 + {1\over 2}\sqrt 2 =
\Nn{39.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 39 + {1\over 2}\sqrt 2 =
\Nn{39.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 39 + {1\over 2}\sqrt 2 =
\Nn{39.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">1616.<br />
<a href="square-1616.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1616s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1616b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 40 + {1\over 2}\sqrt 2 =
\Nn{40.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 40 + {1\over 2}\sqrt 2 =
\Nn{40.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 40 + {1\over 2}\sqrt 2 =
\Nn{40.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
</tr>
</tbody>
</table>

------------------------------------------------------------------------

<table class="svg-table" style="width:100%;" data-cellspacing="0"
data-border="0">
<colgroup>
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<tbody>
<tr data-align="center">
<td class="box">1698.<br />
<a href="square-1698.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1698s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">1697.<br />
<a href="square-1698_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 41 + {1\over 2}\sqrt 2 =
\Nn{41.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 41 + {1\over 2}\sqrt 2 =
\Nn{41.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 41 + {1\over 2}\sqrt 2 =
\Nn{41.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">1781.<br />
<a href="square-1781.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1781s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1781b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 42 + {1\over 2}\sqrt 2 =
\Nn{42.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 42 + {1\over 2}\sqrt 2 =
\Nn{42.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 42 + {1\over 2}\sqrt 2 =
\Nn{42.70710678118654}$<br />
Rigid alternative with minimal rotated squares, based on the rigid
$s(52)$ found by David W. Cantrell in 2005.</td>
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
<td class="box">1866.<br />
<a href="square-1866.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1866s.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-1866b.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 43 + {1\over 2}\sqrt 2 =
\Nn{43.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 43 + {1\over 2}\sqrt 2 =
\Nn{43.70710678118654}$<br />
simplified</td>
<td></td>
<td class="desc">$s = 43 + {1\over 2}\sqrt 2 =
\Nn{43.70710678118654}$<br />
Alternative with minimal rotated squares<br />
(SVG not made yet)</td>
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
<td class="box">(1867.)<br />
<a href="square-1867.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 2 + {59\over 2}\sqrt 2 =
\Nn{43.71930009000630}$<br />
Extends the $s(18)$ found by<br />
Frits Göbel in early 1979.</td>
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
<td class="box">1954.<br />
<a href="square-1954.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box">1953.<br />
<a href="square-1954_no_min_rot.svg"></a>
<div style="height: 9.667em">
&#10;</div></td>
<td></td>
<td class="box"><br />
</td>
</tr>
<tr data-align="center">
<td class="desc">$s = 44 + {1\over 2}\sqrt 2 =
\Nn{44.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.</td>
<td></td>
<td class="desc">$s = 44 + {1\over 2}\sqrt 2 =
\Nn{44.70710678118654}$<br />
No alternative with minimal<br />
rotated squares exists, as found by<br />
David Ellsworth in December 2024.<br />
(SVG not made yet)</td>
<td></td>
<td></td>
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
<td class="box">2043.<br />
<a href="square-2043_r0.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-2043.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 45 + {1\over 2}\sqrt 2 =
\Nn{45.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s =
{}^{12}🔒 = \Nn{45.69644276992823}$</span> <span
class="frames">$4s^{12}-1608s^{11}+293084s^{10}-31920420s^9+2301941449s^8-114905182392s^7+4022452365218s^6-97595016541596s^5+1574653827588509s^4-15396232508703888s^3+72639007870740216s^2-58090491554723760s+46014771089277232=0$</span>
</span><br />
Found by David Ellsworth<br />
in December 2024.<br />
Beats the Göbel strip.</td>
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
<td class="box">2135.<br />
<a href="square-2135_r0.svg"></a>
<div class="svg-box">
&#10;</div></td>
<td></td>
<td class="box"><br />
<a href="square-2135.svg"></a>
<div class="svg-box">
&#10;</div></td>
</tr>
<tr data-align="center">
<td class="desc">$s = 46 + {1\over 2}\sqrt 2 =
\Nn{46.70710678118654}$<br />
Extends the $s(52)$ found by<br />
Frits Göbel in early 1979.<br />
Not optimal.</td>
<td></td>
<td class="desc"><span class="toggle"> <span class="frame1">$s =
{}^{4}🔒 = \Nn{46.69429881401871}$</span> <span
class="frames">$s^4-123s^3+5644s^2-127660s+1423760=0$</span>
</span><br />
Found by David Ellsworth<br />
in December 2024.<br />
Beats the Göbel strip.</td>
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
