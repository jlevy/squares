# Lean Feasibility Spike for the `s(11) ≥ 381/100` Certificate

This directory retains nine Lean theorem proofs for the finite counting argument,
atomic-mass symmetry, and scalar inequalities used in the fractional certificate.
It contains no formal proof of the geometric coverage reduction or of `s(11) ≥ 381/100`.
The complete current argument and exact certificate check are the
[proof card](../t-018-proof-card.md),
[embedded theorem and verifier](../t-018-verifiable-claim-381-100.md), and
[minimal exact checker](../minimal_verify.py).

## Verification Status

The source was reviewed and ported on 2026-09-06 from commit
`04127189a7f08cab35b3c3b6e098d7cc9a729ee0`, originally on the
`codex/pr78-s11-adversarial-review` branch.
The six source and build files retain their reviewed bytes; this README corrects their
scope and replay status against the retained `381/100` certificate.
The source branch is provenance, not evidence that its claims are correct.

| Check | Evidence retained here |
| --- | --- |
| Source inspection | Nine theorem declarations, each with a proof body; no `sorry`, `admit`, custom `axiom`, or `native_decide` in the two Lean files |
| Historical build | The source README reports Lean 4.32.1 and Mathlib 4.32.1 builds and an axiom audit; this port did not reproduce those runs |
| Current Lean syntax, elaboration, and kernel checks | Not run: this continuation host has neither the pinned toolchain nor its dependency cache |
| Build dependencies | A committed toolchain, Lake configuration, and manifest pin the Lean version and all nine dependency revisions |
| Full packing theorem | Not formalized; the Lean source does not define oriented squares, packings, or `s(n)` |

A syntax check alone would establish only that the parser accepts the source.
A successful Lean build elaborates the theorem statements and checks their proof terms,
but the axiom audit is also needed: a theorem using a custom axiom or a placeholder
could build while assuming the desired conclusion.
An **axiomatized theorem** has such an unproved dependency; a **placeholder**, such as
`sorry`, leaves a proof obligation unresolved.
Static inspection of these files establishes neither successful elaboration nor a kernel
check.

The historical README reports that the axiom audit used only `propext`,
`Classical.choice`, and `Quot.sound`, Lean’s standard axioms for propositional
extensionality, choice, and quotients.
That report remains unreplayed here.
[`AxiomAudit.lean`](AxiomAudit.lean) prints the dependencies of all nine theorems so a
future replay can verify the claim directly.

## Scope of the Nine Theorems

[`Kernel.lean`](Kernel.lean) has 149 physical lines, including comments.
Its statements cover:

- `sum_assignedMass_le_total`: assigning each nonnegative atom to at most one index
  cannot increase total mass
- `finite_nonnegative_counting_contradiction`: unit mass at each index contradicts total
  mass below the number of indices
- `ownerOf_eq_some_iff` and `finite_nonnegative_mass_bound`: the set-based version,
  assuming each atom belongs to at most one set
- `mass_image_eq_of_permutation`: mass is preserved by an involution when a
  weight-preserving permutation maps the atom sites accordingly
- `n11_total_mass`: the scalar inequality `434547/40000 < 11`
- `n11_net_reaches_pi_over_four`: the scalar inequality
  `(207107/500000)² + 2(207107/500000) − 1 ≥ 0`
- `n11_shrink_margin`: the scalar inequality `(9977/10000)(1 + 207107/90000000) < 1`
- `support_radius_lt_one`: if `B ≥ 0`, `c ≤ 1`, `s ≤ D`, and `B(1 + D) < 1`, then
  `B(c + s) < 1`

These statements isolate parts of the human argument
`11 ≤ Σⱼ μ(Qⱼ) ≤ μ(K) = 434547/40000 < 11`. The set theorem assumes unique membership;
it does not derive it from square geometry.
The symmetry theorem assumes the site permutation; it does not check the certificate’s
1,121 atoms. The three scalar lemmas check numbers used in Conditions 2–4, rather than
deciding those conditions on certificate data.
In particular, despite its abbreviated name, `n11_net_reaches_pi_over_four` contains no
trigonometry and does not prove the equivalence between its polynomial inequality and
reaching π/4.

## Reproduce the Lean Check

With [Elan](https://github.com/leanprover/elan) installed by its documented method, run
these commands in this directory:

```shell
lake exe cache get
lake build Kernel
lake env lean AxiomAudit.lean
```

The committed `lean-toolchain`, `lakefile.toml`, and `lake-manifest.json` pin Lean,
Mathlib, and Mathlib’s transitive dependencies.
Keep the manifest when replaying: `lake update` changes dependency resolutions.
Lake fetches the committed revisions; `.lake/` contains downloaded and built files and
is not part of this package.
The historical source reports approximately 10 GB for the cold toolchain and cache.
No download or installation was attempted during this port.
Retain the command output and axiom audit when a fresh replay is performed, and update
the status table from that evidence.

## Remaining Proof Layers

A complete Lean proof still needs the definitions of oriented squares and packing, the
strict-containment and nearest-angle lemmas, the half-angle tangent identities, the
diagonal-reflection reduction, and the continuum-to-finite coverage reduction.
It also needs a checked connection to the certificate data.
The current Python checker decides Condition 5 over **567,130,649 reachable event
cells** at 181 directions for the `381/100` certificate.
The 90,546,593-cell count belongs to the separate `19/5` certificate in
[`thirdparty/`](../thirdparty/README.md).
Neither computation runs in this Lean spike.

A possible next formalization target is a proof-producing Condition 5 receipt that
records feasible vertical intervals and range minima for each event strip.
With 1,121 atoms, at most `2 × 1121 + 1 = 2243` strips per direction follow from at most
two horizontal-coordinate events per atom and two domain endpoints.
Thus `181 × 2243` is a bound on candidate strip records, not on the proof’s eventual
size or cost: each range-minimum claim and the coverage theorem would still need proof.
No such receipt or checker is implemented here.

`native_decide` can discharge a computation through a compiler-trusting axiom.
The resulting proof term may pass the kernel, but its conclusion then depends on that
additional assumption; it is not independent verification of the compiled computation.
The retained source does not use it.

[`minimal_verify.py`](../minimal_verify.py) remains the self-contained decision
procedure for the retained certificate: 329 physical lines at integration commit
`7e932f1b`, checked on 2026-09-06, using only the standard library on CPython 3.12 or
later. Its exact replay and the handwritten implication establish the computer-assisted
lower bound recorded as T-018; this feasibility spike does not change that result’s
formal-proof status.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
