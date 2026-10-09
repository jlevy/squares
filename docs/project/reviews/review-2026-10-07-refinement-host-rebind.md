# Refinement Host Relocation and Rational Feasibility Review

The #425 `host-v3` relocation is accepted for coordinator-authorized replay of the two
selected counts, n=105 and n=292. The #428 n=68 rational witness passed fresh polygon
and support checks, including two invalid full-roster controls.
Repository integration and final storage admission remain pending.

Reviewer: the separately prompted `refinement_review` agent, strong tier, GPT-6 Astra at
xhigh reasoning. Review date: 7 October 2026 in America/Los_Angeles; the execution and
acquisition date is 8 October UTC. This is a scoped review of external artifacts and
work in progress based on repository head `0d01524be4235b7f12e6a971d73ea7d576fbac0f`,
not a final PR-head review.

## #425: Accepted Host Relocation

The source is
[`lollipoll/couzo-five-exact-certificates` at `bc389ddf7d65277cd19a9b08fb285d86346d6806`](https://github.com/lollipoll/couzo-five-exact-certificates/tree/bc389ddf7d65277cd19a9b08fb285d86346d6806).
Only `reviewed/witnesses/n105.json` and `reviewed/witnesses/n292.json` are selected.
The historical n=130/263/272 material and the restricted n=105 dual are outside this
acceptance. An unrestricted lower bound cannot be inferred from that dual.

The preserved checkpoint is under
`/Volumes/spud-ext1/agent-scratch/import-resume-refinements/tmp/`. Its
`squares-425-engineering-preparation/` directory contains both `frozen-v2/` and
`host-v3/`. This path identifies local audit custody; publication must supply durable
recovery rather than rely on disposable scratch.

| Accepted artifact | SHA-256 |
| --- | --- |
| `host-v3/prepared-manifest.json` | `c89637f9f4f9c432af82bffbfb3cccd06104a0c4602b50496dfe363a5ccd621e` |
| `host-v3/runtime-identity.json` | `0c98a917e6d201736db334f27f57bbdc59e843f5c67977d5a1ed728432ea883c` |
| `couzo_replay.py` | `f1a938265e897a9157a36ce016a0615e92bac5c965996de63483a47eddba847b` |
| `couzo_refinement_packets.py` | `11fe3792f3f37361a6b44c545e2a50b5c67df6e631c8067601cd642cb38aa82f` |
| Retained house schema | `754ddd6eea0558344c174302318ed1e7235d9665f37ef4f6fdea1f1e627664dc` |

An independent byte comparison checked every science file beneath the two frozen roots.
All ten prepared jobs, both raw source files and the retained schema are unchanged.
Removing `runtime` from the two parsed manifests leaves equal objects.
The runner and adapter match the accepted frozen digests above.
All 13 retained module source texts are unchanged and equal their files in the import
worktree.

The only changed runtime fields are `executable`, `python`, `schema_selected`, and each
module’s absolute `path`. Python remains 3.14.7 with optimization disabled; the build
changes from Linux Clang 22.1.3 to macOS Clang 21.0.0. Dependency versions remain PyYAML
6.0.3, jsonschema 4.26.0, jsonschema-rs 0.49.9, mpmath 1.3.0 and strif 3.1.0. The
hardcoded Linux schema path in `prepare()` is unchanged; relocation copies already
reviewed science files and does not invoke that preparation entry point.

The reviewer independently ran the unchanged runner’s
`validate --root .../squares-425-engineering-preparation/host-v3` using
`packing/.venv/bin/python3 -B`, with `PYTHONPATH` selecting the import worktree’s
`packing` and `packing/src`. It exited 0 in 3.45 seconds.
This command performs input and runtime admission without geometry decisions.

The prior mathematics and binding acceptances remain scoped to `frozen-v2`:
`squares-425-complete-input-math-review/runner-review/review.md` and
`squares-425-binding-review/final-protocol-review.txt`, relative to the checkpoint root.
This addendum covers their relocation to the exact new identities above.
It does not count those earlier acceptances as newly independent reviews.
The coordinator must explicitly bind the new manifest to accepted review records and
assign the replay’s CPU lease before execution.

The unchanged protocol requires two positive jobs and eight full-roster controls:
duplicate-square overlap, outside-container, overlap by `1/10^100`, and wall protrusion
by `1/10^100`, each at both counts.
It requires 47,946 positive pairs per route and 239,730 pairs over all ten jobs per
route. Tiny overlap must retain the native pair 0/1 failure and the independent
designated gap `-1/10^100`; tiny wall must retain that exact actual minimum clearance on
both routes. These are replay obligations, not completed outcomes in this review.
After replay, inspect every actual receipt, child exit, timeout flag, complete input,
route result and timing against the accepted manifest.

## #428: Verified Rational Feasibility

The certificate is
[`refinement-v1.1.0/n68.json` at `fded686668e29258dad2eb29d0482fa3fd51bd6b`](https://github.com/lollipoll/certified-square-packing-68/blob/fded686668e29258dad2eb29d0482fa3fd51bd6b/refinement-v1.1.0/n68.json),
49,162 bytes, SHA-256
`6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9`. Its full ceiling is

```text
879879523721828390257668096702139408352101903022787926324037/100000000000000000000000000000000000000000000000000000000000
```

The reviewer read both complete standalone programs before loading them: `verify.py`
(polygon edge-normal SAT) and `independent_support_check.py` (center/support radii).
Their retained program pins are respectively
`911b9822334636ffc49472e4df32e38cb162efbfad9a4684879f006b1c90e7f9` and
`48e1ae336855ba5cc05c3fd161bf51ef71cab24ebc33ae590be040f78a932423`. The replay used the
project Python 3.14.7 with `-I -B`, assertions enabled, standard-library `runpy`, and an
independent check of the raw certificate digest.
It executed no analytic launcher or search producer.

| Full-roster job | Polygon | Support | Pairs per route |
| --- | --- | --- | ---: |
| Original 68 squares | Accepted | Accepted | 2,278 |
| Square 2 replaced by square 1 | Rejected; pair gap `-1` | Rejected; pair gap `-1` | 2,278 |
| First center moved to `x=2L` | Rejected; negative wall clearance | Rejected; same wall clearance | 2,278 |

The positive routes agree exactly on both rational minima.
Their pair margin is approximately `9.99999999888e-71`; wall clearance is approximately
`2.29019373019e-61`. These decimals describe the exact results, not acceptance
tolerances. All six route calls completed, covering 13,668 unordered-pair decisions, and
the review command exited 0 in 7.65 seconds.

The importer’s separate retained
[source geometry receipt](../../../packing/resources/web/rehwaldt-n68-refinement-2026-10-07/receipts/source-geometry.json.gz)
contains the complete three input rosters and six route results.
The reviewer checked its original input against the pinned raw JSON and confirmed each
recorded verdict and pair count.
That receipt uses `x=-2L` for its outside control; the reviewer’s independently executed
control used `x=2L`. The receipt’s timings belong to the importer’s execution, not to
the reviewer’s.

Exact `Fraction` subtraction from Daniel’s stated rational ceiling gives

```text
8798795237260591647898096977212073675963/100000000000000000000000000000000000000000000000000000000000
```

This positive difference establishes the stated comparison between these two values.
The shorter upward display `8.798795237218283903` is larger than Daniel’s value and
cannot represent the improvement.
Retain the complete fraction or its complete terminating decimal.
A broader current-best or priority claim requires the separate source comparison.

The implementations share the certificate, half-angle parameterization, separating axis
theorem, Python and `Fraction` arithmetic.
The independent routes support finite rational feasibility only.
The contact-system root, analytic relaxation, restricted orientation dual, local or
global optimality, rigidity and human peer review receive no assurance from these
executions.

## Integration Findings and Custody

The source-to-facts comparison passes for all 465 squares across n=68/105/292. For
n=105/292, every new witness’s complete deciding input also equals the corresponding
accepted frozen positive input.
Translation by `(L/2,L/2)` occurs once; `center_expansion` remains quoted metadata
describing upstream work.

**R1 — High: bind the live facts consumer to retained evidence.** In the reviewed
work-in-progress `refinement_packets.read_fact`, strict structural re-admission alone
accepts a changed, syntactically valid side or coordinate triple.
`to_witness` then supplies the fixed source revision and URL to those changed facts.
The current files equal the acquired source, but this reader does not itself establish
that equality. **Fix:** make the integration checker compare the complete facts and
emitted deciding input with pinned, recoverable source and the complete input behind the
admitted receipt. Exercise changed-side and changed-coordinate refusals through the live
consumer. A later integration check may discharge this finding; this review does not
claim one already exists.

**R2 — High: finish durable recovery and snapshot admission.** The available
109,658-byte private-snapshot headroom cannot hold the older 143,396-byte pair of
compressed expanded-input artifacts, before adding receipts or reviews.
The snapshot cap remains 201,326,592 bytes.
A source release alone does not retain the newly executed host receipts or this
relocation decision.
**Fix:** provide a concrete recovery path for raw source, complete semantic jobs,
runtime/schema, full actual results, reviews and process outcomes; validate the
recovered bytes or complete objects against the reviewed originals.
Measure the finished worker snapshot and run the affected private-control consumers.

A compact representation is plausible without dropping evidence: the two raw #425
sources plus the full original runtime object, including all 13 module texts and both
protocol programs, compress to 62,844 bytes with XZ in a single JSON object.
The raw n=68 source compresses separately to 4,732 bytes.
The reviewed deterministic recipes can recover expanded inputs; their recovered objects
must equal all ten original reviewed baselines.
These measurements omit some required final evidence and integration code, so they do
not establish that the final import fits.
A published evidence asset also needs a pinned manifest, tested recovery and explicit
private-worker access.

The design keeps immutable scientific input separate from host runtime metadata and
avoids copying repeated expanded corners merely to reproduce a witness.
The final PR still needs its own code, records, renderer, release-pin, custody, storage
and validation review.
This addendum assigns no registry assurance and approves no merge.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
