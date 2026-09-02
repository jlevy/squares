# W9 Remediation Pass

W9 turns a confirmed defect or issue backlog into bounded, reviewed repair waves.
It is the workflow for systematic remediation, not a synonym for whatever engineering
work happens to be available.

## Entry Contract

Enter with:

- a generated inventory from `packing/defects.yaml` and live tbd;
- an explicit selection rule and a bounded wave, rather than the whole backlog as one
  task;
- the owning defect and bead for every selected item;
- the claim or behavior each repair must preserve; and
- a focused validation command and a regression requirement.

Prioritize soundness and validity risk before bookkeeping, robustness, performance, or
cosmetic cleanup unless an upstream dependency makes that order impossible.
Group defects only when they share a trust boundary, implementation surface, and
validation regime. The convenience of changing neighboring files is not a reason to put
unrelated defects in one wave.

## One Remediation Wave

1. Regenerate the defect view and reconcile it with live tbd.
2. Classify each candidate as actionable, blocked, obsolete, already fixed but
   unguarded, or owned by another evidence workflow.
3. Select a bounded wave and state why it outranks the deferred candidates.
4. Reproduce each selected defect or show the retained evidence that makes reproduction
   unsafe or impossible.
5. Repair the smallest owning surface and add the regression named by the defect.
6. Run focused checks, then the gate tier required by the changed trust boundary.
7. Update `packing/defects.yaml`, close or reroute the owning beads, regenerate
   `defects.md`, and preserve every item that did not close.
8. Return through W10 for reader-document review, reprioritization, and selection of the
   next entry point.

Every selected item leaves one terminal disposition:

- **fixed** — the cause is removed and a regression now guards it;
- **contained** — the unsafe route is mechanically refused, with the remaining repair
  still tracked;
- **rerouted** — the issue actually needs W1, W2, W5, W6, W7, or W8 evidence before a
  repair can be defined honestly;
- **blocked** — the named dependency and the condition that would clear it remain live;
  or
- **obsolete** — current artifacts prove the report no longer applies, and the record
  says what superseded it.

W9 does not create a scientific verdict.
If a repair would need a new packing measurement or a changed claim, route that work to
the workflow that owns the evidence and keep the defect open until that result returns.

## Current Backlog Candidate

The W10 review following Agenda 015 created `think-cyko` for the 56 defects currently
reported open by `defects.md`. That count is a snapshot, not the wave definition.
The first W9 entry must regenerate the inventory, rank it by current risk and
dependency, and select a bounded subset before changing code.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
