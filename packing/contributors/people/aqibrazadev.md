---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: aqibrazadev
  display_name: 'aqibrazadev'
  aliases: [aqibrazadev]
  sources:
    - id: source-credit
      archive_path: packing/resources/web/couzo-issue763-2026-10-23/receipts/claim-map.json
      locator: 'The others list keeps the credit certified_bounds.json states at 964ee2b at 9 counts, "aqibrazadev, Kaggle notebook "squares-in-squares-top-lb-blending-visualization" run 361516058", with the notebook kaggle.com/code/aqibrazadev/squares-in-squares-top-lb-blending-visualization the manifest names. The source gives the handle and no other name.'
    - id: public-profile
      url: https://www.kaggle.com/aqibrazadev
      locator: 'Kaggle public profile page of the account aqibrazadev, read 2026-10-24T13:52Z by the stage 1 triage (think-lyf9): its title is "Aqib Raza". Recorded as the name the profile states; it is not taken as the credit name, and whether the account is that person is asked of the publisher (think-lyf9).'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'The [aqibrazadev blending 2026-10-23] entry uses the author label aqibrazadev, the handle, since the source gives no other name.'
  provenance:
    - field: /display_name
      sources: [source-credit, bibliography]
    - field: /aliases
      sources: [source-credit, bibliography]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
