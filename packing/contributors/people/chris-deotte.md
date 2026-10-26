---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: chris-deotte
  display_name: 'Chris Deotte'
  surname: Deotte
  real_name: 'Chris Deotte'
  aliases: [Deotte]
  sources:
    - id: source-credit
      archive_path: packing/resources/web/evand-n299-2026-10-26/acquisition/declaration.json
      locator: 'The third claim quotes issue 824''s credit section: a fault-line composition by Evan Daniel''s "independent implementation of Chris Deotte''s multi-gadget fault DP, described in his Kaggle notebooks", and the request that Chris Deotte be credited "for the method and for the start", the s(334) packing in his public Kaggle notebook "squares-in-squares-ftmc-milp-refill-22-311".'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [Daniel n299 2026-10-26] entry credits Daniel after Deotte; credited_names maps Chris Deotte to Deotte.'
  provenance:
    - field: /display_name
      sources: [source-credit]
    - field: /real_name
      sources: [source-credit]
    - field: /surname
      sources: [bibliography]
    - field: /aliases/0
      sources: [bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
