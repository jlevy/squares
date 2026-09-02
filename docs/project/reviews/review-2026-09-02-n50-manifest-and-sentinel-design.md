# Design Note: `n = 50` Manifest and Sentinel Contract

**Date:** 2026-09-02

**Status:** Target-blind design note; no experiment, scientific result, or campaign
transition

Exp-050 bound four inputs but omitted the producer runner.
Its no-overwrite test could therefore show only that the observed process returned an
existing-result error, not that the exact producer refused before evaluating a fixture.
Exp-055 closed that gap for its prospective control by binding the producer, injecting
live sentinels before dynamic import, and verifying a canonical zero-call trace
independently. A future n = 50 round must incorporate that protocol into its own
preregistered launch boundary.
Exp-055 cannot bind a later producer retroactively.

This note specifies that launch boundary.
It authorizes no source retrieval, target access, geometry computation, producer
execution, experiment registration, or result publication.

## Required Pre-Run Manifest

The round must freeze one canonical, strict-JSON manifest before admission.
The experiment record must bind the SHA-256 of the manifest bytes; the result must
repeat that digest. The manifest must reject duplicate keys and non-finite numbers and
must not contain its own digest.

The manifest must bind:

- the round, hypothesis, frozen scientific revision, launch revision, and exact
  repository-relative experiment and result paths;
- the literal invocation as an argument array, the `packing/` working directory, the
  environment allowlist, and whether normal Python, optimized Python, or both are
  admissible;
- the launcher and resolved Python identities: path, SHA-256, implementation, full
  version, optimization mode, and platform; if `uv run --frozen` is used, the `uv`
  executable, `.python-version`, `pyproject.toml`, and `uv.lock` also belong to the
  closure;
- every first-party executable byte reachable from argument parsing through result
  publication, including package initializers, producer, imported helpers, adapters,
  verifiers, serializers, and publication code;
- every frozen data input, fixture, receipt, schema, and test or admission program on
  which launch permission depends;
- the controller, sentinel harness, independent admission verifier, independent result
  verifier, and their focused tests; and
- for every entry, one exact repository-relative path, role, byte length, and full
  lowercase 64-hex SHA-256, plus a sorted path inventory that refuses an added, removed,
  renamed, duplicated, symlinked, or unlisted executable file.

“Producer hash” alone is insufficient if the producer imports mutable local code.
The manifest generator must compute the transitive first-party import closure from the
literal entry point and compare it with an explicit allowlist.
Dynamic imports and runtime-loaded files must be declared separately.
An unresolved import, namespace ambiguity, editable package outside the repository, or
executable byte without a manifest entry is an admission refusal.

## Literal Invocation and Refusal Order

The experiment record, manifest, admission receipt, and result must carry the same
argument array. A shell-rendered command may be included for readers, but it cannot be
the binding form.
The controller must refuse a changed module, flag, result path, working
directory, interpreter, environment variable, or optimization mode before loading the
producer.

After the controller verifies the manifest and injects the sentinels, the producer’s
order is fixed:

1. decode the already bound arguments without reading a scientific input;
2. require the exact registered result path and sandbox root;
3. use a non-following existence check on that path;
4. if the path exists, raise the exact preregistered exception type and text; and
5. only when the path is absent, cross the first downstream seam.

The existing-result branch must not hash inputs, load a fixture, import a real intake,
evaluate a receipt, access source or target bytes, perform geometry, open a network
channel, or enter publication.
Import-time side effects count as stage calls.
The controller must therefore install fake modules before dynamically importing the
hash-matched producer, as exp-055 did, rather than patching an already imported module.

## Injected Sentinel and Stage Trace

The fixed sentinel inventory must include at least these exp-055 seams:

- `binding_observation`
- `fixture_loading`
- `receipt_evaluation`
- `publication`

If the future round has a source, target, geometry, subprocess, or network seam, the
manifest must either add a separately named sentinel for that seam or declare and verify
that the closure contains no such capability.
A generic “I/O” sentinel cannot stand for unnamed paths.

Each sentinel is a live bomb with its own call counter and distinct exception.
Before admission, each bomb must fire exactly once in an isolated synthetic calibration.
The existing-result control then runs the exact producer and exact argument array
against a temporary root in which the registered relative result path is occupied.
Acceptance requires the exact refusal and a canonical trace with an empty call list and
a zero count for every sentinel.
The real registered result path remains untouched during this control.

## Result-Path and Absence Boundary

The preregistration must name one repository-relative result path and assert its exact
state at three boundaries: absent when the manifest is frozen, absent immediately before
the one authorized invocation, and present exactly once afterward.
“Absent” means `lstat` finds no file, directory, or symlink at the path; no tracked
entry, partial file, temporary sibling, alternate spelling, or hard-link alias may
supply a prior result.

