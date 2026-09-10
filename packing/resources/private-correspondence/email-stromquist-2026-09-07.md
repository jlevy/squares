[Emails to Joshua Levy from Walter Stromquist, 2026-09-07 and 2026-09-09]

I skimmed your square-packing paper and am impressed by your clarity and detail (and/or
that of your electronic underlings).
I will read it more carefully, but not today; another deadline presses.
Expect a reply before long.

Till then, two things.
You found my website, but probably you didn’t get to the three unpublished notes on
square packing that are posted there.
On my “research and publications” list, under Geometry etc., find the three memos linked
at “-I”, “-II”, and “-III”. There is at least one tiny item in them that might inspire a
tiny revision of your paper.
(Mystery mostly due to haste; more later.)

Also: Back in the day, we called proofs like yours “dots proofs.”
With an intern, sometime in the 1980’s, I tried to find a dots proof for n=6. We found
out that there isn’t a pure dots proof, but there is a proof of n=6 that starts with a
preliminary argument and finishes with dots.
That is what I did with n=11, too.
If I skimmed correctly, your lower-bound proofs are all pure dots proofs (and
symmetrical at that).
I wonder whether the helper arguments can be made systematic; if so, much better lower
bounds should be possible.

* * *

Taking a harder look at the case of n=26, I now understand that 5.62132 < 5.650629. So
my contribution has vanished into history.
Also, my contribution for n=18 wasn’t new, even in 1984.

Your agents were skeptical about my bound for n=11, and rightly so.
In the 2003 paper, figure 14, the quadrilateral southwest of point G is not covered by
Lemma 4, and in fact, a square with a center there could avoid the given points.
The proof can be fixed by moving G to where it ought to have been in the first
place---evenly spaced vertically between the corner points above it (point F) and below
it (leftmost A). Instead of G=(0.8, 1.85) it should be at G=(0.8, s/2-.05). Or, G=(0.8,
1.845) would do. Then the case of a=0.945, b=0.8 should appear in the table following
lemma 4. I suspect the “1.85” was a late, misguided edit aimed at concreteness.
Darn.

Have your agents considered “fractional packings”?
Instead of fitting n squares into a container, try fitting a larger collection of
squares with weights.
We count squares by the sum of their weights, and follow the rule that, for each point P
in the container, the sum of the weights of the squares whose interiors contain P can’t
exceed 1. Any “dots proof” (or certificate like yours) would ban fractional packings
with total weight n as well as real packings of n squares.

The smallest container for fractional packings with total weight 11 might be smaller
than the smallest container for actual 11-packings.
In that case, your method can’t push the lower bound past that limit.

So helper arguments aren’t just a convenience; they may be essential.

It might even be the case that there is a fractional packing with n = 6 in a container
smaller than 3x3. Maybe we found one in that project with the intern, but I don’t
remember.
Maybe we just found a fractional packing that spoiled a lemma we wanted to rely
on. My notes from that project might still exist, and I might be able to find them, but
not quickly.

At any rate, there is a duality theorem here somewhere.
The upper bound for fractional packings is surely equal to the lower bound for (this
kind of) certificates.
I don’t think I have ever written a proof, but it has to follow from linear programming
duality.

The continuous version would be this.
A continuous-fractional packing would be a density function on the space of squares (or
legal shapes in a larger context) such that certain integrals are >=1 and the overall
integral determines its “size”.
The continuous version of the dots proof would be a measure on that same space such that
every square (or legal shape) has measure >=1. Then the largest continuous-fractional
packing for any container should match the smallest measure.
Again, I haven’t tried to write a proof but it it should follow from the discrete
version and some compactness lemmas.
