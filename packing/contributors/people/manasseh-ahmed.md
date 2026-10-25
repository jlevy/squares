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
      url: https://github.com/Kleddamag/the-seventeenth-square-candidate/blob/653b9589d0f8a152f01adc56b1d48ba53d49abc3/CREDITS.md
      locator: 'CREDITS.md of the n = 17 edition at 653b958, line 28: “Manasseh Ahmed (github.com/Queuingtheorydotcom), 11SquaresOptimal (github.com/Queuingtheorydotcom/11SquaresOptimal): the proof shape”. The packet keeps no upstream bytes; its acquisition/upstream-subtree.sha256 binds the file at SHA-256 fab3b10b36da9842d0f6168ff7b080da50449028d1d116d62995326a5eeda9c8, and its Source and Credit table summarizes the credit in the Human credit row.'
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
    - id: n12-publication
      archive_path: packing/resources/web/jatloe-n12-lean-2026-10-16/receipts/announcement/tweet-2113097037306569124.json
      url: https://x.com/ManassehA06/status/2113097037306569124
      locator: 'The announcement of the twelve-square formalization, 22 October 2026: user.id_str 1499452114313129988, the account of the n = 11 announcements, screen_name ManassehA06. Every commit of Queuingtheorydotcom/Jatloe12SquaresFormalized, which the jatloe-n12-lean-2026-10-16 packet pins, is by Queuingtheorydotcom.'
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
      sources: [primary-byline, n17-credits]
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
      sources: [primary-byline, intake-identity, n17-credits]
    - field: /links/1
      sources: [announcement-account, intake-identity]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
