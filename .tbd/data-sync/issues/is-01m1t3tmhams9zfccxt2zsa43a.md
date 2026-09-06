---
type: is
id: is-01m1t3tmhams9zfccxt2zsa43a
title: "Explainer PDF: Chromium doubles four outline titles"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T01:02:50.922Z
updated_at: 2026-09-06T01:02:50.922Z
---
Measured 2026-09-06. With tagged and outline both set, the PDF gets 13 bookmarks and four of them are doubled: 'Packing 11 SquaresPacking 11 Squares', 'The Five ConditionsThe Five Conditions', 'From a Continuum of Angles to 181From a Continuum of Angles to 181', 'Generator and VerifierGenerator and Verifier'.

Those are exactly the four headings that begin a page. Re-rendered at a different margin, giving a different pagination, the doubled SET CHANGES -- so it is a fragmentation bug in Chromium's outline generator and not the markup. Confirmed clean upstream: the source h2 elements are single, and the structure tree has exactly 12 H2 entries with no duplicates.

Fix: one pikepdf pass over the outline after export -- for each title, if the string is an exact doubling s+s, halve it. That would also be the place to set /Author and /Subject, which Chromium cannot set and for which it emits no XMP.

Not done now because it adds a PDF library to the dependency set for a cosmetic defect in the navigation pane, and the dependency question deserves its own decision rather than riding along.
