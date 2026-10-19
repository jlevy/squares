# wand125 Tools Retrieved 2026-09-29

[wand125/square-packing-tools](https://github.com/wand125/square-packing-tools) is the
maintained MIT-licensed source of the transfer, ladder, budget-recovery and performance
tools used with Tokoharu’s rectangle-density solver.
It also publishes an exact point and threshold-charge row checker.
The citation key is **[wand125 tools 2026]**; certificate results remain attributed to
their own sources, including **[wand125 rectangle bounds 2026]** and the September 28
update.

## Source and Pin

| Field | Value |
| --- | --- |
| Repository | <https://github.com/wand125/square-packing-tools> |
| Revision | `0d33ab61726c2ab03e3eb8f457dabaf22db8571f` |
| Git tree | `d7e28ad3c94a4d26b37992df21af47235c5a055c` |
| Commit date (UTC) | 2026-09-29 02:04:36 |
| Retained source | [upstream.tar.gz](upstream.tar.gz), complete `git archive` of the pinned revision |
| License and credit | MIT; `LICENSE`, `THIRD_PARTY_NOTICES.md` and `solver/PROVENANCE.md` are retained inside the archive |

The source credits wand125’s work with Codex and Claude, Tokoharu’s rectangle method,
solver and unchanged verifier, and Evan Daniel’s point-verifier implementation.
The live repository is an integration source; this immutable packet is the evidence for
the review. Updating one does not silently update the other.
Extract the archive into task scratch on the external volume to inspect or run it; keep
source bytes unchanged.
The archive includes the upstream tests and notices.

## Separately Pinned Update

The [updated source archive](update-3eb08e6/upstream.tar.gz) and
[provenance](update-3eb08e6/source-provenance.json) retain
`3eb08e6c675d8d5aa953cb93da049a3f3cdc6123`, four commits after the original pin.
The update addresses our mass-budget and ceiling-guidance findings and adds upstream CI;
Tokoharu's canonical C++ coverage checker remains unchanged. The
[current process map](../../../../docs/project/guides/verification-tooling.md#wand125-verification-process-and-independent-equivalence)
separates wrapper admission, complete coverage, independent acceptance and matched
performance. Updated controls and benchmarks remain separate from historical receipts.

The provisional T-056/T-057 identifiers in the historical intake below now correspond to
**T-058/T-059**; the result register is authoritative. None of these tools establishes
T-060's claimed exact global optimum.

## Claims and Review

The announcement supplies tools rather than a new numerical lower bound.
The
[mathematical review](../../../../docs/project/reviews/review-2026-09-29-wand125-tools-mathematics.md)
separates two citable claims in the [results register](../../../frontier/RESULTS.md):

- **T-056:** the stated general `B·UB(n)` ceiling.
  Reported and disputed: the finite orientation net and rounded upper-bound inputs leave
  proof obligations.
- **T-057:** the source reports agreement with all 12,028 Kleddamag n11 row minima using
  `general_pose_tree`. This is a row-scan claim; it does not independently establish the
  global counting theorem or rectangle-density coverage.

Neither registration promotes a frontier bound. 
The [ceiling resolution](../../../../docs/project/reviews/review-2026-10-02-wand125-ceiling-resolution.md)
of 2 October proves the ceiling in corrected form, exactly for each $n=1,\dots,100$, in
[exact ceiling certificates](receipts/ceiling-certificates-2026-10-02.json.gz) with a
[summary receipt](receipts/ceiling-certificates-2026-10-02.json): `B·UB(n)` at the 64
integer-grid rows and the update's `B(1+D)·UB(n)` at all 100.
Transfers and rescaling must produce a fresh certificate with exact mass below the
target count and complete coverage; search success and a coverage-only acceptance
message are insufficient.

The pinned source's
[lazy-zmx2 reports](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/point_verifier_lazy/README.md)
compare implementations for the already registered $s(32)=6$ (**T-051**) and $s(45)=7$
(**T-053**) certificates. They report complete census comparisons and private timings,
not distinct packing claims requiring new T identifiers. These lazy-verifier runs have
not been replayed or admitted here; the existing evidence and V/C ratings for T-051 and
T-053 remain unchanged. Separate replay and performance work remains under `think-lg4u`
and `think-wk08`; `think-lest` tracks this classification.

The [verification tooling overview](../../../../docs/project/guides/verification-tooling.md)
records which checks are independent, which replay upstream code, and what remains to be
implemented or replayed.
Review and integration work is tracked by `think-8cps`.

## Preliminary Executed Checks

Using project CPython 3.14.7 and the unchanged source extracted on external scratch:

- [The source’s general-pose-tree tests](receipts/pose-tree-tests.log): 9 passed, 1
  skipped. The optional comparison against a separate square-packing-bounds checkout was
  not enabled.
- [Three n11 rows](receipts/n11-sample.jsonl), indices 0, 6014 and 12027: all exact
  minima matched `1000047518`, and all returned witnesses replayed.
  The input was the retained Kleddamag `6a733f3` packet at
  `packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11`.

These samples do not include the reported global minimum and do not decide T-057’s
complete 12,028-row equality claim.
The source runner appends resumable output; a complete replay must check the exact row
census and reject duplicates or missing rows.
The test invocation was `python -m pytest -q -o addopts='' -p no:cacheprovider
general_pose_tree/tests`; the row invocation was
`python general_pose_tree/run_n11.py CERT_DIR OUTPUT.jsonl 0,6014,12027`. No upstream LP
performance claim was benchmarked.

The [admission negative control](receipts/admission-control.json), reproduced by
[`devtools.audit_wand125_tools`](../../../devtools/audit_wand125_tools.py), runs the
unchanged upstream driver and C++ checker on `n=1, L=3/2`. It scales a uniform measure
to mass `289/10`; the coverage check passes all 201 directions, and the driver
[announces `s(1) >= 1.5`](receipts/admission-control.log).
Since `s(1)=1`, that announcement is false.
The coverage calculation is compatible with the large mass; the missing `mass < n`
admission check is the defect.
This receipt is a negative control and must never be treated as an accepted packing
certificate.

Reproduce from `packing/`, using a fresh external scratch directory:

```bash
python -m devtools.audit_wand125_tools PINNED_CHECKOUT \
  --scratch FRESH_EXTERNAL_SCRATCH --out DURABLE_RECEIPTS --timeout 60
```

## Native Rectangle Checkpoint

The new [`sqpack.rectangle_density`](../../../src/sqpack/rectangle_density.py) uses
exact rational clipping and common-core subdivision independently of `verify.cpp`. Its
[mathematical contract](../../../../docs/project/reviews/review-2026-09-29-native-rectangle-contract.md)
states the admission and coverage proof.

| Input and scope | Native result | Receipt |
| --- | --- | --- |
| [Analytic n3 control](native-analytic-control.json), all 201 directions at side `3/2`, threshold 1 | VERIFIED; exact mass `1683003/625000 < 3` | [Complete control](receipts/native-analytic.json) |
| The upstream false n1 bound, mass `289/10` | REFUSED before coverage | [Admission refusal](receipts/native-admission-refusal.json) |
| Retained Tokoharu n11 at `381/100`, angle 1, at most 100 nodes | INCONCLUSIVE; 46 accepted leaves and 9 unresolved leaves | [Bounded probe](receipts/native-n11-bounded.json) |

The analytic control exercises a complete native proof.
The n11 probe establishes neither full-angle coverage nor even a complete decision at
its selected angle. No existing frontier confirmation is promoted.
`think-bmf3` owns the continuation to complete retained-certificate verification; the
[W7 plan](../../../../docs/project/specs/active/plan-2026-09-29-native-rectangle-verification.md)
defines the next slice.

From `packing/`, the complete control is reproducible with:

```bash
python -m devtools.verify_rectangle_density \
  resources/web/wand125-tools-2026-09-29/native-analytic-control.json \
  --n 3 --side 3/2 --angles all --max-nodes-per-angle 10000 \
  --max-depth 20 --max-seconds 30
```

Exit 0 requires complete coverage and the strict mass budget.
Exit 2 reports a partial or inconclusive run.
A coverage counterexample rejects the candidate; it is not a packing witness or a
refutation of the claimed lower bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
