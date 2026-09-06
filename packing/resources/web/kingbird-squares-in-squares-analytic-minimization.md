# Archived: Kingbird analytic minimization notes

**Source:**
https://kingbird.myphotos.cc/packing/squares_in_squares__analytic_minimization.html  
**Archived:** 2026-09-05  
**Method:** `curl` plus Pandoc; the original HTML is preserved alongside this file.  
**SHA-256 of HTML:**
`a49f70689b904dd466eb04ca7b764320935d58c15610a8b0f5e2fd2c91ca0310`

These are first-party method notes for the catalogue’s symbolic minimization workflow.
They motivate stationary equations but do not supply a completeness theorem, constraint
qualification, or global optimality proof for a packing.

* * *

Squares in Squares  
Analytic Minimization of Underdetermined Nonlinear Systems  
by <a href="https://github.com/Davidebyzero"
style="text-decoration:none">David Ellsworth</a>

To optimize a packing with true exactitude, an analytic (or
symbolic/algebraic) solution is necessary. This is where the number of
independent variables is matched by the number of constraints, enabling
the multivariate Newton-Raphson method to be used (which in Mathematica
is done with `FindRoot[]`), or in the case of packings below a certain
level of complexity, a symbolic/algebraic solution (`Solve[]`).

The side lenth of the enclosing square, \$s\$, is the first independent
variable – the one that we want to minimize. The others are in most
cases the distinct non-orthogonal angles (or slopes) of the squares in
the packing, which in my notation are \$a\$, \$b\$, \$c\$, etc. For
example in [\$s(17)\$](square-17.svg) there are two angles, for a total
of three independent variables \$\\s, a, b\\\$.

The constraints are equations, which declare certain squares to be
touching certain other squares (corner to edge or corner to corner) or
the corner of a square to be touching an edge of the enclosing square.
In my notation they are `f1`, `f2`, `f3`, etc., which are functions of
subsets of the independent variables, each to be set equal to zero, e.g.
`f1==0`.

A problem arises when there are fewer constraints than independent
variables, making the system of equations underdetermined. What we'd
like to do is make it a square system of equations (same number of
constraints as variables) by using the minimization of \$s\$ as a
constraint. In the two-variable case \$\\s, a\\\$ with only one
constraint equation `f1==0`, it's easy to create the extra constraint
equation:

        D[f1,a] == 0

