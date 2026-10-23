---
type: is
id: is-01m5kcqwe1tdkhh4aemhnzjt19
title: Attribute and bound Packing frontend setup before choosing browser provisioning
kind: task
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: ci-followups
labels: []
dependencies: []
parent_id: is-01m5kcfhfdmgfb03gn3drg43rc
hold: null
hold_until: null
created_at: 2026-10-23T03:26:44.149Z
updated_at: 2026-10-23T04:48:51.474Z
started_at: 2026-10-23T03:32:14.482Z
---
Packing run39892772106 frontend job120216469741 at bf38442f248d089b9862d04ee0658f85b51d7b0c spent524s in combined concurrent npm/Playwright setup (03:03:58-03:12:42 UTC). Comparison39893731935 job120219204931 spent16s; npm and Playwright browser caches hit, npm took1s while apt still updated/downloaded. Current logs unavailable during audit, so npm versus apt attribution is unknown. Retain final logs; add separate process timings, explicit setup ceilings and useful failure output in project-native tooling. Compare a pinned provisioned environment or minimal verified system-dependency path with current --with-deps, including cold/warm cost and storage. Preserve locked inputs, disabled npm scripts, all browser assertions and least privilege. No speedup accepted from one runner observation. Coordinate Pages-specific existing think-fqhc and think-898i; ordinary browser fixture optimization already belongs to think-nqnx. Deliver measured proposal before workflow implementation.

## Notes

Confirmed logs: old run39892772106 job120216469741 npm96packages2s; apt25.9MB8m32s50.6kB/s. Comparison39893731935 job120219204931 same ubuntu24.04 image20261012.334.1/provisioner20261012.601, same archive mirror azure.archive.ubuntu.com and package versions, archive transfer1s35.4MB/s. Slow indexes6609kB/s then packages near50kB/s, no Ign/Err; consistent with transfer throttling but mirror/CDN versus runner route/host shaping unproved. Repository/workflow search and pinned Playwright1.62 implementation show no Dl-Limit/Acquire/APT_CONFIG/proxy/retry overrides; hosted effective apt config not captured. Current711634 run39895010889 setup13s byAPI; detailed image/log unavailable while active. Smallest proposal: reuse existing Pages image+lock-keyed apt archive cache for Chromium, bound install, report separate process times, failure/timeout controls, cold/warm measurement. Existing binary cache does not cache system packages. No pinned browser container found; provisioned image is separate scope. Full durable evidence /Volumes/spud-ext2/agent-notes/squares/review-2026-10-22-ci-release-latency.md. No implementation or speedup claim.

2026-10-23 implementation and hosted observations for PR #743 (https://github.com/jlevy/squares/pull/743), included in commit 020c7f73111c4c083e0cc21466ccea53668cec8d:

Packing now reuses Pages' browser/image/lockfile apt archive cache. The native browser_setup helper preserves npm ci --ignore-scripts and pinned Playwright --with-deps --only-shell Chromium, concurrent installers, 180-second process ceilings and a four-minute workflow ceiling, logs/JSON receipts, and owned-process cleanup. Only known Azure Ubuntu archive URL tokens are promoted to the runner's existing canonical HTTPS alternative; unknown entries, security mirrors, priorities, suites, components and archive verification remain intact. The exact runner image already declares canonical HTTPS at priority 2: https://github.com/actions/runner-images/blob/ubuntu24/20261012.334/images/ubuntu/scripts/build/configure-apt-sources.sh . Focused setup tests: 10 passed, lint/types clean. Tutorial tests were admitted from a complete successful module run and assigned required-Chromium frontend ownership.

Completed head d92602eca956c9ac765b629f8ed7395cbee8663d, Packing run 39899655598, frontend job 120238434209 (https://github.com/jlevy/squares/actions/runs/39899655598/job/120238434209): setup passed in 18s by API timestamps, 04:21:18–04:21:36 UTC. Apt archive cache was cold (0 packages/0 bytes). Playwright reported 17.18s, exit 0, no timeout; npm reported 2.33s, exit 0. Canonical HTTPS fetched the same 25.9 MB in 3s (7,436 kB/s). Initial bounded Azure/cold run 39897971993 at c278006b391f6879f5b0d65ef84a816a5f9f6c20 reached its 180s ceiling while downloading fonts; npm took 1.57s. Older unbounded slow setup was 524s. These observations are not a controlled or universal speedup: the original workflow also had healthy 13s setup at head 7116343d2630096bb2901165c0933fadd1e645e8, run 39895010889. No warm-cache benefit is claimed.

The same d92602ec frontend step passed in 705s by API timestamps, 04:21:36–04:33:21 UTC. Native site-layout wall was 702.06s: 508 passed/6 skipped in the parallel phase (539.97s), 74 forwarders passed (117.56s), and 4 HTTP cases passed (42.23s). Workbench behavior (190.01s), browser floor (120.47s), and browser liveness (45.14s) overlapped and must not be summed. Thus healthy bounded setup does not solve the remaining roughly 11m45s browser workload: existing think-nqnx still owns browser fixture optimization; think-ht59 retains the broader CI objective and timing-policy work. No three-minute end-to-end result is claimed. This frontend was green while other jobs failed separate functional checks; replacement head 020c7f731 awaits its own terminal verdict.

Second completed setup observation, head 020c7f73111c4c083e0cc21466ccea53668cec8d, Packing run 39901015355, frontend job 120242352990 (https://github.com/jlevy/squares/actions/runs/39901015355/job/120242352990): setup passed in 14s by API timestamps (04:35:03–04:35:17 UTC). This time the image/lock-keyed apt cache hit with 17 packages/25,937,806 bytes. Playwright reported 14.06s, npm 1.24s, both exit 0/no timeout; apt needed 0 B/25.9 MB of archives, while still fetching 12.5 MB of metadata in 4s. This verifies archive reuse while retaining dependency installation. It is not a controlled claim about the four-second difference from the cold run.

The same frontend validation passed in 448s by API timestamps (04:35:17–04:42:45 UTC), native site-layout wall 445.51s: parallel phase 508 passed/6 skipped in 341.07s, 74 forwarders in 73.55s, four HTTP cases in 28.99s. The variation from the previous 705s observation is not attributed to this setup fix. Existing think-nqnx/think-ht59 retain the browser/end-to-end runtime work. All non-Pages CI passed at this head; Pages identified only the two new tutorial SVGs missing asset registration. That separate registry repair is committed in 739e283b6921d576a96c595ecd4d139c33e96c39 and tracked by closed think-nr8l; final-head CI remains in progress.
