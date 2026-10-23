---
softschema:
  contract: packing.squares:Contributor/v1
  schema: ../schemas/contributor.schema.yaml
  envelope: contributor
  status: enforced
contributor:
  id: joshua-levy
  display_name: 'Joshua Levy'
  surname: Levy
  real_name: 'Joshua Levy'
  aliases: [Levy, jlevy, ojoshe, '@ojoshe']
  links:
    - kind: github
      url: https://github.com/jlevy
      handle: jlevy
    - kind: twitter
      url: https://x.com/ojoshe
      handle: ojoshe
  sources:
    - id: primary-byline
      archive_path: LICENSE
      locator: 'Copyright notices and required attribution name Joshua Levy.'
    - id: bibliography
      archive_path: packing/resources/bibliography.yaml
      locator: 'Source author, credit and credited_names fields retain the printed attribution labels.'
    - id: announcement-account
      archive_path: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/announcement/tweet-2107513739222380935.json
      url: https://x.com/ojoshe/status/2107513739222380935
      locator: 'user.name is Joshua Levy, user.screen_name is ojoshe, and user.id_str is 2246453394.'
    - id: daniel-343-credit
      archive_path: packing/resources/web/evand-n343-sweep-2026-10-20/source/CREDITS.md
      url: https://github.com/evand/square-packing/blob/88385abc95ab25d520302282d1946cbb07bc9cf3/CREDITS.md
      locator: 'Parallel 2026 work explicitly names Joshua Levy (jlevy), the Squares Project; this source supplies the personal identity behind the new Daniel n343 credit, unlike generic collective-project labels.'
    - id: daniel-regularized-credit
      archive_path: packing/resources/web/evand-regularized-2026-10-20/source/CREDITS.md
      url: https://github.com/evand/square-packing/blob/0075967bace18a3deabcc0baa64c2fb294fc80a0/CREDITS.md
      locator: 'Parallel 2026 work explicitly names Joshua Levy (jlevy), the Squares Project; this retained source supplies the personal identity behind the T-225 bibliography credit.'
    - id: owner-credit-links-2026-10-22
      archive_path: packing/contributors/reviews/2026-10-22-credit-link-audit.md
      locator: 'Owner Confirmation and Source Boundaries: the owner confirms the exact curated Levy labels as personal profile joins; upstream collective wording and source roles remain unchanged.'
    - id: daniel-n183-credit
      archive_path: packing/resources/web/evand-n183-subgrid-2026-10-19/source/CREDITS.md
      locator: 'Parallel 2026 work explicitly names Joshua Levy (jlevy), the Squares Project. The bibliography separately records register seed data as the role for the n183 source.'
  provenance:
    - field: /surname
      sources: [primary-byline, bibliography]
    - field: /display_name
      sources: [primary-byline]
    - field: /real_name
      sources: [primary-byline]
    - field: /aliases/0
      sources: [primary-byline, bibliography]
    - field: /aliases/1
      sources: [primary-byline]
    - field: /aliases/2
      sources: [announcement-account]
    - field: /aliases/3
      sources: [announcement-account]
    - field: /links/0
      sources: [primary-byline]
    - field: /links/1
      sources: [announcement-account]
---
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
