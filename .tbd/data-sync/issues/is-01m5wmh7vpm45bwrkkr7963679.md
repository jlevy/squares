---
type: is
id: is-01m5wmh7vpm45bwrkkr7963679
title: Redraw the assets and move their records with them
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
created_at: 2026-10-26T17:36:04.982Z
updated_at: 2026-10-26T18:26:08.103Z
---
Apply the rule, redraw and re-measure.

- Redraw both poster families and every advertised export
  (`development.md`, "Release assets are drawn at their component's version bump").
- Move the retained composite descriptions in `build_known_best_atlas` with the drawing:
  they are prose a reviewer reads against it, and they name the address today.
- Re-measure the print layout. A changed line shifts baselines and ink bounds, which
  `check_print_layout` and the poster records hold.
- Take the release-impact decision for the infographic family rather than a
  no-public-change record: both families and every advertised export advance together,
  and this changes what the asset prints.
- Verify the PDFs by reading them, not by trusting the generator.

Depends on the rule bead.

## Notes

## Why this did not ride with PR #837, 26 October 2026

The generator change is four literals and was written and reverted on that branch; what
stops it is the redraw, not the strings.

`build_known_best_atlas --check-composites` on main at `002e3a188c47` reports that
`known-best-1-324.svg` was drawn at `v0.7.0-79926e`, data of 23 October, and that the pin
has since moved: the drawing trails the record in five cards.

```
n=31  lower-bound  s(31) ≥ 5.95250  → 5.97750
n=182 side-bound   s(182) ≤ 13.97410 → 13.97092
n=268 side-bound   s(268) ≤ 16.87882 → 16.87437
n=303 side-bound   s(303) ≤ 17.90978 → 17.90698
n=304 side-bound   s(304) ≤ 17.92943 → 17.92690
```

Those five fail nothing today, because a poster may trail the data between bumps. But the
address line can only be redrawn at a bump, and a bump redraws the whole family, so a cut
made for the address carries the five bound changes with it. That is the owner's call
about what the next infographic edition says, not a side effect of a wording fix.

So the cut is deliberate work:

```bash
uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.7.1 \
    --component infographics --impact patch --scope "..."
```

`--update-composites` refuses a stale pin and an uncommitted tree, and the family is about
106 MB of retained SVG, PNG and PDF with digest receipts, so the redraw is the expensive
half. Confirm the scope line with the owner before cutting, and say in it that the
edition carries both the address line and the five moved cards.

The colophon half of think-1zuf shipped in PR #837: every page's footer and all four
papers' HTML and PDFs now read "The Squares Project · squaremath.org ·
github.com/jlevy/squares".
