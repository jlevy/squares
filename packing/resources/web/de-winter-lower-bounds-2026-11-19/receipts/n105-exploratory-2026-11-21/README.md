# n105 Exploratory Native Replay, 21 November 2026

The coordinator replayed the first archived direction at each of n105’s four angular
levels through `devtools.replay_rectangle_receipts`, using the author’s pinned octagon
kernel. All four originals passed and matched the archived node, leaf and least-bound
values. All four quarter-mass controls returned `UNDECIDED` with an unresolved box after
65 nodes. These are exploratory **same-implementation** results on Apple Clang 21 and
Darwin arm64; they confer no verification or confirmation rung.

The selected `(K, r)` pairs are `(160, 0)`, `(480, 98)`, `(1440, 860)` and
`(4320, 4250)`. Full coverage requires 273 archived directions.
The 99/100 control, source-measure premises and independent review remain outstanding.

[Input custody](input-custody.json) records eight gzip payloads, 198,560 bytes,
recovered from JoostdeWinter/square-packing at
`21d944c43098e2261ab7d713cd10f02a5eb13f3d`. Lengths and digests match the retained
acquisition record and [certificate manifest](input-manifest.json).
Its `source_programs_executed: false` describes acquisition; these native runs occurred
afterward.

The landed wrapper validates five producer files before import, stages their checked
bytes and checks receipt source identity before compilation.
It used `c++ -O3 -std=c++17`, selecting Apple Clang 21.0.0 on
`arm64-apple-darwin25.5.0`, with unedited source.
The [host declaration](host.txt) records one worker, cap 2,100,000 and a 600-second wall
ceiling. This host/compiler differs from the [control plan’s](../controls-plan.txt) GCC
13.3.0 environment.

| Run | Approximate native CPU seconds | Timed wall seconds | Timed user + system CPU seconds |
| --- | ---: | ---: | ---: |
| Original | 2.825 | 12.34 | 4.47 |
| Quarter | 0.080 | 1.76 | 1.48 |

Native figures sum the receipt fields; timed invocations include compilation and wrapper
work. Exact [original](original.jsonl) and [quarter](quarter.jsonl) outputs and
[original](original.validation.log) and [quarter](quarter.validation.log) timing logs
are unchanged. Originals report exit 0, `verified: true`, `matches_archive: true` and
least bounds at least `2^48`. Controls report exit 1 and unresolved coverage, with 260
nodes total, below the cap; the driver’s exit alone does not establish this.

Both guards recorded `authority: full` and actual swap-headroom interventions.
The original run had two pauses and two resumes, with 18.4 seconds paused over a
24.7-second watch; the quarter run had one pause and one resume, with 9.2 seconds paused
over 12.4 seconds. Neither guard killed or aborted a process.
Full guard journals and stderr remain in external session scratch.
Sampled pressure stayed at level 1, with about 1.64–1.65 GB free on the swap volume.
Watcher and timed-invocation intervals differ; do not subtract them or treat these wall
times as an undisturbed performance baseline.

The sample changes no frontier value, registration or adoption.
It does not replace original-archive premise verification or claim a replay of #1039.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
