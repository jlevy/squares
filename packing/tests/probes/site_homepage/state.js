// The homepage's live tile state and computed typography/card placement.
async () => {
  await document.fonts.ready;
  const cells = document.getElementById("homepage-atlas-cells");
  const toggle = document.querySelector("[data-homepage-atlas-toggle]");
  const chevron = toggle?.querySelector(".site-icon-arrow");
  const status = document.querySelector("[data-homepage-atlas-status]");
  const scope = document.querySelector(".site-recent-scope");
  const allTiles = [...(cells?.querySelectorAll("a.site-atlas-cell") ?? [])];
  const tiles = allTiles.filter((tile) => tile.getClientRects().length > 0);
  const legend = document.querySelector(".site-rung-legend");
  const cardLabel = document.querySelector(".site-card-label");
  /** @param {Element} element */
  const titleStyle = (element) => {
    const style = getComputedStyle(element);
    return {
      family: style.fontFamily,
      size: style.fontSize,
      weight: style.fontWeight,
      style: style.fontStyle,
      transform: style.textTransform,
    };
  };
  const mainTitle = document.getElementById("the-problem");
  /** @param {string} id */
  const mediaLinks = (id) => {
    const links = [];
    for (
      let sibling = document.getElementById(id)?.nextElementSibling;
      sibling && !sibling.matches("h1, h2, h3, h4, h5, h6");
      sibling = sibling.nextElementSibling
    ) {
      for (const link of sibling.querySelectorAll("a.site-card-link")) {
        links.push(link.getAttribute("href"));
      }
    }
    return links;
  };
  const solos = [...document.querySelectorAll(".site-project-card, .site-cards")].flatMap((row) => {
    const cards = row.querySelectorAll(":scope > .site-card");
    const card = cards[0];
    if (cards.length !== 1 || !card) {
      return [];
    }
    const parent = row.matches(".site-project-card") ? row.parentElement : row;
    if (!parent) {
      return [];
    }
    const frame = parent.getBoundingClientRect();
    const box = card.getBoundingClientRect();
    return [
      {
        label: card.textContent?.trim(),
        center_offset: (box.left + box.right - frame.left - frame.right) / 2,
      },
    ];
  });
  const frame = cells?.getBoundingClientRect();
  const occupied = tiles.map((tile) => tile.getBoundingClientRect());
  const left = Math.min(...occupied.map((box) => box.left));
  const right = Math.max(...occupied.map((box) => box.right));
  return {
    centering: frame
      ? {
          width: right - left,
          frame_width: frame.width,
          offset: (left + right - frame.left - frame.right) / 2,
          fits: right - left <= frame.width + 0.5,
          page_overflow:
            document.documentElement.scrollWidth - document.documentElement.clientWidth,
        }
      : null,
    cases: tiles.map((tile) => Number(tile.getAttribute("data-case"))),
    prepared_cases: allTiles.length,
    images: {
      decoded: allTiles.filter((tile) => tile.querySelector('img[data-atlas-image-state="ready"]'))
        .length,
      loaded: allTiles.filter((tile) => {
        const image = tile.querySelector("img");
        return image?.complete && image.naturalWidth > 0;
      }).length,
      failed: cells?.querySelectorAll('img[data-atlas-image-state="failed"]').length ?? 0,
    },
    control_groups: [...document.querySelectorAll("[data-atlas-controls] [role=tablist]")].map(
      (list) => list.getAttribute("aria-label"),
    ),
    atlas_legend: document.querySelector("[data-atlas-legend]") !== null,
    control_type: [
      ...document.querySelectorAll("[data-atlas-controls] [role=tab], [data-atlas-toggle]"),
    ].map((button) => {
      const style = getComputedStyle(button);
      const reference = button.matches('[role="tab"]')
        ? document.querySelector(".site-nav")
        : status;
      return {
        size: Number.parseFloat(style.fontSize),
        base: reference ? Number.parseFloat(getComputedStyle(reference).fontSize) : null,
      };
    }),
    case_names: Object.fromEntries(
      tiles.map((tile) => [tile.getAttribute("data-case"), tile.getAttribute("aria-label")]),
    ),
    number_fonts: [
      ...new Set(
        tiles.map((tile) => {
          const number = tile.querySelector(".site-atlas-n");
          return number ? getComputedStyle(number).fontFamily : null;
        }),
      ),
    ],
    sans_family: cardLabel ? getComputedStyle(cardLabel).fontFamily : null,
    mark_errors: tiles.flatMap((tile) => {
      const number = tile.querySelector(".site-atlas-n");
      const star = number?.querySelector(".site-star");
      if (!number) {
        return [tile.getAttribute("data-case")];
      }
      const numberBox = number.getBoundingClientRect();
      const starBox = star?.getBoundingClientRect();
      const tileBox = tile.getBoundingClientRect();
      return numberBox.left >= tileBox.left &&
        numberBox.right <= tileBox.right &&
        (!starBox || (starBox.left > numberBox.right && starBox.right <= tileBox.right))
        ? []
        : [
            `Case ${tile.getAttribute("data-case")}: number ${numberBox.left}..${numberBox.right}; ` +
              `star ${starBox ? `${starBox.left}..${starBox.right}` : "none"}; ` +
              `tile ${tileBox.left}..${tileBox.right}`,
          ];
    }),
    raw_markup: cells?.querySelectorAll("pre, code").length ?? 0,
    star_cases: allTiles
      .filter((tile) => tile.querySelector(".site-star"))
      .map((tile) => Number(tile.getAttribute("data-case"))),
    label_errors: allTiles.flatMap((tile) => {
      const n = tile.getAttribute("data-case");
      const label = tile.querySelector(".site-atlas-n");
      return label?.firstChild?.textContent?.trim() === n &&
        label.querySelectorAll(":scope > :not(.site-star)").length === 0 &&
        tile.querySelectorAll("img").length === 1
        ? []
        : [n];
    }),
    view: cells?.parentElement?.getAttribute("data-atlas-view"),
    stage: Number(cells?.parentElement?.getAttribute("data-atlas-count")),
    cells_role: cells?.getAttribute("role"),
    visible_cases: tiles.filter((tile) => tile.getClientRects().length > 0).length,
    drawings: {
      cards: tiles.length,
      rows: [...(cells?.querySelectorAll(".site-atlas-row") ?? [])]
        .filter((row) => row.getClientRects().length > 0)
        .map((row) => Number(row.getAttribute("data-atlas-row"))),
      size: cells?.parentElement?.getAttribute("data-atlas-size"),
      scale: cells?.parentElement?.getAttribute("data-atlas-scale"),
    },
    busy: cells?.getAttribute("aria-busy"),
    toggle:
      toggle instanceof HTMLButtonElement
        ? {
            disabled: toggle.disabled,
            expanded: toggle.getAttribute("aria-expanded"),
            controls: toggle.getAttribute("aria-controls"),
            label: toggle.textContent?.trim(),
            name: toggle.getAttribute("aria-label"),
            arrow: chevron?.getAttribute("data-arrow"),
            arrow_hidden: chevron?.getAttribute("aria-hidden"),
            arrow_mask: chevron ? getComputedStyle(chevron).maskImage : null,
            arrow_width: chevron?.getBoundingClientRect().width,
            focused: document.activeElement === toggle,
          }
        : null,
    status:
      status instanceof HTMLElement
        ? {
            role: status.getAttribute("role"),
            text: status.textContent?.trim(),
            hidden: status.hidden,
          }
        : null,
    headings: [...document.querySelectorAll("h2.site-title")].map((heading) => heading.id),
    main_titles: [...document.querySelectorAll("h1.site-title")].map((heading) => heading.id),
    lower_headings: document.querySelectorAll("h3, h4, h5, h6").length,
    main_title_style: mainTitle ? titleStyle(mainTitle) : null,
    h1_spacing: [...document.querySelectorAll("h1.site-title")].map((heading) => ({
      id: heading.id,
      above: Number.parseFloat(getComputedStyle(heading).marginBlockStart),
    })),
    section_title_styles: [...document.querySelectorAll("h1.site-title, h2.site-title")]
      .filter((heading) => heading !== mainTitle)
      .map(titleStyle),
    recent_title: document.getElementById("recent-results")?.textContent?.trim(),
    media: { visuals: mediaLinks("visuals") },
    legacy_pdf_anchor: document.getElementById("pdfs-and-videos") !== null,
    scope_present: scope !== null,
    legend_present: legend !== null,
    actions: [...document.querySelectorAll(".site-action")].map((action) => {
      const style = getComputedStyle(action);
      return {
        label: action.textContent?.trim(),
        family: style.fontFamily,
        transform: style.textTransform,
      };
    }),
    solo_cards: solos,
  };
};