But it's not obvious why that works – it's not as simple and direct as
just setting the derivative of \$s\$ (with respect to some other
variable) equal to zero. So instead, when solving
[\$s(39)\$](square-39_r3.svg), [\$s(87)\$](square-87_r2.svg), and
[\$s(41)\$](square-41_r2.svg) back in June 2023, I came up with a method
using a using a
[discriminant](https://en.wikipedia.org/wiki/Discriminant) that, in
hindsight, was actually a more complicated roundabout way of doing the
same thing as above.

When there were three or more variables, I did not know any general way
to get a solution other than to use `FindMinimum[]` or similar. That
resulted in a solution that's not only slower, but much worse or even
incapable of computing to very high precision (thousands of digits).
Getting a closed-form or polynomial root solution requires either using
`Solve[]` (solving symbolically) which has the same requirements as an
analytic solution, or calculating the variables to high enough precision
that `RootApproximant[]` can be used to find the exact polynomial root
solution, which `FindMinimum[]` fails to do on complicated packings.

I did find that in the case of [the *s*(29) found by Thierry Gensane and
Philippe Ryckelynck](square-29_r3.svg), which has six variables and five
natural constraints, there is a certain derivative that just so happens
to work as sixth constraint when set equal to zero. But there's no
apparent reason why it should work with this particular derivative, and
there was no such derivative for other packings, even similar ones such
as [\$s(55)\$](square-55.svg) with its eight variables and seven natural
constraints.

## Three variables and two constraints

On December 2, 2024 I stumbled upon a way to handle the case of three
variables and two constraint functions. Let the variables be \$\\s, a,
b\\\$ and the first two constraint functions be `f1` and `f2`. (The
variables \$\\a,b\\\$ can be either angles or slopes; it works either
way).

At first I was using `s1` and `s2`, which are two functions of `a` and
`b` that are the result of `Solve[]`ing `f1==0` and `f2==0` for `s`,
respectively. Wherever `s1 == s2`, there is a valid solution (trio of
variables `a`, `b`, and `s = s1 = s2` that meets the constraints).

I had my third constraint as:

        D[s1,a] / D[s1,b] == D[s2,a] / D[s2,b]

which successfully found me the minimum. I did not at first understand
why it worked.

I was kind of stuck on the ratios being equal; it didn't make sense to
me that this would signal a minimum/maximum. Then I realized that the
ratios are an incomplete representation – they're just slopes. To
complete the representation we can make each a vector, with direction
and magnitude (or slope and signed magnitude). And at a local minimum
(or maximum) `s`, these two vectors *point in exactly opposite
directions*. The magnitudes don't have to be equal, just the vectors'
slopes, i.e. our two ratios of derivatives. (Right now the signed
magnitudes are kind of hidden and we only have the slopes, but the sign
of `D[s1,a]` will be opposite that of `D[s2,a]` and the sign of
`D[s1,b]` will be opposite that of `D[s2,b]`. Those opposite signs
cancel out in the ratios, making the ratios equal even in sign.)

These two gradient vectors indicate the two directions of movement
within the \$(a,b)\$ plane of greatest increase in \$s\$, according to
the two different constraint functions. (One can visualize up/down as
the \$s\$ axis, perpendicular to the \$(a,b)\$ plane.) The two
constraint functions each form a curved 2D surface in 3D, the two of
which intersect along a 1D curve, along which are the only valid
solutions to the constraints. On any point along this curve other than
the endpoint, the two vectors of greatest \$s\$ increase are not exactly
opposite each other, so some motion sideways to the vectors can still
decrease \$s\$ while remaining on the 1D curve of validity. But once the
two vectors point in exactly opposite directions, the only directions of
movement that don't increase \$s\$ are perpendicular to the two vectors,
and that just leaves \$s\$ constant (not to mention also departing from
the curve of validity). So that is a local minimum (or maximum) for
\$s\$, and an endpoint of the 1D curve.

Let's switch to the better formulation now (in which we can get
magnitude if we want – not that we need it yet). We don't need `s1` and
`s2`; we don't need to `Solve[]` anything. Instead, we can take the
ratios of other partial derivatives to get the partial derivatives we
need:

Instead of `D[s1,a]`, we use `D[f1,a] / D[f1,s]`. If you express this
mathematically as (∂f1/∂a) / (∂f1/∂s), the two `∂f1` cancel out leaving
`∂s/∂a`. (There's no mention of `f1` anymore in that, but it's still
representing "`f1`'s version of the situation".) We do the same for `b`,
getting `D[f1,b] / D[f1,s]`.

Then to get the equivalent of `D[s1,a] / D[s1,b]`, we take:

        (D[f1,a] / D[f1,s]) / (D[f1,b] / D[f1,s])

Note that we get another cancellation, of `D[f1,s]`, leaving us with
`D[f1,a] / D[f1,b]`. Which is equivalent to our original
`D[s1,a] / D[s1,b]`. So then our third constraint will be:

        D[f1,a] / D[f1,b] == D[f2,a] / D[f2,b]

To get full vectors with magnitude and direction, we could take
`{D[f1,a] / D[f1,s], D[f1,b] / D[f1,s]}`, or put more simply,
`{D[f1,a], D[f1,b]} / D[f1,s]`, and do the same for `f2` to get the
other vector. Printing them in `ToPolarCoordinates[]` form would then
show, that at the point of minimum `s`, the two vectors point in exactly
opposite directions, i.e. angles differing by exactly Pi=180° (but with
magnitudes that are probably different). But this only has illustrative
purpose at this point, and is extraneous from the actual `FindRoot[]`.

## A generalization

So then I was puzzling out how this might be extended to more variables,
and played around with matrices for a while before figuring it out.

When you construct a Jacobian square matrix of the gradients, it
contains the partial derivative, with respect to each variable, of `s`
and each constraint function; the columns are your variables, and the
rows are your constraints, except with the first row being `s`. Since
`s` is both the first row and the first column, this signals that it's
what we want to minimize (or maximize). The first row of the matrix will
be `{1, 0, 0,..., 0}`, since the derivative of `s` with respect to all
of the other independent variables is zero. It's just a simple
derivative, not the extrapolated effect of the FindRoot's search, so
`D[s,a]` for example is just going to be 0.

