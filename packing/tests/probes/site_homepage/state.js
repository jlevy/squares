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
  const svg = tiles[0]?.querySelector("[data-homepage-atlas-svg]");
  const cards = tiles.flatMap((tile) => [
    ...tile.querySelectorAll('g[data-feature="packing-card"]'),
  ]);
  const legend = document.querySelector(".site-rung-legend");
  const heading = legend?.querySelector(".site-rung-legend-heading");
  const table = document.querySelector("table.site-results");
  const cardLabel = document.querySelector(".site-card-label");
  const box = legend?.getBoundingClientRect();
  const parent = legend?.parentElement?.getBoundingClientRect();
  const headingStyle = heading ? getComputedStyle(heading) : null;
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
  const headingRange = document.createRange();
  if (heading) {
    headingRange.selectNodeContents(heading);
  }
  const titleBox = heading ? headingRange.getBoundingClientRect() : null;
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
  return {
    cases: tiles.map((tile) => Number(tile.getAttribute("data-case"))),
    prepared_cases: allTiles.length,
    raw_markup: cells?.querySelectorAll("pre, code").length ?? 0,
    star_cases: allTiles
      .filter((tile) => tile.querySelector('[data-feature="legend-star"]'))
      .map((tile) => Number(tile.getAttribute("data-case"))),
    label_errors: allTiles.flatMap((tile) => {
      const n = tile.getAttribute("data-case");
      const texts = [...tile.querySelectorAll("text")];
      return texts.length === 1 &&
        texts[0]?.getAttribute("data-feature") === "packing-label" &&
        texts[0]?.textContent?.trim() === n &&
        tile.querySelectorAll('[data-feature="evidence-badge"]').length === 0
        ? []
        : [n];
    }),
    view: cells?.parentElement?.getAttribute("data-atlas-view"),
    stage: Number(cells?.parentElement?.getAttribute("data-atlas-count")),
    cells_role: cells?.getAttribute("role"),
    visible_cases: tiles.filter((tile) => tile.getClientRects().length > 0).length,
    svg: {
      cards: cards.length,
      rows: [...new Set(cards.map((card) => Number(card.getAttribute("data-row"))))],
      viewbox: svg?.getAttribute("viewBox"),
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
    section_title_styles: [...document.querySelectorAll("h1.site-title, h2.site-title")]
      .filter((heading) => heading !== mainTitle)
      .map(titleStyle),
    recent_title: document.getElementById("recent-results")?.textContent?.trim(),
    media: { pdfs: mediaLinks("pdfs"), video: mediaLinks("video") },
    legacy_pdf_anchor: document.getElementById("pdfs-and-videos") !== null,
    scope_present: scope !== null,
    legend:
      legend instanceof HTMLElement && box && parent && headingStyle
        ? {
            title: heading?.textContent?.trim(),
            transform: headingStyle.textTransform,
            style: headingStyle.fontStyle,
            family: headingStyle.fontFamily,
            size: headingStyle.fontSize,
            card_label_size: cardLabel ? getComputedStyle(cardLabel).fontSize : null,
            entries: [...legend.querySelectorAll(".site-significance-label, .site-chip")].map(
              (entry) => entry.textContent?.trim(),
            ),
            paragraphs: legend.querySelectorAll("p").length,
            helper_text: legend.textContent?.includes("What each rung means"),
            rows: [...legend.querySelectorAll(":scope > p")].map((line) => {
              const icons = line.querySelector(".site-rung-legend-icons");
              const name = line.querySelector(".site-rung-legend-name");
              const iconBox = icons?.getBoundingClientRect();
              const nameBox = name?.getBoundingClientRect();
              return {
                icon_left: iconBox?.left,
                icon_right: iconBox?.right,
                label_left: nameBox?.left,
                center_offset:
                  iconBox && nameBox
                    ? (iconBox.top + iconBox.bottom - nameBox.top - nameBox.bottom) / 2
                    : null,
              };
            }),
            lines: [...legend.querySelectorAll(":scope > p")].map((line) =>
              [...line.querySelectorAll(".site-rung-legend-name")].map((name) =>
                name.textContent?.trim(),
              ),
            ),
            title_align: headingStyle.textAlign,
            title_center_offset: titleBox
              ? (titleBox.left + titleBox.right - box.left - box.right) / 2
              : null,
            star: legend.querySelector(".site-star") !== null,
            detail: legend.getAttribute("href"),
            shared_card: legend.matches("a.site-card.site-card-link"),
            destination_kind: legend.getAttribute("data-go"),
            nested_links: legend.querySelectorAll("a").length,
            accessible_name: legend.getAttribute("aria-label"),
            center_offset: (box.left + box.right - parent.left - parent.right) / 2,
            width: box.width,
            left: box.left,
            right: box.right,
            rem: Number.parseFloat(getComputedStyle(document.documentElement).fontSize),
            table_width: table?.getBoundingClientRect().width,
            scroll_width: legend.scrollWidth,
            client_width: legend.clientWidth,
          }
        : null,
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
