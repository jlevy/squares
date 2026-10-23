---
title: CI and Release Latency Audit, 22 October 2026
description: Measured setup and browser costs, prior fixes, and proposed follow-up work during PR737 delivery.
---
# CI and Release Latency Audit, 22 October 2026

Ordinary hosted validation remains expensive after the earlier CI fixes.
The observed critical path combines a variable setup cost with a consistently
substantial browser workload.
This audit supports `think-nnny` and the
[CI iteration-cost plan](../specs/active/plan-2026-10-14-ci-iteration-cost.md).
It proposes work; it implements no workflow or validation change.

## Measurements and Limits

Times below are UTC on 23 October, during the 22 October local session.
Commands used: `gh run view --json jobs`, `gh run view --job ... --log`, `gh pr view`,
`git log`, `git blame`, and inspection of `.github/workflows/packing-validation.yml` and
`.github/workflows/pages.yml`. The review applied `tbd guidelines ci-and-gates-rules
release-engineering-rules`.

| Evidence | Observation | Limit |
| --- | --- | --- |
| [Packing 39892772106](https://github.com/jlevy/squares/actions/runs/39892772106), head `bf38442f248d089b9862d04ee0658f85b51d7b0c`, frontend job `120216469741` | Combined npm and Playwright setup took 524s, 03:03:58–03:12:42. Frontend site validation subsequently took 663.84s; workbench behavior (181.63s) and browser floor (111.8s) overlapped it. Every other required worker finished by 03:12:44. | Completed logs attribute setup to apt package downloads: 25.9 MB in 8m32s (50.6 kB/s), reported at 03:12:37. npm installed 96 packages in 2s at 03:04:01. A provisioning speedup remains unmeasured. |
| [Pages 39892772091](https://github.com/jlevy/squares/actions/runs/39892772091) | Succeeded by 03:09:18, about 7m19s after creation. Overview rendering twice took 206s; its preview-card/head check took 78s. | PR validation does not establish a production deployment. |
| [Packing 39893731935, frontend](https://github.com/jlevy/squares/actions/runs/39893731935/job/120219204931), head `79abd064d34119cd4157deb39784e551d52ec4e8` | Setup took 16s. npm and Playwright caches hit; npm installed 96 packages in 1s. apt still fetched metadata and packages. Checkout took 87s. Frontend contracts took about 485s. | Different head and runner; this comparison separates plausible cost components but is not a controlled speedup measurement. |

The completed comparison’s site step took 483.52s: the parallel functional phase
reported 485 passed and six skipped in 392.38s, followed by 51 serial forwarders in
59.26s and four serial HTTP cases in 29.89s. Browser-floor checks took 72.4s and
workbench behavior 100.4s while overlapping that critical path.
Those durations must not be summed as sequential wall time.

The log reports 483.5s against the frontend tier’s 165s ceiling and recorded 104.74s.
Its cost verdict is advisory under `think-ht59`. A green functional verdict therefore
does not establish the three-minute objective.
The observation does not identify which fixtures or individual browser operations
account for the 392s phase.

## Apt Transfer Diagnosis

The slow and fast completed frontend jobs used the same `ubuntu-24.04` image, version
`20261012.334.1`, and image provisioner `20261012.601`. Both fetched the same 25.9 MB
package set from `http://azure.archive.ubuntu.com/ubuntu`, selected through
`file:/etc/apt/apt-mirrors.txt`. The slow run fetched repository indexes at 6,609 kB/s,
then archives at 50.6 kB/s; the fast comparison fetched archives at 35.4 MB/s. Package
versions match, including `fonts-freefont-ttf`, `fonts-wqy-zenhei`, glib, and NSS.

The slow run progressed through individual packages without `Ign:` or `Err:` lines.
For example, the 5,641 kB FreeFont request at 03:05:57 was followed by the next package
at 03:07:43, while the 7,472 kB Zen Hei request at 03:08:43 was followed by the next at
03:11:10. Those gaps fit the aggregate rate near 50 kB/s. This is evidence of slow
archive transfer, not eight minutes of package unpacking, dependency solving, npm, or
browser assertions. It is consistent with a throttled transfer path; these logs cannot
distinguish a mirror/CDN limit, network shaping, or runner-specific routing.
They do not establish a repository-configured throttle.

Searches of workflows, Makefile, and gate configuration found no `Dl-Limit`,
`Acquire::`, `APT_CONFIG`, proxy setting, or apt retry override.
The local pinned Playwright 1.62.0 implementation invokes plain `apt-get update`, then
`apt-get install -y --no-install-recommends`; it sets no download rate.
The hosted runner’s effective apt configuration was not captured, so an inherited
per-runner setting remains untested.
No environment or secret values were dumped.

The newer [711634 run](https://github.com/jlevy/squares/actions/runs/39895010889),
frontend job `120223294989`, completed combined setup in 13s, 03:27:20–03:27:33. Its
detailed logs and image version were unavailable while active.
This third sample supports variability, but is not a controlled diagnosis or proof of a
fix.

The smallest next engineering change is to apply the existing Pages apt-archive cache
pattern to Packing’s Chromium setup, with a bounded install and per-process durations.
Pages already keys `~/apt-archives` by browser, runner image, and Python lockfile,
retaining downloaded package files while still letting apt resolve required versions.
Packing’s frontend caches only browser binaries and npm downloads.
Add targeted negative controls for install failure and timeout, then measure cold and
warm runs; a cold cache still needs bounded network behavior.
Do not change mirrors or disable system dependency installation based solely on this
sample. No pinned Playwright container or provisioned browser image was found in the
inspected repository workflows; introducing one would be a separate measured toolchain
change.

## Post-Merge Pages Deployment

The
[main Pages run 39896243132](https://github.com/jlevy/squares/actions/runs/39896243132)
published merge `31584003e738ac4d8e0583e053f688db45c66f6c` to
[squaremath.org](https://squaremath.org/). Publication completed about 6m45s after the
run began; the run reached its terminal verdict after 9m16s. Measured critical-path
steps were scope (38s), overview preparation (4m26s), publication assembly (1m12s),
deployment (10s), and live verification (2m33s). Within overview preparation, setup took
36s, two render passes took 2m34s, and two preview-card/head passes took 1m06s. Live
verification included about 50s of setup and browser installation and 1m41s for the
audit itself.
Step and job timing overlap, so these figures are not additive estimates of
total run time.

The
[PR Pages run 39895010919](https://github.com/jlevy/squares/actions/runs/39895010919)
also prepared the overview in 4m29s: two render passes took 2m36s and preview-card/head
passes took 1m05s. The repeated render and card passes are visible work within each run.
A main run still needs evidence for the immutable merge commit and authority to publish;
this comparison alone does not show that promoting the PR artifact would be equivalent.

The main run’s deploy succeeded, but `verify-deployment` failed five navigation checks.
Its checker still sought the full case table on Atlas, while the deployed table is on
Frontier; it also expected the old single Papers navigation marker on four paper pages
that now expose active Learn and Papers states.
The follow-up repair moves the index check to Frontier and parses those states as
elements and attributes.
The public pages were reachable; the failed job was a stale verification contract, not
evidence that publication itself failed.
A local rerun of the repaired checker against the deployed merge completed in 507.51s:
5,245 of 5,245 checks passed, with 950 unique requests and no retries.
That rerun used the navigation repair before its final attribute-order-independent
parser refinement; focused navigation tests passed after that refinement.

## What the Earlier Changes Established

| Change | Delivered result | Why delay remains |
| --- | --- | --- |
| [#724](https://github.com/jlevy/squares/pull/724), merge `ffd0f4af7` | Documents focused local checks before a draft push and hosted full gates. Its basis was 30–65 minutes for local push validation versus a 12.5-minute hosted median. | Documentation only: the PR explicitly changes no workflow, hook, or check. It removes a serial local obligation; it does not shorten hosted execution. |
| [#618](https://github.com/jlevy/squares/pull/618), merge `fc2ceae79` | Quick reachable-test defaults and component-owned release validation. | Its scope improves local/release selection and explicitly leaves ordinary CI’s three-minute objective unresolved. |
| [#620](https://github.com/jlevy/squares/pull/620), merge `4c9af6902` | Removes unsafe cross-run verdict reuse, partitions complete native work, and repairs timing policy. | The PR explicitly claims no controlled runtime improvement. Reusing unrelated green verdicts would undo its provenance repair. |
| [#629](https://github.com/jlevy/squares/pull/629) and [#634](https://github.com/jlevy/squares/pull/634), merge `3685616df` for #634 | Retain timeout evidence and give all forwarder tests required browser ownership and serial isolation. | Coverage and diagnostics repairs preserve work. #634 records a 576.845s site step and explicitly does not claim a three-minute result. |
| [#693](https://github.com/jlevy/squares/pull/693), merge `a5acd5708` | Fixes a captured `Page.close()` race by closing an owned context per forwarder visit. `think-yops` records green main run 39373931375 and a 4,708-check deployed audit. | Removing a specific hang does not eliminate normal rendering or browser assertions. The comparison’s forwarders pass in 59s, while the broader phase still takes 392s. |

## Proposed Work in Priority Order

1. **Attribute and bound Packing setup: `think-9jkf`, child of `think-nnny`.** Retain
   the target run’s final logs, time the two concurrent processes independently, and
   give setup an explicit ceiling with useful partial failure output.
   The existing combined step waits on both processes and has no individual elapsed-time
   report. Compare a pinned provisioned environment or verified minimal system-dependency
   path against `--with-deps`; include cold/warm cost, storage, toolchain identity, and
   failure behavior. The browser cache stores `~/.cache/ms-playwright`, not installed
   system packages. Completed logs establish apt downloads as the 524s observation’s
   dominant cause; the remedy remains to be measured.
2. **Reuse `think-nqnx` for browser fixture work.** It already owns measuring repeated
   canonical rendering and full record admission across xdist processes.
   Its acceptance rule requires three alternating uncontended comparisons, including
   preparation, with at least 30s and 10% inclusive wall reduction and unchanged
   assertions and nodes.
   Profile before implementing shared immutable preparation.
   Preserve private mutable copies and contexts, and fresh reads on the next invocation.
   No duplicate child bead was created; `think-nnny` depends on this existing work.
3. **Reuse `think-fqhc` and coordinate `think-898i` for Pages installation.** The former
   records a roughly 57-minute apt stall in run 39815232525; the latter records an
   unrelated repository’s stale apt metadata failing Firefox installation.
   Both concern setup reliability before tests.
   `think-nnny` depends on `think-fqhc`; consolidate overlapping implementation work
   before claiming either bead.
4. **Measure checkout and scheduling after attribution.** Full history is required for
   some provenance checks.
   The comparison’s 87s checkout warrants measuring which owners require it before
   narrowing fetch scope.
   Any later repartition must prove disjoint, exhaustive ownership and include
   preparation and artifact transfer in its wall measurement.
   `think-qk9w` is the broader existing cache/invalidation work; `think-kxmq` and
   `think-ht59` retain the overall CI objective.

## Test and Process Cleanup

The delegated Astra audit assigns semantic test cleanup to `think-z2sp`, a child of
`think-nnny`. Overview assertions currently lock invitation text, lead-ins, full
sentences, and markup; replace those with parsed nonempty introductions, formal
identity, and canonical destinations.
Filter expectations should use small independent cutoff, date, and supersession fixtures
while retaining real-registry wiring.
Homepage ordering, card counts, and paper slicing need one semantic owner plus browser
alignment and navigation checks.
Contributor assertions should parse destinations and Sources, retaining unsafe-URI
refusals, provenance, and the prohibition on invented identity.
Acceptance requires missing content, wrong links, and boundary errors to fail while copy
edits and corpus growth pass.
Verify current paths and line numbers before editing.

`think-u22w`, also under `think-nnny`, owns reconciling duplicate full-local wording
around development.md line 226 with the focused-local, push, parallel-hosted rule.
It also owns investigating mergeability refresh when the base changes while checks run:
the current branch workflow reacts to pushes and can miss base movement.
These are proposals for a later delivery; no gate or test changes accompany this audit.

## Local Work, Hosted Gates, and Publication

The owner’s requested workflow is focused local validation, then push immediately; full
hosted gates run in parallel with review.
A repeated full local gate before the same hosted gate adds serial latency and does not
demonstrate the remote merge tree.
Ready-for-review and merge still require the correct head’s required hosted checks.
Research checkpoints remain explicit rather than an accidental prerequisite to every
iteration. Follow the
[hosted draft gate rule](../../../development.md#hosted-ci-gates-a-draft-pull-request).

Pages already prepares artifacts for dependent consumers.
Preserve the release guideline’s build-once principle: validate the prepared bytes and
promote those bytes, with separate publication evidence.
Sharing prepared artifacts within an invocation is distinct from suppressing selected
checks using another run’s unauthenticated artifact name.
A final cleanup must report local, PR, post-merge, and deployment costs separately and
identify which repetitions are necessary for changed source identity or publication
authority.

This audit makes no speedup claim and changes no deadline, coverage, assertion,
scientific acceptance rule, or publication requirement.
Proposed implementation belongs in a later PR after the navigation delivery.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
