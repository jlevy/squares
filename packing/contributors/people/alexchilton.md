---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: alexchilton
  display_name: 'alexchilton'
  aliases: [alexchilton]
  sources:
    - id: source-credit
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/receipts/claim-map.json
      locator: 'The others list keeps the credit certified_bounds.json states at 964ee2b at 11 counts, "alexchilton, Kaggle notebook "fault-line-dp-basin-hopping-lb-22-3747" run 361412241", with the notebook kaggle.com/code/alexchilton/fault-line-dp-basin-hopping-lb-22-3747 the manifest names. The source gives the handle and no other name.'
    - id: public-profile
      url: https://www.kaggle.com/alexchilton
      locator: 'Kaggle public profile page of the account alexchilton, read 2026-10-24T13:52Z by the stage 1 triage (think-lyf9): its title is "alex chilton". Recorded as the name the profile states; it is not taken as the credit name, and whether the account is that person is asked of the publisher (think-lyf9).'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [alexchilton fault-line 2026-10-23] entry uses the author label alexchilton, the handle, since the source gives no other name.'
  provenance:
    - field: /display_name
      sources: [source-credit, bibliography]
    - field: /aliases
      sources: [source-credit, bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
