---
type: is
id: is-01m2ckqtz9kp5ra8ev43r545v5
title: "D-490: two new occurrences, one naming a link rectangle that moved 5.25pt"
kind: bug
status: open
priority: 2
version: 2
labels:
  - n11
  - research-tooling
dependencies: []
created_at: 2026-09-13T05:27:16.199Z
updated_at: 2026-09-13T07:10:55.344Z
---
D-490's record says 'Another occurrence must preserve the new location report before any hypothesis can be selected.' PR 157 produced two, on the same commit 74e4d653, in runs 34717875498 (original and re-run). Both predate the _difference hardening on PR 149, so treat the OBJECT ATTRIBUTION as unreliable -- that is the header-matching bug those commits fixed -- but the quoted byte windows come straight from the two renders and stand on their own.

Occurrence A: 839866 then 839866 normalised, length delta 0, attributed to object 152, differing in binary stream bytes. Consistent with a compressed stream (font subset or image) built differently at identical length.

Occurrence B is the informative one: 839457 then 839866, length delta 409, attributed to object 159 as a Link, and the quoted windows differ inside a /Rect:
  b' 0]\n/Rect [474.73953 537.0047 496.48898 553.5047]\n/A <</Type /Ac'
  b' 0]\n/Rect [474.73953 537.0047 491.23911 553.5047]\n/A <</Type /Ac'
Same left edge, same top and bottom, right edge 496.48898 against 491.23911 -- a link annotation 5.25pt narrower in one render than the other. That is a TEXT MEASUREMENT difference, not content going missing: the linked run of text was laid out at two different widths in one process, one page, one moment. A face that had not applied when the draw was taken would produce exactly this, since fallback metrics give a different advance width.

Note this corrects a reading I posted publicly on PR 157 (issuecomment-5648627182), where I characterised the shorter render as 'something intermittently absent'. The evidence is sharper and different in kind: nothing is absent, a measurement differs. The same over-reading is what the PR 149 commits fixed in the diagnostic itself, which now declines to infer truncation from an exact prefix.

The 409-byte length delta is then downstream of layout rather than a cause: annotation rectangles, content-stream positions and the cross-reference offsets that follow all shift when one text run measures differently.

Whether that is enough to select a hypothesis is the defect owner's call, not this bead's. What this bead supplies is the occurrence data the record asked for, plus the caveat that both reports came from the pre-fix locator.

## Notes

Follow-up 2026-09-13T07:10Z: the PR 149 fix landed, and it targets this bead's mechanism directly.

Commits 0fd04d5f ("validate the PDF publication artifact end to end") and 8d0a3ff2 ("preserve PDF diagnostics before rerunning CI") split render_explainer_pdf.check() into _check_renders / check / check_artifact, and add packing/tests/test_pdf_math_browser.py -- real browser controls gated behind SQPACK_PDF_MATH_BROWSER=1 that inject a genuinely invalid FontFace and a real FontFaceSet.load timeout, leaving the actual KPress runtime, host fallback, export waits and final DOM guard in use rather than substituting a synthetic rejection.

The part that bears on occurrence B: per development.md as amended, the exporter now checks that visible math is typeset BEFORE drawing PDF bytes, and a completed font-error fallback that exposes literal TeX fails that check. Occurrence B's hypothesis was precisely that a face which had not applied at draw time yields fallback advance widths, hence the 5.25pt narrower /Rect. The new guard is the control for that hypothesis.

Two things this does NOT establish, and they should not be conflated:
1. It does not confirm occurrence B's cause. It installs a check that would catch one candidate mechanism. Whether the guard actually fires on a recurrence is the evidence, and it has not been observed firing.
2. It does not retroactively repair the object attribution in either occurrence. Both reports still predate the _difference hardening, so the object numbers (152, 159) remain unreliable; the quoted byte windows still stand on their own.

Status for the defect owner: the occurrence data this bead was asked to supply is unchanged, and there is now a mechanism-specific guard upstream of it. Selecting a hypothesis remains the owner's call.
