# PR 127 Integration Checkpoint Evidence

These are the actual local validation outputs for the corrected PR 116/121/127 stack.
The full invocation at `ef8a2e72518b492747f32e1abe32563033524365` failed six of its 69
steps. Repairs at `cbe9fd76ee05a6d82804d45075454edd105398a8` passed the 62-step fast
surface and the three previously failing deferred components.
Four successful deferred components from the original invocation have unchanged source
and inputs across that nine-file repair.
This composition covers all 69 steps; it is not a successful new full invocation, and
the original failure remains in the record.

| Invocation | Source | Outcome | Wall seconds | Retained output |
| --- | --- | --- | ---: | --- |
| Full checkpoint | `ef8a2e72` | Six failed steps; the four reused geometry components passed | 1313.94 | [Raw stdout](full-ef8a2e72.txt) |
| Fast surface | `cbe9fd76` | All 62 steps passed, including 4304 fast tests | 298.34 | [Raw stdout](fast-cbe9fd76.txt), [run and step receipts](fast-cbe9fd76/) |
| Slow and exhaustive components | `cbe9fd76` | 97 slow and 55 exhaustive tests passed | 1542.95 | [Raw stdout](slow-cbe9fd76.txt), [run and step receipts](slow-cbe9fd76/) |
| Negative controls | `cbe9fd76` | Passed | 329.13 | [Raw stdout](negative-cbe9fd76.txt), [run and step receipts](negative-cbe9fd76/) |

The four reused steps are the known-best `n=1..324` atlas rebuild, single-square
translation escape screen, exact rational grid replay, and `n=40` rigidity bracket
replay. The repair changes only the handoff records and generated views, their
selected-entry control, and the negative-control snapshot guard.
It does not change those four geometry producers, readers, witnesses or dependencies.

The structured receipts are copied without modification from the runner’s output.
Only run and step summaries are retained beside the raw stdout; command-level logs and
JUnit copies are omitted.
The initial full invocation did not produce structured receipts, so its source identity
is the coordinator’s recorded clean revision and its evidence is the unmodified raw
stdout. No later receipt is manufactured for that run.

All commands used the project’s Python 3.14.7 environment.
Corrected test invocations set `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` for the
installed Cairo library, as documented in the development guide.
The first full run’s local environment and storage-guard failures do not change any
scientific verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
