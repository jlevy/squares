// The archive's actual facets, disclosed cards, centered controls and shared meters.
/** @param {{ meters?: string, chooser?: string, choice?: string, overrideChooser?: boolean } | null} options */
async (options) => {
  const { meters = "", chooser = "", choice = "", overrideChooser = false } = options ?? {};
  const override = document.createElement("style");
  if (overrideChooser) {
    override.textContent = ".site-news-filters .site-tabs button { font-size: 40px !important; }";
    document.head.append(override);
  }
  if (chooser) {
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  }
  /** @param {Element | null} element */
  const appearance = (element) => {
    if (!element) {
      return null;
    }
    const style = getComputedStyle(element);
    return Object.fromEntries(
      [
        "font-family",
        "font-size",
        "font-weight",
        "line-height",
        "letter-spacing",
        "color",
        "background-color",
        "padding-top",
        "padding-right",
        "padding-bottom",
        "padding-left",
        "border-top-width",
        "border-bottom-width",
        "border-radius",
        "outline-color",
        "outline-style",
        "outline-width",
        "transition-property",
        "transition-duration",
        "transition-timing-function",
      ].map((name) => [name, style.getPropertyValue(name)]),
    );
  };
  const group = chooser ? document.querySelector(chooser) : null;
  const option = choice ? (group?.querySelector(choice) ?? null) : null;
  const count = document.querySelector(".site-table-tools .site-count");
  const countRow = count?.closest(".site-table-tools");
  const firstCard = document.querySelector("[data-news-day]:not([hidden])");

  const controls = document.querySelector("[data-news-filters]");
  const specimen = document.createElement("div");
  specimen.innerHTML = meters;
  document.querySelector(".site-page")?.append(specimen);
  const samples = [...specimen.querySelectorAll(".site-significance")].map((meter) => {
    const style = getComputedStyle(meter);
    const bars = [...meter.querySelectorAll(".site-significance-bar")];
    return {
      level: Number(meter.getAttribute("data-level")),
      label: meter.getAttribute("aria-label"),
      width: meter.getBoundingClientRect().width,
      font: Number.parseFloat(style.fontSize),
      border: Number.parseFloat(style.borderTopWidth),
      filled: bars.filter((bar) => bar.getAttribute("data-filled") === "true").length,
      bars: bars.map((bar) => ({
        height: bar.getBoundingClientRect().height,
        width: bar.getBoundingClientRect().width,
        fill: getComputedStyle(bar).backgroundColor,
        border: Number.parseFloat(getComputedStyle(bar).borderTopWidth),
        filled: bar.getAttribute("data-filled") === "true",
      })),
    };
  });
  specimen.remove();
  const result = {
    chooser: group
      ? {
          appearance: appearance(option),
          role: group.getAttribute("role"),
          focus_visible: option?.matches(":focus-visible"),
          selected: option?.getAttribute("aria-selected"),
          pressed: option?.getAttribute("aria-pressed"),
          border: getComputedStyle(group).borderTopWidth,
          gap: getComputedStyle(group).gap,
          height: option?.getBoundingClientRect().height,
        }
      : null,
    count_style: appearance(count),
    count_right_gap:
      count && countRow
        ? countRow.getBoundingClientRect().right - count.getBoundingClientRect().right
        : null,
    count_card_right_gap:
      count && firstCard
        ? firstCard.getBoundingClientRect().right - count.getBoundingClientRect().right
        : null,
    count_above_cards:
      count && firstCard
        ? count.getBoundingClientRect().bottom < firstCard.getBoundingClientRect().top
        : null,
    groups: [...document.querySelectorAll("[data-news-filters] [role=group]")].map((item) => ({
      name: document.getElementById(item.getAttribute("aria-labelledby") || "")?.textContent,
      hidden_legend: document
        .getElementById(item.getAttribute("aria-labelledby") || "")
        ?.classList.contains("site-visually-hidden"),
      tabs: item.querySelectorAll("[role=tab]").length,
    })),
    scores: [
      ...(controls?.querySelectorAll('button[data-news-score][aria-pressed="true"]') ?? []),
    ].map((button) => button.getAttribute("data-news-score")),
    topics: [
      ...(controls?.querySelectorAll('button[data-news-topic][aria-pressed="true"]') ?? []),
    ].map((button) => button.getAttribute("data-news-topic")),
    controls_hidden: controls instanceof HTMLElement && controls.hidden,
    count: controls?.querySelector("[data-news-count]")?.textContent,
    empty:
      controls?.querySelector("[data-news-empty]") instanceof HTMLElement &&
      !controls.querySelector("[data-news-empty]")?.hasAttribute("hidden"),
    cards: [...document.querySelectorAll("[data-news-day]")].map((card) => {
      const box = card.getBoundingClientRect();
      const button = card.querySelector(".site-news-expand");
      const buttonBox = button?.getBoundingClientRect();
      const body = card.querySelector(".site-news-body");
      return {
        id: card.id,
        visible: card.getClientRects().length > 0,
        score: Number(card.getAttribute("data-news-score")),
        topics: (card.getAttribute("data-news-topics") || "").split(" ").filter(Boolean),
        expanded: button?.getAttribute("aria-expanded"),
        button_hidden: button instanceof HTMLButtonElement && button.hidden,
        center_offset: buttonBox
          ? (buttonBox.left + buttonBox.right - box.left - box.right) / 2
          : null,
        full: body instanceof HTMLElement && body.clientHeight >= body.scrollHeight - 1,
      };
    }),
    samples,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
  override.remove();
  return result;
};
