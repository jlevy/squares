---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: robert-wainwright
  display_name: Robert Wainwright
  surname: Wainwright
  real_name: Robert Wainwright
  aliases:
  - Wainwright
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 19: Found first by Robert Wainwright in late 1979; based on packing found by Charles F. Cottingham
      in early 1979.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Robert Wainwright to Wainwright; bibliography source notes preserve the catalogue
      credit context.
  provenance:
  - field: /display_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /surname
    sources:
    - catalogue-credit
    - bibliography
  - field: /real_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /aliases
    sources:
    - catalogue-credit
    - bibliography
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
