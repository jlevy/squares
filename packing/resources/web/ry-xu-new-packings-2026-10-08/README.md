# ry-xu’s new square packings: issue #432

This packet retains complete factual inputs and exact deciding outcomes for all 25
packings reported in [issue #432](https://github.com/jlevy/squares/issues/432). The
immutable source is
[ry-xu/square_packing at 8dc4152](https://github.com/ry-xu/square_packing/tree/8dc415296f697f5140caea27c7a0193d52deb4e6).
No upstream program was executed.
The source tree had no license file; this packet contains factual certificates, derived
geometry and acquisition metadata, rather than upstream implementation or explanatory
prose.

Credit for the reported constructions belongs to ry-xu.
The source describes an LLM-assisted search and certificate workflow.
This import independently checks feasibility; it does not establish a global optimum,
search completeness or novelty.

## Complete rational inputs and decisions

`facts/complete-certificates.json.xz` contains the original certificate text for all 25
counts: 51, 70, 84, 86, 88, 102, 103, 105, 108, 123, 126, 127, 129, 130, 131, 146, 153,
175, 179, 236, 258, 261, 263, 267 and 295. Each certificate’s acquired SHA-256 is frozen
in `packing/devtools/ryxu_arrangement_reports.py`. Acquisition also compared original
bytes with the immutable Git tree’s blob identity.

The source’s exact rational side and full centre/half-angle roster are used unchanged.
The certificates already include the source’s stated dilation; this import adds none.
The source’s printed decimal does not decide an upper bound.
Safe display values are computed upwards from the complete exact rational side.

`receipts/exact-certification.json.xz` contains all 75 full-roster jobs: each original
packing, a duplicated-square overlap control, and a square translated outside its
container. Every job retains the full deciding input and complete outcomes of the native
rational witness verifier and independent rational corner/SAT checker.
The conversion from source half-angle coordinates is a shared boundary that requires
review; the two deciding geometry implementations are distinct.

The actual two-worker replay took 330.19143345800694 seconds and made 2,078,082 pair
decisions. All 25 positives passed both routes; all 50 controls failed both routes.
Counts superseded by better existing packings remain in the packet.
Initial comparison found 18 possible current improvements and seven superseded inputs;
final adoption must compare exact sides with the current integrated frontier.

From `packing/`, using the project interpreter and task-specific external scratch:

```bash
python -m devtools.ryxu_arrangement_reports certify --jobs-dir "$TMPDIR/ryxu-jobs" --workers 2
python -m devtools.ryxu_arrangement_reports check
```

The deciding command retains child stdout, stderr and exit records in the specified
scratch directory. The complete source facts and final deciding receipt belong in the
repository. A receipt check binds all original source bytes, every square, all controls,
both full native outcomes and their complete pair counts.
`check --replay` reruns the selected cases rather than trusting the retained outcomes.

## Separate undilated n=51 construction

`facts/n051-undilated-record.json.xz` retains the complete 51-square exact record
extracted from the source’s `square_packing_records.json`. Its original source blob and
canonical selected record are separately bound in `ryxu_radical_n51.py`. The side is
`(16 + 5√2)/3`, a root of `9s² − 96s + 206`; this is a construction upper bound, with no
claim that `s(51)` equals it.

All source coordinates are parsed with a closed rational/radical grammar.
The native route uses a certified number field for the positive root of `x² − 2`. The
independent route uses pairs of rational coefficients, exact order through rational
comparisons, and directly constructs axis-aligned squares and diamonds.
It shares neither the native number-field implementation nor its geometry
implementation.

The three complete 51-square jobs retain native inputs and both full outcomes in
`receipts/n051-radical-*.json.xz`. The durable replay made 7,650 pair decisions in
18.707450165995397 seconds.
Its positive passed and both controls failed.
Native number-field diagnostic decimals are retained as diagnostics; the complete input
coefficient pairs define the exact geometry.
The independent checker counted 119 pairs touching on a separating axis; this count is
not the source’s different contact statistic.

```bash
python -m devtools.ryxu_radical_n51 certify
python -m devtools.ryxu_radical_n51 check --replay
```

Both imports still require independent review, production custody and frontier
integration checks before their assurance status is promoted.
The source facts and actual deciding results are preserved even if an input is
superseded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
