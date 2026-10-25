---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: vladislav-lavrentev
  display_name: 'Vladislav Lavrentev'
  surname: Lavrentev
  real_name: 'Vladislav Lavrentev'
  aliases: [Lavrentev, lightningv08]
  sources:
    - id: source-credit
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/receipts/claim-map.json
      locator: 'The others list keeps the credits certified_bounds.json states at 964ee2b, "Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11" at 2 counts and "Vladislav Lavrentev (lightningv08), Kaggle notebook "squares-in-squares-cuda-packing-search" run 361589987" at 7, with the notebook kaggle.com/code/lightningv08/squares-in-squares-cuda-packing-search the manifest names.'
    - id: source-intake
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/README.md
      locator: 'The Notebook Rows section credits Vladislav Lavrentev (lightningv08) by name, as the source does, for the rows of both runs of his notebook; Credit and Lineage names him for the 253 rows Couzo refined from his packings.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [Lavrentev CUDA Packing Search v11 2026-10-23] and [Lavrentev CUDA Packing Search run 361589987 2026-10-23] entries use the author label Lavrentev; credited_names maps Vladislav Lavrentev to Lavrentev.'
  provenance:
    - field: /display_name
      sources: [source-credit, source-intake]
    - field: /real_name
      sources: [source-credit, source-intake]
    - field: /surname
      sources: [bibliography]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [source-credit]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
