---
type: is
id: is-01m4h9p81sxyd6k2dwx7zgh1g7
title: Take Evan Daniel's Lean closed forms for 62 quadratic register sides (7d047a9) as evidence for T-120..T-124
kind: task
status: open
priority: 3
version: 5
delegate: null
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T21:39:14.104Z
updated_at: 2026-10-31T20:15:07.509Z
started_at: 2026-10-31T20:02:09.396Z
---
evand/square-packing 7d047a9 gives Lean closed forms a + b*sqrt(d) for 62 quadratic register sides; ed01e0d says an issue is drafted. Import as evidence for T-120..T-124 when the issue arrives.

## Notes

## 2026-10-12: T-124 is #420's, not a fifth #419 form (review A on #531, A5)

The #419 forms this bead takes evidence for are T-120 to T-123. T-124 is #420's "178 source configurations are reported non-strict local minima" (result-requests.yaml #420 local-minima-178), which the Lean binding also bears on. The #419 follow-up of 12 October (https://github.com/jlevy/squares/issues/419#issuecomment-6119246619) said "Of the four forms registered from this issue ... T-120 to T-124 stay at V0/C0", copying the range the record's lean-packs-binding-2026-10-11 text and this bead's title used. The record now reads "the forms this entry maps, T-120 to T-123 and the retained catalogue, and of #420's T-124" (#531, commit a4a8a7d05).

**The next #419 reply says "T-120 to T-123, and #420's T-124"** wherever it names the range. No correction reply is posted for this alone; the rungs the 12 October reply stated are right (T-124 is V0/C0 in results.yaml).

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): existing issue https://github.com/jlevy/squares/issues/419 states the remaining work (reply https://github.com/jlevy/squares/issues/419#issuecomment-6119246619: 2.1 process-hours for 41 counts, 10.3 for 258, no build yet); the build budget is on https://github.com/jlevy/squares/issues/543. Tracker https://github.com/jlevy/squares/issues/544.

2026-10-31 bold-ritchie-l10 (intake lane L10, epic think-3guf; branch claude/bold-ritchie-xo28us-l10): **the Lean build cannot run in this environment, stopped.** No build ran; nothing was retained.

What the build needs, read at the pin through raw.githubusercontent.com (HTTP 200 each): evand/square-packing 6bbae379d23bd4a1d893f33fb254489eeb2cc3c0 `lean/lean-toolchain` = `leanprover/lean4:v4.33.1`; `lean/lakefile.toml` requires mathlib `rev = "v4.33.1"`; `lean/lake-manifest.json` pins mathlib 0df444a360eaa60ab8c11dca51a86af692955474 (with plausible, LeanSearchClient, importGraph, proofwidgets, aesop, Qq, batteries, Cli); `lean/Sqpack/Spec.lean` begins `import Mathlib`, and every Packs module reaches it.

Probes from this session's agent proxy, 2026-10-31 about 20:15Z (HEAD requests; `curl -sS -I -L`):
- Toolchain: fetchable. https://github.com/leanprover/elan/releases/download/v4.1.2/elan-x86_64-unknown-linux-gnu.tar.gz and https://github.com/leanprover/lean4/releases/download/v4.33.1/lean-4.33.1-linux.tar.zst both answer 200 after one redirect to release-assets.githubusercontent.com. https://releases.lean-lang.org/lean4/v4.33.1/lean-4.33.1-linux.tar.zst: `curl: (56) CONNECT tunnel failed, response 403`.
- Mathlib cache: **refused.** Mathlib 0df444a3's `lake exe cache get` downloads only from `https://lakecache.blob.core.windows.net/{container}` (Cache/Infra.lean lines 102-103, `azureURL`; override only by `MATHLIB_CACHE_GET_URL` or `--cache-from`, and no other reachable mirror is known). https://lakecache.blob.core.windows.net/mathlib4/: `curl: (56) CONNECT tunnel failed, response 403`; the proxy status lists it as connect_rejected ("the egress proxy refused the connection ... the host is not allowed for this session").
- Mathlib source: `git ls-remote https://github.com/leanprover-community/mathlib4 refs/tags/v4.33.1` answers 0df444a360eaa60ab8c11dca51a86af692955474, so lake's git clones would pass; https://github.com/leanprover-community/mathlib4/archive/0df444a3....tar.gz answers 403. Without the cache, `import Mathlib` means building all of Mathlib from source here, far beyond the 2.1 process-hours priced for the 41 modules and not priced by this lane.
- Disk: 4.6 GB free on / (df -h, 20:13Z), against the 9 to 10 GB the evand-k2-minus-c-lean-2026-10-18 and evand-rect-small-n-lean-2026-10-22 packets give for the toolchain and Mathlib 0df444a3's cache.

Route that would work: a host that reaches lakecache.blob.core.windows.net with about 10 GB free (or a fork-dispatched Actions run, as #543's D6 says for n = 11), then the packet at 6bbae37 and `lake exe cache get && lake build` of the 41 modules with the axiom receipt.

**The 41 counts re-measured against main 737d8311e** (each count's `reported_upper_bound` and `verified_upper_bound` read from packing/frontier/n-NNN.md):
- The quadratic form is no longer the house at 8: 176 (Mishapolk KKT refinements 2026-10-14), 204 (Daniel #845, adopted in #852), 227 and 229 (Daniel regularized lists 2026-10-20), 232 (Couzo #844, adopted in #852), 260 (Daniel #845, adopted in #852), 264 (Mishapolk KKT refinements 2026-10-14) and 299 (Daniel n299 update 2026-10-29). Their verified bound is that smaller packing's exact feasibility; the Lean proof there would bind a packing that is no longer the record.
- At the other 33 the house is still the Kingbird quadratic form and the verified bound a rational above it. 19 still rest on E-evand-exact-ceilings-2026-10-05-*: 104, 109, 125, 149, 150, 151, 170, 174, 201, 202, 203, 231, 233, 234, 257, 262, 265, 296, 298. 14 now rest on the regularized-bounds exact decisions (E-regularized-bounds-2026-10-12-exact-decision, at 290 E-regularized-bounds-2026-10-13-grid-slack-exact-decision): 53, 101, 122, 124, 145, 147, 148, 173, 197, 200, 226, 290, 291, 294.
So the ask (#419, 11 October) now bears on 33 counts, not 41. The claim is released back to open.
