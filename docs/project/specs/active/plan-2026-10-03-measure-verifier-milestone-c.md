# Measure Verifier Milestone C: The Continuous-Angle Family

**Status:** Active

This is the Milestone C section of the independent measure verifier’s specification
(`docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`, lane W1),
written by lane W2 for the bead tree under `think-gpe0`. Its mathematics comes from
§§3–4 of the
[s(59) and s(77) mixed-cover review](../../reviews/review-2026-10-02-wand125-s59-s77-mixed-covers.md)
and from the specification’s §1.7, which states the lemmas this plan names (E, P, S, Z,
W, H, T, DP). It adds no mathematics of its own; it says what `sqverify-fast` must
prove, in what order, and how each step is checked.

## Scope

Milestones A and B decide the net-and-shrink families T, M and L: 201 directions, a
shrunk core of side $B$, and a threshold compared with slack.
Milestone C decides formats D (`mixed 1`: points and axis-parallel segments) and P
(closed point covers), whose claim is stronger and sharper:

> every closed unit square $Q \subseteq [0, s]^2$, at every centre $c$ and every angle
> $\theta$, has $\mu(Q) \ge 1$,

with total mass below $n$. The scaling form of the counting lemma then gives $s(n) \ge
s$ with no net and no shrink, so a cover at margin zero is a proof, and every comparison
with $1$ must be exact or certified.
Points count when they lie in the closed square; a segment counts the parametric
fraction of its closed intersection, in full when it lies along an edge (review §3.2).

The certificates are those of the specification’s §4.1 for families D and P: `s13`,
`s21`, `s32`, `s45`, `n59`, `s60`, `n77` and wand125’s point cover of `s(45)`, with the
format statements for
[point covers](../../../../packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12/certificates/FORMAT.md)
and
[mixed covers](../../../../packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/certificates/s21/FORMAT.md).

## What Carries Over

- Exact admission with duplicate-key and token checks, exact mass sums, and refusals
  with exit status 2; a new parser for the text formats, written from the format
  statements.
- The arithmetic of `SOUNDNESS.md`: branch-free directed rounding (I1), certified
  enclosure of every rational input by exact comparison (I2), and slack against every
  floating-point decision (F2), with an exact rational fallback.
- The box tree: depth-first over an arena, children inheriting the mass proved inside
  every pose of the parent and the list of items still straddling, with the sampled
  release audit (A3) and its fault-injection control.
- Receipts per root, the census tool, the controls tool, the exact oracle as the
  differential reference, and the performance loop’s accept rule.

## What Is New

**Poses and boxes.** A pose is $(c_x, c_y, u)$ with $u = \tan(\theta/2)$, so cosine and
sine are rational in $u$; a box is a closed product of three intervals, split into
closed halves. Admissibility is $w/2 \le c_x, c_y \le s - w/2$ with $w = (1 + 2u -
u^2)/(1 + u^2)$; a box with no admissible pose is a leaf (lemma E).

**Regions.** Full mode needs no symmetry: centres over the whole admissible range with
$u \in [0, \tfrac12]$, for $\mu$ and for $\mu$ reflected by $y \mapsto s - y$, which
covers every angle. $D_4$ mode checks invariance under $x \mapsto s - x$ and $x
\leftrightarrow y$ exactly, as a measure (point weights aggregated, line densities
merged), refuses otherwise, and covers $[0, s/2]^2 \times [0, \tfrac12]$. Full mode is
the default; $D_4$ mode is a cheaper second receipt.

**Points (lemma P).** Four quadratics in $u$, affine in the centre, decide whether a
point lies in the square; over a box, each maximum is at a centre corner and at an end
or the vertex in $u$. A point is inside every pose when all four maxima are proved
nonpositive, outside every pose when one minimum is proved positive, and straddling
otherwise; children inherit both decisions, as rectangles do in net mode.

