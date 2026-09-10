# Wall Constructor: Mathematical Admission Addendum

**Verdict:** GO for the minimal sixteen-class constructor and subsequent 128
component-containment tests, with the controls below.
Retain nonempty point and segment centre sets.
This review evaluates the design and source APIs, not target classes or areas.
It changes no H143 protocol.

## Signed-Frame Provenance

Use the complete `OwnerDirectionManifest` at the frozen `angle_limit` and
`direction_steps`. Record those two parameters as well as q, B, and the source Git
revision. A count of 361 is necessary but does not establish completeness: validate the
indices, rational first and second axes, and complete folded-source lists against the
declared generated manifest.
Require exact unit first axes and second axis $Ju$. Freeze the exact sixteen class IDs,
marks, sectors, and order against the branch manifest.
A wrong mark or omitted class is an invalid input.

For each canonical orientation $u$, generate the four signed rays $J^k u$, with
$k=0,1,2,3$. The full signed-ray set must equal their union.
Require 1444 distinct geometric rays in this frozen regime.
Deduplication must not conceal duplicate canonical orientations or a missing signed-axis
selector.

**Prefer one canonical orientation index per signed ray.** The existing manifest has
already quotiented square orientations by quarter-turns, so a valid ray belongs to one
such index. Retain that orientation’s entire `sources` tuple, including folded-source
aliases already merged there.
Recording the quarter-turn selector is useful but not essential: the exact ray and
canonical axis determine it uniquely.
The proposed `orientation_indices` field may remain a tuple for API convenience, but it
must be a singleton under this contract.
Do not aggregate several purportedly canonical orientation indices into a ray and
thereby hide an invalid manifest.

Select every ray in the class’s exact closed sector.
The two cross-product tests in the plan are valid because the retained first-to-last arc
is shorter than $\pi$. Check the selected set against the full signed-ray set and the
sector predicate; do not infer completeness from endpoints or counts alone.
Preserve endpoint membership in both adjacent closed classes.
Deduplicate within a class, not across classes.
An empty retained-frame list is an instrument error, not an impossible owner class.

Diagonal reflection requires the ordered-frame map

$$r'=S(Jr),\qquad Jr'=S(r),\qquad S(x,y)=(y,x).$$

Using $r'=S(r)$ with a freshly computed $Jr'$ gives the wrong displacement box.
Under the correct map, the two support intervals exchange roles, with unchanged scalar
values: the old $Jr$ interval becomes the new $r'$ interval and conversely.
Transport $Z_r$ and the world-coordinate polygons by $S$, and resolve their target
orientation index and source list through the exact manifest.
Do not assume that orientation indices or reflected-source flags stay unchanged.
The target class is the other mark with sector $7-j$ modulo eight.

These are local manifest and transport guards.
No new provenance framework, digest manifest, or independent geometric engine is needed.

## Degenerate Legal-Centre Sets

The conservative policy is sound.
Exact point and segment vertex sets suffice to compute all support extrema, and their
rectangles must participate in the final intersection.
Keep the proposed permanent controls through the public wrapper, since the independent
union clipper deliberately discards zero-area intersections.

The optional strict-containment pruning also has a valid justification under the
recorded premises, but is unnecessary for this implementation.
A selected owner core lies strictly inside its physical parent and hence inside the
container, so its centre lies in $\operatorname{int}K_r$. The displacement box $Q_r$ is
full dimensional because $h>0$ and $r,Jr$ are orthonormal.
If a point of $Q_r$ lies in $\operatorname{int}K_r$, nearby interior points of $Q_r$ do
too; consequently $K_r\cap Q_r$ has positive area.
Thus a zero-area intersection cannot contain an actual strict owner centre.
Closed displacement or sector boundaries create no exception.
Keep this as a documented optional lemma rather than changing the admitted boundary
policy now.

Distinguish an empty frame from an invalid frame computation.
A class is impossible only after every required frame has completed and has an empty
centre set under the chosen policy.
A partial frame list cannot establish impossibility.

## Proper Inclusion by Exact Area

Yes: after exact nesting, area strictness is sufficient and necessary here.
Let $P$ be the old positive-area closed convex footprint and $A$ the new closed convex
footprint, with $P\subseteq A$. A point of $A\setminus P$ has a neighbourhood outside
the closed set $P$; that neighbourhood intersects the full-dimensional convex polygon
$A$ in positive area.
Therefore

$$P\subsetneq A\quad\Longleftrightarrow\quad
\operatorname{area}(P)<\operatorname{area}(A).$$

Use exact shoelace areas after convex normalization.
Positive area and successful nesting are prerequisites; equal areas alone do not decide
containment. Once nesting passes, equal areas mean equal sets, so an additional
polygon-equality engine is unnecessary.
A negative gain or failed nesting is an invalid construction, not a negative geometric
result.

The constructor may expose `proper_inclusion` as the exact comparison in its receipt.
Run the sixteen actual comparisons only inside the prospectively frozen geometry
experiment. Synthetic comparisons establish readiness without asserting target gains.

## Required Controls and Small Implementation Corrections

Keep the plan’s permanent point/segment/empty intersection, oblique support, max/min
reversal, unchanged-extrema corner cut, complete-manifest, nesting, and reflection
controls. Normalize the centre-set representation before assigning dimension.
Preserve nonempty degenerate results after every clipping step, not merely at
serialization. For each allowed frame, check that the returned support bounds equal the
literal vertex extrema and that its rectangle contains the mark.
A possible class must retain its old positive-area footprint; this also guarantees a
positive-area final result.

The whole-face synthetic fixture with $h=1$ and $K=[0,2]^2$ is suitable for the generic
clip-and-support helper, but that K is not `closed_centre_set()`'s physical container
rectangle at that h. To test the physical wrapper, translate the fixture by $(1,1)$ and
use q=4: $K=[1,3]^2$, $m=(1/2,1)$, and $Q=[1/2,3/2]\times[1,2]$. Its clipped set is
$[1,3/2]\times[1,2]$ and its common rectangle is $[1/2,2]\times[1,2]$. This is a
synthetic control, not an evaluation of a registered owner class.

For the 128 component tests, exact membership of every certified old-patch vertex in the
relevant convex wall footprint proves containment.
Combine successful relations with their corresponding certified dot pattern.
A failed component relation leaves that tuple unresolved; it does not refute whole-union
containment or dot coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
