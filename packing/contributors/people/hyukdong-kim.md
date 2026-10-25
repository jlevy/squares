---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: hyukdong-kim
  display_name: Hyukdong Kim
  surname: Kim
  real_name: Hyukdong Kim
  aliases: [Kim, HyukdongKim]
  links:
    - kind: github
      url: https://github.com/HyukdongKim
      handle: HyukdongKim
  sources:
    - id: source-intake
      archive_path: packing/resources/web/hyukdongkim-exact-forms-2026-10-25/README.md
      locator: Source and Credit retains issue 804's credit name, “Hyukdong Kim (ORCID 0000-0001-5787-8066)”, filed by the GitHub account HyukdongKim; acquisition/issue-804.json keeps the issue as read.
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: '[Kim exact forms 2026-10-25] credits Kim; credited_names maps Hyukdong Kim to Kim.'
  provenance:
    - field: /display_name
      sources: [bibliography, source-intake]
    - field: /real_name
      sources: [source-intake]
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
