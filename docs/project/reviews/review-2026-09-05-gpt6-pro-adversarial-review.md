# Adversarial review of the \(s(11)\ge 3.81\) claim

**Verdict: the claimed bound survives this review.
I found no fatal flaw in the detailed mathematical argument or in either published
certificate.** I did find several definite mathematical misstatements in the explainer,
limitations in the generic verifier, and overstated descriptions of independence and
validation. Those should be corrected, but they do not overturn the actual \(3.81\)
result.

## 1. What I checked—and what I actually reproduced

I examined the rendered explainer, both linked verifiable-claim documents, the embedded
standard-library verifier, the separate minimal verifier, the repository’s exact sweep
and interval verification implementations, the retention gate, the generator, and the
package intended for third-party checking.
The explainer examined identifies itself as the September 5, 2026 draft, version
`v0.1.0-3bd273e6`. ([Jlevy][1])

There are two important execution qualifications.
The supplied Markdown endpoint would not parse in the browsing tool, so I reviewed its
rendered counterpart and the linked raw proof/code documents.
Also, direct repository downloads into the execution container were unavailable.
I therefore reconstructed the certificates from their published symmetry representatives
and obtained **exact matches to both published SHA-256 digests**. I ran a **semantic
transcription of the published exact sweep**, not a byte-identical downloaded copy of
the original program.

The certificate bytes were thus authenticated against the published hashes; the executed
verifier source was not independently hash-authenticated.
I did **not** rerun the repository’s interval branch-and-bound implementation.
The bundle makes these distinctions explicit.

### Exact computational results

These are my recomputed results, not copied verification logs.

| Check | Stronger certificate | Earlier certificate |
| --- | ---: | ---: |
| Container side | \(381/100=3.81\) | \(19/5=3.8\) |
| Atoms | 1,121 | 425 |
| Directions checked | 181 | 181 |
| Total mass | \(434547/40000=10.863675\) | \(43391/4000=10.84775\) |
| Minimum covered mass | \(4001/4000=1.00025\) | \(50003/50000=1.00006\) |
| One minimizing direction | \(0\) | \(0\) |
| Corresponding center | \((27/50,27/50)\) | \((53/100,53/100)\) |
| Admissible event cells scored | **567,130,649** | **90,546,593** |
| Five mathematical conditions | **All pass** | **All pass** |

The stronger certificate’s minimum and minimizing center match the detailed claim
document. The earlier certificate’s digest matches the identity recorded in the checking
package.

For both certificates, I obtained

$$
B=\frac{9977}{10000},\qquad
D=\frac{207107}{90000000},
$$

and the exact containment check

$$
B(1+D)
=\frac{899996306539}{900000000000}<1.
$$

The net-endpoint check is also strictly positive:

$$
t_{180}^{2}+2t_{180}-1
=\frac{309449}{250000000000}>0.
$$

I checked nonnegative weights, weighted \(D_4\) symmetry, and that all atoms lie inside
the container.

I also wrote a separate **exact rational polygon-clipping and direct-summation oracle**.
It agreed with the reviewed sweep on 96 deterministic small cases, including duplicate
atoms, zero weights, empty support, event coincidences, atoms outside the container, and
multiple quadrants. This is meaningful differential testing, not a formal proof of
correctness for every possible input.

* * *

## 2. Findings

### Finding 1: The claimed danger from using a non-strict containment inequality is mathematically false

**Classification: definite error in the explanation; not a defect in the sufficient
condition actually used.**

After its contradiction, the explainer says that replacing \(<\) with \(\le\) in
Condition 4 could allow the shrunken squares to share an atom on a common boundary.
That assertion is false for the stated nontrivial increasing net.
([Jlevy][1])

Suppose

$$
B(1+D)\le1.
$$

The net has a positive gap, so \(D>0\). For a nearest-net angular mismatch \(d\), the
proof establishes \(\tan d\le D\).

If \(d=0\), then

$$
B\le\frac1{1+D}<1.
$$

If \(d>0\), then \(d<\pi/2\) and \(\cos d<1\), giving

$$
\begin{aligned}
B(\cos d+\sin d)
&=B\cos d(1+\tan d)\\
&<B(1+\tan d)\\
&\le B(1+D)\\
&\le1.
\end{aligned}
$$

**The required geometric containment remains strict in both cases.**

Thus the current strict rational condition is safe but unnecessarily restrictive.
The explanation mistakes a convenient stronger-than-necessary condition for a necessary
safeguard.

