---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: f-gobel
  display_name: Frits Göbel
  surname: Göbel
  aliases:
  - Göbel
  - Gobel
  - F. Göbel
  - Goebel
  sources:
  - id: primary-byline
    archive_path: packing/resources/papers/gobel-1979-geometrical-packing-and-covering-problems.pdf
    locator: Page 1 title and literal F. GOBEL byline support the retained initial-name alias.
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: Source author, credit and credited_names fields retain the printed attribution labels.
  - id: catalogue-credit
    archive_path: packing/resources/web/kingbird-squares-in-squares.md
    url: https://kingbird.myphotos.cc/packing/squares_in_squares.html
    locator: Entry 65 credits Frits Göbel in early 1979. The bibliography credited_names map prints the same full
      name; the [SQUISH third request 2026-10-09] note explicitly states Goebel is Göbel in the credit’s ASCII spelling.
  provenance:
  - field: /surname
    sources:
    - primary-byline
    - bibliography
  - field: /display_name
    sources:
    - catalogue-credit
    - bibliography
  - field: /aliases
    sources:
    - primary-byline
    - bibliography
    - catalogue-credit
  - field: /real_name
    sources:
    - catalogue-credit
    - bibliography
  real_name: Frits Göbel
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
