---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: manasseh-ahmed
  display_name: Manasseh Ahmed
  surname: Ahmed
  real_name: Manasseh Ahmed
  aliases:
    - Ahmed
    - Mannaseh Ahmed
    - Queuingtheorydotcom
    - ManassehA06
    - MathCompSciFTW
    - Square Packing Fan
    - '@Queuingtheorydotcom'
    - '@ManassehA06'
    - '@MathCompSciFTW'
  display_aliases: [MathCompSciFTW, Square Packing Fan]
  links:
    - kind: github
      url: https://github.com/Queuingtheorydotcom
      handle: Queuingtheorydotcom
    - kind: twitter
      url: https://x.com/ManassehA06
      handle: ManassehA06
  sources:
    - id: owner-confirmation
      archive_path: attribution.md
      locator: 'Decisions and Exceptions, the Manasseh Ahmed row: the owner’s confirmation that @ManassehA06, Queuingtheorydotcom and Manasseh Ahmed are one person, credited by his real name.'
    - id: n17-credits
      archive_path: packing/resources/web/kleddamag-n17-candidate-2026-10-12/README.md
      locator: 'Source and Credit, the Human credit row: the n = 17 edition’s CREDITS.md credits “Manasseh Ahmed’s 11SquaresOptimal” for the proof shape.'
    - id: primary-byline
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/11SquaresFormalized/ACKNOWLEDGEMENTS.md
      locator: 'Acknowledgements names @Queuingtheorydotcom for the underlying proof and integration; bibliography explicitly identifies its Ahmed attribution.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
    - id: announcement-account
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/announcement/tweet-2107508501610217640.json
      url: https://x.com/ManassehA06/status/2107508501610217640
      locator: 'user.id_str is 1499452114313129988; user.screen_name is ManassehA06; user.name is Square Packing Fan.'
    - id: earlier-announcement-account
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/announcement/tweet-2104772485816168618.json
      url: https://x.com/ManassehA06/status/2104772485816168618
      locator: 'The September announcement has the same user.id_str, 1499452114313129988, as the October announcement.'
    - id: intake-identity
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md
      locator: 'Opening identity account and Source and Pin table record the owner-confirmed GitHub/X join, former MathCompSciFTW handle, and curated Mannaseh Ahmed spelling; primary receipts expose only the account display name.'
  provenance:
    - field: /surname
      sources: [bibliography]
    - field: /display_name
      sources: [owner-confirmation, n17-credits]
    - field: /real_name
      sources: [owner-confirmation, n17-credits]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [intake-identity]
    - field: /aliases/2
      sources: [primary-byline]
    - field: /aliases/3
      sources: [announcement-account]
    - field: /aliases/4
      sources: [intake-identity, earlier-announcement-account]
    - field: /aliases/5
      sources: [announcement-account]
    - field: /aliases/6
      sources: [primary-byline]
    - field: /aliases/7
      sources: [announcement-account]
    - field: /aliases/8
      sources: [intake-identity, earlier-announcement-account]
    - field: /links/0
      sources: [primary-byline, intake-identity]
    - field: /links/1
      sources: [announcement-account, intake-identity]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