**Lines.** Segments are grouped by the line they lie on, with each line’s cumulative
mass a nondecreasing piecewise-linear function built exactly at admission; a point on a
line may be assigned to it as an atom, and any assignment is sound.
A line’s chord in the square has four end functions of $(d, u)$; lemma S bounds one line
by its chord proved common to every pose, lemma Z bounds two lines at unit spacing
together through the exact identity that couples their chord ends (this closes boxes
near $\theta =
0^+$, where single-line bounds vanish), lemma W uses admissibility for a line at
distance one from a wall, lemma T maps horizontal lines to vertical ones, and lemma DP
takes the best partition of each chain of lines into singletons and pairs.

**Angle zero (lemma H).** A box with $u_0 = 0$ contains axis-parallel poses, where the
chord end functions have no finite limit and a segment along an edge counts in full.
`sqverify-fast` must state, prove and test its own argument that every bound it computes
on such a box holds at its poses with $u = 0$, not only as $u \to 0^+$.

## Arithmetic

Binary64 enclosures carry the bulk, as in net mode.
Three places need more care:

- Lemma P’s maxima in $u$, where a quadratic’s vertex may sit at an end: decide the sign
  from enclosures of the end values and of the vertex value, with the exact path when an
  enclosure straddles zero at the depth floor.
- Lemma Z’s infimum over its candidate breakpoints, which takes both one-sided limits at
  each atom height; computed from enclosed breakpoints, with the candidate set’s
  correctness tested against an exact evaluation on sampled boxes.
- The chord end functions near $u = 0$, whose terms grow like $1/u$: enclose them in a
  form that stays finite on boxes with $u_0 > 0$ and route $u_0 = 0$ boxes through lemma
  H.

Every lemma gets a property test against the exact oracle, as R2 and R5 have: the exact
capture of points and segments at sampled poses, including poses at a box’s corners, at
$u = 0$, and with points on the square’s edges.

## Slices

| Slice | Deliverable | Exit |
| --- | --- | --- |
| C1. Admission and oracle | Parsers for formats D and P; exact $D_4$ invariance check; the exact capture at a rational pose; `SOUNDNESS.md` section for the claim, the regions and lemma E | Every retained cover admitted; a cover with one point moved refused in $D_4$ mode; the oracle agrees with an independent evaluator in the check tool |
| C2. Points | Lemma P with inheritance; full and $D_4$ regions; receipts per root | `s13` and `s32` verified in both modes; the drop-heaviest-point controls refused with exact witnesses |
| C3. Single lines | Line measures, chord enclosures, lemmas S, T and W | Property tests of the chord enclosures over boxes, including near $u = 0$ |
| C4. Pairs and angle zero | Lemmas Z, H and DP | `s21`, `s45`, `n59`, `s60`, `n77` and the wand125 `s(45)` point cover verified; their drop-heaviest-segment controls refused |
| C5. Controls and census | Fault injection on a cover; the census of every retained cover with receipts; agreement per root with the authors’ recorded results | Spec §4.2’s continuous-mode controls refused; census complete |
| C6. Performance | Black-box timing of the authors’ checker per root through the replay command, beside this crate’s CPU, by the performance loop’s rules | The target of the specification’s §4.5, or the loop reopened |

C1 and C2 can start at once.
C3 depends on C1, and C4 depends on C3; C5 and C6 run beside C4 as each certificate
lands.

## Inputs and Independence

Allowed, beyond what Milestones A and B used: §§3–4 of the s(59) and s(77) review (read
for this plan), the specification’s §1.7, the format statements above, and the cover
files and their JSON or log summaries as data.
Not opened: `zmx2.rs`, `zm_mixed.py`, `mixed_cover.py`, and the checker-driving
internals of `replay_evand_zmx2.py`; the authors’ checker runs only as a black box, for
timing.
`ZMX2.md`, the authors’ paper proofs of the lemmas, is not on the forbidden list;
it stays unread unless the coordinator clears it, and the lemmas are proved again in
`SOUNDNESS.md` from the specification’s statements.

## Open Questions

- Full mode doubles the roots against $D_4$ mode, before any symmetry saving; the census
  will say whether every cover affords it.
- Review §4 records that a point-assignment rule not invariant under quarter turns left
  boxes open in a full-mode run of the `s(32)` point cover.
  Assignment does not affect soundness, only completeness; C2 should try more than one
  rule.
- Whether the exact fallback near the threshold is fast enough for covers whose least
  bound sits at margin zero, which the scaling argument allows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
