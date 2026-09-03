# Review Packets: Agenda 015 Second Wave

**Date:** 2026-09-02

**Author:** Codex, for the project maintainers

**Status:** Frozen BC-144 packet set for BC-145 independent review

These three packets carry the terminal agenda-015 decisions for the n = 17 continuation,
the n = 68 side-semantics refusal and the n = 54 synthetic source contract to fresh
independent reviewers.
They are review instructions, not new experiments.
Reviewers judge retained evidence without repairing it, opening a source or target
channel, running a scientific producer or widening a claim boundary.

## Frozen Revision and Common Contract

The evidence revision is `313624cc08650bb9054e969da9cfd91ad83e2125`. Every experiment,
checkpoint, progress marker, session, hypothesis, instrument and test named below is
read from that immutable tree with `git show`. Later commits may add packet, review and
coordinator-state records; they do not replace the frozen bytes.
A changed executable, checkpoint, progress or test path invalidates safe worktree replay
of the affected packet.

Each packet is preassigned to a fresh BC-145 reviewer who did not author or audit its
BC-144 packet. Mathematical and scientific-boundary judgments use Max effort; mechanical
hash, absence and command checks use XHigh or higher.
Run Python only from `packing/` with the project’s Python 3.14 environment.
Mutations use pytest temporary paths, disable repository caches and bytecode, and must
not alter a retained artifact.

For each packet report one of:

- **pass:** the exact decision, evidence boundary and limitation reproduce;
- **bounded caveat:** the outcome reproduces, but a material frozen limitation prevents
  review clearance;
- **discrepancy:** retained evidence contradicts the recorded decision or boundary; or
- **cannot-reproduce:** the safe replay cannot be completed at the frozen revision.

A pass grants BC-146 permission to change only that experiment’s `needs_review` field
from `true` to `false`. It does not change a decision, hypothesis disposition, frontier,
instrument state or future route.
Any other determination leaves `needs_review: true`. Each reviewer returns **Artifact,
Result, Guard, Next** and names every mismatch.

Before replay, confirm that
`git diff --exit-code 313624cc08650bb9054e969da9cfd91ad83e2125 -- <packet executable,
checkpoint, progress and test paths>` is empty.
The coordinator session is expected to gain BC-144 through BC-146 state after the
freeze; inspect its frozen form with `git show`, not as a worktree-equality condition.
The hashes below are SHA-256 values of bytes at the full frozen revision.

## Packet A: n = 17 / H-052

**Preassignment:** one fresh Max reviewer for the terminal-state and scientific-boundary
judgment, with XHigh-or-higher mechanical checks.

### Decision under review

| Experiment | Frozen decision | Evidence status | Proposed BC-146 transition |
| --- | --- | --- | --- |
| exp-056 | `unresolved`, `needs_review: true`, stopped by `timebox`; cost-role outcome `criterion_missed` | One fixed 05:27--11:23Z elapsed lease retained 170 contiguous agreeing rows through ordinal 169; progress records ordinal 170 at `independent_started`; result absent | Clear review only if the terminal checkpoint, no-partial-row interruption, absence and prefix-only claim boundary pass |

The 21,360-second value is the fixed elapsed lease, including the admitted host-handoff
gap, not active CPU time.
Eleven directions remain uncomputed.
A pass leaves H-052 undecided and moves no lower bound or frontier.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-056 record | `c3328f0ff8cf946ece5441a75df46c90ec1c1fc36bebc64288e5c7262ee2ba9b` |
| terminal checkpoint | `0d39a7e734e8afc62fda914fda4ec8b5e9b2e48ea1b1d8b197dc08e27e7a35d4` |
| terminal progress | `0875f31fbf7391cfa40349812ca38a786069830a28f1c8d92ffd4ab33ecfe93c` |
| session-078 | `0eaba23e7b7afe45aadd484c55703c609ceff331978cf07049cae04b613f4f3a` |
| H-052 | `dd5160d20ca074b182521db6cd3a0dd9d96ddb02530010c50d4ea3b5010d847c` |
| child `run.py` | `f45227508b28f37759df836db08dbad2031d600ef2b1ac087b73f8322b156b05` |
| child `__init__.py` | `ce25d0c6f97d463833260561fdc06b9434c3a9539d3aee9aabd7a98a268778fb` |
| child focused test | `3aa7c0b1816d3545dbf7e77e4fa31f3dc58d5ab727ffb5ad25f64c3049ee137a` |
| unchanged resume driver | `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` |
| resume focused test | `4226ab0cb5f9e46256b5fc47d5bc493dfbb6ef77354e9e7a61d624ba4db76a53` |
| parent checkpoint | `db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` |
| parent progress | `08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af` |

