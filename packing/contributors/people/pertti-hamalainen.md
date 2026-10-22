---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: pertti-hamalainen
  display_name: Pertti Hämäläinen
  surname: Hämäläinen
  real_name: Pertti Hämäläinen
  aliases:
  - Hämäläinen
  sources:
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: 'Entry 18: Found by Pertti Hämäläinen in 1980; the pictured alternative with minimal rotated squares
      is credited separately to Mats Gustafsson in 1981.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: credited_names maps Pertti Hämäläinen to Hämäläinen; bibliography source notes preserve the catalogue
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
