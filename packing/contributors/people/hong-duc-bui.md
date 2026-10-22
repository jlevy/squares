---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: hong-duc-bui
  display_name: Hong Duc Bui
  surname: Bui
  real_name: Hong Duc Bui
  aliases:
  - Bui
  - H. D. Bui
  sources:
  - id: paper-byline
    archive_path: packing/resources/papers/square-packing-x06-wasted-area-2508.04603.raw.md
    locator: The opening author byline names Hong Duc Bui.
    url: https://arxiv.org/abs/2508.04603
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The squarepacker k2-minus-c-upper entries credit Bui; the source note identifies H.
      D. Bui and arXiv:2508.04603v2.
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
  - field: /aliases/1
    sources:
    - bibliography
    - paper-byline
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