The last retained row hash is
`8947b38e0351048c3a67d914f2b8449185686d920913f5a2404898bdeca4c0b6`. It is a chain link,
not the checkpoint-file digest, and the reviewer must keep those roles distinct.

### Declared absences and safe replay

The canonical result
`campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.json`
must remain absent.
No writer may be live, exp-056 must not be rerun, and review must not
evaluate a target direction.

From `packing/`, run only:

```text
test ! -e campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.json
.venv/bin/python3 -m cases.n17_weighted_certificate_child.run --status campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m cases.n17_weighted_certificate_child.run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -O -m cases.n17_weighted_certificate_child.run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest -q -p no:cacheprovider tests/test_n17_weighted_certificate_child.py tests/test_n17_weighted_certificate_resume.py
```

The status must report 170 rows, ordinals 0--169, `all_agree: true` and a verified
chain; progress must report ordinal 170 at `independent_started`, chained to the actual
last-row hash above.
Both self-test streams must hash to
`9d6cbdc83ad83bf5234b872d67931b7003a038fa870ebc426133368e8e43a28e`, report the 36-guard
inventory hash `612349379b70ccddfa5bd4f5265a747caca768c5b9a9627b4057e69a5791f894`, and
skip none. Seventeen focused tests must pass.

The load-bearing named mutation is `tampered-child-chain-link`. The reviewer also checks
the interruption, no-partial-row and interrupted-versus-uninterrupted equivalence
receipts. A row count, ordinal, chain, agreement, hash, absence or guard mismatch is a
discrepancy. Review cannot resume ordinal 170.

## Packet B: n = 68 / H-058

**Preassignment:** one fresh Max reviewer for the source-provenance and
conjunctive-model judgment, with XHigh-or-higher mechanical checks.

### Decision under review

| Experiment | Frozen decision | Evidence status | Proposed BC-146 transition |
| --- | --- | --- | --- |
| exp-057 | `unresolved`, `needs_review: true`; guard-role outcome `invalid` | The literal fourteen-digit printed-rational point model is mechanically defensible; nearest-six and truncate-six side semantics lack source provenance; BC-139 stopped before source or network access; result absent | Clear review only if the mechanical controls, provenance refusal, no-access boundary and unresolved decision pass |

The registered criterion is conjunctive across all three side models.
The surviving literal point model cannot readmit exp-057 alone.
A pass leaves H-058 unmeasured, does not revive BC-139 and moves no frontier fact.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-057 record | `6815ea48321bc65cbd20d853bdd12ab7b324f273fafb69be943d5a7c63b65d96` |
| session-080 | `f0f58d17a2159981c79825c5137a663be3e26d5f1bb4822a4aefbcf94e3180a2` |
| H-058 | `5689e654e8828877144ef066772b00e491a1df5bb3f2b6997301ff4364a11de8` |
| side `semantics.py` | `dfdbc57724adbc9cc878afe6ff0b3fb0d2c549ac3eb9bbdf7dba772c82f28932` |
| bound `bound_run.py` | `5d6303f228748e76e4a85512d41011a6200602216d925cc8e4de2773a4d90331` |
| semantics focused test | `e8f91e3fb85cb370c617049ef1c7cc23bae04c8f71c83481cc786020afbba3cd` |
| frozen production `adapter.py` | `9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539` |
| frozen production `run.py` | `8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54` |
| frozen production `verify.py` | `e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a` |
| production focused test | `17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df` |
| refusal `run.py` | `3d91046ad9d4ea7b3a7e2f3e7f1ca02aec7cd7118d2291a50f622e8541020029` |
| refusal `verify.py` | `1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f` |

Session-080’s `e2c5a743…` exp-057 hash and the experiment’s short `11ce70ee` commit
field are historical author-time anchors, not the frozen packet hash.
Only the current hash above binds exp-057 in this review.

### Declared absences and safe replay

The canonical exp-057 result and `square-68.svg` must be absent before and after review.
The declared URL and parent digest grant no access authority.
Do not fetch a source, open the network, run `--record`, manufacture side provenance or
inspect n = 68 target geometry.

From `packing/`, run only:

```text
test ! -e campaign/series/series-000-smoke-and-calibration/results/exp-057-h-058-n68-one-parent-localization.json
test ! -e square-68.svg
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m cases.unitsquare_precision.production.bound_run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -O -m cases.unitsquare_precision.production.bound_run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest -q -p no:cacheprovider tests/test_unitsquare_precision_semantics.py tests/test_unitsquare_precision_production.py
```

Normal and optimized self-test streams must be byte-identical at SHA-256
`790a973ee5e11e079a3c41dab578311d491eabe5dee76a120ee3a12f5702d76b`, all 13 named binding
guards must fire, and 62 focused tests must pass.
The load-bearing named mutation is `wrong-direction`; it must refuse both a downward
positive truncate-six interval and a one-sided nearest-six interval.
The reviewer also confirms that the fourteen-digit release-text token is not a
six-decimal SVG coordinate token and that the record cites no source rule projecting
those coordinate semantics onto it.

