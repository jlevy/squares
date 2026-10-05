# n17bb-native

This crate is the optional native kernel for the retained $n=17$ sub-pattern
branch-and-bound search.
It ports the pilot’s `pair_term`, `dual_bound`, LP step, and tightening loop to Rust
while preserving their Python interface.
The dense simplex implementation retains its basis between the LP step and bound
tightening. Sessions admit one to fifteen boxes and at most 512 rows; pair evaluation
requires `merge_gap=0`.

The extension uses Python 3.14’s stable ABI. Build and copy it to an importable name
without changing Python dependencies:

```shell
cd packing
uv run --frozen python -m devtools.build_n17_bb_native
```

The helper runs rustfmt, Clippy, unit tests, rustdoc, and the locked release build.
Its last output line is the directory containing `n17bb_native.abi3.so`, or the
equivalent name on the current platform.
From `packing/`, the default is `n17bb_native/target/python`; `--output-dir` selects
another destination.

The native path is an accelerator rather than independent proof evidence.
Differential replay checks it bit for bit against the Python LP and tightening loops
when those loops use the same copied `TinyLP` backend.
The ordinary pilot uses HiGHS and can traverse a different tree.
Summary equality is required only with that same-LP Python reference; HiGHS can produce
different duals, node counts, and budget-limited summaries.

Sound pruning does not trust the simplex objective by itself.
The LP supplies candidate nonnegative multipliers, and `dual_bound` evaluates the
resulting linear combination over the whole coordinate box with outward-rounded interval
arithmetic. Only a strictly positive interval lower bound closes a node.
Tightening uses the same operation to admit each stronger coordinate bound.
Pair constraints likewise carry outward-rounded trigonometric enclosures from the pilot.
Certificate recording and Taylor-mode runs stay on the Python implementations, so the
native path cannot bypass their evidence paths.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
