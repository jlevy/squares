---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: nate-chaoweeraprasit
  display_name: Nate Chaoweeraprasit
  surname: Chaoweeraprasit
  real_name: Nate Chaoweeraprasit
  aliases: [Chaoweeraprasit, natcha, thatennine, itsnaka, 'Nate Chaoweeraprasit (itsnaka)']
  display_aliases: [natcha]
  links:
    - kind: github
      url: https://github.com/itsnaka
      handle: itsnaka
    - kind: twitter
      url: https://x.com/thatennine
      handle: thatennine
  sources:
    - id: source-intake
      archive_path: packing/resources/web/squish-401-2026-10-07/README.md
      url: https://github.com/jlevy/squares/issues/401
      locator: 'Opening paragraph names Nate Chaoweeraprasit (itsnaka); Source and Credit records his human credit and the itsnaka/squish-certs repository.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'credited_names maps Nate Chaoweeraprasit and Nate Chaoweeraprasit (itsnaka) to Chaoweeraprasit; SQUISH entries retain the surname author label.'
    - id: owner-confirmation
      archive_path: attribution.md
      locator: 'Decisions and Exceptions, the Nate Chaoweeraprasit row dated 2026-10-20: the owner confirms the real name behind natcha and the X account https://x.com/thatennine. The account was not independently inspected.'
  provenance:
    - field: /display_name
      sources: [source-intake, owner-confirmation]
    - field: /real_name
      sources: [source-intake, owner-confirmation]
    - field: /surname
      sources: [bibliography, owner-confirmation]
    - field: /aliases/0
      sources: [bibliography]
    - field: /aliases/1
      sources: [owner-confirmation]
    - field: /aliases/2
      sources: [owner-confirmation]
    - field: /aliases/3
      sources: [source-intake, bibliography]
    - field: /aliases/4
      sources: [source-intake, bibliography]
    - field: /links/0
      sources: [source-intake]
    - field: /links/1
      sources: [owner-confirmation]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