A changed hash, created result or source byte, network access, silent named mutation or
claim that one surviving model satisfies the three-model criterion is a discrepancy.
Inability to run the safe controls is cannot-reproduce.

## Packet C: n = 54 / H-055

**Preassignment:** one fresh Max reviewer for algebraic and scientific-boundary
judgment, with XHigh-or-higher canonical-byte and import-closure checks.

### Decision under review

| Work item | Frozen decision | Evidence status | Proposed BC-146 transition |
| --- | --- | --- | --- |
| BC-141 | Complete; admit `N54SourceContract/v1` and canonical `N54Result/v1` without amendment | Prospective synthetic-only contract; author and clean-room verifier agree; 79 tests pass; both exit mutations reject; no durable result | Record independent pass or caveat only; H-055 has no `needs_review` transition and remains `instrument_ready: false` |

This packet reviews reusable instrumentation, not a scientific experiment.
No pass may claim live-source fidelity, actual source-label-to-row correspondence,
witness values, precision cells, geometry, feasibility, optimality or a packing bound.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| agenda-015 | `add6eaf4f19317c66661e973c8bcb0f3dc042eac52dd8e756129bd083eb4682c` |
| session-082 | `858c5a76396f8244e0861c61bc996cc4abd05c7850f3bf1683a48ee5beb2a0ad` |
| H-055 | `b8107be65c45cce9c72282ea21102b7f15ac0d31dc93fc47b424dfc9add6d36d` |
| package `__init__.py` | `a4fe1195f79a58b63f18153fa650d2902e6f8df6279402bbc8b0aa4e30c3bbde` |
| author `contract.py` | `1546c5aa6e8f1d9db6942ec76c39692cd408aac9865cbd3753da7fc3ba71338c` |
| author `run.py` | `0f92dea3040581f528c474e44e3970995872233c6bfa3d7a1fafb66c4bf68ef2` |
| synthetic fixture | `92ef9c467564f651efc561d69005c3b0cb847d13f4766ce0e16f365bde791de3` |
| independent `verify.py` | `ba297fcb4ed182784dc08b263706571e736bd72c53d5ccb858adb6855a3cb10b` |
| author focused test | `1c1492f74d63978fdc87b02363e92aaca7e537677c891f487faaa61ca41be912` |
| independent focused test | `028e07bc7e4107c1007ce9f615c36202fa1bf477b1b839f7a5f2e27266ef5be8` |
| frozen formula-audit dependency | `d2029b897393e8604d813eeea0817b657b33d33d935aebe284831e3754955b10` |
| `.python-version` | `922fe0c3de073b01988e23348ea184456161678c5e329e6f34be89be24383f93` |
| `pyproject.toml` | `65ed40a69656a0b490c9e37293503179b618d22a650fe061ba6a8c1438506210` |
| `uv.lock` | `e2785d194b74236df63e839092fae6eb1b7424f5717199380584b932f38cf9bc` |

### Declared absences and safe replay

No retained `N54Result/v1` file exists.
No source/live bytes, source-derived precision cells, target or witness-row values,
geometry, producer result or network access are part of the packet.
The independent verifier must import only the standard library and must not import the
author contract or runner, UnitSquare production code, `sqpack`, SymPy, XML or lxml.

From `packing/`, run only:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m cases.n54_source_contract.run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -O -m cases.n54_source_contract.run --selftest
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m pytest -q -p no:cacheprovider tests/test_n54_source_contract.py tests/test_n54_source_contract_independent.py
```

Normal and optimized author streams must be byte-identical at SHA-256
`79008d0738f17102e77b4c45c54af01f0b0faf8666ab650289dbdef4f89aa3d9`; all 79 tests must
pass. Packet integrity requires both BC-141 exit mutations:
`missing_structural_inventory` must refuse with
`missing or unexpected synthetic source endpoint`, and `correspondence_swap` must remain
bijective yet refuse with `synthetic structural-tag drift`.

The reviewer confirms strict exact-key JSON, duplicate-key/float/exponent/non-finite
refusal, sorted compact ASCII encoding and exactly one terminal newline, plus the
independent import closure.
A missing mutation, author/independent disagreement, forbidden import or access,
published result, noncanonical byte stream or widened source or geometry claim is a
discrepancy.

## BC-145 Reconciliation Rule

BC-145 records the three determinations separately; a pass in one packet cannot hide a
caveat or discrepancy in another.
BC-146 clears only explicitly earned exp-056 or exp-057 review flags, records BC-141’s
independent disposition without changing H-055, and otherwise preserves every frozen
decision verbatim. Repairs and continuations need newly registered future rounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