Publication must create a fresh file atomically without replacement, flush the file and
parent directory, and refuse a missing parent or any pre-existing target.
The result receipt must retain:

- the manifest digest and exact invocation;
- the result path, byte length, and postpublication SHA-256;
- pre- and post-run SHA-256 values for every immutable input;
- the pre-run absence receipt and the set of files created or changed by the process;
- sentinel calibrations, the existing-result zero-call trace, and mutation outcomes; and
- a claim boundary that distinguishes admission evidence, an executed refusal, and any
  separately authorized scientific measurement.

Any unregistered mutation outside the one result path is a failed round.
A refusal run must leave the result path absent; an existing-result control must leave
the occupied temporary bytes identical; and an independent replay must not rewrite the
result.

## Required Mutation Matrix

Admission must reject, with a preregistered reason, every mutation below:

1. changed bytes for the producer, any transitive executable, a frozen input, the
   manifest, launcher, lockfile, or verifier;
2. one closure file added, omitted, renamed, duplicated, or replaced by a symlink;
3. changed argument, result path, working directory, environment entry, interpreter, or
   optimization mode;
4. each sentinel moved before the existing-result check;
5. each sentinel omitted, replaced by a dead sentinel, or calibrated at a count other
   than one;
6. changed refusal type or text, including text that says evaluation occurred first;
7. an occupied result, overwrite attempt, missing result parent, symlink target, or
   alternate path spelling;
8. a nonzero stage call, a stage absent from the trace, or different normal and
   optimized canonical bytes; and
9. a result with a changed manifest digest, input hash, absence receipt, mutation
   inventory, claim boundary, or `needs_review` state.

The mutation receipt must list every leaf explicitly.
A summary count cannot show which guard fired.

## Independent Admission and Replay

A different-lane verifier must admit the round before the one authorized invocation.
It must import neither the producer nor the sentinel harness and must not share their
constants at runtime.
From data and file bytes alone, it checks the manifest digest, full closure inventory,
every hash, literal invocation, interpreter contract, result absence, sentinel liveness
receipts, zero-call observation, mutation inventory, and normal/optimized equivalence.
Admission emits a canonical receipt whose SHA-256 is recorded before launch.
It does not open source, target, geometry, or network seams.

After publication, a separately invoked no-import verifier must parse the immutable
result as strict canonical JSON, rehash the manifest and all bound files, verify every
pre/post binding and declared absence, enforce the exact result schema and claim
boundary, and reproduce the mutation checks in temporary paths.
Its normal and optimized stdout bytes must agree when both modes are preregistered.
The verifier may confirm the retained protocol and result bytes; it may not infer an
unrecorded geometry or source claim.

Admission or replay refuses if any closure member drifted, the registered path state is
wrong, the verifier must import production code, or a required fact exists only in a
session narrative.
The result remains review-pending until an independent campaign review
checks the retained receipt.

## Existing Exact Anchors

These values identify the evidence inspected for this design.
They are not hashes for a future round:

| Surface | SHA-256 |
| --- | --- |
| Exp-050 immutable result | `ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02` |
| Exp-050 producer runner bound by exp-055 | `52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d` |
| Exp-055 immutable result | `9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c` |
| Exp-055 independent verifier | `950fd4a4c41224792742d11e5e6b3f2caeeb4937204d680671892ba28820a0df` |
| Exp-055 normal/optimized observation | `b14af9986826001c52e602bcf6185a2814c8dad8914f11b663a21dbe2d8e2879` |

The future preregistration must supply new full hashes and named absences for its own
bytes and paths. Reusing these values without byte identity is a refusal.

## Unresolved Implementation Choices

- The repository has no named tool yet that emits and validates the required transitive
  executable-closure manifest.
  The future W7 design must choose that tool and define how it handles dynamic imports
  and standard-library identity.
- The controller must decide whether cross-host replay binds the Python executable
  byte-for-byte or admits a preregistered set of platform-specific executable digests.
  A version string alone does not settle this.
- A future round with authorized source or network access must name those seams and
  their retention boundary before admission.
  This note does not choose or authorize them.

## Inspected Evidence and Guard

This note was derived read-only from agenda-015 card 4, the exp-050 and exp-055
experiment and result records, the exp-050 producer, and exp-055’s harness, controller,
independent verifier, hypothesis, and session closeout.
No producer, source, target, geometry, network, test, verifier, hash-generation,
campaign-validation, Git, or tbd command ran.
No campaign record, code, generated view, or retained result changed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
