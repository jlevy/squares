---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: yohei-nakajima
  display_name: Yohei Nakajima
  surname: Nakajima
  real_name: Yohei Nakajima
  aliases:
  - Nakajima
  - Y. Nakajima
  sources:
  - id: source-intake
    archive_path: packing/resources/web/dostashev-records-2026-10-11/README.md
    locator: The methods credit names Yohei Nakajima for the soft-to-rigid method; the retained
      source README reference 8 identifies Y. Nakajima and links this project.
    url: https://github.com/yoheinakajima/soft-to-rigid-packing
  - id: bibliography
    archive_path: packing/resources/bibliography.yaml
    locator: The Ostashev record and composition entries credit Nakajima for the soft-to-rigid method
      identified in their retained source.
  provenance:
  - field: /display_name
    sources:
    - source-intake
  - field: /real_name
    sources:
    - source-intake
  - field: /surname
    sources:
    - bibliography
  - field: /aliases/0
    sources:
    - bibliography
    - source-intake
  - field: /aliases/1
    sources:
    - bibliography
    - source-intake
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
