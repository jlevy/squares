---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: anna-slivkova
  display_name: Anna Slivková
  surname: Slivková
  real_name: Anna Slivková
  aliases:
  - Slivková
  sources:
  - id: paper-byline
    archive_path: packing/resources/papers/basic-slivkova-2018-optimal-piercing-square.raw.md
    locator: The opening author byline names Anna Slivková, with accents encoded as separate glyphs
      in the PDF text extraction.
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The [Basic-Slivkova 2018] entry lists Slivková as the second author, matching the retained
      paper byline.
  provenance:
  - field: /display_name
    sources:
    - paper-byline
  - field: /real_name
    sources:
    - paper-byline
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
    - paper-byline
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
