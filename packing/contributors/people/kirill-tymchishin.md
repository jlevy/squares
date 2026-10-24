---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: kirill-tymchishin
  display_name: 'Kirill Tymchishin'
  surname: Tymchishin
  real_name: 'Kirill Tymchishin'
  aliases: [Tymchishin, kirilltym]
  sources:
    - id: source-credit
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/receipts/claim-map.json
      locator: 'The others list keeps the credits certified_bounds.json states at 964ee2b, "Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3" at 37 counts and "Kirill Tymchishin (kirilltym), Kaggle notebook "22-3662-cpu-cuda-mps-eda-union" run 361576574" at 15, each with the notebook kaggle.com/code/kirilltym/... the manifest names.'
    - id: source-intake
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/README.md
      locator: 'The Notebook Rows section credits Kirill Tymchishin (kirilltym) by name, as the source does, for the rows of his two notebooks.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [Tymchishin CPU Alternating Reclosure v3 2026-10-23] and [Tymchishin 22-3662 2026-10-23] entries use the author label Tymchishin; credited_names maps Kirill Tymchishin to Tymchishin.'
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
