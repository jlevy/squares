---
type: is
id: is-01m1sj3bd92ye5hrffxr5cw530
title: "Print: a page break can land right after a section heading"
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-05T19:53:02.121Z
updated_at: 2026-09-05T20:39:14.157Z
closed_at: 2026-09-05T20:39:14.157Z
close_reason: "Diagnosed and fixed, but not where the report pointed. No heading is stranded: kpress's break-after: avoid matches all thirteen and was proved load-bearing. Forcing the atlas onto its own page is a no-op, it is already there, and twelve of thirteen printed pages come out byte-identical. The real defect was kpress dropping only the inline half of the page shell's gutter in print; the block half survived onto the @page margin. Fixed upstream in jlevy/kpress squares/page-fixes 3eada69: 13 pages to 12, premature whitespace 25.51in to 17.58in."
resolution: null
duplicate_of: null
---
Headings need break-after: avoid (and orphans/widows handling) so a heading is never the last thing on a page. This belongs in kpress's print stylesheet rather than in the explainer's shell; kpress is vendored at vendor/kpress on branch squares/page-fixes, so the fix is a PR there. Check whether kpress already sets it and, if so, why it is not taking effect for this page.

## Notes

MEASURED: zero stranded headings in the 14-page print, across three deterministic runs and two independent extractors. kpress's rule (print.css 80-90) is correct, matches all 13 headings, is not overridden, and is load-bearing: neutralising it with !important produces one strand immediately. Chromium honours break-after: avoid, including when the next block is a break-inside: avoid figure taller than a page (0 strands across 20 spacer x height cells). The real defect is premature whitespace: pages 2, 6, 8 and 10 end 7.93in, 6.69in, 5.95in and 3.53in short, 32.94in total, because the next figure is break-inside: avoid and too tall for the space left. A heading plus one short paragraph followed by eight inches of nothing reads as a break after the header. Fix is the figure caps in explainer-shell.html: img 7in->6in and canvas 5.4in->4.5in takes whitespace 32.94in->17.58in and 14 pages->12. 6in is the threshold; 6.25 and 6.5 leave page 2 unchanged. kpress's own gap is a missing size guard beside its figure break-inside rule, not a heading rule.
