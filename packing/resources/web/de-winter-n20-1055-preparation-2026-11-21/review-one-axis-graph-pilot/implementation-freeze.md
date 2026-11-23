# Frozen Implementation: Sixteen-Case Graph Pilot

This implements the unchanged
[predeclared selection and mathematical plan](graph-pilot-plan.md).
The selected indices are exactly
`0,244,489,734,978,1223,1468,1712,1957,2202,2446,2691,2936,3180,3425,3670`. The checker
has not yet been executed, imported, compiled or syntax-checked.

## Input and Streaming Boundary

The exact 785,142-byte case-to-clause gzip is copied as data.
The checker first hashes its stored bytes, then hashes all 24,888,016 expanded bytes
using 64 KiB blocks.
It accepts only the predeclared identities.

A separate incremental JSON decoder reads every case index in sequence and the complete
source summary, with a 1 MiB buffer ceiling and a 256 KiB case ceiling.
Only the sixteen selected rows are retained.
Each selected row is bound by its original JSON-byte digest.
The solver validates its edge domain, original literal masks and path-origin partition.
There is no producer import, geometry execution or bank lookup.

## Enumeration and Induction

The implementation uses a partial assignment represented by an assigned-bit set and the
subset assigned one.
A clause already satisfied is skipped.
A clause with no unassigned literal and no satisfied literal is a contradiction.
A clause with one unassigned variable forces that variable’s literal value.
Opposing forced values are a contradiction; otherwise all forced variables are added and
the scan repeats.

Every propagation step preserves the complete model set under the current assignment.
If no forced variable remains, choose the lowest unset bit and visit both disjoint
values. Each child fixes another variable, so recursion terminates.
If every clause is satisfied, enumerate every subset of the free-bit set.
Those subsets are exactly the remaining completions.
This proves exhaustive traversal by induction on the number of unset variables.

Each emitted mask must be within the declared edge domain, unique, and satisfy every
original clause. After a case finishes, a separate literal-by-literal evaluator rechecks
every model without using the solver’s bitwise satisfaction expression.
The complete sorted model list is retained; counts alone are not accepted.

The formula domain disallows a positive and negative occurrence of the same variable
within one clause. Such tautological clauses never occur in the accepted input.
The production input clauses are purely positive or purely negative; the toy controls
also exercise mixed clauses with disjoint positive and negative literals.
No subsumption, symmetry reduction, branch heuristic or clause deletion is added.

## Seventeen Frozen Controls

The twelve three-variable formulas and expected counts are exactly those in the
predeclared plan. An independently expanded literal evaluator enumerates all eight
assignments for each formula.
The solver’s complete model set must match, and the truth-table count must also equal
the hand-declared count.

Five deliberately faulty outcomes must be refused:

- Reversed polarity of the positive-unit fixture.
- Omitting the odd branch from an unconstrained three-variable model roster.
- Duplicating one emitted mask.
- Emitting mask 8 in a three-variable domain.
- Solving an unconstrained three-variable formula under an imposed one-model cap.

The first four are rejected by the domain, uniqueness or independent model-set audit.
The last must stop with the exact reason `total-model-cap`. Control searches have
separate counters; their work is included in total runtime, while the pilot’s reported
search-node and model counters cover only selected cases.
All seventeen controls must pass before the pilot begins.

## Limits and Completion

The limits remain 60 supervised seconds, 55 internal seconds, 0.25 GiB owned process
tree, pressure-1 admission and stop at pressure 2. The checker also stops at 0.23 GiB
worker peak RSS, leaving room below the tree ceiling.
Search-node and model limits remain one million total nodes, 100,000 total models and
50,000 per case. Output ceilings remain 16 MiB expanded and 4 MiB compressed.

The coordinator explicitly authorized this short pilot to overlap the already guarded
paper comparison and remote sweep at pressure 1 with the strict cap.
This modifies only execution scheduling from the earlier serial-slot plan.
Selection, mathematical domain and resource ceilings are unchanged.
The retained supervisor checks pressure 1 both at preflight and in the initial observer
sample before releasing the worker.

No result is complete unless all sixteen cases finish, all seventeen controls pass and
the independent model audits pass.
A caught cap or failure produces an incomplete receipt with the precise stop reason,
completed case rows and any incomplete current model list; the worker returns nonzero.
An external kill may leave only the supervisor/guard failure journal.
Such an attempt cannot be interpreted as a mathematical refutation or success.

Every case retains its original row identity, original clause-list identity, model
roster, nodes, conflicts, forced assignments, terminal satisfied subspaces and timings.
The output is deterministic gzip except for recorded measurements, and its expanded
identity is verified by a streaming roundtrip.

## Invocation

From this directory, with isolated project Python 3.14:

```bash
"$PYTHON" -I -B strict-supervisor.py "$OUT/pilot-execution-01" 60 0.25 \
  "$PYTHON" -I -B check_graph_pilot.py \
  --input case-clauses.json.gz --output "$OUT/graph-pilot.json.gz"
```

Use fresh output paths and external scratch/cache variables.
The supervisor uses the installed memory-guard skill in observe-only mode and owns
termination of this dedicated process group at a declared cap.
No unrelated process may be signaled.

The reviewer’s prior exposure to the producer solver is disclosed.
This first-party search and literal-level checker are independent implementations.
Only accepted clause data is reused.

Even a completed pilot decides only these sixteen finite Boolean model sets.
It does not establish all 3,671 graph rosters, the producer’s 273,584 total,
graph-to-bank applicability or Stage 4 acceptance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
