---
type: is
id: is-01m0w07k24sv5nc6hzacmc6tjt
title: "TUTORIAL: make the new assurance vocabulary self-consistent with the witness schema"
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T08:22:48.132Z
updated_at: 2026-08-25T08:29:43.781Z
closed_at: 2026-08-25T08:29:43.781Z
close_reason: "Implemented in TUTORIAL.md on claude/packing-tutorial-review-r2p25t (82c68dc), on top of the SVG toolkit and the #31 frontier-assurance branch. Notation card (new §10) and vocabulary card rebuilt; the LP written out with an on-ramp; the quench's two loops described with the path-dependence reason; precision costs, latency budgets and the 1e-11 cause added; the primitive element theorem answered; §11 further reading and arithmetic inventory added; assurance and method tokens aligned to witnesses/witness.schema.yaml; accuracy fixes applied. TR-2 needed no work — #31 had already replaced the superseded absolute. The restated gate step count was removed rather than corrected, so it cannot drift a fourth time; the status-document half stays open as think-4b9m."
resolution: null
duplicate_of: null
---
Review finding TR-15.

PR #31 migrated `TUTORIAL.md` off the three evidence tiers (`f64_screen`, `polished`,
`exact`) and onto an assurance/method/precision split.
The migration is complete — no tier language survives in the document — and the split is
a real improvement, particularly "A numerical result remains numerical at tolerance
`1e-100`", which closes what this review had filed as its own finding under think-i22v.

Three token-level inconsistencies arrived with it.
Canonical values are the schema enums in `witnesses/witness.schema.yaml`:

- assurance: `reported | numerically-checked | verified`
- method: `numerical-f64 | numerical-multiprecision | interval-certified | exact-algebraic`

**1. §9's vocabulary card drops the hyphen.** It renders the middle assurance value as
`` `numerically checked` ``; §5's table and the schema both use `numerically-checked`.
Its two neighbours in the same cell are exact enum values, so the middle one reads as
one too.

**2. §8 mixes registers inside one table.** The corner row is annotated
`` numerically checked (`numerical-f64`) `` and the row directly below it is
`numerically checked (floating LP)`. `floating LP` is not one of the four method values.

**3. Two method tokens are used before being introduced.** §5 tokenizes only
`numerical-f64` and `numerical-multiprecision`, then describes the formal side in prose
("exact algebraic replay, rigorous interval certification, and scoped proof").
§8 then uses `` `exact-algebraic` `` five times as a token, and `interval-certified`
never appears at all. Listing all four values in §5 makes the table self-contained and
removes a fresh instance of the think-8hdt problem — a token a reader meets without a
definition.

All three are raised on the originating PR as well:
https://github.com/jlevy/thinking-scratchpad/pull/31#issuecomment-5407514755
They are tracked here because they are `TUTORIAL.md` edits whichever branch makes them.

**Checked and withdrawn**, recorded so they are not re-raised:

- §6's "The retained Schadt `n = 29` decimal pose is numerically checked at 300 digits
  and tolerance `1e-100`" is correct. It looked like it was promoting the witness file's
  `claim.assurance: reported`, but `E-n029-schadt-numerical` in `frontier/evidence.yaml`
  carries `assurance: numerically-checked`, `performed_by: repository`, and
  `replay_status: passed` at exactly those parameters, distinct from the source's
  `E-n029-schadt-report`.
- The three `n = 29` side values across `frontier/n-029.md` and the witnesses are three
  different objects — reported upper bound, the decimal pose's own side, and a
  deliberately weaker rational `verified_upper_bound` — not a divergence.
