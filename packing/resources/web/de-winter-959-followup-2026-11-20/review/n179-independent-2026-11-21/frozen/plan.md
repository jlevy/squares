# N179 Independent Review Plan

**Frozen before verification outcomes, 2026-11-21.** Reviewer: `/root/intake_n179_blind`
(tbd strong-max). Owner of task bead `think-esp4`: coordinator.
Workflow: `tbd shortcut new-research-brief`, narrowed by the delegated brief to an
independent Stage 4 mathematical review and external evidence only.

## Inputs and Independence

The sole mathematical data input is `n179.minpoly.json.gz` at the supplied original
source path, SHA-256 `28edf9561e87037b5c681e4ff0051a1bd1b8e5401c1a8376fe2e66c2c18663d1`.
The primary author statement is
[Joost de Winter’s comment](https://github.com/jlevy/squares/issues/959#issuecomment-7050119161),
created 2026-11-20T20:41:05Z and updated 2026-11-20T20:41:19Z. It claims a 179-square
construction of side the published 70-square side plus five.

Before this freeze the reviewer read the JSON structure and source coefficients, and
that one comment.
An original README was queried for data-format terms (no matches); only
its heading inventory and Markdown/text filenames were displayed.
No producer programs, project verification programs, derived certificate copies,
receipts, prior verdicts or Stage 4 outcome documents were read.
The project workflow, Python/lint configuration, memory-guard documentation, and
prose-formatting instructions are procedural inputs, not mathematical evidence.

## Mathematical Model

All polynomial coefficient lists are interpreted in ascending degree.
Let

$$f(T)=T^5+14T^4+6T^3-4T^2-7T-2.$$

Let `t` be the real root in the source’s exact rational `t_interval`. A rational
coefficient array `a` denotes the element sum `a[k] t^k`. The replay will certify
uniqueness of the root in that interval by a rational Sturm sequence, and attempt
irreducibility modulo the ordered primes 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31. For
degree five, the finite-field certificate is `X^(p^5)=X mod f` and `gcd(X^p-X,f)=1`; a
successful prime proves irreducibility over the rationals.
A failure to find such a prime within that list is unresolved field-degree evidence, not
evidence that the geometry is false.

The side is the element `S.in_K`:

$$S=1199/89-(209/178)t-(78/89)t^2-(335/178)t^3-(12/89)t^4.$$

For each source record define the center `(x,y)` from its arrays and interpret `u` as a
half-angle parameter, with orthonormal axes

$$e=((1-u^2)/(1+u^2),2u/(1+u^2)),\qquad v=(-e_y,e_x).$$

The square is `{(x,y)+a e+b v : -1/2 <= a,b <= 1/2}`. This explicit definition is
sufficient for an existence proof even if a producer’s undocumented representation
convention differs. The replay must check exactly 179 entries, source orientation-class
consistency, nonzero denominators, and exact unit norms and perpendicularity.
`pins`, `equations`, stationarity flags, decimal approximations and producer statistics
are not premises of the geometry proof.

## Finite Implication and Replay

Arithmetic uses independently written standard-library rational polynomial operations;
products and quotients are reduced modulo `f`, with a Euclidean inverse for quotients.
Equality is equality of reduced coefficients.
For a nonzero element, rational interval Horner evaluation over the isolating interval
must exclude zero; otherwise bisect the root interval exactly, up to 256 refinements.
No tolerance or floating-point sign is accepted as proof.

For a square, the four wall margins are `x-rx`, `S-x-rx`, `y-ry`, `S-y-ry`, where
`rx=(abs(e_x)+abs(v_x))/2` and `ry=(abs(e_y)+abs(v_y))/2`. Their nonnegativity contains
the entire convex square in `[0,S]^2`. For each of all 15,931 unordered pairs, examine
the four edge normals from the two squares.
On one axis `a`, prove

$$|(c_j-c_i)\mathbin{\cdot}a|\;\geq\;
 (|e_i\mathbin{\cdot}a|+|v_i\mathbin{\cdot}a|
 +|e_j\mathbin{\cdot}a|+|v_j\mathbin{\cdot}a|)/2.$$

This separates the interiors of the projected intervals and hence of the squares;
equality permits boundary contact.
The square axes are also edge normals up to sign.
A floating approximation may order candidate axes but never decides validity.
If no axis passes, report that pair as failed/unresolved rather than silently dropping
it. Store the selected axis and exact sign for every pair and the sign of every wall
margin.

Verify `S.poly(S)=0` exactly and certify `S.interval` contains `S`. Compute `S-5`, its
interval and the exact shifted polynomial `S.poly(X+5)`. The source permits this
algebraic shift, but does not independently identify `S-5` with the externally published
70-square construction.
No optimality or record improvement claim follows from this finite construction check.

## Predeclared Controls

Run the following before the source geometry in the same independent verifier:

- Exact signs of zero, plus one and minus one; the relation `f(t)=0`; and a polynomial
  differing from it by one, which must be nonzero.
- A root interval `[0,1/10]`, which must be rejected as containing no root.
- An axis-aligned unit square centered at `(1/2,1/2)` in side one, which must pass with
  four exact wall contacts.
- Two unit squares centered at `(1/2,1/2)` and `(3/2,1/2)` in side two, which must pass
  with a shared edge.
- Coincident copies of the first square, which must fail pair separation.
- Moving the first center to `(-1/10,1/2)`, which must fail containment.
- Duplicating source square zero in source position one, which must fail pair `(0,1)`.
- Replacing `S` by `S-1/1000000`, which is expected to fail containment.
  If it passes, report an inconclusive boundary-sensitivity control rather than infer a
  valid source construction from this mutation.

The acceptance condition is completion of the root/field checks, exact side checks, all
required controls, all 716 wall margins and all 15,931 pair separations, with zero
negative or unresolved required margins.
Counts and any exact contacts are retained.

## Resource Bound and Preservation

One numerical worker uses the supplied Python 3.14.7 interpreter, without installs.
Its initial hard wall cap is 300 seconds from numerical-worker start, enforced by
`SIGALRM` inside the worker.
Cap expiry records partial progress, never success.
A separate, dedicated memory guard is observe-only and watches that worker PID. Scratch
is `/Volumes/spud-ext2/agent-scratch/n179-blind-20261121`, with dedicated `TMPDIR`,
`CARGO_TARGET_DIR`, `UV_CACHE_DIR` and failed-only pytest retention settings.
Source code, frozen plan, receipts and review evidence remain under
`/Volumes/spud-ext2/agent-evidence/n179-blind-20261121`. The external volume was
confirmed mounted with 127 GiB available and writable.

Freeze the implementation bytes and this plan in a manifest before any execution of
controls or source geometry.
Preserve those bytes unchanged.
After the first frozen result, read the standard Stage 4 document requirements and
create a separate runnable copy for project Ruff/BasedPyright checks.
Any changed executable copy must be compared with the original, rerun and recorded
separately; it cannot rewrite the first result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
