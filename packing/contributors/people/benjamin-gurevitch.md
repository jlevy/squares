---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: benjamin-gurevitch
  display_name: Benjamin Gurevitch
  surname: Gurevitch
  real_name: Benjamin Gurevitch
  aliases:
  - Gurevitch
  - Benjamin-Gurevitch
  links:
  - kind: github
    url: https://github.com/Benjamin-Gurevitch
    handle: Benjamin-Gurevitch
  sources:
  - id: formalization-acknowledgment
    archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md
    url: https://github.com/Queuingtheorydotcom/11SquaresFormalized/blob/cdc746ed907d258057c283aeb6d077cb2c27e349/ACKNOWLEDGEMENTS.md
    locator: Line 7 names Benjamin Gurevitch (@Benjamin-Gurevitch), links the GitHub account, and credits help with
      T03 and its returned-case formalization.
  - id: public-profile
    url: https://api.github.com/users/Benjamin-Gurevitch
    locator: 'Public GitHub profile checked 2026-10-21: login Benjamin-Gurevitch, name Benjamin Gurevitch, type
      User.'
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: '[Ahmed 11SquaresFormalized 2026], authors[3], prints Gurevitch; the note names Benjamin Gurevitch
      and his T03 role.'
  provenance:
  - field: /display_name
    sources:
    - formalization-acknowledgment
    - public-profile
  - field: /surname
    sources:
    - formalization-acknowledgment
    - bibliography
  - field: /real_name
    sources:
    - formalization-acknowledgment
    - public-profile
  - field: /aliases
    sources:
    - formalization-acknowledgment
    - bibliography
  - field: /links
    sources:
    - formalization-acknowledgment
    - public-profile
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