So, say we have four variables `s`, `a`, `b`, `c` and three constraint
functions `f1`, `f2`, `f3`. In Mathematica taking the Jacobian gradient
matrix is as simple as just:

        grad = Grad[{s, f1, f2, f3}, {s, a, b, c}]

which, expanded out, would be:

        {Grad[s , {s, a, b, c}],
         Grad[f1, {s, a, b, c}],
         Grad[f2, {s, a, b, c}],
         Grad[f3, {s, a, b, c}]}

or expanded even further:

        {{D[s ,s], D[s ,a], D[s ,b], D[s ,c]},
         {D[f1,s], D[f1,a], D[f1,b], D[f1,c]},
         {D[f2,s], D[f2,a], D[f2,b], D[f2,c]},
         {D[f3,s], D[f3,a], D[f3,b], D[f3,c]}}

And the first row is going to be {1, 0, 0, 0}, since none of those are
functions; they're just variables, that, at this snapshot, can be
considered constant.

Taken as a whole, the matrix indicates an instantaneous (tangent) linear
approximation of what effect adding 1 to any variable will have on `s`
and the constraint functions. If you multiply this matrix (with dot
product) by a one-column matrix of deltas for your variables:

        grad . {{∆s}, {∆a}, {∆b}, {∆c}}

you get a one-column matrix indicating the linear approximation of what
the resulting deltas will be for `s` and each of your constraint
functions:

        {{∆s*D[s ,s] + ∆a*D[s ,a] + ∆b*D[s ,b] + ∆c*D[s ,c]},
         {∆s*D[f1,s] + ∆a*D[f1,a] + ∆b*D[f1,b] + ∆c*D[f1,c]},
         {∆s*D[f2,s] + ∆a*D[f2,a] + ∆b*D[f2,b] + ∆c*D[f2,c]},
         {∆s*D[f3,s] + ∆a*D[f3,a] + ∆b*D[f3,b] + ∆c*D[f3,c]}}

But what we want is to go in the opposite direction. We want to know
what set of deltas for the variables will result in changing `s` while
keeping the constraint functions' values constant (at zero). We want
whatever value for "deltas" for which

        grad . deltas

would give us this one-column matrix:

        {{1},
         {0},
         {0},
         {0}}

To do that we invert the matrix, and multiply this by whatever amount we
want to change `s` by. Multiplying our variables by that matrix will
then modify `s` by the amount we want while keeping the constraint
functions constant (to a linear approximation, at least).

Except that's not really what we want to do. We just want to know if
inverting the matrix is possible. If it's not possible to invert the
matrix, that means not all changes in `s` (while keeping the constraints
at zero) are attainable. And that's exactly what we want; we want it to
be impossible to decrease `s`. We want the matrix to go down by at least
one rank, so that its span no longer covers the entire space.

When a matrix isn't invertible, it's a singular matrix. This is the case
if and only if the determinant of the matrix is zero. So, as our last
constraint function, we set that determinant equal to zero:

        Det[grad] == 0

And voila! We have a constraint that takes us to a local minimum (or
maximum) of `s`.

And funnily enough, a Jacobian gradient matrix is precisly how Newton's
method is implemented in the multi-variable case, and how `FindRoot[]`
works. In that case, it actually does invert the matrix and multiply by
it and subtract that, which if the functions were linear, would take it
directly to "all constraints equal zero" in one step.

So this "`FindRoot` breakthrough" actually results in "nesting" a
Jacobian determinant inside a Jacobian, if you take into account how
`FindRoot` works internally.

And before this, I didn't even know what a Jacobian was. Sometimes
`FindRoot[]` would complain about a Singular Jacobian. Now I know what
that means; it means it's reached a point where it can't invert the
matrix anymore, so it doesn't know where to go next.

(I had worked with matrix inversion practically, though, in a couple of
projects: 1) the project where I reverse-engineered the ECC error
correction codes of a couple of hard drives – though that's on Galois
fields rather than real numbers; 2) playing with using Fourier
transform + matrix inversion for deconvolution of bitmap images – needed
high precision 16-bit per RGB channel, otherwise it added lots of
noise.)

