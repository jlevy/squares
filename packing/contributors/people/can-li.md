---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: can-li
  display_name: Can Li
  surname: Li
  real_name: Can Li
  aliases: [Li, Li Can]
  links:
    - kind: publication
      url: https://doi.org/10.5281/zenodo.23038546
  sources:
    - id: source-intake
      archive_path: packing/resources/web/wang-li-n11-2026-09-29/README.md
      locator: Provenance table records creators Wang, Ke and Li, Can and DOI 10.5281/zenodo.23038546; opening gives Wang Ke and Li Can.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Wang Li n11 2026] records the author credit Li. credited_names maps Can Li to Li.'
  provenance:
    - field: /display_name
      sources: [bibliography, source-intake]
    - field: /real_name
      sources: [bibliography, source-intake]
    - field: /surname
      sources: [bibliography]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [source-intake]
    - field: /links/0
      sources: [source-intake]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
