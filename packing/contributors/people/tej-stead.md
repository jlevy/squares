---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: tej-stead
  display_name: Tej Stead
  surname: Stead
  real_name: Tej Stead
  aliases:
  - Stead
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: Multiple packing entries explicitly credit refinements or optimization to Tej Stead
      in June 2026.
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names explicitly maps Tej Stead to Stead.
  provenance:
  - field: /display_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /real_name
    sources:
    - catalogue-credit
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