The bundle includes a small example with \(B(1+D)=1\) that passes coverage but is
rejected by the existing checker at Condition 4. This is a conservative rejection, not
an unsound acceptance.

**Recommended correction:** remove the warning about equality causing shared-boundary
double counting. Retaining the strict test is harmless, provided it is described as a
sufficient condition.

### Finding 2: The condensed explainer omits two essential qualifications

**Classification: substantive exposition gaps, repaired by the detailed proof.**

**First, disjoint interiors are not disjoint closed squares.** The introductory counting
passage says the unit squares are disjoint and therefore no atom is counted twice.
But the packing definition permits shared boundaries.
For example,

$$
[0,1]\times[0,1]
\quad\text{and}\quad
[1,2]\times[0,1]
$$

have disjoint interiors, while both contain the atom \((1,1/2)\). Atomic measures can
assign positive mass to a shared boundary; an area-zero argument does not help.
([Jlevy][1])

**Second, the final contradiction omits reflection and pullback.** It says an original
unit square at any orientation contains a concentric \(B\)-square at one of the original
181 net angles. Literally, this is false: the net runs approximately from \(0^\circ\) to
\(45^\circ\). A unit square at \(60^\circ\) is roughly \(15^\circ\) from its nearest
original net angle, far too much mismatch for \(B=0.9977\). ([Jlevy][1])

The correct construction is to reflect the \(60^\circ\) square to \(30^\circ\),
construct an inner net-oriented square there, and reflect that inner square back.
Its final orientation belongs to the **reflected net**, not necessarily the original
net.

Importantly, **the detailed proof explicitly does this correctly**. It pulls each inner
square back into its own original square’s interior before counting.
It does not assume that independently reflecting different original squares preserves
their disjointness.

**Recommended correction:** introduce interior containment before the first counting
argument, and preserve the reflection-and-pullback sentence in the condensed
contradiction.

### Finding 3: The generic verifier does not decide every input allowed by its stated theorem

**Classification: demonstrated checker-domain mismatch; no effect on the two supplied
certificates.**

The embedded verifier’s `least_mass` routine raises an exception when

$$
B(|c|+|s|)\ge L.
$$

But this combines two distinct cases:

* When \(B(|c|+|s|)>L\), no square at that direction fits.
  Condition 5 is **vacuously true** for that direction.
* When equality holds, exactly one center is feasible.
  Its covered mass can be checked directly.

Neither is inherently invalid theorem data.
The theorem itself does not require every direction’s feasible center domain to have
nonempty interior.

Here is a concrete valid theorem input:

$$
n=2,\qquad L=B=\frac12,\qquad
(t_0,t_1)=\left(0,\frac12\right),
$$

with one atom of weight \(1\) at \((1/4,1/4)\).

It is symmetric, its total mass is below \(2\), the net reaches \(\pi/4\), and

$$
B(1+D)=\frac34<1.
$$

At direction zero, the unique \(B\)-square covers the atom.
At the other direction, \(c=3/5\) and \(s=4/5\), so the square’s axis-aligned width is
\(7/10>L\): there are no placements to check.

All theorem hypotheses hold, but the embedded verifier raises an exception at direction
zero. **I reproduced this behavior.**

The corresponding sweep explanation also assumes a feasible domain with interior without
making that an explicit restriction on the stated theorem.
The separate checking package documents handling for empty and singleton domains, so the
public verification paths are inconsistent in this respect.

**Recommended correction:** explicitly handle these cases, or restrict the advertised
checker domain and distinguish “unsupported input” from “failed hypothesis.”

### Finding 4: The generic verifier validates mathematical parameters, not every declaration in the file

**Classification: artifact-integrity limitation; not an example of proving a false
theorem.**

The embedded checker reads the mathematical parameters and atoms but ignores descriptive
fields including `claim`, `total_mass`, and `least_cell_mass`. It also does not pin the
input to the published certificate hash.

I tested a small valid certificate and then replaced its metadata with:

```text
claim: s(11) >= 100
total_mass: -100
least_cell_mass: 500
```

The generic checker still succeeded.

The qualification is crucial: **it printed the computed conclusion `s(2) >= 3/4`, not
the fabricated claim.** So this is not a false mathematical acceptance.
It shows that success cannot be interpreted as validation of every assertion written in
the input file.

This matters for automated consumers that associate a successful exit status with the
file’s metadata rather than the checker’s computed conclusion.

The separate minimal verifier and full retention gate already provide stronger
protections. They compare declarations with recomputed values; the retention gate also
checks that the accepted file has not changed and reports its digest.
Those safeguards deserve credit.