## Two variables and one constraint

This case collapses into the a derivative, explaining why that method
works for e.g. the old [\$s(39)\$](square-39_r3.svg),
[\$s(87)\$](square-87_r2.svg), and [\$s(41)\$](square-41_r2.svg):

        Det[Grad[{s,f1}, {s,a}]] == Det[{D[s,s], D[s,a]}, {D[f1,s], D[f1,a]}]
                                 == Det[{  1   ,   0   }, {D[f1,s], D[f1,a]}]
                                 == 0*D[f1,s] + 1*D[f1,a]
                                 == D[f1,a]

## The full generalization

I had wondered, back in December 2024, what to do if the number of
independent variables minus the number of constraints was greater than
one. The answer I settled on was to conjecture that "nesting" additional
Jacobians could result in a solution for such a case, but I had no
packings to test it on.

Optimizing Thomas Schadt's improvement of \$s(39)\$ [provided such a
testing ground](square-39_r5.svg), in which there are three variables
and only one constraint. It turns out that solving this really is as
simple as I thought:

        f2 = Det[Grad[{s,f1   }, {s,a  }]];
        f3 = Det[Grad[{s,f1,f2}, {s,a,b}]];

This provides the needed extra two constraint functions.

## Packings that use this technique

Three or more variables with two less constraints:

- [\$s(39)\_\text{r5}\$](square-39_r5.svg) and
  [\$s(126)\$](square-126.svg)

Three or more variables with one less constraint:

- [\$s(29)\_\text{r3}\$](square-29_r3.svg),
  [\$s(55)\_\text{r4}\$](square-55_r4.svg),
  [\$s(55)\_\text{r5}\$](square-55_r5.svg), and
  [\$s(55)\_\text{r7}\$](square-55_r7.svg)
- [\$s(55)\$](square-55.svg)
- [\$s(39)\$](square-39.svg)
- [\$s(71)\_\text{r8}\$](square-71_r8.svg)
- [\$s(108)\$](square-108.svg)
- [\$s(51)\$](square-51.svg)
- [\$s(53)\_\text{r3}\$](square-53_r3.svg) and others like it:
  [\$s(177)\$](square-177.svg), [\$s(266)\$](square-266.svg),
  [\$s(106)\$](square-106.svg)
- [\$s(87)\$](square-87.svg)
- [\$s(37)\_\text{r2}\$](square-37_r2.svg)
- [\$s(37)\_\text{r3}\$](square-37_r3.svg) (non-record-setting)
- [\$s(1453)\$](square-1453.svg), and others like it but
  non-record-setting: [\$s(260)\_\text{r1}\$](square-260_r1.svg),
  [\$s(446)\_\text{r1}\$](square-446_r1.svg),
  [\$s(791)\_\text{r1}\$](square-791_r1.svg), and
  [\$s(1097)\_\text{r1}\$](square-1097_r1.svg)

Trivial cases with two variables and one constraint:

- [\$s(39)\_\text{r3}\$](square-39_r3.svg),
  [\$s(87)\_\text{r2}\$](square-87_r2.svg),
  [\$s(41)\_\text{r2}\$](square-41_r2.svg),
  [\$s(175)\_\text{r2}\$](square-175_r2.svg) and
  [\$s(175)\_\text{r3}\$](square-175_r3.svg)
- [\$s(126)\_\text{r2}\$](square-126_r2.svg),
  [\$s(126)\_\text{r3}\$](square-126_r3.svg)
- [\$s(69)\$](square-69.svg), [\$s(205)\$](square-205.svg),
  [\$s(234)\$](square-234.svg), [\$s(128)\$](square-128.svg),
  [\$s(152)\$](square-152.svg), [\$s(235)\$](square-235.svg),
  [\$s(300)\$](square-300.svg)
- [\$s(147)\_\text{r2}\$](square-147_r2.svg) and
  [\$s(264)\_\text{r2}\$](square-264_r2.svg) (non-record-setting)
- [\$s(53)\$](square-53.svg) to minimize an angle (for non-essential
  aesthetic purposes)
