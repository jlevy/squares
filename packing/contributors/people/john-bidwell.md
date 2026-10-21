---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: john-bidwell
  display_name: John Bidwell
  surname: Bidwell
  real_name: John Bidwell
  aliases: [Bidwell]
  sources:
    - id: survey-credit
      archive_path: packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
      url: https://erich-friedman.github.io/papers/squares/squares.html
      locator: 'Erich Friedman’s DS7 survey, the section on 17 and 29 squares: “in 1998, John Bidwell, an undergraduate student at the University of Hawaii, improved this packing”; the n = 17 table row credits Bidwell; reference [1] is “J. Bidwell, 1998, private communication.”'
    - id: catalogue-credit
      archive_path: packing/resources/web/kingbird-squares-in-squares.md
      url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
      locator: 'Entry 17: the degree-18 polynomial for s, then “Found by John Bidwell in 1998. Based on packing found by Pertti Hämäläinen in 1980.”'
    - id: picture-credits
      archive_path: packing/resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json
      locator: 'The n = 17 credits read from the catalogue SVG: “Found by John Bidwell (an undergraduate student at the University of Hawaii) in 1997 or 1998” and “Source: Private communication between Erich Friedman and John Bidwell, 1998”.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'credited_names maps John Bidwell to Bidwell; the [Chang n83 2026-09-24] credit names Bidwell from the catalogue line “Extends the s(17) found by John Bidwell in 1998”.'
  provenance:
    - field: /surname
      sources: [survey-credit, bibliography]
    - field: /display_name
      sources: [survey-credit, catalogue-credit, picture-credits]
    - field: /real_name
      sources: [survey-credit, catalogue-credit]
    - field: /aliases/0
      sources: [survey-credit, bibliography]
  bio_sources: [survey-credit, catalogue-credit]
---
John Bidwell found the 17-square packing in 1998 while an undergraduate at the
University of Hawaii.
He also improved a packing of 29 squares.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