**Recommended correction:** align integrity checks across public entry points, or
prominently distinguish parameter verification from complete artifact/claim
verification.

### Finding 5: The promise that lightening one atom causes refusal is false

**Classification: definite overstatement in the validation instructions.**

The claim documents broadly promise that lightening an atom will make the verifier
refuse the certificate.
The actual stronger certificate provides a counterexample.

Its central atom, at

$$
\left(\frac{381}{200},\frac{381}{200}\right),
$$

has weight \(27899/200000\). Decrease that weight by \(1/200000\).

The center is a one-point \(D_4\) orbit, so symmetry remains intact.
Total mass decreases, improving Condition 2. The geometry and net do not change.
Every placement loses at most \(1/200000\), so its mass remains at least

$$
\frac{4001}{4000}-\frac1{200000}
=\frac{200049}{200000}
=1.000245>1.
$$

**The modified weights still satisfy all five mathematical conditions.**

This conclusion follows directly from the completed baseline sweep and a uniform
perturbation bound; it does not require a second full sweep.
A hash-pinned checker would reject changed bytes unless its pin were updated or
disabled, but that is a separate identity check.

The package’s carefully specified destructive perturbations can still be useful tests.
They do not establish that every decrease of one atom must fail.

**Recommended correction:** state exact perturbations and magnitudes, identify which
condition each is intended to violate, and include benign perturbations expected to
remain valid.

### Finding 6: The linear-programming discussion conflates feasibility, optimization scope, and numerical expectations

**Classification: conceptual overstatements; none is necessary for the packing
contradiction.**

There are three distinct problems.

**The finite LP depends on more than \(L\) and \(B\).** It depends on the candidate atom
sites and the direction net.
The generator explicitly takes both.
A more accurate notation would be

$$
\tau^*(A,\Theta;L,B),
$$

where \(A\) is the site set and \(\Theta\) the net.
Optimizing over arbitrary atom positions is a different problem from optimizing weights
on fixed sites.

The assertion that a certificate exists exactly when \(\tau^*<n\) also needs the other
admissibility conditions retained.
The mass LP alone does not enforce the net and containment hypotheses.
For example, take \(L=B=2\), the net \(t=\{0,1/2\}\), and one unit-weight atom at the
center. The axis-aligned square covers it, and the other direction has no fitting
placement. The covering LP has optimum \(1<2\), but this does not prove that two unit
squares fail to fit in a side-2 container: Condition 4 fails.

**A round-number optimum is not evidence of a bug.** Integer or simple rational optima
can arise from the incidence constraints themselves, regardless of whether \(n\) appears
in the objective. Even

$$
\min w\quad\text{subject to }w\ge1
$$

has the perfectly valid integer optimum \(1\). The explainer’s categorical assertion to
the contrary is unjustified.
([Jlevy][1])

**Exact certificate validation proves feasibility, not LP optimality.** The stronger
submitted vector has minimum mass \(4001/4000\). Multiplying all its weights by
\(4000/4001\) preserves coverage and reduces total mass to

$$
\frac{434547}{40010}.
$$

Thus the submitted vector is not itself an exact minimizer of the unnormalized covering
LP. This is compatible with obtaining it by rounding and inflating a numerical
optimum—the generator explicitly performs such inflation—but an exact optimization claim
does not follow from the packing verifier.

**Recommended correction:** specify the optimization domain, describe the output as a
verified feasible rational certificate, and reserve exact optimality claims for a
separate optimality certificate.

### Finding 7: The independence and third-party-validation descriptions are overstated

**Classification: verification-provenance problem, not a mathematical counterexample.**

The explainer calls the linked package a third-party check.
Its own README explicitly states that the project authored it and that it is **not
itself third-party validation**. It also deliberately checks the earlier \(3.8\)
certificate rather than the headline \(3.81\) certificate.
([Jlevy][1])

The detailed claim also says the two other verification routes share no code with one
another. At whole-program level that is inaccurate.
The interval module imports the `Certificate` representation from `certificate.py`, and
the retention gate constructs and supplies the shared representation.
The gate’s documentation acknowledges shared infrastructure.

The coverage algorithms are genuinely different—exact event cells versus interval
branch-and-bound—and that diversity is valuable.
But these are distinct properties:

**Different algorithms are not the same as independent implementations, independent
input handling, or validation by a separate party.**

**Recommended correction:** use “first-party package for third-party checking,” and
describe precisely which components the verification routes share.

### Finding 8: Mutable code links weaken reproducibility

**Classification: reproducibility limitation; certificate identity itself is well
supported.**

