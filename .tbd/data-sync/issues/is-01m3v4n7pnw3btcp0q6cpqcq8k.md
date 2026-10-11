---
type: is
id: is-01m3v4n7pnw3btcp0q6cpqcq8k
title: Classify every result by kind (lower bound, upper bound, optimality, simplification, …) and retire the 'not a bound' tag
kind: feature
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:08:00.595Z
updated_at: 2026-10-01T17:12:07.438Z
closed_at: 2026-10-01T17:12:07.437Z
close_reason: "Merged with jlevy/squares#270 (main 7f1ad844e, 2026-10-01): kind on every result, checked; kind chip and Kind filter on the site; 'not a bound' retired. Open with the owner: the ten medium-confidence classifications and whether standing derives from kind for T-003, T-004, T-005, T-054, T-055."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'I also had asked for a bead around classifying all the results as lower bound or upper bound or optimality or simplification or possibly others. It shouldn't block this work but it's an important refinement. We should not have a tag "not a bound" as that is too vague.' The original bead was never synced from the cloud sandbox. Scope: (1) a required kind on every entry of packing/frontier/results.yaml, with a closed vocabulary in the schema: lower bound, upper bound, optimality (an exact value settled), simplification (a shorter or cleaner proof or certificate of a known result), and whatever else the 61 entries actually need, each named for what it is (for example rigidity or local isolation, case exclusion, erratum or correction, second certificate, audit); propose the vocabulary from the register and have the owner confirm it. (2) check_results enforces it, and derives or cross-checks it against the claim where it can. (3) The standing 'not a bound' (render_recent_results, overview_sections.NOT_A_BOUND_LABEL, the all-results prose, paper-design.md) is retired: a result that is not a bound shows its kind instead. (4) The site shows the kind as a chip or column and filters by it in the shared filter bar; RESULTS.md groups or labels by it. A separate PR after the website, ladder and prose-cleanup PRs, since all of them edit results.yaml; not blocking.

## Notes

jlevy/squares#270 at a4eebc8e4, stacked on #271, hosted run green, marked ready by the owner 2026-10-01. Site part done: a kind chip under the rungs, a Kind filter (preset ?kind=…), the popover shows kind; nine results have no standing. Open with the owner: whether standing should be derived from kind for the five non-bound kinds that cite a bound's evidence (T-003, T-004, T-005, T-054, T-055; decision 5 in the plan); the ten medium-confidence classifications. Case pages' result lists still show rungs only.
