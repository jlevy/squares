---
type: is
id: is-01m0vz9s4ffb2vcf7hx5xeacg8
title: SYNOPSIS and conventions say thirty-one gate steps; validate.py now registers thirty-two
kind: bug
status: closed
priority: 2
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0w0c7yd4nabyntb3137stwm
created_at: 2026-08-25T08:06:31.310Z
updated_at: 2026-08-25T08:26:58.050Z
closed_at: 2026-08-25T08:26:58.049Z
close_reason: "Fixed PR #31 finding 1 by removing three duplicated live gate counts and pointing readers to packing-validate --list, the existing authoritative inventory. The dated 31-step checkpoint remains unchanged as a historical measurement."
resolution: null
duplicate_of: null
---
The deterministic SVG rendering merge added `Step("deterministic SVG rendering",
_svg_rendering)` to the `STEPS` tuple in `src/sqpack/cli/validate.py`, which now holds
**32** entries. Two prose counts were not updated with it:

- `SYNOPSIS.md` (“Reading the gate”): “`packing-validate` runs thirty-one steps.”
- `conventions.md` §10: “`packing-validate` runs thirty-one read-only steps
  concurrently…”

`SYNOPSIS.md` also carries “passes all 31 normal-gate steps in 103.91 wall-seconds” in
“Where This Stands”. That one is a *recorded checkpoint measurement*, not a live count,
so it should be left alone or re-dated against a fresh run rather than edited to 32 —
changing a recorded figure to match current code would misreport what was measured.

`conventions.md` §10 already names the right invariant: `STEPS` in
`src/sqpack/cli/validate.py` “is the only registration point”, and `packing-validate
--list` “prints the authoritative names and tiers”.
Both prose counts restate a value the code owns, which is why they drifted.

Two questions worth deciding together with the fix:

1. **Should the prose carry the number at all?** Three documents restate it — the two
   above plus `TUTORIAL.md`, which says thirty and is tracked as TR-1 of
   `review-2026-08-25-tutorial-pedagogy-and-accuracy.md`. A count restated in three
   places will drift again.
2. **Should `devtools.check_synopsis` enforce it?** The gate has a `synopsis agrees with
   the artifacts` step and it did not catch this, which is consistent with the
   repository's own standing observation that no soundness defect in the log was caught
   by the gate. If the number stays in prose, deriving or checking it against
   `len(STEPS)` is cheap.

Not a soundness defect — nothing mathematical depends on it — but it is exactly the
shape of record drift the defect log exists to track, so it may warrant a `D-NNN` rather
than only a bead. That call belongs with whoever fixes it.

## Notes

PR #31 review finding 1 at TUTORIAL.md:433, SYNOPSIS.md:479, and conventions.md:332 confirms the live gate count drift after the SVG merge. Prefer removing duplicated live counts and pointing to packing-validate --list; leave the dated 31-step checkpoint unchanged.