The publication displays a draft version, but many proof and verifier links target the
mutable `main` branch.
The certificate hashes identify the data very well; they do not identify the executable
verifier, dependency environment, or complete exposition used for a reported run.
([Jlevy][1])

The retention gate’s unchanged-file checks and digest reporting are good protections
against artifact substitution.
They are not a replacement for an immutable release of the whole proof package.

**Recommended correction:** provide commit-specific permalinks or a release archive
containing the theorem, certificates, verifier sources, relevant lockfile, and complete
verification outputs.
External replays should identify both the certificate bytes and the executed source.

### Finding 9: Smaller software-contract and diagnostic issues

**Classification: low-severity issues outside the validity of the retained
certificate.**

The `generate` function’s docstring says it searches and then decides a certificate
exactly, but its implementation constructs and returns the candidate without invoking
`verify`. Returning an unverified candidate is reasonable; the contract should say so
explicitly.

The generic standard-library verifier allocates a quadratic event grid and continues
into the expensive sweep even after earlier conditions fail.
It lacks several resource and schema limits present in the full retention loader.
This can matter for malformed or oversized inputs, but it is not evidence of a wrong
result for the fixed, hashed certificates here.

Finally, the minimal verifier’s direct mass cross-check uses a cell midpoint without
separately proving that the midpoint is a feasible center.
A cell can intersect the feasible domain while its midpoint lies outside it.
The cross-check still verifies the cell’s constant mass, and the preceding intersection
test supports the decision, so **I do not classify this as an acceptance bug**. It is a
weaker witness check than constructing an actual point in the feasible intersection.

* * *

## 3. Why these findings do not invalidate the actual proof

The detailed argument survives the principal adversarial objections.

The original squares may touch, but each constructed inner square lies strictly inside
its own original square’s interior.
Reflection is undone before disjointness is used.
At fixed orientation, the exact sweep considers the continuum of centers through event
cells rather than merely sampling center points.
Closed coverage rectangles and nonnegative weights handle event boundaries safely, and
the feasible domains have nonempty interior for the actual certificates.

The resulting contradiction is therefore legitimate:

$$
11
\le \sum_{j=1}^{11}\operatorname{mass}(P_j)
\le \sum_i w_i
=\frac{434547}{40000}
<11.
$$

The floating-point search does not itself undermine this: only the resulting rational
certificate is needed.
In the interval source, unresolved searches and restricted-direction checks also do not
become full acceptance; the current implementation explicitly guards against that.

## 4. A small additional consequence: the certificate supports a slightly stronger bound

This is not a shortcoming, but it exposes some unused certified margin.

Set

$$
a=\frac{250001}{250000}=1.000004.
$$

Dilate every atom position, \(L\), and \(B\) by \(a\), leaving weights and the net
unchanged. Inverse dilation gives a bijection between new and old square placements, so
the coverage condition is unchanged.
Symmetry and total mass are unchanged as well.

The new containment product remains strictly below one:

$$
aB(1+D)
=\frac{224999976631056539}{225000000000000000}<1.
$$

Consequently, the same verified data and theorem imply

$$
\boxed{s(11)\ge\frac{95250381}{25000000}=3.81001524.}
$$

This is an algebraic corollary, not a separately replayed third certificate.
It does **not** justify simply dividing \(L\) by \(B\); any dilation must preserve the
angular containment inequality.

## 5. Overall assessment

**The mathematical claim is substantially stronger than the quality of some of its
explanatory prose.** The complete exact replay passed, the certificate hashes matched,
the independent small-instance oracle agreed, and I found no counterexample to the
detailed implication from the five conditions to the packing obstruction.

Before presenting the explainer as a polished proof reference, I would correct the false
equality warning, restore the boundary and reflection qualifications, reconcile the
checker’s advertised domain with its implementation, remove the blanket perturbation and
round-number-LP claims, and clarify the independence language.

The historical claim is a separate matter.
The original journal abstract confirms Stromquist’s 2003 lower bound, but my focused
search is not a complete priority review.
Nor does this certificate establish the optimal packing side or the optimality of the
best known construction.
([The Electronic Journal of Combinatorics][2])

**Bottom line:** no fatal flaw found; both published certificates passed the reproduced
exact checks.
The report identifies real corrections and verification limitations, but it
does not provide grounds to reject the \(3.81\) lower bound.

[1]: https://jlevy.github.io/squares/ "s(11) ≥ 381/100: A New Lower Bound on the Square Packing Problem"
[2]: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8 "Packing 10 or 11 Unit Squares in a Square | The Electronic Journal of Combinatorics"

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
