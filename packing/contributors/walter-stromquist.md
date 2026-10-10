---
softschema:
  contract: packing.squares:Contributor/v1
  schema: contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: walter-stromquist
  display_name: Walter Stromquist
  real_name: Walter Stromquist
  aliases: [Stromquist]
  sources:
    - id: paper-byline
      archive_path: packing/resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md
      url: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8
      locator: Author byline, title, venue and year at the beginning of the paper transcription.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: The [Stromquist 2003] entry credits Stromquist in volume 10, article R8.
  provenance:
    - field: /display_name
      sources: [paper-byline]
    - field: /real_name
      sources: [paper-byline]
    - field: /aliases/0
      sources: [bibliography]
  bio_sources: [paper-byline]
---
Walter Stromquist wrote “Packing 10 or 11 Unit Squares in a Square,” published in The
Electronic Journal of Combinatorics in 2003.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
